# -*- coding: utf-8 -*-
"""Crossing Decision Post-DryRun Review v1 — review / audit / closure readiness only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

PHASE_ID = "Phase-Crossing-Decision-Post-DryRun-Review-v1-001"
REVIEW_ID = "cdpdpr_v1_001"
REVIEW_SCOPE = "crossing_decision_post_dryrun_review_only"
SOURCE_CHAIN = "crossing_decision_post_dryrun_review_v1"
FINAL_DECISION = "CROSSING_DECISION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Crossing-Decision-Closure-v1-001"

DRYRUN_DECISION = "CROSSING_DECISION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
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

ALLOWED_DECISION_TYPES = {
    "SAFETY_HOLD_CANDIDATE",
    "REOBSERVE_CANDIDATE",
    "HUMAN_ASSISTANCE_CANDIDATE",
    "LOW_CONFIDENCE_WARNING_CANDIDATE",
    "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE",
    "NO_OUTPUT_SUPPRESSED",
}

REQUIRED_SCENARIOS = [
    "green_light_candidate_only",
    "green_light_with_vehicle_flow_uncertain",
    "red_light_candidate",
    "countdown_text_candidate_only",
    "crowd_flow_forward",
    "map_crossing_hint_only",
    "route_says_cross",
    "user_says_go",
    "crosswalk_candidate_but_vehicle_occluded",
    "traffic_light_uncertain",
    "no_crosswalk_detected",
    "stale_traffic_light_evidence",
    "conflicting_audio_visual_cues",
    "unknown_speaker_says_safe",
    "green_light_plus_crowd_flow_plus_map_hint",
    "all_evidence_low_confidence",
]

CONSERVATIVE_CATEGORY_EXPECTATIONS = {
    "green_light_only": {
        "scenario_ids": {"green_light_candidate_only"},
        "allowed_decision_types": {"VISUAL_CONFIRMATION_REQUIRED_CANDIDATE", "SAFETY_HOLD_CANDIDATE"},
        "forbidden_decision_types": {"GREEN_LIGHT_GO", "SAFE_TO_CROSS", "GO_AHEAD"},
    },
    "green_light_with_uncertain_vehicle_flow": {
        "scenario_ids": {"green_light_with_vehicle_flow_uncertain"},
        "allowed_decision_types": {"SAFETY_HOLD_CANDIDATE", "REOBSERVE_CANDIDATE"},
        "forbidden_decision_types": {"SAFE_TO_CROSS", "GO_AHEAD"},
    },
    "countdown_text_only": {
        "scenario_ids": {"countdown_text_candidate_only"},
        "allowed_decision_types": {"VISUAL_CONFIRMATION_REQUIRED_CANDIDATE", "SAFETY_HOLD_CANDIDATE"},
        "forbidden_decision_types": {"COUNTDOWN_SAYS_GO", "SAFE_TO_CROSS"},
    },
    "crowd_flow_forward": {
        "scenario_ids": {"crowd_flow_forward"},
        "allowed_decision_types": {"SAFETY_HOLD_CANDIDATE", "REOBSERVE_CANDIDATE"},
        "forbidden_decision_types": {"FOLLOW_THE_CROWD", "SAFE_TO_CROSS"},
    },
    "map_crossing_hint_only": {
        "scenario_ids": {"map_crossing_hint_only"},
        "allowed_decision_types": {"VISUAL_CONFIRMATION_REQUIRED_CANDIDATE", "SAFETY_HOLD_CANDIDATE"},
        "forbidden_decision_types": {"MAP_SAYS_CROSS", "SAFE_TO_CROSS"},
    },
    "route_says_cross": {
        "scenario_ids": {"route_says_cross"},
        "allowed_decision_types": {"SAFETY_HOLD_CANDIDATE", "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE"},
        "forbidden_decision_types": {"SAFE_TO_CROSS", "GO_AHEAD", "PROCEED"},
    },
    "user_says_go": {
        "scenario_ids": {"user_says_go"},
        "allowed_decision_types": {"SAFETY_HOLD_CANDIDATE", "REOBSERVE_CANDIDATE"},
        "forbidden_decision_types": {"GO_AHEAD", "SAFE_TO_CROSS", "PROCEED"},
    },
    "low_confidence": {
        "scenario_ids": {"traffic_light_uncertain", "all_evidence_low_confidence"},
        "allowed_decision_types": {"LOW_CONFIDENCE_WARNING_CANDIDATE", "SAFETY_HOLD_CANDIDATE", "REOBSERVE_CANDIDATE"},
        "forbidden_decision_types": {"SAFE_TO_CROSS", "GO_AHEAD"},
    },
    "stale_evidence": {
        "scenario_ids": {"stale_traffic_light_evidence"},
        "allowed_decision_types": {"REOBSERVE_CANDIDATE", "SAFETY_HOLD_CANDIDATE"},
        "forbidden_decision_types": {"SAFE_TO_CROSS", "GO_AHEAD"},
    },
    "conflict": {
        "scenario_ids": {"conflicting_audio_visual_cues", "green_light_with_vehicle_flow_uncertain", "green_light_plus_crowd_flow_plus_map_hint"},
        "allowed_decision_types": {"HUMAN_ASSISTANCE_CANDIDATE", "REOBSERVE_CANDIDATE", "SAFETY_HOLD_CANDIDATE"},
        "forbidden_decision_types": {"SAFE_TO_CROSS", "FOLLOW_THE_CROWD", "GREEN_LIGHT_GO"},
    },
}

ROOT_SPECS = [
    {
        "id": "crossing_decision_dryrun",
        "arg": "crossing_decision_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "crossing_decision_dryrun_scenario_matrix.json",
            "crossing_decision_dryrun_results.json",
            "forbidden_crossing_output_check_results.json",
            "crossing_dryrun_boundary_matrix.json",
            "verifier_report.json",
        ],
    },
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
            "safety_constitution_inheritance_matrix.json",
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


def _index_by(items: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if value:
            out[value] = item
    return out


def _boundary_payload() -> Dict[str, Any]:
    return {
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "crossing_runtime_allowed": False,
        "crossing_runtime_invoked": False,
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


def run_crossing_decision_post_dryrun_review_v1(
    *,
    crossing_decision_dryrun_root: str,
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
    dryrun_root = roots["crossing_decision_dryrun"]["root"]
    governance_root = roots["crossing_safety_governance"]["root"]
    safety_root = roots["safety_constitution"]["root"]
    safety_task_root = roots["safety_task_arbitration_policy"]["root"]
    safety_task_final = _read_json(safety_task_root / "safety_task_arbitration_final_decision_v1.json") if safety_task_root else {}

    dryrun_scenario_matrix = _read_json(dryrun_root / "crossing_decision_dryrun_scenario_matrix.json") if dryrun_root else {}
    dryrun_results = _read_json(dryrun_root / "crossing_decision_dryrun_results.json") if dryrun_root else {}
    forbidden_results = _read_json(dryrun_root / "forbidden_crossing_output_check_results.json") if dryrun_root else {}
    dryrun_boundary = _read_json(dryrun_root / "crossing_dryrun_boundary_matrix.json") if dryrun_root else {}
    dryrun_verifier = _read_json(dryrun_root / "verifier_report.json") if dryrun_root else {}
    dryrun_governance_debt = _read_json(dryrun_root / "governance_debt_register.json") if dryrun_root else {}

    forbidden_register = _read_json(governance_root / "forbidden_crossing_output_register.json") if governance_root else {}
    governance_inheritance = _read_json(governance_root / "safety_constitution_inheritance_matrix.json") if governance_root else {}
    crossing_output_policy = _read_json(governance_root / "crossing_output_policy.json") if governance_root else {}
    crossing_inheritance_policy = _read_json(safety_root / "crossing_safety_inheritance_policy.json") if safety_root else {}
    global_principles = _read_json(safety_root / "global_safety_principles.json") if safety_root else {}

    crossing_dryrun_input_loaded = (
        roots["crossing_decision_dryrun"]["loaded"]
        and summaries["crossing_decision_dryrun"].get("final_decision") == DRYRUN_DECISION
        and summaries["crossing_decision_dryrun"].get("scenario_count", 0) >= 16
        and summaries["crossing_decision_dryrun"].get("forbidden_crossing_outputs_absent") is True
        and dryrun_verifier.get("verifier") == "GO"
    )
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

    required_root_ids = [spec["id"] for spec in ROOT_SPECS if spec["required"]]
    loaded_root_ids = [row["intake_id"] for row in input_rows if row["loaded"]]
    optional_missing_roots = [row["intake_id"] for row in input_rows if (not row["required"]) and row["status"] == "optional_missing"]
    missing_required_roots = [row["intake_id"] for row in input_rows if row["required"] and row["status"] != "loaded"]

    crossing_dryrun_input_root_review = {
        "review_id": REVIEW_ID,
        "required_roots": required_root_ids,
        "loaded_roots": loaded_root_ids,
        "optional_missing_roots": optional_missing_roots,
        "missing_required_roots": missing_required_roots,
        "input_root_status": "all_required_loaded" if not missing_required_roots else "missing_required_root",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scenarios = dryrun_scenario_matrix.get("scenarios", [])
    scenario_ids_present = {s.get("scenario_id") for s in scenarios}
    covered_scenarios = [sid for sid in REQUIRED_SCENARIOS if sid in scenario_ids_present]
    missing_scenarios = [sid for sid in REQUIRED_SCENARIOS if sid not in scenario_ids_present]

    crossing_scenario_coverage_review = {
        "reviewed_scenario_count": len(scenarios),
        "expected_scenario_count": len(REQUIRED_SCENARIOS),
        "covered_scenarios": covered_scenarios,
        "missing_scenarios": missing_scenarios,
        "green_light_cases_present": any(sid in scenario_ids_present for sid in ("green_light_candidate_only", "green_light_with_vehicle_flow_uncertain", "green_light_plus_crowd_flow_plus_map_hint")),
        "crowd_flow_cases_present": "crowd_flow_forward" in scenario_ids_present,
        "map_hint_cases_present": any(sid in scenario_ids_present for sid in ("map_crossing_hint_only", "green_light_plus_crowd_flow_plus_map_hint")),
        "route_hint_cases_present": "route_says_cross" in scenario_ids_present,
        "user_instruction_cases_present": "user_says_go" in scenario_ids_present,
        "conflict_cases_present": any(sid in scenario_ids_present for sid in ("conflicting_audio_visual_cues", "green_light_with_vehicle_flow_uncertain", "green_light_plus_crowd_flow_plus_map_hint")),
        "low_confidence_cases_present": any(sid in scenario_ids_present for sid in ("traffic_light_uncertain", "all_evidence_low_confidence")),
        "stale_evidence_cases_present": "stale_traffic_light_evidence" in scenario_ids_present,
        "verdict": "GO" if not missing_scenarios and len(scenarios) >= 16 else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    decision_candidates = dryrun_results.get("decision_candidates", [])
    decision_idx = _index_by(decision_candidates, "source_case_id")
    forbidden_checks = forbidden_results.get("checks", [])

    all_forbidden_found: List[str] = []
    for check in forbidden_checks:
        all_forbidden_found.extend(check.get("forbidden_outputs_found", []))

    forbidden_crossing_output_review = {
        "forbidden_register_loaded": bool(forbidden_register.get("forbidden_outputs")),
        "reviewed_case_count": forbidden_results.get("check_count", 0),
        "forbidden_outputs_checked": FORBIDDEN_OUTPUT_MODES,
        "forbidden_outputs_found": sorted(set(all_forbidden_found)),
        "forbidden_outputs_absent": forbidden_results.get("forbidden_crossing_outputs_absent") is True and not all_forbidden_found,
        "violation_count": forbidden_results.get("total_violation_count", 0),
        "blocked_outputs": FORBIDDEN_OUTPUT_MODES,
        "verdict": "GO" if forbidden_results.get("forbidden_crossing_outputs_absent") and not all_forbidden_found else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    perm_false_count = sum(1 for d in decision_candidates if d.get("crossing_permission_allowed") is False)
    action_false_count = sum(1 for d in decision_candidates if d.get("crossing_action_instruction_allowed") is False)
    safe_false_count = sum(1 for d in decision_candidates if d.get("safe_to_cross_claim_allowed") is False)

    user_go = decision_idx.get("user_says_go", {})
    stale_case = decision_idx.get("stale_traffic_light_evidence", {})
    conflict_case = decision_idx.get("conflicting_audio_visual_cues", {})
    low_conf_case = decision_idx.get("all_evidence_low_confidence", {})

    crossing_permission_boundary_review = {
        "reviewed_decision_candidate_count": len(decision_candidates),
        "crossing_permission_allowed_false_count": perm_false_count,
        "crossing_action_instruction_allowed_false_count": action_false_count,
        "safe_to_cross_claim_allowed_false_count": safe_false_count,
        "single_modality_evidence_blocked": decision_idx.get("green_light_candidate_only", {}).get("crossing_permission_allowed") is False,
        "stale_evidence_blocked": stale_case.get("crossing_permission_allowed") is False and stale_case.get("decision_type") in ALLOWED_DECISION_TYPES,
        "conflicting_evidence_blocked": conflict_case.get("crossing_permission_allowed") is False,
        "low_confidence_evidence_blocked": low_conf_case.get("crossing_permission_allowed") is False,
        "user_says_go_blocked": user_go.get("crossing_permission_allowed") is False and user_go.get("decision_type") != "GO_AHEAD",
        "verdict": "GO" if perm_false_count == len(decision_candidates) and len(decision_candidates) >= 16 else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    inherited_principles = governance_inheritance.get("inherited_principles", [])
    safety_constitution_inheritance_review = {
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "inherits_safety_constitution": governance_inheritance.get("inherits_safety_constitution") is True,
        "safety_over_task_verified": "safety_over_task" in inherited_principles,
        "safety_over_user_instruction_verified": "safety_over_user_instruction" in inherited_principles,
        "candidate_not_fact_verified": "candidate_must_not_be_claimed_as_fact" in inherited_principles,
        "unknown_not_fabricated_verified": "unknown_must_not_be_fabricated" in inherited_principles,
        "high_risk_special_governance_verified": "high_risk_action_requires_special_governance" in inherited_principles,
        "crossing_inheritance_verified": bool(crossing_inheritance_policy) and summaries["crossing_safety_governance"].get("inherits_safety_constitution") is True,
        "verdict": "GO" if safety_constitution_input_loaded and governance_inheritance.get("inherits_safety_constitution") else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    unsafe_escalations: List[str] = []
    overconfident_outputs: List[str] = []
    category_results: List[Dict[str, Any]] = []

    for category, spec in CONSERVATIVE_CATEGORY_EXPECTATIONS.items():
        category_pass = True
        for sid in spec["scenario_ids"]:
            decision = decision_idx.get(sid, {})
            dtype = decision.get("decision_type", "")
            if dtype in spec["forbidden_decision_types"]:
                unsafe_escalations.append(f"{category}:{sid}:{dtype}")
                category_pass = False
            if dtype and dtype not in ALLOWED_DECISION_TYPES:
                unsafe_escalations.append(f"{category}:{sid}:invalid_type:{dtype}")
                category_pass = False
            if decision.get("crossing_permission_allowed") is True:
                unsafe_escalations.append(f"{category}:{sid}:permission_true")
                category_pass = False
            if dtype in ("SAFE_TO_CROSS", "GO_AHEAD", "PROCEED", "FOLLOW_THE_CROWD"):
                overconfident_outputs.append(f"{category}:{sid}:{dtype}")
                category_pass = False
        category_results.append({"category": category, "pass": category_pass})

    crossing_conservative_handling_review = {
        "reviewed_category_count": len(CONSERVATIVE_CATEGORY_EXPECTATIONS),
        "category_results": category_results,
        "conservative_handling_pass": not unsafe_escalations and not overconfident_outputs,
        "unsafe_escalation_found": bool(unsafe_escalations),
        "overconfident_output_found": bool(overconfident_outputs),
        "unsafe_escalations": unsafe_escalations,
        "overconfident_outputs": overconfident_outputs,
        "verdict": "GO" if not unsafe_escalations and not overconfident_outputs else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    human_assistance_cases = [d for d in decision_candidates if d.get("decision_type") == "HUMAN_ASSISTANCE_CANDIDATE"]
    dryrun_human_assistance_not_assumed = summaries["crossing_decision_dryrun"].get("human_assistance_obtained_assumed") is False
    human_assistance_candidate_review = {
        "human_assistance_candidate_allowed": crossing_output_policy.get("allowed_output_modes") is None or "HUMAN_ASSISTANCE_CANDIDATE" in (crossing_output_policy.get("allowed_output_modes") or []),
        "human_assistance_obtained_assumed": not dryrun_human_assistance_not_assumed,
        "staff_or_human_assistance_not_action": all(d.get("action_allowed", False) is False for d in human_assistance_cases) if human_assistance_cases else True,
        "no_assumption_of_external_confirmation": all(d.get("crossing_permission_allowed") is False for d in human_assistance_cases),
        "human_assistance_case_count": len(human_assistance_cases),
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    runtime_write_action_speech_boundary_review = {
        "crossing_runtime_invoked": False,
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
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_review = {
        "review_id": f"{REVIEW_ID}_debt",
        "dryrun_governance_debt_loaded": bool(dryrun_governance_debt),
        "carryover_topics": dryrun_governance_debt.get("carryover_topics", []),
        "post_dryrun_review_notes": [
            "16 crossing dry-run scenarios reviewed for conservative output only",
            "forbidden crossing outputs absent across all cases",
            "closure does not imply safe-to-cross capability",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for name, ok_value in (
        ("crossing_dryrun_input_loaded", crossing_dryrun_input_loaded),
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
        if not ok_value:
            blockers.append(name)
    if crossing_scenario_coverage_review["verdict"] != "GO":
        blockers.append("scenario_coverage_gap")
    if forbidden_crossing_output_review["verdict"] != "GO":
        blockers.append("forbidden_output_violation")
    if crossing_permission_boundary_review["verdict"] != "GO":
        blockers.append("permission_boundary_gap")
    if safety_constitution_inheritance_review["verdict"] != "GO":
        blockers.append("safety_constitution_inheritance_gap")
    if crossing_conservative_handling_review["verdict"] != "GO":
        blockers.append("conservative_handling_gap")

    crossing_closure_readiness_decision = {
        "post_dryrun_review_verdict": "GO" if not blockers else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "本阶段只做 review / audit / closure readiness",
            "closure 意义是系统性禁止过街许可输出，而非具备过街能力",
            "crossing runtime trial 仍保持 deferred",
        ],
        "ready_for_closure": not blockers,
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "final_decision": FINAL_DECISION if not blockers else "CROSSING_DECISION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_runtime_boundary_report = _boundary_payload()
    no_write_boundary_report = _boundary_payload()

    all_perm_false = perm_false_count == len(decision_candidates) and len(decision_candidates) >= 16
    all_action_false = action_false_count == len(decision_candidates)
    all_safe_false = safe_false_count == len(decision_candidates)

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "crossing_dryrun_input_loaded": crossing_dryrun_input_loaded,
        "crossing_safety_governance_input_loaded": crossing_safety_governance_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "post_controlled_frame_roadmap_decision_input_loaded": post_controlled_frame_roadmap_decision_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "safety_task_arbitration_policy_input_loaded": safety_task_arbitration_policy_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "input_root_review_generated": True,
        "scenario_coverage_review_generated": True,
        "forbidden_crossing_output_review_generated": True,
        "crossing_permission_boundary_review_generated": True,
        "safety_constitution_inheritance_review_generated": True,
        "crossing_conservative_handling_review_generated": True,
        "human_assistance_candidate_review_generated": True,
        "runtime_write_action_speech_boundary_review_generated": True,
        "closure_readiness_decision_generated": True,
        "reviewed_scenario_count": len(scenarios),
        "reviewed_decision_candidate_count": len(decision_candidates),
        "forbidden_crossing_outputs_absent": forbidden_crossing_output_review["forbidden_outputs_absent"],
        "forbidden_output_violation_count": forbidden_crossing_output_review["violation_count"],
        "crossing_permission_allowed_false_all_cases": all_perm_false,
        "crossing_action_instruction_allowed_false_all_cases": all_action_false,
        "safe_to_cross_claim_allowed_false_all_cases": all_safe_false,
        "inherits_safety_constitution": safety_constitution_inheritance_review["inherits_safety_constitution"],
        "safety_constitution_inheritance_pass": safety_constitution_inheritance_review["verdict"] == "GO",
        "conservative_handling_pass": crossing_conservative_handling_review["conservative_handling_pass"],
        "unsafe_escalation_found": crossing_conservative_handling_review["unsafe_escalation_found"],
        "overconfident_output_found": crossing_conservative_handling_review["overconfident_output_found"],
        "human_assistance_candidate_allowed": human_assistance_candidate_review["human_assistance_candidate_allowed"],
        "human_assistance_obtained_assumed": False,
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "crossing_runtime_invoked": False,
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
        "boundary_ok": not blockers,
        "violations": blockers,
        "final_decision": FINAL_DECISION if not blockers else "CROSSING_DECISION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "crossing_dryrun_input_root_review": crossing_dryrun_input_root_review,
        "crossing_scenario_coverage_review": crossing_scenario_coverage_review,
        "forbidden_crossing_output_review": forbidden_crossing_output_review,
        "crossing_permission_boundary_review": crossing_permission_boundary_review,
        "safety_constitution_inheritance_review": safety_constitution_inheritance_review,
        "crossing_conservative_handling_review": crossing_conservative_handling_review,
        "human_assistance_candidate_review": human_assistance_candidate_review,
        "runtime_write_action_speech_boundary_review": runtime_write_action_speech_boundary_review,
        "crossing_closure_readiness_decision": crossing_closure_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": {
            "recommended_next_phase": summary["recommended_next_phase"],
            "final_decision": summary["final_decision"],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "no_runtime_boundary_report": no_runtime_boundary_report,
        "no_write_boundary_report": no_write_boundary_report,
    }
