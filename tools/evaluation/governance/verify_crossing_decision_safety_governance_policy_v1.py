#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Crossing Decision Safety Governance Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Crossing-Decision-Safety-Governance-Policy-v1-001"
FINAL_DECISION = "CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY_READY_FOR_CROSSING_DECISION_DRYRUN"
NEXT_PHASE = "Phase-Crossing-Decision-DryRun-v1-001"
MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160

EXPECTED_EVIDENCE_TYPES = [
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

EXPECTED_SCHEMA_FIELDS = [
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

EXPECTED_CONFLICT_CASES = [
    "green_light_vs_vehicle_flow_conflict",
    "map_crossing_hint_vs_visual_absence",
    "crowd_flow_vs_traffic_uncertain",
    "ocr_countdown_vs_traffic_light_uncertain",
    "route_says_cross_vs_safety_uncertain",
    "user_instruction_vs_safety_boundary",
    "stale_memory_vs_current_observation",
    "audio_cue_vs_visual_uncertain",
]

EXPECTED_FORBIDDEN_OUTPUTS = [
    "CROSS_NOW",
    "SAFE_TO_CROSS",
    "GO_AHEAD",
    "PROCEED",
    "FOLLOW_THE_CROWD",
    "GREEN_LIGHT_GO",
    "MAP_SAYS_CROSS",
    "COUNTDOWN_SAYS_GO",
]

EXPECTED_ALLOWED_OUTPUTS = [
    "NO_OUTPUT_SUPPRESSED",
    "SAFETY_HOLD_CANDIDATE",
    "REOBSERVE_CANDIDATE",
    "HUMAN_ASSISTANCE_CANDIDATE",
    "LOW_CONFIDENCE_WARNING_CANDIDATE",
    "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE",
    "TEXT_ONLY_DRY_PREVIEW",
]

EXPECTED_SCENARIOS = [
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
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/crossing_decision_safety_governance_policy_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    crossing_decision_safety_governance_policy = _load_json(root / "crossing_decision_safety_governance_policy.json")
    crossing_evidence_candidate_schema = _load_json(root / "crossing_evidence_candidate_schema.json")
    crossing_permission_boundary_policy = _load_json(root / "crossing_permission_boundary_policy.json")
    crossing_uncertainty_policy = _load_json(root / "crossing_uncertainty_policy.json")
    crossing_conflict_policy = _load_json(root / "crossing_conflict_policy.json")
    crossing_output_policy = _load_json(root / "crossing_output_policy.json")
    crossing_human_assistance_policy = _load_json(root / "crossing_human_assistance_policy.json")
    crossing_safety_scenario_matrix = _load_json(root / "crossing_safety_scenario_matrix.json")
    crossing_boundary_matrix = _load_json(root / "crossing_boundary_matrix.json")
    safety_constitution_inheritance_matrix = _load_json(root / "safety_constitution_inheritance_matrix.json")
    forbidden_crossing_output_register = _load_json(root / "forbidden_crossing_output_register.json")
    governance_debt_register = _load_json(root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
        "safety_constitution",
        "post_controlled_frame_roadmap_decision",
        "controlled_frame_input_closure",
        "map_location_readonly_context",
        "vision_strengthening_closure",
        "safety_task_arbitration_policy",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}", idx.get(intake_id, {}).get("loaded") is True)
    for intake_id in (
        "task_aware_visual_focus_policy",
        "selective_tracking_adapter_policy",
        "visual_ocr_map_task_feedback_dryrun",
        "basic_navigation_loop_vision_strengthening_dryrun",
        "minimal_runtime_controlled_output_definition",
        "minimal_runtime_text_only_output_post_review",
        "voice_command_ownership_gate_policy",
        "voice_interruption_governance_dryrun",
        "gps_route_context_dryrun",
        "worldmodel_lookup_framework",
    ):
        status = idx.get(intake_id, {}).get("status")
        ok(f"input.{intake_id}.optional", status in {"loaded", "optional_missing"}, status)
    ok("input.row_count", input_root_matrix.get("row_count") == len(rows), input_root_matrix.get("row_count"))

    for key in (
        "safety_constitution_input_loaded",
        "post_controlled_frame_roadmap_decision_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "safety_task_arbitration_policy_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "crossing_decision_safety_governance_policy_defined",
        "crossing_evidence_candidate_schema_defined",
        "crossing_permission_boundary_policy_defined",
        "crossing_uncertainty_policy_defined",
        "crossing_conflict_policy_defined",
        "crossing_output_policy_defined",
        "crossing_human_assistance_policy_defined",
        "safety_constitution_inheritance_matrix_generated",
        "forbidden_crossing_output_register_generated",
        "scenario_matrix_generated",
        "inherits_safety_constitution",
        "traffic_light_candidate_not_crossing_permission",
        "green_light_candidate_not_crossing_permission",
        "countdown_text_candidate_not_crossing_permission",
        "crowd_flow_candidate_not_crossing_permission",
        "pedestrian_flow_candidate_not_crossing_permission",
        "map_crossing_hint_not_crossing_permission",
        "route_crossing_hint_not_crossing_permission",
        "user_says_go_not_crossing_permission",
        "single_modality_evidence_not_crossing_permission",
        "stale_evidence_not_crossing_permission",
        "conflicting_evidence_not_crossing_permission",
        "low_confidence_evidence_not_crossing_permission",
        "conflict_blocks_crossing_action",
        "uncertainty_requires_hold_or_confirm",
        "human_assistance_candidate_allowed",
        "speech_allowed_false_until_gate",
        "action_allowed_false",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)
    ok("summary.policy_scope", summary.get("policy_scope") == "crossing_decision_safety_governance_policy_only")
    ok("summary.scenario_count", summary.get("scenario_count", 0) >= 14, summary.get("scenario_count"))
    for key in (
        "crossing_runtime_allowed",
        "crossing_permission_output_allowed",
        "crossing_action_instruction_allowed",
        "safe_to_cross_claim_allowed",
        "human_assistance_obtained_assumed",
        "navigation_action_allowed",
        "crossing_decision_runtime_invoked",
        "camera_invoked",
        "visual_model_invoked",
        "map_api_invoked",
        "gaode_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    ok("summary.fact_status_not_fact", summary.get("fact_status_not_fact") is True)
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("policy.id", crossing_decision_safety_governance_policy.get("policy_id") == "cdsgp_v1_001")
    ok("policy.scope", crossing_decision_safety_governance_policy.get("policy_scope") == "crossing_decision_safety_governance_policy_only")
    ok("policy.inherited_ref", isinstance(crossing_decision_safety_governance_policy.get("inherited_safety_constitution_ref"), str) and crossing_decision_safety_governance_policy.get("inherited_safety_constitution_ref").endswith(".json"))
    for key in (
        "crossing_evidence_boundary_ref",
        "crossing_permission_boundary_ref",
        "crossing_uncertainty_policy_ref",
        "crossing_conflict_policy_ref",
        "crossing_output_policy_ref",
        "crossing_human_assistance_policy_ref",
        "no_runtime_boundary_ref",
        "no_write_boundary_ref",
    ):
        ok(f"policy.{key}", isinstance(crossing_decision_safety_governance_policy.get(key), str) and crossing_decision_safety_governance_policy.get(key).endswith(".json"))
    ok("policy.inherits_safety_constitution", crossing_decision_safety_governance_policy.get("inherits_safety_constitution") is True)
    ok("policy.policy_only", crossing_decision_safety_governance_policy.get("crossing_governance_is_policy_only") is True)
    ok("policy.crossing_runtime_allowed", crossing_decision_safety_governance_policy.get("crossing_runtime_allowed") is False)
    ok("policy.crossing_permission_output_allowed", crossing_decision_safety_governance_policy.get("crossing_permission_output_allowed") is False)
    ok("policy.crossing_action_instruction_allowed", crossing_decision_safety_governance_policy.get("crossing_action_instruction_allowed") is False)
    ok("policy.current_phase_cannot_decide_safe_to_cross", crossing_decision_safety_governance_policy.get("current_phase_cannot_decide_safe_to_cross") is True)

    evidence_types = set(crossing_evidence_candidate_schema.get("allowed_evidence_types", []))
    schema_fields = set(crossing_evidence_candidate_schema.get("schema_fields", []))
    for evidence_type in EXPECTED_EVIDENCE_TYPES:
        ok(f"evidence_type.{evidence_type}", evidence_type in evidence_types)
    for field_name in EXPECTED_SCHEMA_FIELDS:
        ok(f"schema_field.{field_name}", field_name in schema_fields)
    defaults = crossing_evidence_candidate_schema.get("default_constraints", {})
    ok("schema.default.current_action_allowed", defaults.get("current_action_allowed") is False)
    ok("schema.default.crossing_permission_allowed", defaults.get("crossing_permission_allowed") is False)
    ok("schema.default.fact_status", defaults.get("fact_status") == "not_fact")

    for key in (
        "traffic_light_candidate_not_crossing_permission",
        "green_light_candidate_not_crossing_permission",
        "countdown_text_candidate_not_crossing_permission",
        "crowd_flow_candidate_not_crossing_permission",
        "pedestrian_flow_candidate_not_crossing_permission",
        "map_crossing_hint_not_crossing_permission",
        "route_crossing_hint_not_crossing_permission",
        "user_says_go_not_crossing_permission",
        "memory_hint_not_crossing_permission",
        "single_modality_evidence_not_crossing_permission",
        "stale_evidence_not_crossing_permission",
        "conflicting_evidence_not_crossing_permission",
        "low_confidence_evidence_not_crossing_permission",
        "inherits_safety_constitution",
    ):
        ok(f"permission_boundary.{key}", crossing_permission_boundary_policy.get(key) is True)
    for key in (
        "crossing_permission_output_allowed",
        "crossing_action_instruction_allowed",
        "safe_to_cross_claim_allowed",
    ):
        ok(f"permission_boundary.{key}", crossing_permission_boundary_policy.get(key) is False)

    uncertainty_rules = {row.get("uncertainty_case"): row for row in crossing_uncertainty_policy.get("rules", [])}
    expected_rule_targets = {
        "insufficient_evidence": "HOLD_OR_CONFIRM_CANDIDATE",
        "low_confidence": "HOLD_OR_CONFIRM_CANDIDATE",
        "stale_evidence": "REOBSERVE_CANDIDATE",
        "conflicting_evidence": "REOBSERVE_OR_HUMAN_ASSISTANCE_CANDIDATE",
        "occluded_vehicle_flow": "DO_NOT_ADVANCE_CANDIDATE",
        "traffic_light_uncertain": "DO_NOT_ADVANCE_CANDIDATE",
        "no_crosswalk_detected": "DO_NOT_CROSS_CANDIDATE",
        "map_only_crossing_hint": "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE",
    }
    for case_name, target in expected_rule_targets.items():
        row = uncertainty_rules.get(case_name, {})
        ok(f"uncertainty_rule.{case_name}.present", case_name in uncertainty_rules)
        ok(f"uncertainty_rule.{case_name}.target", row.get("required_candidate") == target, row.get("required_candidate"))
        ok(f"uncertainty_rule.{case_name}.crossing_permission_allowed", row.get("crossing_permission_allowed") is False)
    ok("uncertainty.requires_hold_or_confirm", crossing_uncertainty_policy.get("uncertainty_requires_hold_or_confirm") is True)

    conflict_cases = set(crossing_conflict_policy.get("conflict_cases", []))
    generated_candidates = set(crossing_conflict_policy.get("generated_candidates", []))
    for case_name in EXPECTED_CONFLICT_CASES:
        ok(f"conflict_case.{case_name}", case_name in conflict_cases)
    for candidate_name in ("CrossingConflictCandidate", "ReobserveRequestCandidate", "HumanAssistanceCandidate", "SafetyHoldCandidate"):
        ok(f"conflict_generated.{candidate_name}", candidate_name in generated_candidates)
    principles = crossing_conflict_policy.get("principles", {})
    for key in (
        "conflict_blocks_crossing_action",
        "conflict_cannot_be_resolved_by_LLM_guess",
        "conflict_cannot_be_resolved_by_map_alone",
        "conflict_cannot_be_resolved_by_user_command_alone",
        "conflict_requires_reobserve_hold_or_human_assistance",
    ):
        ok(f"conflict_principle.{key}", principles.get(key) is True)

    allowed_outputs = set(crossing_output_policy.get("allowed_output_modes", []))
    forbidden_outputs = set(crossing_output_policy.get("forbidden_output_modes", []))
    for output_name in EXPECTED_ALLOWED_OUTPUTS:
        ok(f"allowed_output.{output_name}", output_name in allowed_outputs)
    for output_name in EXPECTED_FORBIDDEN_OUTPUTS:
        ok(f"forbidden_output.{output_name}", output_name in forbidden_outputs)
    ok("output_policy.speech_allowed", crossing_output_policy.get("speech_allowed") is False)
    ok("output_policy.user_heard_assumed", crossing_output_policy.get("user_heard_assumed") is False)
    ok("output_policy.action_allowed", crossing_output_policy.get("action_allowed") is False)
    ok("output_policy.navigation_action_allowed", crossing_output_policy.get("navigation_action_allowed") is False)
    ok("output_policy.crossing_permission_output_allowed", crossing_output_policy.get("crossing_permission_output_allowed") is False)
    ok("output_policy.crossing_action_instruction_allowed", crossing_output_policy.get("crossing_action_instruction_allowed") is False)
    ok("output_policy.safe_to_cross_claim_allowed", crossing_output_policy.get("safe_to_cross_claim_allowed") is False)

    for key in (
        "tell_user_information_is_insufficient_when",
        "human_assistance_candidate_allowed",
        "no_real_speech_output",
        "no_task_state_commit",
        "no_navigation_action",
    ):
        ok(f"human_policy.{key}", crossing_human_assistance_policy.get(key) is True)
    ok("human_policy.human_assistance_obtained_assumed", crossing_human_assistance_policy.get("human_assistance_obtained_assumed") is False)
    for key in (
        "ask_human_assistance_when",
        "seek_staff_assistance_when",
        "stop_and_wait_when",
        "ask_user_to_confirm_visually_or_auditorily_when",
    ):
        ok(f"human_policy.{key}", isinstance(crossing_human_assistance_policy.get(key), list) and len(crossing_human_assistance_policy.get(key, [])) >= 2)

    scenario_rows = crossing_safety_scenario_matrix.get("scenarios", [])
    scenario_idx = {row.get("scenario_id"): row for row in scenario_rows}
    ok("scenario_matrix.count", crossing_safety_scenario_matrix.get("scenario_count", 0) >= 14, crossing_safety_scenario_matrix.get("scenario_count"))
    for scenario_id in EXPECTED_SCENARIOS:
        row = scenario_idx.get(scenario_id, {})
        ok(f"scenario.{scenario_id}.present", scenario_id in scenario_idx)
        ok(f"scenario.{scenario_id}.trigger_note", isinstance(row.get("trigger_note"), str) and bool(row.get("trigger_note")))
        ok(f"scenario.{scenario_id}.expected_outcome", isinstance(row.get("expected_outcome"), str) and bool(row.get("expected_outcome")))
        ok(f"scenario.{scenario_id}.crossing_permission_allowed", row.get("crossing_permission_allowed") is False)
        ok(f"scenario.{scenario_id}.crossing_action_instruction_allowed", row.get("crossing_action_instruction_allowed") is False)
        ok(f"scenario.{scenario_id}.safe_to_cross_claim_allowed", row.get("safe_to_cross_claim_allowed") is False)
        ok(f"scenario.{scenario_id}.fact_status", row.get("fact_status") == "not_fact")

    ok("boundary_matrix.policy_scope", crossing_boundary_matrix.get("policy_scope") == "crossing_decision_safety_governance_policy_only")
    for key in (
        "crossing_runtime_allowed",
        "crossing_permission_output_allowed",
        "crossing_action_instruction_allowed",
        "safe_to_cross_claim_allowed",
        "action_allowed",
        "navigation_action_allowed",
        "speech_allowed",
    ):
        ok(f"boundary_matrix.{key}", crossing_boundary_matrix.get(key) is False)
    ok("boundary_matrix.fact_status_not_fact", crossing_boundary_matrix.get("fact_status_not_fact") is True)

    ok("inheritance.inherits_safety_constitution", safety_constitution_inheritance_matrix.get("inherits_safety_constitution") is True)
    ok("inheritance.inherited_principles_count", len(safety_constitution_inheritance_matrix.get("inherited_principles", [])) >= 8)
    for key in (
        "traffic_light_candidate_not_crossing_permission",
        "green_light_candidate_not_crossing_permission",
        "map_crossing_hint_not_crossing_permission",
        "crowd_flow_candidate_not_crossing_permission",
        "OCR_countdown_text_not_crossing_permission",
        "user_says_go_not_crossing_permission",
        "navigation_route_says_cross_not_crossing_permission",
        "crossing_decision_requires_special_safety_governance",
    ):
        ok(f"inheritance.constraint.{key}", safety_constitution_inheritance_matrix.get("inherited_crossing_constraints", {}).get(key) is True)

    forbidden_register_set = set(forbidden_crossing_output_register.get("forbidden_outputs", []))
    ok("forbidden_register.count", forbidden_crossing_output_register.get("forbidden_count") == len(EXPECTED_FORBIDDEN_OUTPUTS), forbidden_crossing_output_register.get("forbidden_count"))
    for output_name in EXPECTED_FORBIDDEN_OUTPUTS:
        ok(f"forbidden_register.{output_name}", output_name in forbidden_register_set)

    ok("debt.count", len(governance_debt_register.get("carryover_topics", [])) >= 8, len(governance_debt_register.get("carryover_topics", [])))
    ok("debt.crossing_dryrun_required_next", governance_debt_register.get("crossing_dryrun_required_next") is True)
    ok("debt.controlled_sample_before_runtime", governance_debt_register.get("controlled_sample_before_runtime_still_required") is True)
    ok("debt.speech_gate_deferred", governance_debt_register.get("speech_gate_for_crossing_output_still_deferred") is True)

    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended_next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)
    ok("next_phase.reason", isinstance(next_phase_recommendation.get("reason"), str) and bool(next_phase_recommendation.get("reason")))

    for report_name, report in (
        ("no_runtime_boundary_report", no_runtime_boundary_report),
        ("no_write_boundary_report", no_write_boundary_report),
    ):
        ok(f"{report_name}.policy_scope", report.get("policy_scope") == "crossing_decision_safety_governance_policy_only")
        ok(f"{report_name}.no_runtime_executed", report.get("no_runtime_executed") is True)
        ok(f"{report_name}.no_new_runtime_enabled", report.get("no_new_runtime_enabled") is True)
        ok(f"{report_name}.boundary_ok", report.get("boundary_ok") is True)
        for key in (
            "crossing_decision_runtime_invoked",
            "camera_invoked",
            "visual_model_invoked",
            "map_api_invoked",
            "gaode_api_invoked",
            "gps_runtime_invoked",
            "ocr_provider_invoked",
            "ocrrequest_submitted",
            "tracking_runtime_invoked",
            "optical_flow_runtime_invoked",
            "speech_gate_invoked",
            "vop_invoked",
            "tts_invoked",
            "task_state_committed_now",
            "navigation_action_triggered",
            "route_modified",
            "scene_delta_generated",
            "world_model_written",
            "memory_written",
            "library_written",
            "fact_written",
        ):
            ok(f"{report_name}.{key}", report.get(key) is False)
        ok(f"{report_name}.violations", report.get("violations") == [])

    passed_count = sum(1 for check in checks if check["passed"])
    verifier_report = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "check_count": len(checks),
        "passed_count": passed_count,
        "failed_count": len(checks) - passed_count,
        "verifier": "GO" if len(checks) >= MIN_CHECKS and passed_count == len(checks) else "NO_GO",
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": verifier_report["verifier"],
                "check_count": verifier_report["check_count"],
                "passed_count": verifier_report["passed_count"],
                "failed_count": verifier_report["failed_count"],
                "final_decision": verifier_report["final_decision"],
                "recommended_next_phase": verifier_report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier_report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
