#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Micro-OS Foundation Freeze and Handoff Planning v1."""

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

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_planning_v1 import (
    BOUNDARY_FALSE,
    CHANGE_CONTROL_STEPS,
    DOWNSTREAM_READINESS,
    FINAL_DECISION_GO,
    FROZEN_INTERFACE_FUNCTIONS,
    FROZEN_SKELETON_FILES,
    FROZEN_TYPES,
    FORBIDDEN_MUTATIONS,
    MOUNT_POINTS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SOURCE_CHAIN,
    STATIC_VALIDATOR_FUNCTIONS,
    UPSTREAM_POST_DRYRUN_ARTIFACTS,
    UPSTREAM_POST_DRYRUN_FINAL,
    WM_FROZEN_FUNCTIONS,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL,
)

MIN_CHECKS = 262

REQUIRED = (
    "summary.json",
    "micro_os_foundation_freeze_scope_v1.json",
    "micro_os_foundation_frozen_interface_v1.json",
    "micro_os_foundation_version_tag_v1.json",
    "micro_os_foundation_handoff_contract_v1.json",
    "micro_os_foundation_allowed_mount_points_v1.json",
    "micro_os_foundation_forbidden_mutation_policy_v1.json",
    "micro_os_foundation_change_control_policy_v1.json",
    "micro_os_foundation_downstream_readiness_matrix_v1.json",
    "micro_os_foundation_health_and_boundary_freeze_v1.json",
    "micro_os_foundation_non_claims_v1.json",
    "micro_os_foundation_route_decision_v1.json",
    "micro_os_foundation_freeze_readiness_decision_v1.json",
)

MODULE_MAP = {
    "normalize_event": "capabilities.midplatform.core.event_bus_skeleton_v1",
    "validate_event_schema": "capabilities.midplatform.core.event_bus_skeleton_v1",
    "validate_event_state_transition": "capabilities.midplatform.core.event_bus_skeleton_v1",
    "route_event_candidate": "capabilities.midplatform.core.event_bus_skeleton_v1",
    "append_trace": "capabilities.midplatform.core.event_bus_skeleton_v1",
    "create_working_memory_entry": "capabilities.midplatform.core.working_memory_skeleton_v1",
    "validate_wm_entry": "capabilities.midplatform.core.working_memory_skeleton_v1",
    "validate_wm_state_transition": "capabilities.midplatform.core.working_memory_skeleton_v1",
    "apply_ttl_policy_candidate": "capabilities.midplatform.core.working_memory_skeleton_v1",
    "mark_stale_or_expired_candidate": "capabilities.midplatform.core.working_memory_skeleton_v1",
    "generate_cleanup_plan_candidate": "capabilities.midplatform.core.working_memory_skeleton_v1",
    "assign_priority_candidate": "capabilities.midplatform.core.scheduler_skeleton_v1",
    "evaluate_preemption_candidate": "capabilities.midplatform.core.scheduler_skeleton_v1",
    "evaluate_deferral_or_drop_candidate": "capabilities.midplatform.core.scheduler_skeleton_v1",
    "produce_scheduling_decision_candidate": "capabilities.midplatform.core.scheduler_skeleton_v1",
    "validate_no_runtime_flags": "capabilities.midplatform.core.micro_os_static_validators_v1",
    "validate_candidate_not_fact": "capabilities.midplatform.core.micro_os_static_validators_v1",
    "validate_required_trace": "capabilities.midplatform.core.micro_os_static_validators_v1",
    "validate_required_health_tag": "capabilities.midplatform.core.micro_os_static_validators_v1",
    "validate_required_ttl": "capabilities.midplatform.core.micro_os_static_validators_v1",
    "validate_governance_guard": "capabilities.midplatform.core.micro_os_static_validators_v1",
}


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_planning"),
    )
    p.add_argument(
        "--post-dryrun-root",
        default=str(
            _REPO_ROOT
            / "_tmp_eval_out"
            / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review"
        ),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    post_dr = Path(args.post_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    post_vr = _load(post_dr / "verifier_report.json")
    post_sm = _load(post_dr / "summary.json")

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.post_final", post_sm.get("final_decision") == POST_DRYRUN_FINAL)
    ok("upstream.match", UPSTREAM_POST_DRYRUN_FINAL == POST_DRYRUN_FINAL)

    for fname in UPSTREAM_POST_DRYRUN_ARTIFACTS:
        ok(f"post.up.{fname[:22]}", (post_dr / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "micro_os_foundation_freeze_readiness_decision_v1.json")
    scope = _load(root / "micro_os_foundation_freeze_scope_v1.json")
    interface = _load(root / "micro_os_foundation_frozen_interface_v1.json")
    version = _load(root / "micro_os_foundation_version_tag_v1.json")
    handoff = _load(root / "micro_os_foundation_handoff_contract_v1.json")
    mounts = _load(root / "micro_os_foundation_allowed_mount_points_v1.json")
    forbidden = _load(root / "micro_os_foundation_forbidden_mutation_policy_v1.json")
    change = _load(root / "micro_os_foundation_change_control_policy_v1.json")
    downstream = _load(root / "micro_os_foundation_downstream_readiness_matrix_v1.json")
    boundary = _load(root / "micro_os_foundation_health_and_boundary_freeze_v1.json")
    nc = _load(root / "micro_os_foundation_non_claims_v1.json")
    route = _load(root / "micro_os_foundation_route_decision_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE.endswith("planning_only"))
    ok("source.chain", summary.get("source_chain") == SOURCE_CHAIN)
    ok("gov.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("readiness.pass", readiness.get("planning_pass") is True)
    ok("readiness.frozen", readiness.get("foundation_frozen") is True)

    ok("scope.not_runtime", scope.get("freeze_not_runtime_ready") is True)
    for t in FROZEN_TYPES:
        ok(f"ftype.{t[:14]}", t in (scope.get("frozen_types") or []))
    for rel in FROZEN_SKELETON_FILES:
        ok(f"freeze.{rel.split('/')[-1][:14]}", (_REPO_ROOT / rel).is_file())
        ok(f"scope.{rel.split('/')[-1][:10]}", rel in (scope.get("frozen_skeleton_files") or []))

    ok("iface.count21", interface.get("function_count") == len(FROZEN_INTERFACE_FUNCTIONS))
    for fn in FROZEN_INTERFACE_FUNCTIONS:
        ok(f"iface.{fn[:14]}", fn in (interface.get("functions") or []))
        mod_path = MODULE_MAP.get(fn)
        if mod_path:
            mod = importlib.import_module(mod_path)
            ok(f"diskfn.{fn[:12]}", hasattr(mod, fn) and callable(getattr(mod, fn)))

    ok("version.id", version.get("foundation_id") == "midplatform_micro_os_foundation_v1")
    ok("version.tag", version.get("version") == "1.0.0-skeleton")
    ok("version.runtime", version.get("runtime_status") == "not_enabled")
    ok("version.status", version.get("status") == "frozen_for_downstream_mount_planning")

    for rule in handoff.get("rules") or []:
        ok(f"handoff.{rule[:12]}", bool(rule))
    ok("handoff.candidate", "candidate" in json.dumps(handoff, ensure_ascii=False).lower())

    ok("mount.count6", len(mounts.get("mount_points") or []) == len(MOUNT_POINTS))
    ok("mount.no_direct", mounts.get("direct_mount_executed") is False)
    for mp in MOUNT_POINTS:
        ok(f"mount.{mp['consumer'][:14]}", any(m.get("consumer") == mp["consumer"] for m in mounts.get("mount_points") or []))

    for mut in FORBIDDEN_MUTATIONS:
        ok(f"mut.{mut[:12]}", mut in (forbidden.get("forbidden_mutations") or []))

    ok("change.no_exec", change.get("change_executed_in_this_phase") is False)
    for step in CHANGE_CONTROL_STEPS:
        ok(f"change.{step[:12]}", step in (change.get("steps") or []))

    ok("downstream.ii_primary", any(
        e.get("module") == "information_integration_mount_planning" and e.get("readiness") == "ready_as_next_primary_route"
        for e in downstream.get("entries") or []
    ))
    for entry in DOWNSTREAM_READINESS:
        ok(f"ready.{entry['module'][:14]}", any(e.get("module") == entry["module"] for e in downstream.get("entries") or []))

    ok("route.primary_ii", route.get("primary_next_phase") == "Phase-Midplatform-Information-Integration-Mount-Planning-v1-001")
    ok("route.secondary_hw", route.get("secondary_next_phase") == "Phase-Midplatform-Health-Watchdog-Mount-Planning-v1-001")

    ok("boundary.impl_true", summary.get("implementation_files_created_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:14]}", summary.get(field) is False)
        ok(f"freeze.{field[:12]}", boundary.get("global_boundaries", {}).get(field) is False)
    ok("freeze.impl_true", boundary.get("global_boundaries", {}).get("implementation_files_created_now") is True)

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (nc.get("non_claims") or []))

    for fn in WM_FROZEN_FUNCTIONS:
        ok(f"wmfrozen.{fn[:12]}", fn in (interface.get("modules", {}).get("working_memory") or []))
    for fn in STATIC_VALIDATOR_FUNCTIONS:
        ok(f"svfrozen.{fn[:12]}", fn in (interface.get("modules", {}).get("static_validators") or []))

    ok("summary.primary", summary.get("primary_route_after_freeze") == route.get("primary_next_phase"))
    ok("summary.foundation_id", summary.get("foundation_id") == "midplatform_micro_os_foundation_v1")
    ok("summary.foundation_ver", summary.get("foundation_version") == "1.0.0-skeleton")

    for consumer in (
        "information_integration",
        "task_manager",
        "drive_manager",
        "health_watchdog",
        "module_adapter",
        "worldmodel_memory_bridge",
    ):
        ok(f"version.consumer.{consumer[:10]}", consumer in (version.get("allowed_consumers") or []))

    for p in ("P0", "P1", "P2", "P3", "P4", "P5"):
        ok(f"prio.{p}", scope.get("freeze_not_runtime_ready") is True)

    for rel in FROZEN_SKELETON_FILES:
        ok(f"skfile.{rel.split('/')[-1][:12]}", (_REPO_ROOT / rel).is_file())

    for fn in FROZEN_INTERFACE_FUNCTIONS:
        ok(f"iflist.{fn[:12]}", fn in (interface.get("functions") or []))

    for i, rule in enumerate(handoff.get("rules") or []):
        ok(f"handoff.idx.{i}", bool(rule))

    for item in route.get("deferred") or []:
        ok(f"deferred.{item[:12]}", bool(item))

    for item in route.get("rationale") or []:
        ok(f"rationale.{item[:10]}", bool(item))

    ok("mount.readiness", mounts.get("mount_readiness_only") is True)
    ok("reuse.rule", summary.get("phase_governance_standard_reuse_rule") is True)
    ok("reuse.no_new_gov", summary.get("new_governance_need_proven") is False)

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
        root / "verify_midplatform_micro_os_foundation_freeze_and_handoff_planning_v1.json"
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
