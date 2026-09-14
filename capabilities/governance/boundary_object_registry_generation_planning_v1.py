# -*- coding: utf-8 -*-
"""Boundary Object Registry Generation Planning v1.

Generation planning only: define registry generation source inventory, whitelist,
integrity checks, contamination prevention, entry conversion, policy entry rules.
Does not generate registry, register objects, or execute final validation/contamination.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.boundary_object_registry_planning_v1 import (
    BOUNDARY_CATEGORIES,
    PROTECTED_OBJECT_TYPES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Boundary-Object-Registry-Generation-Planning-v1-001"
PLANNING_SCOPE = "boundary_object_registry_generation_planning_only"
SOURCE_CHAIN = "boundary_object_registry_generation_planning_v1"

SOURCE_PHASE = "Phase-Boundary-Object-Registry-Roadmap-Decision-v1-001"
SELECTED_ROUTE = "Route A — Boundary Object Registry Generation Planning"
UPSTREAM_REQUIRED_FINAL = (
    "BOUNDARY_OBJECT_REGISTRY_ROADMAP_DECISION_READY_FOR_REGISTRY_GENERATION_PLANNING"
)
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_GENERATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Generation-DryRun-v1-001"

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "boundary_object_registry_roadmap_decision_policy_v1.json",
    "completed_boundary_object_registry_chain_review_v1.json",
    "boundary_object_registry_roadmap_route_candidate_matrix_v1.json",
    "boundary_registry_generation_dependency_matrix_v1.json",
    "boundary_registry_generation_planning_scope_v1.json",
    "boundary_registry_roadmap_non_release_matrix_v1.json",
    "registry_generation_entry_readiness_risk_matrix_v1.json",
    "boundary_registry_roadmap_decision_non_claims_register_v1.json",
    "boundary_registry_roadmap_readiness_decision_v1.json",
)

SOURCE_TYPES: Tuple[Tuple[str, str, bool], ...] = (
    ("boundary object planning artifacts", "planning phase _eval_out and matrices", True),
    ("boundary object dry-run artifacts", "dry-run consumption matrices", True),
    ("boundary object post-review artifacts", "post-dryrun review matrices", True),
    ("roadmap decision artifacts", "roadmap decision policy and scope", True),
    ("owner/operator protocol artifacts", "owner/operator approval protocol chain", True),
    ("evidence chain artifacts", "evidence chain governance chain", True),
    ("success claim gate artifacts", "success claim gate canonicalization chain", True),
    ("permission semantics artifacts", "permission semantics canonicalization", True),
    ("terminology artifacts", "terminology canonical table chain", True),
    ("governance constraints manifest", "migration_governance_development_constraints_v1", True),
    ("phase verdict table", "LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE", True),
    ("architecture docs index", "docs/architecture governance index", False),
    ("evaluation docs index", "docs/architecture/evaluation index", False),
    ("non-claims registers", "phase non-claims registers", True),
    ("verifier reports", "phase verifier_report.json audit support only", False),
    ("summary artifacts", "phase summary.json auxiliary only", False),
)

SOURCE_ARTIFACT_WHITELIST: Tuple[Tuple[str, str, bool, bool, str], ...] = (
    ("boundary_object_category_planning_matrix", "primary category definitions", True, True, ""),
    ("boundary_object_read_write_policy_planning_matrix", "read/write policy source", True, True, ""),
    ("boundary_object_migration_policy_planning_matrix", "migration policy source", True, True, ""),
    ("boundary_object_evidence_policy_planning_matrix", "evidence policy source", True, True, ""),
    ("boundary_object_rollback_policy_planning_matrix", "rollback policy source", True, True, ""),
    ("protected_and_blocked_object_planning_matrix", "protected object definitions", True, True, ""),
    ("boundary_object_owner_operator_dependency_matrix", "owner/operator dependency source", True, False, ""),
    ("boundary_object_file_operation_policy_planning_matrix", "file operation policy source", True, False, ""),
    ("boundary_object_forbidden_shortcut_matrix", "forbidden shortcut constraints", True, False, ""),
    ("boundary_object_verifier_usage_planning_matrix", "verifier usage rules", True, False, ""),
    ("boundary_object_non_claims_planning_matrix", "non-claims constraints for generation", True, False, ""),
    ("boundary_object_registry_output_plan", "planned registry output schema", True, False, ""),
    ("roadmap_generation_planning_scope", "generation planning scope from roadmap", True, False, ""),
    ("governance_constraints_manifest", "hard governance constraints", True, True, ""),
    ("phase_verifier_report", "audit support only", False, False, "verifier_report cannot be single entry source"),
    ("phase_summary", "auxiliary metadata only", False, False, "summary cannot be registry primary source"),
)

INTEGRITY_CHECKS: Tuple[Tuple[str, str, str], ...] = (
    ("source exists", "artifact file present", "missing source file"),
    ("source schema valid", "JSON schema and row counts", "invalid schema"),
    ("source phase identity valid", "phase field matches expected chain", "wrong phase identity"),
    ("source verifier GO observed", "upstream verifier=GO", "upstream not GO"),
    ("source boundary_ok observed", "upstream boundary_ok=true", "upstream boundary failed"),
    ("source governance_constraints_ref valid", "constraints ref matches canonical", "constraints mismatch"),
    ("source timestamp present", "phase completion metadata", "missing timestamp"),
    ("source lineage present", "source_chain and upstream refs", "missing lineage"),
    ("source non-claims present", "non-claims register consumed", "missing non-claims"),
    ("source no-permission-release confirmed", "permission flags false", "permission released in source"),
    ("source no-file-operation confirmed", "file_operation_executed_now=false", "file op in source"),
    ("source no-registry-generation confirmed", "registry not generated in source", "registry generated in source"),
    ("source cross-artifact consistency", "matrices consistent across artifacts", "cross-artifact conflict"),
    ("source stale/deprecated check", "phase not superseded", "stale source"),
)

CONTAMINATION_RISKS: Tuple[Tuple[str, str, str], ...] = (
    ("summary-only contamination", "summary used as sole registry source", "reject summary-only derivation"),
    ("verifier-report-only contamination", "verifier_report as single entry source", "require multi-source chain"),
    ("stale artifact contamination", "deprecated phase artifacts", "reject stale sources"),
    ("deprecated phase contamination", "superseded phase outputs", "whitelist current phases only"),
    ("failed verifier contamination", "NO_GO verifier outputs", "reject non-GO sources"),
    ("non-GO source contamination", "boundary_ok=false sources", "require GO upstream"),
    ("permission-release-contaminated source", "source with released permissions", "reject contaminated source"),
    ("runtime-artifact contamination", "runtime-generated artifacts", "reject runtime_invoked sources"),
    ("auto-generated-doc contamination", "documentation_auto_sync artifacts", "reject auto-sync as source"),
    ("duplicate object entry contamination", "duplicate category entries", "dedupe on generation"),
    ("conflicting category contamination", "conflicting policy across sources", "resolve conflicts pre-generation"),
    ("protected object misclassification", "protected assets marked writable", "enforce protected rules"),
    ("evidence artifact misclassification", "eval_out as success evidence", "audit support only"),
    ("migration batch misclassification", "batch arming from planning artifact", "reject batch_arming in source"),
)

POLICY_ENTRY_TYPES: Tuple[str, ...] = (
    "read_write_policy_entry",
    "migration_policy_entry",
    "evidence_policy_entry",
    "rollback_policy_entry",
    "owner_operator_dependency_entry",
    "file_operation_policy_entry",
    "forbidden_shortcut_entry",
    "verifier_usage_entry",
    "non_claims_entry",
    "readiness_gate_entry",
)

OWNER_OPERATOR_DEPS: Tuple[Tuple[str, bool, bool, bool, bool, bool], ...] = (
    ("registry generation authorization", True, True, True, True, True),
    ("registry source validation authority", True, True, False, True, True),
    ("contamination check authority", True, True, False, True, True),
    ("protected object classification authority", True, True, True, True, True),
    ("policy entry approval authority", True, True, True, True, True),
    ("registry readiness approval authority", True, True, True, True, True),
    ("object registration authority", True, True, True, True, True),
    ("registry rollback authority", True, True, True, True, True),
    ("registry post-generation review authority", True, True, False, True, True),
    ("registry success claim authority", True, True, True, True, True),
)

VERIFIER_CHECKS: Tuple[Tuple[str, str, str, str, str], ...] = (
    ("G01", "registry_generation_not_executed_in_planning", "planning", "boundary_object_registry_generation_executed_now", "generation executed in planning", "P0"),
    ("G02", "registry_not_generated_in_planning", "planning", "boundary_object_registry_generated_now", "registry generated in planning", "P0"),
    ("G03", "object_not_registered_in_planning", "planning", "boundary_object_registered_now", "object registered in planning", "P0"),
    ("G04", "registry_source_not_final_validated", "planning", "registry_source_final_validated_now", "source final validated in planning", "P0"),
    ("G05", "contamination_check_not_final_executed", "planning", "registry_contamination_check_final_executed_now", "contamination final in planning", "P0"),
    ("G06", "entry_not_generated_in_planning", "planning", "registry_entry_generated_now", "entry generated in planning", "P0"),
    ("G07", "protected_object_not_modified", "planning", "protected_asset_modified_now", "protected modified in planning", "P0"),
    ("G08", "file_operation_not_executed", "planning", "file_operation_executed_now", "file op in planning", "P0"),
    ("G09", "summary_not_primary_source", "generation", "summary as primary", "summary-only registry", "P0"),
    ("G10", "verifier_report_not_single_source", "generation", "verifier_report single source", "verifier-only entry", "P0"),
    ("G11", "non_claims_not_object_entry", "generation", "non_claims as object entry", "non-claims mistaken for entry", "P0"),
    ("G12", "source_integrity_required_before_generation", "generation", "integrity bypass", "generation without integrity", "P0"),
    ("G13", "contamination_check_required_before_generation", "generation", "contamination bypass", "generation without contamination check", "P0"),
    ("G14", "owner_operator_required_before_generation", "generation", "owner_operator bypass", "generation without owner/operator", "P0"),
    ("G15", "readiness_gate_required_before_generation", "generation", "readiness bypass", "generation without readiness gate", "P0"),
    ("G16", "generation_planning_does_not_authorize_generation", "planning", "registry_generation_authorized_now", "planning authorizes generation", "P0"),
)

NON_CLAIM_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    ("generation planning GO", "generation planning GO does not mean registry generated"),
    ("source inventory", "source inventory planned does not mean source final validated"),
    ("whitelist", "whitelist planned does not mean source whitelisted now"),
    ("integrity check", "integrity check planned does not mean final validation executed"),
    ("contamination rule", "contamination rule planned does not mean contamination check executed"),
    ("conversion rule", "conversion rule planned does not mean entry generated"),
    ("protected entry", "protected entry rule planned does not mean protected object modified"),
    ("owner/operator dependency", "owner/operator dependency planned does not mean authorization granted"),
    ("verifier usage", "verifier usage planned does not mean verifier modified"),
    ("output plan", "output plan generated does not mean artifacts generated"),
    ("roadmap route", "roadmap selected route does not mean generation authorized"),
    ("readiness decision", "readiness decision does not mean registry generation allowed"),
)

OUTPUT_PLAN_ARTIFACTS: Tuple[Tuple[str, str], ...] = (
    ("boundary_object_registry_generation_policy_v1.json", "generation phase policy"),
    ("registry_generation_source_inventory_v1.json", "source inventory at generation"),
    ("registry_source_artifact_whitelist_v1.json", "whitelist at generation"),
    ("registry_source_integrity_check_matrix_v1.json", "integrity checks executed"),
    ("registry_contamination_prevention_matrix_v1.json", "contamination prevention applied"),
    ("registry_entry_conversion_rule_matrix_v1.json", "entry conversion rules applied"),
    ("registry_protected_object_entry_rule_matrix_v1.json", "protected entry rules applied"),
    ("registry_policy_entry_rule_matrix_v1.json", "policy entry rules applied"),
    ("registry_owner_operator_dependency_matrix_v1.json", "owner/operator deps at generation"),
    ("registry_generation_verifier_usage_matrix_v1.json", "verifier usage at generation"),
    ("registry_generation_non_claims_rules_v1.json", "non-claims at generation"),
    ("registry_generation_readiness_decision_v1.json", "generation readiness gate"),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "boundary_object_registry_generation_planning_only": True,
        "boundary_object_registry_generation_executed_now": False,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "registry_generation_authorized_now": False,
        "registry_source_final_validated_now": False,
        "registry_generation_source_validated_now": False,
        "registry_contamination_check_final_executed_now": False,
        "registry_generation_contamination_checked_now": False,
        "registry_entry_generated_now": False,
        "registry_entry_committed_now": False,
        "protected_asset_modified_now": False,
        "human_review_queue_modified_now": False,
        "dnae_or_permanent_block_modified_now": False,
        "file_operation_executed_now": False,
        "write_permission_released_now": False,
        "migration_permission_released_now": False,
        "evidence_permission_released_now": False,
        "rollback_permission_released_now": False,
        "owner_approval_request_sent_now": False,
        "operator_acknowledgement_request_sent_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "abort_authority_confirmed_now": False,
        "scope_confirmation_accepted_now": False,
        "verifier_rerun_authorized_now": False,
        "evidence_generation_authorized_now": False,
        "evidence_acceptance_authorized_now": False,
        "success_claim_authority_confirmed_now": False,
        "authorization_granted_now": False,
        "evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "success_evidence_generated_now": False,
        "evidence_accepted_for_success_claim_now": False,
        "success_claim_allowed": False,
        "evidence_chain_canonicalization_executed_now": False,
        "evidence_registry_generated_now": False,
        "success_claim_gate_generated_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "debt_fix_executed_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_planning_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(root / "boundary_registry_roadmap_readiness_decision_v1.json") if root else None
    routes = _try_read_json(root / "boundary_object_registry_roadmap_route_candidate_matrix_v1.json") if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in UPSTREAM_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
    loaded = summary is not None and verifier is not None and readiness is not None and not missing
    return {
        "root": root,
        "loaded": loaded,
        "summary": summary or {},
        "verifier": verifier or {},
        "readiness": readiness or {},
        "routes": routes or {},
        "artifacts": art,
        "missing": missing,
    }


def _build_source_inventory() -> List[Dict[str, Any]]:
    return [
        _row(
            source_type=st,
            source_description=desc,
            candidate_source_allowed=allowed,
            required_for_registry_generation=allowed,
            source_trust_level="high" if allowed else "auxiliary",
            source_read_allowed=True,
            source_write_allowed_now=False,
            source_final_validated_now=False,
            used_for_generation_now=False,
        )
        for st, desc, allowed in SOURCE_TYPES
    ]


def _build_source_whitelist() -> List[Dict[str, Any]]:
    return [
        _row(
            source_artifact_type=atype,
            whitelist_reason=reason,
            allowed_as_registry_source=primary or secondary,
            allowed_as_primary_source=primary,
            allowed_as_secondary_source=secondary,
            forbidden_as_source_reason=forbidden,
            requires_integrity_check=True,
            requires_contamination_check=True,
            whitelisted_now=False,
            final_validated_now=False,
        )
        for atype, reason, primary, secondary, forbidden in SOURCE_ARTIFACT_WHITELIST
    ]


def _build_integrity_checks() -> List[Dict[str, Any]]:
    return [
        _row(
            integrity_check=check,
            why_required=why,
            required_for_generation=True,
            failure_condition=fail,
            planned_verifier_check=f"verify_integrity_{check.replace(' ', '_')}",
            final_check_executed_now=False,
            source_final_validated_now=False,
        )
        for check, why, fail in INTEGRITY_CHECKS
    ]


def _build_contamination_prevention() -> List[Dict[str, Any]]:
    return [
        _row(
            contamination_risk=risk,
            why_dangerous=why,
            prevention_rule=f"block generation when {risk}",
            required_detection=True,
            planned_verifier_check=f"verify_contamination_{risk.replace(' ', '_')}",
            contamination_checked_now=False,
            final_generation_allowed_now=False,
        )
        for risk, why, _prevention in CONTAMINATION_RISKS
    ]


def _build_entry_conversion() -> List[Dict[str, Any]]:
    return [
        _row(
            boundary_object_category=cat,
            entry_required_fields=["category", "read_policy", "write_policy", "migration_policy", "evidence_policy", "rollback_policy"],
            source_requirements=["planning_matrix", "dryrun_matrix", "post_review_matrix"],
            risk_level_mapping="P0" if cat in ("protected assets", "human review queue / HR", "DnAE / permanent block") else "P1",
            read_write_policy_mapping="from read_write_policy_planning_matrix",
            migration_policy_mapping="from migration_policy_planning_matrix",
            evidence_policy_mapping="from evidence_policy_planning_matrix",
            rollback_policy_mapping="from rollback_policy_planning_matrix",
            owner_operator_dependency_mapping="from owner_operator_dependency_matrix",
            entry_generated_now=False,
            entry_committed_now=False,
        )
        for cat, _meaning, _why in BOUNDARY_CATEGORIES
    ]


def _build_protected_entry_rules() -> List[Dict[str, Any]]:
    return [
        _row(
            protected_object_type=obj,
            required_registry_fields=["protected_object_type", "protection_reason", "read_allowed", "write_allowed_now"],
            protection_reason=why,
            required_source_chain=["planning", "dryrun", "post_review"],
            write_allowed_now=False,
            move_allowed_now=False,
            delete_allowed_now=False,
            merge_allowed_now=False,
            entry_generated_now=False,
            entry_committed_now=False,
        )
        for obj, why in PROTECTED_OBJECT_TYPES
    ]


def _build_policy_entry_rules() -> List[Dict[str, Any]]:
    return [
        _row(
            policy_entry_type=pet,
            required_source_artifacts=["planning_matrices", "dryrun_matrices", "post_review_matrices"],
            required_fields=["policy_type", "constraints", "owner_operator_deps"],
            conversion_rule=f"convert planning+dryrun+review to {pet}",
            required_integrity_checks=["source integrity", "cross-artifact consistency"],
            required_contamination_checks=["summary-only", "verifier-report-only"],
            entry_generated_now=False,
            entry_committed_now=False,
        )
        for pet in POLICY_ENTRY_TYPES
    ]


def _build_owner_operator_deps() -> List[Dict[str, Any]]:
    return [
        _row(
            dependency=dep,
            required_owner_approval=ro,
            required_operator_acknowledgement=op,
            required_execution_window=win,
            required_scope_confirmation=scope,
            required_abort_authority=abort,
            satisfied_now=False,
            authorization_granted_now=False,
        )
        for dep, ro, op, win, scope, abort in OWNER_OPERATOR_DEPS
    ]


def _build_verifier_usage() -> List[Dict[str, Any]]:
    return [
        _row(
            verifier_check_id=vid,
            check_name=name,
            target_phase_types=targets,
            required_fields=fields,
            failure_condition=fail,
            severity=sev,
            planned_now=True,
            verifier_modified_now=False,
            enforced_now=False,
        )
        for vid, name, targets, fields, fail, sev in VERIFIER_CHECKS
    ]


def _build_non_claims() -> List[Dict[str, Any]]:
    return [
        _row(
            scenario=scenario,
            required_non_claim=claim,
            risk_if_missing="registry generation misread",
            must_be_in_summary=True,
            must_be_in_verifier_report=True,
            planned_now=True,
            generated_now=False,
        )
        for scenario, claim in NON_CLAIM_SCENARIOS
    ]


def _build_output_plan() -> List[Dict[str, Any]]:
    return [
        _row(
            planned_artifact=artifact,
            purpose=purpose,
            required=True,
            used_by_future_registry_generation=True,
            used_by_future_verifier=True,
            used_by_owner_operator_protocol=True,
            used_by_evidence_chain=True,
            used_by_real_rehearsal_chain=True,
            used_by_migration_chain=True,
            not_generated_now=True,
        )
        for artifact, purpose in OUTPUT_PLAN_ARTIFACTS
    ]


def run_boundary_object_registry_generation_planning_v1(
    *,
    boundary_object_registry_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(boundary_object_registry_roadmap_decision_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    routes = upstream["routes"] or upstream["artifacts"].get(
        "boundary_object_registry_roadmap_route_candidate_matrix_v1.json", {}
    )

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream roadmap verifier not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok not true")
    if up_summary.get("selected_route") != SELECTED_ROUTE:
        blockers.append("upstream selected_route is not Route A")
    if up_readiness.get("ready_for_boundary_object_registry_generation_planning") is not True:
        blockers.append("not ready_for_boundary_object_registry_generation_planning")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("boundary_object_registry_generation_planning_selected") is not True:
        blockers.append("boundary_object_registry_generation_planning_selected not true")
    for flag in (
        "boundary_object_registry_generation_executed_now",
        "boundary_object_registry_generated_now",
        "boundary_object_registered_now",
        "registry_generation_authorized_now",
        "registry_generation_source_validated_now",
        "registry_generation_contamination_checked_now",
        "protected_asset_modified_now",
        "human_review_queue_modified_now",
        "dnae_or_permanent_block_modified_now",
        "file_operation_executed_now",
        "write_permission_released_now",
        "migration_permission_released_now",
        "evidence_permission_released_now",
        "rollback_permission_released_now",
        "owner_approval_request_sent_now",
        "execution_window_opened_now",
        "evidence_generation_authorized_now",
        "evidence_generated_now",
        "success_claim_allowed",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must be false")
    for flag in (
        "ready_for_boundary_object_registry_generation",
        "ready_for_boundary_object_registration",
        "ready_for_registry_generation_authorization",
        "ready_for_registry_source_validation",
        "ready_for_registry_contamination_check",
        "ready_for_owner_approval_request",
        "ready_for_file_operation",
        "ready_for_real_rollback_rehearsal_execution",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")
    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    route_a = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "A"), {})
    route_h = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "H"), {})
    if route_a.get("selected_now") is not True:
        blockers.append("Route A not selected in upstream")
    if route_h.get("blocked_now") is not True:
        blockers.append("Route H must be blocked upstream")

    source_rows = _build_source_inventory()
    whitelist_rows = _build_source_whitelist()
    integrity_rows = _build_integrity_checks()
    contamination_rows = _build_contamination_prevention()
    conversion_rows = _build_entry_conversion()
    protected_rows = _build_protected_entry_rules()
    policy_rows = _build_policy_entry_rules()
    oo_rows = _build_owner_operator_deps()
    verifier_rows = _build_verifier_usage()
    non_claims_rows = _build_non_claims()
    output_rows = _build_output_plan()

    summary_whitelist = next((w for w in whitelist_rows if w.get("source_artifact_type") == "phase_summary"), {})
    verifier_whitelist = next((w for w in whitelist_rows if w.get("source_artifact_type") == "phase_verifier_report"), {})
    if summary_whitelist.get("allowed_as_primary_source") is not False:
        blockers.append("summary must not be primary source")
    if verifier_whitelist.get("allowed_as_registry_source") is True and not verifier_whitelist.get("forbidden_as_source_reason"):
        blockers.append("verifier_report must have forbidden single-source reason")

    planning_pass = (
        len(source_rows) >= 16
        and len(whitelist_rows) >= 16
        and len(integrity_rows) >= 14
        and len(contamination_rows) >= 14
        and len(conversion_rows) >= 16
        and len(protected_rows) >= 12
        and len(policy_rows) >= 10
        and len(oo_rows) >= 10
        and len(verifier_rows) >= 16
        and len(non_claims_rows) >= 12
        and len(output_rows) >= 12
        and all(r.get("not_generated_now") is True for r in output_rows)
        and all(r.get("entry_generated_now") is False for r in conversion_rows)
        and all(r.get("entry_committed_now") is False for r in protected_rows)
        and not blockers
    )
    boundary_ok = planning_pass

    boundary_object_registry_generation_planning_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_selected_route_observed=up_summary.get("selected_route"),
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
    )

    registry_generation_source_inventory_planning_matrix = {
        "rows": source_rows,
        "row_count": len(source_rows),
        **_planning_meta(),
    }
    registry_source_artifact_whitelist_planning_matrix = {
        "rows": whitelist_rows,
        "row_count": len(whitelist_rows),
        **_planning_meta(),
    }
    registry_source_integrity_check_planning_matrix = {
        "rows": integrity_rows,
        "row_count": len(integrity_rows),
        **_planning_meta(),
    }
    registry_contamination_prevention_planning_matrix = {
        "rows": contamination_rows,
        "row_count": len(contamination_rows),
        **_planning_meta(),
    }
    registry_entry_conversion_rule_planning_matrix = {
        "rows": conversion_rows,
        "row_count": len(conversion_rows),
        **_planning_meta(),
    }
    registry_protected_object_entry_rule_planning_matrix = {
        "rows": protected_rows,
        "row_count": len(protected_rows),
        **_planning_meta(),
    }
    registry_policy_entry_rule_planning_matrix = {
        "rows": policy_rows,
        "row_count": len(policy_rows),
        **_planning_meta(),
    }
    registry_owner_operator_dependency_planning_matrix = {
        "rows": oo_rows,
        "row_count": len(oo_rows),
        **_planning_meta(),
    }
    registry_generation_verifier_usage_planning_matrix = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        **_planning_meta(),
    }
    registry_generation_non_claims_planning_matrix = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        **_planning_meta(),
    }
    registry_generation_output_plan = {
        "rows": output_rows,
        "row_count": len(output_rows),
        **_planning_meta(),
    }

    boundary_object_registry_generation_planning_readiness_decision = {
        "ready_for_boundary_object_registry_generation_dryrun": boundary_ok,
        "ready_for_boundary_object_registry_generation": False,
        "ready_for_boundary_object_registration": False,
        "ready_for_registry_generation_authorization": False,
        "ready_for_registry_source_final_validation": False,
        "ready_for_registry_contamination_check_final_execution": False,
        "ready_for_registry_entry_generation": False,
        "ready_for_registry_entry_commit": False,
        "ready_for_owner_approval_request": False,
        "ready_for_operator_acknowledgement_request": False,
        "ready_for_execution_window_opening": False,
        "ready_for_evidence_generation_authorization": False,
        "ready_for_file_operation": False,
        "ready_for_restore_map_generation": False,
        "ready_for_rollback_execution": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "registry_generation_planning_completed": boundary_ok,
        "source_inventory_planned": True,
        "source_whitelist_planned": True,
        "source_integrity_check_planned": True,
        "contamination_prevention_planned": True,
        "entry_conversion_rule_planned": True,
        "protected_entry_rule_planned": True,
        "policy_entry_rule_planned": True,
        "owner_operator_dependency_planned": True,
        "verifier_usage_planned": True,
        "non_claims_planned": True,
        "output_plan_generated": True,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "registry_entry_generated_now": False,
        "registry_entry_committed_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_GENERATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "boundary_object_registry_roadmap_decision_input_loaded": upstream["loaded"],
        "source_inventory_count": len(source_rows),
        "source_whitelist_count": len(whitelist_rows),
        "integrity_check_count": len(integrity_rows),
        "contamination_prevention_count": len(contamination_rows),
        "entry_conversion_count": len(conversion_rows),
        "protected_entry_rule_count": len(protected_rows),
        "policy_entry_rule_count": len(policy_rows),
        "owner_operator_dependency_count": len(oo_rows),
        "verifier_usage_count": len(verifier_rows),
        "non_claims_count": len(non_claims_rows),
        "output_plan_count": len(output_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_GENERATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "boundary_object_registry_generation_planning_policy": boundary_object_registry_generation_planning_policy,
        "registry_generation_source_inventory_planning_matrix": registry_generation_source_inventory_planning_matrix,
        "registry_source_artifact_whitelist_planning_matrix": registry_source_artifact_whitelist_planning_matrix,
        "registry_source_integrity_check_planning_matrix": registry_source_integrity_check_planning_matrix,
        "registry_contamination_prevention_planning_matrix": registry_contamination_prevention_planning_matrix,
        "registry_entry_conversion_rule_planning_matrix": registry_entry_conversion_rule_planning_matrix,
        "registry_protected_object_entry_rule_planning_matrix": registry_protected_object_entry_rule_planning_matrix,
        "registry_policy_entry_rule_planning_matrix": registry_policy_entry_rule_planning_matrix,
        "registry_owner_operator_dependency_planning_matrix": registry_owner_operator_dependency_planning_matrix,
        "registry_generation_verifier_usage_planning_matrix": registry_generation_verifier_usage_planning_matrix,
        "registry_generation_non_claims_planning_matrix": registry_generation_non_claims_planning_matrix,
        "registry_generation_output_plan": registry_generation_output_plan,
        "boundary_object_registry_generation_planning_readiness_decision": boundary_object_registry_generation_planning_readiness_decision,
    }
