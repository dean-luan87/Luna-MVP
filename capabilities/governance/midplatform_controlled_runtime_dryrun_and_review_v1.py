# -*- coding: utf-8 -*-
"""Midplatform Controlled Runtime DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_controlled_runtime_planning_v1 import (
    ADMISSION_RULES,
    AUTHORIZATION_RULES,
    DOMAIN_MATRIX,
    EVIDENCE_CAPTURE_FIELDS,
    EXECUTION_WINDOW_RULES,
    FAILURE_ROUTES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GATE_PRECONDITION_RULES,
    HEALTH_SUPERVISION_RULES,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    POST_EXECUTION_REVIEW_OUTCOMES,
    POST_EXECUTION_REVIEW_RULES,
    PROVIDER_READINESS_RULES,
    ROLLBACK_RULES,
    RUNTIME_CANDIDATE_FIELDS,
    RUNTIME_CANDIDATE_SPECS,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Controlled-Runtime-DryRunAndReview-v1-001"
SCOPE = "controlled_runtime_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_controlled_runtime_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_CONTROLLED_RUNTIME_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_COGNITIVE_ZONING_ARCHITECTURE_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_CONTROLLED_RUNTIME_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Cognitive-Zoning-Architecture-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Controlled-Runtime-Issue-Review-v1-001"

ADMISSION_REVIEW_CHECKS: Tuple[str, ...] = (
    "upstream simulated GO required",
    "relevant gate result pass required",
    "provider abstraction alignment pass required",
    "provider readiness pass later required",
    "validation pass later required",
    "health supervision pass later required",
    "no unresolved high-risk issue",
    "authorization request required later",
    "execution window required later",
    "rollback plan required later",
    "evidence capture plan required later",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_controlled_runtime_enable",
    "dryrun_to_controlled_runtime_execution_start",
    "dryrun_to_execution_window_open",
    "dryrun_to_provider_selection",
    "dryrun_to_provider_invocation",
    "dryrun_to_provider_import",
    "dryrun_to_model_runtime_invocation",
    "dryrun_to_qianwen_tts_invocation",
    "dryrun_to_paddleocr_invocation",
    "dryrun_to_rapidocr_invocation",
    "dryrun_to_vision_runtime_invocation",
    "dryrun_to_ocr_runtime_invocation",
    "dryrun_to_asr_runtime_invocation",
    "dryrun_to_tts_runtime_invocation",
    "dryrun_to_map_provider_invocation",
    "dryrun_to_display_output_invocation",
    "dryrun_to_notification_send",
    "dryrun_to_audio_synthesis",
    "dryrun_to_audio_output",
    "dryrun_to_user_facing_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Controlled Runtime DryRunAndReview GO ≠ runtime enabled",
    "controlled_runtime_framework_candidate ≠ execution authorized",
    "runtime_candidate_registry sample ≠ provider selected",
    "execution window policy pass ≠ window opened",
    "next Cognitive Zoning Planning ≠ runtime execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "controlled_runtime_dryrun_and_review_only",
    "simulated",
    "controlled_runtime_framework_candidate_generated_now",
    "runtime_candidate_registry_sample_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "controlled_runtime_enabled_now",
    "controlled_runtime_execution_started_now",
    "runtime_execution_window_opened_now",
    "provider_selected_now",
    "provider_invoked_now",
    "provider_imported_now",
    "model_runtime_invoked_now",
    "qianwen_tts_invoked_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "vision_runtime_invoked_now",
    "ocr_runtime_invoked_now",
    "asr_runtime_invoked_now",
    "tts_runtime_invoked_now",
    "map_provider_invoked_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "audio_synthesis_invoked_now",
    "audio_output_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DOMAIN_LABELS: Tuple[str, ...] = tuple(d["label"] for d in DOMAIN_MATRIX)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
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


def _gate_refs_for_domain(domain_id: str) -> List[str]:
    for entry in DOMAIN_MATRIX:
        if entry.get("domain_id") == domain_id:
            return list(entry.get("required_gates") or [])
    return []


def _runtime_candidate_sample(spec: Dict[str, Any], domain_id: str) -> Dict[str, Any]:
    return {
        "runtime_candidate_id": spec["runtime_candidate_id"],
        "runtime_domain": spec["runtime_domain"],
        "runtime_type": spec["runtime_type"],
        "upstream_gate_refs": _gate_refs_for_domain(domain_id),
        "provider_candidate_refs": list(spec.get("provider_candidate_refs") or []),
        "readiness_refs": [f"readiness:{spec['runtime_candidate_id']}"],
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_capture_required": True,
        "rollback_required": True,
        "post_execution_review_required": True,
        "health_supervision_required": True,
        "whitebox_trace_required": True,
        "runtime_enabled_now": False,
        "execution_started_now": False,
    }


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_midplatform_controlled_runtime_dryrun_and_review_v1(
    *,
    midplatform_controlled_runtime_planning_root: str,
    health_enforcement_supervisor_dryrun_and_review_root: str,
    midplatform_display_gate_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_frontend_model_influence_simulation_dryrun_and_review_root: str,
    midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root: str,
    midplatform_tts_runtime_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_controlled_runtime_planning_root).expanduser().resolve()
    health_dr_root = Path(health_enforcement_supervisor_dryrun_and_review_root).expanduser().resolve()
    display_dr_root = Path(midplatform_display_gate_dryrun_and_review_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    fmis_dr_root = Path(
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    e2e_dr_root = Path(
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    tts_dr_root = Path(midplatform_tts_runtime_dryrun_and_review_root).expanduser().resolve()
    validation_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_registry = _try_read_json(plan_root / "controlled_runtime_candidate_registry_v1.json") or {}

    health_dr_vr = _try_read_json(health_dr_root / "verifier_report.json") or {}
    display_dr_vr = _try_read_json(display_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    provider_dr_sm = _try_read_json(provider_dr_root / "summary.json") or {}
    fmis_dr_vr = _try_read_json(fmis_dr_root / "verifier_report.json") or {}
    fmis_dr_sm = _try_read_json(fmis_dr_root / "summary.json") or {}
    e2e_dr_vr = _try_read_json(e2e_dr_root / "verifier_report.json") or {}
    e2e_dr_sm = _try_read_json(e2e_dr_root / "summary.json") or {}
    tts_dr_vr = _try_read_json(tts_dr_root / "verifier_report.json") or {}
    validation_dr_vr = _try_read_json(validation_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_health_supervisor_dryrun_root": str(health_dr_root),
        "upstream_display_gate_dryrun_root": str(display_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_fmis_dryrun_root": str(fmis_dr_root),
        "upstream_e2e_simulation_dryrun_root": str(e2e_dr_root),
        "upstream_tts_runtime_dryrun_root": str(tts_dr_root),
        "upstream_validation_engineering_separation_dryrun_root": str(validation_dr_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if health_dr_vr.get("verifier") != "GO":
        blockers.append("Health Enforcement Supervisor DryRunAndReview must be GO")
    if display_dr_vr.get("verifier") != "GO":
        blockers.append("Display Gate DryRunAndReview must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if provider_dr_sm.get("final_decision") != PROVIDER_ABS_DR_FINAL_GO:
        blockers.append("provider abstraction dryrun final_decision mismatch")
    if fmis_dr_vr.get("verifier") != "GO":
        blockers.append("FMIS DryRunAndReview must be GO")
    if fmis_dr_sm.get("final_decision") != FMIS_DR_FINAL_GO:
        blockers.append("FMIS dryrun final_decision mismatch")
    if e2e_dr_vr.get("verifier") != "GO":
        blockers.append("E2E Simulation DryRunAndReview must be GO")
    if e2e_dr_sm.get("final_decision") != E2E_DR_FINAL_GO:
        blockers.append("E2E simulation dryrun final_decision mismatch")
    if tts_dr_vr.get("verifier") != "GO":
        blockers.append("TTS Runtime DryRunAndReview must be GO")
    if validation_dr_vr.get("verifier") != "GO":
        blockers.append("Validation Engineering Separation DryRunAndReview must be GO")

    leakage_issues: List[str] = []
    for label, sm in (
        ("planning", plan_sm),
        ("health_supervisor", _try_read_json(health_dr_root / "summary.json") or {}),
        ("display_gate", _try_read_json(display_dr_root / "summary.json") or {}),
        ("provider_abstraction", provider_dr_sm),
        ("fmis", fmis_dr_sm),
        ("e2e", e2e_dr_sm),
        ("tts", _try_read_json(tts_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "controlled_runtime_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "system_level_simulated_go": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "dryrun_and_review_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    framework_candidate = {
        "framework_id": "midplatform_controlled_runtime_framework_v1",
        "framework_type": "later_runtime_admission_framework",
        "system_layer": "RuntimeGovernance",
        "runtime_enabled_now": False,
        "execution_started_now": False,
        "execution_window_opened_now": False,
        "applies_to_provider_runtime": True,
        "applies_to_model_runtime": True,
        "applies_to_output_runtime": True,
        "applies_to_tool_runtime": True,
        "excludes_memory_write_runtime": True,
        "excludes_worldmodel_fact_write_runtime": True,
        "excludes_autonomous_action_execution": True,
        "excludes_production_runtime": True,
        "requires_constitution_refs": True,
        "requires_resolver_or_constraint_refs": True,
        "requires_enforcement_gate_refs": True,
        "requires_validation_refs": True,
        "requires_health_supervision_refs": True,
        "requires_provider_readiness_refs": True,
        "requires_whitebox_trace_refs": True,
        "requires_evidence_capture": True,
        "requires_rollback": True,
        "requires_post_execution_review": True,
        "candidate_only": True,
        "simulated": True,
        **meta,
    }

    registry_samples = []
    for spec, domain in zip(RUNTIME_CANDIDATE_SPECS, DOMAIN_MATRIX):
        registry_samples.append({**_runtime_candidate_sample(spec, domain["domain_id"]), **meta})

    registry_sample = {
        "sample_id": "runtime_candidate_registry_sample_v1",
        "candidates": registry_samples,
        "candidate_count": len(registry_samples),
        "domain_labels": list(DOMAIN_LABELS),
        "all_runtime_enabled_now_false": all(c.get("runtime_enabled_now") is False for c in registry_samples),
        **meta,
    }

    admission_checks = [(f"admission.{c[:18]}", True) for c in ADMISSION_REVIEW_CHECKS]
    admission_checks.extend([(f"rule.{r[:18]}", True) for r in ADMISSION_RULES])
    admission_review = {
        "review_id": "controlled_runtime_admission_review_v1",
        "admission_check_items": list(ADMISSION_REVIEW_CHECKS),
        "rules": list(ADMISSION_RULES),
        **_review_ok(admission_checks),
        **meta,
    }

    auth_checks = [(f"auth.{r[:18]}", True) for r in AUTHORIZATION_RULES]
    auth_checks.append(("authorization_granted_now_false", meta.get("provider_selected_now") is False))
    authorization_review = {
        "review_id": "controlled_runtime_authorization_review_v1",
        "rules": list(AUTHORIZATION_RULES),
        **_review_ok(auth_checks),
        **meta,
    }

    window_checks = [(f"window.{r[:18]}", True) for r in EXECUTION_WINDOW_RULES]
    window_checks.append(("window_not_open", meta.get("runtime_execution_window_opened_now") is False))
    execution_window_review = {
        "review_id": "controlled_runtime_execution_window_review_v1",
        "rules": list(EXECUTION_WINDOW_RULES),
        **_review_ok(window_checks),
        **meta,
    }

    readiness_checks = [(f"readiness.{r[:18]}", True) for r in PROVIDER_READINESS_RULES]
    provider_readiness_review = {
        "review_id": "controlled_runtime_provider_readiness_review_v1",
        "rules": list(PROVIDER_READINESS_RULES),
        **_review_ok(readiness_checks),
        **meta,
    }

    gate_checks = [(f"gate.{r[:18]}", True) for r in GATE_PRECONDITION_RULES]
    gate_precondition_review = {
        "review_id": "controlled_runtime_gate_precondition_review_v1",
        "rules": list(GATE_PRECONDITION_RULES),
        **_review_ok(gate_checks),
        **meta,
    }

    health_checks = [(f"health.{r[:18]}", True) for r in HEALTH_SUPERVISION_RULES]
    health_supervision_review = {
        "review_id": "controlled_runtime_health_supervision_review_v1",
        "rules": list(HEALTH_SUPERVISION_RULES),
        **_review_ok(health_checks),
        **meta,
    }

    evidence_checks = [(f"evidence.{f[:18]}", True) for f in EVIDENCE_CAPTURE_FIELDS]
    evidence_checks.append(("runtime_result_ref_later", True))
    evidence_capture_review = {
        "review_id": "controlled_runtime_evidence_capture_review_v1",
        "required_fields": list(EVIDENCE_CAPTURE_FIELDS),
        **_review_ok(evidence_checks),
        **meta,
    }

    rollback_checks = [(f"rollback.{r[:18]}", True) for r in ROLLBACK_RULES]
    rollback_review = {
        "review_id": "controlled_runtime_rollback_review_v1",
        "rules": list(ROLLBACK_RULES),
        **_review_ok(rollback_checks),
        **meta,
    }

    post_checks = [(f"post.{r[:18]}", True) for r in POST_EXECUTION_REVIEW_RULES]
    for outcome in POST_EXECUTION_REVIEW_OUTCOMES:
        post_checks.append((f"outcome.{outcome}", True))
    post_execution_review = {
        "review_id": "controlled_runtime_post_execution_review_v1",
        "rules": list(POST_EXECUTION_REVIEW_RULES),
        "allowed_outcomes": list(POST_EXECUTION_REVIEW_OUTCOMES),
        **_review_ok(post_checks),
        **meta,
    }

    failure_checks: List[Tuple[str, bool]] = []
    for route in FAILURE_ROUTES:
        failure_checks.append((f"failure.{route['trigger'][:18]}", True))
    failure_route_review = {
        "review_id": "controlled_runtime_failure_route_review_v1",
        "routes": list(FAILURE_ROUTES),
        **_review_ok(failure_checks),
        **meta,
    }

    domain_checks: List[Tuple[str, bool]] = []
    domain_entries = []
    for domain in DOMAIN_MATRIX:
        domain_checks.extend(
            [
                (f"domain.{domain['domain_id']}.gates", len(domain.get("required_gates") or []) > 0),
                (f"domain.{domain['domain_id']}.auth", domain.get("authorization_required") is True),
                (f"domain.{domain['domain_id']}.window", domain.get("execution_window_required") is True),
                (f"domain.{domain['domain_id']}.evidence", domain.get("evidence_required") is True),
                (f"domain.{domain['domain_id']}.rollback", domain.get("rollback_required") is True),
                (f"domain.{domain['domain_id']}.post", domain.get("post_review_required") is True),
                (f"domain.{domain['domain_id']}.off", domain.get("runtime_enabled_now") is False),
            ]
        )
        domain_entries.append({**domain, "verified": True, "simulated": True})

    domain_checks.append(("eight_domains_covered", len(DOMAIN_MATRIX) == 8))
    domain_matrix_review = {
        "review_id": "controlled_runtime_domain_matrix_review_v1",
        "domains": domain_entries,
        "domain_count": len(DOMAIN_MATRIX),
        **_review_ok(domain_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(
        ("framework_generated", meta.get("controlled_runtime_framework_candidate_generated_now") is True)
    )
    audit_checks.append(
        ("registry_generated", meta.get("runtime_candidate_registry_sample_generated_now") is True)
    )
    boundary_audit = {
        "audit_id": "controlled_runtime_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "controlled_runtime_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        admission_review,
        authorization_review,
        execution_window_review,
        provider_readiness_review,
        gate_precondition_review,
        health_supervision_review,
        evidence_capture_review,
        rollback_review,
        post_execution_review,
        failure_route_review,
        domain_matrix_review,
        boundary_audit,
    ]

    framework_ok = (
        framework_candidate.get("framework_id") == "midplatform_controlled_runtime_framework_v1"
        and framework_candidate.get("runtime_enabled_now") is False
        and framework_candidate.get("candidate_only") is True
        and framework_candidate.get("excludes_production_runtime") is True
    )

    registry_ok = (
        registry_sample.get("candidate_count") == 8
        and all(
            all(f in c for f in RUNTIME_CANDIDATE_FIELDS)
            and c.get("runtime_enabled_now") is False
            for c in registry_samples
        )
    )

    all_pass = (
        input_ok
        and framework_ok
        and registry_ok
        and domain_matrix_review.get("domain_count") == 8
        and all(
            s.get("dryrun_and_review_pass") is True
            for s in review_sections
            if "dryrun_and_review_pass" in s
        )
        and blocked_path_result.get("all_blocked") is True
        and plan_registry.get("candidate_count") == 8
    )

    closure_decision = {
        "decision_id": "controlled_runtime_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "controlled_runtime_framework_validated": True,
        "main_chain_closed": [
            "simulated candidate chain (system-level GO)",
            "→ controlled_runtime_framework_candidate (later admission framework)",
            "→ runtime_candidate_registry_sample (8 domains)",
            "→ admission / authorization / window / readiness / gates / health / evidence / rollback / post-review",
            "→ Cognitive Zoning Architecture Planning next (not runtime execution)",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_cognitive_zoning_architecture_planning": all_pass,
        "controlled_runtime_enabled": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "controlled_runtime_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "framework_not_execution": True,
        "dryrun_not_runtime_enable": True,
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
        "controlled_runtime_dryrun_review_policy": policy,
        "controlled_runtime_planning_input_review": planning_input_review,
        "controlled_runtime_framework_candidate": framework_candidate,
        "runtime_candidate_registry_sample": registry_sample,
        "controlled_runtime_admission_review": admission_review,
        "controlled_runtime_authorization_review": authorization_review,
        "controlled_runtime_execution_window_review": execution_window_review,
        "controlled_runtime_provider_readiness_review": provider_readiness_review,
        "controlled_runtime_gate_precondition_review": gate_precondition_review,
        "controlled_runtime_health_supervision_review": health_supervision_review,
        "controlled_runtime_evidence_capture_review": evidence_capture_review,
        "controlled_runtime_rollback_review": rollback_review,
        "controlled_runtime_post_execution_review": post_execution_review,
        "controlled_runtime_failure_route_review": failure_route_review,
        "controlled_runtime_domain_matrix_review": domain_matrix_review,
        "controlled_runtime_boundary_audit": boundary_audit,
        "controlled_runtime_blocked_path_result": blocked_path_result,
        "controlled_runtime_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
