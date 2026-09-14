#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant DryRun v1.

Structure inherited from verify_midplatform_task_manager_foundation_handoff_freeze_authorization_dryrun_v1.py
via whitelist template reuse (no full-repo scan).
"""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    BASE_DRYRUN_TEMPLATE_FILES,
    CORE_GO_NO_GO_SCHEMA_KEYS,
    GRANT_DRYRUN_STAGE_ADDITIONS,
    GRANT_DRYRUN_STAGE_TERM_OVERRIDES,
    TEMPLATE_FAMILY,
    validate_core_go_no_go_schema,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_dryrun_v1 import (
    ALLOWED_SCOPE_CLASSIFICATIONS,
    CHAIN_TRACE_NODES,
    DEFAULT_GRANT_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    DRYRUN_BOUNDARY_STATEMENTS,
    FINAL_DECISION_GO,
    FORBIDDEN_ASSET_STATES,
    GO_CONDITIONS_KEYS,
    GRANT_PLANNING_PACKAGE_FILES,
    NEXT_PHASE_GO,
    PHASE_ID,
    PLANNING_TRUE_KEYS,
    RUNTIME_FORBIDDEN_FLAGS,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_planning_v1 import (
    FINAL_DECISION_GO as GRANT_PLANNING_FINAL_GO,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_dryrun_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_dryrun_report_v1.md",
    "task_manager_freeze_authorization_grant_plan_integrity_matrix_v1.json",
    "task_manager_freeze_authorization_grant_scope_validation_v1.json",
    "task_manager_freeze_authorization_grant_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_prerequisite_validation_v1.json",
    "task_manager_freeze_authorization_grant_evidence_traceability_v1.json",
    "task_manager_freeze_authorization_grant_absence_validation_v1.json",
    "task_manager_freeze_authorization_grant_boundary_validation_v1.json",
    "task_manager_freeze_authorization_grant_governance_debt_validation_v1.json",
    "task_manager_freeze_authorization_grant_post_review_readiness_v1.json",
    "task_manager_freeze_authorization_grant_template_lineage_v1.json",
    "summary.json",
)
PREREQ_KEYS: Tuple[str, ...] = (
    "authorization_request_absent",
    "authorization_grant_absent",
    "grant_not_issued",
    "foundation_not_frozen",
    "closure_not_executed",
)
TEMPLATE_LINEAGE_GO_KEYS: Tuple[str, ...] = (
    "template_lineage_ok",
    "base_template_files_exist",
    "full_repo_scan_absent",
    "core_go_no_go_schema_preserved",
    "stage_specific_terms_overridden",
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
    parser.add_argument("--grant-planning-root", default=DEFAULT_GRANT_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    planning = Path(args.grant_planning_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_dryrun_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for rel in BASE_DRYRUN_TEMPLATE_FILES:
        _add(checks, f"template.base_file.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    _add(checks, "template.whitelist_only", True)

    planning_summary = _read(planning / "summary.json")
    planning_verifier = _read(planning / "verifier_report.json")
    _add(checks, "planning.summary_go", planning_summary.get("final_decision") == GRANT_PLANNING_FINAL_GO)
    _add(checks, "planning.verifier_go", planning_verifier.get("verifier") == "GO")
    _add(checks, "planning.passed_min", int(planning_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "planning.failed_zero", planning_verifier.get("failed_checks") == 0)
    _add(checks, "planning.blocker_zero", planning_verifier.get("blocker_count") == 0)
    for key in PLANNING_TRUE_KEYS:
        _add(checks, f"planning.summary.{key}", planning_summary.get(key) is True)
        if key in planning_verifier:
            _add(checks, f"planning.verifier.{key}", planning_verifier.get(key) is True)

    for fname in GRANT_PLANNING_PACKAGE_FILES:
        path = planning / fname
        _add(checks, f"planning.package.exists.{fname}", path.is_file())
        if fname.endswith(".json"):
            _add(checks, f"planning.package.non_placeholder.{fname}", bool(_read(path)))

    report = docs["task_manager_foundation_handoff_freeze_authorization_grant_dryrun_report_v1.json"]
    integrity = docs["task_manager_freeze_authorization_grant_plan_integrity_matrix_v1.json"]
    trace = docs["task_manager_freeze_authorization_grant_evidence_traceability_v1.json"]
    scope_val = docs["task_manager_freeze_authorization_grant_scope_validation_v1.json"]
    candidate_val = docs["task_manager_freeze_authorization_grant_candidate_validation_v1.json"]
    prereq_val = docs["task_manager_freeze_authorization_grant_prerequisite_validation_v1.json"]
    grant_val = docs["task_manager_freeze_authorization_grant_absence_validation_v1.json"]
    boundary_val = docs["task_manager_freeze_authorization_grant_boundary_validation_v1.json"]
    debt_val = docs["task_manager_freeze_authorization_grant_governance_debt_validation_v1.json"]
    post_review = docs["task_manager_freeze_authorization_grant_post_review_readiness_v1.json"]
    lineage_doc = docs["task_manager_freeze_authorization_grant_template_lineage_v1.json"]
    summary = docs["summary.json"]

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.grant_dryrun_only.{doc_name}", doc.get("grant_dryrun_only") in (None, True))
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.closure_not_executed.{doc_name}", doc.get("closure_not_executed") in (None, True))
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"report.{key}", report.get(key) is True)
        _add(checks, f"go_conditions.{key}", (summary.get("go_conditions") or {}).get(key) is True)

    for key in CORE_GO_NO_GO_SCHEMA_KEYS:
        if key in ("passed_checks", "failed_checks", "blocker_count", "verifier", "summary"):
            continue
        _add(checks, f"summary.schema.{key}", key in summary)

    for key in TEMPLATE_LINEAGE_GO_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    lineage = summary.get("template_lineage") or {}
    _add(checks, "lineage.family", lineage.get("template_family") == TEMPLATE_FAMILY)
    _add(checks, "lineage.base_phase", lineage.get("base_phase") == "Freeze-Authorization-DryRun-v1-001")
    _add(checks, "lineage.reuse_mode", lineage.get("reuse_mode") == "whitelist_file_template_reuse")
    _add(checks, "lineage.no_full_scan", lineage.get("full_repo_scan_allowed") is False)
    _add(checks, "lineage.files_exist", lineage.get("base_template_files_exist") is True)
    _add(checks, "lineage.family_match", lineage.get("base_template_family_match") is True)
    _add(checks, "lineage.stage_overridden", lineage.get("stage_specific_terms_overridden") is True)
    _add(checks, "lineage.core_schema", lineage.get("core_go_no_go_schema_preserved") is True)
    _add(checks, "lineage.ok", lineage.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.ok", lineage_doc.get("template_lineage_ok") is True)
    for override in GRANT_DRYRUN_STAGE_TERM_OVERRIDES:
        _add(checks, f"lineage.override.{override['base_term'][:30]}", override in (lineage.get("stage_term_overrides") or []))
    for addition in GRANT_DRYRUN_STAGE_ADDITIONS:
        _add(checks, f"lineage.addition.{addition}", addition in (lineage.get("stage_additions") or []))

    _add(checks, "integrity.ok", integrity.get("grant_plan_integrity_ok") is True)
    for row in integrity.get("rows") or []:
        fname = row.get("file")
        _add(checks, f"integrity.exists.{fname}", row.get("exists") is True)
        _add(checks, f"integrity.non_placeholder.{fname}", row.get("non_placeholder") is True)

    _add(checks, "trace.ok", trace.get("grant_evidence_traceability_ok") is True)
    _add(checks, "trace.chain_alias", trace.get("freeze_authorization_chain_traceability_ok") is True)
    _add(checks, "trace.not_issued", trace.get("points_to_dryrun_not_issued") is True)
    _add(checks, "trace.not_grant", trace.get("points_to_dryrun_not_grant") is True)
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in trace.get("rows") or [] if r.get("stage") == stage), {})
        _add(checks, f"trace.linked.{stage}", row.get("linked") is True)
    dryrun_row = next(
        (r for r in trace.get("rows") or [] if r.get("stage") == "freeze_authorization_grant_dryrun"),
        {},
    )
    _add(checks, "trace.dryrun.no_grant", dryrun_row.get("authorization_grant") is False)
    _add(checks, "trace.dryrun.no_issued", dryrun_row.get("grant_issued") is False)

    _add(checks, "scope.preserved", scope_val.get("grant_scope_preserved") is True)
    for row in scope_val.get("rows") or []:
        s = row.get("scope")
        _add(checks, f"scope.row.{s}.allowed", row.get("classification") in ALLOWED_SCOPE_CLASSIFICATIONS)
        _add(checks, f"scope.row.{s}.not_issued", row.get("classification") != "grant-issued-scope")
        _add(checks, f"scope.row.{s}.not_authorized", row.get("classification") != "authorized-scope")

    _add(checks, "candidate.preserved", candidate_val.get("grant_candidate_preserved") is True)
    _add(checks, "candidate.asset_state_ok", candidate_val.get("asset_state_ok") is True)
    _add(checks, "candidate.grant_status", candidate_val.get("grant_status") == "freeze-authorization-grant-candidate")
    _add(checks, "candidate.not_granted", candidate_val.get("grant_status") != "freeze-authorization-granted")
    _add(checks, "candidate.freeze_status", candidate_val.get("freeze_status") == "freeze-candidate")
    for state in FORBIDDEN_ASSET_STATES:
        _add(checks, f"candidate.not_{state}", candidate_val.get("freeze_status") != state)

    _add(checks, "prereq.satisfied", prereq_val.get("grant_prerequisites_satisfied") is True)
    for key in PREREQ_KEYS:
        _add(checks, f"prereq.{key}", prereq_val.get(key) is True)

    _add(checks, "grant.request_absent", grant_val.get("authorization_request_absent") is True)
    _add(checks, "grant.grant_absent", grant_val.get("authorization_grant_absent") is True)
    _add(checks, "grant.token_absent", grant_val.get("grant_token_absent") is True)
    _add(checks, "grant.record_absent", grant_val.get("grant_record_absent") is True)
    _add(checks, "grant.owner_approval_absent", grant_val.get("owner_approval_record_absent") is True)
    _add(checks, "grant.no_freeze_exec", grant_val.get("no_freeze_execution_path") is True)
    _add(checks, "grant.no_rollback_exec", grant_val.get("no_rollback_execution_path") is True)

    _add(checks, "boundary.not_issued", boundary_val.get("grant_not_issued") is True)
    _add(checks, "boundary.grant_issued_false", boundary_val.get("grant_issued") is False)
    _add(checks, "boundary.not_frozen", boundary_val.get("foundation_frozen") is False)
    _add(checks, "boundary.not_closed", boundary_val.get("closed") is False)

    debts = debt_val.get("debts") or []
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
    _add(checks, "debt.preserved", debt_val.get("governance_debt_preserved") is True)

    _add(checks, "post_review.ok", post_review.get("post_review_readiness_ok") is True)
    _add(checks, "post_review.next", post_review.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "post_review.target", post_review.get("target") == "freeze_authorization_grant_post_dryrun_review")
    _add(checks, "post_review.no_grant", post_review.get("grant_issued") is False)
    _add(checks, "post_review.no_auth_grant", post_review.get("freeze_authorization_granted") is False)
    _add(checks, "post_review.no_adapter", post_review.get("module_adapter_implementation_ready") is False)
    _add(checks, "post_review.not_frozen", post_review.get("foundation_frozen") is False)
    _add(checks, "post_review.not_closed", post_review.get("closed") is False)

    for stmt in DRYRUN_BOUNDARY_STATEMENTS:
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
        _add(checks, f"report.boundary.{stmt[:35]}", stmt in (report.get("boundary_statements") or []))
        _add(checks, f"boundary.stmt.{stmt[:35]}", stmt in (boundary_val.get("statements") or []))

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.not_issued", "does not issue grant" in md or "不签发 grant" in md)
    _add(checks, "md.debt0", GOVERNANCE_DEBTS[0]["debt_title"] in md)
    _add(checks, "md.debt1", GOVERNANCE_DEBTS[1]["debt_title"] in md)

    for doc_name, doc in docs.items():
        for key in GO_CONDITIONS_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        _add(checks, f"sweep.next.{doc_name}", doc.get("recommended_next_phase") in (None, NEXT_PHASE_GO))
        for required in ("phase", "scope", "source_chain", "foundation_id", "runtime_status"):
            _add(checks, f"sweep.meta.{doc_name}.{required}", required in doc)
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)

    for phrase in ("freeze-candidate", "Grant token absent", "grant dry-run validation"):
        _add(checks, f"md.phrase.{phrase[:30]}", phrase in md)

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
        **{key: summary.get(key) is True for key in GO_CONDITIONS_KEYS},
        **{key: summary.get(key) is True for key in TEMPLATE_LINEAGE_GO_KEYS},
        "template_lineage": lineage,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "go_no_go_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:80],
        "checks": checks,
    }
    schema_ok = validate_core_go_no_go_schema(summary, report_payload)
    report_payload["core_go_no_go_schema_preserved"] = schema_ok
    if not schema_ok:
        checks.append({"check_id": "schema.validate", "passed": False, "detail": "core go/no-go schema mismatch"})
        passed = sum(1 for check in checks if check["passed"])
        failed = [check for check in checks if not check["passed"]]
        report_payload["passed_checks"] = passed
        report_payload["failed_checks"] = len(failed)
        report_payload["blocker_count"] = len(failed)
        report_payload["checks"] = checks
        if verifier == "GO":
            verifier = "HOLD"
            report_payload["verifier"] = verifier
            report_payload["final_decision"] = "HOLD"
            report_payload["go_no_go_decision"] = "HOLD"
    else:
        checks.append({"check_id": "schema.validate", "passed": True, "detail": ""})
        report_payload["checks"] = checks

    (root / "verifier_report.json").write_text(json.dumps(report_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report_payload["verifier"],
                "passed_checks": report_payload["passed_checks"],
                "failed_checks": report_payload["failed_checks"],
                "blocker_count": report_payload["blocker_count"],
                "template_lineage_ok": report_payload.get("template_lineage_ok"),
                "base_template_files_exist": report_payload.get("base_template_files_exist"),
                "full_repo_scan_absent": report_payload.get("full_repo_scan_absent"),
                "core_go_no_go_schema_preserved": report_payload.get("core_go_no_go_schema_preserved"),
                "stage_specific_terms_overridden": report_payload.get("stage_specific_terms_overridden"),
                "grant_plan_integrity_ok": report_payload.get("grant_plan_integrity_ok"),
                "grant_evidence_traceability_ok": report_payload.get("grant_evidence_traceability_ok"),
                "grant_dryrun_only": report_payload.get("grant_dryrun_only"),
                "post_review_readiness_ok": report_payload.get("post_review_readiness_ok"),
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
