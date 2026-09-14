#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Mount DryRunAndReview v1."""

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
    FINAL_DECISION_GO as HW_HANDOFF_FINAL,
)
from capabilities.midplatform.midplatform_task_manager_mount_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    DECISION_CENTER_DEPENDENCY_RULES,
    DOWNSTREAM_HANDOFFS,
    DRYRUN_NON_CLAIMS,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    GOVERNANCE_BOUNDARIES,
    HEALTH_METRICS,
    HEALTH_WATCHDOG_DEPENDENCY_RULES,
    INPUT_REQUIRED_FIELDS,
    INPUT_TYPES,
    MODEL_USES_LATER,
    NEXT_PHASE_GO,
    OUTPUT_CANDIDATES,
    PHASE_ID,
    PROCESSING_STEPS,
    RULE_USES,
    SAMPLE_FLOWS,
    SCOPE,
    TASK_STATES,
)
from capabilities.midplatform.midplatform_task_manager_mount_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
)

MIN_CHECKS = 540
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_task_manager_mount_dryrun_and_review"
DEFAULT_PLANNING = REPO_ROOT / "_tmp_eval_out" / "midplatform_task_manager_mount_planning"
DEFAULT_HW = REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_foundation_handoff_dryrun_and_review"

REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "upstream_mount_contract_consumability_review_v1.json",
    "health_watchdog_frozen_dependency_review_v1.json",
    "decision_center_frozen_dependency_review_v1.json",
    "mount_contract_10_section_review_v1.json",
    "input_contract_dryrun_v1.json",
    "output_contract_dryrun_v1.json",
    "processing_model_dryrun_v1.json",
    "task_state_machine_dryrun_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "governance_boundary_dryrun_v1.json",
    "downstream_handoff_matrix_review_v1.json",
    "sample_flow_dryrun_v1.json",
    "failure_route_dryrun_review_v1.json",
    "mount_health_metric_scope_review_v1.json",
    "boundary_matrix_review_v1.json",
    "non_claims_review_v1.json",
    "issue_register_v1.json",
    "mount_dryrun_readiness_decision_v1.json",
    "summary.json",
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
    parser.add_argument("--planning-root", default=str(DEFAULT_PLANNING))
    parser.add_argument("--health-watchdog-handoff-root", default=str(DEFAULT_HW))
    args = parser.parse_args()

    root = Path(args.output_root)
    planning = Path(args.planning_root)
    hw_root = Path(args.health_watchdog_handoff_root)
    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS}
    checks: List[Dict[str, Any]] = []

    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", bool(docs[fname]))

    planning_summary = _read(planning / "summary.json")
    planning_verifier = _read(planning / "verifier_report.json")
    hw_summary = _read(hw_root / "summary.json")
    hw_verifier = _read(hw_root / "verifier_report.json")
    _add(checks, "upstream.planning.go", planning_summary.get("final_decision") == PLANNING_FINAL)
    _add(checks, "upstream.planning.verifier", planning_verifier.get("verifier") == "GO")
    _add(checks, "upstream.hw.go", hw_summary.get("final_decision") == HW_HANDOFF_FINAL)
    _add(checks, "upstream.hw.verifier", hw_verifier.get("verifier") == "GO")
    _add(checks, "upstream.hw.foundation", hw_summary.get("foundation_id") == "midplatform_health_watchdog_foundation_v1")
    _add(checks, "upstream.hw.runtime", hw_summary.get("runtime_status") == "not_enabled")

    summary = docs["summary.json"]
    upstream = docs["upstream_mount_contract_consumability_review_v1.json"]
    hw_dep = docs["health_watchdog_frozen_dependency_review_v1.json"]
    dc_dep = docs["decision_center_frozen_dependency_review_v1.json"]
    contract = docs["mount_contract_10_section_review_v1.json"]
    inp = docs["input_contract_dryrun_v1.json"]
    out = docs["output_contract_dryrun_v1.json"]
    proc = docs["processing_model_dryrun_v1.json"]
    sm = docs["task_state_machine_dryrun_v1.json"]
    mra = docs["model_rule_algorithm_placement_review_v1.json"]
    gov = docs["governance_boundary_dryrun_v1.json"]
    handoff = docs["downstream_handoff_matrix_review_v1.json"]
    samples = docs["sample_flow_dryrun_v1.json"]
    failures = docs["failure_route_dryrun_review_v1.json"]
    metrics = docs["mount_health_metric_scope_review_v1.json"]
    boundary = docs["boundary_matrix_review_v1.json"]
    nc = docs["non_claims_review_v1.json"]
    issues = docs["issue_register_v1.json"]
    readiness = docs["mount_dryrun_readiness_decision_v1.json"]

    _add(checks, "phase.id", summary.get("phase") == PHASE_ID)
    _add(checks, "scope.id", summary.get("scope") == SCOPE)
    _add(checks, "summary.pass", summary.get("dryrun_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "readiness.pass", readiness.get("dryrun_pass") is True)
    _add(checks, "readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "issues.blocker0", issues.get("blocker_count") == 0)

    for doc_name, doc in docs.items():
        _add(checks, f"meta.foundation.{doc_name}", doc.get("foundation_id") == "midplatform_health_watchdog_foundation_v1")
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")

    _add(checks, "upstream.review.pass", upstream.get("dryrun_and_review_pass") is True)
    _add(checks, "upstream.review.no_blocker", upstream.get("blocker") is False)
    _add(checks, "upstream.artifact_count", upstream.get("artifact_count") >= 19)

    _add(checks, "hw_dep.pass", hw_dep.get("dryrun_and_review_pass") is True)
    _add(checks, "hw_dep.foundation", hw_dep.get("dependency_foundation_id") == "midplatform_health_watchdog_foundation_v1")
    _add(checks, "hw_dep.no_redefine", hw_dep.get("must_not_redefine_health_watchdog") is True)
    _add(checks, "hw_dep.no_modify_type", hw_dep.get("must_not_modify_health_watchdog_candidate_type") is True)
    _add(checks, "hw_dep.not_executed_task", hw_dep.get("hold_blocked_safety_not_executed_task") is True)
    _add(checks, "hw_dep.not_recovered", hw_dep.get("recovery_recommendation_not_recovered") is True)
    _add(checks, "hw_dep.no_runtime", hw_dep.get("health_watchdog_runtime_required") is False)
    for rule in HEALTH_WATCHDOG_DEPENDENCY_RULES:
        _add(checks, f"hw_dep.rule.{rule[:50]}", any(rule[:45] in str(c.get("check_id")) for c in hw_dep.get("checks") or []))

    _add(checks, "dc_dep.pass", dc_dep.get("dryrun_and_review_pass") is True)
    _add(checks, "dc_dep.foundation", dc_dep.get("dependency_foundation_id") == "midplatform_decision_center_foundation_v1")
    _add(checks, "dc_dep.no_redefine", dc_dep.get("must_not_redefine_decision_center") is True)
    _add(checks, "dc_dep.no_modify", dc_dep.get("must_not_modify_decision_candidate") is True)
    _add(checks, "dc_dep.not_final", dc_dep.get("decision_candidate_not_final_action") is True)
    _add(checks, "dc_dep.no_runtime", dc_dep.get("decision_center_runtime_required") is False)
    for rule in DECISION_CENTER_DEPENDENCY_RULES:
        _add(checks, f"dc_dep.rule.{rule[:50]}", any(rule[:45] in str(c.get("check_id")) for c in dc_dep.get("checks") or []))

    _add(checks, "contract.pass", contract.get("dryrun_and_review_pass") is True)
    for section in TEMPLATE_SECTIONS:
        _add(checks, f"contract.section.{section}", section in (contract.get("sections") or []))

    _add(checks, "input.pass", inp.get("dryrun_and_review_pass") is True)
    for item in INPUT_TYPES:
        _add(checks, f"input.{item}", any(item in str(c.get("check_id")) for c in inp.get("checks") or []))
    for field in INPUT_REQUIRED_FIELDS:
        _add(checks, f"input.required.{field}", any(field in str(c.get("check_id")) for c in inp.get("checks") or []))
    for key in ("candidate_not_fact_validated", "trace_validated", "health_tag_validated", "source_chain_validated", "governance_ref_for_high_risk_validated"):
        _add(checks, f"input.{key}", inp.get(key) is True)

    _add(checks, "output.pass", out.get("dryrun_and_review_pass") is True)
    _add(checks, "output.candidate_only", out.get("all_outputs_candidate_only") is True)
    for item in OUTPUT_CANDIDATES:
        _add(checks, f"output.{item}", item in (out.get("outputs") or []))
    _add(checks, "output.task_candidate_not_execution", any("task_candidate_not_task_execution" in str(c.get("check_id")) and c.get("pass") for c in out.get("checks") or []))
    _add(checks, "output.task_step_not_executed", any("task_step_candidate_not_executed_step" in str(c.get("check_id")) and c.get("pass") for c in out.get("checks") or []))
    _add(checks, "output.task_handoff_not_direct", any("task_handoff_candidate_not_direct_mount" in str(c.get("check_id")) and c.get("pass") for c in out.get("checks") or []))

    _add(checks, "processing.pass", proc.get("dryrun_and_review_pass") is True)
    _add(checks, "processing.candidate_only", proc.get("candidate_only") is True)
    _add(checks, "processing.no_task_runtime", proc.get("task_runtime_executed") is False)
    for step in PROCESSING_STEPS:
        _add(checks, f"processing.{step[:45]}", step in (proc.get("steps") or []))

    _add(checks, "state.pass", sm.get("dryrun_and_review_pass") is True)
    for state in TASK_STATES:
        _add(checks, f"state.{state}", state in (sm.get("states") or []))
    for state in ("ready", "hold", "blocked", "paused", "not_ready", "requires_observation"):
        _add(checks, f"state.cover.{state}", state in (sm.get("covered_terminal_candidate_states") or []))

    _add(checks, "mra.pass", mra.get("dryrun_and_review_pass") is True)
    _add(checks, "mra.model_false", mra.get("model_invoked_now") is False)
    for item in MODEL_USES_LATER:
        _add(checks, f"mra.model_later.{item}", item in (mra.get("model_uses_later") or []))
    for item in RULE_USES:
        _add(checks, f"mra.rule.{item}", item in (mra.get("rules") or []))

    _add(checks, "gov.pass", gov.get("dryrun_and_review_pass") is True)
    for rule in GOVERNANCE_BOUNDARIES:
        _add(checks, f"gov.rule.{rule[:45]}", any(rule[:35] in str(c.get("check_id")) for c in gov.get("checks") or []))
    for scenario in (
        "task_execution_attempted",
        "tool_call_attempted",
        "output_attempted",
        "memory_write_attempted",
        "worldmodel_write_attempted",
        "model_invocation_attempted_now",
        "provider_invocation_attempted_now",
    ):
        _add(checks, f"gov.scenario.{scenario}", any(scenario in str(s.get("scenario")) and s.get("blocked") for s in gov.get("scenarios") or []))

    _add(checks, "handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    _add(checks, "handoff.direct_false", handoff.get("direct_mount") is False)
    _add(checks, "handoff.mount_now_false", handoff.get("mount_now") is False)
    targets = {h.get("target"): h for h in handoff.get("handoffs") or []}
    for item in DOWNSTREAM_HANDOFFS:
        _add(checks, f"handoff.target.{item['target']}", item["target"] in targets)
        _add(checks, f"handoff.direct.{item['target']}", targets.get(item["target"], {}).get("direct_mount") is False)

    _add(checks, "samples.pass", samples.get("dryrun_and_review_pass") is True)
    _add(checks, "samples.count7", samples.get("sample_count") >= 7)
    sample_docs = {s.get("flow_id"): s for s in samples.get("samples") or []}
    for sample in SAMPLE_FLOWS:
        doc = sample_docs.get(sample["flow_id"]) or {}
        _add(checks, f"sample.{sample['flow_id']}", doc.get("passed") is True)
        _add(checks, f"sample.input.{sample['flow_id']}", bool(doc.get("input")))
        _add(checks, f"sample.processing.{sample['flow_id']}", bool(doc.get("processing")))
        _add(checks, f"sample.output.{sample['flow_id']}", bool(doc.get("output")))
        _add(checks, f"sample.blocked.{sample['flow_id']}", bool(doc.get("blocked_paths")))
        _add(checks, f"sample.terminal.{sample['flow_id']}", bool(doc.get("terminal_status")))

    _add(checks, "failures.pass", failures.get("dryrun_and_review_pass") is True)
    _add(checks, "failures.count16", failures.get("route_count") >= 16)
    for route in FAILURE_ROUTES:
        doc = next((r for r in failures.get("routes") or [] if r.get("route_id") == route["route_id"]), {})
        _add(checks, f"failure.{route['route_id']}", bool(doc))
        for field in ("detection_signal", "impact", "default_response", "hold_or_block_candidate", "forbidden_shortcut"):
            _add(checks, f"failure.{route['route_id']}.{field}", bool(doc.get(field)))

    _add(checks, "metrics.pass", metrics.get("dryrun_and_review_pass") is True)
    _add(checks, "metrics.no_runtime", metrics.get("real_health_runtime_enabled") is False)
    for metric in HEALTH_METRICS:
        _add(checks, f"metric.{metric}", metric in (metrics.get("metrics") or []))

    global_b = boundary.get("global_boundaries") or {}
    _add(checks, "boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    for flag in BOUNDARY_FALSE:
        _add(checks, f"boundary.false.{flag}", global_b.get(flag) is False)
        for artifact_name, doc in docs.items():
            _add(checks, f"artifact_boundary.false.{artifact_name}.{flag}", doc.get(flag) is False)

    _add(checks, "non_claim.pass", nc.get("dryrun_and_review_pass") is True)
    for claim in DRYRUN_NON_CLAIMS:
        _add(checks, f"non_claim.{claim}", claim in (nc.get("non_claims") or []))

    for sample in SAMPLE_FLOWS:
        for flag in BOUNDARY_FALSE:
            _add(checks, f"grid.sample_boundary.{sample['flow_id']}.{flag}", global_b.get(flag) is False)
    for output in OUTPUT_CANDIDATES:
        for flag in BOUNDARY_FALSE:
            _add(checks, f"grid.output_boundary.{output}.{flag}", global_b.get(flag) is False)

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
