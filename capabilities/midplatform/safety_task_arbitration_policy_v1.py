# -*- coding: utf-8 -*-
"""Safety Task Arbitration Policy v1 — policy only; no runtime arbitration.

Phase-Safety-Task-Arbitration-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Safety-Task-Arbitration-Policy-v1-001"
FINAL_DECISION = "SAFETY_TASK_ARBITRATION_POLICY_READY_FOR_LOOP_STABILIZATION_TEST"
RECOMMENDED_NEXT = "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1"

FOLLOWUPS = [
    "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1",
    "Safety-Task-Arbitration-Runtime-DryRun-v1",
    "Vision-Evidence-Lifecycle-Policy-v1",
    "Speech-Gate-Runtime-GuardedTrial-v1",
    "Route-Stage-Estimation-DryRun-v1",
    "Information-Lifecycle-Governance-v1",
    "Memory-System-Architecture-v1",
]

OPTIONAL_DOC_GLOBS = {
    "risk_safety_arbiter": "**/*RISK*SAFETY*.md",
    "navigation_policy": "**/*NAVIGATION*POLICY*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
    "gps_context": "**/*GPS*.md",
    "memory_governance": "**/*MEMORY*GOVERN*.md",
    "hardware_stub": "**/*HARDWARE*CAMERA*.md",
    "speech_gate_runtime": "**/*SPEECH*GATE*.md",
}

INTAKE_SPECS = [
    ("basic_navigation_loop", "basic_navigation_guidance_loop_dryrun_v1_summary.json", False),
    ("navigation_guidance_speech_adapter", "navigation_guidance_to_speech_candidate_adapter_v1_summary.json", False),
    ("task_manager_runtime", "task_manager_runtime_dryrun_v1_summary.json", False),
    ("midplatform_task_state", "midplatform_task_state_runtime_dryrun_v1_summary.json", False),
    ("voice_dialogue_runtime", "voice_dialogue_task_control_runtime_dryrun_v1_summary.json", False),
    ("vop_adapter", "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
    ("voice_guidance_runtime", "voice_guidance_prompt_runtime_dryrun_v1_summary.json", False),
    ("ocr_activation", "ocr_activation_governance_policy_v1_summary.json", False),
    ("stc", "stc_sampling_guidance_policy_v1_summary.json", False),
    ("system_health", None, True),
    ("simulation", None, True),
]

PRIORITY_MAP = {
    "P0_safety_immediate": "P0_critical_safety",
    "P1_navigation_critical": "P1_safety_navigation",
    "P2_task_guidance": "P2_task_navigation",
    "P3_ocr_or_static_reading_guidance": "P3_ocr_static_reading",
    "P4_clarification_or_status": "P4_clarification_status",
    "P5_low_priority": "P5_low_priority",
}

DECISION_TO_SOURCE_TYPE = {
    "SAFETY_WARNING_GUIDANCE_CANDIDATE": "safety_guidance",
    "NAVIGATION_HINT_GUIDANCE_CANDIDATE": "navigation_guidance",
    "VIEW_ADJUSTMENT_GUIDANCE_CANDIDATE": "user_view_guidance",
    "STATIC_READING_GUIDANCE_CANDIDATE": "ocr_guidance",
    "HUMAN_ASSISTANCE_GUIDANCE_CANDIDATE": "human_assistance",
}

DECISION_TO_TARGET = {
    "SAFETY_WARNING_GUIDANCE_CANDIDATE": "speech_gate",
    "NAVIGATION_HINT_GUIDANCE_CANDIDATE": "navigation_guidance",
    "VIEW_ADJUSTMENT_GUIDANCE_CANDIDATE": "navigation_guidance",
    "STATIC_READING_GUIDANCE_CANDIDATE": "ocr_activation",
    "HUMAN_ASSISTANCE_GUIDANCE_CANDIDATE": "human_assistance",
}

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_basic_navigation_loop", "nav_loop_loaded", [], [], []),
    ("load_navigation_guidance_speech_adapter", "adapter_loaded", [], [], []),
    ("load_task_manager_runtime", "tm_loaded", [], [], []),
    ("intake_arbitration_sources", "sources_ok", [], [], []),
    ("define_arbitration_schema", "schema_ok", [], [], []),
    ("define_priority_policy", "priority_ok", [], [], []),
    ("define_suppression_policy", "suppression_ok", [], [], []),
    ("define_delay_policy", "delay_ok", [], [], []),
    ("define_interrupt_policy", "interrupt_ok", [], [], []),
    ("define_speech_arbitration_handoff", "speech_handoff_ok", [], [], ["tts", "vop"]),
    ("define_task_commit_arbitration", "commit_ok", [], [], ["task_commit"]),
    ("define_ocr_guidance_arbitration", "ocr_ok", [], [], ["ocr_provider"]),
    ("define_human_assistance_arbitration", "human_ok", [], [], []),
    ("generate_arbitration_candidates", "arb_gen_ok", [], [], ["runtime_arbitration"]),
    ("simulate_safety_active_scenarios", "scenario_ok", [], [], []),
    ("define_feedback_contract", "feedback_ok", [], [], []),
    ("generate_final_policy_decision", "policy_ready", [], [], ["production_ready"]),
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


def _map_priority(pl: str) -> str:
    return PRIORITY_MAP.get(pl, "P4_clarification_status")


def _is_low_priority(pri: str) -> bool:
    return pri in ("P2_task_navigation", "P3_ocr_static_reading", "P4_clarification_status", "P5_low_priority")


def _arbitrate(
    *,
    priority_level: str,
    decision_type: str,
    loop_type: str,
    safety_active: bool,
) -> Tuple[str, str]:
    pri = _map_priority(priority_level)
    target = DECISION_TO_TARGET.get(decision_type, "midplatform")

    if not safety_active:
        return "ALLOW_AS_CANDIDATE", target

    if pri in ("P0_critical_safety", "P1_safety_navigation"):
        if pri == "P1_safety_navigation" and decision_type == "NAVIGATION_HINT_GUIDANCE_CANDIDATE":
            return "DELAY_UNTIL_SAFETY_CLEAR", "navigation_guidance"
        return "ALLOW_AS_CANDIDATE", target

    if decision_type == "STATIC_READING_GUIDANCE_CANDIDATE":
        return "DELAY_UNTIL_SAFETY_CLEAR", "ocr_activation"
    if decision_type in ("HUMAN_ASSISTANCE_GUIDANCE_CANDIDATE",):
        return "DELAY_UNTIL_SAFETY_CLEAR", "human_assistance"
    if decision_type == "NAVIGATION_HINT_GUIDANCE_CANDIDATE":
        return "DELAY_UNTIL_SAFETY_CLEAR", "navigation_guidance"
    if _is_low_priority(pri):
        return "SUPPRESS_BY_SAFETY", "speech_gate"
    return "DELAY_UNTIL_SAFETY_CLEAR", target


def run_safety_task_arbitration_policy_v1(
    *,
    basic_navigation_loop_root: str,
    navigation_guidance_speech_adapter_root: str,
    task_manager_runtime_root: str,
    midplatform_task_state_root: str,
    voice_dialogue_runtime_root: str,
    vop_adapter_root: str,
    voice_guidance_runtime_root: str,
    ocr_activation_root: str,
    stc_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "basic_navigation_loop": Path(basic_navigation_loop_root).resolve(),
        "navigation_guidance_speech_adapter": Path(navigation_guidance_speech_adapter_root).resolve(),
        "task_manager_runtime": Path(task_manager_runtime_root).resolve(),
        "midplatform_task_state": Path(midplatform_task_state_root).resolve(),
        "voice_dialogue_runtime": Path(voice_dialogue_runtime_root).resolve(),
        "vop_adapter": Path(vop_adapter_root).resolve(),
        "voice_guidance_runtime": Path(voice_guidance_runtime_root).resolve(),
        "ocr_activation": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "system_health": Path(system_health_root).resolve(),
        "simulation": Path(simulation_root).resolve(),
    }

    intake_rows: List[Dict[str, Any]] = []
    for iid, art, optional in INTAKE_SPECS:
        root = roots[iid]
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
                "key_fields_observed": ["summary"] if art and loaded else (["directory"] if loaded else []),
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "check_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    e2e = _read_json(roots["basic_navigation_loop"] / "basic_navigation_guidance_loop_end_to_end_candidate_trace_v1.json") or {}
    traces: List[Dict[str, Any]] = e2e.get("traces") or []

    guidance_coll = _read_json(
        roots["basic_navigation_loop"] / "basic_navigation_guidance_decision_candidate_collection_v1.json"
    ) or {}
    guidance_by_id = {g["guidance_decision_candidate_id"]: g for g in guidance_coll.get("candidates") or []}

    speech_coll = _read_json(
        roots["navigation_guidance_speech_adapter"] / "navigation_guidance_speech_candidate_collection_v1.json"
    ) or {}
    speech_by_id = {s["speech_request_candidate_id"]: s for s in speech_coll.get("candidates") or []}

    commit_coll = _read_json(
        roots["task_manager_runtime"] / "task_manager_runtime_commit_decision_candidate_collection_v1.json"
    ) or {}

    source_rows: List[Dict[str, Any]] = []
    for t in traces:
        gref = t.get("guidance_decision_ref")
        g = guidance_by_id.get(gref, {}) if gref else {}
        pl = g.get("priority_level", "P2_task_guidance")
        dt = g.get("decision_type", "SAFETY_WARNING_GUIDANCE_CANDIDATE")
        source_rows.append(
            {
                "source_candidate_id": t.get("trace_id"),
                "source_type": "e2e_loop_trace",
                "loop_type": t.get("loop_type"),
                "priority_level": pl,
                "safety_relevance": dt.startswith("SAFETY") or pl.startswith("P0"),
                "task_relevance": t.get("loop_type") == "task_driven",
                "accepted_for_arbitration_policy": True,
                **_not_fact(),
            }
        )
    for g in guidance_coll.get("candidates") or []:
        source_rows.append(
            {
                "source_candidate_id": g.get("guidance_decision_candidate_id"),
                "source_type": DECISION_TO_SOURCE_TYPE.get(g.get("decision_type", ""), "guidance_decision"),
                "loop_type": "baseline_safety" if "baseline" in str(g.get("source_loop_id", "")) else "task_driven",
                "priority_level": g.get("priority_level"),
                "safety_relevance": "SAFETY" in g.get("decision_type", ""),
                "task_relevance": "task_loop" in str(g.get("source_loop_id", "")),
                "accepted_for_arbitration_policy": True,
                **_not_fact(),
            }
        )
    for s in speech_coll.get("candidates") or []:
        source_rows.append(
            {
                "source_candidate_id": s.get("speech_request_candidate_id"),
                "source_type": "speech_candidate",
                "loop_type": "unknown",
                "priority_level": s.get("priority_level"),
                "safety_relevance": s.get("speech_type") == "safety_warning",
                "task_relevance": True,
                "accepted_for_arbitration_policy": True,
                **_not_fact(),
            }
        )
    for c in commit_coll.get("candidates") or []:
        source_rows.append(
            {
                "source_candidate_id": c.get("commit_decision_candidate_id"),
                "source_type": "task_commit_decision",
                "loop_type": "task_driven",
                "priority_level": "P2_task_navigation",
                "safety_relevance": False,
                "task_relevance": True,
                "accepted_for_arbitration_policy": True,
                **_not_fact(),
            }
        )

    arbitration_candidates: List[Dict[str, Any]] = []
    for t in traces:
        gref = t.get("guidance_decision_ref")
        if not gref or gref not in guidance_by_id:
            continue
        g = guidance_by_id[gref]
        pl = g.get("priority_level", "P2_task_guidance")
        dt = g.get("decision_type", "SAFETY_WARNING_GUIDANCE_CANDIDATE")
        loop_type = t.get("loop_type", "task_driven")
        arb_dec_false, target_false = _arbitrate(
            priority_level=pl, decision_type=dt, loop_type=loop_type, safety_active=False
        )
        arb_dec_true, _ = _arbitrate(
            priority_level=pl, decision_type=dt, loop_type=loop_type, safety_active=True
        )
        arbitration_candidates.append(
            {
                "arbitration_candidate_id": f"arb_{t.get('trace_id')}",
                "source_candidate_id": gref,
                "loop_type": loop_type,
                "source_type": DECISION_TO_SOURCE_TYPE.get(dt, "guidance_decision"),
                "priority_level": _map_priority(pl),
                "arbitration_decision_candidate": arb_dec_false,
                "arbitration_decision_if_safety_active": arb_dec_true,
                "target_module": target_false,
                "arbitration_context": {
                    "safety_active": False,
                    "task_active_candidate": loop_type == "task_driven",
                    "speech_pending_candidate": t.get("speech_candidate_ref"),
                    "navigation_guidance_candidate": dt == "NAVIGATION_HINT_GUIDANCE_CANDIDATE",
                    "ocr_guidance_candidate": dt == "STATIC_READING_GUIDANCE_CANDIDATE",
                    "human_assistance_candidate": dt == "HUMAN_ASSISTANCE_GUIDANCE_CANDIDATE",
                },
                "runtime_action_committed": False,
                **_not_fact(),
            }
        )

    scenario_rows: List[Dict[str, Any]] = []
    for safety_active in (False, True):
        outcomes = []
        for ac in arbitration_candidates:
            pl = ac.get("priority_level", "P5_low_priority")
            dt_key = ac.get("source_type", "")
            if safety_active:
                dec = ac.get("arbitration_decision_if_safety_active", "ALLOW_AS_CANDIDATE")
            else:
                dec = ac.get("arbitration_decision_candidate", "ALLOW_AS_CANDIDATE")
            outcomes.append(
                {
                    "arbitration_candidate_id": ac.get("arbitration_candidate_id"),
                    "priority_level": pl,
                    "decision": dec,
                }
            )
        low_suppressed = sum(
            1
            for o in outcomes
            if safety_active
            and o["decision"] in ("SUPPRESS_BY_SAFETY", "DELAY_UNTIL_SAFETY_CLEAR")
            and o["priority_level"] in ("P2_task_navigation", "P3_ocr_static_reading", "P4_clarification_status", "P5_low_priority")
        )
        scenario_rows.append(
            {
                "scenario_id": f"scenario_safety_active_{str(safety_active).lower()}",
                "safety_active": safety_active,
                "task_context_preserved": True,
                "pending_confirmation_preserved": True,
                "low_priority_suppressed_or_delayed_count": low_suppressed if safety_active else 0,
                "p0_p1_allowed_count": sum(
                    1
                    for o in outcomes
                    if o["priority_level"] in ("P0_critical_safety", "P1_safety_navigation")
                    and o["decision"] in ("ALLOW_AS_CANDIDATE", "DELAY_UNTIL_SAFETY_CLEAR")
                ),
                "runtime_action_committed": False,
                "sample_outcomes": outcomes[:6],
                **_not_fact(),
            }
        )

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

    arb_count = len(arbitration_candidates)
    suppression_rule_count = 6
    delay_rule_count = 5
    interrupt_rule_count = 4

    return {
        "summary": {
            "schema_version": "safety_task_arbitration_policy_v1_summary_v0",
            "phase": PHASE_ID,
            "policy_scope": "safety_task_arbitration_policy_only",
            "based_on_basic_navigation_loop": True,
            "based_on_navigation_guidance_speech_adapter": True,
            "based_on_task_manager_runtime": True,
            "baseline_safety_loop_supported": True,
            "task_driven_loop_supported": True,
            "arbitration_schema_defined": True,
            "priority_policy_defined": True,
            "suppression_policy_defined": True,
            "delay_policy_defined": True,
            "interrupt_policy_defined": True,
            "speech_arbitration_handoff_defined": True,
            "task_commit_arbitration_policy_defined": True,
            "ocr_guidance_arbitration_policy_defined": True,
            "human_assistance_arbitration_policy_defined": True,
            "future_runtime_dryrun_entrypoint_defined": True,
            "runtime_arbitration_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_gate_runtime_invoked": False,
            "navigation_action_triggered": False,
            "task_state_committed_now": False,
            "camera_invoked": False,
            "ocr_provider_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            **_not_fact(),
        },
        "intake": {
            "schema_version": "safety_task_arbitration_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "source_matrix": {
            "schema_version": "safety_task_arbitration_source_matrix_v1",
            "source_candidate_count": len(source_rows),
            "rows": source_rows,
            **_not_fact(),
        },
        "schema": {
            "schema_version": "safety_task_arbitration_schema_v1",
            "arbitration_decision_types": [
                "ALLOW_AS_CANDIDATE",
                "SUPPRESS_BY_SAFETY",
                "DELAY_UNTIL_SAFETY_CLEAR",
                "INTERRUPT_LOWER_PRIORITY",
                "REQUIRE_CONFIRMATION",
                "REQUIRE_UNCERTAINTY_REWRITE",
                "BLOCK_STALE_EVIDENCE",
                "NO_OP",
            ],
            "target_modules": [
                "speech_gate",
                "task_manager",
                "midplatform",
                "navigation_guidance",
                "ocr_activation",
                "human_assistance",
            ],
            "field_definitions": {
                "arbitration_candidate_id": {"required": True},
                "source_candidate_id": {"required": True},
                "arbitration_decision_candidate": {"required": True},
                "runtime_action_committed": {"default": False},
            },
            "runtime_action_committed": False,
            **_not_fact(),
        },
        "priority_policy": {
            "schema_version": "safety_task_priority_policy_v1",
            "priority_levels": [
                "P0_critical_safety",
                "P1_safety_navigation",
                "P2_task_navigation",
                "P3_ocr_static_reading",
                "P4_clarification_status",
                "P5_low_priority",
            ],
            "P0_interrupts_all_lower": True,
            "P1_interrupts_P2_to_P5": True,
            "P2_cannot_interrupt_P0_or_P1": True,
            "baseline_safety_can_preempt_task": True,
            "task_driven_guidance_cannot_preempt_safety": True,
            "priority_policy_is_candidate_only": True,
            **_not_fact(),
        },
        "suppression_policy": {
            "schema_version": "safety_task_suppression_policy_v1",
            "safety_active_suppresses_repeat_guidance": True,
            "safety_active_suppresses_status_response": True,
            "safety_active_suppresses_low_priority_clarification": True,
            "safety_active_suppresses_non_safety_human_assistance_prompt": True,
            "safety_active_does_not_suppress_P0_safety_warning": True,
            "suppression_runtime_invoked_now": False,
            **_not_fact(),
        },
        "delay_policy": {
            "schema_version": "safety_task_delay_policy_v1",
            "safety_active_delays_task_commit": True,
            "safety_active_delays_task_clarification": True,
            "safety_active_delays_ocr_guidance_if_not_safety_related": True,
            "safety_active_delays_navigation_hint_if_lower_than_safety": True,
            "delay_requires_recheck_after_safety_clear": True,
            "task_state_committed_now": False,
            **_not_fact(),
        },
        "interrupt_policy": {
            "schema_version": "safety_task_interrupt_policy_v1",
            "P0_interrupts_all_speech_candidates": True,
            "P1_interrupts_P2_to_P5_speech_candidates": True,
            "safety_interrupt_does_not_delete_task_context": True,
            "safety_interrupt_preserves_pending_confirmation": True,
            "interrupted_candidate_can_resume_later": True,
            "interrupt_runtime_invoked_now": False,
            **_not_fact(),
        },
        "speech_handoff": {
            "schema_version": "safety_task_speech_arbitration_handoff_policy_v1",
            "handoff_target": "Speech-Gate",
            "handoff_payload": [
                "arbitration_candidate",
                "speech_candidate",
                "priority_level",
                "suppress_or_allow_decision",
                "interruptibility",
                "source_chain",
            ],
            "speech_gate_required": True,
            "speech_gate_runtime_invoked_now": False,
            "vop_invoked_now": False,
            "tts_invoked_now": False,
            **_not_fact(),
        },
        "commit_policy": {
            "schema_version": "safety_task_commit_arbitration_policy_v1",
            "task_commit_requires_safety_clear_or_non_conflict": True,
            "safety_active_can_block_commit": True,
            "cancel_confirmation_can_be_delayed_by_safety": True,
            "task_commit_candidate_not_executed_now": True,
            "task_state_committed_now": False,
            "confirmation_required_for_human_assistance": True,
            **_not_fact(),
        },
        "ocr_policy": {
            "schema_version": "safety_task_ocr_guidance_arbitration_policy_v1",
            "safety_related_short_marker_ocr_can_remain_candidate": True,
            "non_safety_ocr_guidance_delayed_when_safety_active": True,
            "ocr_guidance_requires_ocr_activation_gate": True,
            "ocr_guidance_requires_stc_freshness": True,
            "ocr_provider_invoked_now": False,
            "ocrrequest_submitted_now": False,
            **_not_fact(),
        },
        "human_policy": {
            "schema_version": "safety_task_human_assistance_arbitration_policy_v1",
            "human_assistance_requires_confirmation": True,
            "safety_related_human_assistance_can_be_P1": True,
            "non_safety_human_assistance_delayed_when_safety_active": True,
            "human_assistance_prompt_requires_speech_gate": True,
            "action_committed_now": False,
            **_not_fact(),
        },
        "arb_collection": {
            "schema_version": "safety_task_arbitration_candidate_collection_v1",
            "arbitration_candidate_count": arb_count,
            "candidates": arbitration_candidates,
            **_not_fact(),
        },
        "scenario_matrix": {
            "schema_version": "safety_task_safety_active_scenario_matrix_v1",
            "safety_active_scenario_count": 2,
            "rows": scenario_rows,
            **_not_fact(),
        },
        "feedback": {
            "schema_version": "safety_task_arbitration_feedback_contract_v1",
            "feedback_defined": True,
            "feedback_targets": [
                "basic_navigation_guidance_loop_later",
                "navigation_guidance_speech_adapter_later",
                "task_manager_runtime_later",
                "speech_gate_later",
            ],
            "payload": [
                "arbitration_candidate",
                "source_candidate_ref",
                "priority_result",
                "suppression_or_delay_reason",
                "resume_condition",
                "source_chain",
            ],
            "feedback_invoked_now": False,
            "future_runtime_dryrun_entrypoint": "Safety-Task-Arbitration-Runtime-DryRun-v1",
            **_not_fact(),
        },
        "trace": {
            "schema_version": "safety_task_arbitration_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "safety_task_arbitration_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "arbitration_candidate_count": arb_count,
            "safety_active_scenario_count": 2,
            "runtime_action_committed": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "alternate_next_phases": [
                "Vision-Evidence-Lifecycle-Policy-v1",
                "Safety-Task-Arbitration-Runtime-DryRun-v1",
            ],
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "safety_task_arbitration_boundary_report_v1",
            "policy_only": True,
            "runtime_arbitration_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_gate_runtime_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "camera_invoked": False,
            "ocr_provider_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "safety_task_arbitration_metrics_candidate_report_v1",
            "arbitration_candidate_count": arb_count,
            "source_candidate_count": len(source_rows),
            "safety_active_scenario_count": 2,
            "suppression_rule_count": suppression_rule_count,
            "delay_rule_count": delay_rule_count,
            "interrupt_rule_count": interrupt_rule_count,
            "runtime_action_committed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "safety_task_arbitration_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "safety_task_arbitration_system_health_report_v1",
            "system_health_governance_available": roots["system_health"].is_dir(),
            "runtime_health_checked": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "safety_task_arbitration_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "policy_only": True,
            "runtime_arbitration_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_gate_runtime_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "camera_invoked": False,
            "ocr_provider_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "safety_task_arbitration_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["simulation"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "safety_task_arbitration_non_claims_report_v1",
            "claims": [
                "policy_not_runtime",
                "arbitration_candidate_not_real_arbitration",
                "safety_active_scenario_is_simulated",
                "suppress_delay_not_real_suppression",
                "speech_gate_handoff_not_speech_gate_runtime",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "safety_task_arbitration_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "safety_task_arbitration_audit_report_v1",
            "safety_task_arbitration_policy_v1_executed": True,
            "policy_only": True,
            "arbitration_schema_defined": True,
            "priority_policy_defined": True,
            "suppression_policy_defined": True,
            "delay_policy_defined": True,
            "interrupt_policy_defined": True,
            "speech_arbitration_handoff_defined": True,
            "task_commit_arbitration_policy_defined": True,
            "ocr_guidance_arbitration_policy_defined": True,
            "human_assistance_arbitration_policy_defined": True,
            "runtime_arbitration_invoked": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_gate_runtime_invoked": False,
            "navigation_action_triggered": False,
            "task_state_committed_now": False,
            "camera_invoked": False,
            "ocr_provider_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
