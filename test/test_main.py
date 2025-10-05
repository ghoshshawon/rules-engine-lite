import json
import pytest
from src.evaluator import Evaluator, RuleEvaluator

@pytest.fixture
def payload():
    with open("src/input_files/payload.json", "r") as file:
        return json.load(file)

class TestEvaluator:

    def test_high_amount_rule(self, payload):
        evaluator = Evaluator(payload)
        results = evaluator.evaluate()

        found = False
        for rule_res in results:
            if rule_res["rule_id"] == "high_amount":
                found = True
                assert rule_res["decision"] in ["review", "approve"]
                assert rule_res["score"] >= 0
                assert isinstance(rule_res["reason"], str)
                assert isinstance(rule_res["trace"], list)
        assert found, "high_amount rule not found in results"

    def test_geo_mismatch_rule(self, payload):
        evaluator = Evaluator(payload)
        results = evaluator.evaluate()

        found = False
        for rule_res in results:
            if rule_res["rule_id"] == "geo_mismatch":
                found = True
                assert rule_res["decision"] in ["deny", "approve"]
                assert isinstance(rule_res["score"], (int, float))
                assert isinstance(rule_res["reason"], str)
                assert isinstance(rule_res["trace"], list)
        assert found, "geo_mismatch rule not found in results"

    def test_all_rules_have_structure(self, payload):
        evaluator = Evaluator(payload)
        results = evaluator.evaluate()

        for rule_res in results:
            assert "rule_id" in rule_res
            assert "decision" in rule_res
            assert "score" in rule_res
            assert "reason" in rule_res
            assert "trace" in rule_res
            assert isinstance(rule_res["trace"], list)

    # def test_score_within_bounds(self, payload):
    #     evaluator = Evaluator(payload)
    #     results = evaluator.evaluate()
    #     for r in results:
    #         assert 0 <= r["score"] <= 100

    # def test_invalid_operator_handling(self, monkeypatch, payload):
    #     def mock_evaluate_rule(self, rule_id, decision, score_delta, reason):
    #         raise Exception("Unknown operator")

    #     monkeypatch.setattr(RuleEvaluator, "evaluate_rule", mock_evaluate_rule)
    #     evaluator = Evaluator(payload)
    #     with pytest.raises(Exception, match="Unknown operator"):
    #         evaluator.evaluate()