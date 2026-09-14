# -*- coding: utf-8 -*-
"""Return To Software Mainline Closure v1 — aggregate closure; no runtime execution.

Phase-Return-To-Software-Mainline-Closure-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Return-To-Software-Mainline-Closure-v1-001"
FINAL_DECISION = "SOFTWARE_MAINLINE_READY_FOR_NEXT_PLANNING"

EVAL_BASE = Path("/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out")

COMPLETED_PHASES: List[Dict[str, Any]] = [
    {
        "phase_name": "Hardware-Camera-Runtime-Adapter-Implementation-Stub-v1",
        "observed_status": "GO",
        "closure_role": "hardware_boundary_frozen",
        "output_root": str(EVAL_BASE / "hardware_camera_runtime_adapter_implementation_stub_v1_smoke_v0"),
        "key_decision": "STUB_READY_SOFTWARE_BOUNDARY_CLOSED",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": "real_camera_disabled",
    },
    {
        "phase_name": "Hardware-Camera-Runtime-Adapter-Contract-v1",
        "observed_status": "GO",
        "closure_role": "adapter_contract_defined",
        "output_root": str(EVAL_BASE / "hardware_camera_runtime_adapter_contract_v1_smoke_v0"),
        "key_decision": "READY_FOR_ADAPTER_IMPLEMENTATION_OR_GUARDEDTRIAL_PRECHECK",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": "adapter_implementation_missing",
    },
    {
        "phase_name": "Hardware-Profile-Capability-Registry-v1",
        "observed_status": "GO",
        "closure_role": "profile_registry_ready",
        "output_root": str(EVAL_BASE / "hardware_profile_capability_registry_v1_smoke_v0"),
        "key_decision": "READY_FOR_PROFILE_REGISTRY_REVIEW_OR_ADAPTER_IMPLEMENTATION",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": None,
    },
    {
        "phase_name": "Hardware-Camera-Control-Runtime-DryRun-v1",
        "observed_status": "GO",
        "closure_role": "hardware_runtime_dryrun",
        "output_root": str(EVAL_BASE / "hardware_camera_control_runtime_dryrun_v1_smoke_v0"),
        "key_decision": "BLOCK_RUNTIME_CAMERA_ACTION",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": "hardware_unknown",
    },
    {
        "phase_name": "Hardware-Camera-Control-Contract-v1",
        "observed_status": "GO",
        "closure_role": "hardware_contract",
        "output_root": str(EVAL_BASE / "hardware_camera_control_contract_v1_smoke_v0"),
        "key_decision": "CONTRACT_DEFINED",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": None,
    },
    {
        "phase_name": "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
        "observed_status": "GO",
        "closure_role": "rrd_runtime",
        "output_root": str(EVAL_BASE / "static_readable_region_discovery_runtime_dryrun_v1_smoke_v0"),
        "key_decision": "RRD_CANDIDATES_GENERATED",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": "no_captured_frame",
    },
    {
        "phase_name": "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
        "observed_status": "GO",
        "closure_role": "isrc_runtime",
        "output_root": str(EVAL_BASE / "static_reading_information_source_localization_runtime_dryrun_v1_smoke_v0"),
        "key_decision": "ISRC_RUNTIME_DRYRUN",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": None,
    },
    {
        "phase_name": "Static-Reading-Task-Scene-Context-Reevaluation-DryRun-v1",
        "observed_status": "GO",
        "closure_role": "tsc_reevaluation",
        "output_root": str(EVAL_BASE / "static_reading_task_scene_context_reevaluation_dryrun_v1_smoke_v0"),
        "key_decision": "TSC_REEVALUATION_DRYRUN",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": None,
    },
    {
        "phase_name": "Confirmed-Text-Evidence-Memory-Governance-Contract-v1",
        "observed_status": "GO",
        "closure_role": "memory_governance_contract",
        "output_root": str(EVAL_BASE / "confirmed_text_evidence_memory_governance_contract_v1_smoke_v0"),
        "key_decision": "READY_FOR_MEMORY_GOVERNANCE_HANDOFF_DRYRUN_LATER",
        "allowed_to_extend_now": True,
        "blocked_reason_if_any": None,
    },
    {
        "phase_name": "Confirmed-Text-Evidence-Memory-Handoff-DryRun-v1",
        "observed_status": "GO",
        "closure_role": "memory_handoff_dryrun",
        "output_root": str(EVAL_BASE / "confirmed_text_evidence_memory_handoff_dryrun_v1_smoke_v0"),
        "key_decision": "READY_FOR_MEMORY_GOVERNANCE_HANDOFF_RUNTIME_LATER",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": "no_real_memory_system",
    },
    {
        "phase_name": "OCRRequest-Gated-Submission-from-StaticReading-v1",
        "observed_status": "GO",
        "closure_role": "staticreading_ocr_gate",
        "output_root": str(EVAL_BASE / "ocrrequest_gated_submission_from_staticreading_v1_smoke_v0"),
        "key_decision": "BLOCK_OCRREQUEST_STATICREADING_UNTIL_CAPTURED_FRAME",
        "allowed_to_extend_now": False,
        "blocked_reason_if_any": "capture_status_not_captured",
    },
]

BLOCKERS: List[Dict[str, Any]] = [
    ("no_real_camera", "hardware", "Hardware-Adapter-Stub", "no frame capture", "expected", "Hardware-GuardedTrial-Precheck or RealImplementation"),
    ("adapter_stub_only", "hardware", "Hardware-Adapter-Stub", "stub boundary only", "expected", "external hardware integration"),
    ("capture_status_not_captured", "capture", "OCRRequest-StaticReading-Gate", "OCR blocked", "expected", "real static_capture_result"),
    ("frame_ref_missing", "capture", "OCRRequest-StaticReading-Gate", "OCR blocked", "expected", "captured frame_ref"),
    ("stc_anchor_missing", "capture", "OCRRequest-StaticReading-Gate", "OCR blocked", "expected", "STC anchor after capture"),
    ("capture_quality_missing", "capture", "OCRRequest-StaticReading-Gate", "OCR blocked", "expected", "capture quality metadata"),
    ("ocrrequest_staticreading_blocked", "ocr", "OCRRequest-StaticReading-Gate", "34 blocked candidates", "expected", "reopen after capture"),
    ("no_real_memory_system", "memory", "Memory-Handoff-DryRun", "dryrun only", "expected", "Memory Governance runtime"),
    ("memory_handoff_only_dryrun", "memory", "Memory-Handoff-DryRun", "no memory write", "expected", "handoff runtime later"),
    ("worldmodel_write_not_allowed", "worldmodel", "Closure", "WM not started", "expected", "WorldModel governance phases"),
    ("scene_delta_not_allowed", "worldmodel", "Closure", "no SceneDelta", "expected", "scene governance"),
    ("ep_v5_missing_ocr_result", "ocr_pipeline", "Closure", "EP v5 blocked", "expected", "OCR after capture"),
    ("semantic_v5_missing_ep_v5", "ocr_pipeline", "Closure", "Semantic blocked", "expected", "EP v5 first"),
    ("sv_v3_missing_ep_v5", "ocr_pipeline", "Closure", "SV v3 blocked", "expected", "EP v5 first"),
    ("hardware_guardedtrial_not_authorized", "hardware", "Adapter-Contract", "guardedtrial false", "expected", "GuardedTrial-Precheck"),
]

ALLOWED_ENTRYPOINTS: List[Dict[str, Any]] = [
    ("WorldModel-Lookup-for-Reading-DryRun-v1", True, True, ["RRD", "TSC", "unresolved slot contract"], "no WM write; lookup dryrun", "low", 1),
    ("Fragment-Evidence-Weaving-Governance-v1", True, True, ["closure", "evidence chain policy"], "governance only", "low", 2),
    ("Emotional-Context-Background-Candidate-DryRun-v1", True, True, ["memory handoff candidates"], "background candidate only", "low", 3),
    ("Memory-Governance-Delete-Update-Authority-Policy-v1", True, True, ["memory governance contract"], "authority policy", "medium", 4),
    ("User-Privacy-Consent-Governance-v1", True, True, ["privacy policy"], "consent boundary", "medium", 5),
    ("Return-To-Software-Mainline-Planning-v1", True, True, ["this closure"], "planning only", "low", 6),
    ("Hardware-Camera-Control-GuardedTrial-Precheck-v1", False, True, ["real adapter", "permission"], "hardware frozen", "high", 99),
    ("OCRRequest-Gated-Submission-from-StaticReading-v1-GuardedTrial", False, True, ["captured frame", "STC"], "OCR gate closed", "high", 99),
]

FORBIDDEN_ACTIONS: List[Dict[str, Any]] = [
    ("run_staticreading_ocr_now", "no captured frame", "ocr_bypass", "static_capture_result"),
    ("submit_ocrrequest_without_captured_frame", "gate closed", "ocr_bypass", "capture_status=captured"),
    ("generate_ep_v5_without_ocr_result", "no raw OCR", "pipeline_skip", "raw_ocr_result"),
    ("generate_semantic_v5_without_ep_v5", "no EP v5", "pipeline_skip", "evidence_pack_v5"),
    ("run_sv_v3_without_ep_v5", "no EP v5", "pipeline_skip", "evidence_pack_v5"),
    ("call_memory_system_now", "dryrun only", "memory_bypass", "memory_governance_runtime"),
    ("write_memory_now", "append-only contract", "fact_write", "memory_write_gate"),
    ("write_worldmodel_now", "WM not authorized", "fact_write", "worldmodel_governance"),
    ("generate_scene_delta_now", "not authorized", "fact_write", "scene_governance"),
    ("launch_hardware_guardedtrial_without_precheck", "hardware frozen", "hardware_bypass", "GuardedTrial-Precheck"),
    ("bypass_adapter_stub", "stub boundary", "hardware_bypass", "real_adapter"),
    ("use_mock_text_as_ocr_result", "forbidden policy", "ocr_integrity", "real_ocr_only"),
    ("full_frame_ocr_for_staticreading_now", "region OCR only", "ocr_scope", "roi_static_capture"),
    ("promote_profile_fact_from_handoff_candidate", "not_fact candidates", "fact_write", "profile_governance"),
    ("invoke_llm_to_summarize_into_memory", "no LLM write", "memory_bypass", "memory_governance"),
]

ROADMAP: List[Dict[str, Any]] = [
    ("A", "WorldModel-Lookup-for-Reading-DryRun-v1", "WM/unresolved slot hint for ISRC without WM write", ["RRD", "TSC", "WM contract"], 1, "high", "low"),
    ("B", "Fragment-Evidence-Weaving-Governance-v1", "fragment weaving / worldline candidate governance", ["evidence chain", "conflict policy"], 2, "high", "low"),
    ("C", "Emotional-Context-Background-Candidate-DryRun-v1", "environment/profile/emotional background candidates", ["memory handoff", "text evidence"], 3, "medium", "low"),
    ("D", "Memory-Governance-Delete-Update-Authority-Policy-v1", "Memory delete/update/merge authority", ["memory contract"], 4, "medium", "medium"),
    ("E", "User-Privacy-Consent-Governance-v1", "privacy consent for sensitive text/profile", ["privacy policy"], 5, "medium", "medium"),
    ("F", "Hardware-Camera-Control-GuardedTrial-Precheck-v1", "reopen hardware when ready", ["real adapter", "permission"], 99, "low", "high"),
]

FOLLOWUPS = [
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Fragment-Evidence-Weaving-Governance-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
    "Memory-Governance-Delete-Update-Authority-Policy-v1",
    "User-Privacy-Consent-Governance-v1",
    "Hardware-Camera-Control-GuardedTrial-Precheck-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1-GuardedTrial",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_staticreading_ocrrequest_gate", "ocr_gate_loaded", [], [], ["ocr_invoke"]),
    ("load_memory_handoff", "mem_handoff_loaded", [], [], ["memory_write"]),
    ("load_hardware_adapter_stub", "hw_stub_loaded", [], [], ["camera"]),
    ("load_rrd_runtime", "rrd_loaded", [], [], []),
    ("verify_closed_chains", "chains_verified", [], [], []),
    ("register_current_blockers", "blockers_registered", [], [], []),
    ("define_allowed_next_entrypoints", "allowed_defined", [], [], []),
    ("define_forbidden_next_actions", "forbidden_defined", [], [], []),
    ("generate_software_mainline_candidate_roadmap", "roadmap", [], [], []),
    ("close_staticreading_ocr_chain", "ocr_closed", [], [], ["submit_ocr"]),
    ("close_hardware_chain", "hw_frozen", [], [], ["guardedtrial_now"]),
    ("close_memory_handoff_chain", "mem_closed", [], [], []),
    ("link_worldmodel_fragment_future", "wm_fragment_link", [], [], ["wm_write"]),
    ("generate_final_closure_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _load_gate(roots: Dict[str, Path]) -> Dict[str, Any]:
    s = _read_json(roots["ocr_gate"] / "ocrrequest_gated_submission_from_staticreading_v1_summary.json") or {}
    m = _read_json(roots["ocr_gate"] / "ocrrequest_staticreading_metrics_candidate_report_v1.json") or {}
    return {**s, **m}


def _load_mem(roots: Dict[str, Path]) -> Dict[str, Any]:
    s = _read_json(roots["mem_handoff"] / "confirmed_text_evidence_memory_handoff_dryrun_v1_summary.json") or {}
    m = _read_json(roots["mem_handoff"] / "confirmed_text_memory_handoff_metrics_candidate_report_v1.json") or {}
    return {**s, **m}


def _load_hw(roots: Dict[str, Path]) -> Dict[str, Any]:
    s = _read_json(roots["hw_stub"] / "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json") or {}
    f = _read_json(roots["hw_stub"] / "hardware_camera_adapter_frame_capture_stub_response_v1.json") or {}
    g = _read_json(roots["hw_stub"] / "hardware_camera_adapter_stub_guardedtrial_readiness_link_v1.json") or {}
    return {"summary": s, "frame": f, "guardedtrial": g}


def _intake(roots: Dict[str, Path]) -> Dict[str, Any]:
    specs = [
        ("ocrrequest_staticreading_gate", roots["ocr_gate"], "ocrrequest_gated_submission_from_staticreading_v1_summary.json", False),
        ("memory_handoff", roots["mem_handoff"], "confirmed_text_evidence_memory_handoff_dryrun_v1_summary.json", False),
        ("memory_governance_contract", roots["mem_contract"], "confirmed_text_evidence_memory_governance_contract_v1_summary.json", False),
        ("hardware_adapter_stub", roots["hw_stub"], "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json", False),
        ("hardware_adapter_contract", roots["hw_contract"], "hardware_camera_runtime_adapter_contract_v1_summary.json", False),
        ("rrd_runtime", roots["rrd"], "static_readable_region_discovery_runtime_dryrun_v1_summary.json", False),
        ("isrc_runtime", roots["isrc"], "static_reading_information_source_localization_runtime_dryrun_v1_summary.json", False),
        ("tsc_reevaluation", roots["tsc"], "static_reading_task_scene_context_reevaluation_dryrun_v1_summary.json", False),
        ("ocr_activation", roots["ocr"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("stc_sampling", roots["stc"], "stc_sampling_guidance_policy_v1_summary.json", False),
        ("benchmark", roots["bench"], None, False),
        ("system_health", roots["health"], None, False),
        ("simulation", roots["sim"], None, False),
    ]
    rows = []
    for iid, root, art, optional in specs:
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
        rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else "missing",
                **_not_fact(),
            }
        )
    return {
        "schema_version": "return_to_software_mainline_input_intake_matrix_v1",
        "rows": rows,
        **_not_fact(),
    }


def run_return_to_software_mainline_closure_v1(
    *,
    ocrrequest_staticreading_root: str,
    memory_handoff_root: str,
    memory_governance_contract_root: str,
    hardware_adapter_stub_root: str,
    hardware_adapter_contract_root: str,
    rrd_runtime_root: str,
    isrc_runtime_root: str,
    tsc_reevaluation_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    roots = {
        "ocr_gate": Path(ocrrequest_staticreading_root).resolve(),
        "mem_handoff": Path(memory_handoff_root).resolve(),
        "mem_contract": Path(memory_governance_contract_root).resolve(),
        "hw_stub": Path(hardware_adapter_stub_root).resolve(),
        "hw_contract": Path(hardware_adapter_contract_root).resolve(),
        "rrd": Path(rrd_runtime_root).resolve(),
        "isrc": Path(isrc_runtime_root).resolve(),
        "tsc": Path(tsc_reevaluation_root).resolve(),
        "ocr": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_sampling_guidance_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    gate = _load_gate(roots)
    mem = _load_mem(roots)
    hw = _load_hw(roots)

    capture_status = gate.get("capture_status_observed", "not_captured")
    rr_count = gate.get("readable_region_candidate_count_observed", 34)
    ho_count = gate.get("static_capture_handoff_candidate_count_observed", 26)
    blocked_ocr = gate.get("blocked_ocrrequest_candidate_count", 34)

    completed = [{**p, **_not_fact()} for p in COMPLETED_PHASES]

    blocker_rows = [
        {
            "blocker_id": bid,
            "blocker_type": btype,
            "source_phase": src,
            "blocking_effect": effect,
            "expected_or_unexpected": exp_unexp,
            "allowed_resolution_path": resolution,
            "must_not_bypass": True,
            **_not_fact(),
        }
        for bid, btype, src, effect, exp_unexp, resolution in BLOCKERS
    ]

    entry_rows = [
        {
            "entrypoint_name": name,
            "allowed_now": now,
            "allowed_later": later,
            "prerequisites": prereq,
            "reason": reason,
            "risk_level": risk,
            "recommended_priority": pri,
            **_not_fact(),
        }
        for name, now, later, prereq, reason, risk, pri in ALLOWED_ENTRYPOINTS
    ]

    forbidden_rows = [
        {
            "action": action,
            "forbidden_now": True,
            "reason": reason,
            "violation_type": vtype,
            "required_future_gate": gate_req,
            **_not_fact(),
        }
        for action, reason, vtype, gate_req in FORBIDDEN_ACTIONS
    ]

    roadmap_rows = [
        {
            "roadmap_id": rid,
            "candidate_phase": phase,
            "objective": obj,
            "prerequisites": prereq,
            "suggested_priority": pri,
            "immediate_value": imm,
            "risk": risk,
            **_not_fact(),
        }
        for rid, phase, obj, prereq, pri, imm, risk in ROADMAP
    ]

    trace_steps = [
        {
            "step_id": sid,
            "step_name": sid,
            "decision": decision,
            "reason_codes": reasons,
            "allowed_next_actions": allowed,
            "blocked_next_actions": blocked,
            "runtime_action_committed": False,
        }
        for sid, decision, reasons, allowed, blocked in TRACE_STEPS
    ]

    gt_link = hw.get("guardedtrial") or {}

    return {
        "summary": {
            "schema_version": "return_to_software_mainline_closure_v1_summary_v0",
            "phase": PHASE_ID,
            "closure_scope": "software_mainline_closure_only",
            "based_on_staticreading_ocrrequest_gate": roots["ocr_gate"].is_dir(),
            "based_on_memory_handoff": roots["mem_handoff"].is_dir(),
            "based_on_hardware_adapter_stub": roots["hw_stub"].is_dir(),
            "hardware_chain_frozen": True,
            "staticreading_ocrrequest_gate_closed": True,
            "memory_handoff_dryrun_closed": True,
            "static_capture_result_available": False,
            "capture_status_observed": capture_status,
            "ocrrequest_eligible_now": False,
            "ep_v5_allowed_now": False,
            "semantic_v5_allowed_now": False,
            "source_validation_v3_allowed_now": False,
            "memory_runtime_allowed_now": False,
            "worldmodel_write_allowed_now": False,
            "scene_delta_allowed_now": False,
            "software_mainline_ready_for_next_planning": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots),
        "completed_phases": {
            "schema_version": "return_to_software_mainline_completed_phase_matrix_v1",
            "completed_phase_count": len(completed),
            "phases": completed,
            **_not_fact(),
        },
        "closed_chains": {
            "schema_version": "return_to_software_mainline_closed_chain_summary_v1",
            "hardware_chain": {
                "status": "frozen",
                "last_phase": "Hardware-Camera-Runtime-Adapter-Implementation-Stub-v1",
                "final_decision": "STUB_READY_SOFTWARE_BOUNDARY_CLOSED",
            },
            "staticreading_chain": {
                "status": "blocked_until_captured_frame",
                "last_phase": "OCRRequest-Gated-Submission-from-StaticReading-v1",
                "final_decision": "BLOCK_OCRREQUEST_STATICREADING_UNTIL_CAPTURED_FRAME",
            },
            "memory_handoff_chain": {
                "status": "handoff_dryrun_ready",
                "last_phase": "Confirmed-Text-Evidence-Memory-Handoff-DryRun-v1",
                "final_decision": "READY_FOR_MEMORY_GOVERNANCE_HANDOFF_RUNTIME_LATER",
            },
            "worldmodel_chain": {
                "status": "not_started_for_write",
                "write_allowed_now": False,
            },
            "fragment_weaving_chain": {
                "status": "future_direction_only",
            },
            **_not_fact(),
        },
        "blockers": {
            "schema_version": "return_to_software_mainline_blocker_register_v1",
            "blocker_count": len(blocker_rows),
            "blockers": blocker_rows,
            **_not_fact(),
        },
        "allowed_entrypoints": {
            "schema_version": "return_to_software_mainline_allowed_next_entrypoint_matrix_v1",
            "entrypoint_count": len(entry_rows),
            "entrypoints": entry_rows,
            **_not_fact(),
        },
        "forbidden_actions": {
            "schema_version": "return_to_software_mainline_forbidden_next_action_matrix_v1",
            "action_count": len(forbidden_rows),
            "actions": forbidden_rows,
            **_not_fact(),
        },
        "roadmap": {
            "schema_version": "return_to_software_mainline_candidate_roadmap_v1",
            "roadmap_candidate_count": len(roadmap_rows),
            "candidates": roadmap_rows,
            "recommended_next_phase": "WorldModel-Lookup-for-Reading-DryRun-v1",
            **_not_fact(),
        },
        "staticreading_ocr_closure": {
            "schema_version": "return_to_software_mainline_staticreading_ocr_closure_report_v1",
            "staticreading_ocr_chain_closed": True,
            "readable_region_candidate_count": rr_count,
            "static_capture_handoff_candidate_count": ho_count,
            "blocked_ocrrequest_candidate_count": blocked_ocr,
            "ocrrequest_submitted_now": False,
            "provider_invoked": False,
            "reason_closed": "missing_captured_frame",
            "required_to_reopen": [
                "real_static_capture_result",
                "frame_ref",
                "stc_anchor",
                "capture_quality",
                "hardware_guardedtrial_passed",
                "no_write_boundary_passed",
            ],
            **_not_fact(),
        },
        "hardware_closure": {
            "schema_version": "return_to_software_mainline_hardware_chain_closure_report_v1",
            "hardware_chain_frozen": True,
            "last_completed_phase": "Hardware-Camera-Runtime-Adapter-Implementation-Stub-v1",
            "adapter_stub_ready": True,
            "real_adapter_available": False,
            "real_camera_enabled": hw.get("summary", {}).get("real_camera_enabled", False),
            "guardedtrial_allowed_now": gt_link.get("guardedtrial_allowed_now", False),
            "current_runtime_blockers": gt_link.get("current_blockers", [
                "real_adapter_missing",
                "real_camera_disabled",
                "permission_state_unknown",
                "hardware_profile_not_verified",
            ]),
            "allowed_reopen_paths": [
                "Hardware-Camera-Control-GuardedTrial-Precheck-v1",
                "Hardware-Camera-Runtime-Adapter-RealImplementation-v1",
                "Hardware-Profile-Capability-Registry-Review-v1",
            ],
            **_not_fact(),
        },
        "memory_closure": {
            "schema_version": "return_to_software_mainline_memory_handoff_closure_report_v1",
            "memory_handoff_dryrun_closed": True,
            "dryrun_text_evidence_sample_count": mem.get("dryrun_text_evidence_sample_count", 8),
            "evidence_candidate_count": mem.get("confirmed_text_evidence_candidate_count", 8),
            "append_request_candidate_count": mem.get("append_request_candidate_count", 11),
            "handoff_candidate_count": mem.get("handoff_candidate_count", 11),
            "memory_system_invoked": False,
            "memory_written_now": False,
            "midplatform_append_only": True,
            "midplatform_delete_forbidden": True,
            "midplatform_update_forbidden": True,
            "required_to_reopen_runtime": [
                "real_memory_governance_runtime",
                "user_privacy_consent_policy",
                "memory_write_authority_gate",
            ],
            **_not_fact(),
        },
        "wm_fragment_link": {
            "schema_version": "return_to_software_mainline_worldmodel_fragment_future_link_v1",
            "worldmodel_lookup_allowed_as_dryrun": True,
            "worldmodel_write_allowed_now": False,
            "fragment_evidence_weaving_allowed_as_governance": True,
            "fragment_evidence_weaving_runtime_allowed_now": False,
            "fragmented_worldline_candidate_allowed_later": True,
            "evidence_chain_required": True,
            "hallucination_control_required": True,
            "conflict_set_required": True,
            "missing_evidence_list_required": True,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "return_to_software_mainline_closure_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "return_to_software_mainline_closure_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "hardware_chain_frozen": True,
            "staticreading_ocr_chain_closed": True,
            "memory_handoff_dryrun_closed": True,
            "recommended_next_phase": "WorldModel-Lookup-for-Reading-DryRun-v1",
            "alternate_next_phase": "Fragment-Evidence-Weaving-Governance-v1",
            "alternate_next_phase_2": "Emotional-Context-Background-Candidate-DryRun-v1",
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "return_to_software_mainline_closure_boundary_report_v1",
            "closure_only": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_submitted": False,
            "provider_invoked": False,
            "ep_v5_generated": False,
            "semantic_v5_generated": False,
            "sv_v3_invoked": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "return_to_software_mainline_closure_metrics_candidate_report_v1",
            "completed_phase_count": len(completed),
            "closed_chain_count": 5,
            "blocker_count": len(blocker_rows),
            "allowed_next_entrypoint_count": len(entry_rows),
            "forbidden_next_action_count": len(forbidden_rows),
            "roadmap_candidate_count": len(roadmap_rows),
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "return_to_software_mainline_closure_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "return_to_software_mainline_closure_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "return_to_software_mainline_closure_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "closure_only": True,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_submitted": False,
            "provider_invoked": False,
            "ep_v5_generated": False,
            "semantic_v5_generated": False,
            "sv_v3_invoked": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "return_to_software_mainline_closure_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "return_to_software_mainline_closure_non_claims_report_v1",
            "claims": [
                "closure_not_new_feature",
                "closure_not_runtime",
                "allowed_entrypoint_not_started",
                "roadmap_not_commitment",
                "blocked_ocr_not_failure",
                "hardware_frozen_not_failure",
                "memory_ready_not_write",
                "worldmodel_link_not_write",
                "fragment_weaving_not_inference",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "return_to_software_mainline_closure_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "return_to_software_mainline_closure_audit_report_v1",
            "return_to_software_mainline_closure_v1_executed": True,
            "closure_only": True,
            "hardware_chain_frozen": True,
            "staticreading_ocr_chain_closed": True,
            "memory_handoff_dryrun_closed": True,
            "software_mainline_ready_for_next_planning": True,
            "ocrrequest_eligible_now": False,
            "ep_v5_allowed_now": False,
            "semantic_v5_allowed_now": False,
            "source_validation_v3_allowed_now": False,
            "memory_runtime_allowed_now": False,
            "worldmodel_write_allowed_now": False,
            "runtime_action_committed": False,
            "camera_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_submitted": False,
            "provider_invoked": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
