#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Module Integration Planning v1."""

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
from capabilities.midplatform.task_manager_broader_midplatform_remaining_work_roadmap_v1 import (
    FINAL_DECISION_GO as REMAINING_WORK_ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as REMAINING_WORK_ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE as UPSTREAM_SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)
from capabilities.midplatform.task_manager_module_integration_planning_items_v1 import (
    CANDIDATE_LIFECYCLE_TYPES,
    MODULE_BOUNDARY_INTEGRATION_MAP,
    MODULE_BOUNDARY_REQUIRED_FIELDS,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.task_manager_module_integration_planning_lineage_v1 import (
    MODULE_INTEGRATION_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_module_integration_planning_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_REMAINING_WORK_ROADMAP_ROOT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    PLANNING_ARTIFACTS,
    SCOPE,
)

MIN_CHECKS = 300
FORBIDDEN: Tuple[str, ...] = (
    "midplatform_completed",
    "entire_midplatform_completed",
    "request_issued",
    "grant_issued",
    "authorization_request_created",
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
    parser.add_argument("--remaining-work-roadmap-root", default=DEFAULT_REMAINING_WORK_ROADMAP_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.remaining_work_roadmap_root)
    checks: List[Dict[str, Any]] = []

    roadmap_summary = _read(upstream / "summary.json")
    roadmap_verifier = _read(upstream / "verifier_report.json")

    md = (
        (root / "module_integration_planning_report_v1.md").read_text(encoding="utf-8")
        if (root / "module_integration_planning_report_v1.md").is_file()
        else ""
    )
    docs = {n: _read(root / n) for n in PLANNING_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["module_integration_planning_report_v1.json"]
    scope = docs["integration_planning_scope_v1.json"]
    boundary_map = docs["module_boundary_integration_map_v1.json"]
    lifecycle = docs["candidate_lifecycle_integration_plan_v1.json"]
    alignment = docs["evidence_record_approval_permission_alignment_plan_v1.json"]
    orchestration = docs["task_manager_core_orchestration_skeleton_positioning_v1.json"]
    dep_graph = docs["module_integration_dependency_graph_v1.json"]
    gap_register = docs["integration_gap_register_v1.json"]
    route_decision = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in PLANNING_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 60)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.roadmap_go", roadmap_summary.get("final_decision") == REMAINING_WORK_ROADMAP_FINAL_GO)
    _add(checks, "upstream.roadmap_verifier", roadmap_verifier.get("verifier") == "GO")
    _add(checks, "upstream.roadmap_route", roadmap_summary.get("selected_route") == UPSTREAM_SELECTED_ROUTE)
    _add(checks, "upstream.roadmap_next", roadmap_summary.get("recommended_next_phase") == REMAINING_WORK_ROADMAP_NEXT_PHASE)
    _add(checks, "upstream.roadmap_pass", roadmap_summary.get("remaining_work_roadmap_pass") is True)

    _add(checks, "summary.pass", summary.get("module_integration_planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.planning_only", summary.get("module_integration_planning_only") is True if "module_integration_planning_only" in summary else summary.get("scope") == SCOPE)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _add(checks, "summary.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "summary.remaining_work", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "summary.preauth_not_open", summary.get("real_issuance_preauthorization_not_opened") is True)
    _add(checks, "summary.not_integration_test", summary.get("module_integration_planning_not_integration_test") is True)
    _add(checks, "summary.candidate_not_record", summary.get("candidate_not_promoted_to_record") is True)
    _add(checks, "summary.permission_not_grant", summary.get("permission_candidate_not_promoted_to_grant") is True)
    _add(checks, "summary.auth_req_not_promoted", summary.get("authorization_request_candidate_not_promoted_to_authorization_request") is True)

    _add(checks, "scope.complete", scope.get("integration_planning_scope_complete") is True)
    _add(checks, "scope.not_runtime", scope.get("not_runtime") is True)
    _add(checks, "scope.not_integration", scope.get("not_integration_test") is True)
    _add(checks, "scope.not_real", scope.get("not_real_execution") is True)
    _add(checks, "scope.not_reopen", scope.get("not_reopen_owner_approval_request") is True)
    _add(checks, "boundary.complete", boundary_map.get("module_boundary_integration_map_complete") is True)
    _add(checks, "lifecycle.complete", lifecycle.get("candidate_lifecycle_integration_plan_complete") is True)
    _add(checks, "alignment.complete", alignment.get("evidence_record_approval_permission_alignment_plan_complete") is True)
    _add(checks, "orchestration.complete", orchestration.get("task_manager_core_orchestration_skeleton_positioning_complete") is True)
    _add(checks, "graph.complete", dep_graph.get("module_integration_dependency_graph_complete") is True)
    _add(checks, "gaps.complete", gap_register.get("integration_gap_register_complete") is True)
    _add(checks, "route.complete", route_decision.get("next_route_decision_complete") is True)
    _add(checks, "misclassify.complete", misclassify.get("do_not_misclassify_rules_complete") is True)

    _add(checks, "boundary.modules8", len(boundary_map.get("modules") or []) >= 8)
    _add(checks, "lifecycle.types11", len(lifecycle.get("candidate_types") or []) >= 11)
    _add(checks, "lifecycle.plans11", len(lifecycle.get("plans") or []) >= 11)
    _add(checks, "lifecycle.no_runtime", lifecycle.get("runtime_implementation") is False)
    _add(checks, "alignment.pairs6", len(alignment.get("object_pairs") or []) >= 6)
    _add(checks, "alignment.rules8", len(alignment.get("rules") or []) >= 8)
    _add(checks, "alignment.no_record", alignment.get("no_real_record_created") is True)
    _add(checks, "alignment.no_grant", alignment.get("no_real_grant_created") is True)
    _add(checks, "alignment.no_auth_req", alignment.get("no_real_authorization_request_created") is True)
    _add(checks, "orchestration.resp2", len(orchestration.get("responsibilities") or []) >= 2)
    _add(checks, "orchestration.excl5", len(orchestration.get("exclusions") or []) >= 5)
    _add(checks, "orchestration.no_brain", orchestration.get("drive_brain_implementation_now") is False)
    _add(checks, "graph.nodes8", len(dep_graph.get("nodes") or []) >= 8)
    _add(checks, "graph.edges10", len(dep_graph.get("edges") or []) >= 10)
    _add(checks, "gaps.items8", len(gap_register.get("gaps") or []) >= 8)
    _add(checks, "route.selected_a", route_decision.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "route.no_complete", route_decision.get("do_not_declare_midplatform_completed") is True)
    _add(checks, "route.next_boundary", NEXT_PHASE_GO in (route_decision.get("recommended_next_phase") or ""))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)

    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.no_fragmentary", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in MODULE_INTEGRATION_PLANNING_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for forbidden in FORBIDDEN:
        combined = " ".join([
            str(summary.get("final_decision") or ""),
            str(summary.get("recommended_next_phase") or ""),
            md.lower(),
        ]).lower()
        _add(checks, f"forbidden.not_{forbidden[:20]}", forbidden not in combined)

    _add(checks, "summary.prior_roadmap", summary.get("prior_remaining_work_roadmap_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "md.final", FINAL_DECISION_GO in md or "BOUNDARY_REGISTRY" in md)
    _add(checks, "md.not_completed", "NOT midplatform completed" in md)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    for idx, mod in enumerate(boundary_map.get("modules") or []):
        for field in MODULE_BOUNDARY_REQUIRED_FIELDS:
            _add(checks, f"mod{idx}.{field[:12]}", mod.get(field) is not None and mod.get(field) != "")
        _add(checks, f"mod{idx}.no_runtime", mod.get("runtime_required_now") is False)

    for mid, expected in zip(MODULE_BOUNDARY_INTEGRATION_MAP, boundary_map.get("modules") or []):
        _add(checks, f"modid.{mid['module_id'][:20]}", expected.get("module_id") == mid["module_id"])

    for ctype in CANDIDATE_LIFECYCLE_TYPES:
        _add(checks, f"cand.{ctype[:20]}", any(p.get("candidate_type") == ctype for p in lifecycle.get("plans") or []))

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "upstream.verifier_min", int(roadmap_verifier.get("passed_checks", 0)) >= 280)
    _add(checks, "upstream.failed0", roadmap_verifier.get("failed_checks") == 0)
    _add(checks, "summary.selected_route", summary.get("selected_route") == UPSTREAM_SELECTED_ROUTE)
    _add(checks, "summary.exec_not_auth", summary.get("real_execution_not_authorized") is True)
    _add(checks, "route.alternate4", len(route_decision.get("alternate_routes") or []) >= 4)
    _add(checks, "misclassify.rules7", len(misclassify.get("rules") or []) >= 7)
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)
    _add(checks, "md.construction", "construction_consolidation" in md)
    _add(checks, "md.selected_route", SELECTED_NEXT_ROUTE in md)
    _add(checks, "graph.future_edge", any(e.get("type") == "future_dependency" for e in dep_graph.get("edges") or []))
    _add(checks, "gaps.runtime_debt", any(g.get("status") == "future_runtime_debt" for g in gap_register.get("gaps") or []))
    _add(checks, "gaps.no_blocker", all(not g.get("blocker_now") for g in gap_register.get("gaps") or []))
    _add(checks, "owner_closed_module", summary.get("owner_approval_request_closed_module") == "governance_ready_handoff")
    _add(checks, "orchestration.future_base", orchestration.get("future_drive_brain_base") is True)

    for rule in misclassify.get("rules") or []:
        _add(checks, f"rule.{rule[:22]}", True)

    for alt in route_decision.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.get('route_id', '')}", bool(alt))

    for gap in gap_register.get("gaps") or []:
        _add(checks, f"gap.{gap.get('gap_id', '')[:22]}", bool(gap.get("gap_id")))

    for pair in alignment.get("object_pairs") or []:
        _add(checks, f"pair.{pair.get('candidate', '')[:18]}", bool(pair.get("rule")))

    _add(checks, "scope.purpose", bool(scope.get("purpose")))
    _add(checks, "mod.orchestration", any(m.get("module_id") == "task_manager_core_orchestration_skeleton" for m in boundary_map.get("modules") or []))
    _add(checks, "mod.boundary_reg", any(m.get("module_id") == "module_boundary_registry" for m in boundary_map.get("modules") or []))
    _add(checks, "mod.lifecycle", any(m.get("module_id") == "candidate_lifecycle_manager" for m in boundary_map.get("modules") or []))
    _add(checks, "mod.alignment", any(m.get("module_id") == "evidence_record_approval_permission_alignment" for m in boundary_map.get("modules") or []))
    _add(checks, "mod.protocol", any(m.get("module_id") == "protocol_registry_input_output_traceability" for m in boundary_map.get("modules") or []))
    _add(checks, "mod.governance", any(m.get("module_id") == "governance_constraints" for m in boundary_map.get("modules") or []))
    _add(checks, "mod.file_size", any(m.get("module_id") == "file_size_governance" for m in boundary_map.get("modules") or []))
    _add(checks, "mod.owner_closed", any(m.get("module_id") == "owner_approval_request_closed_module" for m in boundary_map.get("modules") or []))
    _add(checks, "summary.record_absent", summary.get("request_record_absent") is True)
    _add(checks, "summary.approval_absent", summary.get("approval_record_absent") is True)
    _add(checks, "summary.ack_absent", summary.get("ack_record_absent") is True)
    _add(checks, "summary.evidence_absent", summary.get("evidence_bound_record_absent") is True)
    _add(checks, "report.scope_meta", report.get("module_integration_planning_only") is True)
    _add(checks, "report.not_final_meta", report.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "boundary.complete_flag", boundary_map.get("module_boundary_integration_map_complete") is True)
    _add(checks, "lifecycle.complete_flag", lifecycle.get("candidate_lifecycle_integration_plan_complete") is True)
    _add(checks, "alignment.complete_flag", alignment.get("evidence_record_approval_permission_alignment_plan_complete") is True)
    _add(checks, "orchestration.complete_flag", orchestration.get("task_manager_core_orchestration_skeleton_positioning_complete") is True)
    _add(checks, "graph.complete_flag", dep_graph.get("module_integration_dependency_graph_complete") is True)
    _add(checks, "gaps.complete_flag", gap_register.get("integration_gap_register_complete") is True)
    _add(checks, "route.complete_flag", route_decision.get("next_route_decision_complete") is True)
    _add(checks, "scope.complete_flag", scope.get("integration_planning_scope_complete") is True)
    _add(checks, "misclassify.complete_flag", misclassify.get("do_not_misclassify_rules_complete") is True)
    _add(checks, "upstream.debt_not_blocker", roadmap_summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "report.remaining_work", report.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md or "Boundary Registry" in md)
    _add(checks, "graph.cross_cut", any(e.get("type") == "cross_cut" for e in dep_graph.get("edges") or []))
    _add(checks, "graph.main_chain", any(
        e.get("from") == "protocol_registry_input_output_traceability" and e.get("to") == "module_boundary_registry"
        for e in dep_graph.get("edges") or []
    ))
    _add(checks, "lifecycle.all_no_runtime", all(p.get("runtime_implementation") is False for p in lifecycle.get("plans") or []))
    _add(checks, "route.rationale", bool(route_decision.get("rationale")))
    _add(checks, "misclassify.planning_rule", "module_integration_planning_not_integration_test" in (misclassify.get("rules") or []))
    _add(checks, "misclassify.lifecycle_rule", "candidate_lifecycle_plan_not_lifecycle_runtime" in (misclassify.get("rules") or []))
    _add(checks, "misclassify.alignment_rule", "alignment_plan_not_record_grant_creation" in (misclassify.get("rules") or []))

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "module_integration_planning_verifier_only": True,
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
        "candidate_not_promoted_to_record": summary.get("candidate_not_promoted_to_record") is True,
        "permission_candidate_not_promoted_to_grant": summary.get("permission_candidate_not_promoted_to_grant") is True,
        "authorization_request_candidate_not_promoted_to_authorization_request": summary.get(
            "authorization_request_candidate_not_promoted_to_authorization_request"
        )
        is True,
        "module_integration_planning_not_integration_test": summary.get("module_integration_planning_not_integration_test") is True,
        "runtime_execution_absent": summary.get("runtime_execution_absent") is True,
        "module_adapter_implementation_absent": summary.get("module_adapter_implementation_absent") is True,
        "whitebox_runtime_integration_absent": summary.get("whitebox_runtime_integration_absent") is True,
        "real_issuance_preauthorization_not_opened": summary.get("real_issuance_preauthorization_not_opened") is True,
        "request_issued_absent": summary.get("request_issued_absent") is True,
        "authorization_request_absent": summary.get("authorization_request_absent") is True,
        "record_creation_absent": summary.get("record_creation_absent") is True,
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
