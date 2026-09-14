"""Synthetic fixtures for Decision Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionOptionCandidateV1,
    RiskCandidateV1,
    SourceRefV1,
    UtilityCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_io_types_v1 import (
    DecisionGovernanceInputV1,
)


@dataclass(frozen=True)
class DecisionFixtureCaseV1:
    case_id: str
    description: str
    request: DecisionGovernanceInputV1
    expected_state: str
    expected_outcome_kind: str
    expected_selected_option: Optional[str]
    expected_handoff_eligible: bool
    expected_negative_guards: Tuple[str, ...]
    synthetic_only: bool = True


def _ref(owner: str, ref_id: str, ref_type: str = "REFERENCE") -> SourceRefV1:
    return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _opt(
    option_id: str,
    benefit: int,
    severity: int,
    likelihood: int,
    cost: int,
    hard_constraints_ok: bool,
    permission_allowed: bool,
    safety_allowed: bool,
    role_allowed: bool,
    reversibility: str,
    intent_alignment: int,
    evidence_ready: bool = True,
) -> DecisionOptionCandidateV1:
    return DecisionOptionCandidateV1(
        option_id=option_id,
        option_statement=f"option:{option_id}",
        utility=UtilityCandidateV1(
            utility_ref_id=f"utility:{option_id}",
            expected_benefit=benefit,
            tradeoff_notes=("candidate_only",),
            uncertainty=("utility_is_soft_preference",),
            provenance=(f"prov:{option_id}:utility",),
        ),
        risk=RiskCandidateV1(
            risk_ref_id=f"risk:{option_id}",
            severity=severity,
            likelihood=likelihood,
            unknowns=("risk_is_not_safety_authority",),
            provenance=(f"prov:{option_id}:risk",),
        ),
        cost=cost,
        hard_constraints_ok=hard_constraints_ok,
        permission_allowed=permission_allowed,
        safety_allowed=safety_allowed,
        role_allowed=role_allowed,
        reversibility=reversibility,
        intent_alignment=intent_alignment,
        evidence_ready=evidence_ready,
    )


def _mk(
    case_id: str,
    description: str,
    options: Tuple[DecisionOptionCandidateV1, ...],
    expected_state: str,
    expected_outcome_kind: str,
    expected_selected_option: Optional[str],
    expected_handoff_eligible: bool,
    expected_negative_guards: Tuple[str, ...],
    causal_uncertainty_level: str = "LOW",
    competing_causal_hypotheses: bool = False,
    resource_pressure_level: str = "NORMAL",
    evidence_count: int = 2,
    intent_preferred_option_ids: Tuple[str, ...] = (),
    human_confirmation_available: bool = False,
    requires_candidate_only_handoff: bool = False,
) -> DecisionFixtureCaseV1:
    evidence_refs = tuple(
        _ref("Observation Governance", f"evidence:{case_id}:{idx}", "EVIDENCE")
        for idx in range(1, evidence_count + 1)
    )
    request = DecisionGovernanceInputV1(
        scenario_id=case_id,
        intent_refs=(_ref("Intent Governance", f"intent:{case_id}", "INTENT"),),
        causal_refs=(_ref("Causal Governance", f"causal:{case_id}", "CAUSAL"),),
        context_refs=(_ref("Context Governance", f"context:{case_id}", "CONTEXT"),),
        field_refs=(_ref("Cognitive Field", f"field:{case_id}", "FIELD"),),
        role_refs=(_ref("Role Governance", f"role:{case_id}", "ROLE"),),
        permission_refs=(
            _ref("Permission Governance", f"permission:{case_id}", "PERMISSION"),
        ),
        safety_refs=(_ref("Safety Governance", f"safety:{case_id}", "SAFETY"),),
        resource_refs=(_ref("Resource Governance", f"resource:{case_id}", "RESOURCE"),),
        constraint_refs=(
            _ref("Constraint Governance", f"constraint:{case_id}", "CONSTRAINT"),
        ),
        evidence_refs=evidence_refs,
        options=options,
        intent_preferred_option_ids=intent_preferred_option_ids,
        causal_uncertainty_level=causal_uncertainty_level,
        competing_causal_hypotheses=competing_causal_hypotheses,
        resource_pressure_level=resource_pressure_level,
        human_confirmation_available=human_confirmation_available,
        synthetic_only=True,
        candidate_only=True,
    )
    # Reuse read-only field by encoding handoff intent inside scenario id token.
    if requires_candidate_only_handoff:
        request = DecisionGovernanceInputV1(
            **{**request.__dict__, "scenario_id": f"{case_id}__HANDOFF"}
        )
    return DecisionFixtureCaseV1(
        case_id=case_id,
        description=description,
        request=request,
        expected_state=expected_state,
        expected_outcome_kind=expected_outcome_kind,
        expected_selected_option=expected_selected_option,
        expected_handoff_eligible=expected_handoff_eligible,
        expected_negative_guards=expected_negative_guards,
    )


def get_decision_synthetic_fixtures_v1() -> Tuple[DecisionFixtureCaseV1, ...]:
    return (
        _mk(
            "D01_LOW_RISK_SINGLE_CANDIDATE",
            "single low-risk selectable candidate",
            options=(
                _opt("opt_d01", 80, 1, 1, 2, True, True, True, True, "REVERSIBLE", 3),
            ),
            expected_state="SELECTED_CANDIDATE",
            expected_outcome_kind="SELECTED",
            expected_selected_option="opt_d01",
            expected_handoff_eligible=True,
            expected_negative_guards=("preferred_candidate_not_executable_action",),
        ),
        _mk(
            "D02_TWO_CANDIDATE_COEXISTENCE",
            "multi candidate coexistence preserved without forced winner",
            options=(
                _opt("opt_d02_a", 70, 2, 2, 3, True, True, True, True, "REVERSIBLE", 2),
                _opt("opt_d02_b", 69, 2, 2, 3, True, True, True, True, "REVERSIBLE", 2),
            ),
            expected_state="CONTESTED",
            expected_outcome_kind="CONTESTED",
            expected_selected_option=None,
            expected_handoff_eligible=False,
            expected_negative_guards=("no_forced_selection",),
            competing_causal_hypotheses=True,
        ),
        _mk(
            "D03_HIGH_UTILITY_PERMISSION_DENIED",
            "high utility candidate blocked by permission veto",
            options=(
                _opt("opt_d03", 95, 1, 1, 2, True, False, True, True, "REVERSIBLE", 3),
            ),
            expected_state="CONSTRAINED",
            expected_outcome_kind="CONSTRAINED",
            expected_selected_option=None,
            expected_handoff_eligible=False,
            expected_negative_guards=("no_permission_bypass",),
        ),
        _mk(
            "D04_HIGH_UTILITY_SAFETY_VETO",
            "high utility candidate blocked by safety veto",
            options=(
                _opt("opt_d04", 93, 1, 1, 2, True, True, False, True, "REVERSIBLE", 3),
            ),
            expected_state="CONSTRAINED",
            expected_outcome_kind="CONSTRAINED",
            expected_selected_option=None,
            expected_handoff_eligible=False,
            expected_negative_guards=("no_safety_bypass",),
        ),
        _mk(
            "D05_CAUSAL_UNCERTAINTY_DEFER",
            "high causal uncertainty triggers defer",
            options=(
                _opt("opt_d05", 80, 2, 2, 2, True, True, True, True, "REVERSIBLE", 2),
            ),
            expected_state="DEFERRED",
            expected_outcome_kind="DEFER",
            expected_selected_option=None,
            expected_handoff_eligible=False,
            expected_negative_guards=("causal_not_decision",),
            causal_uncertainty_level="HIGH",
        ),
        _mk(
            "D06_EVIDENCE_GAP_REQUEST_MORE",
            "insufficient evidence triggers request more evidence",
            options=(
                _opt("opt_d06", 78, 2, 2, 2, True, True, True, True, "REVERSIBLE", 2),
            ),
            expected_state="NEEDS_MORE_EVIDENCE",
            expected_outcome_kind="REQUEST_MORE_EVIDENCE",
            expected_selected_option=None,
            expected_handoff_eligible=False,
            expected_negative_guards=("no_fabricated_confirmation",),
            evidence_count=0,
        ),
        _mk(
            "D07_NO_ACCEPTABLE_OPTION_ABSTAIN",
            "all options violate hard constraints, abstain",
            options=(
                _opt(
                    "opt_d07_a", 88, 2, 2, 2, False, True, True, True, "REVERSIBLE", 3
                ),
                _opt(
                    "opt_d07_b", 85, 2, 2, 2, False, True, True, True, "REVERSIBLE", 2
                ),
            ),
            expected_state="ABSTAINED",
            expected_outcome_kind="ABSTAIN",
            expected_selected_option=None,
            expected_handoff_eligible=False,
            expected_negative_guards=("hard_constraints_before_soft_preferences",),
        ),
        _mk(
            "D08_REVERSIBLE_CANDIDATE",
            "reversible candidate remains eligible",
            options=(
                _opt("opt_d08", 76, 2, 2, 2, True, True, True, True, "REVERSIBLE", 2),
            ),
            expected_state="ELIGIBLE",
            expected_outcome_kind="ELIGIBLE",
            expected_selected_option="opt_d08",
            expected_handoff_eligible=True,
            expected_negative_guards=("decision_not_action",),
        ),
        _mk(
            "D09_IRREVERSIBLE_CONFIRMATION_REQUIRED",
            "irreversible candidate requires confirmation",
            options=(
                _opt("opt_d09", 90, 3, 3, 3, True, True, True, True, "IRREVERSIBLE", 3),
            ),
            expected_state="NEEDS_CONFIRMATION",
            expected_outcome_kind="CONFIRMATION_REQUIRED",
            expected_selected_option="opt_d09",
            expected_handoff_eligible=False,
            expected_negative_guards=("no_fabricated_confirmation",),
            human_confirmation_available=False,
        ),
        _mk(
            "D10_RESOURCE_CONSTRAINT_LOWER_COST",
            "resource pressure prefers lower cost option",
            options=(
                _opt(
                    "opt_d10_high", 88, 2, 2, 9, True, True, True, True, "REVERSIBLE", 2
                ),
                _opt(
                    "opt_d10_low", 74, 1, 2, 2, True, True, True, True, "REVERSIBLE", 1
                ),
            ),
            expected_state="ELIGIBLE",
            expected_outcome_kind="ELIGIBLE",
            expected_selected_option="opt_d10_low",
            expected_handoff_eligible=True,
            expected_negative_guards=("resource_degradation",),
            resource_pressure_level="DEGRADED",
        ),
        _mk(
            "D11_ROLE_CONSTRAINT_ELIGIBILITY_SHIFT",
            "role constraints alter option eligibility",
            options=(
                _opt(
                    "opt_d11_role_blocked",
                    82,
                    2,
                    2,
                    2,
                    True,
                    True,
                    True,
                    False,
                    "REVERSIBLE",
                    2,
                ),
                _opt(
                    "opt_d11_role_ok",
                    70,
                    2,
                    2,
                    2,
                    True,
                    True,
                    True,
                    True,
                    "REVERSIBLE",
                    1,
                ),
            ),
            expected_state="CONSTRAINED",
            expected_outcome_kind="CONSTRAINED",
            expected_selected_option="opt_d11_role_ok",
            expected_handoff_eligible=True,
            expected_negative_guards=("role_influence_not_owner",),
        ),
        _mk(
            "D12_INTENT_PREFERENCE_NO_OVERRULE",
            "intent preference cannot over-authorize blocked option",
            options=(
                _opt(
                    "opt_d12_pref_blocked",
                    96,
                    1,
                    1,
                    3,
                    True,
                    False,
                    True,
                    True,
                    "REVERSIBLE",
                    4,
                ),
                _opt(
                    "opt_d12_safe", 72, 2, 2, 2, True, True, True, True, "REVERSIBLE", 1
                ),
            ),
            expected_state="CONSTRAINED",
            expected_outcome_kind="CONSTRAINED",
            expected_selected_option="opt_d12_safe",
            expected_handoff_eligible=True,
            expected_negative_guards=("intent_not_decision",),
            intent_preferred_option_ids=("opt_d12_pref_blocked",),
        ),
        _mk(
            "D13_COMPETING_CAUSAL_HYPOTHESES",
            "competing causal hypotheses keep decision contested",
            options=(
                _opt("opt_d13_a", 79, 2, 2, 2, True, True, True, True, "REVERSIBLE", 2),
                _opt("opt_d13_b", 78, 2, 2, 2, True, True, True, True, "REVERSIBLE", 2),
            ),
            expected_state="CONTESTED",
            expected_outcome_kind="CONTESTED",
            expected_selected_option=None,
            expected_handoff_eligible=False,
            expected_negative_guards=("causal_not_decision",),
            competing_causal_hypotheses=True,
        ),
        _mk(
            "D14_DECISION_TO_ACTION_TASK_CANDIDATE_ONLY",
            "handoff remains candidate-only without execution",
            options=(
                _opt("opt_d14", 84, 1, 1, 2, True, True, True, True, "REVERSIBLE", 2),
            ),
            expected_state="SELECTED_CANDIDATE",
            expected_outcome_kind="SELECTED",
            expected_selected_option="opt_d14",
            expected_handoff_eligible=True,
            expected_negative_guards=("decision_layer_not_action_executor",),
            requires_candidate_only_handoff=True,
        ),
    )
