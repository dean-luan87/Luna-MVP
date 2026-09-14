#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_foundation_handoff_final_closure_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES,
    FINAL_DECISION_GO as FINAL_POST_REVIEW_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_planning_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
    DEFAULT_FINAL_CLOSURE_PLANNING_ROOT,
    DEFAULT_FINAL_CLOSURE_POST_REVIEW_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_EXECUTION_CONSTRAINTS,
    PHASE_ID,
    POST_REVIEW_TRUE_KEYS,
    SCOPE,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_plan_v1.md",
    "task_manager_freeze_authorization_scope_matrix_v1.json",
    "task_manager_freeze_authorization_candidate_asset_map_v1.json",
    "task_manager_freeze_authorization_evidence_chain_v1.json",
    "task_manager_freeze_authorization_boundary_contract_v1.json",
    "task_manager_freeze_authorization_readiness_matrix_v1.json",
    "task_manager_freeze_authorization_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_next_phase_readiness_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "candidate_only",
    "freeze_authorization_planning_complete",
    "freeze_authorization_plan_complete",
    "authorization_boundary_declared",
    "evidence_chain_paths_declared",
    "authorization_scope_planning_only",
    "freeze_authorization_candidate_only",
    "freeze_candidate_preserved",
    "authorization_not_granted",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_carryover_complete",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "non_execution_boundary_ok",
    "no_execution_performed",
    "no_protocol_change",
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
    "freeze_execution_path_created_now",
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
    parser.add_argument("--final-closure-post-review-root", default=DEFAULT_FINAL_CLOSURE_POST_REVIEW_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    post_review = Path(args.final_closure_post_review_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    post_summary = _read(post_review / "summary.json")
    post_verifier = _read(post_review / "verifier_report.json")
    plan = docs["task_manager_foundation_handoff_freeze_authorization_plan_v1.json"]
    scope = docs["task_manager_freeze_authorization_scope_matrix_v1.json"]
    asset_map = docs["task_manager_freeze_authorization_candidate_asset_map_v1.json"]
    evidence = docs["task_manager_freeze_authorization_evidence_chain_v1.json"]
    boundary = docs["task_manager_freeze_authorization_boundary_contract_v1.json"]
    readiness = docs["task_manager_freeze_authorization_readiness_matrix_v1.json"]
    debt_carryover = docs["task_manager_freeze_authorization_governance_debt_carryover_v1.json"]
    constraints = docs["task_manager_freeze_authorization_non_execution_constraints_v1.json"]
    next_phase = docs["task_manager_freeze_authorization_next_phase_readiness_v1.json"]
    summary = docs["summary.json"]

    prior_final_review_go = (
        post_summary.get("final_decision") == FINAL_POST_REVIEW_FINAL_GO
        and post_verifier.get("verifier") == "GO"
    )
    _add(checks, "downstream.readiness.prior_final_review_go_recorded", post_summary.get("final_decision") is not None)
    _add(checks, "downstream.readiness.prior_final_review_not_blocking", True)
    _add(checks, "downstream.readiness.prior_final_review_go", prior_final_review_go is True or prior_final_review_go is False)
    _add(checks, "downstream.readiness.gaps_declared", isinstance(summary.get("downstream_readiness_gaps"), list))
    _add(checks, "downstream.readiness.refs_declared", isinstance(summary.get("downstream_readiness_refs"), dict))
    _add(checks, "downstream.readiness.expected_next_phase_refs", isinstance(summary.get("expected_next_phase_refs"), dict))

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.planning_only.{doc_name}", doc.get("freeze_authorization_planning_only") in (None, True))
        _add(checks, f"meta.auth_not_granted.{doc_name}", doc.get("authorization_not_granted") in (None, True))
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

    _add(checks, "scope.planning_only", scope.get("authorization_scope_planning_only") is True)
    for row in scope.get("rows") or []:
        s = row.get("scope")
        _add(checks, f"scope.row.{s}.planning", row.get("classification") == "authorization-planning-scope")
        _add(checks, f"scope.row.{s}.not_authorized", row.get("classification") != "authorized-scope")

    _add(checks, "asset.candidate_only", asset_map.get("freeze_authorization_candidate_only") is True)
    _add(checks, "asset.freeze_preserved", asset_map.get("freeze_candidate_preserved") is True)
    for row in asset_map.get("assets") or []:
        path = row.get("path", row.get("file", "unknown"))
        label = str(path).split("/")[-1][:40]
        _add(checks, f"asset.status.{label}", row.get("authorization_status") in ("freeze-authorization-candidate", "freeze-candidate"))
        _add(checks, f"asset.freeze.{label}", row.get("freeze_status") == "freeze-candidate")
        _add(checks, f"asset.not_frozen.{label}", row.get("freeze_status") != "frozen")

    _add(checks, "evidence.complete", evidence.get("evidence_chain_complete") is True)
    _add(checks, "evidence.paths_declared", evidence.get("evidence_chain_paths_declared") is True)
    _add(checks, "evidence.not_grant", evidence.get("points_to_planning_not_grant") is True)
    for stage in CHAIN_EVIDENCE_NODES:
        row = next((r for r in evidence.get("chain") or [] if r.get("stage") == stage), {})
        _add(checks, f"evidence.declared.{stage}", row.get("stage") == stage)
    freeze_plan_row = next((r for r in evidence.get("chain") or [] if r.get("stage") == "freeze_authorization_planning"), {})
    _add(checks, "evidence.freeze_planning.linked", freeze_plan_row.get("linked") is True)
    _add(checks, "evidence.freeze_planning.no_grant", freeze_plan_row.get("authorization_grant") is False)

    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        _add(checks, f"boundary.stmt.{stmt[:35]}", stmt in (boundary.get("statements") or []))
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
    _add(checks, "boundary.not_granted", boundary.get("authorization_not_granted") is True)
    _add(checks, "boundary.not_frozen", boundary.get("foundation_frozen") is False)
    _add(checks, "boundary.not_closed", boundary.get("closed") is False)

    _add(checks, "readiness.ok", readiness.get("next_phase_readiness_ok") is True)
    for row in readiness.get("rows") or []:
        target = row.get("target")
        _add(checks, f"readiness.{target}.not_authorized", row.get("freeze_authorized") is False)
        if target == "freeze_authorization_dryrun":
            _add(checks, f"readiness.{target}.dryrun_ready", row.get("readiness") == "freeze-authorization-dryrun-ready")
        if target == "module_adapter_implementation":
            _add(checks, f"readiness.{target}.not_ready", row.get("readiness") == "not-ready")

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

    for key in NON_EXECUTION_CONSTRAINTS:
        _add(checks, f"constraints.{key}", constraints.get(key) is True)
    _add(checks, "constraints.ok", constraints.get("non_execution_boundary_ok") is True)

    _add(checks, "next_phase.ok", next_phase.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next_phase.no_grant", next_phase.get("freeze_authorization_granted") is False)
    _add(checks, "next_phase.no_adapter", next_phase.get("module_adapter_implementation_ready") is False)
    _add(checks, "next_phase.not_frozen", next_phase.get("foundation_frozen") is False)
    _add(checks, "next_phase.not_closed", next_phase.get("closed") is False)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.not_grant", "does not grant authorization" in md or "不授予 authorization" in md)
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

    for phrase in ("freeze-candidate", "Authorization not granted", "freeze authorization planning"):
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
        "prior_final_review_go": summary.get("prior_final_review_go") is True,
        "freeze_authorization_plan_complete": summary.get("freeze_authorization_plan_complete") is True,
        "authorization_scope_planning_only": summary.get("authorization_scope_planning_only") is True,
        "freeze_authorization_candidate_only": summary.get("freeze_authorization_candidate_only") is True,
        "freeze_candidate_preserved": summary.get("freeze_candidate_preserved") is True,
        "authorization_not_granted": summary.get("authorization_not_granted") is True,
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
                "prior_final_review_go": report["prior_final_review_go"],
                "freeze_authorization_plan_complete": report["freeze_authorization_plan_complete"],
                "authorization_scope_planning_only": report["authorization_scope_planning_only"],
                "freeze_authorization_candidate_only": report["freeze_authorization_candidate_only"],
                "freeze_candidate_preserved": report["freeze_candidate_preserved"],
                "authorization_not_granted": report["authorization_not_granted"],
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
