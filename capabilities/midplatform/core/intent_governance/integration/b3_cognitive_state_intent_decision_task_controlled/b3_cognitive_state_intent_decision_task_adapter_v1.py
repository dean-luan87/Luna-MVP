"""Narrow B2-reference to existing Intent, Decision and Task owners."""

from __future__ import annotations

from typing import Iterable, Mapping, Tuple

from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionOptionCandidateV1,
    RiskCandidateV1,
    SourceRefV1 as DecisionSourceRefV1,
    UtilityCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_io_types_v1 import (
    DecisionGovernanceInputV1,
)
from capabilities.midplatform.core.intent_governance.intent_core_types_v1 import (
    SourceRefV1 as IntentSourceRefV1,
)
from capabilities.midplatform.core.intent_governance.intent_io_types_v1 import (
    IntentGovernanceInputV1,
    IntentGovernanceOutputV1,
)
from capabilities.midplatform.core.intent_governance.intent_governance_skeleton_v1 import (
    IntentGovernanceSkeletonV1,
)
from capabilities.midplatform.core.decision_governance.decision_governance_engine_v1 import (
    DecisionGovernanceEngineV1,
)
from capabilities.midplatform.core.task_manager_skeleton_v1 import (
    build_task_candidate,
    classify_task_readiness,
)

from .b3_cognitive_state_intent_decision_task_types_v1 import (
    B2CognitiveStateFlowReferenceV1,
    B3TaskBridgeInputV1,
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value)))


def _intent_ref(owner: str, ref_id: str, ref_type: str) -> IntentSourceRefV1:
    return IntentSourceRefV1(
        owner=owner,
        ref_id=ref_id,
        ref_type=ref_type,
        read_only=True,
        reference_only=True,
        source_mutation_allowed=False,
    )


def _decision_ref(owner: str, ref_id: str, ref_type: str) -> DecisionSourceRefV1:
    return DecisionSourceRefV1(
        owner=owner,
        ref_id=ref_id,
        ref_type=ref_type,
        read_only=True,
        reference_only=True,
        source_mutation_allowed=False,
    )


def validate_b2_reference(source: B2CognitiveStateFlowReferenceV1) -> Tuple[str, ...]:
    issues = []
    required = {
        "cognitive_state_ref": source.cognitive_state_ref,
        "cognitive_flow_ref": source.cognitive_flow_ref,
        "current_world_ref": source.current_world_ref,
        "trace_ref": source.trace_ref,
    }
    issues.extend(name for name, value in required.items() if not str(value).strip())
    if not source.candidate_only:
        issues.append("b2_reference_not_candidate_only")
    if not source.read_only:
        issues.append("b2_reference_not_read_only")
    if source.source_mutation_executed:
        issues.append("b2_source_mutation_present")
    if source.provider_invocation:
        issues.append("b2_provider_invocation_present")
    if not source.context_refs:
        issues.append("missing_context_reference")
    if not source.provenance_refs or not source.temporal_refs:
        issues.append("missing_lineage_reference")
    return tuple(issues)


def build_intent_input(
    source: B2CognitiveStateFlowReferenceV1,
    *,
    intent_scenario_id: str,
) -> IntentGovernanceInputV1:
    source_refs = (
        _intent_ref("Cognitive State Formation Governance", source.cognitive_state_ref, "COGNITIVE_STATE"),
        _intent_ref("Cognitive Flow Governance", source.cognitive_flow_ref, "COGNITIVE_FLOW"),
        *(_intent_ref("Cognitive Attention Governance", ref, "ATTENTION") for ref in source.attention_refs),
        *(_intent_ref("Cognitive Hypothesis Governance", ref, "HYPOTHESIS") for ref in source.hypothesis_refs),
        *(_intent_ref("Observation Control Governance", ref, "OBSERVATION_NEED") for ref in source.observation_need_refs),
    )
    context_refs = tuple(
        _intent_ref("Context Foundation", ref, "CONTEXT") for ref in source.context_refs
    )
    pcn_refs = tuple(
        _intent_ref("Personal Cognitive Network Governance", ref, "PCN")
        for ref in source.pcn_refs
    )
    return IntentGovernanceInputV1(
        scenario_id=intent_scenario_id,
        context_refs=context_refs,
        pcn_refs=pcn_refs,
        source_refs=source_refs,
        field_refs=tuple(
            _intent_ref("Field State Reducer", ref, "FIELD") for ref in source.field_refs
        ),
        unknowns=_unique((*source.uncertainty_refs, *source.conflict_refs)),
        synthetic_only=True,
        candidate_only=True,
    )


def build_decision_option(
    case_id: str,
    *,
    permission_allowed: bool = True,
    safety_allowed: bool = True,
    hard_constraints_ok: bool = True,
    evidence_ready: bool = True,
    reversibility: str = "REVERSIBLE",
) -> DecisionOptionCandidateV1:
    option_id = f"option:{case_id}"
    return DecisionOptionCandidateV1(
        option_id=option_id,
        option_statement=f"candidate_option:{case_id}",
        utility=UtilityCandidateV1(
            utility_ref_id=f"utility:{case_id}",
            expected_benefit=90,
            tradeoff_notes=("candidate_only",),
            uncertainty=("utility_is_soft_preference",),
            provenance=(f"provenance:{case_id}:utility",),
        ),
        risk=RiskCandidateV1(
            risk_ref_id=f"risk:{case_id}",
            severity=1,
            likelihood=1,
            unknowns=("risk_is_not_safety_authority",),
            provenance=(f"provenance:{case_id}:risk",),
        ),
        cost=2,
        hard_constraints_ok=hard_constraints_ok,
        permission_allowed=permission_allowed,
        safety_allowed=safety_allowed,
        role_allowed=True,
        reversibility=reversibility,
        intent_alignment=3,
        evidence_ready=evidence_ready,
    )


def build_decision_input(
    source: B2CognitiveStateFlowReferenceV1,
    intent_output: IntentGovernanceOutputV1,
    *,
    case_id: str,
    option: DecisionOptionCandidateV1,
    high_uncertainty: bool = False,
    competing_hypotheses: bool = False,
    resource_pressure_level: str = "NORMAL",
    no_evidence: bool = False,
) -> DecisionGovernanceInputV1:
    intent_refs = tuple(
        _decision_ref("Intent Governance", candidate.intent_id, "INTENT_CANDIDATE")
        for candidate in intent_output.intent_candidates
    )
    evidence_refs = () if no_evidence else tuple(
        _decision_ref("Observation Governance", ref, "EVIDENCE")
        for ref in source.provenance_refs[:2]
    )
    scenario_id = f"{case_id}__HANDOFF" if not no_evidence and not high_uncertainty and not competing_hypotheses else case_id
    return DecisionGovernanceInputV1(
        scenario_id=scenario_id,
        intent_refs=intent_refs,
        causal_refs=(
            _decision_ref(
                "Cognitive Flow Governance",
                source.cognitive_flow_ref,
                "COGNITIVE_FLOW",
            ),
        ),
        context_refs=tuple(
            _decision_ref("Context Foundation", ref, "CONTEXT") for ref in source.context_refs
        ),
        field_refs=tuple(
            _decision_ref("Field State Reducer", ref, "FIELD") for ref in source.field_refs
        ),
        role_refs=(),
        permission_refs=(_decision_ref("Permission Governance", f"permission:{case_id}", "PERMISSION"),),
        safety_refs=(_decision_ref("Safety Governance", f"safety:{case_id}", "SAFETY"),),
        resource_refs=(_decision_ref("Resource Governance", f"resource:{case_id}", "RESOURCE"),),
        constraint_refs=(_decision_ref("Constraint Governance", f"constraint:{case_id}", "CONSTRAINT"),),
        evidence_refs=evidence_refs,
        options=(option,),
        causal_uncertainty_level="HIGH" if high_uncertainty else "LOW",
        competing_causal_hypotheses=competing_hypotheses,
        resource_pressure_level=resource_pressure_level,
        human_confirmation_available=False,
        synthetic_only=True,
        candidate_only=True,
    )


def build_task_bridge_input(
    source: B2CognitiveStateFlowReferenceV1,
    decision_output,
    *,
    case_id: str,
    observation_required: bool = False,
) -> B3TaskBridgeInputV1:
    selected = decision_output.selection_candidate.selected_candidate_ref
    blocked = () if selected else (f"decision_block:{case_id}",)
    return B3TaskBridgeInputV1(
        candidate_id=selected or f"decision:none:{case_id}",
        source_decision_ref=selected or f"decision:none:{case_id}",
        source_health_refs=(),
        task_context_refs=tuple((*source.context_refs, source.current_world_ref)),
        required_observation_refs=source.observation_need_refs if observation_required else (),
        decision_block_refs=blocked,
        task_summary=f"candidate_task:{case_id}",
        trace_ref=f"trace:{case_id}:task",
        governance_ref=f"governance:{case_id}",
    )


def run_intent(source: B2CognitiveStateFlowReferenceV1, intent_scenario_id: str) -> IntentGovernanceOutputV1:
    return IntentGovernanceSkeletonV1().run_case(
        build_intent_input(source, intent_scenario_id=intent_scenario_id)
    )


def run_decision(request: DecisionGovernanceInputV1):
    return DecisionGovernanceEngineV1().run_case(request)


def build_task_candidates(task_input: B3TaskBridgeInputV1):
    readiness = classify_task_readiness(
        task_input,
        decision_refs=task_input.decision_block_refs,
        governance_ref=task_input.governance_ref,
    )
    candidate = build_task_candidate(task_input, readiness, task_input.governance_ref)
    return readiness, candidate
