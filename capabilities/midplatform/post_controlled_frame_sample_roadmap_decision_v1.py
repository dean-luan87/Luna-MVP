# -*- coding: utf-8 -*-
"""Post Controlled Frame Sample Roadmap Decision v1.

本阶段只做路线裁决（roadmap decision / prioritization / boundary freeze）。
不读取真实图像/视频内容，不打开文件，不进入任何 runtime，不写入 WorldModel/Memory/Fact/Library。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001"
DECISION_SCOPE = "post_controlled_frame_sample_roadmap_decision_only"
SOURCE_CHAIN = "post_controlled_frame_sample_roadmap_decision_v1"
DECISION_ID = "pcfsrd_v1_001"

FINAL_DECISION = "POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION_READY_FOR_FILE_METADATA_BOUNDARY_PLANNING"
NEXT_PHASE = "Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001"

CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION = "CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_SAMPLE_POST_REVIEW_DECISION = "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
CONTROLLED_FRAME_SAMPLE_DRYRUN_DECISION = "CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
CONTROLLED_FRAME_SAMPLE_PLANNING_DECISION = "CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN"

POST_CROSSING_DECISION_ROADMAP_DECISION = "POST_CROSSING_DECISION_ROADMAP_DECISION_READY_FOR_CONTROLLED_FRAME_SAMPLE_PLANNING"
CROSSING_DECISION_CLOSURE_DECISION = "CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_INPUT_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "controlled_frame_sample_closure",
        "arg": "controlled_frame_sample_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_sample_closure_summary.json", "validated_capability_summary.json"],
    },
    {
        "id": "controlled_frame_sample_post_review",
        "arg": "controlled_frame_sample_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_sample_closure_readiness_decision.json", "verifier_report.json"],
    },
    {
        "id": "controlled_frame_sample_dryrun",
        "arg": "controlled_frame_sample_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_sample_dryrun_results.json", "verifier_report.json"],
    },
    {
        "id": "controlled_frame_sample_planning",
        "arg": "controlled_frame_sample_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_sample_planning_policy.json", "controlled_frame_sample_manifest_schema.json"],
    },
    {
        "id": "post_crossing_decision_roadmap_decision",
        "arg": "post_crossing_decision_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "crossing_decision_closure",
        "arg": "crossing_decision_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_input_closure",
        "arg": "controlled_frame_input_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "safety_constitution",
        "arg": "safety_constitution_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    # Optional roots (允许不存在，必须标记 optional_missing)
    {"id": "vision_frame_trace_stream_registry", "arg": "vision_frame_trace_stream_registry_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "vision_frame_input_governance", "arg": "vision_frame_input_governance_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "vision_roi_proposal_stub", "arg": "vision_roi_proposal_stub_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "system_health_hardware_profile", "arg": "system_health_hardware_profile_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "simulation_lab_profile", "arg": "simulation_lab_profile_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "privacy_governance_docs", "arg": "privacy_governance_docs_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
]


ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Controlled Frame File Existence / Metadata Boundary Planning",
        "route_type": "file_metadata_boundary_planning",
        "readiness_level": "high",
        "dependency": [
            "controlled frame sample manifest-level closure",
            "file existence check boundary definition",
            "external metadata boundary definition",
            "real hash strategy governance (policy only)",
            "fixture registry boundary",
        ],
        "risk_level": "medium",
        "expected_value": "very_high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "adds the missing 'file/metadata boundary layer' between manifest-only governance and any future guarded image read",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "B",
        "route_name": "Guarded Image Read Preplan",
        "route_type": "guarded_image_read_preplan",
        "readiness_level": "medium",
        "dependency": [
            "file existence / metadata boundary planning",
            "privacy manual review workflow",
            "guarded read allowlist/denylist design",
            "audit trace requirement",
        ],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "high",
        "write_risk": "low",
        "governance_debt_impact": "preplan only; must not claim real image read or runtime enablement",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "先补齐文件存在性/路径合法性/外部 metadata 边界与真实 hash 策略，再进入更高风险的 guarded image read preplan",
        "recommended_phase_name": "Phase-Guarded-Image-Read-Preplan-v1-001",
    },
    {
        "route_id": "C",
        "route_name": "Controlled Static Image Read Guarded Trial",
        "route_type": "guarded_trial_real_image_read",
        "readiness_level": "low",
        "dependency": [
            "guarded image read preplan",
            "fixture registry with review gate",
            "minimized runtime integration and abort/rollback",
        ],
        "risk_level": "very_high",
        "expected_value": "medium",
        "runtime_risk": "very_high",
        "write_risk": "medium",
        "governance_debt_impact": "high-risk; must remain deferred until all boundary layers are frozen",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "当前主线仍是 manifest-level governance；不满足受控真实图像读取试验的前置边界与审计要求",
        "recommended_phase_name": "Phase-Controlled-Static-Image-Read-Guarded-Trial-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "Gate Taxonomy / Gate Requirement Framework",
        "route_type": "project_optimization_governance",
        "readiness_level": "medium",
        "dependency": [
            "gate families inventory",
            "verifier template standardization",
            "allow/block/degrade/fallback standard",
        ],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "reduces gate sprawl; important project optimization but should not interrupt boundary layering",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "重要但属于项目优化；当前主线优先推进 file/metadata boundary layer",
        "recommended_phase_name": "Phase-Gate-Taxonomy-Gate-Requirement-Framework-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "MidPlatform Function Governance / Consolidation",
        "route_type": "governance_consolidation",
        "readiness_level": "medium",
        "dependency": [
            "governance debt carryover",
            "schema deduplication",
            "module registry consolidation",
        ],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "reduces duplicated governance modules",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "当前不插队；等 file/metadata boundary 规划落地后再收束中台治理债务",
        "recommended_phase_name": "Phase-MidPlatform-Function-Governance-Consolidation-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "MidPlatform Resilience / Robustness Preplan",
        "route_type": "resilience_preplan",
        "readiness_level": "medium",
        "dependency": [
            "midplatform topology review",
            "single point failure analysis",
            "degraded operation policy",
        ],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "low",
        "governance_debt_impact": "captures fragility topics without runtime changes",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "P1 轨道；不打断当前 mainline 的 file/metadata boundary 规划",
        "recommended_phase_name": "Phase-MidPlatform-Resilience-Robustness-Preplan-v1-001",
    },
    {
        "route_id": "G",
        "route_name": "Offline Distributed MidPlatform Architecture Preplan",
        "route_type": "future_architecture_preplan",
        "readiness_level": "low",
        "dependency": [
            "local-first constraints",
            "offline/weak-network mode policy",
            "distributed candidate sync policy",
        ],
        "risk_level": "medium",
        "expected_value": "strategic",
        "runtime_risk": "medium",
        "write_risk": "medium",
        "governance_debt_impact": "long-horizon architecture candidate",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "继续 deferred；等核心边界层完成后再开架构前置规划",
        "recommended_phase_name": "Phase-Offline-Distributed-MidPlatform-Architecture-Preplan-v1-001",
    },
    {
        "route_id": "H",
        "route_name": "Minimal Controlled Visual Runtime Planning",
        "route_type": "runtime_planning",
        "readiness_level": "low",
        "dependency": [
            "file existence / metadata boundary",
            "guarded image read preplan",
            "safety & privacy governance hardening",
        ],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "medium",
        "governance_debt_impact": "runtime planning is premature without file/metadata and guarded read boundaries",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "需先完成 file/metadata boundary + guarded read preplan，否则 runtime 规划会放大治理债务",
        "recommended_phase_name": "Phase-Minimal-Controlled-Visual-Runtime-Planning-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "WorldModel / Memory / Library Governance",
        "route_type": "future_governance_cluster",
        "readiness_level": "low",
        "dependency": [
            "entity resolution governance",
            "fact admission governance",
            "memory consolidation governance",
        ],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "must stay deferred to preserve no-write guarantees",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "当前主线保持 no-write；WML 治理继续 deferred",
        "recommended_phase_name": "Phase-WorldModel-Memory-Library-Governance-v1-001",
    },
    {
        "route_id": "J",
        "route_name": "Exploration Drive / Emotion Map / Affective Engine",
        "route_type": "future_affective_candidate",
        "readiness_level": "very_low",
        "dependency": [
            "grounded world information",
            "event chain maturity",
            "memory governance",
        ],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "high",
        "write_risk": "high",
        "governance_debt_impact": "long-horizon direction; must not enter mainline now",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "长期方向，P2 deferred；当前阶段仅路线裁决不进入实现",
        "recommended_phase_name": "Phase-Exploration-Drive-Emotion-Affective-Engine-v1-001",
    },
]


GATE_TAXONOMY_FUTURE_TOPICS = [
    "gate_type_taxonomy",
    "gate_level_definition",
    "gate_input_output_contract",
    "allow_block_degrade_fallback_standard",
    "veto_power_definition",
    "override_policy",
    "dependency_graph",
    "audit_trace_requirement",
    "failure_mode_requirement",
    "recovery_mode_requirement",
    "verifier_requirement_template",
    "safety_layering",
    "independent_safety_path",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root and root.is_dir() and all((root / name).is_file() for name in artifacts))
    return {"root": root, "loaded": loaded, "summary": _read_json(root / summary_file) if root and (root / summary_file).is_file() else {}}


def _boundary_payload() -> Dict[str, Any]:
    return {
        "decision_scope": DECISION_SCOPE,
        "roadmap_decision_only": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "real_file_hash_computed": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "crossing_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "entity_resolution_runtime_invoked": False,
        "fact_admission_runtime_invoked": False,
        "memory_consolidation_invoked": False,
        "library_experience_commit_invoked": False,
        "emotion_engine_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_post_controlled_frame_sample_roadmap_decision_v1(
    *,
    controlled_frame_sample_closure_root: str,
    controlled_frame_sample_post_review_root: str,
    controlled_frame_sample_dryrun_root: str,
    controlled_frame_sample_planning_root: str,
    post_crossing_decision_roadmap_decision_root: str,
    crossing_decision_closure_root: str,
    controlled_frame_input_closure_root: str,
    map_location_readonly_context_root: str,
    safety_constitution_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    vision_frame_trace_stream_registry_root: Optional[str] = None,
    vision_frame_input_governance_root: Optional[str] = None,
    vision_roi_proposal_stub_root: Optional[str] = None,
    system_health_hardware_profile_root: Optional[str] = None,
    simulation_lab_profile_root: Optional[str] = None,
    privacy_governance_docs_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows: List[Dict[str, Any]] = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    summaries = {key: roots[key]["summary"] for key in roots}
    closure_root = roots["controlled_frame_sample_closure"]["root"]
    closure_summary_payload = _read_json(closure_root / "controlled_frame_sample_closure_summary.json") if closure_root else {}
    closure_validated_payload = _read_json(closure_root / "validated_capability_summary.json") if closure_root else {}

    controlled_frame_sample_closure_input_loaded = (
        roots["controlled_frame_sample_closure"]["loaded"]
        and summaries["controlled_frame_sample_closure"].get("final_decision") == CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION
        and summaries["controlled_frame_sample_closure"].get("controlled_frame_sample_closed") is True
    )
    controlled_frame_sample_post_review_input_loaded = (
        roots["controlled_frame_sample_post_review"]["loaded"]
        and summaries["controlled_frame_sample_post_review"].get("final_decision") == CONTROLLED_FRAME_SAMPLE_POST_REVIEW_DECISION
    )
    controlled_frame_sample_dryrun_input_loaded = (
        roots["controlled_frame_sample_dryrun"]["loaded"]
        and summaries["controlled_frame_sample_dryrun"].get("final_decision") == CONTROLLED_FRAME_SAMPLE_DRYRUN_DECISION
    )
    controlled_frame_sample_planning_input_loaded = (
        roots["controlled_frame_sample_planning"]["loaded"]
        and summaries["controlled_frame_sample_planning"].get("final_decision") == CONTROLLED_FRAME_SAMPLE_PLANNING_DECISION
    )
    post_crossing_decision_roadmap_input_loaded = (
        roots["post_crossing_decision_roadmap_decision"]["loaded"]
        and summaries["post_crossing_decision_roadmap_decision"].get("final_decision") == POST_CROSSING_DECISION_ROADMAP_DECISION
    )
    crossing_decision_closure_input_loaded = (
        roots["crossing_decision_closure"]["loaded"]
        and summaries["crossing_decision_closure"].get("final_decision") == CROSSING_DECISION_CLOSURE_DECISION
    )
    controlled_frame_input_closure_input_loaded = (
        roots["controlled_frame_input_closure"]["loaded"]
        and summaries["controlled_frame_input_closure"].get("final_decision") == CONTROLLED_FRAME_INPUT_CLOSURE_DECISION
    )
    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_DECISION
    )
    safety_constitution_input_loaded = (
        roots["safety_constitution"]["loaded"] and summaries["safety_constitution"].get("final_decision") == SAFETY_CONSTITUTION_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = roots["ocr_final_closure"]["loaded"] and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION

    current_status_summary = {
        "current_mainline_status": "controlled_frame_sample_chain_closed_ready_for_next_roadmap_phase",
        "controlled_frame_sample_planning_closed": True,
        "controlled_frame_sample_dryrun_closed": True,
        "controlled_frame_sample_post_review_closed": True,
        "controlled_frame_sample_closed": True,
        "manifest_metadata_only": True,
        "real_image_readiness_claimed": False,
        "real_video_readiness_claimed": False,
        "visual_runtime_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "source_closure_ref": "_eval_out/controlled_frame_sample_closure_v1_smoke_v0/controlled_frame_sample_closure_summary.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    completed_capability_summary = {
        "capabilities": [
            {
                "capability_name": name,
                "completion_level": "policy_or_planning_or_dryrun_or_review_or_closure",
                "runtime_enabled": False,
                "production_ready": False,
                "validated_in_current_mainline": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for name in [
                "Controlled Frame Sample Planning v1",
                "Controlled Frame Sample DryRun v1",
                "Controlled Frame Sample Post-DryRun Review v1",
                "Controlled Frame Sample Closure v1",
                "Post Crossing Decision Roadmap Decision v1",
                "Crossing Decision Closure v1",
                "Controlled Frame Input Closure v1",
                "Map / Location Read-Only Context Policy v1",
                "Luna Safety Constitution Policy v1",
                "Minimal Runtime Integration Closure v1",
                "OCR Mainline Final Closure v1",
            ]
        ],
        "validated_capability_names_from_sample_closure": closure_validated_payload.get("capabilities", closure_validated_payload.get("validated_capabilities", [])),
        "source_closure_summary_payload": closure_summary_payload,
        "completed_capability_count": 11,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    route_rows = [{**route, "source_chain": SOURCE_CHAIN, **_not_fact()} for route in ROUTE_OPTIONS]
    route_option_matrix = {
        "routes": route_rows,
        "route_option_count": len(route_rows),
        "selected_route_id": "A",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    p0_routes = [r["route_name"] for r in ROUTE_OPTIONS if r["recommended_priority"] == "P0"]
    p1_routes = [r["route_name"] for r in ROUTE_OPTIONS if r["recommended_priority"] == "P1"]
    p2_routes = [r["route_name"] for r in ROUTE_OPTIONS if r["recommended_priority"] == "P2"]
    priority_ranking = {
        "P0": p0_routes,
        "P1": p1_routes,
        "P2": p2_routes,
        "p0_route_count": len(p0_routes),
        "p1_route_count": len(p1_routes),
        "p2_route_count": len(p2_routes),
        "selected_top_priority_route": "Controlled Frame File Existence / Metadata Boundary Planning",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_gate_taxonomy_register = {
        "gate_taxonomy_deferred": True,
        "current_status": "project_optimization_deferred",
        "runtime_allowed_now": False,
        "implementation_allowed_now": False,
        "recommended_priority": "P1",
        "selected_now": False,
        "required_future_topics": GATE_TAXONOMY_FUTURE_TOPICS,
        "defer_reason": "gate taxonomy is valuable but does not block file/metadata boundary layering",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_resilience_distributed_midplatform_register = {
        "midplatform_resilience_deferred": True,
        "offline_distributed_midplatform_deferred": True,
        "current_status": "future_architecture_candidate",
        "runtime_allowed_now": False,
        "direct_action_allowed": False,
        "selected_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_worldmodel_memory_library_emotion_register = {
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "exploration_drive_deferred": True,
        "emotion_engine_deferred": True,
        "deferred_items": [
            {
                "capability_name": "WorldModel Candidate Layer",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "selected_now": False,
                "defer_reason": "no-write mainline; entity resolution / fact admission governance not yet expanded",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Memory / Library Governance",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "selected_now": False,
                "defer_reason": "no-write mainline; memory consolidation and library experience governance remain deferred",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Exploration Drive",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "selected_now": False,
                "defer_reason": "future-only; do not enter runtime now",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Emotion Map / Affective Engine",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "selected_now": False,
                "defer_reason": "future-only; requires grounded world information and memory governance maturity",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_freeze = {
        "no_runtime": True,
        "no_write": True,
        "no_action": True,
        "no_speech": True,
        "no_fact": True,
        "no_live_camera": True,
        "no_image_read": True,
        "no_video_read": True,
        "no_file_open": True,
        "no_video_decode": True,
        "no_frame_extract": True,
        "no_real_hash": True,
        "no_visual_model": True,
        "no_map_api": True,
        "no_OCR_provider": True,
        "no_tracking_runtime": True,
        "no_crossing_runtime": True,
        "no_worldmodel_write": True,
        "no_memory_write": True,
        "no_library_write": True,
        "no_entity_resolution": True,
        "no_fact_admission": True,
        "no_emotion_engine": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_roadmap_register = {
        "carryover_topics": [
            {"topic": t, "roadmap_impact": "kept explicit during boundary layering", "source_chain": SOURCE_CHAIN, **_not_fact()}
            for t in [
                "file existence boundary missing",
                "path legality governance missing",
                "external metadata boundary missing",
                "real hash strategy governance missing",
                "fixture registry governance missing",
                "guarded image read preplan deferred",
                "gate taxonomy required later",
                "midplatform function governance required later",
                "midplatform resilience required later",
                "offline distributed architecture deferred",
            ]
        ],
        "gate_taxonomy_required_later": True,
        "midplatform_function_governance_required_later": True,
        "midplatform_resilience_required_later": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "non_claims": [
            "roadmap decision 不等于真实图像读取",
            "roadmap decision 不等于文件打开",
            "roadmap decision 不等于视频解码/抽帧",
            "roadmap decision 不等于真实 hash 计算",
            "roadmap decision 不等于视觉模型/OCR/tracking/map/crossing runtime",
            "roadmap decision 不等于生产推理/训练",
            "roadmap decision 不等于 WorldModel/Memory/Fact/Library 写入",
            "selected next phase 不等于允许 image read",
            "selected next phase 不等于 runtime enablement",
            "Gate Taxonomy 当前不进入实现",
            "MidPlatform governance 当前不插队实现",
        ],
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "runtime_enablement_claimed": False,
        "production_readiness_claimed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    recommended_next_phase_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": "_eval_out/controlled_frame_sample_closure_v1_smoke_v0/controlled_frame_sample_closure_summary.json",
        "current_mainline_status": current_status_summary["current_mainline_status"],
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": NEXT_PHASE,
        "rejected_or_deferred_routes": [r["route_name"] for r in ROUTE_OPTIONS if not r["selected_now"]],
        "decision_reason": [
            "Controlled Frame Sample 链已完成 manifest-level closure（planning+dryrun+post-review+closure）",
            "样例链仍然是 manifest-metadata-only，不等于真实图像/视频读取，也不等于视觉 runtime",
            "从 manifest 直接跳到 image read 会越过“文件是否存在、路径是否合法、外部 metadata 是否允许、真实 hash 策略”的中间层",
            "优先补齐 Controlled Frame File Existence / Metadata Boundary Planning：只做存在性与 metadata 边界，不读取图像内容",
            "Gate Taxonomy / MidPlatform governance / resilience / offline distributed 继续作为后续治理与架构候选，不插队实现",
        ],
        "boundary_freeze_ref": "boundary_freeze.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "priority_level": "P0",
        "route_name": "Controlled Frame File Existence / Metadata Boundary Planning",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for flag_name, flag_value in (
        ("controlled_frame_sample_closure_input_loaded", controlled_frame_sample_closure_input_loaded),
        ("controlled_frame_sample_post_review_input_loaded", controlled_frame_sample_post_review_input_loaded),
        ("controlled_frame_sample_dryrun_input_loaded", controlled_frame_sample_dryrun_input_loaded),
        ("controlled_frame_sample_planning_input_loaded", controlled_frame_sample_planning_input_loaded),
        ("post_crossing_decision_roadmap_input_loaded", post_crossing_decision_roadmap_input_loaded),
        ("crossing_decision_closure_input_loaded", crossing_decision_closure_input_loaded),
        ("controlled_frame_input_closure_input_loaded", controlled_frame_input_closure_input_loaded),
        ("map_location_readonly_context_input_loaded", map_location_readonly_context_input_loaded),
        ("safety_constitution_input_loaded", safety_constitution_input_loaded),
        ("minimal_runtime_integration_closure_loaded", minimal_runtime_integration_closure_loaded),
        ("ocr_final_closure_loaded", ocr_final_closure_loaded),
    ):
        if not flag_value:
            blockers.append(flag_name)

    route_names = {r["route_name"] for r in ROUTE_OPTIONS}
    selected_route = "Controlled Frame File Existence / Metadata Boundary Planning"

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "controlled_frame_sample_closure_input_loaded": controlled_frame_sample_closure_input_loaded,
        "controlled_frame_sample_post_review_input_loaded": controlled_frame_sample_post_review_input_loaded,
        "controlled_frame_sample_dryrun_input_loaded": controlled_frame_sample_dryrun_input_loaded,
        "controlled_frame_sample_planning_input_loaded": controlled_frame_sample_planning_input_loaded,
        "post_crossing_decision_roadmap_input_loaded": post_crossing_decision_roadmap_input_loaded,
        "crossing_decision_closure_input_loaded": crossing_decision_closure_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "current_status_summary_generated": True,
        "completed_capability_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "deferred_gate_taxonomy_register_generated": True,
        "deferred_resilience_distributed_midplatform_register_generated": True,
        "deferred_worldmodel_memory_library_emotion_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": len(ROUTE_OPTIONS),
        "p0_route_count": len(p0_routes),
        "p1_route_count": len(p1_routes),
        "p2_route_count": len(p2_routes),
        "controlled_frame_file_metadata_boundary_route_exists": "Controlled Frame File Existence / Metadata Boundary Planning" in route_names,
        "guarded_image_read_preplan_route_exists": "Guarded Image Read Preplan" in route_names,
        "controlled_static_image_read_guarded_trial_route_exists": "Controlled Static Image Read Guarded Trial" in route_names,
        "gate_taxonomy_route_exists": "Gate Taxonomy / Gate Requirement Framework" in route_names,
        "midplatform_function_governance_route_exists": "MidPlatform Function Governance / Consolidation" in route_names,
        "midplatform_resilience_route_exists": "MidPlatform Resilience / Robustness Preplan" in route_names,
        "offline_distributed_midplatform_route_exists": "Offline Distributed MidPlatform Architecture Preplan" in route_names,
        "minimal_controlled_visual_runtime_route_exists": "Minimal Controlled Visual Runtime Planning" in route_names,
        "worldmodel_memory_library_route_exists": "WorldModel / Memory / Library Governance" in route_names,
        "exploration_emotion_route_exists": "Exploration Drive / Emotion Map / Affective Engine" in route_names,
        "selected_route": selected_route,
        "controlled_frame_sample_closed": True,
        "manifest_metadata_only": True,
        "real_image_readiness_claimed": False,
        "real_video_readiness_claimed": False,
        "visual_runtime_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "gate_taxonomy_deferred": True,
        "gate_taxonomy_project_optimization": True,
        "midplatform_resilience_deferred": True,
        "offline_distributed_midplatform_deferred": True,
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "exploration_drive_deferred": True,
        "emotion_engine_deferred": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "real_file_hash_computed": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "crossing_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "emotion_engine_invoked": False,
        "boundary_ok": not blockers,
        "violations": blockers,
        "final_decision": FINAL_DECISION if not blockers else "POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_controlled_frame_sample_roadmap_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": current_status_summary["source_closure_ref"],
        "current_mainline_status": current_status_summary["current_mainline_status"],
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": summary["recommended_next_phase"],
        "rejected_or_deferred_routes": recommended_next_phase_decision["rejected_or_deferred_routes"],
        "decision_reason": recommended_next_phase_decision["decision_reason"],
        "boundary_freeze_ref": "boundary_freeze.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "post_controlled_frame_sample_roadmap_decision": post_controlled_frame_sample_roadmap_decision,
        "current_controlled_frame_sample_status_summary": current_status_summary,
        "completed_capability_summary": completed_capability_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "deferred_gate_taxonomy_register": deferred_gate_taxonomy_register,
        "deferred_resilience_distributed_midplatform_register": deferred_resilience_distributed_midplatform_register,
        "deferred_worldmodel_memory_library_emotion_register": deferred_worldmodel_memory_library_emotion_register,
        "boundary_freeze": boundary_freeze,
        "governance_debt_roadmap_register": governance_debt_roadmap_register,
        "non_claims_register": non_claims_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }

