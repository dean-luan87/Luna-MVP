import time

from c3_policy.store import save_policy, load_policy_raw
from c3_policy.types import ObservationPolicy, ObservationRule


def test_store_roundtrip(tmp_path):
    policy = ObservationPolicy(
        policy_id="obs-policy-test",
        version=1,
        generated_at=time.time(),
        environment="test",
        rules=[ObservationRule(roi_kind="exit_area", priority=1)],
        evidence={"source": "C3"},
    )
    path = tmp_path / "policy.json"
    save_policy(policy, str(path))
    data = load_policy_raw(str(path))
    assert data["policy_id"] == "obs-policy-test"
    assert data["environment"] == "test"
    assert len(data["rules"]) == 1
