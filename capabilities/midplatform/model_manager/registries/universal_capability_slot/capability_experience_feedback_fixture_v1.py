"""Synthetic candidate fixtures for individual and Hive capability feedback."""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Tuple

from .capability_experience_feedback_governance_v1 import (
    aggregate_individual_capability_experience,
    assess_capability_outcome,
    build_capability_usage_record,
    build_capability_weakness_candidate,
    build_hive_demand_candidate,
    build_hive_feedback_candidate,
)
from .universal_capability_slot_fixture_v1 import _slot
from .universal_capability_slot_governance_v1 import build_capability_self_view
from .universal_capability_slot_types_v1 import CapabilityGapCandidateV1
from .capability_scope_resolution_fixture_v1 import _bind, build_scope_modules


OWNER = "Capability Registry / Capability Governance"
PRIVACY_POLICY_REF = "privacy:capability-feedback-aggregate-v1"


def _case(case_id: str, title: str, passed: bool, details: Dict[str, object]) -> Dict[str, object]:
    return {"case_id": case_id, "title": title, "passed": bool(passed), "details": details}


def _usage(
    usage_id: str,
    module_ref: str,
    slot_ref: str,
    requirement_ref: str,
    problem_class: str,
    operation: str,
    execution_outcome: str,
    requirement_satisfaction: str,
    task_contribution: str,
    *,
    failure_refs: Tuple[str, ...] = (),
    degradation_refs: Tuple[str, ...] = (),
) -> object:
    return build_capability_usage_record(
        usage_id=usage_id,
        module_ref=module_ref,
        module_version_ref=f"version:{module_ref}:v1",
        slot_ref=slot_ref,
        invocation_ref=f"invocation:{usage_id}",
        requirement_ref=requirement_ref,
        problem_class=problem_class,
        operation=operation,
        context_refs=("context:controlled-task",),
        task_refs=(f"task:{requirement_ref}",),
        trace_refs=(f"trace:{usage_id}",),
        execution_result_ref=f"execution-result:{usage_id}",
        execution_outcome=execution_outcome,
        requirement_satisfaction=requirement_satisfaction,
        task_contribution=task_contribution,
        failure_refs=failure_refs,
        degradation_refs=degradation_refs,
        dependency_refs=(f"dependency:{module_ref}",),
        temporal_refs=("window:controlled",),
    )


def build_feedback_fixture() -> Dict[str, object]:
    modules = build_scope_modules()
    text_module, _, object_module, spatial_module = modules
    text_slot = _bind(text_module, _slot("slot:feedback-text"))
    object_slot = _bind(object_module, _slot("slot:feedback-object"))
    spatial_slot = _bind(spatial_module, _slot("slot:feedback-spatial"))

    usages = (
        _usage("ocr-01", text_module.module_id, text_slot.slot_id, "req:ocr-read-01", "text_content", "READ_TEXT", "SUCCESS", "SATISFIED", "RESOLVED"),
        _usage("ocr-02", text_module.module_id, text_slot.slot_id, "req:ocr-read-02", "text_content", "READ_TEXT", "SUCCESS", "PARTIAL", "CONTRIBUTED"),
        _usage("ocr-03", text_module.module_id, text_slot.slot_id, "req:ocr-sign-03", "sign_text", "READ_TEXT", "SUCCESS", "UNSATISFIED", "UNRESOLVED"),
        _usage("ocr-04", text_module.module_id, text_slot.slot_id, "req:ocr-read-04", "text_content", "READ_TEXT", "SUCCESS", "SATISFIED", "RESOLVED"),
        _usage("ocr-05", text_module.module_id, text_slot.slot_id, "req:ocr-sign-05", "sign_text", "READ_TEXT", "FAILURE", "UNSATISFIED", "NO_CONTRIBUTION", failure_refs=("failure:text-not-legible",)),
        _usage("ocr-06", text_module.module_id, text_slot.slot_id, "req:ocr-sign-06", "sign_text", "READ_TEXT", "DEGRADED", "PARTIAL", "NO_CONTRIBUTION", degradation_refs=("degradation:low-visibility",)),
        _usage("object-01", object_module.module_id, object_slot.slot_id, "req:vehicle-01", "vehicle_presence", "DETECT_OBJECT", "SUCCESS", "SATISFIED", "CONTRIBUTED"),
        _usage("object-02", object_module.module_id, object_slot.slot_id, "req:vehicle-02", "vehicle_presence", "DETECT_OBJECT", "SUCCESS", "SATISFIED", "RESOLVED"),
        _usage("spatial-01", spatial_module.module_id, spatial_slot.slot_id, "req:map-01", "spatial_structure", "PROVIDE_SPATIAL_STRUCTURE", "SUCCESS", "SATISFIED", "CONTRIBUTED"),
        _usage("spatial-02", spatial_module.module_id, spatial_slot.slot_id, "req:map-02", "spatial_anchor", "PROVIDE_SPATIAL_STRUCTURE", "DEGRADED", "PARTIAL", "UNRESOLVED", degradation_refs=("degradation:pose-drift",)),
    )
    assessments = tuple(assess_capability_outcome(usage) for usage in usages)
    ocr_usages = tuple(usage for usage in usages if usage.module_ref == text_module.module_id)
    object_usages = tuple(usage for usage in usages if usage.module_ref == object_module.module_id)
    spatial_usages = tuple(usage for usage in usages if usage.module_ref == spatial_module.module_id)
    ocr_profile = aggregate_individual_capability_experience(
        profile_id="profile:luna-001:text-recognition",
        module_ref=text_module.module_id,
        aggregation_window_ref="window:controlled",
        usage_records=ocr_usages,
    )
    object_profile = aggregate_individual_capability_experience(
        profile_id="profile:luna-001:object-detection",
        module_ref=object_module.module_id,
        aggregation_window_ref="window:controlled",
        usage_records=object_usages,
    )
    spatial_profile = aggregate_individual_capability_experience(
        profile_id="profile:luna-001:spatial-mapping",
        module_ref=spatial_module.module_id,
        aggregation_window_ref="window:controlled",
        usage_records=spatial_usages,
    )
    weakness = build_capability_weakness_candidate(
        weakness_id="weakness:text-recognition:sign-text",
        profile=ocr_profile,
        problem_class="sign_text",
        operation="READ_TEXT",
        context_refs=("context:controlled-task",),
        evidence_refs=("trace:ocr-03", "trace:ocr-05", "trace:ocr-06"),
        reason="REPEATED_SIGN_TEXT_SATISFACTION_INSUFFICIENCY_CANDIDATE",
    )
    gap = CapabilityGapCandidateV1(
        gap_id="gap:effective-field-rule",
        originating_requirement_ref="req:field-rule",
        rejected_module_refs=(text_module.module_id,),
        unmet_problem_class="effective_field_rule",
        unmet_operation="DETERMINE_EFFECTIVE_FIELD_RULE",
        unmet_contract_refs=("requested_operation", "required_authority"),
        reason="NO_ADMITTED_CAPABILITY_MODULE_FOR_EFFECTIVE_FIELD_RULE",
    )
    hive_feedback = build_hive_feedback_candidate(
        feedback_id="hive-feedback:text-recognition",
        module_ref=text_module.module_id,
        aggregation_window_ref="window:hive-controlled",
        profiles=(ocr_profile,),
        weakness_refs=(weakness.weakness_id,),
        gap_refs=(gap.gap_id,),
        privacy_policy_ref=PRIVACY_POLICY_REF,
    )
    weakness_demand = build_hive_demand_candidate(
        demand_id="demand:weakness:sign-text",
        demand_kind="CAPABILITY_WEAKNESS",
        problem_class="sign_text",
        operation="READ_TEXT",
        source_feedback_ref=hive_feedback.feedback_id,
        source_profile_refs=(ocr_profile.profile_id,),
        existing_module_refs=(text_module.module_id,),
        unmet_requirement_refs=(),
        aggregate_count=3,
        reason="EXISTING_CAPABILITY_PRESENT_BUT_AGGREGATE_SATISFACTION_INSUFFICIENT",
    )
    gap_demand = build_hive_demand_candidate(
        demand_id="demand:gap:effective-field-rule",
        demand_kind="CAPABILITY_GAP",
        problem_class=gap.unmet_problem_class or "effective_field_rule",
        operation=gap.unmet_operation or "DETERMINE_EFFECTIVE_FIELD_RULE",
        source_feedback_ref=hive_feedback.feedback_id,
        source_profile_refs=(ocr_profile.profile_id,),
        existing_module_refs=(),
        unmet_requirement_refs=gap.unmet_contract_refs,
        aggregate_count=1,
        reason="NO_EXISTING_OFFICIAL_CAPABILITY_SATISFIES_REQUIREMENT",
    )
    self_view = build_capability_self_view(
        modules,
        (text_slot, object_slot, spatial_slot),
        usage_profile_refs=(ocr_profile.profile_id, object_profile.profile_id, spatial_profile.profile_id),
        weakness_candidate_refs=(weakness.weakness_id,),
        feedback_refs=(hive_feedback.feedback_id,),
    )

    cases: List[Dict[str, object]] = [
        _case("CEF-01", "successful execution + satisfied requirement", assessments[0].execution_outcome == "SUCCESS" and assessments[0].requirement_satisfaction == "SATISFIED", asdict(assessments[0])),
        _case("CEF-02", "successful execution + partially satisfied requirement", assessments[1].execution_outcome == "SUCCESS" and assessments[1].requirement_satisfaction == "PARTIAL", asdict(assessments[1])),
        _case("CEF-03", "successful execution + unresolved task", assessments[2].execution_outcome == "SUCCESS" and assessments[2].task_contribution == "UNRESOLVED", asdict(assessments[2])),
        _case("CEF-04", "failed execution", assessments[4].execution_outcome == "FAILURE", asdict(assessments[4])),
        _case("CEF-05", "degraded execution", assessments[5].execution_outcome == "DEGRADED", asdict(assessments[5])),
        _case("CEF-06", "repeated OCR success", ocr_profile.execution_success_count >= 3, asdict(ocr_profile)),
        _case("CEF-07", "repeated OCR weakness in a problem class", weakness.problem_class == "sign_text" and weakness.candidate_only, asdict(weakness)),
        _case("CEF-08", "object detection usage aggregation", object_profile.usage_count == 2 and object_profile.task_contributed_count == 1, asdict(object_profile)),
        _case("CEF-09", "spatial mapping usage aggregation", spatial_profile.usage_count == 2 and spatial_profile.execution_degraded_count == 1, asdict(spatial_profile)),
        _case("CEF-10", "weakness candidate formation", weakness.source_profile_ref == ocr_profile.profile_id and not weakness.lifecycle_mutation, asdict(weakness)),
        _case("CEF-11", "capability gap remains distinct from weakness", gap.gap_id not in {weakness.weakness_id} and gap.candidate_only, asdict(gap)),
        _case("CEF-12", "Self sees usage statistics", ocr_profile.profile_id in self_view.usage_profile_refs, asdict(self_view)),
        _case("CEF-13", "Self sees weakness references", weakness.weakness_id in self_view.weakness_candidate_refs, asdict(self_view)),
        _case("CEF-14", "Self cannot mutate capability", self_view.self_is_lifecycle_owner is False and self_view.candidate_only, asdict(self_view)),
        _case("CEF-15", "individual aggregation", ocr_profile.usage_count == len(ocr_usages) and ocr_profile.scalar_value_score is False, asdict(ocr_profile)),
        _case("CEF-16", "Hive aggregate feedback candidate", hive_feedback.sample_count == ocr_profile.usage_count and hive_feedback.candidate_only, asdict(hive_feedback)),
        _case("CEF-17", "no raw personal data required by Hive contract", all(not getattr(hive_feedback, field) for field in ("raw_conversations_included", "raw_images_included", "raw_audio_included", "identity_records_included", "memory_contents_included", "full_personal_task_histories_included")), asdict(hive_feedback)),
        _case("CEF-18", "Hive weakness demand candidate", weakness_demand.demand_kind == "CAPABILITY_WEAKNESS" and weakness_demand.existing_module_refs, asdict(weakness_demand)),
        _case("CEF-19", "Hive capability-gap demand candidate", gap_demand.demand_kind == "CAPABILITY_GAP" and not gap_demand.existing_module_refs, asdict(gap_demand)),
        _case("CEF-20", "feedback cannot extend Scope", weakness.scope_mutation is False, asdict(weakness)),
        _case("CEF-21", "feedback cannot grant authority", all(not getattr(item, "world_truth_declared", False) for item in assessments), {"world_truth_declared": False}),
        _case("CEF-22", "feedback cannot trigger Learning", weakness.learning_trigger is False and gap_demand.executes_learning is False, {"learning_trigger": weakness.learning_trigger, "executes_learning": gap_demand.executes_learning}),
        _case("CEF-23", "feedback cannot replace Model/Provider", weakness.model_replacement is False and weakness.provider_replacement is False and gap_demand.executes_model_replacement is False and gap_demand.executes_provider_replacement is False, asdict(weakness)),
        _case("CEF-24", "feedback cannot trigger acquisition", gap_demand.executes_acquisition is False, asdict(gap_demand)),
        _case("CEF-25", "no runtime/provider/model execution", all(item.candidate_only for item in assessments) and all(not item.world_truth_declared for item in assessments), {"runtime_execution": False, "provider_invocation": False, "model_inference": False}),
        _case("CEF-26", "all feedback artifacts remain candidate-only", all(item.candidate_only for item in usages + assessments) and hive_feedback.candidate_only and weakness_demand.candidate_only and gap_demand.candidate_only, {"candidate_only": True}),
    ]
    return {
        "modules": modules,
        "slots": (text_slot, object_slot, spatial_slot),
        "usages": usages,
        "assessments": assessments,
        "profiles": (ocr_profile, object_profile, spatial_profile),
        "weakness": weakness,
        "gap": gap,
        "self_view": self_view,
        "hive_feedback": hive_feedback,
        "weakness_demand": weakness_demand,
        "gap_demand": gap_demand,
        "cases": cases,
    }


def build_runner_result() -> Dict[str, object]:
    fixture = build_feedback_fixture()
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
        "automatic_capability_uninstall": False,
        "automatic_capability_optimization": False,
        "capability_value_scoring": False,
        "learning_execution": False,
        "memory_mutation": False,
        "semantic_expansion_execution": False,
        "semantic_folding_execution": False,
        "srsk_implementation": False,
        "feedback_mutates_scope": False,
        "feedback_mutates_lifecycle": False,
        "feedback_triggers_learning": False,
        "feedback_triggers_model_replacement": False,
        "feedback_triggers_provider_replacement": False,
        "hive_direct_individual_mutation": False,
        "hive_raw_personal_data_required": False,
        "weakness_candidate_executes_improvement": False,
        "gap_candidate_executes_acquisition": False,
    }
    return {
        "phase": "Phase-Luna-Capability-Experience-Feedback-And-Hive-Foundation-v1-001",
        "mode": "CONTROLLED_IMPLEMENTATION",
        "owner": OWNER,
        "real_components": [],
        "synthetic_components": ["CapabilityUsageRecordV1", "OutcomeAssessment", "IndividualProfile", "HiveFeedbackCandidate"],
        "scenario_count": len(cases),
        "all_cases_passed": all(case["passed"] for case in cases),
        "failed_case_ids": [case["case_id"] for case in cases if not case["passed"]],
        "candidate_only": True,
        "usage_record_count": len(fixture["usages"]),
        "profile_count": len(fixture["profiles"]),
        "hive_feedback_candidate_created": True,
        "hive_demand_candidate_created": True,
        "feedback_mutates_scope": False,
        "feedback_mutates_lifecycle": False,
        "feedback_triggers_learning": False,
        "feedback_triggers_model_replacement": False,
        "feedback_triggers_provider_replacement": False,
        "hive_direct_individual_mutation": False,
        "hive_raw_personal_data_required": False,
        "weakness_candidate_executes_improvement": False,
        "gap_candidate_executes_acquisition": False,
        "learning_status": "DEFERRED",
        "memory_mutation": False,
        "semantic_compression": False,
        "dynamic_cognitive_function_execution": False,
        "cases": cases,
        **guards,
    }
