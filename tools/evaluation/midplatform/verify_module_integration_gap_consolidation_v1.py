#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Module Integration Gap Consolidation v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.module_integration_gap_consolidation_items_v1 import (
    COMPLETED_MODULES,
    DO_NOT_REOPEN_RULES,
    GAP_CLASSIFICATIONS,
    NEXT_MODULE_CANDIDATES,
    REMAINING_GAPS,
    SELECTED_NEXT_MODULE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.module_integration_gap_consolidation_lineage_v1 import (
    MODULE_INTEGRATION_GAP_CONSOLIDATION_WHITELIST_FILES,
)
from capabilities.midplatform.module_integration_gap_consolidation_v1 import (
    DEFAULT_MODULE_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS
from capabilities.midplatform.task_manager_core_orchestration_module_level_controlled_dryrun_v1 import (
    FINAL_DECISION_GO as MODULE_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as MODULE_DRYRUN_NEXT_PHASE,
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
ARTIFACTS: Tuple[str, ...] = (
    "module_integration_gap_consolidation_report_v1.json",
    "module_integration_gap_consolidation_report_v1.md",
    "integration_gap_consolidation_scope_v1.json",
    "completed_module_inventory_v1.json",
    "remaining_gap_inventory_v1.json",
    "gap_classification_matrix_v1.json",
    "module_chain_readiness_map_v1.json",
    "next_module_candidate_selection_v1.json",
    "do_not_reopen_do_not_overbuild_rules_v1.json",
    "next_route_decision_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOC_PATHS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_MODULE_INTEGRATION_GAP_CONSOLIDATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MODULE_INTEGRATION_GAP_CONSOLIDATION_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_MODULE_INTEGRATION_GAP_CONSOLIDATION_V1_GO_NO_GO_PACK_V0.md",
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
    parser.add_argument("--module-dryrun-root", default=DEFAULT_MODULE_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    upstream = Path(args.module_dryrun_root)
    checks: List[Dict[str, Any]] = []

    dryrun_summary = _read(upstream / "summary.json")
    dryrun_verifier = _read(upstream / "verifier_report.json")
    md = (root / "module_integration_gap_consolidation_report_v1.md").read_text(encoding="utf-8") if (root / "module_integration_gap_consolidation_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["module_integration_gap_consolidation_report_v1.json"]
    scope = docs["integration_gap_consolidation_scope_v1.json"]
    completed = docs["completed_module_inventory_v1.json"]
    remaining = docs["remaining_gap_inventory_v1.json"]
    matrix = docs["gap_classification_matrix_v1.json"]
    chain_map = docs["module_chain_readiness_map_v1.json"]
    selection = docs["next_module_candidate_selection_v1.json"]
    reopen_rules = docs["do_not_reopen_do_not_overbuild_rules_v1.json"]
    route_doc = docs["next_route_decision_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 40)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    for doc in DOC_PATHS:
        _add(checks, f"doc.{doc.split('/')[-1][:24]}", (REPO_ROOT / doc).is_file())

    _add(checks, "upstream.dryrun_go", dryrun_summary.get("final_decision") == MODULE_DRYRUN_FINAL_GO)
    _add(checks, "upstream.dryrun_verifier", dryrun_verifier.get("verifier") == "GO")
    _add(checks, "upstream.dryrun_next", dryrun_summary.get("recommended_next_phase") == MODULE_DRYRUN_NEXT_PHASE)
    _add(checks, "upstream.dryrun_ok", dryrun_summary.get("module_level_controlled_dryrun_ok") is True)
    _add(checks, "upstream.all_scenarios", dryrun_summary.get("all_scenarios_passed") is True)

    _add(checks, "summary.pass", summary.get("module_integration_gap_consolidation_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _expect_false(checks, "summary.promotion_exec", summary.get("candidate_promotion_executed"))
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))
    _add(checks, "summary.handoff_gap", summary.get("module_handoff_contract_gap_identified") is True)
    _add(checks, "summary.orch_not_ext", summary.get("core_orchestration_not_extended") is True)
    _add(checks, "summary.runtime_not_ready", summary.get("runtime_not_ready") is True)
    _add(checks, "summary.real_exec_not_ready", summary.get("real_execution_not_ready") is True)
    _add(checks, "summary.int_test_deferred", summary.get("integration_test_planning_deferred") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)

    _add(checks, "scope.not_orch_ext", scope.get("not_core_orchestration_extension") is True)
    _add(checks, "scope.not_integration", scope.get("not_integration_test") is True)
    _add(checks, "scope.not_runtime", scope.get("not_runtime") is True)

    _add(checks, "completed.complete", completed.get("completed_module_inventory_complete") is True)
    _add(checks, "completed.count12", completed.get("module_count") >= 12)
    _add(checks, "remaining.complete", remaining.get("remaining_gap_inventory_complete") is True)
    _add(checks, "remaining.count16", remaining.get("gap_count") >= 16)

    for m in COMPLETED_MODULES:
        mid = m["module_id"]
        entry = next((x for x in completed.get("modules") or [] if x.get("module_id") == mid), {})
        _add(checks, f"mod.{mid[:20]}", bool(entry))
        _add(checks, f"mod.{mid[:12]}.no_rt", entry.get("runtime_ready") is False)
        _add(checks, f"mod.{mid[:12]}.no_it", entry.get("integration_tested") is False)

    for g in REMAINING_GAPS:
        gid = g["gap_id"]
        entry = next((x for x in remaining.get("gaps") or [] if x.get("gap_id") == gid), {})
        _add(checks, f"gap.{gid[:20]}", bool(entry))
        _add(checks, f"gap.{gid[:12]}.no_blk", not entry.get("blocker_now") if entry.get("classification") in ("future_runtime_debt", "future_design") else True)

    _add(checks, "matrix.complete", matrix.get("gap_classification_matrix_complete") is True)
    _add(checks, "matrix.future_rt_ok", matrix.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "matrix.future_design_ok", matrix.get("future_design_not_current_blocker") is True)
    _add(checks, "matrix.int_deferred", matrix.get("integration_test_planning_deferred") is True)
    _add(checks, "matrix.runtime_not_ready", matrix.get("runtime_not_ready") is True)
    for cls in GAP_CLASSIFICATIONS:
        _add(checks, f"cls.{cls[:18]}", cls in (matrix.get("classifications") or []))

    _add(checks, "chain.complete", chain_map.get("module_chain_readiness_map_complete") is True)
    _add(checks, "chain.controlled_flow", chain_map.get("boundary_lifecycle_alignment_orchestration_controlled_flow") is True)
    _add(checks, "chain.handoff_cand", chain_map.get("orchestration_produces_handoff_candidate") is True)
    _add(checks, "chain.handoff_not_impl", chain_map.get("module_handoff_contract_implemented") is False)
    _add(checks, "chain.int_not_impl", chain_map.get("integration_level_contract_implemented") is False)
    _add(checks, "chain.test_not_impl", chain_map.get("system_level_test_plan_implemented") is False)
    _add(checks, "chain.adapter_absent", chain_map.get("runtime_adapter_ready") is False)
    _add(checks, "chain.whitebox_absent", chain_map.get("whitebox_runtime_ready") is False)

    _add(checks, "selection.complete", selection.get("next_module_candidate_selection_complete") is True)
    _add(checks, "selection.handoff", selection.get("selected_module") == SELECTED_NEXT_MODULE)
    for c in NEXT_MODULE_CANDIDATES:
        _add(checks, f"cand.{c['route_id']}", any(x.get("route_id") == c["route_id"] for x in selection.get("candidates") or []))

    _add(checks, "reopen.complete", reopen_rules.get("do_not_reopen_do_not_overbuild_rules_complete") is True)
    for rule in DO_NOT_REOPEN_RULES:
        _add(checks, f"reopen.{rule[:18]}", rule in (reopen_rules.get("rules") or []))

    _add(checks, "route.complete", route_doc.get("next_route_decision_complete") is True)
    _add(checks, "route.handoff", NEXT_PHASE_GO in (route_doc.get("recommended_next_phase") or ""))
    _add(checks, "route.no_complete", route_doc.get("do_not_declare_midplatform_completed") is True)

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.survival_absent", summary.get("survival_brain_implementation_absent") is True)
    _add(checks, "summary.reflection_absent", summary.get("reflection_brain_implementation_absent") is True)
    _add(checks, "summary.drive_absent", summary.get("drive_brain_implementation_absent") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)

    for rel in MODULE_INTEGRATION_GAP_CONSOLIDATION_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')} {md}".lower()
        _add(checks, f"forbidden.not_{fb[:15]}", fb not in combined)

    _add(checks, "summary.prior_dryrun", summary.get("prior_core_orchestration_module_dryrun_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "summary.no_fragment", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "upstream.verifier_min", int(dryrun_verifier.get("passed_checks", 0)) >= 360)

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)

    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.final", FINAL_DECISION_GO in md or "HANDOFF" in md)
    _add(checks, "md.handoff", SELECTED_NEXT_MODULE in md)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "upstream.failed0", dryrun_verifier.get("failed_checks") == 0)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "summary.remaining_work", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "summary.scope_meta", summary.get("scope") == SCOPE)
    _add(checks, "summary.selected_module", summary.get("selected_next_module") == SELECTED_NEXT_MODULE)
    _add(checks, "gap.handoff_identified", any(g.get("gap_id") == "module_handoff_contract_not_implemented" for g in remaining.get("gaps") or []))

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)
        _add(checks, f"phase_tier.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")

    for idx, m in enumerate(COMPLETED_MODULES):
        _add(checks, f"mod_idx.{idx}", m["module_id"] in [x.get("module_id") for x in completed.get("modules") or []])

    for idx, g in enumerate(REMAINING_GAPS):
        _add(checks, f"gap_idx.{idx}", g["gap_id"] in [x.get("gap_id") for x in remaining.get("gaps") or []])
        _add(checks, f"gap_cls.{idx}", g["classification"] in GAP_CLASSIFICATIONS)

    for alt in route_doc.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.get('route_id', '')}", bool(alt))

    _add(checks, "summary.file_size_exists", summary.get("file_size_governance_review_exists") is True)
    _add(checks, "summary.file_size_ok", summary.get("file_size_governance_review_ok") is True)
    _add(checks, "summary.monolithic_absent", summary.get("monolithic_file_absent") is True)
    _add(checks, "summary.full_scan_absent", summary.get("full_repo_scan_absent") is True)
    _add(checks, "summary.tmp_scan_absent", summary.get("tmp_eval_out_scan_absent") is True)
    _add(checks, "summary.index_first", summary.get("summary_index_first_reading_ok") is True)
    _add(checks, "summary.limited_scan", summary.get("limited_directory_scan_ok") is True)
    _add(checks, "summary.future_rt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)
    _add(checks, "summary.future_design_ok", summary.get("future_design_not_current_blocker") is True)
    _add(checks, "summary.record_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.auth_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.route_absent", summary.get("route_execution_absent") is True)
    _add(checks, "summary.handoff_absent", summary.get("module_handoff_runtime_absent") is True)
    _add(checks, "owner_closed_module", summary.get("owner_approval_request_closed_module") == "governance_ready_handoff")
    _add(checks, "md.gaps", "Remaining gaps" in md or "gaps" in md.lower())
    _add(checks, "md.completed", "Completed modules" in md)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md or "Handoff" in md)
    _add(checks, "report.pass_flag", report.get("module_integration_gap_consolidation_pass") is True)
    _add(checks, "selection.rationale", bool(selection.get("rationale")))
    _add(checks, "matrix.counts", bool(matrix.get("counts")))
    _add(checks, "chain.runtime_not_ready", chain_map.get("runtime_not_ready") is True)
    _add(checks, "chain.real_not_ready", chain_map.get("real_execution_not_ready") is True)

    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"go_cond.{key[:18]}", summary.get(key) is True)

    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_exists.{idx}", row.get("exists") is True)

    for g in remaining.get("gaps") or []:
        if g.get("gap_id") == "module_handoff_contract_not_implemented":
            _add(checks, "handoff_gap.p1", g.get("priority") == "P1")
            _add(checks, "handoff_gap.blocker", g.get("blocker_now") is True)
            _add(checks, "handoff_gap.structure", g.get("classification") == "required_next_for_structure")

    for m in completed.get("modules") or []:
        if m.get("module_id") == "task_manager_core_orchestration_module_level_controlled_dryrun":
            _add(checks, "orch_dryrun.level", m.get("completion_level") == "module_dryrun_go")

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "module_integration_gap_consolidation_verifier_only": True,
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
