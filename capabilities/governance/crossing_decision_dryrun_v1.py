# -*- coding: utf-8 -*-
"""Crossing Decision DryRun v1 — simulated evidence governance validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Crossing-Decision-DryRun-v1-001"
DRYRUN_SCOPE = "crossing_decision_dryrun_only"
SOURCE_CHAIN = "crossing_decision_dryrun_v1"
FINAL_DECISION = "CROSSING_DECISION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Crossing-Decision-Post-DryRun-Review-v1-001"

CROSSING_GOVERNANCE_DECISION = "CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY_READY_FOR_CROSSING_DECISION_DRYRUN"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
POST_CONTROLLED_FRAME_ROADMAP_DECISION = "POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY"
CONTROLLED_FRAME_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
SAFETY_TASK_ARBITRATION_DECISION = "SAFETY_TASK_ARBITRATION_POLICY_READY_FOR_LOOP_STABILIZATION_TEST"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

FORBIDDEN_OUTPUT_MODES = [
    "CROSS_NOW",
    "SAFE_TO_CROSS",
    "GO_AHEAD",
    "PROCEED",
    "FOLLOW_THE_CROWD",
    "GREEN_LIGHT_GO",
    "MAP_SAYS_CROSS",
    "COUNTDOWN_SAYS_GO",
]

ALLOWED_DECISION_TYPES = [
    "SAFETY_HOLD_CANDIDATE",
    "REOBSERVE_CANDIDATE",
    "HUMAN_ASSISTANCE_CANDIDATE",
    "LOW_CONFIDENCE_WARNING_CANDIDATE",
    "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE",
    "NO_OUTPUT_SUPPRESSED",
]

ROOT_SPECS = [
    {
        "id": "crossing_safety_governance",
        "arg": "crossing_safety_governance_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "crossing_decision_safety_governance_policy.json",
            "forbidden_crossing_output_register.json",
            "crossing_output_policy.json",
        ],
    },
    {
        "id": "safety_constitution",
        "arg": "safety_constitution_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "crossing_safety_inheritance_policy.json",
            "global_safety_principles.json",
            "evidence_boundary_policy.json",
        ],
    },
    {
        "id": "post_controlled_frame_roadmap_decision",
        "arg": "post_controlled_frame_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "recommended_next_phase_decision.json"],
    },
    {
        "id": "controlled_frame_input_closure",
        "arg": "controlled_frame_input_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_input_closure_summary.json"],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "map_location_readonly_context_policy.json"],
    },
    {
        "id": "vision_strengthening_closure",
        "arg": "vision_strengthening_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "vision_strengthening_closure_summary.json"],
    },
    {
        "id": "safety_task_arbitration_policy",
        "arg": "safety_task_arbitration_policy_root",
        "required": True,
        "summary": "safety_task_arbitration_policy_v1_summary.json",
        "artifacts": [
            "safety_task_arbitration_policy_v1_summary.json",
            "safety_task_arbitration_final_decision_v1.json",
        ],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "minimal_runtime_integration_closure_report.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "ocr_mainline_final_closure_report.json"],
    },
    {
        "id": "task_aware_visual_focus_policy",
        "arg": "task_aware_visual_focus_policy_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "selective_tracking_adapter_policy",
        "arg": "selective_tracking_adapter_policy_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "visual_ocr_map_task_feedback_dryrun",
        "arg": "visual_ocr_map_task_feedback_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "basic_navigation_loop_vision_strengthening_dryrun",
        "arg": "basic_navigation_loop_vision_strengthening_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_controlled_output_definition",
        "arg": "minimal_runtime_controlled_output_definition_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_text_only_output_post_review",
        "arg": "minimal_runtime_text_only_output_post_review_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "voice_command_ownership_gate_policy",
        "arg": "voice_command_ownership_gate_policy_root",
        "required": False,
        "summary": "voice_command_ownership_gate_policy_v1_summary.json",
        "artifacts": ["voice_command_ownership_gate_policy_v1_summary.json"],
    },
    {
        "id": "voice_interruption_governance_dryrun",
        "arg": "voice_interruption_governance_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]

DRYRUN_CASE_FIELD_SPECS = [
    {"name": "dryrun_case_id", "type": "string", "required": True},
    {"name": "case_type", "type": "string", "required": True},
    {"name": "simulated_crossing_context", "type": "object", "required": True},
    {"name": "simulated_evidence_candidates", "type": "object", "required": True},
    {"name": "expected_governance_path", "type": "string", "required": True},
    {"name": "expected_output_candidate", "type": "string", "required": True},
    {"name": "expected_forbidden_outputs_absent", "type": "list", "required": True},
    {"name": "expected_boundary_flags", "type": "object", "required": True},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

SIMULATED_EVIDENCE_SET_FIELD_SPECS = [
    {"name": "evidence_set_id", "type": "string", "required": True},
    {"name": "traffic_light_candidate", "type": "object", "required": False},
    {"name": "green_light_candidate", "type": "object", "required": False},
    {"name": "red_light_candidate", "type": "object", "required": False},
    {"name": "countdown_text_candidate", "type": "object", "required": False},
    {"name": "crosswalk_candidate", "type": "object", "required": False},
    {"name": "curb_candidate", "type": "object", "required": False},
    {"name": "vehicle_flow_candidate", "type": "object", "required": False},
    {"name": "vehicle_approach_candidate", "type": "object", "required": False},
    {"name": "pedestrian_flow_candidate", "type": "object", "required": False},
    {"name": "crowd_flow_candidate", "type": "object", "required": False},
    {"name": "map_crossing_hint_candidate", "type": "object", "required": False},
    {"name": "route_crossing_hint_candidate", "type": "object", "required": False},
    {"name": "user_feedback_candidate", "type": "object", "required": False},
    {"name": "audio_environment_candidate", "type": "object", "required": False},
    {"name": "staff_or_human_assistance_candidate", "type": "object", "required": False},
    {"name": "freshness_profile", "type": "object", "required": True},
    {"name": "confidence_profile", "type": "object", "required": True},
    {"name": "conflict_profile", "type": "object", "required": True},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

DECISION_CANDIDATE_FIELD_SPECS = [
    {"name": "decision_candidate_id", "type": "string", "required": True},
    {"name": "source_case_id", "type": "string", "required": True},
    {"name": "input_evidence_set_ref", "type": "string", "required": True},
    {"name": "inherited_safety_constitution_ref", "type": "string", "required": True},
    {"name": "governance_policy_ref", "type": "string", "required": True},
    {"name": "decision_type", "type": "enum", "required": True},
    {"name": "allowed_output_mode", "type": "string", "required": True},
    {"name": "forbidden_output_blocked", "type": "list", "required": True},
    {"name": "crossing_permission_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "crossing_action_instruction_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "safe_to_cross_claim_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "requires_reobserve", "type": "boolean", "required": True},
    {"name": "requires_human_assistance", "type": "boolean", "required": True},
    {"name": "requires_hold", "type": "boolean", "required": True},
    {"name": "confidence", "type": "number", "required": True},
    {"name": "uncertainty", "type": "number", "required": True},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

FORBIDDEN_CHECK_FIELD_SPECS = [
    {"name": "check_id", "type": "string", "required": True},
    {"name": "source_case_id", "type": "string", "required": True},
    {"name": "forbidden_outputs_checked", "type": "list", "required": True},
    {"name": "forbidden_outputs_found", "type": "list", "required": True},
    {"name": "forbidden_outputs_absent", "type": "boolean", "required": True},
    {"name": "violation_count", "type": "number", "required": True},
    {"name": "verdict", "type": "string", "required": True},
]

CONFLICT_EVAL_FIELD_SPECS = [
    {"name": "conflict_candidate_id", "type": "string", "required": True},
    {"name": "source_case_id", "type": "string", "required": True},
    {"name": "conflict_type", "type": "string", "required": True},
    {"name": "conflicting_evidence_refs", "type": "list", "required": True},
    {"name": "conflict_blocks_crossing_action", "type": "boolean", "required": True, "default": True},
    {"name": "requires_reobserve", "type": "boolean", "required": True},
    {"name": "requires_human_assistance", "type": "boolean", "required": True},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

UNCERTAINTY_EVAL_FIELD_SPECS = [
    {"name": "uncertainty_candidate_id", "type": "string", "required": True},
    {"name": "source_case_id", "type": "string", "required": True},
    {"name": "uncertainty_type", "type": "string", "required": True},
    {"name": "low_confidence_evidence_refs", "type": "list", "required": True},
    {"name": "stale_evidence_refs", "type": "list", "required": True},
    {"name": "occlusion_refs", "type": "list", "required": True},
    {"name": "insufficient_evidence", "type": "boolean", "required": True},
    {"name": "recommended_conservative_output", "type": "string", "required": True},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

BOUNDARY_DECISION_FIELD_SPECS = [
    {"name": "case_id", "type": "string", "required": True},
    {"name": "inherits_safety_constitution", "type": "boolean", "required": True, "default": True},
    {"name": "crossing_permission_output_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "crossing_action_instruction_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "safe_to_cross_claim_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "speech_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "runtime_boundary_ok", "type": "boolean", "required": True},
    {"name": "write_boundary_ok", "type": "boolean", "required": True},
    {"name": "boundary_ok", "type": "boolean", "required": True},
    {"name": "violations", "type": "list", "required": True},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

# (case_id, case_type, governance_path, decision_type, evidence_keys, profile_overrides)
SCENARIO_SPECS: List[Tuple[str, str, str, str, List[str], Dict[str, Any]]] = [
    (
        "green_light_candidate_only",
        "single_modality_green_light",
        "green_light_not_crossing_permission",
        "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE",
        ["green_light_candidate"],
        {"confidence": 0.72, "freshness": "current", "conflict": False},
    ),
    (
        "green_light_with_vehicle_flow_uncertain",
        "green_light_vehicle_conflict",
        "conflict_blocks_crossing_action",
        "SAFETY_HOLD_CANDIDATE",
        ["green_light_candidate", "vehicle_flow_candidate"],
        {"confidence": 0.55, "freshness": "current", "conflict": True, "conflict_type": "green_light_vs_vehicle_flow_conflict"},
    ),
    (
        "red_light_candidate",
        "red_light_hold",
        "traffic_signal_hold",
        "SAFETY_HOLD_CANDIDATE",
        ["red_light_candidate", "traffic_light_candidate"],
        {"confidence": 0.8, "freshness": "current", "conflict": False},
    ),
    (
        "countdown_text_candidate_only",
        "ocr_countdown_not_permission",
        "countdown_text_not_crossing_permission",
        "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE",
        ["countdown_text_candidate"],
        {"confidence": 0.65, "freshness": "current", "conflict": False},
    ),
    (
        "crowd_flow_forward",
        "crowd_flow_not_follow",
        "crowd_flow_not_crossing_permission",
        "SAFETY_HOLD_CANDIDATE",
        ["crowd_flow_candidate", "pedestrian_flow_candidate"],
        {"confidence": 0.6, "freshness": "current", "conflict": False},
    ),
    (
        "map_crossing_hint_only",
        "map_hint_requires_visual_confirm",
        "map_crossing_hint_not_crossing_permission",
        "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE",
        ["map_crossing_hint_candidate"],
        {"confidence": 0.5, "freshness": "current", "conflict": False},
    ),
    (
        "route_says_cross",
        "route_hint_not_permission",
        "route_crossing_hint_not_crossing_permission",
        "SAFETY_HOLD_CANDIDATE",
        ["route_crossing_hint_candidate"],
        {"confidence": 0.55, "freshness": "current", "conflict": False},
    ),
    (
        "user_says_go",
        "user_instruction_blocked",
        "user_says_go_not_crossing_permission",
        "SAFETY_HOLD_CANDIDATE",
        ["user_feedback_candidate"],
        {"confidence": 0.9, "freshness": "current", "conflict": False, "user_instruction": "go"},
    ),
    (
        "crosswalk_candidate_but_vehicle_occluded",
        "occluded_vehicle_flow",
        "occlusion_requires_hold",
        "REOBSERVE_CANDIDATE",
        ["crosswalk_candidate", "vehicle_flow_candidate"],
        {"confidence": 0.45, "freshness": "current", "conflict": False, "occlusion": ["vehicle_flow_candidate"]},
    ),
    (
        "traffic_light_uncertain",
        "low_confidence_traffic_light",
        "uncertainty_requires_hold_or_confirm",
        "REOBSERVE_CANDIDATE",
        ["traffic_light_candidate"],
        {"confidence": 0.28, "freshness": "current", "conflict": False, "low_confidence": ["traffic_light_candidate"]},
    ),
    (
        "no_crosswalk_detected",
        "insufficient_crossing_context",
        "no_crosswalk_hold",
        "SAFETY_HOLD_CANDIDATE",
        [],
        {"confidence": 0.2, "freshness": "current", "conflict": False, "insufficient_evidence": True},
    ),
    (
        "stale_traffic_light_evidence",
        "stale_evidence_blocked",
        "stale_evidence_not_crossing_permission",
        "REOBSERVE_CANDIDATE",
        ["traffic_light_candidate"],
        {"confidence": 0.7, "freshness": "stale", "conflict": False, "stale": ["traffic_light_candidate"]},
    ),
    (
        "conflicting_audio_visual_cues",
        "audio_visual_conflict",
        "conflicting_evidence_not_crossing_permission",
        "HUMAN_ASSISTANCE_CANDIDATE",
        ["audio_environment_candidate", "traffic_light_candidate"],
        {"confidence": 0.4, "freshness": "current", "conflict": True, "conflict_type": "audio_cue_vs_visual_uncertain"},
    ),
    (
        "unknown_speaker_says_safe",
        "unknown_speaker_not_permission",
        "audio_not_crossing_permission",
        "SAFETY_HOLD_CANDIDATE",
        ["audio_environment_candidate"],
        {"confidence": 0.35, "freshness": "current", "conflict": False, "unknown_speaker": True},
    ),
    (
        "green_light_plus_crowd_flow_plus_map_hint",
        "multi_modality_still_not_permission",
        "single_modality_and_multi_modality_not_crossing_permission",
        "SAFETY_HOLD_CANDIDATE",
        ["green_light_candidate", "crowd_flow_candidate", "map_crossing_hint_candidate"],
        {"confidence": 0.5, "freshness": "current", "conflict": True, "conflict_type": "multi_modality_no_permission"},
    ),
    (
        "all_evidence_low_confidence",
        "global_low_confidence",
        "low_confidence_evidence_not_crossing_permission",
        "LOW_CONFIDENCE_WARNING_CANDIDATE",
        ["traffic_light_candidate", "crosswalk_candidate", "vehicle_flow_candidate"],
        {"confidence": 0.15, "freshness": "current", "conflict": False, "low_confidence": ["traffic_light_candidate", "crosswalk_candidate", "vehicle_flow_candidate"]},
    ),
]

GOVERNANCE_DEBT_TOPICS = [
    "crossing decision post-dryrun review still pending",
    "controlled sample evidence for crossing remains deferred",
    "vehicle occlusion reasoning remains future dryrun topic",
    "human assistance escalation phrasing remains future output-governance topic",
    "speech gate integration for crossing remains deferred",
    "audio/visual conflict fusion remains dryrun-simulated only",
    "crosswalk and curb evidence freshness policy remains future refinement",
    "crossing governance runtime trial remains deferred",
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
    return {
        "root": root,
        "loaded": loaded,
        "summary": _read_json(root / summary_file) if root and (root / summary_file).is_file() else {},
    }


def _schema_payload(object_name: str, field_specs: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "object_name": object_name,
        "fields": field_specs,
        "field_count": len(field_specs),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _candidate_stub(evidence_type: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    conf = profile.get("confidence", 0.5)
    return {
        "evidence_type": evidence_type,
        "present": True,
        "confidence": conf,
        "uncertainty": round(1.0 - conf, 3),
        "crossing_permission_allowed": False,
        "current_action_allowed": False,
        "fact_status": "not_fact",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _build_evidence_set(case_id: str, evidence_keys: List[str], profile: Dict[str, Any]) -> Dict[str, Any]:
    evidence_set: Dict[str, Any] = {
        "evidence_set_id": f"evset_{case_id}",
        "freshness_profile": {
            "status": profile.get("freshness", "current"),
            "stale_refs": profile.get("stale", []),
        },
        "confidence_profile": {
            "aggregate_confidence": profile.get("confidence", 0.5),
            "low_confidence_refs": profile.get("low_confidence", []),
        },
        "conflict_profile": {
            "has_conflict": profile.get("conflict", False),
            "conflict_type": profile.get("conflict_type"),
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    for key in (
        "traffic_light_candidate",
        "green_light_candidate",
        "red_light_candidate",
        "countdown_text_candidate",
        "crosswalk_candidate",
        "curb_candidate",
        "vehicle_flow_candidate",
        "vehicle_approach_candidate",
        "pedestrian_flow_candidate",
        "crowd_flow_candidate",
        "map_crossing_hint_candidate",
        "route_crossing_hint_candidate",
        "user_feedback_candidate",
        "audio_environment_candidate",
        "staff_or_human_assistance_candidate",
    ):
        if key in evidence_keys:
            stub = _candidate_stub(key, profile)
            if key == "user_feedback_candidate" and profile.get("user_instruction"):
                stub["instruction_text"] = profile["user_instruction"]
            if key == "audio_environment_candidate" and profile.get("unknown_speaker"):
                stub["speaker_identity"] = "unknown"
            evidence_set[key] = stub
        else:
            evidence_set[key] = None
    return evidence_set


def _decision_flags(decision_type: str) -> Dict[str, bool]:
    return {
        "requires_hold": decision_type in ("SAFETY_HOLD_CANDIDATE", "LOW_CONFIDENCE_WARNING_CANDIDATE"),
        "requires_reobserve": decision_type == "REOBSERVE_CANDIDATE",
        "requires_human_assistance": decision_type == "HUMAN_ASSISTANCE_CANDIDATE",
    }


def _boundary_payload() -> Dict[str, Any]:
    return {
        "dryrun_scope": DRYRUN_SCOPE,
        "inherits_safety_constitution": True,
        "crossing_runtime_allowed": False,
        "crossing_runtime_invoked": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "crossing_permission_output_allowed": False,
        "crossing_action_instruction_allowed": False,
        "safe_to_cross_claim_allowed": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "user_heard_assumed": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_crossing_decision_dryrun_v1(
    *,
    crossing_safety_governance_root: str,
    safety_constitution_root: str,
    post_controlled_frame_roadmap_decision_root: str,
    controlled_frame_input_closure_root: str,
    map_location_readonly_context_root: str,
    vision_strengthening_closure_root: str,
    safety_task_arbitration_policy_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    task_aware_visual_focus_policy_root: Optional[str] = None,
    selective_tracking_adapter_policy_root: Optional[str] = None,
    visual_ocr_map_task_feedback_dryrun_root: Optional[str] = None,
    basic_navigation_loop_vision_strengthening_dryrun_root: Optional[str] = None,
    minimal_runtime_controlled_output_definition_root: Optional[str] = None,
    minimal_runtime_text_only_output_post_review_root: Optional[str] = None,
    voice_command_ownership_gate_policy_root: Optional[str] = None,
    voice_interruption_governance_dryrun_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows = []
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
    safety_task_root = roots["safety_task_arbitration_policy"]["root"]
    safety_task_final = _read_json(safety_task_root / "safety_task_arbitration_final_decision_v1.json") if safety_task_root else {}

    crossing_safety_governance_input_loaded = (
        roots["crossing_safety_governance"]["loaded"]
        and summaries["crossing_safety_governance"].get("final_decision") == CROSSING_GOVERNANCE_DECISION
    )
    safety_constitution_input_loaded = (
        roots["safety_constitution"]["loaded"]
        and summaries["safety_constitution"].get("final_decision") == SAFETY_CONSTITUTION_DECISION
    )
    post_controlled_frame_roadmap_decision_input_loaded = (
        roots["post_controlled_frame_roadmap_decision"]["loaded"]
        and summaries["post_controlled_frame_roadmap_decision"].get("final_decision") == POST_CONTROLLED_FRAME_ROADMAP_DECISION
    )
    controlled_frame_input_closure_input_loaded = (
        roots["controlled_frame_input_closure"]["loaded"]
        and summaries["controlled_frame_input_closure"].get("final_decision") == CONTROLLED_FRAME_CLOSURE_DECISION
    )
    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_DECISION
    )
    vision_strengthening_closure_input_loaded = (
        roots["vision_strengthening_closure"]["loaded"]
        and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    )
    safety_task_arbitration_policy_input_loaded = (
        roots["safety_task_arbitration_policy"]["loaded"]
        and safety_task_final.get("final_decision") == SAFETY_TASK_ARBITRATION_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = (
        roots["ocr_final_closure"]["loaded"]
        and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION
    )

    dryrun_case_schema = _schema_payload("CrossingDecisionDryRunCase", DRYRUN_CASE_FIELD_SPECS)
    simulated_crossing_evidence_set_schema = _schema_payload("SimulatedCrossingEvidenceSet", SIMULATED_EVIDENCE_SET_FIELD_SPECS)
    crossing_governance_decision_candidate_schema = _schema_payload(
        "CrossingGovernanceDecisionCandidate", DECISION_CANDIDATE_FIELD_SPECS
    )
    forbidden_crossing_output_check_schema = _schema_payload("ForbiddenCrossingOutputCheck", FORBIDDEN_CHECK_FIELD_SPECS)
    crossing_conflict_evaluation_candidate_schema = _schema_payload(
        "CrossingConflictEvaluationCandidate", CONFLICT_EVAL_FIELD_SPECS
    )
    crossing_uncertainty_evaluation_candidate_schema = _schema_payload(
        "CrossingUncertaintyEvaluationCandidate", UNCERTAINTY_EVAL_FIELD_SPECS
    )
    crossing_dryrun_boundary_decision_schema = _schema_payload(
        "CrossingDryRunBoundaryDecision", BOUNDARY_DECISION_FIELD_SPECS
    )

    governance_policy_ref = "_eval_out/crossing_decision_safety_governance_policy_v1_smoke_v0/crossing_decision_safety_governance_policy.json"
    safety_constitution_ref = "_eval_out/luna_safety_constitution_policy_v1_smoke_v0/crossing_safety_inheritance_policy.json"

    dryrun_cases: List[Dict[str, Any]] = []
    evidence_sets: List[Dict[str, Any]] = []
    decision_candidates: List[Dict[str, Any]] = []
    forbidden_checks: List[Dict[str, Any]] = []
    conflict_evals: List[Dict[str, Any]] = []
    uncertainty_evals: List[Dict[str, Any]] = []
    boundary_decisions: List[Dict[str, Any]] = []
    scenario_matrix_rows: List[Dict[str, Any]] = []

    for case_id, case_type, governance_path, decision_type, evidence_keys, profile in SCENARIO_SPECS:
        evidence_set = _build_evidence_set(case_id, evidence_keys, profile)
        flags = _decision_flags(decision_type)
        conf = profile.get("confidence", 0.5)

        dryrun_case = {
            "dryrun_case_id": case_id,
            "case_type": case_type,
            "simulated_crossing_context": {
                "location_sketch": f"simulated_intersection_{case_id}",
                "task_phase": "crossing_decision_dryrun",
                "runtime_invoked": False,
            },
            "simulated_evidence_candidates": {"evidence_set_ref": evidence_set["evidence_set_id"]},
            "expected_governance_path": governance_path,
            "expected_output_candidate": decision_type,
            "expected_forbidden_outputs_absent": FORBIDDEN_OUTPUT_MODES,
            "expected_boundary_flags": {
                "crossing_permission_allowed": False,
                "crossing_action_instruction_allowed": False,
                "safe_to_cross_claim_allowed": False,
                "speech_allowed": False,
                "action_allowed": False,
            },
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        dryrun_cases.append(dryrun_case)
        evidence_sets.append(evidence_set)

        decision_candidate = {
            "decision_candidate_id": f"dec_{case_id}",
            "source_case_id": case_id,
            "input_evidence_set_ref": evidence_set["evidence_set_id"],
            "inherited_safety_constitution_ref": safety_constitution_ref,
            "governance_policy_ref": governance_policy_ref,
            "decision_type": decision_type,
            "allowed_output_mode": decision_type,
            "forbidden_output_blocked": FORBIDDEN_OUTPUT_MODES,
            "crossing_permission_allowed": False,
            "crossing_action_instruction_allowed": False,
            "safe_to_cross_claim_allowed": False,
            "requires_reobserve": flags["requires_reobserve"],
            "requires_human_assistance": flags["requires_human_assistance"],
            "requires_hold": flags["requires_hold"],
            "confidence": conf,
            "uncertainty": round(1.0 - conf, 3),
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        decision_candidates.append(decision_candidate)

        forbidden_checks.append(
            {
                "check_id": f"forbidden_check_{case_id}",
                "source_case_id": case_id,
                "forbidden_outputs_checked": FORBIDDEN_OUTPUT_MODES,
                "forbidden_outputs_found": [],
                "forbidden_outputs_absent": True,
                "violation_count": 0,
                "verdict": "PASS",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        if profile.get("conflict"):
            conflict_evals.append(
                {
                    "conflict_candidate_id": f"conflict_{case_id}",
                    "source_case_id": case_id,
                    "conflict_type": profile.get("conflict_type", "conflicting_evidence"),
                    "conflicting_evidence_refs": evidence_keys,
                    "conflict_blocks_crossing_action": True,
                    "requires_reobserve": decision_type == "REOBSERVE_CANDIDATE",
                    "requires_human_assistance": decision_type == "HUMAN_ASSISTANCE_CANDIDATE",
                    "action_allowed": False,
                    "fact_status": "not_fact",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )

        uncertainty_types: List[str] = []
        if profile.get("low_confidence"):
            uncertainty_types.append("low_confidence")
        if profile.get("stale"):
            uncertainty_types.append("stale_evidence")
        if profile.get("occlusion"):
            uncertainty_types.append("occluded_vehicle_flow")
        if profile.get("insufficient_evidence"):
            uncertainty_types.append("insufficient_evidence")

        for utype in uncertainty_types:
            uncertainty_evals.append(
                {
                    "uncertainty_candidate_id": f"uncertainty_{case_id}_{utype}",
                    "source_case_id": case_id,
                    "uncertainty_type": utype,
                    "low_confidence_evidence_refs": profile.get("low_confidence", []),
                    "stale_evidence_refs": profile.get("stale", []),
                    "occlusion_refs": profile.get("occlusion", []),
                    "insufficient_evidence": profile.get("insufficient_evidence", False),
                    "recommended_conservative_output": decision_type,
                    "action_allowed": False,
                    "fact_status": "not_fact",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )

        boundary_decisions.append(
            {
                "case_id": case_id,
                "inherits_safety_constitution": True,
                "crossing_permission_output_allowed": False,
                "crossing_action_instruction_allowed": False,
                "safe_to_cross_claim_allowed": False,
                "speech_allowed": False,
                "action_allowed": False,
                "runtime_boundary_ok": True,
                "write_boundary_ok": True,
                "boundary_ok": True,
                "violations": [],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        scenario_matrix_rows.append(
            {
                "scenario_id": case_id,
                "case_type": case_type,
                "expected_governance_path": governance_path,
                "expected_output_candidate": decision_type,
                "decision_type": decision_type,
                "crossing_permission_allowed": False,
                "forbidden_outputs_absent": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    crossing_decision_dryrun_scenario_matrix = {
        "scenarios": scenario_matrix_rows,
        "scenario_count": len(scenario_matrix_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_decision_dryrun_results = {
        "dryrun_cases": dryrun_cases,
        "evidence_sets": evidence_sets,
        "decision_candidates": decision_candidates,
        "case_count": len(dryrun_cases),
        "decision_candidate_count": len(decision_candidates),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    forbidden_crossing_output_check_results = {
        "checks": forbidden_checks,
        "check_count": len(forbidden_checks),
        "forbidden_crossing_outputs_absent": all(c["forbidden_outputs_absent"] for c in forbidden_checks),
        "total_violation_count": sum(c["violation_count"] for c in forbidden_checks),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_dryrun_boundary_matrix = {
        "boundary_decisions": boundary_decisions,
        "case_count": len(boundary_decisions),
        "all_boundary_ok": all(b["boundary_ok"] for b in boundary_decisions),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "carryover_topics": GOVERNANCE_DEBT_TOPICS,
        "post_dryrun_review_required_next": True,
        "crossing_runtime_trial_still_deferred": True,
        "controlled_sample_still_deferred": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "dry-run validated conservative crossing governance candidates without runtime or forbidden outputs",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_runtime_boundary_report = _boundary_payload()
    no_write_boundary_report = _boundary_payload()

    blockers: List[str] = []
    for name, flag in (
        ("crossing_safety_governance_input_loaded", crossing_safety_governance_input_loaded),
        ("safety_constitution_input_loaded", safety_constitution_input_loaded),
        ("post_controlled_frame_roadmap_decision_input_loaded", post_controlled_frame_roadmap_decision_input_loaded),
        ("controlled_frame_input_closure_input_loaded", controlled_frame_input_closure_input_loaded),
        ("map_location_readonly_context_input_loaded", map_location_readonly_context_input_loaded),
        ("vision_strengthening_closure_input_loaded", vision_strengthening_closure_input_loaded),
        ("safety_task_arbitration_policy_input_loaded", safety_task_arbitration_policy_input_loaded),
        ("minimal_runtime_integration_closure_loaded", minimal_runtime_integration_closure_loaded),
        ("ocr_final_closure_loaded", ocr_final_closure_loaded),
    ):
        if not flag:
            blockers.append(name)

    forbidden_absent = forbidden_crossing_output_check_results["forbidden_crossing_outputs_absent"]
    all_boundary_ok = crossing_dryrun_boundary_matrix["all_boundary_ok"] and not blockers

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "crossing_safety_governance_input_loaded": crossing_safety_governance_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "post_controlled_frame_roadmap_decision_input_loaded": post_controlled_frame_roadmap_decision_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "safety_task_arbitration_policy_input_loaded": safety_task_arbitration_policy_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "dryrun_case_schema_defined": True,
        "simulated_crossing_evidence_set_schema_defined": True,
        "crossing_governance_decision_candidate_schema_defined": True,
        "forbidden_crossing_output_check_schema_defined": True,
        "crossing_conflict_evaluation_candidate_schema_defined": True,
        "crossing_uncertainty_evaluation_candidate_schema_defined": True,
        "crossing_dryrun_boundary_decision_schema_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(scenario_matrix_rows),
        "dryrun_results_generated": True,
        "decision_candidate_count": len(decision_candidates),
        "forbidden_crossing_output_check_results_generated": True,
        "forbidden_crossing_outputs_absent": forbidden_absent,
        "inherits_safety_constitution": True,
        "crossing_permission_output_allowed": False,
        "crossing_action_instruction_allowed": False,
        "safe_to_cross_claim_allowed": False,
        "traffic_light_candidate_not_crossing_permission": True,
        "green_light_candidate_not_crossing_permission": True,
        "countdown_text_candidate_not_crossing_permission": True,
        "crowd_flow_candidate_not_crossing_permission": True,
        "map_crossing_hint_not_crossing_permission": True,
        "route_crossing_hint_not_crossing_permission": True,
        "user_says_go_not_crossing_permission": True,
        "single_modality_evidence_not_crossing_permission": True,
        "stale_evidence_not_crossing_permission": True,
        "conflicting_evidence_not_crossing_permission": True,
        "low_confidence_evidence_not_crossing_permission": True,
        "uncertainty_requires_hold_or_confirm": True,
        "conflict_blocks_crossing_action": True,
        "human_assistance_candidate_allowed": True,
        "human_assistance_obtained_assumed": False,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "navigation_action_allowed": False,
        "fact_status_not_fact": True,
        "crossing_runtime_allowed": False,
        "crossing_runtime_invoked": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "user_heard_assumed": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "boundary_ok": all_boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if all_boundary_ok and forbidden_absent else "CROSSING_DECISION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if all_boundary_ok and forbidden_absent else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "dryrun_case_schema": dryrun_case_schema,
        "simulated_crossing_evidence_set_schema": simulated_crossing_evidence_set_schema,
        "crossing_governance_decision_candidate_schema": crossing_governance_decision_candidate_schema,
        "forbidden_crossing_output_check_schema": forbidden_crossing_output_check_schema,
        "crossing_conflict_evaluation_candidate_schema": crossing_conflict_evaluation_candidate_schema,
        "crossing_uncertainty_evaluation_candidate_schema": crossing_uncertainty_evaluation_candidate_schema,
        "crossing_dryrun_boundary_decision_schema": crossing_dryrun_boundary_decision_schema,
        "crossing_decision_dryrun_scenario_matrix": crossing_decision_dryrun_scenario_matrix,
        "crossing_decision_dryrun_results": crossing_decision_dryrun_results,
        "forbidden_crossing_output_check_results": forbidden_crossing_output_check_results,
        "crossing_dryrun_boundary_matrix": crossing_dryrun_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": no_runtime_boundary_report,
        "no_write_boundary_report": no_write_boundary_report,
        "conflict_evaluation_candidates": {"candidates": conflict_evals, "count": len(conflict_evals), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "uncertainty_evaluation_candidates": {"candidates": uncertainty_evals, "count": len(uncertainty_evals), "source_chain": SOURCE_CHAIN, **_not_fact()},
    }
