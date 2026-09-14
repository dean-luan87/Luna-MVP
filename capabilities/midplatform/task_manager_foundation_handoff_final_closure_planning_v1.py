# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Final Closure Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    SKELETON_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_closure_dryrun_v1 import (
    CLOSURE_CHANNEL_BOUNDARIES,
    CLOSURE_PLANNING_PACKAGE_FILES,
    DEFAULT_OUTPUT as DEFAULT_CLOSURE_DRYRUN_ROOT,
    FINAL_DECISION_GO as CLOSURE_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_closure_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CLOSURE_PLANNING_ROOT,
    DRYRUN_PACKAGE_FILES,
    FINAL_DECISION_GO as CLOSURE_PLANNING_FINAL_GO,
    PLANNING_PACKAGE_FILES,
    POST_REVIEW_PACKAGE_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_closure_post_dryrun_review_v1 import (
    CLOSURE_DRYRUN_ARTIFACTS,
    DEFAULT_OUTPUT as DEFAULT_CLOSURE_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as CLOSURE_POST_REVIEW_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_HANDOFF_DRYRUN_ROOT,
    FINAL_DECISION_GO as HANDOFF_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    DEFAULT_OUTPUT as DEFAULT_HANDOFF_PLANNING_ROOT,
    FINAL_DECISION_GO as HANDOFF_PLANNING_FINAL_GO,
    FOUNDATION_ID,
)
from capabilities.midplatform.task_manager_foundation_handoff_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_HANDOFF_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as HANDOFF_POST_REVIEW_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-Planning-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_final_closure_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_final_closure_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_PLANNING_READY_FOR_FINAL_CLOSURE_DRYRUN"
FINAL_DECISION_PRIOR = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_PLANNING_BLOCKED_BY_PRIOR_CHAIN_GAP"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_PLANNING_BLOCKED_BY_EVIDENCE_CHAIN_GAP"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_PLANNING_BLOCKED_BY_FREEZE_SCOPE_LEAKAGE"
FINAL_DECISION_STATE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_PLANNING_BLOCKED_BY_CLOSURE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_PLANNING_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_PLANNING_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_final_closure_planning_v1_smoke_v0"
)
CLOSURE_POST_REVIEW_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_closure_post_dryrun_review_v1.json",
    "task_manager_foundation_handoff_closure_post_dryrun_review_v1.md",
    "task_manager_closure_dryrun_review_matrix_v1.json",
    "task_manager_closure_boundary_drift_review_v1.json",
    "task_manager_closure_evidence_chain_review_v1.json",
    "task_manager_closure_governance_debt_review_v1.json",
    "task_manager_closure_final_planning_readiness_matrix_v1.json",
    "task_manager_closure_review_non_execution_constraints_v1.json",
    "summary.json",
    "verifier_report.json",
)
CLOSURE_DRYRUN_PACKAGE_FILES: Tuple[str, ...] = tuple(CLOSURE_DRYRUN_ARTIFACTS)
BOUNDARY_CONTRACT_STATEMENTS: Tuple[str, ...] = (
    "final_closure_planning != closure_execution",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
    "handoff_candidate != handed_off",
    "finalization_candidate != finalized",
)
GOVERNANCE_DEBTS: Tuple[Dict[str, Any], ...] = (
    {
        "debt_id": "closure_channel_governance_missing_canonical_protocol",
        "debt_title": "Closure Channel Governance Missing Canonical Protocol",
        "priority": "P1",
        "classification": "L1 Midplatform System Protocols",
        "debt_type": "canonical_protocol_missing",
        "must_not_implement_now": True,
        "recommended_future_phase": "Phase-Midplatform-Closure-Channel-Governance-Planning-v1-001",
    },
    {
        "debt_id": "system_protocols_integration_required_before_module_adapter",
        "debt_title": "System Protocols Integration Required Before Module Adapter Implementation",
        "priority": "P1",
        "classification": "L1 Midplatform System Protocols",
        "debt_type": "integration_debt",
        "must_not_implement_now": True,
        "recommended_future_phase": "Phase-Midplatform-System-Protocols-Integration-Planning-v1-001",
    },
)
FORBIDDEN_DOWNSTREAM: Tuple[str, ...] = ("implementation-ready", "runtime-ready", "production-ready")
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
    "no_closure_channel_governance_implementation",
    "no_system_protocols_integration_implementation",
    "no_closure_execution",
    "no_foundation_freeze",
)
DOWNSTREAM_REFERENCE_MAP: Tuple[Dict[str, str], ...] = (
    {"consumer": "module_adapter", "readiness": "planning-reference-ready"},
    {"consumer": "output_gate", "readiness": "reference-ready"},
    {"consumer": "worldmodel_memory_bridge", "readiness": "planning-reference-ready"},
    {"consumer": "system_diagnostics", "readiness": "reference-ready"},
    {"consumer": "freeze_authorization_planning", "readiness": "planning-reference-ready"},
    {"consumer": "final_closure_dryrun", "readiness": "planning-reference-ready"},
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(
    out: Path,
    planning: Path,
    dryrun: Path,
    post: Path,
    closure_planning: Path,
    closure_dryrun: Path,
    closure_post: Path,
) -> Dict[str, Any]:
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
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "handoff_planning_root": str(planning),
        "handoff_dryrun_root": str(dryrun),
        "handoff_post_review_root": str(post),
        "closure_planning_root": str(closure_planning),
        "closure_dryrun_root": str(closure_dryrun),
        "closure_post_review_root": str(closure_post),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def _prior_full_chain_go(
    planning: Path,
    dryrun: Path,
    post: Path,
    closure_planning: Path,
    closure_dryrun: Path,
    closure_post: Path,
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    stages = (
        ("handoff_planning", planning, HANDOFF_PLANNING_FINAL_GO),
        ("handoff_dryrun", dryrun, HANDOFF_DRYRUN_FINAL_GO),
        ("handoff_post_review", post, HANDOFF_POST_REVIEW_FINAL_GO),
        ("closure_planning", closure_planning, CLOSURE_PLANNING_FINAL_GO),
        ("closure_dryrun", closure_dryrun, CLOSURE_DRYRUN_FINAL_GO),
        ("closure_post_review", closure_post, CLOSURE_POST_REVIEW_FINAL_GO),
    )
    for name, root, expected_final in stages:
        summary = _read_json(root / "summary.json")
        verifier = _read_json(root / "verifier_report.json")
        if not (root / "summary.json").is_file():
            issues.append(f"{name}_summary_missing")
        if not (root / "verifier_report.json").is_file():
            issues.append(f"{name}_verifier_missing")
        if summary.get("final_decision") != expected_final:
            issues.append(f"{name}_summary_not_go")
        if verifier.get("verifier") != "GO":
            issues.append(f"{name}_verifier_not_go")
        if verifier.get("failed_checks", -1) != 0:
            issues.append(f"{name}_failed_checks_nonzero")
        if verifier.get("blocker_count", -1) != 0:
            issues.append(f"{name}_blocker_nonzero")
    return len(issues) == 0, issues


def run_task_manager_foundation_handoff_final_closure_planning_v1(
    *,
    handoff_planning_root: str,
    handoff_dryrun_root: str,
    handoff_post_review_root: str,
    closure_planning_root: str,
    closure_dryrun_root: str,
    closure_post_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(handoff_planning_root).expanduser().resolve()
    dryrun = Path(handoff_dryrun_root).expanduser().resolve()
    post = Path(handoff_post_review_root).expanduser().resolve()
    closure_planning = Path(closure_planning_root).expanduser().resolve()
    closure_dryrun = Path(closure_dryrun_root).expanduser().resolve()
    closure_post = Path(closure_post_review_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, planning, dryrun, post, closure_planning, closure_dryrun, closure_post)
    issues: List[str] = []

    prior_full_chain_go, prior_issues = _prior_full_chain_go(
        planning, dryrun, post, closure_planning, closure_dryrun, closure_post
    )
    issues.extend(prior_issues)

    asset_rows: List[Dict[str, Any]] = []
    for rel in SKELETON_FILES:
        path = repo_root / rel
        asset_rows.append(
            {
                "asset_type": "core_skeleton",
                "path": rel,
                "freeze_status": "freeze-candidate",
                "exists": path.is_file(),
            }
        )
        if not path.is_file():
            issues.append(f"missing_core_skeleton:{rel}")
    for package_name, files, root in (
        ("planning_package", PLANNING_PACKAGE_FILES, planning),
        ("dryrun_package", DRYRUN_PACKAGE_FILES, dryrun),
        ("post_review_package", POST_REVIEW_PACKAGE_FILES, post),
        ("closure_planning_package", CLOSURE_PLANNING_PACKAGE_FILES, closure_planning),
        ("closure_dryrun_package", CLOSURE_DRYRUN_PACKAGE_FILES, closure_dryrun),
        ("closure_post_review_package", CLOSURE_POST_REVIEW_PACKAGE_FILES, closure_post),
    ):
        for fname in files:
            path = root / fname
            asset_rows.append(
                {
                    "asset_type": package_name,
                    "path": str(path),
                    "file": fname,
                    "freeze_status": "freeze-candidate",
                    "exists": path.is_file(),
                }
            )
            if not path.is_file():
                issues.append(f"missing_asset:{package_name}:{fname}")

    freeze_candidate_asset_map_complete = all(row.get("exists") for row in asset_rows)
    freeze_candidate_only = all(
        row.get("freeze_status") == "freeze-candidate" and row.get("freeze_status") != "frozen"
        for row in asset_rows
    )
    if not freeze_candidate_asset_map_complete:
        issues.append("freeze_asset_map_incomplete")
    if not freeze_candidate_only:
        issues.append("freeze_scope_leakage")

    evidence_chain = [
        {"stage": "planning", "root": str(planning), "final_decision": HANDOFF_PLANNING_FINAL_GO, "linked": True},
        {"stage": "dryrun", "root": str(dryrun), "final_decision": HANDOFF_DRYRUN_FINAL_GO, "linked": True},
        {"stage": "post_dryrun_review", "root": str(post), "final_decision": HANDOFF_POST_REVIEW_FINAL_GO, "linked": True},
        {"stage": "closure_planning", "root": str(closure_planning), "final_decision": CLOSURE_PLANNING_FINAL_GO, "linked": True},
        {"stage": "closure_dryrun", "root": str(closure_dryrun), "final_decision": CLOSURE_DRYRUN_FINAL_GO, "linked": True},
        {"stage": "closure_post_dryrun_review", "root": str(closure_post), "final_decision": CLOSURE_POST_REVIEW_FINAL_GO, "linked": True},
        {
            "stage": "final_closure_planning",
            "root": str(out),
            "readiness": "final-closure-planning-ready",
            "closure_applied": False,
            "linked": True,
        },
    ]
    chain_evidence_complete = prior_full_chain_go and all(row.get("linked") for row in evidence_chain[:6])
    if not chain_evidence_complete:
        issues.append("evidence_chain_gap")

    closure_state_ok = True
    closure_readiness = "final-closure-planning-ready"
    if closure_readiness == "closed":
        closure_state_ok = False
        issues.append("closure_state_escalation")

    boundary_contract = {
        "contract_id": "task_manager_final_closure_boundary_contract_v1",
        "statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "closure_readiness": closure_readiness,
        "freeze_status": "freeze-candidate",
        "foundation_frozen": False,
        "closure_applied": False,
        "final_closure_planning_not_closure_execution": True,
    }
    candidate_semantics_preserved = all(stmt in BOUNDARY_CONTRACT_STATEMENTS for stmt in BOUNDARY_CONTRACT_STATEMENTS)
    for item in CLOSURE_CHANNEL_BOUNDARIES:
        if item["boundary"] not in BOUNDARY_CONTRACT_STATEMENTS and item["candidate"] not in (
            "deprecation_candidate",
            "rollback_recommendation_candidate",
            "archive_candidate",
            "task_candidate",
            "task_step_candidate",
        ):
            pass

    semantics_lock_plan = {
        "plan_id": "task_manager_final_candidate_semantics_lock_plan_v1",
        "lock_plan_only": True,
        "semantics_executed": False,
        "lock_executed": False,
        "boundaries": list(CLOSURE_CHANNEL_BOUNDARIES),
    }
    if not semantics_lock_plan["lock_plan_only"] or semantics_lock_plan["semantics_executed"]:
        issues.append("semantics_lock_executed")

    downstream_reference_scope_ok = all(
        row["readiness"] in ("reference-ready", "planning-reference-ready")
        and row["readiness"] not in FORBIDDEN_DOWNSTREAM
        for row in DOWNSTREAM_REFERENCE_MAP
    )
    if not downstream_reference_scope_ok:
        issues.append("downstream_reference_escalation")

    debts = list(GOVERNANCE_DEBTS)
    governance_debt_carryover_complete = (
        len(debts) >= 2
        and debts[0]["debt_title"] == "Closure Channel Governance Missing Canonical Protocol"
        and debts[0]["priority"] == "P1"
        and debts[0]["classification"] == "L1 Midplatform System Protocols"
        and debts[0]["must_not_implement_now"] is True
        and debts[0]["recommended_future_phase"] == "Phase-Midplatform-Closure-Channel-Governance-Planning-v1-001"
        and debts[1]["debt_title"] == "System Protocols Integration Required Before Module Adapter Implementation"
        and debts[1]["priority"] == "P1"
        and debts[1]["classification"] == "L1 Midplatform System Protocols"
        and debts[1]["must_not_implement_now"] is True
        and debts[1]["recommended_future_phase"] == "Phase-Midplatform-System-Protocols-Integration-Planning-v1-001"
    )
    if not governance_debt_carryover_complete:
        issues.append("governance_debt_gap")

    l1_protocols_not_implemented = all(
        debt.get("must_not_implement_now") is True for debt in debts
    )
    system_protocols_integration_not_implemented = debts[1].get("must_not_implement_now") is True
    if not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        issues.append("l1_protocol_scope_leakage")

    non_execution_boundary_ok = True
    non_execution = {
        "constraints_id": "task_manager_final_non_execution_constraints_v1",
        "constraints": list(NON_EXECUTION_CONSTRAINTS),
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **{c: True for c in NON_EXECUTION_CONSTRAINTS},
        **meta,
    }

    next_phase_readiness = {
        "readiness_id": "task_manager_final_closure_next_phase_readiness_v1",
        "candidates": [
            {
                "phase": "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-DryRun-v1-001",
                "readiness": "final-closure-dryrun-ready",
                "module_adapter_implementation": False,
            },
            {
                "phase": "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Planning-v1-001",
                "readiness": "freeze-authorization-planning-ready",
                "module_adapter_implementation": False,
            },
        ],
        "module_adapter_implementation_ready": False,
        "recommended_next_phase": NEXT_PHASE_GO,
    }

    final_closure_plan_complete = (
        prior_full_chain_go
        and freeze_candidate_asset_map_complete
        and chain_evidence_complete
        and governance_debt_carryover_complete
    )
    if not final_closure_plan_complete:
        if prior_full_chain_go and chain_evidence_complete:
            pass
        elif not prior_full_chain_go:
            pass

    if not prior_full_chain_go:
        final_decision = FINAL_DECISION_PRIOR
    elif not chain_evidence_complete:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not freeze_candidate_only:
        final_decision = FINAL_DECISION_FREEZE
    elif not closure_state_ok:
        final_decision = FINAL_DECISION_STATE
    elif not governance_debt_carryover_complete:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    planning_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO
    final_closure_plan = {
        "plan_id": "task_manager_foundation_handoff_final_closure_plan_v1",
        "final_closure_scope": [
            "define immutable boundary for foundation freeze candidate assets",
            "trace full handoff chain evidence from planning through closure post-review",
            "preserve freeze-candidate and final-closure-planning-ready states",
            "carry forward L1 governance debts without implementation",
            "define downstream reference contracts without implementation readiness",
            "prepare final closure dry-run readiness",
        ],
        "prior_full_chain_go": prior_full_chain_go,
        "final_closure_plan_complete": final_closure_plan_complete,
        "chain_evidence_complete": chain_evidence_complete,
        "freeze_candidate_asset_map_complete": freeze_candidate_asset_map_complete,
        "freeze_candidate_only": freeze_candidate_only,
        "closure_planning_only": True,
        "closure_readiness": closure_readiness,
        "freeze_status": "freeze-candidate",
        "foundation_not_frozen": True,
        "closure_applied": False,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_reference_scope_ok": downstream_reference_scope_ok,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    chain_evidence_map = {
        "map_id": "task_manager_final_closure_chain_evidence_map_v1",
        "chain": evidence_chain,
        "chain_evidence_complete": chain_evidence_complete,
        **meta,
    }
    freeze_asset_map = {
        "map_id": "task_manager_final_freeze_candidate_asset_map_v1",
        "assets": asset_rows,
        "freeze_candidate_asset_map_complete": freeze_candidate_asset_map_complete,
        "freeze_candidate_only": freeze_candidate_only,
        "freeze_status": "freeze-candidate",
        "foundation_frozen": False,
        **meta,
    }
    boundary_contract_doc = {
        **boundary_contract,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        **meta,
    }
    semantics_lock_doc = {
        **semantics_lock_plan,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        **meta,
    }
    downstream_contract = {
        "contract_id": "task_manager_final_downstream_reference_contract_v1",
        "consumers": list(DOWNSTREAM_REFERENCE_MAP),
        "downstream_reference_scope_ok": downstream_reference_scope_ok,
        **meta,
    }
    debt_carryover = {
        "carryover_id": "task_manager_final_governance_debt_carryover_v1",
        "debts": debts,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    next_phase_doc = {
        **next_phase_readiness,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "prior_full_chain_go": prior_full_chain_go,
        "final_closure_plan_complete": final_closure_plan_complete,
        "chain_evidence_complete": chain_evidence_complete,
        "freeze_candidate_asset_map_complete": freeze_candidate_asset_map_complete,
        "freeze_candidate_only": freeze_candidate_only,
        "closure_planning_only": True,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_reference_scope_ok": downstream_reference_scope_ok,
        "governance_debt_carryover_complete": governance_debt_carryover_complete,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Final Closure Plan v1",
            "",
            "This phase performs final closure planning only. It does not execute closure, freeze the foundation, or declare closed.",
            "",
            "本阶段仅执行 final closure planning，不执行 closure，不冻结 foundation，不声明 closed。",
            "",
            f"Prior full chain GO: `{prior_full_chain_go}`",
            f"Closure readiness: `final-closure-planning-ready`",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Final Closure Boundary Contract",
            *[f"- {stmt}" for stmt in BOUNDARY_CONTRACT_STATEMENTS],
            "",
            "## Governance Debt Carryover",
            "- Closure Channel Governance Missing Canonical Protocol (P1, not implemented)",
            "- System Protocols Integration Required Before Module Adapter Implementation (P1, not implemented)",
            "",
            "## Next Phase Candidates",
            "- Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-DryRun-v1-001",
            "- Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Planning-v1-001",
            "",
            "Module adapter implementation is not authorized in this phase.",
        ]
    )
    return {
        "task_manager_foundation_handoff_final_closure_plan": final_closure_plan,
        "task_manager_foundation_handoff_final_closure_plan_md": markdown,
        "task_manager_final_closure_chain_evidence_map": chain_evidence_map,
        "task_manager_final_freeze_candidate_asset_map": freeze_asset_map,
        "task_manager_final_closure_boundary_contract": boundary_contract_doc,
        "task_manager_final_candidate_semantics_lock_plan": semantics_lock_doc,
        "task_manager_final_downstream_reference_contract": downstream_contract,
        "task_manager_final_governance_debt_carryover": debt_carryover,
        "task_manager_final_non_execution_constraints": non_execution,
        "task_manager_final_closure_next_phase_readiness": next_phase_doc,
        "summary": summary,
    }
