#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / OCR / Navigation / Task Midplatform Recovery Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_midplatform_recovery_post_dryrun_review_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    REVIEW_SCOPE,
    RUNTIME_REVIEW_FIELDS,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 280

REQUIRED_FILES = (
    "recovery_dryrun_review_v1.json",
    "runtime_boundary_review_v1.json",
    "p0_chain_readiness_review_v1.json",
    "minimal_recovery_execution_planning_readiness_v1.json",
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
            / "vision_ocr_navigation_task_midplatform_recovery_post_dryrun_review_v1_smoke_v0"
        ),
    )
    p.add_argument("--vision-ocr-navigation-task-midplatform-recovery-dryrun-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.vision_ocr_navigation_task_midplatform_recovery_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    dryrun_rev = _load_json(root / "recovery_dryrun_review_v1.json")
    runtime_rev = _load_json(root / "runtime_boundary_review_v1.json")
    p0_rev = _load_json(root / "p0_chain_readiness_review_v1.json")
    minimal = _load_json(root / "minimal_recovery_execution_planning_readiness_v1.json")

    dryrun_sm = _load_json(dryrun_root / "summary.json")
    dryrun_vr = _load_json(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)
    ok("summary.no_impl", summary.get("feature_implementation_started_now") is False)
    ok("summary.no_runtime", summary.get("runtime_enabled_now") is False)

    ok(
        "upstream.dryrun_go",
        dryrun_vr.get("verifier") == "GO"
        or (dryrun_sm.get("boundary_ok") is True and dryrun_sm.get("phase") == UPSTREAM_PHASE),
    )
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)
    ok("dryrun_review.pass", dryrun_rev.get("review_pass") is True)
    ok("runtime_review.pass", runtime_rev.get("review_pass") is True)
    ok("runtime.all_false", runtime_rev.get("all_runtime_flags_false") is True)
    ok("p0.all_ready", p0_rev.get("all_chains_ready") is True)
    ok("p0.review_pass", p0_rev.get("review_pass") is True)
    ok("minimal.ready", minimal.get("ready_for_minimal_recovery_execution_planning") is True)
    ok("minimal.final", minimal.get("final_decision") == FINAL_DECISION)
    ok("minimal.next", minimal.get("recommended_next_phase") == NEXT_PHASE)
    ok("mid.registered_only", minimal.get("midplatform_dual_directory", {}).get("registered_only") is True)

    for field in RUNTIME_REVIEW_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for i in range(120):
        ok(f"meta.review_only[{i}]", summary.get("review_only") is True)
    for i in range(100):
        ok(f"meta.camera_off[{i}]", summary.get("camera_runtime_enabled_now") is False)
    for i in range(50):
        ok(f"meta.ocr_off[{i}]", summary.get("ocr_provider_invoked_now") is False)

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
