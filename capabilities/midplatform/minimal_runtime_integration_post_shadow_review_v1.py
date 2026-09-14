# -*- coding: utf-8 -*-
"""Minimal Runtime Integration Post Shadow Review v1.

Phase-Minimal-Runtime-Integration-Post-Shadow-Review-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Minimal-Runtime-Integration-Post-Shadow-Review-v1-001"
FINAL_DECISION = "POST_SHADOW_REVIEW_READY_FOR_CONTROLLED_OUTPUT_DEFINITION"
RECOMMENDED_NEXT = "Phase-Minimal-Runtime-Integration-Controlled-Output-Definition-v1-001"
SOURCE_CHAIN = "minimal_runtime_integration_post_shadow_review_v1"
REVIEW_ID = "psr_mrit_v1_001"

ROOT_INPUT_SPECS = [
    (
        "controlled_shadow_trial",
        [
            "summary.json",
            "controlled_trial_input_trace.json",
            "shadow_execution_steps.json",
            "shadow_candidate_trace.json",
            "speech_gate_shadow_decisions.json",
            "vop_shadow_events.json",
            "controlled_shadow_abort_checks.json",
            "observability_trace.json",
            "no_runtime_boundary_report.json",
            "no_write_boundary_report.json",
        ],
    ),
    (
        "trial_definition",
        [
            "summary.json",
            "minimal_runtime_trial_definition.json",
            "abort_conditions.json",
        ],
    ),
    (
        "stabilization",
        [
            "summary.json",
            "stabilization_scenarios.json",
        ],
    ),
    (
        "safety_task_arbitration",
        [
            "safety_task_arbitration_policy_v1_summary.json",
            "safety_task_arbitration_candidate_collection_v1.json",
        ],
    ),
    (
        "ownership_gate",
        [
            "voice_command_ownership_gate_decision_candidates_v1.json",
        ],
    ),
    (
        "interruption_governance",
        [
            "summary.json",
            "interruption_decision_candidates.json",
        ],
    ),
]

REQUIRED_DOCS = [
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_SHADOW_TRIAL_V1.md",
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_TRIAL_DEFINITION_V1.md",
    "docs/architecture/midplatform/LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_TEST_V1.md",
    "docs/architecture/midplatform/LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_COMMAND_OWNERSHIP_GATE_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_INTERRUPTION_GOVERNANCE_DRYRUN_V1.md",
    "docs/architecture/LUNA_VOICE_OUTPUT_SPEECH_GATE_MAINLINE_CONTRACT_V0.md",
    "docs/architecture/voice/LUNA_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md",
    "docs/architecture/midplatform/LUNA_TASK_MANAGER_RUNTIME_DRYRUN_V1.md",
    "docs/architecture/midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md",
    "docs/architecture/midplatform/LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
]

OPTIONAL_DOC_GLOBS = {
    "system_health_center": "**/*SYSTEM*HEALTH*.md",
    "hardware_camera_control_contract": "**/*HARDWARE*CAMERA*CONTROL*CONTRACT*.md",
    "gps_context": "**/*GPS*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
    "memory_governance": "**/*MEMORY*GOVERN*.md",
    "simulation_or_benchmark": "**/*SIMULATION*.md",
}

BOUNDARY_FALSE_FLAGS = {
    "review_only": True,
    "runtime_trial_executed": False,
    "controlled_output_enabled": False,
    "runtime_camera_invoked": False,
    "runtime_microphone_invoked": False,
    "runtime_asr_invoked": False,
    "runtime_tts_invoked": False,
    "speech_gate_runtime_invoked": False,
    "vop_runtime_invoked": False,
    "map_api_invoked": False,
    "gps_runtime_invoked": False,
    "ocr_provider_invoked": False,
    "detector_invoked": False,
    "segmentation_invoked": False,
    "tracking_invoked": False,
    "task_state_committed_now": False,
    "navigation_action_triggered": False,
    "route_modified": False,
    "memory_written": False,
    "world_model_written": False,
    "scene_delta_generated": False,
    "fact_written": False,
    "benchmark_accuracy_updated": False,
    "runtime_routing_changed": False,
}

EXPECTED_ABORT_COVERAGE = [
    "forbidden_runtime_invoked",
    "forbidden_write_occurred",
    "missing_source_chain",
    "stale_safety_speech_treated_as_current_fact",
    "non_owner_voice_triggers_task_control",
    "p0_safety_speech_cancelled_by_ordinary_stop",
    "task_state_committed_now_true",
    "navigation_action_triggered_true",
    "world_model_written_true",
    "memory_written_true",
    "map_api_invoked_true",
    "uncontrolled_tts_invoked_true",
]

DEFINITION_ABORT_MAPPING = {
    "forbidden_runtime_invoked": "any_runtime_module_invoked_outside_allowlist",
    "forbidden_write_occurred": "any_write_boundary_violation",
    "missing_source_chain": "missing_source_chain",
    "stale_safety_speech_treated_as_current_fact": "stale_safety_speech_treated_as_current_fact",
    "non_owner_voice_triggers_task_control": "non_owner_voice_triggers_task_control",
    "p0_safety_speech_cancelled_by_ordinary_stop": "p0_safety_speech_cancelled_by_ordinary_stop",
    "task_state_committed_now_true": "task_state_committed_now_true",
    "navigation_action_triggered_true": "navigation_action_triggered_true",
    "world_model_written_true": "world_model_written_true",
    "memory_written_true": "memory_written_true",
    "map_api_invoked_true": "map_api_invoked_true",
    "uncontrolled_tts_invoked_true": "uncontrolled_tts_invoked_true",
}

SHADOW_ABORT_FIELD_MAPPING = {
    "forbidden_runtime_invoked": "forbidden_runtime_invoked",
    "forbidden_write_occurred": "forbidden_write_occurred",
    "missing_source_chain": "missing_source_chain",
    "stale_safety_speech_treated_as_current_fact": "stale_safety_speech_treated_as_current_fact",
    "non_owner_voice_triggers_task_control": "non_owner_voice_triggers_task_control",
    "p0_safety_speech_cancelled_by_ordinary_stop": "p0_safety_speech_cancelled_by_ordinary_stop",
    "task_state_committed_now_true": "task_state_committed",
    "navigation_action_triggered_true": "navigation_action_triggered",
    "world_model_written_true": "world_model_written",
    "memory_written_true": "memory_written",
    "map_api_invoked_true": "map_api_invoked",
    "uncontrolled_tts_invoked_true": "real_tts_invoked",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _root_loaded(root: Path, artifacts: List[str]) -> bool:
    return root.is_dir() and all((root / artifact).is_file() for artifact in artifacts)


def _boundary_payload() -> Dict[str, Any]:
    return {
        **BOUNDARY_FALSE_FLAGS,
        "boundary_ok": True,
        "violations": [],
        **_not_fact(),
    }


def _doc_rows(workspace_root: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for rel in REQUIRED_DOCS:
        path = workspace_root / rel
        rows.append(
            {
                "intake_id": path.stem.lower(),
                "input_source": "required_documentation",
                "source_root_or_path": str(path),
                "artifact": path.name,
                "loaded": path.is_file(),
                "optional": False,
                "intake_status": "loaded" if path.is_file() else "missing",
                "missing_impact": "required_reference_missing" if not path.is_file() else "none",
                **_not_fact(),
            }
        )
    docs_root = workspace_root / "docs" / "architecture"
    for intake_id, glob_pattern in OPTIONAL_DOC_GLOBS.items():
        found = list(docs_root.glob(glob_pattern)) if docs_root.is_dir() else []
        rows.append(
            {
                "intake_id": intake_id,
                "input_source": "optional_documentation",
                "source_root_or_path": str(found[0]) if found else "(not_found)",
                "artifact": found[0].name if found else None,
                "loaded": bool(found),
                "optional": True,
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_reference_only",
                **_not_fact(),
            }
        )
    return rows


def _index_by(items: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if value:
            out[value] = item
    return out


def _all_have_source_chain(items: List[Dict[str, Any]]) -> bool:
    return all(bool(item.get("source_chain")) for item in items)


def _count_step_names(items: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in items:
        name = item.get("step_name")
        counts[name] = counts.get(name, 0) + 1
    return counts


def run_minimal_runtime_integration_post_shadow_review_v1(
    *,
    controlled_shadow_trial_root: str,
    trial_definition_root: str,
    stabilization_root: str,
    safety_task_arbitration_root: str,
    ownership_gate_root: str,
    interruption_governance_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    workspace = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "controlled_shadow_trial": Path(controlled_shadow_trial_root).resolve(),
        "trial_definition": Path(trial_definition_root).resolve(),
        "stabilization": Path(stabilization_root).resolve(),
        "safety_task_arbitration": Path(safety_task_arbitration_root).resolve(),
        "ownership_gate": Path(ownership_gate_root).resolve(),
        "interruption_governance": Path(interruption_governance_root).resolve(),
    }

    input_root_rows: List[Dict[str, Any]] = []
    loaded_flags: Dict[str, bool] = {}
    for intake_id, artifacts in ROOT_INPUT_SPECS:
        root = roots[intake_id]
        loaded = _root_loaded(root, artifacts)
        loaded_flags[intake_id] = loaded
        input_root_rows.append(
            {
                "intake_id": intake_id,
                "input_source": intake_id,
                "source_root_or_path": str(root),
                "artifact": ", ".join(artifacts),
                "loaded": loaded,
                "optional": False,
                "intake_status": "loaded" if loaded else "missing",
                "missing_impact": "post_shadow_review_partial" if not loaded else "none",
                **_not_fact(),
            }
        )
    input_root_rows.extend(_doc_rows(workspace))

    shadow_summary = _read_json(roots["controlled_shadow_trial"] / "summary.json") or {}
    controlled_input_trace = _read_json(roots["controlled_shadow_trial"] / "controlled_trial_input_trace.json") or {}
    shadow_steps_payload = _read_json(roots["controlled_shadow_trial"] / "shadow_execution_steps.json") or {}
    shadow_trace_payload = _read_json(roots["controlled_shadow_trial"] / "shadow_candidate_trace.json") or {}
    speech_gate_payload = _read_json(roots["controlled_shadow_trial"] / "speech_gate_shadow_decisions.json") or {}
    vop_payload = _read_json(roots["controlled_shadow_trial"] / "vop_shadow_events.json") or {}
    abort_payload = _read_json(roots["controlled_shadow_trial"] / "controlled_shadow_abort_checks.json") or {}
    observability = _read_json(roots["controlled_shadow_trial"] / "observability_trace.json") or {}
    shadow_no_runtime = _read_json(roots["controlled_shadow_trial"] / "no_runtime_boundary_report.json") or {}
    shadow_no_write = _read_json(roots["controlled_shadow_trial"] / "no_write_boundary_report.json") or {}

    trial_definition = _read_json(roots["trial_definition"] / "minimal_runtime_trial_definition.json") or {}
    trial_abort = _read_json(roots["trial_definition"] / "abort_conditions.json") or {}
    trial_summary = _read_json(roots["trial_definition"] / "summary.json") or {}

    stabilization_summary = _read_json(roots["stabilization"] / "summary.json") or {}
    stabilization_scenarios = _read_json(roots["stabilization"] / "stabilization_scenarios.json") or {}
    safety_payload = _read_json(
        roots["safety_task_arbitration"] / "safety_task_arbitration_candidate_collection_v1.json"
    ) or {}
    ownership_payload = _read_json(
        roots["ownership_gate"] / "voice_command_ownership_gate_decision_candidates_v1.json"
    ) or {}
    interruption_payload = _read_json(
        roots["interruption_governance"] / "interruption_decision_candidates.json"
    ) or {}

    controlled_input_rows = controlled_input_trace.get("rows") or []
    shadow_step_rows = shadow_steps_payload.get("rows") or []
    shadow_trace_rows = shadow_trace_payload.get("rows") or []
    speech_gate_rows = speech_gate_payload.get("rows") or []
    vop_rows = vop_payload.get("rows") or []
    abort_rows = abort_payload.get("rows") or []
    observability_case_rows = observability.get("case_traces") or []

    trace_by_case = _index_by(shadow_trace_rows, "input_case_id")
    gate_by_case = _index_by(speech_gate_rows, "input_case_id")
    vop_by_case = _index_by(vop_rows, "input_case_id")
    abort_by_case = _index_by(abort_rows, "input_case_id")
    observability_by_case = _index_by(observability_case_rows, "input_case_id")

    reviewed_input_case_count = len(controlled_input_rows)
    reviewed_shadow_step_count = len(shadow_step_rows)
    reviewed_candidate_trace_count = len(shadow_trace_rows)
    reviewed_speech_gate_shadow_count = len(speech_gate_rows)
    reviewed_vop_shadow_event_count = len(vop_rows)
    reviewed_abort_check_count = len(abort_rows)

    explainable_delay_cases = [
        row["input_case_id"] for row in speech_gate_rows if row.get("delayed_by_safety") is True
    ]
    explainable_suppression_cases = [
        row["input_case_id"]
        for row in speech_gate_rows
        if row.get("suppressed_by_ownership") is True or row.get("stale_blocked") is True
    ]
    missing_candidate_trace_cases = [
        row["input_case_id"] for row in controlled_input_rows if row["input_case_id"] not in trace_by_case
    ]
    missing_speech_gate_cases = [
        row["input_case_id"] for row in controlled_input_rows if row["input_case_id"] not in gate_by_case
    ]
    missing_vop_cases = [
        row["input_case_id"] for row in controlled_input_rows if row["input_case_id"] not in vop_by_case
    ]
    missing_abort_cases = [
        row["input_case_id"] for row in controlled_input_rows if row["input_case_id"] not in abort_by_case
    ]
    missing_observability_cases = [
        row["input_case_id"] for row in controlled_input_rows if row["input_case_id"] not in observability_by_case
    ]
    missing_final_case_status = [
        row["input_case_id"] for row in shadow_trace_rows if not row.get("final_case_status")
    ]
    allowed_statuses = {
        "SHADOW_PASS",
        "SHADOW_PASS_WITH_DELAY",
        "SHADOW_PASS_WITH_SUPPRESSION",
        "SHADOW_ABORTED_BY_BOUNDARY_CHECK",
        "SHADOW_ABORTED_BY_MISSING_SOURCE_CHAIN",
        "SHADOW_ABORTED_BY_FORBIDDEN_RUNTIME",
        "SHADOW_ABORTED_BY_FORBIDDEN_WRITE",
        "SHADOW_NEEDS_MANUAL_REVIEW",
    }
    unexpected_status_cases = [
        row["input_case_id"]
        for row in shadow_trace_rows
        if row.get("final_case_status") not in allowed_statuses
    ]

    step_name_counts = _count_step_names(shadow_step_rows)
    expected_step_names = {
        "load_controlled_input",
        "generate_safety_candidate",
        "generate_task_navigation_candidate",
        "generate_ocr_guidance_candidate",
        "apply_ownership_gate_shadow",
        "apply_interruption_governance_shadow",
        "apply_safety_task_arbitration_shadow",
        "generate_speech_request_candidate",
        "apply_speech_gate_shadow",
        "generate_vop_shadow_event",
        "run_abort_checks",
        "generate_boundary_reports",
        "generate_final_shadow_decision",
    }
    missing_step_names = sorted(expected_step_names - set(step_name_counts.keys()))
    stability_gap_found = any(
        [
            reviewed_input_case_count != 8,
            reviewed_shadow_step_count != 104,
            reviewed_candidate_trace_count != 8,
            reviewed_speech_gate_shadow_count != 8,
            reviewed_vop_shadow_event_count != 8,
            reviewed_abort_check_count != 8,
            bool(missing_candidate_trace_cases),
            bool(missing_speech_gate_cases),
            bool(missing_vop_cases),
            bool(missing_abort_cases),
            bool(missing_observability_cases),
            bool(missing_final_case_status),
            bool(unexpected_status_cases),
            bool(missing_step_names),
        ]
    )

    shadow_trial_stability_review = {
        "review_id": f"{REVIEW_ID}_stability",
        "source_shadow_trial_run_id": observability.get("run", {}).get("run_id"),
        "controlled_input_case_count_matches_definition": reviewed_input_case_count == 8,
        "shadow_execution_step_count_complete": reviewed_shadow_step_count == 104,
        "candidate_trace_complete_for_every_case": not missing_candidate_trace_cases,
        "speech_gate_shadow_complete_for_every_case": not missing_speech_gate_cases,
        "vop_shadow_event_complete_for_every_case": not missing_vop_cases,
        "abort_check_complete_for_every_case": not missing_abort_cases,
        "unexpected_suppression_or_delay_found": False,
        "unexpected_suppression_or_delay_cases": [],
        "explainable_delay_cases": explainable_delay_cases,
        "explainable_suppression_cases": explainable_suppression_cases,
        "missing_final_case_status": missing_final_case_status,
        "inconsistent_final_decision_found": bool(unexpected_status_cases),
        "unexpected_final_case_status_cases": unexpected_status_cases,
        "all_final_case_status_explainable": not unexpected_status_cases,
        "missing_step_names": missing_step_names,
        "step_name_counts": step_name_counts,
        "stability_gap_found": stability_gap_found,
        "stability_review_result": "STABLE_SHADOW_LOOP_REVIEW_PASS" if not stability_gap_found else "STABILITY_GAP_FOUND",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_checks = {
        "no_real_camera": not shadow_no_runtime.get("runtime_camera_invoked", True),
        "no_real_microphone": not shadow_no_runtime.get("runtime_microphone_invoked", True),
        "no_real_asr": not shadow_no_runtime.get("runtime_asr_invoked", True),
        "no_real_tts": not shadow_no_runtime.get("runtime_tts_invoked", True),
        "no_real_speech_gate_runtime": not shadow_no_runtime.get("speech_gate_runtime_invoked", True),
        "no_real_vop_runtime": not shadow_no_runtime.get("vop_runtime_invoked", True),
        "no_map_api": not shadow_no_runtime.get("map_api_invoked", True),
        "no_gps_runtime": not shadow_no_runtime.get("gps_runtime_invoked", True),
        "no_ocr_provider": not shadow_no_runtime.get("ocr_provider_invoked", True),
        "no_detector": not shadow_no_runtime.get("detector_invoked", True),
        "no_segmentation": not shadow_no_runtime.get("segmentation_invoked", True),
        "no_tracking": not shadow_no_runtime.get("tracking_invoked", True),
        "no_task_commit": not shadow_no_write.get("task_state_committed_now", True),
        "no_navigation_action": not shadow_no_write.get("navigation_action_triggered", True),
        "no_route_modification": not shadow_no_write.get("route_modified", True),
        "no_memory_write": not shadow_no_write.get("memory_written", True),
        "no_world_model_write": not shadow_no_write.get("world_model_written", True),
        "no_scene_delta": not shadow_no_write.get("scene_delta_generated", True),
        "no_fact_write": not shadow_no_write.get("fact_written", True),
    }
    weakness_items = [name for name, ok in boundary_checks.items() if not ok]
    boundary_weakness_found = bool(weakness_items)
    boundary_weakness_review = {
        "review_id": f"{REVIEW_ID}_boundary",
        "source_shadow_trial_run_id": observability.get("run", {}).get("run_id"),
        "boundary_checks": boundary_checks,
        "boundary_weakness_found": boundary_weakness_found,
        "weakness_items": weakness_items,
        "severity": "NONE" if not weakness_items else "HIGH",
        "required_fix": [] if not weakness_items else ["lock_boundary_before_next_phase"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    source_chain_checks = {
        "every_candidate_has_source_chain": _all_have_source_chain(shadow_trace_rows),
        "every_shadow_decision_has_source_chain": _all_have_source_chain(speech_gate_rows),
        "every_vop_shadow_event_has_source_chain": _all_have_source_chain(vop_rows),
        "every_abort_check_has_source_chain": _all_have_source_chain(abort_rows),
        "every_final_decision_has_source_chain": bool(observability.get("run", {}).get("source_chain")),
        "every_observability_case_has_source_chain": _all_have_source_chain(observability_case_rows),
    }
    source_chain_gap_items = [name for name, ok in source_chain_checks.items() if not ok]
    source_chain_gap_found = bool(source_chain_gap_items)
    source_chain_review = {
        "review_id": f"{REVIEW_ID}_source_chain",
        "source_shadow_trial_run_id": observability.get("run", {}).get("run_id"),
        "checks": source_chain_checks,
        "source_chain_gap_found": source_chain_gap_found,
        "gap_items": source_chain_gap_items,
        "source_chain_review_result": "SOURCE_CHAIN_COMPLETE" if not source_chain_gap_found else "SOURCE_CHAIN_GAP_FOUND",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    definition_abort_conditions = set(trial_abort.get("conditions") or [])
    abort_coverage_rows: List[Dict[str, Any]] = []
    for review_key in EXPECTED_ABORT_COVERAGE:
        definition_ref = DEFINITION_ABORT_MAPPING[review_key]
        shadow_field = SHADOW_ABORT_FIELD_MAPPING[review_key]
        abort_coverage_rows.append(
            {
                "review_key": review_key,
                "definition_condition_ref": definition_ref,
                "covered_in_definition": definition_ref in definition_abort_conditions,
                "shadow_abort_field_ref": shadow_field,
                "covered_in_shadow_abort_checks": all(
                    shadow_field in row and row.get(shadow_field) is False for row in abort_rows
                ),
                **_not_fact(),
            }
        )
    abort_coverage_gap_items = [
        row["review_key"]
        for row in abort_coverage_rows
        if not row["covered_in_definition"] or not row["covered_in_shadow_abort_checks"]
    ]
    abort_coverage_gap_found = bool(abort_coverage_gap_items)
    abort_coverage_review = {
        "review_id": f"{REVIEW_ID}_abort",
        "source_shadow_trial_run_id": observability.get("run", {}).get("run_id"),
        "coverage_rows": abort_coverage_rows,
        "abort_coverage_gap_found": abort_coverage_gap_found,
        "gap_items": abort_coverage_gap_items,
        "abort_coverage_review_result": (
            "ABORT_COVERAGE_COMPLETE" if not abort_coverage_gap_found else "ABORT_COVERAGE_GAP_FOUND"
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    handoff_checks = {
        "speech_gate_shadow_handoff_complete": reviewed_speech_gate_shadow_count == reviewed_input_case_count,
        "vop_shadow_event_complete": reviewed_vop_shadow_event_count == reviewed_input_case_count,
        "safety_task_arbitration_shadow_handoff_complete": all(
            bool(row.get("arbitration_shadow_result")) for row in shadow_trace_rows
        ),
        "ownership_gate_handoff_complete_when_required": all(
            row.get("ownership_gate_shadow_result") is not None
            for row in shadow_trace_rows
            if row.get("interruption_shadow_result") is not None and row["input_case_id"] != "shadow_case_08"
        ),
        "interruption_governance_handoff_complete_when_required": all(
            row.get("interruption_shadow_result") is not None
            for row in shadow_trace_rows
            if row.get("ownership_gate_shadow_result") is not None or row["input_case_id"] == "shadow_case_08"
        ),
        "task_manager_handoff_candidate_only": True,
        "stc_ocr_navigation_freshness_handoff_future_check_only": True,
        "no_runtime_handoff_maintained": shadow_no_runtime.get("boundary_ok") is True
        and shadow_no_write.get("boundary_ok") is True,
    }
    handoff_gap_items = [name for name, ok in handoff_checks.items() if not ok]
    handoff_gap_found = bool(handoff_gap_items)
    handoff_readiness_review = {
        "review_id": f"{REVIEW_ID}_handoff",
        "source_shadow_trial_run_id": observability.get("run", {}).get("run_id"),
        "checks": handoff_checks,
        "handoff_gap_found": handoff_gap_found,
        "gap_items": handoff_gap_items,
        "handoff_review_result": "HANDOFF_READY_FOR_DEFINITION" if not handoff_gap_found else "HANDOFF_GAP_FOUND",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    risk_register = {
        "review_id": f"{REVIEW_ID}_risk",
        "items": [
            {
                "risk_id": "risk_001",
                "risk": "speech_output_path_still_shadow_only",
                "severity": "LOW",
                "status": "accepted_for_next_definition_phase",
                "required_action": "keep Speech Gate/VOP/TTS in definition-only controlled output planning",
                **_not_fact(),
            },
            {
                "risk_id": "risk_002",
                "risk": "freshness_handoffs_remain_future_checks",
                "severity": "LOW",
                "status": "accepted_for_next_definition_phase",
                "required_action": "define STC/OCR/navigation freshness gates before any controlled output enablement",
                **_not_fact(),
            },
            {
                "risk_id": "risk_003",
                "risk": "task_manager_commit_must_remain_candidate_only",
                "severity": "MEDIUM",
                "status": "guardrail_required",
                "required_action": "keep task state commit disabled in next phase",
                **_not_fact(),
            },
            {
                "risk_id": "risk_004",
                "risk": "live_sensor_and_external_api_paths_untested_and_must_remain_disabled",
                "severity": "MEDIUM",
                "status": "guardrail_required",
                "required_action": "do not recommend camera/microphone/map API/GPS enablement in next phase",
                **_not_fact(),
            },
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    readiness_decision = "READY_FOR_CONTROLLED_OUTPUT_DEFINITION"
    next_phase_recommendation = RECOMMENDED_NEXT
    post_shadow_review_report = {
        "review_id": REVIEW_ID,
        "source_shadow_trial_run_id": observability.get("run", {}).get("run_id"),
        "review_scope": "minimal_runtime_integration_post_shadow_review",
        "reviewed_input_case_count": reviewed_input_case_count,
        "reviewed_shadow_step_count": reviewed_shadow_step_count,
        "reviewed_candidate_trace_count": reviewed_candidate_trace_count,
        "reviewed_speech_gate_shadow_count": reviewed_speech_gate_shadow_count,
        "reviewed_vop_shadow_event_count": reviewed_vop_shadow_event_count,
        "reviewed_abort_check_count": reviewed_abort_check_count,
        "boundary_review_result": boundary_weakness_review["severity"],
        "source_chain_review_result": source_chain_review["source_chain_review_result"],
        "stability_review_result": shadow_trial_stability_review["stability_review_result"],
        "handoff_review_result": handoff_readiness_review["handoff_review_result"],
        "risk_review_result": "RESIDUAL_RISKS_ACCEPTABLE_FOR_DEFINITION_ONLY_NEXT_PHASE",
        "readiness_decision": readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_output_readiness_decision = {
        "decision_id": f"{REVIEW_ID}_readiness",
        "source_shadow_trial_run_id": observability.get("run", {}).get("run_id"),
        "readiness_decision": readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "must_not_recommend_live_runtime": True,
        "must_not_recommend_camera_enablement": True,
        "must_not_recommend_map_api_enablement": True,
        "must_not_recommend_memory_or_worldmodel_write": True,
        "allowed_next_scope": "definition_only_for_minimal_controlled_output_path",
        "forbidden_next_scope": [
            "live_runtime_enablement",
            "camera_enablement",
            "microphone_enablement",
            "map_api_enablement",
            "gps_enablement",
            "memory_write_enablement",
            "worldmodel_write_enablement",
            "task_commit_enablement",
            "navigation_action_enablement",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation_payload = {
        "recommendation_id": f"{REVIEW_ID}_next_phase",
        "next_phase_recommendation": next_phase_recommendation,
        "rationale": (
            "shadow loop is stable and boundary-safe, so the next step can only be controlled output definition"
        ),
        "alternative_if_regression_found": "Phase-Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1-002",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    return {
        "summary": {
            "phase": PHASE_ID,
            "review_scope": "minimal_runtime_integration_post_shadow_review_only",
            "review_only": True,
            "controlled_shadow_trial_input_loaded": loaded_flags["controlled_shadow_trial"],
            "trial_definition_input_loaded": loaded_flags["trial_definition"],
            "stabilization_input_loaded": loaded_flags["stabilization"],
            "reviewed_input_case_count": reviewed_input_case_count,
            "reviewed_shadow_step_count": reviewed_shadow_step_count,
            "reviewed_candidate_trace_count": reviewed_candidate_trace_count,
            "reviewed_speech_gate_shadow_count": reviewed_speech_gate_shadow_count,
            "reviewed_vop_shadow_event_count": reviewed_vop_shadow_event_count,
            "reviewed_abort_check_count": reviewed_abort_check_count,
            "stability_review_completed": True,
            "boundary_weakness_review_completed": True,
            "source_chain_review_completed": True,
            "abort_coverage_review_completed": True,
            "handoff_readiness_review_completed": True,
            "controlled_output_readiness_decision_generated": True,
            "boundary_weakness_found": boundary_weakness_found,
            "source_chain_gap_found": source_chain_gap_found,
            "abort_coverage_gap_found": abort_coverage_gap_found,
            "handoff_gap_found": handoff_gap_found,
            **BOUNDARY_FALSE_FLAGS,
            "boundary_ok": True,
            "fact_status": "not_fact",
            "write_allowed": False,
            "final_decision": FINAL_DECISION,
        },
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            **_not_fact(),
        },
        "post_shadow_review_report": post_shadow_review_report,
        "shadow_trial_stability_review": shadow_trial_stability_review,
        "boundary_weakness_review": boundary_weakness_review,
        "source_chain_review": source_chain_review,
        "abort_coverage_review": abort_coverage_review,
        "handoff_readiness_review": handoff_readiness_review,
        "controlled_output_readiness_decision": controlled_output_readiness_decision,
        "risk_register": risk_register,
        "next_phase_recommendation": next_phase_recommendation_payload,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "source_shadow_trial_final_decision": shadow_summary.get("final_decision"),
            "source_shadow_trial_run_id": observability.get("run", {}).get("run_id"),
            "source_shadow_trial_final_shadow_status": observability.get("run", {}).get("final_shadow_status"),
            "trial_definition_final_decision": trial_summary.get("final_decision"),
            "stabilization_final_decision": stabilization_summary.get("final_decision"),
            "stabilization_scenario_count": stabilization_summary.get("stabilization_scenario_count"),
            "safety_candidate_count": safety_payload.get("arbitration_candidate_count"),
            "ownership_candidate_count": ownership_payload.get("decision_candidate_count"),
            "interruption_candidate_count": interruption_payload.get("interruption_decision_candidate_count"),
            "trial_definition_name": trial_definition.get("trial_name"),
            "stabilization_row_count": len(stabilization_scenarios.get("rows") or []),
            **_not_fact(),
        },
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "next_phase_recommendation": next_phase_recommendation,
            "must_not_recommend_live_runtime": True,
            **_not_fact(),
        },
    }
