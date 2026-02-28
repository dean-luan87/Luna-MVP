import time

from luna_badge_v1_2.governance.evolution.rollout_manager import RolloutManager
from luna_badge_v1_2.governance.evolution.threshold_metrics import ThresholdMetricsCollector
from luna_badge_v1_2.governance.evolution.threshold_proposer import ThresholdProposer
from luna_badge_v1_2.governance.evolution.threshold_store import (
    ThresholdStore,
    ThresholdVersion,
)
from luna_badge_v1_2.governance.instinct_controller.c_thresholds import (
    DEFAULT_C_THRESHOLD_PROFILE,
)


def test_proposer_can_return_empty():
    store = ThresholdStore()
    proposer = ThresholdProposer()
    collector = ThresholdMetricsCollector()
    base = store.get_default()
    metrics = collector.snapshot(base.version_id)
    assert proposer.propose(base, metrics) == []


def test_default_threshold_always_exists():
    store = ThresholdStore()
    assert store.get_default() is not None


def test_non_default_requires_base_version():
    store = ThresholdStore()
    version = ThresholdVersion(
        version_id="candidate_v1",
        profile=DEFAULT_C_THRESHOLD_PROFILE,
        base_version=None,
        issued_at=time.time(),
        description="candidate without base",
    )
    try:
        store.add_version(version)
    except ValueError as exc:
        assert "base_version" in str(exc)
    else:
        raise AssertionError("Expected base_version enforcement for non-default")


def test_rollback_always_reaches_default():
    rollout = RolloutManager()
    rollout.rollback()
    assert rollout.active_version == "default"
