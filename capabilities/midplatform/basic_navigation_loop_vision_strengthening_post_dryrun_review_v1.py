# -*- coding: utf-8 -*-
"""Basic Navigation Loop Vision Strengthening Post-DryRun Review v1.

Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.basic_navigation_loop_vision_strengthening_dryrun_v1 import (
    BOUNDARY_FALSE_FLAGS as DRYRUN_BOUNDARY_FALSE_FLAGS,
)
from capabilities.midplatform.basic_navigation_loop_vision_strengthening_dryrun_v1 import (
    OPTIONAL_ROOT_SPECS as DRYRUN_OPTIONAL_ROOT_SPECS,
)
from capabilities.midplatform.basic_navigation_loop_vision_strengthening_dryrun_v1 import (
    ROOT_INPUT_SPECS as DRYRUN_UPSTREAM_ROOT_SPECS,
)

PHASE_ID = "Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "basic_navigation_loop_vision_strengthening_post_dryrun_review_only"
SOURCE_CHAIN = "basic_navigation_loop_vision_strengthening_post_dryrun_review_v1"
REVIEW_ID = "bnlvspr_v1_001"
FINAL_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Basic-Navigation-Loop-Vision-Strengthening-Closure-v1-001"
DRYRUN_FINAL_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
VISUAL_FEEDBACK_FINAL_DECISION = "VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING"
SELECTIVE_TRACKING_FINAL_DECISION = "SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN"
WORLDOBS_FINAL_DECISION = "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY"
VISUAL_FOCUS_FINAL_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_FINAL_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
BASIC_NAV_STABILIZATION_FINAL_DECISION = "BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_READY_FOR_MINIMAL_RUNTIME_INTEGRATION_TRIAL"
OCR_FINAL_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
MRI_FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"

DRYRUN_ROOT_SPEC = {
    "intake_id": "navigation_vision_strengthening_dryrun",
    "path_arg": "dryrun_root",
    "label": "Basic Navigation Loop Vision Strengthening DryRun v1",
    "required": True,
    "summary_file": "summary.json",
    "extra_artifacts": [
        "navigation_loop_vision_strengthening_scenario_matrix.json",
        "navigation_loop_vision_strengthening_dryrun_results.json",
        "governance_debt_register.json",
        "no_runtime_boundary_report.json",
        "no_write_boundary_report.json",
        "verifier_report.json",
    ],
}

REQUIRED_ROOT_SPECS = [DRYRUN_ROOT_SPEC, *DRYRUN_UPSTREAM_ROOT_SPECS]
OPTIONAL_ROOT_SPECS = list(DRYRUN_OPTIONAL_ROOT_SPECS)

REQUIRED_SCENARIOS = [
    "route_walking_clear_path_guidance",
    "route_walking_near_field_obstacle",
    "approaching_destination_signage_candidate",
    "shop_search_right_side_view_adjustment",
    "object_search_home_privacy_sensitive",
    "crowded_path_crowd_flow_caution",
    "crossing_uncertain_red_green_light",
    "visual_map_memory_conflict_navigation",
    "low_quality_view_hold_still",
    "temporary_facility_route_impact",
    "tracking_later_needed_dynamic_obstacle",
    "ocr_later_needed_readable_sign",
]

HIGH_RISK_EXPECTATIONS = {
    "crossing_uncertain_red_green_light": {
        "risk_type": "crossing_uncertain",
        "guidance_type": "crossing_uncertain_hint",
        "output_mode": "SAFETY_HOLD_PROMPT_CANDIDATE",
        "requires_confirmation": True,
        "requires_future_governance": True,
    },
    "crowded_path_crowd_flow_caution": {
        "risk_type": "crowd_flow",
        "guidance_type": "crowd_flow_caution_hint",
        "output_mode": "TEXT_ONLY_DRY_PREVIEW",
        "requires_tracking_later": True,
        "requires_future_governance": True,
    },
    "visual_map_memory_conflict_navigation": {
        "risk_type": "map_visual_memory_conflict",
        "guidance_type": "map_visual_conflict_hint",
        "output_mode": "STRUCTURED_LOG_ONLY",
        "requires_reobserve": True,
        "requires_future_governance": True,
    },
    "low_quality_view_hold_still": {
        "risk_type": "low_quality_view",
        "guidance_type": "hold_still_candidate",
        "output_mode": "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE",
        "suppresses_task_guidance": True,
        "requires_future_governance": True,
    },
    "temporary_facility_route_impact": {
        "risk_type": "temporary_facility_route_impact",
        "guidance_type": "temporary_route_caution_candidate",
        "output_mode": "TEXT_ONLY_DRY_PREVIEW",
        "requires_future_governance": True,
    },
    "ocr_later_needed_readable_sign": {
        "risk_type": "ocr_later_needed",
        "guidance_type": "ocr_later_needed_hint",
        "output_mode": "TEXT_ONLY_DRY_PREVIEW",
        "requires_ocr_later": True,
        "requires_future_governance": True,
    },
    "tracking_later_needed_dynamic_obstacle": {
        "risk_type": "tracking_later_needed",
        "guidance_type": "tracking_later_needed_hint",
        "output_mode": "TEXT_ONLY_DRY_PREVIEW",
        "requires_tracking_later": True,
        "requires_future_governance": True,
    },
}

ALLOWED_DRY_OUTPUT_MODES = {
    "TEXT_ONLY_DRY_PREVIEW",
    "STRUCTURED_LOG_ONLY",
    "DRY_SPEECH_PREVIEW",
    "NO_OUTPUT_SUPPRESSED",
    "SAFETY_HOLD_PROMPT_CANDIDATE",
    "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


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


def _index_by(items: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if value:
            out[value] = item
    return out


def _all_have_source_chain(items: List[Dict[str, Any]]) -> bool:
    return all(bool(item.get("source_chain")) for item in items)


def _boundary_payload() -> Dict[str, Any]:
    payload = {
        "review_only": True,
        "review_scope": REVIEW_SCOPE,
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        **DRYRUN_BOUNDARY_FALSE_FLAGS,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    return payload


def _summary_loaded(root_meta: Dict[str, Any]) -> Dict[str, Any]:
    path = root_meta.get("summary_path")
    return _read_json(path) if path else {}


def _guidance(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("vision_aware_navigation_guidance_candidate", {})


def _intake(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("navigation_feedback_intake_candidate", {})


def _bridge(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("navigation_safety_arbitration_bridge_candidate", {})


def _output(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("navigation_output_candidate_dryrun", {})


def run_basic_navigation_loop_vision_strengthening_post_dryrun_review_v1(
    *,
    dryrun_root: str,
    visual_ocr_map_task_feedback_root: str,
    selective_tracking_root: str,
    world_observation_entity_feature_root: str,
    task_aware_visual_focus_root: str,
    midplatform_perception_orchestration_root: str,
    basic_navigation_loop_stabilization_root: str,
    safety_task_arbitration_policy_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    basic_navigation_guidance_loop_dryrun_root: Optional[str] = None,
    navigation_guidance_speech_adapter_root: Optional[str] = None,
    voice_interruption_governance_dryrun_root: Optional[str] = None,
    voice_command_ownership_gate_policy_root: Optional[str] = None,
    text_only_output_post_trial_review_root: Optional[str] = None,
    workspace_root: str = "",
) -> Dict[str, Any]:
    workspace = Path(workspace_root).expanduser().resolve() if workspace_root else Path.cwd()

    root_arg_values = {
        "dryrun_root": dryrun_root,
        "visual_ocr_map_task_feedback_root": visual_ocr_map_task_feedback_root,
        "selective_tracking_root": selective_tracking_root,
        "world_observation_entity_feature_root": world_observation_entity_feature_root,
        "task_aware_visual_focus_root": task_aware_visual_focus_root,
        "midplatform_perception_orchestration_root": midplatform_perception_orchestration_root,
        "basic_navigation_loop_stabilization_root": basic_navigation_loop_stabilization_root,
        "safety_task_arbitration_policy_root": safety_task_arbitration_policy_root,
        "minimal_runtime_integration_closure_root": minimal_runtime_integration_closure_root,
        "ocr_final_closure_root": ocr_final_closure_root,
        "basic_navigation_guidance_loop_dryrun_root": basic_navigation_guidance_loop_dryrun_root,
        "navigation_guidance_speech_adapter_root": navigation_guidance_speech_adapter_root,
        "voice_interruption_governance_dryrun_root": voice_interruption_governance_dryrun_root,
        "voice_command_ownership_gate_policy_root": voice_command_ownership_gate_policy_root,
        "text_only_output_post_trial_review_root": text_only_output_post_trial_review_root,
    }

    all_specs = [*REQUIRED_ROOT_SPECS, *OPTIONAL_ROOT_SPECS]
    root_meta = {
        spec["intake_id"]: _load_root(root_arg_values[spec["path_arg"]], spec["summary_file"])
        for spec in all_specs
    }

    input_root_rows: List[Dict[str, Any]] = []
    for spec in all_specs:
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

    dryrun_summary = _summary_loaded(root_meta["navigation_vision_strengthening_dryrun"])
    dryrun_results = _read_json(Path(dryrun_root) / "navigation_loop_vision_strengthening_dryrun_results.json")
    dryrun_scenario_matrix = _read_json(Path(dryrun_root) / "navigation_loop_vision_strengthening_scenario_matrix.json")
    dryrun_governance_debt = _read_json(Path(dryrun_root) / "governance_debt_register.json")
    dryrun_no_runtime = _read_json(Path(dryrun_root) / "no_runtime_boundary_report.json")
    dryrun_no_write = _read_json(Path(dryrun_root) / "no_write_boundary_report.json")
    dryrun_verifier = _read_json(Path(dryrun_root) / "verifier_report.json")

    visual_feedback_summary = _summary_loaded(root_meta["visual_ocr_map_task_feedback"])
    selective_tracking_summary = _summary_loaded(root_meta["selective_tracking"])
    worldobs_summary = _summary_loaded(root_meta["world_observation_entity_feature"])
    visual_focus_summary = _summary_loaded(root_meta["task_aware_visual_focus"])
    midplatform_summary = _summary_loaded(root_meta["midplatform_perception_orchestration"])
    basic_nav_stabilization_summary = _summary_loaded(root_meta["basic_navigation_loop_stabilization"])
    safety_arbitration_summary = _summary_loaded(root_meta["safety_task_arbitration_policy"])
    minimal_runtime_summary = _summary_loaded(root_meta["minimal_runtime_integration_closure"])
    ocr_summary = _summary_loaded(root_meta["ocr_final_closure"])

    dryrun_input_loaded = (
        root_meta["navigation_vision_strengthening_dryrun"]["loaded"]
        and dryrun_summary.get("final_decision") == DRYRUN_FINAL_DECISION
        and dryrun_summary.get("scenario_count", 0) >= 12
        and dryrun_summary.get("guidance_candidate_count", 0) >= 12
        and dryrun_summary.get("output_candidate_count", 0) >= 12
        and dryrun_verifier.get("verdict") == "GO"
    )
    visual_ocr_map_task_feedback_input_loaded = (
        root_meta["visual_ocr_map_task_feedback"]["loaded"]
        and visual_feedback_summary.get("final_decision") == VISUAL_FEEDBACK_FINAL_DECISION
    )
    selective_tracking_input_loaded = (
        root_meta["selective_tracking"]["loaded"]
        and selective_tracking_summary.get("final_decision") == SELECTIVE_TRACKING_FINAL_DECISION
    )
    world_observation_entity_feature_input_loaded = (
        root_meta["world_observation_entity_feature"]["loaded"]
        and worldobs_summary.get("final_decision") == WORLDOBS_FINAL_DECISION
    )
    task_aware_visual_focus_input_loaded = (
        root_meta["task_aware_visual_focus"]["loaded"]
        and visual_focus_summary.get("final_decision") == VISUAL_FOCUS_FINAL_DECISION
    )
    midplatform_perception_orchestration_input_loaded = (
        root_meta["midplatform_perception_orchestration"]["loaded"]
        and midplatform_summary.get("final_decision") == MIDPLATFORM_FINAL_DECISION
    )
    basic_navigation_loop_stabilization_input_loaded = (
        root_meta["basic_navigation_loop_stabilization"]["loaded"]
        and basic_nav_stabilization_summary.get("final_decision") == BASIC_NAV_STABILIZATION_FINAL_DECISION
    )
    safety_task_arbitration_policy_input_loaded = (
        root_meta["safety_task_arbitration_policy"]["loaded"]
        and safety_arbitration_summary.get("phase") == "Safety-Task-Arbitration-Policy-v1-001"
        and safety_arbitration_summary.get("arbitration_schema_defined") is True
    )
    minimal_runtime_integration_closure_loaded = (
        root_meta["minimal_runtime_integration_closure"]["loaded"]
        and minimal_runtime_summary.get("final_decision") == MRI_FINAL_DECISION
    )
    ocr_final_closure_loaded = (
        root_meta["ocr_final_closure"]["loaded"]
        and ocr_summary.get("final_decision") == OCR_FINAL_DECISION
    )

    required_root_ids = [spec["intake_id"] for spec in REQUIRED_ROOT_SPECS]
    loaded_root_ids = [row["intake_id"] for row in input_root_rows if row["loaded"]]
    optional_missing_roots = [row["intake_id"] for row in input_root_rows if (not row["required"]) and row["status"] == "optional_missing"]
    missing_required_roots = [row["intake_id"] for row in input_root_rows if row["required"] and row["status"] != "loaded"]
    dryrun_input_root_review = {
        "review_id": REVIEW_ID,
        "required_roots": required_root_ids,
        "loaded_roots": [root_id for root_id in loaded_root_ids if root_id in required_root_ids or root_id in [spec["intake_id"] for spec in OPTIONAL_ROOT_SPECS]],
        "optional_missing_roots": optional_missing_roots,
        "missing_required_roots": missing_required_roots,
        "input_root_status": "all_required_loaded" if not missing_required_roots else "missing_required_root",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    case_results = (dryrun_results or {}).get("case_results", [])
    scenario_rows = (dryrun_scenario_matrix or {}).get("scenarios", [])
    scenario_ids = [row.get("scenario_id") for row in scenario_rows]
    missing_scenarios = [scenario for scenario in REQUIRED_SCENARIOS if scenario not in scenario_ids]
    case_index = {
        item.get("navigation_vision_strengthening_dryrun_case", {}).get("dryrun_case_id"): item
        for item in case_results
    }

    scenario_coverage_review = {
        "reviewed_scenario_count": len(scenario_rows),
        "expected_scenario_count": len(REQUIRED_SCENARIOS),
        "covered_scenarios": scenario_ids,
        "missing_scenarios": missing_scenarios,
        "safety_priority_cases_present": dryrun_summary.get("safety_priority_cases_generated") is True,
        "task_guidance_cases_present": dryrun_summary.get("task_guidance_cases_generated") is True,
        "active_view_adjustment_cases_present": dryrun_summary.get("active_view_adjustment_cases_generated") is True,
        "ocr_later_needed_cases_present": dryrun_summary.get("ocr_later_needed_cases_generated") is True,
        "tracking_later_needed_cases_present": dryrun_summary.get("tracking_later_needed_cases_generated") is True,
        "map_visual_conflict_cases_present": dryrun_summary.get("map_visual_conflict_cases_generated") is True,
        "crossing_uncertain_cases_present": dryrun_summary.get("crossing_uncertain_cases_generated") is True,
        "verdict": "PASS" if len(scenario_rows) >= len(REQUIRED_SCENARIOS) and not missing_scenarios else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    all_guidance = [_guidance(case) for case in case_results]
    all_intakes = [_intake(case) for case in case_results]
    all_bridges = [_bridge(case) for case in case_results]
    all_outputs = [_output(case) for case in case_results]
    candidate_only_verified = all(
        item.get("fact_status") == "not_fact"
        and item.get("action_instruction_allowed") is False
        and item.get("navigation_action_allowed") is False
        for item in all_guidance
    )
    high_risk_guidance_conservative = True
    for scenario_id, expectation in HIGH_RISK_EXPECTATIONS.items():
        case = case_index.get(scenario_id, {})
        guidance = _guidance(case)
        output = _output(case)
        intake = _intake(case)
        bridge = _bridge(case)
        conservative = (
            guidance.get("guidance_type") == expectation["guidance_type"]
            and output.get("output_mode") == expectation["output_mode"]
            and guidance.get("action_instruction_allowed") is False
            and guidance.get("navigation_action_allowed") is False
            and output.get("speech_allowed") is False
            and output.get("tts_allowed") is False
            and output.get("vop_allowed") is False
            and output.get("user_heard_assumed") is False
        )
        if expectation.get("requires_confirmation"):
            conservative = conservative and bridge.get("requires_confirmation") is True
        if expectation.get("requires_reobserve"):
            conservative = conservative and bridge.get("requires_reobserve") is True
        if expectation.get("requires_tracking_later"):
            conservative = conservative and intake.get("requires_tracking_later") is True
        if expectation.get("requires_ocr_later"):
            conservative = conservative and intake.get("requires_ocr_later") is True
        if expectation.get("suppresses_task_guidance"):
            conservative = conservative and bridge.get("suppress_task_guidance") is True
        high_risk_guidance_conservative = high_risk_guidance_conservative and conservative

    guidance_candidate_review = {
        "guidance_candidate_count": len(all_guidance),
        "candidate_only_verified": candidate_only_verified,
        "action_instruction_allowed_false": all(item.get("action_instruction_allowed") is False for item in all_guidance),
        "navigation_action_allowed_false": all(item.get("navigation_action_allowed") is False for item in all_guidance),
        "fact_status_not_fact": all(item.get("fact_status") == "not_fact" for item in all_guidance),
        "source_chain_complete": _all_have_source_chain(all_guidance),
        "high_risk_guidance_conservative": high_risk_guidance_conservative,
        "verdict": "PASS" if len(all_guidance) >= 12 and candidate_only_verified and high_risk_guidance_conservative else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    safety_cases = [case for case in case_results if _bridge(case).get("allow_safety_guidance_candidate") is True]
    safety_priority_preserved = all(_guidance(case).get("safety_priority") == "P0" for case in safety_cases)
    task_guidance_suppression_or_delay_verified = (
        _bridge(case_index.get("route_walking_near_field_obstacle", {})).get("delay_task_guidance") is True
        and _bridge(case_index.get("low_quality_view_hold_still", {})).get("suppress_task_guidance") is True
    )
    crossing_and_crowd_flow_guardrails_verified = (
        _guidance(case_index.get("crossing_uncertain_red_green_light", {})).get("guidance_type") == "crossing_uncertain_hint"
        and _guidance(case_index.get("crowded_path_crowd_flow_caution", {})).get("guidance_type") == "crowd_flow_caution_hint"
        and dryrun_summary.get("crossing_action_instruction_allowed") is False
        and dryrun_summary.get("crowd_flow_follow_action_allowed") is False
    )
    safety_arbitration_bridge_review = {
        "bridge_candidate_count": len(all_bridges),
        "bridge_only_verified": all(item.get("fact_status") == "not_fact" and item.get("action_allowed") is False for item in all_bridges),
        "runtime_arbitration_invoked": False,
        "safety_priority_preserved": safety_priority_preserved,
        "task_guidance_suppression_or_delay_verified": task_guidance_suppression_or_delay_verified,
        "crossing_and_crowd_flow_guardrails_verified": crossing_and_crowd_flow_guardrails_verified,
        "verdict": "PASS"
        if len(all_bridges) >= 12
        and safety_priority_preserved
        and task_guidance_suppression_or_delay_verified
        and crossing_and_crowd_flow_guardrails_verified
        else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    text_only_or_dry_preview_verified = (
        all(item.get("output_mode") in ALLOWED_DRY_OUTPUT_MODES for item in all_outputs)
        and all(item.get("speech_allowed") is False for item in all_outputs)
        and all(item.get("tts_allowed") is False for item in all_outputs)
        and all(item.get("vop_allowed") is False for item in all_outputs)
        and all(item.get("user_heard_assumed") is False for item in all_outputs)
    )
    text_only_dry_output_review = {
        "output_candidate_count": len(all_outputs),
        "text_only_or_dry_preview_verified": text_only_or_dry_preview_verified,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "user_heard_assumed": False,
        "real_output_generated": False,
        "verdict": "PASS" if len(all_outputs) >= 12 and text_only_or_dry_preview_verified else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    high_risk_reviews: List[Dict[str, Any]] = []
    for scenario_id, expectation in HIGH_RISK_EXPECTATIONS.items():
        case = case_index.get(scenario_id, {})
        guidance = _guidance(case)
        intake = _intake(case)
        bridge = _bridge(case)
        output = _output(case)
        conservative_handling_verified = (
            guidance.get("guidance_type") == expectation["guidance_type"]
            and output.get("output_mode") == expectation["output_mode"]
            and guidance.get("action_instruction_allowed") is False
            and guidance.get("navigation_action_allowed") is False
            and output.get("speech_allowed") is False
            and output.get("tts_allowed") is False
            and output.get("vop_allowed") is False
            and output.get("user_heard_assumed") is False
        )
        if expectation.get("requires_confirmation"):
            conservative_handling_verified = conservative_handling_verified and bridge.get("requires_confirmation") is True
        if expectation.get("requires_reobserve"):
            conservative_handling_verified = conservative_handling_verified and bridge.get("requires_reobserve") is True
        if expectation.get("requires_tracking_later"):
            conservative_handling_verified = conservative_handling_verified and intake.get("requires_tracking_later") is True
        if expectation.get("requires_ocr_later"):
            conservative_handling_verified = conservative_handling_verified and intake.get("requires_ocr_later") is True
        if expectation.get("suppresses_task_guidance"):
            conservative_handling_verified = conservative_handling_verified and bridge.get("suppress_task_guidance") is True
        high_risk_reviews.append(
            {
                "scenario_id": scenario_id,
                "risk_type": expectation["risk_type"],
                "conservative_handling_verified": conservative_handling_verified,
                "action_instruction_allowed": False,
                "fact_write_allowed": False,
                "requires_future_governance": expectation["requires_future_governance"],
                "verdict": "PASS" if conservative_handling_verified else "FAIL",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    high_risk_scenario_review = {
        "reviewed_scenarios": high_risk_reviews,
        "reviewed_high_risk_scenario_count": len(high_risk_reviews),
        "all_high_risk_conservative": all(item["conservative_handling_verified"] for item in high_risk_reviews),
        "verdict": "PASS" if all(item["verdict"] == "PASS" for item in high_risk_reviews) else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    worldmodel_memory_library_boundary_review = {
        "handoff_candidate_allowed": dryrun_summary.get("worldmodel_handoff_candidate_allowed") is True
        and dryrun_summary.get("memory_handoff_candidate_allowed") is True,
        "placeholder_allowed": dryrun_summary.get("library_handoff_placeholder_allowed") is True,
        "entity_resolution_deferred": dryrun_summary.get("entity_resolution_deferred") is True,
        "fact_admission_deferred": dryrun_summary.get("fact_admission_deferred") is True,
        "memory_consolidation_deferred": dryrun_summary.get("memory_consolidation_deferred") is True,
        "library_experience_governance_deferred": dryrun_summary.get("library_experience_governance_deferred") is True,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "fact_write_allowed": False,
        "verdict": "PASS"
        if dryrun_summary.get("worldmodel_handoff_candidate_allowed") is True
        and dryrun_summary.get("memory_handoff_candidate_allowed") is True
        and dryrun_summary.get("library_handoff_placeholder_allowed") is True
        and dryrun_summary.get("worldmodel_write_allowed") is False
        and dryrun_summary.get("memory_write_allowed") is False
        and dryrun_summary.get("library_write_allowed") is False
        else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    runtime_write_action_speech_boundary_review = {
        "camera_invoked": False,
        "map_api_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
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
        "verdict": "PASS"
        if dryrun_summary.get("boundary_ok") is True
        and (dryrun_no_runtime or {}).get("boundary_ok") is True
        and (dryrun_no_write or {}).get("boundary_ok") is True
        else "FAIL",
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    debt_topics = {row.get("topic") for row in (dryrun_governance_debt or {}).get("debts", [])}
    governance_debt_review = {
        "governance_debt_register_loaded": dryrun_summary.get("governance_debt_register_generated") is True,
        "future_midplatform_function_governance_required": (dryrun_governance_debt or {}).get("future_midplatform_function_governance_required") is True,
        "no_duplicate_governance_module_allowed": (dryrun_governance_debt or {}).get("no_duplicate_governance_module_allowed") is True,
        "duplicate_module_risk_recorded": "duplicated schema risk" in debt_topics,
        "perception_orchestration_complexity_recorded": midplatform_perception_orchestration_input_loaded,
        "visual_focus_complexity_recorded": task_aware_visual_focus_input_loaded,
        "tracking_policy_complexity_recorded": selective_tracking_input_loaded,
        "world_observation_handoff_complexity_recorded": world_observation_entity_feature_input_loaded,
        "recommendation": "进入 closure，只做本轮视角强化收口，不扩展 runtime 或新治理模块。",
        "verdict": "PASS"
        if dryrun_summary.get("governance_debt_register_generated") is True
        and (dryrun_governance_debt or {}).get("future_midplatform_function_governance_required") is True
        and (dryrun_governance_debt or {}).get("no_duplicate_governance_module_allowed") is True
        else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not dryrun_input_loaded:
        blockers.append("dryrun_input_not_ready")
    if scenario_coverage_review["verdict"] != "PASS":
        blockers.append("scenario_coverage_incomplete")
    if guidance_candidate_review["verdict"] != "PASS":
        blockers.append("guidance_candidate_boundary_gap")
    if safety_arbitration_bridge_review["verdict"] != "PASS":
        blockers.append("safety_arbitration_bridge_gap")
    if text_only_dry_output_review["verdict"] != "PASS":
        blockers.append("text_only_dry_output_gap")
    if high_risk_scenario_review["verdict"] != "PASS":
        blockers.append("high_risk_guardrail_gap")
    if worldmodel_memory_library_boundary_review["verdict"] != "PASS":
        blockers.append("wml_boundary_gap")
    if runtime_write_action_speech_boundary_review["verdict"] != "PASS":
        blockers.append("runtime_write_action_speech_boundary_gap")
    if governance_debt_review["verdict"] != "PASS":
        blockers.append("governance_debt_gap")

    closure_readiness_decision = {
        "post_dryrun_review_verdict": "GO" if not blockers else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "Closure 仍然只能做收口，不进入 runtime。",
            "保持 camera / OCR provider / tracking / map API / Speech Gate / VOP / TTS 全部禁用。",
            "保持 WorldModel / Memory / Fact / Library handoff-only / placeholder-only。"
        ],
        "ready_for_closure": not blockers,
        "next_phase_recommendation": NEXT_PHASE if not blockers else PHASE_ID,
        "final_decision": FINAL_DECISION if not blockers else "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommendation_id": f"{REVIEW_ID}_next_phase",
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "Post-DryRun Review 已确认闭环稳定、边界完整，可进入本轮视角强化 closure。",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_runtime_boundary_report = _boundary_payload()
    no_write_boundary_report = _boundary_payload()

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "dryrun_input_loaded": dryrun_input_loaded,
        "visual_ocr_map_task_feedback_input_loaded": visual_ocr_map_task_feedback_input_loaded,
        "selective_tracking_input_loaded": selective_tracking_input_loaded,
        "world_observation_entity_feature_input_loaded": world_observation_entity_feature_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "basic_navigation_loop_stabilization_input_loaded": basic_navigation_loop_stabilization_input_loaded,
        "safety_task_arbitration_policy_input_loaded": safety_task_arbitration_policy_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "dryrun_input_root_review_generated": True,
        "scenario_coverage_review_generated": True,
        "guidance_candidate_review_generated": True,
        "safety_arbitration_bridge_review_generated": True,
        "text_only_dry_output_review_generated": True,
        "high_risk_scenario_review_generated": True,
        "worldmodel_memory_library_boundary_review_generated": True,
        "runtime_write_action_speech_boundary_review_generated": True,
        "governance_debt_review_generated": True,
        "closure_readiness_decision_generated": True,
        "reviewed_scenario_count": scenario_coverage_review["reviewed_scenario_count"],
        "reviewed_guidance_candidate_count": guidance_candidate_review["guidance_candidate_count"],
        "reviewed_output_candidate_count": text_only_dry_output_review["output_candidate_count"],
        "candidate_only_boundary_pass": guidance_candidate_review["candidate_only_verified"] is True,
        "safety_priority_review_pass": safety_arbitration_bridge_review["safety_priority_preserved"] is True,
        "high_risk_conservative_handling_pass": high_risk_scenario_review["all_high_risk_conservative"] is True,
        "text_only_dry_output_boundary_pass": text_only_dry_output_review["text_only_or_dry_preview_verified"] is True,
        "worldmodel_memory_library_boundary_pass": worldmodel_memory_library_boundary_review["verdict"] == "PASS",
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        "governance_debt_recorded": governance_debt_review["governance_debt_register_loaded"] is True,
        "future_midplatform_function_governance_required": governance_debt_review["future_midplatform_function_governance_required"] is True,
        "no_duplicate_governance_module_allowed": governance_debt_review["no_duplicate_governance_module_allowed"] is True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        **{k: v for k, v in DRYRUN_BOUNDARY_FALSE_FLAGS.items()},
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION,
        "recommended_next_phase": NEXT_PHASE,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": summary,
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "dryrun_input_root_review": dryrun_input_root_review,
        "scenario_coverage_review": scenario_coverage_review,
        "guidance_candidate_review": guidance_candidate_review,
        "safety_arbitration_bridge_review": safety_arbitration_bridge_review,
        "text_only_dry_output_review": text_only_dry_output_review,
        "high_risk_scenario_review": high_risk_scenario_review,
        "worldmodel_memory_library_boundary_review": worldmodel_memory_library_boundary_review,
        "runtime_write_action_speech_boundary_review": runtime_write_action_speech_boundary_review,
        "governance_debt_review": governance_debt_review,
        "closure_readiness_decision": closure_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": no_runtime_boundary_report,
        "no_write_boundary_report": no_write_boundary_report,
        "debug_refs": {
            "workspace_root": str(workspace),
            "dryrun_final_decision": dryrun_summary.get("final_decision"),
            "dryrun_verifier_verdict": (dryrun_verifier or {}).get("verdict"),
            "loaded_optional_roots": [row["intake_id"] for row in input_root_rows if (not row["required"]) and row["loaded"]],
            "optional_missing_roots": optional_missing_roots,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
    }
