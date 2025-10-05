import json
import pytest
from src.evaluator import Evaluator, RuleEvaluator

@pytest.fixture
def payload():
    with open("src/input_files/payload.json", "r") as file:
        return json.load(file)

class TestEvaluator:

    def test_high_amount(self, payload):
        evaluator = Evaluator(payload)
        results = evaluator.evaluate()
        print("\nTRACE:", results[0]['trace'])

        found = False
        for rule_res in results:
            if rule_res["rule_id"] == "high_amount":
                found = True
                assert rule_res["decision"] in ["review", "approve"]
                assert rule_res["score"] >= 0
                assert isinstance(rule_res["reason"], str)
                assert isinstance(rule_res["trace"], list)
        assert found, "high_amount rule not found in results"

    def test_geo_mismatch(self, payload):
        evaluator = Evaluator(payload)
        results = evaluator.evaluate()
        print("\nTRACE:", results[0]['trace'])

        found = False
        for rule_res in results:
            if rule_res["rule_id"] == "geo_mismatch":
                found = True
                assert rule_res["decision"] in ["deny", "approve"]
                assert isinstance(rule_res["score"], (int, float))
                assert isinstance(rule_res["reason"], str)
                assert isinstance(rule_res["trace"], list)
        assert found, "geo_mismatch rule not found in results"
    
    def test_score_within_bounds(self, payload):
        evaluator = Evaluator(payload)
        results = evaluator.evaluate()
        print("\nTRACE:", results[0]['trace'])
        for r in results:
            assert 0 <= r["score"] <= 100
    # def test_missing_attributes(self):
    #     payload = {"amount": 2000}   
    #     evaluator = Evaluator(payload)
    #     results = evaluator.evaluate()
    #     print("\nTRACE (missing attrs):", results[0]['trace'])
    #     assert any("Missing attribute" in cond.get("error", "") for cond in results[0]['trace'])

    def test_all(self, payload):
        evaluator = Evaluator(payload)
        results = evaluator.evaluate()
        print("\nTRACE:", results[0]['trace'])

        for rule_res in results:
            assert "rule_id" in rule_res
            assert "decision" in rule_res
            assert "score" in rule_res
            assert "reason" in rule_res
            assert "trace" in rule_res
            assert isinstance(rule_res["trace"], list)

    

