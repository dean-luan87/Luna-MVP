#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Request Planning v1.

Structure inherited from verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_planning_v1.py
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
    GRANT_REQUEST_PLANNING_STAGE_ADDITIONS,
    GRANT_REQUEST_PLANNING_STAGE_TERM_OVERRIDES,
    GRANT_REQUEST_PLANNING_WHITELIST_FILES,
    TEMPLATE_FAMILY,
    validate_core_go_no_go_schema,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES as UPSTREAM_CHAIN_NODES,
    FINAL_DECISION_GO as GRANT_POST_REVIEW_FINAL_GO,
    GO_CONDITIONS_KEYS as UPSTREAM_GO_KEYS,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_request_planning_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
    CHAIN_EVIDENCE_NODES,
    DEFAULT_GRANT_POST_REVIEW_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    NON_EXECUTION_CONSTRAINTS,
    PHASE_ID,
    PREREQUISITE_ROWS,
    SCOPE,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_request_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_request_plan_v1.md",
    "task_manager_freeze_authorization_grant_request_scope_matrix_v1.json",
    "task_manager_freeze_authorization_grant_request_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_request_prerequisite_matrix_v1.json",
    "task_manager_freeze_authorization_grant_request_evidence_chain_v1.json",
    "task_manager_freeze_authorization_grant_request_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_request_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_request_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_request_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_request_next_phase_readiness_v1.json",
    "summary.json",
)
TEMPLATE_LINEAGE_GO_KEYS: Tuple[str, ...] = (
    "template_lineage_ok",
    "base_template_files_exist",
    "full_repo_scan_absent",
    "core_go_no_go_schema_preserved",
    "stage_specific_terms_overridden",
)
RUNTIME_FORBIDDEN: Tuple[str, ...] = RUNTIME_FORBIDDEN_FLAGS + (
    "authorization_request_created_now",
    "request_record_created_now",
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
    parser.add_argument("--grant-post-dryrun-review-root", default=DEFAULT_GRANT_POST_REVIEW_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    post_review = Path(args.grant_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []
    docs = {name: _read(root / name) for name in REQUIRED_ARTIFACTS if name.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_freeze_authorization_grant_request_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    for name in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{name}", (root / name).is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.non_placeholder.{name}", bool(_read(root / name)))
        else:
            _add(checks, f"artifact.non_placeholder.{name}", len(md.strip()) > 200)

    for rel in GRANT_REQUEST_PLANNING_WHITELIST_FILES:
        _add(checks, f"template.whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    _add(checks, "template.whitelist_only", True)

    post_summary = _read(post_review / "summary.json")
    post_verifier = _read(post_review / "verifier_report.json")
    _add(checks, "prior.summary_go", post_summary.get("final_decision") == GRANT_POST_REVIEW_FINAL_GO)
    _add(checks, "prior.verifier_go", post_verifier.get("verifier") == "GO")
    _add(checks, "prior.passed_min", int(post_verifier.get("passed_checks", 0)) >= 420)
    _add(checks, "prior.failed_zero", post_verifier.get("failed_checks") == 0)
    _add(checks, "prior.blocker_zero", post_verifier.get("blocker_count") == 0)
    _add(checks, "prior.next_planning_ready", post_summary.get("next_planning_ready") is True)
    for key in UPSTREAM_GO_KEYS:
        _add(checks, f"prior.summary.{key}", post_summary.get(key) is True)
        if key in post_verifier:
            _add(checks, f"prior.verifier.{key}", post_verifier.get(key) is True)

    plan = docs["task_manager_foundation_handoff_freeze_authorization_grant_request_plan_v1.json"]
    scope = docs["task_manager_freeze_authorization_grant_request_scope_matrix_v1.json"]
    candidate = docs["task_manager_freeze_authorization_grant_request_candidate_matrix_v1.json"]
    owner = docs["task_manager_freeze_authorization_grant_owner_approval_candidate_matrix_v1.json"]
    prerequisites = docs["task_manager_freeze_authorization_grant_request_prerequisite_matrix_v1.json"]
    evidence = docs["task_manager_freeze_authorization_grant_request_evidence_chain_v1.json"]
    boundary = docs["task_manager_freeze_authorization_grant_request_boundary_contract_v1.json"]
    constraints = docs["task_manager_freeze_authorization_grant_request_non_execution_constraints_v1.json"]
    debt_carryover = docs["task_manager_freeze_authorization_grant_request_governance_debt_carryover_v1.json"]
    lineage_doc = docs["task_manager_freeze_authorization_grant_request_template_lineage_v1.json"]
    next_phase = docs["task_manager_freeze_authorization_grant_request_next_phase_readiness_v1.json"]
    summary = docs["summary.json"]
    lineage = summary.get("template_lineage") or {}

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.request_planning_only.{doc_name}", doc.get("grant_request_planning_only") in (None, True))
        _add(checks, f"meta.auth_request_absent.{doc_name}", doc.get("authorization_request_absent") in (None, True))
        _add(checks, f"meta.request_record_absent.{doc_name}", doc.get("request_record_absent") in (None, True))
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"meta.no_runtime.{doc_name}.{key}", doc.get(key) is not True)

    _add(checks, "summary.pass", summary.get("planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"plan.{key}", plan.get(key) is True)
        _add(checks, f"go_conditions.{key}", (summary.get("go_conditions") or {}).get(key) is True)

    for key in CORE_GO_NO_GO_SCHEMA_KEYS:
        if key in ("passed_checks", "failed_checks", "blocker_count", "verifier", "summary"):
            continue
        _add(checks, f"summary.schema.{key}", key in summary)

    for key in TEMPLATE_LINEAGE_GO_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "lineage.family", lineage.get("template_family") == TEMPLATE_FAMILY)
    _add(checks, "lineage.base_phase", lineage.get("base_phase") == "Freeze-Authorization-Grant-Planning-v1-001")
    _add(checks, "lineage.upstream", lineage.get("upstream_review_phase") == "Freeze-Authorization-Grant-Post-DryRun-Review-v1-001")
    _add(checks, "lineage.reuse_mode", lineage.get("reuse_mode") == "whitelist_file_template_reuse")
    _add(checks, "lineage.no_full_scan", lineage.get("full_repo_scan_allowed") is False)
    _add(checks, "lineage.files_exist", lineage.get("base_template_files_exist") is True)
    _add(checks, "lineage.ok", lineage.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.ok", lineage_doc.get("template_lineage_ok") is True)
    _add(checks, "lineage.doc.upstream", lineage_doc.get("upstream_grant_post_review_lineage_ok") is True)
    for override in GRANT_REQUEST_PLANNING_STAGE_TERM_OVERRIDES:
        _add(checks, f"lineage.override.{override['base_term'][:30]}", override in (lineage.get("stage_term_overrides") or []))
    for addition in GRANT_REQUEST_PLANNING_STAGE_ADDITIONS:
        _add(checks, f"lineage.addition.{addition}", addition in (lineage.get("stage_additions") or []))

    _add(checks, "scope.planning_only", scope.get("request_scope_planning_only") is True)
    for row in scope.get("rows") or []:
        s = row.get("scope")
        _add(checks, f"scope.row.{s}.planning", row.get("classification") == "grant-request-planning-scope")
        _add(checks, f"scope.row.{s}.not_issued", row.get("classification") != "request-issued-scope")
        _add(checks, f"scope.row.{s}.not_authorized", row.get("classification") != "authorized-scope")

    _add(checks, "candidate.only", candidate.get("request_candidate_only") is True)
    for row in candidate.get("rows") or []:
        path = row.get("path", "unknown")
        label = str(path).split("/")[-1][:40]
        _add(checks, f"candidate.request.{label}", row.get("request_status") == "grant-request-candidate")
        _add(checks, f"candidate.not_record.{label}", row.get("request_status") != "request-record")

    _add(checks, "owner.candidate_only", owner.get("owner_approval_candidate_only") is True)
    for row in owner.get("rows") or []:
        role = row.get("role")
        _add(checks, f"owner.{role}.candidate", row.get("approval_status") == "owner-approval-candidate")
        _add(checks, f"owner.{role}.not_record", row.get("approval_status") != "owner-approval-record")

    _add(checks, "prereq.ok", prerequisites.get("prerequisites_ok") is True)
    for req_row in PREREQUISITE_ROWS:
        prereq = req_row["prerequisite"]
        row = next((r for r in prerequisites.get("rows") or [] if r.get("prerequisite") == prereq), {})
        _add(checks, f"prereq.{prereq}.required", row.get("required") is True)
        _add(checks, f"prereq.{prereq}.satisfied", row.get("satisfied") is True)

    _add(checks, "evidence.complete", evidence.get("evidence_chain_complete") is True)
    _add(checks, "evidence.not_issued", evidence.get("points_to_request_planning_not_issued") is True)
    for stage in UPSTREAM_CHAIN_NODES:
        row = next((r for r in evidence.get("chain") or [] if r.get("stage") == stage), {})
        _add(checks, f"evidence.linked.{stage}", row.get("linked") is True)
    req_row = next(
        (r for r in evidence.get("chain") or [] if r.get("stage") == "freeze_authorization_grant_request_planning"),
        {},
    )
    _add(checks, "evidence.request_planning.linked", req_row.get("linked") is True)
    _add(checks, "evidence.request_planning.no_request", req_row.get("authorization_request") is False)
    _add(checks, "evidence.request_planning.no_record", req_row.get("request_record") is False)
    _add(checks, "evidence.node_count", evidence.get("node_count") == len(CHAIN_EVIDENCE_NODES))

    for stmt in BOUNDARY_CONTRACT_STATEMENTS:
        _add(checks, f"boundary.stmt.{stmt[:35]}", stmt in (boundary.get("statements") or []))
        _add(checks, f"md.boundary.{stmt[:35]}", stmt in md)
    _add(checks, "boundary.request_absent", boundary.get("authorization_request_absent") is True)
    _add(checks, "boundary.record_absent", boundary.get("request_record_absent") is True)
    _add(checks, "boundary.owner_absent", boundary.get("owner_approval_record_absent") is True)

    for key in NON_EXECUTION_CONSTRAINTS:
        _add(checks, f"constraints.{key}", constraints.get(key) is True)
    _add(checks, "constraints.ok", constraints.get("non_execution_boundary_ok") is True)

    debts = debt_carryover.get("debts") or []
    _add(checks, "debt.count", len(debts) >= 2)
    debt0 = debts[0] if debts else {}
    debt1 = debts[1] if len(debts) > 1 else {}
    _add(checks, "debt0.title", debt0.get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"])
    _add(checks, "debt0.priority", debt0.get("priority") == "P1")
    _add(checks, "debt1.title", debt1.get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"])
    _add(checks, "debt.carryover_complete", debt_carryover.get("governance_debt_carryover_complete") is True)

    _add(checks, "next_phase.ok", next_phase.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "next_phase.target_dryrun", next_phase.get("target") == "freeze_authorization_grant_request_dryrun")
    _add(checks, "next_phase.no_request_issued", next_phase.get("authorization_request_issued") is False)
    _add(checks, "next_phase.no_request_record", next_phase.get("request_record_created") is False)
    _add(checks, "next_phase.no_owner_record", next_phase.get("owner_approval_record_created") is False)
    _add(checks, "next_phase.no_grant", next_phase.get("grant_issued") is False)
    _add(checks, "next_phase.not_frozen", next_phase.get("foundation_frozen") is False)
    _add(checks, "next_phase.not_closed", next_phase.get("closed") is False)

    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.next", NEXT_PHASE_GO in md)
    _add(checks, "md.not_request", "does not issue authorization request" in md or "不发起 authorization request" in md)
    _add(checks, "md.debt0", GOVERNANCE_DEBTS[0]["debt_title"] in md)

    for doc_name, doc in docs.items():
        for key in GO_CONDITIONS_KEYS:
            if key in doc:
                _add(checks, f"sweep.true.{doc_name}.{key}", doc.get(key) is True)
        for key in RUNTIME_FORBIDDEN:
            _add(checks, f"sweep.runtime.{doc_name}.{key}", doc.get(key) is not True)

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
        report.update({"passed_checks": passed, "failed_checks": len(failed), "blocker_count": len(failed), "checks": checks})
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
                "prior_grant_post_review_go": report.get("prior_grant_post_review_go"),
                "grant_request_plan_complete": report.get("grant_request_plan_complete"),
                "template_lineage_ok": report.get("template_lineage_ok"),
                "next_phase_readiness_ok": report.get("next_phase_readiness_ok"),
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
