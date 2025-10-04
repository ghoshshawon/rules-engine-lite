import json
from src.db import connect_db
from src.import_rules import ImportRules, Import_to_db

def test_simple_approval():
    rule_path = "src/import_rules/files/payload.json"
    
    payload = {
    "amount": 1250.75,
    "currency": "USD",
    "payer": {"country": "US", "ip_country": "MX"},
    "device": {"country": "US"},
    "items": [{"sku": "A1", "price": 200.0}, {"sku": "B2", "price": 1050.75}]
    }
    test_rules = {
        "rules": [
            {
                "id": "high_amount",
                "when": {"all": [{"op": ">", "left": "amount", "right": 1000}]},
                "then": {"decision": "review", "score_delta": 20, "reason": "High amount"}
            }
        ],
        "defaults": {"decision": "approve", "base_score": 0}
    }
    
    
    with open (rule_path,'w') as file:
        json.dump(test_rules,file)
    
    db_insert = Import_to_db("src/import_rules/files/payload.json")
    db_insert.insert_rules() 
        
        
        
    
    
    
