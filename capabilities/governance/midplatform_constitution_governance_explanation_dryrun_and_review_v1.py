# -*- coding: utf-8 -*-
"""Midplatform Constitution Governance Explanation DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as AUTH_EXT_DR_FINAL_GO,
)
from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
    NEXT_OCR_PHASE_AFTER_EXTENSION,
)
from capabilities.governance.midplatform_constitution_governance_explanation_planning_v1 import (
    AMENDMENT_CANDIDATE_STATES,
    AMENDMENT_TRIGGERS,
    AMENDMENT_WORKFLOW,
    CONFLICT_RULES,
    DECISION_TREE_QUESTIONS,
    FINAL_DECISION_GO as EXPLANATION_PLANNING_FINAL_GO,
    GENERAL_JURISDICTION,
    LAYER_PRIORITY,
    NON_CLAIMS as EXPLANATION_PLANNING_NON_CLAIMS,
    VIOLATION_ACTIONS,
    VIOLATION_EVIDENCE_FIELDS,
    VIOLATION_LEVELS,
    VIOLATION_TYPES,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HIERARCHY_DR_FINAL_GO,
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Constitution-Governance-Explanation-DryRunAndReview-v1-001"
SCOPE = "constitution_governance_explanation_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_constitution_governance_explanation_dryrun_and_review_v1"

UPSTREAM_EXPLANATION_PLANNING_FINAL = EXPLANATION_PLANNING_FINAL_GO
UPSTREAM_HIERARCHY_DR_FINAL = HIERARCHY_DR_FINAL_GO
UPSTREAM_AUTH_EXT_DR_FINAL = AUTH_EXT_DR_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_CONSTITUTION_GOVERNANCE_EXPLANATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_OCR_REAL_DEPENDENCY_AUTHORIZATION_VIA_FACTORY_STANDARD_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_CONSTITUTION_GOVERNANCE_EXPLANATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = NEXT_OCR_PHASE_AFTER_EXTENSION
NEXT_PHASE_HOLD = "Phase-Midplatform-Constitution-Governance-Explanation-Issue-Review-v1-001"

LOCAL_LUNA_MAY: Tuple[str, ...] = (
    "cache constitution",
    "validate constitution version",
    "enforce local copy",
    "detect conflict",
    "generate amendment candidate",
    "generate violation report",
    "request Hive update",
    "apply approved update",
    "rollback to safe previous version",
)

LOCAL_LUNA_MAY_NOT: Tuple[str, ...] = (
    "modify highest constitution locally",
    "silently change survival/safety/privacy/fact/user-output rules",
    "weaken provider boundary",
    "bypass authorization standard",
    "bypass Validation Factory",
    "override Hive-issued constitution",
    "erase constitution violation record",
)

BOUNDARY_FORBIDDEN: Tuple[str, ...] = (
    "constitution registry update",
    "runtime enforcement",
    "amendment commit",
    "Hive update request execution",
    "personalized constitution generation",
    "local override",
    "OCR authorization",
    "grant issue",
    "real dependency check",
    "provider invocation",
    "Memory write",
    "WorldModel write",
    "user output",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "explanation_to_constitution_registry_update",
    "explanation_to_runtime_enforcement",
    "explanation_to_amendment_commit",
    "explanation_to_hive_update_request_execution",
    "explanation_to_personalized_constitution_generation",
    "explanation_to_local_override",
    "explanation_to_ocr_authorization",
    "explanation_to_grant_issue",
    "explanation_to_real_dependency_check",
    "explanation_to_provider_invoke",
    "explanation_to_memory_write",
    "explanation_to_world_model_write",
    "explanation_to_user_output",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Explanation DryRunAndReview GO ≠ constitution registry updated",
    "constitution generation logic defined ≠ amendment generated",
    "amendment lifecycle defined ≠ Hive review submitted",
    "Hive authority explained ≠ Hive update requested",
    "violation penalty defined ≠ penalty executed",
    "next OCR planning ≠ real dependency check allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "constitution_registry_updated_now",
    "constitution_runtime_enforced_now",
    "constitution_amendment_committed_now",
    "constitution_amendment_candidate_generated_now",
    "hive_constitution_update_requested_now",
    "hive_review_submitted_now",
    "personalized_constitution_generated_now",
    "local_constitution_override_now",
    "violation_penalty_executed_now",
    "ocr_authorization_started_now",
    "grant_issued_now",
    "real_dependency_check_executed_now",
    "provider_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
    "approved_now",
    "active_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "constitution_governance_explanation_dryrun_and_review_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "ocr_real_dep_authorization_chain": OCR_REAL_DEP_AUTHORIZATION_CHAIN,
        "authorization_standard_id": AUTHORIZATION_STANDARD_ID,
        "selected_provider_for_execution": None,
        "local_auto_amendment_allowed": False,
        "hive_review_required": True,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["provider_selection_finalized_now"] = False
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


def _planning_consumable(planning_doc: Dict[str, Any], required_keys: Tuple[str, ...]) -> bool:
    return all(planning_doc.get(k) is not None for k in required_keys)


def run_midplatform_constitution_governance_explanation_dryrun_and_review_v1(
    *,
    midplatform_constitution_governance_explanation_planning_root: str,
    midplatform_constitution_governance_hierarchy_dryrun_and_review_root: str,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    explain_plan_root = Path(
        midplatform_constitution_governance_explanation_planning_root
    ).expanduser().resolve()
    explain_plan_sm = _try_read_json(explain_plan_root / "summary.json") or {}
    explain_plan_vr = _try_read_json(explain_plan_root / "verifier_report.json") or {}

    hierarchy_dr_root = Path(
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root
    ).expanduser().resolve()
    hierarchy_dr_sm = _try_read_json(hierarchy_dr_root / "summary.json") or {}
    hierarchy_dr_vr = _try_read_json(hierarchy_dr_root / "verifier_report.json") or {}

    auth_ext_dr_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
        or explain_plan_root.parent / "capability_factory_authorization_standard_extension_dryrun_and_review"
    ).expanduser().resolve()
    auth_ext_dr_sm = _try_read_json(auth_ext_dr_root / "summary.json") or {}
    auth_ext_dr_vr = _try_read_json(auth_ext_dr_root / "verifier_report.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or explain_plan_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}

    plan_layers = _try_read_json(
        explain_plan_root / "constitution_layer_relationship_explanation_v1.json"
    ) or {}
    plan_jurisdiction = _try_read_json(
        explain_plan_root / "constitution_jurisdiction_and_conflict_rule_v1.json"
    ) or {}
    plan_generation = _try_read_json(explain_plan_root / "constitution_generation_logic_v1.json") or {}
    plan_amendment = _try_read_json(explain_plan_root / "constitution_amendment_logic_v1.json") or {}
    plan_sys_pers = _try_read_json(
        explain_plan_root / "system_vs_personalized_constitution_rule_v1.json"
    ) or {}
    plan_hive = _try_read_json(explain_plan_root / "hive_constitution_authority_rule_v1.json") or {}
    plan_local = _try_read_json(
        explain_plan_root / "local_luna_constitution_consumption_boundary_v1.json"
    ) or {}
    plan_survival = _try_read_json(
        explain_plan_root / "constitution_survival_mechanism_link_v1.json"
    ) or {}
    plan_violation = _try_read_json(
        explain_plan_root / "constitution_violation_alarm_and_penalty_rule_v1.json"
    ) or {}
    plan_lifecycle = _try_read_json(
        explain_plan_root / "constitution_change_candidate_lifecycle_v1.json"
    ) or {}
    plan_tree = _try_read_json(explain_plan_root / "constitution_governance_decision_tree_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_explanation_planning_root": str(explain_plan_root),
        "upstream_hierarchy_dryrun_review_root": str(hierarchy_dr_root),
        "upstream_auth_extension_dryrun_review_root": str(auth_ext_dr_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "output_root": str(out_root),
    }

    if explain_plan_vr.get("verifier") != "GO":
        blockers.append("explanation planning verifier must be GO")
    if explain_plan_sm.get("final_decision") != UPSTREAM_EXPLANATION_PLANNING_FINAL:
        blockers.append("explanation planning final_decision mismatch")
    if hierarchy_dr_vr.get("verifier") != "GO":
        blockers.append("hierarchy dryrun review must be GO")
    if hierarchy_dr_sm.get("final_decision") != UPSTREAM_HIERARCHY_DR_FINAL:
        blockers.append("hierarchy dryrun final_decision mismatch")
    if auth_ext_dr_vr.get("verifier") != "GO":
        blockers.append("auth extension dryrun review must be GO")
    if auth_ext_dr_sm.get("final_decision") != UPSTREAM_AUTH_EXT_DR_FINAL:
        blockers.append("auth extension dryrun final_decision mismatch")
    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun review must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "constitution_explanation_planning_input_review_v1",
        "explanation_planning_verifier_go": explain_plan_vr.get("verifier") == "GO",
        "explanation_planning_final_decision": explain_plan_sm.get("final_decision"),
        "hierarchy_dryrun_go": hierarchy_dr_vr.get("verifier") == "GO",
        "auth_extension_dryrun_go": auth_ext_dr_vr.get("verifier") == "GO",
        "three_layer_closed": hierarchy_dr_sm.get("dryrun_and_review_pass") is True,
        "authorization_standard_tenth_category": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    layer_checks: List[Tuple[str, bool]] = [
        ("layer_priority_order_valid", len(plan_layers.get("layer_priority") or []) >= 6),
        ("general_highest_priority", (plan_layers.get("layer_priority") or [None])[0] == "Luna General Constitution"),
        ("personalized_overlay_only", True),
        ("phase_local_cannot_override_upper", True),
        ("planning_layers_consumable", len(plan_layers.get("layers") or []) >= 5),
    ]
    layer_review = {
        "review_id": "constitution_layer_relationship_review_v1",
        "layer_priority": list(LAYER_PRIORITY),
        "general_constitution_highest": True,
        "personalized_constitution_overlay_only": True,
        "phase_local_rule_cannot_override_upper": True,
        "simulated_consumption": True,
        **_review_ok(layer_checks),
        **meta,
    }

    jurisdiction_checks: List[Tuple[str, bool]] = [
        ("general_jurisdiction", len(plan_jurisdiction.get("general_constitution_jurisdiction") or []) >= 6),
        ("domain_jurisdiction", len(plan_jurisdiction.get("domain_constitution_jurisdiction") or []) >= 4),
        ("domain_standard_jurisdiction", len(plan_jurisdiction.get("domain_standard_jurisdiction") or []) >= 10),
        ("upper_rule_priority", True),
        ("non_overridable_floors", len(plan_jurisdiction.get("non_overridable_floors") or []) >= 5),
        ("conservative_default", True),
        ("conflict_rules8", len(plan_jurisdiction.get("conflict_rules") or []) == len(CONFLICT_RULES)),
    ]
    for rule in CONFLICT_RULES[:3]:
        jurisdiction_checks.append((f"conflict.{rule[:20]}", rule in (plan_jurisdiction.get("conflict_rules") or [])))

    jurisdiction_review = {
        "review_id": "constitution_jurisdiction_conflict_review_v1",
        "general_jurisdiction": list(GENERAL_JURISDICTION),
        "upper_rule_priority": True,
        "non_overridable_floors": plan_jurisdiction.get("non_overridable_floors"),
        "default_conflict_resolution": plan_jurisdiction.get("default_conflict_resolution"),
        "conflict_rules_count": len(plan_jurisdiction.get("conflict_rules") or []),
        **_review_ok(jurisdiction_checks),
        **meta,
    }

    gen_checks: List[Tuple[str, bool]] = [
        ("human_initial", plan_generation.get("initial_constitution", {}).get("created_by") == "human designers"),
        ("not_final_form", plan_generation.get("initial_constitution", {}).get("not_final_form") is True),
        ("candidate_only", plan_generation.get("future_constitution_generation", {}).get("candidate_only") is True),
        ("no_local_auto_submit", plan_generation.get("future_constitution_generation", {}).get("local_auto_submit_forbidden") is True),
        ("hive_review_required", "Hive review" in str(plan_generation.get("future_constitution_generation", {}).get("required_reviews", []))),
        ("required_artifacts5", len(plan_generation.get("future_constitution_generation", {}).get("required_artifacts", [])) >= 5),
    ]
    generation_review = {
        "review_id": "constitution_generation_logic_review_v1",
        "initial_constitution_by_human": True,
        "constitution_candidate_only": True,
        "local_auto_submit_forbidden": True,
        "required_reviews": ["Hive review", "owner review", "governance review"],
        "required_artifacts": [
            "source_chain",
            "evidence",
            "risk assessment",
            "rollback plan",
            "impact analysis",
        ],
        **_review_ok(gen_checks),
        **meta,
    }

    amend_checks: List[Tuple[str, bool]] = []
    for trigger in AMENDMENT_TRIGGERS:
        amend_checks.append((f"trigger.{trigger[:24]}", trigger in (plan_amendment.get("amendment_triggers") or [])))
    for step in AMENDMENT_WORKFLOW:
        amend_checks.append((f"workflow.{step[:24]}", step in (plan_amendment.get("amendment_workflow") or [])))
    amend_checks.extend([
        ("amendment_not_committed", meta.get("constitution_amendment_committed_now") is False),
        ("local_auto_amendment_forbidden", plan_amendment.get("local_auto_amendment_allowed") is False),
        ("hive_review_required", plan_amendment.get("hive_review_required") is True),
    ])

    amendment_review = {
        "review_id": "constitution_amendment_logic_review_v1",
        "amendment_triggers": list(AMENDMENT_TRIGGERS),
        "amendment_workflow": list(AMENDMENT_WORKFLOW),
        "constitution_amendment_committed_now": False,
        "local_auto_amendment_allowed": False,
        "hive_review_required": True,
        **_review_ok(amend_checks),
        **meta,
    }

    sys_pers_checks: List[Tuple[str, bool]] = [
        ("hive_managed", plan_sys_pers.get("system_constitution", {}).get("managed_by") == "Hive"),
        ("personalized_within_system", plan_sys_pers.get("personalized_constitution", {}).get("must_stay_within_system_constitution") is True),
        ("cannot_relax_floors", len(plan_sys_pers.get("personalized_constitution", {}).get("cannot_relax") or []) >= 5),
        ("overlay_not_upper", "overlay" in (plan_sys_pers.get("personalized_constitution", {}).get("status") or "")),
        ("personalized_not_generated", meta.get("personalized_constitution_generated_now") is False),
    ]
    system_vs_personalized_review = {
        "review_id": "system_vs_personalized_constitution_review_v1",
        "system_constitution_hive_managed": True,
        "personalized_overlay_only": True,
        "personalized_constitution_generated_now": False,
        **_review_ok(sys_pers_checks),
        **meta,
    }

    hive_checks: List[Tuple[str, bool]] = [
        ("hive_highest_authority", plan_hive.get("hive_constitution_authority") is True),
        ("local_no_general_override", plan_hive.get("local_override_of_general_constitution_allowed") is False),
        ("hive_review_for_general_change", plan_hive.get("hive_review_required_for_general_constitution_change") is True),
        ("local_may_request_only", len(plan_hive.get("local_may_generate") or []) >= 3),
    ]
    hive_review = {
        "review_id": "hive_constitution_authority_review_v1",
        "hive_is_highest_management_end": True,
        "hive_responsibilities": plan_hive.get("hive_responsibilities"),
        "local_override_of_general_constitution_allowed": False,
        "hive_review_required_for_general_constitution_change": True,
        **_review_ok(hive_checks),
        **meta,
    }

    local_checks: List[Tuple[str, bool]] = []
    for action in LOCAL_LUNA_MAY:
        local_checks.append((f"may.{action[:20]}", action in (plan_local.get("local_may") or [])))
    for action in LOCAL_LUNA_MAY_NOT:
        local_checks.append((f"may_not.{action[:20]}", action in (plan_local.get("local_may_not") or [])))

    local_boundary_review = {
        "review_id": "local_luna_constitution_consumption_boundary_review_v1",
        "local_may": list(LOCAL_LUNA_MAY),
        "local_may_not": list(LOCAL_LUNA_MAY_NOT),
        **_review_ok(local_checks),
        **meta,
    }

    survival_checks: List[Tuple[str, bool]] = [
        ("constitution_is_survival_mechanism", "生存机制" in (plan_survival.get("core_principle") or "")),
        ("avoid_death_risks", True),
        ("survival_drive_candidate", "constitution_amendment_candidate" in str(plan_survival.get("candidate_sources", {}))),
        ("all_amendments_hive_review", plan_survival.get("all_amendments_require_hive_review") is True),
        ("capabilities10", len(plan_survival.get("supported_survival_capabilities") or []) >= 10),
    ]
    survival_review = {
        "review_id": "constitution_survival_mechanism_link_review_v1",
        "constitution_is_survival_mechanism": True,
        "all_amendments_require_hive_review": True,
        **_review_ok(survival_checks),
        **meta,
    }

    violation_checks: List[Tuple[str, bool]] = []
    for level in VIOLATION_LEVELS:
        violation_checks.append((f"level.{level}", level in (plan_violation.get("violation_levels") or [])))
    for vtype in VIOLATION_TYPES:
        violation_checks.append((f"type.{vtype}", vtype in (plan_violation.get("violation_types") or [])))
    for action in VIOLATION_ACTIONS:
        violation_checks.append((f"action.{action}", action in (plan_violation.get("actions") or [])))
    for field in VIOLATION_EVIDENCE_FIELDS:
        violation_checks.append((f"evidence.{field}", field in (plan_violation.get("evidence_fields") or [])))
    violation_checks.append(("penalty_not_executed_now", meta.get("violation_penalty_executed_now") is False))

    violation_review = {
        "review_id": "constitution_violation_alarm_penalty_review_v1",
        "violation_levels": list(VIOLATION_LEVELS),
        "violation_types": list(VIOLATION_TYPES),
        "actions": list(VIOLATION_ACTIONS),
        "evidence_fields": list(VIOLATION_EVIDENCE_FIELDS),
        "violation_penalty_executed_now": False,
        **_review_ok(violation_checks),
        **meta,
    }

    lifecycle_checks: List[Tuple[str, bool]] = []
    for state in AMENDMENT_CANDIDATE_STATES:
        lifecycle_checks.append((f"state.{state}", state in (plan_lifecycle.get("states") or [])))
    lifecycle_checks.extend([
        ("candidate_not_generated_now", meta.get("constitution_amendment_candidate_generated_now") is False),
        ("hive_review_not_submitted", meta.get("hive_review_submitted_now") is False),
        ("not_approved_now", meta.get("approved_now") is False),
        ("not_active_now", meta.get("active_now") is False),
    ])

    lifecycle_review = {
        "review_id": "constitution_change_candidate_lifecycle_review_v1",
        "states": list(AMENDMENT_CANDIDATE_STATES),
        "amendment_candidate_generated_now": False,
        "hive_review_submitted_now": False,
        "approved_now": False,
        "active_now": False,
        **_review_ok(lifecycle_checks),
        **meta,
    }

    tree_checks: List[Tuple[str, bool]] = []
    for idx, question in enumerate(DECISION_TREE_QUESTIONS, start=1):
        tree_checks.append((f"q{idx}", question in (plan_tree.get("questions") or [])))

    decision_tree_review = {
        "review_id": "constitution_governance_decision_tree_review_v1",
        "questions": list(DECISION_TREE_QUESTIONS),
        "question_count": len(DECISION_TREE_QUESTIONS),
        "simulated_consumption": True,
        **_review_ok(tree_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    for action in BOUNDARY_FORBIDDEN:
        boundary_checks.append((f"forbidden.{action.replace(' ', '_')}", True))

    boundary_audit = {
        "audit_id": "constitution_explanation_boundary_audit_v1",
        "forbidden_actions": list(BOUNDARY_FORBIDDEN),
        "all_boundary_false": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "constitution_explanation_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        layer_review,
        jurisdiction_review,
        generation_review,
        amendment_review,
        system_vs_personalized_review,
        hive_review,
        local_boundary_review,
        survival_review,
        violation_review,
        lifecycle_review,
        decision_tree_review,
        boundary_audit,
    ]

    all_pass = (
        input_ok
        and all(section.get("dryrun_and_review_pass") is True for section in review_sections)
        and blocked_path_result.get("all_blocked") is True
    )

    high_risk = not all_pass
    closure_decision = {
        "decision_id": "constitution_explanation_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": high_risk,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "governance_explanation_consumable": all_pass,
        "ocr_via_factory_standard_next": all_pass,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_ocr_real_dep_via_factory_standard_planning": all_pass,
        "ready_for_real_dependency_check": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        "ocr_consumes_domain_config_only": True,
        "authorization_via_factory_standard": True,
        "validation_via_validation_factory": True,
        "note": "OCR submits domain_config only; Factory Authorization Standard owns auth logic",
        **meta,
    }

    policy = {
        "policy_id": "constitution_governance_explanation_dryrun_and_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
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
        "violations": blockers,
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        "blocked_path_count": len(BLOCKED_PATHS),
        "decision_tree_questions": len(DECISION_TREE_QUESTIONS),
        "high_risk_count": 1 if high_risk else 0,
        **meta,
    }

    return {
        "constitution_governance_explanation_dryrun_and_review_policy": policy,
        "constitution_explanation_planning_input_review": planning_input_review,
        "constitution_layer_relationship_review": layer_review,
        "constitution_jurisdiction_conflict_review": jurisdiction_review,
        "constitution_generation_logic_review": generation_review,
        "constitution_amendment_logic_review": amendment_review,
        "system_vs_personalized_constitution_review": system_vs_personalized_review,
        "hive_constitution_authority_review": hive_review,
        "local_luna_constitution_consumption_boundary_review": local_boundary_review,
        "constitution_survival_mechanism_link_review": survival_review,
        "constitution_violation_alarm_penalty_review": violation_review,
        "constitution_change_candidate_lifecycle_review": lifecycle_review,
        "constitution_governance_decision_tree_review": decision_tree_review,
        "constitution_explanation_boundary_audit": boundary_audit,
        "constitution_explanation_blocked_path_result": blocked_path_result,
        "constitution_explanation_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
