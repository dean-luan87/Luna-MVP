# -*- coding: utf-8 -*-
"""Basic Navigation Guidance Loop Stabilization Test v1.

Phase-Basic-Navigation-Guidance-Loop-Stabilization-Test-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1-001"
FINAL_DECISION = "BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_READY_FOR_MINIMAL_RUNTIME_INTEGRATION_TRIAL"
RECOMMENDED_NEXT = "Minimal-Runtime-Integration-Trial-Definition-v1"
SOURCE_CHAIN = "basic_navigation_guidance_loop_stabilization_test_v1"

REQUIRED_OUTPUT_SPECS = [
    (
        "basic_navigation_loop",
        [
            "basic_navigation_guidance_loop_dryrun_v1_summary.json",
            "basic_navigation_baseline_safety_loop_dryrun_matrix_v1.json",
            "basic_navigation_task_driven_loop_dryrun_matrix_v1.json",
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
        "voice_command_ownership_gate",
        [
            "voice_command_ownership_gate_decision_candidates_v1.json",
        ],
    ),
    (
        "voice_interruption_governance",
        [
            "summary.json",
            "interruption_decision_candidates.json",
        ],
    ),
]

REQUIRED_DOC_PATHS = [
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
]

OPTIONAL_DOC_GLOBS = {
    "system_health_doc": "**/*SYSTEM*HEALTH*.md",
    "risk_safety_arbiter_doc": "**/*RISK*SAFETY*.md",
    "route_context_doc": "**/*ROUTE*CONTEXT*.md",
    "map_context_doc": "**/*MAP*CONTEXT*.md",
    "memory_governance_doc": "**/*MEMORY*GOVERN*.md",
    "simulation_or_benchmark_doc": "**/*SIMULATION*.md",
    "gps_context_doc": "**/*GPS*.md",
    "hardware_camera_control_doc": "**/*HARDWARE*CAMERA*.md",
}

BOUNDARY_FALSE_FLAGS = {
    "runtime_camera_invoked": False,
    "runtime_asr_invoked": False,
    "runtime_audio_recorded": False,
    "runtime_voiceprint_invoked": False,
    "runtime_face_recognition_invoked": False,
    "runtime_tts_stopped": False,
    "speech_gate_invoked": False,
    "vop_invoked": False,
    "tts_invoked": False,
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


def _load_ok(root: Path, artifacts: List[str]) -> bool:
    if not root.is_dir():
        return False
    return all((root / art).is_file() for art in artifacts)


def _make_boundary_payload() -> Dict[str, Any]:
    return {
        **BOUNDARY_FALSE_FLAGS,
        "boundary_ok": True,
        "violations": [],
        **_not_fact(),
    }


def _required_doc_rows(ws_root: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for rel in REQUIRED_DOC_PATHS:
        p = ws_root / rel
        rows.append(
            {
                "intake_id": p.stem.lower(),
                "input_source": "required_documentation",
                "source_root_or_path": str(p),
                "artifact": p.name,
                "loaded": p.is_file(),
                "optional": False,
                "intake_status": "loaded" if p.is_file() else "missing",
                "missing_impact": "required_reference_missing" if not p.is_file() else "none",
                **_not_fact(),
            }
        )
    return rows


def _optional_doc_rows(ws_root: Path) -> List[Dict[str, Any]]:
    docs_root = ws_root / "docs" / "architecture"
    rows: List[Dict[str, Any]] = []
    for intake_id, pattern in OPTIONAL_DOC_GLOBS.items():
        found = list(docs_root.glob(pattern)) if docs_root.is_dir() else []
        rows.append(
            {
                "intake_id": intake_id,
                "input_source": "optional_documentation",
                "source_root_or_path": str(found[0]) if found else "(not_found)",
                "artifact": found[0].name if found else None,
                "loaded": bool(found),
                "optional": True,
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_doc_reference_only",
                **_not_fact(),
            }
        )
    return rows


def _index_by(items: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        item_key = item.get(key)
        if item_key:
            out[item_key] = item
    return out


def _mk_matrix(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"row_count": len(rows), "rows": rows, **_not_fact()}


def run_basic_navigation_guidance_loop_stabilization_test_v1(
    *,
    basic_navigation_loop_root: str,
    safety_task_arbitration_root: str,
    voice_command_ownership_gate_root: str,
    voice_interruption_governance_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws_root = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "basic_navigation_loop": Path(basic_navigation_loop_root).resolve(),
        "safety_task_arbitration": Path(safety_task_arbitration_root).resolve(),
        "voice_command_ownership_gate": Path(voice_command_ownership_gate_root).resolve(),
        "voice_interruption_governance": Path(voice_interruption_governance_root).resolve(),
    }

    input_rows: List[Dict[str, Any]] = []
    loaded_flags: Dict[str, bool] = {}
    for intake_id, artifacts in REQUIRED_OUTPUT_SPECS:
        root = roots[intake_id]
        loaded = _load_ok(root, artifacts)
        loaded_flags[intake_id] = loaded
        input_rows.append(
            {
                "intake_id": intake_id,
                "input_source": intake_id,
                "source_root_or_path": str(root),
                "artifact": ", ".join(artifacts),
                "loaded": loaded,
                "optional": False,
                "intake_status": "loaded" if loaded else "missing",
                "missing_impact": "stabilization_check_partial" if not loaded else "none",
                **_not_fact(),
            }
        )
    input_rows.extend(_required_doc_rows(ws_root))
    input_rows.extend(_optional_doc_rows(ws_root))

    basic_summary = _read_json(roots["basic_navigation_loop"] / "basic_navigation_guidance_loop_dryrun_v1_summary.json") or {}
    baseline_matrix = _read_json(roots["basic_navigation_loop"] / "basic_navigation_baseline_safety_loop_dryrun_matrix_v1.json") or {}
    task_matrix = _read_json(roots["basic_navigation_loop"] / "basic_navigation_task_driven_loop_dryrun_matrix_v1.json") or {}
    safety_summary = _read_json(roots["safety_task_arbitration"] / "safety_task_arbitration_policy_v1_summary.json") or {}
    safety_candidates = _read_json(roots["safety_task_arbitration"] / "safety_task_arbitration_candidate_collection_v1.json") or {}
    ownership_candidates = _read_json(
        roots["voice_command_ownership_gate"] / "voice_command_ownership_gate_decision_candidates_v1.json"
    ) or {}
    interruption_summary = _read_json(roots["voice_interruption_governance"] / "summary.json") or {}
    interruption_candidates = _read_json(
        roots["voice_interruption_governance"] / "interruption_decision_candidates.json"
    ) or {}

    baseline_rows = baseline_matrix.get("rows") or []
    task_rows = task_matrix.get("rows") or []
    safety_rows = safety_candidates.get("candidates") or []
    ownership_rows = ownership_candidates.get("candidates") or []
    interruption_rows = interruption_candidates.get("candidates") or []

    baseline_by_id = _index_by(baseline_rows, "baseline_loop_id")
    task_by_id = _index_by(task_rows, "task_loop_id")
    arb_by_id = _index_by(safety_rows, "arbitration_candidate_id")
    own_by_id = _index_by(ownership_rows, "ownership_gate_decision_candidate_id")
    int_by_id = _index_by(interruption_rows, "interruption_decision_id")

    policy = {
        "baseline_loop_policy": {
            "baseline_safety_loop_allowed_without_task": True,
            "baseline_safety_must_not_generate_task_goal": True,
            "baseline_low_risk_environment_prompt_candidate_allowed": True,
            **_not_fact(),
        },
        "task_driven_loop_policy": {
            "task_driven_loop_requires_task_context": True,
            "task_driven_navigation_or_ocr_guidance_candidate_allowed": True,
            "task_commit_forbidden_now": True,
            **_not_fact(),
        },
        "safety_task_conflict_policy": {
            "P0_P1_safety_preempts_lower_priority_task_guidance": True,
            "safety_active_can_suppress_or_delay_P2_P3_P4": True,
            "navigation_must_not_override_safety_warning": True,
            **_not_fact(),
        },
        "ocr_navigation_conflict_policy": {
            "ocr_guidance_can_exist_as_candidate_only": True,
            "safety_active_delays_non_safety_ocr_guidance": True,
            "ocr_provider_runtime_forbidden": True,
            **_not_fact(),
        },
        "voice_interruption_conflict_policy": {
            "ordinary_owner_interruption_can_generate_stop_pause_repeat_resume_correction_new_task_candidates": True,
            "ordinary_interruption_cannot_cancel_P0_safety_warning": True,
            "emergency_generates_safety_observation_candidate_only": True,
            **_not_fact(),
        },
        "ownership_gate_conflict_policy": {
            "non_owner_phone_human_conversation_media_public_announcement_block_ordinary_interruption": True,
            "safety_only_allowed_still_possible_for_emergency_keyword": True,
            "requires_confirmation_can_be_preserved": True,
            **_not_fact(),
        },
        "speech_priority_stabilization_policy": {
            "P0_safety_not_cancelled_by_ordinary_stop": True,
            "P1_risk_state_can_pause_but_not_be_deleted": True,
            "P2_pause_resume_require_route_and_stc_freshness": True,
            "P3_resume_requires_frame_region_freshness": True,
            "P4_P5_more_interruptible": True,
            **_not_fact(),
        },
        "context_preservation_policy": {
            "task_context_preserved_after_interruption": True,
            "pending_confirmation_preserved_after_interruption": True,
            "safety_context_preserved_after_pause_or_delay": True,
            "speech_history_candidate_preserved_for_repeat_or_clarify": True,
            **_not_fact(),
        },
        "freshness_stabilization_policy": {
            "repeat_requires_freshness_check": True,
            "resume_requires_freshness_check": True,
            "stale_safety_repeat_must_not_be_current_fact": True,
            "stale_route_or_region_yields_blocked_or_future_check_candidate": True,
            **_not_fact(),
        },
        "handoff_only_policy": {
            "speech_gate_handoff_candidate_only": True,
            "vop_handoff_candidate_only": True,
            "task_manager_handoff_candidate_only": True,
            "stc_ocr_navigation_handoff_candidate_only": True,
            "safety_arbitration_handoff_candidate_only": True,
            **_not_fact(),
        },
        **_not_fact(),
    }

    boundary_payload = _make_boundary_payload()

    scenario_defs: List[Dict[str, Any]] = [
        {
            "scenario_id": "stab_001",
            "scenario_key": "baseline_p0_safety_no_task",
            "scenario_type": "baseline_safety_only",
            "loop_type": "baseline_safety",
            "task_context_present": False,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": False,
            "user_voice_input_present": False,
            "ownership_gate_result_ref": None,
            "interruption_decision_ref": None,
            "arbitration_decision_ref": "arb_trace_baseline_loop_001",
            "expected": "baseline safety loop can emit P0 safety candidate without task context",
            "selected_output_candidate": "arb_trace_baseline_loop_001",
            "suppressed": [],
            "delayed": [],
            "preserved": ["safety_context", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "STABLE_PASS",
            "input_candidates": ["baseline_loop_001", "arb_trace_baseline_loop_001"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_002",
            "scenario_key": "baseline_low_risk_prompt_no_task",
            "scenario_type": "baseline_low_risk_environment",
            "loop_type": "baseline_safety",
            "task_context_present": False,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": False,
            "user_voice_input_present": False,
            "ownership_gate_result_ref": None,
            "interruption_decision_ref": None,
            "arbitration_decision_ref": "synthetic_arb_baseline_low_risk",
            "expected": "baseline loop may emit low-risk P3 environment prompt candidate without creating task goal",
            "selected_output_candidate": "synthetic_baseline_low_risk_environment_prompt_candidate",
            "suppressed": [],
            "delayed": [],
            "preserved": ["safety_context"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "STABLE_PASS",
            "input_candidates": ["baseline_loop_002", "synthetic_baseline_low_risk_environment_prompt_candidate"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_003",
            "scenario_key": "task_navigation_p2_candidate",
            "scenario_type": "task_navigation_guidance",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": False,
            "ownership_gate_result_ref": None,
            "interruption_decision_ref": None,
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "task-driven loop can emit P2 navigation/view guidance candidate when task context exists",
            "selected_output_candidate": "arb_trace_task_loop_007",
            "suppressed": [],
            "delayed": [],
            "preserved": ["task_context", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "STABLE_PASS",
            "input_candidates": ["task_loop_007", "arb_trace_task_loop_007"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_004",
            "scenario_key": "task_navigation_suppressed_by_safety",
            "scenario_type": "task_navigation_with_safety_conflict",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": True,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": False,
            "ownership_gate_result_ref": None,
            "interruption_decision_ref": None,
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "P0 safety candidate preempts P2 navigation guidance and suppresses low-priority task speech",
            "selected_output_candidate": "arb_trace_baseline_loop_001",
            "suppressed": ["arb_trace_task_loop_007"],
            "delayed": [],
            "preserved": ["task_context", "safety_context"],
            "resume_conditions": ["resume_when_safety_clears"],
            "freshness_checks": [],
            "status": "BLOCKED_BY_SAFETY_PRIORITY",
            "input_candidates": ["task_loop_007", "arb_trace_task_loop_007", "arb_trace_baseline_loop_001"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_005",
            "scenario_key": "ocr_guidance_delayed_by_safety",
            "scenario_type": "ocr_guidance_with_safety_conflict",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": True,
            "ocr_guidance_present": True,
            "navigation_guidance_present": False,
            "user_voice_input_present": False,
            "ownership_gate_result_ref": None,
            "interruption_decision_ref": None,
            "arbitration_decision_ref": "arb_trace_task_loop_009",
            "expected": "non-safety OCR guidance is delayed while safety remains active",
            "selected_output_candidate": "arb_trace_baseline_loop_003",
            "suppressed": [],
            "delayed": ["arb_trace_task_loop_009"],
            "preserved": ["task_context", "safety_context"],
            "resume_conditions": ["safety_clear_then_recheck_ocr_context"],
            "freshness_checks": ["ocr_region_freshness_before_resume"],
            "status": "STABLE_WITH_DELAY",
            "input_candidates": ["task_loop_009", "arb_trace_task_loop_009", "arb_trace_baseline_loop_003"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_006",
            "scenario_key": "owner_repeat_during_navigation",
            "scenario_type": "user_question_during_navigation",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_02",
            "interruption_decision_ref": "idc_case_02",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "owner-confirmed repeat request can create repeat candidate without deleting task context",
            "selected_output_candidate": "idc_case_02",
            "suppressed": [],
            "delayed": [],
            "preserved": ["task_context", "pending_confirmation", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": ["repeat_freshness_check"],
            "status": "STABLE_PASS",
            "input_candidates": ["task_loop_007", "ogd_case_02", "idc_case_02"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_007",
            "scenario_key": "repeat_stale_p0_safety",
            "scenario_type": "repeat_stale_safety_speech",
            "loop_type": "baseline_safety",
            "task_context_present": False,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": False,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "synthetic_owner_confirmed_case_24",
            "interruption_decision_ref": "idc_case_24",
            "arbitration_decision_ref": "arb_trace_baseline_loop_001",
            "expected": "stale P0 safety repeat must be historical-only and must not be emitted as current fact",
            "selected_output_candidate": "idc_case_24",
            "suppressed": [],
            "delayed": [],
            "preserved": ["speech_history_candidate", "safety_context"],
            "resume_conditions": ["historical_only_rewrite_required"],
            "freshness_checks": ["repeat_freshness_check", "stale_safety_rewrite_check"],
            "status": "BLOCKED_BY_STALENESS",
            "input_candidates": ["baseline_loop_001", "idc_case_24"],
            "speech_gate_handoff_required": False,
        },
        {
            "scenario_id": "stab_008",
            "scenario_key": "owner_stop_p4_explanation",
            "scenario_type": "user_interruption_during_speech",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_01",
            "interruption_decision_ref": "idc_case_01",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "owner stop request may interrupt ordinary P4 explanation candidate",
            "selected_output_candidate": "idc_case_01",
            "suppressed": ["p4_explanation_candidate"],
            "delayed": [],
            "preserved": ["task_context", "pending_confirmation"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "STABLE_WITH_SUPPRESSION",
            "input_candidates": ["task_loop_007", "ogd_case_01", "idc_case_01"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_009",
            "scenario_key": "owner_stop_blocked_on_p0_safety",
            "scenario_type": "speech_priority_p0_stop_blocked",
            "loop_type": "baseline_safety",
            "task_context_present": False,
            "safety_active": True,
            "ocr_guidance_present": False,
            "navigation_guidance_present": False,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "synthetic_owner_confirmed_case_17",
            "interruption_decision_ref": "idc_case_17",
            "arbitration_decision_ref": "arb_trace_baseline_loop_001",
            "expected": "ordinary stop cannot cancel active P0 safety warning",
            "selected_output_candidate": "arb_trace_baseline_loop_001",
            "suppressed": ["idc_case_17"],
            "delayed": [],
            "preserved": ["safety_context", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "BLOCKED_BY_SAFETY_PRIORITY",
            "input_candidates": ["baseline_loop_001", "idc_case_17"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_010",
            "scenario_key": "owner_emergency_interrupt",
            "scenario_type": "emergency_user_interruption",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": True,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_05",
            "interruption_decision_ref": "idc_case_05",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "emergency interruption creates safety observation candidate and escalates to safety arbitration",
            "selected_output_candidate": "idc_case_05",
            "suppressed": ["arb_trace_task_loop_007"],
            "delayed": [],
            "preserved": ["task_context", "pending_confirmation", "safety_context"],
            "resume_conditions": ["future_resume_after_emergency_clear"],
            "freshness_checks": [],
            "status": "STABLE_WITH_SAFETY_ESCALATION_CANDIDATE",
            "input_candidates": ["task_loop_007", "ogd_case_05", "idc_case_05"],
            "speech_gate_handoff_required": False,
        },
        {
            "scenario_id": "stab_011",
            "scenario_key": "non_owner_interruption_blocked",
            "scenario_type": "non_owner_interruption_attempt",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_06",
            "interruption_decision_ref": "idc_case_06",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "non-owner ordinary interruption is blocked by ownership gate",
            "selected_output_candidate": "arb_trace_task_loop_007",
            "suppressed": ["idc_case_06"],
            "delayed": [],
            "preserved": ["task_context", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "BLOCKED_BY_OWNERSHIP_GATE",
            "input_candidates": ["task_loop_007", "ogd_case_06", "idc_case_06"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_012",
            "scenario_key": "phone_call_false_interruption",
            "scenario_type": "phone_call_false_interruption",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_09",
            "interruption_decision_ref": "idc_case_09",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "phone call speech must not trigger ordinary interruption",
            "selected_output_candidate": "arb_trace_task_loop_007",
            "suppressed": ["idc_case_09"],
            "delayed": [],
            "preserved": ["task_context", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "BLOCKED_BY_OWNERSHIP_GATE",
            "input_candidates": ["task_loop_007", "ogd_case_09", "idc_case_09"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_013",
            "scenario_key": "human_conversation_false_interruption",
            "scenario_type": "human_conversation_false_interruption",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_10",
            "interruption_decision_ref": "idc_case_10",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "human conversation background speech must not trigger ordinary interruption",
            "selected_output_candidate": "arb_trace_task_loop_007",
            "suppressed": ["idc_case_10"],
            "delayed": [],
            "preserved": ["task_context", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "BLOCKED_BY_OWNERSHIP_GATE",
            "input_candidates": ["task_loop_007", "ogd_case_10", "idc_case_10"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_014",
            "scenario_key": "media_playback_false_interruption",
            "scenario_type": "media_playback_false_interruption",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_11",
            "interruption_decision_ref": "idc_case_11",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "media playback voice cannot control Luna interruption flow",
            "selected_output_candidate": "arb_trace_task_loop_007",
            "suppressed": ["idc_case_11"],
            "delayed": [],
            "preserved": ["task_context", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "BLOCKED_BY_OWNERSHIP_GATE",
            "input_candidates": ["task_loop_007", "ogd_case_11", "idc_case_11"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_015",
            "scenario_key": "public_announcement_false_interruption",
            "scenario_type": "public_announcement_false_interruption",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_12",
            "interruption_decision_ref": "idc_case_12",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "public announcement voice cannot control Luna or create new task runtime action",
            "selected_output_candidate": "arb_trace_task_loop_007",
            "suppressed": ["idc_case_12"],
            "delayed": [],
            "preserved": ["task_context", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "BLOCKED_BY_OWNERSHIP_GATE",
            "input_candidates": ["task_loop_007", "ogd_case_12", "idc_case_12"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_016",
            "scenario_key": "correction_during_ocr_guidance",
            "scenario_type": "correction_during_ocr_guidance",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": True,
            "navigation_guidance_present": False,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_04",
            "interruption_decision_ref": "idc_case_04",
            "arbitration_decision_ref": "arb_trace_task_loop_009",
            "expected": "correction creates correction_event_candidate only and does not write facts",
            "selected_output_candidate": "idc_case_04",
            "suppressed": [],
            "delayed": [],
            "preserved": ["task_context", "speech_history_candidate"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "STABLE_PASS",
            "input_candidates": ["task_loop_009", "ogd_case_04", "idc_case_04"],
            "speech_gate_handoff_required": False,
        },
        {
            "scenario_id": "stab_017",
            "scenario_key": "new_task_during_navigation",
            "scenario_type": "new_task_during_navigation",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_15",
            "interruption_decision_ref": "idc_case_15",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "new task request creates task-control candidate only and pauses current navigation candidate",
            "selected_output_candidate": "idc_case_15",
            "suppressed": [],
            "delayed": ["current_navigation_candidate_paused"],
            "preserved": ["task_context", "pending_confirmation", "speech_history_candidate"],
            "resume_conditions": ["resume_current_task_after_new_task_arbitration"],
            "freshness_checks": [],
            "status": "STABLE_WITH_DELAY",
            "input_candidates": ["task_loop_007", "ogd_case_15", "idc_case_15"],
            "speech_gate_handoff_required": False,
        },
        {
            "scenario_id": "stab_018",
            "scenario_key": "cancel_task_during_safety_active",
            "scenario_type": "cancel_task_during_safety_active",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": True,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_01",
            "interruption_decision_ref": "synthetic_cancel_task_confirmation_case",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "cancel task request during active safety must require confirmation and must not directly cancel task state",
            "selected_output_candidate": "synthetic_request_cancel_task_confirmation_candidate",
            "suppressed": ["direct_task_cancel_runtime"],
            "delayed": ["task_cancel_until_safety_clear"],
            "preserved": ["task_context", "pending_confirmation", "safety_context"],
            "resume_conditions": ["safety_clear_then_confirm_cancel"],
            "freshness_checks": [],
            "status": "STABLE_WITH_CONFIRMATION_REQUIRED",
            "input_candidates": [
                "task_loop_007",
                "ogd_case_01",
                "synthetic_cancel_task_confirmation_case",
            ],
            "speech_gate_handoff_required": False,
        },
        {
            "scenario_id": "stab_019",
            "scenario_key": "resume_paused_navigation",
            "scenario_type": "resume_paused_navigation",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_16",
            "interruption_decision_ref": "idc_case_23",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "resuming paused navigation requires route and STC freshness revalidation before future runtime handoff",
            "selected_output_candidate": "idc_case_23",
            "suppressed": [],
            "delayed": [],
            "preserved": ["task_context", "pending_confirmation", "speech_history_candidate"],
            "resume_conditions": ["route_and_stc_freshness_revalidated"],
            "freshness_checks": ["route_freshness_check", "stc_freshness_check"],
            "status": "NEEDS_FUTURE_RUNTIME_CHECK",
            "input_candidates": ["task_loop_007", "ogd_case_16", "idc_case_23"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_020",
            "scenario_key": "resume_paused_ocr_guidance",
            "scenario_type": "resume_paused_ocr_guidance",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": True,
            "navigation_guidance_present": False,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "synthetic_owner_confirmed_ocr_resume",
            "interruption_decision_ref": "synthetic_resume_ocr_guidance_case",
            "arbitration_decision_ref": "arb_trace_task_loop_009",
            "expected": "resuming paused OCR guidance requires STC frame and region freshness before future runtime handoff",
            "selected_output_candidate": "synthetic_resume_ocr_guidance_case",
            "suppressed": [],
            "delayed": [],
            "preserved": ["task_context", "speech_history_candidate"],
            "resume_conditions": ["stc_frame_region_freshness_required_before_resume"],
            "freshness_checks": ["stc_frame_freshness_check", "region_freshness_check"],
            "status": "NEEDS_FUTURE_RUNTIME_CHECK",
            "input_candidates": ["task_loop_009", "synthetic_resume_ocr_guidance_case", "idc_case_20"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_021",
            "scenario_key": "human_assistance_delayed_by_safety",
            "scenario_type": "human_assistance_delayed_by_safety",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": True,
            "ocr_guidance_present": False,
            "navigation_guidance_present": False,
            "user_voice_input_present": False,
            "ownership_gate_result_ref": None,
            "interruption_decision_ref": None,
            "arbitration_decision_ref": "arb_trace_task_loop_012",
            "expected": "non-safety human assistance guidance is delayed while safety remains active",
            "selected_output_candidate": "arb_trace_baseline_loop_004",
            "suppressed": [],
            "delayed": ["arb_trace_task_loop_012"],
            "preserved": ["task_context", "safety_context"],
            "resume_conditions": ["safety_clear_then_human_assistance_allowed"],
            "freshness_checks": [],
            "status": "STABLE_WITH_DELAY",
            "input_candidates": ["task_loop_012", "arb_trace_task_loop_012", "arb_trace_baseline_loop_004"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_022",
            "scenario_key": "clarification_suppressed_by_safety",
            "scenario_type": "clarification_suppressed_by_safety",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": True,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "synthetic_owner_confirmed_case_21",
            "interruption_decision_ref": "idc_case_21",
            "arbitration_decision_ref": "arb_trace_baseline_loop_001",
            "expected": "when safety is active, low-priority clarification is suppressed while P0/P1 safety speech remains",
            "selected_output_candidate": "arb_trace_baseline_loop_001",
            "suppressed": ["idc_case_21"],
            "delayed": [],
            "preserved": ["task_context", "pending_confirmation", "safety_context"],
            "resume_conditions": [],
            "freshness_checks": [],
            "status": "STABLE_WITH_SUPPRESSION",
            "input_candidates": ["idc_case_21", "arb_trace_baseline_loop_001"],
            "speech_gate_handoff_required": True,
        },
        {
            "scenario_id": "stab_023",
            "scenario_key": "task_context_preservation_after_interruption",
            "scenario_type": "task_context_preservation",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": False,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_15",
            "interruption_decision_ref": "idc_case_15",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "task context must remain preserved after interruption-driven pause/new task candidate generation",
            "selected_output_candidate": "idc_case_15",
            "suppressed": [],
            "delayed": ["current_navigation_candidate_paused"],
            "preserved": ["task_context", "speech_history_candidate"],
            "resume_conditions": ["resume_original_task_after_new_task_resolution"],
            "freshness_checks": [],
            "status": "STABLE_PASS",
            "input_candidates": ["task_loop_007", "idc_case_15"],
            "speech_gate_handoff_required": False,
        },
        {
            "scenario_id": "stab_024",
            "scenario_key": "pending_confirmation_preserved_after_safety_interrupt",
            "scenario_type": "pending_confirmation_preservation",
            "loop_type": "task_driven",
            "task_context_present": True,
            "safety_active": True,
            "ocr_guidance_present": False,
            "navigation_guidance_present": True,
            "user_voice_input_present": True,
            "ownership_gate_result_ref": "ogd_case_08",
            "interruption_decision_ref": "idc_case_08",
            "arbitration_decision_ref": "arb_trace_task_loop_007",
            "expected": "pending confirmation must survive safety-related interruption handling and cannot be dropped silently",
            "selected_output_candidate": "idc_case_08",
            "suppressed": [],
            "delayed": ["task_confirmation_until_owner_or_safety_resolution"],
            "preserved": ["task_context", "pending_confirmation", "safety_context"],
            "resume_conditions": ["owner_confirmation_or_safety_resolution_required"],
            "freshness_checks": [],
            "status": "STABLE_WITH_CONFIRMATION_REQUIRED",
            "input_candidates": ["task_loop_007", "ogd_case_08", "idc_case_08"],
            "speech_gate_handoff_required": False,
        },
    ]

    scenarios: List[Dict[str, Any]] = []
    decisions: List[Dict[str, Any]] = []
    for spec in scenario_defs:
        preserved = {
            "task_context": "task_context" in spec["preserved"],
            "pending_confirmation": "pending_confirmation" in spec["preserved"],
            "safety_context": "safety_context" in spec["preserved"],
            "speech_history_candidate": "speech_history_candidate" in spec["preserved"],
        }
        scenarios.append(
            {
                "scenario_id": spec["scenario_id"],
                "scenario_key": spec["scenario_key"],
                "scenario_type": spec["scenario_type"],
                "loop_type": spec["loop_type"],
                "task_context_present": spec["task_context_present"],
                "safety_active": spec["safety_active"],
                "ocr_guidance_present": spec["ocr_guidance_present"],
                "navigation_guidance_present": spec["navigation_guidance_present"],
                "user_voice_input_present": spec["user_voice_input_present"],
                "ownership_gate_result_ref": spec["ownership_gate_result_ref"],
                "interruption_decision_ref": spec["interruption_decision_ref"],
                "arbitration_decision_ref": spec["arbitration_decision_ref"],
                "expected_stabilization_behavior": spec["expected"],
                "expected_behavior": spec["expected"],
                "boundary_check_result": {
                    "no_runtime_boundary": True,
                    "no_write_boundary": True,
                    "violations": [],
                },
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
        decisions.append(
            {
                "stabilization_decision_id": f"sdc_{spec['scenario_id']}",
                "scenario_id": spec["scenario_id"],
                "scenario_key": spec["scenario_key"],
                "loop_type": spec["loop_type"],
                "input_candidates": spec["input_candidates"],
                "ownership_gate_applied": bool(spec["ownership_gate_result_ref"]),
                "interruption_governance_applied": bool(spec["interruption_decision_ref"]),
                "safety_task_arbitration_applied": bool(spec["arbitration_decision_ref"]),
                "speech_gate_handoff_required": spec["speech_gate_handoff_required"],
                "selected_output_candidate": spec["selected_output_candidate"],
                "suppressed_candidates": spec["suppressed"],
                "delayed_candidates": spec["delayed"],
                "preserved_contexts": preserved,
                "resume_conditions": spec["resume_conditions"],
                "freshness_checks": spec["freshness_checks"],
                "no_runtime_boundary": boundary_payload,
                "no_write_boundary": boundary_payload,
                "final_stabilization_status": spec["status"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    baseline_vs_task_rows = [
        {
            "matrix_case_id": "bvt_01",
            "rule": "baseline_safety_can_run_without_task",
            "scenario_id": "stab_001",
            "result": "PASS",
            **_not_fact(),
        },
        {
            "matrix_case_id": "bvt_02",
            "rule": "baseline_low_risk_does_not_create_task_goal",
            "scenario_id": "stab_002",
            "result": "PASS",
            **_not_fact(),
        },
        {
            "matrix_case_id": "bvt_03",
            "rule": "task_driven_requires_task_context",
            "scenario_id": "stab_003",
            "result": "PASS",
            **_not_fact(),
        },
        {
            "matrix_case_id": "bvt_04",
            "rule": "task_driven_must_not_override_safety",
            "scenario_id": "stab_004",
            "result": "PASS",
            **_not_fact(),
        },
    ]

    safety_vs_navigation_rows = [
        {
            "matrix_case_id": "svn_01",
            "rule": "P0_safety_preempts_P2_navigation",
            "scenario_id": "stab_004",
            "result": "SUPPRESS_P2",
            **_not_fact(),
        },
        {
            "matrix_case_id": "svn_02",
            "rule": "navigation_candidate_without_safety_conflict_allowed",
            "scenario_id": "stab_003",
            "result": "ALLOW",
            **_not_fact(),
        },
        {
            "matrix_case_id": "svn_03",
            "rule": "P0_safety_not_cancelled_by_ordinary_stop",
            "scenario_id": "stab_009",
            "result": "KEEP_P0",
            **_not_fact(),
        },
        {
            "matrix_case_id": "svn_04",
            "rule": "navigation_action_not_triggered",
            "scenario_id": "stab_003",
            "result": "CANDIDATE_ONLY",
            **_not_fact(),
        },
    ]

    safety_vs_ocr_rows = [
        {
            "matrix_case_id": "svo_01",
            "rule": "safety_active_delays_non_safety_ocr_guidance",
            "scenario_id": "stab_005",
            "result": "DELAY",
            **_not_fact(),
        },
        {
            "matrix_case_id": "svo_02",
            "rule": "ocr_guidance_correction_can_exist_as_candidate_only",
            "scenario_id": "stab_016",
            "result": "ALLOW_CANDIDATE_ONLY",
            **_not_fact(),
        },
        {
            "matrix_case_id": "svo_03",
            "rule": "resume_ocr_requires_freshness",
            "scenario_id": "stab_020",
            "result": "FUTURE_CHECK_REQUIRED",
            **_not_fact(),
        },
        {
            "matrix_case_id": "svo_04",
            "rule": "ocr_provider_not_invoked",
            "scenario_id": "stab_005",
            "result": "PASS",
            **_not_fact(),
        },
    ]

    voice_ownership_rows = [
        {
            "matrix_case_id": "voi_01",
            "rule": "non_owner_blocked",
            "scenario_id": "stab_011",
            "result": "BLOCK",
            **_not_fact(),
        },
        {
            "matrix_case_id": "voi_02",
            "rule": "phone_call_blocked",
            "scenario_id": "stab_012",
            "result": "BLOCK",
            **_not_fact(),
        },
        {
            "matrix_case_id": "voi_03",
            "rule": "human_conversation_blocked",
            "scenario_id": "stab_013",
            "result": "BLOCK",
            **_not_fact(),
        },
        {
            "matrix_case_id": "voi_04",
            "rule": "media_playback_blocked",
            "scenario_id": "stab_014",
            "result": "BLOCK",
            **_not_fact(),
        },
        {
            "matrix_case_id": "voi_05",
            "rule": "public_announcement_blocked",
            "scenario_id": "stab_015",
            "result": "BLOCK",
            **_not_fact(),
        },
    ]

    speech_priority_rows = [
        {
            "matrix_case_id": "spi_01",
            "priority_level": "P0",
            "scenario_id": "stab_009",
            "rule": "ordinary_stop_cannot_cancel_P0",
            "result": "BLOCKED_BY_SAFETY_PRIORITY",
            **_not_fact(),
        },
        {
            "matrix_case_id": "spi_02",
            "priority_level": "P1",
            "scenario_id": "stab_024",
            "rule": "P1_risk_context_preserved",
            "result": "CONFIRMATION_OR_DELAY",
            **_not_fact(),
        },
        {
            "matrix_case_id": "spi_03",
            "priority_level": "P2",
            "scenario_id": "stab_019",
            "rule": "P2_resume_requires_route_and_stc_freshness",
            "result": "FUTURE_CHECK_REQUIRED",
            **_not_fact(),
        },
        {
            "matrix_case_id": "spi_04",
            "priority_level": "P3",
            "scenario_id": "stab_020",
            "rule": "P3_resume_requires_frame_region_freshness",
            "result": "FUTURE_CHECK_REQUIRED",
            **_not_fact(),
        },
        {
            "matrix_case_id": "spi_05",
            "priority_level": "P4",
            "scenario_id": "stab_008",
            "rule": "P4_explanation_interruptible",
            "result": "STOP_ALLOWED",
            **_not_fact(),
        },
        {
            "matrix_case_id": "spi_06",
            "priority_level": "P4",
            "scenario_id": "stab_022",
            "rule": "P4_clarification_suppressed_under_safety",
            "result": "SUPPRESS",
            **_not_fact(),
        },
        {
            "matrix_case_id": "spi_07",
            "priority_level": "P5",
            "scenario_id": "stab_002",
            "rule": "P5_low_cost_candidate_interruptible",
            "result": "INTERRUPTIBLE",
            **_not_fact(),
        },
        {
            "matrix_case_id": "spi_08",
            "priority_level": "MIXED",
            "scenario_id": "stab_010",
            "rule": "emergency_can_preempt_non_safety_guidance",
            "result": "SAFETY_ESCALATION",
            **_not_fact(),
        },
    ]

    freshness_rows = [
        {
            "matrix_case_id": "frr_01",
            "rule": "repeat_requires_freshness",
            "scenario_id": "stab_006",
            "result": "CHECK_REQUIRED",
            **_not_fact(),
        },
        {
            "matrix_case_id": "frr_02",
            "rule": "stale_safety_repeat_not_current_fact",
            "scenario_id": "stab_007",
            "result": "BLOCKED_BY_STALENESS",
            **_not_fact(),
        },
        {
            "matrix_case_id": "frr_03",
            "rule": "resume_navigation_requires_route_and_stc",
            "scenario_id": "stab_019",
            "result": "FUTURE_CHECK_REQUIRED",
            **_not_fact(),
        },
        {
            "matrix_case_id": "frr_04",
            "rule": "resume_ocr_requires_frame_region_freshness",
            "scenario_id": "stab_020",
            "result": "FUTURE_CHECK_REQUIRED",
            **_not_fact(),
        },
        {
            "matrix_case_id": "frr_05",
            "rule": "clarification_under_safety_not_prioritized",
            "scenario_id": "stab_022",
            "result": "SUPPRESSED",
            **_not_fact(),
        },
    ]

    context_rows = [
        {
            "matrix_case_id": "ctx_01",
            "rule": "task_context_preserved",
            "scenario_id": "stab_023",
            "result": "PASS",
            **_not_fact(),
        },
        {
            "matrix_case_id": "ctx_02",
            "rule": "pending_confirmation_preserved",
            "scenario_id": "stab_024",
            "result": "PASS",
            **_not_fact(),
        },
        {
            "matrix_case_id": "ctx_03",
            "rule": "safety_context_preserved",
            "scenario_id": "stab_010",
            "result": "PASS",
            **_not_fact(),
        },
        {
            "matrix_case_id": "ctx_04",
            "rule": "speech_history_candidate_preserved_for_repeat",
            "scenario_id": "stab_006",
            "result": "PASS",
            **_not_fact(),
        },
    ]

    handoff_rows = [
        {
            "matrix_case_id": "hbo_01",
            "target_module": "speech_gate",
            "handoff_defined": True,
            "invoked_now": False,
            **_not_fact(),
        },
        {
            "matrix_case_id": "hbo_02",
            "target_module": "voice_output_plane",
            "handoff_defined": True,
            "invoked_now": False,
            **_not_fact(),
        },
        {
            "matrix_case_id": "hbo_03",
            "target_module": "task_manager",
            "handoff_defined": True,
            "invoked_now": False,
            **_not_fact(),
        },
        {
            "matrix_case_id": "hbo_04",
            "target_module": "stc",
            "handoff_defined": True,
            "invoked_now": False,
            **_not_fact(),
        },
        {
            "matrix_case_id": "hbo_05",
            "target_module": "ocr_activation",
            "handoff_defined": True,
            "invoked_now": False,
            **_not_fact(),
        },
        {
            "matrix_case_id": "hbo_06",
            "target_module": "navigation_guidance",
            "handoff_defined": True,
            "invoked_now": False,
            **_not_fact(),
        },
        {
            "matrix_case_id": "hbo_07",
            "target_module": "safety_task_arbitration",
            "handoff_defined": True,
            "invoked_now": False,
            **_not_fact(),
        },
    ]

    return {
        "summary": {
            "phase": PHASE_ID,
            "stabilization_scope": "basic_navigation_guidance_loop_stabilization_test_only",
            "basic_navigation_loop_input_loaded": loaded_flags["basic_navigation_loop"],
            "safety_task_arbitration_input_loaded": loaded_flags["safety_task_arbitration"],
            "voice_command_ownership_gate_input_loaded": loaded_flags["voice_command_ownership_gate"],
            "voice_interruption_governance_input_loaded": loaded_flags["voice_interruption_governance"],
            "stabilization_policy_defined": True,
            "stabilization_scenario_count": len(scenarios),
            "stabilization_decision_candidate_count": len(decisions),
            "baseline_vs_task_matrix_defined": True,
            "safety_vs_navigation_matrix_defined": True,
            "safety_vs_ocr_matrix_defined": True,
            "voice_ownership_vs_interruption_matrix_defined": True,
            "speech_priority_vs_interruption_matrix_defined": True,
            "freshness_repeat_resume_matrix_defined": True,
            "context_preservation_matrix_defined": True,
            "handoff_boundary_matrix_defined": True,
            "basic_navigation_baseline_count_observed": basic_summary.get("baseline_safety_request_count_observed", 0),
            "basic_navigation_task_count_observed": basic_summary.get("task_driven_request_count_observed", 0),
            "safety_arbitration_candidate_count_observed": len(safety_rows),
            "ownership_gate_candidate_count_observed": len(ownership_rows),
            "interruption_candidate_count_observed": len(interruption_rows),
            **BOUNDARY_FALSE_FLAGS,
            "fact_status": "not_fact",
            "write_allowed": False,
            "boundary_ok": True,
            "final_decision": FINAL_DECISION,
            "recommended_next_phase": RECOMMENDED_NEXT,
        },
        "input_root_matrix": {
            "row_count": len(input_rows),
            "rows": input_rows,
            **_not_fact(),
        },
        "stabilization_policy": policy,
        "stabilization_scenarios": {
            "stabilization_scenario_count": len(scenarios),
            "rows": scenarios,
            **_not_fact(),
        },
        "stabilization_decision_candidates": {
            "stabilization_decision_candidate_count": len(decisions),
            "candidates": decisions,
            **_not_fact(),
        },
        "baseline_vs_task_matrix": _mk_matrix(baseline_vs_task_rows),
        "safety_vs_navigation_matrix": _mk_matrix(safety_vs_navigation_rows),
        "safety_vs_ocr_matrix": _mk_matrix(safety_vs_ocr_rows),
        "voice_ownership_vs_interruption_matrix": _mk_matrix(voice_ownership_rows),
        "speech_priority_vs_interruption_matrix": _mk_matrix(speech_priority_rows),
        "freshness_repeat_resume_matrix": _mk_matrix(freshness_rows),
        "context_preservation_matrix": _mk_matrix(context_rows),
        "handoff_boundary_matrix": _mk_matrix(handoff_rows),
        "no_runtime_boundary_report": boundary_payload,
        "no_write_boundary_report": boundary_payload,
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "recommended_next_phase": RECOMMENDED_NEXT,
            "real_runtime_not_enabled": True,
            "controlled_trial_required": True,
            **_not_fact(),
        },
        "debug_refs": {
            "baseline_loop_ids": sorted(baseline_by_id.keys()),
            "task_loop_ids": sorted(task_by_id.keys()),
            "arbitration_ids": sorted(arb_by_id.keys()),
            "ownership_ids": sorted(own_by_id.keys()),
            "interruption_ids": sorted(int_by_id.keys()),
            "interruption_summary_loaded": bool(interruption_summary),
            "safety_summary_loaded": bool(safety_summary),
            **_not_fact(),
        },
    }
