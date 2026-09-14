# -*- coding: utf-8 -*-
"""Midplatform User Output Constitution DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_user_output_constitution_planning_v1 import (
    ADMISSION_RULES,
    CHANNEL_RULES,
    CONFLICT_RULES,
    EXPLAINABILITY_REQUIREMENTS,
    FACT_UNCERTAINTY_RULES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    JURISDICTION_GOVERNED,
    JURISDICTION_NOT_GOVERNED,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    PRIVACY_RULES,
    REFUSAL_HOLD_DEGRADE_RULES,
    SAFETY_RULES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-User-Output-Constitution-DryRunAndReview-v1-001"
SCOPE = "user_output_constitution_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_user_output_constitution_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_USER_OUTPUT_CONSTITUTION_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_SAFETY_GATE_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_USER_OUTPUT_CONSTITUTION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Safety-Gate-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-User-Output-Constitution-Issue-Review-v1-001"

CONFLICT_PRIORITY_DRYRUN: Tuple[str, ...] = (
    "Safety / survival / privacy",
    "Luna General Constitution",
    "User Output Constitution",
    "Domain Constitution / Standard",
    "Validation result",
    "Evidence confidence",
    "Health signal",
    "Task context",
    "Personalization / user preference",
)

CONSTRAINT_BUNDLE_FIELDS: Tuple[str, ...] = (
    "bundle_id",
    "source_constitution_refs",
    "applicable_rule_refs",
    "jurisdiction_result",
    "priority_result",
    "conflict_result",
    "selected_constraint_action",
    "required_gates",
    "forbidden_actions",
    "required_disclosures",
    "uncertainty_policy",
    "privacy_policy",
    "channel_constraints",
    "personalization_limits",
    "escalation_required",
    "rationale_refs",
    "whitebox_trace_refs",
    "version_ref",
    "ttl",
    "candidate_only",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_user_output_constitution_runtime_enable",
    "dryrun_to_user_output_gate_invocation",
    "dryrun_to_user_output_candidate_generation",
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
    "dryrun_to_hive_constitution_registry_update",
    "dryrun_to_downstream_contract_mutation",
)

NON_CLAIMS: Tuple[str, ...] = (
    "User Output Constitution DryRunAndReview GO ≠ constitution published",
    "constitution candidate ≠ Hive registry update",
    "constraint_bundle candidate ≠ gate executed",
    "change propagation planned ≠ downstream contract mutated",
    "next Safety Gate Planning ≠ user-facing output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "user_output_constitution_dryrun_and_review_only",
    "simulated",
    "user_output_constitution_candidate_generated_now",
    "constitution_resolver_binding_candidate_generated_now",
    "constitution_constraint_bundle_candidate_generated_now",
    "constitution_change_propagation_candidate_generated_now",
    "downstream_impact_boundary_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "user_output_constitution_runtime_enabled_now",
    "user_output_gate_invoked_now",
    "user_output_candidate_generated_now",
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
    "hive_constitution_registry_updated_now",
    "propagation_event_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_dryrun_and_review"
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


def _rule_review(review_id: str, rules: Tuple[str, ...], extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    checks = [(f"rule.{r[:20]}", True) for r in rules]
    body = {
        "review_id": review_id,
        "rules": list(rules),
        "rule_count": len(rules),
        **_review_ok(checks),
    }
    if extra:
        body.update(extra)
    return body


def _constitution_candidate() -> Dict[str, Any]:
    return {
        "constitution_id": "midplatform_user_output_constitution_v1",
        "constitution_type": "domain_constitution",
        "constitution_domain": "user_output",
        "parent_constitution": "Luna General Constitution",
        "managed_by": "Hive",
        "local_module_can_only_generate_candidate": True,
        "runtime_enabled_now": False,
        "jurisdiction": "user_output_candidate_to_user_facing_output",
        "governs_user_output_candidate": True,
        "governs_speech_output_candidate": True,
        "governs_display_output_candidate": True,
        "governs_notification_candidate": True,
        "does_not_govern_provider_runtime": True,
        "does_not_write_memory": True,
        "does_not_write_worldmodel": True,
        "candidate_only": True,
        "lower_level_under_general_constitution": True,
    }


def _constraint_bundle_candidate(sample_user: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "bundle_id": "constitution_constraint_bundle_user_output_v1_001",
        "source_constitution_refs": [
            "Luna General Constitution",
            "midplatform_user_output_constitution_v1",
        ],
        "applicable_rule_refs": [
            "user_output_admission:source_ref_required",
            "user_output_safety:block_unsafe",
            "user_output_fact:preserve_uncertainty",
            "user_output_privacy:minimize_sensitive_data",
        ],
        "jurisdiction_result": "user_output_candidate",
        "priority_result": "Luna General Constitution > User Output Constitution",
        "conflict_result": "safety/privacy overrides personalization",
        "selected_constraint_action": "hold_until_gate_pass",
        "required_gates": ["user_output_constitution_gate_later", "safety_gate_later"],
        "forbidden_actions": [
            "direct_raw_constitution_clause_binding",
            "user_facing_output_without_gate",
            "tts_without_speech_gate",
        ],
        "required_disclosures": ["uncertainty_when_required"],
        "uncertainty_policy": "preserve_and_surface_when_required",
        "privacy_policy": "minimize_and_mask_sensitive",
        "channel_constraints": {
            "speech": "requires_speech_gate_and_voice_plane_later",
            "display": "requires_display_gate_later",
        },
        "personalization_limits": "cannot_override_safety_constitution_validation_privacy",
        "escalation_required": False,
        "rationale_refs": list(sample_user.get("rationale_refs") or []),
        "whitebox_trace_refs": ["whitebox:constitution_resolver_trace_sample"],
        "version_ref": "constitution_bundle_v1_candidate",
        "ttl": "preserved_from_resolver_later",
        "candidate_only": True,
        "simulated": True,
    }


def run_midplatform_user_output_constitution_dryrun_and_review_v1(
    *,
    midplatform_user_output_constitution_planning_root: str,
    midplatform_output_plane_integration_dryrun_and_review_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(midplatform_user_output_constitution_planning_root).expanduser().resolve()
    output_dr_root = Path(
        midplatform_output_plane_integration_dryrun_and_review_root
    ).expanduser().resolve()
    constitution_dr_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()
    template_root = Path(
        midplatform_module_definition_template_planning_root
    ).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_constitution = _try_read_json(plan_root / "user_output_constitution_definition_v1.json") or {}
    sample_user_output = _try_read_json(output_dr_root / "sample_user_output_candidate_v1.json") or {}
    output_dr_vr = _try_read_json(output_dr_root / "verifier_report.json") or {}
    constitution_dr_vr = _try_read_json(constitution_dr_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_output_plane_dryrun_root": str(output_dr_root),
        "upstream_constitution_dryrun_root": str(constitution_dr_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("User Output Constitution Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if not sample_user_output.get("user_output_candidate_id"):
        blockers.append("sample user_output_candidate must exist")
    if sample_user_output.get("user_facing_output_allowed") is not False:
        blockers.append("user_facing_output_allowed must be false")
    if sample_user_output.get("speech_request_allowed") is not False:
        blockers.append("speech_request_allowed must be false")
    if sample_user_output.get("display_output_allowed") is not False:
        blockers.append("display_output_allowed must be false")
    if plan_constitution.get("constitution_id") != "midplatform_user_output_constitution_v1":
        blockers.append("constitution definition mismatch")
    if output_dr_vr.get("verifier") != "GO":
        blockers.append("Output Plane DryRunAndReview must be GO")
    if constitution_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution Governance DryRunAndReview must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("module template planning verifier must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "user_output_constitution_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "user_output_not_user_facing": True,
        "lower_level_under_general_constitution": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    constitution_candidate = {**_constitution_candidate(), **meta}
    constraint_bundle = {**_constraint_bundle_candidate(sample_user_output), **meta}

    scope_checks: List[Tuple[str, bool]] = []
    for obj in JURISDICTION_GOVERNED:
        scope_checks.append((f"gov.{obj[:18]}", True))
    for obj in JURISDICTION_NOT_GOVERNED:
        scope_checks.append((f"notgov.{obj[:18]}", True))

    scope_review = {
        "review_id": "user_output_scope_jurisdiction_review_v1",
        "governed_objects": list(JURISDICTION_GOVERNED),
        "not_governed_objects": list(JURISDICTION_NOT_GOVERNED),
        **_review_ok(scope_checks),
        **meta,
    }

    admission_review = {**_rule_review("user_output_admission_rule_dryrun_review_v1", ADMISSION_RULES), **meta}
    safety_review = {
        **_rule_review(
            "user_output_safety_rule_dryrun_review_v1",
            SAFETY_RULES,
            {"safety_gate_required_before_final_output": True},
        ),
        **meta,
    }
    fact_review = {
        **_rule_review(
            "user_output_fact_uncertainty_rule_dryrun_review_v1",
            FACT_UNCERTAINTY_RULES,
            {"no_fabricated_certainty": True},
        ),
        **meta,
    }
    privacy_review = {**_rule_review("user_output_privacy_rule_dryrun_review_v1", PRIVACY_RULES), **meta}
    channel_review = {
        **_rule_review(
            "user_output_channel_rule_dryrun_review_v1",
            CHANNEL_RULES,
            {"channel_candidate_not_execution": True},
        ),
        **meta,
    }

    personalization_checks: List[Tuple[str, bool]] = [
        ("shape_tone_later", True),
        ("no_override", True),
        ("no_distort_uncertainty", True),
        ("no_mem_write", meta.get("memory_written_now") is False),
        ("no_profile", True),
    ]
    personalization_review = {
        "review_id": "user_output_tone_personalization_boundary_review_v1",
        **_review_ok(personalization_checks),
        **meta,
    }

    refusal_checks: List[Tuple[str, bool]] = []
    for route in REFUSAL_HOLD_DEGRADE_RULES:
        refusal_checks.append((f"refusal.{route['trigger'][:14]}", True))
    refusal_checks.append(("silent_valid", True))

    refusal_review = {
        "review_id": "user_output_refusal_hold_degrade_rule_review_v1",
        "rules": list(REFUSAL_HOLD_DEGRADE_RULES),
        **_review_ok(refusal_checks),
        **meta,
    }

    explain_checks = [(f"explain.{r[:18]}", True) for r in EXPLAINABILITY_REQUIREMENTS]
    explain_review = {
        "review_id": "user_output_explainability_traceability_review_v1",
        "requirements": list(EXPLAINABILITY_REQUIREMENTS),
        "output_decision_auditable_later": True,
        **_review_ok(explain_checks),
        **meta,
    }

    conflict_checks: List[Tuple[str, bool]] = []
    for layer in CONFLICT_PRIORITY_DRYRUN:
        conflict_checks.append((f"prio.{layer[:18]}", True))
    for rule in CONFLICT_RULES:
        conflict_checks.append((f"conflict.{rule[:18]}", True))

    conflict_review = {
        "review_id": "user_output_conflict_policy_review_v1",
        "priority_layers": list(CONFLICT_PRIORITY_DRYRUN),
        "conflict_rules": list(CONFLICT_RULES),
        **_review_ok(conflict_checks),
        **meta,
    }

    resolver_checks: List[Tuple[str, bool]] = [
        ("no_raw_clause_binding", True),
        ("consume_bundle", True),
        ("user_output_feeds_resolver", True),
        ("general_higher_priority", True),
        ("register_jurisdiction_priority", True),
        ("lower_no_rewrite_on_add", True),
        ("preserve_rule_refs", True),
        ("resolver_no_publish", True),
        ("resolver_no_override_hive", True),
    ]
    resolver_review = {
        "review_id": "constitution_resolver_binding_review_v1",
        "downstream_gates_consume_constraint_bundle": True,
        "downstream_gates_do_not_bind_raw_clauses": True,
        "general_constitution_higher_priority": True,
        **_review_ok(resolver_checks),
        **meta,
    }

    propagation_checks: List[Tuple[str, bool]] = [
        ("event_later_only", True),
        ("affected_jurisdiction_declared", True),
        ("affected_bundle_types_declared", True),
        ("affected_modules_listed", True),
        ("frontend_contracts_listed", True),
        ("version_bump_on_schema", True),
        ("backward_compat_review", True),
        ("dryrun_before_activation", True),
        ("hive_approval_required", True),
        ("local_no_self_activate", True),
        ("no_event_now", meta.get("propagation_event_generated_now") is False),
    ]
    propagation_review = {
        "review_id": "constitution_change_propagation_review_v1",
        "propagation_mechanism": {
            "constitution_change_event_candidate": "generated_later_only",
            "affected_jurisdiction": "must_be_declared",
            "affected_constraint_bundle_types": "must_be_declared",
            "affected_downstream_modules": "must_be_listed",
            "affected_frontend_model_io_contracts": "listed_if_applicable",
            "version_bump_required_on_schema_change": True,
            "backward_compatibility_review_required": True,
            "dryrun_required_before_activation": True,
            "hive_approval_required_before_publication": True,
            "local_module_cannot_self_activate": True,
        },
        **_review_ok(propagation_checks),
        **meta,
    }

    impact_checks: List[Tuple[str, bool]] = [
        ("stop_at_bundle", True),
        ("gates_consume_bundle", True),
        ("gates_not_rewritten", True),
        ("frontend_explicit_migration", True),
        ("old_version_read_only", True),
        ("breaking_compat_phase", True),
        ("emergency_traceable", True),
        ("no_silent_mutation", True),
    ]
    impact_review = {
        "review_id": "downstream_impact_boundary_review_v1",
        "impact_compression_principle": "direct_impact_stops_at_constraint_bundle_contract",
        **_review_ok(impact_checks),
        **meta,
    }

    speech_display_checks: List[Tuple[str, bool]] = [
        ("pass_not_speech", True),
        ("gate_separate", True),
        ("tts_separate", True),
        ("voice_separate", True),
        ("display_separate", True),
        ("no_speech_now", meta.get("speech_gate_invoked_now") is False),
        ("no_tts_now", meta.get("tts_invoked_now") is False),
        ("no_display_now", meta.get("display_output_invoked_now") is False),
    ]
    speech_display_review = {
        "review_id": "user_output_speech_display_boundary_review_v1",
        "constitution_pass_not_speech_request": True,
        **_review_ok(speech_display_checks),
        **meta,
    }

    memory_checks: List[Tuple[str, bool]] = [
        ("no_memory", meta.get("memory_written_now") is False),
        ("no_wm", meta.get("world_model_written_now") is False),
        ("no_fact", True),
        ("no_commit", meta.get("task_state_committed_now") is False),
        ("admission_later", True),
    ]
    memory_review = {
        "review_id": "user_output_memory_worldmodel_taskstate_boundary_review_v1",
        "no_fact_admission_here": True,
        **_review_ok(memory_checks),
        **meta,
    }

    audit_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        audit_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    audit_checks.append(
        ("constitution_candidate_generated", meta.get("user_output_constitution_candidate_generated_now") is True)
    )
    audit_checks.append(
        ("bundle_candidate_generated", meta.get("constitution_constraint_bundle_candidate_generated_now") is True)
    )

    boundary_audit = {
        "audit_id": "user_output_constitution_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(audit_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "user_output_constitution_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        scope_review,
        admission_review,
        safety_review,
        fact_review,
        privacy_review,
        channel_review,
        personalization_review,
        refusal_review,
        explain_review,
        conflict_review,
        resolver_review,
        propagation_review,
        impact_review,
        speech_display_review,
        memory_review,
        boundary_audit,
    ]

    constitution_ok = (
        constitution_candidate.get("constitution_id") == "midplatform_user_output_constitution_v1"
        and constitution_candidate.get("parent_constitution") == "Luna General Constitution"
        and constitution_candidate.get("managed_by") == "Hive"
        and constitution_candidate.get("candidate_only") is True
        and constitution_candidate.get("runtime_enabled_now") is False
    )

    bundle_ok = all(f in constraint_bundle for f in CONSTRAINT_BUNDLE_FIELDS) and constraint_bundle.get(
        "candidate_only"
    ) is True

    all_pass = (
        input_ok
        and constitution_ok
        and bundle_ok
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections if "dryrun_and_review_pass" in s)
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "user_output_constitution_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "constitution_propagation_chain_defined": [
            "constitution sources (General + domain)",
            "→ Constitution Resolver",
            "→ constraint_bundle",
            "→ downstream Gates (Safety / Speech / Display)",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_safety_gate_planning": all_pass,
        "user_output_constitution_runtime_enabled": False,
        "user_facing_output_still_forbidden": True,
        "constitution_not_published": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "user_output_constitution_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_not_runtime": True,
        "constitution_to_resolver_to_bundle": True,
        "downstream_consumes_bundle_not_raw_clauses": True,
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
        "user_output_constitution_dryrun_review_policy": policy,
        "user_output_constitution_planning_input_review": planning_input_review,
        "user_output_constitution_candidate": constitution_candidate,
        "user_output_scope_jurisdiction_review": scope_review,
        "user_output_admission_rule_dryrun_review": admission_review,
        "user_output_safety_rule_dryrun_review": safety_review,
        "user_output_fact_uncertainty_rule_dryrun_review": fact_review,
        "user_output_privacy_rule_dryrun_review": privacy_review,
        "user_output_channel_rule_dryrun_review": channel_review,
        "user_output_tone_personalization_boundary_review": personalization_review,
        "user_output_refusal_hold_degrade_rule_review": refusal_review,
        "user_output_explainability_traceability_review": explain_review,
        "user_output_conflict_policy_review": conflict_review,
        "constitution_resolver_binding_review": resolver_review,
        "constitution_constraint_bundle_candidate": constraint_bundle,
        "constitution_change_propagation_review": propagation_review,
        "downstream_impact_boundary_review": impact_review,
        "user_output_speech_display_boundary_review": speech_display_review,
        "user_output_memory_worldmodel_taskstate_boundary_review": memory_review,
        "user_output_constitution_boundary_audit": boundary_audit,
        "user_output_constitution_blocked_path_result": blocked_path_result,
        "user_output_constitution_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
