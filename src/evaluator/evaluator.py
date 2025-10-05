import json
from ..db import connection

class EvaluationError(Exception):
   
    def __init__(self, message: str, code: int = 400):
        super().__init__(message)
        self.code = code
                    
class Evaluator:
    def __init__(self, input):
        self.input = input
        
    def get_input(self):
        return self.input    
    
    def evaluate(self):
        conn, cursor = connection()
        data = self.get_input()
        data_dict = json.loads(data) if isinstance(data, str) else data

        cursor.execute("SELECT rule_id, decision, score_delta, reason FROM rules")
        all_rules = cursor.fetchall()

        rule_evaluator = RuleEvaluator(data_dict, cursor)

    
        results = []
        for rule in all_rules:
            result = rule_evaluator.evaluate_rule(*rule)
            results.append(result)

        conn.close()
        return results

class RuleEvaluator:
    def __init__(self, data_dict, cursor):
        self.data_dict = data_dict
        self.cursor = cursor

    def normalize_value(self, val):
        if isinstance(val, str):
            if val.isdigit():
                return int(val)
            try:
                return float(val)
            except ValueError:
                return val.strip()
        return val

    def evaluate_rule(self, rule_id, decision, score_delta, reason):
        self.cursor.execute(
            "SELECT condition_type, op, left_path, right_value FROM conditions WHERE rule_id=%s",
            (rule_id,)
        )
        conds = self.cursor.fetchall()

        passed = True
        trace = []

        for condition_type, op, left_path, right_value in conds:
            
            try:
                right_value = json.loads(right_value)
            except Exception:
                raise EvaluationError(f"Invalid JSON in right_value for rule {rule_id}", code=400)
            
            keys = left_path.split(".")
            left_val = self.data_dict

            try:
                for k in keys:
                    if k.isdigit():
                        k = int(k)
                    left_val = left_val[k]
            except (KeyError, IndexError, TypeError):
                left_val = None

            if left_val in (None, "", [], {}):
                trace.append({
                    "condition": f"{left_path} {op} {right_value}",
                    "passed": False,
                    "note": "Skipped: missing or empty value"
                })
                if condition_type == "all":
                    passed = False
                continue

            left_val = self.normalize_value(left_val)
            right_value = self.normalize_value(right_value)
            if op not in {">", "<", ">=", "<=", "==", "!=", "in"}:
                raise EvaluationError(f"Unknown operator: {op}", code=422)

            try:
                result = {
                    ">": left_val > right_value,
                    "<": left_val < right_value,
                    ">=": left_val >= right_value,
                    "<=": left_val <= right_value,
                    "==": left_val == right_value,
                    "!=": left_val != right_value,
                    "in": left_val in right_value
                }.get(op, False)
            except Exception as e:
                result = False

            trace.append({
                "condition": f"{left_path} {op} {right_value}",
                "passed": result
            })

            if condition_type == "all" and not result:
                passed = False
                break
            if condition_type == "any" and result:
                passed = True

        return {
            "rule_id": rule_id,
            "decision": decision if passed else "approve",
            "score": score_delta if passed else 0,
            "reason": reason if passed else "No conditions passed",
            "trace": trace
        }
