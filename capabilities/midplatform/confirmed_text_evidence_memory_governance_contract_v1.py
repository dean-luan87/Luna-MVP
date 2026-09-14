# -*- coding: utf-8 -*-
"""Confirmed Text Evidence Memory Governance Contract v1 — contract only, no Memory I/O.

Phase-Confirmed-Text-Evidence-Memory-Governance-Contract-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Confirmed-Text-Evidence-Memory-Governance-Contract-v1-001"
FINAL_DECISION = "READY_FOR_MEMORY_GOVERNANCE_HANDOFF_DRYRUN_LATER"

EVIDENCE_STATUSES = [
    "candidate",
    "confirmed",
    "rejected",
    "expired",
    "superseded",
    "conflict_pending",
]

TEXT_TYPES = [
    "safety_warning",
    "doorplate",
    "shop_sign",
    "department_sign",
    "transit_line",
    "restroom_sign",
    "notice",
    "instruction",
    "user_explicit_reading",
    "unknown_text",
]

FUTURE_USAGE_SCOPES = [
    "current_task_support",
    "world_model_hint",
    "user_environment_context",
    "user_profile_context",
    "emotional_context_background",
]

TARGET_MEMORY_DOMAINS = [
    "text_evidence_memory",
    "world_context_memory",
    "user_environment_context_memory",
    "user_profile_context_memory",
    "emotional_context_background_memory",
]

PAYLOAD_TYPES = [
    "confirmed_text_evidence",
    "expired_text_observation",
    "correction_candidate",
    "supersession_candidate",
    "conflict_candidate",
    "unresolved_text_candidate",
]

ALLOWED_OPS = [
    "append_request",
    "read_request",
    "call_reference",
    "query_reference",
]

FORBIDDEN_OPS = [
    "delete_memory",
    "update_memory",
    "overwrite_memory",
    "merge_memory",
    "purge_memory",
    "mutate_memory_metadata",
    "force_ttl_change",
    "force_conflict_resolution",
]

CORRECTION_REASONS = [
    "ocr_error",
    "user_correction",
    "later_observation_conflict",
    "stale_information",
    "wrong_scene_context",
    "wrong_task_context",
]

PRIVACY_CLASSES = [
    ("public_text", False, False, False),
    ("semi_public_text", False, False, False),
    ("private_text", True, False, True),
    ("sensitive_personal_text", True, True, True),
    ("medical_text", True, True, True),
    ("financial_text", True, True, True),
    ("identity_document_text", True, True, True),
    ("location_sensitive_text", True, False, True),
]

STALE_ROUTES = [
    "expired_text_observation_candidate",
    "world_change_hint_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
    "unresolved_text_candidate",
]

FOLLOWUPS = [
    "Confirmed-Text-Evidence-Memory-Handoff-DryRun-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
    "Memory-Governance-Delete-Update-Authority-Policy-v1",
    "User-Privacy-Consent-Governance-v1",
    "Return-To-Software-Mainline-Closure-v1",
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_software_mainline_context", "context_loaded", [], [], []),
    ("load_ocr_activation_governance", "ocr_gov_loaded", [], [], ["ocr_invoke"]),
    ("load_static_reading_chain", "reading_chain_loaded", [], [], []),
    ("load_worldmodel_unresolved_slot_contract", "wm_slot_loaded", [], [], ["wm_write"]),
    ("define_confirmed_text_evidence_schema", "schema_defined", [], [], []),
    ("define_memory_append_request_schema", "append_schema_defined", [], [], ["memory_write"]),
    ("define_midplatform_permission_policy", "permission_defined", [], [], ["delete", "update"]),
    ("define_append_only_correction_policy", "correction_defined", [], [], ["overwrite"]),
    ("define_supersession_conflict_policy", "conflict_defined", [], [], ["resolve_conflict"]),
    ("define_expired_stale_routing_policy", "stale_routing_defined", [], [], ["discard_expired"]),
    ("define_memory_read_call_policy", "read_policy_defined", [], [], []),
    ("define_privacy_sensitivity_policy", "privacy_defined", [], [], []),
    ("define_memory_governance_boundary", "boundary_defined", [], [], []),
    ("generate_final_contract_decision", FINAL_DECISION, [], [], ["routing_change"]),
]

OPTIONAL_DOC_CANDIDATES = [
    ("memory_governance_docs", "docs/architecture/midplatform/LUNA_MEMORY_GOVERNANCE_V0.md"),
    ("user_profile_docs", "docs/architecture/midplatform/LUNA_USER_PROFILE_CONTEXT_V0.md"),
    ("emotional_context_docs", "docs/architecture/midplatform/LUNA_EMOTIONAL_CONTEXT_BACKGROUND_V0.md"),
    ("worldmodel_docs", "docs/architecture/LUNA_WORLD_MODEL_V0.md"),
    ("text_evidence_docs", "docs/architecture/ocr_bridge/LUNA_OCR_EVIDENCE_GOVERNANCE_AUTHORITY_FREEZE_V0.md"),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _intake(roots: Dict[str, Path], workspace_root: Optional[Path]) -> Dict[str, Any]:
    specs = [
        ("hardware_adapter_stub", roots["hw_stub"], "hardware_camera_runtime_adapter_implementation_stub_v1_summary.json", False),
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
        "schema_version": "confirmed_text_evidence_memory_input_intake_matrix_v1",
        "rows": rows,
        **_not_fact(),
    }


def _confirmed_text_schema() -> Dict[str, Any]:
    return {
        "schema_version": "confirmed_text_evidence_schema_v1",
        "description": "Candidate structure for midplatform-confirmed text evidence; not a memory fact.",
        "required_fields": [
            "text_evidence_id",
            "evidence_status",
            "text_content",
            "text_language",
            "text_type",
            "source_chain",
            "ocr_request_ref",
            "evidence_pack_ref",
            "readable_region_ref",
            "information_source_ref",
            "task_context_ref",
            "scene_context_ref",
            "time_anchor",
            "spatial_anchor",
            "confidence_policy",
            "validation_policy",
            "privacy_sensitivity",
            "retention_intent",
            "future_usage_scope",
        ],
        "evidence_status_values": EVIDENCE_STATUSES,
        "text_type_values": TEXT_TYPES,
        "future_usage_scope_values": FUTURE_USAGE_SCOPES,
        "example_placeholder": {
            "text_evidence_id": "cte_placeholder_v0",
            "evidence_status": "candidate",
            "text_content": "(placeholder — contract only)",
            "text_language": "zh",
            "text_type": "unknown_text",
            "source_chain": ["static_reading", "rrd", "ocr_activation"],
            "ocr_request_ref": None,
            "evidence_pack_ref": None,
            "readable_region_ref": "rrc_placeholder",
            "information_source_ref": "isa_placeholder",
            "task_context_ref": "tsc_placeholder",
            "scene_context_ref": "scene_placeholder",
            "time_anchor": "time_anchor_placeholder",
            "spatial_anchor": "spatial_anchor_placeholder",
            "confidence_policy": "confidence_policy_placeholder",
            "validation_policy": "validation_policy_placeholder",
            "privacy_sensitivity": "public_text",
            "retention_intent": "retain_for_governance_review",
            "future_usage_scope": FUTURE_USAGE_SCOPES,
        },
        **_not_fact(),
    }


def _append_request_schema() -> Dict[str, Any]:
    return {
        "schema_version": "confirmed_text_memory_append_request_schema_v1",
        "required_fields": [
            "append_request_id",
            "request_source",
            "operation",
            "target_memory_domain",
            "payload_ref",
            "payload_type",
            "source_chain",
            "append_reason",
            "privacy_sensitivity",
            "review_required",
            "memory_governance_required",
            "memory_write_invoked_now",
        ],
        "request_source": "midplatform",
        "operation": "append_only",
        "target_memory_domain_values": TARGET_MEMORY_DOMAINS,
        "payload_type_values": PAYLOAD_TYPES,
        "memory_governance_required": True,
        "memory_write_invoked_now": False,
        **_not_fact(),
    }


def _permission_policy() -> Dict[str, Any]:
    rules = []
    for op in ALLOWED_OPS:
        rules.append(
            {
                "operation": op,
                "allowed_for_midplatform": True,
                "required_governance_layer": "memory_governance_for_commit",
                "violation_if_called": None,
                "audit_required": True,
            }
        )
    for op in FORBIDDEN_OPS:
        rules.append(
            {
                "operation": op,
                "allowed_for_midplatform": False,
                "required_governance_layer": "memory_governance_only",
                "violation_if_called": f"MIDPLATFORM_{op.upper()}_FORBIDDEN",
                "audit_required": True,
            }
        )
    return {
        "schema_version": "midplatform_memory_permission_policy_v1",
        "allowed_operations": ALLOWED_OPS,
        "forbidden_operations": FORBIDDEN_OPS,
        "rules": rules,
        "midplatform_append_only": True,
        "midplatform_delete_forbidden": True,
        "midplatform_update_forbidden": True,
        **_not_fact(),
    }


def _correction_policy() -> Dict[str, Any]:
    return {
        "schema_version": "confirmed_text_append_only_correction_policy_v1",
        "original_evidence_never_overwritten": True,
        "correction_as_new_record": True,
        "correction_links_original": True,
        "correction_requires_reason": True,
        "correction_requires_source_chain": True,
        "correction_requires_review": True,
        "memory_governance_resolves_later": True,
        "midplatform_update_original_forbidden": True,
        "correction_candidate_schema": {
            "correction_id": "string",
            "original_text_evidence_id": "string",
            "corrected_text_content": "string",
            "correction_reason": "enum",
            "source_chain": "list",
            "review_required": True,
        },
        "allowed_correction_reasons": CORRECTION_REASONS,
        "write_now": False,
        **_not_fact(),
    }


def _supersession_conflict_policy() -> Dict[str, Any]:
    return {
        "schema_version": "confirmed_text_supersession_conflict_policy_v1",
        "supersession_as_new_record": True,
        "conflict_as_new_record": True,
        "original_record_retained": True,
        "conflict_status": "conflict_pending",
        "memory_governance_required": True,
        "midplatform_conflict_resolution_forbidden": True,
        "candidate_types": [
            "supersession_candidate",
            "conflict_candidate",
            "duplicate_candidate",
            "contradiction_candidate",
        ],
        **_not_fact(),
    }


def _expired_stale_routing() -> Dict[str, Any]:
    return {
        "schema_version": "confirmed_text_expired_stale_routing_policy_v1",
        "stale_blocks_current_action": True,
        "stale_does_not_imply_discard": True,
        "expired_text_can_feed_long_term_candidate": True,
        "stale_text_can_feed_world_change_hint": True,
        "stale_text_can_feed_user_environment_context": True,
        "stale_text_can_feed_user_profile_context": True,
        "stale_text_can_feed_emotional_context_background": True,
        "memory_delete_for_expiration_forbidden_to_midplatform": True,
        "routing_candidates": STALE_ROUTES,
        **_not_fact(),
    }


def _read_call_policy() -> Dict[str, Any]:
    return {
        "schema_version": "confirmed_text_memory_read_call_reference_policy_v1",
        "midplatform_can_read_memory": True,
        "midplatform_can_call_reference": True,
        "midplatform_can_query_reference": True,
        "read_result_is_not_current_fact_by_default": True,
        "memory_result_requires_freshness_check": True,
        "memory_result_requires_source_chain_check": True,
        "memory_result_requires_task_context_check": True,
        "memory_result_requires_privacy_check": True,
        "memory_result_cannot_override_live_observation": True,
        **_not_fact(),
    }


def _privacy_policy() -> Dict[str, Any]:
    classes = []
    for cls, review, redact, confirm in PRIVACY_CLASSES:
        classes.append(
            {
                "privacy_class": cls,
                "storage_allowed_candidate": True,
                "review_required": review,
                "redaction_required": redact,
                "user_confirmation_required": confirm,
                "allowed_future_usage_scope": FUTURE_USAGE_SCOPES if cls == "public_text" else ["user_environment_context"],
                "forbidden_future_usage_scope": ["emotional_context_background"] if cls in ("medical_text", "financial_text", "identity_document_text") else [],
            }
        )
    return {
        "schema_version": "confirmed_text_memory_privacy_sensitivity_policy_v1",
        "privacy_classes": classes,
        "medical_text_review_required": True,
        "financial_text_review_required": True,
        "identity_document_text_review_required": True,
        "write_now": False,
        **_not_fact(),
    }


def _responsibility_boundary() -> Dict[str, Any]:
    return {
        "schema_version": "memory_governance_responsibility_boundary_v1",
        "midplatform_allowed": [
            "append_candidate",
            "read_reference",
            "call_reference",
            "query_reference",
            "attach_source_chain",
            "attach_context_anchor",
        ],
        "midplatform_forbidden": [
            "delete",
            "update",
            "overwrite",
            "merge",
            "purge",
            "resolve_conflict",
            "set_final_retention",
            "mutate_profile_fact",
        ],
        "memory_governance_owns": [
            "delete",
            "update",
            "merge",
            "conflict_resolution",
            "deduplication",
            "retention_policy",
            "ttl_policy",
            "privacy_review",
            "user_profile_promotion",
            "emotional_context_promotion",
        ],
        **_not_fact(),
    }


def run_confirmed_text_evidence_memory_governance_contract_v1(
    *,
    hardware_adapter_stub_root: str,
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
        "hw_stub": Path(hardware_adapter_stub_root).resolve(),
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

    perm = _permission_policy()
    privacy = _privacy_policy()
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

    forbidden_count = len(FORBIDDEN_OPS)
    allowed_count = len(ALLOWED_OPS)

    return {
        "summary": {
            "schema_version": "confirmed_text_evidence_memory_governance_contract_v1_summary_v0",
            "phase": PHASE_ID,
            "contract_scope": "confirmed_text_evidence_memory_governance_contract_only",
            "based_on_ocr_activation_governance": roots["ocr"].is_dir(),
            "based_on_static_reading_chain": roots["rrd"].is_dir() and roots["isrc"].is_dir(),
            "based_on_worldmodel_unresolved_slot": roots["wm"].is_dir(),
            "memory_governance_contract_defined": True,
            "confirmed_text_evidence_schema_defined": True,
            "memory_append_request_schema_defined": True,
            "memory_read_call_policy_defined": True,
            "midplatform_append_only_policy_defined": True,
            "midplatform_delete_forbidden": True,
            "midplatform_update_forbidden": True,
            "correction_append_policy_defined": True,
            "supersession_append_policy_defined": True,
            "conflict_append_policy_defined": True,
            "expired_stale_text_routing_policy_defined": True,
            "privacy_sensitivity_policy_defined": True,
            "memory_governance_handoff_defined": True,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "memory_deleted_now": False,
            "memory_updated_now": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots, ws),
        "evidence_schema": _confirmed_text_schema(),
        "append_schema": _append_request_schema(),
        "permission": perm,
        "correction": _correction_policy(),
        "supersession_conflict": _supersession_conflict_policy(),
        "expired_stale": _expired_stale_routing(),
        "read_call": _read_call_policy(),
        "privacy": privacy,
        "responsibility": _responsibility_boundary(),
        "handoff": {
            "schema_version": "confirmed_text_memory_governance_handoff_candidate_v1",
            "handoff_candidate_generated": True,
            "handoff_allowed_later": True,
            "handoff_invoked_now": False,
            "payload_schema": [
                "append_request",
                "confirmed_text_evidence",
                "source_chain",
                "time_anchor",
                "spatial_anchor",
                "confidence_policy",
                "privacy_sensitivity",
                "future_usage_scope",
                "correction_or_conflict_link",
            ],
            "memory_system_invoked_now": False,
            "memory_write_invoked_now": False,
            **_not_fact(),
        },
        "worldmodel_link": {
            "schema_version": "confirmed_text_worldmodel_scenedelta_link_policy_v1",
            "confirmed_text_can_feed_world_model_hint": True,
            "confirmed_text_can_feed_unresolved_slot": True,
            "confirmed_text_can_feed_world_change_hint": True,
            "confirmed_text_cannot_write_world_model_directly": True,
            "confirmed_text_cannot_generate_scene_delta_directly": True,
            "world_model_promotion_requires_worldmodel_governance": True,
            "scene_delta_generation_requires_scene_governance": True,
            **_not_fact(),
        },
        "user_emotional_link": {
            "schema_version": "confirmed_text_user_emotional_context_link_policy_v1",
            "candidate_types": [
                "user_environment_context_candidate",
                "user_profile_context_candidate",
                "emotional_context_background_candidate",
            ],
            "text_evidence_can_support_user_environment_context": True,
            "text_evidence_can_support_profile_candidate": True,
            "text_evidence_can_support_emotional_context_background": True,
            "midplatform_cannot_promote_to_profile_fact": True,
            "emotional_context_candidate_requires_future_emotion_engine": True,
            "write_now": False,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "confirmed_text_evidence_memory_governance_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "confirmed_text_evidence_memory_governance_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "memory_governance_contract_defined": True,
            "midplatform_append_only": True,
            "midplatform_delete_forbidden": True,
            "midplatform_update_forbidden": True,
            "memory_system_invoked_now": False,
            "memory_written_now": False,
            "recommended_next_phase": "Confirmed-Text-Evidence-Memory-Handoff-DryRun-v1",
            "alternate_next_phase": "OCRRequest-Gated-Submission-from-StaticReading-v1",
            "alternate_next_phase_2": "WorldModel-Lookup-for-Reading-DryRun-v1",
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "confirmed_text_evidence_memory_governance_boundary_report_v1",
            "contract_only": True,
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
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "confirmed_text_evidence_memory_governance_metrics_candidate_report_v1",
            "schema_defined_count": 8,
            "permission_rule_count": len(perm["rules"]),
            "forbidden_operation_count": forbidden_count,
            "allowed_operation_count": allowed_count,
            "long_term_candidate_route_count": len(STALE_ROUTES),
            "privacy_class_count": len(PRIVACY_CLASSES),
            "runtime_action_committed_count": 0,
            "memory_write_invoked_count": 0,
            "memory_delete_invoked_count": 0,
            "memory_update_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "confirmed_text_evidence_memory_governance_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "confirmed_text_evidence_memory_governance_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "confirmed_text_evidence_memory_governance_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "contract_only": True,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "memory_deleted_now": False,
            "memory_updated_now": False,
            "memory_overwritten_now": False,
            "memory_merged_now": False,
            "world_model_written": False,
            "scene_delta_written": False,
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
            "schema_version": "confirmed_text_evidence_memory_governance_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "confirmed_text_evidence_memory_governance_non_claims_report_v1",
            "claims": [
                "no_real_memory_write",
                "confirmed_text_schema_not_fact",
                "append_request_not_execution",
                "read_policy_not_runtime_query",
                "stale_routing_not_long_term_write",
                "profile_candidate_not_profile_fact",
                "emotional_candidate_not_emotion_fact",
                "handoff_not_memory_invoke",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "confirmed_text_evidence_memory_governance_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "confirmed_text_evidence_memory_governance_audit_report_v1",
            "confirmed_text_evidence_memory_governance_contract_v1_executed": True,
            "contract_only": True,
            "memory_governance_contract_defined": True,
            "midplatform_append_only_policy_defined": True,
            "midplatform_delete_forbidden": True,
            "midplatform_update_forbidden": True,
            "correction_append_policy_defined": True,
            "supersession_append_policy_defined": True,
            "conflict_append_policy_defined": True,
            "expired_stale_text_routing_policy_defined": True,
            "privacy_sensitivity_policy_defined": True,
            "memory_governance_handoff_defined": True,
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
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
