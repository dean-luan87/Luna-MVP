import time

from map_d0.cache_policy import CachePolicy
from map_d0.packages import LocalPackageState


def test_cache_policy_evict_l2_first():
    now = time.time()
    local_states = {
        "city_a": {
            "L1": LocalPackageState(is_present=True, last_used_ts=now),
            "L2": LocalPackageState(is_present=True, last_used_ts=now),
        },
        "city_b": {
            "L1": LocalPackageState(is_present=True, last_used_ts=now - 100),
            "L2": LocalPackageState(is_present=True, last_used_ts=now - 100),
        },
        "city_c": {
            "L1": LocalPackageState(is_present=True, last_used_ts=now - 200),
            "L2": LocalPackageState(is_present=True, last_used_ts=now - 200),
        },
    }

    policy = CachePolicy(max_cities=2)
    decisions = policy.decide(local_states)

    assert any(
        d.city_id == "city_c" and d.layer == "L2" and d.action == "evict"
        for d in decisions
    )
