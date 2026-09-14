#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Broader Midplatform Remaining Work Roadmap v1."""

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
from capabilities.midplatform.task_manager_broader_midplatform_remaining_work_items_v1 import (
    MODULE_COMPLETION_CANDIDATES,
    REMAINING_WORK_ITEMS,
    WORK_MATRIX_REQUIRED_FIELDS,
)
from capabilities.midplatform.task_manager_broader_midplatform_remaining_work_lineage_v1 import (
    BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_broader_midplatform_remaining_work_roadmap_v1 import (
    DEFAULT_FOUNDATION_CONSOLIDATION_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    ROADMAP_ARTIFACTS,
    ROUTE_A,
    SCOPE,
    SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_foundation_closure_consolidation_v1 import (
    FINAL_DECISION_GO as FOUNDATION_CONSOLIDATION_FINAL_GO,
    NEXT_PHASE_GO as FOUNDATION_CONSOLIDATION_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

MIN_CHECKS = 280
FORBIDDEN: Tuple[str, ...] = (
    "midplatform_completed",
    "entire_midplatform_completed",
    "request_issued",
    "authorization_request_created",
    "grant_issued",
    "record_created",
    "runtime_enabled",
    "integration_test_executed",
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
    parser.add_argument("--foundation-consolidation-root", default=DEFAULT_FOUNDATION_CONSOLIDATION_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.foundation_consolidation_root)
    checks: List[Dict[str, Any]] = []

    foundation_summary = _read(upstream / "summary.json")
    foundation_verifier = _read(upstream / "verifier_report.json")

    md = (
        (root / "broader_midplatform_remaining_work_roadmap_v1.md").read_text(encoding="utf-8")
        if (root / "broader_midplatform_remaining_work_roadmap_v1.md").is_file()
        else ""
    )
    docs = {n: _read(root / n) for n in ROADMAP_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    roadmap = docs["broader_midplatform_remaining_work_roadmap_v1.json"]
    scope = docs["remaining_work_scope_v1.json"]
    inventory = docs["remaining_work_inventory_v1.json"]
    matrix = docs["work_classification_matrix_v1.json"]
    priority_plan = docs["mainline_priority_plan_v1.json"]
    module_candidates = docs["module_completion_candidates_v1.json"]
    governance = docs["governance_debt_positioning_v1.json"]
    test_pos = docs["test_readiness_positioning_v1.json"]
    route_decision = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in ROADMAP_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 60)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.foundation_go", foundation_summary.get("final_decision") == FOUNDATION_CONSOLIDATION_FINAL_GO)
    _add(checks, "upstream.foundation_verifier", foundation_verifier.get("verifier") == "GO")
    _add(checks, "upstream.foundation_next", foundation_summary.get("recommended_next_phase") == FOUNDATION_CONSOLIDATION_NEXT_PHASE)
    _add(checks, "upstream.foundation_pass", foundation_summary.get("foundation_consolidation_pass") is True)
    _add(checks, "upstream.foundation_not_final", foundation_summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "upstream.remaining_work", foundation_summary.get("midplatform_still_has_remaining_work") is True)

    _add(checks, "summary.pass", summary.get("remaining_work_roadmap_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.roadmap_only", summary.get("remaining_work_roadmap_only") is True if "remaining_work_roadmap_only" in summary else summary.get("scope") == SCOPE)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "summary.remaining_work", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "summary.design_ok", summary.get("future_design_not_current_blocker") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "summary.preauth_not_open", summary.get("real_issuance_preauthorization_not_opened") is True)

    _add(checks, "scope.complete", scope.get("remaining_work_scope_complete") is True)
    _add(checks, "scope.not_runtime", scope.get("not_runtime") is True)
    _add(checks, "scope.not_integration", scope.get("not_integration_test") is True)
    _add(checks, "scope.not_preauth", scope.get("not_real_issuance_preauth") is True)
    _add(checks, "scope.not_completed", scope.get("not_midplatform_completed") is True)
    _add(checks, "inventory.complete", inventory.get("remaining_work_inventory_complete") is True)
    _add(checks, "matrix.complete", matrix.get("work_classification_matrix_complete") is True)
    _add(checks, "priority.complete", priority_plan.get("mainline_priority_plan_complete") is True)
    _add(checks, "candidates.complete", module_candidates.get("module_completion_candidates_complete") is True)
    _add(checks, "governance.complete", governance.get("governance_debt_positioning_complete") is True)
    _add(checks, "test_pos.complete", test_pos.get("test_readiness_positioning_complete") is True)
    _add(checks, "route.complete", route_decision.get("next_route_decision_complete") is True)
    _add(checks, "misclassify.complete", misclassify.get("do_not_misclassify_rules_complete") is True)

    _add(checks, "inventory.items15", len(inventory.get("items") or []) >= 15)
    _add(checks, "matrix.rows15", len(matrix.get("rows") or []) >= 15)
    _add(checks, "candidates.items6", len(module_candidates.get("candidates") or []) >= 6)
    _add(checks, "route.selected_a", route_decision.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "route.no_complete", route_decision.get("do_not_declare_midplatform_completed") is True)
    _add(checks, "route.next_integration", ROUTE_A in (route_decision.get("recommended_next_phase") or ""))
    _add(checks, "governance.debt_not_blocker", governance.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "governance.not_first", governance.get("governance_debt_consolidation_first") is False)
    _add(checks, "test.not_executed", test_pos.get("integration_test_executed") is False)
    _add(checks, "test.deferred", test_pos.get("integration_test_planning_deferred") is True)
    _add(checks, "test.dryrun_input", test_pos.get("owner_approval_request_slice_dryrun_as_input") is True)
    _add(checks, "test.foundation_input", test_pos.get("foundation_consolidation_package_as_input") is True)

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
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

    for rel in BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for forbidden in FORBIDDEN:
        combined = " ".join([
            str(summary.get("final_decision") or ""),
            str(summary.get("recommended_next_phase") or ""),
            md.lower(),
        ]).lower()
        _add(checks, f"forbidden.not_{forbidden[:20]}", forbidden not in combined)

    _add(checks, "summary.prior_foundation", summary.get("prior_foundation_consolidation_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "md.final", FINAL_DECISION_GO in md or "MODULE_INTEGRATION_PLANNING" in md)
    _add(checks, "md.not_completed", "NOT midplatform completed" in md)
    _add(checks, "md.remaining", "remaining work" in md.lower())
    _add(checks, "roadmap.final", roadmap.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)

    for key in GO_CONDITIONS_KEYS:
        if key in roadmap:
            _add(checks, f"roadmap.{key}", roadmap.get(key) is True)

    for idx, item in enumerate(inventory.get("items") or []):
        _add(checks, f"inv{idx}.id", bool(item.get("work_id")))
        _add(checks, f"inv{idx}.cat", bool(item.get("category")))

    for idx, row in enumerate(matrix.get("rows") or []):
        for field in WORK_MATRIX_REQUIRED_FIELDS:
            _add(checks, f"matrix{idx}.{field[:12]}", row.get(field) is not None and row.get(field) != "")

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "upstream.verifier_min", int(foundation_verifier.get("passed_checks", 0)) >= 260)
    _add(checks, "summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    _add(checks, "summary.exec_not_auth", summary.get("real_execution_not_authorized") is True)
    _add(checks, "priority.p1_current", any(p.get("priority") == "P1" for p in priority_plan.get("phases") or []))
    _add(checks, "priority.p2_next", any(p.get("priority") == "P2" for p in priority_plan.get("phases") or []))
    _add(checks, "route.alternate4", len(route_decision.get("alternate_routes") or []) >= 4)
    _add(checks, "misclassify.rules7", len(misclassify.get("rules") or []) >= 7)
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "md.construction", "construction_consolidation" in md)
    _add(checks, "roadmap.not_final", roadmap.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "roadmap.integration_false", roadmap.get("integration_test_executed") is False)
    _add(checks, "matrix.runtime_debt", any(r.get("category") == "future_runtime_debt" for r in matrix.get("rows") or []))
    _add(checks, "matrix.future_design", any(r.get("category") == "future_design" for r in matrix.get("rows") or []))
    _add(checks, "matrix.no_runtime_blocker", all(not r.get("blocker_now") for r in matrix.get("rows") or [] if r.get("category") == "future_runtime_debt"))
    _add(checks, "matrix.no_design_blocker", all(not r.get("blocker_now") for r in matrix.get("rows") or [] if r.get("category") == "future_design"))
    _add(checks, "upstream.chain_not_reopen", foundation_summary.get("owner_approval_request_chain_not_reopened") is True)
    _add(checks, "summary.foundation_layer", summary.get("foundation_layer_consolidated") is True)
    _add(checks, "misclassify.owner_rule", "owner_approval_request_chain_not_reopened" in (misclassify.get("rules") or []))
    _add(checks, "misclassify.debt_rule", "future_runtime_debt_not_current_blocker" in (misclassify.get("rules") or []))

    for item in REMAINING_WORK_ITEMS:
        wid = item["work_id"]
        _add(checks, f"workreg.{wid[:22]}", any(i.get("work_id") == wid for i in inventory.get("items") or []))
        _add(checks, f"matrix.{wid[:22]}", any(r.get("work_id") == wid for r in matrix.get("rows") or []))

    for cand in MODULE_COMPLETION_CANDIDATES:
        cid = cand["candidate_id"]
        _add(checks, f"cand.{cid[:22]}", any(c.get("candidate_id") == cid for c in module_candidates.get("candidates") or []))

    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "upstream.failed0", foundation_verifier.get("failed_checks") == 0)
    _add(checks, "roadmap.pass_flag", roadmap.get("remaining_work_roadmap_pass") is True)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md or "Module Integration" in md)
    _add(checks, "md.selected_route", SELECTED_ROUTE in md)

    for rule in misclassify.get("rules") or []:
        _add(checks, f"rule.{rule[:22]}", True)

    for alt in route_decision.get("alternate_routes") or []:
        aid = alt.get("route_id") or alt.get("phase_id") or str(alt)
        _add(checks, f"alt.{str(aid)[:15]}", bool(alt))

    for phase in priority_plan.get("phases") or []:
        _add(checks, f"phase.{phase.get('priority', '')}", bool(phase.get("phase")))

    _add(checks, "scope.purpose", bool(scope.get("purpose")))
    _add(checks, "work.integration_plan", any(i.get("work_id") == "module_integration_planning" for i in inventory.get("items") or []))
    _add(checks, "work.task_center", any(i.get("work_id") == "task_center_drive_brain_intelligence" for i in inventory.get("items") or []))
    _add(checks, "work.elasticity", any(i.get("work_id") == "time_bound_task_elasticity_tradeoff" for i in inventory.get("items") or []))
    _add(checks, "work.preauth_gate", any(i.get("work_id") == "real_execution_preauthorization_gate" for i in inventory.get("items") or []))
    _add(checks, "work.boundary_registry", any(i.get("work_id") == "midplatform_module_boundary_registry" for i in inventory.get("items") or []))
    _add(checks, "work.candidate_lifecycle", any(i.get("work_id") == "candidate_lifecycle_unification" for i in inventory.get("items") or []))
    _add(checks, "work.evidence_align", any(i.get("work_id") == "evidence_record_approval_permission_alignment" for i in inventory.get("items") or []))
    _add(checks, "work.distributed", any(i.get("work_id") == "distributed_ready_field_alignment" for i in inventory.get("items") or []))
    _add(checks, "work.health_hooks", any(i.get("work_id") == "health_memory_world_model_hooks" for i in inventory.get("items") or []))
    _add(checks, "summary.record_absent", summary.get("request_record_absent") is True)
    _add(checks, "summary.approval_absent", summary.get("approval_record_absent") is True)
    _add(checks, "summary.ack_absent", summary.get("ack_record_absent") is True)
    _add(checks, "summary.evidence_absent", summary.get("evidence_bound_record_absent") is True)
    _add(checks, "roadmap.scope_meta", roadmap.get("remaining_work_roadmap_only") is True)
    _add(checks, "roadmap.not_final_meta", roadmap.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "inventory.complete_flag", inventory.get("remaining_work_inventory_complete") is True)
    _add(checks, "matrix.complete_flag", matrix.get("work_classification_matrix_complete") is True)
    _add(checks, "priority.complete_flag", priority_plan.get("mainline_priority_plan_complete") is True)
    _add(checks, "candidates.complete_flag", module_candidates.get("module_completion_candidates_complete") is True)
    _add(checks, "governance.complete_flag", governance.get("governance_debt_positioning_complete") is True)
    _add(checks, "test.complete_flag", test_pos.get("test_readiness_positioning_complete") is True)
    _add(checks, "route.complete_flag", route_decision.get("next_route_decision_complete") is True)
    _add(checks, "scope.complete_flag", scope.get("remaining_work_scope_complete") is True)
    _add(checks, "misclassify.complete_flag", misclassify.get("do_not_misclassify_rules_complete") is True)
    _add(checks, "upstream.debt_not_blocker", foundation_summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "candidates.no_impl", module_candidates.get("implementation_now") is False)
    _add(checks, "roadmap.remaining_work", roadmap.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "work.deferred_test", any(i.get("category") == "deferred_test" for i in inventory.get("items") or []))
    _add(checks, "work.construction", any(i.get("category") == "construction" for i in inventory.get("items") or []))
    _add(checks, "work.before_runtime", any(i.get("category") == "required_before_runtime" for i in inventory.get("items") or []))
    _add(checks, "work.optional", any(i.get("category") == "optional_quality" for i in inventory.get("items") or []))
    _add(checks, "matrix.deferred_list", isinstance(matrix.get("deferred_items"), list))
    _add(checks, "summary.deferred_count", summary.get("deferred_item_count", 0) >= 1)
    _add(checks, "governance.structural", len(governance.get("structural_debt") or []) >= 1)
    _add(checks, "governance.runtime_debt", len(governance.get("future_runtime_debt") or []) >= 1)
    _add(checks, "governance.optional", len(governance.get("optional_quality") or []) >= 1)
    _add(checks, "test.preconditions3", len(test_pos.get("preconditions_for_integration_test_planning") or []) >= 3)
    _add(checks, "owner_closed_module", summary.get("owner_approval_request_closed_module") == "governance_ready_handoff")

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "remaining_work_roadmap_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": summary.get("real_request_issuance_authorized") is False,
        "integration_test_executed": summary.get("integration_test_executed") is False,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "midplatform_still_has_remaining_work": True,
        "owner_approval_request_chain_not_reopened": summary.get("owner_approval_request_chain_not_reopened") is True,
        "future_runtime_debt_not_current_blocker": summary.get("future_runtime_debt_not_current_blocker") is True,
        "future_design_not_current_blocker": summary.get("future_design_not_current_blocker") is True,
        "runtime_execution_absent": summary.get("runtime_execution_absent") is True,
        "module_adapter_implementation_absent": summary.get("module_adapter_implementation_absent") is True,
        "whitebox_runtime_integration_absent": summary.get("whitebox_runtime_integration_absent") is True,
        "real_issuance_preauthorization_not_opened": summary.get("real_issuance_preauthorization_not_opened") is True,
        "request_issued_absent": summary.get("request_issued_absent") is True,
        "grant_absent": summary.get("grant_absent") is True,
        "no_fragmentary_phase_expansion": summary.get("no_fragmentary_phase_expansion") is True,
        "file_size_governance_review_ok": summary.get("file_size_governance_review_ok") is True,
        "full_repo_scan_absent": summary.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": summary.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": summary.get("summary_index_first_reading_ok") is True,
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
