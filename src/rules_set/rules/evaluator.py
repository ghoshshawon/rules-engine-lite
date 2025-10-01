import json
import rules as rl

class SetRules:
    def __init__(self, rule_data):
            self.rule_data = rule_data

    def print_rules(self):
        for data in self.rule_data:
            print("ID:", data["id"])
            print("WHEN:", data["when"])
            print("THEN:", data["then"])
            print("----")
    # Usage
    if __name__ == "__main__":
        sr = SetRules(rl.rule_data)
        sr.print_rules()
            
   