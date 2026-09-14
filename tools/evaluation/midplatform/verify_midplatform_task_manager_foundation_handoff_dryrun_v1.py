#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff DryRun v1."""

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
    DEFAULT_OUTPUT,
    DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    PLANNING_PACKAGE_FILES,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_dryrun_report_v1.json",
    "task_manager_foundation_handoff_dryrun_report_v1.md",
    "task_manager_handoff_package_integrity_matrix_v1.json",
    "task_manager_handoff_evidence_traceability_matrix_v1.json",
    "task_manager_handoff_downstream_consumption_dryrun_matrix_v1.json",
    "task_manager_handoff_non_execution_verification_v1.json",
    "summary.json",
)
FALSE_FLAGS: Tuple[str, ...] = (
    "task_execution_now",
    "tool_call_now",
    "runtime_enabled_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "module_adapter_mounted_now",
    "real_scheduler_enabled_now",
)
FORBIDDEN_ESCALATIONS: Tuple[str, ...] = (
    "implementation-ready",
    "runtime-ready",
    "production-ready",
    "foundation_frozen",
    "foundation_finalized",
    "production_ready",
    "frozen",
    "finalized",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _contains_forbidden(value: Any) -> bool:
    if isinstance(value, str):
        return value in FORBIDDEN_ESCALATIONS
    if isinstance(value, dict):
        return any(_contains_forbidden(v) for v in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden(v) for v in value)
    return False


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []

    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS if fname.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_dryrun_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""
    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", (root / fname).is_file())

    planning_summary = _read(planning / "summary.json")
    planning_verifier = _read(planning / "verifier_report.json")
    _add(checks, "planning.summary_go", planning_summary.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "planning.verifier_go", planning_verifier.get("verifier") == "GO")
    _add(checks, "planning.blocker0", planning_summary.get("blocker_count") == 0)
    for fname in PLANNING_PACKAGE_FILES:
        path = planning / fname
        _add(checks, f"planning.package.exists.{fname}", path.is_file())
        if fname.endswith(".json"):
            planning_doc = _read(path)
            _add(checks, f"planning.package.non_placeholder.{fname}", bool(planning_doc))
            _add(checks, f"planning.package.runtime.{fname}", planning_doc.get("runtime_status") in (None, "not_enabled"))
            _add(checks, f"planning.package.planning_only.{fname}", planning_doc.get("foundation_handoff_planning_only") in (None, True))
            _add(checks, f"planning.package.no_forbidden_status.{fname}", not _contains_forbidden(planning_doc))
            for flag in FALSE_FLAGS:
                _add(checks, f"planning.package.false.{fname}.{flag}", planning_doc.get(flag) is not True)
        else:
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
            _add(checks, f"planning.package.non_placeholder.{fname}", len(text.strip()) > 200)
            for token in ("task_candidate != task execution", "task_step_candidate != executed step", "task_handoff_candidate != direct mount"):
                _add(checks, f"planning.package.md.token.{token}", token in text)

    report = docs["task_manager_foundation_handoff_dryrun_report_v1.json"]
    integrity = docs["task_manager_handoff_package_integrity_matrix_v1.json"]
    evidence = docs["task_manager_handoff_evidence_traceability_matrix_v1.json"]
    downstream = docs["task_manager_handoff_downstream_consumption_dryrun_matrix_v1.json"]
    non_execution = docs["task_manager_handoff_non_execution_verification_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.dryrun_only.{doc_name}", doc.get("dryrun_only") is True)
        _add(checks, f"meta.not_frozen.{doc_name}", doc.get("foundation_not_frozen") is True)
        _add(checks, f"meta.no_forbidden_status.{doc_name}", not _contains_forbidden(doc))
        for flag in FALSE_FLAGS:
            _add(checks, f"meta.false.{doc_name}.{flag}", doc.get(flag) is not True)

    _add(checks, "summary.pass", summary.get("dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in (
        "handoff_package_integrity_ok",
        "evidence_traceability_ok",
        "candidate_semantics_preserved",
        "non_execution_boundary_ok",
        "downstream_scope_ok",
        "foundation_not_frozen",
        "dryrun_only",
    ):
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"report.{key}", report.get(key) is True)

    _add(checks, "md.non_empty", len(md.strip()) > 200)
    _add(checks, "md.final_decision", FINAL_DECISION_GO in md)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md)

    integrity_rows = integrity.get("rows") or []
    _add(checks, "integrity.ok", integrity.get("handoff_package_integrity_ok") is True)
    for fname in PLANNING_PACKAGE_FILES:
        row = next((item for item in integrity_rows if item.get("file") == fname), {})
        _add(checks, f"integrity.row.exists.{fname}", row.get("exists") is True)
        _add(checks, f"integrity.row.non_placeholder.{fname}", row.get("non_placeholder") is True)
        _add(checks, f"integrity.row.readable.{fname}", row.get("readable") is True)
        _add(checks, f"integrity.row.no_extra_status.{fname}", row.get("status") is None)

    evidence_rows = evidence.get("rows") or []
    _add(checks, "evidence.ok", evidence.get("evidence_traceability_ok") is True)
    for key in ("dryrun_summary", "dryrun_verifier", "post_dryrun_summary", "post_dryrun_verifier"):
        row = next((item for item in evidence_rows if item.get("evidence_key") == key), {})
        _add(checks, f"evidence.row.{key}", row.get("referenced") is True and bool(row.get("path")))
    for rel in (
        "capabilities/midplatform/core/task_manager_types_v1.py",
        "capabilities/midplatform/core/task_manager_skeleton_v1.py",
        "capabilities/midplatform/core/task_manager_static_validators_v1.py",
    ):
        row = next((item for item in evidence_rows if item.get("evidence_key") == rel), {})
        _add(checks, f"evidence.core.{rel}", row.get("referenced") is True and row.get("role") == "core_skeleton_evidence")

    for key in (
        "candidate_semantics_preserved",
        "task_candidate_is_not_task_execution",
        "task_step_candidate_is_not_executed_step",
        "task_handoff_candidate_is_not_direct_mount",
        "non_execution_boundary_ok",
        "constraints_ok",
        "foundation_not_frozen",
        "dryrun_only",
        "no_runtime_executor",
        "no_scheduler_binding",
        "no_task_execution_authority",
        "no_output_authorization",
        "no_memory_worldmodel_write_path",
        "no_module_adapter_integration",
        "no_authorization_grant",
    ):
        _add(checks, f"non_execution.{key}", non_execution.get(key) is True)

    _add(checks, "downstream.scope", downstream.get("downstream_scope_ok") is True)
    _add(checks, "downstream.future_protocol", downstream.get("future_protocol_dependency_ok") is True)
    _add(checks, "downstream.no_implementation", downstream.get("no_implementation_ready") is True)
    _add(checks, "downstream.no_runtime", downstream.get("no_runtime_ready") is True)
    _add(checks, "downstream.no_production", downstream.get("no_production_readiness") is True)
    for row in downstream.get("rows") or []:
        consumer = row.get("consumer")
        _add(checks, f"downstream.impl_false.{consumer}", row.get("implementation_ready") == "false")
        _add(checks, f"downstream.not_runtime_ready.{consumer}", row.get("readiness") != "runtime-ready")
        _add(checks, f"downstream.not_production_ready.{consumer}", row.get("readiness") != "production-ready")
        _add(checks, f"downstream.not_implementation_ready.{consumer}", row.get("readiness") != "implementation-ready")
        _add(checks, f"downstream.not_empty.{consumer}", bool(row.get("readiness")))
        _add(checks, f"downstream.allowed_scope.{consumer}", "ready" in row.get("readiness", "") or "future_l1_protocol" in row.get("readiness", ""))
    _add(
        checks,
        "future.icg.only_dependency",
        any(row.get("consumer") == "information_channel_governance" and row.get("readiness") == "future_l1_protocol_input" for row in downstream.get("rows") or []),
    )
    _add(
        checks,
        "future.protocol.only_dependency",
        any(row.get("consumer") == "protocol_governance" and row.get("readiness") == "future_l1_protocol_dependency" for row in downstream.get("rows") or []),
    )

    # Cross-artifact consistency and no-escalation sweep.
    for doc_name, doc in docs.items():
        _add(checks, f"sweep.decision_not_closed.{doc_name}", doc.get("final_decision") in (None, FINAL_DECISION_GO))
        _add(checks, f"sweep.next_post_review.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        _add(checks, f"sweep.no_runtime_executor.{doc_name}", doc.get("runtime_executor_created_now") is not True)
        _add(checks, f"sweep.no_scheduler_binding.{doc_name}", doc.get("scheduler_binding_created_now") is not True)
        _add(checks, f"sweep.no_task_authority.{doc_name}", doc.get("task_execution_authority_granted_now") is not True)
        _add(checks, f"sweep.no_output_authority.{doc_name}", doc.get("output_authorization_granted_now") is not True)
        _add(checks, f"sweep.no_module_adapter.{doc_name}", doc.get("module_adapter_integration_created_now") is not True)
        _add(checks, f"sweep.no_icg_impl.{doc_name}", doc.get("information_channel_governance_implemented_now") is not True)
        _add(checks, f"sweep.no_protocol_impl.{doc_name}", doc.get("protocol_governance_implemented_now") is not True)
        for key in (
            "handoff_package_integrity_ok",
            "evidence_traceability_ok",
            "candidate_semantics_preserved",
            "non_execution_boundary_ok",
            "downstream_scope_ok",
            "foundation_not_frozen",
            "dryrun_only",
        ):
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        for forbidden_word in ("implementation-ready", "runtime-ready", "production-ready", "foundation_frozen", "foundation_finalized", "production_ready"):
            _add(checks, f"sweep.no_forbidden_word.{doc_name}.{forbidden_word}", forbidden_word not in json.dumps(doc, ensure_ascii=False))
        for expected_key in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta_key.{doc_name}.{expected_key}", expected_key in doc)
        _add(checks, f"sweep.boundary_statement_en.{doc_name}", bool(doc.get("boundary_statement_en")))
        _add(checks, f"sweep.boundary_statement_zh.{doc_name}", bool(doc.get("boundary_statement_zh")))

    for expected_phrase in (
        "handoff_package_integrity_ok",
        "evidence_traceability_ok",
        "candidate_semantics_preserved",
        "non_execution_boundary_ok",
        "downstream_scope_ok",
        "foundation_not_frozen",
        "dryrun_only",
    ):
        _add(checks, f"md.result_phrase.{expected_phrase}", expected_phrase in md)
    for forbidden_phrase in ("foundation finalized", "production-ready", "runtime-ready", "implementation-ready"):
        _add(checks, f"md.no_forbidden_phrase.{forbidden_phrase}", forbidden_phrase not in md)

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
        "handoff_package_integrity_ok": summary.get("handoff_package_integrity_ok") is True,
        "evidence_traceability_ok": summary.get("evidence_traceability_ok") is True,
        "candidate_semantics_preserved": summary.get("candidate_semantics_preserved") is True,
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "downstream_scope_ok": summary.get("downstream_scope_ok") is True,
        "foundation_not_frozen": summary.get("foundation_not_frozen") is True,
        "dryrun_only": summary.get("dryrun_only") is True,
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
                "handoff_package_integrity_ok": report_payload["handoff_package_integrity_ok"],
                "evidence_traceability_ok": report_payload["evidence_traceability_ok"],
                "candidate_semantics_preserved": report_payload["candidate_semantics_preserved"],
                "non_execution_boundary_ok": report_payload["non_execution_boundary_ok"],
                "downstream_scope_ok": report_payload["downstream_scope_ok"],
                "foundation_not_frozen": report_payload["foundation_not_frozen"],
                "dryrun_only": report_payload["dryrun_only"],
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
