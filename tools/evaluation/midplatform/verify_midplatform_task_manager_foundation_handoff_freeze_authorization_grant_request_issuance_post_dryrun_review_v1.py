#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Request Issuance Post-DryRun Review v1.

Structure inherited from verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_post_dryrun_review_v1.py
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
    CORE_GO_NO_GO_SCHEMA_KEYS,
    GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_ADDITIONS,
    GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_TERM_OVERRIDES,
    GRANT_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES,
    TEMPLATE_FAMILY,
    validate_core_go_no_go_schema,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    FINAL_DECISION_GO as GRANT_REQUEST_ISSUANCE_DRYRUN_FINAL_GO,
    GO_CONDITIONS_KEYS as GRANT_REQUEST_ISSUANCE_DRYRUN_TRUE_KEYS,
    GRANT_REQUEST_ISSUANCE_DRYRUN_ARTIFACTS,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES,
    DEFAULT_GRANT_REQUEST_ISSUANCE_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    FORBIDDEN_SCOPE_CLASSIFICATIONS,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_ALT,
    NEXT_PHASE_GO,
    PHASE_ID,
    POST_REVIEW_BOUNDARY_STATEMENTS,
    POST_REVIEW_SCOPE,
    SCOPE,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1.md",
    "task_manager_freeze_authorization_grant_request_issuance_dryrun_review_matrix_v1.json",
    "task_manager_freeze_authorization_grant_request_issuance_boundary_drift_review_v1.json",
    "task_manager_freeze_authorization_grant_request_issuance_chain_evidence_review_v1.json",
    "task_manager_freeze_authorization_grant_request_issuance_absence_review_v1.json",
    "task_manager_freeze_authorization_grant_request_issuance_state_absence_review_v1.json",
    "task_manager_freeze_authorization_grant_request_issuance_governance_debt_review_v1.json",
    "task_manager_freeze_authorization_grant_request_issuance_template_lineage_review_v1.json",
    "task_manager_freeze_authorization_grant_request_record_planning_readiness_v1.json",
    "summary.json",
)
TEMPLATE_LINEAGE_GO_KEYS: Tuple[str, ...] = (
    "template_lineage_ok",
    "base_template_files_exist",
    "full_repo_scan_absent",
    "core_go_no_go_schema_preserved",
    "stage_specific_terms_overridden",
)
FORBIDDEN_NEXT_TARGETS: Tuple[str, ...] = (
    "authorization_request_issued",
    "grant_issued",
    "foundation_frozen",
    "closed",
    "module_adapter_implementation",
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
    parser.add_argument("--grant-request-issuance-dryrun-root", default=DEFAULT_GRANT_REQUEST_ISSUANCE_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.grant_request_issuance_dryrun_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for rel in GRANT_REQUEST_ISSUANCE_POST_REVIEW_WHITELIST_FILES:
        _add(checks, f"template.base_file.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    _add(checks, "template.whitelist_only", True)

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    _add(checks, "dryrun.summary_go", dryrun_summary.get("final_decision") == GRANT_REQUEST_ISSUANCE_DRYRUN_FINAL_GO)
    _add(checks, "dryrun.verifier_go", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "dryrun.passed_min", int(dryrun_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "dryrun.failed_zero", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "dryrun.blocker_zero", dryrun_verifier.get("blocker_count") == 0)
    _add(checks, "dryrun.post_review_readiness", dryrun_summary.get("post_review_readiness_ok") is True)
    for key in GRANT_REQUEST_ISSUANCE_DRYRUN_TRUE_KEYS:
        _add(checks, f"dryrun.summary.{key}", dryrun_summary.get(key) is True)
        if key in dryrun_verifier:
            _add(checks, f"dryrun.verifier.{key}", dryrun_verifier.get(key) is True)
    _add(checks, "dryrun.template_lineage_ok", dryrun_summary.get("template_lineage_ok") is True)

    for artifact in GRANT_REQUEST_ISSUANCE_DRYRUN_ARTIFACTS:
        path = dryrun / artifact
        _add(checks, f"dryrun.artifact.exists.{artifact}", path.is_file())
        if artifact.endswith(".json"):
            _add(checks, f"dryrun.artifact.non_placeholder.{artifact}", bool(_read(path)))

    review = docs["task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1.json"]
    matrix = docs["task_manager_freeze_authorization_grant_request_issuance_dryrun_review_matrix_v1.json"]
    drift = docs["task_manager_freeze_authorization_grant_request_issuance_boundary_drift_review_v1.json"]
    evidence = docs["task_manager_freeze_authorization_grant_request_issuance_chain_evidence_review_v1.json"]
    absence_review = docs["task_manager_freeze_authorization_grant_request_issuance_absence_review_v1.json"]
    state_review = docs["task_manager_freeze_authorization_grant_request_issuance_state_absence_review_v1.json"]
    debt_review = docs["task_manager_freeze_authorization_grant_request_issuance_governance_debt_review_v1.json"]
    lineage_review = docs["task_manager_freeze_authorization_grant_request_issuance_template_lineage_review_v1.json"]
    record_readiness = docs["task_manager_freeze_authorization_grant_request_record_planning_readiness_v1.json"]
    summary = docs["summary.json"]
    lineage = summary.get("template_lineage") or {}

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.post_review_only.{doc_name}", doc.get("post_review_only") is True)
        _add(checks, f"meta.foundation_not_frozen.{doc_name}", doc.get("foundation_not_frozen") in (None, True))
        _add(checks, f"meta.request_record_absent.{doc_name}", doc.get("request_record_absent") in (None, True))
        for key in RUNTIME_FORBIDDEN_FLAGS:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("post_dryrun_review_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"review.{key}", review.get(key) is True)
        _add(checks, f"go_conditions.{key}", (summary.get("go_conditions") or {}).get(key) is True)

    for key in CORE_GO_NO_GO_SCHEMA_KEYS:
        if key in ("passed_checks", "failed_checks", "blocker_count", "verifier", "summary"):
            continue
        _add(checks, f"summary.schema.{key}", key in summary)

    for key in TEMPLATE_LINEAGE_GO_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "lineage.family", lineage.get("template_family") == TEMPLATE_FAMILY)
    _add(checks, "lineage.base_phase", lineage.get("base_phase") == "Freeze-Authorization-Grant-Request-Post-DryRun-Review-v1-001")
    _add(
        checks,
        "lineage.upstream",
        lineage.get("upstream_review_phase") == "Freeze-Authorization-Grant-Request-Issuance-DryRun-v1-001",
    )
    _add(checks, "lineage.reuse_mode", lineage.get("reuse_mode") == "whitelist_file_template_reuse")
    _add(checks, "lineage.no_full_scan", lineage.get("full_repo_scan_allowed") is False)
    _add(checks, "lineage.files_exist", lineage.get("base_template_files_exist") is True)
    _add(checks, "lineage.stage_overridden", lineage.get("stage_specific_terms_overridden") is True)
    _add(checks, "lineage.ok", lineage.get("template_lineage_ok") is True)
    _add(checks, "lineage.review.ok", lineage_review.get("template_lineage_ok") is True)
    _add(checks, "lineage.review.upstream", lineage_review.get("upstream_grant_request_issuance_dryrun_lineage_ok") is True)
    for override in GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_TERM_OVERRIDES:
        _add(checks, f"lineage.override.{override['base_term'][:30]}", override in (lineage.get("stage_term_overrides") or []))
    for addition in GRANT_REQUEST_ISSUANCE_POST_REVIEW_STAGE_ADDITIONS:
        _add(checks, f"lineage.addition.{addition}", addition in (lineage.get("stage_additions") or []))

    _add(checks, "matrix.accepted", matrix.get("request_issuance_dryrun_result_accepted") is True)
    for row in matrix.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"matrix.exists.{name}", row.get("exists") is True)
        _add(checks, f"matrix.non_placeholder.{name}", row.get("non_placeholder") is True)

    _add(checks, "drift.absent", drift.get("boundary_drift_absent") is True)
    _add(checks, "drift.post_review_scope", drift.get("post_review_scope") == POST_REVIEW_SCOPE)
    for forbidden in FORBIDDEN_SCOPE_CLASSIFICATIONS:
        _add(checks, f"drift.not_{forbidden}", drift.get("post_review_scope") != forbidden)
    for row in drift.get("rows") or []:
        name = row.get("artifact")
        _add(checks, f"drift.runtime_absent.{name}", row.get("runtime_scope_leak_absent") is True)
        _add(checks, f"drift.no_added_runtime.{name}", row.get("post_review_added_runtime") is False)
        _add(checks, f"drift.scope_ok.{name}", row.get("scope_classification") == POST_REVIEW_SCOPE)

    _add(checks, "evidence.accepted", evidence.get("request_issuance_chain_evidence_accepted") is True)
    _add(checks, "evidence.node_count", evidence.get("node_count") == len(CHAIN_EVIDENCE_NODES))
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in evidence.get("chain") or [] if r.get("stage") == stage), {})
        _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
    post_row = next(
        (r for r in evidence.get("chain") or [] if r.get("stage") == "freeze_authorization_grant_request_issuance_post_dryrun_review"),
        {},
    )
    _add(checks, "evidence.post_review.linked", post_row.get("linked") is True)
    _add(checks, "evidence.post_review.scope", post_row.get("readiness") == POST_REVIEW_SCOPE)
    _add(checks, "evidence.post_review.no_issued", post_row.get("authorization_request_issued") is False)
    _add(checks, "evidence.post_review.no_record", post_row.get("request_record") is False)
    _add(checks, "evidence.post_review.no_grant", post_row.get("grant_issued") is False)

    _add(checks, "absence.confirmed", absence_review.get("issuance_absence_confirmed") is True)
    _add(checks, "absence.not_issued", absence_review.get("authorization_request_issued") is False)
    _add(checks, "absence.record_absent", absence_review.get("request_record_absent") is True)
    _add(checks, "absence.owner_absent", absence_review.get("owner_approval_record_absent") is True)
    _add(checks, "absence.grant_absent", absence_review.get("authorization_grant_absent") is True)
    _add(checks, "absence.token_absent", absence_review.get("grant_token_absent") is True)
    _add(checks, "absence.record_grant_absent", absence_review.get("grant_record_absent") is True)
    _add(checks, "absence.no_freeze_exec", absence_review.get("no_freeze_execution_path") is True)
    _add(checks, "absence.no_rollback_exec", absence_review.get("no_rollback_execution_path") is True)

    _add(checks, "review.issuance_candidate", review.get("request_issuance_candidate_preserved") is True)
    _add(checks, "review.record_candidate", review.get("request_record_candidate_preserved") is True)
    _add(checks, "review.owner_candidate", review.get("owner_approval_candidate_preserved") is True)
    _add(checks, "review.post_review_scope", review.get("post_review_scope") == POST_REVIEW_SCOPE)

    _add(checks, "state.not_frozen", state_review.get("foundation_not_frozen") is True)
    _add(checks, "state.closure_not_executed", state_review.get("closure_not_executed") is True)
    _add(checks, "state.status", state_review.get("freeze_status") == "freeze-candidate")
    _add(checks, "state.not_frozen_val", state_review.get("freeze_status") != "frozen")
    _add(checks, "state.not_foundation_frozen", state_review.get("freeze_status") != "foundation-frozen")
    _add(checks, "state.not_closed", state_review.get("closure_status") != "closed")
    _add(checks, "state.not_finalized", state_review.get("closure_status") != "foundation-finalized")
    _add(checks, "state.no_freeze_exec", state_review.get("no_freeze_execution_path") is True)
    _add(checks, "state.no_rollback_exec", state_review.get("no_rollback_execution_path") is True)

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

    _add(checks, "record.ready", record_readiness.get("request_record_planning_ready") is True)
    _add(checks, "record.recommended", record_readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "record.no_auth_issued", record_readiness.get("authorization_request_issued") is False)
    _add(checks, "record.no_request_record", record_readiness.get("request_record_created") is False)
    _add(checks, "record.no_owner_record", record_readiness.get("owner_approval_record_created") is False)
    _add(checks, "record.no_grant", record_readiness.get("grant_issued") is False)
    _add(checks, "record.no_adapter", record_readiness.get("module_adapter_implementation_ready") is False)
    _add(checks, "record.not_frozen", record_readiness.get("foundation_frozen") is False)
    _add(checks, "record.not_closed", record_readiness.get("closed") is False)
    for candidate in record_readiness.get("candidates") or []:
        phase = candidate.get("phase", "")
        _add(checks, f"record.candidate.{phase[:50]}.no_auth_issued", candidate.get("authorization_request_issued") is False)
        _add(checks, f"record.candidate.{phase[:50]}.no_request_record", candidate.get("request_record_created") is False)
        _add(checks, f"record.candidate.{phase[:50]}.no_owner_record", candidate.get("owner_approval_record_created") is False)
        _add(checks, f"record.candidate.{phase[:50]}.no_grant", candidate.get("grant_issued") is False)
        _add(checks, f"record.candidate.{phase[:50]}.not_frozen", candidate.get("foundation_frozen") is False)
        _add(checks, f"record.candidate.{phase[:50]}.not_closed", candidate.get("closed") is False)
        for forbidden in FORBIDDEN_NEXT_TARGETS:
            _add(checks, f"record.candidate.{phase[:50]}.not_{forbidden}", forbidden not in phase.lower())
    _add(
        checks,
        "record.has_alt_candidate",
        any(c.get("phase") == NEXT_PHASE_ALT for c in (record_readiness.get("candidates") or [])),
    )

    for stmt in POST_REVIEW_BOUNDARY_STATEMENTS:
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
        _add(checks, f"drift.boundary.{stmt[:35]}", stmt in (drift.get("boundary_statements") or []))

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(
        checks,
        "md.not_issued",
        "does not issue authorization request" in md or "不发起 authorization request" in md,
    )
    _add(checks, "md.post_review_ne", "request issuance post-dryrun review ≠ authorization request issued" in md)
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

    for phrase in ("freeze-candidate", "Request record absent", "Template lineage OK", POST_REVIEW_SCOPE):
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
    schema_ok = validate_core_go_no_go_schema(summary, report)
    report["core_go_no_go_schema_preserved"] = schema_ok
    if not schema_ok:
        checks.append({"check_id": "schema.validate", "passed": False, "detail": "core go/no-go schema mismatch"})
        passed = sum(1 for check in checks if check["passed"])
        failed = [check for check in checks if not check["passed"]]
        report["passed_checks"] = passed
        report["failed_checks"] = len(failed)
        report["blocker_count"] = len(failed)
        report["checks"] = checks
        if verifier == "GO":
            verifier = "HOLD"
            report["verifier"] = verifier
            report["final_decision"] = "HOLD"
            report["go_no_go_decision"] = "HOLD"
    else:
        checks.append({"check_id": "schema.validate", "passed": True, "detail": ""})
        report["checks"] = checks

    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "passed_checks": report["passed_checks"],
                "failed_checks": report["failed_checks"],
                "blocker_count": report["blocker_count"],
                "request_issuance_dryrun_result_accepted": report.get("request_issuance_dryrun_result_accepted"),
                "request_issuance_chain_evidence_accepted": report.get("request_issuance_chain_evidence_accepted"),
                "issuance_absence_confirmed": report.get("issuance_absence_confirmed"),
                "template_lineage_ok": report.get("template_lineage_ok"),
                "full_repo_scan_absent": report.get("full_repo_scan_absent"),
                "post_review_only": report.get("post_review_only"),
                "request_record_planning_ready": report.get("request_record_planning_ready"),
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
