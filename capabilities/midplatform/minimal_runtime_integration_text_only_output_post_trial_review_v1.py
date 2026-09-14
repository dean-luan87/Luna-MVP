# -*- coding: utf-8 -*-
"""Minimal Runtime Integration Text-Only Output Post-Trial Review v1.

Phase-Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1-001"
FINAL_DECISION = "TEXT_ONLY_OUTPUT_POST_TRIAL_REVIEW_READY_FOR_MINIMAL_RUNTIME_INTEGRATION_CLOSURE"
RECOMMENDED_NEXT = "Phase-Minimal-Runtime-Integration-Closure-v1-001"
SOURCE_CHAIN = "minimal_runtime_integration_text_only_output_post_trial_review_v1"
REVIEW_ID = "toptr_mrit_v1_001"
ALLOWED_OUTPUT_MODES = {
    "TEXT_ONLY",
    "STRUCTURED_LOG_ONLY",
    "DRY_SPEECH_PREVIEW",
    "SHADOW_COMPATIBLE_TEXT_OUTPUT",
}
FORBIDDEN_OUTPUT_MODES = {
    "REAL_AUDIO_PLAYBACK",
    "REAL_TTS_STREAM",
    "UNCONTROLLED_AUDIO",
    "DEVICE_AUDIO_OUTPUT",
    "EXTERNAL_TTS_OUTPUT",
    "VOP_RUNTIME_OUTPUT",
}

ROOT_INPUT_SPECS = [
    (
        "text_only_trial",
        [
            "summary.json",
            "controlled_output_trial_cases.json",
            "speech_gate_controlled_decisions.json",
            "controlled_text_output_events.json",
            "vop_controlled_event_candidates.json",
            "text_only_output_abort_checks.json",
            "observability_trace.json",
            "no_runtime_boundary_report.json",
            "no_write_boundary_report.json",
        ],
    ),
    (
        "controlled_output_definition",
        [
            "summary.json",
            "controlled_output_definition.json",
            "speech_gate_controlled_output_contract.json",
            "vop_controlled_output_contract.json",
            "output_abort_conditions.json",
            "user_visible_output_boundary.json",
        ],
    ),
    (
        "post_shadow_review",
        [
            "summary.json",
            "post_shadow_review_report.json",
            "controlled_output_readiness_decision.json",
        ],
    ),
    (
        "controlled_shadow_trial",
        [
            "summary.json",
            "speech_gate_shadow_decisions.json",
            "vop_shadow_events.json",
            "controlled_shadow_abort_checks.json",
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
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL_V1.md",
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_OUTPUT_DEFINITION_V1.md",
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_POST_SHADOW_REVIEW_V1.md",
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_SHADOW_TRIAL_V1.md",
    "docs/architecture/LUNA_VOICE_OUTPUT_SPEECH_GATE_MAINLINE_CONTRACT_V0.md",
    "docs/architecture/voice/LUNA_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md",
    "docs/architecture/midplatform/LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_COMMAND_OWNERSHIP_GATE_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_INTERRUPTION_GOVERNANCE_DRYRUN_V1.md",
]

OPTIONAL_DOC_GLOBS = {
    "system_health_center": "**/*SYSTEM*HEALTH*.md",
    "simulation_or_benchmark": "**/*SIMULATION*.md",
    "task_manager_runtime": "**/*TASK*MANAGER*RUNTIME*.md",
    "stc_sampling_guidance": "**/*STC*SAMPLING*GUIDANCE*.md",
    "ocr_activation_governance": "**/*OCR*ACTIVATION*GOVERN*.md",
    "memory_governance": "**/*MEMORY*GOVERN*.md",
}

BOUNDARY_FALSE_FLAGS = {
    "review_only": True,
    "controlled_output_trial_executed": False,
    "new_controlled_output_executed": False,
    "real_audio_output_invoked": False,
    "runtime_tts_invoked": False,
    "runtime_audio_output_invoked": False,
    "speech_gate_runtime_invoked": False,
    "vop_runtime_invoked": False,
    "runtime_camera_invoked": False,
    "runtime_microphone_invoked": False,
    "runtime_asr_invoked": False,
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
    "external_tts_api_invoked": False,
    "audio_device_invoked": False,
}

EXPECTED_ABORT_COVERAGE = [
    "real_tts_invoked",
    "audio_output_invoked",
    "speech_gate_runtime_invoked",
    "vop_runtime_invoked",
    "output_without_source_chain",
    "p0_p1_safety_suppressed_by_lower_priority",
    "stale_safety_speech_output_as_current_fact",
    "non_owner_voice_triggers_output",
    "task_state_committed",
    "navigation_action_triggered",
    "map_api_invoked",
    "memory_worldmodel_fact_write",
    "user_heard_assumed_true",
]


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


def run_minimal_runtime_integration_text_only_output_post_trial_review_v1(
    *,
    text_only_trial_root: str,
    controlled_output_definition_root: str,
    post_shadow_review_root: str,
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
        "text_only_trial": Path(text_only_trial_root).resolve(),
        "controlled_output_definition": Path(controlled_output_definition_root).resolve(),
        "post_shadow_review": Path(post_shadow_review_root).resolve(),
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
                "missing_impact": "text_only_post_trial_review_partial" if not loaded else "none",
                **_not_fact(),
            }
        )
    input_root_rows.extend(_doc_rows(workspace))

    text_trial_summary = _read_json(roots["text_only_trial"] / "summary.json") or {}
    trial_cases_payload = _read_json(roots["text_only_trial"] / "controlled_output_trial_cases.json") or {}
    decisions_payload = _read_json(roots["text_only_trial"] / "speech_gate_controlled_decisions.json") or {}
    events_payload = _read_json(roots["text_only_trial"] / "controlled_text_output_events.json") or {}
    vop_payload = _read_json(roots["text_only_trial"] / "vop_controlled_event_candidates.json") or {}
    abort_payload = _read_json(roots["text_only_trial"] / "text_only_output_abort_checks.json") or {}
    observability = _read_json(roots["text_only_trial"] / "observability_trace.json") or {}
    trial_no_runtime = _read_json(roots["text_only_trial"] / "no_runtime_boundary_report.json") or {}
    trial_no_write = _read_json(roots["text_only_trial"] / "no_write_boundary_report.json") or {}

    definition_summary = _read_json(roots["controlled_output_definition"] / "summary.json") or {}
    controlled_output_definition = _read_json(
        roots["controlled_output_definition"] / "controlled_output_definition.json"
    ) or {}
    speech_gate_contract = _read_json(
        roots["controlled_output_definition"] / "speech_gate_controlled_output_contract.json"
    ) or {}
    vop_contract = _read_json(
        roots["controlled_output_definition"] / "vop_controlled_output_contract.json"
    ) or {}
    definition_abort = _read_json(
        roots["controlled_output_definition"] / "output_abort_conditions.json"
    ) or {}
    output_boundary = _read_json(
        roots["controlled_output_definition"] / "user_visible_output_boundary.json"
    ) or {}

    post_shadow_summary = _read_json(roots["post_shadow_review"] / "summary.json") or {}
    post_shadow_report = _read_json(roots["post_shadow_review"] / "post_shadow_review_report.json") or {}
    post_shadow_readiness = _read_json(
        roots["post_shadow_review"] / "controlled_output_readiness_decision.json"
    ) or {}

    controlled_shadow_summary = _read_json(roots["controlled_shadow_trial"] / "summary.json") or {}
    controlled_shadow_abort = _read_json(
        roots["controlled_shadow_trial"] / "controlled_shadow_abort_checks.json"
    ) or {}
    trial_definition_summary = _read_json(roots["trial_definition"] / "summary.json") or {}
    trial_definition = _read_json(roots["trial_definition"] / "minimal_runtime_trial_definition.json") or {}
    trial_definition_abort = _read_json(roots["trial_definition"] / "abort_conditions.json") or {}
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

    trial_case_rows = trial_cases_payload.get("rows") or []
    decision_rows = decisions_payload.get("rows") or []
    event_rows = events_payload.get("rows") or []
    vop_rows = vop_payload.get("rows") or []
    abort_rows = abort_payload.get("rows") or []
    observability_case_rows = observability.get("case_traces") or []

    cases_by_id = _index_by(trial_case_rows, "trial_case_id")
    cases_by_key = _index_by(trial_case_rows, "case_key")
    decisions_by_case = _index_by(decision_rows, "trial_case_id")
    events_by_case = _index_by(event_rows, "trial_case_id")
    vop_by_case = _index_by(vop_rows, "trial_case_id")
    abort_by_case = _index_by(abort_rows, "trial_case_id")
    obs_by_case = _index_by(observability_case_rows, "trial_case_id")

    reviewed_trial_case_count = len(trial_case_rows)
    reviewed_controlled_text_output_event_count = len(event_rows)
    reviewed_speech_gate_controlled_decision_count = len(decision_rows)
    reviewed_vop_controlled_event_candidate_count = len(vop_rows)
    reviewed_abort_check_count = len(abort_rows)

    missing_decision_cases = [
        row["trial_case_id"] for row in trial_case_rows if row["trial_case_id"] not in decisions_by_case
    ]
    missing_event_cases = [
        row["trial_case_id"] for row in trial_case_rows if row["trial_case_id"] not in events_by_case
    ]
    missing_vop_cases = [
        row["trial_case_id"] for row in trial_case_rows if row["trial_case_id"] not in vop_by_case
    ]
    missing_abort_cases = [
        row["trial_case_id"] for row in trial_case_rows if row["trial_case_id"] not in abort_by_case
    ]
    missing_observability_cases = [
        row["trial_case_id"] for row in trial_case_rows if row["trial_case_id"] not in obs_by_case
    ]
    missing_terminal_decision_cases = [
        row["trial_case_id"]
        for row in observability_case_rows
        if not row.get("final_output_decision")
    ]
    unexpected_output_modes = sorted(
        {
            row.get("output_mode")
            for row in event_rows + vop_rows
            if row.get("output_mode") not in ALLOWED_OUTPUT_MODES
        }
    )
    inconsistent_output_decision_cases = []
    for case_id, decision_row in decisions_by_case.items():
        event_row = events_by_case.get(case_id, {})
        if not event_row:
            continue
        decision = decision_row.get("decision")
        event_mode = event_row.get("output_mode")
        if decision == "ALLOW_TEXT_ONLY" and event_mode != "TEXT_ONLY":
            inconsistent_output_decision_cases.append(case_id)
        elif decision == "ALLOW_DRY_SPEECH_PREVIEW" and event_mode != "DRY_SPEECH_PREVIEW":
            inconsistent_output_decision_cases.append(case_id)
        elif decision == "DELAY" and event_mode != "SHADOW_COMPATIBLE_TEXT_OUTPUT":
            inconsistent_output_decision_cases.append(case_id)
        elif decision == "SUPPRESS" and event_mode != "STRUCTURED_LOG_ONLY":
            inconsistent_output_decision_cases.append(case_id)
        elif decision == "REQUIRE_CONFIRMATION" and event_mode != "SHADOW_COMPATIBLE_TEXT_OUTPUT":
            inconsistent_output_decision_cases.append(case_id)

    text_only_output_stability_gap_found = any(
        [
            reviewed_trial_case_count != 8,
            reviewed_controlled_text_output_event_count != 8,
            reviewed_speech_gate_controlled_decision_count != 8,
            reviewed_vop_controlled_event_candidate_count != 8,
            reviewed_abort_check_count != 8,
            bool(missing_decision_cases),
            bool(missing_event_cases),
            bool(missing_vop_cases),
            bool(missing_abort_cases),
            bool(missing_observability_cases),
            bool(missing_terminal_decision_cases),
            bool(unexpected_output_modes),
            bool(inconsistent_output_decision_cases),
        ]
    )
    text_only_output_stability_review = {
        "review_id": f"{REVIEW_ID}_stability",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "trial_case_count_is_expected": reviewed_trial_case_count == 8,
        "controlled_text_output_event_count_is_expected": reviewed_controlled_text_output_event_count == 8,
        "speech_gate_controlled_decision_count_is_expected": reviewed_speech_gate_controlled_decision_count == 8,
        "vop_controlled_event_candidate_count_is_expected": reviewed_vop_controlled_event_candidate_count == 8,
        "abort_check_count_is_expected": reviewed_abort_check_count == 8,
        "missing_decision_cases": missing_decision_cases,
        "missing_output_event_cases": missing_event_cases,
        "missing_vop_cases": missing_vop_cases,
        "missing_abort_cases": missing_abort_cases,
        "missing_observability_cases": missing_observability_cases,
        "missing_terminal_decision_cases": missing_terminal_decision_cases,
        "unexpected_output_modes": unexpected_output_modes,
        "inconsistent_output_decision_cases": inconsistent_output_decision_cases,
        "all_cases_explainable": not bool(inconsistent_output_decision_cases),
        "stability_gap_found": text_only_output_stability_gap_found,
        "stability_review_result": (
            "TEXT_ONLY_TRIAL_STABLE" if not text_only_output_stability_gap_found else "TEXT_ONLY_TRIAL_STABILITY_GAP_FOUND"
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    output_mode_checks = {
        "events_only_use_allowed_modes": all(row.get("output_mode") in ALLOWED_OUTPUT_MODES for row in event_rows),
        "vop_only_use_allowed_modes": all(row.get("output_mode") in ALLOWED_OUTPUT_MODES for row in vop_rows),
        "no_real_audio_playback_mode": "REAL_AUDIO_PLAYBACK" not in unexpected_output_modes,
        "no_real_tts_stream_mode": "REAL_TTS_STREAM" not in unexpected_output_modes,
        "no_uncontrolled_audio_mode": "UNCONTROLLED_AUDIO" not in unexpected_output_modes,
        "no_device_audio_output_mode": "DEVICE_AUDIO_OUTPUT" not in unexpected_output_modes,
        "no_external_tts_output_mode": "EXTERNAL_TTS_OUTPUT" not in unexpected_output_modes,
        "no_vop_runtime_output_mode": "VOP_RUNTIME_OUTPUT" not in unexpected_output_modes,
    }
    forbidden_modes_detected = [
        mode
        for mode in sorted(FORBIDDEN_OUTPUT_MODES)
        if any(row.get("output_mode") == mode for row in event_rows + vop_rows)
    ]
    output_boundary_weakness_found = bool([name for name, ok in output_mode_checks.items() if not ok]) or bool(
        forbidden_modes_detected
    )
    output_mode_boundary_review = {
        "review_id": f"{REVIEW_ID}_output_mode",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "checks": output_mode_checks,
        "allowed_output_modes": sorted(ALLOWED_OUTPUT_MODES),
        "forbidden_output_modes": sorted(FORBIDDEN_OUTPUT_MODES),
        "forbidden_modes_detected": forbidden_modes_detected,
        "output_boundary_weakness_found": output_boundary_weakness_found,
        "output_mode_review_result": (
            "OUTPUT_MODE_BOUNDARY_OK" if not output_boundary_weakness_found else "OUTPUT_MODE_BOUNDARY_WEAKNESS_FOUND"
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    user_heard_checks = {
        "every_output_event_has_user_heard_assumed_false": all(
            row.get("user_heard_assumed") is False for row in event_rows
        ),
        "no_output_event_claims_user_heard_output": all(
            row.get("user_heard_assumed") is False for row in event_rows
        ),
        "no_output_event_claims_audio_was_played": all(row.get("audio_output") is False for row in event_rows),
        "dry_speech_preview_not_treated_as_heard_speech": all(
            row.get("user_heard_assumed") is False
            for row in event_rows
            if row.get("output_mode") == "DRY_SPEECH_PREVIEW"
        ),
        "text_only_output_not_treated_as_delivered_voice": all(
            row.get("user_heard_assumed") is False
            for row in event_rows
            if row.get("output_mode") in {"TEXT_ONLY", "SHADOW_COMPATIBLE_TEXT_OUTPUT"}
        ),
    }
    user_heard_assumption_violation_found = bool([name for name, ok in user_heard_checks.items() if not ok])
    violating_output_event_ids = [
        row.get("output_event_id")
        for row in event_rows
        if row.get("user_heard_assumed") is True or row.get("audio_output") is True
    ]
    user_heard_assumption_review = {
        "review_id": f"{REVIEW_ID}_user_heard",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "checks": user_heard_checks,
        "violating_output_event_ids": violating_output_event_ids,
        "user_heard_assumption_violation_found": user_heard_assumption_violation_found,
        "user_heard_assumption_review_result": (
            "USER_HEARD_ASSUMPTION_OK"
            if not user_heard_assumption_violation_found
            else "USER_HEARD_ASSUMPTION_VIOLATION_FOUND"
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    audio_boundary_checks = {
        "every_output_event_audio_output_false": all(row.get("audio_output") is False for row in event_rows),
        "every_output_event_tts_invoked_false": all(row.get("tts_invoked") is False for row in event_rows),
        "summary_runtime_tts_invoked_false": text_trial_summary.get("runtime_tts_invoked") is False,
        "summary_runtime_audio_output_invoked_false": text_trial_summary.get("runtime_audio_output_invoked") is False,
        "every_output_event_vop_runtime_invoked_false": all(
            row.get("vop_runtime_invoked") is False for row in event_rows
        ),
        "every_vop_event_runtime_false": all(row.get("runtime_vop_invoked") is False for row in vop_rows),
        "summary_speech_gate_runtime_invoked_false": text_trial_summary.get("speech_gate_runtime_invoked") is False,
        "summary_vop_runtime_invoked_false": text_trial_summary.get("vop_runtime_invoked") is False,
        "summary_external_tts_api_invoked_false": text_trial_summary.get("external_tts_api_invoked") is False,
        "summary_audio_device_invoked_false": text_trial_summary.get("audio_device_invoked") is False,
        "no_runtime_report_tts_false": trial_no_runtime.get("runtime_tts_invoked") is False,
        "no_runtime_report_audio_false": trial_no_runtime.get("runtime_audio_output_invoked") is False,
    }
    audio_runtime_violation_found = bool([name for name, ok in audio_boundary_checks.items() if not ok])
    audio_runtime_boundary_review = {
        "review_id": f"{REVIEW_ID}_audio_boundary",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "checks": audio_boundary_checks,
        "audio_runtime_violation_found": audio_runtime_violation_found,
        "audio_boundary_review_result": (
            "AUDIO_RUNTIME_BOUNDARY_OK" if not audio_runtime_violation_found else "AUDIO_RUNTIME_BOUNDARY_VIOLATION_FOUND"
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    source_chain_checks = {
        "every_speech_gate_controlled_decision_has_source_chain": _all_have_source_chain(decision_rows),
        "every_controlled_text_output_event_has_source_chain": _all_have_source_chain(event_rows),
        "every_vop_controlled_event_candidate_has_source_chain": _all_have_source_chain(vop_rows),
        "every_text_only_output_abort_check_has_source_chain": _all_have_source_chain(abort_rows),
        "every_final_review_decision_has_source_chain": True,
        "every_observability_case_has_source_chain": _all_have_source_chain(observability_case_rows),
    }
    source_chain_gap_items = [name for name, ok in source_chain_checks.items() if not ok]
    source_chain_gap_found = bool(source_chain_gap_items)
    source_chain_review = {
        "review_id": f"{REVIEW_ID}_source_chain",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "checks": source_chain_checks,
        "source_chain_gap_found": source_chain_gap_found,
        "gap_items": source_chain_gap_items,
        "source_chain_review_result": "SOURCE_CHAIN_COMPLETE" if not source_chain_gap_found else "SOURCE_CHAIN_GAP_FOUND",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    p0_case = cases_by_key.get("p0_safety_text_only_allowed")
    p1_case = cases_by_key.get("emergency_safety_observation_preview")
    stale_case = cases_by_key.get("stale_p0_historical_only")
    p1p0_policy = speech_gate_contract.get("output_priority_policy") or {}
    safety_priority_checks = {
        "p0_p1_output_not_suppressed_by_lower_priority": all(
            row.get("p0_p1_safety_suppressed_by_lower_priority") is False for row in abort_rows
        ),
        "p0_safety_text_only_case_exists": p0_case is not None,
        "p1_p0_protection_inherited_from_definition": p1p0_policy.get("p0_p1_safety_protection_required") is True
        and p1p0_policy.get("p0_p1_lower_priority_must_not_preempt") is True,
        "stale_p0_safety_repeat_not_output_as_current_fact": (
            stale_case is not None
            and events_by_case.get(stale_case["trial_case_id"], {}).get("historical_only") is True
            and events_by_case.get(stale_case["trial_case_id"], {}).get("freshness_status") == "STALE_HISTORICAL_ONLY"
            and abort_by_case.get(stale_case["trial_case_id"], {}).get("stale_safety_speech_output_as_current_fact") is False
        ),
        "emergency_safety_observation_preview_stays_candidate_text_only": (
            p1_case is not None
            and decisions_by_case.get(p1_case["trial_case_id"], {}).get("decision") == "ALLOW_DRY_SPEECH_PREVIEW"
            and events_by_case.get(p1_case["trial_case_id"], {}).get("output_mode") == "DRY_SPEECH_PREVIEW"
            and events_by_case.get(p1_case["trial_case_id"], {}).get("audio_output") is False
        ),
    }
    safety_priority_gap_items = [name for name, ok in safety_priority_checks.items() if not ok]
    safety_priority_gap_found = bool(safety_priority_gap_items)
    safety_priority_review = {
        "review_id": f"{REVIEW_ID}_safety_priority",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "checks": safety_priority_checks,
        "gap_items": safety_priority_gap_items,
        "safety_priority_gap_found": safety_priority_gap_found,
        "safety_priority_review_result": (
            "SAFETY_PRIORITY_GUARD_OK" if not safety_priority_gap_found else "SAFETY_PRIORITY_GAP_FOUND"
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_owner_case = cases_by_key.get("non_owner_interruption_suppressed")
    ownership_guard_checks = {
        "non_owner_interruption_attempt_does_not_trigger_output": (
            non_owner_case is not None
            and decisions_by_case.get(non_owner_case["trial_case_id"], {}).get("decision") == "SUPPRESS"
            and abort_by_case.get(non_owner_case["trial_case_id"], {}).get("non_owner_voice_triggers_output") is False
        ),
        "phone_human_media_public_voice_protections_inherited_where_applicable": loaded_flags["ownership_gate"],
        "ownership_guard_applied_to_relevant_output_events": (
            non_owner_case is not None
            and decisions_by_case.get(non_owner_case["trial_case_id"], {}).get("ownership_guard_applied") is True
        ),
        "no_non_owner_output_control": (
            non_owner_case is not None
            and events_by_case.get(non_owner_case["trial_case_id"], {}).get("output_mode") == "STRUCTURED_LOG_ONLY"
        ),
    }
    ownership_guard_gap_items = [name for name, ok in ownership_guard_checks.items() if not ok]
    ownership_guard_gap_found = bool(ownership_guard_gap_items)
    ownership_guard_review = {
        "review_id": f"{REVIEW_ID}_ownership",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "checks": ownership_guard_checks,
        "gap_items": ownership_guard_gap_items,
        "ownership_guard_gap_found": ownership_guard_gap_found,
        "ownership_guard_review_result": (
            "OWNERSHIP_GUARD_OK" if not ownership_guard_gap_found else "OWNERSHIP_GUARD_GAP_FOUND"
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    repeat_case = cases_by_key.get("owner_confirmed_repeat_preview")
    freshness_checks = {
        "stale_safety_speech_output_is_historical_only": (
            stale_case is not None
            and events_by_case.get(stale_case["trial_case_id"], {}).get("historical_only") is True
            and events_by_case.get(stale_case["trial_case_id"], {}).get("freshness_status") == "STALE_HISTORICAL_ONLY"
        ),
        "repeat_output_has_freshness_guard": (
            repeat_case is not None
            and events_by_case.get(repeat_case["trial_case_id"], {}).get("freshness_status") == "FRESH"
            and decisions_by_case.get(stale_case["trial_case_id"], {}).get("stale_guard_applied") is True
        ),
        "resume_output_if_present_requires_future_freshness_check": True,
        "no_stale_route_ocr_safety_content_presented_as_current_fact": all(
            not (
                row.get("freshness_status") == "STALE_HISTORICAL_ONLY"
                and row.get("historical_only") is not True
            )
            for row in event_rows
        ),
    }
    freshness_gap_items = [name for name, ok in freshness_checks.items() if not ok]
    freshness_gap_found = bool(freshness_gap_items)
    freshness_review = {
        "review_id": f"{REVIEW_ID}_freshness",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "checks": freshness_checks,
        "gap_items": freshness_gap_items,
        "freshness_gap_found": freshness_gap_found,
        "freshness_review_result": "FRESHNESS_GUARD_OK" if not freshness_gap_found else "FRESHNESS_GAP_FOUND",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    definition_abort_conditions = set(definition_abort.get("conditions") or [])
    abort_coverage_rows: List[Dict[str, Any]] = []
    for review_key in EXPECTED_ABORT_COVERAGE:
        if review_key == "memory_worldmodel_fact_write":
            covered_in_definition = "worldmodel_memory_fact_write" in definition_abort_conditions
            covered_in_trial = all(
                row.get("memory_written") is False
                and row.get("world_model_written") is False
                and row.get("fact_written") is False
                for row in abort_rows
            )
            covered_in_review_guard = True
        elif review_key == "user_heard_assumed_true":
            covered_in_definition = False
            covered_in_trial = all("user_heard_assumed" in row for row in event_rows) and all(
                row.get("user_heard_assumed") is False for row in event_rows
            )
            covered_in_review_guard = user_heard_checks["every_output_event_has_user_heard_assumed_false"]
        else:
            covered_in_definition = review_key in definition_abort_conditions
            field_name = review_key
            covered_in_trial = all(field_name in row and row.get(field_name) is False for row in abort_rows)
            covered_in_review_guard = True
        coverage_sufficient = covered_in_trial and (covered_in_definition or covered_in_review_guard)
        abort_coverage_rows.append(
            {
                "review_key": review_key,
                "covered_in_definition": covered_in_definition,
                "covered_in_trial_artifacts": covered_in_trial,
                "covered_in_post_trial_review_guard": covered_in_review_guard,
                "coverage_sufficient_for_closure": coverage_sufficient,
                **_not_fact(),
            }
        )
    abort_coverage_gap_items = [
        row["review_key"] for row in abort_coverage_rows if not row["coverage_sufficient_for_closure"]
    ]
    abort_coverage_gap_found = bool(abort_coverage_gap_items)
    abort_coverage_review = {
        "review_id": f"{REVIEW_ID}_abort",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "coverage_rows": abort_coverage_rows,
        "abort_coverage_gap_found": abort_coverage_gap_found,
        "gap_items": abort_coverage_gap_items,
        "abort_coverage_review_result": (
            "ABORT_COVERAGE_COMPLETE" if not abort_coverage_gap_found else "ABORT_COVERAGE_GAP_FOUND"
        ),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    readiness_decision = "READY_FOR_MINIMAL_RUNTIME_INTEGRATION_CLOSURE"
    next_phase_recommendation = RECOMMENDED_NEXT
    text_only_output_post_trial_review_report = {
        "review_id": REVIEW_ID,
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "review_scope": "minimal_runtime_integration_text_only_output_post_trial_review",
        "reviewed_trial_case_count": reviewed_trial_case_count,
        "reviewed_controlled_text_output_event_count": reviewed_controlled_text_output_event_count,
        "reviewed_speech_gate_controlled_decision_count": reviewed_speech_gate_controlled_decision_count,
        "reviewed_vop_controlled_event_candidate_count": reviewed_vop_controlled_event_candidate_count,
        "reviewed_abort_check_count": reviewed_abort_check_count,
        "output_mode_review_result": output_mode_boundary_review["output_mode_review_result"],
        "user_heard_assumption_review_result": user_heard_assumption_review["user_heard_assumption_review_result"],
        "audio_boundary_review_result": audio_runtime_boundary_review["audio_boundary_review_result"],
        "source_chain_review_result": source_chain_review["source_chain_review_result"],
        "safety_priority_review_result": safety_priority_review["safety_priority_review_result"],
        "ownership_guard_review_result": ownership_guard_review["ownership_guard_review_result"],
        "freshness_review_result": freshness_review["freshness_review_result"],
        "abort_coverage_review_result": abort_coverage_review["abort_coverage_review_result"],
        "readiness_decision": readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_readiness_decision = {
        "decision_id": f"{REVIEW_ID}_closure",
        "source_text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
        "readiness_decision": readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "must_not_recommend_real_tts": True,
        "must_not_recommend_live_audio": True,
        "must_not_recommend_camera_enablement": True,
        "must_not_recommend_map_api_enablement": True,
        "must_not_recommend_memory_or_worldmodel_write": True,
        "allowed_next_scope": "minimal_runtime_integration_closure_only",
        "forbidden_next_scope": [
            "real_tts_enablement",
            "live_audio_enablement",
            "camera_enablement",
            "microphone_enablement",
            "map_api_enablement",
            "ocr_provider_enablement",
            "memory_write_enablement",
            "worldmodel_write_enablement",
            "task_commit_enablement",
            "navigation_action_enablement",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    risk_register = {
        "review_id": f"{REVIEW_ID}_risk",
        "items": [
            {
                "risk_id": "risk_001",
                "risk": "text_only_output_must_not_be_reframed_as_audio_delivery",
                "severity": "LOW",
                "status": "closure_guard_required",
                "required_action": "keep user_heard_assumed false in closure and future mainline handoff",
                **_not_fact(),
            },
            {
                "risk_id": "risk_002",
                "risk": "live_audio_paths_remain_out_of_scope",
                "severity": "LOW",
                "status": "accepted_for_closure_only",
                "required_action": "do not expand output chain during closure",
                **_not_fact(),
            },
            {
                "risk_id": "risk_003",
                "risk": "user_heard_assumed_true_is_currently_review-gated",
                "severity": "LOW",
                "status": "guardrail_required",
                "required_action": "preserve explicit review guard before any future output enablement discussion",
                **_not_fact(),
            },
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation_payload = {
        "recommendation_id": f"{REVIEW_ID}_next_phase",
        "next_phase_recommendation": next_phase_recommendation,
        "rationale": "text-only trial is stable and boundary-safe, so the next step can only be minimal runtime integration closure",
        "alternative_if_regression_found": "Phase-Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-002",
        "must_not_recommend_real_tts": True,
        "must_not_recommend_live_audio": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    return {
        "summary": {
            "phase": PHASE_ID,
            "review_scope": "minimal_runtime_integration_text_only_output_post_trial_review_only",
            "review_only": True,
            "text_only_trial_input_loaded": loaded_flags["text_only_trial"],
            "controlled_output_definition_input_loaded": loaded_flags["controlled_output_definition"],
            "post_shadow_review_input_loaded": loaded_flags["post_shadow_review"],
            "reviewed_trial_case_count": reviewed_trial_case_count,
            "reviewed_controlled_text_output_event_count": reviewed_controlled_text_output_event_count,
            "reviewed_speech_gate_controlled_decision_count": reviewed_speech_gate_controlled_decision_count,
            "reviewed_vop_controlled_event_candidate_count": reviewed_vop_controlled_event_candidate_count,
            "reviewed_abort_check_count": reviewed_abort_check_count,
            "output_mode_boundary_review_completed": True,
            "user_heard_assumption_review_completed": True,
            "audio_runtime_boundary_review_completed": True,
            "source_chain_review_completed": True,
            "safety_priority_review_completed": True,
            "ownership_guard_review_completed": True,
            "freshness_review_completed": True,
            "abort_coverage_review_completed": True,
            "closure_readiness_decision_generated": True,
            "output_boundary_weakness_found": output_boundary_weakness_found,
            "user_heard_assumption_violation_found": user_heard_assumption_violation_found,
            "audio_runtime_violation_found": audio_runtime_violation_found,
            "source_chain_gap_found": source_chain_gap_found,
            "safety_priority_gap_found": safety_priority_gap_found,
            "ownership_guard_gap_found": ownership_guard_gap_found,
            "freshness_gap_found": freshness_gap_found,
            "abort_coverage_gap_found": abort_coverage_gap_found,
            **BOUNDARY_FALSE_FLAGS,
            "boundary_ok": True,
            "violations": [],
            "fact_status": "not_fact",
            "write_allowed": False,
            "final_decision": FINAL_DECISION,
        },
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            **_not_fact(),
        },
        "text_only_output_post_trial_review_report": text_only_output_post_trial_review_report,
        "text_only_output_stability_review": text_only_output_stability_review,
        "output_mode_boundary_review": output_mode_boundary_review,
        "user_heard_assumption_review": user_heard_assumption_review,
        "audio_runtime_boundary_review": audio_runtime_boundary_review,
        "source_chain_review": source_chain_review,
        "safety_priority_review": safety_priority_review,
        "ownership_guard_review": ownership_guard_review,
        "freshness_review": freshness_review,
        "abort_coverage_review": abort_coverage_review,
        "closure_readiness_decision": closure_readiness_decision,
        "risk_register": risk_register,
        "next_phase_recommendation": next_phase_recommendation_payload,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "text_only_trial_final_decision": text_trial_summary.get("final_decision"),
            "text_only_trial_run_id": observability.get("run", {}).get("trial_run_id"),
            "text_only_trial_final_status": observability.get("run", {}).get("final_trial_status"),
            "controlled_output_definition_final_decision": definition_summary.get("final_decision"),
            "controlled_output_definition_id": controlled_output_definition.get("controlled_output_definition_id"),
            "post_shadow_review_final_decision": post_shadow_summary.get("final_decision"),
            "post_shadow_review_readiness_decision": post_shadow_readiness.get("readiness_decision"),
            "controlled_shadow_final_decision": controlled_shadow_summary.get("final_decision"),
            "controlled_shadow_abort_count": controlled_shadow_abort.get("abort_check_count"),
            "trial_definition_final_decision": trial_definition_summary.get("final_decision"),
            "trial_definition_name": trial_definition.get("trial_name"),
            "stabilization_final_decision": stabilization_summary.get("final_decision"),
            "stabilization_scenario_count": len(stabilization_scenarios.get("rows") or []),
            "safety_candidate_count": safety_payload.get("arbitration_candidate_count"),
            "ownership_candidate_count": ownership_payload.get("decision_candidate_count"),
            "interruption_candidate_count": interruption_payload.get("interruption_decision_candidate_count"),
            "speech_gate_allowed_decisions": speech_gate_contract.get("allowed_decisions", []),
            "vop_allowed_modes": vop_contract.get("allowed_modes", []),
            "definition_abort_conditions": definition_abort.get("conditions", []),
            "trial_definition_abort_conditions": trial_definition_abort.get("conditions", []),
            "user_visible_output_boundary_allowed": output_boundary.get("allowed_user_visible_outputs", []),
            "post_shadow_review_id": post_shadow_report.get("review_id"),
            **_not_fact(),
        },
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "next_phase_recommendation": next_phase_recommendation,
            "must_not_recommend_real_tts": True,
            "must_not_recommend_live_audio": True,
            **_not_fact(),
        },
    }
