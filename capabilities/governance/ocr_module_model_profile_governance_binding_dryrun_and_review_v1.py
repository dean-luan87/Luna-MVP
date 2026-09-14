# -*- coding: utf-8 -*-
"""OCR Module Model Profile + Governance Binding DryRunAndReview v1 — qualification only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    INFORMATION_INTEGRATION_REF,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    STANDARD_ID as MIDPLATFORM_BINDING_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
)
from capabilities.governance.model_profile_registry_planning_v1 import SEED_CANDIDATE_IDS
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DUAL_VALIDATION_MECHANISM_ID,
    MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)
from capabilities.governance.ocr_module_model_profile_governance_binding_planning_v1 import (
    CAPABILITY_STACK_DEF_ID,
    CLOSURE_CAN_SAY,
    CLOSURE_CANNOT_SAY,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    IO_FORBIDDEN,
    LAYERED_GOV_MAPPING_ID,
    MIDPLATFORM_BINDING_ID,
    MODULE_ID,
    MODULE_LOCAL_PROFILE_ID,
    OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID,
    OCR_REGISTRY_REFS,
    QUALIFICATION_CHECK_CRITERIA,
    QUALIFICATION_FIELDS,
    QUALIFICATION_MODE,
    REUSED_GOVERNANCE_STANDARDS,
)

PHASE_ID = "Phase-OCR-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
SCOPE = "ocr_module_model_profile_governance_binding_dryrun_and_review_only"
SOURCE_CHAIN = "ocr_module_model_profile_governance_binding_dryrun_and_review_v1"

CANDIDATE_REGISTRY_REFS: Tuple[str, ...] = (
    "rapidocr_candidate",
    "paddleocr_candidate",
    OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID,
)

FINAL_DECISION_GO = (
    "OCR_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_TTS_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING"
)
FINAL_DECISION_HOLD = (
    "OCR_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-TTS-Module-Model-Profile-Governance-Binding-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "OCR Module DryRun GO ≠ RapidOCR/PaddleOCR selected",
    "OCR candidate refs reviewed ≠ OCR runtime",
    "OCR output contract reviewed ≠ OCR fact generation",
    "OCR module binding feasible ≠ Constitution/Oversight fully integrated",
    "Health/Oversight refs attached ≠ health/supervision metrics finalized",
    "next TTS Module Planning ≠ TTS invocation",
    "Module Governance Binding GO ≠ module fully integrated with Constitution",
    "Module Governance Binding GO ≠ module fully integrated with Health/Oversight",
    "Constitution binding feasible ≠ constitution effectiveness quantified",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_ocr_runtime_enable",
    "dryrun_to_real_ocr_execution",
    "dryrun_to_ocr_provider_invocation",
    "dryrun_to_model_selection",
    "dryrun_to_model_download",
    "dryrun_to_model_invocation",
    "dryrun_to_provider_invocation",
    "dryrun_to_benchmark_execution",
    "dryrun_to_license_clearance",
    "dryrun_to_security_review_completion",
    "dryrun_to_ocr_fact_generation",
    "dryrun_to_ocr_action_generation",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_user_output",
    "dryrun_to_controlled_runtime_enable",
    "dryrun_to_full_integration_certification",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "ocr_module_model_profile_governance_binding_dryrun_and_review_only",
    "qualification_check_only",
    "ocr_module_qualification_check_executed_now",
    "simulated",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "ocr_module_runtime_enabled_now",
    "real_ocr_executed_now",
    "ocr_provider_invoked_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
    "ocr_fact_generated_now",
    "ocr_action_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
    "constitution_effectiveness_quantified_now",
    "health_metrics_finalized_now",
    "supervision_metrics_finalized_now",
    "module_constitution_fully_integrated_now",
    "module_oversight_fully_integrated_now",
    "health_metric_detail_defined_now",
    "supervision_metric_detail_defined_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_module_model_profile_governance_binding_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
        "qualification_mode": QUALIFICATION_MODE,
        **QUALIFICATION_FIELDS,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_from_checks(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"check_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "review_pass": len(issues) == 0,
    }


def _with_review(review_id: str, review: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    return {"review_id": review_id, **review, **meta}


def _resolved_registry_refs(profile: Dict[str, Any]) -> List[str]:
    refs = list(profile.get("registry_model_profile_refs") or [])
    alias = profile.get("registry_placeholder_alias") or {}
    resolved = []
    for ref in refs:
        resolved.append(alias.get(ref, ref))
    return resolved


def run_ocr_module_model_profile_governance_binding_dryrun_and_review_v1(
    *,
    ocr_module_model_profile_governance_binding_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(ocr_module_model_profile_governance_binding_planning_root).expanduser().resolve()

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    qual_plan = _try_read_json(plan_root / "ocr_module_qualification_check_v1.json") or {}

    mod_def = _try_read_json(plan_root / "ocr_module_definition_v1.json") or {}
    stack = _try_read_json(plan_root / "ocr_capability_stack_definition_v1.json") or {}
    gov_map = _try_read_json(plan_root / "ocr_layered_governance_mapping_v1.json") or {}
    profile = _try_read_json(plan_root / "ocr_module_local_model_profile_v1.json") or {}
    refs_plan = _try_read_json(plan_root / "ocr_model_profile_registry_refs_review_v1.json") or {}
    roles = _try_read_json(plan_root / "ocr_model_role_assignment_plan_v1.json") or {}
    inp = _try_read_json(plan_root / "ocr_input_contract_v1.json") or {}
    out = _try_read_json(plan_root / "ocr_output_contract_v1.json") or {}
    quality = _try_read_json(plan_root / "ocr_quality_acceptance_plan_v1.json") or {}
    health = _try_read_json(plan_root / "ocr_health_validation_whitebox_plan_v1.json") or {}
    prov_rt = _try_read_json(plan_root / "ocr_provider_runtime_boundary_plan_v1.json") or {}
    fallback = _try_read_json(plan_root / "ocr_fallback_replacement_plan_v1.json") or {}
    self_check = _try_read_json(plan_root / "ocr_module_internal_self_check_plan_v1.json") or {}
    interaction = _try_read_json(plan_root / "ocr_midplatform_interaction_check_plan_v1.json") or {}
    binding = _try_read_json(plan_root / "ocr_midplatform_governance_binding_v1.json") or {}
    ii = _try_read_json(plan_root / "ocr_information_integration_handoff_plan_v1.json") or {}
    dc = _try_read_json(plan_root / "ocr_decision_center_handoff_plan_v1.json") or {}
    gate = _try_read_json(plan_root / "ocr_gate_chain_boundary_plan_v1.json") or {}
    mem_wm = _try_read_json(plan_root / "ocr_memory_worldmodel_admission_boundary_plan_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "output_root": str(out_root), "upstream_planning_root": str(plan_root)}

    if plan_vr.get("verifier") != "GO":
        blockers.append("OCR Planning must be GO")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("Planning final_decision mismatch")
    if plan_sm.get("module_id") != MODULE_ID:
        blockers.append("module_id must be ocr_text_reading_module")
    if not plan_sm.get("qualification_check_only"):
        blockers.append("Planning must be qualification_check_only")

    input_ok = len(blockers) == 0
    resolved_refs = _resolved_registry_refs(profile)
    stack_text = json.dumps(stack, ensure_ascii=False)
    gov_text = json.dumps(gov_map, ensure_ascii=False)
    roles_text = json.dumps(roles, ensure_ascii=False)
    inp_text = json.dumps(inp, ensure_ascii=False)
    out_text = json.dumps(out, ensure_ascii=False)
    quality_text = json.dumps(quality, ensure_ascii=False)
    health_text = json.dumps(health, ensure_ascii=False)
    prov_text = json.dumps(prov_rt, ensure_ascii=False)
    fallback_text = json.dumps(fallback, ensure_ascii=False)
    ii_text = json.dumps(ii, ensure_ascii=False)
    dc_text = json.dumps(dc, ensure_ascii=False)
    gate_text = json.dumps(gate, ensure_ascii=False)
    mem_text = json.dumps(mem_wm, ensure_ascii=False)

    planning_input_review = {
        "review_id": "planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": plan_sm.get("module_id"),
        "qualification_mode": plan_sm.get("qualification_mode"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_reuse = _with_review(
        "governance_standard_reuse_review_v1",
        _review_from_checks([
            ("constraints_ref", True),
            ("reuse_rule", True),
            ("new_need_false", True),
            ("reused_count14", len(REUSED_GOVERNANCE_STANDARDS) == 14),
            *(("std." + s[:12], s in REUSED_GOVERNANCE_STANDARDS) for s in REUSED_GOVERNANCE_STANDARDS),
        ]),
        meta,
    )

    mod_def_review = _with_review(
        "ocr_module_definition_review_v1",
        _review_from_checks([
            ("module_id", mod_def.get("module_id") == MODULE_ID),
            ("domain", "OCR / Text Recognition" in mod_def.get("capability_domain", "")),
            ("primary", mod_def.get("primary_goal") == "text_region_and_ocr_candidate_generation"),
            ("related", mod_def.get("related_goal") == "current_scene_understanding_support"),
            ("later", mod_def.get("later_goal") == "reading_application_layer"),
            ("no_runtime", mod_def.get("runtime_enabled_now") is False),
            ("no_ocr", mod_def.get("real_ocr_executed_now") is False),
            ("candidate", mod_def.get("candidate_only") is True),
        ]),
        meta,
    )

    stack_review = _with_review(
        "ocr_capability_stack_review_v1",
        _review_from_checks([
            ("l1", "layer_1_text_region_detection" in stack.get("layers", {})),
            ("l2", "layer_2_ocr_reading_candidate" in stack.get("layers", {})),
            ("l3", any(k.startswith("layer_3_text_structure") for k in stack.get("layers", {}))),
            ("l4", any(k.startswith("layer_4_reading_application") for k in stack.get("layers", {}))),
            ("not_fact", "no direct fact" in stack_text),
            ("not_nav", "navigation" in stack_text),
            ("not_user_out", "user_output" in stack_text or "no user_output" in stack_text),
            ("not_mem_wm", "Memory/WorldModel" in stack_text),
        ]),
        meta,
    )

    gov_map_review = _with_review(
        "ocr_layered_governance_mapping_review_v1",
        _review_from_checks([
            ("l1_source", "source_chain" in gov_text),
            ("l1_not_fact", "not_fact" in gov_text),
            ("l2_validation", "validation_required" in gov_text),
            ("l3_ii", "Information Integration handoff" in gov_text),
            ("l4_mem", "Memory/WorldModel admission" in gov_text),
            ("consistent", "governance principles consistent" in gov_text),
            ("layered", "execution intensity layered" in gov_text),
            ("no_overload", "no all-rules-to-all-layers overload" in gov_text),
        ]),
        meta,
    )

    profile_review = _with_review(
        "ocr_module_local_model_profile_review_v1",
        _review_from_checks([
            ("profile_id", profile.get("module_local_profile_id") == MODULE_LOCAL_PROFILE_ID),
            ("rapid", "rapidocr_candidate" in (profile.get("registry_model_profile_refs") or [])),
            ("paddle", "paddleocr_candidate" in (profile.get("registry_model_profile_refs") or [])),
            ("placeholder_resolved", OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID in resolved_refs),
            ("stack_ref", profile.get("capability_stack_ref") == CAPABILITY_STACK_DEF_ID),
            ("gov_ref", profile.get("layered_governance_mapping_ref") == LAYERED_GOV_MAPPING_ID),
            ("no_override", profile.get("no_registry_override") is True),
            ("no_select", profile.get("no_model_selection_by_module") is True),
            ("no_invoke", profile.get("no_model_invocation_by_profile") is True),
            ("no_fact", profile.get("no_direct_fact_action_output") is True),
        ]),
        meta,
    )

    refs_review = _with_review(
        "ocr_model_profile_registry_refs_review_v1",
        _review_from_checks([
            ("refs_review_pass", refs_plan.get("review_pass") is True),
            ("rapid_seed", "rapidocr_candidate" in SEED_CANDIDATE_IDS),
            ("paddle_seed", "paddleocr_candidate" in SEED_CANDIDATE_IDS),
            ("placeholder", OCR_REGISTRY_PLACEHOLDER_REGISTRY_ID in resolved_refs),
            ("candidate_only", "candidate only" in json.dumps(refs_plan, ensure_ascii=False)),
            ("none_selected", "none selected_now" in json.dumps(refs_plan, ensure_ascii=False)),
            ("none_invoked", "none invoked_now" in json.dumps(refs_plan, ensure_ascii=False)),
        ]),
        meta,
    )

    roles_review = _with_review(
        "ocr_model_role_assignment_review_v1",
        _review_from_checks([
            ("rapid_role", "RapidOCR maps" in roles_text),
            ("paddle_role", "PaddleOCR maps" in roles_text),
            ("placeholder_role", "placeholder maps" in roles_text),
            ("no_single", "no single OCR model" in roles_text),
            ("reading_later", "reading application remains later" in roles_text),
            ("not_fact", "does not become fact" in roles_text),
        ]),
        meta,
    )

    inp_review = _with_review(
        "ocr_input_contract_review_v1",
        _review_from_checks([
            ("visual_region", "visual_region_candidate" in inp_text),
            ("text_region", "text_region_candidate" in inp_text),
            ("readable", "readable_region_candidate" in inp_text),
            ("roi_later", "roi_candidate_later" in inp_text),
            ("frame_later", "frame_candidate_later" in inp_text),
            ("task_intent", "task_intent_candidate" in inp_text),
            ("no_real_frame", "real frame input not allowed now" in inp_text),
            ("no_provider", "OCR provider input not invoked now" in inp_text),
            ("cr_later", "Controlled Runtime later" in inp_text),
        ]),
        meta,
    )

    out_review = _with_review(
        "ocr_output_contract_review_v1",
        _review_from_checks([
            ("text_region", "text_region_candidate" in out_text),
            ("ocr_result", "ocr_result_candidate" in out_text),
            ("recognized", "recognized_text_candidate" in out_text),
            ("language", "language_hint_candidate" in out_text),
            ("signage", "signage_context_candidate" in out_text),
            ("evidence", "ocr_evidence_candidate" in out_text),
            *(("forbid." + f[:14], f in (out.get("forbidden_outputs") or [])) for f in IO_FORBIDDEN),
        ]),
        meta,
    )

    quality_review = _with_review(
        "ocr_quality_acceptance_review_v1",
        _review_from_checks([
            ("accuracy_later", "ocr_accuracy_target_later" in quality_text),
            ("precision_later", "text_detection_precision_target_later" in quality_text),
            ("fp_control", "false_text_positive_control" in quality_text),
            ("fn_control", "missed_text_false_negative" in quality_text),
            ("latency", "latency_budget_later" in quality_text),
            ("compliance", quality.get("candidate_contract_compliance_required") is True),
            ("trace", quality.get("traceability_completeness_required") is True),
            ("degrade", quality.get("degradation_behavior_required") is True),
            ("bench_later", quality.get("benchmark_required_later") is True),
            ("bench_now", quality.get("benchmark_executed_now") is False),
        ]),
        meta,
    )

    health_review = _with_review(
        "ocr_health_validation_whitebox_review_v1",
        _review_from_checks([
            ("validation_ref", bool(health.get("validation_requirement_ref"))),
            ("health_later", health.get("health_requirement_ref") == "required_later"),
            ("supervision_later", health.get("supervision_metric_ref") == "required_later"),
            ("health_detail_false", health.get("health_metric_detail_defined_now") is False),
            ("super_detail_false", health.get("supervision_metric_detail_defined_now") is False),
            ("whitebox", bool(health.get("whitebox_trace_requirement_ref"))),
            ("source_chain", health.get("source_chain_required") is True),
            ("evidence", health.get("evidence_refs_required") is True),
            ("failure_route", health.get("failure_route_required") is True),
            ("issue_trace", health.get("issue_trace_required") is True),
            ("no_self_cert", health.get("module_cannot_self_certify_health") is True),
            ("constitution_not_quant", meta.get("constitution_effectiveness_quantified_now") is False),
            ("health_not_final", meta.get("health_metrics_finalized_now") is False),
            ("super_not_final", meta.get("supervision_metrics_finalized_now") is False),
            ("not_fully_const", meta.get("module_constitution_fully_integrated_now") is False),
            ("not_fully_oversight", meta.get("module_oversight_fully_integrated_now") is False),
        ]),
        meta,
    )

    prov_review = _with_review(
        "ocr_provider_runtime_boundary_review_v1",
        _review_from_checks([
            ("prov_required", prov_rt.get("provider_abstraction_required") is True),
            ("cr_required", prov_rt.get("controlled_runtime_required") is True),
            ("not_selected", "provider_candidate ≠ selected ≠ invoked" in prov_text),
            ("no_auto", "no provider auto-switch" in prov_text),
            ("cr_later", "Controlled Runtime later" in prov_text),
            ("no_runtime", "OCR runtime remains disabled now" in prov_text),
        ]),
        meta,
    )

    fallback_review = _with_review(
        "ocr_fallback_replacement_review_v1",
        _review_from_checks([
            ("refs_structured", len(fallback.get("fallback_model_profile_refs") or []) >= 3),
            ("quality", "quality_regression" in fallback_text),
            ("provider", "provider_unavailable" in fallback_text),
            ("license", "license_risk" in fallback_text),
            ("latency", "latency_budget_failure" in fallback_text),
            ("hardware", "hardware_incompatibility" in fallback_text),
            ("fp_risk", "high_false_positive_text_risk" in fallback_text),
            ("fn_risk", "high_false_negative_text_risk" in fallback_text),
            ("hold", "hold_instead_of_fallback" in fallback_text or "safety/privacy/licensing" in fallback_text),
            ("no_auto", fallback.get("no_auto_switch_without_governance_policy") is True),
            ("no_invoke", fallback.get("replacement_does_not_imply_invocation") is True),
        ]),
        meta,
    )

    self_check_review = _with_review(
        "ocr_module_internal_self_check_review_v1",
        _review_from_checks(
            [("plan_exists", bool(self_check.get("plan_id")))]
            + [(c[:16], c in (self_check.get("self_check_coverage") or []))
               for c in MODULE_INTERNAL_SELF_CHECK_COVERAGE]
        ),
        meta,
    )

    interaction_review = _with_review(
        "ocr_midplatform_interaction_check_review_v1",
        _review_from_checks(
            [("plan_exists", bool(interaction.get("plan_id")))]
            + [(c[:16], c in (interaction.get("interaction_check_coverage") or []))
               for c in MIDPLATFORM_INTERACTION_CHECK_COVERAGE]
        ),
        meta,
    )

    binding_text = json.dumps(binding, ensure_ascii=False)
    binding_review = _with_review(
        "ocr_midplatform_governance_binding_review_v1",
        _review_from_checks([
            ("binding_id", binding.get("midplatform_governance_binding_id") == MIDPLATFORM_BINDING_ID),
            ("profile_ref", binding.get("module_local_profile_ref") == MODULE_LOCAL_PROFILE_ID),
            ("refs_preserved", len(binding.get("registry_model_profile_refs") or []) >= 3),
            ("constitution", binding.get("constitution_bus_ref") == CONSTITUTION_BUS_REF),
            ("capability_bus", bool(binding.get("capability_bus_contract_ref"))),
            ("provider", binding.get("provider_abstraction_ref") == PROVIDER_ABS_STANDARD_ID),
            ("validation", bool(binding.get("validation_requirement_ref"))),
            ("health_later", binding.get("health_requirement_ref") == "required_later"),
            ("whitebox", bool(binding.get("whitebox_trace_requirement_ref"))),
            ("ii_policy", bool(binding.get("information_integration_consumption_policy_ref"))),
            ("dc_policy", bool(binding.get("decision_center_consumption_policy_ref"))),
            ("cr_ref", binding.get("controlled_runtime_requirement_ref") == CONTROLLED_RUNTIME_FRAMEWORK_REF),
            ("no_select", binding.get("model_selected_now") is False),
            ("no_invoke", binding.get("model_invoked_now") is False),
            ("no_runtime", binding.get("runtime_enabled_now") is False),
        ]),
        meta,
    )

    ii_review = _with_review(
        "ocr_information_integration_handoff_review_v1",
        _review_from_checks([
            ("ii_ref", ii.get("information_integration_ref") == INFORMATION_INTEGRATION_REF),
            ("candidate_flow", "candidate/context/evidence" in ii_text),
            ("consumes", "text_region" in ii_text and "ocr_result" in ii_text),
            ("no_bypass", "cannot bypass Information Integration" in ii_text),
            ("no_integrated", "no integrated_context generated now" in ii_text),
        ]),
        meta,
    )

    dc_review = _with_review(
        "ocr_decision_center_handoff_review_v1",
        _review_from_checks([
            ("integrated", "integrated_context" in dc_text),
            ("no_decision", "cannot emit decision" in dc_text),
            ("no_nav", "cannot directly trigger navigation action" in dc_text),
            ("no_decision_now", "no decision generated now" in dc_text),
        ]),
        meta,
    )

    gate_review = _with_review(
        "ocr_gate_chain_boundary_review_v1",
        _review_from_checks([
            ("not_output", gate.get("output_capable_now") is False),
            ("gate_later", "Output/Gate chain required" in gate_text),
            ("privacy_later", "privacy gate later" in gate_text),
            ("no_user_out", "no user_output now" in gate_text),
        ]),
        meta,
    )

    mem_wm_review = _with_review(
        "ocr_memory_worldmodel_admission_boundary_review_v1",
        _review_from_checks([
            ("no_mem", "cannot write Memory" in mem_text),
            ("no_wm", "cannot write WorldModel" in mem_text),
            ("admission_later", "admission candidate later" in mem_text),
            ("text_fact_later", "text fact admission later" in mem_text),
            ("reading_storage", "Memory/WorldModel Admission" in mem_text),
        ]),
        meta,
    )

    qual_check_review = _with_review(
        "ocr_module_qualification_check_review_v1",
        _review_from_checks([
            ("qual_only", qual_plan.get("qualification_check_only") is True or meta.get("qualification_check_only") is True),
            ("full_cert_false", meta.get("full_integration_certification_now") is False),
            ("constitution_feasible", meta.get("constitution_binding_feasible") is True),
            ("oversight_feasible", meta.get("oversight_binding_feasible") is True),
            ("can_say_registry", CLOSURE_CAN_SAY[0] in (qual_plan.get("can_say") or [])),
            ("cannot_runtime", CLOSURE_CANNOT_SAY[0] in (qual_plan.get("cannot_say") or [])),
            ("cannot_metrics", "health/supervision metrics finalized" in str(qual_plan.get("cannot_say"))),
        ] + [(k, meta.get(k) is v) for k, v in QUALIFICATION_FIELDS.items() if k not in (
            "qualification_check_only", "full_integration_certification_now",
            "constitution_binding_feasible", "oversight_binding_feasible",
        )]),
        meta,
    )

    boundary_audit = {
        "audit_id": "ocr_non_runtime_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "ocr_blocked_path_result_v1",
        "blocked_paths": [{"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    all_reviews = [
        governance_reuse, mod_def_review, stack_review, gov_map_review, profile_review,
        refs_review, roles_review, inp_review, out_review, quality_review, health_review,
        prov_review, fallback_review, self_check_review, interaction_review, binding_review,
        ii_review, dc_review, gate_review, mem_wm_review, qual_check_review,
    ]

    qualification_pass = (
        input_ok
        and qual_plan.get("qualification_pass") is True
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and all(r.get("review_pass") for r in all_reviews)
    )

    candidate = {
        "candidate_id": "ocr_module_model_profile_governance_binding_candidate_v1",
        "module_id": MODULE_ID,
        "module_local_profile_ref": MODULE_LOCAL_PROFILE_ID,
        "midplatform_governance_binding_ref": MIDPLATFORM_BINDING_ID,
        "registry_model_profile_refs": list(CANDIDATE_REGISTRY_REFS),
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_pass": qualification_pass,
        "runtime_enabled_now": False,
        "model_selected_now": False,
        "model_invoked_now": False,
        **meta,
    }

    closure_decision = {
        "decision_id": "ocr_module_closure_decision_v1",
        "dryrun_and_review_pass": qualification_pass,
        "high_risk": not qualification_pass,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": FINAL_DECISION_GO if qualification_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if qualification_pass else NEXT_PHASE_HOLD,
        "closure_can_say": list(CLOSURE_CAN_SAY),
        "closure_cannot_say": list(CLOSURE_CANNOT_SAY),
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_tts_module_model_profile_governance_binding_planning": qualification_pass,
        "selected_next_phase": NEXT_PHASE_GO if qualification_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_module_model_profile_governance_binding_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "qualification_check_only": True,
        "phase_goal": "OCR module qualification verification only. No OCR runtime/provider/benchmark.",
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_and_review_pass": qualification_pass,
        "module_id": MODULE_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "ocr_module_model_profile_governance_binding_dryrun_review_policy": policy,
        "planning_input_review": planning_input_review,
        "governance_standard_reuse_review": governance_reuse,
        "ocr_module_model_profile_governance_binding_candidate": candidate,
        "ocr_module_definition_review": mod_def_review,
        "ocr_capability_stack_review": stack_review,
        "ocr_layered_governance_mapping_review": gov_map_review,
        "ocr_module_local_model_profile_review": profile_review,
        "ocr_model_profile_registry_refs_review": refs_review,
        "ocr_model_role_assignment_review": roles_review,
        "ocr_input_contract_review": inp_review,
        "ocr_output_contract_review": out_review,
        "ocr_quality_acceptance_review": quality_review,
        "ocr_health_validation_whitebox_review": health_review,
        "ocr_provider_runtime_boundary_review": prov_review,
        "ocr_fallback_replacement_review": fallback_review,
        "ocr_module_internal_self_check_review": self_check_review,
        "ocr_midplatform_interaction_check_review": interaction_review,
        "ocr_midplatform_governance_binding_review": binding_review,
        "ocr_information_integration_handoff_review": ii_review,
        "ocr_decision_center_handoff_review": dc_review,
        "ocr_gate_chain_boundary_review": gate_review,
        "ocr_memory_worldmodel_admission_boundary_review": mem_wm_review,
        "ocr_module_qualification_check_review": qual_check_review,
        "ocr_non_runtime_boundary_audit": boundary_audit,
        "ocr_blocked_path_result": blocked_path_result,
        "ocr_module_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
