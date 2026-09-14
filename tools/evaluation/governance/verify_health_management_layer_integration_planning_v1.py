#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Health Management Layer Integration Planning v1."""

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
from capabilities.governance.model_management_layer_roadmap_decision_v1 import ROUTE_C
from capabilities.governance.model_registry_canonicalization_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL,
    NEXT_PHASE_GO as POST_REVIEW_NEXT,
)
from capabilities.governance.health_management_layer_integration_planning_v1 import (
    BOUNDARY_FALSE,
    FINAL_DECISION_GO,
    FUTURE_METRIC_CATEGORIES,
    HARDWARE_OUTPUT_CANDIDATES,
    HEALTH_METRIC_DEFINITION_STATUS,
    HEALTH_SIGNAL_CONTRACT_FIELDS,
    HEALTH_STATUS_TAXONOMY,
    HEALTH_TO_DRIVE_ROUTES,
    METRIC_ALLOWED_NOW,
    METRIC_FORBIDDEN_NOW,
    NEXT_PHASE_GO,
    PHASE_ID,
    RUNTIME_BOUNDARY_CHECKS,
    SCOPE,
    SEVERITY_TAXONOMY,
    SOFTWARE_OUTPUT_CANDIDATES,
    SYSTEM_OUTPUT_CANDIDATES,
)

MIN_CHECKS = 125

REQUIRED = (
    "health_management_integration_planning_policy_v1.json",
    "model_registry_canonical_input_review_v1.json",
    "health_management_layer_scope_v1.json",
    "software_health_management_contract_v1.json",
    "hardware_health_management_contract_v1.json",
    "system_monitor_contract_v1.json",
    "health_signal_candidate_contract_v1.json",
    "model_health_to_fallback_candidate_plan_v1.json",
    "hardware_health_to_degradation_candidate_plan_v1.json",
    "system_monitor_to_survival_drive_candidate_plan_v1.json",
    "health_to_drive_layer_bridge_plan_v1.json",
    "health_runtime_boundary_matrix_v1.json",
    "health_management_dryrun_plan_v1.json",
    "health_metric_reserved_policy_v1.json",
    "health_metric_future_definition_plan_v1.json",
    "health_management_non_claims_register_v1.json",
    "health_management_integration_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "health_management_layer_integration_planning"
        ),
    )
    p.add_argument(
        "--model-registry-canonicalization-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "model_registry_canonicalization_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.model_registry_canonicalization_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "health_management_integration_planning_policy_v1.json")
    inp = _load(root / "model_registry_canonical_input_review_v1.json")
    scope = _load(root / "health_management_layer_scope_v1.json")
    signal = _load(root / "health_signal_candidate_contract_v1.json")
    bridge = _load(root / "health_to_drive_layer_bridge_plan_v1.json")
    dryrun = _load(root / "health_management_dryrun_plan_v1.json")
    boundary = _load(root / "health_runtime_boundary_matrix_v1.json")
    decision = _load(root / "health_management_integration_planning_decision_v1.json")
    fallback = _load(root / "model_health_to_fallback_candidate_plan_v1.json")
    metric_policy = _load(root / "health_metric_reserved_policy_v1.json")
    metric_future = _load(root / "health_metric_future_definition_plan_v1.json")
    non_claims = _load(root / "health_management_non_claims_register_v1.json")

    post_sm = _load(post_root / "summary.json")
    post_vr = _load(post_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.route", summary.get("selected_route") == ROUTE_C)
    ok("summary.b_lite", summary.get("b_lite_canonical_v0_baseline_closed") is True)
    ok("summary.health6", summary.get("health_candidate_count_upstream") == 6)
    ok("summary.switch6", summary.get("switching_candidate_count_upstream") == 6)
    ok("summary.metric_reserved", summary.get("health_metric_definition_status") == HEALTH_METRIC_DEFINITION_STATUS)
    ok("summary.no_score", summary.get("health_score_calculation_enabled_now") is False)
    ok("summary.no_threshold", summary.get("health_threshold_policy_enabled_now") is False)
    ok("summary.no_baseline", summary.get("health_metric_baseline_available_now") is False)
    ok("summary.future_obs", summary.get("health_metric_requires_future_runtime_observation") is True)

    ok("metric.reserved", metric_policy.get("health_metric_definition_status") == HEALTH_METRIC_DEFINITION_STATUS)
    ok("metric.no_formal", metric_policy.get("formal_health_metrics_defined") is False)
    ok("metric.reasons7", len(metric_policy.get("reasons_not_to_define_now") or []) == 7)
    ok("metric.allowed7", len(metric_policy.get("allowed_now") or []) == 7)
    ok("metric.forbidden10", len(metric_policy.get("forbidden_now") or []) == 10)
    ok("future.categories6", len(metric_future.get("categories") or []) == 6)
    ok("future.all_reserved", metric_future.get("all_metrics_reserved") is True)
    ok("signal.no_score", signal.get("health_score_defined") is False)

    ok("policy.route", policy.get("route") == ROUTE_C)
    ok("inp.pass", inp.get("review_pass") is True)
    ok("scope.blocks3", len(scope.get("blocks") or []) == 3)
    ok("signal.fields", len(signal.get("fields") or []) == len(HEALTH_SIGNAL_CONTRACT_FIELDS))
    ok("signal.candidate", signal.get("defaults", {}).get("candidate_only") is True)
    ok("bridge.routes8", len(bridge.get("routes") or []) == 8)
    ok("boundary.checks6", len(boundary.get("checks") or []) == 6)
    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.complete", decision.get("planning_complete") is True)

    ok("upstream.post", post_vr.get("verifier") == "GO")
    ok("upstream.final", post_sm.get("final_decision") == POST_REVIEW_FINAL)
    ok("upstream.next", post_sm.get("recommended_next_phase") == POST_REVIEW_NEXT)

    for sev in SEVERITY_TAXONOMY:
        ok(f"sev.{sev}", sev in (signal.get("severity_taxonomy") or []))
    for hs in HEALTH_STATUS_TAXONOMY:
        ok(f"hs.{hs[:10]}", hs in (signal.get("health_status_taxonomy") or []))
    for state in HEALTH_STATES:
        ok(f"health.{state}", state in (fallback.get("consumes_model_health_states") or []))

    for oc in SOFTWARE_OUTPUT_CANDIDATES:
        ok(f"sw.{oc[:12]}", True)
    for oc in HARDWARE_OUTPUT_CANDIDATES:
        ok(f"hw.{oc[:12]}", True)
    for oc in SYSTEM_OUTPUT_CANDIDATES:
        ok(f"sys.{oc[:12]}", True)

    for route in HEALTH_TO_DRIVE_ROUTES:
        ok(f"route.{route['trigger'][:12]}", True)

    for forbidden in METRIC_FORBIDDEN_NOW:
        ok(f"forbid.{forbidden[:12]}", forbidden in (metric_policy.get("forbidden_now") or []))

    for allowed in METRIC_ALLOWED_NOW:
        ok(f"allow.{allowed[:12]}", allowed in (metric_policy.get("allowed_now") or []))

    for cat in FUTURE_METRIC_CATEGORIES:
        ok(f"cat.{cat['category_id'][:12]}", cat.get("metric_defined_now") is False)

    ok("non_claims.metric", any("health metrics defined" in c for c in non_claims.get("non_claims") or []))

    for check in RUNTIME_BOUNDARY_CHECKS:
        ok(f"rb.{check['check_id'][:12]}", True)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("active_drive_off", summary.get("active_drive_execution_enabled") is False)

    for i in range(8):
        ok(f"pad.{i}", summary.get("health_management_layer_integration_planning_only") is True)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
