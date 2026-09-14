# -*- coding: utf-8 -*-
"""Midplatform Decision Center Planning v1 — plan decision center role and contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as HEALTH_POST_DR_FINAL_GO,
)
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_core_architecture_resume_v1 import (
    FINAL_DECISION_GO as CORE_RESUME_FINAL_GO,
    NEXT_PHASE_GO as CORE_RESUME_NEXT_PHASE,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL_GO,
)
from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as WHITEBOX_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Decision-Center-Planning-v1-001"
SCOPE = "decision_center_planning_only"
SOURCE_CHAIN = "midplatform_decision_center_planning_v1"

UPSTREAM_CORE_RESUME_FINAL = CORE_RESUME_FINAL_GO
UPSTREAM_CORE_RESUME_NEXT = CORE_RESUME_NEXT_PHASE
UPSTREAM_WHITEBOX_DR_FINAL = WHITEBOX_DR_FINAL_GO
UPSTREAM_VALIDATION_SEP_DR_FINAL = VALIDATION_SEP_DR_FINAL_GO
UPSTREAM_CONSTITUTION_DR_FINAL = CONSTITUTION_DR_FINAL_GO
UPSTREAM_HEALTH_POST_DR_FINAL = HEALTH_POST_DR_FINAL_GO

FINAL_DECISION_GO = "MIDPLATFORM_DECISION_CENTER_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_DECISION_CENTER_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Decision-Center-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Decision-Center-Planning-Issue-Review-v1-001"

DECISION_CENTER_DUTIES: Tuple[str, ...] = (
    "consume constitution constraints",
    "consume domain standard refs",
    "consume validation results",
    "consume health signals",
    "consume whitebox visibility",
    "consume evidence confidence",
    "consume task context",
    "consume failure route / issue trace / violation report",
    "emit decision_candidate later",
    "decide allow / block / hold / degrade / reobserve / escalate later",
)

DECISION_CENTER_NOT: Tuple[str, ...] = (
    "Constitution author",
    "Validation executor",
    "Health metric author",
    "Whitebox runtime",
    "Provider runtime",
    "Model runtime",
    "User output plane",
    "Memory writer",
    "WorldModel writer",
)

INPUT_CONTRACT_FIELDS: Tuple[str, ...] = (
    "decision_request_id",
    "source_candidate_refs",
    "evidence_pack_refs",
    "validation_result_refs",
    "health_signal_refs",
    "constitution_constraint_refs",
    "domain_standard_refs",
    "whitebox_visibility_refs",
    "task_context_ref",
    "uncertainty_ref",
    "issue_trace_refs",
    "violation_report_refs",
    "source_chain",
    "ttl",
    "candidate_only",
)

OUTPUT_CONTRACT_FIELDS: Tuple[str, ...] = (
    "decision_candidate_id",
    "decision_type",
    "decision_scope",
    "input_refs",
    "rationale_refs",
    "evidence_refs",
    "validation_refs",
    "health_refs",
    "constitution_refs",
    "selected_action",
    "blocked_reason",
    "escalation_reason",
    "uncertainty_level",
    "downstream_allowed_targets",
    "candidate_only",
    "task_response_generation_allowed",
    "user_output_allowed",
    "memory_write_allowed",
    "world_model_write_allowed",
)

DECISION_ACTIONS: Tuple[str, ...] = (
    "allow_candidate_forward",
    "block_candidate",
    "hold_candidate",
    "request_more_evidence",
    "request_reobserve",
    "degrade_mode_candidate",
    "fallback_candidate",
    "escalate_to_hive_later",
    "escalate_to_owner_later",
    "emit_issue_trace_candidate",
    "emit_violation_report_candidate",
    "reject_candidate",
)

PRIORITY_LAYERS: Tuple[Dict[str, Any], ...] = (
    {"priority": 1, "layer": "General Constitution"},
    {
        "priority": 2,
        "layer": "Safety / survival / privacy / fact admission / user output constraints",
    },
    {"priority": 3, "layer": "Domain Constitution"},
    {"priority": 4, "layer": "Domain Standard"},
    {"priority": 5, "layer": "Validation result"},
    {"priority": 6, "layer": "Health signal / system pressure"},
    {"priority": 7, "layer": "Evidence confidence"},
    {"priority": 8, "layer": "Task context"},
    {"priority": 9, "layer": "User preference"},
)

CONFLICT_RULES: Tuple[str, ...] = (
    "constitution block overrides task request",
    "validation fail overrides candidate forward",
    "severe health pressure can hold/degrade",
    "missing evidence triggers hold/request_more_evidence",
    "low confidence triggers reobserve or hold",
    "violation triggers block/escalate",
    "user preference cannot override constitution/validation/safety",
)

FAILURE_ESCALATION_ROUTES: Tuple[Dict[str, str], ...] = (
    {"trigger": "validation fail", "route": "hold/block + issue_trace"},
    {"trigger": "boundary violation", "route": "violation_report + escalation"},
    {"trigger": "provider failure", "route": "factory/harness issue trace"},
    {"trigger": "missing evidence", "route": "evidence_request_candidate"},
    {"trigger": "health pressure", "route": "degrade/hold"},
    {"trigger": "repeated failure", "route": "constitution_review_candidate later"},
    {"trigger": "severe violation", "route": "Hive escalation later"},
)

RUNTIME_BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "decision_center_runtime_enabled_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "validation_runtime_enabled_now",
    "whitebox_runtime_enabled_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Decision Center Planning GO ≠ decision runtime enabled",
    "decision_candidate contract ≠ decision executed",
    "allow action planned ≠ task_response generated",
    "decision center planned ≠ user output allowed",
    "health consumption planned ≠ health metric defined",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("decision_center_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "decision_center_runtime_enabled_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "user_facing_output_generated_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "validation_runtime_enabled_now",
    "whitebox_runtime_enabled_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_decision_center_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_decision_center_planning_v1(
    *,
    midplatform_core_architecture_resume_root: str,
    midplatform_whitebox_inspection_integration_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    health_management_layer_integration_post_dryrun_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    core_root = Path(midplatform_core_architecture_resume_root).expanduser().resolve()
    whitebox_root = Path(
        midplatform_whitebox_inspection_integration_dryrun_and_review_root
    ).expanduser().resolve()
    val_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    const_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()
    health_root = Path(
        health_management_layer_integration_post_dryrun_review_root
    ).expanduser().resolve()

    core_sm = _try_read_json(core_root / "summary.json") or {}
    core_vr = _try_read_json(core_root / "verifier_report.json") or {}
    core_decision = _load_or_empty(core_root, "midplatform_core_architecture_resume_decision_v1.json")
    whitebox_vr = _try_read_json(whitebox_root / "verifier_report.json") or {}
    whitebox_sm = _try_read_json(whitebox_root / "summary.json") or {}
    val_vr = _try_read_json(val_root / "verifier_report.json") or {}
    val_sm = _try_read_json(val_root / "summary.json") or {}
    const_vr = _try_read_json(const_root / "verifier_report.json") or {}
    const_sm = _try_read_json(const_root / "summary.json") or {}
    health_vr = _try_read_json(health_root / "verifier_report.json") or {}
    health_sm = _try_read_json(health_root / "summary.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_core_resume_root": str(core_root),
        "upstream_whitebox_dryrun_root": str(whitebox_root),
        "upstream_validation_separation_dryrun_root": str(val_root),
        "upstream_constitution_explanation_dryrun_root": str(const_root),
        "upstream_health_post_dryrun_root": str(health_root),
        "output_root": str(out_root),
    }

    if core_vr.get("verifier") != "GO":
        blockers.append("Midplatform Core Architecture Resume verifier must be GO")
    if core_sm.get("final_decision") != UPSTREAM_CORE_RESUME_FINAL:
        blockers.append("core resume final_decision mismatch")
    if core_sm.get("recommended_next_phase") != UPSTREAM_CORE_RESUME_NEXT:
        blockers.append("core resume recommended_next_phase mismatch")
    if core_decision.get("ocr_local_check_sealed") is not True:
        blockers.append("OCR local check must be sealed")
    if core_decision.get("whitebox_integration_sealed") is not True:
        blockers.append("whitebox integration must be sealed")
    if whitebox_vr.get("verifier") != "GO":
        blockers.append("Whitebox Integration DryRunAndReview must be GO")
    if whitebox_sm.get("final_decision") != UPSTREAM_WHITEBOX_DR_FINAL:
        blockers.append("whitebox dryrun final_decision mismatch")
    if val_vr.get("verifier") != "GO":
        blockers.append("Validation Engineering Separation must be GO")
    if val_sm.get("final_decision") != UPSTREAM_VALIDATION_SEP_DR_FINAL:
        blockers.append("validation separation final_decision mismatch")
    if const_vr.get("verifier") != "GO":
        blockers.append("Constitution Governance Explanation must be GO")
    if const_sm.get("final_decision") != UPSTREAM_CONSTITUTION_DR_FINAL:
        blockers.append("constitution explanation final_decision mismatch")
    if health_vr.get("verifier") != "GO":
        blockers.append("Health Management Layer Integration Post DryRun must be GO")
    if health_sm.get("final_decision") != UPSTREAM_HEALTH_POST_DR_FINAL:
        blockers.append("health post dryrun final_decision mismatch")

    input_ok = len(blockers) == 0

    resume_input_review = {
        "review_id": "midplatform_core_resume_input_review_v1",
        "core_resume_verifier": core_vr.get("verifier"),
        "core_resume_final_decision": core_sm.get("final_decision"),
        "core_resume_next_phase": core_sm.get("recommended_next_phase"),
        "ocr_local_check_sealed": core_decision.get("ocr_local_check_sealed"),
        "whitebox_absorption_complete": core_decision.get("whitebox_integration_sealed"),
        "validation_engineering_remains_gatekeeper": True,
        "constitution_remains_rule_source": True,
        "health_remains_pressure_signal_source": True,
        "health_metric_definition_status": health_sm.get("health_metric_definition_status"),
        "upstream_roots": {
            "core_resume": str(core_root),
            "whitebox_dryrun": str(whitebox_root),
            "validation_separation": str(val_root),
            "constitution_explanation": str(const_root),
            "health_post_dryrun": str(health_root),
        },
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    role_definition = {
        "definition_id": "decision_center_role_definition_v1",
        "decision_center_duties": list(DECISION_CENTER_DUTIES),
        "decision_center_is_not": list(DECISION_CENTER_NOT),
        "emit_decision_candidate_later": True,
        "runtime_enabled_now": False,
        **meta,
    }

    input_contract = {
        "contract_id": "decision_center_input_contract_v1",
        "required_fields": list(INPUT_CONTRACT_FIELDS),
        "candidate_only": True,
        "field_definitions": {f: {"required": True} for f in INPUT_CONTRACT_FIELDS},
        **meta,
    }

    output_contract = {
        "contract_id": "decision_center_output_contract_v1",
        "output_type": "decision_candidate",
        "required_fields": list(OUTPUT_CONTRACT_FIELDS),
        "defaults": {
            "candidate_only": True,
            "task_response_generation_allowed": False,
            "user_output_allowed": False,
            "memory_write_allowed": False,
            "world_model_write_allowed": False,
        },
        **meta,
    }

    action_taxonomy = {
        "taxonomy_id": "decision_action_taxonomy_v1",
        "actions": list(DECISION_ACTIONS),
        "action_count": len(DECISION_ACTIONS),
        **meta,
    }

    priority_conflict = {
        "policy_id": "decision_priority_and_conflict_policy_v1",
        "priority_layers": list(PRIORITY_LAYERS),
        "conflict_rules": list(CONFLICT_RULES),
        "user_preference_cannot_override_safety": True,
        **meta,
    }

    constitution_consumption = {
        "plan_id": "constitution_constraint_consumption_plan_v1",
        "consumes_rule_refs_not_writes_rules": True,
        "general_constitution_highest_priority": True,
        "personalized_constitution_overlay_only": True,
        "personalized_cannot_relax_boundaries": True,
        "constitution_conflict_conservative_decision": True,
        **meta,
    }

    validation_consumption = {
        "plan_id": "validation_result_consumption_plan_v1",
        "validation_pass_allows_forward_if_no_higher_block": True,
        "validation_fail_triggers_block_hold_issue_trace": True,
        "boundary_violation_triggers_violation_report_escalation": True,
        "no_validation_result_triggers_hold_request_validation": True,
        "decision_center_does_not_execute_validation_gates": True,
        **meta,
    }

    health_consumption = {
        "plan_id": "health_signal_consumption_plan_v1",
        "health_signal_is_pressure_status_context": True,
        "no_numeric_health_score_invented": True,
        "health_metric_definition_status": health_sm.get("health_metric_definition_status", "reserved_not_defined"),
        "severe_health_pressure_may_hold_degrade": True,
        "health_does_not_auto_authorize_execution": True,
        "health_does_not_replace_constitution_validation": True,
        **meta,
    }

    whitebox_consumption = {
        "plan_id": "whitebox_visibility_consumption_plan_v1",
        "whitebox_provides_explainability_visibility": True,
        "whitebox_does_not_decide": True,
        "node_level_evidence_cannot_define_global_status": True,
        "decision_center_may_use_as_rationale_ref": True,
        **meta,
    }

    evidence_consumption = {
        "plan_id": "evidence_confidence_consumption_plan_v1",
        "evidence_completeness_required": True,
        "source_chain_required": True,
        "low_confidence_leads_reobserve_hold": True,
        "stale_evidence_leads_request_more_evidence": True,
        "missing_evidence_blocks_forward_unless_safe_default": True,
        **meta,
    }

    task_context_consumption = {
        "plan_id": "task_context_consumption_plan_v1",
        "task_context_influences_action_preference": True,
        "task_context_cannot_override_constitution_validation": True,
        "no_task_context_blocks_task_response_generation": True,
        "baseline_safety_operates_independently_later": True,
        **meta,
    }

    failure_escalation = {
        "plan_id": "failure_route_and_escalation_decision_plan_v1",
        "routes": list(FAILURE_ESCALATION_ROUTES),
        **meta,
    }

    task_response_boundary = {
        "plan_id": "decision_to_task_response_boundary_plan_v1",
        "decision_candidate_not_task_response_candidate": True,
        "allow_candidate_forward_not_user_output": True,
        "task_response_requires_separate_integration_phase": True,
        "user_output_requires_output_plane_later": True,
        "memory_world_model_requires_separate_write_policy": True,
        **meta,
    }

    runtime_boundary = {
        "matrix_id": "decision_center_runtime_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in RUNTIME_BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "decision_center_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate decision_center_model_candidate",
            "generate sample decision_request_candidate",
            "generate sample decision_candidate",
            "verify input/output contract",
            "verify priority and conflict handling",
            "verify validation/health/constitution/whitebox/evidence/task context consumption",
            "verify decision ≠ task_response ≠ user_output",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok

    planning_decision = {
        "decision_id": "decision_center_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "decision_center_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_not_runtime": True,
        "decision_center_is_midplatform_arbitration_center": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "decision_center_planning_policy": policy,
        "midplatform_core_resume_input_review": resume_input_review,
        "decision_center_role_definition": role_definition,
        "decision_center_input_contract": input_contract,
        "decision_center_output_contract": output_contract,
        "decision_action_taxonomy": action_taxonomy,
        "decision_priority_and_conflict_policy": priority_conflict,
        "constitution_constraint_consumption_plan": constitution_consumption,
        "validation_result_consumption_plan": validation_consumption,
        "health_signal_consumption_plan": health_consumption,
        "whitebox_visibility_consumption_plan": whitebox_consumption,
        "evidence_confidence_consumption_plan": evidence_consumption,
        "task_context_consumption_plan": task_context_consumption,
        "failure_route_and_escalation_decision_plan": failure_escalation,
        "decision_to_task_response_boundary_plan": task_response_boundary,
        "decision_center_runtime_boundary_matrix": runtime_boundary,
        "decision_center_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "decision_center_planning_decision": planning_decision,
        "summary": summary,
    }


def _load_or_empty(root: Path, fname: str) -> Dict[str, Any]:
    data = _try_read_json(root / fname)
    return data if isinstance(data, dict) else {}
