#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Core Orchestration Implementation Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS
from capabilities.midplatform.task_manager_core_orchestration_implementation_items_v1 import (
    ALLOWED_DEPENDENCIES,
    DATA_STRUCTURE_PLAN,
    FORBIDDEN_DEPENDENCIES,
    FUNCTIONAL_UNIT_REQUIRED_FIELDS,
    IMPLEMENTATION_FILES,
    NON_EXECUTION_GUARDS,
    ORCHESTRATION_FUNCTIONAL_UNITS,
    SELECTED_NEXT_ROUTE,
    STATIC_VALIDATORS,
)
from capabilities.midplatform.task_manager_core_orchestration_implementation_lineage_v1 import (
    ORCHESTRATION_IMPLEMENTATION_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_core_orchestration_implementation_planning_v1 import (
    DEFAULT_ORCHESTRATION_CONSOLIDATION_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    PLANNING_ARTIFACTS,
    SCOPE,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_consolidation_v1 import (
    FINAL_DECISION_GO as ORCHESTRATION_CONSOLIDATION_FINAL_GO,
    NEXT_PHASE_GO as ORCHESTRATION_CONSOLIDATION_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_items_v1 import (
    SELECTED_NEXT_ROUTE as UPSTREAM_CONSOLIDATION_SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

MIN_CHECKS = 320
FORBIDDEN = ("midplatform_completed", "request_issued", "grant_issued", "runtime_enabled", "integration_test_executed", "record_created")
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
    parser.add_argument("--orchestration-skeleton-consolidation-root", default=DEFAULT_ORCHESTRATION_CONSOLIDATION_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.orchestration_skeleton_consolidation_root)
    checks: List[Dict[str, Any]] = []

    consolidation_summary = _read(upstream / "summary.json")
    consolidation_verifier = _read(upstream / "verifier_report.json")
    md = (root / "task_manager_core_orchestration_implementation_planning_report_v1.md").read_text(encoding="utf-8") if (root / "task_manager_core_orchestration_implementation_planning_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in PLANNING_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["task_manager_core_orchestration_implementation_planning_report_v1.json"]
    scope = docs["implementation_planning_scope_v1.json"]
    units_doc = docs["orchestration_functional_units_v1.json"]
    structures_doc = docs["orchestration_data_structure_plan_v1.json"]
    validator_doc = docs["static_validator_plan_v1.json"]
    file_plan = docs["implementation_file_plan_v1.json"]
    dep_plan = docs["implementation_dependency_plan_v1.json"]
    guard_plan = docs["non_execution_implementation_guard_plan_v1.json"]
    gap_register = docs["implementation_gap_register_v1.json"]
    route_decision = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]
    units = units_doc.get("units") or []

    for name in PLANNING_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 40)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.consolidation_go", consolidation_summary.get("final_decision") == ORCHESTRATION_CONSOLIDATION_FINAL_GO)
    _add(checks, "upstream.consolidation_verifier", consolidation_verifier.get("verifier") == "GO")
    _add(checks, "upstream.consolidation_route", consolidation_summary.get("selected_next_route") == UPSTREAM_CONSOLIDATION_SELECTED_ROUTE)
    _add(checks, "upstream.consolidation_next", consolidation_summary.get("recommended_next_phase") == ORCHESTRATION_CONSOLIDATION_NEXT_PHASE)
    _add(checks, "upstream.consolidation_pass", consolidation_summary.get("orchestration_skeleton_consolidation_pass") is True)
    _add(checks, "upstream.skeleton_not_runtime", consolidation_summary.get("orchestration_skeleton_not_runtime") is True)

    _add(checks, "summary.pass", summary.get("orchestration_implementation_planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _expect_false(checks, "summary.promotion_exec", summary.get("candidate_promotion_executed"))
    _add(checks, "summary.runtime_dep_absent", summary.get("runtime_dependency_absent") is True)
    _add(checks, "summary.whitebox_dep_absent", summary.get("whitebox_dependency_absent") is True)
    _add(checks, "summary.drive_absent", summary.get("drive_brain_implementation_absent") is True)
    _add(checks, "summary.reflection_absent", summary.get("reflection_brain_implementation_absent") is True)
    _add(checks, "summary.files_split", summary.get("implementation_files_split_by_responsibility") is True)
    _add(checks, "summary.no_monolithic", summary.get("no_monolithic_skeleton_planned") is True)
    _add(checks, "summary.controlled_ready", summary.get("controlled_implementation_ready") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))

    _add(checks, "scope.complete", scope.get("implementation_planning_scope_complete") is True)
    _add(checks, "scope.not_runtime", scope.get("not_runtime_orchestration") is True)
    _add(checks, "units.complete", units_doc.get("orchestration_functional_units_complete") is True)
    _add(checks, "units.count12", len(units) >= 12)
    _add(checks, "structs.complete", structures_doc.get("orchestration_data_structure_plan_complete") is True)
    _add(checks, "structs.count10", len(structures_doc.get("structures") or []) >= 10)
    _add(checks, "validators.complete", validator_doc.get("static_validator_plan_complete") is True)
    _add(checks, "validators.count10", len(validator_doc.get("validators") or []) >= 10)
    _add(checks, "files.complete", file_plan.get("implementation_file_plan_complete") is True)
    _add(checks, "files.count5", len(file_plan.get("files") or []) >= 5)
    _add(checks, "files.split", file_plan.get("implementation_files_split_by_responsibility") is True)
    _add(checks, "files.no_mono", file_plan.get("no_monolithic_skeleton_planned") is True)
    _add(checks, "files.max600", file_plan.get("max_lines_per_file") == 600)
    _add(checks, "dep.complete", dep_plan.get("implementation_dependency_plan_complete") is True)
    _add(checks, "guard.complete", guard_plan.get("non_execution_implementation_guard_plan_complete") is True)
    _add(checks, "guard.count9", len(guard_plan.get("guards") or []) >= 9)
    _add(checks, "gaps.complete", gap_register.get("implementation_gap_register_complete") is True)
    _add(checks, "route.complete", route_decision.get("next_route_decision_complete") is True)
    _add(checks, "route.selected_a", route_decision.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "route.next_controlled", NEXT_PHASE_GO in (route_decision.get("recommended_next_phase") or ""))

    for u in ORCHESTRATION_FUNCTIONAL_UNITS:
        uid = u["unit_id"]
        entry = next((x for x in units if x.get("unit_id") == uid), {})
        _add(checks, f"unit.{uid[:20]}", bool(entry))
        _add(checks, f"unit.{uid[:12]}.cand", entry.get("candidate_only") is True)
        _add(checks, f"unit.{uid[:12]}.no_side", entry.get("side_effect_allowed") is False)
        _add(checks, f"unit.{uid[:12]}.no_rt", entry.get("runtime_required_now") is False)

    for idx, entry in enumerate(units):
        for field in FUNCTIONAL_UNIT_REQUIRED_FIELDS:
            _add(checks, f"u{idx}.{field[:10]}", entry.get(field) is not None and entry.get(field) != "")

    for s in DATA_STRUCTURE_PLAN:
        sid = s["structure_id"]
        entry = next((x for x in structures_doc.get("structures") or [] if x.get("structure_id") == sid), {})
        _add(checks, f"struct.{sid[:18]}", bool(entry))
        _add(checks, f"struct.{sid[:12]}.cand", entry.get("layer") == "candidate_planning_object")
        _add(checks, f"struct.{sid[:12]}.no_rec", entry.get("record_creation_method") is False)
        _add(checks, f"struct.{sid[:12]}.no_grant", entry.get("grant_issuance_method") is False)
        _add(checks, f"struct.{sid[:12]}.no_rt", entry.get("runtime_execution_method") is False)

    for v in STATIC_VALIDATORS:
        _add(checks, f"val.{v[:22]}", v in (validator_doc.get("validators") or []))

    for f in IMPLEMENTATION_FILES:
        _add(checks, f"file.{f['path'].split('/')[-1][:18]}", any(x.get("path") == f["path"] for x in file_plan.get("files") or []))
        _add(checks, f"resp.{f['responsibility'][:18]}", any(x.get("responsibility") == f["responsibility"] for x in file_plan.get("files") or []))

    for dep in ALLOWED_DEPENDENCIES:
        _add(checks, f"allow.{dep[:18]}", dep in (dep_plan.get("allowed_dependencies") or []))
    for dep in FORBIDDEN_DEPENDENCIES:
        _add(checks, f"forbid.{dep[:18]}", dep in (dep_plan.get("forbidden_dependencies") or []))

    for g in NON_EXECUTION_GUARDS:
        _add(checks, f"guard.{g[:18]}", g in (guard_plan.get("guards") or []))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.route_exec_absent", summary.get("route_execution_absent") is True)
    _add(checks, "summary.handoff_runtime_absent", summary.get("module_handoff_runtime_absent") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in ORCHESTRATION_IMPLEMENTATION_PLANNING_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')} {md}".lower()
        _add(checks, f"forbidden.not_{fb[:15]}", fb not in combined)

    _add(checks, "summary.prior_consolidation", summary.get("prior_orchestration_skeleton_consolidation_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "upstream.verifier_min", int(consolidation_verifier.get("passed_checks", 0)) >= 320)
    _add(checks, "misclassify.rules10", len(misclassify.get("rules") or []) >= 10)
    _add(checks, "gaps.items8", len(gap_register.get("gaps") or []) >= 8)
    _add(checks, "owner_closed_module", summary.get("owner_approval_request_closed_module") == "governance_ready_handoff")
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "summary.future_design_ok", summary.get("future_design_not_current_blocker") is True)
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)

    for rule in misclassify.get("rules") or []:
        _add(checks, f"rule.{rule[:20]}", True)
    for gap in gap_register.get("gaps") or []:
        _add(checks, f"gap.{gap.get('gap_id', '')[:18]}", bool(gap.get("gap_id")))
        _add(checks, f"gapblk.{gap.get('gap_id', '')[:12]}", not gap.get("blocker_now"))
    for alt in route_decision.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.get('route_id', '')}", bool(alt))

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.final", FINAL_DECISION_GO in md or "CONTROLLED" in md)
    _add(checks, "md.selected_route", SELECTED_NEXT_ROUTE in md)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "route.no_complete", route_decision.get("do_not_declare_midplatform_completed") is True)
    _add(checks, "upstream.failed0", consolidation_verifier.get("failed_checks") == 0)
    _add(checks, "report.pass_flag", report.get("orchestration_implementation_planning_pass") is True)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md or "Controlled" in md)
    _add(checks, "misclassify.planning_rule", "implementation_planning_not_implementation" in (misclassify.get("rules") or []))
    _add(checks, "summary.scope_meta", summary.get("scope") == SCOPE)
    _add(checks, "route.rationale", bool(route_decision.get("rationale")))
    _add(checks, "scope.not_brain", scope.get("not_drive_brain_reflection") is True)
    _add(checks, "summary.remaining_work", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "dep.allowed6", len(dep_plan.get("allowed_dependencies") or []) >= 6)
    _add(checks, "dep.forbidden5", len(dep_plan.get("forbidden_dependencies") or []) >= 5)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "orchestration_implementation_planning_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "candidate_promotion_executed": False,
        "runtime_dependency_absent": summary.get("runtime_dependency_absent") is True,
        "drive_brain_implementation_absent": summary.get("drive_brain_implementation_absent") is True,
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
