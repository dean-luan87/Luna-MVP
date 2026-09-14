#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_dryrun_v1 import (
    CHAIN_TRACE_NODES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_planning_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
    CHAIN_EVIDENCE_NODES,
    DEFAULT_FREEZE_AUTH_POST_REVIEW_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_EXECUTION_CONSTRAINTS,
    PHASE_ID,
    POST_REVIEW_TRUE_KEYS,
    PREREQUISITE_ROWS,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_plan_v1.md",
    "task_manager_freeze_authorization_grant_scope_matrix_v1.json",
    "task_manager_freeze_authorization_grant_candidate_asset_map_v1.json",
    "task_manager_freeze_authorization_grant_prerequisite_matrix_v1.json",
    "task_manager_freeze_authorization_grant_evidence_chain_v1.json",
    "task_manager_freeze_authorization_grant_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_next_phase_readiness_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "prior_freeze_authorization_post_review_go",
    "grant_plan_complete",
    "grant_scope_planning_only",
    "grant_candidate_only",
    "grant_not_issued",
    "authorization_request_absent",
    "authorization_grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_carryover_complete",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
)
RUNTIME_FORBIDDEN: Tuple[str, ...] = (
    "runtime_executor_created_now",
    "scheduler_binding_created_now",
    "task_execution_authority_granted_now",
    "output_authorization_granted_now",
    "module_adapter_integration_created_now",
    "information_channel_governance_implemented_now",
    "protocol_governance_implemented_now",
    "closure_channel_governance_implemented_now",
    "system_protocols_integration_implemented_now",
    "authorization_grant_created_now",
    "grant_token_created_now",
    "grant_record_created_now",
    "owner_approval_record_created_now",
    "freeze_execution_path_created_now",
    "rollback_execution_path_created_now",
)
FORBIDDEN_NEXT_TARGETS: Tuple[str, ...] = (
    "grant_issued",
    "foundation_frozen",
    "closed",
    "module_adapter_implementation",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--freeze-authorization-post-review-root", default=DEFAULT_FREEZE_AUTH_POST_REVIEW_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    post_review = Path(args.freeze_authorization_post_review_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    post_summary = _read(post_review / "summary.json")
    post_verifier = _read(post_review / "verifier_report.json")
    _add(checks, "prior.summary_go", post_summary.get("final_decision") == POST_REVIEW_FINAL_GO)
    _add(checks, "prior.verifier_go", post_verifier.get("verifier") == "GO")
    _add(checks, "prior.passed_min", int(post_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.failed_zero", post_verifier.get("failed_checks") == 0)
    _add(checks, "prior.blocker_zero", post_verifier.get("blocker_count") == 0)
    _add(checks, "prior.grant_planning_ready", post_summary.get("grant_planning_ready") is True)
    for key in POST_REVIEW_TRUE_KEYS:
        _add(checks, f"prior.summary.{key}", post_summary.get(key) is True)
        if key in post_verifier:
            _add(checks, f"prior.verifier.{key}", post_verifier.get(key) is True)

    plan = docs["task_manager_foundation_handoff_freeze_authorization_grant_plan_v1.json"]
    scope = docs["task_manager_freeze_authorization_grant_scope_matrix_v1.json"]
    asset_map = docs["task_manager_freeze_authorization_grant_candidate_asset_map_v1.json"]
    prerequisites = docs["task_manager_freeze_authorization_grant_prerequisite_matrix_v1.json"]
    evidence = docs["task_manager_freeze_authorization_grant_evidence_chain_v1.json"]
    boundary = docs["task_manager_freeze_authorization_grant_boundary_contract_v1.json"]
    constraints = docs["task_manager_freeze_authorization_grant_non_execution_constraints_v1.json"]
    debt_carryover = docs["task_manager_freeze_authorization_grant_governance_debt_carryover_v1.json"]
    next_phase = docs["task_manager_freeze_authorization_grant_next_phase_readiness_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.grant_planning_only.{doc_name}", doc.get("grant_planning_only") in (None, True))
        _add(checks, f"meta.grant_not_issued.{doc_name}", doc.get("grant_not_issued") in (None, True))
        _add(checks, f"meta.auth_request_absent.{doc_name}", doc.get("authorization_request_absent") in (None, True))
        _add(checks, f"meta.auth_grant_absent.{doc_name}", doc.get("authorization_grant_absent") in (None, True))
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.closure_not_executed.{doc_name}", doc.get("closure_not_executed") in (None, True))
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in TRUE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"plan.{key}", plan.get(key) is True)

    _add(checks, "scope.planning_only", scope.get("grant_scope_planning_only") is True)
    for row in scope.get("rows") or []:
        s = row.get("scope")
        _add(checks, f"scope.row.{s}.planning", row.get("classification") == "grant-planning-scope")
        _add(checks, f"scope.row.{s}.not_issued", row.get("classification") != "grant-issued-scope")
        _add(checks, f"scope.row.{s}.not_authorized", row.get("classification") != "authorized-scope")

    _add(checks, "asset.candidate_only", asset_map.get("grant_candidate_only") is True)
    for row in asset_map.get("assets") or []:
        path = row.get("path", row.get("file", "unknown"))
        label = str(path).split("/")[-1][:40]
        _add(checks, f"asset.grant_status.{label}", row.get("grant_status") == "freeze-authorization-grant-candidate")
        _add(checks, f"asset.auth_status.{label}", row.get("authorization_status") == "freeze-authorization-grant-candidate")
        _add(checks, f"asset.not_authorized.{label}", row.get("grant_status") != "freeze-authorized")
        _add(checks, f"asset.not_frozen.{label}", row.get("freeze_status") != "frozen")

    _add(checks, "prereq.ok", prerequisites.get("prerequisites_ok") is True)
    for req_row in PREREQUISITE_ROWS:
        prereq = req_row["prerequisite"]
        row = next((r for r in prerequisites.get("rows") or [] if r.get("prerequisite") == prereq), {})
        _add(checks, f"prereq.{prereq}.required", row.get("required") is True)
        _add(checks, f"prereq.{prereq}.satisfied", row.get("satisfied") is True)

    _add(checks, "evidence.complete", evidence.get("evidence_chain_complete") is True)
    _add(checks, "evidence.not_issued", evidence.get("points_to_grant_planning_not_issued") is True)
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in evidence.get("chain") or [] if r.get("stage") == stage), {})
        _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
    for stage in ("freeze_authorization_post_review", "freeze_authorization_grant_planning"):
        row = next((r for r in evidence.get("chain") or [] if r.get("stage") == stage), {})
        _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
    grant_plan_row = next(
        (r for r in evidence.get("chain") or [] if r.get("stage") == "freeze_authorization_grant_planning"),
        {},
    )
    _add(checks, "evidence.grant_planning.linked", grant_plan_row.get("linked") is True)
    _add(checks, "evidence.grant_planning.no_grant", grant_plan_row.get("authorization_grant") is False)
    _add(checks, "evidence.grant_planning.no_issued", grant_plan_row.get("grant_issued") is False)
    _add(checks, "evidence.node_count", evidence.get("node_count") == len(CHAIN_EVIDENCE_NODES))

    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        _add(checks, f"boundary.stmt.{stmt[:35]}", stmt in (boundary.get("statements") or []))
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
    _add(checks, "boundary.not_issued", boundary.get("grant_not_issued") is True)
    _add(checks, "boundary.grant_issued_false", boundary.get("grant_issued") is False)
    _add(checks, "boundary.not_frozen", boundary.get("foundation_frozen") is False)
    _add(checks, "boundary.not_closed", boundary.get("closed") is False)

    for key in NON_EXECUTION_CONSTRAINTS:
        _add(checks, f"constraints.{key}", constraints.get(key) is True)
    _add(checks, "constraints.ok", constraints.get("non_execution_boundary_ok") is True)

    debts = debt_carryover.get("debts") or []
    _add(checks, "debt.count", len(debts) >= 2)
    debt0 = debts[0] if debts else {}
    debt1 = debts[1] if len(debts) > 1 else {}
    _add(checks, "debt0.title", debt0.get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"])
    _add(checks, "debt0.priority", debt0.get("priority") == "P1")
    _add(checks, "debt0.classification", debt0.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt0.must_not_impl", debt0.get("must_not_implement_now") is True)
    _add(checks, "debt1.title", debt1.get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"])
    _add(checks, "debt1.priority", debt1.get("priority") == "P1")
    _add(checks, "debt1.classification", debt1.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt1.must_not_impl", debt1.get("must_not_implement_now") is True)
    _add(checks, "debt.carryover_complete", debt_carryover.get("governance_debt_carryover_complete") is True)

    _add(checks, "next_phase.ok", next_phase.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next_phase.target_dryrun", next_phase.get("target") == "freeze_authorization_grant_dryrun")
    _add(checks, "next_phase.dryrun_ready", next_phase.get("readiness") == "freeze-authorization-grant-dryrun-ready")
    _add(checks, "next_phase.no_grant", next_phase.get("grant_issued") is False)
    _add(checks, "next_phase.no_auth_grant", next_phase.get("freeze_authorization_granted") is False)
    _add(checks, "next_phase.no_adapter", next_phase.get("module_adapter_implementation_ready") is False)
    _add(checks, "next_phase.not_frozen", next_phase.get("foundation_frozen") is False)
    _add(checks, "next_phase.not_closed", next_phase.get("closed") is False)
    for target in FORBIDDEN_NEXT_TARGETS:
        _add(checks, f"next_phase.not_{target}", next_phase.get(target) is not True)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.not_issued", "does not issue grant" in md or "不签发 grant" in md)
    _add(checks, "md.grant_planning_ne", "grant planning ≠ grant issued" in md)
    _add(checks, "md.debt0", GOVERNANCE_DEBTS[0]["debt_title"] in md)
    _add(checks, "md.debt1", GOVERNANCE_DEBTS[1]["debt_title"] in md)

    for doc_name, doc in docs.items():
        for key in TRUE_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)
        _add(checks, f"sweep.boundary_en.{doc_name}", bool(doc.get("boundary_statement_en")))
        _add(checks, f"sweep.boundary_zh.{doc_name}", bool(doc.get("boundary_statement_zh")))

    for phrase in ("freeze-candidate", "Grant not issued", "freeze authorization grant planning"):
        _add(checks, f"md.phrase.{phrase[:30]}", phrase in md)

    passed = sum(1 for check in checks if check["passed"])
    failed = [check for check in checks if not check["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "prior_freeze_authorization_post_review_go": summary.get("prior_freeze_authorization_post_review_go") is True,
        "grant_plan_complete": summary.get("grant_plan_complete") is True,
        "grant_scope_planning_only": summary.get("grant_scope_planning_only") is True,
        "grant_candidate_only": summary.get("grant_candidate_only") is True,
        "grant_not_issued": summary.get("grant_not_issued") is True,
        "authorization_request_absent": summary.get("authorization_request_absent") is True,
        "authorization_grant_absent": summary.get("authorization_grant_absent") is True,
        "foundation_not_frozen": summary.get("foundation_not_frozen") is True,
        "closure_not_executed": summary.get("closure_not_executed") is True,
        "governance_debt_carryover_complete": summary.get("governance_debt_carryover_complete") is True,
        "l1_protocols_not_implemented": summary.get("l1_protocols_not_implemented") is True,
        "system_protocols_integration_not_implemented": summary.get("system_protocols_integration_not_implemented") is True,
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "next_phase_readiness_ok": summary.get("next_phase_readiness_ok") is True,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:80],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "passed_checks": report["passed_checks"],
                "failed_checks": report["failed_checks"],
                "blocker_count": report["blocker_count"],
                "prior_freeze_authorization_post_review_go": report["prior_freeze_authorization_post_review_go"],
                "grant_plan_complete": report["grant_plan_complete"],
                "grant_scope_planning_only": report["grant_scope_planning_only"],
                "grant_candidate_only": report["grant_candidate_only"],
                "grant_not_issued": report["grant_not_issued"],
                "authorization_request_absent": report["authorization_request_absent"],
                "authorization_grant_absent": report["authorization_grant_absent"],
                "foundation_not_frozen": report["foundation_not_frozen"],
                "closure_not_executed": report["closure_not_executed"],
                "governance_debt_carryover_complete": report["governance_debt_carryover_complete"],
                "l1_protocols_not_implemented": report["l1_protocols_not_implemented"],
                "system_protocols_integration_not_implemented": report["system_protocols_integration_not_implemented"],
                "non_execution_boundary_ok": report["non_execution_boundary_ok"],
                "next_phase_readiness_ok": report["next_phase_readiness_ok"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
