# Rules Engine Lite

## Overview
**Rules Engine Lite** is a Python-based mini rules evaluator that decides whether an input should be **approved**, **denied**, or **reviewed**, based on JSON-defined rules stored in a database.  
It also provides **score calculation** and **explainability (trace)** for each decision.

---

### Supported Features
- **Condition Trees**: `all` (AND) / `any` (OR) logic.  
- **Operators**: `==`, `!=`, `>`, `<`, `>=`, `<=`, `in`.  
- **Attribute-to-Attribute Comparisons**: e.g., `amount > limit`.  
- **Nested Attribute Paths**: Dot-notation lookup (`payer.country`, `items.0.price`).  
- **Short-Circuit Evaluation**: Stops evaluating further conditions once outcome is decided (for performance).

## Environment & Versions

- **Python**: 3.11.9
- **pytest**: 8.4.2
- **MySQL**: 8.0.43 

## Requirements

Make sure you have **Python 3.8+** installed.  
Then install required dependencies using:

```bash
pip install -r requirements.txt

```

## Rule Evaluation

### Inputs
- **payload.json**: Arbitrary nested JSON representing an event or transaction.  
- **ruleset.json**: JSON file containing a list of rules (imported into the DB).


### Outputs
Each rule evaluation returns:
- **decision**: One of `"approve"`, `"deny"`, or `"review"`.  
- **score**: Numeric score in the range `[0, 100]`.  
- **trace**: Structured explanation listing which conditions passed/failed and why. 

 
 
##  How to Run the Project

Follow these steps to set up and run the Rules Engine locally   

### 1.Setup Database
After cloning the repo, create the required database and tables by running:

```bash
mysql -u root -p < db_queries.sql
```
### 2.run the main.py

## Customization
### If you want to test different data, update:
#### 1.update the payload.json here src/input_files/payload.json
#### 2.run 
```bash
python python main.py --payload payload.json --rules rules.json
```

### If you want to modify or add new rules, go to:
#### 1.update the ruleset.json here src/import_rules/files/ruleset.json
#### 2.run 
```bash
python python main.py --payload payload.json --rules rules.json
```
