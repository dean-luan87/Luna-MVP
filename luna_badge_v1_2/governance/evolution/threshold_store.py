import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from ..instinct_controller.c_thresholds import (
    CThresholdProfile,
    DEFAULT_C_THRESHOLD_PROFILE,
)


DEFAULT_VERSION_ID = "default"


@dataclass(frozen=True)
class ThresholdVersion:
    version_id: str
    profile: CThresholdProfile
    base_version: Optional[str]
    issued_at: float
    description: str
    ttl_sec: Optional[float] = None
    is_baseline: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.version_id, str) or not self.version_id:
            raise ValueError("version_id must be a non-empty string.")


class ThresholdStore:
    def __init__(self) -> None:
        self._versions: Dict[str, ThresholdVersion] = {}
        self._order: List[str] = []
        default_version = ThresholdVersion(
            version_id=DEFAULT_VERSION_ID,
            profile=DEFAULT_C_THRESHOLD_PROFILE,
            base_version=None,
            issued_at=time.time(),
            description="system default",
            ttl_sec=None,
            is_baseline=True,
        )
        self.add_version(default_version)

    def add_version(self, version: ThresholdVersion) -> None:
        if version.version_id in self._versions:
            raise ValueError(f"version_id already exists: {version.version_id}")
        if version.version_id != DEFAULT_VERSION_ID:
            if not version.base_version:
                raise ValueError("base_version is required for non-default versions.")
            if version.is_baseline:
                raise ValueError("non-default versions cannot be baseline.")
        self._versions[version.version_id] = version
        self._order.append(version.version_id)

    def get_version(self, version_id: str) -> ThresholdVersion:
        if version_id not in self._versions:
            raise KeyError(f"version_id not found: {version_id}")
        return self._versions[version_id]

    def list_versions(self) -> List[ThresholdVersion]:
        return [self._versions[version_id] for version_id in self._order]

    def get_default(self) -> ThresholdVersion:
        return self._versions[DEFAULT_VERSION_ID]
