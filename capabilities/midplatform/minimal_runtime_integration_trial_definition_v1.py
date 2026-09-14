# -*- coding: utf-8 -*-
"""Minimal Runtime Integration Trial Definition v1.

Phase-Minimal-Runtime-Integration-Trial-Definition-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Minimal-Runtime-Integration-Trial-Definition-v1-001"
FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_TRIAL_DEFINITION_READY_FOR_CONTROLLED_SHADOW_TRIAL"
RECOMMENDED_NEXT = "Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1"
SOURCE_CHAIN = "minimal_runtime_integration_trial_definition_v1"

ROOT_INPUT_SPECS = [
    (
        "stabilization",
        "basic_navigation_guidance_loop_stabilization_test_v1_smoke_v0",
        ["summary.json"],
    ),
    (
        "basic_navigation_loop",
        "basic_navigation_guidance_loop_dryrun_v1_smoke_v0",
        ["basic_navigation_guidance_loop_dryrun_v1_summary.json"],
    ),
    (
        "safety_task_arbitration",
        "safety_task_arbitration_policy_v1_smoke_v0",
        ["safety_task_arbitration_policy_v1_summary.json"],
    ),
    (
        "ownership_gate",
        "voice_command_ownership_gate_policy_v1_smoke_v0",
        ["voice_command_ownership_gate_decision_candidates_v1.json"],
    ),
    (
        "interruption_governance",
        "voice_interruption_governance_dryrun_v1_smoke_v0",
        ["summary.json", "interruption_decision_candidates.json"],
    ),
]

REQUIRED_DOCS = [
    "docs/architecture/midplatform/LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_TEST_V1.md",
    "docs/architecture/midplatform/LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_DRYRUN_V1.md",
    "docs/architecture/midplatform/LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_COMMAND_OWNERSHIP_GATE_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_INTERRUPTION_GOVERNANCE_DRYRUN_V1.md",
    "docs/architecture/midplatform/LUNA_VOICE_DIALOGUE_TASK_CONTROL_RUNTIME_DRYRUN_V1.md",
    "docs/architecture/voice/LUNA_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md",
    "docs/architecture/LUNA_VOICE_OUTPUT_SPEECH_GATE_MAINLINE_CONTRACT_V0.md",
    "docs/architecture/midplatform/LUNA_NAVIGATION_GUIDANCE_TO_SPEECH_CANDIDATE_ADAPTER_V1.md",
    "docs/architecture/midplatform/LUNA_TASK_MANAGER_RUNTIME_DRYRUN_V1.md",
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_STATE_RUNTIME_DRYRUN_V1.md",
    "docs/architecture/midplatform/LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
    "docs/architecture/midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md",
    "docs/architecture/system_health/LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md",
]

OPTIONAL_DOC_GLOBS = {
    "hardware_camera_control_contract": "**/*HARDWARE*CAMERA*CONTROL*CONTRACT*.md",
    "vision_evidence_lifecycle": "**/*VISION*EVIDENCE*LIFECYCLE*.md",
    "ocrrequest_docs": "**/*OCRREQUEST*.md",
    "evidence_pack_docs": "**/*EVIDENCE*PACK*.md",
    "gps_context": "**/*GPS*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
    "memory_governance": "**/*MEMORY*GOVERN*.md",
    "simulation_benchmark": "**/*SIMULATION*.md",
}

BOUNDARY_FALSE_FLAGS = {
    "runtime_trial_executed": False,
    "runtime_camera_invoked": False,
    "runtime_microphone_invoked": False,
    "runtime_asr_invoked": False,
    "runtime_voiceprint_invoked": False,
    "runtime_face_recognition_invoked": False,
    "runtime_tts_invoked": False,
    "runtime_tts_stopped": False,
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


def run_minimal_runtime_integration_trial_definition_v1(
    *,
    stabilization_root: str,
    basic_navigation_loop_root: str,
    safety_task_arbitration_root: str,
    ownership_gate_root: str,
    interruption_governance_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    workspace = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "stabilization": Path(stabilization_root).resolve(),
        "basic_navigation_loop": Path(basic_navigation_loop_root).resolve(),
        "safety_task_arbitration": Path(safety_task_arbitration_root).resolve(),
        "ownership_gate": Path(ownership_gate_root).resolve(),
        "interruption_governance": Path(interruption_governance_root).resolve(),
    }

    input_root_rows: List[Dict[str, Any]] = []
    loaded_flags: Dict[str, bool] = {}
    for intake_id, _, artifacts in ROOT_INPUT_SPECS:
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
                "missing_impact": "definition_check_partial" if not loaded else "none",
                **_not_fact(),
            }
        )
    input_root_rows.extend(_doc_rows(workspace))

    stabilization_summary = _read_json(roots["stabilization"] / "summary.json") or {}
    basic_summary = _read_json(
        roots["basic_navigation_loop"] / "basic_navigation_guidance_loop_dryrun_v1_summary.json"
    ) or {}
    safety_summary = _read_json(
        roots["safety_task_arbitration"] / "safety_task_arbitration_policy_v1_summary.json"
    ) or {}
    ownership_rows = _read_json(
        roots["ownership_gate"] / "voice_command_ownership_gate_decision_candidates_v1.json"
    ) or {}
    interruption_summary = _read_json(roots["interruption_governance"] / "summary.json") or {}

    boundary = _boundary_payload()

    allowed_in_future = [
        {
            "module_id": "controlled_sample_input",
            "classification": "allowed_in_future_minimal_trial",
            "mode": "CONTROLLED_ENABLE",
            "rationale": "use fixture/stub input only; no live sensors",
            **_not_fact(),
        },
        {
            "module_id": "stub_frame_input",
            "classification": "allowed_in_future_minimal_trial",
            "mode": "CONTROLLED_ENABLE",
            "rationale": "recorded frame sequence or offline frame trace",
            **_not_fact(),
        },
        {
            "module_id": "basic_navigation_guidance_loop_runtime_candidate",
            "classification": "allowed_in_future_minimal_trial",
            "mode": "CONTROLLED_ENABLE",
            "rationale": "candidate-only loop execution path under runtime guard",
            **_not_fact(),
        },
        {
            "module_id": "safety_task_arbitration_runtime_candidate",
            "classification": "allowed_in_future_minimal_trial",
            "mode": "CONTROLLED_ENABLE",
            "rationale": "arbitration remains candidate/traceable",
            **_not_fact(),
        },
        {
            "module_id": "speech_candidate_generation",
            "classification": "allowed_in_future_minimal_trial",
            "mode": "CONTROLLED_ENABLE",
            "rationale": "speech request candidate generation is needed to prove the minimal loop",
            **_not_fact(),
        },
        {
            "module_id": "speech_gate_shadow",
            "classification": "allowed_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "gate decision may be shadowed without runtime side effects",
            **_not_fact(),
        },
        {
            "module_id": "vop_shadow_or_controlled_output_placeholder",
            "classification": "allowed_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "output plane stays shadow/placeholder in the first minimal trial",
            **_not_fact(),
        },
        {
            "module_id": "system_health_runtime_check_candidate",
            "classification": "allowed_in_future_minimal_trial",
            "mode": "CONTROLLED_ENABLE",
            "rationale": "health observation is allowed only as passive check candidate",
            **_not_fact(),
        },
        {
            "module_id": "structured_logging",
            "classification": "allowed_in_future_minimal_trial",
            "mode": "CONTROLLED_ENABLE",
            "rationale": "trial observability is mandatory",
            **_not_fact(),
        },
    ]

    shadow_only = [
        {
            "module_id": "speech_gate",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "no speech gate runtime side effects in the first trial",
            **_not_fact(),
        },
        {
            "module_id": "voice_output_plane",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "VOP emits only shadow events",
            **_not_fact(),
        },
        {
            "module_id": "tts",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "no real audio playback in the first minimal trial",
            **_not_fact(),
        },
        {
            "module_id": "ocr_provider",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "OCR provider remains shadow or simulated candidate source",
            **_not_fact(),
        },
        {
            "module_id": "asr",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "voice input should be simulated text, not real ASR",
            **_not_fact(),
        },
        {
            "module_id": "camera",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "first trial uses recorded/stub frames, not live camera",
            **_not_fact(),
        },
        {
            "module_id": "gps",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "GPS must remain simulated or absent",
            **_not_fact(),
        },
        {
            "module_id": "map_context",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "map context cannot trigger external API effects",
            **_not_fact(),
        },
        {
            "module_id": "task_manager_commit",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "task manager commit remains disabled in first trial",
            **_not_fact(),
        },
        {
            "module_id": "system_health_recovery",
            "classification": "shadow_only_in_future_minimal_trial",
            "mode": "SHADOW_ONLY",
            "rationale": "recovery acts only as simulated suggestion",
            **_not_fact(),
        },
    ]

    forbidden_in_definition = [
        "live_camera_runtime",
        "live_microphone_runtime",
        "real_asr_runtime",
        "real_tts_runtime",
        "speech_gate_runtime",
        "vop_runtime",
        "ocr_provider_runtime",
        "map_api_runtime",
        "gps_runtime",
        "task_manager_commit_runtime",
        "navigation_action_execution",
        "worldmodel_write",
        "memory_write",
        "scene_delta_commit",
    ]

    forbidden_in_first_trial = [
        "worldmodel_write",
        "memory_write",
        "scene_delta_commit",
        "navigation_action_execution",
        "route_modification",
        "long_term_identity_write",
        "emotion_fact_write",
        "face_runtime",
        "voiceprint_runtime",
        "uncontrolled_tts_interruption",
        "external_api_side_effects",
        "map_api_runtime",
        "gps_runtime",
    ]

    runtime_module_boundary_matrix = {
        "allowed_in_future_minimal_trial": allowed_in_future,
        "shadow_only_in_future_minimal_trial": shadow_only,
        "forbidden_in_current_definition_phase": [
            {"module_id": item, "classification": "forbidden_in_current_definition_phase", **_not_fact()}
            for item in forbidden_in_definition
        ],
        "forbidden_even_in_first_minimal_trial": [
            {"module_id": item, "classification": "forbidden_even_in_first_minimal_trial", **_not_fact()}
            for item in forbidden_in_first_trial
        ],
        **_not_fact(),
    }

    trial_input_plan = {
        "allowed_future_input_sources": [
            "static_fixture_trace",
            "recorded_stub_frame_sequence",
            "simulated_task_context",
            "simulated_safety_event",
            "simulated_user_voice_text",
            "simulated_ocr_candidate",
            "simulated_navigation_guidance_candidate",
        ],
        "live_camera_recommended": False,
        "live_microphone_recommended": False,
        "input_recommendation": "first trial must use controlled sample input or stub trace only",
        "entrypoint_examples": [
            "fixture_json_trace",
            "offline_frame_sequence_manifest",
            "simulated_voice_text_event",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    trial_output_plan = {
        "allowed_future_outputs": [
            "guidance_candidate",
            "arbitration_decision_candidate",
            "speech_request_candidate",
            "speech_gate_shadow_decision",
            "vop_shadow_event",
            "boundary_report",
            "runtime_trace_log",
            "abort_report_if_triggered",
        ],
        "forbidden_future_outputs": [
            "real_navigation_action",
            "fact_write",
            "worldmodel_write",
            "memory_write",
            "scene_delta_commit",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    trial_safety_envelope = {
        "max_trial_duration_seconds": 60,
        "max_speech_candidate_count": 20,
        "max_task_candidate_count": 8,
        "max_ocr_candidate_count": 8,
        "max_error_count_before_abort": 1,
        "allowed_priority_levels": ["P0", "P1", "P2", "P3", "P4", "P5"],
        "p0_p1_safety_protection_required": True,
        "no_external_side_effects_required": True,
        "no_write_boundary_required": True,
        "abort_on_boundary_violation": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    abort_conditions = {
        "conditions": [
            "any_write_boundary_violation",
            "any_runtime_module_invoked_outside_allowlist",
            "task_state_committed_now_true",
            "world_model_written_true",
            "memory_written_true",
            "scene_delta_generated_true",
            "navigation_action_triggered_true",
            "map_api_invoked_true",
            "uncontrolled_tts_invoked_true",
            "speech_gate_runtime_invoked_when_shadow_only",
            "vop_runtime_invoked_when_shadow_only",
            "missing_source_chain",
            "stale_safety_speech_treated_as_current_fact",
            "non_owner_voice_triggers_task_control",
            "p0_safety_speech_cancelled_by_ordinary_stop",
        ],
        "abort_on_boundary_violation": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_plan = {
        "steps": [
            "return_to_stabilization_test_outputs",
            "disable_runtime_trial_flag",
            "preserve_logs",
            "write_abort_report",
            "no_state_rollback_needed_because_no_state_commit_allowed",
            "require_manual_review_before_retry",
        ],
        "rollback_to_phase": "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1-001",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    observability_requirements = {
        "required_fields": [
            "run_id",
            "build_id",
            "git_commit_if_available",
            "source_chain",
            "module_boundary_flags",
            "runtime_invocation_flags",
            "write_boundary_flags",
            "priority_trace",
            "ownership_trace",
            "interruption_trace",
            "arbitration_trace",
            "speech_handoff_trace",
            "error_trace",
            "abort_trace",
            "summary_metrics",
        ],
        "log_requirements": {
            "structured_logging_required": True,
            "candidate_trace_required": True,
            "boundary_flags_required": True,
            "abort_report_required_if_triggered": True,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    go_no_go_criteria = {
        "go_conditions": [
            "trial_definition_generated",
            "all_input_roots_loaded_or_optional_missing_marked",
            "allowed_shadow_forbidden_module_matrix_complete",
            "trial_input_plan_defined",
            "trial_output_plan_defined",
            "trial_safety_envelope_defined",
            "abort_conditions_defined",
            "rollback_plan_defined",
            "observability_requirements_defined",
            "no_runtime_executed",
            "no_write_executed",
            "boundary_ok_true",
            "verifier_go",
        ],
        "no_go_conditions": [
            "any_runtime_executed_in_definition_phase",
            "any_write_occurred",
            "any_forbidden_module_marked_as_allowed",
            "abort_conditions_missing",
            "rollback_plan_missing",
            "observability_plan_missing",
            "missing_source_chain",
            "unclear_distinction_between_definition_and_execution",
            "external_api_allowed",
            "map_api_allowed",
            "worldmodel_or_memory_write_allowed",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    minimal_runtime_trial_definition = {
        "trial_definition_id": "mritd_v1_001",
        "trial_name": "Luna Minimal Runtime Integration Controlled Shadow Trial",
        "trial_scope": "minimal_runtime_integration_trial_definition",
        "trial_mode": "DEFINITION_ONLY",
        "allowed_runtime_modules": [row["module_id"] for row in allowed_in_future],
        "shadow_only_modules": [row["module_id"] for row in shadow_only],
        "forbidden_modules": sorted(set(forbidden_in_definition + forbidden_in_first_trial)),
        "input_sources": trial_input_plan["allowed_future_input_sources"],
        "output_sinks": trial_output_plan["allowed_future_outputs"],
        "safety_constraints": {
            "p0_p1_protected": True,
            "abort_on_boundary_violation": True,
            "emergency_path_must_remain_preemptive": True,
        },
        "speech_constraints": {
            "speech_gate_shadow_only": True,
            "vop_shadow_only": True,
            "tts_real_output_forbidden_in_definition_phase": True,
            "uncontrolled_tts_interrupt_forbidden": True,
        },
        "task_constraints": {
            "task_commit_forbidden": True,
            "task_context_may_be_simulated": True,
            "pending_confirmation_must_be_preserved": True,
        },
        "ocr_constraints": {
            "ocr_provider_real_runtime_forbidden": True,
            "ocr_candidate_may_be_simulated": True,
            "ocr_output_must_remain_candidate_only": True,
        },
        "vision_constraints": {
            "live_camera_forbidden_in_definition_phase": True,
            "recorded_or_stub_frame_only_for_first_trial": True,
        },
        "map_gps_constraints": {
            "map_api_forbidden": True,
            "gps_runtime_forbidden": True,
            "route_modification_forbidden": True,
        },
        "memory_worldmodel_constraints": {
            "worldmodel_write_forbidden": True,
            "memory_write_forbidden": True,
            "fact_write_forbidden": True,
            "scene_delta_commit_forbidden": True,
        },
        "observability_requirements": observability_requirements["required_fields"],
        "abort_conditions": abort_conditions["conditions"],
        "rollback_plan": rollback_plan["steps"],
        "go_no_go_criteria": {
            "go": go_no_go_criteria["go_conditions"],
            "no_go": go_no_go_criteria["no_go_conditions"],
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    future_trial_execution_contract = {
        "contract_id": "future_minimal_runtime_trial_execution_contract_v1",
        "trial_mode": "DEFINITION_ONLY",
        "future_trial_mode": "FUTURE_CONTROLLED_TRIAL",
        "future_entrypoint": "controlled_fixture_or_stub_trace_only",
        "future_allowed_chain": [
            "controlled_sample_input_or_stub_frame",
            "basic_navigation_or_ocr_or_safety_candidate_generation",
            "safety_task_arbitration",
            "speech_candidate_generation",
            "speech_gate_shadow",
            "vop_shadow_or_controlled_output_placeholder",
            "structured_logging_and_boundary_check",
        ],
        "future_controlled_enable_points": [
            "candidate_generation_path",
            "structured_logging",
            "boundary_monitoring",
        ],
        "future_shadow_points": [
            "speech_gate",
            "voice_output_plane",
            "tts",
            "ocr_provider",
            "camera",
            "asr",
            "gps",
            "map_context",
        ],
        "future_exit_conditions": [
            "trial_duration_limit_reached",
            "abort_condition_triggered",
            "controlled_sample_exhausted",
        ],
        "must_abort_conditions_ref": abort_conditions["conditions"],
        "rollback_plan_ref": rollback_plan["steps"],
        "observability_ref": observability_requirements["required_fields"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": {
            "phase": PHASE_ID,
            "definition_scope": "minimal_runtime_integration_trial_definition_only",
            "runtime_trial_executed": False,
            "stabilization_input_loaded": loaded_flags["stabilization"],
            "basic_navigation_loop_input_loaded": loaded_flags["basic_navigation_loop"],
            "safety_task_arbitration_input_loaded": loaded_flags["safety_task_arbitration"],
            "ownership_gate_input_loaded": loaded_flags["ownership_gate"],
            "interruption_governance_input_loaded": loaded_flags["interruption_governance"],
            "trial_definition_generated": True,
            "runtime_module_boundary_matrix_defined": True,
            "trial_input_plan_defined": True,
            "trial_output_plan_defined": True,
            "trial_safety_envelope_defined": True,
            "abort_conditions_defined": True,
            "rollback_plan_defined": True,
            "observability_requirements_defined": True,
            "go_no_go_criteria_defined": True,
            "future_trial_execution_contract_defined": True,
            "stabilization_scenario_count_observed": stabilization_summary.get("stabilization_scenario_count", 0),
            "basic_navigation_baseline_count_observed": basic_summary.get("baseline_safety_request_count_observed", 0),
            "safety_arbitration_loaded": bool(safety_summary),
            "ownership_candidate_count_observed": ownership_rows.get("decision_candidate_count", 0),
            "interruption_candidate_count_observed": interruption_summary.get(
                "interruption_decision_candidate_count", 0
            ),
            **BOUNDARY_FALSE_FLAGS,
            "boundary_ok": True,
            "fact_status": "not_fact",
            "write_allowed": False,
            "final_decision": FINAL_DECISION,
            "recommended_next_phase": RECOMMENDED_NEXT,
        },
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            **_not_fact(),
        },
        "minimal_runtime_trial_definition": minimal_runtime_trial_definition,
        "runtime_module_boundary_matrix": runtime_module_boundary_matrix,
        "trial_input_plan": trial_input_plan,
        "trial_output_plan": trial_output_plan,
        "trial_safety_envelope": trial_safety_envelope,
        "abort_conditions": abort_conditions,
        "rollback_plan": rollback_plan,
        "observability_requirements": observability_requirements,
        "go_no_go_criteria": go_no_go_criteria,
        "future_trial_execution_contract": future_trial_execution_contract,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "recommended_next_phase": RECOMMENDED_NEXT,
            **_not_fact(),
        },
    }
