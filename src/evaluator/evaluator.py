import json
from ..db import connection
class Evaluator:
    def __init__(self, input):
        self.input = input
        
    def get_input(self):
        return self.input    
    
    def evaluate(self):
        conn,cursor =connection()
        data = self.get_input()
        data_dict = json.loads(data)
        for dt in data_dict:
            amount=dt["amount"]
            if(amount):
                cursor.execute("SELECT condition_type, op, left_path, right_value FROM conditions WHERE rule_id=%s", ('high_amount',))
                conds = cursor.fetchall()
               
                
                
                
            
        
        
        