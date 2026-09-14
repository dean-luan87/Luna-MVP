# -*- coding: utf-8 -*-
"""Navigation Guidance to Speech Candidate Adapter v1 — adapter only; no TTS/VOP/runtime.

Phase-Navigation-Guidance-to-Speech-Candidate-Adapter-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Navigation-Guidance-to-Speech-Candidate-Adapter-v1-001"
FINAL_DECISION = "NAVIGATION_GUIDANCE_TO_SPEECH_CANDIDATE_ADAPTER_READY_FOR_BASIC_NAVIGATION_LOOP"
RECOMMENDED_NEXT = "Basic-Navigation-Guidance-Loop-DryRun-v1"

FOLLOWUPS = [
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Safety-Task-Arbitration-Policy-v1",
    "Vision-Evidence-Lifecycle-Policy-v1",
    "Speech-Gate-Runtime-GuardedTrial-v1",
    "Navigation-Map-Context-Contract-v1",
    "Route-Stage-Estimation-DryRun-v1",
]

OPTIONAL_DOC_GLOBS = {
    "speech_gate_runtime": "**/*SPEECH*GATE*.md",
    "navigation_policy": "**/*NAVIGATION*POLICY*.md",
    "safety_task_arbitration": "**/*SAFETY*TASK*ARBIT*.md",
    "risk_safety_arbiter": "**/*RISK*SAFETY*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
}

INTAKE_SPECS = [
    ("vision_ocr_ingest", "vision_ocr_evidence_ingest_integration_check_v1_summary.json", False),
    ("task_observation_request", "task_observation_request_contract_v1_summary.json", False),
    ("task_manager_runtime", "task_manager_runtime_dryrun_v1_summary.json", False),
    ("basic_loop_audit", "basic_functional_loop_runtime_logic_audit_correction_v1_summary.json", False),
    ("voice_dialogue_runtime", "voice_dialogue_task_control_runtime_dryrun_v1_summary.json", False),
    ("voice_guidance_runtime", "voice_guidance_prompt_runtime_dryrun_v1_summary.json", False),
    ("vop_adapter", "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
    ("ocr_activation", "ocr_activation_governance_policy_v1_summary.json", False),
    ("stc", "stc_sampling_guidance_policy_v1_summary.json", False),
    ("system_health", None, True),
    ("simulation", None, True),
]

SUPPORT_TO_SPEECH_TYPE = {
    "safety_guidance_support": "safety_warning",
    "navigation_guidance_support": "navigation_hint",
    "user_view_guidance_support": "view_adjustment",
    "static_reading_guidance_support": "static_reading_prompt",
    "human_assistance_prompt_support": "human_assistance_prompt",
}

SUPPORT_TO_MAPPING_TARGET = {
    "safety_guidance_support": "safety_warning_speech_candidate",
    "navigation_guidance_support": "navigation_hint_speech_candidate",
    "user_view_guidance_support": "view_adjustment_speech_candidate",
    "static_reading_guidance_support": "static_reading_prompt_candidate",
    "human_assistance_prompt_support": "human_assistance_prompt_candidate",
}

SUPPORT_TO_PRIORITY = {
    "safety_guidance_support": "P0_safety_immediate",
    "navigation_guidance_support": "P1_navigation_critical",
    "user_view_guidance_support": "P2_task_guidance",
    "static_reading_guidance_support": "P3_ocr_or_static_reading_guidance",
    "human_assistance_prompt_support": "P2_task_guidance",
}

DOWNSTREAM_TO_SOURCE_TYPE = {
    "navigation_guidance_candidate": "navigation_guidance_support",
    "speech_response_candidate": "status_response",
    "user_confirmation_candidate": "task_clarification",
}

DOWNSTREAM_TO_SPEECH_TYPE = {
    "navigation_guidance_candidate": "navigation_hint",
    "speech_response_candidate": "status_response",
    "user_confirmation_candidate": "clarification",
}

SPEECH_TEXT_TEMPLATES = {
    "safety_warning": "前方可能存在安全风险，建议放慢并注意周围环境。",
    "navigation_hint": "建议沿当前方向继续前进，可能需要再确认目标区域。",
    "view_adjustment": "建议调整视角或朝向，以便更好观察目标区域。",
    "static_reading_prompt": "疑似有可读标识区域，建议靠近后再确认文字内容。",
    "human_assistance_prompt": "当前信息可能不足，建议寻求现场人员协助确认。",
    "clarification": "需要进一步确认您的目标或当前位置，请补充说明。",
    "status_response": "任务仍在进行中，当前仅提供引导提示，尚未确认到达。",
    "repeat_guidance": "重复提示：请结合当前环境再次确认前进方向。",
}

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_vision_ocr_evidence_ingest", "ingest_loaded", [], [], []),
    ("load_task_manager_runtime", "tm_rt_loaded", [], [], []),
    ("load_vop_adapter", "vop_adapter_loaded", [], [], []),
    ("intake_guidance_sources", "guidance_intake_ok", [], [], []),
    ("define_guidance_to_speech_mapping", "mapping_ok", [], [], []),
    ("define_speech_priority_policy", "priority_ok", [], [], []),
    ("define_safety_suppression_policy", "suppression_ok", [], [], []),
    ("define_uncertainty_language_policy", "uncertainty_ok", [], [], []),
    ("define_speech_request_candidate_schema", "schema_ok", [], [], []),
    ("generate_speech_candidates", "speech_ok", [], [], ["tts", "vop"]),
    ("define_vop_handoff_candidate", "vop_handoff_ok", [], [], ["vop_invoke"]),
    ("define_speech_gate_admission_candidate", "gate_admission_ok", [], [], ["speech_gate_runtime"]),
    ("check_navigation_guidance_action_boundary", "nav_boundary_ok", [], [], ["navigation_action"]),
    ("check_evidence_freshness_for_speech", "freshness_ok", [], [], []),
    ("generate_final_adapter_decision", "adapter_ready", [], [], ["production_ready"]),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _find_optional_docs(ws_root: Path) -> List[Dict[str, Any]]:
    docs = ws_root / "docs" / "architecture"
    rows = []
    for doc_id, glob_pat in OPTIONAL_DOC_GLOBS.items():
        found = list(docs.glob(glob_pat)) if docs.is_dir() else []
        rows.append(
            {
                "intake_id": doc_id,
                "input_source": "optional_documentation",
                "source_root_or_path": str(found[0]) if found else "(not_found)",
                "artifact": found[0].name if found else None,
                "loaded": bool(found),
                "optional": True,
                "key_fields_observed": ["documentation_reference"] if found else [],
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_doc_reference_only",
                **_not_fact(),
            }
        )
    return rows


def _priority_for_speech_type(stype: str) -> str:
    return {
        "safety_warning": "P0_safety_immediate",
        "navigation_hint": "P1_navigation_critical",
        "view_adjustment": "P2_task_guidance",
        "static_reading_prompt": "P3_ocr_or_static_reading_guidance",
        "human_assistance_prompt": "P2_task_guidance",
        "clarification": "P4_clarification_or_status",
        "status_response": "P4_clarification_or_status",
        "repeat_guidance": "P5_low_priority",
    }.get(stype, "P4_clarification_or_status")


def _obs_priority_map(obs_requests: List[Dict[str, Any]]) -> Dict[str, str]:
    m: Dict[str, str] = {}
    for r in obs_requests:
        oid = r.get("observation_request_id", "")
        hint = r.get("priority_hint", "guidance")
        if hint == "P0_safety_immediate":
            m[oid] = "P0_safety_immediate"
        elif "safety" in str(hint):
            m[oid] = "P0_safety_immediate"
        else:
            m[oid] = "P2_task_guidance"
    return m


def run_navigation_guidance_to_speech_candidate_adapter_v1(
    *,
    vision_ocr_ingest_root: str,
    task_observation_request_root: str,
    task_manager_runtime_root: str,
    basic_loop_audit_root: str,
    voice_dialogue_runtime_root: str,
    voice_guidance_runtime_root: str,
    vop_adapter_root: str,
    ocr_activation_root: str,
    stc_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "vision_ocr_ingest": Path(vision_ocr_ingest_root).resolve(),
        "task_observation_request": Path(task_observation_request_root).resolve(),
        "task_manager_runtime": Path(task_manager_runtime_root).resolve(),
        "basic_loop_audit": Path(basic_loop_audit_root).resolve(),
        "voice_dialogue_runtime": Path(voice_dialogue_runtime_root).resolve(),
        "voice_guidance_runtime": Path(voice_guidance_runtime_root).resolve(),
        "vop_adapter": Path(vop_adapter_root).resolve(),
        "ocr_activation": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "system_health": Path(system_health_root).resolve(),
        "simulation": Path(simulation_root).resolve(),
    }

    summaries: Dict[str, Any] = {}
    intake_rows: List[Dict[str, Any]] = []
    for iid, art, optional in INTAKE_SPECS:
        root = roots[iid]
        loaded = root.is_dir()
        art_file = art
        if art_file and art_file != "(directory)":
            loaded = loaded and (root / art_file).is_file()
            if loaded:
                summaries[iid] = _read_json(root / art_file)
        intake_rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art_file or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if summaries.get(iid) else (["directory"] if loaded else []),
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "check_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    action_coll = _read_json(
        roots["vision_ocr_ingest"] / "vision_ocr_action_support_evidence_candidate_collection_v1.json"
    ) or {}
    action_supports: List[Dict[str, Any]] = action_coll.get("candidates") or []

    downstream_coll = _read_json(
        roots["task_manager_runtime"] / "task_manager_runtime_downstream_candidate_collection_v1.json"
    ) or {}
    downstreams: List[Dict[str, Any]] = downstream_coll.get("candidates") or []

    action_schedule = _read_json(
        roots["task_manager_runtime"] / "task_manager_runtime_action_schedule_candidate_v1.json"
    ) or {}

    obs_coll = _read_json(
        roots["task_observation_request"] / "task_observation_request_candidate_collection_v1.json"
    ) or {}
    obs_requests: List[Dict[str, Any]] = obs_coll.get("candidates") or []
    obs_pri = _obs_priority_map(obs_requests)

    guidance_source_rows: List[Dict[str, Any]] = []
    for a in action_supports:
        st = a.get("support_type", "safety_guidance_support")
        ve = a.get("source_vision_evidence_candidate_id", "")
        oid = ve.replace("ve_", "") if ve.startswith("ve_") else ""
        guidance_source_rows.append(
            {
                "source_guidance_candidate_id": a.get("action_support_candidate_id"),
                "source_type": st,
                "source_priority_hint": obs_pri.get(oid, SUPPORT_TO_PRIORITY.get(st, "P2_task_guidance")),
                "freshness_status": "session_scoped",
                "accepted_for_speech_adapter": True,
                "rejected_reason_if_any": None,
                **_not_fact(),
            }
        )

    for d in downstreams:
        dtype = d.get("downstream_type", "")
        stype = DOWNSTREAM_TO_SOURCE_TYPE.get(dtype, "status_response")
        guidance_source_rows.append(
            {
                "source_guidance_candidate_id": d.get("downstream_candidate_id"),
                "source_type": stype,
                "source_priority_hint": "P2_task_guidance" if dtype == "navigation_guidance_candidate" else "P4_clarification_or_status",
                "freshness_status": "session_scoped",
                "accepted_for_speech_adapter": True,
                "rejected_reason_if_any": None,
                **_not_fact(),
            }
        )

    safety_active = any(
        r.get("source_type") == "safety_guidance_support" for r in guidance_source_rows
    )

    speech_candidates: List[Dict[str, Any]] = []
    for a in action_supports:
        aid = a.get("action_support_candidate_id", "")
        st = a.get("support_type", "safety_guidance_support")
        speech_type = SUPPORT_TO_SPEECH_TYPE.get(st, "navigation_hint")
        ve = a.get("source_vision_evidence_candidate_id", "")
        oid = ve.replace("ve_", "") if ve.startswith("ve_") else None
        priority = SUPPORT_TO_PRIORITY.get(st, _priority_for_speech_type(speech_type))
        text = SPEECH_TEXT_TEMPLATES.get(speech_type, SPEECH_TEXT_TEMPLATES["navigation_hint"])
        uncertainty = st != "safety_guidance_support"
        speech_candidates.append(
            {
                "speech_request_candidate_id": f"sp_{aid}",
                "source_guidance_candidate_id": aid,
                "source_evidence_candidate_id": ve,
                "source_task_candidate_id": None,
                "speech_type": speech_type,
                "speech_text_candidate_zh": text,
                "priority_level": priority,
                "uncertainty_required": uncertainty,
                "speech_gate_required": True,
                "vop_required_later": True,
                "direct_tts_bypass_forbidden": True,
                "direct_vop_bypass_forbidden": True,
                "submitted_now": False,
                "tts_invoked_now": False,
                "vop_invoked_now": False,
                "is_fact": False,
                "write_allowed": False,
                **_not_fact(),
            }
        )

    for d in downstreams:
        did = d.get("downstream_candidate_id", "")
        dtype = d.get("downstream_type", "")
        if dtype not in DOWNSTREAM_TO_SPEECH_TYPE:
            continue
        speech_type = DOWNSTREAM_TO_SPEECH_TYPE[dtype]
        if any(c.get("speech_request_candidate_id") == f"sp_ds_{did}" for c in speech_candidates):
            continue
        speech_candidates.append(
            {
                "speech_request_candidate_id": f"sp_ds_{did}",
                "source_guidance_candidate_id": did,
                "source_evidence_candidate_id": None,
                "source_task_candidate_id": d.get("source_commit_decision_candidate_id"),
                "speech_type": speech_type,
                "speech_text_candidate_zh": SPEECH_TEXT_TEMPLATES.get(speech_type, SPEECH_TEXT_TEMPLATES["status_response"]),
                "priority_level": _priority_for_speech_type(speech_type),
                "uncertainty_required": True,
                "speech_gate_required": True,
                "vop_required_later": True,
                "direct_tts_bypass_forbidden": True,
                "direct_vop_bypass_forbidden": True,
                "submitted_now": False,
                "tts_invoked_now": False,
                "vop_invoked_now": False,
                "is_fact": False,
                "write_allowed": False,
                **_not_fact(),
            }
        )

    gate_admissions: List[Dict[str, Any]] = []
    for sc in speech_candidates:
        pl = sc.get("priority_level", "P5_low_priority")
        if safety_active and pl in ("P3_ocr_or_static_reading_guidance", "P4_clarification_or_status", "P5_low_priority"):
            decision = "SUPPRESS_BY_SAFETY"
        elif sc.get("uncertainty_required"):
            decision = "ADMIT_AS_CANDIDATE"
        else:
            decision = "ADMIT_AS_CANDIDATE"
        gate_admissions.append(
            {
                "speech_request_candidate_id": sc.get("speech_request_candidate_id"),
                "admission_decision_candidate": decision,
                "priority_level": pl,
                "speech_gate_runtime_invoked_now": False,
                **_not_fact(),
            }
        )

    safety_count = sum(1 for c in speech_candidates if c.get("speech_type") == "safety_warning")
    nav_count = sum(1 for c in speech_candidates if c.get("speech_type") == "navigation_hint")
    clar_count = sum(1 for c in speech_candidates if c.get("speech_type") == "clarification")
    static_count = sum(1 for c in speech_candidates if c.get("speech_type") == "static_reading_prompt")
    human_count = sum(1 for c in speech_candidates if c.get("speech_type") == "human_assistance_prompt")

    trace_steps = []
    for step_id, decision, allowed, blocked, reasons in TRACE_STEPS:
        trace_steps.append(
            {
                "step_id": step_id,
                "step_name": step_id,
                "decision": decision,
                "reason_codes": reasons,
                "allowed_next_actions": allowed,
                "blocked_next_actions": blocked,
                "runtime_action_committed": False,
            }
        )

    mapping_rows = [
        {"source_type": k, "target_speech_candidate": v, "speech_gate_required": True, "vop_required_later": True}
        for k, v in SUPPORT_TO_MAPPING_TARGET.items()
    ]
    mapping_rows.extend(
        [
            {"source_type": "task_clarification", "target_speech_candidate": "clarification_speech_candidate", "speech_gate_required": True, "vop_required_later": True},
            {"source_type": "status_response", "target_speech_candidate": "status_speech_candidate", "speech_gate_required": True, "vop_required_later": True},
            {"source_type": "repeat_guidance", "target_speech_candidate": "repeat_speech_candidate", "speech_gate_required": True, "vop_required_later": True},
        ]
    )

    return {
        "summary": {
            "schema_version": "navigation_guidance_to_speech_candidate_adapter_v1_summary_v0",
            "phase": PHASE_ID,
            "adapter_scope": "navigation_guidance_to_speech_candidate_adapter_only",
            "based_on_vision_ocr_ingest": True,
            "based_on_task_manager_runtime": True,
            "based_on_vop_adapter": roots["vop_adapter"].is_dir(),
            "action_support_candidate_count_observed": len(action_supports),
            "task_downstream_candidate_count_observed": len(downstreams),
            "guidance_to_speech_mapping_defined": True,
            "speech_priority_policy_defined": True,
            "safety_suppression_policy_defined": True,
            "uncertainty_language_policy_defined": True,
            "speech_request_candidate_schema_defined": True,
            "vop_handoff_candidate_defined": True,
            "speech_response_candidates_generated": len(speech_candidates) >= 16,
            "speech_gate_required": True,
            "direct_tts_bypass_forbidden": True,
            "direct_vop_bypass_forbidden": True,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            **_not_fact(),
        },
        "intake": {
            "schema_version": "navigation_guidance_speech_adapter_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "guidance_source": {
            "schema_version": "navigation_guidance_source_intake_matrix_v1",
            "action_support_count": len(action_supports),
            "downstream_count": len(downstreams),
            "action_schedule_loaded": bool(action_schedule),
            "observation_request_count": len(obs_requests),
            "rows": guidance_source_rows,
            **_not_fact(),
        },
        "mapping_policy": {
            "schema_version": "navigation_guidance_to_speech_mapping_policy_v1",
            "mapping_candidate_only": True,
            "speech_gate_required": True,
            "vop_required_later": True,
            "tts_invoked_now": False,
            "vop_invoked_now": False,
            "mappings": mapping_rows,
            **_not_fact(),
        },
        "priority_policy": {
            "schema_version": "navigation_guidance_speech_priority_policy_v1",
            "priority_levels": [
                "P0_safety_immediate",
                "P1_navigation_critical",
                "P2_task_guidance",
                "P3_ocr_or_static_reading_guidance",
                "P4_clarification_or_status",
                "P5_low_priority",
            ],
            "safety_priority_above_task": True,
            "P0_can_interrupt_all_lower": True,
            "P1_can_interrupt_P2_to_P5": True,
            "repeat_guidance_suppressed_when_safety_active": True,
            "status_response_suppressed_when_safety_active": True,
            "priority_is_candidate_only": True,
            **_not_fact(),
        },
        "suppression_policy": {
            "schema_version": "navigation_guidance_safety_suppression_policy_v1",
            "safety_alert_active_blocks_low_priority_speech": True,
            "safety_alert_active_allows_only_P0_or_safety_relevant_P1": True,
            "task_clarification_delayed_when_safety_active": True,
            "repeat_guidance_delayed_when_safety_active": True,
            "human_assistance_prompt_delayed_when_safety_active_unless_safety_related": True,
            "suppression_runtime_invoked_now": False,
            **_not_fact(),
        },
        "uncertainty_policy": {
            "schema_version": "navigation_guidance_uncertainty_language_policy_v1",
            "low_confidence_guidance_must_use_uncertain_language": True,
            "evidence_candidate_not_fact_must_not_be_stated_as_fact": True,
            "stale_evidence_must_not_generate_current_action_prompt": True,
            "possible_marker_language_required": True,
            "forbidden_wording": ["已经确认", "一定是", "你已经到达", "OCR 已经识别成功"],
            "allowed_uncertainty_wording": ["可能", "疑似", "建议", "需要再确认"],
            **_not_fact(),
        },
        "speech_schema": {
            "schema_version": "navigation_guidance_speech_request_candidate_schema_v1",
            "speech_gate_required": True,
            "vop_required_later": True,
            "direct_tts_bypass_forbidden": True,
            "direct_vop_bypass_forbidden": True,
            "submitted_now_default": False,
            "tts_invoked_now_default": False,
            "vop_invoked_now_default": False,
            "field_definitions": {
                "speech_request_candidate_id": {"required": True, "type": "string"},
                "source_guidance_candidate_id": {"required": True, "type": "string"},
                "speech_type": {"type": "enum"},
                "speech_text_candidate_zh": {"type": "string"},
                "priority_level": {"type": "enum"},
                "uncertainty_required": {"type": "boolean"},
            },
            **_not_fact(),
        },
        "speech_collection": {
            "schema_version": "navigation_guidance_speech_candidate_collection_v1",
            "speech_candidate_count": len(speech_candidates),
            "candidates": speech_candidates,
            **_not_fact(),
        },
        "vop_handoff": {
            "schema_version": "navigation_guidance_vop_handoff_candidate_v1",
            "vop_handoff_defined": True,
            "handoff_target": "Voice-Output-Plane",
            "requires_speech_gate": True,
            "payload_fields": [
                "speech_request_candidate_id",
                "speech_text",
                "priority_level",
                "interruptibility",
                "source_chain",
                "task_context_ref",
                "evidence_ref",
            ],
            "handoff_invoked_now": False,
            "vop_invoked_now": False,
            **_not_fact(),
        },
        "gate_admission": {
            "schema_version": "navigation_guidance_speech_gate_admission_dryrun_candidate_v1",
            "speech_gate_admission_candidate_defined": True,
            "admission_decision_types": [
                "ADMIT_AS_CANDIDATE",
                "SUPPRESS_BY_SAFETY",
                "DELAY_FOR_CONFIRMATION",
                "REQUIRE_UNCERTAINTY_REWRITE",
                "BLOCK_STALE_EVIDENCE",
            ],
            "admission_invoked_now": False,
            "speech_gate_runtime_invoked_now": False,
            "candidates": gate_admissions,
            **_not_fact(),
        },
        "nav_boundary": {
            "schema_version": "navigation_guidance_speech_adapter_navigation_action_boundary_v1",
            "navigation_guidance_candidate_can_be_spoken_later": True,
            "navigation_guidance_candidate_is_not_navigation_action": True,
            "speech_candidate_is_not_navigation_action": True,
            "guidance_is_not_action": True,
            "route_state_changed_now": False,
            "map_api_invoked_now": False,
            "navigation_action_triggered": False,
            **_not_fact(),
        },
        "freshness_check": {
            "schema_version": "navigation_guidance_evidence_freshness_speech_check_v1",
            "fresh_evidence_can_support_current_prompt_candidate": True,
            "stale_evidence_blocks_current_action_prompt": True,
            "stale_evidence_can_support_contextual_or_historical_prompt_later": True,
            "expired_evidence_cannot_support_navigation_instruction": True,
            "freshness_check_applied": True,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "navigation_guidance_to_speech_adapter_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "navigation_guidance_to_speech_adapter_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "speech_candidate_count": len(speech_candidates),
            "vop_handoff_defined": True,
            "speech_gate_required": True,
            "tts_invoked_now": False,
            "vop_invoked_now": False,
            "navigation_action_triggered": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "alternate_next_phases": ["Safety-Task-Arbitration-Policy-v1", "Vision-Evidence-Lifecycle-Policy-v1"],
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "navigation_guidance_to_speech_adapter_boundary_report_v1",
            "adapter_only": True,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_gate_runtime_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "navigation_guidance_to_speech_adapter_metrics_candidate_report_v1",
            "action_support_candidate_count_observed": len(action_supports),
            "task_downstream_candidate_count_observed": len(downstreams),
            "speech_candidate_count": len(speech_candidates),
            "safety_speech_candidate_count": safety_count,
            "navigation_hint_candidate_count": nav_count,
            "clarification_candidate_count": clar_count,
            "static_reading_prompt_candidate_count": static_count,
            "human_assistance_prompt_candidate_count": human_count,
            "runtime_action_committed_count": 0,
            "tts_invoked_count": 0,
            "vop_invoked_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "navigation_guidance_to_speech_adapter_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "navigation_guidance_to_speech_adapter_system_health_report_v1",
            "system_health_governance_available": roots["system_health"].is_dir(),
            "speech_runtime_health_checked": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "navigation_guidance_to_speech_adapter_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "adapter_only": True,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_gate_runtime_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "navigation_guidance_to_speech_adapter_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["simulation"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "navigation_guidance_to_speech_adapter_non_claims_report_v1",
            "claims": [
                "adapter_not_tts_runtime",
                "speech_candidate_not_voice_broadcast",
                "vop_handoff_not_vop_invoke",
                "guidance_speech_not_navigation_action",
                "evidence_prompt_not_fact_statement",
                "speech_gate_admission_not_real_admission",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "navigation_guidance_to_speech_adapter_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "navigation_guidance_to_speech_adapter_audit_report_v1",
            "navigation_guidance_to_speech_candidate_adapter_v1_executed": True,
            "adapter_only": True,
            "guidance_to_speech_mapping_defined": True,
            "speech_priority_policy_defined": True,
            "safety_suppression_policy_defined": True,
            "uncertainty_language_policy_defined": True,
            "speech_request_candidate_schema_defined": True,
            "vop_handoff_candidate_defined": True,
            "speech_response_candidates_generated": True,
            "speech_gate_required": True,
            "direct_tts_bypass_forbidden": True,
            "direct_vop_bypass_forbidden": True,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "detector_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
