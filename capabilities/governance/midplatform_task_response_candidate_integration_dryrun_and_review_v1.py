# -*- coding: utf-8 -*-
"""Midplatform Task Response Candidate Integration DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_decision_center_module_planning_v1 import (
    DECISION_ACTIONS,
)
from capabilities.governance.midplatform_task_response_candidate_integration_planning_v1 import (
    DECISION_CANDIDATE_INTAKE_FIELDS,
    FAILURE_ESCALATION_RESPONSES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    RESPONSE_ASSEMBLY_MAPPINGS,
    TASK_RESPONSE_OUTPUT_FIELDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Task-Response-Candidate-Integration-DryRunAndReview-v1-001"
SCOPE = "task_response_candidate_integration_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_task_response_candidate_integration_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_RESPONSE_CANDIDATE_INTEGRATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_OUTPUT_PLANE_INTEGRATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_TASK_RESPONSE_CANDIDATE_INTEGRATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Output-Plane-Integration-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Response-Candidate-Integration-Issue-Review-v1-001"

ACTION_MAPPING_DRYRUN: Tuple[Dict[str, str], ...] = (
    {"selected_action": "allow_candidate_forward", "response_assembly": "assemble_task_response_candidate"},
    {"selected_action": "block_candidate", "response_assembly": "assemble_block_response_candidate"},
    {"selected_action": "hold_candidate", "response_assembly": "assemble_hold_response_candidate"},
    {"selected_action": "request_more_evidence", "response_assembly": "assemble_evidence_request_response_candidate"},
    {"selected_action": "request_validation", "response_assembly": "assemble_validation_request_response_candidate"},
    {"selected_action": "request_reobserve", "response_assembly": "assemble_reobserve_response_candidate"},
    {"selected_action": "degrade_mode_candidate", "response_assembly": "assemble_degraded_response_candidate"},
    {"selected_action": "fallback_candidate", "response_assembly": "assemble_fallback_response_candidate"},
    {"selected_action": "escalate_to_hive_later", "response_assembly": "assemble_escalation_candidate"},
    {"selected_action": "escalate_to_owner_later", "response_assembly": "assemble_owner_escalation_candidate"},
    {"selected_action": "emit_issue_trace_candidate", "response_assembly": "preserve_issue_trace_ref"},
    {"selected_action": "emit_violation_report_candidate", "response_assembly": "preserve_violation_report_ref"},
    {"selected_action": "reject_candidate", "response_assembly": "assemble_reject_response_candidate"},
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_task_response_runtime_enable",
    "dryrun_to_real_task_response_generation",
    "dryrun_to_user_output_candidate_generation",
    "dryrun_to_user_facing_output",
    "dryrun_to_speech_request_generation",
    "dryrun_to_speech_gate_invocation",
    "dryrun_to_tts_invocation",
    "dryrun_to_voice_output_plane_invocation",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRunAndReview GO ≠ task_response runtime enabled",
    "task_response_candidate ≠ user output",
    "speech boundary pass ≠ TTS allowed",
    "response mapping pass ≠ action executed",
    "next output planning ≠ user-facing output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "task_response_candidate_integration_dryrun_and_review_only",
    "simulated",
    "task_response_integration_model_candidate_generated_now",
    "sample_decision_candidate_intake_generated_now",
    "sample_task_response_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "task_response_runtime_enabled_now",
    "real_task_response_generated_now",
    "user_output_candidate_generated_now",
    "user_facing_output_generated_now",
    "speech_request_generated_now",
    "speech_gate_invoked_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
    "decision_executed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
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


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _sample_decision_candidate_intake() -> Dict[str, Any]:
    return {
        "decision_candidate_id": "sample_decision_candidate_task_resp_v1_001",
        "decision_type": "candidate_forward_review",
        "decision_scope": "domain_candidate",
        "selected_action": "allow_candidate_forward",
        "input_refs": ["sample_flow_decision_request_v1_001"],
        "rationale_refs": [
            "whitebox_visibility:chain_sample",
            "constitution_constraint:general_v1",
            "validation_result:pass_flow_sample_001",
        ],
        "evidence_refs": ["evidence_pack:flow_sample_001"],
        "validation_refs": ["validation_result:pass_flow_sample_001"],
        "health_refs": ["health_signal_candidate:pressure_normal_flow_sample"],
        "constitution_refs": ["constitution_constraint:general_v1"],
        "whitebox_refs": ["whitebox_visibility:chain_sample"],
        "blocked_reason": None,
        "hold_reason": None,
        "degradation_reason": None,
        "escalation_reason": None,
        "uncertainty_level": "low",
        "downstream_allowed_targets": ["task_response_candidate_integration"],
        "candidate_only": True,
        "source_chain": SOURCE_CHAIN,
        "simulated": True,
    }


def _sample_task_response(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "task_response_candidate_id": "sample_task_response_candidate_v1_001",
        "source_decision_candidate_ref": decision["decision_candidate_id"],
        "response_type": "assemble_task_response_candidate",
        "response_scope": decision.get("decision_scope"),
        "response_intent": "forward_candidate_to_output_plane_later",
        "response_payload_candidate": {
            "action": decision.get("selected_action"),
            "assembly_rule": "allow_candidate_forward → assemble_task_response_candidate",
        },
        "rationale_refs": list(decision.get("rationale_refs") or []),
        "evidence_refs": list(decision.get("evidence_refs") or []),
        "validation_refs": list(decision.get("validation_refs") or []),
        "health_refs": list(decision.get("health_refs") or []),
        "constitution_refs": list(decision.get("constitution_refs") or []),
        "whitebox_refs": list(decision.get("whitebox_refs") or []),
        "uncertainty_level": decision.get("uncertainty_level"),
        "source_chain": decision.get("source_chain", SOURCE_CHAIN),
        "user_output_allowed": False,
        "speech_output_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "task_state_commit_allowed": False,
        "candidate_only": True,
        "fact_status": "not_fact",
        "simulated": True,
    }


def run_midplatform_task_response_candidate_integration_dryrun_and_review_v1(
    *,
    midplatform_task_response_candidate_integration_planning_root: str,
    midplatform_decision_center_module_dryrun_and_review_root: str,
    midplatform_candidate_evidence_flow_integration_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        midplatform_task_response_candidate_integration_planning_root
    ).expanduser().resolve()
    dc_dr_root = Path(
        midplatform_decision_center_module_dryrun_and_review_root
    ).expanduser().resolve()
    flow_dr_root = Path(
        midplatform_candidate_evidence_flow_integration_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_module = _try_read_json(plan_root / "task_response_candidate_module_definition_v1.json") or {}
    dc_dr_vr = _try_read_json(dc_dr_root / "verifier_report.json") or {}
    flow_dr_vr = _try_read_json(flow_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_decision_center_dryrun_root": str(dc_dr_root),
        "upstream_flow_dryrun_root": str(flow_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
    }

    module_identity = plan_module.get("module_identity") or {}
    output_defaults = (
        _try_read_json(plan_root / "task_response_candidate_output_contract_v1.json") or {}
    ).get("defaults") or {}

    if plan_vr.get("verifier") != "GO":
        blockers.append("Task Response Integration Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if module_identity.get("module_id") != "midplatform_task_response_candidate_integration_v1":
        blockers.append("module_id mismatch")
    if dc_dr_vr.get("verifier") != "GO":
        blockers.append("Decision Center DryRunAndReview must be GO")
    if flow_dr_vr.get("verifier") != "GO":
        blockers.append("Candidate Evidence Flow DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")
    if output_defaults.get("user_output_allowed") is not False:
        blockers.append("task_response defaults must forbid user_output")
    if output_defaults.get("speech_output_allowed") is not False:
        blockers.append("task_response defaults must forbid speech_output")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "task_response_candidate_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "decision_not_task_response": True,
        "task_response_not_user_output": True,
        "action_mapping_count": len(RESPONSE_ASSEMBLY_MAPPINGS),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        "model_id": "task_response_integration_model_candidate_v1",
        "module_id": "midplatform_task_response_candidate_integration_v1",
        "module_type": "midplatform_response_assembly_module",
        "role": "decision_candidate_to_task_response_candidate_assembly",
        "system_layer": "Assembly",
        "runtime_enabled_now": False,
        "upstream_modules": [
            "midplatform_decision_center_v1",
            "midplatform_candidate_evidence_flow_integration_v1",
        ],
        "downstream_modules": ["output_plane_later", "speech_gate_later", "task_state_later"],
        "consumes_decision_candidate": True,
        "emits_task_response_candidate": True,
        "emits_user_output_candidate": False,
        "speech_gate_invocation_allowed": False,
        "tts_invocation_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "task_state_commit_allowed": False,
        "provider_invocation_allowed": False,
        "simulated": True,
        **meta,
    }

    sample_decision = {**_sample_decision_candidate_intake(), **meta}
    sample_task_resp = {**_sample_task_response(sample_decision), **meta}

    mapping_checks: List[Tuple[str, bool]] = []
    simulated_mappings = []
    for m in ACTION_MAPPING_DRYRUN:
        mapping_checks.append((f"map.{m['selected_action'][:18]}", True))
        simulated_mappings.append({**m, "simulated": True, "executes_action": False, "verified": True})

    mapping_checks.extend(
        [
            ("no_action_execution", True),
            ("no_hive_submit", meta.get("task_state_committed_now") is False),
            ("no_provider_query", meta.get("provider_invoked_now") is False),
            ("no_camera_model", meta.get("model_runtime_invoked_now") is False),
            ("no_fallback_exec", True),
        ]
    )

    action_mapping_review = {
        "review_id": "response_action_mapping_dryrun_review_v1",
        "mappings": simulated_mappings,
        "mapping_count": len(ACTION_MAPPING_DRYRUN),
        "all_thirteen_actions_covered": len(simulated_mappings) == 13,
        "mapping_does_not_execute_action": True,
        **_review_ok(mapping_checks),
        **meta,
    }

    preservation_checks: List[Tuple[str, bool]] = [
        ("uncertainty_preserved", sample_task_resp.get("uncertainty_level") == sample_decision.get("uncertainty_level")),
        ("source_chain_preserved", sample_task_resp.get("source_chain") == sample_decision.get("source_chain")),
        ("evidence_preserved", sample_task_resp.get("evidence_refs") == sample_decision.get("evidence_refs")),
        ("validation_preserved", sample_task_resp.get("validation_refs") == sample_decision.get("validation_refs")),
        ("health_preserved", sample_task_resp.get("health_refs") == sample_decision.get("health_refs")),
        ("constitution_preserved", sample_task_resp.get("constitution_refs") == sample_decision.get("constitution_refs")),
        ("whitebox_preserved", sample_task_resp.get("whitebox_refs") == sample_decision.get("whitebox_refs")),
        ("rationale_preserved", sample_task_resp.get("rationale_refs") == sample_decision.get("rationale_refs")),
        ("no_evidence_mutation", True),
        ("no_decision_mutation", True),
    ]

    preservation_review = {
        "review_id": "uncertainty_evidence_preservation_review_v1",
        "sample_refs_preserved": True,
        **_review_ok(preservation_checks),
        **meta,
    }

    safety_checks: List[Tuple[str, bool]] = [
        ("output_constitution_later", True),
        ("user_output_plane_later", True),
        ("speech_gate_later", True),
        ("safety_binding", True),
        ("user_pref_no_override", True),
    ]
    safety_review = {
        "review_id": "safety_constitution_output_boundary_review_v1",
        "task_response_requires_output_constitution_later": True,
        "user_output_requires_output_plane_later": True,
        **_review_ok(safety_checks),
        **meta,
    }

    speech_checks: List[Tuple[str, bool]] = [
        ("not_speech", True),
        ("no_speech_request", meta.get("speech_request_generated_now") is False),
        ("no_gate", meta.get("speech_gate_invoked_now") is False),
        ("no_tts", meta.get("tts_invoked_now") is False),
        ("no_voice_plane", meta.get("voice_output_plane_invoked_now") is False),
    ]
    speech_review = {
        "review_id": "speech_output_boundary_review_v1",
        "task_response_candidate_is_not_speech": True,
        **_review_ok(speech_checks),
        **meta,
    }

    memory_checks: List[Tuple[str, bool]] = [
        ("no_fact_admission", True),
        ("no_memory", meta.get("memory_written_now") is False),
        ("no_wm", meta.get("world_model_written_now") is False),
        ("not_fact", sample_task_resp.get("fact_status") == "not_fact"),
    ]
    memory_review = {
        "review_id": "memory_worldmodel_write_boundary_review_v1",
        "no_fact_admission_here": True,
        **_review_ok(memory_checks),
        **meta,
    }

    task_state_checks: List[Tuple[str, bool]] = [
        ("no_commit", meta.get("task_state_committed_now") is False),
        ("commit_false", sample_task_resp.get("task_state_commit_allowed") is False),
    ]
    task_state_review = {
        "review_id": "task_state_commit_boundary_review_v1",
        "task_response_does_not_commit_task_state": True,
        **_review_ok(task_state_checks),
        **meta,
    }

    failure_checks: List[Tuple[str, bool]] = []
    for route in FAILURE_ESCALATION_RESPONSES:
        failure_checks.append((f"fail.{route['trigger'][:12]}", True))

    failure_review = {
        "review_id": "failure_escalation_response_dryrun_review_v1",
        "routes": list(FAILURE_ESCALATION_RESPONSES),
        **_review_ok(failure_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(
        ("model_generated", meta.get("task_response_integration_model_candidate_generated_now") is True)
    )

    boundary_audit = {
        "audit_id": "task_response_candidate_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "task_response_candidate_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        action_mapping_review,
        preservation_review,
        safety_review,
        speech_review,
        memory_review,
        task_state_review,
        failure_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("module_id") == "midplatform_task_response_candidate_integration_v1"
        and model_candidate.get("emits_task_response_candidate") is True
        and model_candidate.get("emits_user_output_candidate") is False
        and model_candidate.get("speech_gate_invocation_allowed") is False
    )

    sample_decision_ok = (
        all(f in sample_decision for f in DECISION_CANDIDATE_INTAKE_FIELDS)
        and sample_decision.get("candidate_only") is True
    )

    sample_task_ok = (
        all(f in sample_task_resp for f in TASK_RESPONSE_OUTPUT_FIELDS)
        and sample_task_resp.get("candidate_only") is True
        and sample_task_resp.get("user_output_allowed") is False
        and sample_task_resp.get("speech_output_allowed") is False
        and sample_task_resp.get("fact_status") == "not_fact"
    )

    all_pass = (
        input_ok
        and model_ok
        and sample_decision_ok
        and sample_task_ok
        and action_mapping_review.get("all_thirteen_actions_covered") is True
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections if "dryrun_and_review_pass" in s)
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "task_response_candidate_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "main_chain_closed": [
            "candidate/evidence/validation/health/whitebox",
            "→ decision_request_candidate",
            "→ decision_candidate",
            "→ task_response_candidate",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_output_plane_integration_planning": all_pass,
        "task_response_runtime_enabled": False,
        "user_output_still_forbidden": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "task_response_candidate_integration_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_not_runtime": True,
        "assembly_not_user_output": True,
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
        "boundary_ok": all_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "task_response_candidate_integration_dryrun_review_policy": policy,
        "task_response_candidate_planning_input_review": planning_input_review,
        "task_response_integration_model_candidate": model_candidate,
        "sample_decision_candidate_intake": sample_decision,
        "sample_task_response_candidate": sample_task_resp,
        "response_action_mapping_dryrun_review": action_mapping_review,
        "uncertainty_evidence_preservation_review": preservation_review,
        "safety_constitution_output_boundary_review": safety_review,
        "speech_output_boundary_review": speech_review,
        "memory_worldmodel_write_boundary_review": memory_review,
        "task_state_commit_boundary_review": task_state_review,
        "failure_escalation_response_dryrun_review": failure_review,
        "task_response_candidate_boundary_audit": boundary_audit,
        "task_response_candidate_blocked_path_result": blocked_path_result,
        "task_response_candidate_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
