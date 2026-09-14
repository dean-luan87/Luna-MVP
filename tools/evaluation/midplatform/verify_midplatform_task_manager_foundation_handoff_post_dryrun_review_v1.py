#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Post-DryRun Review v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_foundation_handoff_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT,
    DRYRUN_ARTIFACTS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_post_dryrun_review_v1.json",
    "task_manager_foundation_handoff_post_dryrun_review_v1.md",
    "task_manager_handoff_dryrun_review_matrix_v1.json",
    "task_manager_handoff_boundary_drift_review_v1.json",
    "task_manager_handoff_evidence_chain_review_v1.json",
    "task_manager_handoff_closure_readiness_matrix_v1.json",
    "task_manager_handoff_review_non_execution_constraints_v1.json",
    "summary.json",
)
TRUE_KEYS: Tuple[str, ...] = (
    "dryrun_result_accepted",
    "boundary_drift_absent",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_scope_ok",
    "foundation_not_frozen",
    "post_review_only",
    "closure_planning_ready",
)
FORBIDDEN_WORDS: Tuple[str, ...] = (
    "implementation-ready",
    "runtime-ready",
    "production-ready",
    "foundation_frozen",
    "foundation_finalized",
    "production_ready",
)
RUNTIME_FORBIDDEN_KEYS: Tuple[str, ...] = (
    "runtime_executor_created_now",
    "scheduler_binding_created_now",
    "task_execution_authority_granted_now",
    "output_authorization_granted_now",
    "module_adapter_integration_created_now",
    "information_channel_governance_implemented_now",
    "protocol_governance_implemented_now",
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
    parser.add_argument("--dryrun-root", default=DEFAULT_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.dryrun_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_post_dryrun_review_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    _add(checks, "dryrun.summary_go", dryrun_summary.get("final_decision") == DRYRUN_FINAL_GO)
    _add(checks, "dryrun.verifier_go", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "dryrun.passed_min", int(dryrun_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "dryrun.failed_zero", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "dryrun.blocker_zero", dryrun_verifier.get("blocker_count") == 0)
    for key in ("handoff_package_integrity_ok", "evidence_traceability_ok", "candidate_semantics_preserved", "non_execution_boundary_ok", "downstream_scope_ok", "foundation_not_frozen", "dryrun_only"):
        _add(checks, f"dryrun.summary.{key}", dryrun_summary.get(key) is True)
        _add(checks, f"dryrun.verifier.{key}", dryrun_verifier.get(key) is True)
    for artifact in DRYRUN_ARTIFACTS:
        path = dryrun / artifact
        _add(checks, f"dryrun.artifact.exists.{artifact}", path.is_file())
        if artifact.endswith(".json"):
            dryrun_doc = _read(path)
            _add(checks, f"dryrun.artifact.non_placeholder.{artifact}", bool(dryrun_doc))
            _add(checks, f"dryrun.artifact.runtime.{artifact}", dryrun_doc.get("runtime_status") in (None, "not_enabled"))
            _add(checks, f"dryrun.artifact.not_frozen.{artifact}", dryrun_doc.get("foundation_not_frozen") in (None, True))
            _add(checks, f"dryrun.artifact.dryrun_only.{artifact}", dryrun_doc.get("dryrun_only") in (None, True))
            if artifact != "verifier_report.json":
                for word in FORBIDDEN_WORDS:
                    _add(checks, f"dryrun.artifact.no_word.{artifact}.{word}", word not in json.dumps(dryrun_doc, ensure_ascii=False))
        else:
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
            _add(checks, f"dryrun.artifact.non_placeholder.{artifact}", len(text.strip()) > 200)

    review = docs["task_manager_foundation_handoff_post_dryrun_review_v1.json"]
    matrix = docs["task_manager_handoff_dryrun_review_matrix_v1.json"]
    drift = docs["task_manager_handoff_boundary_drift_review_v1.json"]
    evidence = docs["task_manager_handoff_evidence_chain_review_v1.json"]
    closure = docs["task_manager_handoff_closure_readiness_matrix_v1.json"]
    constraints = docs["task_manager_handoff_review_non_execution_constraints_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.post_review_only.{doc_name}", doc.get("post_review_only") is True)
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") is True)
        for key in RUNTIME_FORBIDDEN_KEYS:
            _add(checks, f"meta.no_runtime_key.{doc_name}.{key}", doc.get(key) is not True)
        dumped = json.dumps(doc, ensure_ascii=False)
        for word in FORBIDDEN_WORDS:
            _add(checks, f"meta.no_forbidden_word.{doc_name}.{word}", word not in dumped)

    _add(checks, "summary.pass", summary.get("post_dryrun_review_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in TRUE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"review.{key}", review.get(key) is True)

    _add(checks, "matrix.accepted", matrix.get("dryrun_result_accepted") is True)
    for row in matrix.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"matrix.exists.{name}", row.get("exists") is True)
        _add(checks, f"matrix.non_placeholder.{name}", row.get("non_placeholder") is True)

    _add(checks, "drift.absent", drift.get("boundary_drift_absent") is True)
    _add(checks, "drift.not_frozen", drift.get("foundation_not_frozen") is True)
    for row in drift.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"drift.status_absent.{name}", row.get("forbidden_status_absent") is True)
        _add(checks, f"drift.runtime_absent.{name}", row.get("runtime_scope_leak_absent") is True)
        _add(checks, f"drift.no_added_runtime.{name}", row.get("post_review_added_runtime") is False)

    _add(checks, "evidence.ok", evidence.get("evidence_chain_ok") is True)
    for row in evidence.get("rows") or []:
        _add(checks, f"evidence.referenced.{row.get('evidence_key')}", row.get("referenced") is True)

    _add(checks, "closure.ready", closure.get("closure_planning_ready") is True)
    _add(checks, "closure.not_closed", closure.get("closed") is False)
    _add(checks, "closure.freeze_not_applied", closure.get("foundation_freeze_applied") is False)
    for row in closure.get("rows") or []:
        target = row.get("target")
        if target != "module_adapter_implementation":
            _add(checks, f"closure.row.ready.{target}", row.get("readiness") == "closure-planning-ready")
        _add(checks, f"closure.row.not_closed.{target}", row.get("closed") is False)
        _add(checks, f"closure.row.freeze_not_applied.{target}", row.get("foundation_freeze_applied") is False)
    _add(
        checks,
        "closure.no_module_adapter_impl",
        any(row.get("target") == "module_adapter_implementation" and row.get("readiness") == "not-ready" for row in closure.get("rows") or []),
    )

    for key in (
        "non_execution_boundary_ok",
        "candidate_semantics_preserved",
        "no_runtime_executor",
        "no_scheduler_binding",
        "no_task_execution_authority",
        "no_output_authorization",
        "no_memory_worldmodel_write_path",
        "no_module_adapter_integration",
        "no_information_channel_governance_implementation",
        "no_protocol_governance_implementation",
    ):
        _add(checks, f"constraints.{key}", constraints.get(key) is True)

    _add(checks, "md.non_empty", len(md.strip()) > 200)
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.no_close", "does not close, freeze, or execute" in md)

    for doc_name, doc in docs.items():
        for key in TRUE_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.final_scope.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        _add(checks, f"sweep.no_closed_final.{doc_name}", doc.get("final_decision") in (None, FINAL_DECISION_GO))
        for word in ("module_adapter_implementation_ready", "foundation freeze complete", "foundation frozen"):
            _add(checks, f"sweep.no_claim.{doc_name}.{word}", word not in json.dumps(doc, ensure_ascii=False))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta_key.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN_KEYS:
            _add(checks, f"sweep.runtime_key_absent_true.{doc_name}.{key}", doc.get(key) is not True)
        _add(checks, f"sweep.boundary_statement_en.{doc_name}", bool(doc.get("boundary_statement_en")))
        _add(checks, f"sweep.boundary_statement_zh.{doc_name}", bool(doc.get("boundary_statement_zh")))

    for phrase in (
        "Dry-run accepted",
        "Boundary drift absent",
        "Closure planning ready",
        "does not close, freeze, or execute",
    ):
        _add(checks, f"md.phrase.{phrase}", phrase in md)

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
        "dryrun_result_accepted": summary.get("dryrun_result_accepted") is True,
        "boundary_drift_absent": summary.get("boundary_drift_absent") is True,
        "candidate_semantics_preserved": summary.get("candidate_semantics_preserved") is True,
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "downstream_scope_ok": summary.get("downstream_scope_ok") is True,
        "foundation_not_frozen": summary.get("foundation_not_frozen") is True,
        "post_review_only": summary.get("post_review_only") is True,
        "closure_planning_ready": summary.get("closure_planning_ready") is True,
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
                "dryrun_result_accepted": report["dryrun_result_accepted"],
                "boundary_drift_absent": report["boundary_drift_absent"],
                "candidate_semantics_preserved": report["candidate_semantics_preserved"],
                "non_execution_boundary_ok": report["non_execution_boundary_ok"],
                "downstream_scope_ok": report["downstream_scope_ok"],
                "foundation_not_frozen": report["foundation_not_frozen"],
                "post_review_only": report["post_review_only"],
                "closure_planning_ready": report["closure_planning_ready"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
