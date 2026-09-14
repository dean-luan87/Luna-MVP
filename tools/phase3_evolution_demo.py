import time

from luna_badge_v1_2.governance.evolution.evolution_loop import evolution_loop
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


def main() -> None:
    store = ThresholdStore()
    collector = ThresholdMetricsCollector()
    proposer = ThresholdProposer()
    rollout = RolloutManager()

    collector.record("default", "HOLD")
    collector.record("default", "REQUEST_TAKEOVER")

    candidate = ThresholdVersion(
        version_id="candidate_v1",
        profile=DEFAULT_C_THRESHOLD_PROFILE,
        base_version="default",
        issued_at=time.time(),
        description="manual candidate",
    )
    store.add_version(candidate)

    evolution_loop(store, collector, proposer, rollout)

    print("active_version:", rollout.active_version)
    print("versions:", [v.version_id for v in store.list_versions()])
    print("default_metrics:", collector.snapshot("default"))
    print("submitted_candidates:", "candidate_v1" in rollout._submitted)


if __name__ == "__main__":
    main()
