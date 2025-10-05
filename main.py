from src.db import connect_db
from src.import_rules import ImportRules, Import_to_db
from src.evaluator import Evaluator
import pytest
if __name__ == "__main__":
    db_insert = Import_to_db("src/import_rules/files/ruleset.json")
    db_insert.insert_rules()
    print("\n Running Tests from main.py...\n")
    pytest.main(["-v", "test/test_main.py"])
 