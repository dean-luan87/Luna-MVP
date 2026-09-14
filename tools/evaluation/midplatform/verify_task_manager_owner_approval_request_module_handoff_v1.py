#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Owner Approval Request Module Handoff v1."""

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
    OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_governance_closure_v1 import (
    CURRENT_MODULE_STATE,
    FINAL_DECISION_GO as MODULE_GOVERNANCE_CLOSURE_FINAL_GO,
    REAL_EXECUTION_STATE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_v1 import (
    ABSENCE_KEYS,
    DEFAULT_MODULE_GOVERNANCE_CLOSURE_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    HANDOFF_ARTIFACTS,
    MIDPLATFORM_MAINLINE_ITEMS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)

MIN_CHECKS = 240
FORBIDDEN: Tuple[str, ...] = (
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
    parser.add_argument("--module-governance-closure-root", default=DEFAULT_MODULE_GOVERNANCE_CLOSURE_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.module_governance_closure_root)
    checks: List[Dict[str, Any]] = []

    closure_summary = _read(upstream / "summary.json")
    closure_verifier = _read(upstream / "verifier_report.json")
    closure_handoff = _read(upstream / "module_closure_handoff_v1.json")

    md = (
        (root / "owner_approval_request_module_handoff_report_v1.md").read_text(encoding="utf-8")
        if (root / "owner_approval_request_module_handoff_report_v1.md").is_file()
        else ""
    )
    docs = {n: _read(root / n) for n in HANDOFF_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["owner_approval_request_module_handoff_report_v1.json"]
    status = docs["owner_approval_request_module_status_summary_v1.json"]
    position = docs["owner_approval_request_midplatform_integration_position_v1.json"]
    boundary = docs["owner_approval_request_handoff_boundary_v1.json"]
    mainline = docs["midplatform_mainline_return_plan_v1.json"]
    test_strategy = docs["future_test_strategy_v1.json"]
    debt = docs["governance_debt_and_future_runtime_handoff_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in HANDOFF_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 60)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.closure_go", closure_summary.get("final_decision") == MODULE_GOVERNANCE_CLOSURE_FINAL_GO)
    _add(checks, "upstream.closure_verifier", closure_verifier.get("verifier") == "GO")
    _add(checks, "upstream.chain_closed", closure_handoff.get("chain_closed") is True)
    _add(checks, "upstream.no_extend", closure_handoff.get("do_not_extend_fragmentary_phases") is True)
    _add(checks, "upstream.module_state", closure_summary.get("current_module_state") == CURRENT_MODULE_STATE)
    _add(checks, "upstream.exec_state", closure_summary.get("real_execution_state") == REAL_EXECUTION_STATE)

    _add(checks, "summary.pass", summary.get("module_handoff_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.handoff_only", summary.get("module_handoff_only") is True if "module_handoff_only" in summary else summary.get("scope") == SCOPE)
    _add(checks, "summary.return_mainline", summary.get("return_to_midplatform_mainline") is True)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.module_state", summary.get("current_module_state") == CURRENT_MODULE_STATE)
    _add(checks, "summary.exec_state", summary.get("real_execution_state") == REAL_EXECUTION_STATE)
    _add(checks, "summary.chain_closed", summary.get("chain_closed") is True)
    _add(checks, "summary.no_extend", summary.get("do_not_extend_fragmentary_phases") is True)
    _add(checks, "summary.chain_not_ext", summary.get("owner_approval_request_chain_not_extended") is True)
    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)

    _add(checks, "report.complete", report.get("module_handoff_report_complete") is True)
    _add(checks, "status.complete", status.get("module_status_summary_complete") is True)
    _add(checks, "position.complete", position.get("midplatform_integration_position_complete") is True)
    _add(checks, "boundary.complete", boundary.get("handoff_boundary_complete") is True)
    _add(checks, "mainline.complete", mainline.get("midplatform_mainline_return_plan_complete") is True)
    _add(checks, "strategy.complete", test_strategy.get("future_test_strategy_complete") is True)
    _add(checks, "debt.complete", debt.get("governance_debt_future_runtime_handoff_complete") is True)

    _add(checks, "status.candidate_closed", status.get("candidate_level_closure_complete") is True)
    _add(checks, "status.real_not_auth", status.get("real_execution_not_authorized") is True)
    _add(checks, "position.governance_ready", position.get("registration_status") == "governance_ready_submodule")
    _add(checks, "position.handoff_mainline", position.get("handoff_to_mainline") is True)
    _add(checks, "position.domains5", len(position.get("midplatform_domains") or []) >= 5)
    _add(checks, "boundary.record_absent", boundary.get("record_creation_absent") is True)
    _add(checks, "boundary.no_deliver_runtime", "runtime" in (boundary.get("does_not_deliver") or []))
    _add(checks, "mainline.return", mainline.get("return_to_broader_midplatform") is True)
    _add(checks, "mainline.next", mainline.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "mainline.no_preauth", mainline.get("do_not_open_real_issuance_preauth_unless_mainline_requires") is True)
    _add(checks, "strategy.no_fragmentary", test_strategy.get("no_fragmentary_phase_tests") is True)
    _add(checks, "strategy.layers4", len(test_strategy.get("test_layers") or []) >= 4)
    _add(checks, "strategy.dryrun_input", test_strategy.get("owner_approval_request_slice_dryrun_available_as_input") is True)
    _add(checks, "debt.runtime_debt", len(debt.get("future_runtime_debt") or []) >= 2)
    _add(checks, "debt.mainline_deferred", debt.get("governance_debt_closure") == "deferred_to_midplatform_mainline")

    for item in MIDPLATFORM_MAINLINE_ITEMS:
        _add(checks, f"mainline.{item['item_id'][:20]}", any(
            i.get("item_id") == item["item_id"] for i in mainline.get("mainline_items") or []
        ))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.no_fragmentary", summary.get("no_fragmentary_phase_expansion") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"runtime.no_{flag[:25]}", summary.get(flag) is not True)

    for forbidden in FORBIDDEN:
        combined = " ".join([str(summary.get("final_decision") or ""), str(summary.get("recommended_next_phase") or "")]).lower()
        _add(checks, f"forbidden.not_{forbidden}", forbidden not in combined)

    _add(checks, "summary.prior_closure", summary.get("prior_module_governance_closure_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.handoff", "Handoff" in md)
    _add(checks, "md.mainline", "mainline" in md.lower())
    _add(checks, "upstream.verifier_min", int(closure_verifier.get("passed_checks", 0)) >= 260)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "file_size.read_strategy", file_size.get("read_strategy") == "summary_index_first")
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "next.broader_roadmap", "Broader-Midplatform" in (summary.get("recommended_next_phase") or ""))

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    for idx, doc in enumerate((report, status, mainline, test_strategy)):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "status.closed_module", status.get("module_id") == "task_manager_owner_approval_request")
    _add(checks, "mainline.handoff_status", mainline.get("owner_approval_request_status") == "handed_off_governance_ready")
    _add(checks, "mainline.items6", len(mainline.get("mainline_items") or []) >= 6)
    _add(checks, "boundary.delivers1", len(boundary.get("delivers") or []) >= 1)
    _add(checks, "boundary.not_deliver7", len(boundary.get("does_not_deliver") or []) >= 7)
    _add(checks, "debt.future_route", "real_request_issuance_preauthorization" in (debt.get("future_routes") or []))
    _expect_false(checks, "summary.shared_reval", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.l1_reval", summary.get("l1_input_output_protocol_revalidation"))
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "status.all_slices", status.get("all_slices_candidate_level_closed") is True)
    _add(checks, "position.explicit_auth", position.get("requires_explicit_authorization_before_runtime") is True)
    _add(checks, "strategy.slice_test", "functional_slice_test" in (test_strategy.get("test_layers") or []))
    _add(checks, "strategy.integration", "midplatform_integration_test" in (test_strategy.get("test_layers") or []))
    _add(checks, "upstream.closure_pass", closure_summary.get("module_governance_closure_pass") is True)
    _add(checks, "report.real_not_auth", report.get("real_execution_not_authorized") is True)
    _add(checks, "md.module_state", CURRENT_MODULE_STATE in md)
    _add(checks, "md.chain_closed", "Chain closed" in md)

    for idx, layer in enumerate(test_strategy.get("test_layers") or []):
        _add(checks, f"layer{idx}", bool(layer))

    for idx, item in enumerate(mainline.get("mainline_items") or []):
        _add(checks, f"item{idx}.status", bool(item.get("status")))

    for idx, deliver in enumerate(boundary.get("does_not_deliver") or []):
        _add(checks, f"nodeliver{idx}", bool(deliver))

    _add(checks, "summary.handoff_pass", summary.get("module_handoff_pass") is True)
    _add(checks, "summary.auth_absent2", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.notification_absent", summary.get("notification_sent_absent") is True)
    _add(checks, "summary.record_absent", summary.get("request_record_absent") is True)
    _add(checks, "summary.approval_absent", summary.get("approval_record_absent") is True)
    _add(checks, "summary.ack_absent", summary.get("ack_record_absent") is True)
    _add(checks, "summary.evidence_absent", summary.get("evidence_bound_record_absent") is True)
    _add(checks, "summary.closure_absent", summary.get("closure_not_executed") is True)
    _add(checks, "summary.foundation_not_frozen", summary.get("foundation_not_frozen") is True)
    _add(checks, "status.functional_slices4", len(status.get("functional_slices") or []) == 4)
    _add(checks, "status.do_not_extend", status.get("do_not_extend_fragmentary_phases") is True)
    _add(checks, "position.task_manager", "task_manager" in (position.get("midplatform_domains") or []))
    _add(checks, "position.approval", "approval" in (position.get("midplatform_domains") or []))
    _add(checks, "position.evidence", "evidence" in (position.get("midplatform_domains") or []))
    _add(checks, "boundary.real_false", boundary.get("real_request_issuance_authorized") is False)
    _add(checks, "boundary.grant_absent", boundary.get("grant_absent") is True)
    _add(checks, "mainline.closed_module_item", any(
        i.get("item_id") == "owner_approval_request_closed_module" for i in mainline.get("mainline_items") or []
    ))
    _add(checks, "debt.adapter_debt", "runtime_adapter_implementation" in (debt.get("future_runtime_debt") or []))
    _add(checks, "debt.whitebox_debt", "whitebox_runtime_integration" in (debt.get("future_runtime_debt") or []))
    _add(checks, "strategy.module_test", "module_level_test" in (test_strategy.get("test_layers") or []))
    _add(checks, "strategy.preauth_gate", "real_execution_preauthorization_gate" in (test_strategy.get("test_layers") or []))
    _add(checks, "report.chain_closed", report.get("chain_closed") is True)
    _add(checks, "report.no_extend", report.get("do_not_extend_fragmentary_phases") is True)
    _add(checks, "report.return_mainline", report.get("return_to_midplatform_mainline") is True)
    _add(checks, "upstream.real_not_auth", closure_summary.get("real_execution_not_authorized") is True)
    _add(checks, "upstream.no_fragmentary", closure_summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "md.exec_state", REAL_EXECUTION_STATE in md)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md)
    _add(checks, "closure_handoff.status", closure_handoff.get("handoff_status") == "governance_ready")
    _add(checks, "closure_handoff.next3", len(closure_handoff.get("next_phase_candidates") or []) >= 3)
    _add(checks, "summary.exec_not_auth", summary.get("real_execution_not_authorized") is True)
    _add(checks, "report.record_creation", report.get("record_creation_absent") is True)
    _add(checks, "report.module_state", report.get("current_module_state") == CURRENT_MODULE_STATE)
    _add(checks, "report.exec_state", report.get("real_execution_state") == REAL_EXECUTION_STATE)
    _add(checks, "status.closure_root", bool(status.get("closure_root")))
    _add(checks, "test_strategy.dryrun_root", bool(test_strategy.get("functional_slice_dryrun_root")))
    _add(checks, "debt.complete_flag", debt.get("governance_debt_future_runtime_handoff_complete") is True)
    _add(checks, "boundary.complete_flag", boundary.get("handoff_boundary_complete") is True)
    _add(checks, "position.complete_flag", position.get("midplatform_integration_position_complete") is True)
    _add(checks, "status.complete_flag", status.get("module_status_summary_complete") is True)
    _add(checks, "mainline.complete_flag", mainline.get("midplatform_mainline_return_plan_complete") is True)
    _add(checks, "strategy.complete_flag", test_strategy.get("future_test_strategy_complete") is True)
    _add(checks, "report.complete_flag", report.get("module_handoff_report_complete") is True)
    _add(checks, "summary.closure_pass_upstream", closure_summary.get("module_governance_closure_pass") is True)
    _add(checks, "upstream.failed0", closure_verifier.get("failed_checks") == 0)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "module_handoff_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": summary.get("real_request_issuance_authorized") is False,
        "authorization_request_absent": summary.get("authorization_request_absent") is True,
        "record_creation_absent": summary.get("record_creation_absent") is True,
        "current_module_state": CURRENT_MODULE_STATE,
        "real_execution_state": REAL_EXECUTION_STATE,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
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
