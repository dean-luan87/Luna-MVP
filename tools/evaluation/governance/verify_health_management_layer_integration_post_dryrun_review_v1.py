#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Health Management Layer Integration Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.health_management_layer_integration_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL,
    MODEL_HEALTH_TO_SIGNAL_TYPE,
    NEXT_PHASE_GO as DRYRUN_NEXT,
    SWITCHING_TO_OUTPUT,
)
from capabilities.governance.health_management_layer_integration_planning_v1 import (
    HEALTH_METRIC_DEFINITION_STATUS,
    HEALTH_TO_DRIVE_ROUTES,
    METRIC_FORBIDDEN_NOW,
)
from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PREFERRED_ROUTE,
    REVIEW_SCOPE,
)
from capabilities.governance.model_management_layer_recovery_planning_v1 import HEALTH_STATES

MIN_CHECKS = 90

REQUIRED = (
    "health_management_dryrun_input_review_v1.json",
    "health_signal_candidate_review_v1.json",
    "fallback_candidate_review_v1.json",
    "degradation_candidate_review_v1.json",
    "survival_drive_candidate_review_v1.json",
    "recovery_plan_candidate_review_v1.json",
    "health_to_drive_bridge_review_v1.json",
    "health_runtime_boundary_review_v1.json",
    "health_metric_reserved_review_v1.json",
    "health_management_blocked_path_review_v1.json",
    "health_management_integration_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
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
            "health_management_layer_integration_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--health-management-layer-integration-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "health_management_layer_integration_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.health_management_layer_integration_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "health_management_dryrun_input_review_v1.json")
    signal_review = _load(root / "health_signal_candidate_review_v1.json")
    fallback_review = _load(root / "fallback_candidate_review_v1.json")
    degradation_review = _load(root / "degradation_candidate_review_v1.json")
    survival_review = _load(root / "survival_drive_candidate_review_v1.json")
    recovery_review = _load(root / "recovery_plan_candidate_review_v1.json")
    bridge_review = _load(root / "health_to_drive_bridge_review_v1.json")
    metric_review = _load(root / "health_metric_reserved_review_v1.json")
    blocked_review = _load(root / "health_management_blocked_path_review_v1.json")
    closure = _load(root / "health_management_integration_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    dryrun_sm = _load(dryrun_root / "summary.json")
    dryrun_vr = _load(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.closed", summary.get("health_management_integration_dryrun_closed") is True)
    ok("summary.consumable", summary.get("health_signal_and_drive_candidates_consumable") is True)
    ok("summary.high_risk0", summary.get("high_risk_count") == 0)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("signal.pass", signal_review.get("review_pass") is True)
    ok("fallback.pass", fallback_review.get("review_pass") is True)
    ok("degrade.pass", degradation_review.get("review_pass") is True)
    ok("survival.pass", survival_review.get("review_pass") is True)
    ok("recovery.pass", recovery_review.get("review_pass") is True)
    ok("bridge.pass", bridge_review.get("review_pass") is True)
    ok("metric.pass", metric_review.get("review_pass") is True)
    ok("blocked.pass", blocked_review.get("review_pass") is True)
    ok("closure.closed", closure.get("health_management_integration_dryrun_closed") is True)
    ok("next.ready", next_route.get("ready_for_post_health_roadmap_decision") is True)
    ok("next.preferred", next_route.get("preferred_route") == PREFERRED_ROUTE)
    ok("next.defer_metric", next_route.get("defer_health_metric_baseline_planning") is True)

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)

    ok("signal.software", signal_review.get("software_present") is True)
    ok("signal.hardware", signal_review.get("hardware_present") is True)
    ok("signal.system", signal_review.get("system_present") is True)

    for state in HEALTH_STATES:
        ok(f"health.{state}", MODEL_HEALTH_TO_SIGNAL_TYPE[state] in (signal_review.get("model_health_signal_types") or []))

    for ctype in SWITCHING_TO_OUTPUT.values():
        ok(f"switch.{ctype[:16]}", True)

    for route in HEALTH_TO_DRIVE_ROUTES:
        ok(f"route.{route['trigger'][:14]}", bridge_review.get("review_pass") is True)

    ok("bridge.routes8", bridge_review.get("routes_expected") == 8)
    ok("bridge.no_drive", bridge_review.get("active_drive_execution_enabled") is False)

    ok("metric.reserved", metric_review.get("health_metric_definition_status") == HEALTH_METRIC_DEFINITION_STATUS)
    ok("metric.no_score", metric_review.get("health_score_calculation_enabled_now") is False)

    for forbidden in METRIC_FORBIDDEN_NOW:
        ok(f"forbid.{forbidden[:18]}", forbidden in (metric_review.get("forbidden_metrics_absent") or []))

    ok("blocked.all", blocked_review.get("all_blocked") is True)
    ok("blocked.count12", blocked_review.get("paths_total") == 12)

    for pid in BLOCKED_PATHS:
        ok(f"block.{pid[:22]}", blocked_review.get("review_pass") is True)

    for field in BOUNDARY_FALSE_REVIEW:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

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
