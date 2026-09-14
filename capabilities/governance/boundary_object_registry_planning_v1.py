# -*- coding: utf-8 -*-
"""Boundary Object Registry Planning v1.

Planning only: define boundary object categories, read/write, migration, evidence,
rollback, protected/blocked objects, owner/operator dependencies, file operations.
Does not generate registry, register objects, or release execution permissions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Boundary-Object-Registry-Planning-v1-001"
PLANNING_SCOPE = "boundary_object_registry_planning_only"
SOURCE_CHAIN = "boundary_object_registry_planning_v1"

SOURCE_PHASE = "Phase-Owner-Operator-Approval-Protocol-Roadmap-Decision-v1-001"
SELECTED_ROUTE = "Route A — Boundary Object Registry Planning"
UPSTREAM_REQUIRED_FINAL = (
    "OWNER_OPERATOR_APPROVAL_PROTOCOL_ROADMAP_DECISION_READY_FOR_BOUNDARY_OBJECT_REGISTRY_PLANNING"
)
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Boundary-Object-Registry-DryRun-v1-001"

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "owner_operator_roadmap_decision_policy_v1.json",
    "completed_owner_operator_protocol_review_v1.json",
    "owner_operator_roadmap_route_candidate_matrix_v1.json",
    "owner_operator_to_boundary_object_dependency_matrix_v1.json",
    "boundary_object_registry_planning_scope_v1.json",
    "owner_operator_roadmap_non_release_matrix_v1.json",
    "boundary_object_entry_readiness_risk_matrix_v1.json",
    "owner_operator_roadmap_decision_non_claims_register_v1.json",
    "owner_operator_roadmap_readiness_decision_v1.json",
)

BOUNDARY_CATEGORIES: Tuple[Tuple[str, str, str], ...] = (
    ("protected assets", "canonical protected asset boundary", "migration governance root protection"),
    ("human review queue / HR", "human review queue and records boundary", "HR must not be modified without authorization"),
    ("DnAE / permanent block", "do-not-automate-ever and permanent block objects", "DnAE must remain immutable"),
    ("eval_out artifacts", "_eval_out phase output artifacts", "audit support; not success evidence alone"),
    ("verifier artifacts", "verifier_report and verifier check outputs", "verifier artifacts require dedicated authorization to modify"),
    ("phase verdict table", "migration phase verdict status table", "verdict table updates require governance phase"),
    ("downstream handoff", "downstream handoff documentation links", "handoff must reflect phase boundaries"),
    ("checkpoint", "migration checkpoint snapshots", "checkpoints required for rollback"),
    ("restore map", "restore map artifacts", "restore map required before restore operations"),
    ("docs", "architecture and governance documentation", "docs may be planned; no auto sync in planning"),
    ("capability", "capabilities/governance modules", "capability changes require boundary registry"),
    ("runner/verifier", "evaluation runner and verifier tools", "runner/verifier changes require authorization"),
    ("migration batch", "migration batch definitions and arming state", "batch arming forbidden without full chain"),
    ("evidence artifacts", "evidence chain artifacts", "evidence generation requires boundary registry and authorization"),
    ("file operation boundary", "file read/write/move/delete/rename/merge boundary", "file operations require registry and approval"),
    ("rollback boundary", "rollback rehearsal and restore boundary", "rollback requires restore map and checkpoint"),
)

PROTECTED_OBJECT_TYPES: Tuple[Tuple[str, str], ...] = (
    ("protected assets root", "root protected asset tree must not be modified"),
    ("protected docs", "governance docs under protected scope"),
    ("protected evaluation outputs", "protected _eval_out subsets"),
    ("protected verifier artifacts", "immutable verifier baseline artifacts"),
    ("human review queue", "HR queue must not be modified"),
    ("human review records", "HR records must not be modified"),
    ("DnAE objects", "do-not-automate-ever objects"),
    ("permanent block objects", "permanently blocked migration targets"),
    ("protected migration history", "migration audit history"),
    ("protected rollback history", "rollback audit history"),
    ("protected approval records", "owner/operator approval records"),
    ("protected evidence records", "accepted evidence records"),
)

FILE_OPERATIONS: Tuple[str, ...] = (
    "read",
    "write",
    "create",
    "delete",
    "move",
    "rename",
    "merge",
    "copy",
    "archive",
    "restore",
    "generate",
    "overwrite",
    "append",
    "chmod / permission mutation",
)

FORBIDDEN_SHORTCUTS: Tuple[Tuple[str, str, str, str], ...] = (
    (
        "boundary registry planning does not mean registry generated",
        "boundary_object_registry_generated_now",
        "planning GO ≠ registry generated",
        "P0",
    ),
    (
        "boundary object planned does not mean registered",
        "boundary_object_registered_now",
        "planning GO ≠ object registered",
        "P0",
    ),
    (
        "read allowed does not imply write allowed",
        "write_allowed_now",
        "read policy ≠ write permission",
        "P0",
    ),
    (
        "audit support does not imply success evidence",
        "success_evidence_allowed_now",
        "eval_out audit ≠ success claim",
        "P0",
    ),
    (
        "eval_out artifact does not imply success evidence",
        "success_evidence_allowed_now",
        "eval_out ≠ success evidence",
        "P0",
    ),
    (
        "verifier artifact does not imply runtime evidence",
        "runtime_evidence_generated_now",
        "verifier_report ≠ runtime evidence",
        "P0",
    ),
    (
        "docs sync planning does not imply auto sync executed",
        "documentation_auto_sync_executed_now",
        "docs planned ≠ auto sync",
        "P0",
    ),
    (
        "protected asset observed does not imply modifiable",
        "protected_asset_modified_now",
        "observed ≠ modifiable",
        "P0",
    ),
    (
        "restore map planned does not imply restore allowed",
        "restore_operation_allowed_now",
        "restore map planned ≠ restore allowed",
        "P0",
    ),
    (
        "checkpoint planned does not imply rollback allowed",
        "rollback_allowed_now",
        "checkpoint planned ≠ rollback allowed",
        "P0",
    ),
    (
        "owner/operator dependency planned does not imply authorization granted",
        "authorization_granted_now",
        "dependency planned ≠ authorization granted",
        "P0",
    ),
    (
        "registry planned does not imply migration allowed",
        "migration_allowed_now",
        "registry planned ≠ migration allowed",
        "P0",
    ),
)

VERIFIER_CHECKS: Tuple[Tuple[str, str, str, str, str, str], ...] = (
    ("B01", "boundary_registry_not_generated_in_planning", "planning", "boundary_object_registry_generated_now", "registry generated in planning", "P0"),
    ("B02", "boundary_object_not_registered_in_planning", "planning", "boundary_object_registered_now", "object registered in planning", "P0"),
    ("B03", "protected_assets_not_modified", "planning,dryrun,review", "protected_asset_modified_now", "protected assets modified", "P0"),
    ("B04", "HR_not_modified", "planning,dryrun,review", "human_review_queue_modified_now", "HR modified", "P0"),
    ("B05", "DnAE_not_modified", "planning,dryrun,review", "dnae_or_permanent_block_modified_now", "DnAE modified", "P0"),
    ("B06", "read_does_not_imply_write", "all", "write_allowed_now", "read implies write", "P0"),
    ("B07", "audit_support_not_success_evidence", "evidence", "success_evidence_allowed_now", "audit used as success evidence", "P0"),
    ("B08", "migration_requires_registry", "migration", "boundary_object_registry_generated_now", "migration without registry", "P0"),
    ("B09", "file_operation_requires_registry_and_approval", "file_operation", "file_operation_allowed_now", "file op without registry/approval", "P0"),
    ("B10", "restore_requires_restore_map_and_checkpoint", "rollback", "restore_operation_allowed_now", "restore without map/checkpoint", "P0"),
    ("B11", "evidence_generation_requires_boundary_registry", "evidence", "evidence_generation_allowed_now", "evidence without registry", "P0"),
    ("B12", "success_claim_requires_boundary_and_evidence_chain", "success_claim", "success_claim_allowed", "success claim without boundary chain", "P0"),
)

NON_CLAIM_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    ("planning GO", "planning GO does not mean boundary registry generated"),
    ("registry registered", "planning GO does not mean boundary objects registered"),
    ("category planned", "category planned does not mean object discovered"),
    ("read policy", "read policy planned does not mean write allowed"),
    ("migration policy", "migration policy planned does not mean migration allowed"),
    ("evidence policy", "evidence policy planned does not mean evidence generation allowed"),
    ("rollback policy", "rollback policy planned does not mean rollback allowed"),
    ("protected object", "protected object planned does not mean modifiable"),
    ("owner/operator dependency", "owner/operator dependency planned does not mean authorization granted"),
    ("file operation policy", "file operation policy planned does not mean file operation allowed"),
    ("verifier usage", "verifier usage planned does not mean verifier modified"),
    ("output plan", "output plan generated does not mean artifacts generated"),
)

OUTPUT_PLAN_ARTIFACTS: Tuple[Tuple[str, str, bool, bool, bool, bool, bool], ...] = (
    ("boundary_object_registry_policy_v1.json", "registry policy", True, True, True, True, True),
    ("boundary_object_category_matrix_v1.json", "category matrix", True, True, True, True, True),
    ("boundary_object_read_write_policy_matrix_v1.json", "read/write policy", True, True, True, True, True),
    ("boundary_object_migration_policy_matrix_v1.json", "migration policy", True, True, True, True, True),
    ("boundary_object_evidence_policy_matrix_v1.json", "evidence policy", True, True, True, True, True),
    ("boundary_object_rollback_policy_matrix_v1.json", "rollback policy", True, True, True, True, True),
    ("protected_and_blocked_object_matrix_v1.json", "protected/blocked objects", True, True, True, True, True),
    ("boundary_object_owner_operator_dependency_matrix_v1.json", "owner/operator dependency", True, True, True, True, True),
    ("boundary_object_file_operation_policy_matrix_v1.json", "file operation policy", True, True, True, True, True),
    ("boundary_object_forbidden_shortcut_matrix_v1.json", "forbidden shortcuts", True, True, False, True, True),
    ("boundary_object_verifier_usage_matrix_v1.json", "verifier usage", True, False, True, True, True),
    ("boundary_object_non_claims_rules_v1.json", "non-claims rules", True, True, False, True, True),
    ("boundary_object_registry_readiness_decision_v1.json", "readiness decision", True, True, True, True, True),
)

NO_WRITE_CATEGORIES = frozenset(
    {
        "protected assets",
        "human review queue / HR",
        "DnAE / permanent block",
    }
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "boundary_object_registry_planning_only": True,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "protected_asset_modified_now": False,
        "human_review_queue_modified_now": False,
        "dnae_or_permanent_block_modified_now": False,
        "file_operation_executed_now": False,
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
    readiness = _try_read_json(root / "owner_operator_roadmap_readiness_decision_v1.json") if root else None
    routes = _try_read_json(root / "owner_operator_roadmap_route_candidate_matrix_v1.json") if root else None
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


def _risk_level(category: str) -> str:
    if category in NO_WRITE_CATEGORIES:
        return "P0"
    if category in ("verifier artifacts", "phase verdict table", "migration batch", "rollback boundary"):
        return "P0"
    return "P1"


def _read_policy(category: str) -> str:
    if category == "eval_out artifacts":
        return "read allowed in phase output context; audit support only"
    if category in NO_WRITE_CATEGORIES:
        return "read allowed for governance review; write forbidden by default"
    if category in ("verifier artifacts", "phase verdict table"):
        return "read allowed; modification requires dedicated authorization"
    return "read allowed for planning and dry-run consumption"


def _write_policy(category: str) -> str:
    if category in NO_WRITE_CATEGORIES:
        return "write forbidden by default; requires owner approval + operator ack + execution window + boundary registry"
    if category == "eval_out artifacts":
        return "write allowed only in authorized phase output context; not in planning"
    if category in ("verifier artifacts", "phase verdict table"):
        return "write requires owner approval + operator ack + dedicated authorization"
    if category == "docs":
        return "write planned via governance phase; no auto sync in planning"
    return "write requires boundary registry + owner/operator authorization + execution window"


def _build_category_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            boundary_object_category=cat,
            canonical_meaning=meaning,
            why_required=why,
            default_risk_level=_risk_level(cat),
            read_policy_planned=_read_policy(cat),
            write_policy_planned=_write_policy(cat),
            migration_policy_planned="migration forbidden until boundary registry generated and authorized",
            evidence_policy_planned="evidence generation forbidden until boundary registry and authorization chain complete",
            rollback_policy_planned="rollback requires restore map + checkpoint + owner/operator authorization",
            owner_operator_dependency_planned="owner approval + operator acknowledgement required for write/migration",
            verifier_usage_planned=f"verify_{cat.replace(' ', '_').replace('/', '_')}_boundary",
            registered_now=False,
            registry_generated_now=False,
        )
        for cat, meaning, why in BOUNDARY_CATEGORIES
    ]


def _build_read_write_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for cat, _, _ in BOUNDARY_CATEGORIES:
        no_write_default = cat in NO_WRITE_CATEGORIES
        rows.append(
            _row(
                boundary_object_category=cat,
                read_allowed_by_default=True,
                write_allowed_by_default=False if no_write_default else False,
                write_requires_owner_approval=True,
                write_requires_operator_acknowledgement=True,
                write_requires_execution_window=True,
                write_requires_boundary_registry=True,
                write_allowed_now=False,
                file_operation_allowed_now=False,
                planned_verifier_check=f"verify_rw_{cat.replace(' ', '_').replace('/', '_')}",
            )
        )
    return rows


def _build_migration_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            boundary_object_category=cat,
            migration_allowed_by_default=False,
            migration_requires_owner_approval=True,
            migration_requires_operator_acknowledgement=True,
            migration_requires_restore_map=cat not in ("restore map",),
            migration_requires_rollback_plan=True,
            migration_requires_evidence_chain=True,
            migration_allowed_now=False,
            planned_verifier_check=f"verify_migration_{cat.replace(' ', '_').replace('/', '_')}",
        )
        for cat, _, _ in BOUNDARY_CATEGORIES
    ]


def _build_evidence_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for cat, _, _ in BOUNDARY_CATEGORIES:
        can_gen = cat == "evidence artifacts"
        can_source = cat in (
            "eval_out artifacts",
            "verifier artifacts",
            "checkpoint",
            "downstream handoff",
        )
        can_success = False
        rows.append(
            _row(
                boundary_object_category=cat,
                can_generate_evidence=can_gen,
                can_be_evidence_source=can_source,
                can_be_success_evidence_source=can_success,
                requires_source_chain=True,
                requires_evidence_acceptance=True,
                requires_owner_operator_authorization=True,
                evidence_generation_allowed_now=False,
                success_evidence_allowed_now=False,
                planned_verifier_check=f"verify_evidence_{cat.replace(' ', '_').replace('/', '_')}",
            )
        )
    return rows


def _build_rollback_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            boundary_object_category=cat,
            requires_restore_map=True,
            requires_checkpoint=True,
            requires_pre_change_snapshot=cat not in ("checkpoint", "restore map"),
            requires_owner_operator_authorization=True,
            rollback_allowed_now=False,
            restore_operation_allowed_now=False,
            planned_verifier_check=f"verify_rollback_{cat.replace(' ', '_').replace('/', '_')}",
        )
        for cat, _, _ in BOUNDARY_CATEGORIES
    ]


def _build_protected_blocked_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            protected_object_type=obj_type,
            why_protected=why,
            read_allowed=True,
            write_allowed_now=False,
            move_allowed_now=False,
            delete_allowed_now=False,
            merge_allowed_now=False,
            requires_owner_approval=True,
            requires_operator_acknowledgement=True,
            requires_boundary_registry=True,
            planned_verifier_check=f"verify_protected_{obj_type.replace(' ', '_')}",
        )
        for obj_type, why in PROTECTED_OBJECT_TYPES
    ]


def _build_owner_operator_dependency_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            boundary_object_category=cat,
            requires_owner_approval_for_write=True,
            requires_operator_acknowledgement_for_write=True,
            requires_execution_window_for_write=cat
            not in ("docs", "eval_out artifacts", "phase verdict table"),
            requires_scope_confirmation=True,
            requires_abort_authority=True,
            requires_post_execution_review=cat in ("migration batch", "rollback boundary", "evidence artifacts"),
            dependency_satisfied_now=False,
            authorization_granted_now=False,
        )
        for cat, _, _ in BOUNDARY_CATEGORIES
    ]


def _build_file_operation_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            file_operation=op,
            allowed_by_default=op == "read",
            requires_boundary_registry=op != "read",
            requires_owner_operator_approval=op != "read",
            requires_execution_window=op not in ("read", "copy"),
            requires_restore_map=op in ("restore", "move", "delete", "rename", "merge", "overwrite"),
            requires_checkpoint=op in ("restore", "move", "delete", "rename", "merge", "overwrite"),
            allowed_now=False,
            planned_verifier_check=f"verify_file_op_{op.replace(' ', '_').replace('/', '_')}",
        )
        for op in FILE_OPERATIONS
    ]


def _build_forbidden_shortcut_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            forbidden_shortcut=shortcut,
            why_forbidden=f"prevents misread of {affected}",
            affected_terms=affected,
            required_non_claim=non_claim,
            severity=severity,
            planned_verifier_check=f"verify_shortcut_{affected}",
            enforced_now=False,
        )
        for shortcut, affected, non_claim, severity in FORBIDDEN_SHORTCUTS
    ]


def _build_verifier_usage_matrix() -> List[Dict[str, Any]]:
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


def _build_non_claims_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            scenario=scenario,
            required_non_claim=claim,
            risk_if_missing="boundary registry or authorization misread",
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
            required=required,
            used_by_future_verifier=used_v,
            used_by_owner_operator_protocol=used_o,
            used_by_evidence_chain=used_e,
            used_by_real_rehearsal_chain=used_r,
            used_by_migration_chain=used_r,
            not_generated_now=True,
        )
        for artifact, purpose, required, used_v, used_o, used_e, used_r in OUTPUT_PLAN_ARTIFACTS
    ]


def run_boundary_object_registry_planning_v1(
    *,
    owner_operator_approval_protocol_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(owner_operator_approval_protocol_roadmap_decision_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    routes = upstream["routes"] or upstream["artifacts"].get(
        "owner_operator_roadmap_route_candidate_matrix_v1.json", {}
    )

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream roadmap decision verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_summary.get("selected_route") != SELECTED_ROUTE:
        blockers.append("upstream selected_route is not Route A")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_readiness.get("ready_for_boundary_object_registry_planning") is not True:
        blockers.append("upstream not ready_for_boundary_object_registry_planning")
    for flag in (
        "boundary_object_registry_generated_now",
        "boundary_object_registered_now",
        "owner_approval_request_sent_now",
        "operator_acknowledgement_request_sent_now",
        "owner_approval_granted_now",
        "operator_acknowledgement_granted_now",
        "execution_window_opened_now",
        "evidence_generation_authorized_now",
        "evidence_generated_now",
        "success_claim_allowed",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")
    for flag in (
        "ready_for_boundary_object_registry_generation",
        "ready_for_owner_approval_request",
        "ready_for_operator_acknowledgement_request",
        "ready_for_execution_window_opening",
        "ready_for_evidence_generation_authorization",
        "ready_for_real_rollback_rehearsal_execution",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")
    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("upstream real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("upstream batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    route_a = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "A"), {})
    route_h = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "H"), {})
    if route_a.get("selected_now") is not True:
        blockers.append("Route A not selected in upstream matrix")
    if route_h.get("blocked_now") is not True:
        blockers.append("Route H must be blocked")

    category_rows = _build_category_matrix()
    rw_rows = _build_read_write_matrix()
    migration_rows = _build_migration_matrix()
    evidence_rows = _build_evidence_matrix()
    rollback_rows = _build_rollback_matrix()
    protected_rows = _build_protected_blocked_matrix()
    oo_dep_rows = _build_owner_operator_dependency_matrix()
    file_op_rows = _build_file_operation_matrix()
    shortcut_rows = _build_forbidden_shortcut_matrix()
    verifier_rows = _build_verifier_usage_matrix()
    non_claims_rows = _build_non_claims_matrix()
    output_rows = _build_output_plan()

    protected_frozen = all(
        r.get("write_allowed_now") is False
        and r.get("move_allowed_now") is False
        and r.get("delete_allowed_now") is False
        and r.get("merge_allowed_now") is False
        for r in protected_rows
    )
    rw_frozen = all(r.get("write_allowed_now") is False for r in rw_rows)
    migration_frozen = all(r.get("migration_allowed_now") is False for r in migration_rows)
    evidence_frozen = all(
        r.get("evidence_generation_allowed_now") is False and r.get("success_evidence_allowed_now") is False
        for r in evidence_rows
    )
    rollback_frozen = all(
        r.get("rollback_allowed_now") is False and r.get("restore_operation_allowed_now") is False
        for r in rollback_rows
    )
    file_op_frozen = all(r.get("allowed_now") is False for r in file_op_rows)

    planning_pass = (
        len(category_rows) >= 16
        and len(rw_rows) >= 16
        and len(migration_rows) >= 16
        and len(evidence_rows) >= 16
        and len(rollback_rows) >= 16
        and len(protected_rows) >= 12
        and len(oo_dep_rows) >= 16
        and len(file_op_rows) >= 14
        and len(shortcut_rows) >= 12
        and len(verifier_rows) >= 12
        and len(non_claims_rows) >= 12
        and len(output_rows) >= 13
        and all(r.get("not_generated_now") is True for r in output_rows)
        and all(r.get("registered_now") is False and r.get("registry_generated_now") is False for r in category_rows)
        and protected_frozen
        and rw_frozen
        and migration_frozen
        and evidence_frozen
        and rollback_frozen
        and file_op_frozen
        and not blockers
    )
    boundary_ok = planning_pass

    boundary_object_registry_planning_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_selected_route_observed=up_summary.get("selected_route"),
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
    )

    boundary_object_category_planning_matrix = {
        "rows": category_rows,
        "row_count": len(category_rows),
        **_planning_meta(),
    }
    boundary_object_read_write_policy_planning_matrix = {
        "rows": rw_rows,
        "row_count": len(rw_rows),
        **_planning_meta(),
    }
    boundary_object_migration_policy_planning_matrix = {
        "rows": migration_rows,
        "row_count": len(migration_rows),
        **_planning_meta(),
    }
    boundary_object_evidence_policy_planning_matrix = {
        "rows": evidence_rows,
        "row_count": len(evidence_rows),
        **_planning_meta(),
    }
    boundary_object_rollback_policy_planning_matrix = {
        "rows": rollback_rows,
        "row_count": len(rollback_rows),
        **_planning_meta(),
    }
    protected_and_blocked_object_planning_matrix = {
        "rows": protected_rows,
        "row_count": len(protected_rows),
        **_planning_meta(),
    }
    boundary_object_owner_operator_dependency_matrix = {
        "rows": oo_dep_rows,
        "row_count": len(oo_dep_rows),
        **_planning_meta(),
    }
    boundary_object_file_operation_policy_planning_matrix = {
        "rows": file_op_rows,
        "row_count": len(file_op_rows),
        **_planning_meta(),
    }
    boundary_object_forbidden_shortcut_matrix = {
        "rows": shortcut_rows,
        "row_count": len(shortcut_rows),
        **_planning_meta(),
    }
    boundary_object_verifier_usage_planning_matrix = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        **_planning_meta(),
    }
    boundary_object_non_claims_planning_matrix = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        **_planning_meta(),
    }
    boundary_object_registry_output_plan = {
        "rows": output_rows,
        "row_count": len(output_rows),
        **_planning_meta(),
    }

    boundary_object_registry_planning_readiness_decision = {
        "ready_for_boundary_object_registry_dryrun": boundary_ok,
        "ready_for_boundary_object_registry_generation": False,
        "ready_for_boundary_object_registration": False,
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
        "boundary_object_registry_planning_completed": boundary_ok,
        "category_planning_completed": True,
        "read_write_policy_planned": True,
        "migration_policy_planned": True,
        "evidence_policy_planned": True,
        "rollback_policy_planned": True,
        "protected_blocked_object_planned": True,
        "owner_operator_dependency_planned": True,
        "file_operation_policy_planned": True,
        "forbidden_shortcuts_planned": True,
        "verifier_usage_planned": True,
        "non_claims_planned": True,
        "output_plan_generated": True,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "file_operation_executed_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "owner_operator_approval_protocol_roadmap_decision_input_loaded": upstream["loaded"],
        "source_selected_route_observed": up_summary.get("selected_route"),
        "category_count": len(category_rows),
        "read_write_policy_count": len(rw_rows),
        "migration_policy_count": len(migration_rows),
        "evidence_policy_count": len(evidence_rows),
        "rollback_policy_count": len(rollback_rows),
        "protected_blocked_object_count": len(protected_rows),
        "owner_operator_dependency_count": len(oo_dep_rows),
        "file_operation_policy_count": len(file_op_rows),
        "forbidden_shortcut_count": len(shortcut_rows),
        "verifier_usage_count": len(verifier_rows),
        "non_claims_count": len(non_claims_rows),
        "output_plan_count": len(output_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "boundary_object_registry_planning_policy": boundary_object_registry_planning_policy,
        "boundary_object_category_planning_matrix": boundary_object_category_planning_matrix,
        "boundary_object_read_write_policy_planning_matrix": boundary_object_read_write_policy_planning_matrix,
        "boundary_object_migration_policy_planning_matrix": boundary_object_migration_policy_planning_matrix,
        "boundary_object_evidence_policy_planning_matrix": boundary_object_evidence_policy_planning_matrix,
        "boundary_object_rollback_policy_planning_matrix": boundary_object_rollback_policy_planning_matrix,
        "protected_and_blocked_object_planning_matrix": protected_and_blocked_object_planning_matrix,
        "boundary_object_owner_operator_dependency_matrix": boundary_object_owner_operator_dependency_matrix,
        "boundary_object_file_operation_policy_planning_matrix": boundary_object_file_operation_policy_planning_matrix,
        "boundary_object_forbidden_shortcut_matrix": boundary_object_forbidden_shortcut_matrix,
        "boundary_object_verifier_usage_planning_matrix": boundary_object_verifier_usage_planning_matrix,
        "boundary_object_non_claims_planning_matrix": boundary_object_non_claims_planning_matrix,
        "boundary_object_registry_output_plan": boundary_object_registry_output_plan,
        "boundary_object_registry_planning_readiness_decision": boundary_object_registry_planning_readiness_decision,
    }
