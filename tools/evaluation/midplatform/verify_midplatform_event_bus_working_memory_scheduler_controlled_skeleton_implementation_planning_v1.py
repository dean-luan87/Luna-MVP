#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform EB/WM/Scheduler Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1 import (
    BOUNDARY_FALSE,
    COMMON_TYPES,
    EVENT_BUS_FIELDS,
    EVENT_BUS_SKELETON_FORBIDDEN,
    EVENT_BUS_SKELETON_FUNCTIONS,
    EVENT_STATES,
    EVENT_TYPES,
    FINAL_DECISION_GO,
    GOVERNANCE_GUARD_RULES,
    HEALTH_GUARD_SIGNALS,
    INTERACTION_STEPS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCHEDULER_FIELDS,
    SCHEDULER_SKELETON_FORBIDDEN,
    SCHEDULER_SKELETON_FUNCTIONS,
    SCOPE,
    SKELETON_FILE_PLAN,
    SKELETON_SAMPLES,
    SOURCE_CHAIN,
    TEST_PLAN_CATEGORIES,
    UPSTREAM_DRYRUN_FINAL,
    UPSTREAM_PLANNING_FILES,
    WM_ENTRY_STATES,
    WM_SKELETON_FORBIDDEN,
    WM_SKELETON_FUNCTIONS,
    WORKING_MEMORY_FIELDS,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
)

MIN_CHECKS = 305

REQUIRED = (
    "summary.json",
    "controlled_skeleton_scope_v1.json",
    "controlled_skeleton_file_plan_v1.json",
    "controlled_skeleton_type_contract_v1.json",
    "event_bus_skeleton_contract_v1.json",
    "working_memory_skeleton_contract_v1.json",
    "scheduler_skeleton_contract_v1.json",
    "controlled_skeleton_interaction_plan_v1.json",
    "controlled_skeleton_governance_guard_v1.json",
    "controlled_skeleton_health_guard_v1.json",
    "controlled_skeleton_sample_plan_v1.json",
    "controlled_skeleton_test_plan_v1.json",
    "controlled_skeleton_boundary_matrix_v1.json",
    "controlled_skeleton_non_claims_v1.json",
    "controlled_skeleton_planning_readiness_decision_v1.json",
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
            / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_planning"),
    )
    p.add_argument(
        "--dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_dryrun_and_review"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    dr_root = Path(args.dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    dr_vr = _load(dr_root / "verifier_report.json")
    dr_sm = _load(dr_root / "summary.json")
    plan_vr = _load(plan_root / "verifier_report.json")

    ok("upstream.dr_go", dr_vr.get("verifier") == "GO")
    ok("upstream.dr_final", dr_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.match", UPSTREAM_DRYRUN_FINAL == DRYRUN_FINAL)

    for fname in UPSTREAM_PLANNING_FILES:
        ok(f"plan.up.{fname[:22]}", (plan_root / fname).is_file())
    ok("dr.up.readiness", (dr_root / "dryrun_readiness_decision_v1.json").is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "controlled_skeleton_planning_readiness_decision_v1.json")
    scope = _load(root / "controlled_skeleton_scope_v1.json")
    file_plan = _load(root / "controlled_skeleton_file_plan_v1.json")
    types = _load(root / "controlled_skeleton_type_contract_v1.json")
    eb = _load(root / "event_bus_skeleton_contract_v1.json")
    wm = _load(root / "working_memory_skeleton_contract_v1.json")
    sched = _load(root / "scheduler_skeleton_contract_v1.json")
    interaction = _load(root / "controlled_skeleton_interaction_plan_v1.json")
    gov = _load(root / "controlled_skeleton_governance_guard_v1.json")
    health = _load(root / "controlled_skeleton_health_guard_v1.json")
    samples = _load(root / "controlled_skeleton_sample_plan_v1.json")
    test_plan = _load(root / "controlled_skeleton_test_plan_v1.json")
    boundary = _load(root / "controlled_skeleton_boundary_matrix_v1.json")
    nc = _load(root / "controlled_skeleton_non_claims_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE.endswith("planning_only"))
    ok("source.chain", summary.get("source_chain") == SOURCE_CHAIN)
    ok("gov.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("readiness.pass", readiness.get("planning_pass") is True)
    ok("readiness.impl_false", readiness.get("implementation_files_created_now") is False)

    ok("scope.exists", scope.get("scope_id") == "controlled_skeleton_scope_v1")
    for allowed in ("dataclass", "enum", "pure_function", "in_memory_stub", "static_validator"):
        ok(f"scope.allow.{allowed[:10]}", allowed in (scope.get("allowed") or []))
    for forb in ("real_event_bus_loop", "real_async_queue", "provider_invocation", "memory_write"):
        ok(f"scope.forb.{forb[:10]}", forb in (scope.get("forbidden") or []))

    ok("fileplan.count5", file_plan.get("file_count") == len(SKELETON_FILE_PLAN))
    ok("fileplan.no_create", file_plan.get("create_in_this_phase") is False)
    ok("fileplan.impl_false", file_plan.get("implementation_files_created_now") is False)
    for fp in SKELETON_FILE_PLAN:
        found = next((f for f in file_plan.get("files") or [] if f.get("path") == fp["path"]), {})
        ok(f"file.{fp['path'].split('/')[-1][:14]}", bool(found))
        ok(f"file.{fp['path'].split('/')[-1][:10]}.nc", found.get("create_in_this_phase") is False)
        ok(f"file.{fp['path'].split('/')[-1][:8]}.disk", not (_REPO_ROOT / fp["path"]).is_file())

    ok("types.count14", types.get("type_count") == len(COMMON_TYPES))
    for t in COMMON_TYPES:
        ok(f"type.{t[:14]}", t in (types.get("types") or []))
    for field in EVENT_BUS_FIELDS:
        ok(f"evt.field.{field[:12]}", field in (types.get("event_fields") or []))
    for field in WORKING_MEMORY_FIELDS:
        ok(f"wm.field.{field[:12]}", field in (types.get("working_memory_entry_fields") or []))
    for field in SCHEDULER_FIELDS:
        ok(f"sched.field.{field[:12]}", field in (types.get("scheduling_request_fields") or []))
    for et in EVENT_TYPES:
        ok(f"etype.{et[:12]}", et in (types.get("event_type_enum_values") or []))
    for st in EVENT_STATES:
        ok(f"estate.{st[:10]}", st in (types.get("event_state_enum_values") or []))
    for st in WM_ENTRY_STATES:
        ok(f"wmstate.{st[:10]}", st in (types.get("wm_entry_state_enum_values") or []))
    for p in ("P0", "P1", "P2", "P3", "P4", "P5"):
        ok(f"prio.{p}", p in (types.get("priority_class_enum_values") or []))

    for fn in EVENT_BUS_SKELETON_FUNCTIONS:
        ok(f"eb.fn.{fn[:14]}", fn in (eb.get("allowed_functions") or []))
    for forb in EVENT_BUS_SKELETON_FORBIDDEN:
        ok(f"eb.forb.{forb[:10]}", forb in (eb.get("forbidden") or []))

    for fn in WM_SKELETON_FUNCTIONS:
        ok(f"wm.fn.{fn[:14]}", fn in (wm.get("allowed_functions") or []))
    for forb in WM_SKELETON_FORBIDDEN:
        ok(f"wm.forb.{forb[:10]}", forb in (wm.get("forbidden") or []))
    ok("wm.not_memory", wm.get("working_memory_is_not_memory") is True)
    ok("wm.not_worldmodel", wm.get("working_memory_is_not_worldmodel") is True)

    for fn in SCHEDULER_SKELETON_FUNCTIONS:
        ok(f"sched.fn.{fn[:14]}", fn in (sched.get("allowed_functions") or []))
    for forb in SCHEDULER_SKELETON_FORBIDDEN:
        ok(f"sched.forb.{forb[:10]}", forb in (sched.get("forbidden") or []))

    ok("interaction.candidate", interaction.get("candidate_only") is True)
    ok("interaction.no_dispatch", interaction.get("no_real_dispatch") is True)
    for idx, step in enumerate(INTERACTION_STEPS):
        ok(f"interaction.step{idx}", step in (interaction.get("steps") or []))

    ok("gov.l0", gov.get("l0_constrained") is True)
    for rule in GOVERNANCE_GUARD_RULES:
        ok(f"gov.{rule[:12]}", rule in (gov.get("rules") or []))

    ok("health.candidate_out", health.get("output_type") == "health_issue_candidate")
    ok("health.no_runtime", health.get("real_health_runtime_enabled") is False)
    for sig in HEALTH_GUARD_SIGNALS:
        ok(f"health.{sig[:14]}", sig in (health.get("signals") or []))

    ok("samples.count5", samples.get("sample_count") >= 5)
    for sample in SKELETON_SAMPLES:
        sid = sample["sample_id"]
        found = next((s for s in samples.get("samples") or [] if s.get("sample_id") == sid), {})
        ok(f"sample.{sid[:14]}", bool(found))

    ok("testplan.cat8", test_plan.get("category_count") == len(TEST_PLAN_CATEGORIES))
    for cat in TEST_PLAN_CATEGORIES:
        ok(f"testcat.{cat[:14]}", cat in (test_plan.get("categories") or []))

    for field in BOUNDARY_FALSE:
        ok(f"boundary.global.{field[:14]}", boundary.get("global_boundaries", {}).get(field) is False)
        ok(f"summary.boundary.{field[:10]}", summary.get(field) is False)
    ok("boundary.impl_false", summary.get("implementation_files_created_now") is False)

    for comp in ("event_bus", "working_memory", "scheduler"):
        cb = (boundary.get("foundation_components") or {}).get(comp, {})
        ok(f"comp.{comp[:8]}.impl", cb.get("implementation_files_created_now") is False)

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (nc.get("non_claims") or []))
        ok(f"summary.nc.{claim[:8]}", claim in (summary.get("non_claims") or []))

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
        root / "verify_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1.json"
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
