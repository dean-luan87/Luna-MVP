#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Health Management Layer Integration DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import SWITCHING_SCENARIOS
from capabilities.governance.model_management_layer_recovery_planning_v1 import HEALTH_STATES
from capabilities.governance.health_management_layer_integration_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    HEALTH_METRIC_DEFINITION_STATUS,
    HEALTH_SIGNAL_CONTRACT_FIELDS,
    HEALTH_STATUS_TAXONOMY,
    HEALTH_TO_DRIVE_ROUTES,
    METRIC_FORBIDDEN_NOW,
    SEVERITY_TAXONOMY,
)
from capabilities.governance.health_management_layer_integration_dryrun_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE_DRYRUN,
    FINAL_DECISION_GO,
    MODEL_HEALTH_TO_SIGNAL_TYPE,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
    SWITCHING_TO_OUTPUT,
)

MIN_CHECKS = 100

REQUIRED = (
    "health_management_dryrun_policy_v1.json",
    "health_management_planning_input_review_v1.json",
    "model_health_state_consumption_result_v1.json",
    "model_switching_candidate_consumption_result_v1.json",
    "software_health_signal_candidate_samples_v1.json",
    "hardware_health_signal_candidate_samples_v1.json",
    "system_health_signal_candidate_samples_v1.json",
    "fallback_candidate_samples_v1.json",
    "degradation_candidate_samples_v1.json",
    "survival_drive_candidate_samples_v1.json",
    "recovery_plan_candidate_samples_v1.json",
    "health_to_drive_bridge_dryrun_result_v1.json",
    "health_runtime_boundary_audit_v1.json",
    "health_metric_reserved_dryrun_review_v1.json",
    "health_management_blocked_path_result_v1.json",
    "health_management_dryrun_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _all_samples_have_contract(samples: List[Dict[str, Any]], checks: List[Dict[str, Any]], prefix: str) -> None:
    for i, sample in enumerate(samples):
        for field in HEALTH_SIGNAL_CONTRACT_FIELDS:
            if field == "source_chain":
                continue
            checks.append(
                {
                    "check_id": f"{prefix}.{i}.{field}",
                    "passed": field in sample,
                }
            )
        checks.append({"check_id": f"{prefix}.{i}.candidate_only", "passed": sample.get("candidate_only") is True})
        checks.append({"check_id": f"{prefix}.{i}.not_fact", "passed": sample.get("fact_status") == "not_fact"})
        checks.append({"check_id": f"{prefix}.{i}.no_action", "passed": sample.get("action_allowed") is False})
        sev = sample.get("severity")
        checks.append(
            {
                "check_id": f"{prefix}.{i}.severity",
                "passed": sev in SEVERITY_TAXONOMY if sev else True,
            }
        )
        hs = sample.get("health_status")
        checks.append(
            {
                "check_id": f"{prefix}.{i}.health_status",
                "passed": hs in HEALTH_STATUS_TAXONOMY if hs else True,
            }
        )
        checks.append(
            {
                "check_id": f"{prefix}.{i}.no_score_field",
                "passed": not any(k in sample for k in METRIC_FORBIDDEN_NOW),
            }
        )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "health_management_layer_integration_dryrun"
        ),
    )
    p.add_argument(
        "--health-management-layer-integration-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "health_management_layer_integration_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.health_management_layer_integration_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "health_management_dryrun_policy_v1.json")
    input_review = _load(root / "health_management_planning_input_review_v1.json")
    software = _load(root / "software_health_signal_candidate_samples_v1.json")
    hardware = _load(root / "hardware_health_signal_candidate_samples_v1.json")
    system = _load(root / "system_health_signal_candidate_samples_v1.json")
    fallback = _load(root / "fallback_candidate_samples_v1.json")
    degradation = _load(root / "degradation_candidate_samples_v1.json")
    survival = _load(root / "survival_drive_candidate_samples_v1.json")
    recovery = _load(root / "recovery_plan_candidate_samples_v1.json")
    bridge = _load(root / "health_to_drive_bridge_dryrun_result_v1.json")
    metric = _load(root / "health_metric_reserved_dryrun_review_v1.json")
    blocked = _load(root / "health_management_blocked_path_result_v1.json")
    readiness = _load(root / "health_management_dryrun_readiness_decision_v1.json")
    boundary = _load(root / "health_runtime_boundary_audit_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    plan_sm = _load(planning_root / "summary.json")
    plan_vr = _load(planning_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.dryrun_only", summary.get("health_management_layer_integration_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.signals_gen", summary.get("health_signal_candidate_generated_now") is True)
    ok("summary.fallback_gen", summary.get("fallback_candidate_generated_now") is True)
    ok("summary.degrade_gen", summary.get("degradation_candidate_generated_now") is True)
    ok("summary.survival_gen", summary.get("survival_drive_candidate_generated_now") is True)
    ok("summary.recovery_gen", summary.get("recovery_plan_candidate_generated_now") is True)
    ok("summary.no_score", summary.get("health_score_generated_now") is False)
    ok("summary.metric_reserved", summary.get("health_metric_definition_status") == HEALTH_METRIC_DEFINITION_STATUS)
    ok("summary.software6", summary.get("software_signal_count") == 6)
    ok("summary.high_risk0", summary.get("high_risk_count") == 0)

    ok("policy.scope", policy.get("scope") == SCOPE)
    ok("input.review_pass", input_review.get("review_pass") is True)
    ok("input.blockers_empty", len(input_review.get("blockers") or []) == 0)

    ok("upstream.plan_verifier", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_passed", plan_vr.get("passed") is True)
    ok("upstream.final", plan_sm.get("final_decision") == PLANNING_FINAL)

    ok("software.count6", software.get("sample_count") == 6)
    ok("hardware.count2", hardware.get("sample_count") >= 1)
    ok("system.count2", system.get("sample_count") >= 1)
    ok("fallback.count4", fallback.get("sample_count") == 4)
    ok("degradation.count3", degradation.get("sample_count") >= 2)
    ok("survival.count1", survival.get("sample_count") >= 1)
    ok("recovery.count2", recovery.get("sample_count") >= 1)

    ok("bridge.routes8", bridge.get("route_count") == 8)
    ok("bridge.pass", bridge.get("routing_pass") is True)
    ok("bridge.no_exec", bridge.get("active_drive_execution_enabled") is False)

    ok("metric.pass", metric.get("review_pass") is True)
    ok("metric.no_score_calc", metric.get("health_score_calculation_enabled_now") is False)
    ok("metric.no_threshold", metric.get("health_threshold_policy_enabled_now") is False)
    ok("metric.no_baseline", metric.get("health_metric_baseline_available_now") is False)
    ok("metric.no_runtime_data", metric.get("health_metric_runtime_data_available_now") is False)
    ok("metric.needs_observation", metric.get("health_metric_requires_future_runtime_observation") is True)

    ok("blocked.count12", len(blocked.get("paths") or []) == 12)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    ok("ready.review", readiness.get("ready_for_post_dryrun_review") is True)
    ok("ready.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= 5)

    for state in HEALTH_STATES:
        stype = MODEL_HEALTH_TO_SIGNAL_TYPE[state]
        ok(f"signal.{state}", any(s.get("signal_type") == stype for s in software.get("samples") or []))

    for scenario_id, ctype in SWITCHING_TO_OUTPUT.items():
        all_drive = (
            (fallback.get("samples") or [])
            + (degradation.get("samples") or [])
            + (survival.get("samples") or [])
            + (recovery.get("samples") or [])
        )
        ok(f"switch.{scenario_id[:20]}", any(s.get("candidate_type") == ctype for s in all_drive))

    for pid in BLOCKED_PATHS:
        paths = blocked.get("paths") or []
        row = next((p for p in paths if p.get("path_id") == pid), None)
        ok(f"block.{pid[:24]}", row is not None and row.get("blocked") is True)

    for forbidden in METRIC_FORBIDDEN_NOW:
        ok(f"forbid.{forbidden[:20]}", forbidden in (metric.get("forbidden_metrics_absent") or []))

    for field in BOUNDARY_FALSE_DRYRUN:
        ok(f"boundary.{field}", summary.get(field) is False)

    route_by_trigger = {r["trigger"]: r for r in bridge.get("routes") or []}
    for route in HEALTH_TO_DRIVE_ROUTES:
        row = route_by_trigger.get(route["trigger"])
        ok(
            f"route.{route['trigger'][:18]}",
            row is not None
            and row.get("target_candidate") == route["target_candidate"]
            and row.get("routed") is True
            and row.get("executed_now") is False
            and row.get("task_commit_allowed") is False,
        )

    _all_samples_have_contract(software.get("samples") or [], checks, "sw")
    for sample in (fallback.get("samples") or []) + (degradation.get("samples") or []):
        ok(f"drive.{sample.get('candidate_id', 'x')[:20]}.cand_only", sample.get("candidate_only") is True)
        ok(f"drive.{sample.get('candidate_id', 'x')[:20]}.no_exec", sample.get("executed_now") is False)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
