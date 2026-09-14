#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post-Health Management Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.health_management_layer_integration_planning_v1 import (
    HEALTH_METRIC_DEFINITION_STATUS,
)
from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL,
    PREFERRED_ROUTE,
)
from capabilities.governance.post_health_management_roadmap_decision_v1 import (
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_B,
    DEFERRED_ROUTE_C,
    DEFERRED_ROUTE_D,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROUTE_A,
    SCOPE,
    SELECTED_ROUTE,
)

MIN_CHECKS = 50

REQUIRED = (
    "post_health_roadmap_decision_policy_v1.json",
    "health_post_review_input_review_v1.json",
    "route_a_vision_ocr_voice_controlled_optimization_assessment_v1.json",
    "route_b_health_metric_baseline_defer_assessment_v1.json",
    "route_c_hardware_lifespan_alert_defer_assessment_v1.json",
    "route_d_robustness_baseline_defer_assessment_v1.json",
    "post_health_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_health_metric_hardware_robustness_register_v1.json",
    "next_phase_readiness_decision_v1.json",
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
            "post_health_management_roadmap_decision"
        ),
    )
    p.add_argument(
        "--health-management-layer-integration-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "health_management_layer_integration_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.health_management_layer_integration_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "post_health_roadmap_decision_policy_v1.json")
    input_review = _load(root / "health_post_review_input_review_v1.json")
    route_a = _load(root / "route_a_vision_ocr_voice_controlled_optimization_assessment_v1.json")
    route_b = _load(root / "route_b_health_metric_baseline_defer_assessment_v1.json")
    route_c = _load(root / "route_c_hardware_lifespan_alert_defer_assessment_v1.json")
    route_d = _load(root / "route_d_robustness_baseline_defer_assessment_v1.json")
    matrix = _load(root / "post_health_route_selection_matrix_v1.json")
    preconditions = _load(root / "selected_route_preconditions_v1.json")
    deferred = _load(root / "deferred_health_metric_hardware_robustness_register_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")

    post_sm = _load(post_root / "summary.json")
    post_vr = _load(post_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.defer_b", summary.get("deferred_route_b") == DEFERRED_ROUTE_B)
    ok("summary.metric_reserved", summary.get("health_metric_definition_status") == HEALTH_METRIC_DEFINITION_STATUS)
    ok("summary.defer_metric", summary.get("defer_health_metric_baseline_planning") is True)
    ok("summary.preferred", summary.get("preferred_route") == PREFERRED_ROUTE)

    ok("policy.decision_only", policy.get("post_health_management_roadmap_decision_only") is True)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.closed", input_review.get("health_management_integration_dryrun_closed") is True)
    ok("input.consumable", input_review.get("health_signal_and_drive_candidates_consumable") is True)

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_a.no_real", route_a.get("does_not_enable_real_model_or_provider") is True)
    ok("route_b.deferred", route_b.get("status") == "deferred_until_hardware_ready")
    ok("route_c.deferred", route_c.get("status") == "deferred_until_hardware_layer_ready")
    ok("route_d.deferred", route_d.get("status") == "deferred_until_runtime_observation_ready")

    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    ok("precond.route", preconditions.get("selected_route") == SELECTED_ROUTE)
    ok("deferred.metric", deferred.get("health_metric_definition_status") == HEALTH_METRIC_DEFINITION_STATUS)
    ok("next.ready", next_phase.get("ready_for_vision_ocr_voice_controlled_optimization_planning") is True)
    ok("next.planning_only", next_phase.get("planning_only_no_runtime") is True)

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.final", post_sm.get("final_decision") == POST_REVIEW_FINAL)

    for field in BOUNDARY_FALSE:
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
