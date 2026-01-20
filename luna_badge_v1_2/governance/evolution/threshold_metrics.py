import time
from dataclasses import dataclass
from typing import Dict


@dataclass
class ThresholdMetrics:
    version_id: str
    sample_count: int
    takeover_rate: float
    gate_block_rate: float
    hold_rate: float
    stability_score: float
    last_updated: float


class ThresholdMetricsCollector:
    def __init__(self) -> None:
        self._counts: Dict[str, Dict[str, int]] = {}
        self._last_updated: Dict[str, float] = {}

    def record(self, version_id: str, c_output: str) -> None:
        allowed = {"STOP", "HOLD", "REQUEST_TAKEOVER"}
        if c_output not in allowed:
            raise ValueError(f"Unsupported c_output: {c_output}")
        if version_id not in self._counts:
            self._counts[version_id] = {"STOP": 0, "HOLD": 0, "REQUEST_TAKEOVER": 0}
        self._counts[version_id][c_output] += 1
        self._last_updated[version_id] = time.time()

    def snapshot(self, version_id: str) -> ThresholdMetrics:
        counts = self._counts.get(version_id, {"STOP": 0, "HOLD": 0, "REQUEST_TAKEOVER": 0})
        sample_count = sum(counts.values())
        takeover_rate = (counts["REQUEST_TAKEOVER"] / sample_count) if sample_count else 0.0
        hold_rate = (counts["HOLD"] / sample_count) if sample_count else 0.0
        gate_block_rate = 0.0
        stability_score = 1.0
        last_updated = self._last_updated.get(version_id, time.time())
        return ThresholdMetrics(
            version_id=version_id,
            sample_count=sample_count,
            takeover_rate=takeover_rate,
            gate_block_rate=gate_block_rate,
            hold_rate=hold_rate,
            stability_score=stability_score,
            last_updated=last_updated,
        )
