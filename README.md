# Rules Engine Lite

## Overview
**Rules Engine Lite** is a Python-based mini rules evaluator that decides whether an input should be **approved**, **denied**, or **reviewed**, based on JSON-defined rules stored in a database.  
It also provides **score calculation** and **explainability (trace)** for each decision.

---

## Features
- Load and evaluate rules from JSON or database  
- Support for `all` and `any` condition types  
- Dynamic decision output: `approve`, `deny`, `review`  
- Rule explainability (why a decision was made)  
- Clean and modular Python structure  

---

## Requirements

Make sure you have **Python 3.8+** installed.  
Then install required dependencies using:

```bash
pip install -r requirements.txt

```
##  How to Run the Project

Follow these steps to set up and run the Rules Engine locally 👇  

### 1.Setup Database
After cloning the repo, create the required database and tables by running:

```bash
mysql -u root -p < db_queries.sql
```
### 2.run the main.py

## Others
If you want to test different data, update:
1.Change Input Payload
src/input_files/payload.json
2.run main.py


If you want to modify or add new rules, go to:
1.Update Rules
src/import_rules/files/ruleset.json
2.run main