"""Pure static validators for candidate semantics and negative guards."""

from __future__ import annotations

from typing import Iterable, Tuple

from .self_attribution_types_v1 import SelfAttributionCandidateV1
from .self_continuity_types_v1 import SelfContinuityCandidateV1
from .self_governance_ownership_guard_v1 import validate_inter_owner_boundary
from .self_governance_registry_v1 import (
    ATTRIBUTION_STATES,
    BOUNDARY_CLASSES,
    CANONICAL_OWNER,
    NEGATIVE_GUARDS,
    IDEMPOTENCY_GUARDS,
    SENSITIVITY_LEVELS,
)
from .self_io_types_v1 import SelfGovernanceOutputV1
from .self_reference_types_v1 import SelfReferenceCandidateV1
from .self_trace_types_v1 import SelfProvenanceV1, SelfTraceV1


def validate_self_reference(candidate: SelfReferenceCandidateV1) -> Tuple[str, ...]:
    issues = []
    if candidate.candidate_only is not True:
        issues.append("reference_not_candidate_only")
    if candidate.fact_admitted or candidate.persisted:
        issues.append("reference_promoted_or_persisted")
    if not candidate.source_refs or not candidate.evidence_refs or not candidate.provenance_refs:
        issues.append("reference_lineage_missing")
    if candidate.subject_boundary_class not in BOUNDARY_CLASSES:
        issues.append("boundary_class_invalid")
    if candidate.source_owner_mutation is not False:
        issues.append("reference_source_mutation")
    return tuple(issues)


def validate_self_attribution(candidate: SelfAttributionCandidateV1) -> Tuple[str, ...]:
    issues = []
    if candidate.candidate_only is not True or candidate.fact_admitted or candidate.persisted:
        issues.append("attribution_not_candidate_only")
    if candidate.state not in ATTRIBUTION_STATES:
        issues.append("attribution_state_invalid")
    if candidate.sensitivity not in SENSITIVITY_LEVELS:
        issues.append("sensitivity_invalid")
    if not candidate.source_refs or not candidate.evidence_refs or not candidate.provenance_refs:
        issues.append("attribution_lineage_missing")
    if candidate.source_owner_mutation is not False:
        issues.append("attribution_source_mutation")
    if candidate.stability_partition == "FUTURE_PERSONALITY_DERIVED_SELF" and candidate.state == "ADMITTED_CANDIDATE":
        issues.append("deferred_personality_admitted")
    return tuple(issues)


def validate_continuity(candidate: SelfContinuityCandidateV1) -> Tuple[str, ...]:
    issues = []
    if candidate.candidate_only is not True or candidate.immutable_identity_claim:
        issues.append("continuity_identity_or_candidate_violation")
    if not candidate.provenance_refs or not candidate.root_cycle_trace_id:
        issues.append("continuity_trace_missing")
    if not candidate.stable_refs and not candidate.changed_refs and not candidate.unresolved_refs:
        issues.append("continuity_change_partition_missing")
    return tuple(issues)


def validate_trace_and_provenance(trace: SelfTraceV1, provenance: SelfProvenanceV1) -> Tuple[str, ...]:
    issues = []
    if not trace.reverse_locatable or not provenance.reverse_locatable:
        issues.append("reverse_lookup_missing")
    if trace.provenance_grants_authority:
        issues.append("trace_claims_authority")
    if not provenance.immutable:
        issues.append("provenance_not_immutable")
    if not trace.schema_version or not trace.contract_version:
        issues.append("trace_contract_missing")
    return tuple(issues)


def validate_negative_guards(guards: dict[str, bool]) -> Tuple[str, ...]:
    return tuple(
        key for key, expected in NEGATIVE_GUARDS.items() if guards.get(key) is not expected
    )


def validate_output(output: SelfGovernanceOutputV1) -> Tuple[str, ...]:
    issues = list(validate_self_reference(output.self_reference))
    if output.self_attribution is not None:
        issues.extend(validate_self_attribution(output.self_attribution))
    if output.self_continuity is not None:
        issues.extend(validate_continuity(output.self_continuity))
    issues.extend(validate_trace_and_provenance(output.trace, output.provenance))
    issues.extend(validate_negative_guards(output.negative_guards))
    if set(output.idempotency_guards) != set(IDEMPOTENCY_GUARDS):
        issues.append("idempotency_guard_set_incomplete")
    if output.boundary_class not in BOUNDARY_CLASSES:
        issues.append("output_boundary_invalid")
    if output.synthetic_only is not True or output.candidate_only is not True:
        issues.append("output_mode_invalid")
    if not validate_inter_owner_boundary(output):
        issues.append("inter_owner_boundary_violation")
    return tuple(issues)


def expected_guard_keys() -> Tuple[str, ...]:
    return tuple(NEGATIVE_GUARDS)


def canonical_owner_is_narrow() -> bool:
    return CANONICAL_OWNER == "Self Governance"
