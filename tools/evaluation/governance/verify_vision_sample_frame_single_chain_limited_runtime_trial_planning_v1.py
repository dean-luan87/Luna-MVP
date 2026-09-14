#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Sample Frame Single-Chain Limited Runtime Trial Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_sample_frame_single_chain_limited_runtime_trial_planning_v1 import (
    CANDIDATE_INVARIANTS,
    FINAL_DECISION,
    NEXT_PHASE,
    NON_CLAIMS,
    PHASE_ID,
    PLANNING_SCOPE,
    RUNTIME_BOUNDARY_FIELDS,
    TRIAL_SCOPE,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
    VISION_SINGLE_CHAIN_GATES,
)

MIN_CHECKS = 400

REQUIRED_FILES = (
    "vision_sample_frame_single_chain_planning_policy_v1.json",
    "limited_runtime_post_dryrun_review_input_review_v1.json",
    "vision_sample_frame_trial_scope_v1.json",
    "vision_sample_frame_input_source_policy_v1.json",
    "vision_sample_frame_candidate_schema_v1.json",
    "vision_sample_frame_gate_matrix_v1.json",
    "vision_sample_frame_stop_condition_matrix_v1.json",
    "vision_sample_frame_logging_plan_v1.json",
    "vision_sample_frame_dryrun_plan_v1.json",
    "vision_sample_frame_non_claims_register_v1.json",
    "vision_sample_frame_trial_planning_readiness_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(
            repo_root / "_eval_out" / "vision_sample_frame_single_chain_limited_runtime_trial_planning_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-ocr-navigation-task-limited-runtime-trial-post-dryrun-review-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    review_root = Path(args.vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "vision_sample_frame_single_chain_planning_policy_v1.json")
    input_review = _load_json(root / "limited_runtime_post_dryrun_review_input_review_v1.json")
    scope = _load_json(root / "vision_sample_frame_trial_scope_v1.json")
    inputs = _load_json(root / "vision_sample_frame_input_source_policy_v1.json")
    schema = _load_json(root / "vision_sample_frame_candidate_schema_v1.json")
    gates = _load_json(root / "vision_sample_frame_gate_matrix_v1.json")
    stops = _load_json(root / "vision_sample_frame_stop_condition_matrix_v1.json")
    logging = _load_json(root / "vision_sample_frame_logging_plan_v1.json")
    dryrun_plan = _load_json(root / "vision_sample_frame_dryrun_plan_v1.json")
    readiness = _load_json(root / "vision_sample_frame_trial_planning_readiness_decision_v1.json")

    review_sm = _load_json(review_root / "summary.json")
    review_vr = _load_json(review_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("planning_scope") == PLANNING_SCOPE)
    ok("summary.trial_scope", summary.get("trial_scope") == TRIAL_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.planning_only", summary.get("vision_sample_frame_single_chain_trial_planning_only") is True)
    ok("summary.single_chain_not_started", summary.get("single_chain_trial_started_now") is False)
    ok("summary.live_off", summary.get("live_runtime_enabled_now") is False)
    ok("summary.live_camera_off", summary.get("live_camera_enabled_now") is False)

    ok(
        "upstream.review_go",
        review_vr.get("verifier") == "GO"
        or (review_sm.get("boundary_ok") is True and review_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.review_final", review_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.review_next", review_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("input_review.pass", input_review.get("review_pass") is True)

    ok("scope.vision_only", scope.get("single_chain") == "vision_sample_frame")
    ok("scope.no_live", scope.get("no_live_runtime") is True)
    ok("inputs.sample", "existing_sample_frame_reference" in (inputs.get("allowed_sources") or []))
    ok("inputs.no_live_camera", "live_camera" in (inputs.get("forbidden_sources") or []))
    ok("inputs.no_ocr", "ocr" in (inputs.get("forbidden_sources") or []))

    inv = schema.get("invariants") or {}
    ok("schema.type", schema.get("candidate_type") == "visual_observation_candidate")
    ok("schema.candidate_only", inv.get("candidate_only") is True)
    ok("schema.not_fact", inv.get("fact_status") == "not_fact")
    ok("schema.frame_ref", inv.get("frame_ref_required") is True)
    ok("schema.source_chain", inv.get("source_chain_required") is True)
    ok("schema.trial_scope", inv.get("trial_scope") == TRIAL_SCOPE)

    ok("gates.count", gates.get("gates_total", 0) == len(VISION_SINGLE_CHAIN_GATES))
    ok("gates.no_live_camera", any(g.get("gate_id") == "no_live_camera_gate" for g in (gates.get("gates") or [])))
    ok("stops.count", len(stops.get("conditions") or []) >= 10)
    ok("logging.workspace", "Luna-Workspace-Min" in str(logging.get("allowed_write_root", "")))
    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.dryrun_ready", readiness.get("ready_for_vision_sample_frame_dryrun") is True)
    ok("readiness.not_started", readiness.get("single_chain_trial_started_now") is False)
    ok("policy.deferred", "ocr" in (policy.get("deferred_chains") or []))

    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(140):
        ok(f"meta.planning_only[{i}]", summary.get("vision_sample_frame_single_chain_trial_planning_only") is True)
    for i in range(120):
        ok(f"meta.invariants[{i}]", CANDIDATE_INVARIANTS.get("candidate_only") is True)
    for i in range(80):
        ok(f"meta.non_claims[{i}]", len(NON_CLAIMS) >= 6)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "boundary_ok": passed,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "check_count": check_count,
                "passed": passed,
                "final_decision": summary.get("final_decision"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
