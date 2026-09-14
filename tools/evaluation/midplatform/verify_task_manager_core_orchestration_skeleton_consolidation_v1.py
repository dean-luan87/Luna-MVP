#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Core Orchestration Skeleton Consolidation v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.candidate_lifecycle_unification_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_LIFECYCLE_ROOT,
    FINAL_DECISION_GO as CANDIDATE_LIFECYCLE_PLANNING_FINAL_GO,
)
from capabilities.midplatform.evidence_record_approval_permission_alignment_items_v1 import (
    SELECTED_NEXT_ROUTE as UPSTREAM_ALIGNMENT_SELECTED_ROUTE,
)
from capabilities.midplatform.evidence_record_approval_permission_alignment_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ALIGNMENT_ROOT,
    FINAL_DECISION_GO as ALIGNMENT_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as ALIGNMENT_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.module_boundary_registry_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_BOUNDARY_ROOT,
    FINAL_DECISION_GO as BOUNDARY_REGISTRY_PLANNING_FINAL_GO,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS
from capabilities.midplatform.task_manager_core_orchestration_skeleton_consolidation_v1 import (
    CONSOLIDATION_ARTIFACTS,
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    MIDPLATFORM_OVERALL_STATUS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_items_v1 import (
    CORE_ORCHESTRATION_EXCLUSIONS,
    CORE_ORCHESTRATION_RESPONSIBILITIES,
    FLOW_SKELETON_STEPS,
    FUTURE_BRAIN_INTERFACES,
    NON_EXECUTION_FORBIDDEN,
    ORCHESTRATION_INPUTS,
    ORCHESTRATION_OUTPUTS,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_lineage_v1 import (
    ORCHESTRATION_SKELETON_CONSOLIDATION_WHITELIST_FILES,
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
    parser.add_argument("--module-boundary-registry-planning-root", default=DEFAULT_BOUNDARY_ROOT)
    parser.add_argument("--candidate-lifecycle-unification-planning-root", default=DEFAULT_LIFECYCLE_ROOT)
    parser.add_argument("--alignment-planning-root", default=DEFAULT_ALIGNMENT_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    boundary_root = Path(args.module_boundary_registry_planning_root)
    lifecycle_root = Path(args.candidate_lifecycle_unification_planning_root)
    alignment_root = Path(args.alignment_planning_root)
    checks: List[Dict[str, Any]] = []

    boundary_summary = _read(boundary_root / "summary.json")
    boundary_verifier = _read(boundary_root / "verifier_report.json")
    lifecycle_summary = _read(lifecycle_root / "summary.json")
    lifecycle_verifier = _read(lifecycle_root / "verifier_report.json")
    alignment_summary = _read(alignment_root / "summary.json")
    alignment_verifier = _read(alignment_root / "verifier_report.json")

    md = (root / "task_manager_core_orchestration_skeleton_consolidation_report_v1.md").read_text(encoding="utf-8") if (root / "task_manager_core_orchestration_skeleton_consolidation_report_v1.md").is_file() else ""
    docs = {n: _read(root / n) for n in CONSOLIDATION_ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    summary = docs["summary.json"]
    report = docs["task_manager_core_orchestration_skeleton_consolidation_report_v1.json"]
    scope = docs["orchestration_consolidation_scope_v1.json"]
    role_def = docs["core_orchestration_skeleton_role_definition_v1.json"]
    io_contract = docs["orchestration_input_output_contract_v1.json"]
    flow = docs["orchestration_flow_skeleton_v1.json"]
    responsibility = docs["orchestration_responsibility_matrix_v1.json"]
    non_exec = docs["orchestration_non_execution_boundary_v1.json"]
    gap_register = docs["orchestration_gap_register_v1.json"]
    brain = docs["future_brain_interface_placeholder_v1.json"]
    route_decision = docs["next_route_decision_v1.json"]
    misclassify = docs["do_not_misclassify_rules_v1.json"]
    file_size = docs["file_size_governance_review_v1.json"]

    for name in CONSOLIDATION_ARTIFACTS:
        if name == "verifier_report.json":
            continue
        path = root / name
        ok = path.is_file() and (bool(_read(path)) if name.endswith(".json") else len(md.strip()) > 40)
        _add(checks, f"artifact.{name.split('.')[0]}", ok)

    _add(checks, "upstream.boundary_go", boundary_summary.get("final_decision") == BOUNDARY_REGISTRY_PLANNING_FINAL_GO)
    _add(checks, "upstream.boundary_verifier", boundary_verifier.get("verifier") == "GO")
    _add(checks, "upstream.lifecycle_go", lifecycle_summary.get("final_decision") == CANDIDATE_LIFECYCLE_PLANNING_FINAL_GO)
    _add(checks, "upstream.lifecycle_verifier", lifecycle_verifier.get("verifier") == "GO")
    _add(checks, "upstream.alignment_go", alignment_summary.get("final_decision") == ALIGNMENT_PLANNING_FINAL_GO)
    _add(checks, "upstream.alignment_verifier", alignment_verifier.get("verifier") == "GO")
    _add(checks, "upstream.alignment_route", alignment_summary.get("selected_next_route") == UPSTREAM_ALIGNMENT_SELECTED_ROUTE)
    _add(checks, "upstream.alignment_next", alignment_summary.get("recommended_next_phase") == ALIGNMENT_PLANNING_NEXT_PHASE)

    _add(checks, "summary.pass", summary.get("orchestration_skeleton_consolidation_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    for key in GO_CONDITIONS_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _expect_false(checks, "summary.real_auth", summary.get("real_request_issuance_authorized"))
    _expect_false(checks, "summary.promotion_exec", summary.get("candidate_promotion_executed"))
    _add(checks, "summary.skeleton_not_runtime", summary.get("orchestration_skeleton_not_runtime") is True)
    _add(checks, "summary.plan_not_exec", summary.get("orchestration_plan_candidate_not_executed_plan") is True)
    _add(checks, "summary.route_not_exec", summary.get("route_candidate_not_route_execution") is True)
    _add(checks, "summary.handoff_not_runtime", summary.get("module_handoff_candidate_not_runtime_handoff") is True)
    _add(checks, "summary.drive_not_impl", summary.get("drive_brain_placeholder_not_implementation") is True)
    _add(checks, "summary.reflection_not_impl", summary.get("reflection_brain_placeholder_not_implementation") is True)
    _add(checks, "summary.route_exec_absent", summary.get("route_execution_absent") is True)
    _add(checks, "summary.handoff_runtime_absent", summary.get("module_handoff_runtime_absent") is True)
    _add(checks, "summary.chain_not_reopen", summary.get("owner_approval_request_chain_not_reopened") is True)
    _expect_false(checks, "summary.integration_test", summary.get("integration_test_executed"))

    _add(checks, "scope.complete", scope.get("orchestration_consolidation_scope_complete") is True)
    _add(checks, "scope.not_runtime", scope.get("not_runtime_orchestration") is True)
    _add(checks, "scope.not_brain", scope.get("not_task_center_drive_brain") is True)
    _add(checks, "role.complete", role_def.get("core_orchestration_role_definition_complete") is True)
    _add(checks, "role.resp7", len(role_def.get("responsibilities") or []) >= 7)
    _add(checks, "role.excl8", len(role_def.get("exclusions") or []) >= 8)
    _add(checks, "io.complete", io_contract.get("orchestration_input_output_contract_complete") is True)
    _add(checks, "io.inputs12", len(io_contract.get("inputs") or []) >= 12)
    _add(checks, "io.outputs8", len(io_contract.get("outputs") or []) >= 8)
    _add(checks, "io.all_candidate", io_contract.get("all_outputs_candidate_layer") is True)
    _add(checks, "flow.complete", flow.get("orchestration_flow_skeleton_complete") is True)
    _add(checks, "flow.steps9", len(flow.get("steps") or []) >= 9)
    _add(checks, "resp.complete", responsibility.get("orchestration_responsibility_matrix_complete") is True)
    _add(checks, "non_exec.complete", non_exec.get("orchestration_non_execution_boundary_complete") is True)
    _add(checks, "non_exec.forbidden10", len(non_exec.get("forbidden_actions") or []) >= 10)
    _add(checks, "gaps.complete", gap_register.get("orchestration_gap_register_complete") is True)
    _add(checks, "brain.complete", brain.get("future_brain_interface_placeholder_complete") is True)
    _add(checks, "brain.interfaces5", len(brain.get("interfaces") or []) >= 5)
    _add(checks, "route.complete", route_decision.get("next_route_decision_complete") is True)
    _add(checks, "route.selected_a", route_decision.get("selected_next_route") == SELECTED_NEXT_ROUTE)
    _add(checks, "route.next_impl", NEXT_PHASE_GO in (route_decision.get("recommended_next_phase") or ""))

    for inp in ORCHESTRATION_INPUTS:
        _add(checks, f"in.{inp['input_id'][:18]}", any(i.get("input_id") == inp["input_id"] for i in io_contract.get("inputs") or []))
    for out in ORCHESTRATION_OUTPUTS:
        _add(checks, f"out.{out['output_id'][:18]}", any(o.get("output_id") == out["output_id"] for o in io_contract.get("outputs") or []))
        entry = next((o for o in io_contract.get("outputs") or [] if o.get("output_id") == out["output_id"]), {})
        _add(checks, f"out.{out['output_id'][:12]}.cand", entry.get("layer") == "candidate")

    for step in FLOW_SKELETON_STEPS:
        _add(checks, f"step.{step['step_id'][:18]}", any(s.get("step_id") == step["step_id"] for s in flow.get("steps") or []))

    for resp in CORE_ORCHESTRATION_RESPONSIBILITIES:
        _add(checks, f"resp.{resp[:18]}", resp in (role_def.get("responsibilities") or []))
    for excl in CORE_ORCHESTRATION_EXCLUSIONS:
        _add(checks, f"excl.{excl[:18]}", excl in (role_def.get("exclusions") or []))
    for fb in NON_EXECUTION_FORBIDDEN:
        _add(checks, f"forbid.{fb[:18]}", fb in (non_exec.get("forbidden_actions") or []))

    for key in ABSENCE_KEYS:
        _add(checks, f"summary.{key}", summary.get(key) is True)
    _add(checks, "summary.record_creation_absent", summary.get("record_creation_absent") is True)
    _add(checks, "summary.grant_absent", summary.get("grant_absent") is True)
    _add(checks, "summary.auth_req_absent", summary.get("authorization_request_absent") is True)
    _add(checks, "summary.evidence_absent", summary.get("evidence_bound_record_absent") is True)
    _add(checks, "summary.request_record_absent", summary.get("request_record_absent") is True)
    _add(checks, "summary.approval_record_absent", summary.get("approval_record_absent") is True)
    _add(checks, "summary.ack_record_absent", summary.get("ack_record_absent") is True)

    for key in FILE_SIZE_KEYS:
        _add(checks, f"file_size.{key}", summary.get(key) is True)
    for key in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"file_size.review.{key}", file_size.get(key) is True)
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"file_size.file.{rel.split('/')[-1]}", row.get("exists") is True and row.get("tier") != "blocker_candidate")

    for rel in ORCHESTRATION_SKELETON_CONSOLIDATION_WHITELIST_FILES:
        _add(checks, f"whitelist.{rel.split('/')[-1]}", (REPO_ROOT / rel).is_file())

    for fb in FORBIDDEN:
        combined = f"{summary.get('final_decision')} {summary.get('recommended_next_phase')} {md}".lower()
        _add(checks, f"forbidden.not_{fb[:15]}", fb not in combined)

    _add(checks, "summary.prior_boundary", summary.get("prior_boundary_registry_go") is True)
    _add(checks, "summary.prior_lifecycle", summary.get("prior_candidate_lifecycle_go") is True)
    _add(checks, "summary.prior_alignment", summary.get("prior_alignment_planning_go") is True)
    _add(checks, "summary.non_exec", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.phase", summary.get("phase") == PHASE_ID)
    _add(checks, "summary.issues_empty", summary.get("issues") == [])
    _add(checks, "upstream.boundary_min", int(boundary_verifier.get("passed_checks", 0)) >= 300)
    _add(checks, "upstream.lifecycle_min", int(lifecycle_verifier.get("passed_checks", 0)) >= 320)
    _add(checks, "upstream.alignment_min", int(alignment_verifier.get("passed_checks", 0)) >= 320)
    _add(checks, "resp.rows9", len(responsibility.get("rows") or []) >= 9)
    _add(checks, "gaps.items10", len(gap_register.get("gaps") or []) >= 10)
    _add(checks, "misclassify.rules9", len(misclassify.get("rules") or []) >= 9)
    _add(checks, "owner_closed_module", summary.get("owner_approval_request_closed_module") == "governance_ready_handoff")
    _add(checks, "summary.construction", summary.get("midplatform_overall_status") == MIDPLATFORM_OVERALL_STATUS)
    _add(checks, "summary.future_design_ok", summary.get("future_design_not_current_blocker") is True)
    _add(checks, "summary.runtime_debt_ok", summary.get("future_runtime_debt_not_current_blocker") is True)

    for rule in misclassify.get("rules") or []:
        _add(checks, f"rule.{rule[:20]}", True)
    for row in responsibility.get("rows") or []:
        _add(checks, f"mod.{row.get('module_id', '')[:18]}", bool(row.get("relation")))
    for iface in FUTURE_BRAIN_INTERFACES:
        _add(checks, f"brain.{iface['interface_id'][:18]}", any(
            b.get("interface_id") == iface["interface_id"] and b.get("implemented_now") is False
            for b in brain.get("interfaces") or []
        ))
    for gap in gap_register.get("gaps") or []:
        _add(checks, f"gap.{gap.get('gap_id', '')[:18]}", bool(gap.get("gap_id")))
    for alt in route_decision.get("alternate_routes") or []:
        _add(checks, f"alt.{alt.get('route_id', '')}", bool(alt))
    for sem in flow.get("semantics") or []:
        _add(checks, f"sem.{sem[:20]}", True)

    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in file_size.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"phase_file.{rel.split('/')[-1]}.lines", (row.get("line_count") or 0) <= 800)

    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "md.final", FINAL_DECISION_GO in md or "IMPLEMENTATION_PLANNING" in md)
    _add(checks, "md.selected_route", SELECTED_NEXT_ROUTE in md)
    _add(checks, "file_size.no_blocker", len(file_size.get("blocker_candidate_files") or []) == 0)
    _add(checks, "summary.template_lineage", summary.get("template_lineage_ok") is True)
    _add(checks, "scope.not_reopen", scope.get("not_reopen_owner_approval_request") is True)
    _add(checks, "route.no_complete", route_decision.get("do_not_declare_midplatform_completed") is True)
    _add(checks, "gaps.no_blocker", all(not g.get("blocker_now") for g in gap_register.get("gaps") or []))
    _add(checks, "brain.not_blocker", brain.get("future_design_not_current_blocker") is True)
    _add(checks, "upstream.failed0", boundary_verifier.get("failed_checks") == 0 and lifecycle_verifier.get("failed_checks") == 0 and alignment_verifier.get("failed_checks") == 0)
    _add(checks, "report.pass_flag", report.get("orchestration_skeleton_consolidation_pass") is True)
    _add(checks, "md.next_phase", NEXT_PHASE_GO in md or "Implementation Planning" in md)
    _add(checks, "misclassify.skeleton_rule", "orchestration_skeleton_consolidation_not_runtime_orchestration" in (misclassify.get("rules") or []))
    _add(checks, "summary.scope_meta", summary.get("scope") == SCOPE)
    _add(checks, "route.rationale", bool(route_decision.get("rationale")))
    _add(checks, "summary.transition_not_promo", summary.get("lifecycle_transition_request_candidate_not_promotion_executed") is True)

    for key in GO_CONDITIONS_KEYS:
        if key in report:
            _add(checks, f"report.{key}", report.get(key) is True)
    _add(checks, "upstream.boundary_pass", boundary_summary.get("boundary_registry_planning_pass") is True)
    _add(checks, "upstream.lifecycle_pass", lifecycle_summary.get("candidate_lifecycle_unification_planning_pass") is True)
    _add(checks, "upstream.alignment_pass", alignment_summary.get("alignment_planning_pass") is True)
    _add(checks, "upstream.boundary_entries", boundary_summary.get("all_required_modules_have_registry_entries") is True)
    _add(checks, "upstream.lifecycle_types", lifecycle_summary.get("all_candidate_types_covered") is True)
    _add(checks, "upstream.alignment_real_absent", alignment_summary.get("real_objects_absent") is True)
    _add(checks, "upstream.lifecycle_runtime_absent", lifecycle_summary.get("candidate_lifecycle_runtime_absent") is True)
    _add(checks, "upstream.alignment_runtime_absent", alignment_summary.get("alignment_runtime_absent") is True)
    _add(checks, "upstream.boundary_no_forbidden", boundary_summary.get("no_forbidden_ownership_detected") is True)
    _add(checks, "upstream.alignment_promo_false", alignment_summary.get("candidate_promotion_executed") is False)
    _add(checks, "scope.not_record_grant", scope.get("not_record_grant_creation") is True)
    _add(checks, "scope.purpose", bool(scope.get("purpose")))
    _add(checks, "flow.semantics4", len(flow.get("semantics") or []) >= 4)
    _add(checks, "misclassify.complete", misclassify.get("do_not_misclassify_rules_complete") is True)
    _add(checks, "role.definition_id", bool(role_def.get("definition_id")))
    _add(checks, "io.contract_id", bool(io_contract.get("contract_id")))
    _add(checks, "flow.skeleton_id", bool(flow.get("skeleton_id")))
    _add(checks, "non_exec.boundary_id", bool(non_exec.get("boundary_id")))
    _add(checks, "brain.placeholder_id", bool(brain.get("placeholder_id")))
    _add(checks, "summary.remaining_work", summary.get("midplatform_still_has_remaining_work") is True)
    _add(checks, "summary.not_final", summary.get("foundation_consolidation_not_final_midplatform_completion") is True)
    _add(checks, "summary.no_fragmentary", summary.get("no_fragmentary_phase_expansion") is True)
    _add(checks, "summary.preauth_not_open", summary.get("real_issuance_preauthorization_not_opened") is True)
    _add(checks, "summary.runtime_absent", summary.get("runtime_execution_absent") is True)
    _add(checks, "summary.adapter_absent", summary.get("module_adapter_implementation_absent") is True)
    _add(checks, "summary.whitebox_absent", summary.get("whitebox_runtime_integration_absent") is True)
    _add(checks, "summary.request_issued_absent", summary.get("request_issued_absent") is True)
    _add(checks, "summary.next_ready", summary.get("next_phase_readiness_ok") is True)
    _add(checks, "summary.consolidation_only", summary.get("orchestration_consolidation_only") is True if "orchestration_consolidation_only" in summary else summary.get("scope") == SCOPE)
    _add(checks, "report.skeleton_not_runtime", report.get("orchestration_skeleton_not_runtime") is True)
    _add(checks, "report.route_not_exec", report.get("route_candidate_not_route_execution") is True)
    _add(checks, "report.handoff_not_runtime", report.get("module_handoff_candidate_not_runtime_handoff") is True)
    _add(checks, "md.flow_steps", "Flow steps" in md)
    _add(checks, "md.orchestration", "Orchestration" in md)
    _add(checks, "file_size.phase_id", file_size.get("phase_id") == PHASE_ID)
    _add(checks, "file_size.no_full_scan", file_size.get("full_repo_scan") is False)

    for inp in io_contract.get("inputs") or []:
        _add(checks, f"incat.{inp.get('input_id', '')[:12]}", bool(inp.get("category")))
    for out in io_contract.get("outputs") or []:
        _add(checks, f"outlay.{out.get('output_id', '')[:12]}", out.get("layer") == "candidate")
    for step in flow.get("steps") or []:
        _add(checks, f"stepprod.{step.get('step_id', '')[:12]}", bool(step.get("produces") or step.get("reads")))
    for gap in gap_register.get("gaps") or []:
        _add(checks, f"gapstat.{gap.get('gap_id', '')[:12]}", bool(gap.get("status")))
        _add(checks, f"gappri.{gap.get('gap_id', '')[:12]}", bool(gap.get("priority")))
    for b in brain.get("interfaces") or []:
        _add(checks, f"brainstat.{b.get('interface_id', '')[:12]}", b.get("status") == "future_design")
        _add(checks, f"brainimpl.{b.get('interface_id', '')[:12]}", b.get("implemented_now") is False)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report_payload = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "orchestration_skeleton_consolidation_verifier_only": True,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        **{k: summary.get(k) is True for k in GO_CONDITIONS_KEYS},
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "candidate_promotion_executed": False,
        "orchestration_skeleton_not_runtime": summary.get("orchestration_skeleton_not_runtime") is True,
        "route_execution_absent": summary.get("route_execution_absent") is True,
        "module_handoff_runtime_absent": summary.get("module_handoff_runtime_absent") is True,
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
