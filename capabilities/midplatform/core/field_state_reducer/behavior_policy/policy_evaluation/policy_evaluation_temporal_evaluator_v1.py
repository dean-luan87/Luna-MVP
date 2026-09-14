from __future__ import annotations

from typing import Any, Dict

from .policy_evaluation_types_v1 import EvaluationInput, TemporalEvaluationResult


def evaluate_temporal(
    evaluation_input: EvaluationInput,
    temporal_contract: Dict[str, Any],
) -> TemporalEvaluationResult:
    status = str(evaluation_input.temporal_snapshot.get("status", "unknown"))
    rows = dict(temporal_contract.get("temporal_statuses", {}))
    row = rows.get(status, rows.get("unknown", {}))

    refresh_available = bool(
        evaluation_input.temporal_snapshot.get("refresh_evidence_available", False)
    )
    new_event_available = bool(
        evaluation_input.temporal_snapshot.get("new_event_available", False)
    )

    refresh_required = bool(row.get("refresh_required", False))
    new_event_required = bool(row.get("new_event_required", False))
    blocking = bool(row.get("blocking", False))
    support_eligible = bool(row.get("support_eligible", False))

    if refresh_required and not refresh_available:
        return TemporalEvaluationResult(
            status="temporally_invalid",
            support_eligible=False,
            blocking=True,
            refresh_required=True,
            new_event_required=new_event_required,
            rejection_reason="missing_refresh_evidence",
        )

    if new_event_required and not new_event_available:
        return TemporalEvaluationResult(
            status="temporally_invalid",
            support_eligible=False,
            blocking=True,
            refresh_required=refresh_required,
            new_event_required=True,
            rejection_reason=row.get("rejection_reason") or "invalid_temporal_status",
        )

    if status in {
        "revoked",
        "expired",
        "suspended",
        "superseded",
        "not_yet_valid",
        "unknown",
    }:
        return TemporalEvaluationResult(
            status="temporally_invalid",
            support_eligible=False,
            blocking=True,
            refresh_required=refresh_required,
            new_event_required=new_event_required,
            rejection_reason=row.get("rejection_reason") or "invalid_temporal_status",
        )

    return TemporalEvaluationResult(
        status="active" if support_eligible and not blocking else "temporally_invalid",
        support_eligible=support_eligible,
        blocking=blocking,
        refresh_required=refresh_required,
        new_event_required=new_event_required,
        rejection_reason=None,
    )
