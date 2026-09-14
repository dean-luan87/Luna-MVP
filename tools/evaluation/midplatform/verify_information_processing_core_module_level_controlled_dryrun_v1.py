#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Information Processing Core Module-Level Controlled DryRun v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.information_processing_core_controlled_implementation_v1 import (
    FINAL_DECISION_GO as IPC_IMPL_FINAL_GO,
    NEXT_PHASE_GO as IPC_IMPL_NEXT_PHASE,
)
from capabilities.midplatform.information_processing_core_module_level_controlled_dryrun_items_v1 import (
    CORE_CAPABILITY_TAGS,
    DO_NOT_MISCLASSIFY_RULES,
    DRYRUN_SCENARIOS,
    NON_EXECUTION_GUARDS,
    WORK_MANUAL_FLOW_STEPS,
)
from capabilities.midplatform.information_processing_core_module_level_controlled_dryrun_lineage_v1 import (
    CORE_IMPLEMENTATION_FILES,
    IPC_MODULE_DRYRUN_WHITELIST_FILES,
)
from capabilities.midplatform.information_processing_core_module_level_controlled_dryrun_v1 import (
    DEFAULT_IPC_IMPLEMENTATION_ROOT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.information_processing_core_types_v1 import INFORMATION_TYPE_REGISTRY
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

MIN_CHECKS = 420
FORBIDDEN = ("midplatform_completed", "request_issued", "grant_issued", "runtime_enabled", "integration_test_executed", "record_created")
ARTIFACTS = (
    "information_processing_core_module_level_controlled_dryrun_report_v1.json",
    "module_level_dryrun_scope_v1.json",
    "ipc_module_level_scenario_set_v1.json",
    "ipc_module_level_scenario_results_v1.json",
    "work_manual_flow_validation_v1.json",
    "information_type_coverage_validation_v1.json",
    "candidate_output_validation_v1.json",
    "judge_referee_validation_v1.json",
    "workload_control_dryrun_v1.json",
    "peripheral_constraint_dryrun_v1.json",
    "non_execution_guard_dryrun_v1.json",
    "ipc_qualification_result_v1.json",
    "module_level_dryrun_result_summary_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_V1_GO_NO_GO_PACK_V0.md",
)


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--ipc-implementation-root", default=DEFAULT_IPC_IMPLEMENTATION_ROOT)
    args = parser.parse_args()
    root, upstream = Path(args.output_root), Path(args.ipc_implementation_root)
    checks: List[Dict[str, Any]] = []
    impl_s, impl_v = _read(upstream / "summary.json"), _read(upstream / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    scope = docs["module_level_dryrun_scope_v1.json"]
    scenario_set = docs["ipc_module_level_scenario_set_v1.json"]
    scenario_results = docs["ipc_module_level_scenario_results_v1.json"]
    flow = docs["work_manual_flow_validation_v1.json"]
    type_cov = docs["information_type_coverage_validation_v1.json"]
    cand = docs["candidate_output_validation_v1.json"]
    judge = docs["judge_referee_validation_v1.json"]
    workload = docs["workload_control_dryrun_v1.json"]
    peripheral = docs["peripheral_constraint_dryrun_v1.json"]
    guard = docs["non_execution_guard_dryrun_v1.json"]
    qual = docs["ipc_qualification_result_v1.json"]
    dryrun_sum = docs["module_level_dryrun_result_summary_v1.json"]
    route = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]
    results = scenario_results.get("results") or []

    for name in ARTIFACTS:
        if name == "verifier_report.json":
            continue
        _add(checks, f"art.{name.split('.')[0][:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.impl_go", impl_s.get("final_decision") == IPC_IMPL_FINAL_GO)
    _add(checks, "up.impl_next", impl_s.get("recommended_next_phase") == IPC_IMPL_NEXT_PHASE)
    _add(checks, "up.impl_v", impl_v.get("verifier") == "GO")
    _add(checks, "up.impl_min", int(impl_v.get("passed_checks", 0)) >= 420)
    _add(checks, "sum.pass", summary.get("information_processing_core_module_level_controlled_dryrun_pass") is True)
    _add(checks, "sum.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "sum.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "sum.dryrun_ok", summary.get("ipc_module_level_controlled_dryrun_ok") is True)
    _add(checks, "sum.all_scenarios", summary.get("all_scenarios_passed") is True)
    _add(checks, "sum.failed0", summary.get("failed_scenarios") == 0)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", summary.get(k) is True)

    _add(checks, "scope.ok", scope.get("module_level_dryrun_scope_complete") is True)
    _add(checks, "set.ok", scenario_set.get("ipc_module_level_scenario_set_complete") is True)
    _add(checks, "set.c20", scenario_set.get("scenario_count", 0) >= 20)
    _add(checks, "res.ok", scenario_results.get("ipc_module_level_scenario_results_complete") is True)
    _add(checks, "flow.ok", flow.get("work_manual_flow_validation_complete") is True)
    _add(checks, "flow.complete", flow.get("work_manual_flow_complete") is True)
    _add(checks, "type.ok", type_cov.get("information_type_coverage_validation_complete") is True)
    _add(checks, "type.complete", type_cov.get("information_type_coverage_complete") is True)
    _add(checks, "cand.ok", cand.get("candidate_output_validation_complete") is True)
    _add(checks, "judge.ok", judge.get("judge_referee_validation_complete") is True)
    _add(checks, "workload.ok", workload.get("workload_control_dryrun_complete") is True)
    _add(checks, "periph.ok", peripheral.get("peripheral_constraint_dryrun_complete") is True)
    _add(checks, "guard.ok", guard.get("non_execution_guard_dryrun_complete") is True)
    _add(checks, "qual.ok", qual.get("ipc_qualification_result_complete") is True)
    _add(checks, "drysum.ok", dryrun_sum.get("ipc_module_level_controlled_dryrun_ok") is True)
    _add(checks, "misclass.ok", misclassify.get("do_not_misclassify_rules_complete") is True)
    _add(checks, "route.a", route.get("selected_route_id") == "A")
    _add(checks, "route.next", route.get("recommended_next_phase") == NEXT_PHASE_GO)

    for rel in CORE_IMPLEMENTATION_FILES:
        _add(checks, f"core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for step in WORK_MANUAL_FLOW_STEPS:
        _add(checks, f"step.{step[:16]}", step in [s.get("step") for s in flow.get("steps") or []])
    for t in INFORMATION_TYPE_REGISTRY:
        _add(checks, f"reg.{t[:16]}", t in (type_cov.get("covered_types") or []))
    for tag in CORE_CAPABILITY_TAGS:
        entries = qual.get("entries") or []
        e = next((x for x in entries if x.get("capability_id") == tag), {})
        _add(checks, f"qual.{tag[:16]}", e.get("qualification_passed") is True)
    for g in NON_EXECUTION_GUARDS:
        _add(checks, f"gv.{g[:14]}", guard.get("guards", {}).get(g) is True)
        _add(checks, f"sum.{g[:14]}", summary.get(g) is True)
    for r in DO_NOT_MISCLASSIFY_RULES:
        _add(checks, f"mis.{r[:16]}", r in (misclassify.get("rules") or []))

    for case in results:
        _add(checks, f"sc.{case.get('scenario_id', '')[:16]}", case.get("scenario_passed") is True)
        _add(checks, f"re.{case.get('scenario_id', '')[:12]}", case.get("real_execution") is False)
        _add(checks, f"se.{case.get('scenario_id', '')[:12]}", case.get("side_effect_allowed") is False)

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", summary.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", file_size.get(k) is True)
    for rel in IPC_MODULE_DRYRUN_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")

    _add(checks, "sum.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", summary.get("scope") == SCOPE)
    _add(checks, "sum.issues_empty", summary.get("issues") == [])
    _add(checks, "sum.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "sum.remaining", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "sum.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "sum.no_it", summary.get("integration_test_executed") is False)
    _add(checks, "sum.runtime_abs", summary.get("runtime_execution_absent") is True)
    _add(checks, "sum.handoff_defer", summary.get("handoff_contract_p3_defer_remains_defer") is True)
    _add(checks, "sum.periph", summary.get("peripheral_contract_does_not_constrain_core") is True)
    _add(checks, "sum.unknown_ok", summary.get("unknown_information_allowed") is True)
    _add(checks, "sum.unknown_drop", summary.get("unknown_information_not_silently_dropped") is True)
    _add(checks, "sum.candidate_only", summary.get("all_outputs_candidate_only") is True)
    _add(checks, "sum.side_false", summary.get("all_outputs_side_effect_allowed") is False)
    _add(checks, "sum.real_false", summary.get("all_outputs_real_execution") is False)
    _add(checks, "sum.rtn_false", summary.get("all_outputs_runtime_required_now") is False)
    _add(checks, "sum.selected", summary.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "sum.chain", summary.get("owner_approval_request_chain_not_reopened") is True)
    _add(checks, "periph.handoff", peripheral.get("module_handoff_contract_not_required_for_information_classification") is True)
    _add(checks, "periph.integ", peripheral.get("integration_contract_not_required_for_information_classification") is True)
    _add(checks, "workload.single", workload.get("single_envelope_processing") is True)
    _add(checks, "workload.defer", workload.get("incomplete_information_can_defer") is True)
    _add(checks, "workload.dedup", workload.get("duplicate_information_idempotency_supported") is True)
    _add(checks, "drysum.passed", dryrun_sum.get("passed_scenarios", 0) >= 20)
    _add(checks, "drysum.failed0", dryrun_sum.get("failed_scenarios") == 0)

    for idx, s in enumerate(DRYRUN_SCENARIOS):
        _add(checks, f"scfg.{idx}", s["scenario_id"] in [c.get("scenario_id") for c in results])
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"plines.{idx}", (row.get("line_count") or 0) <= 600)
        _add(checks, f"pex.{idx}", row.get("exists") is True)
    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", summary.get(k) is True)
    for k in ABSENCE_KEYS:
        _add(checks, f"abs.{k[:14]}", summary.get(k) is True)
    for idx, t in enumerate(INFORMATION_TYPE_REGISTRY):
        _add(checks, f"tidx.{idx}", t in (type_cov.get("registered_types") or []))
    for idx, step in enumerate(WORK_MANUAL_FLOW_STEPS):
        s = next((x for x in flow.get("steps") or [] if x.get("step") == step), {})
        _add(checks, f"sout.{idx}", s.get("has_output") is True)
        _add(checks, f"sin.{idx}", s.get("has_input") is True)
    for idx, tag in enumerate(CORE_CAPABILITY_TAGS):
        entry = next((x for x in qual.get("entries") or [] if x.get("capability_id") == tag), {})
        _add(checks, f"qidx.{idx}", entry.get("qualification_passed") is True)
        _add(checks, f"sumcap.{tag[:12]}", summary.get(tag) is True if summary.get(tag) is not None else entry.get("qualification_passed") is True)
    _add(checks, "up.impl_failed0", impl_v.get("failed_checks") == 0)
    _add(checks, "sum.real_auth_false", summary.get("real_request_issuance_authorized") is False)
    _add(checks, "sum.adapter_abs", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "sum.whitebox_abs", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "sum.drive_abs", summary.get("drive_brain_implementation_absent") is True)
    _add(checks, "sum.survival_abs", summary.get("survival_brain_implementation_absent") is True)
    _add(checks, "sum.reflect_abs", summary.get("reflection_brain_implementation_absent") is True)
    _add(checks, "meta.dryrun_only", summary.get("information_processing_core_module_level_controlled_dryrun_only") is True)
    _add(checks, "judge.overreach", judge.get("no_overreach") is True)
    _add(checks, "judge.swallow", judge.get("no_downstream_work_swallowed") is True)
    _add(checks, "cand.side", cand.get("all_outputs_side_effect_allowed") is False)
    _add(checks, "cand.real", cand.get("all_outputs_real_execution") is False)
    report = docs.get("information_processing_core_module_level_controlled_dryrun_report_v1.json", {})
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "scope.job", scope.get("validates_ipc_as_complete_job_role") is True)
    _add(checks, "scope.not_impl", scope.get("not_new_ipc_implementation") is True)
    _add(checks, "scope.not_it", scope.get("not_integration_test") is True)
    _add(checks, "workload.overload", workload.get("overload_can_defer") is True)
    _add(checks, "workload.hrisk", workload.get("high_risk_information_governance_review_candidate") is True)
    _add(checks, "workload.swallow", workload.get("downstream_work_not_swallowed") is True)
    _add(checks, "periph.proto", peripheral.get("protocol_before_workflow_forbidden") is True)
    _add(checks, "periph.const", peripheral.get("constitution_only_hard_constraints_for_safety_authorization_privacy") is True)
    _add(checks, "type.unknown", type_cov.get("unknown_information_allowed") is True)
    _add(checks, "type.scope", type_cov.get("classification_scope_not_unbounded") is True)
    _add(checks, "route.defer_e", any(r.get("deferred") for r in route.get("alternate_routes") or [] if r.get("route_id") == "E"))
    _add(checks, "route.no_polish", route.get("do_not_continue_polishing_ipc") is True)
    _add(checks, "sum.prior_impl", summary.get("prior_ipc_controlled_implementation_go") is True)
    _add(checks, "sum.template", summary.get("template_lineage_ok") is True)
    _add(checks, "sum.no_fragment", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "sum.fs_exists", summary.get("file_size_governance_review_exists") is True)
    for idx, case in enumerate(results):
        _add(checks, f"cdown.{idx}", bool(case.get("downstream_readiness")))
        _add(checks, f"cval.{idx}", (case.get("validation_result") or {}).get("valid") is not False)
        _add(checks, f"cjudge.{idx}", bool(case.get("judge_referee_result")))
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY_RULES):
        _add(checks, f"mis2.{idx}", rule in (misclassify.get("rules") or []))
    for idx, rel in enumerate(CORE_IMPLEMENTATION_FILES):
        _add(checks, f"core2.{idx}", (REPO_ROOT / rel).is_file())
    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok3.{idx}", summary.get(k) is True)

    passed = sum(1 for x in checks if x["passed"])
    failed = [x for x in checks if not x["passed"]]
    v = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    payload = {
        "verifier": v,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "final_decision": FINAL_DECISION_GO if v == "GO" else "HOLD",
        "recommended_next_phase": NEXT_PHASE_GO if v == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "verifier": v,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "final_decision": payload["final_decision"],
        "recommended_next_phase": payload["recommended_next_phase"],
    }, ensure_ascii=False))
    return 0 if v == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
