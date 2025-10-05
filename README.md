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
