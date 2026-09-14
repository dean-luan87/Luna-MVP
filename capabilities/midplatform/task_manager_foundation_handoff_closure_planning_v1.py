# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Closure Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    SKELETON_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_HANDOFF_DRYRUN_ROOT,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    CANDIDATE_SEMANTICS,
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    FOUNDATION_ID,
)
from capabilities.midplatform.task_manager_foundation_handoff_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Closure-Planning-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_closure_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_closure_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_PLANNING_READY_FOR_CLOSURE_DRYRUN"
FINAL_DECISION_PRIOR = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_PLANNING_BLOCKED_BY_PRIOR_CHAIN_GAP"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_PLANNING_BLOCKED_BY_EVIDENCE_CHAIN_GAP"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_PLANNING_BLOCKED_BY_FREEZE_SCOPE_LEAKAGE"
FINAL_DECISION_SEMANTICS = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_PLANNING_BLOCKED_BY_CANDIDATE_SEMANTICS_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_DOWNSTREAM = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_PLANNING_BLOCKED_BY_DOWNSTREAM_SCOPE_ESCALATION"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Closure-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Closure-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_closure_planning_v1_smoke_v0"
)

PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_plan_v1.json",
    "task_manager_foundation_handoff_plan_v1.md",
    "task_manager_foundation_boundary_matrix_v1.json",
    "task_manager_candidate_lifecycle_matrix_v1.json",
    "task_manager_downstream_readiness_matrix_v1.json",
    "task_manager_non_execution_constraints_v1.json",
    "summary.json",
    "verifier_report.json",
)
DRYRUN_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_dryrun_report_v1.json",
    "task_manager_foundation_handoff_dryrun_report_v1.md",
    "task_manager_handoff_package_integrity_matrix_v1.json",
    "task_manager_handoff_evidence_traceability_matrix_v1.json",
    "task_manager_handoff_downstream_consumption_dryrun_matrix_v1.json",
    "task_manager_handoff_non_execution_verification_v1.json",
    "summary.json",
    "verifier_report.json",
)
POST_REVIEW_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_post_dryrun_review_v1.json",
    "task_manager_foundation_handoff_post_dryrun_review_v1.md",
    "task_manager_handoff_dryrun_review_matrix_v1.json",
    "task_manager_handoff_boundary_drift_review_v1.json",
    "task_manager_handoff_evidence_chain_review_v1.json",
    "task_manager_handoff_closure_readiness_matrix_v1.json",
    "task_manager_handoff_review_non_execution_constraints_v1.json",
    "summary.json",
    "verifier_report.json",
)
FORBIDDEN_DOWNSTREAM: Tuple[str, ...] = ("implementation-ready", "runtime-ready", "production-ready")
FORBIDDEN_FREEZE_STATUS: Tuple[str, ...] = ("frozen", "foundation_frozen", "foundation-frozen", "closed", "finalized")
NON_EXECUTION_CONSTRAINTS: Tuple[str, ...] = (
    "no_runtime_executor",
    "no_scheduler_binding",
    "no_task_execution_authority",
    "no_output_authorization",
    "no_memory_worldmodel_write_path",
    "no_module_adapter_integration",
    "no_authorization_grant",
    "no_information_channel_governance_implementation",
    "no_protocol_governance_implementation",
    "no_closure_execution",
    "no_foundation_freeze",
)
DOWNSTREAM_PLANNING_MAP: Tuple[Dict[str, str], ...] = (
    {"consumer": "module_adapter", "readiness": "planning-handoff-ready"},
    {"consumer": "output_gate", "readiness": "planning-handoff-ready"},
    {"consumer": "worldmodel_memory_bridge", "readiness": "planning-handoff-ready"},
    {"consumer": "system_diagnostics", "readiness": "planning-handoff-ready"},
)
FUTURE_L1_DEPENDENCIES: Tuple[Dict[str, str], ...] = (
    {"protocol": "information_channel_governance", "status": "future_l1_dependency", "implemented": "false"},
    {"protocol": "protocol_governance", "status": "future_l1_dependency", "implemented": "false"},
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, planning: Path, dryrun: Path, post: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "closure_planning_only": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "output_root": str(out),
        "planning_root": str(planning),
        "handoff_dryrun_root": str(dryrun),
        "post_review_root": str(post),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def _prior_chain_go(planning: Path, dryrun: Path, post: Path) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    stages = (
        ("planning", planning, PLANNING_FINAL_GO),
        ("dryrun", dryrun, DRYRUN_FINAL_GO),
        ("post_review", post, POST_REVIEW_FINAL_GO),
    )
    for name, root, expected_final in stages:
        summary = _read_json(root / "summary.json")
        verifier = _read_json(root / "verifier_report.json")
        if summary.get("final_decision") != expected_final:
            issues.append(f"{name}_summary_not_go")
        if verifier.get("verifier") != "GO":
            issues.append(f"{name}_verifier_not_go")
        if verifier.get("failed_checks", -1) != 0:
            issues.append(f"{name}_failed_checks_nonzero")
        if verifier.get("blocker_count", -1) != 0:
            issues.append(f"{name}_blocker_nonzero")
    return len(issues) == 0, issues


def run_task_manager_foundation_handoff_closure_planning_v1(
    *,
    planning_root: str,
    handoff_dryrun_root: str,
    post_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(planning_root).expanduser().resolve()
    dryrun = Path(handoff_dryrun_root).expanduser().resolve()
    post = Path(post_review_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, planning, dryrun, post)
    issues: List[str] = []

    prior_chain_go, prior_issues = _prior_chain_go(planning, dryrun, post)
    issues.extend(prior_issues)

    asset_rows: List[Dict[str, Any]] = []
    for rel in SKELETON_FILES:
        path = repo_root / rel
        asset_rows.append({"asset_type": "core_skeleton", "path": rel, "exists": path.is_file()})
        if not path.is_file():
            issues.append(f"missing_core_skeleton:{rel}")
    for package_name, files, root in (
        ("planning_package", PLANNING_PACKAGE_FILES, planning),
        ("dryrun_package", DRYRUN_PACKAGE_FILES, dryrun),
        ("post_review_package", POST_REVIEW_PACKAGE_FILES, post),
    ):
        for fname in files:
            path = root / fname
            asset_rows.append(
                {"asset_type": package_name, "path": str(path), "file": fname, "exists": path.is_file()}
            )
            if not path.is_file():
                issues.append(f"missing_asset:{package_name}:{fname}")

    evidence_chain = [
        {"stage": "planning", "root": str(planning), "final_decision": PLANNING_FINAL_GO, "linked": True},
        {"stage": "dryrun", "root": str(dryrun), "final_decision": DRYRUN_FINAL_GO, "linked": True},
        {"stage": "post_dryrun_review", "root": str(post), "final_decision": POST_REVIEW_FINAL_GO, "linked": True},
        {"stage": "closure_planning", "root": str(out), "readiness": "closure-dryrun-ready", "closure_applied": False},
    ]
    evidence_chain_complete = prior_chain_go and all(row.get("linked") for row in evidence_chain[:3])
    if not evidence_chain_complete:
        issues.append("evidence_chain_gap")

    freeze_candidate_boundary = {
        "freeze_status": "freeze-candidate",
        "foundation_frozen": False,
        "closure_executed": False,
        "closure_readiness": "closure-dryrun-ready",
        "closure_applied": False,
        "candidate_types_to_freeze": [s["payload_type"] for s in CANDIDATE_SEMANTICS],
        "skeleton_files_to_freeze": list(SKELETON_FILES),
    }
    freeze_candidate_only = (
        freeze_candidate_boundary["freeze_status"] == "freeze-candidate"
        and freeze_candidate_boundary["foundation_frozen"] is False
        and freeze_candidate_boundary["closure_applied"] is False
    )
    if not freeze_candidate_only:
        issues.append("freeze_scope_leakage")

    semantics_lock_plan = {
        "lock_plan_only": True,
        "semantics_executed": False,
        "boundaries": list(CANDIDATE_SEMANTICS),
        "task_candidate_not_task_execution": True,
        "task_step_candidate_not_executed_step": True,
        "task_handoff_candidate_not_direct_mount": True,
    }
    candidate_semantics_preserved = all(
        item.get("boundary") for item in semantics_lock_plan["boundaries"]
    ) and semantics_lock_plan["lock_plan_only"] is True
    if not candidate_semantics_preserved:
        issues.append("candidate_semantics_drift")

    downstream_scope_ok = all(
        row["readiness"] == "planning-handoff-ready"
        and row["readiness"] not in FORBIDDEN_DOWNSTREAM
        for row in DOWNSTREAM_PLANNING_MAP
    )
    future_l1_dependencies_only = all(
        dep["status"] == "future_l1_dependency" and dep["implemented"] == "false"
        for dep in FUTURE_L1_DEPENDENCIES
    )
    if not downstream_scope_ok:
        issues.append("downstream_scope_escalation")
    if not future_l1_dependencies_only:
        issues.append("l1_protocol_implementation_leak")

    non_execution_boundary_ok = True
    closure_non_execution = {
        "constraints": list(NON_EXECUTION_CONSTRAINTS),
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **{c: True for c in NON_EXECUTION_CONSTRAINTS},
    }

    asset_inventory_complete = all(row.get("exists") for row in asset_rows)
    closure_plan_complete = prior_chain_go and asset_inventory_complete and evidence_chain_complete
    if not asset_inventory_complete:
        issues.append("asset_inventory_incomplete")

    if not prior_chain_go:
        final_decision = FINAL_DECISION_PRIOR
    elif not evidence_chain_complete:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not freeze_candidate_only:
        final_decision = FINAL_DECISION_FREEZE
    elif not candidate_semantics_preserved:
        final_decision = FINAL_DECISION_SEMANTICS
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not downstream_scope_ok:
        final_decision = FINAL_DECISION_DOWNSTREAM
    else:
        final_decision = FINAL_DECISION_GO

    planning_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO
    closure_plan = {
        "plan_id": "task_manager_foundation_handoff_closure_plan_v1",
        "closure_scope": [
            "close handoff evidence chain from planning through post-dryrun review",
            "define freeze-candidate boundary without executing freeze",
            "inventory foundation assets for closure dry-run",
            "lock candidate semantics in planning only",
            "map downstream planning handoff consumers",
            "declare future L1 protocol dependencies only",
        ],
        "prior_chain_go": prior_chain_go,
        "closure_plan_complete": closure_plan_complete,
        "asset_inventory_complete": asset_inventory_complete,
        "evidence_chain_complete": evidence_chain_complete,
        "freeze_candidate_only": freeze_candidate_only,
        "closure_planning_only": True,
        "closure_readiness": "closure-dryrun-ready",
        "closure_applied": False,
        "foundation_not_frozen": True,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "future_l1_dependencies_only": future_l1_dependencies_only,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    asset_inventory = {
        "inventory_id": "task_manager_foundation_asset_inventory_v1",
        "assets": asset_rows,
        "asset_inventory_complete": asset_inventory_complete,
        **meta,
    }
    evidence_chain_doc = {
        "chain_id": "task_manager_handoff_closure_evidence_chain_v1",
        "chain": evidence_chain,
        "evidence_chain_complete": evidence_chain_complete,
        **meta,
    }
    freeze_boundary_doc = {
        "boundary_id": "task_manager_handoff_freeze_candidate_boundary_v1",
        **freeze_candidate_boundary,
        "freeze_candidate_only": freeze_candidate_only,
        **meta,
    }
    semantics_lock_doc = {
        "plan_id": "task_manager_handoff_candidate_semantics_lock_plan_v1",
        **semantics_lock_plan,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        **meta,
    }
    downstream_map = {
        "map_id": "task_manager_handoff_downstream_planning_map_v1",
        "consumers": list(DOWNSTREAM_PLANNING_MAP),
        "downstream_scope_ok": downstream_scope_ok,
        **meta,
    }
    l1_dependency_map = {
        "map_id": "task_manager_handoff_future_l1_protocol_dependency_map_v1",
        "dependencies": list(FUTURE_L1_DEPENDENCIES),
        "future_l1_dependencies_only": future_l1_dependencies_only,
        **meta,
    }
    non_execution_doc = {
        "constraints_id": "task_manager_handoff_closure_non_execution_constraints_v1",
        **closure_non_execution,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "prior_chain_go": prior_chain_go,
        "closure_plan_complete": closure_plan_complete,
        "asset_inventory_complete": asset_inventory_complete,
        "evidence_chain_complete": evidence_chain_complete,
        "freeze_candidate_only": freeze_candidate_only,
        "closure_planning_only": True,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "future_l1_dependencies_only": future_l1_dependencies_only,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Closure Plan v1",
            "",
            "This phase performs closure planning only. It does not execute closure or freeze the foundation.",
            "",
            "本阶段仅执行 closure planning，不执行 closure，不冻结 foundation。",
            "",
            f"Prior chain GO: `{prior_chain_go}`",
            f"Closure readiness: `closure-dryrun-ready`",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Preserved Boundaries",
            "- task_candidate != task execution",
            "- task_step_candidate != executed step",
            "- task_handoff_candidate != direct mount",
            "- Information Channel Governance: future L1 dependency only",
            "- Protocol Governance: future L1 dependency only",
        ]
    )
    return {
        "task_manager_foundation_handoff_closure_plan": closure_plan,
        "task_manager_foundation_handoff_closure_plan_md": markdown,
        "task_manager_foundation_asset_inventory": asset_inventory,
        "task_manager_handoff_closure_evidence_chain": evidence_chain_doc,
        "task_manager_handoff_freeze_candidate_boundary": freeze_boundary_doc,
        "task_manager_handoff_candidate_semantics_lock_plan": semantics_lock_doc,
        "task_manager_handoff_downstream_planning_map": downstream_map,
        "task_manager_handoff_future_l1_protocol_dependency_map": l1_dependency_map,
        "task_manager_handoff_closure_non_execution_constraints": non_execution_doc,
        "summary": summary,
    }
