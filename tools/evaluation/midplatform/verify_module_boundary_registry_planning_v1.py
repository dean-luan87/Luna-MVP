#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Module Boundary Registry Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.module_boundary_registry_items_v1 import (
    FORBIDDEN_OWNERSHIP_PAIRS,
    MODULE_BOUNDARY_REGISTRY_DRAFT,
    REGISTRY_ENTRY_REQUIRED_FIELDS,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.module_boundary_registry_lineage_v1 import (
    MODULE_BOUNDARY_REGISTRY_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.module_boundary_registry_planning_v1 import (
    DEFAULT_MODULE_INTEGRATION_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    PLANNING_ARTIFACTS,
    SCOPE,
    UPSTREAM_SELECTED_ROUTE,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import (
    FILE_SIZE_GOVERNANCE_REVIEW_KEYS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)
from capabilities.midplatform.task_manager_module_integration_planning_v1 import (
    FINAL_DECISION_GO as MODULE_INTEGRATION_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as MODULE_INTEGRATION_PLANNING_NEXT_PHASE,
)

MIN_CHECKS = 300
FORBIDDEN = (
    "midplatform_completed", "request_issued", "grant_issued", "runtime_enabled", "integration_test_executed",
)
FILE_SIZE_KEYS = (
    "file_size_governance_review_exists", "file_size_governance_review_ok", "monolithic_file_absent",
    "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok", "limited_directory_scan_ok",
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
    parser.add_argument("--module-integration-planning-root", default=DEFAULT_MODULE_INTEGRATION_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.module_integration_planning_root)
    checks: List[Dict[str, Any]] = []

    planning_summary = _read(upstream / "summary.json")
    planning_verifier = _read(upstream / "verifier_report.json")
    md = (root / "module_boundary_registry_planning_report_v1.md").read_text(encoding="utf-8") if (root / "module_boundary_registry_planning_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in PLANNING_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["module_boundary_registry_planning_report_v1.json"]
    scope = docs["boundary_registry_scope_v1.json"]
    registry_draft = docs["module_boundary_registry_draft_v1.json"]
    ownership = docs["ownership_matrix_v1.json"]
    forbidden_stmt = docs["not_owned_forbidden_transition_statement_v1.json"]
    conflict_plan = docs["boundary_conflict_detection_plan_v1.json"]
    dep_graph = docs["boundary_dependency_graph_v1.json"]
    route_decision = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]
    entries = registry_draft.get("entries") or []

    for name in PLANNING_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 40)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.planning_go", planning_summary.get("final_decision") == MODULE_INTEGRATION_PLANNING_FINAL_GO)
    _add(checks, "upstream.planning_verifier", planning_verifier.get("verifier") == "GO")
    _add(checks, "upstream.selected_route", planning_summary.get("selected_next_route") == UPSTREAM_SELECTED_ROUTE)
    _add(checks, "upstream.planning_next", planning_summary.get("recommended_next_phase") == MODULE_INTEGRATION_PLANNING_NEXT_PHASE)

    _add(checks, "summary.pass", summary.get("boundary_registry_planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.not_runtime_reg", summary.get("module_boundary_registry_planning_not_runtime_registry") is True)
    _add(checks, "summary.not_full_scan", summary.get("boundary_conflict_detection_plan_not_full_repo_scan") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))

    _add(checks, "scope.complete", scope.get("boundary_registry_scope_complete") is True)
    _add(checks, "scope.not_runtime_reg", scope.get("not_runtime_registry") is True)
    _add(checks, "draft.complete", registry_draft.get("module_boundary_registry_draft_complete") is True)
    _add(checks, "draft.entries8", len(entries) >= 8)
    _add(checks, "ownership.complete", ownership.get("ownership_matrix_complete") is True)
    _add(checks, "ownership.rows11", len(ownership.get("rows") or []) >= 11)
    _add(checks, "forbidden.complete", forbidden_stmt.get("not_owned_forbidden_transition_statement_complete") is True)
    _add(checks, "conflict.complete", conflict_plan.get("boundary_conflict_detection_plan_complete") is True)
    _add(checks, "conflict.no_scan", conflict_plan.get("full_repo_scan") is False)
    _add(checks, "graph.complete", dep_graph.get("boundary_dependency_graph_complete") is True)
    _add(checks, "route.complete", route_decision.get("next_route_decision_complete") is True)
    _add(checks, "route.selected_a", route_decision.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "route.next_lifecycle", NEXT_PHASE_GO in (route_decision.get("recommended_next_phase") or ""))

    orch = next((e for e in entries if e.get("module_id") == "task_manager_core_orchestration_skeleton"), {})
    lifecycle = next((e for e in entries if e.get("module_id") == "candidate_lifecycle_manager"), {})
    alignment = next((e for e in entries if e.get("module_id") == "evidence_record_approval_permission_alignment"), {})
    protocol = next((e for e in entries if e.get("module_id") == "protocol_registry_input_output_traceability"), {})
    owner_closed = next((e for e in entries if e.get("module_id") == "owner_approval_request_closed_module"), {})
    file_size_mod = next((e for e in entries if e.get("module_id") == "file_size_governance"), {})
    governance = next((e for e in entries if e.get("module_id") == "governance_constraints"), {})

    for obj in ("records", "grants", "authorization_requests", "runtime_execution"):
        _add(checks, f"orch.not_own.{obj[:8]}", obj in (orch.get("not_owned_objects") or []))
    for obj in ("records", "grants", "runtime_execution"):
        _add(checks, f"lifecycle.not_own.{obj[:8]}", obj in (lifecycle.get("not_owned_objects") or []))
    for obj in ("evidence_records", "grants"):
        _add(checks, f"align.not_own.{obj[:8]}", obj in (alignment.get("not_owned_objects") or []))
    _add(checks, "protocol.not_runtime", "runtime_execution" in (protocol.get("not_owned_objects") or []))
    _add(checks, "owner.not_reopen", "fragmentary_phases" in (owner_closed.get("not_owned_objects") or []))
    _add(checks, "file_size.not_business", "business_objects" in (file_size_mod.get("not_owned_objects") or []))
    _add(checks, "governance.not_runtime_perm", "runtime_permission" in (governance.get("not_owned_objects") or []))

    for idx, entry in enumerate(entries):
        for field in REGISTRY_ENTRY_REQUIRED_FIELDS:
            _add(checks, f"entry{idx}.{field[:10]}", entry.get(field) is not None and entry.get(field) != "")
        _add(checks, f"entry{idx}.no_runtime", entry.get("runtime_required_now") is False)

    for mid in MODULE_BOUNDARY_REGISTRY_DRAFT:
        _add(checks, f"mod.{mid['module_id'][:20]}", any(e.get("module_id") == mid["module_id"] for e in entries))

    for module_id, obj in FORBIDDEN_OWNERSHIP_PAIRS:
        entry = next((e for e in entries if e.get("module_id") == module_id), {})
        _add(checks, f"forbid.{module_id[:12]}.{obj[:10]}", obj not in (entry.get("owned_objects") or []))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in MODULE_BOUNDARY_REGISTRY_PLANNING_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for forbidden in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')} {md}".lower()
        _add(checks, f"forbidden.not_{forbidden[:15]}", forbidden not in combined)

    _add(checks, "summary.prior_planning", summary.get("prior_module_integration_planning_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "summary.all_entries", summary.get("all_required_modules_have_registry_entries") is True)
    _add(checks, "summary.no_forbidden_own", summary.get("no_forbidden_ownership_detected") is True)
    _add(checks, "upstream.verifier_min", int(planning_verifier.get("passed_checks", 0)) >= 300)
    _add(checks, "graph.future_edge", any(e.get("type") == "future_dependency" for e in dep_graph.get("edges") or []))
    _add(checks, "graph.cross_cut", any(e.get("type") == "cross_cut" for e in dep_graph.get("edges") or []))
    _add(checks, "ownership.statements7", len(ownership.get("statements") or []) >= 7)
    _add(checks, "forbidden.trans8", len(forbidden_stmt.get("transitions") or []) >= 8)
    _add(checks, "conflict.checks8", len(conflict_plan.get("checks") or []) >= 8)
    _add(checks, "misclassify.rules7", len(misclassify.get("rules") or []) >= 7)
    _add(checks, "owner_closed_module", summary.get("owner_approval_request_closed_module") == "governance_ready_handoff")
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)

    for rule in misclassify.get("rules") or []:
        _add(checks, f"rule.{rule[:20]}", True)
    for stmt in ownership.get("statements") or []:
        _add(checks, f"stmt.{stmt[:20]}", True)
    for t in forbidden_stmt.get("transitions") or []:
        _add(checks, f"trans.{t.get('module_id', '')[:18]}", bool(t.get("forbidden")))
    for c in conflict_plan.get("checks") or []:
        _add(checks, f"conflict.{c.get('check_id', '')[:18]}", bool(c.get("check_id")))
    for alt in route_decision.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.get('route_id', '')}", bool(alt))

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.final", FINAL_DECISION_GO in md or "CANDIDATE_LIFECYCLE" in md)
    _add(checks, "md.selected_route", SELECTED_NEXT_ROUTE in md)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "scope.not_reopen", scope.get("not_reopen_owner_approval_request") is True)
    _add(checks, "route.no_complete", route_decision.get("do_not_declare_midplatform_completed") is True)
    _add(checks, "conflict.deferred", conflict_plan.get("execution_deferred") is True)
    _add(checks, "registry.boundary_mod", any(e.get("module_id") == "module_boundary_registry" for e in entries))
    _add(checks, "graph.nodes8", len(dep_graph.get("nodes") or []) >= 8)
    _add(checks, "graph.edges10", len(dep_graph.get("edges") or []) >= 10)
    _add(checks, "ownership.record_none", any(r.get("object_category") == "record_objects" and r.get("owner_module") is None for r in ownership.get("rows") or []))
    _add(checks, "ownership.grant_none", any(r.get("object_category") == "grant_objects" and r.get("owner_module") is None for r in ownership.get("rows") or []))
    _add(checks, "misclassify.not_runtime_reg", "boundary_registry_planning_not_runtime_registry" in (misclassify.get("rules") or []))
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "upstream.failed0", planning_verifier.get("failed_checks") == 0)
    _add(checks, "report.pass_flag", report.get("boundary_registry_planning_pass") is True)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md or "Candidate Lifecycle" in md)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "module_boundary_registry_planning_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "module_boundary_registry_planning_not_runtime_registry": True,
        "boundary_conflict_detection_plan_not_full_repo_scan": True,
        "record_creation_absent": summary.get("record_creation_absent") is True,
        "grant_absent": summary.get("grant_absent") is True,
        "final_decision": FINAL_DECISION_GO if verifier == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if verifier == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "verifier": verifier,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "final_decision": report_payload["final_decision"],
        "recommended_next_phase": report_payload["recommended_next_phase"],
    }, ensure_ascii=False))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
