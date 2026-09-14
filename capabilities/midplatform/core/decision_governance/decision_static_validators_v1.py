"""Static and behavior validators for Decision Governance outputs."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionCandidateV1,
    DecisionOptionCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.decision_governance.decision_handoff_types_v1 import (
    DecisionToActionTaskHandoffCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_io_types_v1 import (
    DecisionGovernanceOutputV1,
)
from capabilities.midplatform.core.decision_governance.decision_ownership_guard_v1 import (
    validate_candidate_only_handoff,
    validate_canonical_owner,
    validate_no_parallel_owner_token,
    validate_ref_read_only,
)
from capabilities.midplatform.core.decision_governance.decision_registry_v1 import (
    NEGATIVE_GUARD_FLAGS,
    STATE_SET,
)


def validate_input_refs_read_only(all_refs: Iterable[SourceRefV1]) -> bool:
    return validate_ref_read_only(all_refs) and validate_no_parallel_owner_token(
        all_refs
    )


def validate_option(option: DecisionOptionCandidateV1) -> bool:
    return (
        bool(option.option_id)
        and bool(option.option_statement)
        and option.utility.expected_benefit >= 0
        and option.risk.severity >= 0
        and option.risk.likelihood >= 0
        and option.cost >= 0
        and option.reversibility
        in {
            "REVERSIBLE",
            "PARTIALLY_REVERSIBLE",
            "IRREVERSIBLE",
            "UNKNOWN_REVERSIBILITY",
        }
    )


def validate_candidates(items: Iterable[DecisionCandidateV1]) -> bool:
    return all(
        validate_canonical_owner(item.owner)
        and item.candidate_kind == "DECISION_CANDIDATE"
        and item.decision_state in STATE_SET
        and item.decision_authority is True
        and item.action_authority is False
        and item.task_authority is False
        and bool(item.provenance)
        for item in items
    )


def validate_handoff(handoff: DecisionToActionTaskHandoffCandidateV1) -> bool:
    return validate_candidate_only_handoff(handoff)


def validate_trace_completeness(output: DecisionGovernanceOutputV1) -> bool:
    trace = output.trace_candidate
    return (
        bool(trace.decision_candidate_refs)
        and bool(trace.intent_refs)
        and bool(trace.causal_refs)
        and bool(trace.constraint_refs)
        and bool(trace.risk_refs)
        and bool(trace.utility_refs)
        and bool(trace.permission_refs)
        and bool(trace.safety_refs)
        and bool(trace.resource_state_refs)
        and bool(trace.selection_or_nonselection_reason_refs)
        and bool(trace.state_transition_refs)
        and bool(trace.provenance)
    )


def validate_no_runtime_side_effects(output: DecisionGovernanceOutputV1) -> bool:
    return (
        output.candidate_only is True
        and output.decision_output is False
        and output.action_output is False
        and output.task_output is False
        and output.runtime_executed is False
        and output.database_write_executed is False
        and output.source_mutation_executed is False
        and output.fabricated_confirmation is False
    )


def validate_negative_guard_flags() -> bool:
    return all(NEGATIVE_GUARD_FLAGS.values())
