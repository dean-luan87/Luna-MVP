"""Static and contract validators for Causal Governance outputs."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.causal_governance.causal_core_types_v1 import (
    CausalHypothesisCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.causal_governance.causal_counterfactual_types_v1 import (
    CounterfactualCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_handoff_types_v1 import (
    CausalToDecisionHandoffCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_io_types_v1 import (
    CausalGovernanceOutputV1,
)
from capabilities.midplatform.core.causal_governance.causal_ownership_guard_v1 import (
    validate_candidate_only_handoff,
    validate_canonical_owner,
    validate_forbidden_authority_tokens,
    validate_ref_read_only,
)
from capabilities.midplatform.core.causal_governance.causal_registry_v1 import (
    NEGATIVE_GUARD_FLAGS,
    STATE_SET,
)


def validate_input_refs_read_only(all_refs: Iterable[SourceRefV1]) -> bool:
    return validate_ref_read_only(all_refs) and validate_forbidden_authority_tokens(
        all_refs
    )


def validate_hypothesis_candidates(
    items: Iterable[CausalHypothesisCandidateV1],
) -> bool:
    return all(
        validate_canonical_owner(item.owner)
        and item.candidate_kind == "CAUSAL_HYPOTHESIS_CANDIDATE"
        and item.state_candidate in STATE_SET
        and bool(item.provenance)
        and bool(item.temporal_order_refs)
        and item.decision_authority is False
        and item.action_authority is False
        and item.task_authority is False
        for item in items
    )


def validate_counterfactual_candidates(
    items: Iterable[CounterfactualCandidateV1],
) -> bool:
    return all(
        item.counterfactual_is_fact is False
        and item.counterfactual_is_decision is False
        and item.counterfactual_outputs_action is False
        for item in items
    )


def validate_trace_completeness(output: CausalGovernanceOutputV1) -> bool:
    trace = output.trace_candidate
    return (
        bool(trace.hypothesis_refs)
        and bool(trace.evidence_refs)
        and bool(trace.provenance)
        and bool(trace.temporal_order_refs)
        and bool(trace.context_refs)
        and bool(trace.admission_steps)
        and bool(trace.handoff_refs)
    )


def validate_handoff(handoff: CausalToDecisionHandoffCandidateV1) -> bool:
    return validate_candidate_only_handoff(handoff)


def validate_no_runtime_side_effects(output: CausalGovernanceOutputV1) -> bool:
    return (
        output.candidate_only is True
        and output.decision_output is False
        and output.action_output is False
        and output.task_output is False
        and output.runtime_executed is False
        and output.source_mutation_executed is False
    )


def validate_negative_guard_flags() -> bool:
    return all(NEGATIVE_GUARD_FLAGS.values())
