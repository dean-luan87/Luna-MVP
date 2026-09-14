#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Final Closure Post-DryRun Review v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_foundation_handoff_closure_dryrun_v1 import CLOSURE_CHANNEL_BOUNDARIES
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_dryrun_v1 import (
    DRYRUN_BOUNDARY_STATEMENTS,
    FINAL_DECISION_GO as FINAL_CLOSURE_DRYRUN_FINAL_GO,
    GOVERNANCE_DEBTS,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_post_dryrun_review_v1 import (
    ALLOWED_DOWNSTREAM_READINESS,
    CHAIN_EVIDENCE_NODES,
    DEFAULT_FINAL_CLOSURE_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    DRYRUN_TRUE_KEYS,
    FINAL_CLOSURE_DRYRUN_ARTIFACTS,
    FINAL_DECISION_GO,
    FORBIDDEN_DOWNSTREAM,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_final_closure_post_dryrun_review_v1.json",
    "task_manager_foundation_handoff_final_closure_post_dryrun_review_v1.md",
    "task_manager_final_closure_dryrun_review_matrix_v1.json",
    "task_manager_final_closure_boundary_drift_review_v1.json",
    "task_manager_final_closure_chain_evidence_review_v1.json",
    "task_manager_final_freeze_candidate_review_v1.json",
    "task_manager_final_downstream_reference_review_v1.json",
    "task_manager_final_governance_debt_review_v1.json",
    "task_manager_final_authorization_planning_readiness_v1.json",
    "task_manager_final_review_non_execution_constraints_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "final_closure_dryrun_result_accepted",
    "boundary_drift_absent",
    "final_chain_evidence_accepted",
    "freeze_candidate_preserved",
    "closure_candidate_preserved",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_reference_scope_ok",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "post_review_only",
    "authorization_planning_ready",
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
    parser.add_argument("--final-closure-dryrun-root", default=DEFAULT_FINAL_CLOSURE_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.final_closure_dryrun_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_final_closure_post_dryrun_review_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    freeze_val = _read(dryrun / "task_manager_final_freeze_candidate_validation_v1.json")
    boundary_val = _read(dryrun / "task_manager_final_closure_boundary_validation_v1.json")

    _add(checks, "dryrun.summary_go", dryrun_summary.get("final_decision") == FINAL_CLOSURE_DRYRUN_FINAL_GO)
    _add(checks, "dryrun.verifier_go", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "dryrun.passed_min", int(dryrun_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "dryrun.failed_zero", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "dryrun.blocker_zero", dryrun_verifier.get("blocker_count") == 0)
    for key in DRYRUN_TRUE_KEYS:
        _add(checks, f"dryrun.summary.{key}", dryrun_summary.get(key) is True)
        _add(checks, f"dryrun.verifier.{key}", dryrun_verifier.get(key) is True)

    for artifact in FINAL_CLOSURE_DRYRUN_ARTIFACTS:
        path = dryrun / artifact
        _add(checks, f"dryrun.artifact.exists.{artifact}", path.is_file())
        if artifact.endswith(".json"):
            _add(checks, f"dryrun.artifact.non_placeholder.{artifact}", bool(_read(path)))

    review = docs["task_manager_foundation_handoff_final_closure_post_dryrun_review_v1.json"]
    matrix = docs["task_manager_final_closure_dryrun_review_matrix_v1.json"]
    drift = docs["task_manager_final_closure_boundary_drift_review_v1.json"]
    evidence = docs["task_manager_final_closure_chain_evidence_review_v1.json"]
    freeze_review = docs["task_manager_final_freeze_candidate_review_v1.json"]
    downstream = docs["task_manager_final_downstream_reference_review_v1.json"]
    debt_review = docs["task_manager_final_governance_debt_review_v1.json"]
    auth_readiness = docs["task_manager_final_authorization_planning_readiness_v1.json"]
    constraints = docs["task_manager_final_review_non_execution_constraints_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.post_review_only.{doc_name}", doc.get("post_review_only") is True)
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.l1_not_impl.{doc_name}", doc.get("l1_protocols_not_implemented") in (None, True))
        _add(checks, f"meta.sys_proto_not_impl.{doc_name}", doc.get("system_protocols_integration_not_implemented") in (None, True))
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("post_dryrun_review_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in TRUE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"review.{key}", review.get(key) is True)

    _add(checks, "matrix.accepted", matrix.get("final_closure_dryrun_result_accepted") is True)
    for row in matrix.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"matrix.exists.{name}", row.get("exists") is True)
        _add(checks, f"matrix.non_placeholder.{name}", row.get("non_placeholder") is True)

    _add(checks, "drift.absent", drift.get("boundary_drift_absent") is True)
    for row in drift.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"drift.runtime_absent.{name}", row.get("runtime_scope_leak_absent") is True)
        _add(checks, f"drift.no_added_runtime.{name}", row.get("post_review_added_runtime") is False)

    _add(checks, "evidence.accepted", evidence.get("final_chain_evidence_accepted") is True)
    _add(checks, "evidence.node_count", evidence.get("node_count") == len(CHAIN_EVIDENCE_NODES))
    for stage in CHAIN_EVIDENCE_NODES:
        row = next((r for r in evidence.get("chain") or [] if r.get("stage") == stage), {})
        _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)

    _add(checks, "freeze.status", freeze_review.get("freeze_status") == "freeze-candidate")
    _add(checks, "freeze.not_frozen", freeze_review.get("freeze_status") != "frozen")
    _add(checks, "freeze.not_foundation_frozen", freeze_review.get("freeze_status") != "foundation-frozen")
    _add(checks, "freeze.preserved", freeze_review.get("freeze_candidate_preserved") is True)
    _add(checks, "freeze.foundation_not_frozen", freeze_review.get("foundation_frozen") is False)

    _add(checks, "closure.readiness_ok", review.get("closure_readiness") in ("final-closure-post-review-ready", "authorization-planning-ready"))
    _add(checks, "closure.not_closed", review.get("closure_readiness") != "closed")
    _add(checks, "closure.boundary_closed", "closure_candidate != closed" in (boundary_val.get("statements") or []))
    _add(checks, "closure.boundary_dryrun", "final_closure_dryrun != closure_execution" in (boundary_val.get("statements") or []))

    _add(checks, "downstream.ok", downstream.get("downstream_reference_scope_ok") is True)
    for row in downstream.get("consumers") or []:
        consumer = row.get("consumer")
        readiness = row.get("readiness")
        _add(checks, f"downstream.allowed.{consumer}", readiness in ALLOWED_DOWNSTREAM_READINESS)
        for forbidden in FORBIDDEN_DOWNSTREAM:
            _add(checks, f"downstream.not_{forbidden}.{consumer}", readiness != forbidden)

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

    for key in (
        "non_execution_boundary_ok",
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
    ):
        _add(checks, f"constraints.{key}", constraints.get(key) is True)

    _add(checks, "auth.ready", auth_readiness.get("authorization_planning_ready") is True)
    _add(checks, "auth.next", auth_readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "auth.no_adapter", auth_readiness.get("module_adapter_implementation_ready") is False)
    _add(checks, "auth.not_frozen", auth_readiness.get("foundation_frozen") is False)
    _add(checks, "auth.not_closed", auth_readiness.get("closed") is False)
    for candidate in auth_readiness.get("candidates") or []:
        phase = candidate.get("phase", "")
        _add(checks, f"auth.candidate.{phase[:45]}.no_adapter", candidate.get("module_adapter_implementation") is False)
        _add(checks, f"auth.candidate.{phase[:45]}.not_frozen", candidate.get("foundation_frozen") is False)
        _add(checks, f"auth.candidate.{phase[:45]}.not_closed", candidate.get("closed") is False)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.not_execute", "does not execute closure" in md or "不执行 closure" in md)
    _add(checks, "md.debt0", GOVERNANCE_DEBTS[0]["debt_title"] in md)
    _add(checks, "md.debt1", GOVERNANCE_DEBTS[1]["debt_title"] in md)

    for stmt in ("final_closure_dryrun != closure_execution", "freeze_candidate != frozen", "closure_candidate != closed"):
        _add(checks, f"md.boundary.{stmt[:30]}", stmt in md)

    for item in CLOSURE_CHANNEL_BOUNDARIES[:5]:
        _add(checks, f"md.channel.{item['candidate']}", item["boundary"] in md)

    for doc_name, doc in docs.items():
        for key in TRUE_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)
        _add(checks, f"sweep.boundary_en.{doc_name}", bool(doc.get("boundary_statement_en")))
        _add(checks, f"sweep.boundary_zh.{doc_name}", bool(doc.get("boundary_statement_zh")))

    for phrase in ("authorization-planning-ready", "freeze-candidate", "Governance Debts", "Chain evidence accepted"):
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
        "final_closure_dryrun_result_accepted": summary.get("final_closure_dryrun_result_accepted") is True,
        "boundary_drift_absent": summary.get("boundary_drift_absent") is True,
        "final_chain_evidence_accepted": summary.get("final_chain_evidence_accepted") is True,
        "freeze_candidate_preserved": summary.get("freeze_candidate_preserved") is True,
        "closure_candidate_preserved": summary.get("closure_candidate_preserved") is True,
        "candidate_semantics_preserved": summary.get("candidate_semantics_preserved") is True,
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "downstream_reference_scope_ok": summary.get("downstream_reference_scope_ok") is True,
        "governance_debt_preserved": summary.get("governance_debt_preserved") is True,
        "l1_protocols_not_implemented": summary.get("l1_protocols_not_implemented") is True,
        "system_protocols_integration_not_implemented": summary.get("system_protocols_integration_not_implemented") is True,
        "post_review_only": summary.get("post_review_only") is True,
        "authorization_planning_ready": summary.get("authorization_planning_ready") is True,
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
                "final_closure_dryrun_result_accepted": report["final_closure_dryrun_result_accepted"],
                "boundary_drift_absent": report["boundary_drift_absent"],
                "final_chain_evidence_accepted": report["final_chain_evidence_accepted"],
                "freeze_candidate_preserved": report["freeze_candidate_preserved"],
                "closure_candidate_preserved": report["closure_candidate_preserved"],
                "candidate_semantics_preserved": report["candidate_semantics_preserved"],
                "non_execution_boundary_ok": report["non_execution_boundary_ok"],
                "downstream_reference_scope_ok": report["downstream_reference_scope_ok"],
                "governance_debt_preserved": report["governance_debt_preserved"],
                "l1_protocols_not_implemented": report["l1_protocols_not_implemented"],
                "system_protocols_integration_not_implemented": report["system_protocols_integration_not_implemented"],
                "post_review_only": report["post_review_only"],
                "authorization_planning_ready": report["authorization_planning_ready"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
