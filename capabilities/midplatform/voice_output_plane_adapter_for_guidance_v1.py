# -*- coding: utf-8 -*-
"""Voice Output Plane Adapter for Guidance v1 — mapping + admission dry-run (no VOP/TTS/submit).

Phase-Voice-Output-Plane-Adapter-for-Guidance-v1-001

Future relocation: capabilities/voice/
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Voice-Output-Plane-Adapter-for-Guidance-v1-001"
P3 = "P3_OCR_GUIDANCE"
P0 = "P0_SAFETY_CRITICAL"
HOLD_TEXT = "请先停稳，保持画面稳定。"
FINAL_DECISION = "READY_FOR_FUTURE_VOP_SUBMIT"
ADMISSION_DECISION = "ADMIT_AS_CANDIDATE"

FOLLOWUPS = [
    "Assisted-Static-Reading-Mode-v1",
    "Voice-Output-Plane-Adapter-GuardedTrial-v1",
    "Short-Term-Guidance-Memory-Runtime-v1",
    "Speech-Priority-Arbitration-Runtime-v1",
    "Safety-Interrupt-for-Guidance-v1",
    "User-Guidance-Recovery-Runtime-GuardedTrial-v1",
    "Vision-Capture-Runtime-GuardedTrial-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

MAPPING_ROWS = [
    ("prompt_text", "speech_text", "identity", "non_empty_string"),
    ("priority_level", "priority", "identity", "must_be_P3_for_ocr_guidance"),
    ("guidance_session_id", "session_id", "identity", "non_empty"),
    ("task_context_id", "task_context_id", "identity", "non_empty"),
    ("safety_interruptible", "safety_interruptible", "identity", "must_be_true"),
    ("repeat_policy_ref", "repeat_policy_ref", "identity", "path_ref"),
    ("short_term_memory_ref", "short_term_memory_ref", "identity", "path_ref"),
    ("speech_gate_required", "speech_gate_required", "constant_true", "must_be_true"),
    ("voice_output_plane_required", "voice_output_plane_required", "constant_true", "must_be_true"),
]

OPTIONAL_VOP_PATHS = [
    ("voice_output_plane_runtime", "capabilities/voice/voice_output_plane.py"),
    ("speech_request_schema", "docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md"),
    ("speech_gate_runtime", "docs/architecture/LUNA_VOICE_OUTPUT_GUARD_GATE_ALIGNMENT_REVIEW_V0.md"),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake_matrix(
    *,
    vg_runtime: Path,
    vg_template: Path,
    ug_rt: Path,
    vc_rt: Path,
    bench: Path,
    health: Path,
    sim: Path,
    ws_root: Path,
) -> Dict[str, Any]:
    required = [
        ("vg_runtime", vg_runtime, "voice_guidance_prompt_runtime_dryrun_v1_summary.json", False),
        ("vg_template", vg_template, "voice_guidance_prompt_template_v1_summary.json", False),
        ("ug_runtime", ug_rt, "user_guidance_recovery_runtime_dryrun_v1_summary.json", False),
        ("vc_runtime", vc_rt, "vision_capture_runtime_dryrun_v1_summary.json", False),
        ("benchmark_smoke", bench, None, False),
        ("system_health", health, None, False),
        ("simulation", sim, None, False),
    ]
    rows: List[Dict[str, Any]] = []
    for iid, root, artifact, optional in required:
        loaded = root.is_dir()
        if artifact:
            loaded = loaded and (root / artifact).is_file()
        rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": artifact or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else "missing_required",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    sr = _read_json(vg_runtime / "voice_guidance_runtime_speech_request_candidate_v1.json")
    if sr:
        rows.append(
            {
                "intake_id": "speech_request_candidate",
                "input_source": "vg_runtime",
                "source_root_or_path": str(vg_runtime),
                "artifact": "voice_guidance_runtime_speech_request_candidate_v1.json",
                "loaded": True,
                "optional": False,
                "key_fields_observed": ["prompt_text", "priority_level", "speech_gate_required"],
                "intake_status": "loaded",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    for opt_id, rel in OPTIONAL_VOP_PATHS:
        p = ws_root / rel
        rows.append(
            {
                "intake_id": opt_id,
                "input_source": "optional_voice_runtime",
                "source_root_or_path": str(p),
                "artifact": rel,
                "loaded": p.is_file(),
                "optional": True,
                "key_fields_observed": [],
                "intake_status": "loaded" if p.is_file() else "optional_missing",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {
        "schema_version": "voice_output_plane_adapter_input_intake_matrix_v1",
        "rows": rows,
        "all_required_loaded": all(r["loaded"] for r in rows if not r["optional"]),
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _mapping_contract() -> Dict[str, Any]:
    mappings = []
    for src, tgt, rule, validation in MAPPING_ROWS:
        mappings.append(
            {
                "source_field": src,
                "target_field": tgt,
                "required": True,
                "preserved": rule in ("identity", "constant_true"),
                "transform_rule": rule,
                "validation_rule": validation,
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": "voice_output_plane_adapter_mapping_contract_v1",
        "description": "prompt_candidate / speech_request_candidate → SpeechRequest payload for future VOP",
        "mappings": mappings,
        "direct_tts_bypass_forbidden": True,
        "direct_vop_bypass_forbidden": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_voice_output_plane_adapter_for_guidance_v1(
    *,
    voice_guidance_runtime_root: str,
    voice_guidance_template_root: str,
    user_guidance_runtime_root: str,
    vision_capture_runtime_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or Path(__file__).resolve().parents[2])
    vg_rt = Path(voice_guidance_runtime_root).resolve()
    vg_tpl = Path(voice_guidance_template_root).resolve()
    ug_rt = Path(user_guidance_runtime_root).resolve()
    vc_rt = Path(vision_capture_runtime_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    sr_cand = _read_json(vg_rt / "voice_guidance_runtime_speech_request_candidate_v1.json") or {}
    stm = _read_json(vg_rt / "voice_guidance_runtime_stm_mount_candidate_v1.json") or {}
    gate_rt = _read_json(vg_rt / "voice_guidance_runtime_speech_gate_pre_submit_dryrun_v1.json") or {}
    final_rt = _read_json(vg_rt / "voice_guidance_runtime_final_decision_v1.json") or {}
    cooldown_tpl = _read_json(vg_tpl / "voice_guidance_cooldown_repetition_policy_v1.json") or {}

    prompt_text = sr_cand.get("prompt_text", HOLD_TEXT)
    session_id = sr_cand.get("guidance_session_id", "vg_sess_placeholder")
    task_ctx = sr_cand.get("task_context_id", "vg_ctx_placeholder")
    repeat_ref = sr_cand.get("repeat_policy_ref", "voice_guidance_repeat_on_user_inquiry_policy_v1.json")
    stm_ref = sr_cand.get("short_term_memory_ref", "voice_guidance_runtime_stm_mount_candidate_v1.json")
    cooldown_ref = "voice_guidance_cooldown_repetition_policy_v1.json"

    intake = _intake_matrix(
        vg_runtime=vg_rt,
        vg_template=vg_tpl,
        ug_rt=ug_rt,
        vc_rt=vc_rt,
        bench=bench,
        health=health,
        sim=sim,
        ws_root=ws,
    )
    mapping = _mapping_contract()

    adapter_payload = {
        "schema_version": "voice_output_plane_adapter_payload_candidate_v1",
        "adapter_payload_candidate_generated": True,
        "prompt_text": prompt_text,
        "priority": P3,
        "prompt_type": "ocr_guidance",
        "guidance_action": "hold_still",
        "session_id_placeholder": session_id,
        "task_context_id_placeholder": task_ctx,
        "safety_interruptible": True,
        "repeat_policy_ref": repeat_ref,
        "short_term_memory_ref": stm_ref,
        "cooldown_policy_ref": cooldown_ref,
        "speech_gate_required": True,
        "voice_output_plane_required": True,
        "direct_tts_bypass_forbidden": True,
        "direct_vop_bypass_forbidden": True,
        "adapter_invoked_now": False,
        "source_runtime_final_decision": final_rt.get("final_decision"),
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    speech_payload = {
        "schema_version": "voice_output_plane_speech_request_payload_candidate_v1",
        "speech_request_payload_candidate_generated": True,
        "speech_request_schema_version": "speech_request_payload_v1_guidance_adapter_dryrun",
        "speech_text": prompt_text,
        "priority": P3,
        "source_module": "voice_guidance_prompt",
        "reason_code": "assisted_static_capture_guidance",
        "safety_interruptible": True,
        "can_be_interrupted_by": [P0, "P1_NAVIGATION_CRITICAL", "P2_TASK_CRITICAL"],
        "repeat_policy_ref": repeat_ref,
        "short_term_memory_ref": stm_ref,
        "cooldown_policy_ref": cooldown_ref,
        "session_id": session_id,
        "task_context_id": task_ctx,
        "speech_gate_required": True,
        "voice_output_plane_required": True,
        "direct_tts_bypass_forbidden": True,
        "direct_vop_bypass_forbidden": True,
        "submitted_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    admission = {
        "schema_version": "voice_output_plane_speech_gate_admission_dryrun_v1",
        "admission_dryrun_executed": True,
        "speech_request_payload_present": speech_payload.get("speech_request_payload_candidate_generated"),
        "priority_valid": speech_payload.get("priority") == P3,
        "safety_interruptible_valid": speech_payload.get("safety_interruptible") is True,
        "cooldown_policy_ref_present": bool(cooldown_ref),
        "short_term_memory_ref_present": bool(stm_ref),
        "repeat_policy_ref_present": bool(repeat_ref),
        "direct_tts_bypass_detected": False,
        "direct_vop_bypass_detected": False,
        "prior_speech_gate_pre_submit_passed": gate_rt.get("submit_allowed_later") is True,
        "admission_decision": ADMISSION_DECISION,
        "submitted_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    vop_path = ws / OPTIONAL_VOP_PATHS[0][1]
    vop_submit = {
        "schema_version": "voice_output_plane_submit_dryrun_v1",
        "submit_dryrun_executed": True,
        "voice_output_plane_available": vop_path.is_file(),
        "voice_output_plane_optional_missing_allowed": True,
        "submit_allowed_later": admission.get("admission_decision") == ADMISSION_DECISION,
        "voice_output_plane_invoked_now": False,
        "speech_request_submitted_now": False,
        "tts_invoked_now": False,
        "dryrun_decision": FINAL_DECISION,
        "adapter_trace": [
            "intake_loaded",
            "mapping_contract_applied",
            "adapter_payload_built",
            "speech_request_payload_built",
            "speech_gate_admission_dryrun_pass",
            "vop_submit_deferred",
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    safety_matrix = {
        "schema_version": "voice_output_plane_guidance_safety_interruptibility_matrix_v1",
        "incoming_priority": P3,
        "can_be_interrupted_by_p0": True,
        "can_be_interrupted_by_p1": True,
        "can_be_interrupted_by_p2": True,
        "cannot_interrupt_p0": True,
        "cannot_interrupt_p1": True,
        "cannot_interrupt_p2": True,
        "suppress_when_safety_active": True,
        "runtime_interrupt_applied_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    stm_repeat = {
        "schema_version": "voice_output_plane_stm_repeat_reference_preservation_report_v1",
        "short_term_memory_ref_preserved": stm_ref == sr_cand.get("short_term_memory_ref"),
        "repeat_policy_ref_preserved": repeat_ref == sr_cand.get("repeat_policy_ref"),
        "memory_scope": stm.get("memory_scope", "short_term_only"),
        "write_to_runtime_memory_now": False,
        "write_to_long_term_memory_now": False,
        "repeat_allowed_on_user_inquiry": True,
        "cooldown_policy_ref_preserved": True,
        "cooldown_policy_ref": cooldown_ref,
        "stm_fields_observed": list((stm.get("fields") or {}).keys())[:5],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    final = {
        "schema_version": "voice_output_plane_adapter_final_dryrun_decision_v1",
        "final_decision": FINAL_DECISION,
        "speech_request_payload_candidate_generated": True,
        "speech_gate_admission_decision": ADMISSION_DECISION,
        "voice_output_plane_invoked_now": False,
        "speech_request_submitted_now": False,
        "tts_invoked_now": False,
        "selected_prompt_text": prompt_text,
        "selected_priority": P3,
        "recommended_next_phase": "Assisted-Static-Reading-Mode-v1",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "voice_output_plane_adapter_for_guidance_v1_summary_v0",
            "phase": PHASE_ID,
            "adapter_scope": "voice_output_plane_adapter_dryrun_only",
            "capability_location": "capabilities/midplatform/voice_output_plane_adapter_for_guidance_v1.py",
            "future_relocation": "capabilities/voice/",
            "based_on_voice_guidance_prompt_runtime": vg_rt.is_dir(),
            "current_case_loaded": True,
            "speech_request_candidate_observed": sr_cand.get("speech_request_candidate_generated") is True,
            "adapter_payload_candidate_generated": True,
            "speech_request_payload_candidate_generated": True,
            "speech_gate_admission_dryrun_executed": True,
            "voice_output_plane_submit_dryrun_executed": True,
            "selected_prompt_text": prompt_text,
            "selected_priority": P3,
            "safety_interruptible": True,
            "speech_gate_required": True,
            "direct_tts_bypass_forbidden": True,
            "direct_vop_bypass_forbidden": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "long_term_memory_written": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": intake,
        "mapping": mapping,
        "adapter_payload": adapter_payload,
        "speech_payload": speech_payload,
        "admission": admission,
        "vop_submit": vop_submit,
        "safety_matrix": safety_matrix,
        "stm_repeat": stm_repeat,
        "final": final,
        "boundary": {
            "schema_version": "voice_output_plane_adapter_boundary_report_v1",
            "adapter_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "long_term_memory_written": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "voice_output_plane_adapter_metrics_candidate_report_v1",
            "adapter_payload_candidate_generated": True,
            "speech_request_payload_candidate_generated": True,
            "speech_gate_admission_dryrun_executed": True,
            "voice_output_plane_submit_dryrun_executed": True,
            "runtime_tts_invoked_count": 0,
            "voice_output_plane_invoked_count": 0,
            "speech_request_submitted_count": 0,
            "short_term_memory_written_count": 0,
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "voice_output_plane_adapter_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "voice_output_plane_adapter_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "voice_output_plane_adapter_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "adapter_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "long_term_memory_written": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "voice_output_plane_adapter_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "voice_output_plane_adapter_non_claims_report_v1",
            "claims": [
                "no_vop_invoke",
                "no_speech_request_submit",
                "no_tts",
                "adapter_payload_not_runtime_submit",
                "speech_payload_not_submitted_request",
                "admission_dryrun_not_real_gate",
                "stm_ref_preservation_not_stm_write",
                "no_user_guidance_action",
                "no_ocr",
                "no_world_model",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "voice_output_plane_adapter_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "voice_output_plane_adapter_audit_report_v1",
            "voice_output_plane_adapter_for_guidance_v1_executed": True,
            "adapter_dryrun_only": True,
            "adapter_payload_candidate_generated": True,
            "speech_request_payload_candidate_generated": True,
            "speech_gate_admission_dryrun_executed": True,
            "voice_output_plane_submit_dryrun_executed": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "long_term_memory_written": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "scene_delta_candidate_generated": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
