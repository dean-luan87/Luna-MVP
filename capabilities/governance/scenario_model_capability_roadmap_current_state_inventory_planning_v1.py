# -*- coding: utf-8 -*-
"""Scenario Model Capability Roadmap and Current State Inventory Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_scene_understanding_output_chain_closure_review_v1 import (
    FINAL_DECISION_GO as CLOSURE_REVIEW_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_user_output_gate_chain_dryrun_v1 import (
    FINAL_DECISION_GO as GATE_CHAIN_DR_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_PLUG_DR_FINAL_GO,
)

PHASE_ID = "Phase-Scenario-Model-Capability-Roadmap-and-Current-State-Inventory-Planning-v1-001"
SCOPE = "scenario_model_capability_roadmap_inventory_planning_only"
SOURCE_CHAIN = "scenario_model_capability_roadmap_current_state_inventory_planning_v1"

FINAL_DECISION_GO = (
    "SCENARIO_MODEL_CAPABILITY_ROADMAP_AND_CURRENT_STATE_INVENTORY_PLANNING_"
    "READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "SCENARIO_MODEL_CAPABILITY_ROADMAP_AND_CURRENT_STATE_INVENTORY_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Scenario-Model-Capability-Roadmap-and-Current-State-Inventory-DryRunAndReview-v1-001"
)
NEXT_PHASE_HOLD = "Phase-Scenario-Model-Capability-Roadmap-Issue-Review-v1-001"

CAPABILITY_DOMAIN_IDS: Tuple[str, ...] = (
    "first_person_vision_scene_understanding",
    "ocr_text_recognition_reading",
    "asr_voice_input",
    "tts_voice_output",
    "map_location_navigation_application",
    "spatiotemporal_world_continuity",
    "memory_personal_continuity",
    "emotion_engine_social_adaptation",
    "evolutionary_recursion_self_improvement",
    "provider_model_management",
    "output_gate_chain",
    "health_whitebox_validation_governance",
)

DOMAIN_INVENTORY_FIELDS: Tuple[str, ...] = (
    "capability_domain_id",
    "current_goal_stage",
    "first_stage_goal",
    "later_stage_goal",
    "implementation_plan",
    "actual_completion_status",
    "existing_assets_or_artifacts",
    "already_integrated_or_registered_models",
    "candidate_model_sources",
    "model_source_strategy",
    "module_local_model_profile_needed",
    "midplatform_governance_binding_needed",
    "input_contracts",
    "output_contracts",
    "supervision_requirements",
    "quality_acceptance_criteria",
    "current_gaps",
    "next_actions",
    "version_update_replacement_notes",
)

ASSET_STATUS_TYPES: Tuple[str, ...] = (
    "implemented_artifact",
    "dryrun_validated",
    "candidate_registered",
    "planned_only",
    "deferred",
    "blocked",
    "not_started",
)

MODULE_PROFILE_FIELDS: Tuple[str, ...] = (
    "module_id", "capability_domain", "capability_stack_ref", "layered_governance_mapping_ref",
    "model_profile_id", "model_role", "model_source_strategy", "model_name_candidate",
    "model_version", "model_license_ref", "model_update_policy_ref", "input_contract_ref",
    "output_contract_ref", "candidate_output_type", "confidence_semantics", "latency_budget",
    "resource_budget", "health_metrics_required", "validation_tests_required",
    "fallback_model_refs", "replacement_conditions", "provider_abstraction_ref",
    "governance_binding_ref", "no_direct_fact_action_output",
)

MIDPLATFORM_BINDING_FIELDS: Tuple[str, ...] = (
    "model_profile_ref", "capability_bus_contract_ref", "constitution_bus_ref",
    "provider_abstraction_ref", "layered_capability_stack_ref", "layered_governance_mapping_ref",
    "validation_requirement_ref", "health_requirement_ref", "whitebox_trace_requirement_ref",
    "information_integration_consumption_policy", "decision_center_consumption_policy",
    "controlled_runtime_requirement_ref", "memory_worldmodel_admission_policy_ref",
    "output_gate_requirement_ref", "version_compatibility_ref",
)

EXTERNAL_CANDIDATE_REGISTER_FIELDS: Tuple[str, ...] = (
    "candidate_name", "capability_domain", "model_source_strategy", "current_status",
    "known_version_info_required_later", "license_review_required_later",
    "update_tracking_required_later", "provider_abstraction_required",
    "model_profile_required_later", "not_selected_now", "not_invoked_now",
)

MODEL_SOURCE_TYPES: Tuple[str, ...] = (
    "direct_open_source_or_external_provider",
    "reference_inspired_rebuild",
    "self_developed_core_capability",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Planning GO ≠ model selected",
    "current asset inventory ≠ runtime readiness",
    "existing YOLO/OCR/TTS mention ≠ Luna 2.0 model profile complete",
    "candidate register ≠ license cleared",
    "next DryRunAndReview ≠ benchmark or runtime",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("scenario_model_capability_roadmap_inventory_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "model_selected_now", "model_downloaded_now", "model_invoked_now", "provider_invoked_now",
    "model_runtime_enabled_now", "benchmark_executed_now", "training_started_now",
    "fine_tuning_started_now", "code_generation_executed_now", "skill_added_now",
    "runtime_enabled_now", "memory_written_now", "world_model_written_now",
    "task_state_committed_now", "user_output_generated_now",
)

ROADMAP_RISKS: Tuple[str, ...] = (
    "dependency_risk", "license_risk", "model_update_breakage", "provider_lock_in",
    "hallucination_false_recognition_risk", "identity_privacy_risk", "unsafe_navigation_risk",
    "memory_worldmodel_contamination", "auto_switch_instability", "overfitting_market_feedback",
    "model_becoming_universal_brain_risk", "module_bypassing_governance_risk",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "scenario_model_capability_roadmap_current_state_inventory_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
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


def _domain_entry(
    domain_id: str,
    *,
    current_goal_stage: str,
    first_stage_goal: List[str],
    later_stage_goal: List[str],
    implementation_plan: List[str],
    actual_completion_status: List[str],
    existing_assets: List[str],
    integrated_models: List[str],
    candidate_sources: List[str],
    source_strategy: str,
    input_contracts: List[str],
    output_contracts: List[str],
    supervision: List[str],
    acceptance: List[str],
    gaps: List[str],
    next_actions: List[str],
    version_notes: str,
) -> Dict[str, Any]:
    return {
        "capability_domain_id": domain_id,
        "current_goal_stage": current_goal_stage,
        "first_stage_goal": first_stage_goal,
        "later_stage_goal": later_stage_goal,
        "implementation_plan": implementation_plan,
        "actual_completion_status": actual_completion_status,
        "existing_assets_or_artifacts": existing_assets,
        "already_integrated_or_registered_models": integrated_models,
        "candidate_model_sources": candidate_sources,
        "model_source_strategy": source_strategy,
        "module_local_model_profile_needed": True,
        "midplatform_governance_binding_needed": True,
        "input_contracts": input_contracts,
        "output_contracts": output_contracts,
        "supervision_requirements": supervision,
        "quality_acceptance_criteria": acceptance,
        "current_gaps": gaps,
        "next_actions": next_actions,
        "version_update_replacement_notes": version_notes,
    }


def run_scenario_model_capability_roadmap_current_state_inventory_planning_v1(
    *,
    first_person_scene_understanding_output_chain_closure_review_root: str,
    first_person_scene_understanding_user_output_gate_chain_dryrun_root: str,
    first_person_scene_understanding_output_candidate_dryrun_root: str,
    first_person_scene_understanding_task_response_candidate_dryrun_root: str,
    first_person_scene_understanding_decision_chain_candidate_dryrun_root: str,
    first_person_scene_understanding_information_integration_chain_dryrun_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    seed_core_pluggable_layer_architecture_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    closure_pending = False

    closure_root = Path(first_person_scene_understanding_output_chain_closure_review_root).expanduser().resolve()
    gate_root = Path(first_person_scene_understanding_user_output_gate_chain_dryrun_root).expanduser().resolve()
    stack_root = Path(layered_capability_stack_standard_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root).expanduser().resolve()
    provider_root = Path(provider_abstraction_standard_alignment_dryrun_and_review_root).expanduser().resolve()
    ds_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    sc_plug_root = Path(seed_core_pluggable_layer_architecture_dryrun_and_review_root).expanduser().resolve()

    closure_vr = _try_read_json(closure_root / "verifier_report.json") or {}
    closure_sm = _try_read_json(closure_root / "summary.json") or {}
    gate_vr = _try_read_json(gate_root / "verifier_report.json") or {}
    stack_vr = _try_read_json(stack_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    ds_vr = _try_read_json(ds_root / "verifier_report.json") or {}
    sc_plug_vr = _try_read_json(sc_plug_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root), "upstream_closure_review_root": str(closure_root)}

    if closure_vr.get("verifier") == "GO":
        if closure_sm.get("final_decision") != CLOSURE_REVIEW_FINAL_GO:
            blockers.append("closure review final_decision mismatch")
    elif gate_vr.get("verifier") == "GO":
        closure_pending = True
        meta["closure_pending"] = True
    else:
        blockers.append("Output Chain Closure Review or Gate Chain DryRun must be GO")

    for name, vr in (
        ("stack_std", stack_vr), ("constitution_bus", cb_vr), ("provider_abs", provider_vr),
        ("drive_signal", ds_vr), ("seed_core_plug", sc_plug_vr),
    ):
        if vr.get("verifier") != "GO":
            blockers.append(f"{name} must be GO")

    input_ok = len(blockers) == 0

    upstream_input = {
        "review_id": "upstream_output_chain_input_review_v1",
        "review_pass": input_ok,
        "closure_review_verifier": closure_vr.get("verifier"),
        "closure_pending": closure_pending,
        "four_goal_priority_confirmed": True,
        "layered_stack_standard_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layered_governance_mapping_ref": ADDENDUM_ID,
        "blockers": list(blockers),
        **meta,
    }

    luna_roadmap = {
        "roadmap_id": "luna_model_capability_roadmap_v1",
        "roadmap_type": "product_development_roadmap_with_inventory",
        "answers": [
            "每个能力域第一阶段目标是什么",
            "当前已经接入/验证/规划了什么",
            "已完成内容对应哪个目标",
            "缺口在哪里",
            "下一阶段该补模型/合同/测试还是治理",
        ],
        "capability_domain_count": len(CAPABILITY_DOMAIN_IDS),
        **meta,
    }

    vision_domain = _domain_entry(
        "first_person_vision_scene_understanding",
        current_goal_stage="stage_1",
        first_stage_goal=[
            "当前场景理解", "目标识别", "文字区域识别", "基础风险/障碍候选", "目标追踪候选",
            "语音任务到目标搜索绑定",
            "输出 visual_observation_candidate / target_recognition_candidate / scene_context_candidate / risk_context_candidate",
            "不输出 fact/action/user_output",
        ],
        later_stage_goal=["连续帧理解", "VLM 场景摘要", "Grounded segmentation", "真实 camera controlled runtime"],
        implementation_plan=[
            "YOLO-family 基础目标检测候选", "Grounded SAM style grounding/segmentation later",
            "Tracking candidate 连续追踪 later", "VLM scene understanding later",
            "OCR module binding 文字候选", "Information Integration 整合场景/风险/任务意图",
            "Decision Center 裁决 observe_more/hold/ask_user",
        ],
        actual_completion_status=[
            "First-Person II→Decision→Task Response→Output Candidate→Gate Chain DryRun GO",
            "候选已定义: visual_observation/target_recognition/text_recognition/target_tracking/scene_context/spatiotemporal/world_continuity/risk_context",
            "当前 fixture/candidate/dryrun", "camera/real frame/vision runtime 未开启",
            "YOLO 历史接入需重新映射 Luna 2.0 capability stack",
        ],
        existing_assets=[
            "first_person_scene_understanding_information_integration_chain_dryrun",
            "first_person_scene_understanding_decision_chain_candidate_dryrun",
            "first_person_scene_understanding_task_response_candidate_dryrun",
            "first_person_scene_understanding_output_candidate_dryrun",
            "first_person_scene_understanding_user_output_gate_chain_dryrun",
        ],
        integrated_models=["yolo_family_candidate_registered", "vision_provider_candidate_historical"],
        candidate_sources=["yolo_family", "grounded_sam_style", "tracking_candidate", "vlm_scene_candidate"],
        source_strategy="direct_open_source_or_external_provider",
        input_contracts=["frame_candidate", "task_intent_candidate"],
        output_contracts=["visual_observation_candidate", "target_recognition_candidate", "scene_context_candidate", "risk_context_candidate"],
        supervision=["validation", "health", "whitebox", "layered_governance_L1"],
        acceptance=["candidate_only_compliance", "confidence_calibration", "latency_budget"],
        gaps=[
            "未做真实 camera controlled runtime", "未做真实连续帧理解", "未做 tracking provider benchmark",
            "未做 Grounded segmentation model profile", "未做 VLM scene model profile", "未做 acceptance 实测",
        ],
        next_actions=[
            "建立 Vision Module-local Model Profile", "登记 YOLO/Grounding/Tracking/VLM candidates",
            "定义 Vision input/output contract", "定义 benchmark/latency/resource/confidence criteria",
            "先做 controlled runtime readiness planning 不直接启 runtime",
        ],
        version_notes="YOLO/Grounding/Tracking 需 version/update/replacement policy per provider abstraction",
    )

    ocr_domain = _domain_entry(
        "ocr_text_recognition_reading",
        current_goal_stage="stage_1_stage_4_reading_later",
        first_stage_goal=[
            "text_region_candidate", "ocr_result_candidate", "signage_context_candidate",
            "OCR evidence candidate", "不写事实，不直接影响导航动作",
        ],
        later_stage_goal=["text structure understanding", "long text reading capability"],
        implementation_plan=["RapidOCR/PaddleOCR/future OCR providers", "segment-first/region-first OCR", "reading capability later"],
        actual_completion_status=[
            "OCRRequest/OCR evidence/provider abstraction/real dependency minimal check 历史已有",
            "RapidOCR/PaddleOCR 链路需 Luna 2.0 重新归档", "OCR output 默认 candidate not fact",
        ],
        existing_assets=["ocr_provider_authorization_request", "ocr_real_dependency_formal_execution", "provider_abstraction_ocr_binding"],
        integrated_models=["paddleocr_candidate", "rapidocr_candidate"],
        candidate_sources=["paddleocr", "rapidocr", "other_ocr_provider"],
        source_strategy="direct_open_source_or_external_provider",
        input_contracts=["roi_candidate", "frame_candidate"],
        output_contracts=["text_region_candidate", "ocr_result_candidate", "signage_context_candidate"],
        supervision=["validation", "whitebox", "provider_readiness"],
        acceptance=["ocr_accuracy_candidate", "false_positive_control"],
        gaps=["真实 OCR provider runtime 未打开", "文本结构理解未完成", "长文本阅读未完成", "OCR quality benchmark 待补"],
        next_actions=["OCR Module-local Model Profile", "OCR benchmark plan", "region-first contract finalize"],
        version_notes="OCR provider version/license tracking required before runtime",
    )

    tts_domain = _domain_entry(
        "tts_voice_output",
        current_goal_stage="stage_3_output_layer",
        first_stage_goal=[
            "TTS Runtime abstract planning", "qianwen_tts_candidate registered",
            "speech_request_candidate/audio_artifact_candidate only", "不触发真实 TTS/audio",
        ],
        later_stage_goal=["voice profile", "naturalness benchmark", "local TTS MOSS-style"],
        implementation_plan=["TTS provider abstraction", "Speech Gate→Voice Output Plane→TTS Runtime chain"],
        actual_completion_status=[
            "TTS Runtime Planning + DryRun GO", "Qianwen current preferred provider candidate not selected/invoked",
            "Speech Gate/Voice Output Plane/TTS Runtime 边界清楚",
        ],
        existing_assets=["midplatform_tts_runtime_dryrun", "midplatform_voice_output_plane_dryrun", "provider_abstraction_tts_binding"],
        integrated_models=["qianwen_tts_candidate_registered"],
        candidate_sources=["qianwen_tts", "moss_tts_style", "local_tts"],
        source_strategy="direct_open_source_or_external_provider",
        input_contracts=["speech_request_candidate"],
        output_contracts=["audio_artifact_candidate"],
        supervision=["speech_gate", "output_gate", "controlled_runtime"],
        acceptance=["latency", "naturalness", "privacy"],
        gaps=["未做真实 TTS 调用", "未做 voice profile/model selection", "未做 latency/quality benchmark", "MOSS-TTS 待登记"],
        next_actions=["TTS model profile inventory", "voice profile contract", "benchmark plan"],
        version_notes="qianwen_tts_candidate ≠ selected ≠ invoked; no auto-switch",
    )

    asr_domain = _domain_entry(
        "asr_voice_input",
        current_goal_stage="not_started_runtime",
        first_stage_goal=["ASR transcript candidate", "voice intent candidate", "不直接驱动 action"],
        later_stage_goal=["multi-turn voice dialogue", "speaker diarization", "voice-to-task chain"],
        implementation_plan=["SenseVoice/Whisper-like/Qwen-ASR style candidates", "Voice Input Capability Stack later"],
        actual_completion_status=["语音交互主线尚未完整 runtime 接入", "ASR/语音输入/多轮语义/真实语音到任务链闭环尚未完成"],
        existing_assets=["voice_capability_stack_reference_in_layered_stack_standard"],
        integrated_models=[],
        candidate_sources=["sensevoice", "whisper_like", "qwen_asr_style"],
        source_strategy="direct_open_source_or_external_provider",
        input_contracts=["audio_candidate"],
        output_contracts=["transcript_candidate"],
        supervision=["validation", "privacy"],
        acceptance=["wer_candidate", "latency"],
        gaps=["Voice Input Stack 未完整", "ASR provider 未登记 profile", "无 benchmark"],
        next_actions=["Voice Input Capability Stack planning", "ASR candidate register", "input contract"],
        version_notes="deferred until Voice Input stack defined",
    )

    map_domain = _domain_entry(
        "map_location_navigation_application",
        current_goal_stage="stage_3",
        first_stage_goal=["route context candidate", "navigation application context", "不执行导航动作"],
        later_stage_goal=["facility search", "transit navigation", "navigation action candidate later"],
        implementation_plan=["map provider abstraction", "route reasoning reference rebuild", "depends Stage 1+2"],
        actual_completion_status=[
            "navigation application context candidate 在 First-Person 链完成", "map provider runtime 未开启",
        ],
        existing_assets=["first_person_navigation_application_task_response_review", "map_navigation_capability_stack_reference"],
        integrated_models=[],
        candidate_sources=["map_provider_candidate"],
        source_strategy="reference_inspired_rebuild",
        input_contracts=["map_context_candidate", "location_context_candidate"],
        output_contracts=["route_context_candidate", "navigation_readiness_candidate"],
        supervision=["safety_gate", "navigation_action_gate_blocked"],
        acceptance=["navigation_readiness", "safety_hold_rate"],
        gaps=["map provider runtime 未开", "route/facility search profile 未建", "navigation benchmark 未做"],
        next_actions=["map/location model profile", "route context profile", "facility search profile"],
        version_notes="Stage 3 only; depends Stage 1+2 readiness",
    )

    st_domain = _domain_entry(
        "spatiotemporal_world_continuity",
        current_goal_stage="stage_2",
        first_stage_goal=["frame sequence", "scene delta", "world continuity hypothesis", "freshness/conflict/gap"],
        later_stage_goal=["STCM", "visual-map alignment", "missing context completion"],
        implementation_plan=[
            "Luna 自研/参考重建: Scene Delta/STCM/world continuity governance",
            "外部模型提供 visual/tracking/SLAM/scene graph 信号，治理整合自有",
        ],
        actual_completion_status=[
            "spatiotemporal_context/world_continuity 候选在 First-Person II 链定义",
            "freshness/conflict/gap refs 在 decision/output 链保留",
        ],
        existing_assets=["first_person_spatiotemporal_task_response_review", "layered_governance_mapping_L2"],
        integrated_models=["tracking_signal_candidate"],
        candidate_sources=["tracking", "slam_signal", "scene_graph_reference"],
        source_strategy="reference_inspired_rebuild",
        input_contracts=["frame_sequence_candidate", "integrated_context_candidate"],
        output_contracts=["spatiotemporal_context_candidate", "world_continuity_hypothesis_candidate"],
        supervision=["freshness", "conflict", "gap", "evidence_chain"],
        acceptance=["continuity_hypothesis_not_fact", "gap_detection_rate"],
        gaps=["STCM 未实现", "visual-map alignment 未做", "真实连续帧未启"],
        next_actions=["STCM architecture plan", "continuity manager profile", "reference extraction"],
        version_notes="不能由单一外部模型替代",
    )

    memory_domain = _domain_entry(
        "memory_personal_continuity",
        current_goal_stage="stage_5_later",
        first_stage_goal=["memory context candidate read only", "no write without admission"],
        later_stage_goal=["Personal Continuity Module", "life memory module", "relationship model"],
        implementation_plan=["Luna 自研 Personal Continuity", "external embedding/retrieval 仅检索器官", "Memory Admission Gate"],
        actual_completion_status=["memory_write blocked in all dryruns", "memory capability stack reference defined"],
        existing_assets=["memory_capability_stack_reference", "memory_admission_gate_in_coverage_matrix"],
        integrated_models=["embedding_retrieval_candidate_later"],
        candidate_sources=["embedding_retrieval_later"],
        source_strategy="self_developed_core_capability",
        input_contracts=["memory_context_candidate"],
        output_contracts=["memory_admission_proposal_candidate"],
        supervision=["memory_admission_gate", "identity_gate", "privacy_gate"],
        acceptance=["anti_copy", "anti_miswrite", "write_admission_rate"],
        gaps=["Personal Continuity Module 未实现", "memory stick 硬件化 later", "retrieval profile 未建"],
        next_actions=["Personal Continuity architecture", "admission policy", "retrieval candidate register"],
        version_notes="写入准入/身份连续/防克隆/防污染 Luna 自研",
    )

    emotion_domain = _domain_entry(
        "emotion_engine_social_adaptation",
        current_goal_stage="stage_5_survival_submodule",
        first_stage_goal=["emotion signal candidate", "social rhythm hint candidate"],
        later_stage_goal=["relationship model", "expression adaptation"],
        implementation_plan=["Emotion Engine 属 Survival Drive 子模块", "外部情绪识别模型作信号", "治理/关系模型 Luna 自研"],
        actual_completion_status=["emotion capability stack reference", "drive_signal in II chain"],
        existing_assets=["emotion_capability_stack_reference", "seed_core_drive_signal_contract"],
        integrated_models=["emotion_recognition_signal_candidate_later"],
        candidate_sources=["speech_emotion", "facial_emotion_later"],
        source_strategy="self_developed_core_capability",
        input_contracts=["drive_signal_candidate"],
        output_contracts=["emotion_signal_candidate"],
        supervision=["survival_priority", "relationship_gate_later"],
        acceptance=["emotion_not_fact", "social_adaptation_candidate"],
        gaps=["Emotion Engine runtime 未建", "relationship model 未建"],
        next_actions=["Emotion Engine profile", "signal vs governance boundary doc"],
        version_notes="核心情感治理 Luna 自研",
    )

    evolution_domain = _domain_entry(
        "evolutionary_recursion_self_improvement",
        current_goal_stage="stage_6_proposal_only",
        first_stage_goal=["capability gap proposal", "model replacement recommendation proposal"],
        later_stage_goal=["skill expansion proposal", "logic revision proposal"],
        implementation_plan=["Evolutionary Recursion Survival submodule", "analysis models 辅助", "governance/owner/validation/rollback 必须"],
        actual_completion_status=["evolutionary_recursion in stage 6 roadmap", "proposal_only in all boundaries"],
        existing_assets=["seed_core_pluggable_layer_architecture", "evolutionary_recursion in layered stack"],
        integrated_models=["feedback_analysis_candidate_later"],
        candidate_sources=["market_analysis_reference"],
        source_strategy="self_developed_core_capability",
        input_contracts=["feedback_candidate"],
        output_contracts=["proposal_candidate"],
        supervision=["owner_review", "validation", "rollback"],
        acceptance=["proposal_only", "no_auto_code_change"],
        gaps=["Evolution module 未实现", "proposal workflow 未建"],
        next_actions=["Evolution governance plan", "proposal-only boundary tests"],
        version_notes="外部模型不能自我修改 Luna; proposal_only=true",
    )

    provider_domain = _domain_entry(
        "provider_model_management",
        current_goal_stage="foundation",
        first_stage_goal=["provider abstraction", "candidate register", "no auto-switch"],
        later_stage_goal=["model registry", "version tracking", "replacement orchestration"],
        implementation_plan=["runtime≠provider", "module profile + midplatform binding", "unified version/replacement policy"],
        actual_completion_status=[
            "Provider Abstraction Standard DryRun GO", "qianwen/OCR/vision as provider_candidate",
            "Controlled Runtime framework planned",
        ],
        existing_assets=["provider_abstraction_standard_alignment_dryrun", "controlled_runtime_planning"],
        integrated_models=["provider_candidate_registry"],
        candidate_sources=["all_external_candidates"],
        source_strategy="self_developed_core_capability",
        input_contracts=["provider_readiness_request_candidate"],
        output_contracts=["provider_readiness_result_candidate"],
        supervision=["authorization_gate", "provider_readiness_gate"],
        acceptance=["no_auto_switch", "license_tracking"],
        gaps=["unified model registry 未实现", "auto-switch policy enforcement 未 runtime"],
        next_actions=["Model Registry planning", "provider profile template", "replacement orchestration"],
        version_notes="provider_candidate≠selected≠invoked",
    )

    output_domain = _domain_entry(
        "output_gate_chain",
        current_goal_stage="stage_3_output_enforcement",
        first_stage_goal=["user_output_candidate", "gate_result_candidate", "enforcement_result_candidate"],
        later_stage_goal=["Voice Output Plane", "Display Output execution later"],
        implementation_plan=["Constitution→Safety→Speech→Display Gate chain", "16 gate coverage matrix"],
        actual_completion_status=["Output Candidate DryRun GO", "Gate Chain DryRun GO", "Closure Review GO"],
        existing_assets=["midplatform_user_output_constitution", "safety/speech/display_gate_dryruns", "gate_chain_coverage_matrix"],
        integrated_models=[],
        candidate_sources=[],
        source_strategy="self_developed_core_capability",
        input_contracts=["user_output_candidate"],
        output_contracts=["gate_result_candidate", "enforcement_result_candidate"],
        supervision=["all_output_gates", "privacy_identity_later"],
        acceptance=["gate_chain_complete_candidate", "no_user_facing_without_gate"],
        gaps=["execution layer Voice/Display runtime 未启"],
        next_actions=["Gate Chain Closure maintained", "execution handoff when controlled runtime ready"],
        version_notes="gate result ≠ execution",
    )

    health_domain = _domain_entry(
        "health_whitebox_validation_governance",
        current_goal_stage="foundation_oversight",
        first_stage_goal=["health signal carry", "whitebox trace", "validation tests"],
        later_stage_goal=["Health Enforcement Supervisor runtime"],
        implementation_plan=["Health external to Bus", "Validation Factory", "Whitebox trace required on all models"],
        actual_completion_status=["health_enforcement_supervisor_dryrun", "whitebox in all candidate chains", "health_ref carried not judged by Bus"],
        existing_assets=["health_enforcement_supervisor_dryrun", "validation_in_layered_governance"],
        integrated_models=[],
        candidate_sources=[],
        source_strategy="self_developed_core_capability",
        input_contracts=["health_signal_bundle"],
        output_contracts=["health_supervision_result_candidate"],
        supervision=["external_oversight_not_bus_self_judge"],
        acceptance=["traceability_completeness"],
        gaps=["Health Supervisor runtime 未启", "per-model health metrics 未绑定"],
        next_actions=["Model health metrics template", "bind to module profile"],
        version_notes="Bus transports health_ref ≠ Bus judges health",
    )

    domain_map = {
        "first_person_vision_scene_understanding": vision_domain,
        "ocr_text_recognition_reading": ocr_domain,
        "asr_voice_input": asr_domain,
        "tts_voice_output": tts_domain,
        "map_location_navigation_application": map_domain,
        "spatiotemporal_world_continuity": st_domain,
        "memory_personal_continuity": memory_domain,
        "emotion_engine_social_adaptation": emotion_domain,
        "evolutionary_recursion_self_improvement": evolution_domain,
        "provider_model_management": provider_domain,
        "output_gate_chain": output_domain,
        "health_whitebox_validation_governance": health_domain,
    }

    domain_inventory = {
        "matrix_id": "capability_domain_inventory_matrix_v1",
        "domain_count": len(CAPABILITY_DOMAIN_IDS),
        "domains": [domain_map[did] for did in CAPABILITY_DOMAIN_IDS],
        **meta,
    }

    asset_inventory = {
        "inventory_id": "current_model_asset_inventory_v1",
        "status_types": list(ASSET_STATUS_TYPES),
        "assets": [
            {"asset_id": "yolo_object_detection", "category": "vision", "status": "candidate_registered", "notes": "historical; remap to Luna 2.0 stack"},
            {"asset_id": "paddleocr", "category": "ocr", "status": "candidate_registered"},
            {"asset_id": "rapidocr", "category": "ocr", "status": "candidate_registered"},
            {"asset_id": "ocr_request_evidence_chain", "category": "ocr", "status": "dryrun_validated"},
            {"asset_id": "qianwen_tts_candidate", "category": "tts", "status": "candidate_registered", "not_selected": True, "not_invoked": True},
            {"asset_id": "tts_runtime_planning", "category": "tts", "status": "dryrun_validated"},
            {"asset_id": "asr_voice_input", "category": "asr", "status": "not_started", "notes": "voice interaction not runtime-connected"},
            {"asset_id": "first_person_scene_chain", "category": "vision", "status": "dryrun_validated"},
            {"asset_id": "provider_abstraction_standard", "category": "provider", "status": "dryrun_validated"},
            {"asset_id": "controlled_runtime_framework", "category": "provider", "status": "planned_only"},
            {"asset_id": "output_speech_display_gate_chain", "category": "output", "status": "dryrun_validated"},
            {"asset_id": "grounded_sam_segmentation", "category": "vision", "status": "planned_only"},
            {"asset_id": "tracking_provider", "category": "vision", "status": "planned_only"},
            {"asset_id": "moss_tts_local", "category": "tts", "status": "deferred"},
            {"asset_id": "sensevoice_asr", "category": "asr", "status": "deferred"},
        ],
        **meta,
    }

    goal_domain_matrix = {
        "matrix_id": "goal_stage_to_capability_domain_matrix_v1",
        "mappings": [
            {"goal_stage": "stage_1", "domains": ["first_person_vision_scene_understanding", "ocr_text_recognition_reading"]},
            {"goal_stage": "stage_2", "domains": ["spatiotemporal_world_continuity"]},
            {"goal_stage": "stage_3", "domains": ["map_location_navigation_application", "tts_voice_output", "output_gate_chain"]},
            {"goal_stage": "stage_4", "domains": ["ocr_text_recognition_reading"]},
            {"goal_stage": "stage_5", "domains": ["memory_personal_continuity", "emotion_engine_social_adaptation"]},
            {"goal_stage": "stage_6", "domains": ["evolutionary_recursion_self_improvement"]},
            {"goal_stage": "foundation", "domains": ["provider_model_management", "health_whitebox_validation_governance", "asr_voice_input"]},
        ],
        **meta,
    }

    roadmap_template = {
        "template_id": "capability_domain_roadmap_template_v1",
        "required_sections": list(DOMAIN_INVENTORY_FIELDS),
        "section_count": len(DOMAIN_INVENTORY_FIELDS),
        **meta,
    }

    def _roadmap_file(domain_id: str, roadmap_id: str) -> Dict[str, Any]:
        d = domain_map[domain_id]
        return {"roadmap_id": roadmap_id, "capability_domain": domain_id, **d, **meta}

    vision_roadmap = _roadmap_file("first_person_vision_scene_understanding", "vision_scene_understanding_roadmap_v1")
    ocr_roadmap = _roadmap_file("ocr_text_recognition_reading", "ocr_text_reading_roadmap_v1")
    tts_roadmap = _roadmap_file("tts_voice_output", "tts_voice_output_roadmap_v1")
    asr_roadmap = _roadmap_file("asr_voice_input", "asr_voice_input_roadmap_v1")
    map_roadmap = _roadmap_file("map_location_navigation_application", "map_navigation_roadmap_v1")
    st_roadmap = _roadmap_file("spatiotemporal_world_continuity", "spatiotemporal_world_continuity_roadmap_v1")
    memory_roadmap = _roadmap_file("memory_personal_continuity", "memory_personal_continuity_roadmap_v1")
    emotion_roadmap = _roadmap_file("emotion_engine_social_adaptation", "emotion_engine_roadmap_v1")
    evolution_roadmap = _roadmap_file("evolutionary_recursion_self_improvement", "evolutionary_recursion_roadmap_v1")
    provider_roadmap = _roadmap_file("provider_model_management", "provider_model_management_roadmap_v1")

    source_taxonomy = {
        "taxonomy_id": "model_source_strategy_taxonomy_v1",
        "source_types": list(MODEL_SOURCE_TYPES),
        "A_direct": "direct_open_source_or_external_provider",
        "B_reference": "reference_inspired_rebuild",
        "C_self_dev": "self_developed_core_capability",
        **meta,
    }

    external_candidates = [
        {"candidate_name": "yolo_family", "capability_domain": "first_person_vision_scene_understanding", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "candidate_registered"},
        {"candidate_name": "grounded_sam_style", "capability_domain": "first_person_vision_scene_understanding", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "planned_only"},
        {"candidate_name": "paddleocr", "capability_domain": "ocr_text_recognition_reading", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "candidate_registered"},
        {"candidate_name": "rapidocr", "capability_domain": "ocr_text_recognition_reading", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "candidate_registered"},
        {"candidate_name": "sensevoice", "capability_domain": "asr_voice_input", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "deferred"},
        {"candidate_name": "whisper_like", "capability_domain": "asr_voice_input", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "deferred"},
        {"candidate_name": "qianwen_tts", "capability_domain": "tts_voice_output", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "candidate_registered"},
        {"candidate_name": "moss_tts_style", "capability_domain": "tts_voice_output", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "deferred"},
        {"candidate_name": "object_tracking", "capability_domain": "first_person_vision_scene_understanding", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "planned_only"},
        {"candidate_name": "vlm_scene_understanding", "capability_domain": "first_person_vision_scene_understanding", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "planned_only"},
        {"candidate_name": "embedding_retrieval", "capability_domain": "memory_personal_continuity", "model_source_strategy": "direct_open_source_or_external_provider", "current_status": "deferred"},
    ]
    for c in external_candidates:
        c.update({
            "known_version_info_required_later": True,
            "license_review_required_later": True,
            "update_tracking_required_later": True,
            "provider_abstraction_required": True,
            "model_profile_required_later": True,
            "not_selected_now": True,
            "not_invoked_now": True,
        })

    external_register = {
        "register_id": "external_open_source_candidate_register_v1",
        "candidates": external_candidates,
        "register_only": True,
        **meta,
    }

    reference_register = {
        "register_id": "reference_research_product_candidate_register_v1",
        "reference_not_dependency": True,
        "references": [
            "world_model_scene_prediction", "first_person_video_understanding", "embodied_agent_task_chain",
            "mcp_tool_protocol", "multimodal_memory_continuity", "scene_graph_spatial_map",
            "stcm_spatiotemporal_consistency", "ai_glasses_assistant_workflow",
        ],
        **meta,
    }

    self_dev_register = {
        "register_id": "self_developed_core_capability_register_v1",
        "capabilities": [
            "seed_core", "survival_drive", "emotion_engine_governance", "evolutionary_recursion_governance",
            "personal_continuity_module", "constitution_bus", "capability_bus_governance",
            "layered_capability_stack", "layered_governance_mapping", "information_integration_layer",
            "decision_center_governance", "stcm_governance", "memory_admission_governance",
        ],
        **meta,
    }

    module_contract = {
        "contract_id": "module_local_model_profile_contract_v1",
        "required_fields": list(MODULE_PROFILE_FIELDS),
        "no_direct_fact_action_output_default": True,
        **meta,
    }

    mid_binding = {
        "contract_id": "midplatform_model_governance_binding_contract_v1",
        "required_fields": list(MIDPLATFORM_BINDING_FIELDS),
        "layered_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layered_governance_ref": ADDENDUM_ID,
        "constitution_bus_ref": "luna_constitution_capability_bus_governance_v1",
        **meta,
    }

    io_contract = {
        "standard_id": "model_input_output_contract_standard_v1",
        "default_output": "candidate/evidence/signal/context",
        "forbidden": ["direct_fact", "direct_action", "direct_user_output", "direct_memory_write", "direct_runtime_enable"],
        **meta,
    }

    acceptance = {
        "criteria_id": "model_quality_acceptance_criteria_v1",
        "criteria": ["accuracy", "latency", "resource", "stability", "confidence_calibration", "candidate_compliance", "privacy", "safety"],
        **meta,
    }

    versioning = {
        "policy_id": "model_versioning_and_update_policy_v1",
        "fields": ["model_id", "model_version", "provider_version", "license_ref", "rollback_policy", "benchmark_revalidation_required"],
        **meta,
    }

    replacement = {
        "policy_id": "model_replacement_and_fallback_policy_v1",
        "no_auto_switch_without_policy": True,
        "hold_instead_of_fallback": True,
        **meta,
    }

    gap_matrix = {
        "matrix_id": "current_gap_and_next_action_matrix_v1",
        "entries": [
            {
                "capability_domain_id": did,
                "current_gap": domain_map[did]["current_gaps"][0] if domain_map[did]["current_gaps"] else "none",
                "severity": "high" if did in ("first_person_vision_scene_understanding", "ocr_text_recognition_reading") else "medium",
                "blocker_or_non_blocker": "non_blocker" if did != "asr_voice_input" else "blocker_for_voice_mainline",
                "next_action": domain_map[did]["next_actions"][0] if domain_map[did]["next_actions"] else "maintain",
                "recommended_phase": "controlled_runtime_readiness_planning" if "runtime" in str(domain_map[did]["next_actions"]) else NEXT_PHASE_GO,
                "dependency": domain_map[did]["current_goal_stage"],
                "priority": "P0" if did == "first_person_vision_scene_understanding" else "P1",
            }
            for did in CAPABILITY_DOMAIN_IDS
        ],
        **meta,
    }

    risk_register = {"register_id": "roadmap_risk_register_v1", "risks": list(ROADMAP_RISKS), **meta}

    dryrun_plan = {
        "plan_id": "roadmap_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "objectives": [
            "generate scenario_model_capability_roadmap_candidate",
            "verify each domain has goals/plan/completion/gaps/next_actions",
            "verify assets map to goal stages",
            "verify module profile + midplatform binding",
            "no model select/invoke/download",
        ],
        **meta,
    }

    planning_pass = input_ok
    planning_decision = {
        "decision_id": "scenario_model_capability_roadmap_inventory_planning_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "scenario_model_capability_roadmap_inventory_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "roadmap_and_inventory_only": True,
        **meta,
    }

    non_claims = {"register_id": "non_claims_register_v1", "non_claims": list(NON_CLAIMS), **meta}

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "closure_pending": closure_pending,
        "capability_domain_count": len(CAPABILITY_DOMAIN_IDS),
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "scenario_model_capability_roadmap_inventory_policy": policy,
        "upstream_output_chain_input_review": upstream_input,
        "luna_model_capability_roadmap": luna_roadmap,
        "capability_domain_inventory_matrix": domain_inventory,
        "current_model_asset_inventory": asset_inventory,
        "goal_stage_to_capability_domain_matrix": goal_domain_matrix,
        "capability_domain_roadmap_template": roadmap_template,
        "vision_scene_understanding_roadmap": vision_roadmap,
        "ocr_text_reading_roadmap": ocr_roadmap,
        "tts_voice_output_roadmap": tts_roadmap,
        "asr_voice_input_roadmap": asr_roadmap,
        "map_navigation_roadmap": map_roadmap,
        "spatiotemporal_world_continuity_roadmap": st_roadmap,
        "memory_personal_continuity_roadmap": memory_roadmap,
        "emotion_engine_roadmap": emotion_roadmap,
        "evolutionary_recursion_roadmap": evolution_roadmap,
        "provider_model_management_roadmap": provider_roadmap,
        "model_source_strategy_taxonomy": source_taxonomy,
        "external_open_source_candidate_register": external_register,
        "reference_research_product_candidate_register": reference_register,
        "self_developed_core_capability_register": self_dev_register,
        "module_local_model_profile_contract": module_contract,
        "midplatform_model_governance_binding_contract": mid_binding,
        "model_input_output_contract_standard": io_contract,
        "model_quality_acceptance_criteria": acceptance,
        "model_versioning_and_update_policy": versioning,
        "model_replacement_and_fallback_policy": replacement,
        "current_gap_and_next_action_matrix": gap_matrix,
        "roadmap_risk_register": risk_register,
        "roadmap_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "scenario_model_capability_roadmap_inventory_planning_decision": planning_decision,
        "summary": summary,
    }
