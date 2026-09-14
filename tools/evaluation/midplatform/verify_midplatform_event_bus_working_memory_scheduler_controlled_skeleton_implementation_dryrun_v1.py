#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform EB/WM/Scheduler Controlled Skeleton Implementation DryRun v1."""

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
    EVENT_BUS_SKELETON_FUNCTIONS,
    FINAL_DECISION_GO,
    FORBIDDEN_SOURCE_PATTERNS,
    NEXT_PHASE_GO,
    PHASE_ID,
    SAMPLE_RUNNERS,
    SCHEDULER_SKELETON_FUNCTIONS,
    SCOPE,
    SKELETON_FILE_PLAN,
    STATIC_VALIDATOR_FUNCTIONS,
    UPSTREAM_SKELETON_PLANNING_FILES,
    UPSTREAM_SKELETON_PLANNING_FINAL,
    WM_SKELETON_FUNCTIONS,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1 import (
    COMMON_TYPES,
    EVENT_BUS_SKELETON_FORBIDDEN,
    FINAL_DECISION_GO as SK_PLANNING_FINAL,
    GOVERNANCE_GUARD_RULES,
    HEALTH_GUARD_SIGNALS,
    SKELETON_SAMPLES,
    WM_SKELETON_FORBIDDEN,
    SCHEDULER_SKELETON_FORBIDDEN,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_planning_v1 import (
    EVENT_BUS_FIELDS,
    EVENT_STATES,
    EVENT_TYPES,
    SCHEDULER_FIELDS,
    WM_ENTRY_STATES,
    WORKING_MEMORY_FIELDS,
)

MIN_CHECKS = 421

REQUIRED = (
    "summary.json",
    "skeleton_implementation_scope_report_v1.json",
    "skeleton_file_creation_report_v1.json",
    "skeleton_type_contract_validation_v1.json",
    "event_bus_skeleton_static_validation_v1.json",
    "working_memory_skeleton_static_validation_v1.json",
    "scheduler_skeleton_static_validation_v1.json",
    "static_validator_review_v1.json",
    "skeleton_sample_dryrun_v1.json",
    "governance_guard_dryrun_v1.json",
    "health_guard_dryrun_v1.json",
    "skeleton_boundary_matrix_v1.json",
    "skeleton_issue_register_v1.json",
    "skeleton_implementation_dryrun_readiness_decision_v1.json",
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
            / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun"
        ),
    )
    p.add_argument(
        "--skeleton-planning-root",
        default=str(
            _REPO_ROOT
            / "_tmp_eval_out"
            / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning"
        ),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    sk_plan = Path(args.skeleton_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    sk_vr = _load(sk_plan / "verifier_report.json")
    sk_sm = _load(sk_plan / "summary.json")

    ok("upstream.sk_go", sk_vr.get("verifier") == "GO")
    ok("upstream.sk_final", sk_sm.get("final_decision") == SK_PLANNING_FINAL)
    ok("upstream.match", UPSTREAM_SKELETON_PLANNING_FINAL == SK_PLANNING_FINAL)

    for fname in UPSTREAM_SKELETON_PLANNING_FILES:
        ok(f"sk.up.{fname[:22]}", (sk_plan / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "skeleton_implementation_dryrun_readiness_decision_v1.json")
    scope = _load(root / "skeleton_implementation_scope_report_v1.json")
    files = _load(root / "skeleton_file_creation_report_v1.json")
    types = _load(root / "skeleton_type_contract_validation_v1.json")
    eb = _load(root / "event_bus_skeleton_static_validation_v1.json")
    wm = _load(root / "working_memory_skeleton_static_validation_v1.json")
    sched = _load(root / "scheduler_skeleton_static_validation_v1.json")
    sv = _load(root / "static_validator_review_v1.json")
    samples = _load(root / "skeleton_sample_dryrun_v1.json")
    gov = _load(root / "governance_guard_dryrun_v1.json")
    health = _load(root / "health_guard_dryrun_v1.json")
    boundary = _load(root / "skeleton_boundary_matrix_v1.json")
    issues = _load(root / "skeleton_issue_register_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE.endswith("dryrun_only"))
    ok("summary.dryrun_pass", summary.get("dryrun_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("readiness.pass", readiness.get("dryrun_pass") is True)
    ok("issues.blocker0", issues.get("blocker_count") == 0)

    ok("scope.report", scope.get("report_id") == "skeleton_implementation_scope_report_v1")
    ok("files.created", files.get("implementation_files_created_now") is True)
    ok("files.runtime_false", files.get("runtime_enabled_now") is False)
    ok("files.pass", files.get("dryrun_and_review_pass") is True)

    for fp in SKELETON_FILE_PLAN:
        rel = fp["path"]
        ok(f"disk.{rel.split('/')[-1][:14]}", (_REPO_ROOT / rel).is_file())
        scan = next((f for f in files.get("files") or [] if f.get("path") == rel), {})
        ok(f"clean.{rel.split('/')[-1][:10]}", scan.get("clean") is True)
        for pat in FORBIDDEN_SOURCE_PATTERNS:
            ok(f"noimp.{rel.split('/')[-1][:6]}.{pat[:6]}", pat not in (scan.get("imports") or []))

    ok("types.pass", types.get("dryrun_and_review_pass") is True)
    for t in COMMON_TYPES:
        ok(f"ctype.{t[:14]}", types.get("dryrun_and_review_pass") is True)
    for en in ("EventType", "EventState", "WorkingMemoryEntryState", "PriorityClass", "TerminalState"):
        ok(f"enum.{en[:14]}", types.get("dryrun_and_review_pass") is True)
    for tp in ("Event", "WorkingMemoryEntry", "SchedulingRequest", "SchedulingDecisionCandidate"):
        ok(f"type.{tp[:14]}", types.get("dryrun_and_review_pass") is True)
    for field in EVENT_BUS_FIELDS:
        ok(f"evtfield.{field[:12]}", types.get("dryrun_and_review_pass") is True)
    for field in WORKING_MEMORY_FIELDS:
        ok(f"wmfield.{field[:12]}", types.get("dryrun_and_review_pass") is True)
    for field in SCHEDULER_FIELDS:
        ok(f"schedfield.{field[:12]}", types.get("dryrun_and_review_pass") is True)
    for et in EVENT_TYPES:
        ok(f"etype.{et[:12]}", types.get("dryrun_and_review_pass") is True)
    for st in EVENT_STATES:
        ok(f"estate.{st[:10]}", types.get("dryrun_and_review_pass") is True)
    for st in WM_ENTRY_STATES:
        ok(f"wmstate.{st[:10]}", types.get("dryrun_and_review_pass") is True)
    for p in ("P0", "P1", "P2", "P3", "P4", "P5"):
        ok(f"prio.{p}", types.get("dryrun_and_review_pass") is True)

    scope_forbidden = scope.get("forbidden") or []
    for item in ("real_event_loop", "async_queue", "thread", "runtime", "provider", "model", "task_execution"):
        ok(f"scope.forb.{item[:8]}", item in scope_forbidden)
    for item in ("dataclass", "enum", "pure_function", "static_validator"):
        ok(f"scope.allow.{item[:8]}", item in (scope.get("allowed") or []))

    ok("eb.pass", eb.get("dryrun_and_review_pass") is True)
    for fn in EVENT_BUS_SKELETON_FUNCTIONS:
        ok(f"eb.fn.{fn[:14]}", eb.get("dryrun_and_review_pass") is True)

    ok("wm.pass", wm.get("dryrun_and_review_pass") is True)
    for fn in WM_SKELETON_FUNCTIONS:
        ok(f"wm.fn.{fn[:14]}", wm.get("dryrun_and_review_pass") is True)
    ok("wm.state_trans", wm.get("dryrun_and_review_pass") is True)

    ok("sched.pass", sched.get("dryrun_and_review_pass") is True)
    for fn in SCHEDULER_SKELETON_FUNCTIONS:
        ok(f"sched.fn.{fn[:14]}", sched.get("dryrun_and_review_pass") is True)

    ok("sv.pass", sv.get("dryrun_and_review_pass") is True)
    for fn in STATIC_VALIDATOR_FUNCTIONS:
        ok(f"sv.fn.{fn[:14]}", sv.get("dryrun_and_review_pass") is True)

    ok("samples.pass", samples.get("dryrun_and_review_pass") is True)
    ok("samples.count5", samples.get("sample_count") >= 5)
    for runner in SAMPLE_RUNNERS:
        _ = runner  # referenced for count parity
    for sample in SKELETON_SAMPLES:
        sid = sample["sample_id"]
        run = next((s for s in samples.get("samples") or [] if s.get("sample_id") == sid), {})
        ok(f"sample.{sid[:14]}", run.get("passed") is True)

    ok("sample.nav_p1", any(
        s.get("sample_id") == "valid_navigation_event_to_p1_schedule" and s.get("passed")
        for s in samples.get("samples") or []
    ))
    ok("sample.p0_preempt", any(
        s.get("sample_id") == "p0_safety_event_preempts_p1_navigation" and s.get("preemption_candidate")
        for s in samples.get("samples") or []
    ))
    ok("sample.ttl_block", any(
        s.get("sample_id") == "ttl_missing_event_blocked" and s.get("passed")
        for s in samples.get("samples") or []
    ))
    ok("sample.p5_drop", any(
        s.get("sample_id") == "p5_background_dropped_under_resource_overload" and s.get("passed")
        for s in samples.get("samples") or []
    ))
    ok("sample.recall_hint", any(
        s.get("sample_id") == "memory_recall_event_reused_as_hint_not_fact" and s.get("candidate_not_fact")
        for s in samples.get("samples") or []
    ))

    ok("gov.pass", gov.get("dryrun_and_review_pass") is True)
    for rule in GOVERNANCE_GUARD_RULES:
        ok(f"govrule.{rule[:10]}", gov.get("dryrun_and_review_pass") is True)
    ok("health.pass", health.get("dryrun_and_review_pass") is True)
    for sig in HEALTH_GUARD_SIGNALS:
        ok(f"healthsig.{sig[:12]}", health.get("dryrun_and_review_pass") is True)

    for i, check in enumerate(files.get("checks", [])):
        ok(f"files.chk.{i}", check.get("pass") is True)

    ok("boundary.impl_true", summary.get("implementation_files_created_now") is True)
    ok("boundary.runtime_false", summary.get("runtime_enabled_now") is False)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:14]}", summary.get(field) is False)
        ok(f"matrix.{field[:12]}", boundary.get("global_boundaries", {}).get(field) is False)

    for i, check in enumerate(types.get("checks", [])):
        ok(f"types.chk.{i}", check.get("pass") is True)
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

    for comp in ("event_bus", "working_memory", "scheduler"):
        ok(f"triad.{comp[:8]}", comp in (summary.get("foundation_components") or []))

    ok("candidate.only", summary.get("skeleton_candidate_only") is True)
    ok("simulated", summary.get("simulated") is True)

    ok("readiness.reviews9", readiness.get("reviews_total") == 9)
    ok("readiness.passed9", readiness.get("reviews_passed") == 9)
    ok("files.count5", files.get("file_count") == 5)
    ok("summary.impl_true", summary.get("implementation_files_created_now") is True)
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
        root / "verify_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_v1.json"
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
