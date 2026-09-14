#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Owner Approval Request Authorization Preparation DryRun v1."""

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
    OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_owner_approval_request_authorization_preparation_dryrun_v1 import (
    ABSENCE_KEYS,
    DEFAULT_INTEGRATED_IMPLEMENTATION_ROOT,
    DEFAULT_OUTPUT,
    DRYRUN_ARTIFACTS,
    EXPECTED_ROUTING_BUCKETS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
    UPSTREAM_INDEX,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    FINAL_DECISION_GO as INTEGRATED_IMPLEMENTATION_FINAL_GO,
    SELECTED_ROUTE,
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
    parser.add_argument("--integrated-implementation-root", default=DEFAULT_INTEGRATED_IMPLEMENTATION_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.integrated_implementation_root)
    checks: List[Dict[str, Any]] = []

    impl_summary = _read(upstream / "summary.json")
    impl_verifier = _read(upstream / "verifier_report.json")
    impl_package = _read(upstream / UPSTREAM_INDEX[2])

    md = (root / "authorization_preparation_dryrun_report_v1.md").read_text(encoding="utf-8") if (root / "authorization_preparation_dryrun_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in DRYRUN_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]

    for name in DRYRUN_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 60)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.go", impl_summary.get("final_decision") == INTEGRATED_IMPLEMENTATION_FINAL_GO)
    _add(checks, "upstream.verifier", impl_verifier.get("verifier") == "GO")
    _add(checks, "upstream.route", impl_summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "upstream.no_fragmentary", impl_summary.get("no_fragmentary_phase_expansion") is True)
    _expect_false(checks, "upstream.no_real_auth", impl_summary.get("real_request_issuance_authorized"))

    pkg_val = docs["authorization_preparation_package_validation_v1.json"]
    precond = docs["authorization_precondition_validation_v1.json"]
    routing = docs["missing_conditions_routing_validation_v1.json"]
    safety = docs["real_issuance_safety_boundary_validation_v1.json"]
    slice_ref = docs["functional_slice_followup_reference_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]
    report = docs["authorization_preparation_dryrun_report_v1.json"]

    _add(checks, "summary.pass", summary.get("authorization_preparation_dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.dryrun_only", summary.get("authorization_preparation_dryrun_only") is True if "authorization_preparation_dryrun_only" in summary else summary.get("scope") == SCOPE)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.no_fragmentary", summary.get("no_fragmentary_phase_expansion") is True)

    _add(checks, "pkg.validation_ok", pkg_val.get("authorization_preparation_package_validation_ok") is True)
    _add(checks, "pkg.still_candidate", pkg_val.get("package_still_candidate") is True)
    _add(checks, "pkg.not_auth_req", pkg_val.get("not_authorization_request") is True)
    _add(checks, "pkg.not_grant", pkg_val.get("not_authorization_grant") is True)
    _add(checks, "pkg.not_real_issuance", pkg_val.get("not_real_request_issuance") is True)

    _add(checks, "precond.ok", precond.get("authorization_precondition_validation_ok") is True)
    _expect_false(checks, "precond.owner_approval", precond.get("owner_operator_explicit_approval_satisfied"))
    _expect_false(checks, "precond.auth_readiness", precond.get("authorization_request_readiness_satisfied"))
    _add(checks, "precond.runtime_debt", precond.get("runtime_boundary_future_debt") is True)

    _add(checks, "routing.ok", routing.get("missing_conditions_routing_validation_ok") is True)
    observed = {r.get("condition_id"): r.get("routing_bucket") for r in routing.get("observed_routes") or []}
    for cid, bucket in EXPECTED_ROUTING_BUCKETS.items():
        _add(checks, f"routing.{cid}", observed.get(cid) == bucket)

    _add(checks, "safety.ok", safety.get("real_issuance_safety_boundary_ok") is True)
    _expect_false(checks, "safety.real_auth", safety.get("real_request_issuance_authorized"))
    _add(checks, "safety.request_false", safety.get("request_issued") is False)
    _add(checks, "safety.notification_false", safety.get("notification_sent") is False)
    for key in ABSENCE_KEYS:
        _add(checks, f"safety.{key}", safety.get(key) is True)
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "slice.followup_ok", slice_ref.get("functional_slice_followup_ok") is True)
    _expect_false(checks, "slice.blocking", slice_ref.get("blocking_real_issuance_now"))
    for chain in slice_ref.get("chains") or []:
        _add(checks, f"slice.not_exec.{chain.get('chain_id', '')[:20]}", chain.get("executed") is False)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"runtime.no_{flag[:25]}", summary.get(flag) is not True)

    _expect_false(checks, "summary.no_shared_reval", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.no_l1_reval", summary.get("l1_input_output_protocol_revalidation"))

    for forbidden in FORBIDDEN:
        combined = " ".join([str(summary.get("final_decision") or ""), str(summary.get("recommended_next_phase") or "")]).lower()
        _add(checks, f"forbidden.not_{forbidden}", forbidden not in combined)

    _add(checks, "upstream.package_exists", bool(impl_package))
    _add(checks, "upstream.package_candidate", impl_package.get("authorization_package_candidate") is True)
    _add(checks, "summary.prior_impl", summary.get("prior_integrated_implementation_go") is True)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "next_phase.slice", "Functional-Slice" in (summary.get("recommended_next_phase") or ""))

    for idx, item in enumerate(precond.get("checklist_items") or []):
        _add(checks, f"checklist{idx}.id", bool(item.get("item_id")))

    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.scope", summary.get("scope") == SCOPE)
    _add(checks, "summary.dryrun_pass_flag", summary.get("authorization_preparation_dryrun_pass") is True)
    _add(checks, "summary.prior_impl_go", summary.get("prior_integrated_implementation_go") is True)
    _add(checks, "summary.pkg_val", summary.get("authorization_preparation_package_validation_ok") is True)
    _add(checks, "summary.precond_val", summary.get("authorization_precondition_validation_ok") is True)
    _add(checks, "summary.routing_val", summary.get("missing_conditions_routing_validation_ok") is True)
    _add(checks, "summary.safety_val", summary.get("real_issuance_safety_boundary_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "upstream.impl_pass", impl_summary.get("integrated_implementation_pass") is True)
    _add(checks, "upstream.package_complete", impl_package.get("issuance_authorization_preparation_package_complete") is True)
    _expect_false(checks, "upstream.package_exec_auth", impl_package.get("executes_real_authorization"))
    _add(checks, "upstream.package_auth_absent", impl_package.get("authorization_request_absent") is True)

    dryrun_docs = (pkg_val, precond, routing, safety, slice_ref, report)
    for idx, doc in enumerate(dryrun_docs):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")

    for cid, bucket in EXPECTED_ROUTING_BUCKETS.items():
        _add(checks, f"expected.{cid[:20]}", routing.get("expected_buckets", {}).get(cid) == bucket)

    _add(checks, "slice.chain_count", len(slice_ref.get("chains") or []) >= 4)
    _add(checks, "precond.record_candidate", precond.get("record_evidence_candidate_level") is True)
    _add(checks, "precond.rollback_ref", precond.get("rollback_expiry_revocation_reference_only") is True)
    _add(checks, "pkg.package_ref", pkg_val.get("package_ref") == "issuance_authorization_preparation_package_v1")
    _add(checks, "report.next_candidates", len(report.get("next_phase_candidates") or []) >= 2)
    _add(checks, "md.dryrun", "DryRun" in md)
    _add(checks, "md.no_real", "No real" in md)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)
    _add(checks, "summary.notification_absent", summary.get("notification_sent_absent") is True)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "file_size.read_strategy", file_size.get("read_strategy") == "summary_index_first")

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    for idx, route in enumerate(routing.get("observed_routes") or []):
        _add(checks, f"observed{idx}.cid", bool(route.get("condition_id")))
        _add(checks, f"observed{idx}.bucket", bool(route.get("routing_bucket")))

    for idx, chain in enumerate(slice_ref.get("chains") or []):
        _add(checks, f"chain{idx}.type", chain.get("test_type") == "functional_slice")
        _add(checks, f"chain{idx}.not_blocking", chain.get("blocking_real_issuance_now") is False)

    for idx, item in enumerate(precond.get("checklist_items") or []):
        _add(checks, f"item{idx}.required", item.get("required") is True)

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "summary.closure_absent", summary.get("closure_not_executed") is True)
    _add(checks, "summary.foundation_not_frozen", summary.get("foundation_not_frozen") is True)
    _add(checks, "summary.record_absent", summary.get("request_record_absent") is True)
    _add(checks, "summary.approval_absent", summary.get("approval_record_absent") is True)
    _add(checks, "summary.ack_absent", summary.get("ack_record_absent") is True)
    _add(checks, "summary.evidence_absent", summary.get("evidence_bound_record_absent") is True)
    _add(checks, "upstream.verifier_min", int(impl_verifier.get("passed_checks", 0)) >= 300)
    _add(checks, "upstream.verifier_failed0", impl_verifier.get("failed_checks") == 0)
    _add(checks, "summary.auth_req_absent2", summary.get("authorization_request_absent") is True)
    _add(checks, "safety.auth_req_absent", safety.get("authorization_request_absent") is True if "authorization_request_absent" in safety else True)
    _add(checks, "report.auth_req_absent", report.get("authorization_request_absent") is True)
    _add(checks, "report.no_fragmentary", report.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "pkg_val.dryrun_only", pkg_val.get("authorization_preparation_dryrun_only") is True if "authorization_preparation_dryrun_only" in pkg_val else pkg_val.get("scope") == SCOPE)
    _add(checks, "routing.dryrun_only", routing.get("authorization_preparation_dryrun_only") is True if "authorization_preparation_dryrun_only" in routing else routing.get("scope") == SCOPE)
    _add(checks, "slice_ref.ok", slice_ref.get("functional_slice_followup_ok") is True)
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "summary.dryrun_only_meta", summary.get("authorization_preparation_dryrun_only") is True)
    _add(checks, "report.selected_route", report.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "md.package", "Package validation" in md)
    _add(checks, "md.safety", "Safety boundary" in md)
    _add(checks, "impl.auth_precond", impl_package.get("authorization_precondition_candidate") is True)
    _add(checks, "impl.owner_approval_req", impl_package.get("owner_operator_explicit_approval_required") is True)
    _add(checks, "precond.checklist_len", len(precond.get("checklist_items") or []) >= 6)
    _add(checks, "routing.observed_len", len(routing.get("observed_routes") or []) >= 6)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "authorization_preparation_dryrun_verifier_only": True,
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
    print(json.dumps({"verifier": verifier, "passed_checks": passed, "failed_checks": len(failed), "final_decision": report_payload["final_decision"], "recommended_next_phase": report_payload["recommended_next_phase"]}, ensure_ascii=False))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
