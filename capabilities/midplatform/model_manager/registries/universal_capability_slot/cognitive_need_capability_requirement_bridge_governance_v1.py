"""Controlled Need -> CapabilityRequirement formation and replanning."""

from __future__ import annotations

from typing import Iterable, Optional, Tuple

from .cognitive_need_capability_requirement_bridge_types_v1 import (
    CapabilityRequirementFormationCandidateV1,
    CognitiveNeedCandidateV1,
    CognitiveNextStepAssessmentV1,
    CognitiveNeedReplanningCandidateV1,
)
from .universal_capability_slot_types_v1 import (
    CapabilityGapCandidateV1,
    CapabilityModuleV1,
    CapabilityRequirementV1,
    CapabilityResolutionCandidateV1,
    CapabilityScopeAssessmentV1,
)


URGENCY_VALUES = ("LOW", "NORMAL", "HIGH", "SAFETY_PRIORITY")
SAFETY_RELEVANCE_VALUES = ("NONE", "RELEVANT", "CRITICAL")
EVIDENCE_AUTHORITY = "EVIDENCE_ONLY"
CURRENT_MINIMUM_NEED = "CURRENT_MINIMUM_NECESSARY_NEED"
SUFFICIENCY_STATUSES = ("SUFFICIENT", "PARTIAL", "INSUFFICIENT", "UNKNOWN")
CONTINUATION_DISPOSITIONS = ("STOP_SUFFICIENT", "CONTINUE", "REOBSERVE", "REPLAN", "DEFER")
REQUIREMENT_DISPOSITIONS = ("STILL_RELEVANT", "SATISFIED", "OBSOLETE", "SUPERSEDED", "REPLANNING_REQUIRED")
REPLANNING_RESULTS = {
    "OUT_OF_CAPABILITY_SCOPE",
    "PROBLEM_CLASS_UNSUPPORTED",
    "OPERATION_UNSUPPORTED",
    "INPUT_CONTRACT_UNSUPPORTED",
    "OUTPUT_CONTRACT_UNSUPPORTED",
    "AUTHORITY_NOT_ALLOWED",
    "CAPABILITY_MODULE_NOT_REGISTERED",
    "MODULE_LIFECYCLE_INCOMPATIBLE",
    "MODULE_LIFECYCLE_UNAVAILABLE",
    "MODULE_NOT_BOUND_TO_SLOT",
    "PERMISSION_BLOCKED",
    "RESOURCE_BLOCKED",
    "CAPABILITY_SUSPENDED",
    "CAPABILITY_DEGRADED_REQUIRES_GOVERNED_USE",
    "IMPLEMENTATION_REFERENCE_MISSING",
}


def validate_cognitive_need(need: CognitiveNeedCandidateV1) -> Tuple[str, ...]:
    issues = []
    if not need.need_id:
        issues.append("missing_need_id")
    if not need.problem_description:
        issues.append("missing_problem_description")
    if not need.missing_information_class:
        issues.append("missing_information_class")
    if not need.required_evidence_class:
        issues.append("missing_required_evidence_class")
    if need.urgency not in URGENCY_VALUES:
        issues.append("unsupported_urgency")
    if need.safety_relevance not in SAFETY_RELEVANCE_VALUES:
        issues.append("unsupported_safety_relevance")
    if not need.candidate_only:
        issues.append("need_not_candidate_only")
    if need.materialization_status != CURRENT_MINIMUM_NEED:
        issues.append("need_not_current_minimum")
    if not need.state_version_ref:
        issues.append("missing_state_version_ref")
    return tuple(issues)


def form_capability_requirement(
    need: CognitiveNeedCandidateV1,
    *,
    formation_id: str,
    problem_class: str,
    requested_operation: str,
    input_contract_ref: str,
    output_contract_ref: str,
    requirement_type: str,
    task_context: str,
    required_semantic_depth: str = "MINIMAL",
    requested_module_id: Optional[str] = None,
    permission_refs: Iterable[str] = (),
    resource_refs: Iterable[str] = (),
    execution_boundary_ref: str = "Capability Governance -> existing execution boundary",
) -> CapabilityRequirementFormationCandidateV1:
    issues = validate_cognitive_need(need)
    if issues:
        raise ValueError("invalid cognitive need: " + ",".join(issues))
    if not problem_class or not requested_operation or not input_contract_ref or not output_contract_ref:
        raise ValueError("minimum sufficient requirement fields are required")
    requirement = CapabilityRequirementV1(
        requirement_id=f"requirement:{formation_id}",
        requested_module_id=requested_module_id,
        purpose=problem_class,
        task_context=task_context,
        required_semantic_depth=required_semantic_depth,
        permission_refs=tuple(permission_refs),
        resource_refs=tuple(resource_refs),
        execution_boundary_ref=execution_boundary_ref,
        requester_ref=need.source_intent_ref,
        requirement_type=requirement_type,
        problem_class=problem_class,
        requested_operation=requested_operation,
        input_contract_ref=input_contract_ref,
        expected_output_contract_ref=output_contract_ref,
        required_authority=EVIDENCE_AUTHORITY,
        task_context_refs=tuple(
            ref for ref in (need.source_context_ref, need.source_field_ref, need.source_attention_ref) if ref
        ),
        trace_ref=need.trace_ref,
    )
    return CapabilityRequirementFormationCandidateV1(
        formation_id=formation_id,
        source_need_ref=need.need_id,
        requirement_ref=requirement.requirement_id,
        requirement=requirement,
        selected_problem_class=problem_class,
        requested_operation=requested_operation,
        input_contract_ref=input_contract_ref,
        output_contract_ref=output_contract_ref,
        required_authority=EVIDENCE_AUTHORITY,
        requirement_minimized=True,
        trace_ref=need.trace_ref,
        source_state_version_ref=need.state_version_ref,
    )


def replan_after_capability_result(
    formation: CapabilityRequirementFormationCandidateV1,
    *,
    scope_assessment: Optional[CapabilityScopeAssessmentV1] = None,
    resolution: Optional[CapabilityResolutionCandidateV1] = None,
    capability_gap: Optional[CapabilityGapCandidateV1] = None,
    refined_need_ref: Optional[str] = None,
    decomposed_need_refs: Iterable[str] = (),
    alternative_requirement_refs: Iterable[str] = (),
    prior_requirement_disposition: str = "REPLANNING_REQUIRED",
) -> CognitiveNeedReplanningCandidateV1:
    trigger_result = scope_assessment.scope_result if scope_assessment else (resolution.reason if resolution else "UNKNOWN")
    if resolution and resolution.status == "DEGRADED_CANDIDATE":
        trigger_result = resolution.reason
    reason = scope_assessment.reason if scope_assessment else (resolution.reason if resolution else "CAPABILITY_RESULT_REQUIRES_COGNITIVE_REPLANNING")
    gap_ref = capability_gap.gap_id if capability_gap else (resolution.capability_gap_ref if resolution else None)
    return CognitiveNeedReplanningCandidateV1(
        replan_id=f"replan:{formation.formation_id}",
        source_need_ref=formation.source_need_ref,
        source_requirement_ref=formation.requirement_ref,
        trigger_result=trigger_result,
        reason=reason,
        refined_need_ref=refined_need_ref,
        decomposed_need_refs=tuple(decomposed_need_refs),
        alternative_requirement_refs=tuple(alternative_requirement_refs),
        information_insufficient=True,
        capability_gap_ref=gap_ref,
        source_state_version_ref=formation.source_state_version_ref,
        prior_requirement_disposition=prior_requirement_disposition,
    )


def assess_provisional_next_step(
    *,
    assessment_id: str,
    source_cognitive_state_ref: str,
    source_plan_ref: Optional[str],
    current_need_ref: str,
    selected_next_need_ref: Optional[str],
    remaining_candidate_refs: Iterable[str],
    selected_as_current_minimum_step: bool,
    state_version_ref: str,
    sufficiency_status: str,
    continuation_disposition: str,
    trace_ref: Optional[str],
) -> CognitiveNextStepAssessmentV1:
    if sufficiency_status not in SUFFICIENCY_STATUSES:
        raise ValueError(f"unsupported sufficiency status: {sufficiency_status}")
    if continuation_disposition not in CONTINUATION_DISPOSITIONS:
        raise ValueError(f"unsupported continuation disposition: {continuation_disposition}")
    if selected_as_current_minimum_step and not selected_next_need_ref:
        raise ValueError("the current minimum step requires a selected Need")
    if not selected_as_current_minimum_step and selected_next_need_ref:
        raise ValueError("only the current minimum need may be selected")
    if continuation_disposition == "STOP_SUFFICIENT" and sufficiency_status != "SUFFICIENT":
        raise ValueError("STOP_SUFFICIENT requires SUFFICIENT status")
    return CognitiveNextStepAssessmentV1(
        assessment_id=assessment_id,
        source_cognitive_state_ref=source_cognitive_state_ref,
        source_plan_ref=source_plan_ref,
        current_need_ref=current_need_ref,
        selected_next_need_ref=selected_next_need_ref,
        remaining_candidate_refs=tuple(remaining_candidate_refs),
        selected_as_current_minimum_step=selected_as_current_minimum_step,
        remaining_candidates_binding=False,
        state_version_ref=state_version_ref,
        sufficiency_status=sufficiency_status,
        continuation_disposition=continuation_disposition,
        trace_ref=trace_ref,
    )


def reassess_requirement_against_state(
    formation: CapabilityRequirementFormationCandidateV1,
    *,
    current_state_version_ref: str,
    sufficiency_status: str,
    new_evidence_ref: Optional[str] = None,
) -> str:
    """Return a disposition candidate; does not mutate the Requirement."""
    if not current_state_version_ref:
        return "REPLANNING_REQUIRED"
    if sufficiency_status == "SUFFICIENT":
        return "SATISFIED"
    if formation.source_state_version_ref and formation.source_state_version_ref != current_state_version_ref:
        return "SUPERSEDED" if new_evidence_ref else "REPLANNING_REQUIRED"
    return "STILL_RELEVANT"


def validate_next_step_assessment(assessment: CognitiveNextStepAssessmentV1) -> Tuple[str, ...]:
    issues = []
    if not assessment.candidate_only:
        issues.append("next_step_not_candidate_only")
    if assessment.remaining_candidates_binding:
        issues.append("remaining_candidates_are_binding")
    if assessment.continuation_disposition == "STOP_SUFFICIENT" and assessment.sufficiency_status != "SUFFICIENT":
        issues.append("stop_without_sufficiency")
    if not assessment.stop_sufficient_not_failure:
        issues.append("stop_marked_as_failure")
    if not assessment.unexecuted_after_sufficiency_not_failure:
        issues.append("unexecuted_marked_as_failure")
    return tuple(issues)


def validate_bridge_boundaries(
    formation: CapabilityRequirementFormationCandidateV1,
    module: Optional[CapabilityModuleV1] = None,
) -> Tuple[str, ...]:
    issues = []
    requirement = formation.requirement
    if requirement.required_authority != EVIDENCE_AUTHORITY:
        issues.append("authority_not_evidence_only")
    if formation.technical_implementation_selected:
        issues.append("implementation_selected_by_brain")
    if formation.model_selected:
        issues.append("model_selected_by_brain")
    if formation.provider_selected:
        issues.append("provider_selected_by_brain")
    if formation.scope_assumed:
        issues.append("scope_assumed_before_gate")
    if formation.authority_escalated:
        issues.append("authority_escalated")
    if module and requirement.requested_module_id and requirement.requested_module_id != module.module_id:
        issues.append("module_hint_mismatch")
    return tuple(issues)
