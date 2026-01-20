from .rollout_manager import RolloutManager
from .threshold_metrics import ThresholdMetricsCollector
from .threshold_proposer import ThresholdProposer
from .threshold_store import ThresholdStore


def evolution_loop(
    store: ThresholdStore,
    collector: ThresholdMetricsCollector,
    proposer: ThresholdProposer,
    rollout: RolloutManager,
) -> None:
    for version in store.list_versions():
        try:
            metrics = collector.snapshot(version.version_id)
            candidates = proposer.propose(version, metrics)
            rollout.submit(candidates)
        except Exception:
            continue
