#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify First Person Vision Navigation Candidate Flow DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.first_person_vision_navigation_candidate_flow_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DRYRUN_NON_CLAIMS,
    FINAL_DECISION_GO,
    II_HANDOFF_CONFIRMATIONS,
    MAP_LOCATION_FIELDS,
    NAVIGATION_TASK_FIELDS,
    NEXT_PHASE_GO,
    OCR_RESULT_FIELDS,
    PERCEPTION_ZONE_CONFIRMATIONS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
    VISUAL_OBSERVATION_FIELDS,
    VISUAL_OCR_MAP_BINDING_CONFIRMATIONS,
)
from capabilities.governance.first_person_vision_navigation_candidate_flow_planning_v1 import (
    DRIVE_OBSERVATION_PRIORITY_CONFIRMATIONS,
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)

MIN_CHECKS = 185

REQUIRED = (
    "first_person_vision_navigation_candidate_flow_dryrun_review_policy_v1.json",
    "candidate_flow_planning_input_review_v1.json",
    "sample_visual_observation_candidate_v1.json",
    "sample_ocr_result_candidate_v1.json",
    "sample_map_location_context_candidate_v1.json",
    "sample_route_context_candidate_v1.json",
    "sample_navigation_task_candidate_v1.json",
    "perception_zone_candidate_flow_review_v1.json",
    "visual_ocr_map_binding_review_v1.json",
    "drive_observation_priority_review_v1.json",
    "information_integration_handoff_review_v1.json",
    "candidate_not_fact_review_v1.json",
    "candidate_flow_boundary_audit_v1.json",
    "candidate_flow_blocked_path_result_v1.json",
    "candidate_flow_closure_decision_v1.json",
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
            "first_person_vision_navigation_candidate_flow_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_vision_navigation_candidate_flow_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.plan_final_expected", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok("upstream.plan_next_expected", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)

    summary = _load(root / "summary.json")
    policy = _load(root / "first_person_vision_navigation_candidate_flow_dryrun_review_policy_v1.json")
    input_review = _load(root / "candidate_flow_planning_input_review_v1.json")
    visual = _load(root / "sample_visual_observation_candidate_v1.json")
    ocr = _load(root / "sample_ocr_result_candidate_v1.json")
    map_loc = _load(root / "sample_map_location_context_candidate_v1.json")
    route = _load(root / "sample_route_context_candidate_v1.json")
    nav = _load(root / "sample_navigation_task_candidate_v1.json")
    perception = _load(root / "perception_zone_candidate_flow_review_v1.json")
    binding = _load(root / "visual_ocr_map_binding_review_v1.json")
    drive = _load(root / "drive_observation_priority_review_v1.json")
    handoff = _load(root / "information_integration_handoff_review_v1.json")
    not_fact = _load(root / "candidate_not_fact_review_v1.json")
    boundary = _load(root / "candidate_flow_boundary_audit_v1.json")
    blocked = _load(root / "candidate_flow_blocked_path_result_v1.json")
    closure = _load(root / "candidate_flow_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_runtime", policy.get("dryrun_not_runtime_not_execute") is True)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.plan_go", input_review.get("planning_verifier") == "GO")

    for field in VISUAL_OBSERVATION_FIELDS:
        ok(f"visual.{field[:18]}", field in visual)
    ok("visual.candidate", visual.get("candidate_only") is True)
    ok("visual.runtime_false", visual.get("runtime_source") is False)

    for field in OCR_RESULT_FIELDS:
        ok(f"ocr.{field[:18]}", field in ocr)
    ok("ocr.candidate", ocr.get("candidate_only") is True)

    for field in MAP_LOCATION_FIELDS:
        ok(f"map.{field[:18]}", field in map_loc)

    ok("route.candidate", route.get("candidate_only") is True)

    for field in NAVIGATION_TASK_FIELDS:
        ok(f"nav.{field[:18]}", field in nav)
    ok("nav.no_commit", nav.get("task_state_commit_allowed") is False)

    ok("perception.review_pass", perception.get("dryrun_and_review_pass") is True)
    for conf in PERCEPTION_ZONE_CONFIRMATIONS:
        ok(f"perception.{conf[:18]}", conf in (perception.get("confirmations") or []))

    ok("binding.review_pass", binding.get("dryrun_and_review_pass") is True)
    for conf in VISUAL_OCR_MAP_BINDING_CONFIRMATIONS:
        ok(f"binding.{conf[:18]}", conf in (binding.get("confirmations") or []))

    ok("drive.review_pass", drive.get("dryrun_and_review_pass") is True)
    ok("drive.no_runtime", drive.get("drive_invoked_runtime") is False)
    for conf in DRIVE_OBSERVATION_PRIORITY_CONFIRMATIONS:
        ok(f"drive.{conf[:18]}", conf in (drive.get("confirmations") or []))

    ok("handoff.review_pass", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.no_decision", handoff.get("decision_candidate_generated") is False)
    for conf in II_HANDOFF_CONFIRMATIONS:
        ok(f"handoff.{conf[:18]}", conf in (handoff.get("confirmations") or []))

    ok("not_fact.review_pass", not_fact.get("dryrun_and_review_pass") is True)
    ok("not_fact.all_candidate", not_fact.get("all_samples_candidate_only") is True)
    ok("not_fact.no_output", not_fact.get("no_user_output") is True)

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count15", blocked.get("blocked_count") == 15)
    for path in BLOCKED_PATHS:
        ok(f"blocked.{path[:18]}", any(
            b.get("path_id") == path and b.get("status") == "blocked"
            for b in (blocked.get("blocked_paths") or [])
        ))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_vision_navigation_integration_chain_dryrun") is True)
    ok("next_route.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

    for claim in DRYRUN_NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    min_checks = MIN_CHECKS if MIN_CHECKS else total
    verifier = "GO" if passed == total and passed >= min_checks else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": min_checks,
        "dryrun_and_review_pass": summary.get("dryrun_and_review_pass"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
