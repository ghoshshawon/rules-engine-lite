import json
from ..db import connection

class EvaluationError(Exception):
   
    def __init__(self, message: str, code: int = 400):
        super().__init__(message)
        self.code = code
def normalize_value(val):
    
    if isinstance(val, str):           
        if val.isdigit():              
            return int(val)
        try:
            return float(val)         
        except ValueError:
            return val.strip()         
    return val                         

class Evaluator:
    def __init__(self, input):
        self.input = input
        
    def get_input(self):
        return self.input    
    
    def evaluate(self):
        conn, cursor = connection()
        data = self.get_input()

        if isinstance(data, str):
            data_dict = json.loads(data)
        else:
            data_dict = data

        cursor.execute("SELECT rule_id, decision, score_delta, reason FROM rules")
        all_rules = cursor.fetchall()
        results = []

        for rule_id, decision, score_delta, reason in all_rules:
            cursor.execute(
                "SELECT condition_type, op, left_path, right_value FROM conditions WHERE rule_id=%s",
                (rule_id,)
            )
            conds = cursor.fetchall()

            passed = True
            trace = []

            for cond in conds:
                condition_type, op, left_path, right_value = cond
                right_value = json.loads(right_value)

                # Extract left_val from nested data
                keys = left_path.split(".")
                left_val = data_dict
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
                left_val = normalize_value(left_val)
                right_value = normalize_value(right_value)
                if left_val is None:
                    result = False
                else:
                    try:
    
                        result = False
                        if op == ">":
                            result = left_val > right_value
                        elif op == "<":
                            result = left_val < right_value
                        elif op == ">=":
                            result = left_val >= right_value
                        elif op == "<=":
                            result = left_val <= right_value
                        elif op == "==":
                            result = left_val == right_value
                        elif op == "!=":
                            result = left_val != right_value
                        elif op == "in":
                            result = left_val in right_value
                        else:
                            print(f" Unknown operator: {op}")
                            continue
                    except Exception as e:
                        print(f" Error comparing {left_val} {op} {right_value}: {e}")
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

           
            if passed:
                results.append({
                    "rule_id": rule_id,
                    "decision": decision,
                    "score": score_delta,
                    "reason": reason,
                    "trace": trace
                })
            else:
                results.append({
                    "rule_id": rule_id,
                    "decision": "approve", 
                    "score": 0,
                    "reason": "No conditions passed",
                    "trace": trace
                })

        conn.close()
        return results