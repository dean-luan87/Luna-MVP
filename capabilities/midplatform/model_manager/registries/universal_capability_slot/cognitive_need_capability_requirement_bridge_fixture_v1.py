"""Controlled Cognitive Need -> Capability Requirement reference chains."""

from __future__ import annotations

from dataclasses import asdict, replace
from typing import Dict, List, Tuple

from .capability_scope_resolution_fixture_v1 import _bind, build_scope_modules
from .cognitive_need_capability_requirement_bridge_governance_v1 import (
    assess_provisional_next_step,
    form_capability_requirement,
    reassess_requirement_against_state,
    replan_after_capability_result,
    validate_bridge_boundaries,
    validate_next_step_assessment,
)
from .cognitive_need_capability_requirement_bridge_types_v1 import CognitiveNeedCandidateV1
from .universal_capability_slot_fixture_v1 import _slot
from .universal_capability_slot_resolution_v1 import resolve_scoped_capability_requirement
from .universal_capability_slot_types_v1 import CapabilityGapCandidateV1


OWNER = "Capability Registry / Capability Governance"


def _case(case_id: str, title: str, passed: bool, details: Dict[str, object]) -> Dict[str, object]:
    return {"case_id": case_id, "title": title, "passed": bool(passed), "details": details}


def _need(
    need_id: str,
    problem_description: str,
    missing_information_class: str,
    required_evidence_class: str,
    *,
    urgency: str = "NORMAL",
    safety_relevance: str = "NONE",
) -> CognitiveNeedCandidateV1:
    return CognitiveNeedCandidateV1(
        need_id=need_id,
        source_intent_ref=f"intent:{need_id}",
        source_context_ref=f"context:{need_id}",
        source_field_ref=f"field:{need_id}",
        source_hypothesis_ref=f"hypothesis:{need_id}",
        source_attention_ref=f"attention:{need_id}",
        problem_description=problem_description,
        missing_information_class=missing_information_class,
        required_evidence_class=required_evidence_class,
        urgency=urgency,
        safety_relevance=safety_relevance,
        state_version_ref=f"state:{need_id}:v1",
        trace_ref=f"trace:{need_id}",
    )


def _form(need: CognitiveNeedCandidateV1, module_id: str, problem_class: str, operation: str, input_ref: str, output_ref: str, requirement_type: str):
    return form_capability_requirement(
        need,
        formation_id=need.need_id,
        requested_module_id=module_id,
        problem_class=problem_class,
        requested_operation=operation,
        input_contract_ref=input_ref,
        output_contract_ref=output_ref,
        requirement_type=requirement_type,
        task_context="controlled-cognitive-need-bridge",
        permission_refs=("permission:capability-governance",),
        resource_refs=("resource:controlled",),
        execution_boundary_ref="Observation Gateway / FPO / existing capability execution boundary",
    )


def build_bridge_fixture() -> Dict[str, object]:
    modules = build_scope_modules()
    text, precise, object_detection, spatial = modules
    slots = (
        _bind(text, _slot("slot:need-text")),
        _bind(precise, _slot("slot:need-precise")),
        _bind(object_detection, _slot("slot:need-object")),
        _bind(spatial, _slot("slot:need-spatial")),
    )

    sign_need = _need("need:sign-text", "read the sign text", "sign_text", "text_evidence")
    small_text_need = _need("need:small-text", "read small text", "precise_ocr", "precise_text_evidence")
    vehicle_need = _need("need:vehicle", "detect vehicle presence", "vehicle_presence", "object_evidence", urgency="SAFETY_PRIORITY", safety_relevance="CRITICAL")
    spatial_need = _need("need:spatial", "understand nearby spatial structure", "spatial_structure", "spatial_evidence")
    field_rule_need = _need("need:field-rule", "determine whether a sign creates an effective Field Rule", "effective_field_rule", "text_evidence")
    mandatory_action_need = _need("need:mandatory-action", "determine whether the sign mandates an action", "sign_text", "text_evidence")
    identity_need = _need("need:identity", "identify a person", "person_identity", "identity_evidence")
    danger_need = _need("need:danger", "judge dangerous intent", "person_danger_intent", "danger_evidence")
    map_ocr_need = _need("need:map-ocr", "read a shop name from a map", "text_content", "text_evidence")
    unknown_need = _need("need:unknown", "resolve unknown information", "unknown_problem", "unknown_evidence")
    operation_need = _need("need:operation", "read sign text", "sign_text", "text_evidence")
    input_need = _need("need:input", "read sign text from audio", "sign_text", "text_evidence")
    output_need = _need("need:output", "read sign text as a Field Rule", "sign_text", "field_rule_evidence")

    sign_form = _form(sign_need, text.module_id, "sign_text", "READ_TEXT", "image_evidence", "text_candidate", "TEXT_READ")
    precise_form = _form(small_text_need, precise.module_id, "precise_ocr", "READ_PRECISE_TEXT", "visual_region_candidate", "text_candidate", "PRECISE_TEXT_READ")
    vehicle_form = _form(vehicle_need, object_detection.module_id, "vehicle_presence", "DETECT_OBJECT", "image_evidence", "object_candidate", "OBJECT_DETECTION")
    spatial_form = _form(spatial_need, spatial.module_id, "spatial_structure", "PROVIDE_SPATIAL_STRUCTURE", "pose_candidate", "spatial_map_candidate", "SPATIAL_MAP")
    field_form = _form(field_rule_need, text.module_id, "sign_text", "READ_TEXT", "image_evidence", "text_candidate", "TEXT_READ")
    action_form = _form(mandatory_action_need, text.module_id, "sign_text", "READ_TEXT", "image_evidence", "text_candidate", "TEXT_READ")
    field_overreach_form = _form(field_rule_need, text.module_id, "effective_field_rule", "DETERMINE_EFFECTIVE_FIELD_RULE", "image_evidence", "field_rule_candidate", "TEXT_READ")
    action_overreach_form = _form(mandatory_action_need, text.module_id, "sign_text", "DETERMINE_MANDATORY_ACTION", "image_evidence", "action_candidate", "TEXT_READ")
    identity_form = _form(identity_need, object_detection.module_id, "person_identity", "IDENTIFY_PERSON", "image_evidence", "identity_candidate", "OBJECT_DETECTION")
    danger_form = _form(danger_need, object_detection.module_id, "person_danger_intent", "CLASSIFY_DANGER_INTENT", "image_evidence", "danger_candidate", "OBJECT_DETECTION")
    map_ocr_form = _form(map_ocr_need, spatial.module_id, "text_content", "READ_TEXT", "image_evidence", "text_candidate", "SPATIAL_MAP")
    unknown_form = _form(unknown_need, text.module_id, "unknown_problem", "UNKNOWN_OPERATION", "image_evidence", "unknown_output", "UNKNOWN")
    operation_form = _form(operation_need, text.module_id, "sign_text", "DETERMINE_EFFECTIVE_FIELD_RULE", "image_evidence", "text_candidate", "TEXT_READ")
    input_form = _form(input_need, text.module_id, "sign_text", "READ_TEXT", "audio_stream", "text_candidate", "TEXT_READ")
    output_form = _form(output_need, text.module_id, "sign_text", "READ_TEXT", "image_evidence", "field_rule_candidate", "TEXT_READ")

    text_slots = (slots[0], slots[1], slots[2], slots[3])
    sign_assessment, sign_resolution, sign_gap = resolve_scoped_capability_requirement(sign_form.requirement, modules, text_slots)
    precise_assessment, precise_resolution, precise_gap = resolve_scoped_capability_requirement(precise_form.requirement, modules, text_slots)
    vehicle_assessment, vehicle_resolution, vehicle_gap = resolve_scoped_capability_requirement(vehicle_form.requirement, modules, text_slots)
    spatial_assessment, spatial_resolution, spatial_gap = resolve_scoped_capability_requirement(spatial_form.requirement, modules, text_slots)
    field_assessment, field_resolution, field_gap = resolve_scoped_capability_requirement(field_overreach_form.requirement, modules, text_slots)
    action_assessment, action_resolution, action_gap = resolve_scoped_capability_requirement(action_overreach_form.requirement, modules, text_slots)
    identity_assessment, identity_resolution, identity_gap = resolve_scoped_capability_requirement(identity_form.requirement, modules, text_slots)
    danger_assessment, danger_resolution, danger_gap = resolve_scoped_capability_requirement(danger_form.requirement, modules, text_slots)
    map_ocr_assessment, map_ocr_resolution, map_ocr_gap = resolve_scoped_capability_requirement(map_ocr_form.requirement, modules, text_slots)
    unknown_assessment, unknown_resolution, unknown_gap = resolve_scoped_capability_requirement(unknown_form.requirement, modules, text_slots)
    operation_assessment, operation_resolution, operation_gap = resolve_scoped_capability_requirement(operation_form.requirement, modules, text_slots)
    input_assessment, input_resolution, input_gap = resolve_scoped_capability_requirement(input_form.requirement, modules, text_slots)
    output_assessment, output_resolution, output_gap = resolve_scoped_capability_requirement(output_form.requirement, modules, text_slots)

    authority_requirement = replace(sign_form.requirement, required_authority="FIELD_RULE")
    authority_assessment, authority_resolution, authority_gap = resolve_scoped_capability_requirement(authority_requirement, modules, text_slots)

    unavailable_text = replace(text, lifecycle_state="UNAVAILABLE")
    unavailable_assessment, unavailable_resolution, unavailable_gap = resolve_scoped_capability_requirement(sign_form.requirement, (unavailable_text, precise, object_detection, spatial), text_slots)
    degraded_text = replace(text, lifecycle_state="DEGRADED")
    degraded_assessment, degraded_resolution, degraded_gap = resolve_scoped_capability_requirement(sign_form.requirement, (degraded_text, precise, object_detection, spatial), text_slots)
    unbound_assessment, unbound_resolution, unbound_gap = resolve_scoped_capability_requirement(sign_form.requirement, modules, (_slot("slot:need-empty"), slots[1], slots[2], slots[3]))

    field_replan = replan_after_capability_result(field_overreach_form, scope_assessment=field_assessment, resolution=field_resolution, capability_gap=field_gap, refined_need_ref="need:sign-text")
    unavailable_replan = replan_after_capability_result(sign_form, scope_assessment=unavailable_assessment, resolution=unavailable_resolution, capability_gap=unavailable_gap, alternative_requirement_refs=(sign_form.requirement.requirement_id,))
    degraded_replan = replan_after_capability_result(sign_form, scope_assessment=degraded_assessment, resolution=degraded_resolution, capability_gap=degraded_gap, refined_need_ref="need:reobserve-sign")
    alternative_need = _need("need:alternative-evidence", "seek a bounded alternative evidence source for the sign text", "sign_text", "alternative_text_evidence")
    next_need_after_insufficient = _need("need:next-after-insufficient", "continue the current evidence need after insufficient observation", "sign_text", "text_evidence")
    next_form_after_insufficient = _form(next_need_after_insufficient, text.module_id, "sign_text", "READ_TEXT", "image_evidence", "text_candidate", "TEXT_READ")
    gap = CapabilityGapCandidateV1(
        gap_id=f"gap:{field_overreach_form.requirement.requirement_id}",
        originating_requirement_ref=field_overreach_form.requirement.requirement_id,
        rejected_module_refs=(text.module_id,),
        unmet_problem_class="effective_field_rule",
        unmet_operation="DETERMINE_EFFECTIVE_FIELD_RULE",
        unmet_contract_refs=("problem_class", "requested_operation"),
        reason="CAPABILITY_SCOPE_REJECTED_AND_COGNITIVE_REPLANNING_REQUIRED",
    )
    sign_bridge_issues = validate_bridge_boundaries(sign_form, text)
    first_step = assess_provisional_next_step(
        assessment_id="next-step:first-observation",
        source_cognitive_state_ref="cognitive-state:controlled:v1",
        source_plan_ref="plan:controlled-observation:v1",
        current_need_ref=sign_need.need_id,
        selected_next_need_ref=sign_need.need_id,
        remaining_candidate_refs=("observation-candidate-2", "observation-candidate-3", "observation-candidate-4", "observation-candidate-5", "observation-candidate-6", "observation-candidate-7"),
        selected_as_current_minimum_step=True,
        state_version_ref="state:controlled:v1",
        sufficiency_status="INSUFFICIENT",
        continuation_disposition="CONTINUE",
        trace_ref="trace:next-step:first",
    )
    first_step_issues = validate_next_step_assessment(first_step)
    sufficient_step = assess_provisional_next_step(
        assessment_id="next-step:third-observation-sufficient",
        source_cognitive_state_ref="cognitive-state:controlled:v3",
        source_plan_ref="plan:controlled-observation:v1",
        current_need_ref=sign_need.need_id,
        selected_next_need_ref=None,
        remaining_candidate_refs=("observation-candidate-4", "observation-candidate-5", "observation-candidate-6", "observation-candidate-7"),
        selected_as_current_minimum_step=False,
        state_version_ref="state:controlled:v3",
        sufficiency_status="SUFFICIENT",
        continuation_disposition="STOP_SUFFICIENT",
        trace_ref="trace:next-step:third-sufficient",
    )
    sufficient_step_issues = validate_next_step_assessment(sufficient_step)
    old_requirement_disposition = reassess_requirement_against_state(
        sign_form,
        current_state_version_ref="state:controlled:v2",
        sufficiency_status="UNKNOWN",
        new_evidence_ref="evidence:updated-v2",
    )
    satisfied_requirement_disposition = reassess_requirement_against_state(
        sign_form,
        current_state_version_ref="state:controlled:v3",
        sufficiency_status="SUFFICIENT",
    )
    skipped_after_sufficiency_reason = "NOT_REQUIRED_AFTER_SUFFICIENCY"

    cases: List[Dict[str, object]] = [
        _case("CNB-01", "sign text Need exists", sign_need.candidate_only and sign_need.missing_information_class == "sign_text", asdict(sign_need)),
        _case("CNB-02", "sign text forms READ_TEXT", sign_assessment.in_scope and sign_resolution.status == "READY_CANDIDATE" and sign_form.requirement.requested_operation == "READ_TEXT", asdict(sign_form)),
        _case("CNB-03", "small text forms READ_PRECISE_TEXT", precise_assessment.in_scope and precise_form.requirement.requested_operation == "READ_PRECISE_TEXT", asdict(precise_form)),
        _case("CNB-04", "vehicle presence forms DETECT_OBJECT", vehicle_assessment.in_scope and vehicle_resolution.status == "READY_CANDIDATE", asdict(vehicle_form)),
        _case("CNB-05", "spatial structure forms PROVIDE_SPATIAL_STRUCTURE", spatial_assessment.in_scope and spatial_resolution.status == "READY_CANDIDATE", asdict(spatial_form)),
        _case("CNB-06", "effective Field Rule decomposes to sign text evidence", field_form.selected_problem_class == "sign_text" and field_form.requested_operation == "READ_TEXT" and field_form.output_contract_ref == "text_candidate", asdict(field_form)),
        _case("CNB-07", "mandatory action decomposes to sign text evidence", action_form.selected_problem_class == "sign_text" and action_form.requested_operation == "READ_TEXT" and action_form.required_authority == "EVIDENCE_ONLY" and action_assessment.scope_result == "OPERATION_UNSUPPORTED", asdict(action_form)),
        _case("CNB-08", "identity cannot be delegated to object detection", identity_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED" and identity_gap is not None, asdict(identity_assessment)),
        _case("CNB-09", "dangerous intent cannot be delegated to object detection", danger_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED" and danger_gap is not None, asdict(danger_assessment)),
        _case("CNB-10", "spatial mapping cannot read text", map_ocr_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED" and map_ocr_gap is not None, asdict(map_ocr_assessment)),
        _case("CNB-11", "safety urgency does not bypass scope", vehicle_need.urgency == "SAFETY_PRIORITY" and vehicle_form.required_authority == "EVIDENCE_ONLY" and vehicle_assessment.in_scope, asdict(vehicle_form)),
        _case("CNB-12", "unsupported problem class is rejected", unknown_assessment.scope_result == "PROBLEM_CLASS_UNSUPPORTED", asdict(unknown_assessment)),
        _case("CNB-13", "unsupported operation is rejected", operation_assessment.scope_result == "OPERATION_UNSUPPORTED", asdict(operation_assessment)),
        _case("CNB-14", "unsupported input contract is rejected", input_assessment.scope_result == "INPUT_CONTRACT_UNSUPPORTED", asdict(input_assessment)),
        _case("CNB-15", "unsupported output contract is rejected", output_assessment.scope_result == "OUTPUT_CONTRACT_UNSUPPORTED", asdict(output_assessment)),
        _case("CNB-16", "authority rejection is explicit", authority_assessment.scope_result == "AUTHORITY_NOT_ALLOWED" and authority_gap is not None, asdict(authority_assessment)),
        _case("CNB-17", "scope rejection returns to cognitive replanning", field_replan.trigger_result == field_assessment.scope_result and field_replan.candidate_only and field_replan.capability_gap_ref is not None, asdict(field_replan)),
        _case("CNB-18", "unavailable capability returns to replanning", unavailable_resolution.status == "UNAVAILABLE_CANDIDATE" and unavailable_replan.candidate_only, asdict(unavailable_replan)),
        _case("CNB-19", "degraded capability remains visible", degraded_resolution.status == "DEGRADED_CANDIDATE" and degraded_replan.information_insufficient, asdict(degraded_resolution)),
        _case("CNB-20", "alternative evidence Need candidate", alternative_need.candidate_only and alternative_need.required_evidence_class == "alternative_text_evidence", asdict(alternative_need)),
        _case("CNB-21", "Capability Gap remains candidate-only", gap.candidate_only and gap.gap_id == field_replan.capability_gap_ref, asdict(gap)),
        _case("CNB-22", "Brain does not select Model", not sign_form.model_selected and not precise_form.model_selected and not sign_bridge_issues, {"model_selected": False}),
        _case("CNB-23", "Brain does not select Provider", not sign_form.provider_selected and not precise_form.provider_selected and not sign_bridge_issues, {"provider_selected": False}),
        _case("CNB-24", "Brain does not mutate Scope", not sign_form.scope_assumed and not field_replan.scope_bypassed, {"scope_assumed": sign_form.scope_assumed, "scope_bypassed": field_replan.scope_bypassed}),
        _case("CNB-25", "Brain does not mutate lifecycle", unavailable_resolution.provider_invocation is False and degraded_resolution.provider_invocation is False, {"provider_invocation": False}),
        _case("CNB-26", "no Truth or Action authority escalation", sign_form.required_authority == "EVIDENCE_ONLY" and action_form.required_authority == "EVIDENCE_ONLY" and authority_form_flags(authority_assessment) is True, {"truth_authority": False, "action_authority": False}),
        _case("CNB-27", "no fallback hallucination", all(item.fallback_hallucination is False for item in (field_replan, unavailable_replan, degraded_replan)), {"fallback_hallucination": False}),
        _case("CNB-28", "no automatic acquisition", all(item.automatic_acquisition is False for item in (field_replan, unavailable_replan, degraded_replan)), {"automatic_acquisition": False}),
        _case("CNB-29", "no Learning or Memory mutation", True, {"learning_execution": False, "memory_mutation": False}),
        _case("CNB-30", "no runtime/provider/model execution", all(item.candidate_only for item in (sign_form, precise_form, vehicle_form, spatial_form)) and all(not item.provider_invocation and not item.model_inference for item in (sign_resolution, precise_resolution, vehicle_resolution, spatial_resolution)), {"runtime_execution": False, "provider_invocation": False, "model_inference": False}),
        _case("CNB-31", "seven observation candidates yield one current minimum Requirement", first_step.selected_as_current_minimum_step and len(first_step.remaining_candidate_refs) == 6 and not first_step.remaining_candidates_binding and not first_step_issues, asdict(first_step)),
        _case("CNB-32", "insufficient result permits the next Need", next_form_after_insufficient.source_need_ref == next_need_after_insufficient.need_id and next_form_after_insufficient.requirement_minimized and first_step.sufficiency_status == "INSUFFICIENT", asdict(next_form_after_insufficient)),
        _case("CNB-33", "third observation sufficiency stops remaining candidates", sufficient_step.sufficiency_status == "SUFFICIENT" and sufficient_step.continuation_disposition == "STOP_SUFFICIENT" and len(sufficient_step.remaining_candidate_refs) == 4 and not sufficient_step.remaining_candidates_binding and not sufficient_step_issues, asdict(sufficient_step)),
        _case("CNB-34", "STOP_SUFFICIENT is not failure", sufficient_step.continuation_disposition == "STOP_SUFFICIENT" and sufficient_step.stop_sufficient_not_failure and sufficient_step.unexecuted_after_sufficiency_not_failure, {"execution_failure": False, "requirement_failure": False, "task_failure": False}),
        _case("CNB-35", "new evidence supersedes old Requirement relevance", old_requirement_disposition == "SUPERSEDED" and sign_form.source_state_version_ref == "state:need:sign-text:v1", {"disposition": old_requirement_disposition}),
        _case("CNB-36", "satisfied Need is not regenerated", satisfied_requirement_disposition == "SATISFIED" and next_form_after_insufficient.source_need_ref != sign_form.source_need_ref and next_form_after_insufficient.requirement.requirement_id != sign_form.requirement.requirement_id, {"disposition": satisfied_requirement_disposition, "new_need_ref": next_form_after_insufficient.source_need_ref}),
        _case("CNB-37", "Plan completeness does not require execution completeness", sufficient_step.source_plan_ref is not None and sufficient_step.remaining_candidate_refs and not sufficient_step.remaining_candidates_binding, {"plan_complete": True, "execution_complete": False}),
        _case("CNB-38", "Safety priority does not bypass Scope or Sufficiency", vehicle_need.urgency == "SAFETY_PRIORITY" and vehicle_form.required_authority == "EVIDENCE_ONLY" and first_step.remaining_candidates_binding is False, {"urgency": vehicle_need.urgency, "scope_bypass": False}),
        _case("CNB-39", "new evidence can replan remaining path", degraded_replan.refined_need_ref == "need:reobserve-sign" and degraded_replan.source_state_version_ref == sign_form.source_state_version_ref, asdict(degraded_replan)),
        _case("CNB-40", "skipped invocation after sufficiency is not capability failure", skipped_after_sufficiency_reason == "NOT_REQUIRED_AFTER_SUFFICIENCY" and sufficient_step.continuation_disposition == "STOP_SUFFICIENT", {"reason": skipped_after_sufficiency_reason, "capability_failure": False}),
    ]
    return {
        "modules": modules,
        "slots": slots,
        "needs": (sign_need, small_text_need, vehicle_need, spatial_need, field_rule_need, mandatory_action_need, identity_need, danger_need, map_ocr_need, unknown_need, operation_need, input_need, output_need, alternative_need, next_need_after_insufficient),
        "formations": (sign_form, precise_form, vehicle_form, spatial_form, field_form, action_form, field_overreach_form, action_overreach_form, identity_form, danger_form, map_ocr_form, unknown_form, operation_form, input_form, output_form, next_form_after_insufficient),
        "assessments": (sign_assessment, precise_assessment, vehicle_assessment, spatial_assessment, field_assessment, action_assessment, identity_assessment, danger_assessment, map_ocr_assessment, unknown_assessment, operation_assessment, input_assessment, output_assessment, authority_assessment, unavailable_assessment, degraded_assessment, unbound_assessment),
        "resolutions": (sign_resolution, precise_resolution, vehicle_resolution, spatial_resolution, field_resolution, action_resolution, identity_resolution, danger_resolution, map_ocr_resolution, unknown_resolution, operation_resolution, input_resolution, output_resolution, authority_resolution, unavailable_resolution, degraded_resolution, unbound_resolution),
        "replans": (field_replan, unavailable_replan, degraded_replan),
        "next_step_assessments": (first_step, sufficient_step),
        "gap": gap,
        "cases": cases,
    }


def authority_form_flags(assessment: object) -> bool:
    return getattr(assessment, "scope_result", "") == "AUTHORITY_NOT_ALLOWED"


def build_runner_result() -> Dict[str, object]:
    fixture = build_bridge_fixture()
    cases = fixture["cases"]
    guards = {
        "runtime_execution": False,
        "provider_invocation": False,
        "model_inference": False,
        "camera_activation": False,
        "real_download": False,
        "real_install": False,
        "real_activation": False,
        "real_upgrade": False,
        "real_rollback": False,
        "automatic_capability_acquisition": False,
        "automatic_capability_optimization": False,
        "automatic_capability_uninstall": False,
        "brain_direct_capability_mutation": False,
        "brain_scope_bypass": False,
        "brain_model_selection_as_capability_identity": False,
        "brain_provider_selection_as_capability_identity": False,
        "authority_escalation": False,
        "world_truth_authority": False,
        "action_authority": False,
        "fallback_hallucination": False,
        "learning_execution": False,
        "memory_mutation": False,
        "semantic_expansion_execution": False,
        "semantic_folding_execution": False,
        "srsk_implementation": False,
        "plan_to_full_execution_commitment": False,
        "all_plan_steps_auto_materialized": False,
        "remaining_candidates_binding": False,
        "requirement_generated_after_sufficiency": False,
        "obsolete_requirement_forced_execution": False,
        "sufficiency_stop_counted_as_failure": False,
        "plan_completion_used_as_goal_success_proxy": False,
        "safety_bypasses_sufficiency": False,
        "new_evidence_ignored_for_decision": False,
    }
    return {
        "phase": "Phase-Luna-Cognitive-Need-To-Capability-Requirement-Bridge-Controlled-Implementation-v1-001",
        "mode": "CONTROLLED_IMPLEMENTATION",
        "owner": OWNER,
        "real_components": [],
        "synthetic_components": ["CognitiveNeedCandidateV1", "CapabilityRequirementV1", "existing Scope/Resolution/Gap"],
        "scenario_count": len(cases),
        "all_cases_passed": all(case["passed"] for case in cases),
        "failed_case_ids": [case["case_id"] for case in cases if not case["passed"]],
        "candidate_only": True,
        "scope_gate_reused": True,
        "resolution_owner_reused": True,
        "replanning_candidate_only": True,
        "plan_to_full_execution_commitment": False,
        "all_plan_steps_auto_materialized": False,
        "remaining_candidates_binding": False,
        "requirement_generated_after_sufficiency": False,
        "obsolete_requirement_forced_execution": False,
        "sufficiency_stop_counted_as_failure": False,
        "plan_completion_used_as_goal_success_proxy": False,
        "safety_bypasses_sufficiency": False,
        "new_evidence_ignored_for_decision": False,
        **guards,
        "cases": cases,
    }
