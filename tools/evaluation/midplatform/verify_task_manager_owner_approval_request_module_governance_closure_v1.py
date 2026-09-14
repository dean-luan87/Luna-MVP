#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Owner Approval Request Module Governance Closure v1."""

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
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_owner_approval_request_functional_slice_dryrun_v1 import (
    FINAL_DECISION_GO as FUNCTIONAL_SLICE_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    FUNCTIONAL_SLICE_CHAINS,
    SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_governance_closure_v1 import (
    ABSENCE_KEYS,
    CLOSURE_ARTIFACTS,
    CURRENT_MODULE_STATE,
    DEFAULT_FUNCTIONAL_SLICE_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    FORBIDDEN_ROUTES,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_A,
    NEXT_PHASE_B,
    NEXT_PHASE_C,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    REAL_EXECUTION_STATE,
    SCOPE,
)

MIN_CHECKS = 260
FORBIDDEN_DECISION: Tuple[str, ...] = (
    "request_issued",
    "authorization_request_created",
    "grant_issued",
    "record_created",
    "foundation_frozen",
    "runtime_enabled",
)
FILE_SIZE_KEYS: Tuple[str, ...] = (
    "file_size_governance_review_exists",
    "file_size_governance_review_ok",
    "monolithic_file_absent",
    "full_repo_scan_absent",
    "tmp_eval_out_scan_absent",
    "summary_index_first_reading_ok",
    "limited_directory_scan_ok",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool) -> None:
    checks.append({"check_id": check_id, "passed": bool(passed)})


def _expect_false(checks: List[Dict[str, Any]], check_id: str, value: Any) -> None:
    _add(checks, check_id, value is False)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--functional-slice-dryrun-root", default=DEFAULT_FUNCTIONAL_SLICE_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.functional_slice_dryrun_root)
    checks: List[Dict[str, Any]] = []

    dryrun_summary = _read(upstream / "summary.json")
    dryrun_verifier = _read(upstream / "verifier_report.json")

    md = (root / "module_governance_closure_report_v1.md").read_text(encoding="utf-8") if (root / "module_governance_closure_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in CLOSURE_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["module_governance_closure_report_v1.json"]
    module_result = docs["module_result_closure_v1.json"]
    slice_summary = docs["functional_slice_closure_summary_v1.json"]
    gov_closure = docs["governance_rule_closure_v1.json"]
    non_exec = docs["non_execution_closure_v1.json"]
    preconds = docs["real_execution_preconditions_v1.json"]
    decision = docs["module_closure_decision_v1.json"]
    handoff = docs["module_closure_handoff_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in CLOSURE_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 60)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.dryrun_go", dryrun_summary.get("final_decision") == FUNCTIONAL_SLICE_DRYRUN_FINAL_GO)
    _add(checks, "upstream.dryrun_verifier", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "upstream.dryrun_pass", dryrun_summary.get("functional_slice_dryrun_pass") is True)
    _add(checks, "upstream.all_primary", dryrun_summary.get("all_slice_primary_results_reached") is True)
    _add(checks, "upstream.forbidden_absent", dryrun_summary.get("forbidden_state_transitions_absent") is True)
    _add(checks, "upstream.real_exec_absent", dryrun_summary.get("functional_slice_real_execution_absent") is True)

    for sid in FUNCTIONAL_SLICE_CHAINS:
        _add(checks, f"upstream.{sid[:18]}.ok", dryrun_summary.get(f"{sid}_dryrun_ok") is True)

    _add(checks, "summary.pass", summary.get("module_governance_closure_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_A)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.closure_only", summary.get("module_governance_closure_only") is True if "module_governance_closure_only" in summary else summary.get("scope") == SCOPE)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.module_state", summary.get("current_module_state") == CURRENT_MODULE_STATE)
    _add(checks, "summary.exec_state", summary.get("real_execution_state") == REAL_EXECUTION_STATE)
    _expect_false(checks, "summary.shared_reval", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.l1_reval", summary.get("l1_input_output_protocol_revalidation"))

    _add(checks, "module_result.complete", module_result.get("module_result_closure_complete") is True)
    _add(checks, "slice_summary.complete", slice_summary.get("functional_slice_closure_summary_complete") is True)
    _add(checks, "gov_rule.complete", gov_closure.get("governance_rule_closure_complete") is True)
    _add(checks, "non_exec.complete", non_exec.get("non_execution_closure_complete") is True)
    _add(checks, "preconds.complete", preconds.get("real_execution_preconditions_complete") is True)
    _add(checks, "decision.complete", decision.get("module_closure_decision_complete") is True)
    _add(checks, "handoff.complete", handoff.get("module_closure_handoff_complete") is True)

    _add(checks, "decision.module_state", decision.get("current_module_state") == CURRENT_MODULE_STATE)
    _add(checks, "decision.exec_state", decision.get("real_execution_state") == REAL_EXECUTION_STATE)
    _add(checks, "decision.allowed3", len(decision.get("allowed_routes") or []) == 3)
    _add(checks, "decision.forbidden6", len(decision.get("forbidden_routes") or []) >= 6)
    _add(checks, "handoff.chain_closed", handoff.get("chain_closed") is True)
    _add(checks, "handoff.no_fragmentary", handoff.get("do_not_extend_fragmentary_phases") is True)
    _add(checks, "handoff.governance_ready", handoff.get("handoff_status") == "governance_ready")

    for sid in FUNCTIONAL_SLICE_CHAINS:
        row = next((s for s in slice_summary.get("slices") or [] if s.get("slice_id") == sid), {})
        _add(checks, f"slice.{sid[:16]}.closed", row.get("candidate_level_result_achieved") is True)
        _add(checks, f"slice.{sid[:16]}.dryrun_ok", row.get("dryrun_ok") is True)

    _add(checks, "slice_summary.all_closed", slice_summary.get("all_slices_candidate_level_closed") is True)
    _add(checks, "slice_summary.count4", slice_summary.get("slice_count") == 4)

    _add(checks, "gov.lightweight", gov_closure.get("lightweight_protocol_refs_only") is True)
    _add(checks, "gov.result_first", bool(gov_closure.get("result_first_module_engineering_rule_ref")))
    _add(checks, "gov.module_first", bool(gov_closure.get("module_first_development_verification_cadence_rule_ref")))
    _add(checks, "gov.reuse_first", bool(gov_closure.get("reuse_first_protocol_engineering_rule_ref")))
    _add(checks, "gov.validate_once", bool(gov_closure.get("validate_once_per_module_rule_ref")))

    _add(checks, "preconds.real_not_auth", preconds.get("real_execution_not_authorized") is True)
    for item in preconds.get("preconditions") or []:
        pid = item.get("precondition_id", "")
        _add(checks, f"precond.{pid[:20]}.status", bool(item.get("status")))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
        _add(checks, f"non_exec.{key}", non_exec.get("absence_matrix", {}).get(key) is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"runtime.no_{flag[:25]}", summary.get(flag) is not True)

    for forbidden in FORBIDDEN_DECISION:
        combined = " ".join([str(summary.get("final_decision") or ""), str(summary.get("recommended_next_phase") or "")]).lower()
        _add(checks, f"forbidden.not_{forbidden}", forbidden not in combined)

    for route in FORBIDDEN_ROUTES:
        _add(checks, f"decision.forbids_{route[:18]}", route in (decision.get("forbidden_routes") or []))

    _add(checks, "summary.prior_dryrun", summary.get("prior_functional_slice_dryrun_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.closure", "Closure" in md)
    _add(checks, "md.no_real", "No real" in md)
    _add(checks, "md.module_state", CURRENT_MODULE_STATE in md)

    _add(checks, "upstream.verifier_min", int(dryrun_verifier.get("passed_checks", 0)) >= 260)
    _add(checks, "upstream.verifier_failed0", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)
    _add(checks, "summary.notification_absent", summary.get("notification_sent_absent") is True)
    _add(checks, "summary.record_absent", summary.get("request_record_absent") is True)
    _add(checks, "summary.approval_absent", summary.get("approval_record_absent") is True)
    _add(checks, "summary.ack_absent", summary.get("ack_record_absent") is True)
    _add(checks, "summary.evidence_absent", summary.get("evidence_bound_record_absent") is True)
    _add(checks, "summary.closure_absent", summary.get("closure_not_executed") is True)
    _add(checks, "summary.foundation_not_frozen", summary.get("foundation_not_frozen") is True)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "file_size.read_strategy", file_size.get("read_strategy") == "summary_index_first")
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "handoff.has_handoff", NEXT_PHASE_A in (handoff.get("next_phase_candidates") or []))
    _add(checks, "handoff.has_preauth", NEXT_PHASE_B in (handoff.get("next_phase_candidates") or []))
    _add(checks, "handoff.has_roadmap", NEXT_PHASE_C in (handoff.get("next_phase_candidates") or []))

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    for idx, doc in enumerate((report, module_result, decision, handoff)):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "summary.no_fragmentary", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "summary.route", summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "module_result.q1", bool(module_result.get("module_governance_question_1")))
    _add(checks, "non_exec.q3", bool(non_exec.get("module_governance_question_3")))
    _add(checks, "preconds.q4", bool(preconds.get("module_governance_question_4")))
    _add(checks, "handoff.q2", bool(handoff.get("module_governance_question_2")))
    _add(checks, "decision.closure_stmt", bool(decision.get("closure_statement")))
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "summary.state_closed", summary.get("current_module_state_governance_candidate_chain_closed") is True)
    _add(checks, "summary.exec_not_auth", summary.get("real_execution_not_authorized") is True)
    _add(checks, "report.module_state", report.get("current_module_state") == CURRENT_MODULE_STATE)
    _add(checks, "report.exec_state", report.get("real_execution_state") == REAL_EXECUTION_STATE)
    _add(checks, "md.exec_state", REAL_EXECUTION_STATE in md)
    _add(checks, "gov.no_fragmentary", gov_closure.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "slice_summary.primary", slice_summary.get("all_slice_primary_results_reached") is True)
    _add(checks, "preconds.len5", len(preconds.get("preconditions") or []) >= 5)
    _add(checks, "module_result.len4", len(module_result.get("slice_results") or []) == 4)
    _add(checks, "upstream.route", dryrun_summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "report.next_candidates", len(report.get("next_phase_candidates") or []) == 3)

    for idx, route in enumerate(decision.get("allowed_routes") or []):
        _add(checks, f"allowed{idx}.phase", bool(route.get("phase_id")))
        _add(checks, f"allowed{idx}.intent", bool(route.get("intent")))

    for idx, row in enumerate(module_result.get("slice_results") or []):
        _add(checks, f"mresult{idx}.primary", row.get("primary_result_reached") is True)
        _add(checks, f"mresult{idx}.label", bool(row.get("result_label")))

    _add(checks, "summary.closure_pass", summary.get("module_governance_closure_pass") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "report.closure_pass", report.get("module_governance_closure_pass") is True)
    _add(checks, "non_exec.real_false", non_exec.get("real_request_issuance_authorized") is False)
    _add(checks, "gov.file_size_ref", bool(gov_closure.get("file_size_module_split_governance_rule_ref")))
    _add(checks, "handoff.recommended", handoff.get("recommended_next_phase") == NEXT_PHASE_A)
    _add(checks, "md.result_closure", "Module result closure" in md)
    _add(checks, "upstream.no_fragmentary", dryrun_summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "slice_summary.forbidden", slice_summary.get("forbidden_state_transitions_absent") is True)
    _add(checks, "slice_summary.real_absent", slice_summary.get("functional_slice_real_execution_absent") is True)
    _add(checks, "precond.owner_blocking", any(
        p.get("precondition_id") == "owner_operator_explicit_approval" and p.get("level") == "blocking_before_real_issuance"
        for p in preconds.get("preconditions") or []
    ))
    _add(checks, "precond.runtime_debt", any(
        p.get("precondition_id") == "runtime_boundary_readiness" and p.get("status") == "future_runtime_debt"
        for p in preconds.get("preconditions") or []
    ))
    _add(checks, "decision.route_a", any(r.get("route_id") == "A" for r in decision.get("allowed_routes") or []))
    _add(checks, "decision.route_b", any(r.get("route_id") == "B" for r in decision.get("allowed_routes") or []))
    _add(checks, "decision.route_c", any(r.get("route_id") == "C" for r in decision.get("allowed_routes") or []))

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "module_governance_closure_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": summary.get("real_request_issuance_authorized") is False,
        "authorization_request_absent": summary.get("authorization_request_absent") is True,
        "current_module_state": CURRENT_MODULE_STATE,
        "real_execution_state": REAL_EXECUTION_STATE,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_A if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": verifier,
                "passed_checks": passed,
                "failed_checks": len(failed),
                "final_decision": report_payload["final_decision"],
                "recommended_next_phase": report_payload["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
