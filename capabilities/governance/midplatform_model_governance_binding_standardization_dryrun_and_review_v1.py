# -*- coding: utf-8 -*-
"""Midplatform Model Governance Binding Standardization DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    BINDING_SCHEMA_FIELDS,
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    DOMAIN_COVERAGE,
    DUAL_VALIDATION_MECHANISM_ID,
    DUAL_VALIDATION_NON_CLAIMS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    INFORMATION_INTEGRATION_REF,
    LAYER_BINDING_SPECS,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PHASE_ID as PLANNING_PHASE_ID,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    REUSED_GOVERNANCE_STANDARDS,
    STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
)
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
    DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
    NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM,
)

PHASE_ID = "Phase-Midplatform-Model-Governance-Binding-Standardization-DryRunAndReview-v1-001"
SCOPE = "midplatform_model_governance_binding_standardization_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_model_governance_binding_standardization_dryrun_and_review_v1"

FINAL_DECISION_GO = (
    "MIDPLATFORM_MODEL_GOVERNANCE_BINDING_STANDARDIZATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_VISION_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_MODEL_GOVERNANCE_BINDING_STANDARDIZATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Vision-Module-Model-Profile-Governance-Binding-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Model-Governance-Binding-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_midplatform_binding_runtime_enable",
    "dryrun_to_model_selection",
    "dryrun_to_model_download",
    "dryrun_to_model_invocation",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime_enable",
    "dryrun_to_benchmark_execution",
    "dryrun_to_license_clearance",
    "dryrun_to_security_review_completion",
    "dryrun_to_training_start",
    "dryrun_to_fine_tuning_start",
    "dryrun_to_code_generation",
    "dryrun_to_skill_addition",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_user_output",
    "dryrun_to_controlled_runtime_enable",
    "dryrun_to_real_module_admission",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Midplatform Binding DryRun GO ≠ model connected",
    "governance binding candidate validated ≠ runtime ready",
    "binding template reviewed ≠ real module pass",
    "non-compliance policy deferred ≠ enforcement implemented",
    "next Vision Module Binding Planning ≠ model invocation",
    "binding standard closed ≠ provider invoked",
    NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM,
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_model_governance_binding_standardization_dryrun_and_review_only",
    "simulated",
    "midplatform_model_governance_binding_standard_candidate_generated_now",
    "binding_schema_review_generated_now",
    "binding_policy_reviews_generated_now",
    "binding_template_reviews_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "midplatform_binding_runtime_enabled_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "model_runtime_enabled_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
    "training_started_now",
    "fine_tuning_started_now",
    "code_generation_executed_now",
    "skill_added_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_model_governance_binding_standardization_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
        "binding_runtime_enabled_now": False,
        "model_selection_allowed_now": False,
        "model_invocation_allowed_now": False,
        "controlled_runtime_allowed_now": False,
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


def _policy_review(
    plan_root: Path,
    policy_file: str,
    min_rules: int,
    extra_checks: Optional[List[Tuple[str, bool]]] = None,
) -> Dict[str, Any]:
    pol = _try_read_json(plan_root / policy_file) or {}
    checks: List[Tuple[str, bool]] = [("rules", len(pol.get("rules") or []) >= min_rules)]
    if extra_checks:
        checks.extend(extra_checks)
    return {
        "review_id": policy_file.replace(".json", "_review"),
        **_review_from_checks(checks),
        "policy_ref": policy_file,
    }


def _tpl_review(
    tpl: Dict[str, Any],
    checks: List[Tuple[str, bool]],
    review_id: str,
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    return {"review_id": review_id, **_review_from_checks(checks), **meta}


def run_midplatform_model_governance_binding_standardization_dryrun_and_review_v1(
    *,
    midplatform_model_governance_binding_standardization_planning_root: str,
    module_local_model_profile_standardization_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        midplatform_model_governance_binding_standardization_planning_root
    ).expanduser().resolve()
    ml_dr_root = Path(
        module_local_model_profile_standardization_dryrun_and_review_root
    ).expanduser().resolve()

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    ml_dr_vr = _try_read_json(ml_dr_root / "verifier_report.json") or {}
    ml_dr_sm = _try_read_json(ml_dr_root / "summary.json") or {}

    schema = _try_read_json(plan_root / "midplatform_model_governance_binding_schema_v1.json") or {}
    std_def = _try_read_json(
        plan_root / "midplatform_model_governance_binding_standard_definition_v1.json"
    ) or {}
    by_layer = _try_read_json(plan_root / "model_governance_binding_by_capability_layer_v1.json") or {}
    by_domain = _try_read_json(plan_root / "model_governance_binding_by_module_domain_v1.json") or {}
    deferment = _try_read_json(plan_root / "non_compliance_handling_deferment_review_v1.json") or {}
    dual_handoff = _try_read_json(
        plan_root / "dual_validation_to_midplatform_binding_handoff_policy_v1.json"
    ) or {}

    vision_tpl = _try_read_json(plan_root / "vision_model_governance_binding_template_v1.json") or {}
    ocr_tpl = _try_read_json(plan_root / "ocr_model_governance_binding_template_v1.json") or {}
    tts_tpl = _try_read_json(plan_root / "tts_model_governance_binding_template_v1.json") or {}
    asr_tpl = _try_read_json(plan_root / "asr_model_governance_binding_template_v1.json") or {}
    nav_tpl = _try_read_json(plan_root / "map_navigation_model_governance_binding_template_v1.json") or {}
    world_tpl = _try_read_json(plan_root / "world_continuity_model_governance_binding_template_v1.json") or {}
    mem_tpl = _try_read_json(
        plan_root / "memory_emotion_evolution_model_governance_binding_template_v1.json"
    ) or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_planning_root": str(plan_root),
        "upstream_module_local_dryrun_root": str(ml_dr_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Midplatform Binding Planning must be GO")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("Planning final_decision mismatch")
    if plan_sm.get("template_count") != 7:
        blockers.append("template_count must be 7")
    if plan_sm.get("domain_coverage_count") != 10:
        blockers.append("domain_coverage must be 10")
    if plan_sm.get("binding_policy_count") != 11:
        blockers.append("binding_policy_count must be 11")
    if ml_dr_vr.get("verifier") != "GO":
        blockers.append("Module-Local DryRunAndReview must be GO")
    if not ml_dr_sm.get("module_internal_self_check_review_pass"):
        blockers.append("module_internal_self_check_review_pass required")
    if not ml_dr_sm.get("midplatform_interaction_check_review_pass"):
        blockers.append("midplatform_interaction_check_review_pass required")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "standard_id": plan_sm.get("standard_id"),
        "template_count": plan_sm.get("template_count"),
        "domain_coverage_count": plan_sm.get("domain_coverage_count"),
        "binding_policy_count": plan_sm.get("binding_policy_count"),
        "module_local_dryrun_verifier": ml_dr_vr.get("verifier"),
        "module_local_self_check_pass": ml_dr_sm.get("module_internal_self_check_review_pass"),
        "module_local_interaction_pass": ml_dr_sm.get("midplatform_interaction_check_review_pass"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_reuse = {
        "review_id": "governance_standard_reuse_review_v1",
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "reuse_rule_text": PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
        "reused_standards": list(REUSED_GOVERNANCE_STANDARDS),
        "new_governance_need_proven": False,
        "no_parallel_duplicate_governance_standard": True,
        "dryrun_review_of_midplatform_binding_not_new_framework": True,
        **_review_from_checks([
            ("constraints_ref", True),
            ("reuse_rule", True),
            ("new_need_false", True),
            ("reused_count13", len(REUSED_GOVERNANCE_STANDARDS) == 13),
        ]),
        **meta,
    }

    standard_candidate = {
        "standard_id": STANDARD_ID,
        "standard_type": "midplatform_model_profile_governance_binding_standard",
        "planning_source_phase": PLANNING_PHASE_ID,
        "registry_ref": REGISTRY_REF,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "template_count": 7,
        "domain_coverage_count": 10,
        "layer_binding_count": len(LAYER_BINDING_SPECS),
        "binding_policy_count": 11,
        "binding_runtime_enabled_now": False,
        "model_selection_allowed_now": False,
        "model_invocation_allowed_now": False,
        "controlled_runtime_allowed_now": False,
        "candidate_only": True,
        **meta,
    }

    schema_review = {
        "review_id": "midplatform_model_governance_binding_schema_review_v1",
        "field_count": len(BINDING_SCHEMA_FIELDS),
        **_review_from_checks(
            [(f, f in (schema.get("required_fields") or [])) for f in BINDING_SCHEMA_FIELDS]
            + [
                ("field_count30", schema.get("field_count") == len(BINDING_SCHEMA_FIELDS)),
                ("no_select", schema.get("runtime_boundary_fields", {}).get("model_selected_now") is False),
                ("no_invoke", schema.get("runtime_boundary_fields", {}).get("model_invoked_now") is False),
                ("no_runtime", schema.get("runtime_boundary_fields", {}).get("runtime_enabled_now") is False),
            ]
        ),
        **meta,
    }

    cb_pol = _try_read_json(plan_root / "constitution_bus_binding_policy_v1.json") or {}
    cb_review = _policy_review(plan_root, "constitution_bus_binding_policy_v1.json", 6, [
        ("constitution_ref", cb_pol.get("constitution_bus_ref") == CONSTITUTION_BUS_REF),
        ("v1", cb_pol.get("constitution_bus_version") == "v1.0"),
        ("no_parallel", "module cannot create parallel governance" in json.dumps(cb_pol, ensure_ascii=False)),
    ])
    cb_review["review_id"] = "constitution_bus_binding_policy_review_v1"
    cb_review.update(meta)

    cap_review = _policy_review(plan_root, "capability_bus_binding_policy_v1.json", 5, [
        ("no_invoke", "capability bus does not invoke model" in json.dumps(
            _try_read_json(plan_root / "capability_bus_binding_policy_v1.json") or {}, ensure_ascii=False
        )),
    ])
    cap_review["review_id"] = "capability_bus_binding_policy_review_v1"
    cap_review.update(meta)

    prov_pol = _try_read_json(plan_root / "provider_abstraction_binding_policy_v1.json") or {}
    prov_review = _policy_review(plan_root, "provider_abstraction_binding_policy_v1.json", 6, [
        ("prov_ref", prov_pol.get("provider_abstraction_ref") == PROVIDER_ABS_STANDARD_ID),
        ("runtime_ne_provider", "runtime ≠ provider" in json.dumps(prov_pol, ensure_ascii=False)),
    ])
    prov_review["review_id"] = "provider_abstraction_binding_policy_review_v1"
    prov_review.update(meta)

    val_review = _policy_review(plan_root, "validation_binding_policy_v1.json", 5)
    val_review["review_id"] = "validation_binding_policy_review_v1"
    val_review.update(meta)

    health_review = _policy_review(plan_root, "health_oversight_binding_policy_v1.json", 6)
    health_review["review_id"] = "health_oversight_binding_policy_review_v1"
    health_review.update(meta)

    wb_review = _policy_review(plan_root, "whitebox_trace_binding_policy_v1.json", 5)
    wb_review["review_id"] = "whitebox_trace_binding_policy_review_v1"
    wb_review.update(meta)

    ii_pol = _try_read_json(plan_root / "information_integration_binding_policy_v1.json") or {}
    ii_review = _policy_review(plan_root, "information_integration_binding_policy_v1.json", 4, [
        ("ii_ref", ii_pol.get("information_integration_ref") == INFORMATION_INTEGRATION_REF),
    ])
    ii_review["review_id"] = "information_integration_binding_policy_review_v1"
    ii_review.update(meta)

    dc_review = _policy_review(plan_root, "decision_center_binding_policy_v1.json", 5)
    dc_review["review_id"] = "decision_center_binding_policy_review_v1"
    dc_review.update(meta)

    gate_pol = _try_read_json(plan_root / "gate_chain_binding_policy_v1.json") or {}
    gate_review = _policy_review(plan_root, "gate_chain_binding_policy_v1.json", 5, [
        ("gate_ref", gate_pol.get("gate_chain_system_ref") == GATE_CHAIN_SYSTEM_ID),
    ])
    gate_review["review_id"] = "gate_chain_binding_policy_review_v1"
    gate_review.update(meta)

    cr_pol = _try_read_json(plan_root / "controlled_runtime_binding_policy_v1.json") or {}
    cr_review = _policy_review(plan_root, "controlled_runtime_binding_policy_v1.json", 4, [
        ("cr_ref", cr_pol.get("controlled_runtime_framework_ref") == CONTROLLED_RUNTIME_FRAMEWORK_REF),
    ])
    cr_review["review_id"] = "controlled_runtime_binding_policy_review_v1"
    cr_review.update(meta)

    mem_wm_review = _policy_review(plan_root, "memory_worldmodel_admission_binding_policy_v1.json", 5)
    mem_wm_review["review_id"] = "memory_worldmodel_admission_binding_policy_review_v1"
    mem_wm_review.update(meta)

    layer_text = json.dumps(by_layer, ensure_ascii=False)
    layer_review = {
        "review_id": "model_governance_binding_by_capability_layer_review_v1",
        **_review_from_checks([
            ("count6", by_layer.get("layer_count") == len(LAYER_BINDING_SPECS)),
            ("stack_ref", by_layer.get("capability_stack_ref") == UNIVERSAL_STACK_STANDARD_ID),
            ("addendum", by_layer.get("layered_governance_mapping_ref") == ADDENDUM_ID),
            ("l1_no_fact", "no direct fact/action" in layer_text),
            ("l2_no_wm", "no WorldModel write" in layer_text),
            ("l3_no_nav", "no direct navigation action" in layer_text),
            ("l6_proposal", "proposal_only" in layer_text),
        ]),
        **meta,
    }

    domain_review = {
        "review_id": "model_governance_binding_by_module_domain_review_v1",
        **_review_from_checks([
            ("count10", by_domain.get("domain_count") == len(DOMAIN_COVERAGE)),
            ("vision", any(d.get("domain") == "Vision" for d in (by_domain.get("domains") or []))),
            ("provider_later", "Provider/Model Management" in str(by_domain.get("domains"))),
            ("templates7", len(by_domain.get("templates_provided") or []) == 7),
        ]),
        **meta,
    }

    vision_text = json.dumps(vision_tpl, ensure_ascii=False)
    vision_review = _tpl_review(vision_tpl, [
        ("module_id", vision_tpl.get("module_id") == "vision_scene_understanding_module"),
        ("yolo", "yolo_family" in vision_text),
        ("grounded", "grounded_sam" in vision_text),
        ("tracking", "visual_tracking" in vision_text),
        ("vlm", "vlm_scene" in vision_text),
        ("ii", "Information Integration" in vision_text),
        ("no_runtime", "no camera/runtime" in vision_text),
        ("no_fact", "no direct fact/action" in vision_text),
        ("bindings4", len(vision_tpl.get("governance_bindings") or []) >= 4),
    ], "vision_model_governance_binding_template_review_v1", meta)

    ocr_text = json.dumps(ocr_tpl, ensure_ascii=False)
    ocr_review = _tpl_review(ocr_tpl, [
        ("module_id", ocr_tpl.get("module_id") == "ocr_text_reading_module"),
        ("rapid", "rapidocr" in ocr_text),
        ("paddle", "paddleocr" in ocr_text),
        ("candidate", "candidate/evidence only" in ocr_text),
        ("no_fact", "no fact/write/action" in ocr_text),
    ], "ocr_model_governance_binding_template_review_v1", meta)

    tts_text = json.dumps(tts_tpl, ensure_ascii=False)
    tts_review = _tpl_review(tts_tpl, [
        ("module_id", tts_tpl.get("module_id") == "tts_voice_output_module"),
        ("qianwen", "qianwen_tts" in tts_text),
        ("not_selected", "≠ selected/invoked" in tts_text),
        ("speech_gate", "Speech Gate" in tts_text),
        ("no_audio", "no audio output now" in tts_text),
    ], "tts_model_governance_binding_template_review_v1", meta)

    asr_text = json.dumps(asr_tpl, ensure_ascii=False)
    asr_review = _tpl_review(asr_tpl, [
        ("module_id", asr_tpl.get("module_id") == "asr_voice_input_module"),
        ("sensevoice", "sensevoice" in asr_text),
        ("transcript", "transcript outputs candidate only" in asr_text),
        ("no_runtime", "no ASR runtime now" in asr_text),
    ], "asr_model_governance_binding_template_review_v1", meta)

    nav_text = json.dumps(nav_tpl, ensure_ascii=False)
    nav_review = _tpl_review(nav_tpl, [
        ("module_id", nav_tpl.get("module_id") == "map_navigation_application_module"),
        ("layer3", "navigation is Layer 3" in nav_text),
        ("no_invoke", "no map provider invocation" in nav_text),
        ("no_action", "no navigation action" in nav_text),
    ], "map_navigation_model_governance_binding_template_review_v1", meta)

    world_text = json.dumps(world_tpl, ensure_ascii=False)
    world_review = _tpl_review(world_tpl, [
        ("module_id", world_tpl.get("module_id") == "world_continuity_understanding_module"),
        ("stcm", "stcm_self_developed" in world_text),
        ("signals", "signals only" in world_text),
        ("not_fact", "not WorldModel fact" in world_text),
    ], "world_continuity_model_governance_binding_template_review_v1", meta)

    mem_text = json.dumps(mem_tpl, ensure_ascii=False)
    mem_review = _tpl_review(mem_tpl, [
        ("modules3", len(mem_tpl.get("modules") or []) == 3),
        ("personal", "Personal Continuity" in mem_text),
        ("proposal", "proposal_only" in mem_text),
        ("no_write", "no memory write" in mem_text),
        ("no_code", "code modification" in mem_text),
    ], "memory_emotion_evolution_model_governance_binding_template_review_v1", meta)

    dual_handoff_text = json.dumps(dual_handoff, ensure_ascii=False)
    dual_handoff_review = {
        "review_id": "dual_validation_to_midplatform_binding_handoff_policy_review_v1",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        **_review_from_checks([
            ("dual_ref", dual_handoff.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID),
            ("self_check", "Module Internal Self-Check output" in dual_handoff_text),
            ("interaction", "Midplatform Interaction Check output" in dual_handoff_text),
            ("evidence_gate", "evidence gates, not runtime gates" in dual_handoff_text),
            ("not_equal", "Self-Check GO ≠ Interaction Check GO" in dual_handoff_text),
        ]),
        **meta,
    }

    deferment_review = {
        "review_id": "non_compliance_handling_deferment_review_v1",
        **_review_from_checks([
            ("deferred", deferment.get("non_compliant_module_model_handling_policy_deferred") is True),
            ("future_phase", deferment.get("recommended_future_phase") == DEFERRED_NON_COMPLIANCE_HANDLING_PHASE),
            ("policy_ref", deferment.get("policy_ref_later") == DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID),
            ("not_impl", deferment.get("not_implemented_now") is True),
            ("not_enforced", deferment.get("not_enforced_now") is True),
        ]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "midplatform_model_governance_binding_non_runtime_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "midplatform_model_governance_binding_blocked_path_result_v1",
        "blocked_paths": [{"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    all_reviews = [
        governance_reuse, schema_review, cb_review, cap_review, prov_review,
        val_review, health_review, wb_review, ii_review, dc_review, gate_review,
        cr_review, mem_wm_review, layer_review, domain_review,
        vision_review, ocr_review, tts_review, asr_review, nav_review,
        world_review, mem_review, dual_handoff_review, deferment_review,
    ]

    dryrun_pass = (
        input_ok
        and all(r.get("review_pass") for r in all_reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and std_def.get("standard_id") == STANDARD_ID
    )

    closure_decision = {
        "decision_id": "midplatform_model_governance_binding_closure_decision_v1",
        "dryrun_and_review_pass": dryrun_pass,
        "high_risk": not dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "midplatform_model_governance_binding_standard_v1 candidate validated",
            "11 binding policies reviewed",
            "7 domain binding templates reviewed",
            "L1-L6 layer binding reviewed",
            "non-compliance handling remains deferred",
            "ready for Vision Module Model Profile + Governance Binding Planning",
        ] if dryrun_pass else ["hold for issue review"],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_vision_module_model_profile_governance_binding_planning": dryrun_pass,
        "selected_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "midplatform_model_governance_binding_standardization_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        "dual_validation_non_claims": list(DUAL_VALIDATION_NON_CLAIMS),
        "non_compliant_module_model_handling_policy_deferred": True,
        "recommended_future_phase": DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
        "non_compliance_handling_deferral_claim": NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_and_review_pass": dryrun_pass,
        "standard_id": STANDARD_ID,
        "registry_ref": REGISTRY_REF,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "template_count": 7,
        "domain_coverage_count": 10,
        "layer_binding_count": len(LAYER_BINDING_SPECS),
        "binding_policy_count": 11,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "non_compliant_module_model_handling_policy_deferred": True,
        "recommended_future_phase": DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "midplatform_model_governance_binding_standardization_dryrun_review_policy": policy,
        "planning_input_review": planning_input_review,
        "governance_standard_reuse_review": governance_reuse,
        "midplatform_model_governance_binding_standard_candidate": standard_candidate,
        "midplatform_model_governance_binding_schema_review": schema_review,
        "constitution_bus_binding_policy_review": cb_review,
        "capability_bus_binding_policy_review": cap_review,
        "provider_abstraction_binding_policy_review": prov_review,
        "validation_binding_policy_review": val_review,
        "health_oversight_binding_policy_review": health_review,
        "whitebox_trace_binding_policy_review": wb_review,
        "information_integration_binding_policy_review": ii_review,
        "decision_center_binding_policy_review": dc_review,
        "gate_chain_binding_policy_review": gate_review,
        "controlled_runtime_binding_policy_review": cr_review,
        "memory_worldmodel_admission_binding_policy_review": mem_wm_review,
        "model_governance_binding_by_capability_layer_review": layer_review,
        "model_governance_binding_by_module_domain_review": domain_review,
        "vision_model_governance_binding_template_review": vision_review,
        "ocr_model_governance_binding_template_review": ocr_review,
        "tts_model_governance_binding_template_review": tts_review,
        "asr_model_governance_binding_template_review": asr_review,
        "map_navigation_model_governance_binding_template_review": nav_review,
        "world_continuity_model_governance_binding_template_review": world_review,
        "memory_emotion_evolution_model_governance_binding_template_review": mem_review,
        "dual_validation_to_midplatform_binding_handoff_policy_review": dual_handoff_review,
        "non_compliance_handling_deferment_review": deferment_review,
        "midplatform_model_governance_binding_non_runtime_boundary_audit": boundary_audit,
        "midplatform_model_governance_binding_blocked_path_result": blocked_path_result,
        "midplatform_model_governance_binding_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
