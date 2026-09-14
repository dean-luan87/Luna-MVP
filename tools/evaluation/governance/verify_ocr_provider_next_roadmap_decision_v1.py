#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Next Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_v1 import (
    FINAL_DECISION_GO as HARNESS_FINAL,
    HARNESS_ID,
    NEXT_PHASE_GO as HARNESS_NEXT,
)
from capabilities.governance.ocr_provider_next_roadmap_decision_v1 import (
    BLOCKED_ROUTE_C,
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_A,
    DEFERRED_ROUTE_D,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REQUIRED_FUTURE_DOMAINS,
    ROUTE_B,
    SCOPE,
    SELECTED_ROUTE,
)

MIN_CHECKS = 61

REQUIRED = (
    "ocr_provider_next_roadmap_decision_policy_v1.json",
    "controlled_provider_readiness_harness_input_review_v1.json",
    "route_a_continue_ocr_authorization_assessment_v1.json",
    "route_b_vision_voice_harness_adoption_assessment_v1.json",
    "route_c_ocr_real_dependency_authorization_assessment_v1.json",
    "route_d_pause_provider_return_midplatform_assessment_v1.json",
    "ocr_provider_next_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_routes_register_v1.json",
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
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_next_roadmap_decision",
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    harness_root = Path(args.controlled_provider_readiness_harness_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "controlled_provider_readiness_harness_input_review_v1.json")
    route_a = _load(root / "route_a_continue_ocr_authorization_assessment_v1.json")
    route_b = _load(root / "route_b_vision_voice_harness_adoption_assessment_v1.json")
    route_c = _load(root / "route_c_ocr_real_dependency_authorization_assessment_v1.json")
    route_d = _load(root / "route_d_pause_provider_return_midplatform_assessment_v1.json")
    matrix = _load(root / "ocr_provider_next_route_selection_matrix_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")

    harness_vr = _load(harness_root / "verifier_report.json")
    harness_sm = _load(harness_root / "summary.json")
    future_plan = _load(harness_root / "future_consumer_adoption_plan_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.decision_only", summary.get("ocr_provider_next_roadmap_decision_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.harness_go", input_review.get("upstream_verifier_go") is True)
    ok("input.ocr_validated", input_review.get("ocr_first_consumer_validated") is True)
    ok("input.anti_recursion", input_review.get("anti_recursion_active") is True)

    ok("upstream.harness_go", harness_vr.get("verifier") == "GO")
    ok("upstream.harness_final", harness_sm.get("final_decision") == HARNESS_FINAL)
    ok("upstream.harness_next", harness_sm.get("recommended_next_phase") == HARNESS_NEXT)
    ok("upstream.harness_id", harness_sm.get("harness_id") == HARNESS_ID)

    domains = {c.get("domain") for c in (future_plan.get("consumers") or [])}
    for d in REQUIRED_FUTURE_DOMAINS:
        ok(f"future.{d}", d in domains)

    ok("route_a.deferred", route_a.get("status") == "deferred")
    ok("route_b.selected", route_b.get("status") == "selected")
    ok("route_c.blocked", route_c.get("status") == "blocked_until_explicit_authorization")
    ok("route_d.deferred", route_d.get("status") == "deferred")
    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)

    ok("next.ready", next_phase.get("ready_for_vision_voice_provider_harness_adoption_planning") is True)
    ok("next.no_ocr_auth", next_phase.get("do_not_start_ocr_authorization_now") is True)
    ok("next.no_real_dep", next_phase.get("do_not_start_real_dependency_check_now") is True)
    ok("next.no_vision_voice", next_phase.get("do_not_enable_vision_voice_provider_now") is True)

    ok("summary.defer_a", summary.get("deferred_route_a") == DEFERRED_ROUTE_A)
    ok("summary.block_c", summary.get("blocked_route_c") == BLOCKED_ROUTE_C)
    ok("summary.defer_d", summary.get("deferred_route_d") == DEFERRED_ROUTE_D)

    ok("summary.no_auth", summary.get("ocr_authorization_started_now") is False)
    ok("summary.no_harness_adopt", summary.get("vision_harness_adoption_started_now") is False)

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
