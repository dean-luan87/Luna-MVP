# -*- coding: utf-8 -*-
"""Return To Vision Mainline Planning v1.

Phase-Return-To-Vision-Mainline-Planning-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Return-To-Vision-Mainline-Planning-v1-001"
PLANNING_ID = "rtvmp_v1_001"
FORMAL_MAINLINE_NAME = "Task-Aware Perception Orchestration"
FORMAL_MAINLINE_GOAL = (
    "Freeze Luna vision-strengthening mainline as a MidPlatform-orchestrated, "
    "candidate-only, reuse-first engineering roadmap without enabling runtime."
)
FINAL_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
NEXT_PHASE = "Phase-MidPlatform-Perception-Orchestration-Policy-v1-001"
SOURCE_CHAIN = "return_to_vision_mainline_planning_v1"

ROOT_INPUT_SPECS = [
    {
        "intake_id": "preplan_input",
        "path_arg": "preplan_input_root",
        "label": "Return-To-Vision Mainline Preplan v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "vision_mainline_capability_priority_plan.json",
            "proposed_next_phases.json",
            "vision_mainline_non_claims_register.json",
            "deferred_worldmodel_memory_library_boundary.json",
            "worldmodel_memory_library_placeholder_plan.json",
        ],
    },
    {
        "intake_id": "ocr_final_closure",
        "path_arg": "ocr_final_closure_root",
        "label": "OCR Mainline Final Closure v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "ocr_mainline_final_closure_report.json",
            "ocr_to_vision_handoff_plan.json",
        ],
    },
    {
        "intake_id": "minimal_runtime_integration_closure",
        "path_arg": "minimal_runtime_integration_closure_root",
        "label": "Minimal Runtime Integration Closure v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "minimal_runtime_integration_closure_report.json",
            "vision_mainline_handoff_plan.json",
        ],
    },
]

REQUIRED_DOCS = {
    "preplan_doc": "docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md",
    "ocr_final_closure_doc": "docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md",
    "minimal_runtime_integration_closure_doc": "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md",
    "ocr_phase_verdict_table": "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
}

OPTIONAL_DOCS = {
    "task_observation_request_contract": "docs/architecture/evaluation/LUNA_EVALUATION_TASK_OBSERVATION_REQUEST_CONTRACT_V1.md",
    "task_manager_contract": "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CONTRACT_V1.md",
    "midplatform_task_state_runtime_dryrun": "docs/architecture/evaluation/LUNA_EVALUATION_MIDPLATFORM_TASK_STATE_RUNTIME_DRYRUN_V1.md",
    "safety_task_arbitration_policy": "docs/architecture/midplatform/LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "stc_sampling_guidance_policy": "docs/architecture/midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md",
    "ocr_activation_governance_policy": "docs/architecture/midplatform/LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
    "static_readable_region_discovery": "docs/architecture/midplatform/LUNA_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md",
    "vision_frame_trace_stream_registry": "docs/architecture/vision/LUNA_VISION_FRAME_TRACE_STREAM_REGISTRY_V0.md",
    "vision_frame_input_governance": "docs/architecture/vision/LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md",
    "vision_roi_proposal_stub": "docs/architecture/vision/LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md",
    "vision_recognition_evidence_pack": "docs/architecture/vision/LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md",
    "worldmodel_unresolved_observation_slot_contract": "docs/architecture/evaluation/LUNA_EVALUATION_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md",
    "worldmodel_lookup_for_reading_framework": "docs/architecture/midplatform/LUNA_WORLDMODEL_LOOKUP_FOR_READING_FRAMEWORK_V1.md",
    "confirmed_text_evidence_memory_governance_contract": "docs/architecture/midplatform/LUNA_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md",
    "map_anchor": "docs/architecture/LUNA_MAP_ANCHOR_EVIDENCE_SCHEMA_V0.md",
    "system_health_center_governance": "docs/architecture/system_health/LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md",
    "hardware_profile_capability_registry": "docs/architecture/midplatform/LUNA_HARDWARE_PROFILE_CAPABILITY_REGISTRY_V1.md",
    "speech_gate_or_vop_reference": "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_OUTPUT_DEFINITION_V1.md",
}

BOUNDARY_FALSE_FLAGS = {
    "no_runtime_executed": True,
    "no_new_capability_implemented": True,
    "camera_invoked": False,
    "map_api_invoked": False,
    "ocr_provider_invoked": False,
    "tracking_runtime_invoked": False,
    "optical_flow_runtime_invoked": False,
    "world_model_written": False,
    "memory_written": False,
    "library_written": False,
    "fact_written": False,
    "scene_delta_generated": False,
    "task_state_committed_now": False,
    "navigation_action_triggered": False,
}

ADOPTED_PREPLAN_PRINCIPLES = [
    "视觉主线正式名称固定为 Task-Aware Perception Orchestration。",
    "Luna 不再采用 3×3 固定画面切割作为主线。",
    "Luna 不做 full-scene tracking，不追踪全部 moving objects。",
    "中台负责感知编排、资源预算、隐私过滤、冲突治理、信息修正、临时设施治理、World Observation handoff、Safety/Task/OCR/Map/Memory 融合。",
    "Safety Lane always-on，但只生成 candidate，不直接行动。",
    "Task Lane task-dependent，只处理中台批准的 focus slot。",
    "OCR only focus-triggered，不允许 full-frame OCR，不允许真实 provider runtime。",
    "地图 / 路线 / 位置 / 记忆只作为 context hint，不是事实，不是行动权威。",
    "视觉信息过期后仍可归档为 historical / worldmodel candidate，但不得作为当前行动依据。",
    "World Observation Layer 是后台低频世界观察候选层，不是实时行动模块，不直接写 WorldModel。",
    "WorldEntityFeatureCandidate 是长期认知世界基础，但当前只允许 candidate / handoff，不允许 fact write。",
    "Resource Budget 归中台，不归视觉模块。",
    "Privacy Filtering 归中台处理阶段，不在采集层粗暴阻断。",
    "Information Correction / Reality Mismatch 必须预留。",
    "Temporary / Mobile Social Facility 必须 TTL 化，不得写成固定 POI。",
    "Crossing Decision 需要未来独立 Safety Governance，不得混入普通导航视觉。",
    "Supervision / ByteTrack / OC-SORT / optical flow 只作为后续候选 adapter / evidence，不得当前接 runtime。",
    "WorldModel / Memory / Library 深层治理全部 deferred；当前视觉主线只生成 handoff candidate / placeholder，不执行 entity fusion / fact admission / memory consolidation / library experience governance。",
    "Reuse First, Extend Second, Create Last。优先复用，其次扩展，最后才新增。",
]

REJECTED_PATTERNS = [
    "3x3_grid_as_mainline",
    "full_scene_tracking",
    "full_frame_ocr",
    "map_or_memory_as_action_authority",
    "direct_worldmodel_memory_fact_write",
    "visual_private_resource_budget",
    "visual_private_privacy_filtering",
    "new_parallel_stc_ttl_source_chain",
    "new_parallel_evidence_pack",
    "new_parallel_task_state",
    "new_parallel_speech_gate_or_vop",
    "new_parallel_runtime_trial_or_closure_framework",
    "crossing_as_normal_navigation_visual_subtask",
    "crowd_flow_as_direct_navigation_instruction",
]

REUSE_COMMITMENTS = [
    "Task Observation Request Contract v1",
    "Task Manager / Task State",
    "Safety-Task Arbitration",
    "STC Sampling Guidance",
    "OCR Activation / OCRRequest / readable region / Evidence / TTL / source_chain",
    "Vision Frame / ROI / Evidence Pack",
    "WorldModel unresolved observation slot / lookup",
    "Memory governance",
    "MapAnchor",
    "System Health",
    "Hardware Profile / Resource Gate",
    "Minimal Runtime Integration patterns",
    "OCR Closure boundary patterns",
    "Speech Gate / VOP output boundary",
]

DUPLICATE_MODULE_BANS = [
    "new STC",
    "new TTL / freshness",
    "new source_chain",
    "new Evidence Pack",
    "new Memory write path",
    "new WorldModel write path",
    "new Fact write path",
    "new Task State",
    "new Speech Gate / VOP",
    "new Runtime Trial / Closure framework",
    "new standalone resource budget outside MidPlatform",
    "new standalone privacy filtering outside MidPlatform",
]

GOVERNANCE_BOUNDARY_MATRIX = {
    "camera_runtime_allowed": False,
    "ocr_provider_runtime_allowed": False,
    "tracking_runtime_allowed": False,
    "optical_flow_runtime_allowed": False,
    "map_api_allowed": False,
    "memory_write_allowed": False,
    "library_write_allowed": False,
    "worldmodel_write_allowed": False,
    "fact_write_allowed": False,
    "entity_fusion_runtime_allowed": False,
    "fact_admission_runtime_allowed": False,
    "scene_delta_allowed": False,
    "navigation_action_allowed": False,
    "task_commit_allowed": False,
    "full_frame_ocr_allowed": False,
    "full_scene_tracking_allowed": False,
}

FIRST_BATCH_PHASES = [
    {
        "phase": "Phase-MidPlatform-Perception-Orchestration-Policy-v1-001",
        "goal": "冻结中台感知编排总原则，定义 MidPlatformPerceptionWorkOrder、TaskPhasePerceptionPolicy、Safety Lane / Task Lane、ResourceBudget 中台归属、PrivacyFiltering 中台归属。",
        "phase_kind": "policy",
    },
    {
        "phase": "Phase-Task-Aware-Visual-Focus-Policy-v1-001",
        "goal": "定义 SceneSketchCandidate、VisualFocusPlan、VisualFocusSlot、ActiveViewAdjustmentCandidate、ViewQualityGate、VisualFocus lifecycle。",
        "phase_kind": "policy",
    },
    {
        "phase": "Phase-World-Observation-and-Entity-Feature-Policy-v1-001",
        "goal": "定义 World Observation Layer、WorldEntityFeatureCandidate、Object/Place/Event/Relation/Facility/TemporaryFacility 属性框架、WorldModel handoff candidate。",
        "phase_kind": "policy",
    },
    {
        "phase": "Phase-Selective-Tracking-Adapter-Policy-v1-001",
        "goal": "定义选择性追踪策略，限制 full-scene tracking，规划 road/pedestrian/vehicle/crowd flow tracking，评估 Supervision/ByteTrack/OC-SORT 仅为候选 adapter。",
        "phase_kind": "policy",
    },
    {
        "phase": "Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001",
        "goal": "用模拟任务验证视觉/OCR/地图/记忆/任务信息如何生成 TaskFeedbackCandidate / SafetyFeedbackCandidate。",
        "phase_kind": "dryrun",
    },
    {
        "phase": "Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001",
        "goal": "把视觉候选、OCR 候选、地图/任务上下文接入基础导航闭环 dry-run，仍不进入真实 runtime。",
        "phase_kind": "dryrun",
    },
]

DEFERRED_CAPABILITIES = [
    "real camera runtime",
    "real OCR provider",
    "real tracking runtime",
    "Supervision runtime integration",
    "ByteTrack / OC-SORT runtime",
    "optical flow runtime",
    "map API / 高德 API",
    "Entity Resolution runtime",
    "Object Identity Over Time runtime confirmation",
    "WorldModel Fact Admission",
    "WorldModel write",
    "WorldModel Query Runtime",
    "Memory Consolidation",
    "Memory write",
    "User Preference Fact Write",
    "Emotional Attachment Fact Write",
    "Library Experience Governance",
    "Experience Reuse Admission",
    "Long-term Route Experience Commit",
    "Social Facility Fact Commit",
    "Temporary Facility Long-term Promotion",
    "Fact write",
    "Scene Delta commit",
    "real TTS / audio",
    "face recognition",
    "voiceprint",
    "facial expression / audio emotion",
    "full background recording",
    "crossing action instruction",
]

FUTURE_RESEARCH_CANDIDATES = [
    "crossing decision safety governance",
    "world observation value filtering runtimeization",
    "household/private-space specialized governance dry-run",
    "object identity over time candidate review",
    "optical flow / motion evidence dry-run",
]

NON_CLAIMS = [
    "planning 不等于 runtime",
    "Task-Aware Perception Orchestration 不等于模型已接入",
    "Perception Work Order 不等于真实视觉调度已执行",
    "Scene Sketch 不等于环境事实",
    "VisualFocusPlan 不等于已经真实切割画面",
    "SelectiveTrackingPolicy 不等于追踪 runtime",
    "World Observation 不等于 WorldModel 写入",
    "WorldEntityFeatureCandidate 不等于实体事实",
    "TemporaryFacilityCandidate 不等于固定 POI",
    "CrowdFlowFollowingCandidate 不等于导航指令",
    "CrossingCandidate 不等于允许过马路",
    "Map / Memory hint 不等于现实事实",
    "OCR focus-triggered 不等于 OCR provider runtime",
    "text-only / candidate 输出不等于真实用户听见",
    "WorldModelHandoffCandidate 不等于已经写入 WorldModel",
    "MemoryHandoffCandidate 不等于已经写入 Memory",
    "LibraryHandoffPlaceholder 不等于图书馆经验已生效",
    "ObjectIdentityCandidate 不等于长期对象身份事实",
    "EmotionalAttachmentCandidate 不等于用户情感事实",
    "ExperienceCandidatePlaceholder 不等于经验已复用准入",
]

DEFERRED_WORLDMODEL_MEMORY_LIBRARY_BOUNDARY = {
    "boundary_scope": "deferred_worldmodel_memory_library_boundary",
    "current_vision_mainline_allowed": [
        "generate_visual_observation_candidate",
        "generate_world_observation_candidate",
        "generate_world_entity_feature_candidate",
        "generate_object_identity_candidate",
        "generate_temporary_facility_candidate",
        "generate_perception_correction_candidate",
        "generate_worldmodel_handoff_candidate",
        "generate_memory_handoff_candidate",
        "generate_library_handoff_placeholder",
    ],
    "current_vision_mainline_allowed_candidate_types": [
        "WorldObservationCandidate",
        "VisualObservationCandidate",
        "ExpiredVisualObservationCandidate",
        "WorldEntityFeatureCandidate",
        "ObjectIdentityCandidate",
        "TemporaryFacilityCandidate",
        "PerceptionCorrectionCandidate",
        "WorldModelHandoffCandidate",
        "MemoryHandoffCandidate",
        "LibraryHandoffPlaceholder",
        "ExperienceCandidatePlaceholder",
    ],
    "current_vision_mainline_forbidden": [
        "entity_resolution_runtime",
        "worldmodel_fact_admission",
        "worldmodel_write",
        "memory_write",
        "library_experience_commit",
        "object_identity_fact_commit",
        "emotional_attachment_fact_commit",
        "user_preference_fact_commit",
        "temporary_facility_long_term_promotion",
        "route_experience_commit",
    ],
    "deferred_to_future_phases": [
        "Memory Governance",
        "WorldModel Candidate Layer",
        "WorldModel Fact Admission",
        "Entity Resolution",
        "Library Experience Governance",
        "Experience Reuse Admission",
    ],
    "misuse_risks": [
        "视觉主线提前进入 WorldModel runtime",
        "WorldEntityFeatureCandidate 被误写成实体事实",
        "ObjectIdentityCandidate 被误写成长期对象身份",
        "EmotionalAttachmentCandidate 被误写成用户情感事实",
        "TemporaryFacilityCandidate 被误写成固定 POI",
        "WorldModelHandoffCandidate 被误认为已经写入 WorldModel",
        "MemoryHandoffCandidate 被误认为已经写入 Memory",
        "LibraryHandoffPlaceholder 被误认为图书馆经验已生效",
        "视觉主线吞掉未来 Memory / WorldModel / Library 专项职责",
    ],
    "entity_resolution_deferred": True,
    "fact_admission_deferred": True,
    "memory_consolidation_deferred": True,
    "library_experience_governance_deferred": True,
    "fact_write_allowed": False,
    "memory_write_allowed": False,
    "worldmodel_write_allowed": False,
    "library_write_allowed": False,
    "entity_fusion_runtime_allowed": False,
    "fact_admission_runtime_allowed": False,
    "handoff_candidate_not_fact": True,
    "placeholder_not_runtime": True,
}

WORLDMODEL_MEMORY_LIBRARY_PLACEHOLDER_PLAN = {
    "placeholder_scope": "worldmodel_memory_library_placeholder_plan",
    "handoff_candidates": [
        {
            "candidate_type": "WorldModelHandoffCandidate",
            "allowed_now": True,
            "runtime_write_allowed": False,
            "future_owner": "WorldModel Governance",
        },
        {
            "candidate_type": "MemoryHandoffCandidate",
            "allowed_now": True,
            "runtime_write_allowed": False,
            "future_owner": "Memory Governance",
        },
        {
            "candidate_type": "LibraryHandoffPlaceholder",
            "allowed_now": True,
            "runtime_write_allowed": False,
            "future_owner": "Library System",
        },
        {
            "candidate_type": "ExperienceCandidatePlaceholder",
            "allowed_now": True,
            "runtime_write_allowed": False,
            "future_owner": "Library / Experience Reuse Governance",
        },
    ],
    "required_fields_for_future_use": [
        "source_chain",
        "timestamp",
        "location_context_ref",
        "pose_or_view_context_ref",
        "task_context_ref",
        "freshness_status",
        "ttl_policy_ref",
        "confidence",
        "uncertainty",
        "privacy_tags",
        "conflict_refs",
        "user_feedback_refs",
        "ocr_refs",
        "visual_refs",
        "map_refs",
        "memory_refs",
    ],
    "non_claims": [
        "handoff_candidate_is_not_fact",
        "placeholder_is_not_runtime",
        "object_identity_candidate_is_not_identity_fact",
        "emotional_attachment_candidate_is_not_emotional_fact",
        "temporary_facility_candidate_is_not_fixed_poi",
        "route_experience_candidate_is_not_route_memory_commit",
    ],
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_root(path_str: Optional[str], summary_file: str) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root and root.is_dir())
    summary_path = root / summary_file if loaded else None
    summary_loaded = bool(summary_path and summary_path.is_file())
    return {
        "root": root,
        "loaded": loaded and summary_loaded,
        "summary_path": summary_path if summary_loaded else None,
    }


def _doc_row(repo_root: Path, intake_id: str, rel_path: str, required: bool) -> Dict[str, Any]:
    abs_path = repo_root / rel_path
    loaded = abs_path.is_file()
    return {
        "intake_id": intake_id,
        "label": intake_id,
        "path": rel_path,
        "loaded": loaded,
        "required": required,
        "status": "loaded" if loaded else ("missing_required" if required else "optional_missing"),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _boundary_payload() -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        **BOUNDARY_FALSE_FLAGS,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "fact_write_allowed": False,
        "entity_fusion_runtime_allowed": False,
        "fact_admission_runtime_allowed": False,
        "scene_delta_allowed": False,
        "navigation_action_allowed": False,
        "task_commit_allowed": False,
        "full_scene_tracking_allowed": False,
        "full_frame_ocr_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _load_optional_json(root_meta: Dict[str, Any], filename: str) -> Dict[str, Any]:
    root = root_meta.get("root")
    path = root / filename if root else None
    if path and path.is_file():
        return _read_json(path)
    return {}


def run_return_to_vision_mainline_planning_v1(
    *,
    preplan_input_root: str,
    ocr_final_closure_root: str,
    minimal_runtime_integration_closure_root: str,
    workspace_root: str,
) -> Dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[2]
    workspace = Path(workspace_root).expanduser().resolve()

    root_arg_values = {
        "preplan_input_root": preplan_input_root,
        "ocr_final_closure_root": ocr_final_closure_root,
        "minimal_runtime_integration_closure_root": minimal_runtime_integration_closure_root,
    }
    root_meta = {
        spec["intake_id"]: _load_root(root_arg_values[spec["path_arg"]], spec["summary_file"])
        for spec in ROOT_INPUT_SPECS
    }

    input_root_rows: List[Dict[str, Any]] = []
    for spec in ROOT_INPUT_SPECS:
        meta = root_meta[spec["intake_id"]]
        input_root_rows.append(
            {
                "intake_id": spec["intake_id"],
                "label": spec["label"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "summary_file": spec["summary_file"],
                "extra_artifacts": spec["extra_artifacts"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    for intake_id, rel_path in REQUIRED_DOCS.items():
        input_root_rows.append(_doc_row(repo_root, intake_id, rel_path, True))
    for intake_id, rel_path in OPTIONAL_DOCS.items():
        input_root_rows.append(_doc_row(repo_root, intake_id, rel_path, False))

    preplan_summary = _read_json(root_meta["preplan_input"]["summary_path"]) if root_meta["preplan_input"]["summary_path"] else {}
    ocr_summary = _read_json(root_meta["ocr_final_closure"]["summary_path"]) if root_meta["ocr_final_closure"]["summary_path"] else {}
    mri_summary = _read_json(root_meta["minimal_runtime_integration_closure"]["summary_path"]) if root_meta["minimal_runtime_integration_closure"]["summary_path"] else {}

    capability_plan = _load_optional_json(root_meta["preplan_input"], "vision_mainline_capability_priority_plan.json")
    preplan_next_phases = _load_optional_json(root_meta["preplan_input"], "proposed_next_phases.json")
    preplan_non_claims = _load_optional_json(root_meta["preplan_input"], "vision_mainline_non_claims_register.json")
    preplan_wml_boundary = _load_optional_json(root_meta["preplan_input"], "deferred_worldmodel_memory_library_boundary.json")
    preplan_wml_placeholder_plan = _load_optional_json(root_meta["preplan_input"], "worldmodel_memory_library_placeholder_plan.json")

    preplan_input_loaded = root_meta["preplan_input"]["loaded"] and preplan_summary.get("preplan_ready_for_formal_phase_decision") is True
    ocr_final_closure_loaded = root_meta["ocr_final_closure"]["loaded"] and ocr_summary.get("final_decision") == "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
    minimal_runtime_integration_closure_loaded = (
        root_meta["minimal_runtime_integration_closure"]["loaded"]
        and mri_summary.get("final_decision") == "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
    )

    adopted_preplan_principles = {
        "planning_id": PLANNING_ID,
        "principles": [
            {"principle_id": f"adopted_{idx:02d}", "statement": statement, "source": "return_to_vision_mainline_preplan_v1"}
            for idx, statement in enumerate(ADOPTED_PREPLAN_PRINCIPLES, start=1)
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rejected_patterns_register = {
        "planning_id": PLANNING_ID,
        "patterns": [
            {
                "pattern_id": f"rejected_{idx:02d}",
                "pattern": pattern,
                "rejected_for_mainline": True,
                "source": "formal_planning_freeze",
                **_not_fact(),
            }
            for idx, pattern in enumerate(REJECTED_PATTERNS, start=1)
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    midplatform_reuse_commitment = {
        "commitment_id": f"{PLANNING_ID}_reuse_commitment",
        "formal_commitment": "Reuse First, Extend Second, Create Last",
        "priority_reuse_assets": REUSE_COMMITMENTS,
        "resource_budget_owner": "MidPlatform",
        "privacy_filtering_owner": "MidPlatform",
        "crossing_future_owner": "Safety governance phase",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    duplicate_module_ban_list = {
        "ban_list_id": f"{PLANNING_ID}_duplicate_ban",
        "forbidden_parallel_systems": DUPLICATE_MODULE_BANS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_boundary_matrix = {
        "matrix_id": f"{PLANNING_ID}_boundary_matrix",
        **GOVERNANCE_BOUNDARY_MATRIX,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    first_batch_phase_definitions = {
        "definition_id": f"{PLANNING_ID}_first_batch_phases",
        "phases": [
            {
                **phase,
                "runtime_allowed_now": False,
                "fact_write_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for phase in FIRST_BATCH_PHASES
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_capability_register = {
        "register_id": f"{PLANNING_ID}_deferred_capabilities",
        "deferred_capabilities": [
            {
                "capability": item,
                "requires_separate_phase": True,
                "runtime_allowed_now": False,
                "fact_write_allowed": False,
                **_not_fact(),
            }
            for item in DEFERRED_CAPABILITIES
        ],
        "blocked_capabilities": [
            "real runtime shortcuts",
            "full-scene tracking",
            "full-frame OCR",
            "direct map API integration",
            "direct WorldModel/Memory/Fact write",
        ],
        "future_research_candidates": FUTURE_RESEARCH_CANDIDATES,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_worldmodel_memory_library_boundary = {
        "phase": PHASE_ID,
        **DEFERRED_WORLDMODEL_MEMORY_LIBRARY_BOUNDARY,
        "preplan_boundary_loaded": bool(preplan_wml_boundary.get("boundary_scope")),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    worldmodel_memory_library_placeholder_plan = {
        "phase": PHASE_ID,
        **WORLDMODEL_MEMORY_LIBRARY_PLACEHOLDER_PLAN,
        "preplan_placeholder_loaded": bool(preplan_wml_placeholder_plan.get("placeholder_scope")),
        "worldmodel_handoff_candidate_allowed": True,
        "memory_handoff_candidate_allowed": True,
        "library_handoff_placeholder_allowed": True,
        "experience_candidate_placeholder_allowed": True,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    vision_mainline_non_claims_register = {
        "register_id": f"{PLANNING_ID}_non_claims",
        "statements": NON_CLAIMS,
        "preplan_non_claims_loaded": bool(preplan_non_claims.get("non_claims")),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    roadmap_p0 = capability_plan.get("p0_capabilities") or []
    roadmap_p1 = capability_plan.get("p1_capabilities") or []
    roadmap_p2 = capability_plan.get("p2_capabilities") or []
    vision_mainline_roadmap = {
        "roadmap_id": f"{PLANNING_ID}_roadmap",
        "formal_mainline_name": FORMAL_MAINLINE_NAME,
        "formal_mainline_goal": FORMAL_MAINLINE_GOAL,
        "p0_capability_group": roadmap_p0,
        "p1_capability_group": roadmap_p1,
        "p2_capability_group": roadmap_p2,
        "first_batch_phases": [phase["phase"] for phase in FIRST_BATCH_PHASES],
        "deferred_capabilities": DEFERRED_CAPABILITIES,
        "blocked_capabilities": [
            "runtime camera / OCR provider / tracking / optical flow / map API",
            "direct WorldModel / Memory / Fact write",
            "scene delta commit",
            "crossing action instruction",
        ],
        "future_research_candidates": FUTURE_RESEARCH_CANDIDATES,
        "preplan_phase_sequence_ref": preplan_next_phases.get("phases", []),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    planning_report = {
        "planning_id": PLANNING_ID,
        "planning_scope": "return_to_vision_mainline_planning",
        "preplan_input_ref": str(root_meta["preplan_input"]["root"]) if root_meta["preplan_input"]["root"] else None,
        "adopted_principles": "adopted_preplan_principles.json",
        "rejected_patterns": "rejected_patterns_register.json",
        "formal_mainline_name": FORMAL_MAINLINE_NAME,
        "formal_mainline_goal": FORMAL_MAINLINE_GOAL,
        "phase_sequence": [phase["phase"] for phase in FIRST_BATCH_PHASES],
        "capability_priority_summary": {
            "p0_count": len(roadmap_p0),
            "p1_count": len(roadmap_p1),
            "p2_count": len(roadmap_p2),
        },
        "reuse_commitment_ref": "midplatform_reuse_commitment.json",
        "governance_boundary_ref": "governance_boundary_matrix.json",
        "first_batch_phase_definitions_ref": "first_batch_phase_definitions.json",
        "deferred_worldmodel_memory_library_boundary_ref": "deferred_worldmodel_memory_library_boundary.json",
        "worldmodel_memory_library_placeholder_plan_ref": "worldmodel_memory_library_placeholder_plan.json",
        "worldmodel_memory_library_boundary_deferred": True,
        "next_phase_recommendation": NEXT_PHASE,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    formal_readiness_gate = {
        "gate_id": f"{PLANNING_ID}_formal_readiness",
        "go_conditions": [
            "preplan loaded",
            "OCR closure loaded",
            "Minimal Runtime Integration closure loaded",
            "adopted principles generated",
            "roadmap generated",
            "reuse commitment generated",
            "duplicate ban list generated",
            "boundary matrix generated",
            "first batch phase definitions generated",
            "deferred capability register generated",
            "deferred worldmodel memory library boundary generated",
            "worldmodel memory library placeholder plan generated",
            "non-claims generated",
            "entity resolution deferred",
            "fact admission deferred",
            "memory consolidation deferred",
            "library experience governance deferred",
            "no runtime executed",
            "no write occurred",
            "next phase fixed",
        ],
        "no_go_conditions": [
            "preplan missing",
            "OCR closure missing",
            "Minimal Runtime Integration closure missing",
            "direct runtime recommendation",
            "full-scene tracking recommendation",
            "full-frame OCR recommendation",
            "direct map API recommendation",
            "direct WorldModel/Memory/Fact write recommendation",
            "entity resolution inside visual mainline recommendation",
            "fact admission inside visual mainline recommendation",
            "memory consolidation inside visual mainline recommendation",
            "library experience commit inside visual mainline recommendation",
            "duplicate STC/TTL/Evidence/Memory/Task/Speech/runtime framework recommendation",
            "missing next phase recommendation",
        ],
        "hard_checks": {
            "entity_resolution_deferred": True,
            "fact_admission_deferred": True,
            "memory_consolidation_deferred": True,
            "library_experience_governance_deferred": True,
            "worldmodel_write_allowed": False,
            "memory_write_allowed": False,
            "library_write_allowed": False,
            "entity_fusion_runtime_allowed": False,
            "fact_admission_runtime_allowed": False,
            "handoff_candidate_not_fact": True,
            "placeholder_not_runtime": True,
        },
        "go": (
            preplan_input_loaded
            and ocr_final_closure_loaded
            and minimal_runtime_integration_closure_loaded
        ),
        "next_phase_fixed": NEXT_PHASE,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommendation_id": f"{PLANNING_ID}_next_phase",
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    summary = {
        "phase": PHASE_ID,
        "planning_scope": "return_to_vision_mainline_planning_only",
        "preplan_input_loaded": preplan_input_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "formal_mainline_name": FORMAL_MAINLINE_NAME,
        "planning_report_generated": True,
        "roadmap_generated": True,
        "adopted_preplan_principles_generated": True,
        "rejected_patterns_register_generated": True,
        "midplatform_reuse_commitment_generated": True,
        "duplicate_module_ban_list_generated": True,
        "governance_boundary_matrix_generated": True,
        "first_batch_phase_definitions_generated": True,
        "deferred_capability_register_generated": True,
        "deferred_worldmodel_memory_library_boundary_generated": True,
        "worldmodel_memory_library_placeholder_plan_generated": True,
        "non_claims_register_generated": True,
        "formal_readiness_gate_generated": True,
        "worldmodel_memory_library_boundary_deferred": True,
        "entity_resolution_deferred": True,
        "fact_admission_deferred": True,
        "memory_consolidation_deferred": True,
        "library_experience_governance_deferred": True,
        "worldmodel_handoff_candidate_allowed": True,
        "memory_handoff_candidate_allowed": True,
        "library_handoff_placeholder_allowed": True,
        **BOUNDARY_FALSE_FLAGS,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "fact_write_allowed": False,
        "entity_fusion_runtime_allowed": False,
        "fact_admission_runtime_allowed": False,
        "scene_delta_allowed": False,
        "task_commit_allowed": False,
        "navigation_action_allowed": False,
        "full_scene_tracking_allowed": False,
        "full_frame_ocr_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "boundary_ok": True,
        "violations": [],
        "fact_status": "not_fact",
        "write_allowed": False,
        "final_decision": FINAL_DECISION,
        "recommended_next_phase": NEXT_PHASE,
    }

    return {
        "summary": summary,
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "vision_mainline_planning_report": planning_report,
        "vision_mainline_roadmap": vision_mainline_roadmap,
        "adopted_preplan_principles": adopted_preplan_principles,
        "rejected_patterns_register": rejected_patterns_register,
        "midplatform_reuse_commitment": midplatform_reuse_commitment,
        "duplicate_module_ban_list": duplicate_module_ban_list,
        "governance_boundary_matrix": governance_boundary_matrix,
        "first_batch_phase_definitions": first_batch_phase_definitions,
        "deferred_capability_register": deferred_capability_register,
        "deferred_worldmodel_memory_library_boundary": deferred_worldmodel_memory_library_boundary,
        "worldmodel_memory_library_placeholder_plan": worldmodel_memory_library_placeholder_plan,
        "vision_mainline_non_claims_register": vision_mainline_non_claims_register,
        "formal_readiness_gate": formal_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "workspace_root": str(workspace),
            "preplan_p0_count": len(roadmap_p0),
            "preplan_p1_count": len(roadmap_p1),
            "preplan_p2_count": len(roadmap_p2),
            "preplan_ready_flag": preplan_summary.get("preplan_ready_for_formal_phase_decision"),
            "ocr_final_decision": ocr_summary.get("final_decision"),
            "minimal_runtime_final_decision": mri_summary.get("final_decision"),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "recommended_next_phase": NEXT_PHASE,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
    }
