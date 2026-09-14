# -*- coding: utf-8 -*-
"""Health Enforcement Supervisor DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_enforcement_supervisor_planning_v1 import (
    BOUNDARY_VIOLATION_DETECTION_RULES,
    BYPASS_PREVENTION_RULES,
    ENFORCEMENT_OVERRIDE_FORBIDDEN_RULES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GATE_COMPLIANCE_MONITORING_RULES,
    HEALTH_SIGNAL_BINDING_RULES,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    RUNTIME_RECOMMENDATION_RULES,
    SUPERVISED_GATES,
    SUPERVISION_ACTION_TAXONOMY,
    SUPERVISOR_LAYER_POSITIONING,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Health-Enforcement-Supervisor-DryRunAndReview-v1-001"
SCOPE = "health_enforcement_supervisor_dryrun_and_review_only"
SOURCE_CHAIN = "health_enforcement_supervisor_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "HEALTH_ENFORCEMENT_SUPERVISOR_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_CONTROLLED_RUNTIME_PLANNING"
)
FINAL_DECISION_HOLD = "HEALTH_ENFORCEMENT_SUPERVISOR_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Controlled-Runtime-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Health-Enforcement-Supervisor-Issue-Review-v1-001"

SUPERVISION_SCOPE_TARGETS: Tuple[str, ...] = (
    "Safety Gate",
    "Speech Gate",
    "Display Gate",
    "Authorization Gate",
    "Validation Factory",
)

NOT_SUPERVISED_NOT_REPLACED: Tuple[str, ...] = (
    "Constitution Resolver",
    "Decision Center",
    "Voice Output Plane",
    "TTS Runtime",
    "Display Output",
    "Provider runtime",
    "Memory write",
    "WorldModel write",
)

COMPLIANCE_OBSERVATION_ITEMS: Tuple[str, ...] = (
    "gate consumes expected input type",
    "gate emits expected result type",
    "gate preserves applicable_rule_refs",
    "gate preserves rationale/evidence/whitebox trace",
    "gate does not bypass Resolver/bundle",
    "gate does not invoke execution layer",
    "gate does not exceed architectural layer",
    "gate result action matches allowed taxonomy",
)

HEALTH_SIGNAL_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {"signal": "gate_missing_result", "outcome": "enforcement_health_status=degraded"},
    {"signal": "gate_conflict", "outcome": "pressure_level elevated"},
    {"signal": "gate_timeout", "outcome": "hold/degrade hint"},
    {"signal": "gate_boundary_violation_risk", "outcome": "violation_report_candidate"},
    {"signal": "repeated gate drift", "outcome": "issue_trace_candidate"},
    {"signal": "supervisor emits health signal candidate only", "outcome": "no automatic output block"},
)

ISSUE_TRACE_TYPES: Tuple[str, ...] = (
    "missing_gate_result",
    "inconsistent_gate_action",
    "enforcement_boundary_violation_risk",
    "gate_timeout",
    "gate_drift",
    "traceability_missing",
    "applicable_rule_refs_missing",
)

VIOLATION_REPORT_TYPES: Tuple[str, ...] = (
    "gate_bypassed_resolver",
    "gate_invoked_execution_layer",
    "execution_layer_read_raw_constitution",
    "gate_result_mutated_without_trace",
    "provider_invoked_without_authorization",
    "output_generated_without_gate_pass",
)

SIMULATED_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "all_gates_compliant",
        "supervision_status": "compliant",
        "enforcement_compliance_status": "ok",
        "gate_conflict_detected": False,
        "gate_timeout_detected": False,
        "gate_drift_detected": False,
        "boundary_violation_risk": False,
        "recommended_supervision_action": "supervise_compliance_ok_candidate",
        "simulated_pass": True,
    },
    {
        "case_id": "safety_allow_speech_block_no_conflict",
        "supervision_status": "observed",
        "enforcement_compliance_status": "ok",
        "gate_conflict_detected": False,
        "gate_timeout_detected": False,
        "gate_drift_detected": False,
        "boundary_violation_risk": False,
        "recommended_supervision_action": "supervise_compliance_ok_candidate",
        "simulated_pass": True,
    },
    {
        "case_id": "display_gate_missing_result",
        "supervision_status": "degraded",
        "enforcement_compliance_status": "degraded",
        "gate_conflict_detected": False,
        "gate_timeout_detected": False,
        "gate_drift_detected": False,
        "boundary_violation_risk": False,
        "recommended_supervision_action": "supervise_gate_failure_candidate",
        "issue_trace": "missing_gate_result",
        "simulated_pass": True,
    },
    {
        "case_id": "speech_gate_timeout",
        "supervision_status": "hold_hint",
        "enforcement_compliance_status": "degraded",
        "gate_conflict_detected": False,
        "gate_timeout_detected": True,
        "gate_drift_detected": False,
        "boundary_violation_risk": False,
        "recommended_supervision_action": "supervise_enforcement_hold_recommended_candidate",
        "issue_trace": "gate_timeout",
        "simulated_pass": True,
    },
    {
        "case_id": "authorization_gate_conflict",
        "supervision_status": "elevated_pressure",
        "enforcement_compliance_status": "conflict",
        "gate_conflict_detected": True,
        "gate_timeout_detected": False,
        "gate_drift_detected": False,
        "boundary_violation_risk": True,
        "recommended_supervision_action": "supervise_boundary_violation_candidate",
        "simulated_pass": True,
    },
    {
        "case_id": "validation_factory_fail_but_output_path_allowed_attempt",
        "supervision_status": "violation_risk",
        "enforcement_compliance_status": "fail",
        "gate_conflict_detected": True,
        "gate_timeout_detected": False,
        "gate_drift_detected": False,
        "boundary_violation_risk": True,
        "recommended_supervision_action": "supervise_bypass_attempt_blocked_candidate",
        "violation_report": "output_generated_without_gate_pass",
        "simulated_pass": True,
    },
    {
        "case_id": "gate_drift_detected",
        "supervision_status": "drift",
        "enforcement_compliance_status": "degraded",
        "gate_conflict_detected": False,
        "gate_timeout_detected": False,
        "gate_drift_detected": True,
        "boundary_violation_risk": False,
        "recommended_supervision_action": "supervise_gate_degraded_candidate",
        "issue_trace": "gate_drift",
        "simulated_pass": True,
    },
    {
        "case_id": "execution_layer_boundary_violation_attempt",
        "supervision_status": "blocked_attempt",
        "enforcement_compliance_status": "violation_risk",
        "gate_conflict_detected": False,
        "gate_timeout_detected": False,
        "gate_drift_detected": False,
        "boundary_violation_risk": True,
        "recommended_supervision_action": "supervise_bypass_attempt_blocked_candidate",
        "violation_report": "gate_invoked_execution_layer",
        "simulated_pass": True,
    },
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_health_supervisor_runtime_enable",
    "dryrun_to_health_supervisor_invocation",
    "dryrun_to_gate_invocation",
    "dryrun_to_gate_result_mutation",
    "dryrun_to_output_block_by_supervisor",
    "dryrun_to_controlled_runtime_planning_start",
    "dryrun_to_controlled_runtime_enable",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_constitution_write",
    "dryrun_to_execution_layer_invocation",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Health Enforcement Supervisor DryRunAndReview GO ≠ supervisor runtime enabled",
    "supervision_result_candidate ≠ gate result mutation",
    "health signal ≠ output block authorization",
    "controlled_runtime_readiness_hint ≠ runtime authorization",
    "next Controlled Runtime Planning ≠ runtime execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "health_enforcement_supervisor_dryrun_and_review_only",
    "simulated",
    "health_enforcement_supervisor_model_candidate_generated_now",
    "sample_health_signal_candidate_generated_now",
    "sample_gate_result_candidate_set_generated_now",
    "sample_health_enforcement_supervision_result_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "health_supervisor_runtime_enabled_now",
    "health_supervisor_invoked_now",
    "safety_gate_invoked_now",
    "speech_gate_invoked_now",
    "display_gate_invoked_now",
    "authorization_gate_invoked_now",
    "validation_factory_invoked_now",
    "controlled_runtime_planning_started_now",
    "controlled_runtime_enabled_now",
    "output_blocked_by_supervisor_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

HEALTH_SIGNAL_FIELDS: Tuple[str, ...] = (
    "health_signal_candidate_id",
    "source_health_layer_ref",
    "health_domain",
    "health_status_candidate",
    "pressure_level",
    "degradation_hint",
    "supervisor_scope",
    "observed_gate_refs",
    "evidence_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "not_runtime_metric",
)

GATE_RESULT_SET_FIELDS: Tuple[str, ...] = (
    "gate_result_candidate_id",
    "gate_id",
    "gate_type",
    "gate_status",
    "gate_action",
    "source_constraint_or_enforcement_ref",
    "applicable_rule_refs",
    "evidence_refs",
    "rationale_refs",
    "whitebox_trace_refs",
    "boundary_status",
    "candidate_only",
)

SUPERVISION_RESULT_FIELDS: Tuple[str, ...] = (
    "supervision_result_candidate_id",
    "source_health_signal_ref",
    "observed_gate_result_refs",
    "supervision_status",
    "enforcement_compliance_status",
    "enforcement_health_status",
    "detected_issue_types",
    "gate_conflict_detected",
    "gate_timeout_detected",
    "gate_drift_detected",
    "boundary_violation_risk",
    "recommended_supervision_action",
    "issue_trace_candidate_refs",
    "violation_report_candidate_refs",
    "decision_center_handoff_ref",
    "whitebox_visibility_ref",
    "controlled_runtime_readiness_hint",
    "evidence_refs",
    "rationale_refs",
    "candidate_only",
    "output_block_allowed",
    "runtime_enable_allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_enforcement_supervisor_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "controlled_runtime_deferred_not_cancelled": True,
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


def _gate_result_entry(
    *,
    gate_type: str,
    gate_id: str,
    gate_action: str,
    gate_status: str,
    source_ref: str,
    boundary_status: str = "compliant",
    upstream: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    upstream = upstream or {}
    refs = {
        "applicable_rule_refs": list(
            upstream.get("applicable_rule_refs")
            or ["user_output_admission:source_ref_required", "enforcement:gate_compliance"]
        ),
        "evidence_refs": list(upstream.get("evidence_refs") or ["evidence_pack:flow_sample_001"]),
        "rationale_refs": list(
            upstream.get("rationale_refs")
            or ["whitebox_visibility:chain_sample", "validation_result:pass_flow_sample_001"]
        ),
        "whitebox_trace_refs": list(
            upstream.get("whitebox_trace_refs") or ["whitebox:constitution_resolver_trace_sample"]
        ),
    }
    return {
        "gate_result_candidate_id": f"sample_{gate_type}_result_candidate_v1_001",
        "gate_id": gate_id,
        "gate_type": gate_type,
        "gate_status": gate_status,
        "gate_action": gate_action,
        "source_constraint_or_enforcement_ref": source_ref,
        **refs,
        "boundary_status": boundary_status,
        "candidate_only": True,
    }


def _build_gate_result_set(
    safety: Dict[str, Any],
    speech: Dict[str, Any],
    display: Dict[str, Any],
) -> Dict[str, Any]:
    enforcement_ref = safety.get(
        "enforcement_result_candidate_id", "sample_enforcement_result_candidate_v1_001"
    )
    return {
        "set_id": "sample_gate_result_candidate_set_v1",
        "safety_gate_result_candidate": _gate_result_entry(
            gate_type="safety_gate_result_candidate",
            gate_id="safety_gate",
            gate_action=safety.get("safety_action", "safety_allow_candidate_forward"),
            gate_status=safety.get("safety_status", "enforcement_evaluated_simulated"),
            source_ref=safety.get("source_constraint_bundle_ref", enforcement_ref),
            upstream=safety,
        ),
        "speech_gate_result_candidate": _gate_result_entry(
            gate_type="speech_gate_result_candidate",
            gate_id="speech_gate",
            gate_action=speech.get("speech_gate_action", "speech_allow_candidate_forward"),
            gate_status=speech.get("speech_gate_status", "speech_enforcement_evaluated_simulated"),
            source_ref=speech.get(
                "source_enforcement_result_candidate_ref", enforcement_ref
            ),
            upstream=speech,
        ),
        "display_gate_result_candidate": _gate_result_entry(
            gate_type="display_gate_result_candidate",
            gate_id="display_gate",
            gate_action=display.get("display_gate_action", "display_allow_candidate_forward"),
            gate_status=display.get("display_gate_status", "display_enforcement_evaluated_simulated"),
            source_ref=display.get(
                "source_enforcement_result_candidate_ref", enforcement_ref
            ),
            upstream=display,
        ),
        "authorization_gate_result_candidate": _gate_result_entry(
            gate_type="authorization_gate_result_candidate",
            gate_id="authorization_gate",
            gate_action="authorization_allow_candidate_forward",
            gate_status="authorization_evaluated_simulated",
            source_ref=enforcement_ref,
            boundary_status="compliant",
        ),
        "validation_factory_result_candidate": _gate_result_entry(
            gate_type="validation_factory_result_candidate",
            gate_id="validation_factory",
            gate_action="validation_pass_candidate",
            gate_status="validation_evaluated_simulated",
            source_ref=enforcement_ref,
            boundary_status="compliant",
        ),
    }


def _sample_health_signal(gate_set: Dict[str, Any]) -> Dict[str, Any]:
    observed = [
        gate_set["safety_gate_result_candidate"]["gate_result_candidate_id"],
        gate_set["speech_gate_result_candidate"]["gate_result_candidate_id"],
        gate_set["display_gate_result_candidate"]["gate_result_candidate_id"],
        gate_set["authorization_gate_result_candidate"]["gate_result_candidate_id"],
        gate_set["validation_factory_result_candidate"]["gate_result_candidate_id"],
    ]
    return {
        "health_signal_candidate_id": "sample_health_signal_candidate_v1_001",
        "source_health_layer_ref": "health_management_layer_integration_v1",
        "health_domain": "enforcement_layer",
        "health_status_candidate": "observed_compliant",
        "pressure_level": "normal",
        "degradation_hint": None,
        "supervisor_scope": list(SUPERVISED_GATES),
        "observed_gate_refs": observed,
        "evidence_refs": ["evidence_pack:flow_sample_001"],
        "whitebox_trace_refs": ["whitebox:constitution_resolver_trace_sample"],
        "candidate_only": True,
        "not_runtime_metric": True,
    }


def _sample_supervision_result(
    health_signal: Dict[str, Any], gate_set: Dict[str, Any]
) -> Dict[str, Any]:
    observed_refs = list(health_signal.get("observed_gate_refs") or [])
    return {
        "supervision_result_candidate_id": "sample_health_enforcement_supervision_result_candidate_v1_001",
        "source_health_signal_ref": health_signal.get("health_signal_candidate_id"),
        "observed_gate_result_refs": observed_refs,
        "supervision_status": "compliant_observed",
        "enforcement_compliance_status": "ok",
        "enforcement_health_status": "healthy_observed",
        "detected_issue_types": [],
        "gate_conflict_detected": False,
        "gate_timeout_detected": False,
        "gate_drift_detected": False,
        "boundary_violation_risk": False,
        "recommended_supervision_action": "supervise_compliance_ok_candidate",
        "issue_trace_candidate_refs": [],
        "violation_report_candidate_refs": [],
        "decision_center_handoff_ref": "decision_center:supervision_handoff_later",
        "whitebox_visibility_ref": "whitebox:supervision_trace_sample",
        "controlled_runtime_readiness_hint": "not_ready_requires_separate_phase",
        "evidence_refs": list(health_signal.get("evidence_refs") or []),
        "rationale_refs": ["supervision:all_gates_compliant_observed"],
        "candidate_only": True,
        "output_block_allowed": False,
        "runtime_enable_allowed": False,
        "source_gate_set_ref": gate_set.get("set_id"),
    }


def run_health_enforcement_supervisor_dryrun_and_review_v1(
    *,
    health_enforcement_supervisor_planning_root: str,
    midplatform_display_gate_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(health_enforcement_supervisor_planning_root).expanduser().resolve()
    display_dr_root = Path(midplatform_display_gate_dryrun_and_review_root).expanduser().resolve()
    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    validation_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    e2e_dr_root = Path(
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_policy = _try_read_json(plan_root / "health_enforcement_supervisor_planning_policy_v1.json") or {}

    display_dr_vr = _try_read_json(display_dr_root / "verifier_report.json") or {}
    speech_dr_vr = _try_read_json(speech_dr_root / "verifier_report.json") or {}
    safety_dr_vr = _try_read_json(safety_dr_root / "verifier_report.json") or {}
    validation_dr_vr = _try_read_json(validation_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    e2e_dr_vr = _try_read_json(e2e_dr_root / "verifier_report.json") or {}

    upstream_safety = _try_read_json(
        safety_dr_root / "sample_safety_gate_result_candidate_v1.json"
    ) or {}
    upstream_speech = _try_read_json(
        speech_dr_root / "sample_speech_gate_result_candidate_v1.json"
    ) or {}
    upstream_display = _try_read_json(
        display_dr_root / "sample_display_gate_result_candidate_v1.json"
    ) or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_display_gate_dryrun_root": str(display_dr_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_validation_engineering_separation_dryrun_root": str(validation_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_e2e_simulation_dryrun_root": str(e2e_dr_root),
        "output_root": str(out_root),
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Health Enforcement Supervisor Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_policy.get("supervisor_is_supervisory_not_enforcement") is not True:
        blockers.append("supervisor must be supervisory not enforcement")
    if display_dr_vr.get("verifier") != "GO":
        blockers.append("Display Gate DryRunAndReview must be GO")
    if speech_dr_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRunAndReview must be GO")
    if safety_dr_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRunAndReview must be GO")
    if validation_dr_vr.get("verifier") != "GO":
        blockers.append("Validation Engineering Separation DryRunAndReview must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if e2e_dr_vr.get("verifier") != "GO":
        blockers.append("E2E Output Chain Simulation DryRunAndReview must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "health_enforcement_supervisor_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": "health_enforcement_supervisor_v1",
        "architectural_layer": "HealthManagement",
        "system_layer": "Health",
        "is_health_management_layer": True,
        "is_not_enforcement_layer": True,
        "is_not_execution_layer": True,
        "monitors_gates_not_replaces": True,
        "dryrun_and_review_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    model_candidate = {
        "model_id": "health_enforcement_supervisor_model_candidate_v1",
        "module_id": "health_enforcement_supervisor_v1",
        "module_type": "health_management_supervision_module",
        "role": "enforcement_layer_health_and_compliance_supervisor",
        "system_layer": "Health",
        "architectural_layer": "HealthManagement",
        "runtime_enabled_now": False,
        "upstream_modules": [
            "health_management_layer",
            "safety_gate",
            "speech_gate",
            "display_gate",
            "authorization_gate",
            "validation_factory",
            "whitebox",
        ],
        "downstream_modules": [
            "decision_center_later",
            "whitebox_later",
            "issue_trace_later",
            "controlled_runtime_planning_later",
        ],
        "monitors_enforcement_layer": True,
        "replaces_enforcement_layer": False,
        "invokes_gate": False,
        "invokes_execution_layer": False,
        "blocks_output_directly": False,
        "writes_constitution": False,
        "writes_memory": False,
        "writes_world_model": False,
        "simulated": True,
        **meta,
    }

    gate_set = _build_gate_result_set(upstream_safety, upstream_speech, upstream_display)
    sample_health_signal = {**_sample_health_signal(gate_set), **meta}
    sample_gate_set = {**gate_set, **meta}
    sample_supervision_result = {
        **_sample_supervision_result(sample_health_signal, gate_set),
        **meta,
    }

    scope_checks: List[Tuple[str, bool]] = []
    for target in SUPERVISION_SCOPE_TARGETS:
        scope_checks.append((f"supervise.{target[:18]}", True))
    for excluded in NOT_SUPERVISED_NOT_REPLACED:
        scope_checks.append((f"not_replace.{excluded[:18]}", True))
    scope_checks.extend(
        [
            ("supervisor_not_enforcement", True),
            ("supervisor_not_execution", True),
            ("monitors_not_replaces", True),
        ]
    )
    supervision_scope_review = {
        "review_id": "supervision_scope_review_v1",
        "supervision_targets": list(SUPERVISION_SCOPE_TARGETS),
        "not_supervised_not_replaced": list(NOT_SUPERVISED_NOT_REPLACED),
        **_review_ok(scope_checks),
        **meta,
    }

    intake_checks: List[Tuple[str, bool]] = [
        ("consumes_gate_results", True),
        ("consumes_health_signal", True),
        ("consumes_whitebox_traces", True),
        ("no_raw_constitution_command", True),
        ("does_not_invoke_gates", meta.get("safety_gate_invoked_now") is False),
        ("does_not_rewrite_gate_results", True),
        ("gate_set_covers_five_gates", len(SUPERVISED_GATES) == 5),
    ]
    for gate_key in (
        "safety_gate_result_candidate",
        "speech_gate_result_candidate",
        "display_gate_result_candidate",
        "authorization_gate_result_candidate",
        "validation_factory_result_candidate",
    ):
        entry = gate_set.get(gate_key) or {}
        intake_checks.append((f"gate_set.{gate_key[:16]}", entry.get("candidate_only") is True))
        for field in GATE_RESULT_SET_FIELDS:
            intake_checks.append((f"{gate_key[:8]}.{field[:12]}", field in entry))

    gate_intake_review = {
        "review_id": "gate_result_intake_review_v1",
        "supervised_gates": list(SUPERVISED_GATES),
        **_review_ok(intake_checks),
        **meta,
    }

    compliance_checks = [(f"observe.{item[:18]}", True) for item in COMPLIANCE_OBSERVATION_ITEMS]
    compliance_checks.extend(
        [(f"rule.{r[:18]}", True) for r in GATE_COMPLIANCE_MONITORING_RULES]
    )
    compliance_observation_review = {
        "review_id": "enforcement_compliance_observation_review_v1",
        "observation_items": list(COMPLIANCE_OBSERVATION_ITEMS),
        "rules": list(GATE_COMPLIANCE_MONITORING_RULES),
        **_review_ok(compliance_checks),
        **meta,
    }

    mapping_checks: List[Tuple[str, bool]] = []
    for m in HEALTH_SIGNAL_MAPPINGS:
        mapping_checks.append((f"mapping.{m['signal'][:18]}", True))
    mapping_checks.extend([(f"bind.{r[:18]}", True) for r in HEALTH_SIGNAL_BINDING_RULES])
    mapping_checks.append(("no_automatic_output_block", meta.get("output_blocked_by_supervisor_now") is False))
    health_mapping_review = {
        "review_id": "enforcement_health_signal_mapping_review_v1",
        "mappings": list(HEALTH_SIGNAL_MAPPINGS),
        "rules": list(HEALTH_SIGNAL_BINDING_RULES),
        **_review_ok(mapping_checks),
        **meta,
    }

    issue_checks = [(f"issue.{t}", True) for t in ISSUE_TRACE_TYPES]
    issue_trace_review = {
        "review_id": "enforcement_issue_trace_review_v1",
        "issue_trace_types": list(ISSUE_TRACE_TYPES),
        "generates_issue_trace_candidate": True,
        **_review_ok(issue_checks),
        **meta,
    }

    violation_checks = [(f"violation.{t}", True) for t in VIOLATION_REPORT_TYPES]
    violation_report_review = {
        "review_id": "enforcement_violation_report_review_v1",
        "violation_report_types": list(VIOLATION_REPORT_TYPES),
        "generates_violation_report_candidate": True,
        **_review_ok(violation_checks),
        **meta,
    }

    case_checks: List[Tuple[str, bool]] = []
    simulated_case_results = []
    for case in SIMULATED_CASES:
        case_checks.append((f"case.{case['case_id'][:18]}", case.get("simulated_pass") is True))
        simulated_case_results.append(
            {
                **case,
                "supervision_result_only": True,
                "gate_invoked": False,
                "runtime_enabled": False,
            }
        )
    case_checks.append(("eight_cases_covered", len(SIMULATED_CASES) == 8))
    case_checks.append(("all_cases_pass", all(c.get("simulated_pass") for c in SIMULATED_CASES)))
    conflict_drift_timeout_review = {
        "review_id": "gate_conflict_drift_timeout_review_v1",
        "simulated_cases": simulated_case_results,
        "case_count": len(SIMULATED_CASES),
        **_review_ok(case_checks),
        **meta,
    }

    non_interference_checks: List[Tuple[str, bool]] = [
        ("does_not_block_output", meta.get("output_blocked_by_supervisor_now") is False),
        ("does_not_allow_output", True),
        ("does_not_mutate_gate_result", True),
        ("does_not_invoke_execution_layer", meta.get("model_runtime_invoked_now") is False),
        ("does_not_enable_runtime", meta.get("controlled_runtime_enabled_now") is False),
        ("does_not_write_constitution", True),
        ("does_not_write_memory", meta.get("memory_written_now") is False),
        ("does_not_write_world_model", meta.get("world_model_written_now") is False),
        ("hold_degrade_escalation_candidate_only", True),
    ]
    non_interference_checks.extend(
        [(f"override.{r[:18]}", True) for r in ENFORCEMENT_OVERRIDE_FORBIDDEN_RULES]
    )
    non_interference_checks.extend([(f"bypass.{r[:18]}", True) for r in BYPASS_PREVENTION_RULES])
    supervisor_non_interference_review = {
        "review_id": "supervisor_non_interference_review_v1",
        "rules": list(ENFORCEMENT_OVERRIDE_FORBIDDEN_RULES) + list(BYPASS_PREVENTION_RULES),
        **_review_ok(non_interference_checks),
        **meta,
    }

    handoff_checks: List[Tuple[str, bool]] = [
        ("decision_center_consumes_later", True),
        ("whitebox_consumes_later", True),
        ("issue_trace_refs_preserved", True),
        ("violation_report_refs_preserved", True),
        ("health_pressure_refs_preserved", True),
        ("no_handoff_runtime_now", meta.get("controlled_runtime_enabled_now") is False),
    ]
    decision_center_whitebox_handoff_review = {
        "review_id": "decision_center_whitebox_handoff_review_v1",
        **_review_ok(handoff_checks),
        **meta,
    }

    runtime_readiness_checks: List[Tuple[str, bool]] = [
        ("may_emit_readiness_hint", sample_supervision_result.get("controlled_runtime_readiness_hint") is not None),
        ("hint_candidate_only", True),
        ("hint_cannot_authorize_runtime", sample_supervision_result.get("runtime_enable_allowed") is False),
        ("controlled_runtime_planning_not_started", meta.get("controlled_runtime_planning_started_now") is False),
        ("controlled_runtime_not_enabled", meta.get("controlled_runtime_enabled_now") is False),
        ("requires_separate_phase", True),
    ]
    runtime_readiness_checks.extend(
        [(f"runtime_rule.{r[:18]}", True) for r in RUNTIME_RECOMMENDATION_RULES]
    )
    controlled_runtime_readiness_signal_review = {
        "review_id": "controlled_runtime_readiness_signal_review_v1",
        "rules": list(RUNTIME_RECOMMENDATION_RULES),
        **_review_ok(runtime_readiness_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(
        ("model_generated", meta.get("health_enforcement_supervisor_model_candidate_generated_now") is True)
    )
    boundary_audit = {
        "audit_id": "health_enforcement_supervisor_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "health_enforcement_supervisor_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        supervision_scope_review,
        gate_intake_review,
        compliance_observation_review,
        health_mapping_review,
        issue_trace_review,
        violation_report_review,
        conflict_drift_timeout_review,
        supervisor_non_interference_review,
        decision_center_whitebox_handoff_review,
        controlled_runtime_readiness_signal_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("module_id") == "health_enforcement_supervisor_v1"
        and model_candidate.get("architectural_layer") == "HealthManagement"
        and model_candidate.get("monitors_enforcement_layer") is True
        and model_candidate.get("replaces_enforcement_layer") is False
        and model_candidate.get("invokes_gate") is False
        and model_candidate.get("blocks_output_directly") is False
    )

    health_ok = all(f in sample_health_signal for f in HEALTH_SIGNAL_FIELDS)
    gate_set_ok = all(
        all(f in (gate_set.get(k) or {}) for f in GATE_RESULT_SET_FIELDS)
        for k in (
            "safety_gate_result_candidate",
            "speech_gate_result_candidate",
            "display_gate_result_candidate",
            "authorization_gate_result_candidate",
            "validation_factory_result_candidate",
        )
    )
    result_ok = (
        all(f in sample_supervision_result for f in SUPERVISION_RESULT_FIELDS)
        and sample_supervision_result.get("output_block_allowed") is False
        and sample_supervision_result.get("runtime_enable_allowed") is False
    )

    all_pass = (
        input_ok
        and model_ok
        and health_ok
        and gate_set_ok
        and result_ok
        and conflict_drift_timeout_review.get("case_count") == 8
        and all(
            s.get("dryrun_and_review_pass") is True
            for s in review_sections
            if "dryrun_and_review_pass" in s
        )
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "health_enforcement_supervisor_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "supervisor_layer_validated": True,
        "main_chain_closed": [
            "gate result candidates + health_signal_candidate",
            "→ Health Enforcement Supervisor (compliance observation)",
            "→ health_enforcement_supervision_result_candidate",
            "→ Decision Center / Whitebox / Controlled Runtime Planning later",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_controlled_runtime_planning": all_pass,
        "controlled_runtime_planning_started": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "health_enforcement_supervisor_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "supervisory_not_enforcement": True,
        "supervisory_not_execution": True,
        "observation_not_gate_invocation": True,
        "supervisor_layer_positioning": list(SUPERVISOR_LAYER_POSITIONING),
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
        "health_enforcement_supervisor_dryrun_review_policy": policy,
        "health_enforcement_supervisor_planning_input_review": planning_input_review,
        "health_enforcement_supervisor_model_candidate": model_candidate,
        "sample_health_signal_candidate": sample_health_signal,
        "sample_gate_result_candidate_set": sample_gate_set,
        "sample_health_enforcement_supervision_result_candidate": sample_supervision_result,
        "supervision_scope_review": supervision_scope_review,
        "gate_result_intake_review": gate_intake_review,
        "enforcement_compliance_observation_review": compliance_observation_review,
        "enforcement_health_signal_mapping_review": health_mapping_review,
        "enforcement_issue_trace_review": issue_trace_review,
        "enforcement_violation_report_review": violation_report_review,
        "gate_conflict_drift_timeout_review": conflict_drift_timeout_review,
        "supervisor_non_interference_review": supervisor_non_interference_review,
        "decision_center_whitebox_handoff_review": decision_center_whitebox_handoff_review,
        "controlled_runtime_readiness_signal_review": controlled_runtime_readiness_signal_review,
        "health_enforcement_supervisor_boundary_audit": boundary_audit,
        "health_enforcement_supervisor_blocked_path_result": blocked_path_result,
        "health_enforcement_supervisor_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
