from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

_REGISTRY_PATH = Path("capabilities/registry/luna_capability_registry_v1.json")


def _load_registry(path: Path = _REGISTRY_PATH) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _routing_status_from_lifecycle(lifecycle_status: str) -> str:
    if lifecycle_status == "functional_module_ready":
        return "integration_candidate"
    if lifecycle_status in {
        "building",
        "skeleton_ready",
        "integration_ready",
        "planned",
    }:
        return "controlled_test_candidate"
    if lifecycle_status in {"blocked", "deprecated", "retired", "degraded"}:
        return "blocked"
    return "unknown"


def build_capability_routes_v1(
    *,
    capability_requirements: Iterable[str],
    request_payload_seed: Mapping[str, Any],
    registry_path: Path = _REGISTRY_PATH,
) -> Dict[str, Any]:
    registry = _load_registry(registry_path)
    rows = registry.get("capabilities", [])
    by_id = {str(r.get("capability_id", "")): r for r in rows}

    candidates: List[Dict[str, Any]] = []
    blocked_refs: List[str] = []

    for idx, cap_id in enumerate(
        tuple(str(x) for x in capability_requirements), start=1
    ):
        row = by_id.get(cap_id)
        if row is None:
            candidates.append(
                {
                    "requested_capability_id": cap_id,
                    "capability_status": "unknown",
                    "module_api_ref": None,
                    "request_payload_candidate": dict(request_payload_seed),
                    "dependency_order": idx,
                    "fallback_candidate": "human_review_required",
                    "routing_status": "blocked",
                }
            )
            blocked_refs.append(cap_id)
            continue

        lifecycle_status = str(row.get("lifecycle_status", "planned"))
        routing_status = _routing_status_from_lifecycle(lifecycle_status)
        if routing_status == "blocked":
            blocked_refs.append(cap_id)

        candidates.append(
            {
                "requested_capability_id": cap_id,
                "capability_status": lifecycle_status,
                "module_api_ref": (row.get("module_api") or {}).get("path"),
                "request_payload_candidate": dict(request_payload_seed),
                "dependency_order": idx,
                "fallback_candidate": "fallback_candidate"
                if routing_status != "blocked"
                else "human_review_required",
                "routing_status": routing_status,
            }
        )

    return {
        "execution_request_candidates": tuple(candidates),
        "capability_availability": {
            c["requested_capability_id"]: c["routing_status"] for c in candidates
        },
        "blocked_capabilities": tuple(blocked_refs),
    }
