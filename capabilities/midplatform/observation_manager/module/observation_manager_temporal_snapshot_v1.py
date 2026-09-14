from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_temporal_snapshot_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    snapshot = dict(input_candidate.get("temporal_snapshot") or {})
    present = bool(snapshot)
    return {
        "schema_version": "observation_manager_temporal_snapshot_v1",
        "temporal_snapshot": snapshot,
        "temporal_snapshot_ref": snapshot.get("temporal_snapshot_ref")
        or snapshot.get("frame_time_ref")
        or "",
        "temporal_snapshot_present": present,
        **not_fact(),
    }
