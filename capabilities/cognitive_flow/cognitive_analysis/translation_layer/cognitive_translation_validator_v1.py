"""Independent, non-executing validation for the A3 Translation Layer Skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .cognitive_translation_contract_v1 import NEGATIVE_GUARD_IDS_V1
from .cognitive_translation_types_v1 import (
    ALLOWED_PRIMITIVE_TYPES_V1,
    COGNITIVE_TRANSLATION_SCHEMA_VERSION_V1,
    CognitivePrimitiveCandidateV1,
    CognitiveTranslationCandidateEnvelopeV1,
    CognitiveTranslationFlagsV1,
    CognitiveTranslationRequestEnvelopeV1,
)


@dataclass(frozen=True)
class CognitiveTranslationValidationIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveTranslationValidationResultV1:
    issues: Tuple[CognitiveTranslationValidationIssueV1, ...]
    negative_guards_checked: Tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def _non_empty_references_v1(
    field_ref: str,
    values: Tuple[str, ...],
) -> Tuple[CognitiveTranslationValidationIssueV1, ...]:
    if not values or any(not isinstance(value, str) or not value.strip() for value in values):
        return (CognitiveTranslationValidationIssueV1(
            "reference_missing", field_ref, f"{field_ref} must contain non-empty references"
        ),)
    return ()


def validate_cognitive_translation_request_v1(
    request: CognitiveTranslationRequestEnvelopeV1,
) -> CognitiveTranslationValidationResultV1:
    """Validate input references only; never resolve them or invoke an external capability."""
    issues = []
    if request.schema_version != COGNITIVE_TRANSLATION_SCHEMA_VERSION_V1:
        issues.append(CognitiveTranslationValidationIssueV1(
            "schema_version_invalid", "schema_version", "request must use translation skeleton schema v1"
        ))
    if not isinstance(request.translation_request_id, str) or not request.translation_request_id.strip():
        issues.append(CognitiveTranslationValidationIssueV1(
            "request_id_missing", "translation_request_id", "request identity is required"
        ))
    for field_ref, values in (
        ("evidence_refs", request.evidence_refs),
        ("context_refs", request.context_refs),
        ("provenance_refs", request.provenance_refs),
        ("source_capability_refs", request.source_capability_refs),
    ):
        issues.extend(_non_empty_references_v1(field_ref, values))
    if request.requested_primitive_type not in ALLOWED_PRIMITIVE_TYPES_V1:
        issues.append(CognitiveTranslationValidationIssueV1(
            "primitive_type_invalid", "requested_primitive_type", "only candidate primitive types are allowed"
        ))
    if not isinstance(request.trace_ref, str) or not request.trace_ref.strip():
        issues.append(CognitiveTranslationValidationIssueV1(
            "trace_missing", "trace_ref", "trace reference is required"
        ))
    return CognitiveTranslationValidationResultV1(tuple(issues), NEGATIVE_GUARD_IDS_V1)


def validate_cognitive_translation_candidate_envelope_v1(
    request: CognitiveTranslationRequestEnvelopeV1,
    envelope: CognitiveTranslationCandidateEnvelopeV1,
) -> CognitiveTranslationValidationResultV1:
    """Independently validate Contract, guards, trace, and flags; never call Skeleton."""
    issues = list(validate_cognitive_translation_request_v1(request).issues)
    candidate = envelope.cognitive_primitive_candidate
    flags = envelope.translation_flags
    if envelope.request_ref != request.translation_request_id:
        issues.append(CognitiveTranslationValidationIssueV1(
            "request_reference_mismatch", "request_ref", "envelope must retain the request identity"
        ))
    if candidate.primitive_type != request.requested_primitive_type:
        issues.append(CognitiveTranslationValidationIssueV1(
            "primitive_type_mismatch", "primitive_type", "candidate must retain requested candidate type"
        ))
    if candidate.source_refs != request.evidence_refs or candidate.context_refs != request.context_refs:
        issues.append(CognitiveTranslationValidationIssueV1(
            "reference_mapping_mismatch", "source_refs", "Evidence and Context references must be preserved"
        ))
    if not candidate.candidate_only or candidate.fact_status != "not_fact" or candidate.candidate_status != "translation_not_executed":
        issues.append(CognitiveTranslationValidationIssueV1(
            "guard_1_evidence_to_fact", "candidate_status", "Translation output must remain a not-executed candidate, never Fact"
        ))
    if candidate.primitive_type in {"decision", "action"}:
        issues.append(CognitiveTranslationValidationIssueV1(
            "guard_2_evidence_to_decision", "primitive_type", "Decision/Action are not translation primitive types"
        ))
    provenance = candidate.provenance
    if not isinstance(provenance, dict) or not provenance.get("source_refs") or not provenance.get("trace_ref"):
        issues.append(CognitiveTranslationValidationIssueV1(
            "guard_3_provenance_required", "provenance", "source and trace provenance must be preserved"
        ))
    if candidate.candidate_id in request.source_capability_refs or "external_model_entity_ref" in provenance:
        issues.append(CognitiveTranslationValidationIssueV1(
            "guard_4_model_identity_entity", "candidate_id", "External model identity cannot be a Cognitive Entity"
        ))
    expected_false_flags = (
        "translation_executed", "model_invoked", "external_call", "fact_created",
        "decision_created", "action_created", "state_writeback", "context_mutated",
        "snapshot_mutated", "memory_updated", "learning_candidate_admitted",
    )
    if flags.simulation_only is not True:
        issues.append(CognitiveTranslationValidationIssueV1(
            "simulation_boundary_violation", "simulation_only", "controlled skeleton must remain simulation-only"
        ))
    for name in expected_false_flags:
        if getattr(flags, name) is not False:
            code = "guard_5_state_mutation" if name in {"state_writeback", "context_mutated", "snapshot_mutated"} else "forbidden_operation_present"
            issues.append(CognitiveTranslationValidationIssueV1(
                code, f"translation_flags.{name}", f"{name} must be false for the controlled skeleton"
            ))
    if envelope.negative_guard_refs != NEGATIVE_GUARD_IDS_V1:
        issues.append(CognitiveTranslationValidationIssueV1(
            "negative_guard_inventory_mismatch", "negative_guard_refs", "all five negative guards must be declared"
        ))
    return CognitiveTranslationValidationResultV1(tuple(issues), NEGATIVE_GUARD_IDS_V1)
