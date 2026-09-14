# -*- coding: utf-8 -*-
"""Main Project Structure Migration Governance Debt Register v1.

Register-only: structured登记治理债 from Roadmap Decision Route D signals.
Does not fix debt, release authorization, or execute real rehearsal/migration/batch arming.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    GOVERNANCE_DEBT_CATEGORIES,
)

PHASE_ID = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001"
REGISTER_SCOPE = "main_project_structure_migration_governance_debt_register_only"
REGISTER_ID = "main_proj_struct_migration_governance_debt_register_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_governance_debt_register_v1"

SOURCE_PHASE = (
    "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001"
)
SOURCE_SELECTED_ROUTE = "Route D — Governance Debt Register"
UPSTREAM_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_GOVERNANCE_DEBT_REGISTER"
)

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_READY_FOR_POST_REGISTER_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001"

_EVAL_ROOT = "_eval_out"

SOURCE_PHASE_SPECS: List[Tuple[str, str, List[str]]] = [
    (
        "Execution Planning",
        f"{_EVAL_ROOT}/main_project_structure_migration_rollback_rehearsal_execution_planning_v1_smoke_v0",
        ["permission_semantics_debt", "boundary_object_debt", "terminology_debt"],
    ),
    (
        "Execution DryRun",
        f"{_EVAL_ROOT}/main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1_smoke_v0",
        ["permission_semantics_debt", "success_claim_debt", "evidence_chain_debt"],
    ),
    (
        "Execution Post-DryRun Review",
        f"{_EVAL_ROOT}/main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_v1_smoke_v0",
        ["success_claim_debt", "terminology_debt", "boundary_object_debt"],
    ),
    (
        "Execution Roadmap Decision",
        f"{_EVAL_ROOT}/main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1_smoke_v0",
        ["permission_semantics_debt", "terminology_debt"],
    ),
    (
        "Pre-Authorization Planning",
        f"{_EVAL_ROOT}/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1_smoke_v0",
        ["owner_operator_debt", "permission_semantics_debt", "evidence_chain_debt"],
    ),
    (
        "Pre-Authorization DryRun",
        f"{_EVAL_ROOT}/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1_smoke_v0",
        ["permission_semantics_debt", "success_claim_debt", "terminology_debt"],
    ),
    (
        "Pre-Authorization Post-DryRun Review",
        f"{_EVAL_ROOT}/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1_smoke_v0",
        ["terminology_debt", "success_claim_debt", "owner_operator_debt"],
    ),
    (
        "Pre-Authorization Roadmap Decision",
        f"{_EVAL_ROOT}/main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1_smoke_v0",
        [
            "permission_semantics_debt",
            "boundary_object_debt",
            "evidence_chain_debt",
            "success_claim_debt",
            "owner_operator_debt",
            "test_harness_debt",
            "documentation_sync_debt",
            "terminology_debt",
            "automation_candidate_debt",
        ],
    ),
]

DEBT_SPECS: List[Dict[str, Any]] = [
    {
        "debt_id": "GD-01",
        "debt_type": "permission_semantics_debt",
        "title": "Permission / authorization / execution field semantics unclear",
        "description": "Planning, dry-run, review, and roadmap language can be misread as granted authorization or executable permission.",
        "risk_level": "P0",
        "severity": "critical",
        "likelihood": "high",
        "blast_radius": "all_real_execution_gates",
        "owner_domain": "governance",
        "candidate_future_phase": "Phase-Permission-Semantics-Canonicalization-v1-001",
        "blocks_real_rehearsal": True,
        "blocks_real_migration": True,
        "blocks_batch_arming": True,
    },
    {
        "debt_id": "GD-02",
        "debt_type": "boundary_object_debt",
        "title": "Boundary objects not fully registered and verifier-enforced",
        "description": "Protected assets, HR, DnAE, eval_out, verdict table, handoff objects rely on implicit convention.",
        "risk_level": "P0",
        "severity": "high",
        "likelihood": "medium",
        "blast_radius": "protected_scope_and_file_ops",
        "owner_domain": "governance",
        "candidate_future_phase": "Phase-Boundary-Object-Registry-Planning-v1-001",
        "blocks_real_rehearsal": True,
        "blocks_real_migration": True,
        "blocks_batch_arming": True,
    },
    {
        "debt_id": "GD-03",
        "debt_type": "evidence_chain_debt",
        "title": "Evidence lifecycle and usability gates incomplete",
        "description": "Candidate, dry-run, review, runtime, success-claim, and audit evidence layers not unified.",
        "risk_level": "P1",
        "severity": "high",
        "likelihood": "medium",
        "blast_radius": "success_claim_and_rollback_audit",
        "owner_domain": "governance",
        "candidate_future_phase": "Phase-Evidence-Chain-Governance-Planning-v1-001",
        "blocks_real_rehearsal": True,
        "blocks_real_migration": True,
        "blocks_batch_arming": True,
    },
    {
        "debt_id": "GD-04",
        "debt_type": "success_claim_debt",
        "title": "Verifier GO conflated with real success claim",
        "description": "Phase GO can be misread as rollback/migration success without independent success claim gate.",
        "risk_level": "P0",
        "severity": "critical",
        "likelihood": "high",
        "blast_radius": "rollback_and_migration_claims",
        "owner_domain": "governance",
        "candidate_future_phase": "Phase-Success-Claim-Gate-Canonicalization-v1-001",
        "blocks_real_rehearsal": True,
        "blocks_real_migration": True,
        "blocks_batch_arming": True,
    },
    {
        "debt_id": "GD-05",
        "debt_type": "owner_operator_debt",
        "title": "Owner/operator approval protocol not formalized",
        "description": "Owner approval, operator acknowledgement, execution window, abort authority lack unified structured protocol.",
        "risk_level": "P0",
        "severity": "critical",
        "likelihood": "high",
        "blast_radius": "real_authorization_chain",
        "owner_domain": "governance",
        "candidate_future_phase": "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001",
        "blocks_real_rehearsal": True,
        "blocks_real_migration": True,
        "blocks_batch_arming": True,
    },
    {
        "debt_id": "GD-06",
        "debt_type": "test_harness_debt",
        "title": "Test harness and verifier rerun execution chain incomplete",
        "description": "Verifier rerun and migration test suite planned but real execution authorization chain missing.",
        "risk_level": "P1",
        "severity": "medium",
        "likelihood": "medium",
        "blast_radius": "test_and_verifier_execution",
        "owner_domain": "engineering",
        "candidate_future_phase": "Phase-Migration-Test-Harness-Authorization-Planning-v1-001",
        "blocks_real_rehearsal": True,
        "blocks_real_migration": True,
        "blocks_batch_arming": False,
    },
    {
        "debt_id": "GD-07",
        "debt_type": "documentation_sync_debt",
        "title": "Documentation sync relies on manual updates",
        "description": "README, phase verdict table, Implementation Status, downstream handoff prone to drift and omission.",
        "risk_level": "P1",
        "severity": "medium",
        "likelihood": "high",
        "blast_radius": "phase_admission_and_handoff",
        "owner_domain": "engineering",
        "candidate_future_phase": "Phase-Documentation-Sync-Automation-Planning-v1-001",
        "blocks_real_rehearsal": False,
        "blocks_real_migration": False,
        "blocks_batch_arming": False,
    },
    {
        "debt_id": "GD-08",
        "debt_type": "terminology_debt",
        "title": "High-risk terminology lacks canonical table enforcement",
        "description": "planning/allowed/ready/GO/granted/success used inconsistently across phases.",
        "risk_level": "P0",
        "severity": "critical",
        "likelihood": "high",
        "blast_radius": "all_governance_phases",
        "owner_domain": "governance",
        "candidate_future_phase": "Phase-Terminology-Canonical-Table-v1-001",
        "blocks_real_rehearsal": True,
        "blocks_real_migration": True,
        "blocks_batch_arming": True,
    },
    {
        "debt_id": "GD-09",
        "debt_type": "automation_candidate_debt",
        "title": "Governance automation candidates not authorized or implemented",
        "description": "Phase registry, verdict table, doc sync, boundary checks remain manual with automation only as candidate.",
        "risk_level": "P1",
        "severity": "medium",
        "likelihood": "medium",
        "blast_radius": "governance_maintenance",
        "owner_domain": "engineering",
        "candidate_future_phase": "Phase-Governance-Automation-Candidate-Planning-v1-001",
        "blocks_real_rehearsal": False,
        "blocks_real_migration": False,
        "blocks_batch_arming": False,
    },
]

FUTURE_PHASE_SPECS: List[Dict[str, Any]] = [
    {
        "future_phase_name": "Phase-Permission-Semantics-Canonicalization-v1-001",
        "target_debt_types": ["permission_semantics_debt"],
        "priority": "P0",
    },
    {
        "future_phase_name": "Phase-Boundary-Object-Registry-Planning-v1-001",
        "target_debt_types": ["boundary_object_debt"],
        "priority": "P0",
    },
    {
        "future_phase_name": "Phase-Evidence-Chain-Governance-Planning-v1-001",
        "target_debt_types": ["evidence_chain_debt"],
        "priority": "P1",
    },
    {
        "future_phase_name": "Phase-Success-Claim-Gate-Canonicalization-v1-001",
        "target_debt_types": ["success_claim_debt"],
        "priority": "P0",
    },
    {
        "future_phase_name": "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001",
        "target_debt_types": ["owner_operator_debt"],
        "priority": "P0",
    },
    {
        "future_phase_name": "Phase-Migration-Test-Harness-Authorization-Planning-v1-001",
        "target_debt_types": ["test_harness_debt"],
        "priority": "P1",
    },
    {
        "future_phase_name": "Phase-Documentation-Sync-Automation-Planning-v1-001",
        "target_debt_types": ["documentation_sync_debt"],
        "priority": "P1",
    },
    {
        "future_phase_name": "Phase-Terminology-Canonical-Table-v1-001",
        "target_debt_types": ["terminology_debt"],
        "priority": "P0",
    },
    {
        "future_phase_name": "Phase-Governance-Automation-Candidate-Planning-v1-001",
        "target_debt_types": ["automation_candidate_debt"],
        "priority": "P1",
    },
]

TERMINOLOGY_SPECS: List[Tuple[str, str, str, str, str]] = [
    ("planning", "Structured design of policies/matrices without execution", "authorization granted or execution allowed", "planning_only=true", "does not imply execution"),
    ("dry-run", "Simulated evaluation of artifacts without real side effects", "real operation completed", "dryrun_only=true", "does not imply success or authorization"),
    ("review", "Read-only audit of upstream artifacts and boundaries", "permission release or fix applied", "review_only=true", "does not imply execution"),
    ("roadmap decision", "Route selection for next governance phase only", "authorization or execution release", "roadmap_decision_only=true", "does not imply sandbox/branch/restore"),
    ("authorization planning", "Planning how authorization would be requested", "authorization granted", "authorization_granted_now=false", "does not imply owner approval"),
    ("authorization granted", "Explicit owner/operator authorization recorded now", "verifier GO or route selected", "authorization_granted_now=true", "must not be inferred from planning"),
    ("owner approval", "Owner explicit approval for scoped real action", "developer ran script", "owner_approval_granted_now=true", "does not imply execution committed"),
    ("operator acknowledgement", "Operator ack of scope and boundaries", "automatic on GO", "operator_acknowledgement_granted_now=true", "does not replace owner approval"),
    ("execution window", "Time-bounded window for authorized execution", "always open after planning", "execution_window_opened_now=true", "does not imply rehearsal success"),
    ("allowed", "Permitted for scoped phase type (planning/dry-run/register)", "real execution authorized", "real_*_allowed fields", "register allowed ≠ execution allowed"),
    ("committed", "Real side effect committed in scope", "dry-run or review passed", "execution_committed=true", "does not apply to register-only phases"),
    ("generated", "Artifact physically produced in authorized scope", "candidate named in planning", "evidence_generated_now=true", "candidate ≠ generated"),
    ("evidence candidate", "Planned or simulated evidence placeholder", "runtime evidence or success evidence", "evidence_candidate_only=true", "cannot support success claim"),
    ("runtime evidence", "Evidence from authorized runtime execution", "dry-run matrix or review pass", "not_runtime_evidence=false when real", "requires authorization"),
    ("success claim", "Explicit claim of real-world success", "verifier GO or review pass", "success_claim_allowed=false until gate", "independent from phase GO"),
    ("GO", "Phase-scoped verifier checks passed", "real success or authorization", "verifier=GO in report", "does not imply execution or success claim"),
    ("ready", "Ready for named next phase type", "ready for real execution", "ready_for_* fields disambiguated", "ready for register ≠ ready for rehearsal"),
    ("selected route", "Chosen next governance route", "permissions released for route", "selected_route field", "Route D register ≠ authorization"),
    ("blocked route", "Route explicitly forbidden now", "can be skipped by final decision", "blocked_now=true", "must not appear in final decision as executable"),
    ("deferred route", "Route postponed; not selected now", "forbidden forever", "deferred=true", "may become eligible after debt handling"),
]

AUTOMATION_SPECS: List[Tuple[str, str, str, str, str, str]] = [
    ("AC-01", "phase registry auto update", "phase registry maintenance", "high", "unauthorized phase state mutation", "Phase-Governance-Automation-Candidate-Planning-v1-001"),
    ("AC-02", "phase verdict table auto update", "verdict table sync", "high", "incorrect GO recorded without verifier", "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("AC-03", "README status auto sync", "architecture/evaluation README", "medium", "stale or wrong links", "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("AC-04", "downstream handoff checker", "handoff consistency", "high", "missed non-claims", "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("AC-05", "implementation status checker", "upstream Implementation Status", "medium", "false completion signal", "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("AC-06", "boundary matrix generator", "boundary freeze matrices", "high", "auto-generated wrong boundaries", "Phase-Boundary-Object-Registry-Planning-v1-001"),
    ("AC-07", "non-claims generator", "non-claims registers", "medium", "generic non-claims omit scope", "Phase-Governance-Automation-Candidate-Planning-v1-001"),
    ("AC-08", "terminology review generator", "terminology review artifacts", "high", "false pass on terminology", "Phase-Terminology-Canonical-Table-v1-001"),
    ("AC-09", "permission non-release checker", "authorization matrices", "critical", "silent permission release", "Phase-Permission-Semantics-Canonicalization-v1-001"),
    ("AC-10", "evidence usability checker", "evidence chain gates", "high", "candidate used as success evidence", "Phase-Evidence-Chain-Governance-Planning-v1-001"),
    ("AC-11", "output directory consistency checker", "eval_out layout", "medium", "wrong upstream consumed", "Phase-Governance-Automation-Candidate-Planning-v1-001"),
    ("AC-12", "verifier report aggregation", "verifier_report.json rollup", "medium", "aggregated GO misread as chain success", "Phase-Migration-Test-Harness-Authorization-Planning-v1-001"),
]

DOC_SYNC_AREAS: List[Tuple[str, str, str, str, bool]] = [
    ("architecture README", "manual omission of new governance docs", "PhaseVerdictTableUpdateCheck", True, "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("evaluation README", "eval index drift", "DocumentationSyncMatrix", True, "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("phase verdict table", "verdict row missing or stale", "PhaseVerdictTableUpdateCheck", True, "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("governance docs", "Implementation Status not updated", "ImplementationStatusUpdateMatrix", True, "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("evaluation docs", "smoke result not recorded", "DocumentationSyncMatrix", True, "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("GO / NO-GO pack", "GO criteria drift from verifier", "DownstreamHandoffUpdateMatrix", True, "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("upstream Implementation Status", "downstream not reflected", "ImplementationStatusUpdateMatrix", True, "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("downstream handoff", "handoff omits non-claims", "DownstreamHandoffUpdateMatrix", True, "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("output directory references", "wrong _eval_out path in docs", "output directory consistency checker", True, "Phase-Governance-Automation-Candidate-Planning-v1-001"),
]

VERIFIER_ADDITION_SPECS: List[Tuple[str, str, str, str, str]] = [
    ("VA-01", "phase type flags check", "planning,dryrun,review,roadmap,register", "phase flag vs final_decision", "mismatch → NO-GO", "P0"),
    ("VA-02", "authorization non-release check", "all non-execution phases", "authorization_granted_now=true", "must stay false", "P0"),
    ("VA-03", "execution non-commit check", "all non-execution phases", "execution_committed=true", "must stay false", "P0"),
    ("VA-04", "selected route permission impact check", "roadmap_decision", "permission_release=true on selected route", "must stay false", "P0"),
    ("VA-05", "success claim gate check", "rollback,migration,execution", "success_claim_allowed=true without gate", "blocked until canonical gate", "P0"),
    ("VA-06", "terminology review check", "review,roadmap,register", "terminology review fail", "NO-GO", "P0"),
    ("VA-07", "boundary object registry check", "migration,rollback,register", "missing boundary matrix", "NO-GO for migration phases", "P0"),
    ("VA-08", "evidence usability check", "dryrun,review,rehearsal", "candidate evidence supports success claim", "must reject", "P0"),
    ("VA-09", "owner/operator approval check", "authorization,execution", "owner_approval without protocol", "NO-GO", "P0"),
    ("VA-10", "execution window check", "execution", "execution_window_opened without authorization", "NO-GO", "P0"),
    ("VA-11", "documentation sync check", "all governance phases", "doc sync not declared", "warn or NO-GO per phase", "P1"),
    ("VA-12", "subprocess/runtime/file operation check", "non-execution phases", "subprocess/runtime/file op true", "NO-GO", "P0"),
]

BLOCKED_RULE_SPECS: List[Tuple[str, str, str, str, str]] = [
    ("BR-01", "permission_semantics_debt", "real execution", "permission semantics canonicalized", "Phase-Permission-Semantics-Canonicalization-v1-001"),
    ("BR-02", "terminology_debt", "owner/operator approval request", "terminology canonical table enforced", "Phase-Terminology-Canonical-Table-v1-001"),
    ("BR-03", "success_claim_debt", "success claim", "success claim gate canonicalized", "Phase-Success-Claim-Gate-Canonicalization-v1-001"),
    ("BR-04", "owner_operator_debt", "execution window open", "owner/operator protocol planned and authorized", "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001"),
    ("BR-05", "boundary_object_debt", "file operation", "boundary object registry planned", "Phase-Boundary-Object-Registry-Planning-v1-001"),
    ("BR-06", "evidence_chain_debt", "evidence for success claim", "evidence chain governance planned", "Phase-Evidence-Chain-Governance-Planning-v1-001"),
    ("BR-07", "test_harness_debt", "verifier suite rerun", "test harness authorization planned", "Phase-Migration-Test-Harness-Authorization-Planning-v1-001"),
    ("BR-08", "documentation_sync_debt", "manual doc state as sole admission", "documentation sync automation planned", "Phase-Documentation-Sync-Automation-Planning-v1-001"),
    ("BR-09", "automation_candidate_debt", "automatic phase progression", "automation candidate planning completed", "Phase-Governance-Automation-Candidate-Planning-v1-001"),
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _register_meta() -> Dict[str, Any]:
    return {
        "governance_debt_register_only": True,
        "register_only": True,
        "fix_executed_now": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(path_str: Optional[str], artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in artifacts:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
    loaded = summary is not None and not missing
    return {"root": root, "loaded": loaded, "summary": summary or {}, "artifacts": art, "missing": missing}


def run_main_project_structure_migration_governance_debt_register_v1(
    *,
    pre_authorization_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream_artifacts = [
        "real_rollback_rehearsal_pre_authorization_roadmap_decision_policy_v1.json",
        "completed_pre_authorization_chain_review_v1.json",
        "pre_authorization_roadmap_route_candidate_matrix_v1.json",
        "governance_debt_signal_matrix_v1.json",
        "route_dependency_and_blocker_matrix_v1.json",
        "selected_pre_authorization_roadmap_route_decision_v1.json",
        "permission_authorization_non_release_matrix_v1.json",
        "pre_authorization_roadmap_decision_non_claims_register_v1.json",
        "real_rollback_rehearsal_pre_authorization_roadmap_readiness_decision_v1.json",
        "summary.json",
        "verifier_report.json",
    ]
    upstream = _load_upstream(pre_authorization_roadmap_decision_root, upstream_artifacts)
    up_summary = upstream["summary"]
    up_art = upstream["artifacts"]
    up_verifier = up_art.get("verifier_report.json") or {}
    up_readiness = up_art.get("real_rollback_rehearsal_pre_authorization_roadmap_readiness_decision_v1.json") or {}
    up_signals = up_art.get("governance_debt_signal_matrix_v1.json") or {}
    up_routes = up_art.get("pre_authorization_roadmap_route_candidate_matrix_v1.json") or {}

    upstream_go = up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True
    upstream_boundary_ok = up_summary.get("boundary_ok") is True
    upstream_route = up_summary.get("selected_route") == SOURCE_SELECTED_ROUTE
    upstream_ready = up_readiness.get("ready_for_governance_debt_register") is True
    upstream_final_ok = up_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL
    route_g = next((r for r in (up_routes.get("routes") or []) if r.get("route_id") == "G"), {})
    route_g_blocked = route_g.get("blocked_now") is True or up_summary.get("route_g_blocked_now") is True

    upstream_flags_ok = (
        up_summary.get("authorization_granted_now") is False
        and up_summary.get("owner_approval_granted_now") is False
        and up_summary.get("operator_acknowledgement_granted_now") is False
        and up_summary.get("execution_window_opened_now") is False
        and up_summary.get("real_rehearsal_execution_allowed") is False
        and up_summary.get("real_migration_execution_allowed") is False
        and up_summary.get("batch_arming_allowed") is False
    )

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append("upstream_roadmap_decision_missing_or_incomplete")
    if not upstream_go:
        blockers.append("upstream_roadmap_decision_verifier_not_go")
    if not upstream_boundary_ok:
        blockers.append("upstream_roadmap_decision_boundary_not_ok")
    if not upstream_route:
        blockers.append("upstream_route_d_not_selected")
    if not upstream_ready:
        blockers.append("upstream_ready_for_governance_debt_register_not_true")
    if not upstream_final_ok:
        blockers.append("upstream_final_decision_mismatch")
    if not upstream_flags_ok:
        blockers.append("upstream_permission_flags_not_frozen")
    if not route_g_blocked:
        blockers.append("upstream_route_g_not_blocked")

    boundary_ok = not blockers

    governance_debt_register_policy = {
        "phase_name": PHASE_ID,
        "register_id": REGISTER_ID,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_phase": SOURCE_PHASE,
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_selected_route_observed": SOURCE_SELECTED_ROUTE if upstream_route else up_summary.get("selected_route"),
        "source_ready_for_governance_debt_register_observed": upstream_ready,
        **_register_meta(),
    }

    signal_by_type = {r.get("debt_type"): r for r in (up_signals.get("rows") or [])}
    debt_rows: List[Dict[str, Any]] = []
    for spec in DEBT_SPECS:
        sig = signal_by_type.get(spec["debt_type"], {})
        debt_rows.append(
            {
                "debt_id": spec["debt_id"],
                "debt_type": spec["debt_type"],
                "title": spec["title"],
                "description": spec["description"],
                "observed_during_migration": True,
                "source_phase_refs": sig.get("source_phase_refs")
                or [SOURCE_PHASE, "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001"],
                "source_artifact_refs": [
                    "governance_debt_signal_matrix_v1.json",
                    "migration_governance_development_constraints_v1_manifest.json",
                ],
                "risk_level": spec["risk_level"],
                "risk_description": sig.get("risk_description") or spec["description"],
                "impact_scope": spec["blast_radius"],
                "blocks_real_rehearsal": spec["blocks_real_rehearsal"],
                "blocks_real_migration": spec["blocks_real_migration"],
                "blocks_batch_arming": spec["blocks_batch_arming"],
                "recommended_priority": spec["risk_level"],
                "owner_domain": spec["owner_domain"],
                "candidate_future_phase": spec["candidate_future_phase"],
                "fix_executed_now": False,
                "register_status": "registered",
                **_register_meta(),
            }
        )
    governance_debt_register = {
        "rows": debt_rows,
        "row_count": len(debt_rows),
        "debt_category_count": len(debt_rows),
        **_register_meta(),
    }

    severity_rows: List[Dict[str, Any]] = []
    for spec in DEBT_SPECS:
        severity_rows.append(
            {
                "debt_id": spec["debt_id"],
                "debt_type": spec["debt_type"],
                "severity": spec["severity"],
                "likelihood": spec["likelihood"],
                "blast_radius": spec["blast_radius"],
                "execution_risk": spec["severity"] in ("critical", "high") and spec["blocks_real_rehearsal"],
                "misinterpretation_risk": spec["debt_type"] in ("permission_semantics_debt", "terminology_debt", "success_claim_debt"),
                "automation_risk": spec["debt_type"] in ("automation_candidate_debt", "documentation_sync_debt"),
                "documentation_drift_risk": spec["debt_type"] in ("documentation_sync_debt", "terminology_debt"),
                "recommended_priority": spec["risk_level"],
                "blocks_progression_level": "hard" if spec["blocks_real_rehearsal"] else "soft",
                **_register_meta(),
            }
        )
    governance_debt_severity_matrix = {
        "rows": severity_rows,
        "row_count": len(severity_rows),
        "p0_or_critical_high_count": sum(
            1 for s in DEBT_SPECS if s["risk_level"] == "P0" or s["severity"] in ("critical", "high")
        ),
        **_register_meta(),
    }

    source_phase_rows: List[Dict[str, Any]] = []
    for phase_label, out_dir, debt_types in SOURCE_PHASE_SPECS:
        source_phase_rows.append(
            {
                "source_phase": phase_label,
                "source_output_dir": out_dir,
                "observed_debt_types": debt_types,
                "source_artifact_refs": ["summary.json", "verifier_report.json"],
                "signal_summary": f"Observed {len(debt_types)} debt signal categories during {phase_label}",
                "register_entries_created": [d for d in debt_types if d in GOVERNANCE_DEBT_CATEGORIES],
                "downstream_risk": "misinterpretation of phase GO as execution authorization" if "terminology_debt" in debt_types else "boundary or evidence drift",
                **_register_meta(),
            }
        )
    governance_debt_source_phase_mapping = {
        "rows": source_phase_rows,
        "row_count": len(source_phase_rows),
        **_register_meta(),
    }

    blocked_rows: List[Dict[str, Any]] = []
    for rule_id, debt_type, blocked_action, blocked_until, future in BLOCKED_RULE_SPECS:
        spec = next(s for s in DEBT_SPECS if s["debt_type"] == debt_type)
        blocked_rows.append(
            {
                "rule_id": rule_id,
                "debt_type": debt_type,
                "blocked_action": blocked_action,
                "blocked_until": blocked_until,
                "blocking_reason": f"{debt_type} registered but not remediated; fix_executed_now=false",
                "required_future_phase": future,
                "enforcement_level": "hard" if spec["blocks_real_rehearsal"] else "advisory",
                "applies_to_real_rehearsal": spec["blocks_real_rehearsal"],
                "applies_to_real_migration": spec["blocks_real_migration"],
                "applies_to_batch_arming": spec["blocks_batch_arming"],
                **_register_meta(),
            }
        )
    governance_debt_blocked_progression_rules = {
        "rows": blocked_rows,
        "row_count": len(blocked_rows),
        **_register_meta(),
    }

    future_rows: List[Dict[str, Any]] = []
    for fp in FUTURE_PHASE_SPECS:
        future_rows.append(
            {
                "future_phase_name": fp["future_phase_name"],
                "target_debt_types": fp["target_debt_types"],
                "priority": fp["priority"],
                "entry_condition": "governance debt register completed; post-register review GO",
                "expected_outputs": ["planning artifacts", "verifier checks", "non-claims"],
                "blocked_actions_released_if_completed": [],
                "not_authorization_phase": True,
                **_register_meta(),
            }
        )
    governance_debt_future_phase_mapping = {
        "rows": future_rows,
        "row_count": len(future_rows),
        **_register_meta(),
    }

    verifier_rows: List[Dict[str, Any]] = []
    for vid, check_name, target_types, req_fields, expected, priority in VERIFIER_ADDITION_SPECS:
        verifier_rows.append(
            {
                "verifier_addition_id": vid,
                "check_name": check_name,
                "target_phase_types": target_types,
                "required_fields": req_fields,
                "failure_condition": req_fields.split("→")[-1].strip() if "→" in req_fields else req_fields,
                "expected_result": expected,
                "priority": priority,
                **_register_meta(),
            }
        )
    governance_debt_verifier_addition_plan = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        **_register_meta(),
    }

    doc_sync_rows: List[Dict[str, Any]] = []
    for area, risk, check, auto, future in DOC_SYNC_AREAS:
        doc_sync_rows.append(
            {
                "doc_sync_area": area,
                "current_risk": risk,
                "required_future_check": check,
                "automation_candidate": auto,
                "manual_review_required": True,
                "fix_executed_now": False,
                "candidate_future_phase": future,
                **_register_meta(),
            }
        )
    governance_debt_documentation_sync_improvement_plan = {
        "rows": doc_sync_rows,
        "row_count": len(doc_sync_rows),
        **_register_meta(),
    }

    term_rows: List[Dict[str, Any]] = []
    for term, meaning, forbidden, fields, must_not in TERMINOLOGY_SPECS:
        term_rows.append(
            {
                "term": term,
                "canonical_meaning": meaning,
                "forbidden_interpretation": forbidden,
                "required_fields": fields,
                "must_not_imply": must_not,
                "example_safe_usage": f"{term} in this phase means {meaning.split('.')[0].lower()}",
                "verifier_check_required": True,
                **_register_meta(),
            }
        )
    governance_debt_terminology_canonical_table = {
        "rows": term_rows,
        "row_count": len(term_rows),
        **_register_meta(),
    }

    auto_rows: List[Dict[str, Any]] = []
    for aid, name, process, value, risk, future in AUTOMATION_SPECS:
        auto_rows.append(
            {
                "automation_candidate_id": aid,
                "candidate_name": name,
                "target_process": process,
                "automation_value": value,
                "risk_if_automated": risk,
                "requires_human_review": True,
                "recommended_priority": "P0" if value == "critical" else "P1",
                "not_implemented_now": True,
                "candidate_future_phase": future,
                **_register_meta(),
            }
        )
    governance_debt_automation_candidate_matrix = {
        "rows": auto_rows,
        "row_count": len(auto_rows),
        **_register_meta(),
    }

    ready = boundary_ok
    governance_debt_register_readiness_decision = {
        "ready_for_post_register_review": bool(ready),
        "ready_for_debt_fix_execution": False,
        "ready_for_real_pre_authorization_request": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "governance_debt_register_completed": bool(ready),
        "debt_register_generated": True,
        "severity_matrix_generated": True,
        "source_phase_mapping_generated": True,
        "blocked_progression_rules_generated": True,
        "future_phase_mapping_generated": True,
        "verifier_addition_plan_generated": True,
        "documentation_sync_improvement_plan_generated": True,
        "terminology_canonical_table_generated": True,
        "automation_candidate_matrix_generated": True,
        "fix_executed_now": False,
        "final_decision": FINAL_DECISION if ready else "GOVERNANCE_DEBT_REGISTER_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready else PHASE_ID,
        **_register_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "register_scope": REGISTER_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "pre_authorization_roadmap_decision_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_selected_route_observed": SOURCE_SELECTED_ROUTE if upstream_route else up_summary.get("selected_route"),
        "source_ready_for_governance_debt_register_observed": upstream_ready,
        "debt_category_count": len(debt_rows),
        "severity_matrix_row_count": len(severity_rows),
        "source_phase_mapping_count": len(source_phase_rows),
        "blocked_progression_rule_count": len(blocked_rows),
        "future_phase_mapping_count": len(future_rows),
        "verifier_addition_count": len(verifier_rows),
        "documentation_sync_plan_count": len(doc_sync_rows),
        "terminology_entry_count": len(term_rows),
        "automation_candidate_count": len(auto_rows),
        "p0_or_critical_high_debt_count": governance_debt_severity_matrix["p0_or_critical_high_count"],
        "route_g_blocked_observed": route_g_blocked,
        "boundary_ok": bool(boundary_ok),
        "violations": blockers,
        "final_decision": FINAL_DECISION if ready else "GOVERNANCE_DEBT_REGISTER_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready else PHASE_ID,
        **_register_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "pre_authorization_roadmap_decision",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                **_register_meta(),
            }
        ],
        "row_count": 1,
        **_register_meta(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready else PHASE_ID,
        "final_decision": FINAL_DECISION if ready else "GOVERNANCE_DEBT_REGISTER_REQUIRES_FIXES",
        "reason": "register only; post-register review next; no debt fix or authorization",
        **_register_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "governance_debt_register_policy": governance_debt_register_policy,
        "governance_debt_register": governance_debt_register,
        "governance_debt_severity_matrix": governance_debt_severity_matrix,
        "governance_debt_source_phase_mapping": governance_debt_source_phase_mapping,
        "governance_debt_blocked_progression_rules": governance_debt_blocked_progression_rules,
        "governance_debt_future_phase_mapping": governance_debt_future_phase_mapping,
        "governance_debt_verifier_addition_plan": governance_debt_verifier_addition_plan,
        "governance_debt_documentation_sync_improvement_plan": governance_debt_documentation_sync_improvement_plan,
        "governance_debt_terminology_canonical_table": governance_debt_terminology_canonical_table,
        "governance_debt_automation_candidate_matrix": governance_debt_automation_candidate_matrix,
        "governance_debt_register_readiness_decision": governance_debt_register_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
