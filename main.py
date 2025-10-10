from src.db import connect_db
from src.import_rules import ImportRules, Import_to_db
from src.evaluator import Evaluator
import pytest
import json
import os
import argparse
from fastapi import FastAPI

payload_path="src/input_files/"
rules_path="src/import_rules/files/"
def get_data_rules(payload_file, rules_file):
    data = os.path.join(payload_path, payload_file)
    rules = os.path.join(rules_path, rules_file)
    
    return data,rules

# app = FastAPI()

# @app.get("/")
# def get_welcome():
#      return "welcome"


if __name__ == "__main__":
    
    parser= argparse.ArgumentParser("Rules Evaluation")
    parser.add_argument(
         "--payload",metavar="input data file",required=True,help="Please provide the Payload to verify with rules"
    )
    parser.add_argument(
         "--rules",metavar="rules file",required=True,help="Please provide the Rules"
    )
    args = parser.parse_args()
    data, rules = get_data_rules(args.payload, args.rules)
    os.environ["PAYLOAD_FILE"] = data
    
    db_insert = Import_to_db(rules)
    db_insert.insert_rules()
    print("\n Running Tests from main.py...\n")
    pytest.main(["-v", "test/test_main.py"])
 