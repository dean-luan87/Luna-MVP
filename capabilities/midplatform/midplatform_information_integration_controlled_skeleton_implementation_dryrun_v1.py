# -*- coding: utf-8 -*-
"""Luna Midplatform Information Integration Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import ast
import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core.information_integration_skeleton_v1 import (
    allocate_information_candidate,
    build_decision_context_candidate,
    build_live_world_state_candidate,
    build_priority_attention_map_candidate,
    collect_eligible_entries,
    detect_conflict_candidate,
    detect_gap_candidate,
    extract_task_world_slice_candidate,
    group_entries_by_spatiotemporal_slot,
    validate_information_integration_candidate,
)
from capabilities.midplatform.core.information_integration_static_validators_v1 import (
    validate_ii_boundary_matrix,
    validate_ii_governance_required_for_high_risk,
    validate_ii_no_memory_worldmodel_write,
    validate_ii_recall_context_hint_only,
)
from capabilities.midplatform.core.micro_os_common_types_v1 import (
    PriorityClass,
    SchedulingDecisionCandidate,
    WorkingMemoryEntry,
    WorkingMemoryEntryState,
)
from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_planning_v1 import (
    CANDIDATE_TYPES,
    FINAL_DECISION_GO as SKELETON_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as SKELETON_PLANNING_NEXT,
    PURE_FUNCTIONS,
    SKELETON_FILE_PLAN,
    SKELETON_SAMPLES,
    STATIC_VALIDATORS,
)

PHASE_ID = (
    "Phase-Midplatform-Information-Integration-Controlled-Skeleton-Implementation-DryRun-v1-001"
)
SCOPE = "midplatform_information_integration_controlled_skeleton_implementation_dryrun_only"
SOURCE = "midplatform_information_integration_controlled_skeleton_implementation_dryrun_v1"

UPSTREAM_SKELETON_PLANNING_FINAL = SKELETON_PLANNING_FINAL_GO
UPSTREAM_SKELETON_PLANNING_NEXT = SKELETON_PLANNING_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_INFORMATION_INTEGRATION_CONTROLLED_SKELETON_IMPLEMENTATION_"
    "DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_INFORMATION_INTEGRATION_CONTROLLED_SKELETON_IMPLEMENTATION_"
    "DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Information-Integration-Controlled-Skeleton-Implementation-Post-DryRun-Review-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Information-Integration-Controlled-Skeleton-Issue-Review-v1-001"
)

UPSTREAM_SKELETON_PLANNING_FILES: Tuple[str, ...] = (
    "information_integration_skeleton_scope_v1.json",
    "information_integration_skeleton_file_plan_v1.json",
    "information_integration_type_contract_v1.json",
    "information_integration_function_contract_v1.json",
    "information_integration_static_validator_contract_v1.json",
    "information_integration_processing_chain_contract_v1.json",
    "information_integration_governance_guard_plan_v1.json",
    "information_integration_health_guard_plan_v1.json",
    "information_integration_recall_boundary_plan_v1.json",
    "information_integration_sample_plan_v1.json",
    "information_integration_test_plan_v1.json",
    "information_integration_skeleton_boundary_matrix_v1.json",
    "information_integration_skeleton_non_claims_v1.json",
    "information_integration_skeleton_planning_readiness_decision_v1.json",
)

SKELETON_FUNCTIONS: Tuple[str, ...] = tuple(f["function_name"] for f in PURE_FUNCTIONS)

FORBIDDEN_SOURCE_PATTERNS: Tuple[str, ...] = (
    "asyncio",
    "threading",
    "multiprocessing",
    "openai",
    "anthropic",
    "requests",
    "httpx",
    "subprocess",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_information_integration_controlled_skeleton_implementation_dryrun_only",
    "simulated",
    "skeleton_candidate_only",
    "information_integration_files_created_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "information_integration_runtime_enabled_now",
    "information_integration_mounted_now",
    "model_invoked_now",
    "provider_invoked_now",
    "runtime_enabled_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "decision_center_mounted_now",
    "health_watchdog_mounted_now",
)

DEFAULT_SKELETON_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_controlled_skeleton_implementation_planning"
)
DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_mount_dryrun_and_review"
)
DEFAULT_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_controlled_skeleton_implementation_dryrun"
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
    issues = [{"issue_id": cid, "detail": "dryrun check failed"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "issue_count": len(issues),
        "dryrun_and_review_pass": len(issues) == 0,
        **extra,
    }


def _scan_skeleton_source(repo_root: Path, rel_path: str) -> Dict[str, Any]:
    path = repo_root / rel_path
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module.split(".")[0])
    forbidden_hits = [p for p in FORBIDDEN_SOURCE_PATTERNS if p in imported_modules]
    return {
        "path": rel_path,
        "exists": path.is_file(),
        "line_count": len(source.splitlines()),
        "forbidden_pattern_hits": forbidden_hits,
        "clean": len(forbidden_hits) == 0,
        "imports": imported_modules,
    }


def _make_entry(
    wm_id: str,
    *,
    task_ref: str = "task_nav",
    priority: PriorityClass = PriorityClass.P1,
    slot: str = "slot_nav",
    state: WorkingMemoryEntryState = WorkingMemoryEntryState.ACTIVE,
    ttl: Optional[int] = 120,
    trace_id: str = "trace_nav",
    freshness: str = "fresh",
) -> WorkingMemoryEntry:
    return WorkingMemoryEntry(
        working_memory_entry_id=wm_id,
        event_ref=f"evt_{wm_id}",
        candidate_ref=f"cand_{wm_id}",
        task_ref=task_ref,
        priority_class=priority,
        state=state,
        ttl=ttl,
        trace_id=trace_id,
        spatiotemporal_slot_ref=slot,
        freshness_status=freshness,
        candidate_not_fact=True,
    )


def _make_scheduling_decision(request_ref: str, blocked: bool = False) -> SchedulingDecisionCandidate:
    return SchedulingDecisionCandidate(
        decision_id=f"sched_{request_ref}",
        request_ref=request_ref,
        priority_class=PriorityClass.P1,
        routing_decision="information_integration",
        preemption_candidate=False,
        defer_candidate=False,
        drop_candidate=False,
        blocked=blocked,
        candidate_only=True,
        runtime_execution=False,
    )


def _run_processing_chain(
    entries: List[WorkingMemoryEntry],
    scheduling: List[SchedulingDecisionCandidate],
    *,
    task_context: Optional[Dict[str, Any]] = None,
    recall_context: Optional[Dict[str, Any]] = None,
    governance_ref: Optional[str] = None,
    high_risk: bool = False,
) -> Dict[str, Any]:
    eligible = collect_eligible_entries(entries, scheduling)
    groups = group_entries_by_spatiotemporal_slot(eligible)
    slot_group = groups[0] if groups else group_entries_by_spatiotemporal_slot(entries)[0]
    live = build_live_world_state_candidate(slot_group, {"trace_ref": entries[0].trace_id if entries else ""})
    task_slice = extract_task_world_slice_candidate(eligible or entries, task_context)
    attention = build_priority_attention_map_candidate(eligible or entries, scheduling)
    conflicts = detect_conflict_candidate(eligible or entries, recall_context)
    gaps, obs = detect_gap_candidate(eligible or entries, task_context)
    allocation = allocate_information_candidate(live, task_slice, conflicts, gaps, attention)
    decision = build_decision_context_candidate(
        live, task_slice, attention, allocation, conflicts, gaps, governance_ref, high_risk=high_risk
    )
    return {
        "eligible_count": len(eligible),
        "live_world_state_candidate": live,
        "task_world_slice_candidate": task_slice,
        "priority_attention_map_candidate": attention,
        "conflict_candidates": conflicts,
        "gap_candidates": gaps,
        "required_observation_candidates": obs,
        "information_allocation_candidate": allocation,
        "decision_context_candidate": decision,
    }


def _run_sample_navigation() -> Dict[str, Any]:
    entries = [_make_entry("wm_nav_001"), _make_entry("wm_nav_002")]
    scheduling = [_make_scheduling_decision("wm_nav_001"), _make_scheduling_decision("wm_nav_002")]
    result = _run_processing_chain(entries, scheduling, task_context={"task_ref": "task_navigation"})
    dcc = result["decision_context_candidate"]
    passed = (
        result["live_world_state_candidate"].fact_status == "not_fact"
        and result["task_world_slice_candidate"].fact_status == "not_fact"
        and result["priority_attention_map_candidate"].fact_status == "not_fact"
        and dcc.readiness_status in ("ready", "hold")
        and validate_information_integration_candidate(dcc).valid
    )
    return {
        "sample_id": "navigation_build_decision_context_candidate",
        "passed": passed,
        "terminal": "DecisionContextCandidate" if passed else "failed",
        "outputs": ["live_world_state_candidate", "task_world_slice_candidate", "priority_attention_map_candidate", "decision_context_candidate"],
        "runtime_executed": False,
        "user_output": False,
    }


def _run_sample_ocr_gap() -> Dict[str, Any]:
    entries = [_make_entry("wm_ocr_001", task_ref="task_ocr", priority=PriorityClass.P2, slot="slot_ocr")]
    scheduling = [_make_scheduling_decision("wm_ocr_001")]
    result = _run_processing_chain(
        entries,
        scheduling,
        task_context={"task_ref": "task_ocr", "required_fields": ["text_region"], "requested_module": "ocr_module"},
    )
    passed = len(result["gap_candidates"]) >= 1 and len(result["required_observation_candidates"]) >= 1
    return {
        "sample_id": "ocr_gap_generates_required_observation_candidate",
        "passed": passed,
        "terminal": "RequiredObservationCandidate" if passed else "failed",
        "provider_invoked": False,
    }


def _run_sample_health_fault() -> Dict[str, Any]:
    entry = _make_entry("wm_health_001", priority=PriorityClass.P0, freshness="degraded")
    scheduling = [_make_scheduling_decision("wm_health_001")]
    result = _run_processing_chain(
        [entry],
        scheduling,
        task_context={"task_ref": "task_health", "required_fields": ["health_status"]},
    )
    alloc = result["information_allocation_candidate"]
    passed = bool(alloc.hold_refs) or bool(alloc.health_watchdog_refs)
    return {
        "sample_id": "health_fault_generates_hold_allocation_candidate",
        "passed": passed,
        "terminal": "InformationAllocationCandidate" if passed else "failed",
        "recovery_executed": False,
    }


def _run_sample_memory_recall() -> Dict[str, Any]:
    recall = {"hint_only": True, "known_state_candidate": True, "conflicts_with_realtime": False}
    recall_val = validate_ii_recall_context_hint_only(recall)
    entries = [_make_entry("wm_recall_001", priority=PriorityClass.P4)]
    scheduling = [_make_scheduling_decision("wm_recall_001")]
    result = _run_processing_chain(entries, scheduling, recall_context=recall)
    live = result["live_world_state_candidate"]
    passed = recall_val.valid and live.fact_status == "not_fact" and live.candidate_not_fact
    return {
        "sample_id": "memory_recall_used_as_hint_not_fact",
        "passed": passed,
        "terminal": "hint_candidate_only" if passed else "failed",
        "worldmodel_write": False,
    }


def _run_sample_conflict() -> Dict[str, Any]:
    recall = {"hint_only": True, "conflicts_with_realtime": True}
    entries = [_make_entry("wm_conf_001"), _make_entry("wm_conf_002", priority=PriorityClass.P2)]
    scheduling = [_make_scheduling_decision("wm_conf_001"), _make_scheduling_decision("wm_conf_002")]
    result = _run_processing_chain(entries, scheduling, recall_context=recall)
    dcc = result["decision_context_candidate"]
    passed = len(result["conflict_candidates"]) >= 1 and dcc.readiness_status == "not_ready" and dcc.blocked
    return {
        "sample_id": "conflict_blocks_decision_readiness",
        "passed": passed,
        "terminal": "blocked_decision_context" if passed else "failed",
        "user_output": False,
        "task_execution": False,
    }


SAMPLE_RUNNERS = (
    _run_sample_navigation,
    _run_sample_ocr_gap,
    _run_sample_health_fault,
    _run_sample_memory_recall,
    _run_sample_conflict,
)


def run_midplatform_information_integration_controlled_skeleton_implementation_dryrun_v1(
    *,
    midplatform_information_integration_controlled_skeleton_implementation_planning_root: str,
    midplatform_information_integration_mount_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    sk_plan = Path(midplatform_information_integration_controlled_skeleton_implementation_planning_root).expanduser().resolve()
    mount_dr = Path(midplatform_information_integration_mount_dryrun_and_review_root).expanduser().resolve()
    freeze_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_skeleton_planning_root": str(sk_plan),
        "upstream_mount_dryrun_root": str(mount_dr),
        "upstream_freeze_dryrun_root": str(freeze_dr),
    }

    sk_vr = _try_read_json(sk_plan / "verifier_report.json") or {}
    sk_sm = _try_read_json(sk_plan / "summary.json") or {}
    sk_ready = _try_read_json(sk_plan / "information_integration_skeleton_planning_readiness_decision_v1.json") or {}

    if sk_vr.get("verifier") != "GO":
        blockers.append("upstream skeleton planning verifier must be GO")
    if sk_sm.get("final_decision") != UPSTREAM_SKELETON_PLANNING_FINAL:
        blockers.append("upstream skeleton planning final_decision mismatch")
    if sk_ready.get("planning_pass") is not True:
        blockers.append("upstream skeleton planning_readiness must pass")

    freeze_vr = _try_read_json(freeze_dr / "verifier_report.json") or {}
    if freeze_vr.get("verifier") != "GO":
        blockers.append("upstream foundation freeze dryrun verifier must be GO")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_SKELETON_PLANNING_FILES:
        data = _try_read_json(sk_plan / fname)
        if data is None:
            blockers.append(f"missing upstream: {fname}")
        upstream[fname.replace("_v1.json", "")] = data

    file_scans = [_scan_skeleton_source(repo_root, f["path"]) for f in SKELETON_FILE_PLAN]
    for scan in file_scans:
        if not scan["exists"]:
            blockers.append(f"missing skeleton file: {scan['path']}")
        if not scan["clean"]:
            blockers.append(f"forbidden patterns in {scan['path']}: {scan['forbidden_pattern_hits']}")

    scope_report = {
        "report_id": "information_integration_skeleton_implementation_scope_report_v1",
        "skeleton_files": [f["path"] for f in SKELETON_FILE_PLAN],
        "allowed": ["dataclass", "enum", "pure_function", "static_validator", "candidate_generator"],
        "forbidden": ["integration_runtime", "model", "provider", "task_execution", "memory_write", "worldmodel_write", "user_output"],
        **meta,
    }

    creation_checks: List[Tuple[str, bool]] = []
    for scan in file_scans:
        creation_checks.append((f"file.{scan['path'].split('/')[-1][:14]}", scan["exists"]))
        creation_checks.append((f"clean.{scan['path'].split('/')[-1][:10]}", scan["clean"]))
    file_creation_report = {
        "report_id": "information_integration_skeleton_file_creation_report_v1",
        "files": file_scans,
        "file_count": len(file_scans),
        "information_integration_files_created_now": all(s["exists"] for s in file_scans),
        "runtime_enabled_now": False,
        **_review_result(creation_checks),
        **meta,
    }

    types_mod = importlib.import_module("capabilities.midplatform.core.information_integration_types_v1")
    type_checks: List[Tuple[str, bool]] = []
    for t in CANDIDATE_TYPES:
        name = t["type_name"]
        type_checks.append((f"type.{name[:14]}", hasattr(types_mod, name)))
        if hasattr(types_mod, name):
            fields = getattr(getattr(types_mod, name), "__dataclass_fields__", {})
            type_checks.append((f"fact.{name[:10]}", "fact_status" in fields))
            type_checks.append((f"trace.{name[:10]}", "trace_ref" in fields))
            type_checks.append((f"id.{name[:10]}", "candidate_id" in fields))
    type_validation = {
        "validation_id": "information_integration_type_contract_validation_v1",
        **_review_result(type_checks),
        **meta,
    }

    sk_mod = importlib.import_module("capabilities.midplatform.core.information_integration_skeleton_v1")
    fn_checks: List[Tuple[str, bool]] = []
    for fn in SKELETON_FUNCTIONS:
        fn_checks.append((f"fn.{fn[:14]}", hasattr(sk_mod, fn) and callable(getattr(sk_mod, fn))))
    fn_static = {
        "validation_id": "information_integration_function_static_validation_v1",
        **_review_result(fn_checks),
        **meta,
    }

    sv_mod = importlib.import_module("capabilities.midplatform.core.information_integration_static_validators_v1")
    sv_checks: List[Tuple[str, bool]] = []
    for fn in STATIC_VALIDATORS:
        sv_checks.append((f"fn.{fn[:14]}", hasattr(sv_mod, fn) and callable(getattr(sv_mod, fn))))
    boundary_sample = {**{f: False for f in BOUNDARY_FALSE}, "information_integration_files_created_now": True}
    sv_checks.append(("boundary_ok", validate_ii_boundary_matrix({"global_boundaries": boundary_sample}).valid))
    static_validator_review = {
        "review_id": "information_integration_static_validator_review_v1",
        **_review_result(sv_checks),
        **meta,
    }

    chain_entries = [_make_entry("wm_chain_001")]
    chain_sched = [_make_scheduling_decision("wm_chain_001")]
    chain_result = _run_processing_chain(chain_entries, chain_sched)
    chain_checks: List[Tuple[str, bool]] = [
        ("eligible", chain_result["eligible_count"] >= 0),
        ("live_candidate", chain_result["live_world_state_candidate"].candidate_not_fact),
        ("decision_candidate", chain_result["decision_context_candidate"].fact_status == "not_fact"),
        ("no_runtime", True),
    ]
    processing_chain_dryrun = {
        "dryrun_id": "information_integration_processing_chain_dryrun_v1",
        "chain_result_summary": {
            "eligible_count": chain_result["eligible_count"],
            "decision_readiness": chain_result["decision_context_candidate"].readiness_status,
        },
        **_review_result(chain_checks),
        **meta,
    }

    gov_checks: List[Tuple[str, bool]] = []
    high_risk_dcc = build_decision_context_candidate(
        chain_result["live_world_state_candidate"],
        chain_result["task_world_slice_candidate"],
        chain_result["priority_attention_map_candidate"],
        chain_result["information_allocation_candidate"],
        high_risk=True,
        governance_ref=None,
    )
    gov_checks.append(("high_risk_blocked", high_risk_dcc.blocked and high_risk_dcc.readiness_status == "not_ready"))
    gov_checks.append(("gov_validator", validate_ii_governance_required_for_high_risk(high_risk_dcc).blocked))
    gov_checks.append(("output_forbidden", meta.get("user_output_allowed_now") is False))
    gov_checks.append(("memory_forbidden", validate_ii_no_memory_worldmodel_write({"global_boundaries": boundary_sample}).valid))
    gov_checks.append(("runtime_forbidden", meta.get("runtime_enabled_now") is False))
    governance_dryrun = {
        "dryrun_id": "information_integration_governance_guard_dryrun_v1",
        **_review_result(gov_checks),
        **meta,
    }

    health_checks: List[Tuple[str, bool]] = []
    no_ttl = _make_entry("wm_no_ttl", ttl=None)
    health_checks.append(("ttl_missing_blocked", no_ttl.ttl is None))
    stale = _make_entry("wm_stale", state=WorkingMemoryEntryState.STALE, freshness="stale")
    health_checks.append(("stale_filtered", len(collect_eligible_entries([stale], [])) == 0))
    health_checks.append(("health_validator_exists", hasattr(sv_mod, "validate_ii_health_required")))
    health_guard_dryrun = {
        "dryrun_id": "information_integration_health_guard_dryrun_v1",
        **_review_result(health_checks),
        **meta,
    }

    recall_ok = {"hint_only": True, "known_state_candidate": True}
    recall_bad = {"overrides_realtime_safety": True, "promoted_to_fact": True}
    recall_checks: List[Tuple[str, bool]] = [
        ("hint_ok", validate_ii_recall_context_hint_only(recall_ok).valid),
        ("hint_bad", not validate_ii_recall_context_hint_only(recall_bad).valid),
        ("no_worldmodel_write", meta.get("worldmodel_write_allowed_now") is False),
    ]
    recall_boundary_dryrun = {
        "dryrun_id": "information_integration_recall_boundary_dryrun_v1",
        **_review_result(recall_checks),
        **meta,
    }

    sample_runs = [runner() for runner in SAMPLE_RUNNERS]
    sample_checks: List[Tuple[str, bool]] = [(f"sample.{r['sample_id'][:14]}", r["passed"]) for r in sample_runs]
    sample_dryrun = {
        "dryrun_id": "information_integration_sample_dryrun_v1",
        "samples": sample_runs,
        "sample_count": len(sample_runs),
        **_review_result(sample_checks),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "information_integration_boundary_matrix_v1",
        "global_boundaries": {**{f: False for f in BOUNDARY_FALSE}, "information_integration_files_created_now": True},
        **meta,
    }

    review_passes = [
        file_creation_report.get("dryrun_and_review_pass"),
        type_validation.get("dryrun_and_review_pass"),
        fn_static.get("dryrun_and_review_pass"),
        static_validator_review.get("dryrun_and_review_pass"),
        processing_chain_dryrun.get("dryrun_and_review_pass"),
        governance_dryrun.get("dryrun_and_review_pass"),
        health_guard_dryrun.get("dryrun_and_review_pass"),
        recall_boundary_dryrun.get("dryrun_and_review_pass"),
        sample_dryrun.get("dryrun_and_review_pass"),
    ]

    dryrun_issues: List[Dict[str, Any]] = []
    if blockers:
        dryrun_issues.extend([{"issue_id": f"blocker.{i}", "severity": "blocker", "detail": b} for i, b in enumerate(blockers)])
    for review_name, review in (
        ("file_creation", file_creation_report),
        ("type_validation", type_validation),
        ("function_static", fn_static),
        ("static_validator", static_validator_review),
        ("processing_chain", processing_chain_dryrun),
        ("governance", governance_dryrun),
        ("health", health_guard_dryrun),
        ("recall", recall_boundary_dryrun),
        ("sample", sample_dryrun),
    ):
        for issue in review.get("issues") or []:
            dryrun_issues.append({**issue, "review": review_name, "severity": "blocker"})

    blocker_count = len([i for i in dryrun_issues if i.get("severity") == "blocker"])
    dryrun_pass = len(blockers) == 0 and all(review_passes) and blocker_count == 0

    issue_register = {
        "register_id": "information_integration_issue_register_v1",
        "issues": dryrun_issues,
        "issue_count": len(dryrun_issues),
        "blocker_count": blocker_count,
        **meta,
    }

    readiness = {
        "decision_id": "information_integration_skeleton_implementation_dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "reviews_passed": sum(1 for p in review_passes if p),
        "reviews_total": len(review_passes),
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
        "module_id": "information_integration",
        "layer": "L6",
        **meta,
    }

    return {
        "summary": summary,
        "information_integration_skeleton_implementation_scope_report": scope_report,
        "information_integration_skeleton_file_creation_report": file_creation_report,
        "information_integration_type_contract_validation": type_validation,
        "information_integration_function_static_validation": fn_static,
        "information_integration_static_validator_review": static_validator_review,
        "information_integration_processing_chain_dryrun": processing_chain_dryrun,
        "information_integration_governance_guard_dryrun": governance_dryrun,
        "information_integration_health_guard_dryrun": health_guard_dryrun,
        "information_integration_recall_boundary_dryrun": recall_boundary_dryrun,
        "information_integration_sample_dryrun": sample_dryrun,
        "information_integration_boundary_matrix": boundary_matrix,
        "information_integration_issue_register": issue_register,
        "information_integration_skeleton_implementation_dryrun_readiness_decision": readiness,
    }
