from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_revocation_check_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    temporal_snapshot = dict(input_candidate.get("temporal_snapshot") or {})
    revoked = bool(temporal_snapshot.get("revoked", False))
    expired = bool(temporal_snapshot.get("expired", False))
    return {
        "schema_version": "permission_revocation_checker_v1",
        "revoked": revoked,
        "expired": expired,
        "revocation_reason": temporal_snapshot.get("revocation_reason"),
        "expiry_reason": temporal_snapshot.get("expiry_reason"),
        **not_fact(),
    }
