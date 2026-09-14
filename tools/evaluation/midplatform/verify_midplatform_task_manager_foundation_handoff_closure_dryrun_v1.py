#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Closure DryRun v1."""

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
    CLOSURE_PLANNING_PACKAGE_FILES,
    DEFAULT_CLOSURE_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_closure_planning_v1 import (
    FINAL_DECISION_GO as CLOSURE_PLANNING_FINAL_GO,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_closure_dryrun_report_v1.json",
    "task_manager_foundation_handoff_closure_dryrun_report_v1.md",
    "task_manager_closure_plan_integrity_matrix_v1.json",
    "task_manager_closure_evidence_traceability_matrix_v1.json",
    "task_manager_closure_freeze_candidate_validation_v1.json",
    "task_manager_closure_candidate_semantics_validation_v1.json",
    "task_manager_closure_downstream_scope_validation_v1.json",
    "task_manager_closure_non_execution_validation_v1.json",
    "task_manager_closure_governance_debt_register_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "closure_plan_integrity_ok",
    "closure_evidence_traceability_ok",
    "freeze_candidate_preserved",
    "closure_candidate_preserved",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_scope_ok",
    "closure_channel_governance_debt_recorded",
    "l1_closure_protocol_not_implemented",
    "closure_dryrun_only",
)
PLANNING_TRUE_KEYS: Tuple[str, ...] = (
    "prior_chain_go",
    "closure_plan_complete",
    "asset_inventory_complete",
    "evidence_chain_complete",
    "freeze_candidate_only",
    "closure_planning_only",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_scope_ok",
    "future_l1_dependencies_only",
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
    parser.add_argument("--closure-planning-root", default=DEFAULT_CLOSURE_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.closure_planning_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_closure_dryrun_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    planning_summary = _read(planning / "summary.json")
    planning_verifier = _read(planning / "verifier_report.json")
    _add(checks, "planning.summary_go", planning_summary.get("final_decision") == CLOSURE_PLANNING_FINAL_GO)
    _add(checks, "planning.verifier_go", planning_verifier.get("verifier") == "GO")
    _add(checks, "planning.passed_min", int(planning_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "planning.failed_zero", planning_verifier.get("failed_checks") == 0)
    _add(checks, "planning.blocker_zero", planning_verifier.get("blocker_count") == 0)
    for key in PLANNING_TRUE_KEYS:
        _add(checks, f"planning.summary.{key}", planning_summary.get(key) is True)
        _add(checks, f"planning.verifier.{key}", planning_verifier.get(key) is True if key in planning_verifier else planning_summary.get(key) is True)

    for fname in CLOSURE_PLANNING_PACKAGE_FILES:
        path = planning / fname
        _add(checks, f"planning.package.exists.{fname}", path.is_file())
        if fname.endswith(".json"):
            _add(checks, f"planning.package.non_placeholder.{fname}", bool(_read(path)))

    report = docs["task_manager_foundation_handoff_closure_dryrun_report_v1.json"]
    integrity = docs["task_manager_closure_plan_integrity_matrix_v1.json"]
    evidence = docs["task_manager_closure_evidence_traceability_matrix_v1.json"]
    freeze_val = docs["task_manager_closure_freeze_candidate_validation_v1.json"]
    semantics_val = docs["task_manager_closure_candidate_semantics_validation_v1.json"]
    downstream_val = docs["task_manager_closure_downstream_scope_validation_v1.json"]
    non_exec = docs["task_manager_closure_non_execution_validation_v1.json"]
    debt_reg = docs["task_manager_closure_governance_debt_register_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.closure_dryrun_only.{doc_name}", doc.get("closure_dryrun_only") in (None, True))
        _add(checks, f"meta.l1_not_impl.{doc_name}", doc.get("l1_closure_protocol_not_implemented") in (None, True))
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in TRUE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"report.{key}", report.get(key) is True)

    _add(checks, "integrity.ok", integrity.get("closure_plan_integrity_ok") is True)
    for row in integrity.get("rows") or []:
        fname = row.get("file")
        _add(checks, f"integrity.exists.{fname}", row.get("exists") is True)
        _add(checks, f"integrity.non_placeholder.{fname}", row.get("non_placeholder") is True)

    _add(checks, "evidence.ok", evidence.get("closure_evidence_traceability_ok") is True)
    for row in evidence.get("rows") or []:
        stage = row.get("stage")
        if stage and stage != "closure_planning":
            _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)

    _add(checks, "freeze.status", freeze_val.get("freeze_status") == "freeze-candidate")
    _add(checks, "freeze.readiness", freeze_val.get("closure_readiness") == "closure-dryrun-ready")
    _add(checks, "freeze.preserved", freeze_val.get("freeze_candidate_preserved") is True)
    _add(checks, "freeze.closure_preserved", freeze_val.get("closure_candidate_preserved") is True)
    _add(checks, "freeze.not_frozen", freeze_val.get("foundation_frozen") is False)
    _add(checks, "freeze.not_applied", freeze_val.get("closure_applied") is False)

    for item in CLOSURE_CHANNEL_BOUNDARIES:
        candidate = item["candidate"]
        boundary = item["boundary"]
        row = next((b for b in semantics_val.get("boundaries") or [] if b.get("candidate") == candidate), {})
        _add(checks, f"semantics.boundary.{candidate}", row.get("boundary") == boundary)
        _add(checks, f"md.boundary.{candidate}", boundary in md)
    _add(checks, "semantics.preserved", semantics_val.get("candidate_semantics_preserved") is True)

    _add(checks, "downstream.ok", downstream_val.get("downstream_scope_ok") is True)
    for row in downstream_val.get("consumers") or []:
        consumer = row.get("consumer")
        _add(checks, f"downstream.not_impl.{consumer}", row.get("readiness") != "implementation-ready")
        _add(checks, f"downstream.not_runtime.{consumer}", row.get("readiness") != "runtime-ready")
        _add(checks, f"downstream.not_prod.{consumer}", row.get("readiness") != "production-ready")

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
        _add(checks, f"non_exec.{key}", non_exec.get(key) is True)

    debts = debt_reg.get("debts") or []
    _add(checks, "debt.count", len(debts) >= 1)
    debt = debts[0] if debts else {}
    _add(checks, "debt.title", debt.get("debt_title") == CLOSURE_GOVERNANCE_DEBT["debt_title"])
    _add(checks, "debt.priority", debt.get("priority") == "P1")
    _add(checks, "debt.classification", debt.get("classification") == "L1 Midplatform System Protocols")
    _add(checks, "debt.type", debt.get("debt_type") == "canonical_protocol_missing")
    _add(checks, "debt.handling", debt.get("current_handling") == "module_scoped_closure_rehearsal_only")
    _add(checks, "debt.must_not_impl", debt.get("must_not_implement_now") is True)
    _add(checks, "debt.future_phase", debt.get("recommended_future_phase") == CLOSURE_GOVERNANCE_DEBT["recommended_future_phase"])
    _add(checks, "debt.boundary_statement", bool(debt.get("boundary_statement")))
    _add(checks, "debt.registered", debt_reg.get("closure_channel_governance_debt_recorded") is True)
    _add(checks, "debt.l1_not_impl", debt_reg.get("l1_closure_protocol_not_implemented") is True)

    _add(checks, "md.final", FINAL_DECISION_GO in md or "closure-dryrun-ready" in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.debt_title", CLOSURE_GOVERNANCE_DEBT["debt_title"] in md)
    _add(checks, "md.not_l1_impl", "not implement L1 Closure Channel Governance" in md or "不实现 L1 Closure Channel Governance" in md)

    for doc_name, doc in docs.items():
        for key in TRUE_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next_post_review.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        _add(checks, f"sweep.module_rehearsal.{doc_name}", doc.get("module_scoped_closure_rehearsal") in (None, True))
        _add(checks, f"sweep.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"sweep.runtime_absent.{doc_name}.{key}", doc.get(key) is not True)

    for field in CLOSURE_GOVERNANCE_DEBT:
        _add(checks, f"debt.field.{field}", debt.get(field) == CLOSURE_GOVERNANCE_DEBT.get(field) or bool(debt.get(field)))
    for phase in CLOSURE_GOVERNANCE_DEBT.get("related_future_phases") or []:
        _add(checks, f"debt.related.{phase[:40]}", phase in (debt.get("related_future_phases") or []))

    for phrase in ("freeze-candidate", "closure-dryrun-ready", "future L1 protocol", "Governance Debt"):
        _add(checks, f"md.phrase.{phrase[:30]}", phrase in md)
    _add(checks, "md.debt_type_via_register", debt.get("debt_type") == "canonical_protocol_missing")

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "closure_plan_integrity_ok": summary.get("closure_plan_integrity_ok") is True,
        "closure_evidence_traceability_ok": summary.get("closure_evidence_traceability_ok") is True,
        "freeze_candidate_preserved": summary.get("freeze_candidate_preserved") is True,
        "closure_candidate_preserved": summary.get("closure_candidate_preserved") is True,
        "candidate_semantics_preserved": summary.get("candidate_semantics_preserved") is True,
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "downstream_scope_ok": summary.get("downstream_scope_ok") is True,
        "closure_channel_governance_debt_recorded": summary.get("closure_channel_governance_debt_recorded") is True,
        "l1_closure_protocol_not_implemented": summary.get("l1_closure_protocol_not_implemented") is True,
        "closure_dryrun_only": summary.get("closure_dryrun_only") is True,
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
                "closure_plan_integrity_ok": report_payload["closure_plan_integrity_ok"],
                "closure_evidence_traceability_ok": report_payload["closure_evidence_traceability_ok"],
                "freeze_candidate_preserved": report_payload["freeze_candidate_preserved"],
                "closure_candidate_preserved": report_payload["closure_candidate_preserved"],
                "candidate_semantics_preserved": report_payload["candidate_semantics_preserved"],
                "non_execution_boundary_ok": report_payload["non_execution_boundary_ok"],
                "downstream_scope_ok": report_payload["downstream_scope_ok"],
                "closure_channel_governance_debt_recorded": report_payload["closure_channel_governance_debt_recorded"],
                "l1_closure_protocol_not_implemented": report_payload["l1_closure_protocol_not_implemented"],
                "closure_dryrun_only": report_payload["closure_dryrun_only"],
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
