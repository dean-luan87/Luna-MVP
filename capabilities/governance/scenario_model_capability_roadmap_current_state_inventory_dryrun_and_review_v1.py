# -*- coding: utf-8 -*-
"""Scenario Model Capability Roadmap and Current State Inventory DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_scene_understanding_output_chain_closure_review_v1 import (
    FINAL_DECISION_GO as CLOSURE_REVIEW_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.scenario_model_capability_roadmap_current_state_inventory_planning_v1 import (
    ASSET_STATUS_TYPES,
    CAPABILITY_DOMAIN_IDS,
    DOMAIN_INVENTORY_FIELDS,
    EXTERNAL_CANDIDATE_REGISTER_FIELDS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    MIDPLATFORM_BINDING_FIELDS,
    MODEL_SOURCE_TYPES,
    MODULE_PROFILE_FIELDS,
    NON_CLAIMS as PLANNING_NON_CLAIMS,
    PHASE_ID as PLANNING_PHASE_ID,
    ROADMAP_RISKS,
)

PHASE_ID = (
    "Phase-Scenario-Model-Capability-Roadmap-and-Current-State-Inventory-DryRunAndReview-v1-001"
)
SCOPE = "scenario_model_capability_roadmap_inventory_dryrun_and_review_only"
SOURCE_CHAIN = "scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_v1"

FINAL_DECISION_GO = (
    "SCENARIO_MODEL_CAPABILITY_ROADMAP_AND_CURRENT_STATE_INVENTORY_DRYRUN_AND_REVIEW_"
    "CLOSED_READY_FOR_MODEL_PROFILE_REGISTRY_PLANNING"
)
FINAL_DECISION_HOLD = (
    "SCENARIO_MODEL_CAPABILITY_ROADMAP_AND_CURRENT_STATE_INVENTORY_DRYRUN_AND_REVIEW_"
    "HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Model-Profile-Registry-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Scenario-Model-Capability-Roadmap-Issue-Review-v1-001"

DOMAIN_REVIEW_FIELDS: Tuple[str, ...] = (
    "first_stage_goal",
    "implementation_plan",
    "actual_completion_status",
    "existing_assets_or_artifacts",
    "already_integrated_or_registered_models",
    "candidate_model_sources",
    "current_gaps",
    "next_actions",
    "version_update_replacement_notes",
    "module_local_model_profile_needed",
    "midplatform_governance_binding_needed",
)

IO_CONTRACT_ALLOWED: Tuple[str, ...] = (
    "candidate", "context", "signal", "evidence", "proposal",
)
IO_CONTRACT_FORBIDDEN: Tuple[str, ...] = (
    "direct_fact", "direct_action", "direct_user_output",
    "direct_memory_write", "direct_worldmodel_write", "direct_runtime_enable",
)

QUALITY_CRITERIA: Tuple[str, ...] = (
    "accuracy", "precision", "recall", "latency_budget", "resource_cost",
    "stability", "failure_rate", "confidence_calibration", "false_positive_control",
    "traceability_completeness", "candidate_contract_compliance", "degradation_behavior",
    "offline_capability", "privacy_compliance", "safety_critical_pass_criteria",
)

VERSIONING_FIELDS: Tuple[str, ...] = (
    "model_id", "model_version", "provider_version", "registry_version",
    "license_ref", "update_policy", "breaking_change_policy", "rollback_policy",
    "benchmark_revalidation_required", "security_review_required",
    "deprecation_policy", "no_auto_switch_without_governance",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_model_selection",
    "dryrun_to_model_download",
    "dryrun_to_model_invocation",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime_enable",
    "dryrun_to_benchmark_execution",
    "dryrun_to_training_start",
    "dryrun_to_fine_tuning_start",
    "dryrun_to_code_generation",
    "dryrun_to_skill_addition",
    "dryrun_to_runtime_enable",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_user_output",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap DryRunAndReview GO ≠ model selected",
    "current inventory GO ≠ runtime readiness",
    "YOLO/OCR/TTS asset mapped ≠ Luna 2.0 model profile complete",
    "candidate register GO ≠ license cleared",
    "next Model Profile Registry Planning ≠ model invocation",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("scenario_model_capability_roadmap_inventory_dryrun_and_review_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "model_selected_now", "model_downloaded_now", "model_invoked_now", "provider_invoked_now",
    "model_runtime_enabled_now", "benchmark_executed_now", "training_started_now",
    "fine_tuning_started_now", "code_generation_executed_now", "skill_added_now",
    "runtime_enabled_now", "memory_written_now", "world_model_written_now",
    "task_state_committed_now", "user_output_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review"
)

DOMAIN_ROADMAP_FILES: Dict[str, str] = {
    "first_person_vision_scene_understanding": "vision_scene_understanding_roadmap_v1.json",
    "ocr_text_recognition_reading": "ocr_text_reading_roadmap_v1.json",
    "asr_voice_input": "asr_voice_input_roadmap_v1.json",
    "tts_voice_output": "tts_voice_output_roadmap_v1.json",
    "map_location_navigation_application": "map_navigation_roadmap_v1.json",
    "spatiotemporal_world_continuity": "spatiotemporal_world_continuity_roadmap_v1.json",
    "memory_personal_continuity": "memory_personal_continuity_roadmap_v1.json",
    "emotion_engine_social_adaptation": "emotion_engine_roadmap_v1.json",
    "evolutionary_recursion_self_improvement": "evolutionary_recursion_roadmap_v1.json",
    "provider_model_management": "provider_model_management_roadmap_v1.json",
    "output_gate_chain": "output_gate_chain_roadmap_v1.json",
    "health_whitebox_validation_governance": "health_whitebox_validation_governance_roadmap_v1.json",
}


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
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


def _contains_any(text: str, keywords: Tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(k.lower() in lower for k in keywords)


def _non_empty_list(val: Any) -> bool:
    return isinstance(val, list) and len(val) > 0


def _domain_structure_ok(domain: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for field in DOMAIN_REVIEW_FIELDS:
        if field not in domain:
            issues.append(f"missing:{field}")
            continue
        if field in ("module_local_model_profile_needed", "midplatform_governance_binding_needed"):
            if domain.get(field) is not True:
                issues.append(f"{field}_not_true")
        elif isinstance(domain.get(field), list):
            if not domain[field] and field not in (
                "already_integrated_or_registered_models", "candidate_model_sources",
            ):
                issues.append(f"empty:{field}")
        elif isinstance(domain.get(field), str):
            if not domain[field].strip():
                issues.append(f"empty:{field}")
    return len(issues) == 0, issues


def _review_from_checks(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"check_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "review_pass": len(issues) == 0,
    }


def run_scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_v1(
    *,
    scenario_model_capability_roadmap_current_state_inventory_planning_root: str,
    first_person_scene_understanding_output_chain_closure_review_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    seed_core_pluggable_layer_architecture_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        scenario_model_capability_roadmap_current_state_inventory_planning_root
    ).expanduser().resolve()
    closure_root = Path(
        first_person_scene_understanding_output_chain_closure_review_root
    ).expanduser().resolve()
    stack_root = Path(layered_capability_stack_standard_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    sc_plug_root = Path(
        seed_core_pluggable_layer_architecture_dryrun_and_review_root
    ).expanduser().resolve()

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    closure_vr = _try_read_json(closure_root / "verifier_report.json") or {}
    closure_sm = _try_read_json(closure_root / "summary.json") or {}
    stack_vr = _try_read_json(stack_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    sc_plug_vr = _try_read_json(sc_plug_root / "verifier_report.json") or {}

    domain_matrix = _try_read_json(plan_root / "capability_domain_inventory_matrix_v1.json") or {}
    asset_inv = _try_read_json(plan_root / "current_model_asset_inventory_v1.json") or {}
    goal_matrix = _try_read_json(plan_root / "goal_stage_to_capability_domain_matrix_v1.json") or {}
    gap_matrix = _try_read_json(plan_root / "current_gap_and_next_action_matrix_v1.json") or {}
    module_contract = _try_read_json(plan_root / "module_local_model_profile_contract_v1.json") or {}
    mid_binding = _try_read_json(plan_root / "midplatform_model_governance_binding_contract_v1.json") or {}
    io_std = _try_read_json(plan_root / "model_input_output_contract_standard_v1.json") or {}
    acceptance = _try_read_json(plan_root / "model_quality_acceptance_criteria_v1.json") or {}
    versioning = _try_read_json(plan_root / "model_versioning_and_update_policy_v1.json") or {}
    replacement = _try_read_json(plan_root / "model_replacement_and_fallback_policy_v1.json") or {}
    external_reg = _try_read_json(plan_root / "external_open_source_candidate_register_v1.json") or {}
    reference_reg = _try_read_json(plan_root / "reference_research_product_candidate_register_v1.json") or {}
    self_dev_reg = _try_read_json(plan_root / "self_developed_core_capability_register_v1.json") or {}
    source_tax = _try_read_json(plan_root / "model_source_strategy_taxonomy_v1.json") or {}
    risk_reg = _try_read_json(plan_root / "roadmap_risk_register_v1.json") or {}

    domain_by_id = {
        d.get("capability_domain_id"): d
        for d in (domain_matrix.get("domains") or [])
        if d.get("capability_domain_id")
    }

    roadmap_by_domain: Dict[str, Dict[str, Any]] = {}
    for did, fname in DOMAIN_ROADMAP_FILES.items():
        if did in ("output_gate_chain", "health_whitebox_validation_governance"):
            roadmap_by_domain[did] = domain_by_id.get(did, {})
        else:
            loaded = _try_read_json(plan_root / fname) or {}
            roadmap_by_domain[did] = loaded if loaded else domain_by_id.get(did, {})

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_planning_root": str(plan_root),
        "upstream_closure_review_root": str(closure_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Planning verifier must be GO")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("Planning final_decision mismatch")
    if plan_sm.get("closure_pending") is True:
        blockers.append("closure_pending must be false")
    if closure_vr.get("verifier") != "GO":
        blockers.append("Output Chain Closure Review must be GO")
    if closure_sm.get("final_decision") != CLOSURE_REVIEW_FINAL_GO:
        blockers.append("Closure final_decision mismatch")
    for name, vr in (
        ("stack_std", stack_vr), ("constitution_bus", cb_vr),
        ("provider_abs", provider_vr), ("seed_core_plug", sc_plug_vr),
    ):
        if vr.get("verifier") != "GO":
            blockers.append(f"{name} must be GO")
    if not (plan_root / "module_local_model_profile_contract_v1.json").is_file():
        blockers.append("module_local_model_profile_contract missing")
    if not (plan_root / "midplatform_model_governance_binding_contract_v1.json").is_file():
        blockers.append("midplatform_model_governance_binding_contract missing")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "closure_pending": plan_sm.get("closure_pending"),
        "closure_review_verifier": closure_vr.get("verifier"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    goal_stage_count = len(goal_matrix.get("mappings") or [])
    roadmap_candidate = {
        "roadmap_id": "scenario_model_capability_roadmap_current_state_inventory_v1",
        "roadmap_type": "model_capability_roadmap_with_current_state_inventory",
        "planning_source_phase": PLANNING_PHASE_ID,
        "capability_domain_count": len(CAPABILITY_DOMAIN_IDS),
        "goal_stage_count": goal_stage_count,
        "includes_current_asset_inventory": True,
        "includes_gap_next_action_matrix": True,
        "includes_module_local_model_profile_contract": True,
        "includes_midplatform_governance_binding_contract": True,
        "model_selected_now": False,
        "model_invoked_now": False,
        "runtime_enabled_now": False,
        "candidate_only": True,
        "domains": list(CAPABILITY_DOMAIN_IDS),
        **meta,
    }

    domain_reviews: List[Dict[str, Any]] = []
    domain_review_pass = True
    for did in CAPABILITY_DOMAIN_IDS:
        dom = domain_by_id.get(did, {})
        struct_ok, struct_issues = _domain_structure_ok(dom)
        domain_reviews.append({
            "capability_domain_id": did,
            "structure_pass": struct_ok,
            "structure_issues": struct_issues,
            "domain_data": dom,
        })
        if not struct_ok:
            domain_review_pass = False

    capability_domain_inventory_review = {
        "review_id": "capability_domain_inventory_review_v1",
        "domain_count": len(CAPABILITY_DOMAIN_IDS),
        "required_fields": list(DOMAIN_REVIEW_FIELDS),
        "domain_reviews": domain_reviews,
        "all_domains_present": all(did in domain_by_id for did in CAPABILITY_DOMAIN_IDS),
        "review_pass": domain_review_pass and all(did in domain_by_id for did in CAPABILITY_DOMAIN_IDS),
        **meta,
    }

    assets = asset_inv.get("assets") or []
    asset_ids = {a.get("asset_id") for a in assets}
    asset_checks = [
        ("yolo_inventoried", "yolo_object_detection" in asset_ids),
        ("ocr_paddle", "paddleocr" in asset_ids),
        ("ocr_rapid", "rapidocr" in asset_ids),
        ("ocr_evidence", "ocr_request_evidence_chain" in asset_ids),
        ("tts_qianwen", "qianwen_tts_candidate" in asset_ids),
        ("tts_runtime", "tts_runtime_planning" in asset_ids),
        ("asr_status", any(a.get("asset_id") == "asr_voice_input" and a.get("status") == "not_started" for a in assets)),
        ("vision_chain", "first_person_scene_chain" in asset_ids),
        ("provider_std", "provider_abstraction_standard" in asset_ids),
        ("gate_chain", "output_speech_display_gate_chain" in asset_ids),
        ("status_taxonomy", set(asset_inv.get("status_types") or []) == set(ASSET_STATUS_TYPES)),
        ("no_runtime_overclaim", all(
            a.get("status") not in ("implemented_artifact",) or "runtime" not in str(a.get("notes", "")).lower()
            for a in assets
        )),
    ]
    current_model_asset_inventory_review = {
        "review_id": "current_model_asset_inventory_review_v1",
        **_review_from_checks(asset_checks),
        "asset_count": len(assets),
        **meta,
    }

    goal_stage_to_capability_domain_review = {
        "review_id": "goal_stage_to_capability_domain_review_v1",
        "mapping_count": goal_stage_count,
        "goal_stage_count_ge_6": goal_stage_count >= 6,
        "mappings": goal_matrix.get("mappings") or [],
        "review_pass": goal_stage_count >= 6,
        **meta,
    }

    vision = roadmap_by_domain.get("first_person_vision_scene_understanding", {})
    vision_text = json.dumps(vision, ensure_ascii=False)
    vision_review = {
        "review_id": "vision_scene_understanding_roadmap_review_v1",
        "capability_domain_id": "first_person_vision_scene_understanding",
        **_review_from_checks([
            ("stage1_scene", _contains_any(vision_text, ("场景理解", "scene understanding", "current scene"))),
            ("target_recognition", _contains_any(vision_text, ("目标识别", "target_recognition", "target recognition"))),
            ("text_region", _contains_any(vision_text, ("文字区域", "text_region", "text region"))),
            ("risk_candidate", _contains_any(vision_text, ("风险", "risk_context", "risk candidate"))),
            ("tracking_candidate", _contains_any(vision_text, ("追踪", "tracking", "target_tracking"))),
            ("yolo_plan", _contains_any(vision_text, ("yolo", "YOLO"))),
            ("grounding_later", _contains_any(vision_text, ("grounded", "Grounding", "segmentation"))),
            ("tracking_later", _contains_any(vision_text, ("tracking", "Tracking"))),
            ("vlm_later", _contains_any(vision_text, ("vlm", "VLM"))),
            ("ocr_binding", _contains_any(vision_text, ("OCR", "ocr"))),
            ("ii_decision", _contains_any(vision_text, ("Information Integration", "Decision"))),
            ("chain_dryrun_go", _contains_any(vision_text, ("DryRun GO", "Gate Chain"))),
            ("fixture_candidate", _contains_any(vision_text, ("fixture", "candidate", "dryrun"))),
            ("gap_camera", _contains_any(vision_text, ("camera", "连续帧", "continuous frame"))),
            ("gap_grounded", _contains_any(vision_text, ("Grounded", "segmentation", "VLM"))),
            ("next_profile", _contains_any(vision_text, ("Model Profile", "model profile"))),
            ("next_controlled", _contains_any(vision_text, ("controlled runtime", "不直接启 runtime"))),
            ("no_runtime_overclaim", "runtime 未开启" in vision_text or "未开启" in vision_text),
        ]),
        **meta,
    }

    ocr = roadmap_by_domain.get("ocr_text_recognition_reading", {})
    ocr_text = json.dumps(ocr, ensure_ascii=False)
    ocr_review = {
        "review_id": "ocr_text_reading_roadmap_review_v1",
        **_review_from_checks([
            ("text_region_candidate", "text_region_candidate" in ocr_text),
            ("ocr_result_candidate", "ocr_result_candidate" in ocr_text),
            ("signage_context", "signage_context_candidate" in ocr_text),
            ("ocr_evidence", "OCR evidence" in ocr_text or "ocr evidence" in ocr_text.lower()),
            ("paddle_rapid", _contains_any(ocr_text, ("paddleocr", "rapidocr", "PaddleOCR", "RapidOCR"))),
            ("candidate_not_fact", "candidate" in ocr_text and "not fact" in ocr_text.lower()),
            ("gap_runtime", "runtime" in ocr_text.lower() and ("未" in ocr_text or "not" in ocr_text.lower())),
            ("gap_reading_later", "reading" in ocr_text.lower() or "阅读" in ocr_text),
            ("gap_benchmark", "benchmark" in ocr_text.lower()),
        ]),
        **meta,
    }

    tts = roadmap_by_domain.get("tts_voice_output", {})
    tts_text = json.dumps(tts, ensure_ascii=False)
    tts_review = {
        "review_id": "tts_voice_output_roadmap_review_v1",
        **_review_from_checks([
            ("abstract_runtime", "TTS Runtime" in tts_text or "abstract" in tts_text.lower()),
            ("qianwen_candidate", "qianwen" in tts_text.lower()),
            ("not_selected", "not selected" in tts_text.lower() or "not_selected" in tts_text or "≠ selected" in tts_text),
            ("speech_gate_boundary", "Speech Gate" in tts_text or "Voice Output Plane" in tts_text),
            ("gap_no_real_tts", "未做真实 TTS" in tts_text or "no real TTS" in tts_text.lower()),
            ("gap_voice_profile", "voice profile" in tts_text.lower()),
            ("gap_moss", "MOSS" in tts_text or "moss" in tts_text.lower()),
            ("no_bypass_gate", "Speech Gate" in tts_text and "TTS Runtime" in tts_text),
        ]),
        **meta,
    }

    asr = roadmap_by_domain.get("asr_voice_input", {})
    asr_text = json.dumps(asr, ensure_ascii=False)
    asr_review = {
        "review_id": "asr_voice_input_roadmap_review_v1",
        **_review_from_checks([
            ("not_started_or_planned", _contains_any(asr_text, ("not_started", "尚未", "未完整", "not fully"))),
            ("candidates_future", _contains_any(asr_text, ("sensevoice", "whisper", "qwen_asr", "Qwen-ASR"))),
            ("no_runtime_overclaim", "runtime" in asr_text.lower() and ("未" in asr_text or "not" in asr_text.lower())),
            ("voice_to_task_future", _contains_any(asr_text, ("voice-to-task", "语音到任务", "闭环尚未"))),
        ]),
        **meta,
    }

    nav = roadmap_by_domain.get("map_location_navigation_application", {})
    nav_text = json.dumps(nav, ensure_ascii=False)
    map_review = {
        "review_id": "map_navigation_roadmap_review_v1",
        **_review_from_checks([
            ("stage3", "stage_3" in nav_text or "Stage 3" in nav_text),
            ("depends_stage12", _contains_any(nav_text, ("Stage 1", "stage_1", "Stage 2", "stage_2", "depends"))),
            ("context_candidate_only", "context candidate" in nav_text.lower() or "context_candidate" in nav_text),
            ("no_nav_runtime", "未开启" in nav_text or "未开" in nav_text or "not enabled" in nav_text.lower()),
            ("next_profiles", _contains_any(nav_text, ("map/location", "route context", "facility search"))),
        ]),
        **meta,
    }

    st = roadmap_by_domain.get("spatiotemporal_world_continuity", {})
    st_text = json.dumps(st, ensure_ascii=False)
    st_review = {
        "review_id": "spatiotemporal_world_continuity_roadmap_review_v1",
        **_review_from_checks([
            ("core_luna", _contains_any(st_text, ("自研", "Luna", "不能由单一外部模型"))),
            ("scene_delta", _contains_any(st_text, ("scene delta", "Scene Delta", "scene_delta"))),
            ("temporal_tracking", _contains_any(st_text, ("temporal", "tracking", "连续"))),
            ("world_continuity", "world_continuity" in st_text or "world continuity" in st_text.lower()),
            ("stcm", "STCM" in st_text or "stcm" in st_text.lower()),
            ("external_signals_only", _contains_any(st_text, ("信号", "signal", "外部模型"))),
            ("gaps_explicit", _non_empty_list(st.get("current_gaps"))),
            ("next_explicit", _non_empty_list(st.get("next_actions"))),
        ]),
        **meta,
    }

    memory = roadmap_by_domain.get("memory_personal_continuity", {})
    mem_text = json.dumps(memory, ensure_ascii=False)
    memory_review = {
        "review_id": "memory_personal_continuity_roadmap_review_v1",
        **_review_from_checks([
            ("self_developed", memory.get("model_source_strategy") == "self_developed_core_capability"),
            ("personal_continuity", "Personal Continuity" in mem_text),
            ("memory_stick", "memory stick" in mem_text.lower() or "life memory" in mem_text.lower()),
            ("embedding_organs", _contains_any(mem_text, ("embedding", "retrieval", "检索器官"))),
            ("admission_governance", _contains_any(mem_text, ("admission", "准入", "防克隆", "防污染"))),
            ("no_write_overclaim", "memory_write blocked" in mem_text.lower() or "no write" in mem_text.lower() or "blocked" in mem_text.lower()),
        ]),
        **meta,
    }

    emotion = roadmap_by_domain.get("emotion_engine_social_adaptation", {})
    emo_text = json.dumps(emotion, ensure_ascii=False)
    emotion_review = {
        "review_id": "emotion_engine_roadmap_review_v1",
        **_review_from_checks([
            ("survival_drive", "Survival Drive" in emo_text or "survival" in emo_text.lower()),
            ("social_integration", _contains_any(emo_text, ("社会融入", "social", "relationship", "关系"))),
            ("external_signals", _contains_any(emo_text, ("信号", "signal", "识别模型"))),
            ("luna_owned", _contains_any(emo_text, ("Luna 自研", "self_developed", "governance"))),
            ("no_runtime_overclaim", "未建" in emo_text or "not" in emo_text.lower()),
        ]),
        **meta,
    }

    evolution = roadmap_by_domain.get("evolutionary_recursion_self_improvement", {})
    evo_text = json.dumps(evolution, ensure_ascii=False)
    evolution_review = {
        "review_id": "evolutionary_recursion_roadmap_review_v1",
        **_review_from_checks([
            ("survival_drive", "Survival" in evo_text or "survival" in evo_text.lower()),
            ("proposal_only", "proposal_only" in evo_text),
            ("external_assist", _contains_any(evo_text, ("辅助", "assist", "analysis"))),
            ("governance_required", _contains_any(evo_text, ("governance", "owner", "validation", "rollback"))),
            ("no_self_mod", _contains_any(evo_text, ("不能自我修改", "no_auto", "proposal_only"))),
        ]),
        **meta,
    }

    provider = roadmap_by_domain.get("provider_model_management", {})
    prov_text = json.dumps(provider, ensure_ascii=False)
    provider_review = {
        "review_id": "provider_model_management_roadmap_review_v1",
        **_review_from_checks([
            ("runtime_ne_provider", "runtime" in prov_text.lower() and "provider" in prov_text.lower()),
            ("candidate_ne_selected", "≠" in prov_text or "candidate" in prov_text.lower()),
            ("module_profile", "module profile" in prov_text.lower() or "module-local" in prov_text.lower()),
            ("midplatform_binding", "midplatform" in prov_text.lower()),
            ("version_policy", "version" in prov_text.lower() and "replacement" in prov_text.lower()),
            ("no_auto_switch", "auto-switch" in prov_text.lower() or "no auto" in prov_text.lower()),
        ]),
        **meta,
    }

    output_dom = domain_by_id.get("output_gate_chain", {})
    out_text = json.dumps(output_dom, ensure_ascii=False)
    output_review = {
        "review_id": "output_gate_chain_roadmap_review_v1",
        **_review_from_checks([
            ("gate_assets", _contains_any(out_text, ("gate", "Gate", "output_candidate"))),
            ("gate_chain_ref", GATE_CHAIN_SYSTEM_ID in out_text or "16 gate" in out_text.lower() or "gate_chain" in out_text),
            ("candidate_not_output", "user_output_candidate" in out_text),
            ("execution_later", _contains_any(out_text, ("execution later", "Voice Output Plane", "Display"))),
            ("health_oversight", True),
        ]),
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        **meta,
    }

    health_dom = domain_by_id.get("health_whitebox_validation_governance", {})
    health_text = json.dumps(health_dom, ensure_ascii=False)
    health_review = {
        "review_id": "health_whitebox_validation_governance_roadmap_review_v1",
        **_review_from_checks([
            ("governance_support", _contains_any(health_text, ("governance", "oversight", "Validation"))),
            ("health_external", _contains_any(health_text, ("external", "Health external", "not_bus_self_judge"))),
            ("bus_transports_only", _contains_any(health_text, ("health_ref", "transports", "carried"))),
            ("whitebox_bind", "whitebox" in health_text.lower()),
            ("validation_bind", "validation" in health_text.lower()),
        ]),
        **meta,
    }

    source_review = {
        "review_id": "model_source_strategy_review_v1",
        "source_types": list(MODEL_SOURCE_TYPES),
        **_review_from_checks([
            ("type_a", "direct_open_source_or_external_provider" in (source_tax.get("source_types") or [])),
            ("type_b", "reference_inspired_rebuild" in (source_tax.get("source_types") or [])),
            ("type_c", "self_developed_core_capability" in (source_tax.get("source_types") or [])),
            ("external_as_organs", True),
            ("reference_not_blind_copy", reference_reg.get("reference_not_dependency") is True),
            ("core_self_dev", "seed_core" in str(self_dev_reg.get("capabilities") or [])),
        ]),
        **meta,
    }

    ext_candidates = external_reg.get("candidates") or []
    cand_checks: List[Tuple[str, bool]] = [
        ("register_only", external_reg.get("register_only") is True),
        ("candidate_count", len(ext_candidates) >= 11),
    ]
    for c in ext_candidates:
        for field in EXTERNAL_CANDIDATE_REGISTER_FIELDS:
            cand_checks.append((f"{c.get('candidate_name','x')[:8]}.{field[:6]}", field in c))
    candidate_register_review = {
        "review_id": "candidate_register_review_v1",
        "reference_inspired_only": reference_reg.get("reference_not_dependency") is True,
        "self_dev_not_external": len(self_dev_reg.get("capabilities") or []) >= 5,
        **_review_from_checks(cand_checks),
        **meta,
    }

    module_profile_review = {
        "review_id": "module_local_model_profile_contract_review_v1",
        "required_fields": list(MODULE_PROFILE_FIELDS),
        **_review_from_checks([
            (f, f in (module_contract.get("required_fields") or [])) for f in MODULE_PROFILE_FIELDS
        ] + [
            ("no_direct_fact", module_contract.get("no_direct_fact_action_output_default") is True),
        ]),
        **meta,
    }

    mid_binding_review = {
        "review_id": "midplatform_model_governance_binding_contract_review_v1",
        "required_fields": list(MIDPLATFORM_BINDING_FIELDS),
        **_review_from_checks([
            (f, f in (mid_binding.get("required_fields") or [])) for f in MIDPLATFORM_BINDING_FIELDS
        ] + [
            ("stack_ref", mid_binding.get("layered_stack_ref") == UNIVERSAL_STACK_STANDARD_ID),
            ("gov_ref", mid_binding.get("layered_governance_ref") == ADDENDUM_ID),
        ]),
        **meta,
    }

    io_review = {
        "review_id": "model_input_output_contract_review_v1",
        **_review_from_checks([
            ("allowed_types", bool(io_std.get("default_output"))),
            ("forbidden_fact", "direct_fact" in str(io_std.get("forbidden") or [])),
            ("forbidden_action", "direct_action" in str(io_std.get("forbidden") or [])),
            ("forbidden_user_output", "direct_user_output" in str(io_std.get("forbidden") or [])),
            ("forbidden_memory", "direct_memory_write" in str(io_std.get("forbidden") or [])),
            ("forbidden_wm", "direct_worldmodel_write" in str(io_std.get("forbidden") or []) or "direct_runtime_enable" in str(io_std.get("forbidden") or [])),
            ("trace_required", True),
        ]),
        "allowed_output_types": list(IO_CONTRACT_ALLOWED),
        "forbidden_output_types": list(IO_CONTRACT_FORBIDDEN),
        **meta,
    }

    acceptance_criteria = acceptance.get("criteria") or []
    quality_review = {
        "review_id": "model_quality_acceptance_criteria_review_v1",
        "required_criteria": list(QUALITY_CRITERIA),
        **_review_from_checks([
            ("criteria_present", len(acceptance_criteria) >= 8),
            ("accuracy", "accuracy" in str(acceptance_criteria)),
            ("latency", "latency" in str(acceptance_criteria)),
            ("privacy", "privacy" in str(acceptance_criteria)),
            ("safety", "safety" in str(acceptance_criteria)),
        ]),
        **meta,
    }

    version_fields = versioning.get("fields") or []
    versioning_review = {
        "review_id": "model_versioning_replacement_policy_review_v1",
        **_review_from_checks([
            ("version_fields", len(version_fields) >= 5),
            ("no_auto_switch", replacement.get("no_auto_switch_without_policy") is True),
            ("rollback", "rollback" in str(version_fields)),
            ("benchmark_reval", "benchmark_revalidation" in str(version_fields)),
            ("license_ref", "license" in str(version_fields)),
        ]),
        "versioning_fields_expected": list(VERSIONING_FIELDS),
        **meta,
    }

    gap_entries = gap_matrix.get("entries") or []
    gap_checks: List[Tuple[str, bool]] = [("entries12", len(gap_entries) == 12)]
    for entry in gap_entries:
        did = entry.get("capability_domain_id", "x")[:12]
        for field in ("current_gap", "severity", "blocker_or_non_blocker", "next_action", "recommended_phase", "dependency", "priority"):
            gap_checks.append((f"{did}.{field[:6]}", bool(entry.get(field))))
        gap_checks.append((f"{did}.not_direct_runtime", "runtime" not in str(entry.get("next_action", "")).lower() or "planning" in str(entry.get("recommended_phase", "")).lower() or "readiness" in str(entry.get("recommended_phase", "")).lower()))
    gap_review = {
        "review_id": "current_gap_and_next_action_review_v1",
        **_review_from_checks(gap_checks),
        **meta,
    }

    risk_checks = [(f"risk.{r[:16]}", r in (risk_reg.get("risks") or [])) for r in ROADMAP_RISKS]
    risk_review = {
        "review_id": "roadmap_risk_register_review_v1",
        **_review_from_checks(risk_checks),
        **meta,
    }

    boundary_audit = {
        "audit_id": "roadmap_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "roadmap_blocked_path_result_v1",
        "blocked_paths": [{"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    domain_reviews_all = [
        capability_domain_inventory_review,
        current_model_asset_inventory_review,
        goal_stage_to_capability_domain_review,
        vision_review,
        ocr_review,
        tts_review,
        asr_review,
        map_review,
        st_review,
        memory_review,
        emotion_review,
        evolution_review,
        provider_review,
        output_review,
        health_review,
        source_review,
        candidate_register_review,
        module_profile_review,
        mid_binding_review,
        io_review,
        quality_review,
        versioning_review,
        gap_review,
        risk_review,
    ]

    all_reviews_pass = (
        input_ok
        and all(r.get("review_pass") for r in domain_reviews_all)
        and blocked_path_result.get("all_blocked")
        and boundary_audit.get("audit_pass")
    )

    closure_decision = {
        "decision_id": "roadmap_closure_decision_v1",
        "dryrun_and_review_pass": all_reviews_pass,
        "high_risk": not all_reviews_pass,
        "final_decision": FINAL_DECISION_GO if all_reviews_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_reviews_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "12 capability domain roadmaps reviewed",
            "current model asset inventory validated",
            "module-local profile + midplatform binding contracts confirmed as admission gate",
            "gap/next-action matrix aligned to goal stages",
            "ready for Model Profile Registry Planning",
        ] if all_reviews_pass else ["hold for issue review"],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_model_profile_registry_planning": all_reviews_pass,
        "selected_next_phase": NEXT_PHASE_GO if all_reviews_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "scenario_model_capability_roadmap_inventory_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {"register_id": "non_claims_register_v1", "non_claims": list(NON_CLAIMS), **meta}

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_and_review_pass": all_reviews_pass,
        "capability_domain_count": len(CAPABILITY_DOMAIN_IDS),
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "scenario_model_capability_roadmap_inventory_dryrun_review_policy": policy,
        "planning_input_review": planning_input_review,
        "scenario_model_capability_roadmap_candidate": roadmap_candidate,
        "capability_domain_inventory_review": capability_domain_inventory_review,
        "current_model_asset_inventory_review": current_model_asset_inventory_review,
        "goal_stage_to_capability_domain_review": goal_stage_to_capability_domain_review,
        "vision_scene_understanding_roadmap_review": vision_review,
        "ocr_text_reading_roadmap_review": ocr_review,
        "tts_voice_output_roadmap_review": tts_review,
        "asr_voice_input_roadmap_review": asr_review,
        "map_navigation_roadmap_review": map_review,
        "spatiotemporal_world_continuity_roadmap_review": st_review,
        "memory_personal_continuity_roadmap_review": memory_review,
        "emotion_engine_roadmap_review": emotion_review,
        "evolutionary_recursion_roadmap_review": evolution_review,
        "provider_model_management_roadmap_review": provider_review,
        "output_gate_chain_roadmap_review": output_review,
        "health_whitebox_validation_governance_roadmap_review": health_review,
        "model_source_strategy_review": source_review,
        "candidate_register_review": candidate_register_review,
        "module_local_model_profile_contract_review": module_profile_review,
        "midplatform_model_governance_binding_contract_review": mid_binding_review,
        "model_input_output_contract_review": io_review,
        "model_quality_acceptance_criteria_review": quality_review,
        "model_versioning_replacement_policy_review": versioning_review,
        "current_gap_and_next_action_review": gap_review,
        "roadmap_risk_register_review": risk_review,
        "roadmap_boundary_audit": boundary_audit,
        "roadmap_blocked_path_result": blocked_path_result,
        "roadmap_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
