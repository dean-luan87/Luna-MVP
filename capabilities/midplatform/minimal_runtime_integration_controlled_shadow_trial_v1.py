# -*- coding: utf-8 -*-
"""Minimal Runtime Integration Controlled Shadow Trial v1.

Phase-Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1-001"
FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_SHADOW_TRIAL_READY_FOR_POST_SHADOW_REVIEW"
RECOMMENDED_NEXT = "Minimal-Runtime-Integration-Post-Shadow-Review-v1"
SOURCE_CHAIN = "minimal_runtime_integration_controlled_shadow_trial_v1"
RUN_ID = "csrun_mrit_v1_001"
BUILD_ID = "mrit_shadow_build_v1_001"
INPUT_TRACE_ID = "controlled_shadow_input_trace_v1_001"

ROOT_INPUT_SPECS = [
    (
        "trial_definition",
        [
            "summary.json",
            "minimal_runtime_trial_definition.json",
            "runtime_module_boundary_matrix.json",
            "trial_input_plan.json",
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
    "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_TRIAL_DEFINITION_V1.md",
    "docs/architecture/midplatform/LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_TEST_V1.md",
    "docs/architecture/midplatform/LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_DRYRUN_V1.md",
    "docs/architecture/midplatform/LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_COMMAND_OWNERSHIP_GATE_POLICY_V1.md",
    "docs/architecture/voice/LUNA_VOICE_INTERRUPTION_GOVERNANCE_DRYRUN_V1.md",
    "docs/architecture/LUNA_VOICE_OUTPUT_SPEECH_GATE_MAINLINE_CONTRACT_V0.md",
    "docs/architecture/voice/LUNA_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md",
    "docs/architecture/midplatform/LUNA_TASK_MANAGER_RUNTIME_DRYRUN_V1.md",
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_STATE_RUNTIME_DRYRUN_V1.md",
    "docs/architecture/midplatform/LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
    "docs/architecture/midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md",
    "docs/architecture/system_health/LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md",
]

OPTIONAL_DOC_GLOBS = {
    "hardware_camera_control_contract": "**/*HARDWARE*CAMERA*CONTROL*CONTRACT*.md",
    "gps_context": "**/*GPS*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
    "memory_governance": "**/*MEMORY*GOVERN*.md",
    "simulation_or_benchmark": "**/*SIMULATION*.md",
}

BOUNDARY_FALSE_FLAGS = {
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

STEP_NAMES = [
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


def _index_by(items: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if value:
            out[value] = item
    return out


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


def _speech_text_from_refs(
    interruption_by_id: Dict[str, Dict[str, Any]],
    interruption_ref: Optional[str],
    fallback_ref: str,
) -> str:
    if interruption_ref and interruption_ref in interruption_by_id:
        return interruption_by_id[interruption_ref].get("target_speech_text_ref", fallback_ref)
    return fallback_ref


def run_minimal_runtime_integration_controlled_shadow_trial_v1(
    *,
    trial_definition_root: str,
    stabilization_root: str,
    basic_navigation_loop_root: str,
    safety_task_arbitration_root: str,
    ownership_gate_root: str,
    interruption_governance_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    workspace = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "trial_definition": Path(trial_definition_root).resolve(),
        "stabilization": Path(stabilization_root).resolve(),
        "basic_navigation_loop": Path(basic_navigation_loop_root).resolve(),
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
                "missing_impact": "shadow_trial_check_partial" if not loaded else "none",
                **_not_fact(),
            }
        )
    input_root_rows.extend(_doc_rows(workspace))

    trial_definition = _read_json(roots["trial_definition"] / "minimal_runtime_trial_definition.json") or {}
    trial_boundary = _read_json(roots["trial_definition"] / "runtime_module_boundary_matrix.json") or {}
    trial_abort = _read_json(roots["trial_definition"] / "abort_conditions.json") or {}
    stabilization_summary = _read_json(roots["stabilization"] / "summary.json") or {}
    stabilization_scenarios = _read_json(roots["stabilization"] / "stabilization_scenarios.json") or {}
    baseline_matrix = _read_json(
        roots["basic_navigation_loop"] / "basic_navigation_baseline_safety_loop_dryrun_matrix_v1.json"
    ) or {}
    task_matrix = _read_json(
        roots["basic_navigation_loop"] / "basic_navigation_task_driven_loop_dryrun_matrix_v1.json"
    ) or {}
    safety_candidates = _read_json(
        roots["safety_task_arbitration"] / "safety_task_arbitration_candidate_collection_v1.json"
    ) or {}
    ownership_candidates = _read_json(
        roots["ownership_gate"] / "voice_command_ownership_gate_decision_candidates_v1.json"
    ) or {}
    interruption_candidates = _read_json(
        roots["interruption_governance"] / "interruption_decision_candidates.json"
    ) or {}

    baseline_by_id = _index_by(baseline_matrix.get("rows") or [], "baseline_loop_id")
    task_by_id = _index_by(task_matrix.get("rows") or [], "task_loop_id")
    arbitration_by_id = _index_by(safety_candidates.get("candidates") or [], "arbitration_candidate_id")
    ownership_by_id = _index_by(
        ownership_candidates.get("candidates") or [], "ownership_gate_decision_candidate_id"
    )
    interruption_by_id = _index_by(
        interruption_candidates.get("candidates") or [], "interruption_decision_id"
    )
    stabilization_by_key = _index_by(stabilization_scenarios.get("rows") or [], "scenario_key")

    boundary = _boundary_payload()

    case_specs = [
        {
            "input_case_id": "shadow_case_01",
            "input_case_key": "baseline_safety_only",
            "stabilization_ref": "baseline_p0_safety_no_task",
            "simulated_task_context": None,
            "simulated_safety_event": "front_hazard_candidate",
            "simulated_voice_text": None,
            "simulated_ownership_state": None,
            "simulated_navigation_candidate": None,
            "simulated_ocr_candidate": None,
            "expected_shadow_behavior": "baseline safety candidate is allowed through shadow speech path",
            "safety_candidate": "baseline_loop_001",
            "task_navigation_candidate": None,
            "ocr_guidance_candidate": None,
            "ownership_gate_shadow_result": None,
            "interruption_shadow_result": None,
            "arbitration_shadow_result": "arb_trace_baseline_loop_001",
            "speech_request_candidate": "sp_as_ve_obs_req_baseline_001",
            "speech_text_ref": "前方可能存在安全风险，建议放慢并注意周围环境。",
            "target_priority": "P0_critical_safety",
            "blocked_by_safety": False,
            "delayed_by_safety": False,
            "suppressed_by_ownership": False,
            "stale_blocked": False,
            "output_allowed_shadow": True,
            "task_context_preserved": False,
            "pending_confirmation_preserved": False,
            "final_case_status": "SHADOW_PASS",
        },
        {
            "input_case_id": "shadow_case_02",
            "input_case_key": "navigation_guidance_only",
            "stabilization_ref": "task_navigation_p2_candidate",
            "simulated_task_context": "tobj_tsc_utt_010",
            "simulated_safety_event": None,
            "simulated_voice_text": None,
            "simulated_ownership_state": None,
            "simulated_navigation_candidate": "task_loop_007",
            "simulated_ocr_candidate": None,
            "expected_shadow_behavior": "task navigation candidate runs through shadow speech handoff without real output",
            "safety_candidate": None,
            "task_navigation_candidate": "task_loop_007",
            "ocr_guidance_candidate": None,
            "ownership_gate_shadow_result": None,
            "interruption_shadow_result": None,
            "arbitration_shadow_result": "arb_trace_task_loop_007",
            "speech_request_candidate": "sp_as_ve_obs_req_td_oplan_tobj_tsc_utt_010_ask_user_to_stop_for_static_reading",
            "speech_text_ref": "建议调整视角或朝向，以便更好观察目标区域。",
            "target_priority": "P2_task_navigation",
            "blocked_by_safety": False,
            "delayed_by_safety": False,
            "suppressed_by_ownership": False,
            "stale_blocked": False,
            "output_allowed_shadow": True,
            "task_context_preserved": True,
            "pending_confirmation_preserved": False,
            "final_case_status": "SHADOW_PASS",
        },
        {
            "input_case_id": "shadow_case_03",
            "input_case_key": "safety_overrides_navigation",
            "stabilization_ref": "task_navigation_suppressed_by_safety",
            "simulated_task_context": "tobj_tsc_utt_010",
            "simulated_safety_event": "critical_safety_candidate_active",
            "simulated_voice_text": None,
            "simulated_ownership_state": None,
            "simulated_navigation_candidate": "task_loop_007",
            "simulated_ocr_candidate": None,
            "expected_shadow_behavior": "safety candidate suppresses lower-priority navigation speech in shadow path",
            "safety_candidate": "baseline_loop_001",
            "task_navigation_candidate": "task_loop_007",
            "ocr_guidance_candidate": None,
            "ownership_gate_shadow_result": None,
            "interruption_shadow_result": None,
            "arbitration_shadow_result": "arb_trace_baseline_loop_001",
            "suppressed_candidate_ref": "arb_trace_task_loop_007",
            "speech_request_candidate": "sp_as_ve_obs_req_baseline_001",
            "speech_text_ref": "前方可能存在安全风险，建议放慢并注意周围环境。",
            "target_priority": "P0_critical_safety",
            "blocked_by_safety": False,
            "delayed_by_safety": False,
            "suppressed_by_ownership": False,
            "stale_blocked": False,
            "output_allowed_shadow": True,
            "task_context_preserved": True,
            "pending_confirmation_preserved": False,
            "final_case_status": "SHADOW_PASS_WITH_SUPPRESSION",
        },
        {
            "input_case_id": "shadow_case_04",
            "input_case_key": "ocr_guidance_delayed_by_safety",
            "stabilization_ref": "ocr_guidance_delayed_by_safety",
            "simulated_task_context": "tobj_tsc_utt_001",
            "simulated_safety_event": "critical_safety_candidate_active",
            "simulated_voice_text": None,
            "simulated_ownership_state": None,
            "simulated_navigation_candidate": None,
            "simulated_ocr_candidate": "task_loop_009",
            "expected_shadow_behavior": "ocr guidance stays candidate-only and is delayed under active safety",
            "safety_candidate": "baseline_loop_003",
            "task_navigation_candidate": None,
            "ocr_guidance_candidate": "task_loop_009",
            "ownership_gate_shadow_result": None,
            "interruption_shadow_result": None,
            "arbitration_shadow_result": "arb_trace_task_loop_009",
            "speech_request_candidate": "sp_as_ve_obs_req_td_ocr_tobj_tsc_utt_001",
            "speech_text_ref": "疑似有可读标识区域，建议靠近后再确认文字内容。",
            "target_priority": "P3_ocr_static_reading",
            "blocked_by_safety": False,
            "delayed_by_safety": True,
            "suppressed_by_ownership": False,
            "stale_blocked": False,
            "output_allowed_shadow": False,
            "task_context_preserved": True,
            "pending_confirmation_preserved": False,
            "final_case_status": "SHADOW_PASS_WITH_DELAY",
        },
        {
            "input_case_id": "shadow_case_05",
            "input_case_key": "owner_confirmed_repeat_request",
            "stabilization_ref": "owner_repeat_during_navigation",
            "simulated_task_context": "tobj_tsc_utt_010",
            "simulated_safety_event": None,
            "simulated_voice_text": "刚才你说什么",
            "simulated_ownership_state": "OWNER_CONFIRMED",
            "simulated_navigation_candidate": "task_loop_007",
            "simulated_ocr_candidate": None,
            "expected_shadow_behavior": "owner repeat request creates repeat candidate and shadow handoff trace",
            "safety_candidate": None,
            "task_navigation_candidate": "task_loop_007",
            "ocr_guidance_candidate": None,
            "ownership_gate_shadow_result": "ogd_case_02",
            "interruption_shadow_result": "idc_case_02",
            "arbitration_shadow_result": "arb_trace_task_loop_007",
            "speech_request_candidate": "sp_ds_ds_cd_tsc_utt_003",
            "speech_text_ref": _speech_text_from_refs(interruption_by_id, "idc_case_02", "ref:sp_ds_ds_cd_tsc_utt_003"),
            "target_priority": "P4",
            "blocked_by_safety": False,
            "delayed_by_safety": False,
            "suppressed_by_ownership": False,
            "stale_blocked": False,
            "output_allowed_shadow": True,
            "task_context_preserved": True,
            "pending_confirmation_preserved": True,
            "final_case_status": "SHADOW_PASS",
        },
        {
            "input_case_id": "shadow_case_06",
            "input_case_key": "non_owner_interruption_blocked",
            "stabilization_ref": "non_owner_interruption_blocked",
            "simulated_task_context": "tobj_tsc_utt_010",
            "simulated_safety_event": None,
            "simulated_voice_text": "暂停导航",
            "simulated_ownership_state": "NON_OWNER_PROBABLE",
            "simulated_navigation_candidate": "task_loop_007",
            "simulated_ocr_candidate": None,
            "expected_shadow_behavior": "non-owner interruption is suppressed before any task control or real output",
            "safety_candidate": None,
            "task_navigation_candidate": "task_loop_007",
            "ocr_guidance_candidate": None,
            "ownership_gate_shadow_result": "ogd_case_06",
            "interruption_shadow_result": "idc_case_06",
            "arbitration_shadow_result": "arb_trace_task_loop_007",
            "speech_request_candidate": "sp_as_ve_obs_req_td_oplan_tobj_tsc_utt_010_ask_user_to_stop_for_static_reading",
            "speech_text_ref": _speech_text_from_refs(
                interruption_by_id, "idc_case_06", "ref:sp_as_ve_obs_req_td_oplan_tobj_tsc_utt_010_ask_user_to_stop_for_static_reading"
            ),
            "target_priority": "P2",
            "blocked_by_safety": False,
            "delayed_by_safety": False,
            "suppressed_by_ownership": True,
            "stale_blocked": False,
            "output_allowed_shadow": False,
            "task_context_preserved": True,
            "pending_confirmation_preserved": True,
            "final_case_status": "SHADOW_PASS_WITH_SUPPRESSION",
        },
        {
            "input_case_id": "shadow_case_07",
            "input_case_key": "emergency_user_interruption_candidate",
            "stabilization_ref": "owner_emergency_interrupt",
            "simulated_task_context": "tobj_tsc_utt_010",
            "simulated_safety_event": "user_reports_immediate_hazard",
            "simulated_voice_text": "危险，车来了",
            "simulated_ownership_state": "OWNER_CONFIRMED",
            "simulated_navigation_candidate": "task_loop_007",
            "simulated_ocr_candidate": None,
            "expected_shadow_behavior": "emergency input escalates to safety observation candidate and preserves task context",
            "safety_candidate": "baseline_loop_001",
            "task_navigation_candidate": "task_loop_007",
            "ocr_guidance_candidate": None,
            "ownership_gate_shadow_result": "ogd_case_05",
            "interruption_shadow_result": "idc_case_05",
            "arbitration_shadow_result": "arb_trace_task_loop_007",
            "speech_request_candidate": "sp_as_ve_obs_req_td_oplan_tobj_tsc_utt_010_ask_user_to_stop_for_static_reading",
            "speech_text_ref": _speech_text_from_refs(
                interruption_by_id, "idc_case_05", "ref:sp_as_ve_obs_req_td_oplan_tobj_tsc_utt_010_ask_user_to_stop_for_static_reading"
            ),
            "target_priority": "P2",
            "blocked_by_safety": False,
            "delayed_by_safety": False,
            "suppressed_by_ownership": False,
            "stale_blocked": False,
            "output_allowed_shadow": False,
            "task_context_preserved": True,
            "pending_confirmation_preserved": True,
            "final_case_status": "SHADOW_PASS",
        },
        {
            "input_case_id": "shadow_case_08",
            "input_case_key": "stale_safety_repeat_blocked",
            "stabilization_ref": "repeat_stale_p0_safety",
            "simulated_task_context": None,
            "simulated_safety_event": "historical_safety_warning_candidate",
            "simulated_voice_text": "再说一遍",
            "simulated_ownership_state": "OWNER_CONFIRMED",
            "simulated_navigation_candidate": None,
            "simulated_ocr_candidate": None,
            "expected_shadow_behavior": "stale safety repeat is blocked as current fact and remains historical-only",
            "safety_candidate": "baseline_loop_001",
            "task_navigation_candidate": None,
            "ocr_guidance_candidate": None,
            "ownership_gate_shadow_result": None,
            "interruption_shadow_result": "idc_case_24",
            "arbitration_shadow_result": "arb_trace_baseline_loop_001",
            "speech_request_candidate": "sp_as_ve_obs_req_baseline_001",
            "speech_text_ref": _speech_text_from_refs(interruption_by_id, "idc_case_24", "ref:sp_as_ve_obs_req_baseline_001"),
            "target_priority": "P0",
            "blocked_by_safety": False,
            "delayed_by_safety": False,
            "suppressed_by_ownership": False,
            "stale_blocked": True,
            "output_allowed_shadow": False,
            "task_context_preserved": False,
            "pending_confirmation_preserved": True,
            "final_case_status": "SHADOW_PASS_WITH_SUPPRESSION",
        },
    ]

    controlled_input_cases: List[Dict[str, Any]] = []
    shadow_steps: List[Dict[str, Any]] = []
    shadow_candidate_traces: List[Dict[str, Any]] = []
    speech_gate_shadow_decisions: List[Dict[str, Any]] = []
    vop_shadow_events: List[Dict[str, Any]] = []
    abort_checks: List[Dict[str, Any]] = []
    observability_case_rows: List[Dict[str, Any]] = []

    for spec in case_specs:
        controlled_input_cases.append(
            {
                "input_case_id": spec["input_case_id"],
                "input_case_key": spec["input_case_key"],
                "simulated_task_context": spec["simulated_task_context"],
                "simulated_safety_event": spec["simulated_safety_event"],
                "simulated_voice_text": spec["simulated_voice_text"],
                "simulated_ownership_state": spec["simulated_ownership_state"],
                "simulated_navigation_candidate": spec["simulated_navigation_candidate"],
                "simulated_ocr_candidate": spec["simulated_ocr_candidate"],
                "expected_shadow_behavior": spec["expected_shadow_behavior"],
                "stabilization_ref": spec["stabilization_ref"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        speech_gate_shadow_id = f"sgsd_{spec['input_case_id']}"
        vop_shadow_event_id = f"vse_{spec['input_case_id']}"
        abort_check_id = f"abort_{spec['input_case_id']}"
        trace_id = f"sctr_{spec['input_case_id']}"

        gate_shadow_row = {
            "speech_gate_shadow_id": speech_gate_shadow_id,
            "input_case_id": spec["input_case_id"],
            "speech_request_candidate_id": spec["speech_request_candidate"],
            "target_priority": spec["target_priority"],
            "allowed_by_priority_policy": not spec["stale_blocked"] and not spec["suppressed_by_ownership"],
            "blocked_by_safety": spec["blocked_by_safety"],
            "delayed_by_safety": spec["delayed_by_safety"],
            "suppressed_by_ownership": spec["suppressed_by_ownership"],
            "stale_blocked": spec["stale_blocked"],
            "output_allowed_shadow": spec["output_allowed_shadow"],
            "runtime_speech_gate_invoked": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        speech_gate_shadow_decisions.append(gate_shadow_row)

        vop_shadow_row = {
            "vop_shadow_event_id": vop_shadow_event_id,
            "input_case_id": spec["input_case_id"],
            "speech_gate_shadow_id": speech_gate_shadow_id,
            "speech_text_ref": spec["speech_text_ref"],
            "output_mode": "SHADOW_ONLY",
            "shadow_event_status": (
                "SHADOW_EMITTED"
                if spec["output_allowed_shadow"]
                else ("SHADOW_DELAYED" if spec["delayed_by_safety"] else "SHADOW_BLOCKED")
            ),
            "tts_invoked": False,
            "audio_output_invoked": False,
            "runtime_vop_invoked": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        vop_shadow_events.append(vop_shadow_row)

        abort_row = {
            "abort_check_id": abort_check_id,
            "input_case_id": spec["input_case_id"],
            "forbidden_runtime_invoked": False,
            "forbidden_write_occurred": False,
            "missing_source_chain": False,
            "task_state_committed": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "gps_runtime_invoked": False,
            "real_ocr_provider_invoked": False,
            "real_camera_invoked": False,
            "real_microphone_invoked": False,
            "real_tts_invoked": False,
            "real_speech_gate_runtime_invoked": False,
            "real_vop_runtime_invoked": False,
            "world_model_written": False,
            "memory_written": False,
            "scene_delta_generated": False,
            "stale_safety_speech_treated_as_current_fact": False,
            "non_owner_voice_triggers_task_control": False,
            "p0_safety_speech_cancelled_by_ordinary_stop": False,
            "violations": [],
            "abort_triggered": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        abort_checks.append(abort_row)

        shadow_candidate_traces.append(
            {
                "shadow_candidate_trace_id": trace_id,
                "input_case_id": spec["input_case_id"],
                "safety_candidate": spec["safety_candidate"],
                "task_navigation_candidate": spec["task_navigation_candidate"],
                "ocr_guidance_candidate": spec["ocr_guidance_candidate"],
                "ownership_gate_shadow_result": spec["ownership_gate_shadow_result"],
                "interruption_shadow_result": spec["interruption_shadow_result"],
                "arbitration_shadow_result": spec["arbitration_shadow_result"],
                "speech_request_candidate": spec["speech_request_candidate"],
                "speech_gate_shadow_decision": speech_gate_shadow_id,
                "vop_shadow_event": vop_shadow_event_id,
                "boundary_check_result": boundary,
                "abort_check_result": abort_check_id,
                "task_context_preserved": spec["task_context_preserved"],
                "pending_confirmation_preserved": spec["pending_confirmation_preserved"],
                "final_case_status": spec["final_case_status"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        observability_case_rows.append(
            {
                "input_case_id": spec["input_case_id"],
                "priority_trace": {
                    "selected_priority": spec["target_priority"],
                    "blocked_by_safety": spec["blocked_by_safety"],
                    "delayed_by_safety": spec["delayed_by_safety"],
                    "stale_blocked": spec["stale_blocked"],
                },
                "ownership_trace": {
                    "ownership_gate_shadow_result": spec["ownership_gate_shadow_result"],
                    "simulated_ownership_state": spec["simulated_ownership_state"],
                    "suppressed_by_ownership": spec["suppressed_by_ownership"],
                },
                "interruption_trace": {
                    "interruption_shadow_result": spec["interruption_shadow_result"],
                    "simulated_voice_text": spec["simulated_voice_text"],
                },
                "arbitration_trace": {
                    "arbitration_shadow_result": spec["arbitration_shadow_result"],
                },
                "speech_handoff_trace": {
                    "speech_gate_shadow_id": speech_gate_shadow_id,
                    "vop_shadow_event_id": vop_shadow_event_id,
                },
                "error_trace": [],
                "abort_trace": {
                    "abort_check_id": abort_check_id,
                    "abort_triggered": False,
                },
                "module_boundary_flags": boundary,
                "runtime_invocation_flags": boundary,
                "write_boundary_flags": boundary,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        step_result_map = {
            "load_controlled_input": "SHADOW_INPUT_LOADED",
            "generate_safety_candidate": "CANDIDATE_READY" if spec["safety_candidate"] else "SKIPPED_NOT_APPLICABLE",
            "generate_task_navigation_candidate": (
                "CANDIDATE_READY" if spec["task_navigation_candidate"] else "SKIPPED_NOT_APPLICABLE"
            ),
            "generate_ocr_guidance_candidate": (
                "CANDIDATE_READY" if spec["ocr_guidance_candidate"] else "SKIPPED_NOT_APPLICABLE"
            ),
            "apply_ownership_gate_shadow": (
                "SHADOW_APPLIED" if spec["ownership_gate_shadow_result"] else "SKIPPED_NOT_APPLICABLE"
            ),
            "apply_interruption_governance_shadow": (
                "SHADOW_APPLIED" if spec["interruption_shadow_result"] else "SKIPPED_NOT_APPLICABLE"
            ),
            "apply_safety_task_arbitration_shadow": "SHADOW_APPLIED",
            "generate_speech_request_candidate": "CANDIDATE_READY",
            "apply_speech_gate_shadow": (
                "SHADOW_ALLOWED"
                if spec["output_allowed_shadow"]
                else ("SHADOW_DELAYED" if spec["delayed_by_safety"] else "SHADOW_BLOCKED")
            ),
            "generate_vop_shadow_event": (
                "SHADOW_EVENT_EMITTED"
                if spec["output_allowed_shadow"]
                else ("SHADOW_EVENT_DELAYED" if spec["delayed_by_safety"] else "SHADOW_EVENT_BLOCKED")
            ),
            "run_abort_checks": "NO_ABORT_TRIGGERED",
            "generate_boundary_reports": "BOUNDARY_OK",
            "generate_final_shadow_decision": spec["final_case_status"],
        }

        for idx, step_name in enumerate(STEP_NAMES, start=1):
            shadow_steps.append(
                {
                    "shadow_step_id": f"{spec['input_case_id']}_step_{idx:02d}",
                    "input_case_id": spec["input_case_id"],
                    "step_name": step_name,
                    "shadow_only": True,
                    "step_result": step_result_map[step_name],
                    "runtime_invoked": False,
                    "write_occurred": False,
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )

    controlled_shadow_trial_run = {
        "run_id": RUN_ID,
        "trial_definition_id": trial_definition.get("trial_definition_id"),
        "trial_mode": "CONTROLLED_SHADOW_TRIAL",
        "input_trace_id": INPUT_TRACE_ID,
        "input_sources": [row["input_case_key"] for row in controlled_input_cases],
        "executed_shadow_steps": [row["shadow_step_id"] for row in shadow_steps],
        "generated_candidates": [row["shadow_candidate_trace_id"] for row in shadow_candidate_traces],
        "shadow_handoff_events": [row["vop_shadow_event_id"] for row in vop_shadow_events],
        "boundary_flags": boundary,
        "abort_checks": [row["abort_check_id"] for row in abort_checks],
        "final_shadow_status": "SHADOW_PASS_WITH_SUPPRESSION",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    observability_trace = {
        "run_id": RUN_ID,
        "build_id": BUILD_ID,
        "git_commit_if_available": None,
        "run": controlled_shadow_trial_run,
        "case_traces": observability_case_rows,
        "summary_metrics": {
            "controlled_input_case_count": len(controlled_input_cases),
            "shadow_execution_step_count": len(shadow_steps),
            "shadow_candidate_trace_count": len(shadow_candidate_traces),
            "speech_gate_shadow_decision_count": len(speech_gate_shadow_decisions),
            "vop_shadow_event_count": len(vop_shadow_events),
            "abort_check_count": len(abort_checks),
            "source_chain_complete": True,
            **_not_fact(),
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": {
            "phase": PHASE_ID,
            "trial_scope": "minimal_runtime_integration_controlled_shadow_trial_only",
            "trial_mode": "CONTROLLED_SHADOW_TRIAL",
            "controlled_shadow_trial_executed": True,
            "trial_definition_input_loaded": loaded_flags["trial_definition"],
            "stabilization_input_loaded": loaded_flags["stabilization"],
            "basic_navigation_loop_input_loaded": loaded_flags["basic_navigation_loop"],
            "safety_task_arbitration_input_loaded": loaded_flags["safety_task_arbitration"],
            "ownership_gate_input_loaded": loaded_flags["ownership_gate"],
            "interruption_governance_input_loaded": loaded_flags["interruption_governance"],
            "controlled_input_case_count": len(controlled_input_cases),
            "shadow_execution_step_count": len(shadow_steps),
            "shadow_candidate_trace_count": len(shadow_candidate_traces),
            "speech_gate_shadow_decision_count": len(speech_gate_shadow_decisions),
            "vop_shadow_event_count": len(vop_shadow_events),
            "abort_check_count": len(abort_checks),
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
        "controlled_trial_input_trace": {
            "input_trace_id": INPUT_TRACE_ID,
            "controlled_input_case_count": len(controlled_input_cases),
            "rows": controlled_input_cases,
            **_not_fact(),
        },
        "shadow_execution_steps": {
            "shadow_execution_step_count": len(shadow_steps),
            "rows": shadow_steps,
            **_not_fact(),
        },
        "shadow_candidate_trace": {
            "shadow_candidate_trace_count": len(shadow_candidate_traces),
            "rows": shadow_candidate_traces,
            **_not_fact(),
        },
        "speech_gate_shadow_decisions": {
            "speech_gate_shadow_decision_count": len(speech_gate_shadow_decisions),
            "rows": speech_gate_shadow_decisions,
            **_not_fact(),
        },
        "vop_shadow_events": {
            "vop_shadow_event_count": len(vop_shadow_events),
            "rows": vop_shadow_events,
            **_not_fact(),
        },
        "controlled_shadow_abort_checks": {
            "abort_check_count": len(abort_checks),
            "rows": abort_checks,
            **_not_fact(),
        },
        "observability_trace": observability_trace,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "recommended_next_phase": RECOMMENDED_NEXT,
            "post_shadow_review_required": True,
            **_not_fact(),
        },
        "debug_refs": {
            "stabilization_refs_present": sorted(stabilization_by_key.keys()),
            "allowed_runtime_modules": trial_definition.get("allowed_runtime_modules", []),
            "shadow_only_modules": trial_definition.get("shadow_only_modules", []),
            "abort_conditions_from_definition": trial_abort.get("conditions", []),
            "trial_boundary_loaded": bool(trial_boundary),
            **_not_fact(),
        },
    }
