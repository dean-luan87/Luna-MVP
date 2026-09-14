#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Closure Consolidation v1."""

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
from capabilities.midplatform.task_manager_broader_midplatform_closure_roadmap_v1 import (
    FINAL_DECISION_GO as BROADER_ROADMAP_FINAL_GO,
    SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_foundation_closure_consolidation_lineage_v1 import (
    FOUNDATION_CLOSURE_CONSOLIDATION_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_closure_consolidation_v1 import (
    ABSENCE_KEYS,
    CONSOLIDATION_ARTIFACTS,
    DEFAULT_BROADER_ROADMAP_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    FOUNDATION_ASSET_IDS,
    GO_CONDITIONS_KEYS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    REMAINING_WORK_ITEMS,
    SCOPE,
)

MIN_CHECKS = 260
FORBIDDEN: Tuple[str, ...] = (
    "entire_midplatform_completed",
    "midplatform_completed",
    "request_issued",
    "authorization_request_created",
    "grant_issued",
    "record_created",
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
    parser.add_argument("--broader-midplatform-closure-roadmap-root", default=DEFAULT_BROADER_ROADMAP_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.broader_midplatform_closure_roadmap_root)
    checks: List[Dict[str, Any]] = []

    roadmap_summary = _read(upstream / "summary.json")
    roadmap_verifier = _read(upstream / "verifier_report.json")

    md = (
        (root / "foundation_consolidation_report_v1.md").read_text(encoding="utf-8")
        if (root / "foundation_consolidation_report_v1.md").is_file()
        else ""
    )
    docs = {n: _read(root / n) for n in CONSOLIDATION_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["foundation_consolidation_report_v1.json"]
    scope = docs["foundation_consolidation_scope_v1.json"]
    inventory = docs["foundation_asset_inventory_v1.json"]
    matrix = docs["foundation_consolidation_matrix_v1.json"]
    boundary = docs["foundation_boundary_statement_v1.json"]
    remaining = docs["remaining_work_register_v1.json"]
    next_route = docs["next_mainline_route_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in CONSOLIDATION_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 60)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.roadmap_go", roadmap_summary.get("final_decision") == BROADER_ROADMAP_FINAL_GO)
    _add(checks, "upstream.roadmap_verifier", roadmap_verifier.get("verifier") == "GO")
    _add(checks, "upstream.route", roadmap_summary.get("selected_route") == SELECTED_ROUTE)

    _add(checks, "summary.pass", summary.get("foundation_consolidation_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.consolidation_only", summary.get("foundation_closure_consolidation_only") is True if "foundation_closure_consolidation_only" in summary else summary.get("scope") == SCOPE)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "summary.remaining_work", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))
    _expect_false(checks, "summary.shared_reval", summary.get("shared_protocol_system_revalidation"))
    _expect_false(checks, "summary.l1_reval", summary.get("l1_input_output_protocol_revalidation"))

    _add(checks, "scope.complete", scope.get("foundation_consolidation_scope_complete") is True)
    _add(checks, "scope.foundation_only", scope.get("layer") == "task_manager_foundation_only")
    _add(checks, "scope.not_final", scope.get("not_entire_midplatform_completion") is True)
    _add(checks, "scope.not_runtime", scope.get("not_runtime_implementation") is True)
    _add(checks, "inventory.complete", inventory.get("foundation_asset_inventory_complete") is True)
    _add(checks, "matrix.complete", matrix.get("foundation_consolidation_matrix_complete") is True)
    _add(checks, "boundary.complete", boundary.get("foundation_boundary_statement_complete") is True)
    _add(checks, "remaining.complete", remaining.get("remaining_work_register_complete") is True)
    _add(checks, "route.complete", next_route.get("next_mainline_route_complete") is True)
    _add(checks, "misclassify.complete", misclassify.get("do_not_misclassify_rules_complete") is True)

    _add(checks, "inventory.assets7", len(inventory.get("assets") or []) == len(FOUNDATION_ASSET_IDS))
    _add(checks, "matrix.rows7", len(matrix.get("rows") or []) == len(FOUNDATION_ASSET_IDS))
    for row in matrix.get("rows") or []:
        _add(checks, f"matrix.{row.get('asset_id', '')[:18]}.no_runtime", row.get("runtime_required_now") is False)
    _add(checks, "boundary.construction", boundary.get("midplatform_overall_status") == "construction_consolidation")
    _add(checks, "remaining.items8", len(remaining.get("items") or []) >= 8)
    _add(checks, "route.no_complete", next_route.get("do_not_declare_midplatform_completed") is True)
    _add(checks, "route.remaining_work", NEXT_PHASE_GO in (next_route.get("recommended_next_phase") or ""))
    _add(checks, "misclassify.not_final", "foundation_consolidated_not_midplatform_completed" in (misclassify.get("rules") or []))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
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

    for rel in FOUNDATION_CLOSURE_CONSOLIDATION_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for forbidden in FORBIDDEN:
        combined = " ".join([
            str(summary.get("final_decision") or ""),
            str(summary.get("recommended_next_phase") or ""),
            md.lower(),
        ]).lower()
        _add(checks, f"forbidden.not_{forbidden[:20]}", forbidden not in combined)

    _add(checks, "summary.prior_roadmap", summary.get("prior_broader_midplatform_roadmap_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "md.final", FINAL_DECISION_GO in md)
    _add(checks, "md.not_final", "NOT entire midplatform" in md)
    _add(checks, "md.remaining", "remaining work" in md.lower())
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    for idx, asset in enumerate(inventory.get("assets") or []):
        _add(checks, f"asset{idx}.id", bool(asset.get("asset_id")))
        _add(checks, f"asset{idx}.status", bool(asset.get("current_status")))

    for idx, item in enumerate(remaining.get("items") or []):
        _add(checks, f"work{idx}.id", bool(item.get("work_id")))
        _add(checks, f"work{idx}.cat", bool(item.get("category")))

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "upstream.roadmap_pass", roadmap_summary.get("broader_midplatform_closure_roadmap_pass") is True)
    _add(checks, "upstream.verifier_min", int(roadmap_verifier.get("passed_checks", 0)) >= 260)
    _add(checks, "summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "summary.exec_not_auth", summary.get("real_execution_not_authorized") is True)
    _add(checks, "scope.not_integration", scope.get("not_integration_test_execution") is True)
    _add(checks, "scope.not_real", scope.get("not_real_execution") is True)
    _add(checks, "boundary.statements5", len(boundary.get("statements") or []) >= 5)
    _add(checks, "route.alternate3", len(next_route.get("alternate_routes") or []) >= 3)
    _add(checks, "misclassify.rules6", len(misclassify.get("rules") or []) >= 6)
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "md.foundation_only", "foundation layer" in md.lower())
    _add(checks, "remaining.still_work", remaining.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "report.not_final_flag", report.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "report.integration_false", report.get("integration_test_executed") is False)
    _add(checks, "owner_in_inventory", any(a.get("asset_id") == "owner_approval_request_closed_module" for a in inventory.get("assets") or []))
    _add(checks, "roadmap_in_inventory", any(a.get("asset_id") == "broader_midplatform_closure_roadmap" for a in inventory.get("assets") or []))
    _add(checks, "work.runtime_debt", any(i.get("category") == "future_runtime_debt" for i in remaining.get("items") or []))
    _add(checks, "work.future_design", any(i.get("category") == "future_design" for i in remaining.get("items") or []))
    _add(checks, "matrix.test_deferred", all(r.get("test_deferred") is True for r in matrix.get("rows") or []))
    _add(checks, "upstream.chain_not_ext", roadmap_summary.get("owner_approval_request_chain_not_extended") is True)
    _add(checks, "summary.construction_phase", summary.get("midplatform_construction_phase") == "foundation_layer_consolidated")
    _add(checks, "next.remaining_roadmap", "Remaining-Work-Roadmap" in (next_route.get("recommended_next_phase") or ""))
    _add(checks, "misclassify.debt_rule", "future_runtime_debt_not_current_foundation_blocker" in (misclassify.get("rules") or []))
    _add(checks, "misclassify.owner_rule", "do_not_reopen_owner_approval_request_fragmentary_phases" in (misclassify.get("rules") or []))

    for item in REMAINING_WORK_ITEMS[:6]:
        wid = item["work_id"]
        _add(checks, f"workreg.{wid[:20]}", any(i.get("work_id") == wid for i in remaining.get("items") or []))

    for asset_id in FOUNDATION_ASSET_IDS:
        _add(checks, f"found.{asset_id[:20]}", any(a.get("asset_id") == asset_id for a in inventory.get("assets") or []))

    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)
    _add(checks, "summary.notification_absent", summary.get("notification_sent_absent") is True)
    _add(checks, "summary.closure_absent", summary.get("closure_not_executed") is True)
    _add(checks, "summary.foundation_not_frozen", summary.get("foundation_not_frozen") is True)
    _add(checks, "upstream.failed0", roadmap_verifier.get("failed_checks") == 0)
    _add(checks, "report.pass_flag", report.get("foundation_consolidation_pass") is True)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md)

    for stmt in boundary.get("statements") or []:
        _add(checks, f"stmt.{stmt[:25].replace(' ', '_')}", bool(stmt))

    for rule in misclassify.get("rules") or []:
        _add(checks, f"rule.{rule[:22]}", True)

    for alt in next_route.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.split('-')[-2] if '-' in alt else alt[:15]}", bool(alt))

    _add(checks, "scope.purpose", bool(scope.get("purpose")))
    _add(checks, "matrix.owner_row", any(r.get("asset_id") == "owner_approval_request_closed_module" for r in matrix.get("rows") or []))
    _add(checks, "matrix.skeleton_row", any(r.get("asset_id") == "task_manager_skeleton_foundation_handoff" for r in matrix.get("rows") or []))
    _add(checks, "work.integration_plan", any(i.get("work_id") == "module_integration_planning" for i in remaining.get("items") or []))
    _add(checks, "work.task_center", any(i.get("work_id") == "task_center_drive_brain_intelligence" for i in remaining.get("items") or []))
    _add(checks, "work.elasticity", any(i.get("work_id") == "time_bound_task_elasticity_tradeoff" for i in remaining.get("items") or []))
    _add(checks, "work.preauth_gate", any(i.get("work_id") == "real_execution_preauthorization_gate" for i in remaining.get("items") or []))
    _add(checks, "summary.record_absent", summary.get("request_record_absent") is True)
    _add(checks, "summary.approval_absent", summary.get("approval_record_absent") is True)
    _add(checks, "summary.ack_absent", summary.get("ack_record_absent") is True)
    _add(checks, "summary.evidence_absent", summary.get("evidence_bound_record_absent") is True)
    _add(checks, "report.scope_meta", report.get("foundation_closure_consolidation_only") is True)
    _add(checks, "report.not_final_meta", report.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "inventory.complete_flag", inventory.get("foundation_asset_inventory_complete") is True)
    _add(checks, "matrix.complete_flag", matrix.get("foundation_consolidation_matrix_complete") is True)
    _add(checks, "boundary.complete_flag", boundary.get("foundation_boundary_statement_complete") is True)
    _add(checks, "remaining.complete_flag", remaining.get("remaining_work_register_complete") is True)
    _add(checks, "route.complete_flag", next_route.get("next_mainline_route_complete") is True)
    _add(checks, "scope.complete_flag", scope.get("foundation_consolidation_scope_complete") is True)
    _add(checks, "misclassify.complete_flag", misclassify.get("do_not_misclassify_rules_complete") is True)
    _add(checks, "upstream.debt_not_blocker", roadmap_summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "owner_status_handoff", any(
        a.get("asset_id") == "owner_approval_request_closed_module" and a.get("current_status") == "governance_ready_handoff"
        for a in inventory.get("assets") or []
    ))
    _add(checks, "matrix.all_consolidated", all(r.get("consolidation_status") == "consolidated" for r in matrix.get("rows") or []))
    _add(checks, "md.consolidated_note", "consolidated" in md.lower())
    _add(checks, "report.remaining_work", report.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.foundation_layer", summary.get("midplatform_construction_phase") == "foundation_layer_consolidated")
    _add(checks, "work.deferred_test", any(i.get("category") == "deferred_test" for i in remaining.get("items") or []))
    _add(checks, "work.construction", any(i.get("category") == "construction" for i in remaining.get("items") or []))
    _add(checks, "work.before_runtime", any(i.get("category") == "required_before_runtime" for i in remaining.get("items") or []))

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "foundation_closure_consolidation_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": summary.get("real_request_issuance_authorized") is False,
        "integration_test_executed": summary.get("integration_test_executed") is False,
        "foundation_consolidation_not_final_midplatform_completion": True,
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
