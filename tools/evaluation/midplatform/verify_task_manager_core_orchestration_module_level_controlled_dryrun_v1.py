#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Core Orchestration Module-Level Controlled DryRun v1."""

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
from capabilities.midplatform.task_manager_core_orchestration_controlled_skeleton_implementation_v1 import (
    FINAL_DECISION_GO as SKELETON_FINAL_GO,
    NEXT_PHASE_GO as SKELETON_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_core_orchestration_module_level_controlled_dryrun_items_v1 import (
    DRYRUN_SCENARIOS,
    FLOW_STEPS,
    NON_EXECUTION_GUARDS,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.task_manager_core_orchestration_module_level_controlled_dryrun_lineage_v1 import (
    ORCHESTRATION_MODULE_DRYRUN_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_core_orchestration_module_level_controlled_dryrun_v1 import (
    DEFAULT_CONTROLLED_SKELETON_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

MIN_CHECKS = 360
FORBIDDEN = ("midplatform_completed", "request_issued", "grant_issued", "runtime_enabled", "integration_test_executed", "record_created")
FILE_SIZE_KEYS = (
    "file_size_governance_review_exists", "file_size_governance_review_ok", "monolithic_file_absent",
    "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok", "limited_directory_scan_ok",
)
ARTIFACTS: Tuple[str, ...] = (
    "module_level_controlled_dryrun_report_v1.json",
    "module_level_controlled_dryrun_report_v1.md",
    "controlled_dryrun_scope_v1.json",
    "controlled_dryrun_scenario_set_v1.json",
    "controlled_dryrun_scenario_results_v1.json",
    "module_level_flow_validation_v1.json",
    "candidate_output_validation_v1.json",
    "non_execution_guard_dryrun_v1.json",
    "error_blocker_defer_handling_validation_v1.json",
    "module_level_dryrun_result_summary_v1.json",
    "integration_readiness_positioning_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOC_PATHS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--controlled-skeleton-implementation-root", default=DEFAULT_CONTROLLED_SKELETON_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.controlled_skeleton_implementation_root)
    checks: List[Dict[str, Any]] = []

    skeleton_summary = _read(upstream / "summary.json")
    skeleton_verifier = _read(upstream / "verifier_report.json")
    md = (root / "module_level_controlled_dryrun_report_v1.md").read_text(encoding="utf-8") if (root / "module_level_controlled_dryrun_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["module_level_controlled_dryrun_report_v1.json"]
    scope = docs["controlled_dryrun_scope_v1.json"]
    scenario_set = docs["controlled_dryrun_scenario_set_v1.json"]
    scenario_results_doc = docs["controlled_dryrun_scenario_results_v1.json"]
    flow_val = docs["module_level_flow_validation_v1.json"]
    cand_val = docs["candidate_output_validation_v1.json"]
    guard_doc = docs["non_execution_guard_dryrun_v1.json"]
    error_doc = docs["error_blocker_defer_handling_validation_v1.json"]
    dryrun_summary = docs["module_level_dryrun_result_summary_v1.json"]
    integration_doc = docs["integration_readiness_positioning_v1.json"]
    route_doc = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]
    results = scenario_results_doc.get("results") or []

    for name in ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 40)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    for doc in DOC_PATHS:
        _add(checks, f"doc.{doc.split('/')[-1][:24]}", (REPO_ROOT / doc).is_file())

    _add(checks, "upstream.skeleton_go", skeleton_summary.get("final_decision") == SKELETON_FINAL_GO)
    _add(checks, "upstream.skeleton_verifier", skeleton_verifier.get("verifier") == "GO")
    _add(checks, "upstream.skeleton_next", skeleton_summary.get("recommended_next_phase") == SKELETON_NEXT_PHASE)
    _add(checks, "upstream.smoke_ok", skeleton_summary.get("controlled_skeleton_smoke_ok") is True)
    _add(checks, "upstream.all_cand", skeleton_summary.get("all_outputs_candidate_only") is True)

    _add(checks, "summary.pass", summary.get("orchestration_module_level_controlled_dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.failed0", summary.get("failed_scenarios") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _expect_false(checks, "summary.promotion_exec", summary.get("candidate_promotion_executed"))
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))
    _add(checks, "summary.dryrun_ok", summary.get("module_level_controlled_dryrun_ok") is True)
    _add(checks, "summary.all_scenarios", summary.get("all_scenarios_passed") is True)
    _add(checks, "summary.guard_ok", summary.get("non_execution_guard_ok") is True)
    _add(checks, "summary.not_split", summary.get("implementation_not_split_into_subphases") is True)

    _add(checks, "scope.not_runtime", scope.get("not_runtime") is True)
    _add(checks, "scope.not_integration", scope.get("not_integration_test") is True)
    _add(checks, "scenarios.complete", scenario_set.get("controlled_dryrun_scenario_set_complete") is True)
    _add(checks, "scenarios.count11", scenario_set.get("scenario_count") >= 11)
    _add(checks, "results.complete", scenario_results_doc.get("controlled_dryrun_scenario_results_complete") is True)
    _add(checks, "results.count11", len(results) >= 11)

    for s in DRYRUN_SCENARIOS:
        sid = s["scenario_id"]
        entry = next((r for r in results if r.get("scenario_id") == sid), {})
        _add(checks, f"scenario.{sid[:20]}", bool(entry))
        _add(checks, f"scenario.{sid[:12]}.pass", entry.get("scenario_passed") is True)
        _add(checks, f"scenario.{sid[:12]}.no_real", entry.get("real_execution") is False)
        _add(checks, f"scenario.{sid[:12]}.no_side", entry.get("side_effect_allowed") is False)

    _add(checks, "flow.complete", flow_val.get("module_level_flow_validation_complete") is True)
    for step in FLOW_STEPS:
        _add(checks, f"flow.{step[:18]}", any(x.get("step") == step for x in flow_val.get("steps") or []))

    _add(checks, "cand.complete", cand_val.get("candidate_output_validation_complete") is True)
    _add(checks, "cand.all_cand", cand_val.get("all_outputs_candidate_only") is True)

    _add(checks, "guard.complete", guard_doc.get("non_execution_guard_dryrun_complete") is True)
    _add(checks, "guard.ok", guard_doc.get("non_execution_guard_ok") is True)
    for g in NON_EXECUTION_GUARDS:
        _add(checks, f"guard.{g[:18]}", (guard_doc.get("guards") or {}).get(g) is True)

    _add(checks, "error.complete", error_doc.get("error_blocker_defer_handling_validation_complete") is True)
    _add(checks, "error.val_failure", error_doc.get("handles_validation_failure") is True)
    _add(checks, "error.missing_ref", error_doc.get("handles_missing_ref") is True)

    _add(checks, "dryrun_summary.complete", dryrun_summary.get("module_level_dryrun_result_summary_complete") is True)
    _add(checks, "dryrun_summary.ok", dryrun_summary.get("module_level_controlled_dryrun_ok") is True)
    _add(checks, "dryrun_summary.passed", dryrun_summary.get("passed_scenarios") == dryrun_summary.get("total_scenarios"))

    _add(checks, "integration.not_runtime", integration_doc.get("not_ready_for_runtime") is True)
    _add(checks, "integration.not_real", integration_doc.get("not_ready_for_real_execution") is True)
    _add(checks, "integration.no_test", integration_doc.get("integration_test_executed") is False)
    _add(checks, "integration.ready_plan", integration_doc.get("ready_for_downstream_module_integration_planning") is True)

    _add(checks, "route.complete", route_doc.get("next_route_decision_complete") is True)
    _add(checks, "route.selected", route_doc.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "route.gap_consolidation", NEXT_PHASE_GO in (route_doc.get("recommended_next_phase") or ""))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)

    for rel in ORCHESTRATION_MODULE_DRYRUN_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')} {md}".lower()
        _add(checks, f"forbidden.not_{fb[:15]}", fb not in combined)

    _add(checks, "summary.prior_skeleton", summary.get("prior_controlled_skeleton_implementation_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "upstream.verifier_min", int(skeleton_verifier.get("passed_checks", 0)) >= 360)

    for rule in misclassify.get("rules") or []:
        _add(checks, f"rule.{rule[:20]}", True)

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.final", FINAL_DECISION_GO in md or "GAP_CONSOLIDATION" in md)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "route.no_complete", route_doc.get("do_not_declare_midplatform_completed") is True)

    for idx, s in enumerate(DRYRUN_SCENARIOS):
        _add(checks, f"set_idx.{idx}", s["scenario_id"] in (scenario_set.get("scenarios") or []))

    for idx, r in enumerate(results):
        _add(checks, f"res_type.{idx}", bool(r.get("actual_result_type")))
        _add(checks, f"res_guard.{idx}", all((r.get("non_execution_guard_result") or {}).values()))

    for g in NON_EXECUTION_GUARDS:
        _add(checks, f"summary.guard_{g[:10]}", guard_doc.get("non_execution_guard_ok") is True)

    for step in FLOW_STEPS:
        entry = next((x for x in flow_val.get("steps") or [] if x.get("step") == step), {})
        _add(checks, f"flow_ex.{step[:14]}", entry.get("exercised_in_happy_path") is True)

    for alt in route_doc.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.get('route_id', '')}", bool(alt))

    _add(checks, "summary.scope_meta", summary.get("scope") == SCOPE)
    _add(checks, "summary.selected_route", summary.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "upstream.failed0", skeleton_verifier.get("failed_checks") == 0)
    _add(checks, "misclassify.rules9", len(misclassify.get("rules") or []) >= 9)

    _add(checks, "summary.file_size_exists", summary.get("file_size_governance_review_exists") is True)
    _add(checks, "summary.monolithic_absent", summary.get("monolithic_file_absent") is True)
    _add(checks, "summary.tmp_scan_absent", summary.get("tmp_eval_out_scan_absent") is True)
    _add(checks, "summary.index_first", summary.get("summary_index_first_reading_ok") is True)
    _add(checks, "summary.limited_scan", summary.get("limited_directory_scan_ok") is True)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "summary.future_design_ok", summary.get("future_design_not_current_blocker") is True)
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "summary.remaining_work", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "summary.record_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.auth_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.route_absent", summary.get("route_execution_absent") is True)
    _add(checks, "summary.handoff_absent", summary.get("module_handoff_runtime_absent") is True)
    _add(checks, "summary.drive_absent", summary.get("drive_brain_implementation_absent") is True)
    _add(checks, "summary.reflection_absent", summary.get("reflection_brain_implementation_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.no_fragment", summary.get("no_fragmentary_phase_expansion") is True)

    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_tier.{idx}", row.get("tier") == "ok")
        _add(checks, f"phase_exists.{idx}", row.get("exists") is True)
        _add(checks, f"phase_lines.{idx}", (row.get("line_count") or 0) <= 600)

    for idx, r in enumerate(results):
        _add(checks, f"res_pass.{idx}", r.get("scenario_passed") is True)
        _add(checks, f"res_exp.{idx}", bool(r.get("expected_result_type")))
        _add(checks, f"res_prod.{idx}", len(r.get("produced_candidates") or []) >= 1)

    for idx, check in enumerate(cand_val.get("checks") or []):
        _add(checks, f"cand_chk.{idx}.cand", check.get("candidate_only") is True)
        _add(checks, f"cand_chk.{idx}.no_side", check.get("side_effect_allowed") is False)

    for idx, path in enumerate(error_doc.get("decision_paths") or []):
        _add(checks, f"dec_path.{idx}", bool(path.get("scenario_id")))
        _add(checks, f"dec_cand.{idx}", path.get("candidate_only") is True)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"go_cond.{key[:18]}", summary.get(key) is True)

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "orchestration_module_level_controlled_dryrun_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "candidate_promotion_executed": False,
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
