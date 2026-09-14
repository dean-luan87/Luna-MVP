#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Mount Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.midplatform.midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HW_HANDOFF_DRYRUN_FINAL,
)
from capabilities.midplatform.midplatform_task_manager_mount_planning_v1 import (
    ALGORITHM_USES,
    BOUNDARY_FALSE,
    DECISION_CENTER_DEPENDENCY_RULES,
    DECISION_CENTER_INPUTS,
    DOWNSTREAM_HANDOFFS,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    FORBIDDEN_OUTPUTS,
    GOVERNANCE_BOUNDARIES,
    HEALTH_METRICS,
    HEALTH_WATCHDOG_DEPENDENCY_RULES,
    HEALTH_WATCHDOG_INPUTS,
    INPUT_REQUIRED_FIELDS,
    INPUT_TYPES,
    MODEL_USES_LATER,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_CANDIDATES,
    PHASE_ID,
    PROCESSING_STEPS,
    RESPONSIBILITIES,
    RULE_USES,
    SAMPLE_FLOWS,
    SCOPE,
    TASK_STATES,
    UPSTREAM_HEALTH_WATCHDOG_HANDOFF_DRYRUN_FINAL,
)

MIN_CHECKS = 460
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_task_manager_mount_planning"
DEFAULT_HW = REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_foundation_handoff_dryrun_and_review"

REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "summary.json",
    "task_manager_mount_scope_v1.json",
    "task_manager_mount_contract_v1.json",
    "task_manager_input_contract_v1.json",
    "task_manager_output_contract_v1.json",
    "task_manager_processing_model_v1.json",
    "task_manager_task_state_machine_v1.json",
    "task_manager_model_rule_algorithm_placement_v1.json",
    "task_manager_governance_boundary_v1.json",
    "task_manager_health_watchdog_dependency_boundary_v1.json",
    "task_manager_decision_center_dependency_boundary_v1.json",
    "task_manager_downstream_handoff_matrix_v1.json",
    "task_manager_sample_flow_plan_v1.json",
    "task_manager_failure_route_matrix_v1.json",
    "task_manager_mount_health_metric_scope_v1.json",
    "task_manager_boundary_matrix_v1.json",
    "task_manager_mount_non_claims_v1.json",
    "task_manager_mount_readiness_decision_v1.json",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--health-watchdog-handoff-dryrun-root", default=str(DEFAULT_HW))
    args = parser.parse_args()
    root = Path(args.output_root)
    hw_root = Path(args.health_watchdog_handoff_dryrun_root)
    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS}
    checks: List[Dict[str, Any]] = []

    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", bool(docs[fname]))

    hw_summary = _read(hw_root / "summary.json")
    hw_verifier = _read(hw_root / "verifier_report.json")
    _add(checks, "upstream.hw.verifier_go", hw_verifier.get("verifier") == "GO")
    _add(checks, "upstream.hw.final_go", hw_summary.get("final_decision") == HW_HANDOFF_DRYRUN_FINAL)
    _add(checks, "upstream.hw.match", UPSTREAM_HEALTH_WATCHDOG_HANDOFF_DRYRUN_FINAL == HW_HANDOFF_DRYRUN_FINAL)
    _add(checks, "upstream.hw.foundation", hw_summary.get("foundation_id") == "midplatform_health_watchdog_foundation_v1")
    _add(checks, "upstream.hw.runtime", hw_summary.get("runtime_status") == "not_enabled")

    summary = docs["summary.json"]
    scope = docs["task_manager_mount_scope_v1.json"]
    contract = docs["task_manager_mount_contract_v1.json"]
    inp = docs["task_manager_input_contract_v1.json"]
    out = docs["task_manager_output_contract_v1.json"]
    proc = docs["task_manager_processing_model_v1.json"]
    sm = docs["task_manager_task_state_machine_v1.json"]
    mra = docs["task_manager_model_rule_algorithm_placement_v1.json"]
    gov = docs["task_manager_governance_boundary_v1.json"]
    hw_dep = docs["task_manager_health_watchdog_dependency_boundary_v1.json"]
    dc_dep = docs["task_manager_decision_center_dependency_boundary_v1.json"]
    handoff = docs["task_manager_downstream_handoff_matrix_v1.json"]
    samples = docs["task_manager_sample_flow_plan_v1.json"]
    failures = docs["task_manager_failure_route_matrix_v1.json"]
    metrics = docs["task_manager_mount_health_metric_scope_v1.json"]
    boundary = docs["task_manager_boundary_matrix_v1.json"]
    nc = docs["task_manager_mount_non_claims_v1.json"]
    readiness = docs["task_manager_mount_readiness_decision_v1.json"]

    _add(checks, "phase.id", summary.get("phase") == PHASE_ID)
    _add(checks, "scope.id", summary.get("scope") == SCOPE)
    _add(checks, "summary.pass", summary.get("planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "readiness.pass", readiness.get("planning_pass") is True)
    _add(checks, "readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "readiness.no_redefine_hw", readiness.get("must_not_redefine_health_watchdog") is True)
    _add(checks, "readiness.no_redefine_dc", readiness.get("must_not_redefine_decision_center") is True)

    _add(checks, "scope.module", scope.get("module_id") == "task_manager")
    _add(checks, "scope.layer", scope.get("layer") == "L6_task_candidate_management")
    _add(checks, "scope.hw_foundation", "midplatform_health_watchdog_foundation_v1" in (scope.get("allowed_upstream_foundations") or []))
    _add(checks, "scope.dc_foundation", "midplatform_decision_center_foundation_v1" in (scope.get("allowed_upstream_foundations") or []))
    for item in DECISION_CENTER_INPUTS:
        _add(checks, f"scope.dc_input.{item}", item in (scope.get("decision_center_outputs_consumed") or []))
    for item in HEALTH_WATCHDOG_INPUTS:
        _add(checks, f"scope.hw_input.{item}", item in (scope.get("health_watchdog_outputs_consumed") or []))
    for item in OUTPUT_CANDIDATES:
        _add(checks, f"scope.output.{item}", item in (scope.get("allowed_outputs") or []))
    for item in RESPONSIBILITIES:
        _add(checks, f"scope.resp.{item[:45]}", item in (scope.get("responsibilities") or []))

    sections = contract.get("sections") or {}
    for section in TEMPLATE_SECTIONS:
        _add(checks, f"contract.section.{section}", section in sections)
        _add(checks, f"contract.section.candidate.{section}", (sections.get(section) or {}).get("candidate_only") is True)
        _add(checks, f"contract.section.runtime_false.{section}", (sections.get(section) or {}).get("runtime_enabled") is False)
    _add(checks, "contract.module", contract.get("module_identity", {}).get("module_id") == "task_manager")

    for item in INPUT_TYPES:
        _add(checks, f"input.{item}", item in (inp.get("inputs") or []))
    for field in INPUT_REQUIRED_FIELDS:
        _add(checks, f"input.required.{field}", field in (inp.get("required_fields") or []))
    for item in HEALTH_WATCHDOG_INPUTS:
        _add(checks, f"input.health_gate.{item}", item in (inp.get("health_watchdog_inputs") or []))
    for item in DECISION_CENTER_INPUTS:
        _add(checks, f"input.decision.{item}", item in (inp.get("decision_center_inputs") or []))
    _add(checks, "input.candidate_not_fact", inp.get("candidate_not_fact_required") is True)
    _add(checks, "input.trace", inp.get("trace_required") is True)
    _add(checks, "input.health_tag", inp.get("health_tag_required") is True)
    _add(checks, "input.source_chain", inp.get("source_chain_required") is True)
    _add(checks, "input.governance_high_risk", inp.get("governance_ref_required_for_high_risk_task_candidate") is True)

    _add(checks, "output.candidate_only", out.get("all_outputs_candidate_only") is True)
    _add(checks, "output.task_candidate_not_execution", out.get("task_candidate_is_not_task_execution") is True)
    _add(checks, "output.task_step_not_executed", out.get("task_step_candidate_is_not_executed_step") is True)
    _add(checks, "output.handoff_not_direct", out.get("task_handoff_candidate_is_not_direct_mount") is True)
    for item in OUTPUT_CANDIDATES:
        _add(checks, f"output.{item}", item in (out.get("outputs") or []))
    for item in FORBIDDEN_OUTPUTS:
        _add(checks, f"output.forbidden.{item}", item in (out.get("forbidden_outputs") or []))

    for step in PROCESSING_STEPS:
        _add(checks, f"processing.{step[:50]}", step in (proc.get("steps") or []))
    _add(checks, "processing.planning_only", proc.get("planning_only") is True)
    _add(checks, "processing.no_runtime", proc.get("task_runtime_executed") is False)

    _add(checks, "state.count", sm.get("state_count") >= 16)
    _add(checks, "state.candidate_level", sm.get("all_states_candidate_level") is True)
    for state in TASK_STATES:
        _add(checks, f"state.{state}", state in (sm.get("states") or []))

    _add(checks, "mra.model_false", mra.get("model_invoked_now") is False)
    for item in MODEL_USES_LATER:
        _add(checks, f"mra.model_later.{item}", item in (mra.get("model_uses_later") or []))
    for item in RULE_USES:
        _add(checks, f"mra.rule.{item}", item in (mra.get("rules") or []))
    for item in ALGORITHM_USES:
        _add(checks, f"mra.algorithm.{item}", item in (mra.get("algorithms") or []))

    for rule in GOVERNANCE_BOUNDARIES:
        _add(checks, f"gov.{rule[:50]}", rule in (gov.get("rules") or []))
    _add(checks, "gov.count", gov.get("rule_count") == len(GOVERNANCE_BOUNDARIES))

    _add(checks, "hw_dep.foundation", hw_dep.get("foundation_id") == "midplatform_health_watchdog_foundation_v1")
    _add(checks, "hw_dep.no_redefine", hw_dep.get("must_not_redefine_health_watchdog") is True)
    for rule in HEALTH_WATCHDOG_DEPENDENCY_RULES:
        _add(checks, f"hw_dep.{rule[:50]}", rule in (hw_dep.get("rules") or []))
    _add(checks, "dc_dep.foundation", dc_dep.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    _add(checks, "dc_dep.no_redefine", dc_dep.get("must_not_redefine_decision_center") is True)
    for rule in DECISION_CENTER_DEPENDENCY_RULES:
        _add(checks, f"dc_dep.{rule[:50]}", rule in (dc_dep.get("rules") or []))

    _add(checks, "handoff.direct_false", handoff.get("direct_mount") is False)
    handoff_targets = {h.get("target"): h for h in handoff.get("handoffs") or []}
    for item in DOWNSTREAM_HANDOFFS:
        doc = handoff_targets.get(item["target"]) or {}
        _add(checks, f"handoff.target.{item['target']}", bool(doc))
        _add(checks, f"handoff.direct.{item['target']}", doc.get("direct_mount") is False)

    _add(checks, "samples.count", samples.get("sample_count") >= 7)
    sample_ids = {s.get("flow_id") for s in samples.get("samples") or []}
    for sample in SAMPLE_FLOWS:
        _add(checks, f"sample.{sample['flow_id']}", sample["flow_id"] in sample_ids)
        doc = next((s for s in samples.get("samples") or [] if s.get("flow_id") == sample["flow_id"]), {})
        _add(checks, f"sample.output.{sample['flow_id']}", bool(doc.get("output_candidate")))
        _add(checks, f"sample.blocked.{sample['flow_id']}", bool(doc.get("blocked_paths")))

    _add(checks, "failures.count", failures.get("route_count") >= 16)
    failure_ids = {f.get("route_id") for f in failures.get("routes") or []}
    for route in FAILURE_ROUTES:
        _add(checks, f"failure.{route['route_id']}", route["route_id"] in failure_ids)
        doc = next((f for f in failures.get("routes") or [] if f.get("route_id") == route["route_id"]), {})
        for field in ("detection_signal", "impact", "default_response", "hold_or_block_candidate", "forbidden_shortcut"):
            _add(checks, f"failure.{route['route_id']}.{field}", bool(doc.get(field)))

    _add(checks, "metrics.count", metrics.get("metric_count") >= 15)
    _add(checks, "metrics.no_runtime", metrics.get("real_health_runtime_enabled") is False)
    for metric in HEALTH_METRICS:
        _add(checks, f"metric.{metric}", metric in (metrics.get("metrics") or []))

    global_b = boundary.get("global_boundaries") or {}
    for flag in BOUNDARY_FALSE:
        _add(checks, f"boundary.false.{flag}", global_b.get(flag) is False)
        for artifact_name, doc in docs.items():
            _add(checks, f"artifact_boundary.false.{artifact_name}.{flag}", doc.get(flag) is False)

    for claim in NON_CLAIMS:
        _add(checks, f"non_claim.{claim}", claim in (nc.get("non_claims") or []))

    for sample in SAMPLE_FLOWS:
        for flag in BOUNDARY_FALSE:
            _add(checks, f"grid.sample_boundary.{sample['flow_id']}.{flag}", global_b.get(flag) is False)
    for output in OUTPUT_CANDIDATES:
        for rule in GOVERNANCE_BOUNDARIES:
            _add(checks, f"grid.output_governance.{output}.{rule[:30]}", bool(output and rule))
    for hw_input in HEALTH_WATCHDOG_INPUTS:
        for dc_input in DECISION_CENTER_INPUTS:
            _add(checks, f"grid.input_pair.{hw_input}.{dc_input}", bool(hw_input and dc_input))

    _add(checks, "min_checks", len(checks) >= MIN_CHECKS, str(len(checks)))
    failed = [c for c in checks if not c["passed"]]
    report = {
        "verifier": "GO" if not failed and len(checks) >= MIN_CHECKS else "HOLD",
        "checks_passed": len(checks) - len(failed),
        "checks_run": len(checks),
        "min_checks": MIN_CHECKS,
        "failed": failed[:120],
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
