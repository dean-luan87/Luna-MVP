#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Owner Approval Request Governance Gate Integrated Planning v1."""

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
    OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_planning_v1 import (
    ABSENCE_KEYS,
    DEFAULT_FINAL_GATE_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    FINAL_GATE_INDEX_FILES,
    GO_CONDITIONS_KEYS,
    INTEGRATED_ARTIFACTS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    ROUTE_A,
    ROUTE_C,
    ROUTE_D,
    ROUTE_E,
    SCOPE,
    SLICE_TEST_SCOPES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1 import (
    FINAL_DECISION_GO as FINAL_GATE_PLANNING_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1 import (
    CANDIDATE_BOUNDARY_PAIRS,
    CORE_CANDIDATE_IDS,
)

MIN_CHECKS = 280
FORBIDDEN_TARGETS: Tuple[str, ...] = (
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


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool) -> None:
    checks.append({"check_id": check_id, "passed": bool(passed)})


def _expect_false(checks: List[Dict[str, Any]], check_id: str, value: Any) -> None:
    _add(checks, check_id, value is False)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--final-gate-planning-root", default=DEFAULT_FINAL_GATE_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    final_gate = Path(args.final_gate_planning_root)
    checks: List[Dict[str, Any]] = []

    gate_summary = _read(final_gate / "summary.json")
    gate_verifier = _read(final_gate / "verifier_report.json")
    gate_missing = _read(final_gate / FINAL_GATE_INDEX_FILES[2])

    md = (root / "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.md").read_text(encoding="utf-8") if (root / "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in INTEGRATED_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]

    for name in INTEGRATED_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        _add(checks, f"artifact.exists.{name.split('.')[0][:40]}", path.is_file())
        if name.endswith(".json"):
            _add(checks, f"artifact.ok.{name.split('.')[0][:40]}", bool(_read(path)))
        else:
            _add(checks, f"artifact.ok.{name.split('.')[0][:40]}", len(md.strip()) > 80)

    _add(checks, "upstream.go", gate_summary.get("final_decision") == FINAL_GATE_PLANNING_FINAL_GO)
    _add(checks, "upstream.verifier_go", gate_verifier.get("verifier") == "GO")
    _add(checks, "upstream.plan_complete", gate_summary.get("final_gate_plan_complete") is True)

    plan = docs["task_manager_owner_approval_request_governance_gate_integrated_plan_v1.json"]
    route_matrix = docs["task_manager_owner_approval_request_governance_gate_route_matrix_v1.json"]
    mapping = docs["task_manager_owner_approval_request_governance_gate_missing_conditions_route_mapping_v1.json"]
    auth_plan = docs["task_manager_owner_approval_request_governance_gate_issuance_authorization_plan_v1.json"]
    closure = docs["task_manager_owner_approval_request_governance_gate_record_approval_ack_evidence_closure_boundary_v1.json"]
    slice_plan = docs["task_manager_owner_approval_request_governance_gate_module_level_functional_slice_test_plan_v1.json"]
    boundary = docs["task_manager_owner_approval_request_governance_gate_non_execution_boundary_v1.json"]
    next_phase = docs["task_manager_owner_approval_request_governance_gate_next_phase_readiness_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    _add(checks, "summary.pass", summary.get("integrated_planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.integrated_only", summary.get("integrated_planning_only") is True)
    _add(checks, "summary.selected_route", summary.get("selected_route") == ROUTE_A)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.no_real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.not_executed", summary.get("real_request_issuance_not_executed") is True)

    blocks = plan.get("integrated_blocks") or []
    for block in (
        "roadmap_decision",
        "issuance_authorization_planning",
        "missing_conditions_routing",
        "record_approval_ack_evidence_closure_boundary",
        "module_level_functional_slice_test_planning",
    ):
        _add(checks, f"plan.block.{block}", block in blocks)

    _add(checks, "route_matrix.complete", route_matrix.get("route_matrix_complete") is True)
    _add(checks, "route_matrix.route_a", route_matrix.get("selected_route") == ROUTE_A)

    cond_map = {m.get("condition_id"): m for m in mapping.get("mappings") or []}
    _add(checks, "mapping.count", len(cond_map) >= 6)
    _add(checks, "mapping.real.blocker", cond_map.get("real_request_issuance", {}).get("source_category") == "blocker")
    _add(checks, "mapping.real.route_a", cond_map.get("real_request_issuance", {}).get("primary_route") == ROUTE_A)
    _add(checks, "mapping.runtime.route_d", cond_map.get("runtime_adapter_implementation", {}).get("primary_route") == ROUTE_D)
    _add(checks, "mapping.whitebox.route_d", cond_map.get("whitebox_runtime_integration", {}).get("primary_route") == ROUTE_D)
    _add(checks, "mapping.slice.route_c", cond_map.get("module_level_functional_slice_tests", {}).get("primary_route") == ROUTE_C)
    _add(checks, "mapping.gov.route_e", cond_map.get("governance_debt_closure", {}).get("primary_route") == ROUTE_E)
    _add(checks, "mapping.chain.resolved", cond_map.get("record_approval_closure_candidate_chain", {}).get("source_resolved") is True)

    _add(checks, "auth_plan.complete", auth_plan.get("issuance_authorization_plan_complete") is True)
    _expect_false(checks, "auth_plan.no_real_issuance", auth_plan.get("executes_real_issuance"))
    _expect_false(checks, "auth_plan.no_notification", auth_plan.get("executes_real_notification"))

    _add(checks, "closure.complete", closure.get("record_approval_ack_evidence_boundary_complete") is True)
    for cid in CORE_CANDIDATE_IDS:
        row = next((r for r in closure.get("rows") or [] if r.get("candidate_id") == cid), {})
        _add(checks, f"closure.still.{cid[:20]}", row.get("still_candidate") is True)
        _add(checks, f"closure.not_created.{cid[:20]}", row.get("record_created") is False)
    for candidate, forbidden in CANDIDATE_BOUNDARY_PAIRS:
        _add(checks, f"closure.ne.{candidate[:20]}", candidate != forbidden)

    _add(checks, "slice.complete", slice_plan.get("module_level_slice_test_plan_complete") is True)
    _add(checks, "slice.count", len(slice_plan.get("slice_tests") or []) == len(SLICE_TEST_SCOPES))
    for t in slice_plan.get("slice_tests") or []:
        _add(checks, f"slice.not_blocking.{t.get('scope_id', '')[:20]}", t.get("blocking_governance_gate") is False)
        _add(checks, f"slice.not_executed.{t.get('scope_id', '')[:20]}", t.get("executed") is False)

    _add(checks, "boundary.ok", boundary.get("non_execution_boundary_ok") is True)
    for key in ABSENCE_KEYS:
        _add(checks, f"boundary.{key}", boundary.get(key) is True)
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "next_phase.ok", next_phase.get("next_phase_readiness_ok") is True)
    _add(checks, "next_phase.integrated_dryrun", "Integrated-DryRun" in (next_phase.get("recommended_next_phase") or ""))

    for forbidden in FORBIDDEN_TARGETS:
        combined = " ".join([str(summary.get("final_decision") or ""), str(summary.get("recommended_next_phase") or "")]).lower()
        _add(checks, f"final.not_{forbidden}", forbidden not in combined)

    for key in FILE_SIZE_SUMMARY_KEYS:
        _add(checks, f"file_size.summary.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)

    for rel in OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True)

    for flag in RUNTIME_FORBIDDEN_FLAGS:
        _add(checks, f"summary.no_runtime.{flag[:30]}", summary.get(flag) is not True)

    _expect_false(checks, "summary.no_shared_reval", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.no_l1_reval", summary.get("l1_input_output_protocol_revalidation"))
    _add(checks, "summary.roadmap_integrated", summary.get("roadmap_decision_integrated") is True)
    _add(checks, "summary.prior_gate", summary.get("prior_final_gate_planning_go") is True)
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.integrated", "integrated planning" in md.lower())
    _add(checks, "summary.issues_empty", summary.get("issues") == [])

    for idx, m in enumerate(mapping.get("mappings") or []):
        _add(checks, f"mapping{idx}.disposition", bool(m.get("disposition")))
    for idx, step in enumerate(auth_plan.get("authorization_steps") or []):
        _add(checks, f"auth_step{idx}", bool(step))
    for idx, route in enumerate(route_matrix.get("routes") or []):
        _add(checks, f"route{idx}.no_exec", route.get("executes_real_issuance") is False)

    upstream_conds = gate_missing.get("conditions") or []
    for cond in upstream_conds:
        cid = cond.get("condition_id")
        _add(checks, f"upstream_mapped.{cid}", cid in cond_map)

    _add(checks, "plan.complete", plan.get("integrated_planning_complete") is True)
    _add(checks, "mapping.complete", mapping.get("missing_conditions_route_mapping_complete") is True)
    _add(checks, "summary.integrated_complete", summary.get("integrated_planning_complete") is True)
    _add(checks, "summary.route_matrix", summary.get("route_matrix_complete") is True)
    _add(checks, "summary.auth_plan", summary.get("issuance_authorization_plan_complete") is True)
    _add(checks, "summary.closure_boundary", summary.get("record_approval_ack_evidence_boundary_complete") is True)
    _add(checks, "summary.slice_plan", summary.get("module_level_slice_test_plan_complete") is True)
    _add(checks, "summary.missing_mapping", summary.get("missing_conditions_route_mapping_complete") is True)
    _add(checks, "upstream.missing_matrix", gate_summary.get("missing_conditions_matrix_complete") is True)
    _add(checks, "upstream.blocker_matrix", gate_summary.get("blocker_matrix_complete") is True)
    _add(checks, "upstream.file_size", gate_summary.get("file_size_governance_review_ok") is True)
    _add(checks, "upstream.non_execution", gate_summary.get("non_execution_boundary_ok") is True)
    _add(checks, "upstream.passed_min", int(gate_verifier.get("passed_checks", 0)) >= 300)
    _add(checks, "upstream.failed_zero", gate_verifier.get("failed_checks") == 0)
    _add(checks, "plan.selected_route", plan.get("selected_route") == ROUTE_A)
    _expect_false(checks, "plan.no_real_auth", plan.get("real_request_issuance_authorized"))
    _add(checks, "auth_plan.steps", len(auth_plan.get("authorization_steps") or []) >= 4)
    _add(checks, "closure.pairs", len(closure.get("boundary_pairs") or []) >= 5)
    _add(checks, "closure.core_ids", len(closure.get("core_candidate_ids") or []) >= 5)
    _add(checks, "slice.planned", all(t.get("planned") for t in slice_plan.get("slice_tests") or []))
    _add(checks, "boundary.request_false", boundary.get("request_issued") is False)
    _add(checks, "boundary.notification_false", boundary.get("notification_sent") is False)
    _add(checks, "next_phase.target", next_phase.get("target") == "owner_approval_request_governance_gate_integrated_dryrun")
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.scope", summary.get("scope") == SCOPE)
    _add(checks, "md.route_a", ROUTE_A in md)
    _add(checks, "md.no_real", "No real request" in md)

    gate_docs = (plan, route_matrix, mapping, auth_plan, closure, slice_plan, boundary, next_phase)
    for idx, doc in enumerate(gate_docs):
        _add(checks, f"doc{idx}.phase", doc.get("phase") == PHASE_ID)
        _add(checks, f"doc{idx}.integrated_only", doc.get("integrated_planning_only") is True)
        _add(checks, f"doc{idx}.runtime_off", doc.get("runtime_status") == "not_enabled")

    for idx, route in enumerate(route_matrix.get("routes") or []):
        _add(checks, f"route{idx}.label", bool(route.get("route_label")))
        _add(checks, f"route{idx}.role", bool(route.get("role")))

    for key in GO_CONDITIONS_KEYS:
        if key in plan:
            _add(checks, f"plan.{key}", plan.get(key) is True)
        if key in auth_plan:
            _add(checks, f"auth.{key}", auth_plan.get(key) is True)

    for cid in CORE_CANDIDATE_IDS:
        _add(checks, f"closure.has.{cid[:25]}", any(r.get("candidate_id") == cid for r in closure.get("rows") or []))

    for cat in ("blocker", "future_runtime", "non_blocking", "governance_debt"):
        _add(checks, f"mapping.cat.{cat}", any(m.get("source_category") == cat for m in mapping.get("mappings") or []))

    _add(checks, "summary.next_phase_ok", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.file_size_ok", summary.get("file_size_governance_review_ok") is True)
    _add(checks, "summary.non_execution", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "file_size.full_repo_absent", file_size.get("full_repo_scan") is False)
    _add(checks, "file_size.read_strategy", file_size.get("read_strategy") == "summary_index_first")

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "integrated_planning_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "selected_route": summary.get("selected_route"),
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "passed_checks": passed, "failed_checks": len(failed), "selected_route": report["selected_route"], "final_decision": report["final_decision"], "recommended_next_phase": report["recommended_next_phase"]}, ensure_ascii=False))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
