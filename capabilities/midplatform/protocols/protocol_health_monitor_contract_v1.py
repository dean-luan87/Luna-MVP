# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Health Monitor Contract v1 — contract definition only."""

from __future__ import annotations

from typing import Any, Dict, List

HEALTH_MONITOR_DIMENSIONS: List[str] = [
    "assimilation_health",
    "semantic_drift",
    "field_drift",
    "candidate_record_misread",
    "ttl_revocation_expiry_loss",
    "fallback_degraded_mode",
    "quarantine_status",
    "notification_status",
]


def build_health_monitor_contract(protocol_id: str) -> Dict[str, Any]:
    return {
        "contract_id": "protocol_health_monitor_contract_v1",
        "protocol_id": protocol_id,
        "dimensions": HEALTH_MONITOR_DIMENSIONS,
        "runtime_monitoring_enabled": False,
        "supervision_mode": "planning_contract_only",
        "notification_required_on_drift": True,
        "quarantine_on_blocker": True,
    }
