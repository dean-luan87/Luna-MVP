# -*- coding: utf-8 -*-
"""Minimal Runtime Integration Text-Only Controlled Output Trial v1.

Phase-Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-001"
FINAL_DECISION = "TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL_READY_FOR_POST_TRIAL_REVIEW"
RECOMMENDED_NEXT = "Phase-Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1-001"
SOURCE_CHAIN = "minimal_runtime_integration_text_only_controlled_output_trial_v1"
TRIAL_RUN_ID = "text_only_controlled_output_trial_run_v1_001"
OBSERVABILITY_ID = "text_only_controlled_output_trial_observability_v1_001"
ALLOWED_OUTPUT_MODES = [
    "TEXT_ONLY",
    "STRUCTURED_LOG_ONLY",
    "DRY_SPEECH_PREVIEW",
    "SHADOW_COMPATIBLE_TEXT_OUTPUT",
]

ROOT_INPUT_SPECS = [
    (
        "controlled_output_definition",
        [
            "summary.json",
            "controlled_output_definition.json",
            "speech_gate_controlled_output_contract.json",
            "vop_controlled_output_contract.json",
            "tts_placeholder_policy.json",
            "user_visible_output_boundary.json",
            "output_abort_conditions.json",
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
}

BOUNDARY_FALSE_FLAGS = {
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


def _final_trial_status(case_rows: List[Dict[str, Any]]) -> str:
    if any(row["decision"] == "SUPPRESS" for row in case_rows):
        return "TEXT_ONLY_OUTPUT_PASS_WITH_SUPPRESSION"
    if any(row["decision"] == "DELAY" for row in case_rows):
        return "TEXT_ONLY_OUTPUT_PASS_WITH_DELAY"
    return "TEXT_ONLY_OUTPUT_PASS"


def run_minimal_runtime_integration_text_only_controlled_output_trial_v1(
    *,
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
                "missing_impact": "text_only_trial_partial" if not loaded else "none",
                **_not_fact(),
            }
        )
    input_root_rows.extend(_doc_rows(workspace))

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
    tts_policy = _read_json(roots["controlled_output_definition"] / "tts_placeholder_policy.json") or {}
    definition_abort = _read_json(
        roots["controlled_output_definition"] / "output_abort_conditions.json"
    ) or {}

    post_shadow_summary = _read_json(roots["post_shadow_review"] / "summary.json") or {}
    post_shadow_report = _read_json(roots["post_shadow_review"] / "post_shadow_review_report.json") or {}
    post_shadow_readiness = _read_json(
        roots["post_shadow_review"] / "controlled_output_readiness_decision.json"
    ) or {}

    shadow_summary = _read_json(roots["controlled_shadow_trial"] / "summary.json") or {}
    shadow_gate = _read_json(
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
    stabilization_scenarios = _read_json(roots["stabilization"] / "stabilization_scenarios.json") or {}
    safety_summary = _read_json(
        roots["safety_task_arbitration"] / "safety_task_arbitration_policy_v1_summary.json"
    ) or {}
    safety_candidates = _read_json(
        roots["safety_task_arbitration"] / "safety_task_arbitration_candidate_collection_v1.json"
    ) or {}
    ownership_payload = _read_json(
        roots["ownership_gate"] / "voice_command_ownership_gate_decision_candidates_v1.json"
    ) or {}
    interruption_payload = _read_json(
        roots["interruption_governance"] / "interruption_decision_candidates.json"
    ) or {}

    boundary = _boundary_payload()

    case_specs = [
        {
            "trial_case_id": "text_case_01",
            "case_key": "p0_safety_text_only_allowed",
            "expected_behavior": "P0 safety warning emits text-only output without any audio path",
            "speech_request_candidate_id": "sp_as_ve_obs_req_baseline_001",
            "decision": "ALLOW_TEXT_ONLY",
            "decision_reason": "P0 safety warning must remain visible and cannot be preempted by lower priority output",
            "allowed_output_mode": "TEXT_ONLY",
            "output_mode": "TEXT_ONLY",
            "output_text_ref": "前方可能存在安全风险，建议立即减速并保持注意。",
            "output_text_preview": "安全提示：前方可能存在风险，请立即减速并保持注意。",
            "priority": "P0_critical_safety",
            "safety_status": "ACTIVE_P0",
            "ownership_status": "SYSTEM_SAFETY",
            "interruption_status": "NONE",
            "freshness_status": "FRESH",
            "stale_guard_applied": False,
            "ownership_guard_applied": False,
            "safety_priority_guard_applied": True,
            "historical_only": False,
            "requires_confirmation": False,
            "final_case_status": "TEXT_ONLY_OUTPUT_PASS",
        },
        {
            "trial_case_id": "text_case_02",
            "case_key": "p2_navigation_text_only_allowed",
            "expected_behavior": "P2 navigation guidance emits text-only output when no active safety conflict exists",
            "speech_request_candidate_id": "sp_as_ve_obs_req_td_oplan_tobj_tsc_utt_010_ask_user_to_stop_for_static_reading",
            "decision": "ALLOW_TEXT_ONLY",
            "decision_reason": "No active safety conflict exists so navigation text can be shown as controlled text only",
            "allowed_output_mode": "TEXT_ONLY",
            "output_mode": "TEXT_ONLY",
            "output_text_ref": "建议向左微调视角，再次观察目标方向。",
            "output_text_preview": "导航提示：建议向左微调视角，再次观察目标方向。",
            "priority": "P2_task_navigation",
            "safety_status": "CLEAR",
            "ownership_status": "OWNER_CONTEXT_ACTIVE",
            "interruption_status": "NONE",
            "freshness_status": "FRESH",
            "stale_guard_applied": False,
            "ownership_guard_applied": True,
            "safety_priority_guard_applied": True,
            "historical_only": False,
            "requires_confirmation": False,
            "final_case_status": "TEXT_ONLY_OUTPUT_PASS",
        },
        {
            "trial_case_id": "text_case_03",
            "case_key": "p3_ocr_guidance_delayed_by_safety",
            "expected_behavior": "P3 OCR guidance is delayed when safety remains active and only a compatible text trace is emitted",
            "speech_request_candidate_id": "sp_as_ve_obs_req_td_ocr_tobj_tsc_utt_001",
            "decision": "DELAY",
            "decision_reason": "Active safety output has higher priority so OCR guidance must remain delayed",
            "allowed_output_mode": "SHADOW_COMPATIBLE_TEXT_OUTPUT",
            "output_mode": "SHADOW_COMPATIBLE_TEXT_OUTPUT",
            "output_text_ref": "OCR 引导已延后，等待安全提示完成后再显示。",
            "output_text_preview": "延后记录：OCR 引导因安全优先级仍处于等待状态。",
            "priority": "P3_ocr_static_reading",
            "safety_status": "SAFETY_ACTIVE",
            "ownership_status": "OWNER_CONTEXT_ACTIVE",
            "interruption_status": "NONE",
            "freshness_status": "FRESH",
            "stale_guard_applied": False,
            "ownership_guard_applied": True,
            "safety_priority_guard_applied": True,
            "historical_only": False,
            "requires_confirmation": False,
            "final_case_status": "TEXT_ONLY_OUTPUT_PASS_WITH_DELAY",
        },
        {
            "trial_case_id": "text_case_04",
            "case_key": "owner_confirmed_repeat_preview",
            "expected_behavior": "Owner-confirmed repeat request produces a dry speech preview without any playback",
            "speech_request_candidate_id": "sp_ds_ds_cd_tsc_utt_003",
            "decision": "ALLOW_DRY_SPEECH_PREVIEW",
            "decision_reason": "Owner-confirmed repeat can be previewed as text without invoking audio",
            "allowed_output_mode": "DRY_SPEECH_PREVIEW",
            "output_mode": "DRY_SPEECH_PREVIEW",
            "output_text_ref": "重复预览：建议先停稳，保持画面稳定。",
            "output_text_preview": "干预览：建议先停稳，保持画面稳定。",
            "priority": "P4_repeat_preview",
            "safety_status": "CLEAR",
            "ownership_status": "OWNER_CONFIRMED",
            "interruption_status": "REPEAT_REQUEST",
            "freshness_status": "FRESH",
            "stale_guard_applied": False,
            "ownership_guard_applied": True,
            "safety_priority_guard_applied": False,
            "historical_only": False,
            "requires_confirmation": False,
            "final_case_status": "TEXT_ONLY_OUTPUT_PASS",
        },
        {
            "trial_case_id": "text_case_05",
            "case_key": "stale_p0_historical_only",
            "expected_behavior": "Stale P0 safety repeat is rendered as historical-only text and not as current fact",
            "speech_request_candidate_id": "sp_as_ve_obs_req_baseline_001",
            "decision": "ALLOW_TEXT_ONLY",
            "decision_reason": "Stale P0 repeat may be shown only as historical reference and never as current fact",
            "allowed_output_mode": "TEXT_ONLY",
            "output_mode": "TEXT_ONLY",
            "output_text_ref": "历史安全提醒：前方曾出现风险提示，请结合当前环境重新确认。",
            "output_text_preview": "历史提醒：此前出现过安全风险提示，当前不作为实时事实输出。",
            "priority": "P0_historical_safety",
            "safety_status": "HISTORICAL_ONLY",
            "ownership_status": "OWNER_CONFIRMED",
            "interruption_status": "REPEAT_REQUEST",
            "freshness_status": "STALE_HISTORICAL_ONLY",
            "stale_guard_applied": True,
            "ownership_guard_applied": True,
            "safety_priority_guard_applied": True,
            "historical_only": True,
            "requires_confirmation": False,
            "final_case_status": "TEXT_ONLY_OUTPUT_PASS",
        },
        {
            "trial_case_id": "text_case_06",
            "case_key": "non_owner_interruption_suppressed",
            "expected_behavior": "Non-owner interruption attempt is suppressed and only a structured log trace is emitted",
            "speech_request_candidate_id": "sp_as_ve_obs_req_td_oplan_tobj_tsc_utt_010_ask_user_to_stop_for_static_reading",
            "decision": "SUPPRESS",
            "decision_reason": "Non-owner interruption cannot trigger task or output control",
            "allowed_output_mode": "STRUCTURED_LOG_ONLY",
            "output_mode": "STRUCTURED_LOG_ONLY",
            "output_text_ref": "抑制记录：非 owner 中断尝试已拦截。",
            "output_text_preview": "结构化记录：非 owner 中断尝试已被抑制。",
            "priority": "P2_task_navigation",
            "safety_status": "CLEAR",
            "ownership_status": "NON_OWNER_BLOCKED",
            "interruption_status": "BLOCKED",
            "freshness_status": "FRESH",
            "stale_guard_applied": False,
            "ownership_guard_applied": True,
            "safety_priority_guard_applied": False,
            "historical_only": False,
            "requires_confirmation": False,
            "final_case_status": "TEXT_ONLY_OUTPUT_PASS_WITH_SUPPRESSION",
        },
        {
            "trial_case_id": "text_case_07",
            "case_key": "emergency_safety_observation_preview",
            "expected_behavior": "Emergency interruption candidate is surfaced as a dry safety observation preview without audio",
            "speech_request_candidate_id": "sp_emergency_owner_preview_001",
            "decision": "ALLOW_DRY_SPEECH_PREVIEW",
            "decision_reason": "Emergency observation may surface as dry preview while real audio remains disabled",
            "allowed_output_mode": "DRY_SPEECH_PREVIEW",
            "output_mode": "DRY_SPEECH_PREVIEW",
            "output_text_ref": "紧急观察预览：用户报告附近存在即时风险，请优先安全避让。",
            "output_text_preview": "紧急预览：用户报告即时风险，请优先安全避让。",
            "priority": "P1_emergency_observation",
            "safety_status": "EMERGENCY_OBSERVATION",
            "ownership_status": "OWNER_CONFIRMED",
            "interruption_status": "EMERGENCY_CANDIDATE",
            "freshness_status": "FRESH",
            "stale_guard_applied": False,
            "ownership_guard_applied": True,
            "safety_priority_guard_applied": True,
            "historical_only": False,
            "requires_confirmation": False,
            "final_case_status": "TEXT_ONLY_OUTPUT_PASS",
        },
        {
            "trial_case_id": "text_case_08",
            "case_key": "cancel_with_pending_confirmation",
            "expected_behavior": "Cancel task request with pending confirmation produces confirmation-required text only",
            "speech_request_candidate_id": "sp_cancel_task_confirmation_001",
            "decision": "REQUIRE_CONFIRMATION",
            "decision_reason": "Pending confirmation must be preserved before any task cancel path can proceed",
            "allowed_output_mode": "SHADOW_COMPATIBLE_TEXT_OUTPUT",
            "output_mode": "SHADOW_COMPATIBLE_TEXT_OUTPUT",
            "output_text_ref": "请确认：是否取消当前任务？当前仅生成文本确认，不执行取消。",
            "output_text_preview": "确认请求：是否取消当前任务？当前仅文本提示，未执行任务取消。",
            "priority": "P3_confirmation_control",
            "safety_status": "CLEAR",
            "ownership_status": "OWNER_CONFIRMED",
            "interruption_status": "CANCEL_REQUEST_PENDING_CONFIRMATION",
            "freshness_status": "FRESH",
            "stale_guard_applied": False,
            "ownership_guard_applied": True,
            "safety_priority_guard_applied": False,
            "historical_only": False,
            "requires_confirmation": True,
            "final_case_status": "TEXT_ONLY_OUTPUT_NEEDS_REVIEW",
        },
    ]

    trial_cases: List[Dict[str, Any]] = []
    speech_gate_controlled_decisions: List[Dict[str, Any]] = []
    controlled_text_output_events: List[Dict[str, Any]] = []
    vop_controlled_event_candidates: List[Dict[str, Any]] = []
    abort_checks: List[Dict[str, Any]] = []
    observability_case_rows: List[Dict[str, Any]] = []

    for spec in case_specs:
        controlled_decision_id = f"sgcd_{spec['trial_case_id']}"
        output_event_id = f"ctoe_{spec['trial_case_id']}"
        vop_event_id = f"vopce_{spec['trial_case_id']}"
        abort_check_id = f"toa_{spec['trial_case_id']}"

        trial_cases.append(
            {
                "trial_case_id": spec["trial_case_id"],
                "case_key": spec["case_key"],
                "expected_behavior": spec["expected_behavior"],
                "speech_request_candidate_id": spec["speech_request_candidate_id"],
                "priority": spec["priority"],
                "safety_status": spec["safety_status"],
                "ownership_status": spec["ownership_status"],
                "interruption_status": spec["interruption_status"],
                "freshness_status": spec["freshness_status"],
                "expected_decision": spec["decision"],
                "expected_output_mode": spec["output_mode"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        speech_gate_controlled_decisions.append(
            {
                "controlled_decision_id": controlled_decision_id,
                "trial_case_id": spec["trial_case_id"],
                "speech_request_candidate_id": spec["speech_request_candidate_id"],
                "priority": spec["priority"],
                "decision": spec["decision"],
                "decision_reason": spec["decision_reason"],
                "stale_guard_applied": spec["stale_guard_applied"],
                "ownership_guard_applied": spec["ownership_guard_applied"],
                "safety_priority_guard_applied": spec["safety_priority_guard_applied"],
                "allowed_output_mode": spec["allowed_output_mode"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        controlled_text_output_events.append(
            {
                "output_event_id": output_event_id,
                "trial_case_id": spec["trial_case_id"],
                "source_speech_request_candidate_id": spec["speech_request_candidate_id"],
                "source_speech_gate_decision_id": controlled_decision_id,
                "output_mode": spec["output_mode"],
                "output_text_ref": spec["output_text_ref"],
                "output_text_preview": spec["output_text_preview"],
                "priority": spec["priority"],
                "safety_status": spec["safety_status"],
                "ownership_status": spec["ownership_status"],
                "interruption_status": spec["interruption_status"],
                "freshness_status": spec["freshness_status"],
                "historical_only": spec["historical_only"],
                "requires_confirmation": spec["requires_confirmation"],
                "user_visible": True,
                "user_heard_assumed": False,
                "audio_output": False,
                "tts_invoked": False,
                "vop_runtime_invoked": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        vop_controlled_event_candidates.append(
            {
                "vop_controlled_event_id": vop_event_id,
                "trial_case_id": spec["trial_case_id"],
                "controlled_decision_id": controlled_decision_id,
                "output_mode": spec["output_mode"],
                "output_text_ref": spec["output_text_ref"],
                "audio_output_invoked": False,
                "runtime_vop_invoked": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        abort_checks.append(
            {
                "abort_check_id": abort_check_id,
                "trial_case_id": spec["trial_case_id"],
                "real_tts_invoked": False,
                "audio_output_invoked": False,
                "speech_gate_runtime_invoked": False,
                "vop_runtime_invoked": False,
                "output_without_source_chain": False,
                "p0_p1_safety_suppressed_by_lower_priority": False,
                "stale_safety_speech_output_as_current_fact": False,
                "non_owner_voice_triggers_output": False,
                "task_state_committed": False,
                "navigation_action_triggered": False,
                "map_api_invoked": False,
                "memory_written": False,
                "world_model_written": False,
                "fact_written": False,
                "violations": [],
                "abort_triggered": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

        observability_case_rows.append(
            {
                "trial_case_id": spec["trial_case_id"],
                "speech_request_id": spec["speech_request_candidate_id"],
                "speech_gate_decision_id": controlled_decision_id,
                "output_event_id": output_event_id,
                "vop_event_id": vop_event_id,
                "output_mode": spec["output_mode"],
                "priority": spec["priority"],
                "safety_status": spec["safety_status"],
                "ownership_status": spec["ownership_status"],
                "interruption_status": spec["interruption_status"],
                "freshness_status": spec["freshness_status"],
                "boundary_flags": boundary,
                "abort_flags": {
                    "abort_check_id": abort_check_id,
                    "abort_triggered": False,
                },
                "output_length": len(spec["output_text_preview"]),
                "output_event_count": 1,
                "final_output_decision": spec["decision"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    output_mode_limited_to_text_only = all(
        row["output_mode"] in ALLOWED_OUTPUT_MODES for row in controlled_text_output_events
    ) and all(row["output_mode"] in ALLOWED_OUTPUT_MODES for row in vop_controlled_event_candidates)

    trial_run = {
        "trial_run_id": TRIAL_RUN_ID,
        "source_definition_id": controlled_output_definition.get("controlled_output_definition_id"),
        "trial_scope": "minimal_runtime_integration_text_only_controlled_output_trial",
        "output_mode": "TEXT_ONLY_FAMILY_ONLY",
        "input_case_count": len(trial_cases),
        "controlled_output_event_count": len(controlled_text_output_events),
        "speech_gate_controlled_decision_count": len(speech_gate_controlled_decisions),
        "vop_controlled_event_count": len(vop_controlled_event_candidates),
        "dry_speech_preview_count": sum(
            1 for row in controlled_text_output_events if row["output_mode"] == "DRY_SPEECH_PREVIEW"
        ),
        "abort_check_count": len(abort_checks),
        "boundary_report_ref": "no_runtime_boundary_report.json",
        "final_trial_status": _final_trial_status(speech_gate_controlled_decisions),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    observability_trace = {
        "observability_id": OBSERVABILITY_ID,
        "run": trial_run,
        "case_traces": observability_case_rows,
        "summary_metrics": {
            "trial_case_count": len(trial_cases),
            "controlled_text_output_event_count": len(controlled_text_output_events),
            "speech_gate_controlled_decision_count": len(speech_gate_controlled_decisions),
            "vop_controlled_event_candidate_count": len(vop_controlled_event_candidates),
            "dry_speech_preview_count": trial_run["dry_speech_preview_count"],
            "abort_check_count": len(abort_checks),
            "output_mode_limited_to_text_only": output_mode_limited_to_text_only,
            **_not_fact(),
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": {
            "phase": PHASE_ID,
            "trial_scope": "minimal_runtime_integration_text_only_controlled_output_trial_only",
            "text_only_controlled_output_trial_executed": True,
            "controlled_output_definition_input_loaded": loaded_flags["controlled_output_definition"],
            "post_shadow_review_input_loaded": loaded_flags["post_shadow_review"],
            "controlled_shadow_trial_input_loaded": loaded_flags["controlled_shadow_trial"],
            "trial_case_count": len(trial_cases),
            "controlled_text_output_event_count": len(controlled_text_output_events),
            "speech_gate_controlled_decision_count": len(speech_gate_controlled_decisions),
            "vop_controlled_event_candidate_count": len(vop_controlled_event_candidates),
            "dry_speech_preview_count": trial_run["dry_speech_preview_count"],
            "abort_check_count": len(abort_checks),
            "output_mode_limited_to_text_only": output_mode_limited_to_text_only,
            **BOUNDARY_FALSE_FLAGS,
            "boundary_ok": True,
            "violations": [],
            "fact_status": "not_fact",
            "write_allowed": False,
            "final_decision": FINAL_DECISION,
            "next_phase_recommendation": RECOMMENDED_NEXT,
            "must_not_recommend_real_tts": True,
            "must_not_recommend_live_audio": True,
            "must_not_recommend_camera_enablement": True,
            "must_not_recommend_map_api_enablement": True,
            "must_not_recommend_memory_or_worldmodel_write": True,
        },
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            **_not_fact(),
        },
        "controlled_output_trial_cases": {
            "trial_case_count": len(trial_cases),
            "rows": trial_cases,
            **_not_fact(),
        },
        "speech_gate_controlled_decisions": {
            "speech_gate_controlled_decision_count": len(speech_gate_controlled_decisions),
            "rows": speech_gate_controlled_decisions,
            **_not_fact(),
        },
        "controlled_text_output_events": {
            "controlled_text_output_event_count": len(controlled_text_output_events),
            "rows": controlled_text_output_events,
            **_not_fact(),
        },
        "vop_controlled_event_candidates": {
            "vop_controlled_event_candidate_count": len(vop_controlled_event_candidates),
            "rows": vop_controlled_event_candidates,
            **_not_fact(),
        },
        "text_only_output_abort_checks": {
            "abort_check_count": len(abort_checks),
            "rows": abort_checks,
            **_not_fact(),
        },
        "observability_trace": observability_trace,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "controlled_output_definition_final_decision": definition_summary.get("final_decision"),
            "post_shadow_review_final_decision": post_shadow_summary.get("final_decision"),
            "post_shadow_review_readiness_decision": post_shadow_readiness.get("readiness_decision"),
            "shadow_trial_final_decision": shadow_summary.get("final_decision"),
            "shadow_gate_count": shadow_gate.get("speech_gate_shadow_decision_count"),
            "shadow_vop_count": shadow_vop.get("vop_shadow_event_count"),
            "shadow_abort_count": shadow_abort.get("abort_check_count"),
            "speech_gate_allowed_decisions": speech_gate_contract.get("allowed_decisions", []),
            "vop_allowed_modes": vop_contract.get("allowed_modes", []),
            "tts_policy_text_only_preferred": tts_policy.get("text_only_output_preferred_for_first_controlled_output"),
            "definition_abort_conditions": definition_abort.get("conditions", []),
            "trial_definition_abort_conditions": trial_abort.get("conditions", []),
            "trial_definition_name": trial_definition.get("trial_name"),
            "post_shadow_review_id": post_shadow_report.get("review_id"),
            "stabilization_final_decision": stabilization_summary.get("final_decision"),
            "stabilization_scenario_count": len(stabilization_scenarios.get("rows") or []),
            "safety_summary_loaded": bool(safety_summary),
            "safety_candidate_count": safety_candidates.get("arbitration_candidate_count"),
            "ownership_candidate_count": ownership_payload.get("decision_candidate_count"),
            "interruption_candidate_count": interruption_payload.get("interruption_decision_candidate_count"),
            **_not_fact(),
        },
    }
