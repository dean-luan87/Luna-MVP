from dataclasses import dataclass
from typing import Dict, List, Optional

from .threshold_store import DEFAULT_VERSION_ID, ThresholdVersion


@dataclass
class RolloutPlan:
    version_id: str
    canary_ratio: float
    kpi_targets: Dict
    rollback_conditions: Dict


class RolloutManager:
    def __init__(self, default_version_id: str = DEFAULT_VERSION_ID) -> None:
        self._default_version_id = default_version_id
        self._active_version = default_version_id
        self._history: List[str] = [default_version_id]
        self._submitted: Dict[str, ThresholdVersion] = {}

    @property
    def active_version(self) -> str:
        return self._active_version

    def submit(self, candidates: List[ThresholdVersion]) -> None:
        for candidate in candidates:
            self._submitted[candidate.version_id] = candidate

    def activate(self, version_id: str) -> None:
        if version_id != self._default_version_id and version_id not in self._submitted:
            raise ValueError(f"Unknown version_id: {version_id}")
        self._active_version = version_id
        self._history.append(version_id)

    def rollback(self) -> None:
        if len(self._history) <= 1:
            self._active_version = self._default_version_id
            self._history = [self._default_version_id]
            return
        self._history.pop()
        self._active_version = self._history[-1]
