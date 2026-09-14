# -*- coding: utf-8 -*-
"""Minimal Runtime Integration Controlled Output Definition v1.

Phase-Minimal-Runtime-Integration-Controlled-Output-Definition-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Minimal-Runtime-Integration-Controlled-Output-Definition-v1-001"
FINAL_DECISION = "CONTROLLED_OUTPUT_DEFINITION_READY_FOR_TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL"
RECOMMENDED_NEXT = "Phase-Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-001"
SOURCE_CHAIN = "minimal_runtime_integration_controlled_output_definition_v1"

ROOT_INPUT_SPECS = [
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
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_POST_SHADOW_REVIEW_V1.md",
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
    "definition_only": True,
    "controlled_output_enabled": False,
    "controlled_output_executed": False,
    "runtime_trial_executed": False,
    "runtime_camera_invoked": False,
    "runtime_microphone_invoked": False,
    "runtime_asr_invoked": False,
    "runtime_tts_invoked": False,
    "runtime_audio_output_invoked": False,
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

ALLOWED_FUTURE_OUTPUT_MODES = [
    "text_console_output_controlled",
    "structured_log_output_controlled",
    "speech_request_candidate_to_shadow",
    "speech_gate_controlled_decision_candidate",
    "vop_controlled_event_candidate",
    "tts_placeholder_or_dry_output_candidate",
]

SHADOW_ONLY_OUTPUT_MODES = [
    "speech_request_candidate_to_shadow",
    "speech_gate_controlled_decision_candidate",
    "vop_controlled_event_candidate",
]

FORBIDDEN_OUTPUT_MODES = [
    "REAL_AUDIO_PLAYBACK",
    "REAL_TTS_STREAM",
    "UNCONTROLLED_AUDIO",
    "direct_tts",
    "direct_vop_runtime",
    "audio_playback",
    "navigation_instruction_execution",
    "route_modification",
    "external_notification",
    "mobile_push",
    "device_vibration",
    "haptic_output",
    "worldmodel_memory_fact_write",
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


def run_minimal_runtime_integration_controlled_output_definition_v1(
    *,
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
                "missing_impact": "definition_check_partial" if not loaded else "none",
                **_not_fact(),
            }
        )
    input_root_rows.extend(_doc_rows(workspace))

    post_shadow_summary = _read_json(roots["post_shadow_review"] / "summary.json") or {}
    post_shadow_report = _read_json(roots["post_shadow_review"] / "post_shadow_review_report.json") or {}
    post_shadow_readiness = _read_json(
        roots["post_shadow_review"] / "controlled_output_readiness_decision.json"
    ) or {}

    shadow_summary = _read_json(roots["controlled_shadow_trial"] / "summary.json") or {}
    shadow_speech_gate = _read_json(
        roots["controlled_shadow_trial"] / "speech_gate_shadow_decisions.json"
    ) or {}
    shadow_vop = _read_json(roots["controlled_shadow_trial"] / "vop_shadow_events.json") or {}
    shadow_abort = _read_json(
        roots["controlled_shadow_trial"] / "controlled_shadow_abort_checks.json"
    ) or {}

    trial_summary = _read_json(roots["trial_definition"] / "summary.json") or {}
    trial_definition = _read_json(roots["trial_definition"] / "minimal_runtime_trial_definition.json") or {}
    trial_abort = _read_json(roots["trial_definition"] / "abort_conditions.json") or {}

    stabilization_summary = _read_json(roots["stabilization"] / "summary.json") or {}
    safety_summary = _read_json(
        roots["safety_task_arbitration"] / "safety_task_arbitration_policy_v1_summary.json"
    ) or {}
    ownership_payload = _read_json(
        roots["ownership_gate"] / "voice_command_ownership_gate_decision_candidates_v1.json"
    ) or {}
    interruption_payload = _read_json(
        roots["interruption_governance"] / "interruption_decision_candidates.json"
    ) or {}

    speech_gate_controlled_output_contract = {
        "contract_id": "speech_gate_controlled_output_contract_v1_001",
        "input": "speech_request_candidate",
        "required_fields": [
            "priority",
            "text_ref",
            "source_chain",
            "safety_status",
            "ownership_status",
            "interruption_status",
            "freshness_status",
        ],
        "output": "controlled_speech_gate_decision_candidate",
        "allowed_decisions": [
            "ALLOW_TEXT_ONLY",
            "ALLOW_DRY_TTS_PLACEHOLDER",
            "DELAY",
            "SUPPRESS",
            "REQUIRE_CONFIRMATION",
            "ABORT_OUTPUT",
        ],
        "forbidden": [
            "direct_tts",
            "direct_vop_runtime",
            "audio_playback",
            "speech_without_source_chain",
        ],
        "output_priority_policy": {
            "p0_p1_safety_protection_required": True,
            "p0_p1_lower_priority_must_not_preempt": True,
            "p0_p1_can_abort_lower_priority_output": True,
        },
        "stale_safety_speech_historical_only_required": True,
        "non_owner_speech_cannot_trigger_output": True,
        "source_chain_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    vop_controlled_output_contract = {
        "contract_id": "vop_controlled_output_contract_v1_001",
        "input": "controlled_speech_gate_decision_candidate",
        "output": "vop_controlled_event_candidate",
        "allowed_modes": [
            "SHADOW_ONLY",
            "TEXT_ONLY",
            "DRY_OUTPUT_PLACEHOLDER",
        ],
        "forbidden_modes": [
            "REAL_AUDIO_PLAYBACK",
            "REAL_TTS_STREAM",
            "UNCONTROLLED_AUDIO",
        ],
        "must_preserve_speech_request_id": True,
        "must_preserve_source_chain": True,
        "must_expose_output_boundary_flags": True,
        "no_audio_device_call": True,
        "no_tts_engine_call": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tts_placeholder_policy = {
        "policy_id": "tts_placeholder_policy_v1_001",
        "dry_tts_placeholder_allowed_later": True,
        "real_tts_invocation_allowed_now": False,
        "local_audio_playback_allowed_now": False,
        "external_tts_api_allowed": False,
        "text_only_output_preferred_for_first_controlled_output": True,
        "max_output_length_chars": 180,
        "max_output_events_per_run": 8,
        "p0_p1_output_preemption_policy": "P0_P1_PREEMPT_LOWER_PRIORITY_OUTPUTS",
        "interruption_stop_pause_resume_only_as_candidate": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    user_visible_output_boundary = {
        "boundary_id": "user_visible_output_boundary_v1_001",
        "allowed_user_visible_outputs": [
            "console_text_line",
            "structured_jsonl_event",
            "dry_speech_text_preview",
            "controlled_debug_panel_entry",
        ],
        "forbidden_user_visible_outputs": [
            "real_audio_output",
            "navigation_instruction_execution",
            "route_modification",
            "external_notification",
            "mobile_push",
            "device_vibration",
            "haptic_output",
            "worldmodel_memory_fact_write",
        ],
        "text_only_first_trial_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    output_abort_conditions = {
        "conditions": [
            "speech_request_missing_source_chain",
            "speech_gate_decision_missing_source_chain",
            "vop_event_missing_source_chain",
            "real_tts_invoked",
            "audio_output_invoked",
            "speech_gate_runtime_invoked_unexpectedly",
            "vop_runtime_invoked_unexpectedly",
            "uncontrolled_output_mode_detected",
            "p0_safety_suppressed_by_lower_priority",
            "stale_safety_speech_output_as_current_fact",
            "non_owner_voice_triggers_output",
            "worldmodel_memory_fact_write",
            "task_state_commit",
            "navigation_action_triggered",
            "external_api_invoked",
        ],
        "abort_on_uncontrolled_output": True,
        "abort_on_missing_source_chain": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    output_recovery_policy = {
        "policy_id": "output_recovery_policy_v1_001",
        "steps": [
            "abort_output",
            "write_abort_report",
            "disable_controlled_output_flag",
            "return_to_shadow_only_mode",
            "preserve_logs",
            "require_manual_review",
            "no_state_rollback_needed_because_no_state_commit_allowed",
        ],
        "recovery_returns_to_shadow_only": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_output_observability = {
        "observability_id": "controlled_output_observability_v1_001",
        "required_fields": [
            "run_id",
            "source_chain",
            "speech_request_id",
            "speech_gate_decision_id",
            "vop_event_id",
            "output_mode",
            "priority",
            "safety_status",
            "ownership_status",
            "interruption_status",
            "freshness_status",
            "boundary_flags",
            "abort_flags",
            "output_length",
            "output_event_count",
            "final_output_decision",
        ],
        "source_chain_required_for_every_output_contract": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    go_no_go_criteria = {
        "go_conditions": [
            "controlled_output_definition_generated",
            "speech_gate_controlled_output_contract_defined",
            "vop_controlled_output_contract_defined",
            "tts_placeholder_policy_defined",
            "user_visible_output_boundary_defined",
            "output_abort_conditions_defined",
            "output_recovery_policy_defined",
            "controlled_output_observability_defined",
            "no_real_output_enabled",
            "no_runtime_invoked",
            "no_write_occurred",
            "boundary_ok_true",
        ],
        "no_go_conditions": [
            "any_real_audio_output_allowed_now",
            "real_tts_allowed_now",
            "vop_runtime_allowed_now",
            "speech_gate_runtime_allowed_now",
            "missing_source_chain_requirement",
            "no_abort_policy",
            "no_recovery_policy",
            "p0_p1_safety_protection_missing",
            "stale_safety_speech_protection_missing",
            "non_owner_output_protection_missing",
            "external_api_side_effect_allowed",
            "memory_worldmodel_fact_write_allowed",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_output_definition = {
        "controlled_output_definition_id": "cod_v1_001",
        "source_post_shadow_review_id": post_shadow_report.get("review_id"),
        "definition_scope": "minimal_runtime_integration_controlled_output_definition",
        "allowed_future_output_modes": ALLOWED_FUTURE_OUTPUT_MODES,
        "shadow_only_output_modes": SHADOW_ONLY_OUTPUT_MODES,
        "forbidden_output_modes": FORBIDDEN_OUTPUT_MODES,
        "speech_gate_controlled_output_contract_ref": "speech_gate_controlled_output_contract_v1_001",
        "vop_controlled_output_contract_ref": "vop_controlled_output_contract_v1_001",
        "tts_placeholder_policy_ref": "tts_placeholder_policy_v1_001",
        "user_visible_output_boundary_ref": "user_visible_output_boundary_v1_001",
        "output_priority_policy_ref": "speech_gate_controlled_output_contract_v1_001.output_priority_policy",
        "interruption_output_control_policy_ref": "tts_placeholder_policy_v1_001.interruption_stop_pause_resume_only_as_candidate",
        "abort_conditions_ref": "output_abort_conditions_v1_001",
        "recovery_policy_ref": "output_recovery_policy_v1_001",
        "observability_requirements_ref": "controlled_output_observability_v1_001",
        "go_no_go_criteria_ref": "controlled_output_go_no_go_criteria_v1_001",
        "next_phase_recommendation": RECOMMENDED_NEXT,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommendation_id": "controlled_output_next_phase_v1_001",
        "next_phase_recommendation": RECOMMENDED_NEXT,
        "must_not_recommend_live_audio": True,
        "must_not_recommend_camera_enablement": True,
        "must_not_recommend_map_api_enablement": True,
        "must_not_recommend_memory_or_worldmodel_write": True,
        "rationale": "only text-only controlled output trial is allowed after definition-only boundary lock",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    return {
        "summary": {
            "phase": PHASE_ID,
            "definition_scope": "minimal_runtime_integration_controlled_output_definition_only",
            "definition_only": True,
            "post_shadow_review_input_loaded": loaded_flags["post_shadow_review"],
            "controlled_shadow_trial_input_loaded": loaded_flags["controlled_shadow_trial"],
            "trial_definition_input_loaded": loaded_flags["trial_definition"],
            "controlled_output_definition_generated": True,
            "speech_gate_controlled_output_contract_defined": True,
            "vop_controlled_output_contract_defined": True,
            "tts_placeholder_policy_defined": True,
            "user_visible_output_boundary_defined": True,
            "output_abort_conditions_defined": True,
            "output_recovery_policy_defined": True,
            "controlled_output_observability_defined": True,
            "go_no_go_criteria_defined": True,
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
        "controlled_output_definition": controlled_output_definition,
        "speech_gate_controlled_output_contract": speech_gate_controlled_output_contract,
        "vop_controlled_output_contract": vop_controlled_output_contract,
        "tts_placeholder_policy": tts_placeholder_policy,
        "user_visible_output_boundary": user_visible_output_boundary,
        "output_abort_conditions": {
            "abort_conditions_id": "output_abort_conditions_v1_001",
            **output_abort_conditions,
        },
        "output_recovery_policy": output_recovery_policy,
        "controlled_output_observability": controlled_output_observability,
        "go_no_go_criteria": {
            "criteria_id": "controlled_output_go_no_go_criteria_v1_001",
            **go_no_go_criteria,
        },
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "post_shadow_review_final_decision": post_shadow_summary.get("final_decision"),
            "post_shadow_review_readiness_decision": post_shadow_readiness.get("readiness_decision"),
            "shadow_trial_final_decision": shadow_summary.get("final_decision"),
            "shadow_speech_gate_count": shadow_speech_gate.get("speech_gate_shadow_decision_count"),
            "shadow_vop_count": shadow_vop.get("vop_shadow_event_count"),
            "shadow_abort_count": shadow_abort.get("abort_check_count"),
            "trial_definition_final_decision": trial_summary.get("final_decision"),
            "stabilization_final_decision": stabilization_summary.get("final_decision"),
            "safety_summary_loaded": bool(safety_summary),
            "ownership_candidate_count": ownership_payload.get("decision_candidate_count"),
            "interruption_candidate_count": interruption_payload.get("interruption_decision_candidate_count"),
            "trial_definition_name": trial_definition.get("trial_name"),
            "trial_definition_abort_conditions": trial_abort.get("conditions", []),
            **_not_fact(),
        },
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "next_phase_recommendation": RECOMMENDED_NEXT,
            "must_not_recommend_live_audio": True,
            **_not_fact(),
        },
    }
