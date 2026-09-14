# -*- coding: utf-8 -*-
"""Midplatform Task Response Candidate Integration Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_candidate_evidence_flow_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FLOW_DR_FINAL_GO,
    NEXT_PHASE_GO as FLOW_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_core_architecture_resume_v1 import (
    FINAL_DECISION_GO as CORE_RESUME_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_DR_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_planning_v1 import (
    DECISION_ACTIONS,
)
from capabilities.governance.midplatform_module_definition_template_planning_v1 import (
    FINAL_DECISION_GO as TEMPLATE_PLANNING_FINAL_GO,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Task-Response-Candidate-Integration-Planning-v1-001"
SCOPE = "task_response_candidate_integration_planning_only"
SOURCE_CHAIN = "midplatform_task_response_candidate_integration_planning_v1"

UPSTREAM_FLOW_DR_FINAL = FLOW_DR_FINAL_GO
UPSTREAM_FLOW_DR_NEXT = FLOW_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_RESPONSE_CANDIDATE_INTEGRATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_TASK_RESPONSE_CANDIDATE_INTEGRATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Task-Response-Candidate-Integration-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Response-Candidate-Integration-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "decision_candidate ≠ task_response_candidate ≠ user_output_candidate ≠ final broadcast/display"
)

DECISION_CANDIDATE_INTAKE_FIELDS: Tuple[str, ...] = (
    "decision_candidate_id",
    "decision_type",
    "decision_scope",
    "selected_action",
    "input_refs",
    "rationale_refs",
    "evidence_refs",
    "validation_refs",
    "health_refs",
    "constitution_refs",
    "whitebox_refs",
    "blocked_reason",
    "hold_reason",
    "degradation_reason",
    "escalation_reason",
    "uncertainty_level",
    "downstream_allowed_targets",
    "candidate_only",
)

TASK_RESPONSE_OUTPUT_FIELDS: Tuple[str, ...] = (
    "task_response_candidate_id",
    "source_decision_candidate_ref",
    "response_type",
    "response_scope",
    "response_intent",
    "response_payload_candidate",
    "rationale_refs",
    "evidence_refs",
    "validation_refs",
    "health_refs",
    "constitution_refs",
    "whitebox_refs",
    "uncertainty_level",
    "user_output_allowed",
    "speech_output_allowed",
    "memory_write_allowed",
    "world_model_write_allowed",
    "task_state_commit_allowed",
    "candidate_only",
    "fact_status",
)

RESPONSE_ASSEMBLY_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"selected_action": "allow_candidate_forward", "assembly": "assemble_task_response_candidate_later"},
    {"selected_action": "block_candidate", "assembly": "assemble_block_response_candidate_later"},
    {"selected_action": "hold_candidate", "assembly": "assemble_hold_response_candidate_later"},
    {"selected_action": "request_more_evidence", "assembly": "assemble_evidence_request_response_candidate_later"},
    {"selected_action": "request_validation", "assembly": "assemble_validation_request_response_candidate_later"},
    {"selected_action": "request_reobserve", "assembly": "assemble_reobserve_response_candidate_later"},
    {"selected_action": "degrade_mode_candidate", "assembly": "assemble_degraded_response_candidate_later"},
    {"selected_action": "fallback_candidate", "assembly": "assemble_fallback_response_candidate_later"},
    {"selected_action": "escalate_to_hive_later", "assembly": "assemble_escalation_candidate_later"},
    {"selected_action": "escalate_to_owner_later", "assembly": "assemble_owner_escalation_candidate_later"},
    {"selected_action": "emit_issue_trace_candidate", "assembly": "preserve_issue_trace_ref"},
    {"selected_action": "emit_violation_report_candidate", "assembly": "preserve_violation_report_ref"},
    {"selected_action": "reject_candidate", "assembly": "assemble_reject_response_candidate_later"},
)

FAILURE_ESCALATION_RESPONSES: Tuple[Dict[str, str], ...] = (
    {"trigger": "blocked decision", "response": "block response candidate"},
    {"trigger": "hold decision", "response": "hold response candidate"},
    {"trigger": "missing evidence", "response": "evidence request response candidate"},
    {"trigger": "low confidence", "response": "reobserve response candidate"},
    {"trigger": "health pressure", "response": "degraded response candidate"},
    {"trigger": "validation fail", "response": "validation failure response candidate"},
    {"trigger": "boundary violation", "response": "violation response candidate"},
    {"trigger": "severe issue", "response": "escalation response candidate"},
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "decision_executed_now",
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "user_facing_output_generated_now",
    "speech_gate_invoked_now",
    "tts_invoked_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Task Response Candidate Integration Planning GO ≠ task_response generated",
    "task_response_candidate contract ≠ user output allowed",
    "response assembly plan ≠ action executed",
    "speech boundary planned ≠ TTS allowed",
    "memory/worldmodel boundary planned ≠ fact write allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("task_response_candidate_integration_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "task_response_runtime_enabled_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "user_facing_output_generated_now",
    "speech_gate_invoked_now",
    "tts_invoked_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "template_id": TEMPLATE_ID,
        "core_chain_boundary": CORE_CHAIN_BOUNDARY,
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


def _task_response_module_definition() -> Dict[str, Any]:
    return {
        "definition_id": "task_response_candidate_module_definition_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {
            "module_id": "midplatform_task_response_candidate_integration_v1",
            "module_type": "midplatform_response_assembly_module",
            "role": "decision_candidate_to_task_response_candidate_assembly",
            "system_layer": "Assembly",
        },
        "upstream_sources": {
            "upstream_modules": [
                "midplatform_decision_center_v1",
                "midplatform_candidate_evidence_flow_integration_v1",
            ],
            "upstream_object_types": [
                "decision_candidate",
                "source_candidate_refs",
                "evidence_refs",
                "validation_refs",
                "health_refs",
                "whitebox_refs",
                "rationale_refs",
            ],
            "required_inputs": list(DECISION_CANDIDATE_INTAKE_FIELDS),
            "optional_inputs": ["task_context_ref"],
            "forbidden_inputs": [
                "user_output_directive",
                "speech_request",
                "memory_write_directive",
                "task_state_commit_directive",
            ],
        },
        "downstream_targets": {
            "downstream_modules": [
                "output_plane_later",
                "speech_gate_later",
                "task_state_later",
            ],
            "downstream_object_types": ["task_response_candidate"],
            "allowed_outputs": ["task_response_candidate"],
            "forbidden_outputs": [
                "user_output_candidate",
                "speech_output",
                "memory_fact",
                "world_model_fact",
                "task_state_commit",
            ],
        },
        "input_contract": {
            "input_contract": "decision_candidate_intake_contract_v1",
            "source_chain": "preserved_from_decision_candidate",
            "evidence_ref": "preserved",
            "ttl": "preserved",
            "confidence": "preserved_as_uncertainty_level",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": "assemble task_response_candidate from decision_candidate",
            "allowed_transformation": [
                "map selected_action to response assembly rule",
                "preserve refs and uncertainty",
                "attach response_type and response_intent",
            ],
            "forbidden_transformation": [
                "execute decision",
                "modify decision_candidate",
                "invoke TTS or speech gate",
                "write memory or world model",
                "commit task state",
                "invoke provider",
                "generate user output",
            ],
            "arbitration_allowed": False,
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": "task_response_candidate_output_contract_v1",
            "output_object_type": "task_response_candidate",
            "decision_refs": "source_decision_candidate_ref",
            "evidence_refs": "preserved",
            "validation_refs": "preserved",
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": {
            "module_principles": [
                "decision_candidate ≠ task_response_candidate",
                "task_response_candidate ≠ user_output_candidate",
                "assembly candidate-only; action not executed",
            ],
            "priority_policy": "preserve decision refs and uncertainty",
            "conflict_policy": "do not override decision_candidate",
            "fallback_policy": "map fallback action to fallback response candidate later",
            "rollback_policy": "assembly does not commit state",
        },
        "external_constraints": {
            "constitution_constraints": "output constitution required later for user output",
            "domain_standard_constraints": "preserved from decision_candidate",
            "validation_gate_constraints": "validation refs preserved not re-executed",
            "health_signal_constraints": "health refs preserved as context",
            "whitebox_visibility_constraints": "rationale refs preserved",
            "decision_center_constraints": "consume decision_candidate only; do not re-decide",
        },
        "runtime_boundaries": {
            "runtime_enabled_now": False,
            "write_allowed_now": False,
            "provider_invocation_allowed_now": False,
            "user_output_allowed_now": False,
            "memory_allowed_now": False,
            "world_model_allowed_now": False,
        },
        "failure_and_traceability": {
            "failure_route": "blocked/hold/evidence/validation/violation → mapped response candidate",
            "issue_trace": "preserve_issue_trace_ref from decision",
            "violation_report": "preserve_violation_report_ref from decision",
            "escalation_path": "escalation candidate later; no Hive submit now",
            "audit_required": True,
        },
    }


def run_midplatform_task_response_candidate_integration_planning_v1(
    *,
    midplatform_candidate_evidence_flow_integration_dryrun_and_review_root: str,
    midplatform_decision_center_module_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    midplatform_core_architecture_resume_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    flow_dr_root = Path(
        midplatform_candidate_evidence_flow_integration_dryrun_and_review_root
    ).expanduser().resolve()
    dc_dr_root = Path(
        midplatform_decision_center_module_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()
    core_root = Path(midplatform_core_architecture_resume_root).expanduser().resolve()

    flow_dr_sm = _try_read_json(flow_dr_root / "summary.json") or {}
    flow_dr_vr = _try_read_json(flow_dr_root / "verifier_report.json") or {}
    dc_dr_vr = _try_read_json(dc_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}
    core_vr = _try_read_json(core_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_flow_dryrun_root": str(flow_dr_root),
        "upstream_decision_center_dryrun_root": str(dc_dr_root),
        "upstream_template_planning_root": str(template_root),
        "upstream_core_resume_root": str(core_root),
        "output_root": str(out_root),
    }

    if flow_dr_vr.get("verifier") != "GO":
        blockers.append("Candidate Evidence Flow DryRunAndReview verifier must be GO")
    if flow_dr_sm.get("final_decision") != UPSTREAM_FLOW_DR_FINAL:
        blockers.append("flow dryrun final_decision mismatch")
    if flow_dr_sm.get("recommended_next_phase") != UPSTREAM_FLOW_DR_NEXT:
        blockers.append("flow dryrun recommended_next_phase mismatch")
    if dc_dr_vr.get("verifier") != "GO":
        blockers.append("Decision Center Module DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")
    if core_vr.get("verifier") != "GO":
        blockers.append("Core Architecture Resume must be GO")

    module_def = _task_response_module_definition()
    module_valid, module_issues = validate_module_definition(module_def)
    if not module_valid:
        blockers.extend(module_issues)

    input_ok = len(blockers) == 0

    flow_input_review = {
        "review_id": "upstream_candidate_evidence_flow_input_review_v1",
        "flow_dryrun_verifier": flow_dr_vr.get("verifier"),
        "flow_dryrun_final": flow_dr_sm.get("final_decision"),
        "decision_request_chain_closed": True,
        "decision_center_dryrun_go": dc_dr_vr.get("verifier") == "GO",
        "decision_candidate_not_task_response": True,
        "task_response_not_user_output": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    decision_intake = {
        "contract_id": "decision_candidate_intake_contract_v1",
        "required_fields": list(DECISION_CANDIDATE_INTAKE_FIELDS),
        "candidate_only": True,
        "does_not_modify_decision_candidate": True,
        **meta,
    }

    task_response_output = {
        "contract_id": "task_response_candidate_output_contract_v1",
        "output_type": "task_response_candidate",
        "required_fields": list(TASK_RESPONSE_OUTPUT_FIELDS),
        "defaults": {
            "user_output_allowed": False,
            "speech_output_allowed": False,
            "memory_write_allowed": False,
            "world_model_write_allowed": False,
            "task_state_commit_allowed": False,
            "candidate_only": True,
            "fact_status": "not_fact",
        },
        "not_user_output": True,
        "not_speech": True,
        **meta,
    }

    assembly_rules = {
        "plan_id": "response_assembly_rule_plan_v1",
        "mappings": list(RESPONSE_ASSEMBLY_MAPPINGS),
        "mapping_count": len(RESPONSE_ASSEMBLY_MAPPINGS),
        "assembled_later_not_now": True,
        **meta,
    }

    action_mapping = {
        "plan_id": "response_action_mapping_plan_v1",
        "action_mapping_does_not_execute_action": True,
        "response_assembly_candidate_only": True,
        "escalation_does_not_submit_hive_now": True,
        "evidence_request_does_not_query_provider_now": True,
        "reobserve_does_not_invoke_camera_model_now": True,
        "fallback_does_not_execute_fallback_now": True,
        **meta,
    }

    preservation = {
        "plan_id": "uncertainty_and_evidence_preservation_plan_v1",
        "uncertainty_level_preserved": True,
        "source_chain_preserved": True,
        "evidence_refs_preserved": True,
        "validation_refs_preserved": True,
        "health_refs_preserved": True,
        "constitution_refs_preserved": True,
        "whitebox_refs_preserved": True,
        "rationale_refs_preserved": True,
        "no_evidence_mutation": True,
        **meta,
    }

    safety_boundary = {
        "plan_id": "safety_and_constitution_output_boundary_plan_v1",
        "task_response_requires_output_constitution_later": True,
        "user_output_requires_output_plane_later": True,
        "speech_requires_speech_gate_voice_plane_later": True,
        "safety_constraints_remain_binding": True,
        "user_preference_cannot_override_constitution_validation": True,
        **meta,
    }

    speech_boundary = {
        "plan_id": "speech_output_boundary_plan_v1",
        "task_response_candidate_is_not_speech": True,
        "speech_request_generated_now": False,
        "speech_gate_invoked_now": False,
        "tts_invoked_now": False,
        "voice_output_plane_invoked_now": False,
        **meta,
    }

    memory_wm_boundary = {
        "plan_id": "memory_worldmodel_write_boundary_plan_v1",
        "no_fact_admission_here": True,
        "no_memory_write": True,
        "no_world_model_write": True,
        "fact_status_remains_not_fact": True,
        "write_requires_separate_policy_later": True,
        **meta,
    }

    task_state_boundary = {
        "plan_id": "task_state_commit_boundary_plan_v1",
        "task_response_does_not_commit_task_state": True,
        "task_state_commit_allowed": False,
        "task_state_update_requires_separate_integration_later": True,
        **meta,
    }

    failure_escalation = {
        "plan_id": "failure_and_escalation_response_plan_v1",
        "routes": list(FAILURE_ESCALATION_RESPONSES),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "task_response_candidate_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "task_response_candidate_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate task_response_integration_model_candidate",
            "generate sample decision_candidate intake",
            "generate sample task_response_candidate",
            "verify selected_action to response candidate mapping",
            "verify evidence/rationale/uncertainty preservation",
            "verify task_response_candidate ≠ user_output/speech/memory/worldmodel/task_state",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok and module_valid

    planning_decision = {
        "decision_id": "task_response_candidate_integration_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "main_chain_defined": [
            "candidate/evidence/validation/health/whitebox",
            "→ decision_request_candidate",
            "→ decision_candidate",
            "→ task_response_candidate",
        ],
        **meta,
    }

    policy = {
        "policy_id": "task_response_candidate_integration_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "assembly_not_user_output": True,
        "planning_not_runtime": True,
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
        "task_response_candidate_integration_planning_policy": policy,
        "upstream_candidate_evidence_flow_input_review": flow_input_review,
        "task_response_candidate_module_definition": module_def,
        "decision_candidate_intake_contract": decision_intake,
        "task_response_candidate_output_contract": task_response_output,
        "response_assembly_rule_plan": assembly_rules,
        "response_action_mapping_plan": action_mapping,
        "uncertainty_and_evidence_preservation_plan": preservation,
        "safety_and_constitution_output_boundary_plan": safety_boundary,
        "speech_output_boundary_plan": speech_boundary,
        "memory_worldmodel_write_boundary_plan": memory_wm_boundary,
        "task_state_commit_boundary_plan": task_state_boundary,
        "failure_and_escalation_response_plan": failure_escalation,
        "task_response_candidate_boundary_matrix": boundary_matrix,
        "task_response_candidate_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "task_response_candidate_integration_planning_decision": planning_decision,
        "summary": summary,
    }
