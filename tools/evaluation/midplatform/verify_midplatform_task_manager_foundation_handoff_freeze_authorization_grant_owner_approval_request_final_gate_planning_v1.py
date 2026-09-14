#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Final Gate Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import (
    MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
    REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import (
    FILE_SIZE_GOVERNANCE_REVIEW_KEYS,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
)
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1 import (
    ABSENCE_KEYS,
    CORE_CANDIDATE_IDS,
    DEFAULT_OUTPUT,
    DEFAULT_POST_REVIEW_ROOT,
    FINAL_DECISION_GO,
    FINAL_GATE_ARTIFACTS,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    POST_REVIEW_INDEX_FILES,
    READINESS_DIMENSIONS,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
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
    "real_request_issuance",
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
    parser.add_argument("--record-approval-closure-post-review-root", default=DEFAULT_POST_REVIEW_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    post_review = Path(args.record_approval_closure_post_review_root)
    checks: List[Dict[str, Any]] = []

    post_summary = _read(post_review / "summary.json")
    post_verifier = _read(post_review / "verifier_report.json")
    post_candidate = _read(post_review / POST_REVIEW_INDEX_FILES[3])
    post_absence = _read(post_review / POST_REVIEW_INDEX_FILES[4])

    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""
    docs = {
        name: _read(root / name)
        for name in FINAL_GATE_ARTIFACTS
        if name.endswith(".json") and name != "verifier_report.json"
    }
    summary = docs["summary.json"]

    for name in FINAL_GATE_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        _add(checks, f"artifact.exists.{name}", path.is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(path)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 80)

    _add(checks, "post_review.summary.exists", bool(post_summary))
    _add(checks, "post_review.verifier.exists", bool(post_verifier))
    _add(checks, "post_review.summary_go", post_summary.get("final_decision") == POST_REVIEW_FINAL_GO)
    _add(checks, "post_review.verifier_go", post_verifier.get("verifier") == "GO")
    _add(checks, "post_review.passed_min", int(post_verifier.get("passed_checks", 0)) >= 300)
    _add(checks, "post_review.failed_zero", post_verifier.get("failed_checks") == 0)
    _add(checks, "post_review.blocker_zero", post_verifier.get("blocker_count") == 0)
    _add(checks, "post_review.post_review_pass", post_summary.get("post_review_pass") is True)
    _add(checks, "post_review.lightweight", post_summary.get("lightweight_compliance_post_review_only") is True)
    _add(checks, "post_review.file_size_ok", post_summary.get("file_size_governance_review_ok") is True)

    for fname in POST_REVIEW_INDEX_FILES:
        _add(checks, f"post_review.index.exists.{fname}", (post_review / fname).is_file())

    plan = docs["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan_v1.json"]
    readiness = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_readiness_matrix_v1.json"]
    missing = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_v1.json"]
    blockers = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_blocker_matrix_v1.json"]
    boundary = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_non_execution_boundary_v1.json"]
    governance = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_governance_rule_reference_v1.json"]
    next_phase = docs["task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness_v1.json"]
    module_first = docs["module_first_development_verification_cadence_rule_reference_v1.json"]
    file_size_review = docs["file_size_governance_review_v1.json"]

    _add(checks, "summary.pass", summary.get("final_gate_planning_pass") is True)
    _add(checks, "summary.final_gate_only", summary.get("final_gate_planning_only") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.scope", summary.get("scope") == SCOPE)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"plan.{key}", plan.get(key) is True)

    _add(checks, "plan.complete", plan.get("final_gate_plan_complete") is True)
    _add(checks, "plan.no_real_issuance", plan.get("real_request_issuance_authorized") is False)
    _add(checks, "plan.no_real_record", plan.get("real_record_creation_authorized") is False)

    _add(checks, "readiness.complete", readiness.get("final_gate_readiness_matrix_complete") is True)
    for dim in READINESS_DIMENSIONS:
        row = next((r for r in readiness.get("rows") or [] if r.get("dimension_id") == dim), {})
        _add(checks, f"readiness.dim.{dim}", bool(row))

    _add(checks, "missing.complete", missing.get("missing_conditions_matrix_complete") is True)
    for cat in ("blocker", "non_blocking", "future_runtime", "governance_debt"):
        _add(
            checks,
            f"missing.category.{cat}",
            any(c.get("category") == cat for c in missing.get("conditions") or []),
        )

    _add(checks, "blockers.complete", blockers.get("blocker_matrix_complete") is True)
    _add(
        checks,
        "blockers.real_issuance_active",
        any(
            b.get("blocker_id") == "real_request_issuance_not_authorized" and b.get("active")
            for b in blockers.get("blockers") or []
        ),
    )

    _add(checks, "boundary.ok", boundary.get("non_execution_boundary_ok") is True)
    for field in (
        "request_issued",
        "notification_sent",
        "request_record_created",
        "approval_record_created",
        "grant_issued",
        "foundation_frozen",
        "closure_executed",
    ):
        _add(checks, f"boundary.{field}_false", boundary.get(field) is False)
    for key in ABSENCE_KEYS:
        _add(checks, f"boundary.absence.{key}", boundary.get(key) is True)
        _add(checks, f"summary.absence.{key}", summary.get(key) is True)

    _add(checks, "governance.reuse_ok", governance.get("reuse_first_rule_ref_ok") is True)
    _add(checks, "governance.module_first_ok", governance.get("module_first_cadence_rule_ref_ok") is True)
    _add(checks, "governance.validate_once_ok", governance.get("validate_once_rule_ref_ok") is True)
    _add(checks, "governance.reuse_ref", governance.get("reuse_first_protocol_engineering_rule_ref") == REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF)
    _add(
        checks,
        "governance.module_first_ref",
        governance.get("module_first_development_verification_cadence_rule_ref") == MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
    )
    _add(
        checks,
        "governance.validate_once_ref",
        governance.get("validate_once_per_module_rule_ref") == VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
    )
    _expect_false(checks, "governance.no_shared_revalidation", governance.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "governance.no_l1_revalidation", governance.get("l1_input_output_protocol_revalidation"))

    _add(checks, "module_first.complete", module_first.get("module_first_cadence_rule_complete") is True)
    _add(checks, "module_first.ref_ok", module_first.get("module_first_cadence_rule_ref_ok") is True)
    for phase in module_first.get("development_phases") or []:
        _add(checks, f"module_first.phase.{phase[:20]}", bool(phase))

    _add(checks, "next_phase.ok", next_phase.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next_phase.target", next_phase.get("target") == "freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision")
    _add(checks, "next_phase.roadmap_ready", next_phase.get("roadmap_decision_readiness") is True)
    _add(checks, "next_phase.no_real_issuance", next_phase.get("real_request_issuance_authorized") is False)
    for forbidden in FORBIDDEN_NEXT_TARGETS:
        _add(checks, f"next_phase.not_{forbidden}", forbidden not in (next_phase.get("recommended_next_phase") or "").lower())

    for key in FILE_SIZE_SUMMARY_KEYS:
        _add(checks, f"file_size.summary.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size_review.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size_review.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.phase_file.{rel.split('/')[-1]}", row.get("exists") is True)

    for rel in GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"summary.no_runtime.{flag}", summary.get(flag) is not True)

    for cid in CORE_CANDIDATE_IDS:
        row = next((r for r in post_candidate.get("candidates") or [] if r.get("candidate_id") == cid), {})
        _add(checks, f"upstream.candidate.{cid}.still", row.get("still_candidate") is True)

    for key in ABSENCE_KEYS:
        _add(checks, f"post_review.absence.{key}", post_absence.get(key) is True)

    _add(checks, "debt0.must_not_impl", GOVERNANCE_DEBTS[0].get("must_not_implement_now") is True)

    gate_docs = (plan, readiness, missing, blockers, boundary, governance, next_phase, module_first)
    for idx, doc in enumerate(gate_docs):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")
        for key in GO_CONDITIONS_KEYS:
            if key in doc:
                _add(checks, f"doc{idx}.{key}", doc.get(key) is True)

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
    _add(checks, "summary.prior_post_review_go", summary.get("prior_record_approval_closure_post_review_go") is True)
    _add(checks, "plan.final_match", plan.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "next_phase.roadmap", "Roadmap-Decision" in (next_phase.get("recommended_next_phase") or ""))

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.no_real_issuance", "No real request issuance" in md)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])

    for idx, cond in enumerate(missing.get("conditions") or []):
        _add(checks, f"missing.cond{idx}.id", bool(cond.get("condition_id")))
        _add(checks, f"missing.cond{idx}.cat", bool(cond.get("category")))
        _add(checks, f"missing.cond{idx}.note", bool(cond.get("note")))

    for idx, blk in enumerate(blockers.get("blockers") or []):
        _add(checks, f"blocker{idx}.id", bool(blk.get("blocker_id")))
        _add(checks, f"blocker{idx}.severity", bool(blk.get("severity")))

    for idx, row in enumerate(readiness.get("rows") or []):
        _add(checks, f"readiness.row{idx}.status", bool(row.get("status")))
        _add(checks, f"readiness.row{idx}.note", bool(row.get("note")))

    _add(checks, "plan.post_review_decision", plan.get("post_review_final_decision") == POST_REVIEW_FINAL_GO)
    _add(checks, "plan.dimensions_count", len(plan.get("readiness_dimensions") or []) == len(READINESS_DIMENSIONS))
    _add(checks, "plan.core_candidates", len(plan.get("core_candidate_ids") or []) >= 5)
    _add(checks, "post_review.candidate_ok", post_summary.get("candidate_review_ok") is True)
    _add(checks, "post_review.absence_ok", post_summary.get("absence_review_ok") is True)
    _add(checks, "post_review.boundary_ok", post_summary.get("boundary_review_ok") is True)
    _add(checks, "post_review.non_execution", post_summary.get("non_execution_boundary_ok") is True)
    _expect_false(checks, "summary.no_shared_revalidation", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.no_l1_revalidation", summary.get("l1_input_output_protocol_revalidation"))
    _add(checks, "summary.final_gate_planning_only", summary.get("final_gate_planning_only") is True)
    _add(checks, "plan.final_gate_planning_only", plan.get("final_gate_planning_only") is True)
    _add(checks, "boundary.runtime_absent", boundary.get("runtime_execution_absent") is True)
    _add(checks, "module_first.rule_id", bool(module_first.get("rule_id")))
    _add(checks, "module_first.doc_path", bool(module_first.get("doc_rel_path")))
    _add(checks, "governance.file_size_ref", bool(governance.get("file_size_module_split_governance_rule_ref")))
    _add(checks, "governance.file_size_doc", bool(governance.get("file_size_module_split_governance_rule_doc")))
    _add(checks, "next_phase.request_issued_false", next_phase.get("request_issued") is False)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "final_gate_planning_verifier_only": True,
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
                "module_first_cadence_rule_ref_ok": report_payload.get("module_first_cadence_rule_ref_ok"),
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
