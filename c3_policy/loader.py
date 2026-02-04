from __future__ import annotations

from .types import ObservationPolicy, ObservationRule


def load_policy(data: dict) -> ObservationPolicy:
    rules = [ObservationRule(**r) for r in data.get("rules", [])]
    return ObservationPolicy(
        policy_id=data["policy_id"],
        version=data["version"],
        generated_at=data["generated_at"],
        environment=data["environment"],
        rules=rules,
        evidence=data.get("evidence", {}),
    )
