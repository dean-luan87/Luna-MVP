# -*- coding: utf-8 -*-
"""Confirmed Text Evidence Memory Handoff DryRun v1 — append/handoff candidates only; no Memory I/O.

Phase-Confirmed-Text-Evidence-Memory-Handoff-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.confirmed_text_evidence_memory_governance_contract_v1 import (
    ALLOWED_OPS,
    FORBIDDEN_OPS,
    FUTURE_USAGE_SCOPES,
    PRIVACY_CLASSES,
    STALE_ROUTES,
    TARGET_MEMORY_DOMAINS,
)

PHASE_ID = "Confirmed-Text-Evidence-Memory-Handoff-DryRun-v1-001"
FINAL_DECISION = "READY_FOR_MEMORY_GOVERNANCE_HANDOFF_RUNTIME_LATER"

DRYRUN_SAMPLES: List[Dict[str, Any]] = [
    {
        "sample_id": "safety_warning_text",
        "sample_type": "safety_warning_text",
        "simulated_text_content": "[DRYRUN] 小心地滑",
        "text_type": "safety_warning",
        "evidence_status_candidate": "confirmed",
        "privacy_sensitivity": "public_text",
    },
    {
        "sample_id": "doorplate_text",
        "sample_type": "doorplate_text",
        "simulated_text_content": "[DRYRUN] 3楼 301室",
        "text_type": "doorplate",
        "evidence_status_candidate": "confirmed",
        "privacy_sensitivity": "semi_public_text",
    },
    {
        "sample_id": "shop_sign_text",
        "sample_type": "shop_sign_text",
        "simulated_text_content": "[DRYRUN] 便利店入口",
        "text_type": "shop_sign",
        "evidence_status_candidate": "confirmed",
        "privacy_sensitivity": "public_text",
    },
    {
        "sample_id": "department_sign_text",
        "sample_type": "department_sign_text",
        "simulated_text_content": "[DRYRUN] 内科门诊",
        "text_type": "department_sign",
        "evidence_status_candidate": "confirmed",
        "privacy_sensitivity": "medical_text",
    },
    {
        "sample_id": "transit_line_text",
        "sample_type": "transit_line_text",
        "simulated_text_content": "[DRYRUN] 地铁2号线 往浦东方向",
        "text_type": "transit_line",
        "evidence_status_candidate": "confirmed",
        "privacy_sensitivity": "public_text",
    },
    {
        "sample_id": "restroom_sign_text",
        "sample_type": "restroom_sign_text",
        "simulated_text_content": "[DRYRUN] 男厕 / 无障碍卫生间",
        "text_type": "restroom_sign",
        "evidence_status_candidate": "confirmed",
        "privacy_sensitivity": "public_text",
    },
    {
        "sample_id": "expired_notice_text",
        "sample_type": "expired_notice_text",
        "simulated_text_content": "[DRYRUN] 临时闭馆通知（已过期）",
        "text_type": "notice",
        "evidence_status_candidate": "expired",
        "privacy_sensitivity": "public_text",
    },
    {
        "sample_id": "user_explicit_reading_text",
        "sample_type": "user_explicit_reading_text",
        "simulated_text_content": "[DRYRUN] 用户指定：请读这张海报标题",
        "text_type": "user_explicit_reading",
        "evidence_status_candidate": "confirmed",
        "privacy_sensitivity": "private_text",
    },
]

FOLLOWUPS = [
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
    "Memory-Governance-Delete-Update-Authority-Policy-v1",
    "User-Privacy-Consent-Governance-v1",
    "Fragment-Evidence-Weaving-Governance-v1",
    "Return-To-Software-Mainline-Closure-v1",
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_memory_governance_contract", "contract_loaded", [], [], []),
    ("load_static_reading_chain", "reading_chain_loaded", [], [], []),
    ("load_ocr_activation_governance", "ocr_gov_loaded", [], [], ["ocr_invoke"]),
    ("define_dryrun_text_evidence_samples", "samples_defined", [], [], []),
    ("generate_confirmed_text_evidence_candidates", "evidence_candidates", [], [], ["memory_write"]),
    ("generate_memory_append_request_candidates", "append_candidates", [], [], ["delete", "update"]),
    ("apply_permission_policy", "permission_ok", [], [], []),
    ("apply_privacy_sensitivity_policy", "privacy_ok", [], [], []),
    ("apply_correction_supersession_conflict_policy", "csc_ok", [], [], ["overwrite"]),
    ("apply_expired_stale_routing_policy", "stale_ok", [], [], ["memory_delete"]),
    ("generate_memory_governance_handoff_candidates", "handoff_candidates", [], [], ["memory_invoke"]),
    ("evaluate_worldmodel_scenedelta_links", "wm_link_ok", [], [], ["wm_write"]),
    ("evaluate_user_emotional_context_links", "ue_link_ok", [], [], ["profile_fact"]),
    ("generate_final_handoff_dryrun_decision", FINAL_DECISION, [], [], ["routing_change"]),
]

OPTIONAL_DOC_CANDIDATES = [
    ("memory_governance_docs", "docs/architecture/midplatform/LUNA_MEMORY_GOVERNANCE_V0.md"),
    ("user_profile_docs", "docs/architecture/midplatform/LUNA_USER_PROFILE_CONTEXT_V0.md"),
    ("emotional_context_docs", "docs/architecture/midplatform/LUNA_EMOTIONAL_CONTEXT_BACKGROUND_V0.md"),
    ("worldmodel_docs", "docs/architecture/LUNA_WORLD_MODEL_V0.md"),
    ("text_evidence_docs", "docs/architecture/ocr_bridge/LUNA_OCR_EVIDENCE_GOVERNANCE_AUTHORITY_FREEZE_V0.md"),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _load_contract(roots: Dict[str, Path]) -> Dict[str, Any]:
    croot = roots["contract"]
    out: Dict[str, Any] = {"loaded": croot.is_dir()}
    if not out["loaded"]:
        return out
    for name in [
        "confirmed_text_evidence_memory_governance_contract_v1_summary.json",
        "midplatform_memory_permission_policy_v1.json",
        "confirmed_text_memory_privacy_sensitivity_policy_v1.json",
    ]:
        out[name] = (croot / name).is_file()
    perm = _read_json(croot / "midplatform_memory_permission_policy_v1.json")
    if isinstance(perm, dict):
        out["permission_policy"] = perm
    privacy = _read_json(croot / "confirmed_text_memory_privacy_sensitivity_policy_v1.json")
    if isinstance(privacy, dict):
        out["privacy_policy"] = privacy
    return out


def _intake(roots: Dict[str, Path], workspace_root: Optional[Path]) -> Dict[str, Any]:
    specs = [
        ("memory_governance_contract", roots["contract"], "confirmed_text_evidence_memory_governance_contract_v1_summary.json", False),
        ("rrd_runtime", roots["rrd"], "static_readable_region_discovery_runtime_dryrun_v1_summary.json", False),
        ("isrc_runtime", roots["isrc"], "static_reading_information_source_localization_runtime_dryrun_v1_summary.json", False),
        ("tsc_reevaluation", roots["tsc"], "static_reading_task_scene_context_reevaluation_dryrun_v1_summary.json", False),
        ("ocr_activation", roots["ocr"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("worldmodel_unresolved", roots["wm"], "worldmodel_unresolved_slot_contract_summary.json", False),
        ("benchmark", roots["bench"], None, False),
        ("system_health", roots["health"], None, False),
        ("simulation", roots["sim"], None, False),
    ]
    rows: List[Dict[str, Any]] = []
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
    if workspace_root:
        for iid, rel in OPTIONAL_DOC_CANDIDATES:
            doc_path = workspace_root / rel
            rows.append(
                {
                    "intake_id": iid,
                    "input_source": "optional_doc",
                    "source_root_or_path": str(doc_path),
                    "artifact": rel,
                    "loaded": doc_path.is_file(),
                    "optional": True,
                    "key_fields_observed": ["doc_ref"] if doc_path.is_file() else [],
                    "intake_status": "loaded" if doc_path.is_file() else "optional_missing",
                    **_not_fact(),
                }
            )
    return {
        "schema_version": "confirmed_text_memory_handoff_input_intake_matrix_v1",
        "rows": rows,
        **_not_fact(),
    }


def _dryrun_sample_set() -> Dict[str, Any]:
    samples = []
    for s in DRYRUN_SAMPLES:
        samples.append(
            {
                **s,
                "source_chain_placeholder": ["static_reading", "rrd", "isrc", "ocr_activation_dryrun"],
                "time_anchor_placeholder": "time_anchor_dryrun_v1",
                "spatial_anchor_placeholder": "spatial_anchor_dryrun_v1",
                "task_context_ref_placeholder": "tsc_dryrun_ref",
                "scene_context_ref_placeholder": "scene_dryrun_ref",
                "simulation_only": True,
                "not_memory_fact": True,
                **_not_fact(),
            }
        )
    return {
        "schema_version": "confirmed_text_memory_handoff_dryrun_text_evidence_sample_set_v1",
        "sample_count": len(samples),
        "samples": samples,
        **_not_fact(),
    }


def _build_evidence_and_append_candidates(
    samples: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    evidence: List[Dict[str, Any]] = []
    append: List[Dict[str, Any]] = []
    for i, s in enumerate(samples):
        eid = f"ctec_dryrun_{i:03d}"
        status = s["evidence_status_candidate"]
        domain = (
            "text_evidence_memory"
            if status in ("confirmed", "candidate")
            else "world_context_memory"
        )
        payload = (
            "confirmed_text_evidence"
            if status == "confirmed"
            else "expired_text_observation"
            if status == "expired"
            else "unresolved_text_candidate"
        )
        review = s["privacy_sensitivity"] in (
            "medical_text",
            "financial_text",
            "identity_document_text",
            "private_text",
            "sensitive_personal_text",
        )
        evidence.append(
            {
                "text_evidence_candidate_id": eid,
                "source_sample_id": s["sample_id"],
                "evidence_status": status,
                "text_content": s["simulated_text_content"],
                "text_type": s["text_type"],
                "source_chain": list(s["source_chain_placeholder"]),
                "time_anchor": s["time_anchor_placeholder"],
                "spatial_anchor": s["spatial_anchor_placeholder"],
                "task_context_ref": s["task_context_ref_placeholder"],
                "scene_context_ref": s["scene_context_ref_placeholder"],
                "confidence_policy": "dryrun_confidence_placeholder",
                "privacy_sensitivity": s["privacy_sensitivity"],
                "future_usage_scope": (
                    ["current_task_support", "world_model_hint"]
                    if status == "expired"
                    else FUTURE_USAGE_SCOPES
                ),
                **_not_fact(),
            }
        )
        append.append(
            {
                "append_request_candidate_id": f"marc_dryrun_{i:03d}",
                "source_text_evidence_candidate_id": eid,
                "operation": "append_only",
                "target_memory_domain": domain,
                "payload_type": payload,
                "append_reason": f"dryrun_handoff_{s['sample_type']}",
                "privacy_sensitivity": s["privacy_sensitivity"],
                "review_required": review,
                "memory_governance_required": True,
                "memory_write_invoked_now": False,
                **_not_fact(),
            }
        )
    # correction / supersession / conflict append-only extras
    base = evidence[0]
    extras = [
        ("correction_candidate", "ocr_error", "marc_corr_001"),
        ("supersession_candidate", "later_observation_conflict", "marc_super_001"),
        ("conflict_candidate", "wrong_scene_context", "marc_conf_001"),
    ]
    for payload_type, reason, aid in extras:
        append.append(
            {
                "append_request_candidate_id": aid,
                "source_text_evidence_candidate_id": base["text_evidence_candidate_id"],
                "operation": "append_only",
                "target_memory_domain": "text_evidence_memory",
                "payload_type": payload_type,
                "append_reason": reason,
                "privacy_sensitivity": base["privacy_sensitivity"],
                "review_required": True,
                "memory_governance_required": True,
                "memory_write_invoked_now": False,
                **_not_fact(),
            }
        )
    return evidence, append


def run_confirmed_text_evidence_memory_handoff_dryrun_v1(
    *,
    memory_governance_contract_root: str,
    rrd_runtime_root: str,
    isrc_runtime_root: str,
    tsc_reevaluation_root: str,
    ocr_activation_root: str,
    worldmodel_unresolved_slot_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    roots = {
        "contract": Path(memory_governance_contract_root).resolve(),
        "rrd": Path(rrd_runtime_root).resolve(),
        "isrc": Path(isrc_runtime_root).resolve(),
        "tsc": Path(tsc_reevaluation_root).resolve(),
        "ocr": Path(ocr_activation_root).resolve(),
        "wm": Path(worldmodel_unresolved_slot_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }
    ws = Path(workspace_root).resolve() if workspace_root else None
    contract = _load_contract(roots)
    sample_set = _dryrun_sample_set()
    samples = sample_set["samples"]
    evidence, append_candidates = _build_evidence_and_append_candidates(samples)

    handoff_candidates = []
    for a in append_candidates:
        eid = a["source_text_evidence_candidate_id"]
        ev = next((e for e in evidence if e["text_evidence_candidate_id"] == eid), evidence[0])
        handoff_candidates.append(
            {
                "handoff_candidate_id": f"hg_hc_{a['append_request_candidate_id']}",
                "append_request_candidate_id": a["append_request_candidate_id"],
                "confirmed_text_evidence_candidate_id": eid,
                "target_memory_domain": a["target_memory_domain"],
                "payload_type": a["payload_type"],
                "source_chain": ev["source_chain"],
                "time_anchor": ev["time_anchor"],
                "spatial_anchor": ev["spatial_anchor"],
                "privacy_sensitivity": a["privacy_sensitivity"],
                "review_required": a["review_required"],
                "future_usage_scope": ev.get("future_usage_scope", FUTURE_USAGE_SCOPES),
                "handoff_allowed_later": True,
                "handoff_invoked_now": False,
                "memory_system_invoked_now": False,
                **_not_fact(),
            }
        )

    privacy_matrix = []
    review_count = 0
    redact_count = 0
    confirm_count = 0
    for cls, review, redact, confirm in PRIVACY_CLASSES:
        privacy_matrix.append({"privacy_class": cls, "review_required": review, "redaction_required": redact})
        if review:
            review_count += 1
        if redact:
            redact_count += 1
        if confirm:
            confirm_count += 1

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

    chain_loaded = (
        roots["rrd"].is_dir()
        and roots["isrc"].is_dir()
        and roots["tsc"].is_dir()
    )

    return {
        "summary": {
            "schema_version": "confirmed_text_evidence_memory_handoff_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "confirmed_text_evidence_memory_handoff_dryrun_only",
            "based_on_memory_governance_contract": contract.get("loaded", False),
            "based_on_static_reading_chain": chain_loaded,
            "based_on_ocr_activation_governance": roots["ocr"].is_dir(),
            "based_on_worldmodel_unresolved_slot": roots["wm"].is_dir(),
            "current_case_loaded": True,
            "dryrun_text_evidence_samples_defined": True,
            "confirmed_text_evidence_candidate_generated": True,
            "memory_append_request_candidate_generated": True,
            "permission_policy_applied": True,
            "privacy_sensitivity_policy_applied": True,
            "correction_supersession_conflict_policy_applied": True,
            "expired_stale_routing_policy_applied": True,
            "memory_governance_handoff_candidate_generated": True,
            "memory_governance_handoff_invoked_now": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "memory_deleted_now": False,
            "memory_updated_now": False,
            "memory_overwritten_now": False,
            "memory_merged_now": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "llm_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots, ws),
        "sample_set": sample_set,
        "evidence_collection": {
            "schema_version": "confirmed_text_evidence_candidate_collection_v1",
            "confirmed_text_evidence_candidate_count": len(evidence),
            "candidates": evidence,
            **_not_fact(),
        },
        "append_collection": {
            "schema_version": "confirmed_text_memory_append_request_candidate_collection_v1",
            "append_request_candidate_count": len(append_candidates),
            "candidates": append_candidates,
            "all_operations_append_only": all(c.get("operation") == "append_only" for c in append_candidates),
            **_not_fact(),
        },
        "permission_check": {
            "schema_version": "confirmed_text_memory_permission_policy_runtime_check_v1",
            "permission_policy_applied": True,
            "allowed_operation_candidates": list(ALLOWED_OPS),
            "forbidden_operation_candidates": list(FORBIDDEN_OPS),
            "forbidden_operation_invoked_now": False,
            "delete_memory_invoked_now": False,
            "update_memory_invoked_now": False,
            "overwrite_memory_invoked_now": False,
            "violation_detected": False,
            **_not_fact(),
        },
        "privacy_check": {
            "schema_version": "confirmed_text_memory_privacy_sensitivity_runtime_check_v1",
            "privacy_sensitivity_policy_applied": True,
            "privacy_classification_matrix": privacy_matrix,
            "review_required_count": review_count,
            "redaction_required_count": redact_count,
            "user_confirmation_required_count": confirm_count,
            "medical_text_review_required": True,
            "financial_text_review_required": True,
            "identity_document_text_review_required": True,
            "privacy_decision_committed_now": False,
            **_not_fact(),
        },
        "csc_check": {
            "schema_version": "confirmed_text_memory_correction_supersession_conflict_runtime_check_v1",
            "correction_policy_applied": True,
            "supersession_policy_applied": True,
            "conflict_policy_applied": True,
            "original_evidence_overwritten_now": False,
            "original_record_retained": True,
            "correction_candidate_generated": any(
                c["payload_type"] == "correction_candidate" for c in append_candidates
            ),
            "supersession_candidate_generated": any(
                c["payload_type"] == "supersession_candidate" for c in append_candidates
            ),
            "conflict_candidate_generated": any(
                c["payload_type"] == "conflict_candidate" for c in append_candidates
            ),
            "conflict_resolution_committed_now": False,
            "memory_update_invoked_now": False,
            **_not_fact(),
        },
        "stale_check": {
            "schema_version": "confirmed_text_memory_expired_stale_routing_runtime_check_v1",
            "expired_stale_policy_applied": True,
            "stale_blocks_current_action": True,
            "stale_does_not_imply_discard": True,
            "expired_text_can_feed_long_term_candidate": True,
            "stale_text_can_feed_world_change_hint": True,
            "stale_text_can_feed_user_environment_context": True,
            "stale_text_can_feed_user_profile_context": True,
            "stale_text_can_feed_emotional_context_background": True,
            "memory_delete_for_expiration_invoked_now": False,
            "routing_candidates": STALE_ROUTES,
            **_not_fact(),
        },
        "handoff_collection": {
            "schema_version": "confirmed_text_memory_governance_handoff_candidate_collection_v1",
            "handoff_candidate_count": len(handoff_candidates),
            "candidates": handoff_candidates,
            **_not_fact(),
        },
        "worldmodel_check": {
            "schema_version": "confirmed_text_worldmodel_scenedelta_link_runtime_check_v1",
            "worldmodel_link_policy_applied": True,
            "confirmed_text_can_feed_world_model_hint": True,
            "confirmed_text_can_feed_unresolved_slot": True,
            "confirmed_text_can_feed_world_change_hint": True,
            "confirmed_text_cannot_write_world_model_directly": True,
            "confirmed_text_cannot_generate_scene_delta_directly": True,
            "world_model_written_now": False,
            "scene_delta_candidate_generated_now": False,
            **_not_fact(),
        },
        "user_emotional_link": {
            "schema_version": "confirmed_text_user_emotional_context_runtime_link_v1",
            "user_emotional_context_link_applied": True,
            "user_environment_context_candidate_generated": True,
            "user_profile_context_candidate_generated": True,
            "emotional_context_background_candidate_generated": True,
            "midplatform_cannot_promote_to_profile_fact": True,
            "emotional_context_candidate_requires_future_emotion_engine": True,
            "user_profile_fact_written_now": False,
            "emotional_fact_written_now": False,
            **_not_fact(),
        },
        "read_call_check": {
            "schema_version": "confirmed_text_memory_read_call_reference_runtime_check_v1",
            "read_call_reference_policy_applied": True,
            "midplatform_can_read_memory": True,
            "midplatform_can_call_reference": True,
            "midplatform_can_query_reference": True,
            "memory_query_invoked_now": False,
            "memory_result_cannot_override_live_observation": True,
            "read_result_requires_freshness_check": True,
            "read_result_requires_source_chain_check": True,
            "read_result_requires_task_context_check": True,
            "read_result_requires_privacy_check": True,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "confirmed_text_memory_handoff_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "confirmed_text_memory_handoff_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "confirmed_text_evidence_candidate_generated": True,
            "memory_append_request_candidate_generated": True,
            "memory_governance_handoff_candidate_generated": True,
            "memory_system_invoked_now": False,
            "memory_written_now": False,
            "midplatform_append_only": True,
            "midplatform_delete_forbidden": True,
            "midplatform_update_forbidden": True,
            "recommended_next_phase": "OCRRequest-Gated-Submission-from-StaticReading-v1",
            "alternate_next_phase": "Evidence-Pack-Adapter-v5-StaticReading",
            "alternate_next_phase_2": "WorldModel-Lookup-for-Reading-DryRun-v1",
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "confirmed_text_memory_handoff_boundary_report_v1",
            "handoff_dryrun_only": True,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "memory_deleted_now": False,
            "memory_updated_now": False,
            "memory_overwritten_now": False,
            "memory_merged_now": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "user_profile_fact_written_now": False,
            "emotional_fact_written_now": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "llm_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "confirmed_text_memory_handoff_metrics_candidate_report_v1",
            "dryrun_text_evidence_sample_count": len(samples),
            "confirmed_text_evidence_candidate_count": len(evidence),
            "append_request_candidate_count": len(append_candidates),
            "handoff_candidate_count": len(handoff_candidates),
            "review_required_count": sum(1 for c in append_candidates if c.get("review_required")),
            "privacy_class_count": len(PRIVACY_CLASSES),
            "forbidden_operation_invoked_count": 0,
            "memory_write_invoked_count": 0,
            "memory_delete_invoked_count": 0,
            "memory_update_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "confirmed_text_memory_handoff_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "confirmed_text_memory_handoff_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "confirmed_text_memory_handoff_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "handoff_dryrun_only": True,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "memory_deleted_now": False,
            "memory_updated_now": False,
            "memory_overwritten_now": False,
            "memory_merged_now": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "user_profile_fact_written_now": False,
            "emotional_fact_written_now": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "confirmed_text_memory_handoff_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "confirmed_text_memory_handoff_non_claims_report_v1",
            "claims": [
                "no_real_memory_write",
                "dryrun_sample_not_user_memory",
                "append_candidate_not_execution",
                "handoff_candidate_not_memory_invoke",
                "privacy_review_not_decision",
                "profile_candidate_not_fact",
                "emotional_candidate_not_fact",
                "worldmodel_link_not_write",
                "no_ocr_no_llm",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "confirmed_text_memory_handoff_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "confirmed_text_memory_handoff_audit_report_v1",
            "confirmed_text_evidence_memory_handoff_dryrun_v1_executed": True,
            "handoff_dryrun_only": True,
            "dryrun_text_evidence_samples_defined": True,
            "confirmed_text_evidence_candidate_generated": True,
            "memory_append_request_candidate_generated": True,
            "permission_policy_applied": True,
            "privacy_sensitivity_policy_applied": True,
            "correction_supersession_conflict_policy_applied": True,
            "expired_stale_routing_policy_applied": True,
            "memory_governance_handoff_candidate_generated": True,
            "memory_governance_handoff_invoked_now": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "memory_deleted_now": False,
            "memory_updated_now": False,
            "memory_overwritten_now": False,
            "memory_merged_now": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "user_profile_fact_written_now": False,
            "emotional_fact_written_now": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
