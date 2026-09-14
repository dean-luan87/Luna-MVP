from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_understanding.region_owner_analyzer_v1 import (
    analyze_region_owners,
)


def resolve_ownership_v1(
    *,
    device_ref: str,
    region_ref: str,
    ownership_context: Mapping[str, Any],
) -> Dict[str, Any]:
    allowed_regions = set(str(x) for x in ownership_context.get("allowed_regions", []))
    allowed_devices = set(str(x) for x in ownership_context.get("allowed_devices", []))
    blocked_regions = set(str(x) for x in ownership_context.get("blocked_regions", []))

    analyzer = analyze_region_owners(
        profile_key=str(ownership_context.get("profile_key", "stacked_documents")),
        upstream_region_id=region_ref or "region_001",
    )

    region_ok = (
        not allowed_regions or region_ref in allowed_regions
    ) and region_ref not in blocked_regions
    device_ok = not allowed_devices or device_ref in allowed_devices
    ownership_ok = region_ok and device_ok

    return {
        "ownership_ok": ownership_ok,
        "region_ok": region_ok,
        "device_ok": device_ok,
        "ownership_blocked": not ownership_ok,
        "ownership_graph_candidate": analyzer,
        "ownership_reason": "ownership_allowed"
        if ownership_ok
        else "ownership_policy_blocked",
    }
