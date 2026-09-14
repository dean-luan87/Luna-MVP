#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Record Approval Closure Lightweight Post-DryRun Review v1."""

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
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1 import (
    CANDIDATE_BOUNDARY_PAIRS,
    CORE_CANDIDATE_IDS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
    DEFAULT_OUTPUT,
    DEFAULT_RECORD_APPROVAL_CLOSURE_DRYRUN_ROOT,
    DRYRUN_INDEX_FILES,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    POST_REVIEW_ARTIFACTS,
    SCOPE,
)

MIN_CHECKS = 300
FORBIDDEN_NEXT_TARGETS: Tuple[str, ...] = (
    "request_issued",
    "request_record_created",
    "approval_record_created",
    "grant_issued",
    "foundation_frozen",
    "closure_executed",
    "module_adapter_implementation",
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
    parser.add_argument("--record-approval-closure-dryrun-root", default=DEFAULT_RECORD_APPROVAL_CLOSURE_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.record_approval_closure_dryrun_root)
    checks: List[Dict[str, Any]] = []

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    dryrun_candidate = _read(dryrun / DRYRUN_INDEX_FILES[3])
    dryrun_absence = _read(dryrun / DRYRUN_INDEX_FILES[4])
    dryrun_boundary = _read(dryrun / DRYRUN_INDEX_FILES[5])
    dryrun_trace = _read(dryrun / DRYRUN_INDEX_FILES[6])

    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""
    docs = {
        name: _read(root / name)
        for name in POST_REVIEW_ARTIFACTS
        if name.endswith(".json") and name != "verifier_report.json"
    }
    summary = docs["summary.json"]

    for name in POST_REVIEW_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        _add(checks, f"artifact.exists.{name}", path.is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(path)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 80)

    _add(checks, "dryrun.summary.exists", bool(dryrun_summary))
    _add(checks, "dryrun.verifier.exists", bool(dryrun_verifier))
    _add(checks, "dryrun.summary_go", dryrun_summary.get("final_decision") == DRYRUN_FINAL_GO)
    _add(checks, "dryrun.verifier_go", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "dryrun.passed_min", int(dryrun_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "dryrun.failed_zero", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "dryrun.blocker_zero", dryrun_verifier.get("blocker_count") == 0)
    _add(checks, "dryrun.dryrun_pass", dryrun_summary.get("dryrun_pass") is True)
    _add(checks, "dryrun.lightweight_dryrun", dryrun_summary.get("lightweight_compliance_dryrun_only") is True)
    _add(checks, "dryrun.lightweight_verifier", dryrun_verifier.get("lightweight_compliance_verifier_only") is True)
    _add(checks, "dryrun.file_size_ok", dryrun_summary.get("file_size_governance_review_ok") is True)
    _add(checks, "dryrun.candidate_validation_ok", dryrun_summary.get("candidate_validation_ok") is True)
    _add(checks, "dryrun.absence_validation_ok", dryrun_summary.get("absence_validation_ok") is True)

    for fname in DRYRUN_INDEX_FILES:
        _add(checks, f"dryrun.index.exists.{fname}", (dryrun / fname).is_file())

    dryrun_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_result_review_v1.json"]
    candidate_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_review_v1.json"]
    absence_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_review_v1.json"]
    boundary_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_review_v1.json"]
    trace_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_review_v1.json"]
    debt_review = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_review_v1.json"]
    next_phase = docs["task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_next_phase_readiness_v1.json"]
    file_size_review = docs["file_size_governance_review_v1.json"]
    report = docs["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_report_v1.json"]

    _add(checks, "summary.pass", summary.get("post_review_pass") is True)
    _add(checks, "summary.post_review_only", summary.get("post_review_only") is True)
    _add(checks, "summary.lightweight", summary.get("lightweight_compliance_post_review_only") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.scope", summary.get("scope") == SCOPE)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"report.{key}", report.get(key) is True)

    _add(checks, "dryrun_review.accepted", dryrun_review.get("dryrun_result_accepted") is True)
    _add(checks, "dryrun_review.lightweight_verifier", dryrun_review.get("lightweight_compliance_verifier_only") is True)

    _add(checks, "candidate.review_ok", candidate_review.get("candidate_review_ok") is True)
    for cid in CORE_CANDIDATE_IDS:
        row = next((r for r in candidate_review.get("candidates") or [] if r.get("candidate_id") == cid), {})
        _add(checks, f"candidate.still.{cid}", row.get("still_candidate") is True)
        _add(checks, f"candidate.not_created.{cid}", row.get("record_created") is False)
    for candidate, forbidden in CANDIDATE_BOUNDARY_PAIRS:
        _add(checks, f"boundary.ne.{candidate[:30]}", candidate != forbidden)

    _add(checks, "absence.review_ok", absence_review.get("absence_review_ok") is True)
    for key in ABSENCE_KEYS:
        _add(checks, f"absence.{key}", absence_review.get(key) is True)
        _add(checks, f"summary.absence.{key}", summary.get(key) is True)
        _add(checks, f"dryrun.absence.{key}", dryrun_summary.get(key) is True)

    _add(checks, "boundary.review_ok", boundary_review.get("boundary_review_ok") is True)
    _add(checks, "boundary.closure_ne_executed", boundary_review.get("closure_candidate_ne_closure_executed") is True)

    _add(checks, "trace.review_ok", trace_review.get("traceability_reference_review_ok") is True)
    _expect_false(checks, "trace.no_shared_revalidation", trace_review.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "trace.no_l1_revalidation", trace_review.get("l1_input_output_protocol_revalidation"))
    for ref in trace_review.get("protocol_refs") or []:
        _add(checks, f"trace.ref.lightweight.{ref.get('protocol_id')}", ref.get("reference_mode") == "lightweight")

    _add(checks, "debt.preserved", debt_review.get("governance_debt_preserved") is True)
    _add(checks, "debt0.must_not_impl", GOVERNANCE_DEBTS[0].get("must_not_implement_now") is True)

    _add(checks, "next_phase.ok", next_phase.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next_phase.target", next_phase.get("target") == "freeze_authorization_grant_owner_approval_request_final_gate_planning")
    for field in (
        "request_issued",
        "notification_sent",
        "request_record_created",
        "approval_record_created",
        "grant_issued",
        "foundation_frozen",
        "closure_executed",
    ):
        _add(checks, f"next_phase.{field}_false", next_phase.get(field) is False)
    for forbidden in FORBIDDEN_NEXT_TARGETS:
        _add(checks, f"next_phase.not_{forbidden}", forbidden not in (next_phase.get("recommended_next_phase") or "").lower())

    for key in FILE_SIZE_SUMMARY_KEYS:
        _add(checks, f"file_size.summary.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size_review.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size_review.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.phase_file.{rel.split('/')[-1]}", row.get("exists") is True)

    for rel in GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"summary.no_runtime.{flag}", summary.get(flag) is not True)

    _add(checks, "upstream.candidate_ok", dryrun_candidate.get("candidate_validation_ok") is True)
    _add(checks, "upstream.absence_ok", dryrun_absence.get("absence_validation_ok") is True)
    _add(checks, "upstream.boundary_ok", dryrun_boundary.get("boundary_validation_ok") is True)
    _add(checks, "upstream.trace_ok", dryrun_trace.get("traceability_reference_validation_ok") is True)

    review_docs = (dryrun_review, candidate_review, absence_review, boundary_review, trace_review, debt_review, next_phase, report)
    for idx, doc in enumerate(review_docs):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.post_review_only", doc.get("post_review_only") is True)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")
        for key in GO_CONDITIONS_KEYS:
            if key in doc:
                _add(checks, f"doc{idx}.{key}", doc.get(key) is True)

    for key in ABSENCE_KEYS:
        _add(checks, f"dryrun_val.absence.{key}", dryrun_absence.get(key) is True)

    for cid in CORE_CANDIDATE_IDS:
        row = next((r for r in dryrun_candidate.get("candidates") or [] if r.get("candidate_id") == cid), {})
        _add(checks, f"upstream.candidate.{cid}.still", row.get("still_candidate") is True)

    lineage = summary.get("template_lineage") or {}
    for key in (
        "template_lineage_ok",
        "base_template_files_exist",
        "full_repo_scan_allowed",
        "reuse_mode",
        "stage_specific_terms_overridden",
    ):
        _add(checks, f"lineage.{key}", key in lineage or summary.get("template_lineage_ok") is True)

    _add(checks, "summary.template_lineage_ok", summary.get("template_lineage_ok") is True)
    _add(checks, "summary.dryrun_result_accepted", summary.get("dryrun_result_accepted") is True)
    _add(checks, "summary.prior_dryrun_go", summary.get("prior_record_approval_closure_dryrun_go") is True)
    _add(checks, "report.final_match", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "next_phase.final_gate", "Final-Gate-Planning" in (next_phase.get("recommended_next_phase") or ""))

    for pair in candidate_review.get("boundary_pairs") or []:
        c = pair.get("candidate")
        f = pair.get("forbidden_final")
        _add(checks, f"review.boundary.{c[:25]}", c != f)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.lightweight", "Lightweight" in md)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "lightweight_compliance_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
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
                "dryrun_result_accepted": report_payload.get("dryrun_result_accepted"),
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
