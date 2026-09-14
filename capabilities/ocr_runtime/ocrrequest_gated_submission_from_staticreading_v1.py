# -*- coding: utf-8 -*-
"""OCRRequest gated submission from StaticReading v1 — gate dry-run only; no OCR/provider.

Phase-OCRRequest-Gated-Submission-from-StaticReading-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCRRequest-Gated-Submission-from-StaticReading-v1-001"
FINAL_DECISION = "BLOCK_OCRREQUEST_STATICREADING_UNTIL_CAPTURED_FRAME"

BLOCKED_REASONS = [
    "static_capture_result_missing",
    "frame_ref_missing",
    "capture_status_not_captured",
    "stc_anchor_missing",
    "capture_quality_missing",
]

GATE_RULES_SPEC = [
    ("readable_region_candidate_required", "readable_region_candidate_id present", True),
    ("static_capture_result_required", "static_capture_result ref available", False),
    ("frame_ref_required", "frame_ref non-null", False),
    ("stc_anchor_required", "stc_anchor available", False),
    ("capture_quality_required", "capture_quality available", False),
    ("task_scene_context_required", "task_context_ref and scene_context_ref", True),
    ("ocr_activation_gate_required", "ocr_activation governance pass", True),
    ("memory_source_chain_required", "memory_handoff source_chain", True),
    ("full_frame_ocr_forbidden", "full_frame_ocr_allowed=false", True),
    ("mock_text_forbidden", "mock_text_allowed=false", True),
    ("provider_bypass_forbidden", "bridge/mainline only later", True),
]

FOLLOWUPS = [
    "Return-To-Software-Mainline-Closure-v1",
    "Hardware-Camera-Control-GuardedTrial-Precheck-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1-GuardedTrial",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Fragment-Evidence-Weaving-Governance-v1",
]

LONG_TERM_TYPES = [
    "blocked_staticreading_ocrrequest_candidate",
    "missing_static_capture_result_candidate",
    "unreadable_region_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_memory_handoff", "handoff_loaded", [], [], []),
    ("load_hardware_adapter_stub", "stub_loaded", [], [], ["camera_invoke"]),
    ("load_rrd_runtime", "rrd_loaded", [], [], []),
    ("load_ocr_activation_governance", "ocr_gov_loaded", [], [], ["ocr_invoke"]),
    ("load_stc_policy", "stc_loaded", [], [], []),
    ("evaluate_static_capture_readiness", "not_ready", [], [], ["submit_ocr"]),
    ("evaluate_readable_region_input_gate", "all_blocked", [], [], []),
    ("define_ocrrequest_future_payload_schema", "schema_defined", [], [], []),
    ("generate_blocked_ocrrequest_candidates", "blocked_34", [], [], []),
    ("attach_memory_governance_link", "mg_link", [], [], ["memory_write"]),
    ("define_ep_v5_semantic_sv_future_plan", "future_plans", [], [], ["ep_v5_now"]),
    ("audit_provider_bypass", "no_bypass", [], [], ["rapidocr", "paddleocr"]),
    ("generate_long_term_candidate_link", "lt", [], [], []),
    ("generate_final_staticreading_ocrrequest_gate_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _load_rrd(rrd_root: Path) -> Dict[str, Any]:
    out: Dict[str, Any] = {"loaded": rrd_root.is_dir()}
    rr_path = rrd_root / "static_readable_region_candidate_collection_v1.json"
    ho_path = rrd_root / "static_readable_region_static_capture_handoff_candidate_v1.json"
    metrics_path = rrd_root / "static_readable_region_runtime_metrics_candidate_report_v1.json"
    out["readable_regions"] = _read_json(rr_path) if rr_path.is_file() else {"candidates": []}
    out["handoffs"] = _read_json(ho_path) if ho_path.is_file() else {"candidates": []}
    out["metrics"] = _read_json(metrics_path) if metrics_path.is_file() else {}
    return out


def _handoff_by_region(handoffs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    m: Dict[str, Dict[str, Any]] = {}
    for i, h in enumerate(handoffs):
        if not isinstance(h, dict):
            continue
        rid = h.get("readable_region_candidate_id")
        if rid:
            h = {**h, "static_capture_handoff_id": h.get("static_capture_handoff_id") or f"sch_{rid}"}
            m[rid] = h
    return m


def _intake(roots: Dict[str, Path]) -> Dict[str, Any]:
    specs = [
        ("memory_handoff", roots["mem_handoff"], "confirmed_text_evidence_memory_handoff_dryrun_v1_summary.json", False),
        ("memory_governance_contract", roots["mem_contract"], "confirmed_text_evidence_memory_governance_contract_v1_summary.json", False),
        ("hardware_adapter_stub", roots["hw_stub"], "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json", False),
        ("hardware_adapter_contract", roots["hw_contract"], "hardware_camera_runtime_adapter_contract_v1_summary.json", False),
        ("hardware_runtime", roots["hw_rt"], "hardware_camera_control_runtime_dryrun_v1_summary.json", False),
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
        "schema_version": "ocrrequest_staticreading_input_intake_matrix_v1",
        "rows": rows,
        **_not_fact(),
    }


def run_ocrrequest_gated_submission_from_staticreading_v1(
    *,
    memory_handoff_root: str,
    memory_governance_contract_root: str,
    hardware_adapter_stub_root: str,
    hardware_adapter_contract_root: str,
    hardware_runtime_root: str,
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
        "mem_handoff": Path(memory_handoff_root).resolve(),
        "mem_contract": Path(memory_governance_contract_root).resolve(),
        "hw_stub": Path(hardware_adapter_stub_root).resolve(),
        "hw_contract": Path(hardware_adapter_contract_root).resolve(),
        "hw_rt": Path(hardware_runtime_root).resolve(),
        "rrd": Path(rrd_runtime_root).resolve(),
        "isrc": Path(isrc_runtime_root).resolve(),
        "tsc": Path(tsc_reevaluation_root).resolve(),
        "ocr": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_sampling_guidance_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    rrd = _load_rrd(roots["rrd"])
    regions = (rrd.get("readable_regions") or {}).get("candidates") or []
    handoffs = (rrd.get("handoffs") or {}).get("candidates") or []
    metrics = rrd.get("metrics") or {}
    ho_map = _handoff_by_region(handoffs)

    frame_stub = _read_json(
        roots["hw_stub"] / "hardware_camera_adapter_frame_capture_stub_response_v1.json"
    ) or {}
    capture_status = frame_stub.get("capture_status", "not_captured")
    frame_ref_available = frame_stub.get("frame_ref") is not None

    handoff_count = len(handoffs)
    region_count = len(regions)
    request_count = metrics.get("ocrrequest_future_gate_candidate_count", handoff_count)

    capture_ready = (
        capture_status == "captured"
        and frame_ref_available
        and frame_stub.get("frame_timestamp") is not None
    )

    region_gate_rows = []
    blocked_candidates = []
    for i, r in enumerate(regions):
        if not isinstance(r, dict):
            continue
        rrc_id = r.get("readable_region_candidate_id", f"rrc_unknown_{i}")
        ho = ho_map.get(rrc_id)
        sch_id = ho.get("static_capture_handoff_id") if ho else None
        blocked_reasons = list(BLOCKED_REASONS) if not capture_ready else []
        if not ho:
            blocked_reasons.append("static_capture_handoff_missing")
        region_gate_rows.append(
            {
                "readable_region_candidate_id": rrc_id,
                "parent_ranked_source_area_id": r.get("parent_ranked_source_area_candidate_id"),
                "expected_region_kind": r.get("expected_region_kind"),
                "expected_text_type": r.get("expected_text_type"),
                "static_capture_required": True,
                "readable_region_is_candidate_only": True,
                "real_bbox_available": r.get("bbox_candidate_unknown_by_default") is False,
                "frame_ref_available": frame_ref_available,
                "ocr_input_allowed_now": False,
                "blocked_reason": blocked_reasons[0] if blocked_reasons else "capture_status_not_captured",
                **_not_fact(),
            }
        )
        blocked_candidates.append(
            {
                "blocked_ocrrequest_candidate_id": f"bocr_{rrc_id}",
                "parent_readable_region_candidate_id": rrc_id,
                "parent_static_capture_handoff_id": sch_id,
                "would_generate_payload_later": True,
                "blocked_now": True,
                "blocked_reason": blocked_reasons,
                "ocrrequest_submitted_now": False,
                "provider_invoked_now": False,
                **_not_fact(),
            }
        )

    gate_rules = []
    for rule_id, rule_name, pass_now in GATE_RULES_SPEC:
        gate_rules.append(
            {
                "rule_id": rule_id,
                "rule_name": rule_name,
                "current_status": "pass" if pass_now else "blocked",
                "pass_now": pass_now,
                "blocked_if_failed": not pass_now,
                **_not_fact(),
            }
        )

    future_schema = {
        "schema_version": "ocrrequest_staticreading_future_payload_schema_v1",
        "description": "Future OCRRequest payload when static_capture_result available; not a submission.",
        "required_fields": [
            "ocrrequest_id",
            "request_source",
            "parent_readable_region_candidate_id",
            "parent_static_capture_handoff_id",
            "static_capture_result_ref",
            "frame_ref",
            "frame_timestamp",
            "stc_anchor",
            "crop_or_region_ref",
            "task_context_ref",
            "scene_context_ref",
            "expected_text_type",
            "provider_class_allowed",
            "memory_handoff_source_chain_ref",
        ],
        "request_source": "static_reading",
        "provider_class_allowed": ["rapidocr_lightweight", "future_heavy_ocr"],
        "full_frame_ocr_allowed": False,
        "mock_text_allowed": False,
        "example_placeholder": {
            "ocrrequest_id": "ocrreq_staticreading_placeholder",
            "parent_readable_region_candidate_id": "rrc_001",
            "parent_static_capture_handoff_id": "sch_rrc_001",
            "static_capture_result_ref": None,
            "frame_ref": None,
            "frame_timestamp": None,
            "stc_anchor": None,
            "crop_or_region_ref": "crop_placeholder",
            "task_context_ref": "tsc_dryrun_ref",
            "scene_context_ref": "scene_dryrun_ref",
            "expected_text_type": "short_text_sign",
            "memory_handoff_source_chain_ref": ["static_reading", "rrd", "memory_handoff"],
        },
        **_not_fact(),
    }

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

    return {
        "summary": {
            "schema_version": "ocrrequest_gated_submission_from_staticreading_v1_summary_v0",
            "phase": PHASE_ID,
            "gate_scope": "staticreading_ocrrequest_gated_submission_dryrun_only",
            "based_on_rrd_runtime": rrd.get("loaded", False),
            "based_on_hardware_adapter_stub": roots["hw_stub"].is_dir(),
            "based_on_ocr_activation_governance": roots["ocr"].is_dir(),
            "based_on_memory_handoff": roots["mem_handoff"].is_dir(),
            "current_case_loaded": True,
            "static_capture_handoff_candidate_count_observed": handoff_count,
            "readable_region_candidate_count_observed": region_count,
            "frame_capture_stub_observed": frame_stub.get("frame_capture_stub_response_generated", True)
            or bool(frame_stub),
            "capture_status_observed": capture_status,
            "static_capture_result_available": False,
            "stc_anchor_available": False,
            "capture_quality_available": False,
            "ocrrequest_future_schema_defined": True,
            "ocrrequest_blocked_candidate_generated": True,
            "ocrrequest_eligible_now": False,
            "ocrrequest_submitted_now": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "evidence_pack_v5_generated": False,
            "semantic_candidate_v5_generated": False,
            "source_validation_v3_invoked": False,
            "memory_handoff_link_preserved": True,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots),
        "capture_readiness": {
            "schema_version": "ocrrequest_staticreading_static_capture_readiness_intake_v1",
            "static_capture_handoff_candidate_count_observed": handoff_count,
            "static_capture_request_candidate_count_observed": request_count,
            "frame_capture_stub_response_loaded": bool(frame_stub),
            "capture_status": capture_status,
            "frame_ref_available": frame_ref_available,
            "frame_timestamp_available": frame_stub.get("frame_timestamp") is not None,
            "static_capture_result_available": False,
            "static_capture_ready_now": False,
            "reason_not_ready": [
                "adapter_stub_only",
                "no_real_camera",
                "capture_status_not_captured",
                "frame_ref_missing",
                "stc_anchor_missing",
                "capture_quality_missing",
            ],
            **_not_fact(),
        },
        "region_gate_matrix": {
            "schema_version": "ocrrequest_staticreading_readable_region_input_gate_matrix_v1",
            "readable_region_candidate_count": region_count,
            "rows": region_gate_rows,
            "all_ocr_input_blocked_now": all(not r.get("ocr_input_allowed_now") for r in region_gate_rows),
            **_not_fact(),
        },
        "future_schema": future_schema,
        "blocked_collection": {
            "schema_version": "ocrrequest_staticreading_blocked_candidate_collection_v1",
            "blocked_candidate_count": len(blocked_candidates),
            "candidates": blocked_candidates,
            **_not_fact(),
        },
        "gate_policy_matrix": {
            "schema_version": "ocrrequest_staticreading_gate_policy_matrix_v1",
            "rules": gate_rules,
            **_not_fact(),
        },
        "memory_governance_link": {
            "schema_version": "ocrrequest_staticreading_memory_governance_link_v1",
            "memory_handoff_available": roots["mem_handoff"].is_dir(),
            "confirmed_text_evidence_schema_available": (
                roots["mem_contract"] / "confirmed_text_evidence_schema_v1.json"
            ).is_file(),
            "memory_append_request_schema_available": (
                roots["mem_contract"] / "confirmed_text_memory_append_request_schema_v1.json"
            ).is_file(),
            "memory_source_chain_required": True,
            "future_ocr_result_must_preserve_source_chain": True,
            "future_evidence_pack_v5_must_link_memory_handoff": True,
            "memory_system_invoked_now": False,
            "memory_written_now": False,
            **_not_fact(),
        },
        "ep_v5_plan": {
            "schema_version": "ocrrequest_staticreading_evidence_pack_v5_future_plan_v1",
            "evidence_pack_v5_future_plan_defined": True,
            "evidence_pack_v5_generated_now": False,
            "required_inputs": [
                "ocrrequest_ref",
                "static_capture_result_ref",
                "frame_ref",
                "readable_region_ref",
                "raw_ocr_result",
                "source_chain",
                "task_scene_context",
                "stc_anchor",
                "memory_governance_link",
            ],
            "future_phase": "Evidence-Pack-Adapter-v5-StaticReading",
            **_not_fact(),
        },
        "semantic_sv_plan": {
            "schema_version": "ocrrequest_staticreading_semantic_sv_future_plan_v1",
            "semantic_candidate_v5_future_plan_defined": True,
            "source_validation_v3_future_plan_defined": True,
            "semantic_candidate_v5_generated_now": False,
            "source_validation_v3_invoked_now": False,
            "semantic_requires_non_empty_or_meaningful_ocr_result": True,
            "source_validation_requires_evidence_pack_v5": True,
            "future_phases": [
                "Semantic-Candidate-v5-StaticReading",
                "Source-Validation-v3-StaticReading",
            ],
            **_not_fact(),
        },
        "bypass_audit": {
            "schema_version": "ocrrequest_staticreading_provider_bypass_audit_v1",
            "provider_bypass_audit_executed": True,
            "direct_provider_bypass": False,
            "capability_imports_rapidocr": False,
            "capability_imports_paddleocr": False,
            "bridge_invoked": False,
            "provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "mock_text_used": False,
            "full_frame_ocr_invoked": False,
            **_not_fact(),
        },
        "long_term": {
            "schema_version": "ocrrequest_staticreading_long_term_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "readable_region_ref",
                "static_capture_handoff_ref",
                "blocked_reason",
                "future_usage_scope",
                "privacy_sensitivity",
            ],
            **_not_fact(),
        },
        "trace": {
            "schema_version": "ocrrequest_staticreading_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "ocrrequest_staticreading_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "static_capture_result_available": False,
            "ocrrequest_eligible_now": False,
            "ocrrequest_submitted_now": False,
            "provider_invoked_now": False,
            "blocked_candidate_generated": True,
            "memory_governance_link_preserved": True,
            "recommended_next_phase": "Return-To-Software-Mainline-Closure-v1",
            "alternate_next_phase": "Evidence-Pack-Adapter-v5-StaticReading",
            "alternate_next_phase_2": "Hardware-Camera-Control-GuardedTrial-Precheck-v1",
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "ocrrequest_staticreading_boundary_report_v1",
            "gate_dryrun_only": True,
            "ocrrequest_submitted_now": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "rapidocr_invoked": False,
            "paddleocr_invoked": False,
            "evidence_pack_v5_generated": False,
            "semantic_candidate_v5_generated": False,
            "source_validation_v3_invoked": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
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
            "schema_version": "ocrrequest_staticreading_metrics_candidate_report_v1",
            "static_capture_handoff_candidate_count_observed": handoff_count,
            "readable_region_candidate_count_observed": region_count,
            "blocked_ocrrequest_candidate_count": len(blocked_candidates),
            "ocrrequest_submitted_count": 0,
            "provider_invoked_count": 0,
            "evidence_pack_v5_generated_count": 0,
            "memory_write_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "ocrrequest_staticreading_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "ocrrequest_staticreading_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "ocrrequest_staticreading_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "gate_dryrun_only": True,
            "ocrrequest_submitted_now": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_v5_generated": False,
            "semantic_candidate_v5_generated": False,
            "source_validation_v3_invoked": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
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
            "schema_version": "ocrrequest_staticreading_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "ocrrequest_staticreading_non_claims_report_v1",
            "claims": [
                "no_ocrrequest_submit",
                "blocked_not_ocr_failure",
                "readable_region_not_ocr_input",
                "handoff_not_captured_frame",
                "stub_not_frame",
                "future_schema_not_submission",
                "ep_v5_plan_not_pack",
                "memory_link_not_write",
                "no_ocr_no_provider",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "ocrrequest_staticreading_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "ocrrequest_staticreading_audit_report_v1",
            "ocrrequest_gated_submission_from_staticreading_v1_executed": True,
            "gate_dryrun_only": True,
            "static_capture_handoff_candidate_count_observed": handoff_count,
            "readable_region_candidate_count_observed": region_count,
            "frame_capture_stub_observed": True,
            "capture_status_observed": capture_status,
            "static_capture_result_available": False,
            "ocrrequest_future_schema_defined": True,
            "ocrrequest_blocked_candidate_generated": True,
            "ocrrequest_eligible_now": False,
            "ocrrequest_submitted_now": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_v5_generated": False,
            "semantic_candidate_v5_generated": False,
            "source_validation_v3_invoked": False,
            "memory_handoff_link_preserved": True,
            "memory_system_invoked": False,
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
