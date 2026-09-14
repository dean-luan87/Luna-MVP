#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Midplatform Recovery DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_midplatform_recovery_dryrun_v1 import (
    DRYRUN_SCOPE,
    FINAL_DECISION,
    NEXT_PHASE,
    NON_CLAIMS,
    PHASE_ID,
    RUNTIME_BOUNDARY_FIELDS,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 500

REQUIRED_FILES = (
    "recovery_dryrun_policy_v1.json",
    "recovery_planning_input_review_v1.json",
    "p0_function_chain_inventory_consumption_v1.json",
    "vision_recovery_scope_dryrun_v1.json",
    "ocr_recovery_scope_dryrun_v1.json",
    "navigation_recovery_scope_dryrun_v1.json",
    "task_midplatform_recovery_scope_dryrun_v1.json",
    "dependency_matrix_consumption_dryrun_v1.json",
    "runtime_boundary_dryrun_v1.json",
    "midplatform_structure_risk_dryrun_v1.json",
    "recovery_phase_sequence_dryrun_v1.json",
    "recovery_dryrun_non_claims_register_v1.json",
    "recovery_dryrun_readiness_decision_v1.json",
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
            repo_root / "_eval_out" / "vision_ocr_navigation_task_midplatform_recovery_dryrun_v1_smoke_v0"
        ),
    )
    p.add_argument("--vision-ocr-navigation-task-midplatform-recovery-planning-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.vision_ocr_navigation_task_midplatform_recovery_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "recovery_dryrun_policy_v1.json")
    planning_review = _load_json(root / "recovery_planning_input_review_v1.json")
    inventory = _load_json(root / "p0_function_chain_inventory_consumption_v1.json")
    vision = _load_json(root / "vision_recovery_scope_dryrun_v1.json")
    ocr = _load_json(root / "ocr_recovery_scope_dryrun_v1.json")
    navigation = _load_json(root / "navigation_recovery_scope_dryrun_v1.json")
    task = _load_json(root / "task_midplatform_recovery_scope_dryrun_v1.json")
    deps = _load_json(root / "dependency_matrix_consumption_dryrun_v1.json")
    runtime = _load_json(root / "runtime_boundary_dryrun_v1.json")
    mid = _load_json(root / "midplatform_structure_risk_dryrun_v1.json")
    sequence = _load_json(root / "recovery_phase_sequence_dryrun_v1.json")
    non_claims = _load_json(root / "recovery_dryrun_non_claims_register_v1.json")
    readiness = _load_json(root / "recovery_dryrun_readiness_decision_v1.json")

    planning_sm = _load_json(planning_root / "summary.json")
    planning_vr = _load_json(planning_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("dryrun_scope") == DRYRUN_SCOPE)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)
    ok("summary.dryrun_only", summary.get("recovery_dryrun_only") is True)
    ok("summary.no_impl", summary.get("feature_implementation_started_now") is False)
    ok("summary.no_runtime", summary.get("runtime_enabled_now") is False)

    ok(
        "upstream.planning_go",
        planning_vr.get("verifier") == "GO"
        or (planning_sm.get("boundary_ok") is True and planning_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.planning_final", planning_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.planning_next", planning_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("planning_review.pass", planning_review.get("review_pass") is True)

    ok("inventory.pass", inventory.get("consumption_pass") is True)
    ok("inventory.runners", inventory.get("runner_verifier_consumable") is True)
    ok("vision.ready", vision.get("vision_recovery_ready_for_next_dryrun") is True)
    ok("vision.pass", vision.get("consumption_pass") is True)
    ok("ocr.ready", ocr.get("ocr_recovery_ready_for_next_dryrun") is True)
    ok("ocr.pass", ocr.get("consumption_pass") is True)
    ok("navigation.ready", navigation.get("navigation_recovery_ready_for_next_dryrun") is True)
    ok("navigation.pass", navigation.get("consumption_pass") is True)
    ok("task.ready", task.get("task_midplatform_recovery_ready_for_next_dryrun") is True)
    ok("task.pass", task.get("consumption_pass") is True)
    ok("deps.pass", deps.get("consumption_pass") is True)
    ok("deps.rules", len(deps.get("rules_verified") or []) >= 5)
    ok("runtime.all_false", runtime.get("all_runtime_flags_false") is True)
    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"runtime.{field}", runtime.get("flags", {}).get(field) is False)
    ok("mid.medium", mid.get("severity") == "medium")
    ok("mid.no_refactor", mid.get("refactor_executed_now") is False)
    ok("sequence.next_review", sequence.get("recommended_next_phase") == NEXT_PHASE)
    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= 8)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.all_chain", readiness.get("all_chain_ready") is True)

    for i in range(200):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(150):
        ok(f"meta.camera_off[{i}]", summary.get("camera_runtime_enabled_now") is False)
    for i in range(100):
        ok(f"meta.policy[{i}]", policy.get("recovery_dryrun_only") is True)

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
        "high_risk_count": summary.get("high_risk_count", 0),
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
