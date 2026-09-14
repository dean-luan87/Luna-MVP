#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Owner Approval Request Module-Level Functional Slice Planning v1."""

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
    OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_owner_approval_request_authorization_preparation_dryrun_v1 import (
    FINAL_DECISION_GO as AUTHORIZATION_PREPARATION_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    FUNCTIONAL_SLICE_CHAINS,
    SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_level_functional_slice_planning_v1 import (
    ABSENCE_KEYS,
    DEFAULT_AUTHORIZATION_PREPARATION_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_A,
    NEXT_PHASE_B,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    PLANNING_ARTIFACTS,
    SCOPE,
    SLICE_ARTIFACT_BY_ID,
    SLICE_REQUIRED_FIELDS,
    UPSTREAM_INDEX,
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
    parser.add_argument("--authorization-preparation-dryrun-root", default=DEFAULT_AUTHORIZATION_PREPARATION_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.authorization_preparation_dryrun_root)
    checks: List[Dict[str, Any]] = []

    dryrun_summary = _read(upstream / "summary.json")
    dryrun_verifier = _read(upstream / "verifier_report.json")

    md = (root / "module_level_functional_slice_plan_v1.md").read_text(encoding="utf-8") if (root / "module_level_functional_slice_plan_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in PLANNING_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    plan = docs["module_level_functional_slice_plan_v1.json"]
    registry = docs["functional_slice_registry_v1.json"]
    result_first = docs["result_first_module_engineering_rule_reference_v1.json"]
    next_ready = docs["functional_slice_next_phase_readiness_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    slice_docs = {sid: _read(root / SLICE_ARTIFACT_BY_ID[sid]) for sid in FUNCTIONAL_SLICE_CHAINS}

    for name in PLANNING_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 60)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.dryrun_go", dryrun_summary.get("final_decision") == AUTHORIZATION_PREPARATION_DRYRUN_FINAL_GO)
    _add(checks, "upstream.dryrun_verifier", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "upstream.dryrun_pass", dryrun_summary.get("authorization_preparation_dryrun_pass") is True)
    _add(checks, "upstream.route", dryrun_summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "upstream.no_fragmentary", dryrun_summary.get("no_fragmentary_phase_expansion") is True)
    _expect_false(checks, "upstream.no_real_auth", dryrun_summary.get("real_request_issuance_authorized"))

    _add(checks, "summary.pass", summary.get("functional_slice_planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_A)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.planning_only", summary.get("functional_slice_planning_only") is True if "functional_slice_planning_only" in summary else summary.get("scope") == SCOPE)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.no_fragmentary2", summary.get("no_fragmentary_phase_expansion") is True)
    _expect_false(checks, "summary.shared_reval", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.l1_reval", summary.get("l1_input_output_protocol_revalidation"))

    _add(checks, "plan.complete", plan.get("module_level_functional_slice_plan_complete") is True)
    _add(checks, "plan.not_exec", plan.get("execution_allowed") is False)
    _add(checks, "plan.slice_count", len(plan.get("slice_ids") or []) == 4)
    _add(checks, "plan.route", plan.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "plan.result_first_ref", bool(plan.get("result_first_module_engineering_rule_ref")))
    _add(checks, "plan.module_first_ref", bool(plan.get("module_first_development_verification_cadence_rule_ref")))

    _add(checks, "registry.complete", registry.get("functional_slice_registry_complete") is True)
    for entry in registry.get("slices") or []:
        sid = entry.get("slice_id", "")
        _add(checks, f"registry.{sid[:20]}.complete", entry.get("complete") is True)
        _add(checks, f"registry.{sid[:20]}.no_exec", entry.get("execution_allowed") is False)
        _add(checks, f"registry.{sid[:20]}.not_tested", entry.get("test_executed") is False)

    for sid in FUNCTIONAL_SLICE_CHAINS:
        sdoc = slice_docs[sid]
        _add(checks, f"slice.{sid[:18]}.exists", bool(sdoc))
        _add(checks, f"slice.{sid[:18]}.id", sdoc.get("slice_id") == sid)
        _add(checks, f"slice.{sid[:18]}.no_exec", sdoc.get("execution_allowed") is False)
        _add(checks, f"slice.{sid[:18]}.not_tested", sdoc.get("test_executed") is False)
        for field in SLICE_REQUIRED_FIELDS:
            val = sdoc.get(field)
            ok = val is not None and val != "" and not (isinstance(val, (list, dict, tuple)) and len(val) == 0)
            if field in ("execution_allowed", "test_executed"):
                ok = val is False
            _add(checks, f"slice.{sid[:12]}.{field[:20]}", ok)

    _add(checks, "result_first.ok", result_first.get("result_first_rule_ref_ok") is True)
    _add(checks, "result_first.complete", result_first.get("result_first_module_engineering_rule_complete") is True)
    _add(checks, "result_first.module_first", result_first.get("module_first_cadence_rule_ref_ok") is True)
    _add(checks, "result_first.reuse", result_first.get("reuse_first_rule_ref_ok") is True)
    _add(checks, "result_first.validate_once", result_first.get("validate_once_rule_ref_ok") is True)
    _expect_false(checks, "result_first.shared_reval", result_first.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "result_first.l1_reval", result_first.get("l1_input_output_protocol_revalidation"))

    _add(checks, "next.ready", next_ready.get("next_phase_readiness_ok") is True)
    _add(checks, "next.candidates", len(next_ready.get("next_phase_candidates") or []) >= 2)
    candidate_ids = [c.get("phase_id") for c in next_ready.get("next_phase_candidates") or []]
    _add(checks, "next.has_dryrun", NEXT_PHASE_A in candidate_ids)
    _add(checks, "next.has_closure", NEXT_PHASE_B in candidate_ids)

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"runtime.no_{flag[:25]}", summary.get(flag) is not True)

    for forbidden in FORBIDDEN:
        combined = " ".join([str(summary.get("final_decision") or ""), str(summary.get("recommended_next_phase") or "")]).lower()
        _add(checks, f"forbidden.not_{forbidden}", forbidden not in combined)

    _add(checks, "summary.prior_dryrun", summary.get("prior_authorization_preparation_dryrun_go") is True)
    _add(checks, "summary.prior_impl", summary.get("prior_integrated_implementation_go") is True)
    _add(checks, "summary.slice1", summary.get("owner_approval_request_candidate_lifecycle_slice_complete") is True)
    _add(checks, "summary.slice2", summary.get("authorization_preparation_lifecycle_slice_complete") is True)
    _add(checks, "summary.slice3", summary.get("record_approval_ack_evidence_closure_lifecycle_slice_complete") is True)
    _add(checks, "summary.slice4", summary.get("absence_and_rollback_safety_lifecycle_slice_complete") is True)
    _add(checks, "summary.tests_not_exec", summary.get("functional_slice_tests_not_executed") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.scope", summary.get("scope") == SCOPE)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.planning", "planning" in md.lower())
    _add(checks, "md.no_real", "no real" in md.lower())

    _add(checks, "upstream.verifier_min", int(dryrun_verifier.get("passed_checks", 0)) >= 260)
    _add(checks, "upstream.verifier_failed0", dryrun_verifier.get("failed_checks") == 0)
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

    for key in GO_CONDITIONS_KEYS:
        if key in plan:
            _add(checks, f"plan.{key}", plan.get(key) is True)

    planning_docs = (plan, registry, result_first, next_ready)
    for idx, doc in enumerate(planning_docs):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.scope", doc.get("scope") == SCOPE)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")

    for idx, sid in enumerate(FUNCTIONAL_SLICE_CHAINS):
        sdoc = slice_docs[sid]
        _add(checks, f"chain{idx}.primary", bool(sdoc.get("primary_result")))
        _add(checks, f"chain{idx}.entry", bool(sdoc.get("entry_condition")))
        _add(checks, f"chain{idx}.fallback", bool(sdoc.get("fallback_or_defer_strategy")))
        _add(checks, f"chain{idx}.protocol_ref", bool(sdoc.get("protocol_refs_lightweight_only")))

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "plan.final", plan.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "plan.next_candidates", len(plan.get("next_phase_candidates") or []) >= 2)
    _add(checks, "summary.reuse_ok", summary.get("reuse_first_rule_ref_ok") is True)
    _add(checks, "summary.validate_once_ok", summary.get("validate_once_rule_ref_ok") is True)
    _add(checks, "summary.result_first_ok", summary.get("result_first_rule_ref_ok") is True)
    _add(checks, "summary.module_first_ok", summary.get("module_first_cadence_rule_ref_ok") is True)
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "dryrun.auth_req_absent", dryrun_summary.get("authorization_request_absent") is True)
    _add(checks, "dryrun.no_fragmentary", dryrun_summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "plan.tests_not_exec", plan.get("functional_slice_tests_not_executed") is True)
    _add(checks, "registry.slice_len", len(registry.get("slices") or []) == 4)
    _add(checks, "result_first.top_level", bool(result_first.get("top_level_objective_priority_rule_ref")))
    _add(checks, "result_first.file_size_ref", bool(result_first.get("file_size_module_split_governance_rule_ref")))
    _add(checks, "next.recommended", next_ready.get("recommended_next_phase") == NEXT_PHASE_A)
    _add(checks, "md.slice_count", "Slice count" in md)
    _add(checks, "md.route", SELECTED_ROUTE in md)
    _add(checks, "upstream.impl_go_flag", dryrun_summary.get("prior_integrated_implementation_go") is True)
    _add(checks, "summary.plan_complete", summary.get("functional_slice_plan_complete") is True)
    _add(checks, "summary.registry_complete", summary.get("functional_slice_registry_complete") is True)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "functional_slice_planning_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": summary.get("real_request_issuance_authorized") is False,
        "authorization_request_absent": summary.get("authorization_request_absent") is True,
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
