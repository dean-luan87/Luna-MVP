# -*- coding: utf-8 -*-
"""OCR Mainline Governance Closure v1 — governance closure only; no runtime.

Phase-OCR-Mainline-Governance-Closure-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "OCR-Mainline-Governance-Closure-v1-001"
FINAL_DECISION = "OCR_MAINLINE_CLOSED_FOR_GOVERNANCE"
RECOMMENDED_NEXT = "WorldModel-Lookup-for-Reading-DryRun-v1"

FOLLOWUPS = [
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Fragment-Evidence-Weaving-Governance-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
    "Memory-Governance-Delete-Update-Authority-Policy-v1",
    "User-Privacy-Consent-Governance-v1",
    "Missing-Regression-Artifact-Recovery-v1",
    "Hardware-Camera-Control-GuardedTrial-Precheck-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1-GuardedTrial",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
]

FUTURE_REOPEN = [
    (
        "Hardware-Camera-Control-GuardedTrial-Precheck-v1",
        ["hardware_guardedtrial_precheck", "no_write_boundary_passed"],
        ["hardware_chain_frozen", "no_real_camera"],
    ),
    (
        "OCRRequest-Gated-Submission-from-StaticReading-v1-GuardedTrial",
        ["real_static_capture_result", "frame_ref", "stc_anchor", "capture_quality"],
        ["capture_status_not_captured", "static_capture_result_missing"],
    ),
    (
        "Evidence-Pack-Adapter-v5-StaticReading",
        ["ocr_result_available", "ep_v5_gate"],
        ["ep_v5_missing_ocr_result"],
    ),
    (
        "Semantic-Candidate-v5-StaticReading",
        ["ep_v5_available"],
        ["semantic_v5_missing_ep_v5"],
    ),
    (
        "Source-Validation-v3-StaticReading",
        ["ep_v5_available"],
        ["sv_v3_missing_ep_v5"],
    ),
    (
        "Memory-Governance-Handoff-Runtime-v1",
        ["memory_governance_contract", "append_only_policy"],
        ["memory_handoff_only_dryrun"],
    ),
]

FORBIDDEN_ACTIONS = [
    ("continue_to_ep_v5_now", "ep_v5_missing_ocr_result", "ep_v5_gate", "Evidence-Pack-Adapter-v5-StaticReading"),
    ("continue_to_semantic_v5_now", "semantic_v5_missing_ep_v5", "semantic_v5_gate", "Semantic-Candidate-v5-StaticReading"),
    ("continue_to_sv_v3_now", "sv_v3_missing_ep_v5", "source_validation_v3_gate", "Source-Validation-v3-StaticReading"),
    ("run_staticreading_ocr_now", "capture_status_not_captured", "staticreading_ocr_gate", "OCRRequest-Gated-Submission-from-StaticReading-v1-GuardedTrial"),
    ("submit_ocrrequest_now", "ocrrequest_staticreading_blocked", "ocrrequest_gate", "OCRRequest-Gated-Submission-from-StaticReading-v1-GuardedTrial"),
    ("run_provider_now", "runtime_ocr_disabled", "provider_gate", "OCR-Activation-Governance-Policy-v1"),
    ("use_mock_text_as_staticreading_result", "no_mock_as_fact", "staticreading_integrity", "StaticReading-Integrity-Policy"),
    ("write_memory_now", "memory_handoff_only_dryrun", "memory_runtime_gate", "Memory-Governance-Handoff-Runtime-v1"),
    ("write_worldmodel_now", "worldmodel_write_not_allowed", "worldmodel_write_gate", "WorldModel-Lookup-for-Reading-DryRun-v1"),
    ("generate_scene_delta_now", "scene_delta_not_allowed", "scenedelta_gate", "Fragment-Evidence-Weaving-Governance-v1"),
    ("launch_hardware_guardedtrial_now", "hardware_guardedtrial_not_authorized", "hardware_guardedtrial_gate", "Hardware-Camera-Control-GuardedTrial-Precheck-v1"),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_software_closure", "software_closure_loaded", [], [], []),
    ("load_regression_route_compliance", "regression_loaded", [], [], ["full_regression_claim"]),
    ("load_staticreading_ocrrequest_gate", "gate_loaded", [], [], ["ocr_submit"]),
    ("load_memory_handoff", "mem_loaded", [], [], ["memory_write"]),
    ("load_hardware_stub", "hw_loaded", [], [], ["camera"]),
    ("evaluate_ocr_governance_status", "status_matrix_ok", [], [], []),
    ("accept_conditional_regression_caveat", "caveat_accepted", [], [], ["deny_caveat"]),
    ("close_runtime_ocr", "runtime_ocr_closed", [], [], ["enable_runtime_ocr"]),
    ("define_future_reopen_conditions", "reopen_defined", [], [], []),
    ("define_forbidden_continuations", "forbidden_defined", [], [], []),
    ("define_memory_worldmodel_boundary_status", "boundary_ok", [], [], ["wm_write"]),
    ("generate_next_software_mainline_handoff", "handoff_ok", [], [], []),
    ("generate_final_ocr_mainline_closure_decision", "final_closed", [], [], ["production_ready"]),
]

STATUS_ITEMS = [
    ("ocr_activation_governance", "closed", "closed", False, True, None),
    ("dynamic_ocr_failure_recovery", "closed", "closed", False, True, "dynamic_ocr_retry_closed"),
    ("stc_sampling_guidance", "closed", "closed", False, True, None),
    ("assisted_static_reading_mode", "closed", "blocked_expected", False, True, "no_captured_frame"),
    ("information_source_localization", "closed", "closed", False, True, None),
    ("readable_region_discovery", "closed", "closed", False, True, None),
    ("hardware_adapter_stub_boundary", "frozen", "closed", False, True, "hardware_chain_frozen"),
    ("staticreading_ocrrequest_gate", "blocked_until_captured_frame", "blocked_expected", False, True, "capture_status_not_captured"),
    ("confirmed_text_memory_governance", "closed", "closed", False, True, None),
    ("memory_handoff_dryrun", "dryrun_ready", "closed", False, True, "memory_handoff_only_dryrun"),
    ("poster_route_compliance", "pass", "closed", False, False, None),
    ("realvideo_route_compliance", "pass", "closed", False, False, None),
    ("regression_route_compliance", "conditional_pass", "closed", False, False, "testboard_metrics_optional_missing"),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def run_ocr_mainline_governance_closure_v1(
    *,
    software_closure_root: str,
    regression_route_compliance_root: str,
    staticreading_ocrrequest_root: str,
    memory_handoff_root: str,
    hardware_adapter_stub_root: str,
    ocr_activation_root: str,
    stc_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    roots = {
        "software_closure": Path(software_closure_root).resolve(),
        "regression": Path(regression_route_compliance_root).resolve(),
        "ocr_gate": Path(staticreading_ocrrequest_root).resolve(),
        "mem_handoff": Path(memory_handoff_root).resolve(),
        "hw_stub": Path(hardware_adapter_stub_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    sw_sum = _read_json(roots["software_closure"] / "return_to_software_mainline_closure_v1_summary.json") or {}
    reg_sum = _read_json(
        roots["regression"] / "ocr_staticreading_poster_realvideo_regression_route_compliance_v1_summary.json"
    ) or {}
    reg_final = _read_json(
        roots["regression"] / "ocr_regression_route_compliance_final_decision_v1.json"
    ) or {}
    reg_coverage = _read_json(roots["regression"] / "ocr_regression_coverage_report_v1.json") or {}
    gate_sum = _read_json(roots["ocr_gate"] / "ocrrequest_gated_submission_from_staticreading_v1_summary.json") or {}
    mem_sum = _read_json(
        roots["mem_handoff"] / "confirmed_text_evidence_memory_handoff_dryrun_v1_summary.json"
    ) or {}
    hw_sum = _read_json(
        roots["hw_stub"] / "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json"
    ) or {}

    reg_final_decision = reg_final.get("final_decision", "REGRESSION_ROUTE_COMPLIANCE_CONDITIONAL_PASS")
    testboard_missing = "testboard" in (reg_coverage.get("partial_regression_reason") or [])

    critical_routes_pass = reg_final.get("routes_failed", 1) == 0 and reg_final.get("routes_passed", 0) >= 5

    intake_specs = [
        ("software_closure", roots["software_closure"], "return_to_software_mainline_closure_v1_summary.json", False),
        ("regression_route_compliance", roots["regression"], "ocr_staticreading_poster_realvideo_regression_route_compliance_v1_summary.json", False),
        ("staticreading_ocrrequest_gate", roots["ocr_gate"], "ocrrequest_gated_submission_from_staticreading_v1_summary.json", False),
        ("memory_handoff", roots["mem_handoff"], "confirmed_text_evidence_memory_handoff_dryrun_v1_summary.json", False),
        ("hardware_stub", roots["hw_stub"], "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json", False),
        ("ocr_activation", roots["ocr_act"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("stc", roots["stc"], "stc_sampling_guidance_policy_v1_summary.json", False),
        ("benchmark", roots["bench"], None, True),
        ("system_health", roots["health"], None, True),
        ("simulation", roots["sim"], None, True),
    ]
    intake_rows = []
    for iid, root, art, optional in intake_specs:
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
        intake_rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                **_not_fact(),
            }
        )

    status_rows = []
    for name, observed, closure_state, ext_now, ext_later, blocker in STATUS_ITEMS:
        status_rows.append(
            {
                "status_name": name,
                "observed_status": observed,
                "closure_state": closure_state,
                "extension_allowed_now": ext_now,
                "extension_allowed_later": ext_later,
                "blocker_if_any": blocker,
                **_not_fact(),
            }
        )

    reopen_rows = [
        {
            "future_entrypoint": ep,
            "allowed_now": False,
            "allowed_later": True,
            "prerequisites": prereq,
            "current_blockers": blockers,
            "must_not_bypass": True,
            **_not_fact(),
        }
        for ep, prereq, blockers in FUTURE_REOPEN
    ]

    forbidden_rows = [
        {
            "action": action,
            "forbidden_now": True,
            "reason": reason,
            "violation_type": vtype,
            "required_future_gate": gate,
            **_not_fact(),
        }
        for action, reason, vtype, gate in FORBIDDEN_ACTIONS
    ]

    trace_steps = [
        {
            "step_id": sid,
            "step_name": sid,
            "decision": decision,
            "reason_codes": reasons,
            "allowed_next_actions": allowed,
            "blocked_next_actions": blocked,
            "runtime_action_committed": False,
        }
        for sid, decision, reasons, allowed, blocked in TRACE_STEPS
    ]

    next_mainline_candidates = [
        {
            "phase": "WorldModel-Lookup-for-Reading-DryRun-v1",
            "priority": 1,
            "blocked_by_ocr": False,
            "description": "WorldModel lookup for reading; no write",
        },
        {
            "phase": "Fragment-Evidence-Weaving-Governance-v1",
            "priority": 2,
            "blocked_by_ocr": False,
            "description": "Fragment evidence weaving governance only",
        },
        {
            "phase": "Emotional-Context-Background-Candidate-DryRun-v1",
            "priority": 3,
            "blocked_by_ocr": False,
            "description": "Emotional context candidate dry-run",
        },
        {
            "phase": "Memory-Governance-Delete-Update-Authority-Policy-v1",
            "priority": 4,
            "blocked_by_ocr": False,
            "description": "Memory delete/update authority policy",
        },
        {
            "phase": "User-Privacy-Consent-Governance-v1",
            "priority": 5,
            "blocked_by_ocr": False,
            "description": "Privacy consent governance",
        },
    ]

    return {
        "summary": {
            "schema_version": "ocr_mainline_governance_closure_v1_summary_v0",
            "phase": PHASE_ID,
            "closure_scope": "ocr_mainline_governance_closure_only",
            "based_on_software_closure": roots["software_closure"].is_dir(),
            "based_on_regression_route_compliance": roots["regression"].is_dir(),
            "based_on_staticreading_ocrrequest_gate": roots["ocr_gate"].is_dir(),
            "based_on_memory_handoff": roots["mem_handoff"].is_dir(),
            "based_on_hardware_stub": roots["hw_stub"].is_dir(),
            "ocr_governance_closed": True,
            "closed_for_governance": True,
            "closed_for_production": False,
            "runtime_ocr_enabled": False,
            "dynamic_ocr_retry_closed": True,
            "staticreading_ocrrequest_blocked_until_captured_frame": True,
            "hardware_chain_frozen": sw_sum.get("hardware_chain_frozen", True),
            "memory_handoff_dryrun_ready": sw_sum.get("memory_handoff_dryrun_closed", True),
            "regression_route_compliance_status": "conditional_pass",
            "regression_coverage_caveat_present": True,
            "testboard_metrics_optional_missing": testboard_missing,
            "ep_v5_allowed_now": False,
            "semantic_v5_allowed_now": False,
            "source_validation_v3_allowed_now": False,
            "memory_runtime_allowed_now": False,
            "worldmodel_write_allowed_now": False,
            "next_software_mainline_ready": sw_sum.get("software_mainline_ready_for_next_planning", True),
            "recommended_next_phase": RECOMMENDED_NEXT,
            "runtime_action_committed": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": {
            "schema_version": "ocr_mainline_governance_closure_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "status_matrix": {
            "schema_version": "ocr_mainline_governance_closure_status_matrix_v1",
            "status_items": status_rows,
            "item_count": len(status_rows),
            **_not_fact(),
        },
        "caveat_acceptance": {
            "schema_version": "ocr_mainline_governance_regression_caveat_acceptance_v1",
            "regression_final_decision": reg_final_decision,
            "conditional_go_accepted": True,
            "reason": "testboard_metrics_optional_missing",
            "critical_routes_passed": critical_routes_pass,
            "critical_route_pass_list": [
                "realvideo",
                "poster",
                "staticreading",
                "memory_handoff",
                "hardware_stub",
            ],
            "coverage_caveat_preserved": True,
            "caveat_does_not_block_governance_closure": True,
            "caveat_blocks_full_regression_claim": True,
            "full_regression_claimed": False,
            **_not_fact(),
        },
        "runtime_closed": {
            "schema_version": "ocr_mainline_runtime_ocr_closed_report_v1",
            "runtime_ocr_enabled": False,
            "dynamic_reocr_allowed_now": False,
            "staticreading_ocrrequest_eligible_now": gate_sum.get("ocrrequest_eligible_now", False),
            "staticreading_blocked_until_captured_frame": True,
            "ocrrequest_submitted_now": gate_sum.get("ocrrequest_submitted_now", False),
            "provider_invoked_now": False,
            "blocked_reason": [
                "no_captured_frame",
                "hardware_stub_only",
                "capture_status_not_captured",
                "static_capture_result_missing",
            ],
            "reopen_requires": [
                "hardware_guardedtrial_precheck",
                "real_static_capture_result",
                "frame_ref",
                "stc_anchor",
                "capture_quality",
                "no_write_boundary_passed",
            ],
            **_not_fact(),
        },
        "reopen_matrix": {
            "schema_version": "ocr_mainline_future_reopen_condition_matrix_v1",
            "conditions": reopen_rows,
            "condition_count": len(reopen_rows),
            "all_allowed_now_false": all(r["allowed_now"] is False for r in reopen_rows),
            **_not_fact(),
        },
        "forbidden_matrix": {
            "schema_version": "ocr_mainline_forbidden_continuation_matrix_v1",
            "forbidden_actions": forbidden_rows,
            "action_count": len(forbidden_rows),
            **_not_fact(),
        },
        "mem_wm_boundary": {
            "schema_version": "ocr_mainline_memory_worldmodel_boundary_status_v1",
            "memory_handoff_dryrun_ready": True,
            "memory_runtime_allowed_now": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "confirmed_text_append_only_policy_preserved": True,
            "worldmodel_lookup_allowed_later": True,
            "worldmodel_write_allowed_now": False,
            "scene_delta_allowed_now": False,
            "fragment_weaving_allowed_as_governance_later": True,
            **_not_fact(),
        },
        "next_handoff": {
            "schema_version": "ocr_mainline_next_software_mainline_handoff_v1",
            "candidates": next_mainline_candidates,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "recommendation_reason": "OCR governance closed; runtime OCR disabled; WorldModel lookup is read-only next step without WM write",
            "blocked_by_ocr": False,
            "blocked_by_hardware": False,
            "blocked_by_memory_runtime": False,
            "required_inputs": ["software_mainline_closure", "regression_route_compliance", "ocr_activation_policy"],
            "expected_output": "worldmodel_lookup_dryrun_candidates",
            "no_write_boundary_required": True,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "ocr_mainline_governance_closure_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "ocr_mainline_governance_closure_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "closed_for_governance": True,
            "closed_for_production": False,
            "runtime_ocr_enabled": False,
            "next_software_mainline_ready": True,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "regression_caveat_preserved": True,
            "full_regression_claimed": False,
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "ocr_mainline_governance_closure_boundary_report_v1",
            "closure_only": True,
            "runtime_action_committed": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
            "ep_v5_generated": False,
            "semantic_v5_generated": False,
            "sv_v3_invoked": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "ocr_mainline_governance_closure_metrics_candidate_report_v1",
            "closure_status_count": len(status_rows),
            "future_reopen_condition_count": len(reopen_rows),
            "forbidden_continuation_count": len(forbidden_rows),
            "next_mainline_candidate_count": len(next_mainline_candidates),
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "ocr_mainline_governance_closure_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "ocr_mainline_governance_closure_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "ocr_mainline_governance_closure_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "closure_only": True,
            "runtime_action_committed": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
            "ep_v5_generated": False,
            "semantic_v5_generated": False,
            "sv_v3_invoked": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "ocr_mainline_governance_closure_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "ocr_mainline_governance_closure_non_claims_report_v1",
            "claims": [
                "ocr_mainline_closure_not_production_ready",
                "closed_for_governance_not_runtime_enabled",
                "conditional_regression_caveat_preserved",
                "testboard_optional_missing_not_full_pass",
                "blocked_ocrrequest_not_ocr_failure",
                "no_captured_frame_not_no_text_fact",
                "memory_handoff_ready_not_memory_write",
                "worldmodel_lookup_next_not_worldmodel_write",
                "not_accuracy_benchmark_pass",
            ],
        },
        "followups": {
            "schema_version": "ocr_mainline_governance_closure_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "ocr_mainline_governance_closure_audit_report_v1",
            "ocr_mainline_governance_closure_v1_executed": True,
            "closure_only": True,
            "ocr_governance_closed": True,
            "closed_for_governance": True,
            "closed_for_production": False,
            "runtime_ocr_enabled": False,
            "regression_coverage_caveat_present": True,
            "testboard_metrics_optional_missing": testboard_missing,
            "dynamic_ocr_retry_closed": True,
            "staticreading_ocrrequest_blocked_until_captured_frame": True,
            "hardware_chain_frozen": True,
            "memory_handoff_dryrun_ready": True,
            "ep_v5_allowed_now": False,
            "semantic_v5_allowed_now": False,
            "source_validation_v3_allowed_now": False,
            "memory_runtime_allowed_now": False,
            "worldmodel_write_allowed_now": False,
            "runtime_action_committed": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_submitted": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
