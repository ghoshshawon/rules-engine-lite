import json
from ..db import connection
import pdb;
class Evaluator:
    def __init__(self, input):
        self.input = input
        
    def get_input(self):
        return self.input    
    
    def evaluate(self):
        conn,cursor =connection()
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
            # Evaluate conditions
        passed = True
        trace = []

        for cond in conds:
            condition_type, op, left_path, right_value = cond
            right_value = json.loads(right_value)  

            
            keys = left_path.split(".")
            left_val = data_dict
            try:
                for k in keys:
                    if k.isdigit():
                        k = int(k)
                    left_val = left_val[k]
            except (KeyError, IndexError, TypeError):
                left_val = None  

            # Evaluate operator
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
                raise ValueError(f"Unknown operator: {op}")

            trace.append({
                "condition": f"{left_path} {op} {right_value}",
                "passed": result
            })

            if condition_type == "all" and not result:
                passed = False
            if condition_type == "any" and result:
                passed = True

        # Fetch rule's decision if conditions passed
        cursor.execute("SELECT decision, score_delta, reason FROM rules WHERE rule_id=%s", ('high_amount',))
        rule = cursor.fetchone()
        

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
                "decision": "approve",  # default if not passed
                "score": 0,
                "reason": "No conditions passed",
                "trace": trace
            })

        conn.close()
        return results
                
                
                
            
        
        
        