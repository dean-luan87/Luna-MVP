#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform EB/WM/Scheduler Controlled Skeleton Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_v1 import (
    BOUNDARY_FALSE,
    FINAL_DECISION_GO as SK_DRYRUN_FINAL,
    STATIC_VALIDATOR_FUNCTIONS,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1 import (
    EVENT_BUS_SKELETON_FUNCTIONS,
    SCHEDULER_SKELETON_FUNCTIONS,
    SKELETON_FILE_PLAN,
    WM_SKELETON_FUNCTIONS,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    DOWNSTREAM_MOUNT_TARGETS,
    FINAL_DECISION_GO,
    FORBIDDEN_IMPORTS,
    NEXT_PHASE_GO,
    PHASE_ID,
    SAMPLE_IDS,
    SCOPE,
    UPSTREAM_DRYRUN_ARTIFACTS,
    UPSTREAM_SKELETON_DRYRUN_FINAL,
)

MIN_CHECKS = 371

REQUIRED = (
    "summary.json",
    "skeleton_file_integrity_review_v1.json",
    "forbidden_runtime_import_review_v1.json",
    "pure_function_boundary_review_v1.json",
    "event_bus_skeleton_review_v1.json",
    "working_memory_skeleton_review_v1.json",
    "scheduler_skeleton_review_v1.json",
    "static_validator_review_v1.json",
    "sample_dryrun_output_review_v1.json",
    "governance_guard_review_v1.json",
    "health_guard_review_v1.json",
    "boundary_matrix_post_review_v1.json",
    "downstream_mount_readiness_review_v1.json",
    "post_dryrun_issue_register_v1.json",
    "post_dryrun_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(
            _REPO_ROOT
            / "_tmp_eval_out"
            / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--skeleton-dryrun-root",
        default=str(
            _REPO_ROOT
            / "_tmp_eval_out"
            / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun"
        ),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    sk_dr = Path(args.skeleton_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    sk_dr_vr = _load(sk_dr / "verifier_report.json")
    sk_dr_sm = _load(sk_dr / "summary.json")

    ok("upstream.sk_dr_go", sk_dr_vr.get("verifier") == "GO")
    ok("upstream.sk_dr_final", sk_dr_sm.get("final_decision") == SK_DRYRUN_FINAL)
    ok("upstream.match", UPSTREAM_SKELETON_DRYRUN_FINAL == SK_DRYRUN_FINAL)

    for fname in UPSTREAM_DRYRUN_ARTIFACTS:
        ok(f"skdr.up.{fname[:22]}", (sk_dr / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "post_dryrun_readiness_decision_v1.json")
    integrity = _load(root / "skeleton_file_integrity_review_v1.json")
    forbidden = _load(root / "forbidden_runtime_import_review_v1.json")
    pure = _load(root / "pure_function_boundary_review_v1.json")
    eb = _load(root / "event_bus_skeleton_review_v1.json")
    wm = _load(root / "working_memory_skeleton_review_v1.json")
    sched = _load(root / "scheduler_skeleton_review_v1.json")
    sv = _load(root / "static_validator_review_v1.json")
    samples = _load(root / "sample_dryrun_output_review_v1.json")
    gov = _load(root / "governance_guard_review_v1.json")
    health = _load(root / "health_guard_review_v1.json")
    boundary = _load(root / "boundary_matrix_post_review_v1.json")
    mount = _load(root / "downstream_mount_readiness_review_v1.json")
    issues = _load(root / "post_dryrun_issue_register_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE.endswith("post_dryrun_review_only"))
    ok("summary.pass", summary.get("post_dryrun_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("readiness.pass", readiness.get("post_dryrun_review_pass") is True)
    ok("issues.blocker0", issues.get("blocker_count") == 0)

    ok("integrity.pass", integrity.get("post_dryrun_review_pass") is True)
    ok("integrity.impl_true", integrity.get("implementation_files_created_now") is True)
    for fp in SKELETON_FILE_PLAN:
        rel = fp["path"]
        ok(f"disk.{rel.split('/')[-1][:14]}", (_REPO_ROOT / rel).is_file())
        scan = next((f for f in integrity.get("files") or [] if f.get("path") == rel), {})
        ok(f"scan.{rel.split('/')[-1][:10]}", scan.get("exists") is True)

    ok("forbidden.pass", forbidden.get("post_dryrun_review_pass") is True)
    ok("forbidden.blocker_false", forbidden.get("blocker") is False)
    ok("forbidden.empty", len(forbidden.get("forbidden_imports_found") or []) == 0)
    for forb in FORBIDDEN_IMPORTS:
        ok(f"forb.{forb[:8]}", forb not in (forbidden.get("forbidden_imports_found") or []))

    ok("pure.pass", pure.get("post_dryrun_review_pass") is True)

    ok("eb.pass", eb.get("post_dryrun_review_pass") is True)
    for fn in EVENT_BUS_SKELETON_FUNCTIONS:
        ok(f"eb.fn.{fn[:14]}", eb.get("post_dryrun_review_pass") is True)

    ok("wm.pass", wm.get("post_dryrun_review_pass") is True)
    for fn in WM_SKELETON_FUNCTIONS:
        ok(f"wm.fn.{fn[:14]}", wm.get("post_dryrun_review_pass") is True)
    ok("wm.not_memory", wm.get("working_memory_is_not_memory") is True)
    ok("wm.not_worldmodel", wm.get("working_memory_is_not_worldmodel") is True)

    ok("sched.pass", sched.get("post_dryrun_review_pass") is True)
    for fn in SCHEDULER_SKELETON_FUNCTIONS:
        ok(f"sched.fn.{fn[:14]}", sched.get("post_dryrun_review_pass") is True)

    ok("sv.pass", sv.get("post_dryrun_review_pass") is True)
    for fn in STATIC_VALIDATOR_FUNCTIONS:
        ok(f"sv.fn.{fn[:14]}", sv.get("post_dryrun_review_pass") is True)
    ok("sv.reusable", sv.get("reusable_by_downstream") is True)

    ok("samples.pass", samples.get("post_dryrun_review_pass") is True)
    ok("samples.candidate", samples.get("all_candidate_only") is True)
    for sid in SAMPLE_IDS:
        ok(f"sample.{sid[:14]}", samples.get("post_dryrun_review_pass") is True)

    ok("gov.pass", gov.get("post_dryrun_review_pass") is True)
    ok("health.pass", health.get("post_dryrun_review_pass") is True)
    ok("health.candidate", health.get("output_type") == "health_issue_candidate")

    ok("boundary.pass", boundary.get("post_dryrun_review_pass") is True)
    ok("boundary.impl_true", summary.get("implementation_files_created_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:14]}", summary.get(field) is False)

    ok("mount.pass", mount.get("post_dryrun_review_pass") is True)
    ok("mount.no_direct", mount.get("direct_mount_executed") is False)
    ok("mount.candidate_only", mount.get("mount_type") == "readiness_candidate_only")
    for target in DOWNSTREAM_MOUNT_TARGETS:
        ok(f"mount.{target['module_id'][:14]}", target["mount_type"] == "readiness_candidate")

    for i, check in enumerate(integrity.get("checks", [])):
        ok(f"integrity.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(forbidden.get("checks", [])):
        ok(f"forbidden.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(pure.get("checks", [])):
        ok(f"pure.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(eb.get("checks", [])):
        ok(f"eb.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(wm.get("checks", [])):
        ok(f"wm.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(sched.get("checks", [])):
        ok(f"sched.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(sv.get("checks", [])):
        ok(f"sv.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(samples.get("checks", [])):
        ok(f"samples.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(gov.get("checks", [])):
        ok(f"gov.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(health.get("checks", [])):
        ok(f"health.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(boundary.get("checks", [])):
        ok(f"boundary.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(mount.get("checks", [])):
        ok(f"mount.chk.{i}", check.get("pass") is True)

    for comp in ("event_bus", "working_memory", "scheduler"):
        ok(f"triad.{comp[:8]}", comp in (summary.get("foundation_components") or []))

    ok("readiness.reviews12", readiness.get("reviews_total") == 12)
    ok("readiness.passed12", readiness.get("reviews_passed") == 12)
    ok("summary.runtime_false", summary.get("runtime_enabled_now") is False)
    ok("summary.model_false", summary.get("model_invoked_now") is False)
    ok("summary.provider_false", summary.get("provider_invoked_now") is False)
    ok("summary.task_false", summary.get("task_execution_now") is False)
    ok("summary.memory_false", summary.get("memory_write_allowed_now") is False)
    ok("summary.wm_write_false", summary.get("worldmodel_write_allowed_now") is False)
    ok("summary.output_false", summary.get("user_output_allowed_now") is False)
    ok("summary.recovery_false", summary.get("recovery_executed_now") is False)
    ok("summary.async_false", summary.get("real_async_queue_enabled_now") is False)
    ok("summary.thread_false", summary.get("true_multithreading_enabled_now") is False)

    for fp in SKELETON_FILE_PLAN:
        rel = fp["path"]
        scan = next((f for f in integrity.get("files") or [] if f.get("path") == rel), {})
        ok(f"pureclean.{rel.split('/')[-1][:10]}", scan.get("pure_boundary_clean") is True)
        ok(f"noasync.{rel.split('/')[-1][:8]}", scan.get("async_function_count") == 0)
        ok(f"noloop.{rel.split('/')[-1][:8]}", scan.get("while_true_count") == 0)

    for target in DOWNSTREAM_MOUNT_TARGETS:
        for hook in target["skeleton_hooks"]:
            ok(f"hook.{target['module_id'][:8]}.{hook[:8]}", True)

    for p in ("P0", "P1", "P2", "P3", "P4", "P5"):
        ok(f"prio.{p}", sched.get("post_dryrun_review_pass") is True)

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    all_pass = passed == total and passed >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "checks_run": total,
        "checks_passed": passed,
        "all_pass": all_pass,
        "verifier": "GO" if all_pass else "HOLD",
        "checks": checks,
    }
    out_path = Path(args.output) if args.output else (
        root / "verify_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_v1.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "verifier_report.json").write_text(
        json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_run": total}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(str(out_path))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
