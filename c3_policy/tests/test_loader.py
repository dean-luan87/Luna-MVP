import time

from c3_policy.loader import load_policy


def test_load_policy_basic():
    data = {
        "policy_id": "obs-policy-demo",
        "version": 1,
        "generated_at": time.time(),
        "environment": "indoor",
        "rules": [{"roi_kind": "exit_area", "priority": 2}],
        "evidence": {"source": "C3"},
    }
    policy = load_policy(data)
    assert policy.policy_id == "obs-policy-demo"
    assert policy.rules[0].roi_kind == "exit_area"
