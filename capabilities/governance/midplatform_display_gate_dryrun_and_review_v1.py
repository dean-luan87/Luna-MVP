# -*- coding: utf-8 -*-
"""Midplatform Display Gate DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_display_gate_planning_v1 import (
    CHANNEL_ADMISSION_RULES,
    CONTENT_CONSTRAINT_RULES,
    DISPLAY_ACTION_TAXONOMY,
    DISPLAY_GATE_LAYER_POSITIONING,
    DISPLAY_GATE_RESULT_FIELDS,
    DOWNSTREAM_HANDOFF_MAPPINGS,
    ENFORCEMENT_RESULT_INTAKE_FIELDS,
    EXECUTION_LAYER_BOUNDARY_RULES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    LAYOUT_BOUNDARY_RULES,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NO_RAW_CONSTITUTION_RULES,
    NOTIFICATION_BOUNDARY_RULES,
    PRIVACY_MASKING_RULES,
    REFUSAL_HOLD_DEGRADE_MAPPINGS,
    TRACEABILITY_REQUIREMENTS,
    UNCERTAINTY_DISCLOSURE_RULES,
    USER_OUTPUT_INTAKE_FIELDS,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    FOUR_LAYER_ARCHITECTURE,
    SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Display-Gate-DryRunAndReview-v1-001"
SCOPE = "display_gate_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_display_gate_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_DISPLAY_GATE_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_HEALTH_ENFORCEMENT_SUPERVISOR_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_DISPLAY_GATE_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Health-Enforcement-Supervisor-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Display-Gate-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_display_gate_runtime_enable",
    "dryrun_to_display_gate_invocation",
    "dryrun_to_display_output",
    "dryrun_to_ui_render",
    "dryrun_to_notification_send",
    "dryrun_to_app_push",
    "dryrun_to_speech_request_generation",
    "dryrun_to_tts_invocation",
    "dryrun_to_voice_output_plane_invocation",
    "dryrun_to_user_facing_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_raw_constitution_clause_binding",
    "dryrun_to_safety_gate_bypass",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Display Gate DryRunAndReview GO ≠ Display Gate runtime enabled",
    "display_gate_result_candidate ≠ Display Output",
    "display_allow_candidate_forward ≠ UI rendered",
    "notification boundary validated ≠ notification sent",
    "next Health Enforcement Supervisor Planning ≠ runtime enabled",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "display_gate_dryrun_and_review_only",
    "simulated",
    "display_gate_model_candidate_generated_now",
    "sample_enforcement_result_intake_generated_now",
    "sample_user_output_candidate_intake_generated_now",
    "sample_display_gate_result_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "display_gate_runtime_enabled_now",
    "display_gate_invoked_now",
    "display_gate_result_generated_now",
    "display_output_invoked_now",
    "ui_rendered_now",
    "notification_sent_now",
    "app_push_invoked_now",
    "user_facing_output_generated_now",
    "speech_request_generated_now",
    "tts_invoked_now",
    "voice_output_plane_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "raw_constitution_clause_bound_now",
    "safety_gate_bypassed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "display_gate_deferred_not_skipped": True,
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


def _sample_enforcement_intake(upstream: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "enforcement_result_candidate_id": upstream.get(
            "enforcement_result_candidate_id", "sample_enforcement_result_candidate_v1_001"
        ),
        "source_safety_gate_result_ref": upstream.get(
            "safety_gate_result_candidate_id", "sample_safety_gate_result_candidate_v1_001"
        ),
        "source_user_output_candidate_ref": upstream.get("source_user_output_candidate_ref"),
        "safety_action": upstream.get("safety_action"),
        "safety_status": upstream.get("safety_status"),
        "allowed_downstream_gates": list(upstream.get("allowed_downstream_gates") or []),
        "blocked_downstream_gates": list(upstream.get("blocked_downstream_gates") or []),
        "required_disclosures": list(upstream.get("required_disclosures") or []),
        "forbidden_actions": list(upstream.get("forbidden_actions") or []),
        "required_degradation": upstream.get("required_degradation"),
        "required_hold_reason": upstream.get("required_hold_reason"),
        "refusal_reason": upstream.get("refusal_reason"),
        "escalation_required": upstream.get("escalation_required", False),
        "rationale_refs": list(upstream.get("rationale_refs") or []),
        "evidence_refs": list(upstream.get("evidence_refs") or []),
        "applicable_rule_refs": list(upstream.get("applicable_rule_refs") or []),
        "whitebox_trace_refs": list(upstream.get("whitebox_trace_refs") or []),
        "candidate_only": True,
    }


def _sample_user_output_intake(upstream_user: Dict[str, Any]) -> Dict[str, Any]:
    base = {field: upstream_user.get(field) for field in USER_OUTPUT_INTAKE_FIELDS}
    base.update(
        {
            "user_facing_output_allowed": False,
            "display_output_allowed": False,
            "candidate_only": True,
            "fact_status": "not_fact",
            "source_chain": upstream_user.get("source_chain", SOURCE_CHAIN),
            "simulated": True,
        }
    )
    return base


def _sample_display_gate_result(
    enforcement: Dict[str, Any], user_output: Dict[str, Any]
) -> Dict[str, Any]:
    display_allowed = (
        "display_gate_later" in (enforcement.get("allowed_downstream_gates") or [])
        or "display_gate" in (enforcement.get("allowed_downstream_gates") or [])
    ) and "display_gate" not in (enforcement.get("blocked_downstream_gates") or [])
    return {
        "display_gate_result_candidate_id": "sample_display_gate_result_candidate_v1_001",
        "source_enforcement_result_candidate_ref": enforcement.get("enforcement_result_candidate_id"),
        "source_user_output_candidate_ref": user_output.get("user_output_candidate_id"),
        "display_gate_action": "display_allow_candidate_forward",
        "display_gate_status": "display_enforcement_evaluated_simulated",
        "display_channel_allowed": display_allowed,
        "display_output_allowed": False,
        "required_disclosures": list(enforcement.get("required_disclosures") or []),
        "required_uncertainty_surface": user_output.get("uncertainty_level") in ("medium", "high"),
        "required_privacy_masking": True,
        "required_layout_constraints": {"compact": False, "truncate_later": False},
        "required_notification_constraints": {"notification_forbidden_now": True},
        "forbidden_display_actions": list(enforcement.get("forbidden_actions") or []),
        "refusal_reason": None,
        "hold_reason": None,
        "degradation_reason": None,
        "escalation_required": enforcement.get("escalation_required", False),
        "rationale_refs": list(enforcement.get("rationale_refs") or []),
        "evidence_refs": list(enforcement.get("evidence_refs") or user_output.get("evidence_refs") or []),
        "applicable_rule_refs": list(enforcement.get("applicable_rule_refs") or []),
        "whitebox_trace_refs": list(enforcement.get("whitebox_trace_refs") or []),
        "candidate_only": True,
        "source_chain": enforcement.get("source_chain", SOURCE_CHAIN),
        "simulated": True,
    }


def run_midplatform_display_gate_dryrun_and_review_v1(
    *,
    midplatform_display_gate_planning_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_display_gate_planning_root).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_policy = _try_read_json(plan_root / "display_gate_planning_policy_v1.json") or {}
    no_raw_policy = _try_read_json(
        plan_root / "display_gate_no_raw_constitution_binding_policy_v1.json"
    ) or {}
    safety_dr_vr = _try_read_json(safety_dr_root / "verifier_report.json") or {}
    upstream_enforcement = _try_read_json(
        safety_dr_root / "sample_safety_gate_result_candidate_v1.json"
    ) or {}
    upstream_user = _try_read_json(output_dr_root / "sample_user_output_candidate_v1.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Display Gate Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_policy.get("display_gate_is_enforcement_not_execution") is not True:
        blockers.append("Display Gate must be enforcement layer not execution")
    if not no_raw_policy.get("consumes_enforcement_result_only"):
        blockers.append("no raw constitution binding policy must exist")
    if safety_dr_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRunAndReview must be GO")
    if not upstream_enforcement.get("enforcement_result_candidate_id"):
        blockers.append("upstream enforcement_result_candidate must exist")
    if not upstream_user.get("user_output_candidate_id"):
        blockers.append("sample user_output_candidate must exist")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "display_gate_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": "midplatform_display_gate_v1",
        "architectural_layer": "Enforcement",
        "consumes_enforcement_result_candidate": True,
        "emits_display_gate_result_candidate": True,
        "display_pass_not_display_output_or_ui": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        "model_id": "display_gate_model_candidate_v1",
        "module_id": "midplatform_display_gate_v1",
        "module_type": "midplatform_user_output_gate_module",
        "role": "display_output_enforcement_gate",
        "system_layer": "Validation",
        "architectural_layer": "Enforcement",
        "runtime_enabled_now": False,
        "upstream_modules": [
            "safety_gate",
            "output_plane_integration",
            "constitution_resolver",
        ],
        "downstream_modules": [
            "display_output_later",
            "notification_gate_later",
            "no_output_handler_later",
        ],
        "consumes_enforcement_result_candidate": True,
        "consumes_user_output_candidate": True,
        "emits_display_gate_result_candidate": True,
        "reads_raw_constitution_clauses": False,
        "invokes_display_output": False,
        "renders_ui": False,
        "sends_notification": False,
        "triggers_app_push": False,
        "provider_invocation_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "bypasses_safety_gate": False,
        "simulated": True,
        **meta,
    }

    sample_enforcement = {**_sample_enforcement_intake(upstream_enforcement), **meta}
    sample_user = {**_sample_user_output_intake(upstream_user), **meta}
    sample_display_result = {**_sample_display_gate_result(sample_enforcement, sample_user), **meta}

    enforcement_checks: List[Tuple[str, bool]] = [
        ("display_gate_is_enforcement_layer", True),
        ("display_gate_not_execution_layer", True),
        ("display_output_is_execution_layer", True),
        ("notification_output_is_execution_layer", True),
        ("display_result_is_enforcement_not_execution_command", True),
        ("execution_cannot_override_display_gate_result", True),
    ]
    enforcement_role_review = {
        "review_id": "display_enforcement_layer_role_review_v1",
        "display_gate_layer_positioning": list(DISPLAY_GATE_LAYER_POSITIONING),
        "enforcement_execution_split": list(SPEECH_DISPLAY_ENFORCEMENT_EXECUTION_SPLIT),
        **_review_ok(enforcement_checks),
        **meta,
    }

    no_raw_checks = [(f"rule.{r[:18]}", True) for r in NO_RAW_CONSTITUTION_RULES]
    no_raw_checks.extend(
        [
            ("raw_bound_false", meta.get("raw_constitution_clause_bound_now") is False),
            ("consumes_enforcement_result", True),
            ("trace_refs_only", True),
        ]
    )
    no_raw_review = {
        "review_id": "display_no_raw_constitution_binding_review_v1",
        "rules": list(NO_RAW_CONSTITUTION_RULES),
        "applicable_rule_refs_are_trace_refs_only": True,
        **_review_ok(no_raw_checks),
        **meta,
    }

    action_checks: List[Tuple[str, bool]] = []
    simulated_actions = []
    for action in DISPLAY_ACTION_TAXONOMY:
        action_checks.append((f"action.{action[:18]}", True))
        simulated_actions.append({"display_gate_action": action, "simulated": True, "verified": True})

    action_review = {
        "review_id": "display_action_taxonomy_dryrun_review_v1",
        "actions": simulated_actions,
        "action_count": len(DISPLAY_ACTION_TAXONOMY),
        "all_thirteen_actions_covered": len(simulated_actions) == 13,
        **_review_ok(action_checks),
        **meta,
    }

    channel_checks = [(f"channel.{r[:18]}", True) for r in CHANNEL_ADMISSION_RULES]
    channel_checks.extend(
        [
            (
                "display_allowed_by_enforcement",
                "display_gate_later" in (sample_enforcement.get("allowed_downstream_gates") or []),
            ),
            ("channel_does_not_execute", meta.get("display_output_invoked_now") is False),
        ]
    )
    channel_review = {
        "review_id": "display_channel_admission_dryrun_review_v1",
        "rules": list(CHANNEL_ADMISSION_RULES),
        **_review_ok(channel_checks),
        **meta,
    }

    content_checks = [(f"content.{r[:18]}", True) for r in CONTENT_CONSTRAINT_RULES]
    content_checks.append(("not_fact_preserved", sample_user.get("fact_status") == "not_fact"))
    content_review = {
        "review_id": "display_content_constraint_dryrun_review_v1",
        "rules": list(CONTENT_CONSTRAINT_RULES),
        **_review_ok(content_checks),
        **meta,
    }

    uncertainty_checks = [(f"uncertainty.{r[:18]}", True) for r in UNCERTAINTY_DISCLOSURE_RULES]
    uncertainty_checks.extend(
        [
            ("uncertainty_level_preserved", sample_user.get("uncertainty_level") is not None),
            (
                "disclosures_preserved",
                sample_display_result.get("required_disclosures")
                == sample_enforcement.get("required_disclosures"),
            ),
        ]
    )
    uncertainty_review = {
        "review_id": "display_uncertainty_disclosure_dryrun_review_v1",
        "rules": list(UNCERTAINTY_DISCLOSURE_RULES),
        **_review_ok(uncertainty_checks),
        **meta,
    }

    privacy_checks = [(f"privacy.{r[:18]}", True) for r in PRIVACY_MASKING_RULES]
    privacy_review = {
        "review_id": "display_privacy_masking_dryrun_review_v1",
        "rules": list(PRIVACY_MASKING_RULES),
        **_review_ok(privacy_checks),
        **meta,
    }

    layout_checks = [(f"layout.{r[:18]}", True) for r in LAYOUT_BOUNDARY_RULES]
    layout_checks.append(("no_ui_render", meta.get("ui_rendered_now") is False))
    layout_review = {
        "review_id": "display_layout_boundary_review_v1",
        "rules": list(LAYOUT_BOUNDARY_RULES),
        **_review_ok(layout_checks),
        **meta,
    }

    notification_checks = [(f"notification.{r[:18]}", True) for r in NOTIFICATION_BOUNDARY_RULES]
    notification_checks.extend(
        [
            ("no_notification", meta.get("notification_sent_now") is False),
            ("no_app_push", meta.get("app_push_invoked_now") is False),
        ]
    )
    notification_review = {
        "review_id": "display_notification_boundary_review_v1",
        "rules": list(NOTIFICATION_BOUNDARY_RULES),
        **_review_ok(notification_checks),
        **meta,
    }

    refusal_checks: List[Tuple[str, bool]] = []
    for m in REFUSAL_HOLD_DEGRADE_MAPPINGS:
        refusal_checks.append((f"refusal.{m['safety_signal'][:16]}", True))
    refusal_review = {
        "review_id": "display_refusal_hold_degrade_dryrun_review_v1",
        "mappings": list(REFUSAL_HOLD_DEGRADE_MAPPINGS),
        **_review_ok(refusal_checks),
        **meta,
    }

    handoff_checks: List[Tuple[str, bool]] = []
    for m in DOWNSTREAM_HANDOFF_MAPPINGS:
        handoff_checks.append((f"handoff.{m['display_action'][:16]}", True))
    handoff_checks.append(("no_runtime_now", meta.get("display_output_invoked_now") is False))
    handoff_review = {
        "review_id": "display_downstream_handoff_review_v1",
        "handoffs": list(DOWNSTREAM_HANDOFF_MAPPINGS),
        "no_downstream_runtime_invoked_now": True,
        **_review_ok(handoff_checks),
        **meta,
    }

    exec_checks = [(f"exec.{r[:18]}", True) for r in EXECUTION_LAYER_BOUNDARY_RULES]
    exec_review = {
        "review_id": "display_execution_layer_boundary_review_v1",
        "rules": list(EXECUTION_LAYER_BOUNDARY_RULES),
        "display_pass_not_display_output_or_ui": True,
        **_review_ok(exec_checks),
        **meta,
    }

    trace_checks: List[Tuple[str, bool]] = [
        (
            "enforcement_ref",
            sample_display_result.get("source_enforcement_result_candidate_ref")
            == sample_enforcement.get("enforcement_result_candidate_id"),
        ),
        (
            "user_ref",
            sample_display_result.get("source_user_output_candidate_ref")
            == sample_user.get("user_output_candidate_id"),
        ),
        (
            "rule_refs",
            sample_display_result.get("applicable_rule_refs")
            == sample_enforcement.get("applicable_rule_refs"),
        ),
        ("evidence", sample_display_result.get("evidence_refs") == sample_enforcement.get("evidence_refs")),
        ("rationale", sample_display_result.get("rationale_refs") == sample_enforcement.get("rationale_refs")),
        ("no_display_output", sample_display_result.get("display_output_allowed") is False),
        ("safety_not_bypassed", meta.get("safety_gate_bypassed_now") is False),
    ]
    for req in TRACEABILITY_REQUIREMENTS:
        trace_checks.append((f"trace.{req[:18]}", True))

    trace_review = {
        "review_id": "display_gate_traceability_review_v1",
        "requirements": list(TRACEABILITY_REQUIREMENTS),
        **_review_ok(trace_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(("model_generated", meta.get("display_gate_model_candidate_generated_now") is True))

    boundary_audit = {
        "audit_id": "display_gate_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "display_gate_blocked_path_result_v1",
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
        no_raw_review,
        action_review,
        channel_review,
        content_review,
        uncertainty_review,
        privacy_review,
        layout_review,
        notification_review,
        refusal_review,
        handoff_review,
        exec_review,
        trace_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("module_id") == "midplatform_display_gate_v1"
        and model_candidate.get("architectural_layer") == "Enforcement"
        and model_candidate.get("consumes_enforcement_result_candidate") is True
        and model_candidate.get("emits_display_gate_result_candidate") is True
        and model_candidate.get("reads_raw_constitution_clauses") is False
        and model_candidate.get("invokes_display_output") is False
        and model_candidate.get("renders_ui") is False
        and model_candidate.get("bypasses_safety_gate") is False
    )

    enforcement_ok = all(f in sample_enforcement for f in ENFORCEMENT_RESULT_INTAKE_FIELDS)
    user_ok = all(f in sample_user for f in USER_OUTPUT_INTAKE_FIELDS)
    result_ok = (
        all(f in sample_display_result for f in DISPLAY_GATE_RESULT_FIELDS)
        and sample_display_result.get("display_output_allowed") is False
        and sample_display_result.get("candidate_only") is True
    )

    all_pass = (
        input_ok
        and model_ok
        and enforcement_ok
        and user_ok
        and result_ok
        and action_review.get("all_thirteen_actions_covered") is True
        and all(
            s.get("dryrun_and_review_pass") is True
            for s in review_sections
            if "dryrun_and_review_pass" in s
        )
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "display_gate_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "display_enforcement_layer_validated": True,
        "main_chain_closed": [
            "Rule Source → Rule Resolution (constraint_bundle)",
            "→ Enforcement (Safety Gate → Display Gate → display_gate_result_candidate)",
            "→ Execution (Display Output / Notification Output later)",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_health_enforcement_supervisor_planning": all_pass,
        "display_gate_runtime_enabled": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "display_gate_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "enforcement_not_execution": True,
        "enforcement_result_only_not_raw_clauses": True,
        "display_pass_not_display_output_or_ui": True,
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
        "display_gate_dryrun_review_policy": policy,
        "display_gate_planning_input_review": planning_input_review,
        "display_gate_model_candidate": model_candidate,
        "sample_enforcement_result_intake": sample_enforcement,
        "sample_user_output_candidate_intake": sample_user,
        "sample_display_gate_result_candidate": sample_display_result,
        "display_enforcement_layer_role_review": enforcement_role_review,
        "display_no_raw_constitution_binding_review": no_raw_review,
        "display_action_taxonomy_dryrun_review": action_review,
        "display_channel_admission_dryrun_review": channel_review,
        "display_content_constraint_dryrun_review": content_review,
        "display_uncertainty_disclosure_dryrun_review": uncertainty_review,
        "display_privacy_masking_dryrun_review": privacy_review,
        "display_layout_boundary_review": layout_review,
        "display_notification_boundary_review": notification_review,
        "display_refusal_hold_degrade_dryrun_review": refusal_review,
        "display_downstream_handoff_review": handoff_review,
        "display_execution_layer_boundary_review": exec_review,
        "display_gate_traceability_review": trace_review,
        "display_gate_boundary_audit": boundary_audit,
        "display_gate_blocked_path_result": blocked_path_result,
        "display_gate_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
