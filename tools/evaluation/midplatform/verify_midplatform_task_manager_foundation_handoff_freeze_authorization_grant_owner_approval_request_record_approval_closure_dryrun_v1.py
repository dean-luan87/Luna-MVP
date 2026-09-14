#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Record Approval Closure Lightweight Compliance DryRun v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import (
    FILE_SIZE_GOVERNANCE_REVIEW_KEYS,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1 import (
    BOUNDARY_STATEMENTS,
    CANDIDATE_BOUNDARY_PAIRS,
    CORE_CANDIDATE_IDS,
    DEFAULT_OUTPUT,
    DEFAULT_RECORD_APPROVAL_CLOSURE_PLANNING_ROOT,
    DRYRUN_ARTIFACTS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    PLANNING_MATRIX_FILES,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1 import (
    CHAIN_EVIDENCE_NODES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    LIGHTWEIGHT_PROTOCOL_REFS,
)

MIN_CHECKS = 420
REQUIRED_JSON = tuple(n for n in DRYRUN_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json")
ABSENCE_KEYS: Tuple[str, ...] = (
    "request_issued_absent",
    "notification_sent_absent",
    "request_record_absent",
    "approval_record_absent",
    "ack_record_absent",
    "evidence_bound_record_absent",
    "authorization_request_absent",
    "grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "runtime_execution_absent",
    "protocol_runtime_absent",
    "whitebox_runtime_integration_absent",
    "module_adapter_implementation_absent",
)
FILE_SIZE_SUMMARY_KEYS: Tuple[str, ...] = (
    "file_size_governance_review_exists",
    "file_size_governance_review_ok",
    "monolithic_file_absent",
    "large_file_read_avoidance_ok",
    "summary_index_first_reading_ok",
    "verifier_large_file_scan_absent",
    "full_repo_scan_absent",
    "tmp_eval_out_scan_absent",
    "limited_directory_scan_ok",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def _expect_false(checks: List[Dict[str, Any]], check_id: str, value: Any) -> None:
    _add(checks, check_id, value is False)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--record-approval-closure-planning-root", default=DEFAULT_RECORD_APPROVAL_CLOSURE_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.record_approval_closure_planning_root)
    checks: List[Dict[str, Any]] = []

    planning_summary = _read(planning / "summary.json")
    planning_verifier = _read(planning / "verifier_report.json")
    docs = {name: _read(root / name) for name in REQUIRED_JSON}
    md = (root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_report_v1.md").read_text(encoding="utf-8") if (root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_report_v1.md").is_file() else ""
    summary = docs["summary.json"]

    for name in DRYRUN_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        _add(checks, f"artifact.exists.{name}", path.is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(path)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 80)

    _add(checks, "planning.summary.exists", bool(planning_summary))
    _add(checks, "planning.verifier.exists", bool(planning_verifier))
    _add(checks, "planning.summary_go", planning_summary.get("final_decision") == PLANNING_FINAL_GO)
    _add(checks, "planning.verifier_go", planning_verifier.get("verifier") == "GO")
    _add(checks, "planning.passed_min", int(planning_verifier.get("passed_checks", 0)) >= MIN_CHECKS)
    _add(checks, "planning.failed_zero", planning_verifier.get("failed_checks") == 0)
    _add(checks, "planning.blocker_zero", planning_verifier.get("blocker_count") == 0)

    for fname in PLANNING_MATRIX_FILES:
        _add(checks, f"planning.matrix.exists.{fname}", (planning / fname).is_file())
        _add(checks, f"planning.matrix.non_placeholder.{fname}", bool(_read(planning / fname)))

    candidate_val = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_validation_v1.json"]
    matrix_val = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_matrix_validation_v1.json"]
    trace_val = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_validation_v1.json"]
    absence_val = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_validation_v1.json"]
    boundary_val = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_validation_v1.json"]
    debt_val = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_validation_v1.json"]
    post_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_review_readiness_v1.json"]
    file_size_review = docs["file_size_governance_review_v1.json"]

    _add(checks, "summary.lightweight", summary.get("lightweight_compliance_dryrun_only") is True)
    _add(checks, "summary.pass", summary.get("dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.scope", summary.get("scope") == SCOPE)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)

    for key in GO_CONDITIONS_KEYS:
        if key in (
            "shared_protocol_system_revalidation",
            "l1_input_output_protocol_revalidation",
            "protocol_migration",
            "whitebox_runtime_integration",
        ):
            _expect_false(checks, f"summary.{key}", summary.get(key))
        else:
            _add(checks, f"summary.{key}", summary.get(key) is True)

    for cid in CORE_CANDIDATE_IDS:
        row = next((r for r in candidate_val.get("candidates") or [] if r.get("candidate_id") == cid), {})
        _add(checks, f"candidate.exists.{cid}", bool(row))
        _add(checks, f"candidate.still_candidate.{cid}", row.get("still_candidate") is True)
        _add(checks, f"candidate.not_created.{cid}", row.get("record_created") is False)
        _add(checks, f"candidate.closure_not_executed.{cid}", row.get("closure_executed") is False)

    for candidate, forbidden in CANDIDATE_BOUNDARY_PAIRS:
        _add(checks, f"boundary.pair.{candidate}", candidate != forbidden)

    _add(checks, "candidate.validation_ok", candidate_val.get("candidate_validation_ok") is True)
    _add(checks, "matrix.validation_ok", matrix_val.get("matrix_validation_ok") is True)
    for row in matrix_val.get("rows") or []:
        fname = row.get("file")
        _add(checks, f"matrix.row.exists.{fname}", row.get("exists") is True)
        _add(checks, f"matrix.row.non_placeholder.{fname}", row.get("non_placeholder") is True)

    _add(checks, "trace.validation_ok", trace_val.get("traceability_reference_validation_ok") is True)
    _add(checks, "trace.chain_present", bool(trace_val.get("chain")))
    _expect_false(checks, "trace.no_shared_revalidation", trace_val.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "trace.no_l1_revalidation", trace_val.get("l1_input_output_protocol_revalidation"))
    for ref in trace_val.get("protocol_refs") or []:
        pid = ref.get("protocol_id")
        _add(checks, f"trace.protocol.lightweight.{pid}", ref.get("reference_mode") == "lightweight")
    for pid in LIGHTWEIGHT_PROTOCOL_REFS:
        _add(
            checks,
            f"trace.protocol.contains.{pid}",
            any(r.get("protocol_id") == pid for r in trace_val.get("protocol_refs") or []),
        )
    for stage in CHAIN_EVIDENCE_NODES:
        row = next((r for r in trace_val.get("chain") or [] if r.get("stage") == stage), {})
        if stage == "freeze_authorization_grant_owner_approval_request_record_approval_closure_planning":
            _add(checks, f"trace.chain.linked.{stage}", row.get("linked") is True)
        else:
            _add(checks, f"trace.chain.declared.{stage}", bool(row.get("stage")))
    dryrun_stage = "freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun"
    dryrun_row = next((r for r in trace_val.get("chain") or [] if r.get("stage") == dryrun_stage), {})
    _add(checks, "trace.dryrun.linked", dryrun_row.get("linked") is True)
    _add(checks, "trace.dryrun.no_request", dryrun_row.get("authorization_request_issued") is False)
    _add(checks, "trace.dryrun.no_record", dryrun_row.get("request_record") is False)
    _add(checks, "trace.dryrun.no_closure", dryrun_row.get("closure_executed") is False)

    _add(checks, "absence.validation_ok", absence_val.get("absence_validation_ok") is True)
    for key in ABSENCE_KEYS:
        _add(checks, f"absence.{key}", absence_val.get(key) is True)

    _add(checks, "boundary.validation_ok", boundary_val.get("boundary_validation_ok") is True)
    _add(checks, "boundary.closure_candidate_ne_executed", boundary_val.get("closure_candidate_ne_closure_executed") is True)
    for stmt in BOUNDARY_STATEMENTS:
        _add(checks, f"boundary.stmt.{stmt[:40]}", stmt in (boundary_val.get("statements") or []))

    _add(checks, "debt.preserved", debt_val.get("governance_debt_preserved") is True)
    debts = debt_val.get("debts") or []
    _add(checks, "debt.count", len(debts) >= 2)
    if debts:
        _add(checks, "debt0.must_not_impl", debts[0].get("must_not_implement_now") is True)
        _add(checks, "debt0.title", debts[0].get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"])
    if len(debts) > 1:
        _add(checks, "debt1.must_not_impl", debts[1].get("must_not_implement_now") is True)

    _add(checks, "post_review.ok", post_review.get("post_review_readiness_ok") is True)
    _add(checks, "post_review.next", post_review.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(
        checks,
        "post_review.target",
        post_review.get("target") == "freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review",
    )

    _add(checks, "lineage.ok", summary.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.ok", docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_template_lineage_v1.json"].get("template_lineage_ok") is True)

    for key in FILE_SIZE_SUMMARY_KEYS:
        _add(checks, f"file_size.summary.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size_review.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size_review.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.phase_file.exists.{rel.split('/')[-1]}", row.get("exists") is True)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.lightweight", "Lightweight compliance" in md or "lightweight" in md.lower())
    _add(checks, "md.no_shared_revalidation", "shared_protocol_system_revalidation: `false`" in md)
    _add(checks, "md.no_l1_revalidation", "l1_input_output_protocol_revalidation: `false`" in md)

    report = docs["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_report_v1.json"]
    validation_docs = (
        candidate_val,
        matrix_val,
        trace_val,
        absence_val,
        boundary_val,
        debt_val,
        post_review,
        report,
    )
    for idx, doc in enumerate(validation_docs):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.lightweight", doc.get("lightweight_compliance_dryrun_only") is True)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")
        for key in GO_CONDITIONS_KEYS:
            if key not in doc:
                continue
            if key in (
                "shared_protocol_system_revalidation",
                "l1_input_output_protocol_revalidation",
                "protocol_migration",
                "whitebox_runtime_integration",
            ):
                _expect_false(checks, f"doc{idx}.{key}", doc.get(key))
            else:
                _add(checks, f"doc{idx}.{key}", doc.get(key) is True)

    for key in ABSENCE_KEYS:
        _add(checks, f"planning.absence.{key}", planning_summary.get(key) is True)
        _add(checks, f"summary.absence.{key}", summary.get(key) is True)

    planning_completion_keys = (
        "record_approval_closure_plan_complete",
        "record_candidate_closure_matrix_complete",
        "approval_candidate_closure_matrix_complete",
        "ack_candidate_closure_matrix_complete",
        "evidence_binding_closure_matrix_complete",
        "traceability_matrix_complete",
        "protocol_reference_matrix_ok",
        "non_execution_boundary_ok",
        "planning_pass",
        "next_phase_readiness_ok",
    )
    for key in planning_completion_keys:
        _add(checks, f"planning.completion.{key}", planning_summary.get(key) is True)

    go_conditions = summary.get("go_conditions") or {}
    for key in GO_CONDITIONS_KEYS:
        if key in go_conditions:
            if key in (
                "shared_protocol_system_revalidation",
                "l1_input_output_protocol_revalidation",
                "protocol_migration",
                "whitebox_runtime_integration",
            ):
                _expect_false(checks, f"go_conditions.{key}", go_conditions.get(key))
            else:
                _add(checks, f"go_conditions.{key}", go_conditions.get(key) is True)

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"summary.runtime_forbidden.{flag}", summary.get(flag) is not True)

    for rel in GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_WHITELIST_FILES:
        _add(checks, f"whitelist.exists.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for fname in PLANNING_MATRIX_FILES:
        payload = _read(planning / fname)
        _add(checks, f"planning.matrix.meta.phase.{fname}", payload.get("phase") is not None)
        _add(checks, f"planning.matrix.meta.id.{fname}", bool(
            payload.get("matrix_id") or payload.get("validation_id") or payload.get("trace_id")
        ))

    for stmt in BOUNDARY_STATEMENTS:
        _add(checks, f"report.boundary.{stmt[:35]}", stmt in (report.get("boundary_statements") or []))

    for field in (
        "request_issued",
        "notification_sent",
        "request_record_created",
        "approval_record_created",
        "ack_record_created",
        "evidence_bound_record_created",
        "authorization_request_issued",
        "grant_issued",
        "foundation_frozen",
        "closure_executed",
    ):
        _add(checks, f"post_review.{field}_false", post_review.get(field) is False)

    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "summary.dryrun_pass", summary.get("dryrun_pass") is True)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "candidate.core_count", len(candidate_val.get("core_candidate_ids") or []) == 5)
    _add(checks, "matrix.row_count", len(matrix_val.get("rows") or []) == len(PLANNING_MATRIX_FILES))
    _add(checks, "file_size.phase_id", file_size_review.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.read_strategy", file_size_review.get("read_strategy") == "summary_index_first")
    _add(checks, "file_size.no_full_scan", file_size_review.get("full_repo_scan") is False)

    lineage = summary.get("template_lineage") or {}
    for key in (
        "template_family",
        "base_phase",
        "upstream_review_phase",
        "reuse_mode",
        "full_repo_scan_allowed",
        "base_template_files_exist",
        "stage_specific_terms_overridden",
    ):
        _add(checks, f"lineage.field.{key}", key in lineage)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "lightweight_compliance_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS if k not in (
            "shared_protocol_system_revalidation",
            "l1_input_output_protocol_revalidation",
            "protocol_migration",
            "whitebox_runtime_integration",
        )},
        "shared_protocol_system_revalidation": summary.get("shared_protocol_system_revalidation") is False,
        "l1_input_output_protocol_revalidation": summary.get("l1_input_output_protocol_revalidation") is False,
        "protocol_migration": summary.get("protocol_migration") is False,
        "whitebox_runtime_integration": summary.get("whitebox_runtime_integration") is False,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
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
                "lightweight_compliance_verifier_only": True,
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
