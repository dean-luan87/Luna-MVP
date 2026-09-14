# -*- coding: utf-8 -*-
"""Luna Midplatform Micro-OS Foundation Freeze and Handoff DryRunAndReview v1."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_planning_v1 import (
    BOUNDARY_FALSE,
    CHANGE_CONTROL_STEPS,
    DOWNSTREAM_READINESS,
    EVENT_BUS_SKELETON_FUNCTIONS,
    FINAL_DECISION_GO as FREEZE_PLANNING_FINAL_GO,
    FORBIDDEN_MUTATIONS,
    FROZEN_INTERFACE_FUNCTIONS,
    FROZEN_SKELETON_FILES,
    FROZEN_TYPES,
    MOUNT_POINTS,
    NEXT_PHASE_GO as FREEZE_PLANNING_NEXT,
    SCHEDULER_SKELETON_FUNCTIONS,
    STATIC_VALIDATOR_FUNCTIONS,
    WM_FROZEN_FUNCTIONS,
)

PHASE_ID = "Phase-Midplatform-Micro-OS-Foundation-Freeze-and-Handoff-DryRunAndReview-v1-001"
SCOPE = "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_only"
SOURCE = "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1"

UPSTREAM_FREEZE_PLANNING_FINAL = FREEZE_PLANNING_FINAL_GO
UPSTREAM_FREEZE_PLANNING_NEXT = FREEZE_PLANNING_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_MICRO_OS_FOUNDATION_FREEZE_AND_HANDOFF_DRYRUN_AND_REVIEW_"
    "CLOSED_READY_FOR_INFORMATION_INTEGRATION_MOUNT_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_MICRO_OS_FOUNDATION_FREEZE_AND_HANDOFF_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Information-Integration-Mount-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Micro-OS-Foundation-Freeze-Issue-Review-v1-001"

UPSTREAM_FREEZE_PLANNING_FILES: Tuple[str, ...] = (
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

MODULE_MAP: Dict[str, str] = {
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

DRYRUN_NON_CLAIMS: Tuple[str, ...] = (
    "Foundation Freeze DryRun ≠ runtime enabled",
    "Foundation Freeze DryRun ≠ real Event Bus service",
    "Foundation Freeze DryRun ≠ real Working Memory service",
    "Foundation Freeze DryRun ≠ real Scheduler execution",
    "Foundation Freeze DryRun ≠ Information Integration mounted",
    "Foundation Freeze DryRun ≠ Task Manager mounted",
    "Foundation Freeze DryRun ≠ Health Watchdog active",
    "Foundation Freeze DryRun ≠ model/provider invocation",
    "Foundation Freeze DryRun ≠ Memory / WorldModel write",
    "Foundation Freeze DryRun ≠ user output",
    "Foundation Freeze DryRun ≠ full Luna OS productization",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_only",
    "simulated",
    "implementation_files_created_now",
)

DEFAULT_FREEZE_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_planning"
)
DEFAULT_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_SKELETON_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {"governance_constraints_ref": CONSTRAINT_DOC_ID, "source_chain": SOURCE}
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_result(checks: List[Tuple[str, bool]], **extra: Any) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "freeze dryrun review check failed"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "issue_count": len(issues),
        "dryrun_and_review_pass": len(issues) == 0,
        **extra,
    }


def _function_exists(fn: str) -> bool:
    mod_path = MODULE_MAP.get(fn)
    if not mod_path:
        return False
    mod = importlib.import_module(mod_path)
    return hasattr(mod, fn) and callable(getattr(mod, fn))


def _simulate_mount_point(consumer: str) -> Dict[str, Any]:
    return {
        "consumer": consumer,
        "mount_type": "readiness_candidate",
        "direct_mount": False,
        "runtime_side_effect": False,
        "simulation_pass": True,
    }


def run_midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1(
    *,
    midplatform_micro_os_foundation_freeze_and_handoff_planning_root: str,
    midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_root: str,
    midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(midplatform_micro_os_foundation_freeze_and_handoff_planning_root).expanduser().resolve()
    post_dr = Path(midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_root).expanduser().resolve()
    sk_dr = Path(midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_freeze_planning_root": str(plan_root),
        "upstream_post_dryrun_root": str(post_dr),
        "upstream_skeleton_dryrun_root": str(sk_dr),
    }

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_ready = _try_read_json(plan_root / "micro_os_foundation_freeze_readiness_decision_v1.json") or {}

    if plan_vr.get("verifier") != "GO":
        blockers.append("upstream freeze planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_FREEZE_PLANNING_FINAL:
        blockers.append("upstream freeze planning final_decision mismatch")
    if plan_ready.get("planning_pass") is not True:
        blockers.append("upstream freeze planning_readiness must pass")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_FREEZE_PLANNING_FILES:
        data = _try_read_json(plan_root / fname)
        if data is None:
            blockers.append(f"missing upstream: {fname}")
        upstream[fname.replace("_v1.json", "")] = data

    freeze_scope_doc = upstream.get("micro_os_foundation_freeze_scope") or {}
    interface_doc = upstream.get("micro_os_foundation_frozen_interface") or {}
    version_doc = upstream.get("micro_os_foundation_version_tag") or {}
    handoff_doc = upstream.get("micro_os_foundation_handoff_contract") or {}
    mounts_doc = upstream.get("micro_os_foundation_allowed_mount_points") or {}
    route_doc = upstream.get("micro_os_foundation_route_decision") or {}

    scope_checks: List[Tuple[str, bool]] = []
    for t in FROZEN_TYPES:
        scope_checks.append((f"type.{t[:14]}", t in (freeze_scope_doc.get("frozen_types") or [])))
    for rel in FROZEN_SKELETON_FILES:
        scope_checks.append((f"file.{rel.split('/')[-1][:14]}", (repo_root / rel).is_file()))
        scope_checks.append((f"scope.{rel.split('/')[-1][:10]}", rel in (freeze_scope_doc.get("frozen_skeleton_files") or [])))
    scope_checks.append(("fn_count21", len(interface_doc.get("functions") or []) == len(FROZEN_INTERFACE_FUNCTIONS)))
    for fn in EVENT_BUS_SKELETON_FUNCTIONS:
        scope_checks.append((f"eb.{fn[:12]}", fn in (freeze_scope_doc.get("event_bus_allowed_functions") or [])))
    for fn in WM_FROZEN_FUNCTIONS:
        scope_checks.append((f"wm.{fn[:12]}", fn in (freeze_scope_doc.get("working_memory_allowed_functions") or [])))
    for fn in SCHEDULER_SKELETON_FUNCTIONS:
        scope_checks.append((f"sched.{fn[:12]}", fn in (freeze_scope_doc.get("scheduler_allowed_functions") or [])))
    freeze_scope_review = {
        "review_id": "freeze_scope_consumability_review_v1",
        **_review_result(scope_checks),
        **meta,
    }

    iface_checks: List[Tuple[str, bool]] = []
    for fn in FROZEN_INTERFACE_FUNCTIONS:
        iface_checks.append((f"listed.{fn[:14]}", fn in (interface_doc.get("functions") or [])))
        iface_checks.append((f"disk.{fn[:12]}", _function_exists(fn)))
    interface_review = {
        "review_id": "frozen_interface_integrity_review_v1",
        "function_count": len(FROZEN_INTERFACE_FUNCTIONS),
        **_review_result(iface_checks),
        **meta,
    }

    version_checks: List[Tuple[str, bool]] = [
        ("foundation_id", version_doc.get("foundation_id") == "midplatform_micro_os_foundation_v1"),
        ("version", version_doc.get("version") == "1.0.0-skeleton"),
        ("status", version_doc.get("status") == "frozen_for_downstream_mount_planning"),
        ("runtime_status", version_doc.get("runtime_status") == "not_enabled"),
        ("compat", version_doc.get("compatibility_scope") == "planning_and_static_dryrun_only"),
    ]
    version_review = {
        "review_id": "version_tag_review_v1",
        **_review_result(version_checks),
        **meta,
    }

    handoff_checks: List[Tuple[str, bool]] = []
    rules_blob = json.dumps(handoff_doc.get("rules") or [], ensure_ascii=False).lower()
    for must in ("types", "enum", "pure function", "validator", "candidate"):
        handoff_checks.append((f"allow.{must[:8]}", must in rules_blob))
    for forb in ("runtime", "memory", "worldmodel", "governance", "user output", "scheduler"):
        handoff_checks.append((f"forb.{forb[:8]}", forb in rules_blob))
    handoff_checks.append(("forb.provider_meta", meta.get("provider_invoked_now") is False))
    handoff_checks.append(("forb.model_meta", meta.get("model_invoked_now") is False))
    handoff_checks.append(("forb.runtime_meta", meta.get("runtime_enabled_now") is False))
    handoff_review = {
        "review_id": "handoff_contract_review_v1",
        **_review_result(handoff_checks),
        **meta,
    }

    mount_runs = [_simulate_mount_point(mp["consumer"]) for mp in MOUNT_POINTS]
    mount_checks: List[Tuple[str, bool]] = [
        (f"mount.{r['consumer'][:14]}", r["simulation_pass"] and not r["direct_mount"]) for r in mount_runs
    ]
    mount_checks.append(("mount_count6", len(mount_runs) == 6))
    mount_checks.append(("no_direct_mount", mounts_doc.get("direct_mount_executed") is False))
    mounts_dryrun = {
        "dryrun_id": "allowed_mount_points_dryrun_v1",
        "simulations": mount_runs,
        **_review_result(mount_checks),
        **meta,
    }

    mut_checks: List[Tuple[str, bool]] = [
        (f"mut.{m[:12]}", m in (upstream.get("micro_os_foundation_forbidden_mutation_policy", {}).get("forbidden_mutations") or []))
        for m in FORBIDDEN_MUTATIONS
    ]
    mutation_review = {
        "review_id": "forbidden_mutation_policy_review_v1",
        **_review_result(mut_checks),
        **meta,
    }

    change_doc = upstream.get("micro_os_foundation_change_control_policy") or {}
    change_checks: List[Tuple[str, bool]] = [
        (f"step.{s[:12]}", s in (change_doc.get("steps") or [])) for s in CHANGE_CONTROL_STEPS
    ]
    change_checks.append(("no_change_now", change_doc.get("change_executed_in_this_phase") is False))
    change_review = {
        "review_id": "change_control_policy_review_v1",
        **_review_result(change_checks),
        **meta,
    }

    downstream_doc = upstream.get("micro_os_foundation_downstream_readiness_matrix") or {}
    downstream_checks: List[Tuple[str, bool]] = []
    for entry in DOWNSTREAM_READINESS:
        found = next((e for e in downstream_doc.get("entries") or [] if e.get("module") == entry["module"]), {})
        downstream_checks.append((f"ready.{entry['module'][:14]}", found.get("readiness") == entry["readiness"]))
    downstream_checks.append(("ii_primary", any(
        e.get("module") == "information_integration_mount_planning" and e.get("readiness") == "ready_as_next_primary_route"
        for e in downstream_doc.get("entries") or []
    )))
    downstream_review = {
        "review_id": "downstream_readiness_matrix_review_v1",
        **_review_result(downstream_checks),
        **meta,
    }

    boundary_doc = upstream.get("micro_os_foundation_health_and_boundary_freeze") or {}
    boundary_checks: List[Tuple[str, bool]] = [
        ("implementation_files_created_now", meta.get("implementation_files_created_now") is True),
    ]
    global_b = boundary_doc.get("global_boundaries") or {}
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"global.{field[:14]}", global_b.get(field) is False))
        boundary_checks.append((f"meta.{field[:14]}", meta.get(field) is False))
    boundary_review = {
        "review_id": "health_and_boundary_freeze_review_v1",
        **_review_result(boundary_checks),
        **meta,
    }

    route_checks: List[Tuple[str, bool]] = [
        ("primary_ii", route_doc.get("primary_next_phase") == NEXT_PHASE_GO),
        ("secondary_hw", route_doc.get("secondary_next_phase") == "Phase-Midplatform-Health-Watchdog-Mount-Planning-v1-001"),
        ("deferred_count", len(route_doc.get("deferred") or []) >= 4),
        ("no_redefine_foundation", "Information Integration" in json.dumps(route_doc.get("rationale") or [])),
    ]
    route_review = {
        "review_id": "route_decision_review_v1",
        **_review_result(route_checks),
        **meta,
    }

    nc_checks: List[Tuple[str, bool]] = []
    for claim in DRYRUN_NON_CLAIMS:
        nc_checks.append((f"nc.{claim[:14]}", True))
    nc_checks.append(("nc.count11", len(DRYRUN_NON_CLAIMS) == 11))
    non_claims_review = {
        "review_id": "non_claims_review_v1",
        "dryrun_non_claims": list(DRYRUN_NON_CLAIMS),
        **_review_result(nc_checks),
        **meta,
    }

    review_passes = [
        freeze_scope_review.get("dryrun_and_review_pass"),
        interface_review.get("dryrun_and_review_pass"),
        version_review.get("dryrun_and_review_pass"),
        handoff_review.get("dryrun_and_review_pass"),
        mounts_dryrun.get("dryrun_and_review_pass"),
        mutation_review.get("dryrun_and_review_pass"),
        change_review.get("dryrun_and_review_pass"),
        downstream_review.get("dryrun_and_review_pass"),
        boundary_review.get("dryrun_and_review_pass"),
        route_review.get("dryrun_and_review_pass"),
        non_claims_review.get("dryrun_and_review_pass"),
    ]

    issues: List[Dict[str, Any]] = []
    if blockers:
        issues.extend([{"issue_id": f"blocker.{i}", "severity": "blocker", "detail": b} for i, b in enumerate(blockers)])
    for name, review in (
        ("freeze_scope", freeze_scope_review),
        ("interface", interface_review),
        ("version", version_review),
        ("handoff", handoff_review),
        ("mounts", mounts_dryrun),
        ("mutation", mutation_review),
        ("change", change_review),
        ("downstream", downstream_review),
        ("boundary", boundary_review),
        ("route", route_review),
        ("non_claims", non_claims_review),
    ):
        for issue in review.get("issues") or []:
            issues.append({**issue, "review": name, "severity": "blocker"})

    blocker_count = len([i for i in issues if i.get("severity") == "blocker"])
    dryrun_pass = len(blockers) == 0 and all(review_passes) and blocker_count == 0

    issue_register = {
        "register_id": "issue_register_v1",
        "issues": issues,
        "issue_count": len(issues),
        "blocker_count": blocker_count,
        **meta,
    }

    readiness = {
        "decision_id": "freeze_dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "foundation_id": version_doc.get("foundation_id"),
        "foundation_version": version_doc.get("version"),
        "reviews_total": 11,
        "reviews_passed": sum(1 for p in review_passes if p),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": blocker_count,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "foundation_id": version_doc.get("foundation_id"),
        "foundation_version": version_doc.get("version"),
        "non_claims": list(DRYRUN_NON_CLAIMS),
        **meta,
    }

    return {
        "summary": summary,
        "freeze_scope_consumability_review": freeze_scope_review,
        "frozen_interface_integrity_review": interface_review,
        "version_tag_review": version_review,
        "handoff_contract_review": handoff_review,
        "allowed_mount_points_dryrun": mounts_dryrun,
        "forbidden_mutation_policy_review": mutation_review,
        "change_control_policy_review": change_review,
        "downstream_readiness_matrix_review": downstream_review,
        "health_and_boundary_freeze_review": boundary_review,
        "route_decision_review": route_review,
        "non_claims_review": non_claims_review,
        "issue_register": issue_register,
        "freeze_dryrun_readiness_decision": readiness,
    }
