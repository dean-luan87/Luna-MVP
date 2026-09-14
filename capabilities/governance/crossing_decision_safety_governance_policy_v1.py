# -*- coding: utf-8 -*-
"""Crossing Decision Safety Governance Policy v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Crossing-Decision-Safety-Governance-Policy-v1-001"
POLICY_SCOPE = "crossing_decision_safety_governance_policy_only"
SOURCE_CHAIN = "crossing_decision_safety_governance_policy_v1"
POLICY_ID = "cdsgp_v1_001"
FINAL_DECISION = "CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY_READY_FOR_CROSSING_DECISION_DRYRUN"
NEXT_PHASE = "Phase-Crossing-Decision-DryRun-v1-001"

SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
POST_CONTROLLED_FRAME_ROADMAP_DECISION = "POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY"
CONTROLLED_FRAME_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
SAFETY_TASK_ARBITRATION_DECISION = "SAFETY_TASK_ARBITRATION_POLICY_READY_FOR_LOOP_STABILIZATION_TEST"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
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
    {
        "id": "gps_route_context_dryrun",
        "arg": "gps_route_context_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "worldmodel_lookup_framework",
        "arg": "worldmodel_lookup_framework_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]

ALLOWED_EVIDENCE_TYPES = [
    "traffic_light_candidate",
    "traffic_light_state_change_candidate",
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
]

SCHEMA_FIELDS = [
    "evidence_candidate_id",
    "evidence_type",
    "source_ref",
    "confidence",
    "uncertainty",
    "freshness_status",
    "ttl_policy_ref",
    "conflict_refs",
    "current_action_allowed",
    "crossing_permission_allowed",
    "fact_status",
    "source_chain",
]

CROSSING_PERMISSION_BOUNDARY = {
    "traffic_light_candidate_not_crossing_permission": True,
    "green_light_candidate_not_crossing_permission": True,
    "countdown_text_candidate_not_crossing_permission": True,
    "crowd_flow_candidate_not_crossing_permission": True,
    "pedestrian_flow_candidate_not_crossing_permission": True,
    "map_crossing_hint_not_crossing_permission": True,
    "route_crossing_hint_not_crossing_permission": True,
    "user_says_go_not_crossing_permission": True,
    "memory_hint_not_crossing_permission": True,
    "single_modality_evidence_not_crossing_permission": True,
    "stale_evidence_not_crossing_permission": True,
    "conflicting_evidence_not_crossing_permission": True,
    "low_confidence_evidence_not_crossing_permission": True,
}

UNCERTAINTY_RULES = [
    ("insufficient_evidence", "HOLD_OR_CONFIRM_CANDIDATE"),
    ("low_confidence", "HOLD_OR_CONFIRM_CANDIDATE"),
    ("stale_evidence", "REOBSERVE_CANDIDATE"),
    ("conflicting_evidence", "REOBSERVE_OR_HUMAN_ASSISTANCE_CANDIDATE"),
    ("occluded_vehicle_flow", "DO_NOT_ADVANCE_CANDIDATE"),
    ("traffic_light_uncertain", "DO_NOT_ADVANCE_CANDIDATE"),
    ("no_crosswalk_detected", "DO_NOT_CROSS_CANDIDATE"),
    ("map_only_crossing_hint", "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE"),
]

CONFLICT_CASES = [
    "green_light_vs_vehicle_flow_conflict",
    "map_crossing_hint_vs_visual_absence",
    "crowd_flow_vs_traffic_uncertain",
    "ocr_countdown_vs_traffic_light_uncertain",
    "route_says_cross_vs_safety_uncertain",
    "user_instruction_vs_safety_boundary",
    "stale_memory_vs_current_observation",
    "audio_cue_vs_visual_uncertain",
]

CONFLICT_OUTPUTS = [
    "CrossingConflictCandidate",
    "ReobserveRequestCandidate",
    "HumanAssistanceCandidate",
    "SafetyHoldCandidate",
]

ALLOWED_OUTPUT_MODES = [
    "NO_OUTPUT_SUPPRESSED",
    "SAFETY_HOLD_CANDIDATE",
    "REOBSERVE_CANDIDATE",
    "HUMAN_ASSISTANCE_CANDIDATE",
    "LOW_CONFIDENCE_WARNING_CANDIDATE",
    "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE",
    "TEXT_ONLY_DRY_PREVIEW",
]

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

SCENARIOS = [
    ("green_light_candidate_only", "green light candidate exists", "no_crossing_permission"),
    ("green_light_with_vehicle_flow_uncertain", "green light plus uncertain vehicle flow", "safety_hold_candidate"),
    ("red_light_candidate", "red light candidate exists", "do_not_cross_candidate"),
    ("countdown_text_candidate_only", "OCR countdown candidate exists", "no_crossing_permission"),
    ("crowd_flow_forward", "crowd moving forward", "follow_crowd_forbidden"),
    ("map_crossing_hint_only", "map says crossing ahead", "visual_confirmation_required"),
    ("route_says_cross", "route says cross", "no_crossing_permission"),
    ("user_says_go", "user instruction says go", "safety_boundary_blocks_action"),
    ("crosswalk_candidate_but_vehicle_occluded", "crosswalk visible but vehicle flow occluded", "hold_or_reobserve"),
    ("traffic_light_uncertain", "traffic light low confidence", "hold_or_reobserve"),
    ("no_crosswalk_detected", "crossing area uncertain", "do_not_cross_candidate"),
    ("stale_traffic_light_evidence", "stale traffic-light evidence present", "current_action_blocked"),
    ("conflicting_audio_visual_cues", "audio cue conflicts with visual", "human_assistance_candidate"),
    ("unknown_speaker_says_safe", "unknown speaker says safe", "no_crossing_permission"),
]

GOVERNANCE_DEBT_TOPICS = [
    "crossing decision dryrun still pending",
    "controlled sample evidence for crossing remains deferred",
    "vehicle occlusion reasoning remains future dryrun topic",
    "human assistance escalation phrasing remains future output-governance topic",
    "speech gate integration remains deferred",
    "audio/visual conflict fusion remains policy-only",
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


def _boundary_payload() -> Dict[str, Any]:
    return {
        "policy_scope": POLICY_SCOPE,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "crossing_decision_runtime_invoked": False,
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


def run_crossing_decision_safety_governance_policy_v1(
    *,
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
    gps_route_context_dryrun_root: Optional[str] = None,
    worldmodel_lookup_framework_root: Optional[str] = None,
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
    safety_constitution_root_path = roots["safety_constitution"]["root"]
    safety_task_root = roots["safety_task_arbitration_policy"]["root"]
    safety_task_final = _read_json(safety_task_root / "safety_task_arbitration_final_decision_v1.json") if safety_task_root else {}
    inherited_crossing_policy = _read_json(safety_constitution_root_path / "crossing_safety_inheritance_policy.json") if safety_constitution_root_path else {}
    inherited_global_principles = _read_json(safety_constitution_root_path / "global_safety_principles.json") if safety_constitution_root_path else {}
    inherited_evidence_policy = _read_json(safety_constitution_root_path / "evidence_boundary_policy.json") if safety_constitution_root_path else {}

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

    crossing_evidence_candidate_schema = {
        "allowed_evidence_types": ALLOWED_EVIDENCE_TYPES,
        "schema_fields": SCHEMA_FIELDS,
        "default_constraints": {
            "current_action_allowed": False,
            "crossing_permission_allowed": False,
            "fact_status": "not_fact",
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_permission_boundary_policy = {
        **CROSSING_PERMISSION_BOUNDARY,
        "inherits_safety_constitution": True,
        "crossing_permission_output_allowed": False,
        "crossing_action_instruction_allowed": False,
        "safe_to_cross_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_uncertainty_policy = {
        "rules": [
            {
                "uncertainty_case": case_name,
                "required_candidate": output_name,
                "crossing_permission_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for case_name, output_name in UNCERTAINTY_RULES
        ],
        "uncertainty_requires_hold_or_confirm": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_conflict_policy = {
        "conflict_cases": CONFLICT_CASES,
        "generated_candidates": CONFLICT_OUTPUTS,
        "principles": {
            "conflict_blocks_crossing_action": True,
            "conflict_cannot_be_resolved_by_LLM_guess": True,
            "conflict_cannot_be_resolved_by_map_alone": True,
            "conflict_cannot_be_resolved_by_user_command_alone": True,
            "conflict_requires_reobserve_hold_or_human_assistance": True,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_output_policy = {
        "allowed_output_modes": ALLOWED_OUTPUT_MODES,
        "forbidden_output_modes": FORBIDDEN_OUTPUT_MODES,
        "speech_allowed": False,
        "user_heard_assumed": False,
        "action_allowed": False,
        "navigation_action_allowed": False,
        "crossing_permission_output_allowed": False,
        "crossing_action_instruction_allowed": False,
        "safe_to_cross_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_human_assistance_policy = {
        "ask_human_assistance_when": [
            "conflicting evidence persists",
            "vehicle flow is occluded or unresolved",
            "audio and visual cues conflict",
            "unknown environment blocks safe confirmation",
        ],
        "seek_staff_assistance_when": [
            "crossing infrastructure is unclear in complex public environment",
            "traffic control cues remain unresolved",
        ],
        "stop_and_wait_when": [
            "evidence is insufficient",
            "traffic light is uncertain",
            "vehicle flow is uncertain",
        ],
        "ask_user_to_confirm_visually_or_auditorily_when": [
            "map or route hint exists without confirmatory local evidence",
            "crosswalk/crossing context remains partial",
        ],
        "tell_user_information_is_insufficient_when": True,
        "human_assistance_candidate_allowed": True,
        "human_assistance_obtained_assumed": False,
        "no_real_speech_output": True,
        "no_task_state_commit": True,
        "no_navigation_action": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scenario_rows = []
    for scenario_id, trigger_note, outcome in SCENARIOS:
        scenario_rows.append(
            {
                "scenario_id": scenario_id,
                "trigger_note": trigger_note,
                "expected_outcome": outcome,
                "crossing_permission_allowed": False,
                "crossing_action_instruction_allowed": False,
                "safe_to_cross_claim_allowed": False,
                "fact_status": "not_fact",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    crossing_safety_scenario_matrix = {
        "scenarios": scenario_rows,
        "scenario_count": len(scenario_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_boundary_matrix = {
        "policy_scope": POLICY_SCOPE,
        "crossing_runtime_allowed": False,
        "crossing_permission_output_allowed": False,
        "crossing_action_instruction_allowed": False,
        "safe_to_cross_claim_allowed": False,
        "action_allowed": False,
        "navigation_action_allowed": False,
        "speech_allowed": False,
        "fact_status_not_fact": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    safety_constitution_inheritance_matrix = {
        "inherits_safety_constitution": True,
        "inherited_principles": [
            "safety_over_task",
            "safety_over_user_instruction",
            "safety_over_map_hint",
            "safety_over_ocr_text",
            "safety_over_visual_candidate",
            "safety_over_memory_hint",
            "candidate_must_not_be_claimed_as_fact",
            "unknown_must_not_be_fabricated",
            "high_risk_action_requires_special_governance",
        ],
        "inherited_crossing_constraints": inherited_crossing_policy,
        "inherited_global_principles_snapshot": inherited_global_principles,
        "inherited_evidence_boundary_snapshot": inherited_evidence_policy,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    forbidden_crossing_output_register = {
        "forbidden_outputs": FORBIDDEN_OUTPUT_MODES,
        "forbidden_reason": "current phase cannot output crossing permission or equivalent action instructions",
        "forbidden_count": len(FORBIDDEN_OUTPUT_MODES),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "carryover_topics": GOVERNANCE_DEBT_TOPICS,
        "crossing_dryrun_required_next": True,
        "controlled_sample_before_runtime_still_required": True,
        "speech_gate_for_crossing_output_still_deferred": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crossing_decision_safety_governance_policy = {
        "policy_id": POLICY_ID,
        "policy_scope": POLICY_SCOPE,
        "inherited_safety_constitution_ref": "_eval_out/luna_safety_constitution_policy_v1_smoke_v0/crossing_safety_inheritance_policy.json",
        "crossing_evidence_boundary_ref": "crossing_evidence_candidate_schema.json",
        "crossing_permission_boundary_ref": "crossing_permission_boundary_policy.json",
        "crossing_uncertainty_policy_ref": "crossing_uncertainty_policy.json",
        "crossing_conflict_policy_ref": "crossing_conflict_policy.json",
        "crossing_output_policy_ref": "crossing_output_policy.json",
        "crossing_human_assistance_policy_ref": "crossing_human_assistance_policy.json",
        "no_runtime_boundary_ref": "no_runtime_boundary_report.json",
        "no_write_boundary_ref": "no_write_boundary_report.json",
        "inherits_safety_constitution": True,
        "crossing_governance_is_policy_only": True,
        "crossing_runtime_allowed": False,
        "crossing_permission_output_allowed": False,
        "crossing_action_instruction_allowed": False,
        "current_phase_cannot_decide_safe_to_cross": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "crossing governance boundary is frozen; next step can be a strict dry-run that still does not enter runtime",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers = []
    for name, flag in (
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

    summary = {
        "phase": PHASE_ID,
        "policy_scope": POLICY_SCOPE,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "post_controlled_frame_roadmap_decision_input_loaded": post_controlled_frame_roadmap_decision_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "safety_task_arbitration_policy_input_loaded": safety_task_arbitration_policy_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "crossing_decision_safety_governance_policy_defined": True,
        "crossing_evidence_candidate_schema_defined": True,
        "crossing_permission_boundary_policy_defined": True,
        "crossing_uncertainty_policy_defined": True,
        "crossing_conflict_policy_defined": True,
        "crossing_output_policy_defined": True,
        "crossing_human_assistance_policy_defined": True,
        "safety_constitution_inheritance_matrix_generated": True,
        "forbidden_crossing_output_register_generated": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(scenario_rows),
        "inherits_safety_constitution": True,
        "crossing_runtime_allowed": False,
        "crossing_permission_output_allowed": False,
        "crossing_action_instruction_allowed": False,
        "safe_to_cross_claim_allowed": False,
        "traffic_light_candidate_not_crossing_permission": True,
        "green_light_candidate_not_crossing_permission": True,
        "countdown_text_candidate_not_crossing_permission": True,
        "crowd_flow_candidate_not_crossing_permission": True,
        "pedestrian_flow_candidate_not_crossing_permission": True,
        "map_crossing_hint_not_crossing_permission": True,
        "route_crossing_hint_not_crossing_permission": True,
        "user_says_go_not_crossing_permission": True,
        "single_modality_evidence_not_crossing_permission": True,
        "stale_evidence_not_crossing_permission": True,
        "conflicting_evidence_not_crossing_permission": True,
        "low_confidence_evidence_not_crossing_permission": True,
        "conflict_blocks_crossing_action": True,
        "uncertainty_requires_hold_or_confirm": True,
        "human_assistance_candidate_allowed": True,
        "human_assistance_obtained_assumed": False,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "navigation_action_allowed": False,
        "fact_status_not_fact": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "crossing_decision_runtime_invoked": False,
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
        "final_decision": FINAL_DECISION if not blockers else "CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "crossing_decision_safety_governance_policy": crossing_decision_safety_governance_policy,
        "crossing_evidence_candidate_schema": crossing_evidence_candidate_schema,
        "crossing_permission_boundary_policy": crossing_permission_boundary_policy,
        "crossing_uncertainty_policy": crossing_uncertainty_policy,
        "crossing_conflict_policy": crossing_conflict_policy,
        "crossing_output_policy": crossing_output_policy,
        "crossing_human_assistance_policy": crossing_human_assistance_policy,
        "crossing_safety_scenario_matrix": crossing_safety_scenario_matrix,
        "crossing_boundary_matrix": crossing_boundary_matrix,
        "safety_constitution_inheritance_matrix": safety_constitution_inheritance_matrix,
        "forbidden_crossing_output_register": forbidden_crossing_output_register,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }
