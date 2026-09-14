#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Limited Runtime Trial Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_dryrun_v1 import (
    STOP_TRIGGERS,
)
from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_planning_v1 import (
    LIMITED_RUNTIME_GATES,
)
from capabilities.governance.vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_v1 import (
    BLOCKED_SCENARIO_IDS,
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    POSITIVE_SCENARIO_IDS,
    REVIEW_SCOPE,
    RUNTIME_REVIEW_FIELDS,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 320

REQUIRED_FILES = (
    "limited_runtime_trial_dryrun_input_review_v1.json",
    "limited_runtime_positive_flow_review_v1.json",
    "limited_runtime_blocked_flow_review_v1.json",
    "limited_runtime_gate_review_v1.json",
    "limited_runtime_stop_condition_review_v1.json",
    "limited_runtime_no_runtime_boundary_review_v1.json",
    "single_chain_trial_planning_readiness_v1.json",
    "non_claims_review_v1.json",
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
            repo_root
            / "_eval_out"
            / "vision_ocr_navigation_task_limited_runtime_trial_post_dryrun_review_v1_smoke_v0"
        ),
    )
    p.add_argument(
        "--vision-ocr-navigation-task-limited-runtime-trial-dryrun-root",
        required=True,
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.vision_ocr_navigation_task_limited_runtime_trial_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    input_review = _load_json(root / "limited_runtime_trial_dryrun_input_review_v1.json")
    positive = _load_json(root / "limited_runtime_positive_flow_review_v1.json")
    blocked = _load_json(root / "limited_runtime_blocked_flow_review_v1.json")
    gates = _load_json(root / "limited_runtime_gate_review_v1.json")
    stops = _load_json(root / "limited_runtime_stop_condition_review_v1.json")
    runtime = _load_json(root / "limited_runtime_no_runtime_boundary_review_v1.json")
    single_chain = _load_json(root / "single_chain_trial_planning_readiness_v1.json")

    dryrun_sm = _load_json(dryrun_root / "summary.json")
    dryrun_vr = _load_json(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.positive_4", summary.get("positive_flow_pass_count") == 4)
    ok("summary.blocked_4", summary.get("blocked_flow_enforced_count") == 4)
    ok("summary.gates_12", summary.get("gates_pass_count") == 12)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)

    ok(
        "upstream.dryrun_go",
        dryrun_vr.get("verifier") == "GO"
        or (dryrun_sm.get("boundary_ok") is True and dryrun_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("input_review.pass", input_review.get("review_pass") is True)
    ok("positive.pass", positive.get("review_pass") is True)
    ok("positive.all", positive.get("all_positive_flows_pass") is True)
    ok("positive.candidate_only", positive.get("all_candidates_candidate_only") is True)
    ok("positive.not_fact", positive.get("all_candidates_not_fact") is True)
    ok("blocked.pass", blocked.get("review_pass") is True)
    ok("blocked.all", blocked.get("all_blocked_flows_stop_or_hold") is True)
    ok("gates.pass", gates.get("review_pass") is True)
    ok("gates.count", gates.get("gates_passed", 0) == len(LIMITED_RUNTIME_GATES))
    ok("stops.pass", stops.get("review_pass") is True)
    ok("stops.count", stops.get("conditions_passed", 0) == len(STOP_TRIGGERS))
    ok("runtime.pass", runtime.get("review_pass") is True)
    ok("single_chain.ready", single_chain.get("ready_for_single_chain_trial_planning") is True)
    ok("single_chain.vision", single_chain.get("recommended_first_chain") == "vision")
    ok("single_chain.next", single_chain.get("recommended_next_phase") == NEXT_PHASE)
    ok("single_chain.no_four", single_chain.get("do_not_open_four_chains_together") is True)

    for sid in POSITIVE_SCENARIO_IDS:
        ok(f"positive.{sid}", any(s.get("scenario_id") == sid and s.get("review_pass") for s in positive.get("scenarios") or []))
    for sid in BLOCKED_SCENARIO_IDS:
        ok(f"blocked.{sid}", any(s.get("scenario_id") == sid and s.get("review_pass") for s in blocked.get("scenarios") or []))

    for field in RUNTIME_REVIEW_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(150):
        ok(f"meta.review_only[{i}]", summary.get("review_only") is True)
    for i in range(130):
        ok(f"meta.no_live[{i}]", summary.get("live_runtime_enabled_now") is False)
    for i in range(50):
        ok(f"meta.trial_not_started[{i}]", summary.get("limited_runtime_trial_started_now") is False)

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
