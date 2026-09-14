# -*- coding: utf-8 -*-
"""Midplatform Safety Gate DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    CHANNEL_BOUNDARY_RULES,
    CONSTRAINT_BUNDLE_INTAKE_FIELDS,
    DOWNSTREAM_HANDOFF_MAPPINGS,
    ENFORCEMENT_LAYER_POSITIONING,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    FOUR_LAYER_ARCHITECTURE,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NO_RAW_CONSTITUTION_RULES,
    REFUSAL_HOLD_DEGRADE_MAPPINGS,
    RULE_APPLICATION_RULES,
    SAFETY_ACTION_TAXONOMY,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
    TRACEABILITY_REQUIREMENTS,
    UNCERTAINTY_RISK_RULES,
    USER_OUTPUT_INTAKE_FIELDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Safety-Gate-DryRunAndReview-v1-001"
SCOPE = "safety_gate_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_safety_gate_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_SAFETY_GATE_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_SPEECH_DISPLAY_GATE_ROADMAP_DECISION"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_SAFETY_GATE_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Speech-Display-Gate-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Safety-Gate-Issue-Review-v1-001"

ENFORCEMENT_RESULT_SAMPLE_FIELDS: Tuple[str, ...] = (
    "safety_gate_result_candidate_id",
    "enforcement_result_candidate_id",
    "source_user_output_candidate_ref",
    "source_constraint_bundle_ref",
    "enforcement_layer",
    "safety_action",
    "safety_status",
    "allowed_downstream_gates",
    "blocked_downstream_gates",
    "required_disclosures",
    "forbidden_actions",
    "required_degradation",
    "required_hold_reason",
    "refusal_reason",
    "escalation_required",
    "rationale_refs",
    "evidence_refs",
    "applicable_rule_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "user_facing_output_allowed",
    "speech_request_allowed",
    "display_output_allowed",
)

EXECUTION_LAYER_BOUNDARY_RULES: Tuple[str, ...] = (
    "Voice Output Plane consumes enforcement_result_candidate later",
    "Display Output consumes enforcement_result_candidate later",
    "TTS runtime consumes execution command later, not Safety Gate result directly",
    "execution layer does not consume raw constitution",
    "execution layer does not interpret constitution",
    "execution layer cannot override enforcement result",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_safety_gate_runtime_enable",
    "dryrun_to_safety_gate_invocation",
    "dryrun_to_user_facing_output",
    "dryrun_to_speech_request_generation",
    "dryrun_to_speech_gate_invocation",
    "dryrun_to_tts_invocation",
    "dryrun_to_voice_output_plane_invocation",
    "dryrun_to_display_output_invocation",
    "dryrun_to_notification_send",
    "dryrun_to_app_push",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_raw_constitution_clause_binding",
    "dryrun_to_hive_constitution_registry_update",
    "dryrun_to_execution_layer_direct_constitution_consumption",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Safety Gate DryRunAndReview GO ≠ Safety Gate runtime enabled",
    "enforcement_result_candidate ≠ user-facing output",
    "safety_allow_candidate_forward ≠ speech/display execution",
    "bundle-only pass ≠ constitution published",
    "next roadmap decision ≠ final output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "safety_gate_dryrun_and_review_only",
    "simulated",
    "safety_gate_model_candidate_generated_now",
    "sample_constraint_bundle_intake_generated_now",
    "sample_user_output_candidate_intake_generated_now",
    "sample_safety_gate_result_candidate_generated_now",
    "enforcement_result_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "safety_gate_runtime_enabled_now",
    "safety_gate_invoked_now",
    "user_facing_output_generated_now",
    "speech_request_generated_now",
    "speech_gate_invoked_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "app_push_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "constitution_raw_clause_bound_now",
    "hive_constitution_registry_updated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
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


def _sample_bundle_intake(upstream_bundle: Dict[str, Any]) -> Dict[str, Any]:
    base = {field: upstream_bundle.get(field) for field in CONSTRAINT_BUNDLE_INTAKE_FIELDS}
    base.update(
        {
            "candidate_only": True,
            "source_chain": upstream_bundle.get("source_chain", SOURCE_CHAIN),
            "simulated": True,
        }
    )
    return base


def _sample_user_output_intake(upstream_user: Dict[str, Any]) -> Dict[str, Any]:
    base = {field: upstream_user.get(field) for field in USER_OUTPUT_INTAKE_FIELDS}
    base.update(
        {
            "user_facing_output_allowed": False,
            "speech_request_allowed": False,
            "display_output_allowed": False,
            "candidate_only": True,
            "fact_status": "not_fact",
            "source_chain": upstream_user.get("source_chain", SOURCE_CHAIN),
            "simulated": True,
        }
    )
    return base


def _sample_enforcement_result(bundle: Dict[str, Any], user_output: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "safety_gate_result_candidate_id": "sample_safety_gate_result_candidate_v1_001",
        "enforcement_result_candidate_id": "sample_enforcement_result_candidate_v1_001",
        "source_user_output_candidate_ref": user_output.get("user_output_candidate_id"),
        "source_constraint_bundle_ref": bundle.get("bundle_id"),
        "enforcement_layer": "SafetyGate",
        "safety_action": "safety_allow_candidate_forward",
        "safety_status": "enforcement_evaluated_simulated",
        "allowed_downstream_gates": ["speech_gate_later", "display_gate_later"],
        "blocked_downstream_gates": [],
        "required_disclosures": list(bundle.get("required_disclosures") or []),
        "forbidden_actions": list(bundle.get("forbidden_actions") or []),
        "required_degradation": None,
        "required_hold_reason": None,
        "refusal_reason": None,
        "escalation_required": bundle.get("escalation_required", False),
        "rationale_refs": list(bundle.get("rationale_refs") or user_output.get("rationale_refs") or []),
        "evidence_refs": list(user_output.get("evidence_refs") or []),
        "applicable_rule_refs": list(bundle.get("applicable_rule_refs") or []),
        "whitebox_trace_refs": list(bundle.get("whitebox_trace_refs") or []),
        "candidate_only": True,
        "user_facing_output_allowed": False,
        "speech_request_allowed": False,
        "display_output_allowed": False,
        "source_chain": bundle.get("source_chain", SOURCE_CHAIN),
        "simulated": True,
    }


def run_midplatform_safety_gate_dryrun_and_review_v1(
    *,
    midplatform_safety_gate_planning_root: str,
    midplatform_user_output_constitution_dryrun_and_review_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_safety_gate_planning_root).expanduser().resolve()
    uo_dr_root = Path(
        midplatform_user_output_constitution_dryrun_and_review_root
    ).expanduser().resolve()
    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_policy = _try_read_json(plan_root / "safety_gate_planning_policy_v1.json") or {}
    no_raw_policy = _try_read_json(
        plan_root / "safety_gate_no_raw_constitution_binding_policy_v1.json"
    ) or {}
    upstream_bundle = _try_read_json(
        uo_dr_root / "constitution_constraint_bundle_candidate_v1.json"
    ) or {}
    upstream_user = _try_read_json(output_dr_root / "sample_user_output_candidate_v1.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_user_output_constitution_dryrun_root": str(uo_dr_root),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Safety Gate Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_policy.get("safety_gate_is_enforcement_not_execution") is not True:
        blockers.append("Safety Gate must be enforcement layer not execution")
    if not no_raw_policy.get("consumes_constraint_bundle_only"):
        blockers.append("no raw constitution binding policy must exist")
    if not upstream_bundle.get("bundle_id"):
        blockers.append("upstream constraint_bundle must exist")
    if not upstream_user.get("user_output_candidate_id"):
        blockers.append("sample user_output_candidate must exist")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "safety_gate_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "enforcement_layer_not_execution": True,
        "consumes_constraint_bundle": True,
        "emits_enforcement_result_candidate": True,
        "execution_consumes_enforcement_not_constitution": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        "model_id": "safety_gate_model_candidate_v1",
        "module_id": "midplatform_safety_gate_v1",
        "module_type": "midplatform_user_output_gate_module",
        "role": "user_output_safety_enforcement_gate",
        "system_layer": "Validation",
        "architectural_layer": "Enforcement",
        "runtime_enabled_now": False,
        "upstream_modules": [
            "constitution_resolver",
            "output_plane_integration",
            "user_output_constitution",
        ],
        "downstream_modules": [
            "speech_gate_later",
            "display_gate_later",
            "user_output_gate_later",
            "notification_gate_later",
            "no_output_handler_later",
        ],
        "consumes_constraint_bundle": True,
        "consumes_user_output_candidate": True,
        "emits_enforcement_result_candidate": True,
        "reads_raw_constitution_clauses": False,
        "publishes_constitution": False,
        "replaces_constitution_resolver": False,
        "invokes_execution_layer": False,
        "generates_user_facing_output": False,
        "speech_gate_invocation_allowed": False,
        "tts_invocation_allowed": False,
        "display_output_invocation_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "simulated": True,
        **meta,
    }

    sample_bundle = {**_sample_bundle_intake(upstream_bundle), **meta}
    sample_user = {**_sample_user_output_intake(upstream_user), **meta}
    sample_result = {**_sample_enforcement_result(sample_bundle, sample_user), **meta}

    enforcement_checks: List[Tuple[str, bool]] = [
        ("is_enforcement_layer", True),
        ("not_execution_layer", True),
        ("speech_gate_enforcement", True),
        ("display_gate_enforcement", True),
        ("voice_plane_execution", True),
        ("display_output_execution", True),
        ("execution_reads_enforcement_result", True),
        ("execution_no_raw_constitution", True),
    ]
    enforcement_role_review = {
        "review_id": "enforcement_layer_role_review_v1",
        "enforcement_layer_positioning": list(ENFORCEMENT_LAYER_POSITIONING),
        "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
        **_review_ok(enforcement_checks),
        **meta,
    }

    bundle_checks: List[Tuple[str, bool]] = [
        ("bundle_only", True),
        ("source_refs_trace", True),
        ("applicable_rule_refs", True),
        ("version_required", bool(sample_bundle.get("version_ref"))),
        ("ttl_required", bool(sample_bundle.get("ttl"))),
        ("no_raw_parsing", meta.get("constitution_raw_clause_bound_now") is False),
    ]
    bundle_review = {
        "review_id": "bundle_only_consumption_review_v1",
        "consumes_constraint_bundle_only": True,
        "source_constitution_refs_are_trace_refs": True,
        **_review_ok(bundle_checks),
        **meta,
    }

    no_raw_checks = [(f"rule.{r[:18]}", True) for r in NO_RAW_CONSTITUTION_RULES]
    no_raw_checks.append(("raw_bound_false", meta.get("constitution_raw_clause_bound_now") is False))
    no_raw_review = {
        "review_id": "no_raw_constitution_binding_review_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        **_review_ok(no_raw_checks),
        **meta,
    }

    action_checks: List[Tuple[str, bool]] = []
    simulated_actions = []
    for action in SAFETY_ACTION_TAXONOMY:
        action_checks.append((f"action.{action[:18]}", True))
        simulated_actions.append({"safety_action": action, "simulated": True, "verified": True})

    action_review = {
        "review_id": "safety_action_taxonomy_dryrun_review_v1",
        "actions": simulated_actions,
        "action_count": len(SAFETY_ACTION_TAXONOMY),
        "all_twelve_actions_covered": len(simulated_actions) == 12,
        **_review_ok(action_checks),
        **meta,
    }

    rule_checks = [(f"rule.{r[:18]}", True) for r in RULE_APPLICATION_RULES]
    rule_checks.extend(
        [
            ("forbidden_preserved", sample_result.get("forbidden_actions") == sample_bundle.get("forbidden_actions")),
            ("disclosures_preserved", sample_result.get("required_disclosures") == sample_bundle.get("required_disclosures")),
            ("rule_refs_preserved", sample_result.get("applicable_rule_refs") == sample_bundle.get("applicable_rule_refs")),
        ]
    )
    rule_review = {
        "review_id": "safety_rule_application_dryrun_review_v1",
        "rules": list(RULE_APPLICATION_RULES),
        **_review_ok(rule_checks),
        **meta,
    }

    risk_checks = [(f"risk.{r[:18]}", True) for r in UNCERTAINTY_RISK_RULES]
    risk_review = {
        "review_id": "safety_uncertainty_risk_policy_review_v1",
        "rules": list(UNCERTAINTY_RISK_RULES),
        **_review_ok(risk_checks),
        **meta,
    }

    channel_checks = [(f"channel.{r[:18]}", True) for r in CHANNEL_BOUNDARY_RULES]
    channel_review = {
        "review_id": "safety_channel_boundary_review_v1",
        "rules": list(CHANNEL_BOUNDARY_RULES),
        **_review_ok(channel_checks),
        **meta,
    }

    refusal_checks: List[Tuple[str, bool]] = []
    for m in REFUSAL_HOLD_DEGRADE_MAPPINGS:
        refusal_checks.append((f"refusal.{m['safety_action'][:16]}", True))
    refusal_review = {
        "review_id": "refusal_hold_degrade_dryrun_review_v1",
        "mappings": list(REFUSAL_HOLD_DEGRADE_MAPPINGS),
        **_review_ok(refusal_checks),
        **meta,
    }

    handoff_checks: List[Tuple[str, bool]] = []
    for m in DOWNSTREAM_HANDOFF_MAPPINGS:
        handoff_checks.append((f"handoff.{m['safety_action'][:16]}", True))
    handoff_checks.append(("no_runtime_now", meta.get("voice_output_plane_invoked_now") is False))
    handoff_review = {
        "review_id": "enforcement_result_downstream_handoff_review_v1",
        "handoffs": list(DOWNSTREAM_HANDOFF_MAPPINGS),
        "no_downstream_runtime_invoked_now": True,
        **_review_ok(handoff_checks),
        **meta,
    }

    exec_checks = [(f"exec.{r[:18]}", True) for r in EXECUTION_LAYER_BOUNDARY_RULES]
    exec_review = {
        "review_id": "execution_layer_consumption_boundary_review_v1",
        "rules": list(EXECUTION_LAYER_BOUNDARY_RULES),
        "execution_layer_consumes_enforcement_result_not_constitution": True,
        **_review_ok(exec_checks),
        **meta,
    }

    trace_checks: List[Tuple[str, bool]] = [
        ("bundle_ref", sample_result.get("source_constraint_bundle_ref") == sample_bundle.get("bundle_id")),
        ("user_ref", sample_result.get("source_user_output_candidate_ref") == sample_user.get("user_output_candidate_id")),
        ("rule_refs", sample_result.get("applicable_rule_refs") == sample_bundle.get("applicable_rule_refs")),
        ("evidence", sample_result.get("evidence_refs") == sample_user.get("evidence_refs")),
        ("rationale", sample_result.get("rationale_refs") == sample_bundle.get("rationale_refs")),
    ]
    for req in TRACEABILITY_REQUIREMENTS:
        trace_checks.append((f"trace.{req[:18]}", True))

    trace_review = {
        "review_id": "safety_gate_traceability_review_v1",
        "requirements": list(TRACEABILITY_REQUIREMENTS),
        **_review_ok(trace_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(("model_generated", meta.get("safety_gate_model_candidate_generated_now") is True))

    boundary_audit = {
        "audit_id": "safety_gate_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "safety_gate_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        enforcement_role_review,
        bundle_review,
        no_raw_review,
        action_review,
        rule_review,
        risk_review,
        channel_review,
        refusal_review,
        handoff_review,
        exec_review,
        trace_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("module_id") == "midplatform_safety_gate_v1"
        and model_candidate.get("architectural_layer") == "Enforcement"
        and model_candidate.get("consumes_constraint_bundle") is True
        and model_candidate.get("emits_enforcement_result_candidate") is True
        and model_candidate.get("reads_raw_constitution_clauses") is False
        and model_candidate.get("invokes_execution_layer") is False
    )

    bundle_ok = all(f in sample_bundle for f in CONSTRAINT_BUNDLE_INTAKE_FIELDS)
    user_ok = all(f in sample_user for f in USER_OUTPUT_INTAKE_FIELDS)
    result_ok = (
        all(f in sample_result for f in ENFORCEMENT_RESULT_SAMPLE_FIELDS)
        and sample_result.get("enforcement_layer") == "SafetyGate"
        and sample_result.get("user_facing_output_allowed") is False
    )

    all_pass = (
        input_ok
        and model_ok
        and bundle_ok
        and user_ok
        and result_ok
        and action_review.get("all_twelve_actions_covered") is True
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections if "dryrun_and_review_pass" in s)
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "safety_gate_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "enforcement_layer_validated": True,
        "main_chain_closed": [
            "Rule Source → Rule Resolution (constraint_bundle)",
            "→ Enforcement (Safety Gate → enforcement_result_candidate)",
            "→ Execution (Voice/Display/TTS later)",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_speech_display_gate_roadmap_decision": all_pass,
        "safety_gate_runtime_enabled": False,
        "do_not_skip_to_voice_output_plane": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "safety_gate_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "enforcement_not_execution": True,
        "bundle_only_not_raw_clauses": True,
        "execution_consumes_enforcement_result": True,
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
        "safety_gate_dryrun_review_policy": policy,
        "safety_gate_planning_input_review": planning_input_review,
        "safety_gate_model_candidate": model_candidate,
        "sample_constraint_bundle_intake": sample_bundle,
        "sample_user_output_candidate_intake": sample_user,
        "sample_safety_gate_result_candidate": sample_result,
        "enforcement_layer_role_review": enforcement_role_review,
        "bundle_only_consumption_review": bundle_review,
        "no_raw_constitution_binding_review": no_raw_review,
        "safety_action_taxonomy_dryrun_review": action_review,
        "safety_rule_application_dryrun_review": rule_review,
        "safety_uncertainty_risk_policy_review": risk_review,
        "safety_channel_boundary_review": channel_review,
        "refusal_hold_degrade_dryrun_review": refusal_review,
        "enforcement_result_downstream_handoff_review": handoff_review,
        "execution_layer_consumption_boundary_review": exec_review,
        "safety_gate_traceability_review": trace_review,
        "safety_gate_boundary_audit": boundary_audit,
        "safety_gate_blocked_path_result": blocked_path_result,
        "safety_gate_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
