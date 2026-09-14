#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Owner Approval Request Functional Slice DryRun v1."""

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
    OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_owner_approval_request_functional_slice_dryrun_v1 import (
    ABSENCE_KEYS,
    DEFAULT_FUNCTIONAL_SLICE_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    DRYRUN_ARTIFACTS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
    SLICE_DRYRUN_ARTIFACT_BY_ID,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    FUNCTIONAL_SLICE_CHAINS,
    SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_level_functional_slice_planning_v1 import (
    FINAL_DECISION_GO as FUNCTIONAL_SLICE_PLANNING_FINAL_GO,
)

MIN_CHECKS = 260
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
SLICE_CHECK_KEYS: Tuple[str, ...] = (
    "primary_result_reached",
    "entry_condition_met",
    "input_objects_present",
    "output_objects_candidate",
    "state_path_closed",
    "forbidden_state_transitions_absent",
    "success_criteria_met",
    "failure_criteria_recognizable",
    "fallback_or_defer_strategy_present",
    "required_absence_conditions_met",
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
    parser.add_argument("--functional-slice-planning-root", default=DEFAULT_FUNCTIONAL_SLICE_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.functional_slice_planning_root)
    checks: List[Dict[str, Any]] = []

    plan_summary = _read(upstream / "summary.json")
    plan_verifier = _read(upstream / "verifier_report.json")

    md = (root / "functional_slice_dryrun_report_v1.md").read_text(encoding="utf-8") if (root / "functional_slice_dryrun_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in DRYRUN_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["functional_slice_dryrun_report_v1.json"]
    registry = docs["functional_slice_dryrun_registry_v1.json"]
    result_summary = docs["functional_slice_result_summary_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]
    slice_docs = {sid: _read(root / SLICE_DRYRUN_ARTIFACT_BY_ID[sid]) for sid in FUNCTIONAL_SLICE_CHAINS}

    for name in DRYRUN_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 60)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.planning_go", plan_summary.get("final_decision") == FUNCTIONAL_SLICE_PLANNING_FINAL_GO)
    _add(checks, "upstream.planning_verifier", plan_verifier.get("verifier") == "GO")
    _add(checks, "upstream.planning_pass", plan_summary.get("functional_slice_planning_pass") is True)
    _add(checks, "upstream.route", plan_summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "upstream.no_fragmentary", plan_summary.get("no_fragmentary_phase_expansion") is True)

    _add(checks, "summary.pass", summary.get("functional_slice_dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.dryrun_only", summary.get("functional_slice_dryrun_only") is True if "functional_slice_dryrun_only" in summary else summary.get("scope") == SCOPE)
    _add(checks, "summary.single_phase", summary.get("single_phase_all_slices") is True)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _expect_false(checks, "summary.shared_reval", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.l1_reval", summary.get("l1_input_output_protocol_revalidation"))

    _add(checks, "registry.complete", registry.get("functional_slice_dryrun_registry_complete") is True)
    _add(checks, "registry.single_phase", registry.get("single_phase_all_slices") is True)
    for entry in registry.get("slices") or []:
        sid = entry.get("slice_id", "")
        _add(checks, f"registry.{sid[:18]}.ok", entry.get("dryrun_ok") is True)
        _add(checks, f"registry.{sid[:18]}.tested", entry.get("test_executed") is True)
        _expect_false(checks, f"registry.{sid[:18]}.real", entry.get("real_execution"))
        _add(checks, f"registry.{sid[:18]}.no_exec", entry.get("execution_allowed") is False)

    for sid in FUNCTIONAL_SLICE_CHAINS:
        sdoc = slice_docs[sid]
        _add(checks, f"slice.{sid[:18]}.ok", sdoc.get(f"{sid}_dryrun_ok") is True)
        _add(checks, f"slice.{sid[:18]}.tested", sdoc.get("test_executed") is True)
        _expect_false(checks, f"slice.{sid[:18]}.real", sdoc.get("real_execution"))
        _add(checks, f"slice.{sid[:18]}.no_exec", sdoc.get("execution_allowed") is False)
        for key in SLICE_CHECK_KEYS:
            _add(checks, f"slice.{sid[:12]}.{key[:18]}", sdoc.get(key) is True)
        _add(checks, f"slice.{sid[:12]}.fallback", bool(sdoc.get("fallback_or_defer_strategy")))

    _add(checks, "result.all_primary", result_summary.get("all_slice_primary_results_reached") is True)
    _add(checks, "result.forbidden_absent", result_summary.get("forbidden_state_transitions_absent") is True)
    _add(checks, "result.real_absent", result_summary.get("functional_slice_real_execution_absent") is True)
    _add(checks, "result.slice_count", result_summary.get("slice_count") == 4)
    for row in result_summary.get("slice_results") or []:
        sid = row.get("slice_id", "")
        _add(checks, f"result.{sid[:16]}.primary", row.get("primary_result_reached") is True)
        _add(checks, f"result.{sid[:16]}.ok", row.get("dryrun_ok") is True)

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"runtime.no_{flag[:25]}", summary.get(flag) is not True)

    for forbidden in FORBIDDEN:
        combined = " ".join([str(summary.get("final_decision") or ""), str(summary.get("recommended_next_phase") or "")]).lower()
        _add(checks, f"forbidden.not_{forbidden}", forbidden not in combined)

    _add(checks, "summary.prior_planning", summary.get("prior_functional_slice_planning_go") is True)
    _add(checks, "summary.slice1", summary.get("owner_approval_request_candidate_lifecycle_dryrun_ok") is True)
    _add(checks, "summary.slice2", summary.get("authorization_preparation_lifecycle_dryrun_ok") is True)
    _add(checks, "summary.slice3", summary.get("record_approval_ack_evidence_closure_lifecycle_dryrun_ok") is True)
    _add(checks, "summary.slice4", summary.get("absence_and_rollback_safety_lifecycle_dryrun_ok") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.dryrun", "DryRun" in md)
    _add(checks, "md.no_real", "No real" in md)
    _add(checks, "md.single_phase", "Single-phase" in md)

    _add(checks, "upstream.verifier_min", int(plan_verifier.get("passed_checks", 0)) >= 260)
    _add(checks, "upstream.verifier_failed0", plan_verifier.get("failed_checks") == 0)
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
    _add(checks, "next.closure", "Module-Governance-Closure" in (summary.get("recommended_next_phase") or ""))

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    for idx, doc in enumerate((report, registry, result_summary)):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "plan.registry_complete", plan_summary.get("functional_slice_registry_complete") is True)
    _add(checks, "plan.slice_count", len(plan_summary.get("go_conditions") or {}) >= 10 or plan_summary.get("functional_slice_plan_complete") is True)
    _add(checks, "summary.real_exec_absent", summary.get("functional_slice_real_execution_absent") is True)
    _add(checks, "summary.forbidden_absent", summary.get("forbidden_state_transitions_absent") is True)
    _add(checks, "summary.all_primary", summary.get("all_slice_primary_results_reached") is True)
    _add(checks, "registry.len4", len(registry.get("slices") or []) == 4)
    _add(checks, "result.len4", len(result_summary.get("slice_results") or []) == 4)
    _add(checks, "summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "report.route", report.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "md.route", SELECTED_ROUTE in md)
    _add(checks, "md.primary", "primary results" in md.lower())
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "summary.no_fragmentary2", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "report.no_fragmentary", report.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "upstream.plan_complete", plan_summary.get("functional_slice_plan_complete") is True)
    _add(checks, "upstream.prior_dryrun", plan_summary.get("prior_authorization_preparation_dryrun_go") is True)
    _add(checks, "upstream.prior_impl", plan_summary.get("prior_integrated_implementation_go") is True)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "functional_slice_dryrun_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": summary.get("real_request_issuance_authorized") is False,
        "authorization_request_absent": summary.get("authorization_request_absent") is True,
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
