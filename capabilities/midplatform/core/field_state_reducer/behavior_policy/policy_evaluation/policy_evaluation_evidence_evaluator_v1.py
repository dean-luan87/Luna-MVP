from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from .policy_evaluation_types_v1 import EvaluationInput, EvidenceSufficiencyResult


def _parse_utc(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


def evaluate_evidence_sufficiency(
    evaluation_input: EvaluationInput,
    evidence_contract: Dict[str, Any],
) -> EvidenceSufficiencyResult:
    reasons: List[str] = []
    missing_inputs: List[str] = []

    events = tuple(evaluation_input.admitted_events)
    min_count = int(evidence_contract.get("minimum_event_count", 1))
    diversity_need = int(evidence_contract.get("source_diversity_requirement", 1))
    required_provenance = tuple(evidence_contract.get("required_provenance", []))

    if len(events) < min_count:
        reasons.append("insufficient_event_count")

    source_ids = {str(e.get("source_id", "")) for e in events if e.get("source_id")}
    if len(source_ids) < diversity_need:
        reasons.append("source_diversity_insufficient")

    for field in required_provenance:
        if (
            field not in evaluation_input.provenance_snapshot
            or evaluation_input.provenance_snapshot.get(field) in (None, "")
        ):
            missing_inputs.append(f"provenance_snapshot.{field}")
    if missing_inputs:
        reasons.append("missing_provenance")

    now = _parse_utc(evaluation_input.evaluation_requested_at)
    stale = False
    contradiction = False
    for e in events:
        event_time = str(e.get("event_time", ""))
        if event_time:
            age_seconds = (now - _parse_utc(event_time)).total_seconds()
            if age_seconds > 86400:
                stale = True
        if bool(e.get("contradictory", False)):
            contradiction = True

    if stale:
        reasons.append("missing_refresh_evidence")
    if contradiction:
        reasons.append("unresolved_conflict_present")

    if not events:
        return EvidenceSufficiencyResult(
            status="missing_required_source",
            sufficient=False,
            missing_inputs=tuple(missing_inputs),
            rejection_reasons=tuple(
                dict.fromkeys(reasons + ["missing_required_event"])
            ),
        )

    if contradiction:
        return EvidenceSufficiencyResult(
            status="contradictory",
            sufficient=False,
            missing_inputs=tuple(missing_inputs),
            rejection_reasons=tuple(dict.fromkeys(reasons)),
        )

    if missing_inputs:
        return EvidenceSufficiencyResult(
            status="missing_provenance",
            sufficient=False,
            missing_inputs=tuple(missing_inputs),
            rejection_reasons=tuple(dict.fromkeys(reasons)),
        )

    if stale:
        return EvidenceSufficiencyResult(
            status="stale_evidence",
            sufficient=False,
            missing_inputs=tuple(missing_inputs),
            rejection_reasons=tuple(dict.fromkeys(reasons)),
        )

    if reasons:
        return EvidenceSufficiencyResult(
            status="insufficient",
            sufficient=False,
            missing_inputs=tuple(missing_inputs),
            rejection_reasons=tuple(dict.fromkeys(reasons)),
        )

    return EvidenceSufficiencyResult(
        status="sufficient",
        sufficient=True,
        missing_inputs=tuple(),
        rejection_reasons=tuple(),
    )
