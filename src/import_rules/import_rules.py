import json
from ..db import connection
class ImportRules:
    def __init__(self, file_path):
        self.file_path = file_path
        self.rules = self.load_rules()

    def load_rules(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def get_rules(self):
        # data = self.rules
        return self.rules
class Import_to_db(ImportRules):
    
    def __init__(self, file_path):
        super().__init__(file_path)
        
    def insert_rules(self):
        data = self.get_rules()
        conn, cursor = connection()
        try:
            defaults = data.get("defaults", {})
            if defaults:
                 cursor.execute(
                "INSERT INTO defaults (decision, base_score) VALUES (%s, %s)",
                (defaults["decision"], defaults["base_score"])
                )
                 
            for dt in data['rules']:
                    rule_id=dt["id"]
                    
                    cursor.execute("SELECT COUNT(*) FROM rules WHERE rule_id = %s", (rule_id,))
                    exists = cursor.fetchone()[0]
    
                    if exists:
                         print(f"Rule with ID {rule_id} already exists. Skipping insertion.")
                         continue
                    then=dt["then"]
                
                    cursor.execute("INSERT INTO rules(rule_id,decision,score_delta,reason) VALUES (%s,%s,%s,%s)",
                                (rule_id,then["decision"],then["score_delta"],then["reason"]))
                    when_data = dt["when"]
                    for condition_type in ["all", "any"]:
                            if condition_type in when_data:
                                for cond in when_data[condition_type]:
                                    cursor.execute(
                            "INSERT INTO conditions (rule_id, condition_type, op, left_path, right_value) VALUES (%s, %s, %s, %s, %s)",
                            (rule_id, condition_type, cond["op"], cond["left"], json.dumps(cond["right"]))
                                )

                    conn.commit()
            print("Rules and conditions inserted successfully in database.")
        except Exception as e:
            print("Error inserting rules:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


        