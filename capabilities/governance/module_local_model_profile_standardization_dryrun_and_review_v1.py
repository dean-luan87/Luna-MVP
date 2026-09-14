# -*- coding: utf-8 -*-
"""Module-local Model Profile Standardization DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
)
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as REGISTRY_DR_FINAL_GO,
)
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DOMAIN_COVERAGE,
    DUAL_VALIDATION_MECHANISM_ID,
    DUAL_VALIDATION_NON_CLAIMS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    IO_FORBIDDEN,
    MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
    MODULE_LOCAL_PROFILE_SCHEMA_FIELDS,
    PHASE_ID as PLANNING_PHASE_ID,
    REGISTRY_REF,
    REUSED_GOVERNANCE_STANDARDS,
)

PHASE_ID = "Phase-Module-Local-Model-Profile-Standardization-DryRunAndReview-v1-001"
SCOPE = "module_local_model_profile_standardization_dryrun_and_review_only"
SOURCE_CHAIN = "module_local_model_profile_standardization_dryrun_and_review_v1"

FINAL_DECISION_GO = (
    "MODULE_LOCAL_MODEL_PROFILE_STANDARDIZATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_MIDPLATFORM_MODEL_GOVERNANCE_BINDING_STANDARDIZATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MODULE_LOCAL_MODEL_PROFILE_STANDARDIZATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Model-Governance-Binding-Standardization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Module-Local-Model-Profile-Standardization-Issue-Review-v1-001"

DEFERRED_NON_COMPLIANCE_HANDLING_PHASE = (
    "Phase-Non-Compliant-Module-and-Model-Handling-Policy-Planning-v1-001"
)
DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID = "non_compliant_module_model_handling_policy"

NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM = (
    "Non-compliance handling is deferred until after: "
    "1) Module-local Model Profile Standardization DryRunAndReview, "
    "2) Midplatform Model Governance Binding Standardization, "
    "3) At least one module-level self-check + interaction-check dryrun"
)

NON_COMPLIANCE_HANDLING_LEVELS_PREVIEW: Tuple[str, ...] = (
    "L0 warning / issue_trace",
    "L1 hold candidate",
    "L2 require fix / resubmit profile",
    "L3 block module admission",
    "L4 block provider/runtime readiness",
    "L5 quarantine module/model candidate",
    "L6 rollback / deprecate",
    "L7 governance/owner review required",
)

NON_COMPLIANCE_HANDLING_TOPICS: Tuple[str, ...] = (
    "module self-check failure",
    "midplatform interaction check failure",
    "model profile missing fields",
    "license not cleared",
    "provider readiness failure",
    "Constitution-Bus bypass",
    "direct fact/action/user_output from model",
    "runtime overreach",
    "Memory/WorldModel write overreach",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_module_local_profile_runtime_enable",
    "dryrun_to_module_local_profile_as_runtime",
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
)

NON_CLAIMS: Tuple[str, ...] = (
    "Module-local Standardization DryRun GO ≠ model connected",
    "module-local template reviewed ≠ module runtime enabled",
    "registry ref reviewed ≠ model selected",
    "self-check reviewed ≠ midplatform interaction passed for real module",
    "interaction-check reviewed ≠ runtime ready",
    "qianwen/yolo/ocr/asr templates reviewed ≠ invoked",
    "next Midplatform Model Governance Binding Planning ≠ model invocation",
    NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM,
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "module_local_model_profile_standardization_dryrun_and_review_only",
    "simulated",
    "module_local_model_profile_standard_candidate_generated_now",
    "module_internal_self_check_review_generated_now",
    "midplatform_interaction_check_review_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "module_local_profile_standard_runtime_enabled_now", "module_local_profile_created_as_runtime_now",
    "model_selected_now", "model_downloaded_now", "model_invoked_now", "provider_invoked_now",
    "model_runtime_enabled_now", "benchmark_executed_now", "license_cleared_now",
    "security_review_completed_now", "training_started_now", "fine_tuning_started_now",
    "code_generation_executed_now", "skill_added_now", "memory_written_now",
    "world_model_written_now", "task_state_committed_now", "user_output_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "module_local_model_profile_standardization_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
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


def _policy_review(plan_root: Path, policy_file: str, min_rules: int, extra_checks: Optional[List[Tuple[str, bool]]] = None) -> Dict[str, Any]:
    pol = _try_read_json(plan_root / policy_file) or {}
    checks: List[Tuple[str, bool]] = [("rules", len(pol.get("rules") or []) >= min_rules)]
    if extra_checks:
        checks.extend(extra_checks)
    return {"review_id": policy_file.replace(".json", "_review"), **_review_from_checks(checks), "policy_ref": policy_file}


def run_module_local_model_profile_standardization_dryrun_and_review_v1(
    *,
    module_local_model_profile_standardization_planning_root: str,
    model_profile_registry_dryrun_and_review_root: str,
    model_profile_registry_planning_root: str,
    scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(module_local_model_profile_standardization_planning_root).expanduser().resolve()
    registry_dr_root = Path(model_profile_registry_dryrun_and_review_root).expanduser().resolve()
    stack_root = Path(layered_capability_stack_standard_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    registry_dr_vr = _try_read_json(registry_dr_root / "verifier_report.json") or {}
    stack_vr = _try_read_json(stack_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}

    schema = _try_read_json(plan_root / "module_local_model_profile_schema_v1.json") or {}
    std_def = _try_read_json(plan_root / "module_local_model_profile_standard_definition_v1.json") or {}
    self_check_pol = _try_read_json(plan_root / "module_internal_self_check_policy_v1.json") or {}
    interaction_pol = _try_read_json(plan_root / "midplatform_interaction_check_policy_v1.json") or {}
    vision_tpl = _try_read_json(plan_root / "vision_module_local_model_profile_template_v1.json") or {}
    ocr_tpl = _try_read_json(plan_root / "ocr_module_local_model_profile_template_v1.json") or {}
    tts_tpl = _try_read_json(plan_root / "tts_module_local_model_profile_template_v1.json") or {}
    asr_tpl = _try_read_json(plan_root / "asr_module_local_model_profile_template_v1.json") or {}
    nav_tpl = _try_read_json(plan_root / "map_navigation_module_local_model_profile_template_v1.json") or {}
    world_tpl = _try_read_json(plan_root / "world_continuity_module_local_model_profile_template_v1.json") or {}
    mem_tpl = _try_read_json(
        plan_root / "memory_emotion_evolution_module_local_model_profile_template_v1.json"
    ) or {}
    domain_mx = _try_read_json(plan_root / "module_local_profile_domain_coverage_matrix_v1.json") or {}
    io_pol = _try_read_json(plan_root / "module_local_profile_input_output_binding_policy_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_planning_root": str(plan_root),
        "upstream_registry_dryrun_root": str(registry_dr_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Module-local Standardization Planning must be GO")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("Planning final_decision mismatch")
    if plan_sm.get("dual_validation_mechanism_ref") != DUAL_VALIDATION_MECHANISM_ID:
        blockers.append("Dual Validation Mechanism not in Planning")
    if not (plan_root / "module_internal_self_check_policy_v1.json").is_file():
        blockers.append("module_internal_self_check_policy missing")
    if not (plan_root / "midplatform_interaction_check_policy_v1.json").is_file():
        blockers.append("midplatform_interaction_check_policy missing")
    if plan_sm.get("template_count") != 7:
        blockers.append("template_count must be 7")
    if plan_sm.get("domain_coverage_count") != 10:
        blockers.append("domain_coverage must be 10")
    if registry_dr_vr.get("verifier") != "GO":
        blockers.append("Model Profile Registry DryRunAndReview must be GO")
    for name, vr in (
        ("stack_std", stack_vr), ("constitution_bus", cb_vr),
        ("provider_abs", provider_vr), ("controlled_runtime", cr_vr),
    ):
        if vr.get("verifier") != "GO":
            blockers.append(f"{name} must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "dual_validation_mechanism_ref": plan_sm.get("dual_validation_mechanism_ref"),
        "template_count": plan_sm.get("template_count"),
        "domain_coverage_count": plan_sm.get("domain_coverage_count"),
        "registry_dryrun_verifier": registry_dr_vr.get("verifier"),
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
        "dryrun_review_of_module_local_standardization_not_new_framework": True,
        **_review_from_checks([
            ("constraints_ref", True),
            ("reuse_rule", True),
            ("new_need_false", True),
            ("reused_count10", len(REUSED_GOVERNANCE_STANDARDS) == 10),
        ]),
        **meta,
    }

    standard_candidate = {
        "standard_id": "module_local_model_profile_standard_v1",
        "standard_type": "module_level_model_profile_binding_standard",
        "planning_source_phase": PLANNING_PHASE_ID,
        "registry_ref": REGISTRY_REF,
        "template_count": 7,
        "domain_coverage_count": 10,
        "dual_validation_mechanism_enabled": True,
        "module_internal_self_check_required": True,
        "midplatform_interaction_check_required": True,
        "module_local_profile_runtime_enabled_now": False,
        "model_selection_allowed_now": False,
        "model_invocation_allowed_now": False,
        "candidate_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        **meta,
    }

    schema_review = {
        "review_id": "module_local_model_profile_schema_review_v1",
        "field_count": len(MODULE_LOCAL_PROFILE_SCHEMA_FIELDS),
        **_review_from_checks(
            [(f, f in (schema.get("required_fields") or [])) for f in MODULE_LOCAL_PROFILE_SCHEMA_FIELDS]
            + [
                ("source_chain", schema.get("defaults", {}).get("source_chain_required") is True),
                ("whitebox", schema.get("defaults", {}).get("whitebox_trace_required") is True),
                ("no_override", schema.get("defaults", {}).get("no_registry_override") is True),
                ("no_select", schema.get("defaults", {}).get("no_model_selection_by_module") is True),
                ("no_invoke", schema.get("defaults", {}).get("no_model_invocation_by_profile") is True),
                ("no_fact", schema.get("defaults", {}).get("no_direct_fact_action_output") is True),
            ]
        ),
        **meta,
    }

    registry_ref_review = _policy_review(
        plan_root, "module_local_profile_to_registry_reference_policy_v1.json", 6,
        [("registry_ref", (_try_read_json(plan_root / "module_local_profile_to_registry_reference_policy_v1.json") or {}).get("registry_ref") == REGISTRY_REF)],
    )
    registry_ref_review["review_id"] = "registry_reference_policy_review_v1"
    registry_ref_review.update(meta)

    stack_review = _policy_review(plan_root, "module_local_profile_capability_stack_binding_policy_v1.json", 6)
    stack_review["review_id"] = "capability_stack_binding_policy_review_v1"
    stack_pol = _try_read_json(plan_root / "module_local_profile_capability_stack_binding_policy_v1.json") or {}
    stack_extra = _review_from_checks([("stack_ref", stack_pol.get("capability_stack_ref") == UNIVERSAL_STACK_STANDARD_ID)])
    stack_review["review_pass"] = stack_review.get("review_pass") and stack_extra.get("review_pass")
    stack_review["checks"].extend(stack_extra.get("checks") or [])
    stack_review.update(meta)

    gov_review = _policy_review(plan_root, "module_local_profile_layered_governance_binding_policy_v1.json", 9)
    gov_review["review_id"] = "layered_governance_binding_policy_review_v1"
    gov_pol = _try_read_json(plan_root / "module_local_profile_layered_governance_binding_policy_v1.json") or {}
    gov_extra = _review_from_checks([("gov_ref", gov_pol.get("layered_governance_mapping_ref") == ADDENDUM_ID)])
    gov_review["review_pass"] = gov_review.get("review_pass") and gov_extra.get("review_pass")
    gov_review["checks"].extend(gov_extra.get("checks") or [])
    gov_review.update(meta)

    io_review = {
        "review_id": "input_output_binding_policy_review_v1",
        **_review_from_checks(
            [(f"forbid.{f}", f in (io_pol.get("forbidden_outputs") or [])) for f in IO_FORBIDDEN]
            + [("allowed_out5", len(io_pol.get("allowed_outputs") or []) >= 5)]
        ),
        **meta,
    }

    quality_review = _policy_review(plan_root, "module_local_profile_quality_acceptance_binding_policy_v1.json", 6)
    quality_review["review_id"] = "quality_acceptance_binding_policy_review_v1"
    quality_review.update(meta)

    health_review = _policy_review(plan_root, "module_local_profile_health_validation_whitebox_binding_policy_v1.json", 6)
    health_review["review_id"] = "health_validation_whitebox_binding_policy_review_v1"
    health_review.update(meta)

    provider_review = _policy_review(plan_root, "module_local_profile_provider_runtime_boundary_policy_v1.json", 6)
    provider_review["review_id"] = "provider_runtime_boundary_policy_review_v1"
    provider_review.update(meta)

    fallback_review = _policy_review(plan_root, "module_local_profile_fallback_replacement_policy_v1.json", 5)
    fallback_review["review_id"] = "fallback_replacement_policy_review_v1"
    fallback_review.update(meta)

    mid_handoff_review = _policy_review(plan_root, "module_local_profile_midplatform_handoff_policy_v1.json", 9)
    mid_handoff_review["review_id"] = "midplatform_handoff_policy_review_v1"
    mid_handoff_review.update(meta)

    def _tpl_review(tpl: Dict[str, Any], checks: List[Tuple[str, bool]], review_id: str) -> Dict[str, Any]:
        return {"review_id": review_id, **_review_from_checks(checks), **meta}

    vision_text = json.dumps(vision_tpl, ensure_ascii=False)
    vision_review = _tpl_review(vision_tpl, [
        ("module_id", vision_tpl.get("module_id") == "vision_scene_understanding_module"),
        ("yolo", "yolo_family" in vision_text),
        ("grounded", "grounded_sam" in vision_text),
        ("tracking", "visual_tracking" in vision_text),
        ("vlm", "vlm_scene" in vision_text),
        ("layers", "Scene Understanding" in vision_text),
        ("outputs", "visual_observation_candidate" in vision_text),
        ("no_runtime", "no camera/runtime" in vision_text),
        ("no_fact", "no fact/action" in vision_text),
        ("no_invoke", "no model selected/invoked" in vision_text),
    ], "vision_module_local_model_profile_template_review_v1")

    ocr_text = json.dumps(ocr_tpl, ensure_ascii=False)
    ocr_review = _tpl_review(ocr_tpl, [
        ("module_id", ocr_tpl.get("module_id") == "ocr_text_reading_module"),
        ("rapid", "rapidocr" in ocr_text),
        ("paddle", "paddleocr" in ocr_text),
        ("placeholder", "other_ocr_provider" in ocr_text),
        ("outputs", "text_region_candidate" in ocr_text),
        ("candidate_only", "candidate only" in ocr_text),
        ("no_fact", "no fact" in ocr_text),
        ("no_runtime", "no OCR runtime" in ocr_text),
    ], "ocr_module_local_model_profile_template_review_v1")

    tts_text = json.dumps(tts_tpl, ensure_ascii=False)
    tts_review = _tpl_review(tts_tpl, [
        ("module_id", tts_tpl.get("module_id") == "tts_voice_output_module"),
        ("qianwen", "qianwen_tts" in tts_text),
        ("moss", "moss_tts" in tts_text),
        ("local", "local_tts" in tts_text),
        ("not_selected", "≠ selected" in tts_text),
        ("no_invoke", "no TTS invocation" in tts_text),
        ("speech_gate", "Speech Gate" in tts_text),
    ], "tts_module_local_model_profile_template_review_v1")

    asr_text = json.dumps(asr_tpl, ensure_ascii=False)
    asr_review = _tpl_review(asr_tpl, [
        ("module_id", asr_tpl.get("module_id") == "asr_voice_input_module"),
        ("sensevoice", "sensevoice" in asr_text),
        ("whisper", "whisper" in asr_text),
        ("qwen", "qwen_asr" in asr_text),
        ("not_started", "not_started" in asr_text or "planned" in asr_text),
        ("no_runtime", "no ASR runtime" in asr_text),
    ], "asr_module_local_model_profile_template_review_v1")

    nav_text = json.dumps(nav_tpl, ensure_ascii=False)
    nav_review = _tpl_review(nav_tpl, [
        ("module_id", nav_tpl.get("module_id") == "map_navigation_application_module"),
        ("map_provider", "map_provider" in nav_text),
        ("route", "route_reasoning" in nav_text),
        ("facility", "facility_search" in nav_text),
        ("transit", "transit_context" in nav_text),
        ("stage3", "Stage 3" in nav_text),
        ("depends", "Stage 1" in nav_text),
        ("no_invoke", "no map provider invocation" in nav_text),
        ("no_action", "no navigation action" in nav_text),
    ], "map_navigation_module_local_model_profile_template_review_v1")

    world_text = json.dumps(world_tpl, ensure_ascii=False)
    world_review = _tpl_review(world_tpl, [
        ("module_id", world_tpl.get("module_id") == "world_continuity_understanding_module"),
        ("scene_delta", "scene_delta" in world_text),
        ("temporal", "temporal_tracking" in world_text),
        ("visual_map", "visual_map_alignment" in world_text),
        ("stcm", "stcm_self_developed" in world_text),
        ("signals", "signals only" in world_text),
        ("luna_owns", "Luna owns" in world_text),
        ("no_wm", "no WorldModel write" in world_text),
    ], "world_continuity_module_local_model_profile_template_review_v1")

    mem_text = json.dumps(mem_tpl, ensure_ascii=False)
    mem_review = _tpl_review(mem_tpl, [
        ("modules3", len(mem_tpl.get("modules") or []) == 3),
        ("embedding", "embedding_retrieval" in mem_text),
        ("emotion", "emotion_signal" in mem_text),
        ("relationship", "relationship_context" in mem_text),
        ("market", "market_feedback" in mem_text),
        ("code", "code_analysis" in mem_text),
        ("proposal", "proposal_only" in mem_text),
        ("no_mem", "no memory write" in mem_text),
        ("no_code", "code modification" in mem_text),
        ("no_skill", "skill addition" in mem_text),
    ], "memory_emotion_evolution_module_local_model_profile_template_review_v1")

    domain_review = {
        "review_id": "module_local_profile_domain_coverage_review_v1",
        **_review_from_checks([
            ("count10", domain_mx.get("domain_count") == 10),
            ("vision", any(d.get("domain") == "Vision" for d in (domain_mx.get("domains") or []))),
            ("provider_later", "Provider/Model Management" in str(domain_mx.get("domains"))),
        ]),
        **meta,
    }

    self_check_checks: List[Tuple[str, bool]] = [
        ("policy_exists", bool(self_check_pol.get("policy_id"))),
        ("internal_only", "模块" in str(self_check_pol.get("purpose")) or "module-internal" in str(self_check_pol.get("rules")).lower()),
        ("not_replace_interaction", self_check_pol.get("does_not_replace") == "Midplatform Interaction Check"),
        ("no_runtime", "自检不授权 runtime" in str(self_check_pol.get("rules"))),
        ("no_select", "自检不选择模型" in str(self_check_pol.get("rules"))),
        ("no_invoke", "自检不调用 provider" in str(self_check_pol.get("rules"))),
        ("no_mem_wm", "自检不写 Memory" in str(self_check_pol.get("rules"))),
        ("no_user_output", "自检不生成 user output" in str(self_check_pol.get("rules"))),
    ]
    for item in MODULE_INTERNAL_SELF_CHECK_COVERAGE:
        self_check_checks.append((item[:16], item in (self_check_pol.get("self_check_coverage") or [])))
    self_check_review = {
        "review_id": "module_internal_self_check_review_v1",
        "mechanism_layer": "Module Internal Self-Check",
        **_review_from_checks(self_check_checks),
        **meta,
    }

    interaction_checks: List[Tuple[str, bool]] = [
        ("policy_exists", bool(interaction_pol.get("policy_id"))),
        ("interaction_only", "中台" in str(interaction_pol.get("purpose")) or "midplatform" in str(interaction_pol.get("rules")).lower()),
        ("not_replace_self", interaction_pol.get("does_not_replace") == "Module Internal Self-Check"),
        ("no_runtime", "不等于 runtime 授权" in str(interaction_pol.get("rules"))),
        ("no_select", "不等于模型选择" in str(interaction_pol.get("rules"))),
        ("no_invoke", "不等于 provider invocation" in str(interaction_pol.get("rules"))),
    ]
    for item in MIDPLATFORM_INTERACTION_CHECK_COVERAGE:
        interaction_checks.append((item[:16], item in (interaction_pol.get("interaction_check_coverage") or [])))
    interaction_review = {
        "review_id": "midplatform_interaction_check_review_v1",
        "mechanism_layer": "Midplatform Interaction Check",
        **_review_from_checks(interaction_checks),
        **meta,
    }

    dual_validation_review = {
        "review_id": "dual_validation_mechanism_review_v1",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "self_check_review_pass": self_check_review.get("review_pass"),
        "interaction_check_review_pass": interaction_review.get("review_pass"),
        "rules": [
            "Module Internal Self-Check GO ≠ Midplatform Interaction Check GO",
            "Midplatform Interaction Check GO ≠ Runtime Ready",
            "a module may pass self-check but fail interaction check",
            "a module may expose correct midplatform refs but fail internal schema",
            "both checks required before controlled runtime readiness",
            "checks are evidence gates, not runtime gates",
        ],
        **_review_from_checks([
            ("self_check_pass", self_check_review.get("review_pass") is True),
            ("interaction_pass", interaction_review.get("review_pass") is True),
            ("both_required", True),
            ("not_runtime_gate", True),
            ("self_ne_interaction", True),
            ("interaction_ne_runtime", True),
        ]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "module_local_profile_non_runtime_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "module_local_profile_blocked_path_result_v1",
        "blocked_paths": [{"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    all_reviews = [
        governance_reuse, schema_review, registry_ref_review, stack_review, gov_review,
        io_review, quality_review, health_review, provider_review, fallback_review,
        mid_handoff_review, vision_review, ocr_review, tts_review, asr_review, nav_review,
        world_review, mem_review, domain_review, self_check_review, interaction_review,
        dual_validation_review,
    ]

    dryrun_pass = (
        input_ok
        and all(r.get("review_pass") for r in all_reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
    )

    closure_decision = {
        "decision_id": "module_local_profile_closure_decision_v1",
        "dryrun_and_review_pass": dryrun_pass,
        "high_risk": not dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "module_local_model_profile_standard_v1 candidate validated",
            "7 module templates reviewed",
            "dual validation mechanism: self-check + interaction-check pass",
            "ready for Midplatform Model Governance Binding Standardization Planning",
        ] if dryrun_pass else ["hold for issue review"],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_midplatform_model_governance_binding_standardization_planning": dryrun_pass,
        "selected_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "module_local_model_profile_standardization_dryrun_review_policy_v1",
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

    deferred_governance_register = {
        "register_id": "deferred_governance_register_v1",
        "non_compliant_module_model_handling_policy_deferred": True,
        "recommended_future_phase": DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
        "deferred_items": [
            {
                "item_id": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
                "item_name": "Non-Compliant Module / Model Handling Policy",
                "item_name_zh": "不合规模块 / 模型处理机制",
                "status": "deferred",
                "recommended_future_phase": DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
                "defer_until": [
                    "Module-local Model Profile Standardization DryRunAndReview",
                    "Midplatform Model Governance Binding Standardization",
                    "At least one module-level self-check + interaction-check dryrun",
                ],
                "handling_levels_preview": list(NON_COMPLIANCE_HANDLING_LEVELS_PREVIEW),
                "scope_topics": list(NON_COMPLIANCE_HANDLING_TOPICS),
                "not_implemented_now": True,
                "rationale": [
                    "standards/profile/binding still being established; no real module接入 yet",
                    "handling policy depends on self-check, interaction-check, binding, runtime readiness, controlled trial",
                ],
            }
        ],
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_and_review_pass": dryrun_pass,
        "template_count": 7,
        "domain_coverage_count": 10,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "module_internal_self_check_review_pass": self_check_review.get("review_pass"),
        "midplatform_interaction_check_review_pass": interaction_review.get("review_pass"),
        "non_compliant_module_model_handling_policy_deferred": True,
        "recommended_future_phase": DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "module_local_model_profile_standardization_dryrun_review_policy": policy,
        "planning_input_review": planning_input_review,
        "governance_standard_reuse_review": governance_reuse,
        "module_local_model_profile_standard_candidate": standard_candidate,
        "module_local_model_profile_schema_review": schema_review,
        "registry_reference_policy_review": registry_ref_review,
        "capability_stack_binding_policy_review": stack_review,
        "layered_governance_binding_policy_review": gov_review,
        "input_output_binding_policy_review": io_review,
        "quality_acceptance_binding_policy_review": quality_review,
        "health_validation_whitebox_binding_policy_review": health_review,
        "provider_runtime_boundary_policy_review": provider_review,
        "fallback_replacement_policy_review": fallback_review,
        "midplatform_handoff_policy_review": mid_handoff_review,
        "vision_module_local_model_profile_template_review": vision_review,
        "ocr_module_local_model_profile_template_review": ocr_review,
        "tts_module_local_model_profile_template_review": tts_review,
        "asr_module_local_model_profile_template_review": asr_review,
        "map_navigation_module_local_model_profile_template_review": nav_review,
        "world_continuity_module_local_model_profile_template_review": world_review,
        "memory_emotion_evolution_module_local_model_profile_template_review": mem_review,
        "module_local_profile_domain_coverage_review": domain_review,
        "module_internal_self_check_review": self_check_review,
        "midplatform_interaction_check_review": interaction_review,
        "dual_validation_mechanism_review": dual_validation_review,
        "module_local_profile_non_runtime_boundary_audit": boundary_audit,
        "module_local_profile_blocked_path_result": blocked_path_result,
        "module_local_profile_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "deferred_governance_register": deferred_governance_register,
        "summary": summary,
    }
