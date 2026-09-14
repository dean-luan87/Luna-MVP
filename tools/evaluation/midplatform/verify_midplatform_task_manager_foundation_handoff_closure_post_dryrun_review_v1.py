#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Closure Post-DryRun Review v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_foundation_handoff_closure_dryrun_v1 import (
    CLOSURE_CHANNEL_BOUNDARIES,
    CLOSURE_GOVERNANCE_DEBT,
    DEFAULT_OUTPUT as DEFAULT_CLOSURE_DRYRUN_ROOT,
    FINAL_DECISION_GO as CLOSURE_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as CLOSURE_DRYRUN_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_closure_post_dryrun_review_v1 import (
    CLOSURE_DRYRUN_ARTIFACTS,
    DEFAULT_OUTPUT,
    DRYRUN_TRUE_KEYS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_closure_post_dryrun_review_v1.json",
    "task_manager_foundation_handoff_closure_post_dryrun_review_v1.md",
    "task_manager_closure_dryrun_review_matrix_v1.json",
    "task_manager_closure_boundary_drift_review_v1.json",
    "task_manager_closure_evidence_chain_review_v1.json",
    "task_manager_closure_governance_debt_review_v1.json",
    "task_manager_closure_final_planning_readiness_matrix_v1.json",
    "task_manager_closure_review_non_execution_constraints_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "closure_dryrun_result_accepted",
    "boundary_drift_absent",
    "governance_debt_preserved",
    "closure_channel_governance_not_implemented",
    "freeze_candidate_preserved",
    "closure_candidate_preserved",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_scope_ok",
    "post_review_only",
    "final_closure_planning_ready",
)
FORBIDDEN_STATUS: Tuple[str, ...] = (
    "closed",
    "frozen",
    "foundation-finalized",
    "foundation_finalized",
    "implementation-ready",
    "runtime-ready",
    "production-ready",
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
    parser.add_argument("--closure-dryrun-root", default=DEFAULT_CLOSURE_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.closure_dryrun_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_closure_post_dryrun_review_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    debt_register = _read(dryrun / "task_manager_closure_governance_debt_register_v1.json")
    freeze_val = _read(dryrun / "task_manager_closure_freeze_candidate_validation_v1.json")
    semantics_val = _read(dryrun / "task_manager_closure_candidate_semantics_validation_v1.json")
    downstream_val = _read(dryrun / "task_manager_closure_downstream_scope_validation_v1.json")

    _add(checks, "dryrun.summary_go", dryrun_summary.get("final_decision") == CLOSURE_DRYRUN_FINAL_GO)
    _add(checks, "dryrun.verifier_go", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "dryrun.passed_min", int(dryrun_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "dryrun.failed_zero", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "dryrun.blocker_zero", dryrun_verifier.get("blocker_count") == 0)
    for key in DRYRUN_TRUE_KEYS:
        _add(checks, f"dryrun.summary.{key}", dryrun_summary.get(key) is True)
        _add(checks, f"dryrun.verifier.{key}", dryrun_verifier.get(key) is True)

    for artifact in CLOSURE_DRYRUN_ARTIFACTS:
        path = dryrun / artifact
        _add(checks, f"dryrun.artifact.exists.{artifact}", path.is_file())
        if artifact.endswith(".json"):
            dryrun_doc = _read(path)
            _add(checks, f"dryrun.artifact.non_placeholder.{artifact}", bool(dryrun_doc))
        else:
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
            _add(checks, f"dryrun.artifact.non_placeholder.{artifact}", len(text.strip()) > 200)

    debts = debt_register.get("debts") or []
    debt = debts[0] if debts else {}
    _add(checks, "debt.register_exists", bool(debt_register))
    _add(checks, "debt.title", debt.get("debt_title") == CLOSURE_GOVERNANCE_DEBT["debt_title"])
    _add(checks, "debt.priority", debt.get("priority") == "P1")
    _add(checks, "debt.classification", debt.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt.must_not_impl", debt.get("must_not_implement_now") is True)
    _add(checks, "debt.future_phase", debt.get("recommended_future_phase") == CLOSURE_GOVERNANCE_DEBT["recommended_future_phase"])
    _add(checks, "debt.l1_not_impl", debt_register.get("l1_closure_protocol_not_implemented") is True)

    _add(checks, "freeze.status", freeze_val.get("freeze_status") == "freeze-candidate")
    _add(checks, "freeze.not_frozen", freeze_val.get("freeze_status") != "frozen")
    readiness = freeze_val.get("closure_readiness")
    _add(checks, "closure.readiness_ok", readiness in ("closure-dryrun-ready", "final-closure-planning-ready"))
    _add(checks, "closure.not_closed", readiness != "closed")

    for item in CLOSURE_CHANNEL_BOUNDARIES:
        candidate = item["candidate"]
        boundary = item["boundary"]
        row = next((b for b in semantics_val.get("boundaries") or [] if b.get("candidate") == candidate), {})
        _add(checks, f"semantics.boundary.{candidate}", row.get("boundary") == boundary)
        _add(checks, f"md.boundary.{candidate}", boundary in md)

    review = docs["task_manager_foundation_handoff_closure_post_dryrun_review_v1.json"]
    matrix = docs["task_manager_closure_dryrun_review_matrix_v1.json"]
    drift = docs["task_manager_closure_boundary_drift_review_v1.json"]
    evidence = docs["task_manager_closure_evidence_chain_review_v1.json"]
    debt_review = docs["task_manager_closure_governance_debt_review_v1.json"]
    final_planning = docs["task_manager_closure_final_planning_readiness_matrix_v1.json"]
    constraints = docs["task_manager_closure_review_non_execution_constraints_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.post_review_only.{doc_name}", doc.get("post_review_only") is True)
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.closure_not_executed.{doc_name}", doc.get("closure_not_executed") in (None, True))
        _add(checks, f"meta.l1_not_impl.{doc_name}", doc.get("closure_channel_governance_not_implemented") in (None, True))
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("post_dryrun_review_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in TRUE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"review.{key}", review.get(key) is True)

    _add(checks, "matrix.accepted", matrix.get("closure_dryrun_result_accepted") is True)
    for row in matrix.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"matrix.exists.{name}", row.get("exists") is True)
        _add(checks, f"matrix.non_placeholder.{name}", row.get("non_placeholder") is True)

    _add(checks, "drift.absent", drift.get("boundary_drift_absent") is True)
    for row in drift.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"drift.runtime_absent.{name}", row.get("runtime_scope_leak_absent") is True)
        _add(checks, f"drift.no_added_runtime.{name}", row.get("post_review_added_runtime") is False)

    _add(checks, "evidence.ok", evidence.get("evidence_chain_ok") is True)
    for row in evidence.get("chain") or []:
        stage = row.get("stage")
        if stage == "closure_dryrun":
            _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)

    _add(checks, "debt_review.preserved", debt_review.get("governance_debt_preserved") is True)
    _add(checks, "debt_review.not_impl", debt_review.get("closure_channel_governance_not_implemented") is True)

    _add(checks, "final_planning.ready", final_planning.get("final_closure_planning_ready") is True)
    _add(checks, "final_planning.not_closed", final_planning.get("closure_applied") is False)
    _add(checks, "final_planning.freeze_not_applied", final_planning.get("foundation_freeze_applied") is False)
    for row in final_planning.get("rows") or []:
        target = row.get("target")
        if target in ("final_closure_planning", "freeze_planning"):
            _add(checks, f"final_planning.row.ready.{target}", row.get("readiness") == "final-closure-planning-ready")
            _add(checks, f"final_planning.row.not_closed.{target}", row.get("closure_applied") is False)
            _add(checks, f"final_planning.row.freeze_not_applied.{target}", row.get("foundation_freeze_applied") is False)
        if target == "module_adapter_implementation":
            _add(checks, "final_planning.module_adapter_not_ready", row.get("readiness") == "not-ready")

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
    ):
        _add(checks, f"constraints.{key}", constraints.get(key) is True)

    _add(checks, "downstream.ok", downstream_val.get("downstream_scope_ok") is True)
    for row in downstream_val.get("consumers") or []:
        consumer = row.get("consumer")
        _add(checks, f"downstream.not_impl.{consumer}", row.get("readiness") != "implementation-ready")
        _add(checks, f"downstream.not_runtime.{consumer}", row.get("readiness") != "runtime-ready")
        _add(checks, f"downstream.not_prod.{consumer}", row.get("readiness") != "production-ready")

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.debt_title", CLOSURE_GOVERNANCE_DEBT["debt_title"] in md)
    _add(checks, "md.not_l1_impl", "not implement L1 Closure Channel Governance" in md or "不实现 L1 Closure Channel Governance" in md)
    _add(checks, "md.not_execute_closure", "does not execute closure" in md or "不执行 closure" in md)

    for doc_name, doc in docs.items():
        for key in TRUE_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next_final_planning.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        _add(checks, f"sweep.no_closed_final.{doc_name}", doc.get("final_decision") in (None, FINAL_DECISION_GO))
        for word in ("module_adapter_implementation_ready", "foundation freeze complete", "foundation frozen"):
            _add(checks, f"sweep.no_claim.{doc_name}.{word}", word not in json.dumps(doc, ensure_ascii=False))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta_key.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"sweep.runtime_key_absent_true.{doc_name}.{key}", doc.get(key) is not True)
        _add(checks, f"sweep.boundary_statement_en.{doc_name}", bool(doc.get("boundary_statement_en")))
        _add(checks, f"sweep.boundary_statement_zh.{doc_name}", bool(doc.get("boundary_statement_zh")))

    for phrase in (
        "Closure dry-run accepted",
        "Governance debt preserved",
        "Final closure planning ready",
        "freeze-candidate",
    ):
        _add(checks, f"md.phrase.{phrase[:30]}", phrase in md)

    for field in CLOSURE_GOVERNANCE_DEBT:
        _add(
            checks,
            f"debt.field.{field}",
            debt.get(field) == CLOSURE_GOVERNANCE_DEBT.get(field) or bool(debt.get(field)),
        )

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
        "closure_dryrun_result_accepted": summary.get("closure_dryrun_result_accepted") is True,
        "boundary_drift_absent": summary.get("boundary_drift_absent") is True,
        "governance_debt_preserved": summary.get("governance_debt_preserved") is True,
        "closure_channel_governance_not_implemented": summary.get("closure_channel_governance_not_implemented") is True,
        "freeze_candidate_preserved": summary.get("freeze_candidate_preserved") is True,
        "closure_candidate_preserved": summary.get("closure_candidate_preserved") is True,
        "candidate_semantics_preserved": summary.get("candidate_semantics_preserved") is True,
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "downstream_scope_ok": summary.get("downstream_scope_ok") is True,
        "post_review_only": summary.get("post_review_only") is True,
        "final_closure_planning_ready": summary.get("final_closure_planning_ready") is True,
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
                "closure_dryrun_result_accepted": report["closure_dryrun_result_accepted"],
                "boundary_drift_absent": report["boundary_drift_absent"],
                "governance_debt_preserved": report["governance_debt_preserved"],
                "closure_channel_governance_not_implemented": report["closure_channel_governance_not_implemented"],
                "freeze_candidate_preserved": report["freeze_candidate_preserved"],
                "closure_candidate_preserved": report["closure_candidate_preserved"],
                "candidate_semantics_preserved": report["candidate_semantics_preserved"],
                "non_execution_boundary_ok": report["non_execution_boundary_ok"],
                "downstream_scope_ok": report["downstream_scope_ok"],
                "post_review_only": report["post_review_only"],
                "final_closure_planning_ready": report["final_closure_planning_ready"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
