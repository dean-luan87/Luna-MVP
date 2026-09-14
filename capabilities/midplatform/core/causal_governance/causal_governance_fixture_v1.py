"""Synthetic fixtures for Causal Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.causal_governance.causal_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.causal_governance.causal_io_types_v1 import (
    CausalGovernanceInputV1,
)


@dataclass(frozen=True)
class CausalFixtureCaseV1:
    case_id: str
    description: str
    request: CausalGovernanceInputV1
    expected_state: str
    expected_hypothesis_count: int
    expected_guard_tokens: Tuple[str, ...]
    expected_handoff_eligible: bool
    synthetic_only: bool = True


def _ref(owner: str, ref_id: str, ref_type: str = "REFERENCE") -> SourceRefV1:
    return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _mk_case(
    case_id: str,
    desc: str,
    hypotheses: Tuple[str, ...],
    support: Tuple[str, ...],
    opposition: Tuple[str, ...],
    confounders: Tuple[str, ...],
    unknowns: Tuple[str, ...],
    expected_state: str,
    guard_tokens: Tuple[str, ...],
    handoff: bool,
    counterfactual: bool = False,
) -> CausalFixtureCaseV1:
    request = CausalGovernanceInputV1(
        scenario_id=case_id,
        hypothesis_candidates=hypotheses,
        target_event_refs=(_ref("Observation Governance", f"event:{case_id}"),),
        cause_candidate_refs=(_ref("Observation Governance", f"cause:{case_id}"),),
        supporting_evidence_refs=tuple(
            _ref("Observation Governance", f"support:{case_id}:{idx}", "EVIDENCE")
            for idx, _ in enumerate(support, start=1)
        ),
        opposing_evidence_refs=tuple(
            _ref("Observation Governance", f"oppose:{case_id}:{idx}", "EVIDENCE")
            for idx, _ in enumerate(opposition, start=1)
        ),
        confounder_refs=tuple(
            _ref("Context Governance", f"conf:{case_id}:{idx}", "CONFOUNDER")
            for idx, _ in enumerate(confounders, start=1)
        ),
        temporal_order_refs=(
            _ref("Context Governance", f"temporal:{case_id}", "TEMPORAL"),
        ),
        context_refs=(_ref("Context Governance", f"ctx:{case_id}", "CONTEXT"),),
        prior_refs=(_ref("Memory Governance", f"prior:{case_id}", "PRIOR"),),
        intent_refs=(_ref("Intent Governance", f"intent:{case_id}", "INTENT"),),
        influence_refs=(
            _ref("Cognitive Field", f"field:{case_id}", "FIELD_INFLUENCE"),
        ),
        correlation_signal_refs=(
            _ref("Observation Governance", f"corr:{case_id}", "CORRELATION"),
        ),
        unknowns=unknowns,
        counterfactual_requested=counterfactual,
        synthetic_only=True,
        candidate_only=True,
    )
    return CausalFixtureCaseV1(
        case_id=case_id,
        description=desc,
        request=request,
        expected_state=expected_state,
        expected_hypothesis_count=len(hypotheses),
        expected_guard_tokens=guard_tokens,
        expected_handoff_eligible=handoff,
    )


def get_causal_synthetic_fixtures_v1() -> Tuple[CausalFixtureCaseV1, ...]:
    return (
        _mk_case(
            "C01_TEMPORAL_PRECEDENCE_NO_CAUSALITY",
            "temporal precedence without causality promotion",
            ("A may influence B",),
            ("sequence_ref",),
            ("missing_mechanism_ref",),
            ("hidden_driver_candidate",),
            ("mechanism_unknown",),
            "INSUFFICIENT_EVIDENCE",
            ("temporal_precedence_not_causality",),
            True,
        ),
        _mk_case(
            "C02_STRONG_ASSOCIATION_UNRESOLVED_CAUSE",
            "correlation remains unresolved",
            ("H1", "H2"),
            ("association_ref",),
            ("missing_intervention_ref",),
            ("sampling_bias_candidate",),
            ("causal_direction_unknown",),
            "CONTESTED",
            ("correlation_not_causality",),
            True,
        ),
        _mk_case(
            "C03_TWO_COMPETING_HYPOTHESES",
            "multiple competing hypotheses",
            ("H1", "H2"),
            ("support_h1", "support_h2"),
            ("oppose_h1", "oppose_h2"),
            (),
            ("winner_not_determined",),
            "CONTESTED",
            ("multi_hypothesis",),
            True,
        ),
        _mk_case(
            "C04_THIRD_VARIABLE_CONFOUNDER",
            "third-variable confounder",
            ("A->B", "C->A_and_B"),
            ("A_B_association",),
            ("C_presence_ref",),
            ("C",),
            ("confounder_strength_unknown",),
            "CONTESTED",
            ("confounder_candidate",),
            True,
        ),
        _mk_case(
            "C05_SUPPORTING_EVIDENCE_ACCUMULATION",
            "support accumulation keeps candidate status",
            ("H1",),
            ("s1", "s2", "s3"),
            ("weak_o1",),
            (),
            ("residual_unknown",),
            "SUPPORTED",
            ("candidate_not_fact",),
            True,
        ),
        _mk_case(
            "C06_OPPOSING_EVIDENCE",
            "opposition causes contest",
            ("H1",),
            ("s_old",),
            ("o_new",),
            ("measurement_noise_candidate",),
            ("support_opposition_conflict",),
            "CONTESTED",
            ("opposition_preserved",),
            True,
        ),
        _mk_case(
            "C07_HYPOTHESIS_REVISION",
            "revision trace required",
            ("H1_rev1", "H1_rev2"),
            ("s_new",),
            ("o_old",),
            ("context_shift_candidate",),
            ("revision_effect_unknown",),
            "REVISED",
            ("revision_preserved",),
            True,
        ),
        _mk_case(
            "C08_REVOKED_EVIDENCE",
            "revoked evidence drives revocation",
            ("H1",),
            ("s_invalidated",),
            ("revocation_ref",),
            (),
            ("post_revocation_gap",),
            "REVOKED",
            ("revocation_preserved",),
            True,
        ),
        _mk_case(
            "C09_MEMORY_PRIOR_INFLUENCE_NO_AUTHORITY",
            "memory prior influence only",
            ("H1",),
            ("prior_match",),
            ("new_counter_example",),
            ("recall_bias_candidate",),
            ("prior_bias",),
            "CONTESTED",
            ("memory_prior_not_causal_fact",),
            True,
        ),
        _mk_case(
            "C10_INTENT_INFLUENCE_NO_AUTHORITY",
            "intent influence without authority",
            ("H1",),
            ("intent_alignment_ref",),
            ("evidence_mismatch_ref",),
            ("preference_bias_candidate",),
            ("intent_direction_vs_cause_gap",),
            "CONTESTED",
            ("intent_preference_not_causal_conclusion",),
            True,
        ),
        _mk_case(
            "C11_COUNTERFACTUAL_CANDIDATE",
            "counterfactual remains candidate",
            ("H1", "CF_H1"),
            ("baseline_refs",),
            ("counter_evidence_refs",),
            ("intervention_feasibility_candidate",),
            ("counterfactual_assumption_gap",),
            "CONTESTED",
            ("counterfactual_candidate_only",),
            True,
            counterfactual=True,
        ),
        _mk_case(
            "C12_CAUSAL_TO_DECISION_CANDIDATE_HANDOFF",
            "candidate handoff to decision",
            ("H1", "H2"),
            ("s1", "s2"),
            ("o1",),
            ("c1",),
            ("conflict_unresolved",),
            "CONTESTED",
            ("handoff_candidate_only",),
            True,
        ),
    )
