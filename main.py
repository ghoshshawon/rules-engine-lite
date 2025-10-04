from src.db import connect_db
from src.import_rules import ImportRules, Import_to_db
from src.evaluator import Evaluator
 
if __name__ == "__main__":
    db_insert = Import_to_db("src/import_rules/files/payload.json")
    db_insert.insert_rules()  
    
    input={
    "amount": 1250.75,
    "currency": "USD",
    "payer": {"country": "US", "ip_country": "MX"},
    "device": {"country": "US"},
    "items": [{"sku": "A1", "price": 200.0}, {"sku": "B2", "price": 1050.75}]
    }
    ev = Evaluator(input)
 