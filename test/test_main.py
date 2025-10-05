import json
from src import connect_db
from src import ImportRules, Import_to_db
from src.evaluator import Evaluator

def test_simple_approval():
    payload_path = "src/input_files/payload.json"
    
    with open(payload_path,'r') as file:
        payload= json.load(file)
    
    evaluator = Evaluator(payload)
    result = evaluator.evaluate()


    assert result["decision"] == "review"
    assert result["score"] == 20
    assert "High amount" in result["reason"]
    assert any(cond["passed"] for cond in result["trace"])    
        
        
    
    
    
