from c3_policy.compiler import compile_policy


def test_compile_basic():
    confirmed = [
        {"roi_kind": "exit_area", "enabled": True, "priority": 2},
        {"roi_kind": "ad_screen", "enabled": False},
    ]

    policy = compile_policy(confirmed, environment="indoor")

    assert policy.environment == "indoor"
    assert len(policy.rules) == 1
    assert policy.rules[0].roi_kind == "exit_area"
