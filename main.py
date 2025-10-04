from src.db import connect_db
from src.import_rules import ImportRules, Import_to_db
 
if __name__ == "__main__":
    db_insert = Import_to_db("src/import_rules/files/payload.json")
    db_insert.insert_rules()  
 