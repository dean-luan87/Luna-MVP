# -*- coding: utf-8 -*-
"""WorldModel Lookup for Reading Framework v1 — schema/policy only; no lookup runtime.

Phase-WorldModel-Lookup-for-Reading-Framework-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "WorldModel-Lookup-for-Reading-Framework-v1-001"
FINAL_DECISION = "READY_FOR_WORLDMODEL_LOOKUP_READING_DRYRUN_LATER"
RECOMMENDED_NEXT = "WorldModel-Lookup-for-Reading-DryRun-v1"

FOLLOWUPS = [
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "WorldModel-Core-Schema-Contract-v1",
    "WorldModel-Anchor-Registry-v1",
    "Fragment-Evidence-Weaving-Governance-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
    "Memory-Governance-Delete-Update-Authority-Policy-v1",
    "User-Privacy-Consent-Governance-v1",
    "Missing-Regression-Artifact-Recovery-v1",
]

SOURCE_PRIORITY: List[Dict[str, Any]] = [
    {"priority_rank": 1, "source_type": "live_task_context", "use_condition": "task_context_available", "freshness_required": True, "can_override_live_observation": False, "can_trigger_ocr_directly": False, "requires_verification": False},
    {"priority_rank": 2, "source_type": "live_scene_context", "use_condition": "scene_context_available", "freshness_required": True, "can_override_live_observation": False, "can_trigger_ocr_directly": False, "requires_verification": False},
    {"priority_rank": 3, "source_type": "active_route_location_context", "use_condition": "route_or_location_anchor_available", "freshness_required": True, "can_override_live_observation": False, "can_trigger_ocr_directly": False, "requires_verification": True},
    {"priority_rank": 4, "source_type": "worldmodel_anchor", "use_condition": "worldmodel_runtime_available_and_anchor_resolved", "freshness_required": True, "can_override_live_observation": False, "can_trigger_ocr_directly": False, "requires_verification": True},
    {"priority_rank": 5, "source_type": "unresolved_slot", "use_condition": "unresolved_slot_contract_available", "freshness_required": False, "can_override_live_observation": False, "can_trigger_ocr_directly": False, "requires_verification": True},
    {"priority_rank": 6, "source_type": "memory_reference", "use_condition": "memory_governance_and_handoff_available", "freshness_required": True, "can_override_live_observation": False, "can_trigger_ocr_directly": False, "requires_verification": True},
    {"priority_rank": 7, "source_type": "historical_expired_observation", "use_condition": "stale_hint_only_with_freshness_warning", "freshness_required": False, "can_override_live_observation": False, "can_trigger_ocr_directly": False, "requires_verification": True},
    {"priority_rank": 8, "source_type": "scene_task_matrix", "use_condition": "task_scene_matrix_fallback", "freshness_required": False, "can_override_live_observation": False, "can_trigger_ocr_directly": False, "requires_verification": True},
    {"priority_rank": 9, "source_type": "human_staff_assistance", "use_condition": "human_assistance_recommended_or_required", "freshness_required": False, "can_override_live_observation": False, "can_trigger_ocr_directly": False, "requires_verification": True},
]

CLASSIFICATIONS: List[Dict[str, Any]] = [
    ("HIGH_VALUE_LOOKUP_CANDIDATE", "Strong hint for ISRC", ["feed_isrc"], ["submit_ocrrequest"], True, False),
    ("NEEDS_LIVE_VERIFICATION", "Requires capture/OCR gate later", ["prepare_static_capture"], ["write_worldmodel"], True, False),
    ("STALE_BUT_USEFUL", "May feed long-term candidate only", ["feed_long_term_candidate"], ["direct_action"], False, True),
    ("CONFLICTING_HINT", "Hold; user clarification", ["user_clarification"], ["auto_merge"], False, False),
    ("PRIVACY_SENSITIVE_REQUIRES_CONFIRMATION", "Privacy gate before use", ["privacy_confirm"], ["auto_use"], False, False),
    ("HUMAN_ASSISTANCE_RECOMMENDED", "Staff assistance path", ["human_assistance"], ["auto_ocr"], False, False),
    ("NOT_ENOUGH_CONTEXT", "Wait for task/scene", ["wait_task_scene"], ["feed_rrd"], False, False),
    ("DO_NOT_USE_FOR_ACTION", "Do not drive action", [], ["feed_isrc", "submit_ocrrequest", "write_fact"], False, False),
]

FALLBACKS: List[Dict[str, Any]] = [
    ("scene_task_matrix_fallback", "scene_task_matrix", "missing_worldmodel_anchor_or_lookup_empty"),
    ("user_clarification", "user_clarification", "task_scene_incomplete_or_conflicting"),
    ("visual_semantic_path", "visual_semantic_path", "non_text_information_source"),
    ("human_staff_assistance", "human_staff_assistance", "high_risk_or_repeated_failure"),
    ("stop_ocr_path", "stop_ocr_path", "ocr_not_appropriate_for_source_type"),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_ocr_mainline_closure", "ocr_closure_loaded", [], [], ["enable_runtime_ocr"]),
    ("load_static_reading_chain", "static_chain_loaded", [], [], []),
    ("load_worldmodel_unresolved_slot_contract", "unresolved_loaded", [], [], ["write_worldmodel"]),
    ("load_memory_governance_contract", "mem_gov_loaded", [], [], ["memory_write"]),
    ("define_lookup_request_schema", "request_schema_ok", [], [], []),
    ("define_lookup_response_candidate_schema", "response_schema_ok", [], [], ["mark_as_fact"]),
    ("define_lookup_source_priority_policy", "priority_ok", [], [], ["trigger_ocr_directly"]),
    ("define_unresolved_slot_link", "unresolved_link_ok", [], [], []),
    ("define_memory_reference_link", "memory_link_ok", [], [], []),
    ("define_confirmed_text_hint_link", "confirmed_text_ok", [], [], ["write_worldmodel"]),
    ("define_isrc_handoff_policy", "isrc_handoff_ok", [], [], ["invoke_isrc_now"]),
    ("define_rrd_handoff_policy", "rrd_handoff_ok", [], [], ["invoke_rrd_now"]),
    ("define_fallback_policy", "fallback_ok", [], [], ["ocr_invoked"]),
    ("define_future_dryrun_entrypoint", "dryrun_entry_ok", [], [], ["invoke_lookup_now"]),
    ("generate_final_framework_decision", "framework_ready", [], [], ["production_ready"]),
]

LONG_TERM_CANDIDATES = [
    "failed_lookup_context_candidate",
    "missing_worldmodel_anchor_candidate",
    "unresolved_information_source_candidate",
    "stale_but_useful_lookup_hint_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _find_optional_docs(ws_root: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    docs = ws_root / "docs" / "architecture"
    globs_map = {
        "worldmodel_core_schema": "**/LUNA_WORLDMODEL*.md",
        "worldmodel_anchor_registry": "**/*ANCHOR*REGISTRY*.md",
        "fragment_evidence_weaving": "**/*FRAGMENT*EVIDENCE*WEAVING*.md",
        "scene_registry": "**/*SCENE*REGISTRY*.md",
        "map_anchor": "**/*MAP*ANCHOR*.md",
    }
    for doc_id, glob_pat in globs_map.items():
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
                "missing_impact": "none" if found else "optional_doc_reference_only",
                **_not_fact(),
            }
        )
    return rows


def run_worldmodel_lookup_for_reading_framework_v1(
    *,
    ocr_mainline_closure_root: str,
    software_closure_root: str,
    tsc_reevaluation_root: str,
    isrc_runtime_root: str,
    rrd_runtime_root: str,
    worldmodel_unresolved_slot_root: str,
    memory_governance_contract_root: str,
    memory_handoff_root: str,
    ocr_activation_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "ocr_closure": Path(ocr_mainline_closure_root).resolve(),
        "sw_closure": Path(software_closure_root).resolve(),
        "tsc": Path(tsc_reevaluation_root).resolve(),
        "isrc": Path(isrc_runtime_root).resolve(),
        "rrd": Path(rrd_runtime_root).resolve(),
        "unresolved": Path(worldmodel_unresolved_slot_root).resolve(),
        "mem_gov": Path(memory_governance_contract_root).resolve(),
        "mem_handoff": Path(memory_handoff_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    ocr_cl = _read_json(roots["ocr_closure"] / "ocr_mainline_governance_closure_v1_summary.json") or {}
    unresolved_sum = _read_json(roots["unresolved"] / "worldmodel_unresolved_slot_contract_summary.json") or {}
    mem_gov_sum = _read_json(
        roots["mem_gov"] / "confirmed_text_evidence_memory_governance_contract_v1_summary.json"
    ) or {}

    unresolved_available = roots["unresolved"].is_dir() and bool(unresolved_sum)
    mem_gov_available = roots["mem_gov"].is_dir() and bool(mem_gov_sum)
    mem_handoff_available = roots["mem_handoff"].is_dir()

    intake_specs = [
        ("ocr_mainline_closure", roots["ocr_closure"], "ocr_mainline_governance_closure_v1_summary.json", False),
        ("software_closure", roots["sw_closure"], "return_to_software_mainline_closure_v1_summary.json", False),
        ("tsc_reevaluation", roots["tsc"], "static_reading_task_scene_context_reevaluation_dryrun_v1_summary.json", False),
        ("isrc_runtime", roots["isrc"], "static_reading_information_source_localization_runtime_dryrun_v1_summary.json", False),
        ("rrd_runtime", roots["rrd"], "static_readable_region_discovery_runtime_dryrun_v1_summary.json", False),
        ("worldmodel_unresolved_slot", roots["unresolved"], "worldmodel_unresolved_slot_contract_summary.json", False),
        ("memory_governance_contract", roots["mem_gov"], "confirmed_text_evidence_memory_governance_contract_v1_summary.json", False),
        ("memory_handoff_dryrun", roots["mem_handoff"], "confirmed_text_evidence_memory_handoff_dryrun_v1_summary.json", False),
        ("ocr_activation", roots["ocr_act"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("benchmark", roots["bench"], None, True),
        ("system_health", roots["health"], None, True),
        ("simulation", roots["sim"], None, True),
    ]
    intake_rows = []
    for iid, root, art, optional in intake_specs:
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
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "framework_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    request_schema = {
        "schema_version": "worldmodel_lookup_reading_request_schema_v1",
        "schema_only": True,
        "fields": {
            "lookup_request_id": "string",
            "request_source": "static_reading_or_task_scene_context",
            "task_context_ref": "ref",
            "scene_context_ref": "ref",
            "target_information_need": "string",
            "expected_information_source_type": "enum",
            "current_location_anchor": "anchor_ref",
            "route_context_ref": "ref",
            "spatial_anchor": "anchor",
            "time_anchor": "timestamp_ref",
            "user_query_ref": "ref",
            "memory_reference_allowed": "boolean",
            "unresolved_slot_lookup_allowed": "boolean",
            "confirmed_text_hint_allowed": "boolean",
            "live_observation_priority": True,
            "ocr_activation_state_ref": "ref",
            "privacy_sensitivity": "enum",
        },
        "live_observation_priority": True,
        "execution_allowed": False,
        **_not_fact(),
    }

    response_schema = {
        "schema_version": "worldmodel_lookup_reading_response_candidate_schema_v1",
        "schema_only": True,
        "source_types": [
            "worldmodel_anchor",
            "unresolved_slot",
            "memory_reference",
            "confirmed_text_hint",
            "scene_task_matrix",
            "route_context",
            "user_clarification",
            "human_staff_hint",
        ],
        "candidate_information_source_types": [
            "signboard",
            "doorplate",
            "directory_board",
            "warning_sign",
            "restroom_sign",
            "department_sign",
            "transit_line_sign",
            "service_desk",
            "unknown",
        ],
        "fields": {
            "lookup_response_candidate_id": "string",
            "source_type": "enum",
            "candidate_information_source_type": "enum",
            "candidate_location_hint": "string",
            "candidate_spatial_anchor": "anchor",
            "evidence_refs": "list",
            "confidence_placeholder": "number_or_null",
            "freshness_status": "enum",
            "privacy_sensitivity": "enum",
            "requires_live_verification": True,
            "is_fact": False,
            "write_allowed": False,
        },
        "requires_live_verification": True,
        "is_fact": False,
        "write_allowed": False,
        **_not_fact(),
    }

    classification_rows = [
        {
            "classification": cls,
            "meaning": meaning,
            "allowed_next_action": allowed,
            "blocked_next_action": blocked,
            "can_feed_isrc": can_isrc,
            "can_feed_long_term_candidate": can_lt,
            **_not_fact(),
        }
        for cls, meaning, allowed, blocked, can_isrc, can_lt in CLASSIFICATIONS
    ]

    fallback_rows = [
        {
            "fallback_id": fid,
            "fallback_name": name,
            "use_condition": cond,
            "allowed_now_as_policy": True,
            "runtime_invoked_now": False,
            "ocr_invoked_now": False,
            **_not_fact(),
        }
        for fid, name, cond in FALLBACKS
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

    policy_count = 8
    schema_count = 2

    return {
        "summary": {
            "schema_version": "worldmodel_lookup_for_reading_framework_v1_summary_v0",
            "phase": PHASE_ID,
            "framework_scope": "worldmodel_lookup_for_reading_framework_only",
            "based_on_ocr_mainline_closure": roots["ocr_closure"].is_dir(),
            "based_on_static_reading_chain": roots["tsc"].is_dir() and roots["isrc"].is_dir() and roots["rrd"].is_dir(),
            "based_on_worldmodel_unresolved_slot_contract": unresolved_available,
            "based_on_memory_governance": mem_gov_available,
            "worldmodel_lookup_framework_defined": True,
            "lookup_request_schema_defined": True,
            "lookup_response_candidate_schema_defined": True,
            "lookup_source_priority_policy_defined": True,
            "unresolved_slot_link_defined": True,
            "memory_reference_link_defined": True,
            "confirmed_text_hint_link_defined": True,
            "isrc_handoff_policy_defined": True,
            "rrd_handoff_policy_defined": True,
            "fallback_policy_defined": True,
            "future_dryrun_entrypoint_defined": True,
            "worldmodel_runtime_available": False,
            "worldmodel_lookup_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "ocr_invoked": False,
            "ocrrequest_submitted": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
            "recommended_next_phase": RECOMMENDED_NEXT,
        },
        "intake": {
            "schema_version": "worldmodel_lookup_reading_framework_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "request_schema": request_schema,
        "response_schema": response_schema,
        "source_priority": {
            "schema_version": "worldmodel_lookup_reading_source_priority_policy_v1",
            "priorities": [{**p, **_not_fact()} for p in SOURCE_PRIORITY],
            "priority_count": len(SOURCE_PRIORITY),
            **_not_fact(),
        },
        "unresolved_link": {
            "schema_version": "worldmodel_lookup_reading_unresolved_slot_link_policy_v1",
            "unresolved_slot_contract_available": unresolved_available,
            "unresolved_slot_can_feed_lookup_candidate": True,
            "unresolved_slot_is_not_fact": True,
            "unresolved_slot_requires_validation": True,
            "unresolved_slot_can_provide": [
                "possible_information_source_type",
                "previous_unreadable_region",
                "possible_spatial_anchor",
                "missing_text_region",
                "repeated_failed_reading_context",
            ],
            "worldmodel_write_now": False,
            **_not_fact(),
        },
        "memory_link": {
            "schema_version": "worldmodel_lookup_reading_memory_reference_link_policy_v1",
            "memory_governance_contract_available": mem_gov_available,
            "memory_handoff_dryrun_available": mem_handoff_available,
            "memory_reference_can_feed_lookup_candidate": True,
            "memory_reference_cannot_override_live_observation": True,
            "memory_reference_requires_freshness_check": True,
            "memory_reference_requires_source_chain_check": True,
            "memory_reference_requires_privacy_check": True,
            "memory_system_invoked_now": False,
            "memory_written_now": False,
            **_not_fact(),
        },
        "confirmed_text_link": {
            "schema_version": "worldmodel_lookup_reading_confirmed_text_hint_link_policy_v1",
            "confirmed_text_schema_available": mem_gov_available,
            "confirmed_text_can_feed_lookup_hint": True,
            "confirmed_text_can_feed_information_source_candidate": True,
            "confirmed_text_cannot_write_worldmodel_directly": True,
            "confirmed_text_cannot_trigger_ocr_directly": True,
            "confirmed_text_requires_task_scene_alignment": True,
            "confirmed_text_requires_freshness_check": True,
            **_not_fact(),
        },
        "isrc_handoff": {
            "schema_version": "worldmodel_lookup_reading_isrc_handoff_policy_v1",
            "isrc_handoff_policy_defined": True,
            "worldmodel_lookup_candidate_can_feed_isrc": True,
            "isrc_runtime_invoked_now": False,
            "ranked_information_source_area_generated_now": False,
            "required_payload": [
                "task_context",
                "scene_context",
                "lookup_response_candidate",
                "source_chain",
                "freshness_status",
                "spatial_anchor",
                "privacy_sensitivity",
            ],
            "handoff_allowed_later": True,
            **_not_fact(),
        },
        "rrd_handoff": {
            "schema_version": "worldmodel_lookup_reading_rrd_handoff_policy_v1",
            "rrd_handoff_policy_defined": True,
            "isrc_ranked_source_required_before_rrd": True,
            "readable_region_discovery_invoked_now": False,
            "readable_region_candidate_generated_now": False,
            "ocrrequest_eligible_now": False,
            "required_before_rrd": [
                "information_source_candidate",
                "task_scene_context",
                "source_area_candidate",
                "safety_check",
                "stc_freshness",
            ],
            **_not_fact(),
        },
        "fallback": {
            "schema_version": "worldmodel_lookup_reading_fallback_policy_v1",
            "fallback_order": [f[0] for f in FALLBACKS],
            "fallbacks": fallback_rows,
            **_not_fact(),
        },
        "classification": {
            "schema_version": "worldmodel_lookup_reading_candidate_classification_policy_v1",
            "classifications": classification_rows,
            "classification_count": len(classification_rows),
            **_not_fact(),
        },
        "no_write_policy": {
            "schema_version": "worldmodel_lookup_reading_no_write_boundary_policy_v1",
            "worldmodel_lookup_framework_only": True,
            "worldmodel_lookup_invoked": False,
            "world_model_written": False,
            "worldmodel_fact_generated": False,
            "scene_delta_candidate_generated": False,
            "unresolved_slot_written_now": False,
            "world_change_hint_written_now": False,
            "midplatform_fact_written": False,
            "ocr_invoked": False,
            "ocrrequest_submitted": False,
            **_not_fact(),
        },
        "future_dryrun": {
            "schema_version": "worldmodel_lookup_reading_future_dryrun_entrypoint_v1",
            "future_dryrun_entrypoint_defined": True,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "required_before_dryrun": [
                "framework_defined",
                "at_least_one_lookup_source_available",
                "task_scene_context_available",
                "unresolved_slot_contract_available",
                "memory_reference_policy_available",
            ],
            "dryrun_allowed_later": True,
            "dryrun_invoked_now": False,
            "worldmodel_runtime_required_for_dryrun": True,
            "worldmodel_runtime_available_now": False,
            **_not_fact(),
        },
        "long_term": {
            "schema_version": "worldmodel_lookup_reading_long_term_candidate_link_v1",
            "candidates": LONG_TERM_CANDIDATES,
            "can_feed_long_term_candidate": True,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "spatial_anchor",
                "task_context",
                "scene_context",
                "missing_reason",
                "future_usage_scope",
                "privacy_sensitivity",
            ],
            **_not_fact(),
        },
        "trace": {
            "schema_version": "worldmodel_lookup_reading_framework_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "worldmodel_lookup_reading_framework_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "framework_defined": True,
            "worldmodel_runtime_available": False,
            "worldmodel_lookup_invoked_now": False,
            "world_model_written_now": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "worldmodel_lookup_reading_framework_boundary_report_v1",
            "framework_only": True,
            "worldmodel_lookup_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "ocr_invoked": False,
            "ocrrequest_submitted": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "worldmodel_lookup_reading_framework_metrics_candidate_report_v1",
            "schema_defined_count": schema_count,
            "policy_defined_count": policy_count,
            "handoff_policy_count": 2,
            "fallback_policy_count": len(FALLBACKS),
            "classification_count": len(CLASSIFICATIONS),
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "worldmodel_lookup_reading_framework_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "worldmodel_lookup_reading_framework_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "worldmodel_lookup_reading_framework_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "framework_only": True,
            "worldmodel_lookup_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "unresolved_slot_written_now": False,
            "world_change_hint_written_now": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "ocr_invoked": False,
            "ocrrequest_submitted": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "worldmodel_lookup_reading_framework_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "worldmodel_lookup_reading_framework_non_claims_report_v1",
            "claims": [
                "framework_not_lookup_runtime",
                "lookup_schema_not_execution",
                "lookup_candidate_not_worldmodel_fact",
                "unresolved_slot_not_fact",
                "memory_reference_not_current_fact",
                "confirmed_text_hint_not_worldmodel_write",
                "isrc_rrd_handoff_policy_not_execution",
                "future_dryrun_entrypoint_not_executed",
                "no_ocr_no_memory_no_worldmodel_write",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "worldmodel_lookup_reading_framework_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "worldmodel_lookup_reading_framework_audit_report_v1",
            "worldmodel_lookup_for_reading_framework_v1_executed": True,
            "framework_only": True,
            "worldmodel_lookup_framework_defined": True,
            "lookup_request_schema_defined": True,
            "lookup_response_candidate_schema_defined": True,
            "lookup_source_priority_policy_defined": True,
            "unresolved_slot_link_defined": True,
            "memory_reference_link_defined": True,
            "confirmed_text_hint_link_defined": True,
            "isrc_handoff_policy_defined": True,
            "rrd_handoff_policy_defined": True,
            "fallback_policy_defined": True,
            "future_dryrun_entrypoint_defined": True,
            "worldmodel_runtime_available": False,
            "worldmodel_lookup_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "memory_system_invoked": False,
            "memory_written_now": False,
            "ocr_invoked": False,
            "ocrrequest_submitted": False,
            "llm_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
