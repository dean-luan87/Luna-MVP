#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Final Closure DryRun v1."""

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
    ALLOWED_DOWNSTREAM_READINESS,
    CHAIN_TRACE_STAGES,
    DEFAULT_FINAL_CLOSURE_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    DRYRUN_BOUNDARY_STATEMENTS,
    FINAL_CLOSURE_PLANNING_PACKAGE_FILES,
    FINAL_DECISION_GO,
    FORBIDDEN_DOWNSTREAM,
    NEXT_PHASE_GO,
    PHASE_ID,
    PLANNING_TRUE_KEYS,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import (
    FINAL_DECISION_GO as FINAL_CLOSURE_PLANNING_FINAL_GO,
    GOVERNANCE_DEBTS,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_final_closure_dryrun_report_v1.json",
    "task_manager_foundation_handoff_final_closure_dryrun_report_v1.md",
    "task_manager_final_closure_plan_integrity_matrix_v1.json",
    "task_manager_final_closure_chain_traceability_matrix_v1.json",
    "task_manager_final_freeze_candidate_validation_v1.json",
    "task_manager_final_closure_boundary_validation_v1.json",
    "task_manager_final_downstream_reference_validation_v1.json",
    "task_manager_final_governance_debt_validation_v1.json",
    "task_manager_final_non_execution_validation_v1.json",
    "task_manager_final_closure_post_review_readiness_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "final_closure_plan_integrity_ok",
    "final_chain_traceability_ok",
    "freeze_candidate_preserved",
    "closure_candidate_preserved",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_reference_scope_ok",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "final_closure_dryrun_only",
    "post_review_readiness_ok",
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
    parser.add_argument("--final-closure-planning-root", default=DEFAULT_FINAL_CLOSURE_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.final_closure_planning_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_final_closure_dryrun_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    planning_summary = _read(planning / "summary.json")
    planning_verifier = _read(planning / "verifier_report.json")
    _add(checks, "planning.summary_go", planning_summary.get("final_decision") == FINAL_CLOSURE_PLANNING_FINAL_GO)
    _add(checks, "planning.verifier_go", planning_verifier.get("verifier") == "GO")
    _add(checks, "planning.passed_min", int(planning_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "planning.failed_zero", planning_verifier.get("failed_checks") == 0)
    _add(checks, "planning.blocker_zero", planning_verifier.get("blocker_count") == 0)
    for key in PLANNING_TRUE_KEYS:
        _add(checks, f"planning.summary.{key}", planning_summary.get(key) is True)
        if key in planning_verifier:
            _add(checks, f"planning.verifier.{key}", planning_verifier.get(key) is True)

    for fname in FINAL_CLOSURE_PLANNING_PACKAGE_FILES:
        path = planning / fname
        _add(checks, f"planning.package.exists.{fname}", path.is_file())
        if fname.endswith(".json"):
            _add(checks, f"planning.package.non_placeholder.{fname}", bool(_read(path)))

    report = docs["task_manager_foundation_handoff_final_closure_dryrun_report_v1.json"]
    integrity = docs["task_manager_final_closure_plan_integrity_matrix_v1.json"]
    trace = docs["task_manager_final_closure_chain_traceability_matrix_v1.json"]
    freeze_val = docs["task_manager_final_freeze_candidate_validation_v1.json"]
    boundary = docs["task_manager_final_closure_boundary_validation_v1.json"]
    downstream = docs["task_manager_final_downstream_reference_validation_v1.json"]
    debt_val = docs["task_manager_final_governance_debt_validation_v1.json"]
    non_exec = docs["task_manager_final_non_execution_validation_v1.json"]
    post_review = docs["task_manager_final_closure_post_review_readiness_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.dryrun_only.{doc_name}", doc.get("final_closure_dryrun_only") in (None, True))
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.l1_not_impl.{doc_name}", doc.get("l1_protocols_not_implemented") in (None, True))
        _add(checks, f"meta.sys_proto_not_impl.{doc_name}", doc.get("system_protocols_integration_not_implemented") in (None, True))
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in TRUE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"report.{key}", report.get(key) is True)

    _add(checks, "integrity.ok", integrity.get("final_closure_plan_integrity_ok") is True)
    for row in integrity.get("rows") or []:
        fname = row.get("file")
        _add(checks, f"integrity.exists.{fname}", row.get("exists") is True)
        _add(checks, f"integrity.non_placeholder.{fname}", row.get("non_placeholder") is True)

    _add(checks, "trace.ok", trace.get("final_chain_traceability_ok") is True)
    for stage in CHAIN_TRACE_STAGES:
        row = next((r for r in trace.get("rows") or [] if r.get("stage") == stage), {})
        _add(checks, f"trace.linked.{stage}", row.get("linked") is True)

    _add(checks, "freeze.status", freeze_val.get("freeze_status") == "freeze-candidate")
    _add(checks, "freeze.not_frozen", freeze_val.get("freeze_status") != "frozen")
    _add(checks, "freeze.not_foundation_frozen", freeze_val.get("freeze_status") != "foundation-frozen")
    _add(checks, "freeze.preserved", freeze_val.get("freeze_candidate_preserved") is True)
    _add(checks, "freeze.foundation_not_frozen", freeze_val.get("foundation_frozen") is False)

    _add(checks, "closure.state", freeze_val.get("closure_state") == "final-closure-dryrun")
    _add(checks, "closure.readiness", freeze_val.get("closure_readiness") == "final-closure-post-review-ready")
    _add(checks, "closure.not_closed", freeze_val.get("closure_state") != "closed")
    _add(checks, "closure.not_finalized", freeze_val.get("closure_readiness") != "foundation-finalized")
    _add(checks, "closure.preserved", freeze_val.get("closure_candidate_preserved") is True)
    _add(checks, "closure.not_applied", freeze_val.get("closure_applied") is False)

    for stmt in DRYRUN_BOUNDARY_STATEMENTS:
        _add(checks, f"boundary.stmt.{stmt[:35]}", stmt in (boundary.get("statements") or []))
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)

    for item in CLOSURE_CHANNEL_BOUNDARIES[:5]:
        candidate = item["candidate"]
        boundary_stmt = item["boundary"]
        _add(checks, f"md.channel.{candidate}", boundary_stmt in md)

    _add(checks, "downstream.ok", downstream.get("downstream_reference_scope_ok") is True)
    for row in downstream.get("consumers") or []:
        consumer = row.get("consumer")
        readiness = row.get("readiness")
        _add(checks, f"downstream.allowed.{consumer}", readiness in ALLOWED_DOWNSTREAM_READINESS)
        for forbidden in FORBIDDEN_DOWNSTREAM:
            _add(checks, f"downstream.not_{forbidden}.{consumer}", readiness != forbidden)

    debts = debt_val.get("debts") or []
    _add(checks, "debt.count", len(debts) >= 2)
    debt0 = debts[0] if debts else {}
    debt1 = debts[1] if len(debts) > 1 else {}
    _add(checks, "debt0.title", debt0.get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"])
    _add(checks, "debt0.priority", debt0.get("priority") == "P1")
    _add(checks, "debt0.classification", debt0.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt0.must_not_impl", debt0.get("must_not_implement_now") is True)
    _add(checks, "debt0.future_phase", debt0.get("recommended_future_phase") == GOVERNANCE_DEBTS[0]["recommended_future_phase"])
    _add(checks, "debt1.title", debt1.get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"])
    _add(checks, "debt1.priority", debt1.get("priority") == "P1")
    _add(checks, "debt1.classification", debt1.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt1.must_not_impl", debt1.get("must_not_implement_now") is True)
    _add(checks, "debt1.future_phase", debt1.get("recommended_future_phase") == GOVERNANCE_DEBTS[1]["recommended_future_phase"])
    _add(checks, "debt.preserved", debt_val.get("governance_debt_preserved") is True)

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
        _add(checks, f"non_exec.{key}", non_exec.get(key) is True)

    _add(checks, "post_review.ok", post_review.get("post_review_readiness_ok") is True)
    _add(checks, "post_review.next", post_review.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "post_review.no_adapter", post_review.get("module_adapter_implementation_ready") is False)
    _add(checks, "post_review.no_freeze_auth", post_review.get("freeze_authorization_ready") is False)
    _add(checks, "post_review.not_frozen", post_review.get("foundation_frozen") is False)
    _add(checks, "post_review.not_closed", post_review.get("closed") is False)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.not_execute", "does not execute closure" in md or "不执行 closure" in md)
    _add(checks, "md.debt0", GOVERNANCE_DEBTS[0]["debt_title"] in md)
    _add(checks, "md.debt1", GOVERNANCE_DEBTS[1]["debt_title"] in md)

    for doc_name, doc in docs.items():
        for key in TRUE_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next_post_review.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)
        _add(checks, f"sweep.boundary_en.{doc_name}", bool(doc.get("boundary_statement_en")))
        _add(checks, f"sweep.boundary_zh.{doc_name}", bool(doc.get("boundary_statement_zh")))

    for phrase in ("final-closure-dryrun", "freeze-candidate", "Governance Debts", "Red Line Boundaries"):
        _add(checks, f"md.phrase.{phrase[:30]}", phrase in md)

    for field in GOVERNANCE_DEBTS[0]:
        _add(checks, f"debt0.field.{field}", debt0.get(field) == GOVERNANCE_DEBTS[0].get(field) or bool(debt0.get(field)))
    for field in GOVERNANCE_DEBTS[1]:
        _add(checks, f"debt1.field.{field}", debt1.get(field) == GOVERNANCE_DEBTS[1].get(field) or bool(debt1.get(field)))

    passed = sum(1 for check in checks if check["passed"])
    failed = [check for check in checks if not check["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "final_closure_plan_integrity_ok": summary.get("final_closure_plan_integrity_ok") is True,
        "final_chain_traceability_ok": summary.get("final_chain_traceability_ok") is True,
        "freeze_candidate_preserved": summary.get("freeze_candidate_preserved") is True,
        "closure_candidate_preserved": summary.get("closure_candidate_preserved") is True,
        "candidate_semantics_preserved": summary.get("candidate_semantics_preserved") is True,
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "downstream_reference_scope_ok": summary.get("downstream_reference_scope_ok") is True,
        "governance_debt_preserved": summary.get("governance_debt_preserved") is True,
        "l1_protocols_not_implemented": summary.get("l1_protocols_not_implemented") is True,
        "system_protocols_integration_not_implemented": summary.get("system_protocols_integration_not_implemented") is True,
        "final_closure_dryrun_only": summary.get("final_closure_dryrun_only") is True,
        "post_review_readiness_ok": summary.get("post_review_readiness_ok") is True,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:80],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report_payload["verifier"],
                "passed_checks": report_payload["passed_checks"],
                "failed_checks": report_payload["failed_checks"],
                "blocker_count": report_payload["blocker_count"],
                "final_closure_plan_integrity_ok": report_payload["final_closure_plan_integrity_ok"],
                "final_chain_traceability_ok": report_payload["final_chain_traceability_ok"],
                "freeze_candidate_preserved": report_payload["freeze_candidate_preserved"],
                "closure_candidate_preserved": report_payload["closure_candidate_preserved"],
                "candidate_semantics_preserved": report_payload["candidate_semantics_preserved"],
                "non_execution_boundary_ok": report_payload["non_execution_boundary_ok"],
                "downstream_reference_scope_ok": report_payload["downstream_reference_scope_ok"],
                "governance_debt_preserved": report_payload["governance_debt_preserved"],
                "l1_protocols_not_implemented": report_payload["l1_protocols_not_implemented"],
                "system_protocols_integration_not_implemented": report_payload["system_protocols_integration_not_implemented"],
                "final_closure_dryrun_only": report_payload["final_closure_dryrun_only"],
                "post_review_readiness_ok": report_payload["post_review_readiness_ok"],
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
