# -*- coding: utf-8 -*-
"""Task Manager Contract v1 — lifecycle commit authority; contract only; no runtime.

Phase-Task-Manager-Contract-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Task-Manager-Contract-v1-001"
FINAL_DECISION = "TASK_MANAGER_CONTRACT_READY"
RECOMMENDED_NEXT = "Task-Manager-Runtime-DryRun-v1"

FOLLOWUPS = [
    "Task-Manager-Runtime-DryRun-v1",
    "Task-Context-Enrichment-Runtime-DryRun-v1",
    "GPS-Location-Candidate-Contract-v1",
    "Route-Context-Candidate-Contract-v1",
    "Memory-Reference-for-Task-Context-DryRun-v1",
    "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Navigation-Guidance-Task-Policy-v1",
    "Dialogue-Driven-Task-Clarification-Runtime-v1",
    "Task-Manager-Commit-GuardedTrial-v1",
]

ENRICHMENT_TYPES = [
    "time_anchor",
    "spatial_anchor",
    "gps_location_candidate",
    "route_context_candidate",
    "map_context_candidate",
    "scene_context_candidate",
    "memory_reference_context",
    "historical_task_context",
    "unresolved_slot_context",
    "observation_context",
    "system_health_context",
]

ENRICHMENT_SOURCE_ROWS = [
    ("live_task_context", 1, True, True, True),
    ("live_observation", 2, True, True, True),
    ("route_context", 3, True, True, False),
    ("gps_spatial_anchor", 4, True, True, False),
    ("scene_context", 5, True, True, False),
    ("map_reference", 6, True, False, False),
    ("memory_reference", 7, True, False, False),
    ("unresolved_slot", 8, True, True, False),
    ("historical_task_context", 9, True, False, False),
    ("user_clarification", 10, True, True, False),
]

TASK_TYPES = [
    "navigation_task",
    "search_information_task",
    "read_sign_task",
    "confirm_place_task",
    "human_assistance_task",
    "generic_task",
]

LIFECYCLE_EVENTS = [
    "TASK_CREATE_REQUESTED",
    "TASK_CREATED_CANDIDATE",
    "TASK_CONTEXT_UPDATE_REQUESTED",
    "TASK_CONTEXT_UPDATED_CANDIDATE",
    "TASK_PAUSE_REQUESTED",
    "TASK_PAUSED_CANDIDATE",
    "TASK_RESUME_REQUESTED",
    "TASK_RESUMED_CANDIDATE",
    "TASK_CANCEL_REQUESTED",
    "TASK_CANCEL_PENDING_CONFIRMATION",
    "TASK_CANCELLED_CANDIDATE",
    "TASK_STATUS_QUERIED",
    "TASK_GUIDANCE_REQUESTED",
    "TASK_BLOCKED",
    "TASK_ABORTED_CANDIDATE",
    "TASK_COMPLETED_CANDIDATE",
]

COMMIT_DECISIONS = [
    "COMMIT_ALLOWED_LATER",
    "BLOCKED_BY_CONFIRMATION",
    "BLOCKED_BY_SAFETY",
    "BLOCKED_BY_MISSING_CONTEXT",
    "BLOCKED_BY_INVALID_TRANSITION",
    "BLOCKED_BY_DUPLICATE_REQUEST",
    "BLOCKED_BY_TASK_NOT_FOUND",
    "BLOCKED_BY_RUNTIME_DISABLED",
    "REQUIRE_CLARIFICATION",
    "REQUIRE_HUMAN_ASSISTANCE",
    "NO_OP",
]

TM_STATES = [
    ("NO_TASK", "no task exists", ["TASK_CREATE_REQUESTED"], ["TASK_DRAFT"], [], True, True, False),
    ("TASK_DRAFT", "task draft from create candidate", ["TASK_CONTEXT_UPDATE_REQUESTED"], ["TASK_PENDING_CLARIFICATION", "TASK_READY"], [], True, True, False),
    ("TASK_PENDING_CLARIFICATION", "missing goal or scene", ["TASK_CONTEXT_UPDATE_REQUESTED"], ["TASK_READY", "TASK_BLOCKED"], [], True, True, False),
    ("TASK_READY", "task ready to activate", ["TASK_CREATE_REQUESTED"], ["TASK_ACTIVE"], ["TASK_COMPLETED"], True, True, True),
    ("TASK_ACTIVE", "task in progress", ["TASK_PAUSE_REQUESTED", "TASK_CANCEL_REQUESTED", "TASK_STATUS_QUERIED"], ["TASK_PAUSE_PENDING_CONFIRMATION", "TASK_CANCEL_PENDING_CONFIRMATION", "TASK_COMPLETED"], [], True, True, True),
    ("TASK_PAUSE_PENDING_CONFIRMATION", "pause awaiting confirm", ["TASK_PAUSE_REQUESTED"], ["TASK_PAUSED", "TASK_ACTIVE"], [], True, False, False),
    ("TASK_PAUSED", "task paused", ["TASK_RESUME_REQUESTED"], ["TASK_RESUME_PENDING", "TASK_ACTIVE"], [], True, False, False),
    ("TASK_RESUME_PENDING", "resume awaiting confirm", ["TASK_RESUME_REQUESTED"], ["TASK_ACTIVE"], [], True, False, False),
    ("TASK_CANCEL_PENDING_CONFIRMATION", "cancel awaiting confirm", ["TASK_CANCEL_REQUESTED"], ["TASK_CANCELLED", "TASK_ACTIVE"], [], True, False, False),
    ("TASK_CANCELLED", "task cancelled candidate", [], ["NO_TASK", "TASK_ABORTED"], ["TASK_ACTIVE"], True, False, False),
    ("TASK_BLOCKED", "blocked by guard or safety", ["TASK_ABORTED_CANDIDATE"], ["TASK_ABORTED", "NO_TASK"], [], True, True, False),
    ("TASK_COMPLETED", "task completed candidate", [], ["NO_TASK"], ["TASK_ACTIVE"], True, False, False),
    ("TASK_ABORTED", "task aborted", [], ["NO_TASK"], [], True, False, False),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_midplatform_task_state_runtime", "mp_state_loaded", [], [], []),
    ("load_voice_runtime", "voice_runtime_loaded", [], [], []),
    ("load_basic_loop_plan", "loop_plan_loaded", [], [], []),
    ("define_task_object_schema", "task_schema_ok", [], [], []),
    ("define_lifecycle_event_schema", "lifecycle_schema_ok", [], [], []),
    ("define_commit_decision_schema", "commit_schema_ok", [], [], []),
    ("define_state_machine", "fsm_ok", [], [], []),
    ("define_transition_guard_policy", "transition_guard_ok", [], [], ["midplatform_commit"]),
    ("define_confirmation_gate_policy", "confirmation_ok", [], [], []),
    ("define_safety_gate_policy", "safety_ok", [], [], []),
    ("define_idempotency_policy", "idempotency_ok", [], [], ["duplicate_commit"]),
    ("define_rollback_abort_policy", "rollback_ok", [], [], ["runtime_rollback"]),
    ("define_external_boundary_policy", "boundary_ok", [], [], ["voice_commit", "nav_commit"]),
    ("define_runtime_disabled_policy", "runtime_disabled_ok", [], [], ["runtime_commit"]),
    ("define_audit_trace_policy", "audit_ok", [], [], []),
    ("define_midplatform_integration_contract", "integration_ok", [], [], []),
    ("define_task_context_enrichment_schema", "enrichment_schema_ok", [], [], ["fact_write"]),
    ("define_context_enrichment_source_policy", "enrichment_source_ok", [], [], []),
    ("define_task_verification_context_policy", "verification_ctx_ok", [], [], ["task_completed"]),
    ("define_execution_support_context_policy", "execution_support_ok", [], [], ["navigation_action"]),
    ("define_future_runtime_dryrun_entrypoint", "dryrun_entry_ok", [], [], []),
    ("generate_final_contract_decision", "contract_ready", [], [], ["production_ready"]),
]

OPTIONAL_DOC_GLOBS = {
    "task_manager": "**/*TASK*MANAGER*.md",
    "taskchain_runtime": "**/*TASK*CHAIN*.md",
    "dialogue_manager": "**/*DIALOGUE*MANAGER*.md",
    "navigation_task": "**/*NAVIGATION*TASK*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
}


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


def run_task_manager_contract_v1(
    *,
    midplatform_task_state_root: str,
    voice_dialogue_runtime_root: str,
    basic_loop_plan_root: str,
    ocr_activation_root: str,
    stc_root: str,
    system_health_root: str,
    simulation_root: str,
    voice_dialogue_contract_root: Optional[str] = None,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "mp_state": Path(midplatform_task_state_root).resolve(),
        "voice_rt": Path(voice_dialogue_runtime_root).resolve(),
        "contract": Path(
            voice_dialogue_contract_root
            or ws / "_eval_out" / "voice_dialogue_task_control_contract_v1_smoke_v0"
        ).resolve(),
        "loop_plan": Path(basic_loop_plan_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    mp_sum = _read_json(roots["mp_state"] / "midplatform_task_state_runtime_dryrun_v1_summary.json") or {}
    voice_sum = _read_json(roots["voice_rt"] / "voice_dialogue_task_control_runtime_dryrun_v1_summary.json") or {}
    state_coll = _read_json(roots["mp_state"] / "midplatform_task_state_candidate_collection_v1.json") or {}
    lifecycle_coll = _read_json(roots["mp_state"] / "midplatform_task_lifecycle_candidate_collection_v1.json") or {}
    task_state_count = state_coll.get("task_state_candidate_count", 0)
    lifecycle_count = lifecycle_coll.get("lifecycle_candidate_count", 0)

    intake_specs = [
        ("midplatform_task_state_runtime", roots["mp_state"], "midplatform_task_state_runtime_dryrun_v1_summary.json", False),
        ("voice_dialogue_runtime", roots["voice_rt"], "voice_dialogue_task_control_runtime_dryrun_v1_summary.json", False),
        ("voice_dialogue_contract", roots["contract"], "voice_dialogue_task_control_contract_v1_summary.json", False),
        ("basic_functional_loop_plan", roots["loop_plan"], "luna_basic_functional_loop_stabilization_plan_v1_summary.json", False),
        ("ocr_activation", roots["ocr_act"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("stc", roots["stc"], "stc_sampling_guidance_policy_v1_summary.json", False),
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
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "contract_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    state_rows = [
        {
            "state": state,
            "entry_condition": cond,
            "allowed_events": events,
            "allowed_transitions": transitions,
            "blocked_events": blocked,
            "speech_feedback_candidate_allowed": speech,
            "observation_requirement_allowed": obs,
            "navigation_guidance_candidate_allowed": nav,
            "committed_now": False,
            **_not_fact(),
        }
        for state, cond, events, transitions, blocked, speech, obs, nav in TM_STATES
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

    confirmation_rule_count = 6
    safety_rule_count = 5
    idempotency_rule_count = 6
    transition_guard_count = 10

    enrichment_candidates = []
    for i, tsc in enumerate(state_coll.get("candidates") or []):
        tsc_id = tsc.get("task_state_candidate_id", f"tsc_{i}")
        for etype in ("time_anchor", "spatial_anchor", "scene_context_candidate", "observation_context"):
            enrichment_candidates.append(
                {
                    "enrichment_candidate_id": f"enrich_{tsc_id}_{etype}",
                    "source_task_state_candidate_id": tsc_id,
                    "task_id_or_candidate_ref": tsc.get("current_task_state_ref", "task_ref_candidate"),
                    "enrichment_type": etype,
                    "source_chain": "task_manager_contract_v1",
                    "confidence_placeholder": 0.75,
                    "freshness_status": "session_scoped",
                    "privacy_sensitivity": "user_task_context",
                    "can_support_verification": True,
                    "can_support_execution": etype != "system_health_context",
                    "can_override_live_observation": False,
                    "is_fact": False,
                    "write_allowed": False,
                    **_not_fact(),
                }
            )
        enrichment_candidates.append(
            {
                "enrichment_candidate_id": f"enrich_{tsc_id}_gps_location_candidate",
                "source_task_state_candidate_id": tsc_id,
                "task_id_or_candidate_ref": tsc.get("current_task_state_ref"),
                "enrichment_type": "gps_location_candidate",
                "source_chain": "task_manager_contract_v1",
                "confidence_placeholder": None,
                "freshness_status": "optional_missing",
                "privacy_sensitivity": "location",
                "can_support_verification": True,
                "can_support_execution": True,
                "can_override_live_observation": False,
                "is_fact": False,
                "write_allowed": False,
                **_not_fact(),
            }
        )
        enrichment_candidates.append(
            {
                "enrichment_candidate_id": f"enrich_{tsc_id}_memory_reference_context",
                "source_task_state_candidate_id": tsc_id,
                "task_id_or_candidate_ref": tsc.get("current_task_state_ref"),
                "enrichment_type": "memory_reference_context",
                "source_chain": "task_manager_contract_v1",
                "confidence_placeholder": 0.6,
                "freshness_status": "reference_only",
                "privacy_sensitivity": "user_history",
                "can_support_verification": True,
                "can_support_execution": False,
                "can_override_live_observation": False,
                "is_fact": False,
                "write_allowed": False,
                **_not_fact(),
            }
        )

    enrichment_source_rows = [
        {
            "source_type": st,
            "priority_rank": rank,
            "allowed_for_task_verification": ver,
            "allowed_for_execution_support": exe,
            "freshness_required": fresh,
            "source_chain_required": True,
            "can_override_live_observation": False,
            "direct_action_allowed": False,
            **_not_fact(),
        }
        for st, rank, ver, exe, fresh in ENRICHMENT_SOURCE_ROWS
    ]

    return {
        "summary": {
            "schema_version": "task_manager_contract_v1_summary_v0",
            "phase": PHASE_ID,
            "contract_scope": "task_manager_contract_only",
            "based_on_midplatform_task_state_runtime": mp_sum.get("task_state_candidates_generated") is True,
            "based_on_voice_dialogue_runtime": voice_sum.get("voice_intent_candidates_generated") is True,
            "based_on_basic_functional_loop_plan": roots["loop_plan"].is_dir(),
            "task_manager_contract_defined": True,
            "task_schema_defined": True,
            "task_lifecycle_event_schema_defined": True,
            "task_commit_decision_schema_defined": True,
            "task_state_machine_defined": True,
            "transition_guard_policy_defined": True,
            "confirmation_gate_policy_defined": True,
            "idempotency_policy_defined": True,
            "rollback_abort_policy_defined": True,
            "audit_trace_policy_defined": True,
            "task_context_enrichment_schema_defined": True,
            "context_enrichment_source_policy_defined": True,
            "task_verification_context_policy_defined": True,
            "execution_support_context_policy_defined": True,
            "future_runtime_dryrun_entrypoint_defined": True,
            "task_manager_runtime_invoked": False,
            "task_state_committed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "task_completed_now": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "observed_task_state_candidate_count": task_state_count,
            "observed_lifecycle_candidate_count": lifecycle_count,
            "enrichment_candidate_count": len(enrichment_candidates),
        },
        "intake": {
            "schema_version": "task_manager_contract_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "task_schema": {
            "schema_version": "task_manager_task_object_schema_v1",
            "schema_only": True,
            "task_types": TASK_TYPES,
            "field_definitions": {
                "task_id": "string",
                "task_type": "enum",
                "task_goal": "string",
                "task_context": "object",
                "scene_context": "object",
                "route_context_ref": "ref",
                "route_context_candidate": "object",
                "time_anchor": "time_anchor",
                "spatial_anchor": "spatial_anchor",
                "gps_location_candidate": "object",
                "map_context_candidate": "object",
                "memory_reference_context": "object",
                "historical_task_context": "object",
                "unresolved_slot_context": "object",
                "observation_context": "object",
                "verification_context": "object",
                "execution_support_context": "object",
                "context_enrichment_status": "enum",
                "user_intent_ref": "ref",
                "source_chain": "string",
                "created_at_anchor": "time_anchor",
                "updated_at_anchor": "time_anchor",
                "current_task_state": "enum",
                "current_task_version": "integer",
                "safety_priority_state": "string",
                "confirmation_state": "object",
            },
            "context_enrichment_fields": [
                "time_anchor",
                "spatial_anchor",
                "gps_location_candidate",
                "map_context_candidate",
                "route_context_candidate",
                "scene_context_candidate",
                "memory_reference_context",
                "historical_task_context",
                "unresolved_slot_context",
                "observation_context",
                "verification_context",
                "execution_support_context",
            ],
            "ownership": {
                "owner_module": "task_manager",
                "requested_by": "ref",
                "controlled_by_midplatform": True,
            },
            "owner_module": "task_manager",
            **_not_fact(),
        },
        "lifecycle_schema": {
            "schema_version": "task_manager_lifecycle_event_schema_v1",
            "schema_only": True,
            "event_types": LIFECYCLE_EVENTS,
            "field_definitions": {
                "lifecycle_event_id": "string",
                "source_task_state_candidate_id": "ref",
                "source_lifecycle_candidate_id": "ref",
                "event_type": "enum",
                "previous_task_state": "enum",
                "proposed_next_task_state": "enum",
                "transition_guard_result": "string",
                "confirmation_requirement": "boolean",
                "safety_gate_result": "string",
                "idempotency_key": "string",
                "commit_allowed_later": "boolean",
                "committed_now": False,
            },
            "committed_now": False,
            **_not_fact(),
        },
        "commit_schema": {
            "schema_version": "task_manager_commit_decision_schema_v1",
            "schema_only": True,
            "decision_types": COMMIT_DECISIONS,
            "field_definitions": {
                "commit_decision_id": "string",
                "source_lifecycle_event_id": "ref",
                "decision_type": "enum",
                "allowed_now": False,
                "allowed_later": "boolean",
                "blocked_reason": "string",
                "required_next_input": "string",
                "rollback_required": "boolean",
                "audit_required": True,
                "task_state_committed_now": False,
            },
            "allowed_now": False,
            "audit_required": True,
            "task_state_committed_now": False,
            **_not_fact(),
        },
        "state_machine": {
            "schema_version": "task_manager_state_machine_contract_v1",
            "states": state_rows,
            "state_count": len(state_rows),
            **_not_fact(),
        },
        "transition_guard": {
            "schema_version": "task_manager_transition_guard_policy_v1",
            "create_requires_valid_goal": True,
            "activate_requires_task_ready": True,
            "update_requires_existing_task": True,
            "pause_requires_active_task": True,
            "resume_requires_paused_task": True,
            "cancel_requires_existing_task": True,
            "cancel_requires_confirmation": True,
            "complete_requires_task_active_or_ready": True,
            "abort_requires_system_or_user_reason": True,
            "invalid_transition_blocks_commit": True,
            "task_manager_owns_commit": True,
            "guard_count": transition_guard_count,
            **_not_fact(),
        },
        "confirmation_gate": {
            "schema_version": "task_manager_confirmation_gate_policy_v1",
            "cancel_requires_confirmation": True,
            "pause_may_require_confirmation": True,
            "resume_may_require_confirmation": True,
            "high_risk_navigation_requires_confirmation": True,
            "human_assistance_requires_confirmation": True,
            "confirmation_must_match_pending_context": True,
            "stale_confirmation_rejected": True,
            "confirmation_state_is_short_term": True,
            "memory_system_invoked_now": False,
            "confirmation_rule_count": confirmation_rule_count,
            **_not_fact(),
        },
        "safety_gate": {
            "schema_version": "task_manager_safety_gate_policy_v1",
            "safety_alert_can_block_task_commit": True,
            "safety_alert_can_delay_cancel_confirmation": True,
            "safety_alert_can_force_guidance_priority": True,
            "safety_alert_does_not_create_task_fact": True,
            "p0_p1_priority_above_task_dialogue": True,
            "task_commit_recheck_required_after_safety_clears": True,
            "safety_rule_count": safety_rule_count,
            **_not_fact(),
        },
        "idempotency": {
            "schema_version": "task_manager_idempotency_duplicate_policy_v1",
            "idempotency_required": True,
            "idempotency_key_sources": [
                "source_handoff_id",
                "source_lifecycle_candidate_id",
                "task_id",
                "proposed_next_state",
                "time_anchor",
            ],
            "duplicate_commit_forbidden": True,
            "repeated_cancel_confirmation_noop_if_already_cancelled": True,
            "repeated_pause_noop_if_already_paused": True,
            "repeated_resume_noop_if_already_active": True,
            "no_op_must_be_audited": True,
            "idempotency_rule_count": idempotency_rule_count,
            **_not_fact(),
        },
        "rollback_abort": {
            "schema_version": "task_manager_rollback_abort_policy_v1",
            "rollback_required_if_commit_partially_applied": True,
            "abort_allowed_for_safety_or_user_cancel": True,
            "abort_requires_reason": True,
            "rollback_event_must_keep_source_chain": True,
            "original_lifecycle_event_never_overwritten": True,
            "corrective_event_append_only": True,
            "runtime_rollback_invoked_now": False,
            **_not_fact(),
        },
        "external_boundary": {
            "schema_version": "task_manager_external_boundary_policy_v1",
            "task_manager_owns_task_lifecycle": True,
            "midplatform_can_request_commit_candidate": True,
            "midplatform_cannot_commit_lifecycle_directly": True,
            "voice_cannot_commit_lifecycle_directly": True,
            "navigation_guidance_cannot_commit_lifecycle_directly": True,
            "task_manager_cannot_trigger_voice_output_directly": True,
            "task_manager_cannot_trigger_navigation_action_directly": True,
            "task_manager_can_emit_guidance_need_candidate": True,
            "task_manager_can_emit_speech_response_candidate": True,
            "memory_reference_read_only": True,
            "memory_update_delete_forbidden": True,
            "enriched_context_cannot_override_live_observation": True,
            **_not_fact(),
        },
        "context_enrichment_schema": {
            "schema_version": "task_manager_task_context_enrichment_schema_v1",
            "schema_only": True,
            "enrichment_types": ENRICHMENT_TYPES,
            "enrichment_candidate_count": len(enrichment_candidates),
            "candidates": enrichment_candidates,
            "field_definitions": {
                "enrichment_candidate_id": "string",
                "source_task_state_candidate_id": "ref",
                "task_id_or_candidate_ref": "ref",
                "enrichment_type": "enum",
                "source_chain": "string",
                "confidence_placeholder": "number_or_null",
                "freshness_status": "string",
                "privacy_sensitivity": "string",
                "can_support_verification": True,
                "can_support_execution": "boolean",
                "can_override_live_observation": False,
                "is_fact": False,
                "write_allowed": False,
            },
            "can_override_live_observation": False,
            **_not_fact(),
        },
        "enrichment_source_policy": {
            "schema_version": "task_manager_context_enrichment_source_policy_v1",
            "priority_order": [
                "live_task_context",
                "live_observation",
                "route_context",
                "gps_spatial_anchor",
                "scene_context",
                "map_reference",
                "memory_reference",
                "unresolved_slot",
                "historical_task_context",
                "user_clarification",
            ],
            "sources": enrichment_source_rows,
            "memory_read_reference_append_request_only": True,
            "memory_update_delete_forbidden": True,
            "direct_action_allowed": False,
            **_not_fact(),
        },
        "verification_context_policy": {
            "schema_version": "task_manager_task_verification_context_policy_v1",
            "verification_purposes": [
                "verify_task_goal_reached",
                "verify_correct_location",
                "verify_correct_direction",
                "verify_target_information_found",
                "verify_user_confirmation_needed",
                "verify_route_stage",
                "verify_scene_match",
            ],
            "verification_context_required_for_completion": True,
            "user_confirmation_required_when_low_confidence": True,
            "live_observation_required_for_navigation_completion": True,
            "memory_reference_cannot_complete_task_alone": True,
            "gps_candidate_cannot_complete_task_alone": True,
            "task_completed_now": False,
            "write_allowed": False,
            "fact_status": "not_fact",
        },
        "execution_support_policy": {
            "schema_version": "task_manager_execution_support_context_policy_v1",
            "execution_support_purposes": [
                "choose_next_observation",
                "decide_need_for_user_guidance",
                "decide_need_for_navigation_guidance",
                "decide_need_for_ocr_candidate",
                "decide_need_for_human_assistance",
                "decide_task_blocked_by_missing_context",
            ],
            "execution_support_context_can_drive_candidate_generation": True,
            "execution_support_context_cannot_trigger_runtime_action_directly": True,
            "requires_midplatform_gate": True,
            "requires_task_manager_commit_for_lifecycle": True,
            "navigation_action_triggered": False,
            "task_completed_now": False,
            "write_allowed": False,
            "fact_status": "not_fact",
        },
        "runtime_disabled": {
            "schema_version": "task_manager_runtime_disabled_policy_v1",
            "task_manager_runtime_available": False,
            "runtime_commit_allowed_now": False,
            "runtime_dryrun_allowed_later": True,
            "task_state_commit_blocked_now": True,
            "required_before_runtime": [
                "contract_defined",
                "task_state_machine_defined",
                "transition_guard_defined",
                "confirmation_gate_defined",
                "idempotency_policy_defined",
                "audit_trace_policy_defined",
                "task_context_enrichment_defined",
            ],
            **_not_fact(),
        },
        "future_dryrun": {
            "schema_version": "task_manager_future_runtime_dryrun_entrypoint_v1",
            "future_runtime_dryrun_entrypoint_defined": True,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "required_before_dryrun": [
                "contract_defined",
                "midplatform_task_state_candidates_available",
                "state_machine_defined",
                "transition_guard_defined",
                "confirmation_gate_defined",
                "simulation_profile_available",
            ],
            "dryrun_allowed_later": True,
            "dryrun_invoked_now": False,
            **_not_fact(),
        },
        "audit_trace": {
            "schema_version": "task_manager_audit_trace_policy_v1",
            "audit_required_for_all_commit_decisions": True,
            "trace_required_for_all_lifecycle_events": True,
            "source_chain_required": True,
            "decision_reason_required": True,
            "blocked_reason_required_when_blocked": True,
            "confirmation_ref_required_when_confirmation_used": True,
            "safety_ref_required_when_safety_gate_applied": True,
            "original_candidate_never_overwritten": True,
            "corrective_event_append_only": True,
            **_not_fact(),
        },
        "midplatform_integration": {
            "schema_version": "task_manager_midplatform_integration_contract_v1",
            "accepts_task_state_candidates": True,
            "accepts_lifecycle_candidates": True,
            "accepts_guidance_need_candidates": False,
            "accepts_observation_requirement_candidates": False,
            "lifecycle_candidate_required_for_commit": True,
            "task_state_candidate_required_for_context": True,
            "midplatform_task_state_candidate_is_not_committed": True,
            "task_manager_commit_decision_required": True,
            "commit_invoked_now": False,
            "observed_lifecycle_candidate_count": lifecycle_count,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "task_manager_contract_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "task_manager_contract_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "contract_defined": True,
            "task_manager_runtime_available": False,
            "runtime_commit_allowed_now": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "alternate_next_phases": [
                "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
                "Basic-Navigation-Guidance-Loop-DryRun-v1",
            ],
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "task_manager_contract_boundary_report_v1",
            "contract_only": True,
            "task_manager_runtime_invoked": False,
            "task_state_committed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "task_completed_now": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "enriched_context_override_live_observation": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "task_manager_contract_metrics_candidate_report_v1",
            "task_state_count": task_state_count,
            "lifecycle_event_type_count": len(LIFECYCLE_EVENTS),
            "commit_decision_type_count": len(COMMIT_DECISIONS),
            "transition_guard_count": transition_guard_count,
            "confirmation_rule_count": confirmation_rule_count,
            "safety_rule_count": safety_rule_count,
            "idempotency_rule_count": idempotency_rule_count,
            "enrichment_candidate_count": len(enrichment_candidates),
            "enrichment_type_count": len(ENRICHMENT_TYPES),
            "enrichment_source_count": len(enrichment_source_rows),
            "runtime_action_committed_count": 0,
            "task_completed_now": 0,
            "task_state_commit_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "task_manager_contract_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "task_manager_contract_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "task_manager_health_report_candidate_generated": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "task_manager_contract_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "contract_only": True,
            "task_manager_runtime_invoked": False,
            "task_state_committed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "task_manager_contract_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "task_manager_contract_non_claims_report_v1",
            "claims": [
                "contract_not_task_manager_runtime",
                "task_object_schema_not_real_task",
                "lifecycle_event_schema_not_real_event",
                "commit_decision_schema_not_real_commit",
                "future_dryrun_not_runtime_executed",
                "contract_ready_not_production_ready",
                "no_create_cancel_pause_resume",
                "no_navigation_tts_vop",
                "no_fact_write",
                "enrichment_candidate_not_fact",
                "enrichment_cannot_override_live_observation",
                "memory_reference_read_only",
            ],
        },
        "followups": {
            "schema_version": "task_manager_contract_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "task_manager_contract_audit_report_v1",
            "task_manager_contract_v1_executed": True,
            "contract_only": True,
            "task_manager_contract_defined": True,
            "task_schema_defined": True,
            "task_lifecycle_event_schema_defined": True,
            "task_commit_decision_schema_defined": True,
            "task_state_machine_defined": True,
            "transition_guard_policy_defined": True,
            "confirmation_gate_policy_defined": True,
            "idempotency_policy_defined": True,
            "rollback_abort_policy_defined": True,
            "audit_trace_policy_defined": True,
            "task_context_enrichment_schema_defined": True,
            "context_enrichment_source_policy_defined": True,
            "task_verification_context_policy_defined": True,
            "execution_support_context_policy_defined": True,
            "future_runtime_dryrun_entrypoint_defined": True,
            "task_manager_runtime_invoked": False,
            "task_state_committed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "task_completed_now": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
