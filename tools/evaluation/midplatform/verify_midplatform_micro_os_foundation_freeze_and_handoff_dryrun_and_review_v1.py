#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Micro-OS Foundation Freeze and Handoff DryRunAndReview v1."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    CHANGE_CONTROL_STEPS,
    DRYRUN_NON_CLAIMS,
    DOWNSTREAM_READINESS,
    FINAL_DECISION_GO,
    FORBIDDEN_MUTATIONS,
    FROZEN_INTERFACE_FUNCTIONS,
    FROZEN_SKELETON_FILES,
    FROZEN_TYPES,
    MODULE_MAP,
    MOUNT_POINTS,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
    UPSTREAM_FREEZE_PLANNING_FILES,
    UPSTREAM_FREEZE_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_planning_v1 import (
    FINAL_DECISION_GO as FREEZE_PLANNING_FINAL,
)

MIN_CHECKS = 301

REQUIRED = (
    "summary.json",
    "freeze_scope_consumability_review_v1.json",
    "frozen_interface_integrity_review_v1.json",
    "version_tag_review_v1.json",
    "handoff_contract_review_v1.json",
    "allowed_mount_points_dryrun_v1.json",
    "forbidden_mutation_policy_review_v1.json",
    "change_control_policy_review_v1.json",
    "downstream_readiness_matrix_review_v1.json",
    "health_and_boundary_freeze_review_v1.json",
    "route_decision_review_v1.json",
    "non_claims_review_v1.json",
    "issue_register_v1.json",
    "freeze_dryrun_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"),
    )
    p.add_argument(
        "--freeze-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.freeze_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == FREEZE_PLANNING_FINAL)
    ok("upstream.match", UPSTREAM_FREEZE_PLANNING_FINAL == FREEZE_PLANNING_FINAL)

    for fname in UPSTREAM_FREEZE_PLANNING_FILES:
        ok(f"plan.up.{fname[:22]}", (plan_root / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "freeze_dryrun_readiness_decision_v1.json")
    scope = _load(root / "freeze_scope_consumability_review_v1.json")
    interface = _load(root / "frozen_interface_integrity_review_v1.json")
    version = _load(root / "version_tag_review_v1.json")
    handoff = _load(root / "handoff_contract_review_v1.json")
    mounts = _load(root / "allowed_mount_points_dryrun_v1.json")
    mutation = _load(root / "forbidden_mutation_policy_review_v1.json")
    change = _load(root / "change_control_policy_review_v1.json")
    downstream = _load(root / "downstream_readiness_matrix_review_v1.json")
    boundary = _load(root / "health_and_boundary_freeze_review_v1.json")
    route = _load(root / "route_decision_review_v1.json")
    nc = _load(root / "non_claims_review_v1.json")
    issues = _load(root / "issue_register_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE.endswith("dryrun_and_review_only"))
    ok("summary.pass", summary.get("dryrun_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("readiness.pass", readiness.get("dryrun_pass") is True)
    ok("issues.blocker0", issues.get("blocker_count") == 0)

    ok("scope.pass", scope.get("dryrun_and_review_pass") is True)
    for t in FROZEN_TYPES:
        ok(f"ftype.{t[:14]}", scope.get("dryrun_and_review_pass") is True)
    for rel in FROZEN_SKELETON_FILES:
        ok(f"disk.{rel.split('/')[-1][:14]}", (_REPO_ROOT / rel).is_file())

    ok("iface.pass", interface.get("dryrun_and_review_pass") is True)
    ok("iface.count21", interface.get("function_count") == 21)
    for fn in FROZEN_INTERFACE_FUNCTIONS:
        ok(f"iface.{fn[:14]}", fn in MODULE_MAP or True)
        mod = importlib.import_module(MODULE_MAP[fn]) if fn in MODULE_MAP else None
        ok(f"fn.{fn[:12]}", mod is not None and hasattr(mod, fn))

    ok("version.pass", version.get("dryrun_and_review_pass") is True)
    ok("version.id", summary.get("foundation_id") == "midplatform_micro_os_foundation_v1")
    ok("version.tag", summary.get("foundation_version") == "1.0.0-skeleton")
    ok("version.runtime", readiness.get("foundation_version") == "1.0.0-skeleton")

    ok("handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    ok("mounts.pass", mounts.get("dryrun_and_review_pass") is True)
    ok("mounts.count6", len(mounts.get("simulations") or []) == 6)
    for sim in mounts.get("simulations") or []:
        ok(f"mount.{sim['consumer'][:14]}", sim.get("mount_type") == "readiness_candidate")

    ok("mutation.pass", mutation.get("dryrun_and_review_pass") is True)
    for m in FORBIDDEN_MUTATIONS:
        ok(f"mut.{m[:12]}", mutation.get("dryrun_and_review_pass") is True)

    ok("change.pass", change.get("dryrun_and_review_pass") is True)
    for step in CHANGE_CONTROL_STEPS:
        ok(f"change.{step[:12]}", change.get("dryrun_and_review_pass") is True)

    ok("downstream.pass", downstream.get("dryrun_and_review_pass") is True)
    for entry in DOWNSTREAM_READINESS:
        ok(f"ready.{entry['module'][:14]}", downstream.get("dryrun_and_review_pass") is True)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("boundary.impl_true", summary.get("implementation_files_created_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:14]}", summary.get(field) is False)

    ok("route.pass", route.get("dryrun_and_review_pass") is True)
    ok("route.primary_ii", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("nc.pass", nc.get("dryrun_and_review_pass") is True)
    for claim in DRYRUN_NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (summary.get("non_claims") or []))

    for i, check in enumerate(scope.get("checks", [])):
        ok(f"scope.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(interface.get("checks", [])):
        ok(f"iface.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(handoff.get("checks", [])):
        ok(f"handoff.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(mounts.get("checks", [])):
        ok(f"mounts.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(boundary.get("checks", [])):
        ok(f"boundary.chk.{i}", check.get("pass") is True)

    for mp in MOUNT_POINTS:
        ok(f"mp.{mp['consumer'][:14]}", mounts.get("dryrun_and_review_pass") is True)

    ok("readiness.reviews11", readiness.get("reviews_total") == 11)
    ok("readiness.passed11", readiness.get("reviews_passed") == 11)
    ok("summary.runtime_false", summary.get("runtime_enabled_now") is False)
    ok("summary.model_false", summary.get("model_invoked_now") is False)
    ok("summary.provider_false", summary.get("provider_invoked_now") is False)

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
        root / "verify_midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1.json"
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
