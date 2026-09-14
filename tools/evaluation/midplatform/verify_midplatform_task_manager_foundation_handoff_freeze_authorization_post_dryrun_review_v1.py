#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Post-DryRun Review v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    FINAL_DECISION_GO as FREEZE_AUTH_DRYRUN_FINAL_GO,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1 import (
    ALLOWED_SCOPE_CLASSIFICATIONS,
    CHAIN_EVIDENCE_NODES,
    DEFAULT_FREEZE_AUTH_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    DRYRUN_TRUE_KEYS,
    FINAL_DECISION_GO,
    FREEZE_AUTHORIZATION_DRYRUN_ARTIFACTS,
    NEXT_PHASE_GO,
    PHASE_ID,
    POST_REVIEW_BOUNDARY_STATEMENTS,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.md",
    "task_manager_freeze_authorization_dryrun_review_matrix_v1.json",
    "task_manager_freeze_authorization_boundary_drift_review_v1.json",
    "task_manager_freeze_authorization_chain_evidence_review_v1.json",
    "task_manager_freeze_authorization_request_absence_review_v1.json",
    "task_manager_freeze_authorization_grant_absence_review_v1.json",
    "task_manager_freeze_state_absence_review_v1.json",
    "task_manager_freeze_authorization_governance_debt_review_v1.json",
    "task_manager_freeze_authorization_grant_planning_readiness_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "freeze_authorization_dryrun_result_accepted",
    "boundary_drift_absent",
    "freeze_authorization_chain_evidence_accepted",
    "authorization_scope_preserved",
    "freeze_authorization_candidate_preserved",
    "authorization_request_absent",
    "authorization_grant_absent",
    "freeze_execution_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "post_review_only",
    "grant_planning_ready",
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
    parser.add_argument("--freeze-authorization-dryrun-root", default=DEFAULT_FREEZE_AUTH_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.freeze_authorization_dryrun_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    _add(checks, "dryrun.summary_go", dryrun_summary.get("final_decision") == FREEZE_AUTH_DRYRUN_FINAL_GO)
    _add(checks, "dryrun.verifier_go", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "dryrun.passed_min", int(dryrun_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "dryrun.failed_zero", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "dryrun.blocker_zero", dryrun_verifier.get("blocker_count") == 0)
    for key in DRYRUN_TRUE_KEYS:
        _add(checks, f"dryrun.summary.{key}", dryrun_summary.get(key) is True)
        if key in dryrun_verifier:
            _add(checks, f"dryrun.verifier.{key}", dryrun_verifier.get(key) is True)

    for artifact in FREEZE_AUTHORIZATION_DRYRUN_ARTIFACTS:
        path = dryrun / artifact
        _add(checks, f"dryrun.artifact.exists.{artifact}", path.is_file())
        if artifact.endswith(".json"):
            _add(checks, f"dryrun.artifact.non_placeholder.{artifact}", bool(_read(path)))

    review = docs["task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.json"]
    matrix = docs["task_manager_freeze_authorization_dryrun_review_matrix_v1.json"]
    drift = docs["task_manager_freeze_authorization_boundary_drift_review_v1.json"]
    evidence = docs["task_manager_freeze_authorization_chain_evidence_review_v1.json"]
    request_review = docs["task_manager_freeze_authorization_request_absence_review_v1.json"]
    grant_review = docs["task_manager_freeze_authorization_grant_absence_review_v1.json"]
    freeze_state = docs["task_manager_freeze_state_absence_review_v1.json"]
    debt_review = docs["task_manager_freeze_authorization_governance_debt_review_v1.json"]
    grant_readiness = docs["task_manager_freeze_authorization_grant_planning_readiness_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.post_review_only.{doc_name}", doc.get("post_review_only") is True)
        _add(checks, f"meta.auth_not_granted.{doc_name}", doc.get("authorization_grant_absent") in (None, True))
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.grant_not_issued.{doc_name}", doc.get("grant_planning_not_grant_issued") in (None, True))
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("post_dryrun_review_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in TRUE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"review.{key}", review.get(key) is True)

    _add(checks, "matrix.accepted", matrix.get("freeze_authorization_dryrun_result_accepted") is True)
    for row in matrix.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"matrix.exists.{name}", row.get("exists") is True)
        _add(checks, f"matrix.non_placeholder.{name}", row.get("non_placeholder") is True)

    _add(checks, "drift.absent", drift.get("boundary_drift_absent") is True)
    for row in drift.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"drift.runtime_absent.{name}", row.get("runtime_scope_leak_absent") is True)
        _add(checks, f"drift.no_added_runtime.{name}", row.get("post_review_added_runtime") is False)

    _add(checks, "evidence.accepted", evidence.get("freeze_authorization_chain_evidence_accepted") is True)
    _add(checks, "evidence.node_count", evidence.get("node_count") == len(CHAIN_EVIDENCE_NODES))
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in evidence.get("chain") or [] if r.get("stage") == stage), {})
        _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
    post_row = next((r for r in evidence.get("chain") or [] if r.get("stage") == "freeze_authorization_post_review"), {})
    _add(checks, "evidence.post_review.linked", post_row.get("linked") is True)
    _add(checks, "evidence.post_review.no_grant", post_row.get("authorization_grant") is False)

    _add(checks, "request.absent", request_review.get("authorization_request_absent") is True)
    _add(checks, "request.no_request", request_review.get("no_authorization_request") is True)

    _add(checks, "grant.absent", grant_review.get("authorization_grant_absent") is True)
    _add(checks, "grant.no_grant", grant_review.get("no_authorization_grant") is True)
    _add(checks, "grant.freeze_exec_absent", grant_review.get("freeze_execution_absent") is True)
    _add(checks, "grant.no_rollback_exec", grant_review.get("no_rollback_execution_path") is True)

    _add(checks, "freeze_state.not_frozen", freeze_state.get("foundation_not_frozen") is True)
    _add(checks, "freeze_state.closure_not_executed", freeze_state.get("closure_not_executed") is True)
    _add(checks, "freeze_state.status", freeze_state.get("freeze_status") == "freeze-candidate")
    _add(checks, "freeze_state.not_frozen_val", freeze_state.get("freeze_status") != "frozen")
    _add(checks, "freeze_state.not_foundation_frozen", freeze_state.get("freeze_status") != "foundation-frozen")
    _add(checks, "freeze_state.not_closed", freeze_state.get("closure_status") != "closed")
    _add(checks, "freeze_state.not_finalized", freeze_state.get("closure_status") != "foundation-finalized")

    debts = debt_review.get("debts") or []
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
    _add(checks, "debt.preserved", debt_review.get("governance_debt_preserved") is True)

    _add(checks, "grant_readiness.ready", grant_readiness.get("grant_planning_ready") is True)
    _add(checks, "grant_readiness.not_issued", grant_readiness.get("grant_planning_not_grant_issued") is True)
    _add(checks, "grant_readiness.next", grant_readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "grant_readiness.no_grant", grant_readiness.get("freeze_authorization_granted") is False)
    _add(checks, "grant_readiness.no_adapter", grant_readiness.get("module_adapter_implementation_ready") is False)
    _add(checks, "grant_readiness.not_frozen", grant_readiness.get("foundation_frozen") is False)
    _add(checks, "grant_readiness.not_closed", grant_readiness.get("closed") is False)
    for candidate in grant_readiness.get("candidates") or []:
        phase = candidate.get("phase", "")
        _add(checks, f"grant_readiness.candidate.{phase[:45]}.no_grant", candidate.get("grant_issued") is False)
        _add(checks, f"grant_readiness.candidate.{phase[:45]}.not_frozen", candidate.get("foundation_frozen") is False)
        _add(checks, f"grant_readiness.candidate.{phase[:45]}.not_closed", candidate.get("closed") is False)

    for stmt in POST_REVIEW_BOUNDARY_STATEMENTS:
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
        _add(checks, f"drift.boundary.{stmt[:35]}", stmt in (drift.get("boundary_statements") or []))

    _add(checks, "review.scope_preserved", review.get("authorization_scope_preserved") is True)
    for scope_cls in ALLOWED_SCOPE_CLASSIFICATIONS:
        _add(checks, f"scope.allowed.{scope_cls[:30]}", scope_cls in ALLOWED_SCOPE_CLASSIFICATIONS)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.not_grant", "does not grant authorization" in md or "不授予 authorization" in md)
    _add(checks, "md.grant_planning_not_issued", "grant planning ≠ grant issued" in md)
    _add(checks, "md.debt0", GOVERNANCE_DEBTS[0]["debt_title"] in md)
    _add(checks, "md.debt1", GOVERNANCE_DEBTS[1]["debt_title"] in md)

    for doc_name, doc in docs.items():
        for key in TRUE_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)

    for phrase in ("freeze-candidate", "Authorization grant absent", "Grant planning ready"):
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
        "freeze_authorization_dryrun_result_accepted": summary.get("freeze_authorization_dryrun_result_accepted") is True,
        "boundary_drift_absent": summary.get("boundary_drift_absent") is True,
        "freeze_authorization_chain_evidence_accepted": summary.get("freeze_authorization_chain_evidence_accepted") is True,
        "authorization_scope_preserved": summary.get("authorization_scope_preserved") is True,
        "freeze_authorization_candidate_preserved": summary.get("freeze_authorization_candidate_preserved") is True,
        "authorization_request_absent": summary.get("authorization_request_absent") is True,
        "authorization_grant_absent": summary.get("authorization_grant_absent") is True,
        "freeze_execution_absent": summary.get("freeze_execution_absent") is True,
        "foundation_not_frozen": summary.get("foundation_not_frozen") is True,
        "closure_not_executed": summary.get("closure_not_executed") is True,
        "governance_debt_preserved": summary.get("governance_debt_preserved") is True,
        "l1_protocols_not_implemented": summary.get("l1_protocols_not_implemented") is True,
        "system_protocols_integration_not_implemented": summary.get("system_protocols_integration_not_implemented") is True,
        "post_review_only": summary.get("post_review_only") is True,
        "grant_planning_ready": summary.get("grant_planning_ready") is True,
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
                "freeze_authorization_dryrun_result_accepted": report["freeze_authorization_dryrun_result_accepted"],
                "boundary_drift_absent": report["boundary_drift_absent"],
                "freeze_authorization_chain_evidence_accepted": report["freeze_authorization_chain_evidence_accepted"],
                "authorization_scope_preserved": report["authorization_scope_preserved"],
                "freeze_authorization_candidate_preserved": report["freeze_authorization_candidate_preserved"],
                "authorization_request_absent": report["authorization_request_absent"],
                "authorization_grant_absent": report["authorization_grant_absent"],
                "freeze_execution_absent": report["freeze_execution_absent"],
                "foundation_not_frozen": report["foundation_not_frozen"],
                "closure_not_executed": report["closure_not_executed"],
                "governance_debt_preserved": report["governance_debt_preserved"],
                "l1_protocols_not_implemented": report["l1_protocols_not_implemented"],
                "system_protocols_integration_not_implemented": report["system_protocols_integration_not_implemented"],
                "post_review_only": report["post_review_only"],
                "grant_planning_ready": report["grant_planning_ready"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
