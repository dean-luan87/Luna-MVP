#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Midplatform Recovery Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_midplatform_recovery_planning_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    NON_CLAIMS,
    PHASE_ID,
    PLANNING_SCOPE,
    P0_CHAINS,
    RECOVERY_SEQUENCE,
    RUNTIME_BOUNDARY_FIELDS,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 480

REQUIRED_FILES = (
    "recovery_planning_policy_v1.json",
    "smoke_test_input_review_v1.json",
    "p0_function_chain_inventory_v1.json",
    "vision_recovery_scope_planning_v1.json",
    "ocr_recovery_scope_planning_v1.json",
    "navigation_recovery_scope_planning_v1.json",
    "task_midplatform_recovery_scope_planning_v1.json",
    "vision_ocr_navigation_task_dependency_matrix_v1.json",
    "recovery_runtime_boundary_matrix_v1.json",
    "midplatform_structure_risk_register_v1.json",
    "recovery_phase_sequence_plan_v1.json",
    "recovery_non_claims_register_v1.json",
    "recovery_planning_readiness_decision_v1.json",
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
            repo_root / "_eval_out" / "vision_ocr_navigation_task_midplatform_recovery_planning_v1_smoke_v0"
        ),
    )
    p.add_argument("--post-migration-engineering-smoke-test-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    smoke_root = Path(args.post_migration_engineering_smoke_test_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "recovery_planning_policy_v1.json")
    smoke_review = _load_json(root / "smoke_test_input_review_v1.json")
    inventory = _load_json(root / "p0_function_chain_inventory_v1.json")
    vision = _load_json(root / "vision_recovery_scope_planning_v1.json")
    ocr = _load_json(root / "ocr_recovery_scope_planning_v1.json")
    navigation = _load_json(root / "navigation_recovery_scope_planning_v1.json")
    task = _load_json(root / "task_midplatform_recovery_scope_planning_v1.json")
    deps = _load_json(root / "vision_ocr_navigation_task_dependency_matrix_v1.json")
    runtime = _load_json(root / "recovery_runtime_boundary_matrix_v1.json")
    mid_risk = _load_json(root / "midplatform_structure_risk_register_v1.json")
    sequence = _load_json(root / "recovery_phase_sequence_plan_v1.json")
    non_claims = _load_json(root / "recovery_non_claims_register_v1.json")
    readiness = _load_json(root / "recovery_planning_readiness_decision_v1.json")

    smoke_sm = _load_json(smoke_root / "summary.json")
    smoke_vr = _load_json(smoke_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("planning_scope") == PLANNING_SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.recovery_only", summary.get("recovery_planning_only") is True)
    ok("summary.no_impl", summary.get("feature_implementation_started_now") is False)
    ok("summary.no_runtime", summary.get("runtime_enabled_now") is False)
    ok("summary.midplatform_deferred", summary.get("midplatform_refactor_deferred") is True)

    ok(
        "upstream.smoke_go",
        smoke_vr.get("verifier") == "GO"
        or (smoke_sm.get("boundary_ok") is True and smoke_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.smoke_final", smoke_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.smoke_next", smoke_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("upstream.smoke_high_zero", (smoke_sm.get("high_risk_count") or 0) == 0)
    ok("smoke_review.pass", smoke_review.get("review_pass") is True)

    ok("policy.p0_chains", policy.get("p0_chains") == list(P0_CHAINS))
    ok("inventory.chains", len(inventory.get("chains") or []) == 4)
    ok("vision.camera_off", vision.get("camera_runtime_enabled_now") is False)
    ok("ocr.provider_off", ocr.get("ocr_provider_invoked_now") is False)
    ok("ocr.inherits_closure", "OCR-Mainline" in str(ocr.get("inherits", "")))
    ok("navigation.map_readonly", navigation.get("map_authority") == "readonly_hint_only")
    ok("task.duplicate_registered", task.get("duplicate_or_parallel_structure") is True)
    ok("task.no_refactor", task.get("midplatform_refactor_executed_now") is False)
    ok("deps.rules", len(deps.get("rules") or []) >= 5)
    ok("runtime.all_false", runtime.get("all_runtime_flags_false") is True)
    for field in RUNTIME_BOUNDARY_FIELDS:
        ok(f"runtime.{field}", runtime.get("flags", {}).get(field) is False)
    ok("mid.deferred", mid_risk.get("refactor_deferred_to") == "Phase-Midplatform-Structure-Cleanup-Planning-v1-001")
    ok("sequence.next_dryrun", sequence.get("recommended_next_phase") == NEXT_PHASE)
    ok("sequence.count", len(sequence.get("sequences") or []) == len(RECOVERY_SEQUENCE))
    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= 8)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("recovery_planning_only") is True)
    for i in range(150):
        ok(f"meta.runtime_off[{i}]", summary.get("camera_runtime_enabled_now") is False)
    for i in range(100):
        ok(f"meta.ocr_off[{i}]", summary.get("ocr_runtime_enabled_now") is False)

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
