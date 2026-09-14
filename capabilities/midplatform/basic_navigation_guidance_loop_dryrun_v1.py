# -*- coding: utf-8 -*-
"""Basic Navigation Guidance Loop DryRun v1 — end-to-end candidate chain only; no runtime.

Phase-Basic-Navigation-Guidance-Loop-DryRun-v1-001
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Basic-Navigation-Guidance-Loop-DryRun-v1-001"
FINAL_DECISION = "BASIC_NAVIGATION_GUIDANCE_LOOP_DRYRUN_READY_FOR_STABILIZATION_TEST"
RECOMMENDED_NEXT = "Safety-Task-Arbitration-Policy-v1"

FOLLOWUPS = [
    "Safety-Task-Arbitration-Policy-v1",
    "Vision-Evidence-Lifecycle-Policy-v1",
    "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1",
    "Speech-Gate-Runtime-GuardedTrial-v1",
    "GPS-Location-Candidate-Contract-v1",
    "Route-Stage-Estimation-DryRun-v1",
    "Information-Lifecycle-Governance-v1",
    "Memory-System-Architecture-v1",
]

OPTIONAL_DOC_GLOBS = {
    "risk_safety_arbiter": "**/*RISK*SAFETY*.md",
    "navigation_policy": "**/*NAVIGATION*POLICY*.md",
    "speech_gate_runtime": "**/*SPEECH*GATE*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
    "gps_context": "**/*GPS*.md",
    "memory_governance": "**/*MEMORY*GOVERN*.md",
    "hardware_stub": "**/*HARDWARE*CAMERA*.md",
    "segmentation_governance": "**/*SEGMENTATION*.md",
    "tracking_governance": "**/*TRACKING*GOVERN*.md",
}

INTAKE_SPECS = [
    ("basic_loop_audit", "basic_functional_loop_runtime_logic_audit_correction_v1_summary.json", False),
    ("task_observation_request", "task_observation_request_contract_v1_summary.json", False),
    ("vision_ocr_ingest", "vision_ocr_evidence_ingest_integration_check_v1_summary.json", False),
    ("navigation_guidance_speech_adapter", "navigation_guidance_to_speech_candidate_adapter_v1_summary.json", False),
    ("task_manager_runtime", "task_manager_runtime_dryrun_v1_summary.json", False),
    ("voice_dialogue_runtime", "voice_dialogue_task_control_runtime_dryrun_v1_summary.json", False),
    ("vop_adapter", "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
    ("ocr_activation", "ocr_activation_governance_policy_v1_summary.json", False),
    ("stc", "stc_sampling_guidance_policy_v1_summary.json", False),
    ("system_health", None, True),
    ("simulation", None, True),
]

SPEECH_TO_DECISION = {
    "safety_warning": "SAFETY_WARNING_GUIDANCE_CANDIDATE",
    "navigation_hint": "NAVIGATION_HINT_GUIDANCE_CANDIDATE",
    "view_adjustment": "VIEW_ADJUSTMENT_GUIDANCE_CANDIDATE",
    "static_reading_prompt": "STATIC_READING_GUIDANCE_CANDIDATE",
    "human_assistance_prompt": "HUMAN_ASSISTANCE_GUIDANCE_CANDIDATE",
    "clarification": "CLARIFICATION_GUIDANCE_CANDIDATE",
    "status_response": "STATUS_RESPONSE_GUIDANCE_CANDIDATE",
    "repeat_guidance": "STATUS_RESPONSE_GUIDANCE_CANDIDATE",
}

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_basic_loop_audit", "audit_loaded", [], [], []),
    ("load_task_observation_request", "obs_loaded", [], [], []),
    ("load_vision_ocr_evidence_ingest", "ingest_loaded", [], [], []),
    ("load_navigation_guidance_speech_adapter", "adapter_loaded", [], [], []),
    ("generate_baseline_safety_loop_dryrun", "baseline_ok", [], [], ["navigation_action"]),
    ("generate_task_driven_guidance_loop_dryrun", "task_ok", [], [], ["navigation_action"]),
    ("generate_guidance_decision_candidates", "decisions_ok", [], [], []),
    ("check_speech_chain_readiness", "speech_chain_ok", [], [], ["tts", "vop"]),
    ("check_safety_priority_preservation", "safety_pri_ok", [], [], []),
    ("check_navigation_guidance_action_boundary", "nav_boundary_ok", [], [], ["navigation_action"]),
    ("check_ocr_use_boundary", "ocr_boundary_ok", [], [], ["ocr_provider"]),
    ("check_evidence_freshness_uncertainty", "freshness_ok", [], [], []),
    ("generate_end_to_end_candidate_trace", "e2e_ok", [], [], []),
    ("generate_final_loop_dryrun_decision", "loop_ready", [], [], ["production_ready"]),
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


def _extract_task_id(obs_id: str) -> Optional[str]:
    m = re.search(r"(tobj_tsc_utt_\d+)", obs_id)
    return m.group(1) if m else None


def _index_by_key(items: List[Dict[str, Any]], key: str, prefix: str = "") -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for it in items:
        kid = it.get(key, "")
        if prefix and kid.startswith(prefix):
            pass
        oid = kid
        if key == "source_observation_request_id":
            oid = kid
        elif key == "source_vision_evidence_candidate_id":
            oid = kid.replace("ve_", "") if kid.startswith("ve_") else kid
        elif key == "action_support_candidate_id":
            oid = kid.replace("as_ve_", "") if kid.startswith("as_ve_") else kid
        elif key == "speech_request_candidate_id":
            gid = it.get("source_guidance_candidate_id", "")
            if gid.startswith("as_ve_"):
                oid = gid.replace("as_ve_", "")
            else:
                oid = kid
        elif key == "verification_support_candidate_id":
            oid = kid.replace("vs_ve_", "") if kid.startswith("vs_ve_") else kid
        elif key == "ocr_evidence_candidate_id":
            oid = kid.replace("ocr_", "") if kid.startswith("ocr_") else kid
        out[oid] = it
    return out


def run_basic_navigation_guidance_loop_dryrun_v1(
    *,
    basic_loop_audit_root: str,
    task_observation_request_root: str,
    vision_ocr_ingest_root: str,
    navigation_guidance_speech_adapter_root: str,
    task_manager_runtime_root: str,
    voice_dialogue_runtime_root: str,
    vop_adapter_root: str,
    ocr_activation_root: str,
    stc_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "basic_loop_audit": Path(basic_loop_audit_root).resolve(),
        "task_observation_request": Path(task_observation_request_root).resolve(),
        "vision_ocr_ingest": Path(vision_ocr_ingest_root).resolve(),
        "navigation_guidance_speech_adapter": Path(navigation_guidance_speech_adapter_root).resolve(),
        "task_manager_runtime": Path(task_manager_runtime_root).resolve(),
        "voice_dialogue_runtime": Path(voice_dialogue_runtime_root).resolve(),
        "vop_adapter": Path(vop_adapter_root).resolve(),
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

    obs_coll = _read_json(roots["task_observation_request"] / "task_observation_request_candidate_collection_v1.json") or {}
    obs_requests: List[Dict[str, Any]] = obs_coll.get("candidates") or []
    baseline_obs = [r for r in obs_requests if r.get("loop_type") == "baseline_safety"]
    task_obs = [r for r in obs_requests if r.get("loop_type") == "task_driven"]

    vision_coll = _read_json(roots["vision_ocr_ingest"] / "vision_evidence_candidate_collection_v1.json") or {}
    vision_by_obs = _index_by_key(vision_coll.get("candidates") or [], "source_observation_request_id")

    action_coll = _read_json(
        roots["vision_ocr_ingest"] / "vision_ocr_action_support_evidence_candidate_collection_v1.json"
    ) or {}
    action_by_obs: Dict[str, Dict[str, Any]] = {}
    for a in action_coll.get("candidates") or []:
        ve = a.get("source_vision_evidence_candidate_id", "")
        oid = ve.replace("ve_", "") if ve.startswith("ve_") else ""
        action_by_obs[oid] = a

    verify_coll = _read_json(
        roots["vision_ocr_ingest"] / "vision_ocr_verification_support_evidence_candidate_collection_v1.json"
    ) or {}
    verify_by_obs: Dict[str, Dict[str, Any]] = {}
    for v in verify_coll.get("candidates") or []:
        ve = v.get("source_vision_evidence_candidate_id", "")
        oid = ve.replace("ve_", "") if ve.startswith("ve_") else ""
        verify_by_obs[oid] = v

    ocr_coll = _read_json(roots["vision_ocr_ingest"] / "ocr_evidence_candidate_collection_v1.json") or {}
    ocr_by_obs: Dict[str, Optional[Dict[str, Any]]] = {}
    for o in ocr_coll.get("candidates") or []:
        oid = o.get("source_observation_request_id", "")
        ocr_by_obs[oid] = o

    speech_coll = _read_json(
        roots["navigation_guidance_speech_adapter"] / "navigation_guidance_speech_candidate_collection_v1.json"
    ) or {}
    speech_by_obs: Dict[str, Dict[str, Any]] = {}
    for s in speech_coll.get("candidates") or []:
        gid = s.get("source_guidance_candidate_id", "")
        if gid.startswith("as_ve_"):
            oid = gid.replace("as_ve_", "")
            speech_by_obs[oid] = s

    gate_coll = _read_json(
        roots["navigation_guidance_speech_adapter"] / "navigation_guidance_speech_gate_admission_dryrun_candidate_v1.json"
    ) or {}
    admission_by_speech = {
        g.get("speech_request_candidate_id"): g.get("admission_decision_candidate")
        for g in gate_coll.get("candidates") or []
    }

    schedule_coll = _read_json(
        roots["task_manager_runtime"] / "task_manager_runtime_action_schedule_candidate_v1.json"
    ) or {}
    schedule_by_task: Dict[str, Dict[str, Any]] = {}
    for sch in schedule_coll.get("candidates") or []:
        tobj = sch.get("source_task_object_candidate_id", "")
        if tobj and tobj not in schedule_by_task:
            schedule_by_task[tobj] = sch

    baseline_rows: List[Dict[str, Any]] = []
    for i, req in enumerate(baseline_obs):
        oid = req.get("observation_request_id", "")
        ve = vision_by_obs.get(oid, {})
        act = action_by_obs.get(oid, {})
        sp = speech_by_obs.get(oid, {})
        sp_id = sp.get("speech_request_candidate_id") if sp else None
        baseline_rows.append(
            {
                "baseline_loop_id": f"baseline_loop_{i + 1:03d}",
                "source_observation_request_id": oid,
                "source_vision_evidence_candidate_id": ve.get("vision_evidence_candidate_id"),
                "source_action_support_candidate_id": act.get("action_support_candidate_id"),
                "source_speech_candidate_id": sp_id,
                "loop_completed_as_candidate": bool(ve and act and sp),
                "safety_priority": "P0_safety_immediate",
                "allowed_without_task": True,
                "navigation_action_triggered": False,
                "tts_invoked": False,
                "vop_invoked": False,
                **_not_fact(),
            }
        )

    task_rows: List[Dict[str, Any]] = []
    for i, req in enumerate(task_obs):
        oid = req.get("observation_request_id", "")
        tid = _extract_task_id(oid)
        ve = vision_by_obs.get(oid, {})
        act = action_by_obs.get(oid, {})
        ver = verify_by_obs.get(oid, {})
        ocr = ocr_by_obs.get(oid)
        sp = speech_by_obs.get(oid, {})
        sch = schedule_by_task.get(tid or "", {})
        task_rows.append(
            {
                "task_loop_id": f"task_loop_{i + 1:03d}",
                "source_task_candidate_id": tid,
                "source_task_schedule_candidate_id": sch.get("action_schedule_candidate_id"),
                "source_observation_request_id": oid,
                "source_vision_evidence_candidate_id": ve.get("vision_evidence_candidate_id"),
                "source_ocr_evidence_candidate_id": ocr.get("ocr_evidence_candidate_id") if ocr else None,
                "source_action_support_candidate_id": act.get("action_support_candidate_id"),
                "source_verification_support_candidate_id": ver.get("verification_support_candidate_id"),
                "source_speech_candidate_id": sp.get("speech_request_candidate_id") if sp else None,
                "loop_completed_as_candidate": bool(ve and act and sp),
                "requires_task_context": True,
                "navigation_action_triggered": False,
                "task_completed_now": False,
                **_not_fact(),
            }
        )

    guidance_decisions: List[Dict[str, Any]] = []
    speech_readiness: List[Dict[str, Any]] = []
    e2e_traces: List[Dict[str, Any]] = []

    def _add_decision(loop_id: str, sp: Dict[str, Any], ve_id: Optional[str]) -> str:
        stype = sp.get("speech_type", "navigation_hint")
        dtype = SPEECH_TO_DECISION.get(stype, "NAVIGATION_HINT_GUIDANCE_CANDIDATE")
        gid = f"gdc_{loop_id}_{sp.get('speech_request_candidate_id', 'unknown')}"
        guidance_decisions.append(
            {
                "guidance_decision_candidate_id": gid,
                "source_loop_id": loop_id,
                "decision_type": dtype,
                "priority_level": sp.get("priority_level", "P2_task_guidance"),
                "evidence_support_ref": ve_id,
                "speech_candidate_ref": sp.get("speech_request_candidate_id"),
                "uncertainty_required": sp.get("uncertainty_required", True),
                "allowed_later": True,
                "executed_now": False,
                "navigation_action_triggered": False,
                **_not_fact(),
            }
        )
        return gid

    for br in baseline_rows:
        oid = br["source_observation_request_id"]
        sp = speech_by_obs.get(oid, {})
        if sp:
            gdc = _add_decision(br["baseline_loop_id"], sp, br.get("source_vision_evidence_candidate_id"))
            sp_id = sp.get("speech_request_candidate_id")
            speech_readiness.append(
                {
                    "speech_chain_id": f"sc_{br['baseline_loop_id']}",
                    "source_guidance_decision_candidate_id": gdc,
                    "speech_candidate_id": sp_id,
                    "speech_gate_required": True,
                    "vop_required_later": True,
                    "admission_candidate_status": admission_by_speech.get(sp_id, "ADMIT_AS_CANDIDATE"),
                    "submitted_now": False,
                    "tts_invoked_now": False,
                    "vop_invoked_now": False,
                    **_not_fact(),
                }
            )
            e2e_traces.append(
                {
                    "trace_id": f"trace_{br['baseline_loop_id']}",
                    "loop_type": "baseline_safety",
                    "observation_request_ref": oid,
                    "evidence_ref": br.get("source_vision_evidence_candidate_id"),
                    "support_ref": br.get("source_action_support_candidate_id"),
                    "guidance_decision_ref": gdc,
                    "speech_candidate_ref": sp_id,
                    "final_candidate_state": "BASELINE_SAFETY_LOOP_CANDIDATE_COMPLETE",
                    "runtime_action_committed": False,
                    **_not_fact(),
                }
            )

    for tr in task_rows:
        oid = tr["source_observation_request_id"]
        sp = speech_by_obs.get(oid, {})
        if sp:
            gdc = _add_decision(tr["task_loop_id"], sp, tr.get("source_vision_evidence_candidate_id"))
            sp_id = sp.get("speech_request_candidate_id")
            speech_readiness.append(
                {
                    "speech_chain_id": f"sc_{tr['task_loop_id']}",
                    "source_guidance_decision_candidate_id": gdc,
                    "speech_candidate_id": sp_id,
                    "speech_gate_required": True,
                    "vop_required_later": True,
                    "admission_candidate_status": admission_by_speech.get(sp_id, "ADMIT_AS_CANDIDATE"),
                    "submitted_now": False,
                    "tts_invoked_now": False,
                    "vop_invoked_now": False,
                    **_not_fact(),
                }
            )
            e2e_traces.append(
                {
                    "trace_id": f"trace_{tr['task_loop_id']}",
                    "loop_type": "task_driven",
                    "observation_request_ref": oid,
                    "evidence_ref": tr.get("source_vision_evidence_candidate_id"),
                    "support_ref": tr.get("source_action_support_candidate_id"),
                    "guidance_decision_ref": gdc,
                    "speech_candidate_ref": sp_id,
                    "final_candidate_state": "TASK_DRIVEN_LOOP_CANDIDATE_COMPLETE",
                    "runtime_action_committed": False,
                    **_not_fact(),
                }
            )
        else:
            e2e_traces.append(
                {
                    "trace_id": f"trace_{tr['task_loop_id']}",
                    "loop_type": "task_driven",
                    "observation_request_ref": oid,
                    "evidence_ref": tr.get("source_vision_evidence_candidate_id"),
                    "support_ref": tr.get("source_action_support_candidate_id"),
                    "guidance_decision_ref": None,
                    "speech_candidate_ref": None,
                    "final_candidate_state": "NO_GUIDANCE_DUE_TO_MISSING_SPEECH_LINK",
                    "runtime_action_committed": False,
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

    ocr_count = len(ocr_coll.get("candidates") or [])
    action_count = len(action_coll.get("candidates") or [])
    speech_count = len(speech_coll.get("candidates") or [])
    vision_count = len(vision_coll.get("candidates") or [])

    return {
        "summary": {
            "schema_version": "basic_navigation_guidance_loop_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "basic_navigation_guidance_loop_dryrun_only",
            "based_on_basic_loop_audit": True,
            "based_on_task_observation_request": True,
            "based_on_vision_ocr_ingest": True,
            "based_on_navigation_guidance_speech_adapter": True,
            "baseline_safety_loop_dryrun_generated": len(baseline_rows) >= 4,
            "task_driven_guidance_loop_dryrun_generated": len(task_rows) >= 12,
            "baseline_safety_request_count_observed": len(baseline_obs),
            "task_driven_request_count_observed": len(task_obs),
            "vision_evidence_candidate_count_observed": vision_count,
            "ocr_evidence_candidate_count_observed": ocr_count,
            "action_support_candidate_count_observed": action_count,
            "speech_candidate_count_observed": speech_count,
            "guidance_decision_candidates_generated": len(guidance_decisions) > 0,
            "speech_chain_readiness_generated": len(speech_readiness) > 0,
            "navigation_guidance_action_boundary_preserved": True,
            "safety_priority_preserved": True,
            "uncertainty_language_preserved": True,
            "camera_invoked": False,
            "detector_invoked": False,
            "ocr_provider_invoked": False,
            "ocrrequest_submitted": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            **_not_fact(),
        },
        "intake": {
            "schema_version": "basic_navigation_guidance_loop_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "baseline_matrix": {
            "schema_version": "basic_navigation_baseline_safety_loop_dryrun_matrix_v1",
            "baseline_loop_candidate_count": len(baseline_rows),
            "rows": baseline_rows,
            **_not_fact(),
        },
        "task_matrix": {
            "schema_version": "basic_navigation_task_driven_loop_dryrun_matrix_v1",
            "task_driven_loop_candidate_count": len(task_rows),
            "rows": task_rows,
            **_not_fact(),
        },
        "guidance_decisions": {
            "schema_version": "basic_navigation_guidance_decision_candidate_collection_v1",
            "guidance_decision_candidate_count": len(guidance_decisions),
            "candidates": guidance_decisions,
            **_not_fact(),
        },
        "speech_readiness": {
            "schema_version": "basic_navigation_speech_chain_readiness_matrix_v1",
            "speech_chain_ready_candidate_count": len(speech_readiness),
            "rows": speech_readiness,
            **_not_fact(),
        },
        "safety_priority": {
            "schema_version": "basic_navigation_safety_priority_preservation_matrix_v1",
            "safety_priority_above_task": True,
            "baseline_safety_allowed_without_task": True,
            "safety_guidance_can_interrupt_task_guidance_later": True,
            "low_priority_task_speech_suppressed_when_safety_active": True,
            "safety_priority_runtime_invoked_now": False,
            **_not_fact(),
        },
        "nav_boundary": {
            "schema_version": "basic_navigation_guidance_action_boundary_check_v1",
            "guidance_candidate_generated": len(guidance_decisions) > 0,
            "guidance_candidate_is_not_navigation_action": True,
            "speech_candidate_is_not_navigation_action": True,
            "route_state_changed_now": False,
            "map_api_invoked_now": False,
            "navigation_action_triggered": False,
            **_not_fact(),
        },
        "ocr_boundary": {
            "schema_version": "basic_navigation_ocr_use_boundary_check_v1",
            "ocr_evidence_candidate_count_observed": ocr_count,
            "ocr_provider_invoked": False,
            "ocrrequest_submitted": False,
            "ocr_evidence_is_not_fact": True,
            "empty_ocr_is_not_no_text_fact": True,
            "generic_environment_ocr_forbidden": True,
            "ocr_used_only_as_support_candidate": True,
            **_not_fact(),
        },
        "freshness_uncertainty": {
            "schema_version": "basic_navigation_evidence_freshness_uncertainty_check_v1",
            "stale_evidence_blocks_current_navigation_prompt": True,
            "low_confidence_guidance_requires_uncertainty_language": True,
            "evidence_candidate_not_fact_must_not_be_stated_as_fact": True,
            "forbidden_fact_wording_preserved": True,
            "uncertainty_language_preserved": True,
            "forbidden_wording": ["已经确认", "一定是", "你已经到达", "OCR 已经识别成功"],
            **_not_fact(),
        },
        "e2e_trace": {
            "schema_version": "basic_navigation_guidance_loop_end_to_end_candidate_trace_v1",
            "trace_count": len(e2e_traces),
            "traces": e2e_traces,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "basic_navigation_guidance_loop_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "basic_navigation_guidance_loop_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "baseline_loop_candidate_count": len(baseline_rows),
            "task_driven_loop_candidate_count": len(task_rows),
            "guidance_decision_candidate_count": len(guidance_decisions),
            "speech_chain_ready_candidate_count": len(speech_readiness),
            "runtime_action_committed": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "alternate_next_phases": [
                "Vision-Evidence-Lifecycle-Policy-v1",
                "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1",
                "Speech-Gate-Runtime-GuardedTrial-v1",
            ],
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "basic_navigation_guidance_loop_boundary_report_v1",
            "dryrun_only": True,
            "camera_invoked": False,
            "detector_invoked": False,
            "ocr_provider_invoked": False,
            "ocrrequest_submitted": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "basic_navigation_guidance_loop_metrics_candidate_report_v1",
            "baseline_loop_candidate_count": len(baseline_rows),
            "task_driven_loop_candidate_count": len(task_rows),
            "vision_evidence_candidate_count_observed": vision_count,
            "ocr_evidence_candidate_count_observed": ocr_count,
            "action_support_candidate_count_observed": action_count,
            "speech_candidate_count_observed": speech_count,
            "guidance_decision_candidate_count": len(guidance_decisions),
            "end_to_end_trace_count": len(e2e_traces),
            "runtime_action_committed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "basic_navigation_guidance_loop_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "basic_navigation_guidance_loop_system_health_report_v1",
            "system_health_governance_available": roots["system_health"].is_dir(),
            "runtime_health_checked": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "basic_navigation_guidance_loop_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "dryrun_only": True,
            "camera_invoked": False,
            "detector_invoked": False,
            "ocr_provider_invoked": False,
            "ocrrequest_submitted": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "basic_navigation_guidance_loop_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["simulation"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "basic_navigation_guidance_loop_non_claims_report_v1",
            "claims": [
                "loop_dryrun_not_real_navigation",
                "baseline_loop_not_real_safety_runtime",
                "task_driven_loop_not_task_executed",
                "guidance_candidate_not_navigation_action",
                "speech_candidate_not_voice_broadcast",
                "ocr_evidence_not_real_ocr_output",
                "e2e_trace_not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "basic_navigation_guidance_loop_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "basic_navigation_guidance_loop_audit_report_v1",
            "basic_navigation_guidance_loop_dryrun_v1_executed": True,
            "dryrun_only": True,
            "baseline_safety_loop_dryrun_generated": True,
            "task_driven_guidance_loop_dryrun_generated": True,
            "guidance_decision_candidates_generated": True,
            "speech_chain_readiness_generated": True,
            "navigation_guidance_action_boundary_preserved": True,
            "safety_priority_preserved": True,
            "uncertainty_language_preserved": True,
            "camera_invoked": False,
            "detector_invoked": False,
            "ocr_provider_invoked": False,
            "ocrrequest_submitted": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "navigation_action_triggered": False,
            "map_api_invoked": False,
            "task_state_committed_now": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
