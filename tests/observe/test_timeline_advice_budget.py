from advice_budget.schema import AdviceDecision, AdviceCandidate
from observe.timeline_advice_budget import snapshot_advice_budget_debug


def test_advice_budget_written_to_timeline():
    debug = snapshot_advice_budget_debug(
        decisions=[AdviceDecision(True, "soft", 10, "budget_ok")],
        candidates=[AdviceCandidate("path_hint", False, 0.6, "pal")],
    )
    assert debug["count"] == 1
    item = debug["items"][0]
    assert item["allow"] is True
    assert item["reason"] == "budget_ok"
