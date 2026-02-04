from __future__ import annotations

from typing import List
import time

from .types import ObservationPolicy, ObservationRule


def compile_policy(
    confirmed_rois: List[dict],
    environment: str,
    base_version: int = 1,
) -> ObservationPolicy:
    rules = []

    for item in confirmed_rois:
        if not item.get("enabled", False):
            continue

        rules.append(
            ObservationRule(
                roi_kind=item["roi_kind"],
                priority=item.get("priority", 1),
                ttl_s=item.get("ttl_s"),
                conditions=item.get("conditions", {}),
            )
        )

    return ObservationPolicy(
        policy_id=f"obs-policy-{environment}",
        version=base_version,
        generated_at=time.time(),
        environment=environment,
        rules=rules,
        evidence={
            "source": "C3",
            "confirmed_count": len(rules),
        },
    )
