#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Safety Constitution Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Luna-Safety-Constitution-Policy-v1-001"
FINAL_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
NEXT_PHASE = "Phase-Crossing-Decision-Safety-Governance-Policy-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140

EXPECTED_HIGH_RISK_DOMAINS = [
    "crossing_decision",
    "traffic_light_decision",
    "vehicle_flow_decision",
    "crowd_flow_following",
    "navigation_action",
    "medical_advice",
    "financial_decision",
    "legal_decision",
    "identity_recognition",
    "voice_command_ownership",
    "face_voice_identity",
    "privacy_sensitive_context",
    "emotional_intervention",
    "self_harm_or_extreme_distress",
    "memory_fact_write",
    "worldmodel_fact_admission",
    "library_experience_reuse",
    "exploration_drive",
]

EXPECTED_SCENARIOS = [
    "crossing_green_light_candidate",
    "crowd_flow_crossing_candidate",
    "map_says_crossing_ahead",
    "ocr_countdown_text_candidate",
    "user_says_go_cross",
    "low_confidence_obstacle",
    "map_visual_conflict",
    "medical_advice_high_risk",
    "financial_decision_high_risk",
    "emotional_intervention_sensitive",
    "memory_hint_stale",
    "unknown_speaker_emergency_keyword",
]

EXPECTED_SURVIVAL_SCOPE = [
    "safety",
    "robustness",
    "local minimum safety path",
    "offline availability",
    "resource preservation",
    "degraded operation",
    "self-protection",
    "user protection",
    "environment adaptation",
    "exploration drive boundary",
    "midplatform failure fallback",
    "multi-device redundancy",
    "privacy and ethics baseline",
    "emotion engine anti-manipulation",
    "distributed midplatform survival mode",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/luna_safety_constitution_policy_v1_smoke_v0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    luna_safety_constitution_policy = _load_json(root / "luna_safety_constitution_policy.json")
    global_safety_principles = _load_json(root / "global_safety_principles.json")
    high_risk_domain_matrix = _load_json(root / "high_risk_domain_matrix.json")
    evidence_boundary_policy = _load_json(root / "evidence_boundary_policy.json")
    uncertainty_output_policy = _load_json(root / "uncertainty_output_policy.json")
    user_instruction_boundary_policy = _load_json(root / "user_instruction_boundary_policy.json")
    action_authority_boundary_policy = _load_json(root / "action_authority_boundary_policy.json")
    crossing_safety_inheritance_policy = _load_json(root / "crossing_safety_inheritance_policy.json")
    future_survival_constitution_upgrade_path = _load_json(root / "future_survival_constitution_upgrade_path.json")
    safety_constitution_scenario_matrix = _load_json(root / "safety_constitution_scenario_matrix.json")
    safety_constitution_boundary_matrix = _load_json(root / "safety_constitution_boundary_matrix.json")
    governance_debt_register = _load_json(root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}
    for intake_id in (
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
        "voice_command_ownership_gate_policy",
        "voice_interruption_governance_dryrun",
        "minimal_runtime_controlled_output_definition",
        "minimal_runtime_text_only_output_post_review",
        "task_manager_runtime",
        "midplatform_task_state_runtime",
        "gps_route_context_dryrun",
        "ocr_ttl_gate",
        "ocr_source_validation_dryrun",
        "ocr_evidence_pack_reference",
        "worldmodel_lookup_framework",
    ):
        status = idx.get(intake_id, {}).get("status")
        ok(f"input.{intake_id}.optional", status in {"loaded", "optional_missing"}, status)
    ok("input.row_count", input_root_matrix.get("row_count") == len(rows), input_root_matrix.get("row_count"))

    for key in (
        "post_controlled_frame_roadmap_decision_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "safety_task_arbitration_policy_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "luna_safety_constitution_policy_defined",
        "global_safety_principles_defined",
        "high_risk_domain_matrix_generated",
        "evidence_boundary_policy_defined",
        "uncertainty_output_policy_defined",
        "user_instruction_boundary_policy_defined",
        "action_authority_boundary_policy_defined",
        "crossing_safety_inheritance_policy_defined",
        "future_survival_constitution_upgrade_path_defined",
        "scenario_matrix_generated",
        "safety_over_task",
        "safety_over_user_instruction",
        "candidate_must_not_be_claimed_as_fact",
        "unknown_must_not_be_fabricated",
        "uncertainty_requires_conservative_output",
        "high_risk_action_requires_special_governance",
        "map_hint_is_not_fact",
        "ocr_text_candidate_is_not_fact",
        "visual_candidate_is_not_fact",
        "memory_hint_is_not_fact",
        "stale_information_cannot_drive_current_action",
        "user_instruction_cannot_override_safety",
        "traffic_light_candidate_not_crossing_permission",
        "green_light_candidate_not_crossing_permission",
        "map_crossing_hint_not_crossing_permission",
        "crowd_flow_candidate_not_crossing_permission",
        "OCR_countdown_text_not_crossing_permission",
        "user_says_go_not_crossing_permission",
        "crossing_decision_requires_special_safety_governance",
        "safety_constitution_to_survival_constitution_upgrade_later",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{key}", summary.get(key) is True)
    ok("summary.policy_scope", summary.get("policy_scope") == "safety_constitution_policy_only")
    ok("summary.scenario_count", summary.get("scenario_count", 0) >= 12, summary.get("scenario_count"))
    for key in (
        "survival_constitution_runtime_allowed_now",
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
        "entity_resolution_runtime_invoked",
        "fact_admission_runtime_invoked",
        "memory_consolidation_invoked",
        "library_experience_commit_invoked",
        "emotion_engine_invoked",
        "survival_constitution_runtime_invoked",
    ):
        ok(f"summary.{key}", summary.get(key) is False)
    ok("summary.violations", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("policy.id", luna_safety_constitution_policy.get("constitution_id") == "lsc_v1_001")
    ok("policy.scope", luna_safety_constitution_policy.get("constitution_scope") == "safety_constitution_policy_only")
    ok("policy.version", luna_safety_constitution_policy.get("constitution_version") == "v1")
    ok("policy.applies_modules_count", len(luna_safety_constitution_policy.get("applies_to_modules", [])) >= 8, len(luna_safety_constitution_policy.get("applies_to_modules", [])))
    for key in (
        "high_risk_domain_matrix_ref",
        "global_safety_principles_ref",
        "evidence_boundary_policy_ref",
        "uncertainty_output_policy_ref",
        "user_instruction_boundary_policy_ref",
        "action_authority_boundary_policy_ref",
        "crossing_safety_inheritance_policy_ref",
        "future_survival_constitution_upgrade_path_ref",
        "no_runtime_boundary_ref",
        "no_write_boundary_ref",
    ):
        ok(f"policy.{key}", isinstance(luna_safety_constitution_policy.get(key), str) and luna_safety_constitution_policy.get(key).endswith(".json"))
    ok("policy.not_survival", luna_safety_constitution_policy.get("safety_constitution_is_not_survival_constitution") is True)
    ok("policy.upgrade_later", luna_safety_constitution_policy.get("upgrade_to_survival_constitution_required_later") is True)
    ok("policy.current_phase_policy_only", luna_safety_constitution_policy.get("current_phase_policy_only") is True)

    for key in (
        "safety_over_task",
        "safety_over_user_instruction",
        "safety_over_map_hint",
        "safety_over_ocr_text",
        "safety_over_visual_candidate",
        "safety_over_memory_hint",
        "uncertainty_requires_conservative_output",
        "unknown_must_not_be_fabricated",
        "candidate_must_not_be_claimed_as_fact",
        "high_risk_action_requires_special_governance",
        "user_autonomy_must_be_preserved",
        "no_manipulative_emotional_intervention",
        "all_high_risk_output_must_be_traceable",
    ):
        ok(f"global.{key}", global_safety_principles.get(key) is True)

    domain_rows = high_risk_domain_matrix.get("domains", [])
    domain_idx = {row.get("domain_id"): row for row in domain_rows}
    ok("domains.count", high_risk_domain_matrix.get("domain_count", 0) >= len(EXPECTED_HIGH_RISK_DOMAINS), high_risk_domain_matrix.get("domain_count"))
    for domain_id in EXPECTED_HIGH_RISK_DOMAINS:
        row = domain_idx.get(domain_id, {})
        ok(f"domain.{domain_id}.present", domain_id in domain_idx)
        ok(f"domain.{domain_id}.risk_type", isinstance(row.get("risk_type"), str) and bool(row.get("risk_type")))
        ok(f"domain.{domain_id}.risk_level", isinstance(row.get("risk_level"), str) and bool(row.get("risk_level")))
        ok(f"domain.{domain_id}.allowed_output_modes", isinstance(row.get("allowed_output_modes"), list) and len(row.get("allowed_output_modes", [])) >= 1)
        ok(f"domain.{domain_id}.forbidden_output_modes", isinstance(row.get("forbidden_output_modes"), list) and len(row.get("forbidden_output_modes", [])) >= 1)
        ok(f"domain.{domain_id}.required_governance", isinstance(row.get("required_governance"), str) and bool(row.get("required_governance")))
        ok(f"domain.{domain_id}.runtime_allowed_now", row.get("runtime_allowed_now") is False)
        ok(f"domain.{domain_id}.fact_write_allowed", row.get("fact_write_allowed") is False)
        ok(f"domain.{domain_id}.action_allowed", row.get("action_allowed") is False)

    for key in (
        "visual_candidate_is_not_fact",
        "ocr_text_candidate_is_not_fact",
        "map_hint_is_not_fact",
        "memory_hint_is_not_fact",
        "tracking_candidate_is_not_fact",
        "world_observation_candidate_is_not_fact",
        "user_feedback_is_not_fact_by_default",
        "model_answer_is_not_fact_without_evidence",
        "stale_information_cannot_drive_current_action",
        "conflict_requires_review_or_reobserve",
    ):
        ok(f"evidence.{key}", evidence_boundary_policy.get(key) is True)

    for key in (
        "unknown_must_be_stated",
        "low_confidence_requires_caution",
        "high_risk_low_confidence_requires_hold_or_confirm",
        "no_false_certainty",
        "no_action_instruction_when_uncertain",
        "no_arrival_claim_without_confirmation",
        "no_crossing_permission_without_special_governance",
        "no_medical_financial_legal_definitive_advice",
        "user_notice_must_not_overclaim",
    ):
        ok(f"uncertainty.{key}", uncertainty_output_policy.get(key) is True)

    for key in (
        "user_instruction_cannot_override_safety",
        "owner_instruction_cannot_override_high_risk_safety",
        "non_owner_instruction_blocked_by_ownership_gate",
        "emergency_keyword_from_unknown_speaker_safety_observation_only",
        "user_request_for_action_requires_context_check",
        "user_feedback_can_trigger_reobserve_not_fact_write",
    ):
        ok(f"user_boundary.{key}", user_instruction_boundary_policy.get(key) is True)

    for key in (
        "no_module_can_directly_trigger_high_risk_action",
        "map_cannot_trigger_action",
        "OCR_cannot_trigger_action",
        "visual_model_cannot_trigger_action",
        "tracking_cannot_trigger_action",
        "memory_cannot_trigger_action",
        "LLM_cannot_trigger_action",
        "action_requires_dedicated_governance_and_arbitration",
    ):
        ok(f"action_boundary.{key}", action_authority_boundary_policy.get(key) is True)
    ok("action_boundary.current_phase_action_allowed", action_authority_boundary_policy.get("current_phase_action_allowed") is False)

    for key in (
        "traffic_light_candidate_not_crossing_permission",
        "green_light_candidate_not_crossing_permission",
        "map_crossing_hint_not_crossing_permission",
        "crowd_flow_candidate_not_crossing_permission",
        "OCR_countdown_text_not_crossing_permission",
        "user_says_go_not_crossing_permission",
        "navigation_route_says_cross_not_crossing_permission",
        "crossing_decision_requires_special_safety_governance",
        "crossing_output_must_be_conservative",
        "crossing_uncertain_requires_stop_or_confirm_candidate",
    ):
        ok(f"crossing_inheritance.{key}", crossing_safety_inheritance_policy.get(key) is True)

    ok("survival.upgrade_required_later", future_survival_constitution_upgrade_path.get("upgrade_required_later") is True)
    ok("survival.runtime_allowed_now", future_survival_constitution_upgrade_path.get("survival_constitution_runtime_allowed_now") is False)
    ok("survival.current_scope_count", len(future_survival_constitution_upgrade_path.get("safety_constitution_current_scope", [])) >= 5)
    for item in EXPECTED_SURVIVAL_SCOPE:
        ok(f"survival.scope.{item}", item in future_survival_constitution_upgrade_path.get("survival_constitution_future_scope", []))

    scenario_rows = safety_constitution_scenario_matrix.get("scenarios", [])
    scenario_idx = {row.get("scenario_id"): row for row in scenario_rows}
    ok("scenario.count", safety_constitution_scenario_matrix.get("scenario_count", 0) >= 12, safety_constitution_scenario_matrix.get("scenario_count"))
    for scenario_id in EXPECTED_SCENARIOS:
        row = scenario_idx.get(scenario_id, {})
        ok(f"scenario.{scenario_id}.present", scenario_id in scenario_idx)
        ok(f"scenario.{scenario_id}.trigger_note", isinstance(row.get("trigger_note"), str) and bool(row.get("trigger_note")))
        ok(f"scenario.{scenario_id}.expected_outcome", isinstance(row.get("expected_outcome"), str) and bool(row.get("expected_outcome")))
        ok(f"scenario.{scenario_id}.policy_result", row.get("policy_result") == "conservative_or_blocked")
        ok(f"scenario.{scenario_id}.crossing_permission", row.get("crossing_permission") is False)
        ok(f"scenario.{scenario_id}.action_instruction_allowed", row.get("action_instruction_allowed") is False)
        ok(f"scenario.{scenario_id}.fact_write_allowed", row.get("fact_write_allowed") is False)

    for key in (
        "policy_scope",
        "no_runtime",
        "no_write",
        "no_action",
        "no_speech",
        "no_fact",
        "no_live_camera",
        "no_image_read",
        "no_visual_model",
        "no_map_api",
        "no_OCR_provider",
        "no_tracking_runtime",
        "no_worldmodel_write",
        "no_memory_write",
        "no_library_write",
        "no_entity_resolution",
        "no_fact_admission",
        "no_emotion_engine",
        "no_dual_device_runtime",
        "no_failover_runtime",
    ):
        expected = "safety_constitution_policy_only" if key == "policy_scope" else True
        ok(f"boundary_matrix.{key}", safety_constitution_boundary_matrix.get(key) == expected, safety_constitution_boundary_matrix.get(key))
    ok("boundary_matrix.crossing_decision_runtime_allowed", safety_constitution_boundary_matrix.get("crossing_decision_runtime_allowed") is False)
    ok("boundary_matrix.survival_constitution_runtime_allowed_now", safety_constitution_boundary_matrix.get("survival_constitution_runtime_allowed_now") is False)

    carryover = governance_debt_register.get("carryover_topics", [])
    ok("debt.count", len(carryover) >= 8, len(carryover))
    ok("debt.future_survival_constitution_upgrade_required", governance_debt_register.get("future_survival_constitution_upgrade_required") is True)
    ok("debt.crossing_must_inherit", governance_debt_register.get("crossing_must_inherit_safety_constitution") is True)
    ok("debt.no_duplicate_safety_redlines_allowed", governance_debt_register.get("no_duplicate_safety_redlines_allowed") is True)

    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended_next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)
    ok("next_phase.reason", isinstance(next_phase_recommendation.get("reason"), str) and bool(next_phase_recommendation.get("reason")))

    for report_name, report in (
        ("no_runtime_boundary_report", no_runtime_boundary_report),
        ("no_write_boundary_report", no_write_boundary_report),
    ):
        ok(f"{report_name}.policy_scope", report.get("policy_scope") == "safety_constitution_policy_only")
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
            "entity_resolution_runtime_invoked",
            "fact_admission_runtime_invoked",
            "memory_consolidation_invoked",
            "library_experience_commit_invoked",
            "emotion_engine_invoked",
            "survival_constitution_runtime_invoked",
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
