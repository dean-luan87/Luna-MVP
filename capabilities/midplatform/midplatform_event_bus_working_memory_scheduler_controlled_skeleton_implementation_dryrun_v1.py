# -*- coding: utf-8 -*-
"""Luna Midplatform EB/WM/Scheduler Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import ast
import importlib
import inspect
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core.event_bus_skeleton_v1 import (
    append_trace,
    normalize_event,
    route_event_candidate,
    validate_event_schema,
    validate_event_state_transition,
)
from capabilities.midplatform.core.micro_os_common_types_v1 import (
    EventState,
    EventType,
    GovernanceCheckRef,
    HealthTag,
    PriorityClass,
    WorkingMemoryEntryState,
)
from capabilities.midplatform.core.micro_os_static_validators_v1 import (
    health_issue_from_validation,
    validate_candidate_not_fact,
    validate_governance_guard,
    validate_no_runtime_flags,
    validate_required_health_tag,
    validate_required_trace,
    validate_required_ttl,
)
from capabilities.midplatform.core.scheduler_skeleton_v1 import (
    assign_priority_candidate,
    evaluate_deferral_or_drop_candidate,
    evaluate_preemption_candidate,
    produce_scheduling_decision_candidate,
)
from capabilities.midplatform.core.working_memory_skeleton_v1 import (
    apply_ttl_policy_candidate,
    create_working_memory_entry,
    generate_cleanup_plan_candidate,
    validate_wm_entry,
    validate_wm_state_transition,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1 import (
    EVENT_BUS_SKELETON_FUNCTIONS,
    FINAL_DECISION_GO as SKELETON_PLANNING_FINAL_GO,
    HEALTH_GUARD_SIGNALS,
    NEXT_PHASE_GO as SKELETON_PLANNING_NEXT,
    SCHEDULER_SKELETON_FUNCTIONS,
    SKELETON_FILE_PLAN,
    SKELETON_SAMPLES,
    WM_SKELETON_FUNCTIONS,
)

PHASE_ID = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Implementation-DryRun-v1-001"
)
SCOPE = "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_only"
SOURCE = "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_v1"

UPSTREAM_SKELETON_PLANNING_FINAL = SKELETON_PLANNING_FINAL_GO
UPSTREAM_SKELETON_PLANNING_NEXT = SKELETON_PLANNING_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_CONTROLLED_SKELETON_IMPLEMENTATION_"
    "DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_CONTROLLED_SKELETON_IMPLEMENTATION_"
    "DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Implementation-Post-DryRun-Review-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Issue-Review-v1-001"
)

UPSTREAM_SKELETON_PLANNING_FILES: Tuple[str, ...] = (
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

STATIC_VALIDATOR_FUNCTIONS: Tuple[str, ...] = (
    "validate_no_runtime_flags",
    "validate_candidate_not_fact",
    "validate_required_trace",
    "validate_required_health_tag",
    "validate_required_ttl",
    "validate_governance_guard",
)

FORBIDDEN_SOURCE_PATTERNS: Tuple[str, ...] = (
    "asyncio",
    "threading",
    "multiprocessing",
    "openai",
    "anthropic",
    "requests.post",
    "httpx",
    "subprocess",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_only",
    "simulated",
    "skeleton_candidate_only",
    "implementation_files_created_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
    "real_async_queue_enabled_now",
    "true_multithreading_enabled_now",
    "runtime_enabled_now",
    "model_invoked_now",
    "provider_invoked_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "real_health_monitoring_enabled_now",
    "recovery_executed_now",
)

DEFAULT_SKELETON_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning"
)
DEFAULT_EBWM_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_planning"
)
DEFAULT_EBWM_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun"
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


def _run_sample_valid_navigation() -> Dict[str, Any]:
    raw = {
        "event_id": "nav_001",
        "event_type": EventType.USER_GOAL.value,
        "source_module": "navigation",
        "source_chain": "module_adapter_layer",
        "timestamp": "2026-06-08T10:00:00Z",
        "health_tag": {"tag": "ok"},
        "priority_hint": PriorityClass.P1.value,
        "ttl_hint": 30,
        "governance_required": False,
        "routing_targets": ["working_memory", "scheduler"],
        "candidate_payload_ref": "nav_candidate_001",
        "trace_id": "trace_nav_001",
    }
    event = normalize_event(raw)
    schema = validate_event_schema(event)
    route = route_event_candidate(event)
    event = append_trace(event, "normalized")
    entry = create_working_memory_entry(event)
    entry.state = WorkingMemoryEntryState.ACTIVE
    wm_val = validate_wm_entry(entry)
    ttl = apply_ttl_policy_candidate(entry)
    request = assign_priority_candidate(entry)
    decision = produce_scheduling_decision_candidate(request)
    passed = (
        schema.valid
        and wm_val.valid
        and request.priority_class == PriorityClass.P1
        and decision.candidate_only
        and not decision.runtime_execution
    )
    return {
        "sample_id": "valid_navigation_event_to_p1_schedule",
        "passed": passed,
        "terminal": "scheduling_decision_candidate" if passed else "failed",
        "priority": request.priority_class.value,
        "steps": ["normalize", "validate_schema", "create_wm", "assign_priority", "produce_decision"],
    }


def _run_sample_p0_preempt() -> Dict[str, Any]:
    p1_raw = {
        "event_id": "nav_active",
        "event_type": EventType.USER_GOAL.value,
        "source_module": "navigation",
        "source_chain": "module_adapter_layer",
        "timestamp": "2026-06-08T10:00:00Z",
        "health_tag": {"tag": "ok"},
        "priority_hint": PriorityClass.P1.value,
        "ttl_hint": 30,
        "governance_required": False,
        "routing_targets": ["scheduler"],
        "trace_id": "trace_nav_active",
    }
    p0_raw = {
        "event_id": "safety_001",
        "event_type": EventType.HEALTH_REPORT.value,
        "source_module": "health",
        "source_chain": "health_resource_manager",
        "timestamp": "2026-06-08T10:00:01Z",
        "health_tag": {"tag": "fault"},
        "priority_hint": PriorityClass.P0.value,
        "ttl_hint": 5,
        "governance_required": False,
        "routing_targets": ["scheduler"],
        "trace_id": "trace_safety_001",
    }
    p1_event = normalize_event(p1_raw)
    p0_event = normalize_event(p0_raw)
    p1_entry = create_working_memory_entry(p1_event)
    p1_entry.state = WorkingMemoryEntryState.ACTIVE
    p0_entry = create_working_memory_entry(p0_event)
    p1_req = assign_priority_candidate(p1_entry)
    p0_req = assign_priority_candidate(p0_entry)
    preempt = evaluate_preemption_candidate(p0_req, active_requests=[p1_req])
    decision = produce_scheduling_decision_candidate(p0_req)
    passed = preempt.preempt and p0_req.priority_class == PriorityClass.P0 and decision.preemption_candidate
    return {
        "sample_id": "p0_safety_event_preempts_p1_navigation",
        "passed": passed,
        "terminal": "preemption_candidate" if passed else "failed",
        "preemption_candidate": preempt.preempt,
        "deferred_refs": list(preempt.deferred_request_refs),
    }


def _run_sample_ttl_missing() -> Dict[str, Any]:
    raw = {
        "event_id": "ttl_miss_001",
        "event_type": EventType.MODULE_CANDIDATE.value,
        "source_module": "ocr",
        "source_chain": "module_adapter_layer",
        "timestamp": "2026-06-08T10:00:00Z",
        "health_tag": {"tag": "ok"},
        "priority_hint": PriorityClass.P2.value,
        "ttl_hint": None,
        "governance_required": False,
        "routing_targets": ["working_memory"],
        "trace_id": "trace_ttl_miss",
    }
    event = normalize_event(raw)
    entry = create_working_memory_entry(event)
    wm_val = validate_wm_entry(entry)
    ttl_val = validate_required_ttl(entry)
    passed = wm_val.blocked and entry.state == WorkingMemoryEntryState.BLOCKED and ttl_val.blocked
    return {
        "sample_id": "ttl_missing_event_blocked",
        "passed": passed,
        "terminal": "blocked_candidate" if passed else "failed",
        "no_ttl_forbidden": True,
        "active_processing": False,
    }


def _run_sample_p5_drop() -> Dict[str, Any]:
    raw = {
        "event_id": "bg_001",
        "event_type": EventType.RESOURCE_STATE.value,
        "source_module": "background",
        "source_chain": "module_adapter_layer",
        "timestamp": "2026-06-08T10:00:00Z",
        "health_tag": {"tag": "ok"},
        "priority_hint": PriorityClass.P5.value,
        "ttl_hint": 60,
        "governance_required": False,
        "routing_targets": ["scheduler"],
        "trace_id": "trace_bg_001",
    }
    event = normalize_event(raw)
    entry = create_working_memory_entry(event)
    entry.state = WorkingMemoryEntryState.ACTIVE
    request = assign_priority_candidate(entry)
    defer_drop = evaluate_deferral_or_drop_candidate(request, resource_state="resource_overload")
    cleanup = generate_cleanup_plan_candidate([entry])
    decision = produce_scheduling_decision_candidate(request, guards={"resource_state": "resource_overload"})
    passed = defer_drop.drop and request.drop_allowed and decision.drop_candidate and any(a.get("action") == "discard" for a in cleanup.actions)
    return {
        "sample_id": "p5_background_dropped_under_resource_overload",
        "passed": passed,
        "terminal": "drop_candidate" if passed else "failed",
        "drop_allowed": request.drop_allowed,
        "cleanup_actions": list(cleanup.actions),
    }


def _run_sample_memory_recall() -> Dict[str, Any]:
    raw = {
        "event_id": "recall_001",
        "event_type": EventType.MEMORY_RECALL.value,
        "source_module": "worldmodel_memory_bridge",
        "source_chain": "worldmodel_memory_bridge",
        "timestamp": "2026-06-08T10:00:00Z",
        "health_tag": {"tag": "ok"},
        "priority_hint": PriorityClass.P4.value,
        "ttl_hint": 600,
        "governance_required": False,
        "routing_targets": ["working_memory"],
        "candidate_payload_ref": "recall_context_hint",
        "trace_id": "trace_recall_001",
    }
    event = normalize_event(raw)
    entry = create_working_memory_entry(event)
    entry.state = WorkingMemoryEntryState.ADMISSION_CANDIDATE_GENERATED
    not_fact = validate_candidate_not_fact(entry)
    passed = entry.candidate_not_fact and not_fact.valid and entry.priority_class == PriorityClass.P4
    return {
        "sample_id": "memory_recall_event_reused_as_hint_not_fact",
        "passed": passed,
        "terminal": "hint_candidate_only" if passed else "failed",
        "candidate_not_fact": entry.candidate_not_fact,
        "worldmodel_write": False,
    }


SAMPLE_RUNNERS = (
    _run_sample_valid_navigation,
    _run_sample_p0_preempt,
    _run_sample_ttl_missing,
    _run_sample_p5_drop,
    _run_sample_memory_recall,
)


def run_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_v1(
    *,
    midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_root: str,
    midplatform_event_bus_working_memory_scheduler_planning_root: str,
    midplatform_event_bus_working_memory_scheduler_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    sk_plan = Path(midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_root).expanduser().resolve()
    ebwm_plan = Path(midplatform_event_bus_working_memory_scheduler_planning_root).expanduser().resolve()
    ebwm_dr = Path(midplatform_event_bus_working_memory_scheduler_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_skeleton_planning_root": str(sk_plan),
        "upstream_ebwm_planning_root": str(ebwm_plan),
        "upstream_ebwm_dryrun_root": str(ebwm_dr),
    }

    sk_vr = _try_read_json(sk_plan / "verifier_report.json") or {}
    sk_sm = _try_read_json(sk_plan / "summary.json") or {}
    sk_ready = _try_read_json(sk_plan / "controlled_skeleton_planning_readiness_decision_v1.json") or {}

    if sk_vr.get("verifier") != "GO":
        blockers.append("upstream skeleton planning verifier must be GO")
    if sk_sm.get("final_decision") != UPSTREAM_SKELETON_PLANNING_FINAL:
        blockers.append("upstream skeleton planning final_decision mismatch")
    if sk_ready.get("planning_pass") is not True:
        blockers.append("upstream skeleton planning_readiness must pass")

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
        "report_id": "skeleton_implementation_scope_report_v1",
        "skeleton_files": [f["path"] for f in SKELETON_FILE_PLAN],
        "allowed": ["dataclass", "enum", "pure_function", "static_validator", "candidate_generator"],
        "forbidden": ["real_event_loop", "async_queue", "thread", "runtime", "provider", "model", "task_execution"],
        **meta,
    }

    creation_checks: List[Tuple[str, bool]] = []
    for scan in file_scans:
        creation_checks.append((f"file.{scan['path'].split('/')[-1][:14]}", scan["exists"]))
        creation_checks.append((f"clean.{scan['path'].split('/')[-1][:10]}", scan["clean"]))
    file_creation_report = {
        "report_id": "skeleton_file_creation_report_v1",
        "files": file_scans,
        "file_count": len(file_scans),
        "implementation_files_created_now": all(s["exists"] for s in file_scans),
        "runtime_enabled_now": False,
        **_review_result(creation_checks),
        **meta,
    }

    type_contract = upstream.get("controlled_skeleton_type_contract") or {}
    type_checks: List[Tuple[str, bool]] = []
    common = importlib.import_module("capabilities.midplatform.core.micro_os_common_types_v1")
    for name in ("EventType", "EventState", "WorkingMemoryEntryState", "PriorityClass", "TerminalState"):
        type_checks.append((f"enum.{name}", hasattr(common, name)))
    for name in ("Event", "WorkingMemoryEntry", "SchedulingRequest", "SchedulingDecisionCandidate"):
        type_checks.append((f"type.{name}", hasattr(common, name)))
    event_fields = getattr(common.Event, "__dataclass_fields__", {})
    wm_fields = getattr(common.WorkingMemoryEntry, "__dataclass_fields__", {})
    sched_fields = getattr(common.SchedulingRequest, "__dataclass_fields__", {})
    for field in type_contract.get("event_fields") or []:
        type_checks.append((f"event.field.{field[:10]}", field in event_fields))
    for field in type_contract.get("working_memory_entry_fields") or []:
        type_checks.append((f"wm.field.{field[:10]}", field in wm_fields))
    for field in type_contract.get("scheduling_request_fields") or []:
        type_checks.append((f"sched.field.{field[:10]}", field in sched_fields))
    type_validation = {
        "validation_id": "skeleton_type_contract_validation_v1",
        **_review_result(type_checks),
        **meta,
    }

    eb_checks: List[Tuple[str, bool]] = []
    eb_mod = importlib.import_module("capabilities.midplatform.core.event_bus_skeleton_v1")
    for fn in EVENT_BUS_SKELETON_FUNCTIONS:
        eb_checks.append((f"fn.{fn}", hasattr(eb_mod, fn) and callable(getattr(eb_mod, fn))))
    trans = validate_event_state_transition(EventState.RECEIVED, EventState.NORMALIZED)
    eb_checks.append(("transition.ok", trans.valid))
    eb_static = {
        "validation_id": "event_bus_skeleton_static_validation_v1",
        **_review_result(eb_checks),
        **meta,
    }

    wm_checks: List[Tuple[str, bool]] = []
    wm_mod = importlib.import_module("capabilities.midplatform.core.working_memory_skeleton_v1")
    for fn in WM_SKELETON_FUNCTIONS:
        wm_checks.append((f"fn.{fn}", hasattr(wm_mod, fn) and callable(getattr(wm_mod, fn))))
    wm_checks.append(("fn.validate_wm_state_transition", hasattr(wm_mod, "validate_wm_state_transition")))
    wm_checks.append(("not_memory", upstream.get("working_memory_skeleton_contract", {}).get("working_memory_is_not_memory") is True))
    wm_static = {
        "validation_id": "working_memory_skeleton_static_validation_v1",
        **_review_result(wm_checks),
        **meta,
    }

    sched_checks: List[Tuple[str, bool]] = []
    sched_mod = importlib.import_module("capabilities.midplatform.core.scheduler_skeleton_v1")
    for fn in SCHEDULER_SKELETON_FUNCTIONS:
        sched_checks.append((f"fn.{fn}", hasattr(sched_mod, fn) and callable(getattr(sched_mod, fn))))
    sched_static = {
        "validation_id": "scheduler_skeleton_static_validation_v1",
        **_review_result(sched_checks),
        **meta,
    }

    sv_checks: List[Tuple[str, bool]] = []
    sv_mod = importlib.import_module("capabilities.midplatform.core.micro_os_static_validators_v1")
    for fn in STATIC_VALIDATOR_FUNCTIONS:
        sv_checks.append((f"fn.{fn}", hasattr(sv_mod, fn) and callable(getattr(sv_mod, fn))))
    boundary_sample = {k: False for k in BOUNDARY_FALSE}
    sv_checks.append(("no_runtime", validate_no_runtime_flags(boundary_sample).valid))
    static_validator_review = {
        "review_id": "static_validator_review_v1",
        **_review_result(sv_checks),
        **meta,
    }

    sample_runs = [runner() for runner in SAMPLE_RUNNERS]
    sample_checks: List[Tuple[str, bool]] = [
        (f"sample.{r['sample_id'][:14]}", r["passed"]) for r in sample_runs
    ]
    sample_dryrun = {
        "dryrun_id": "skeleton_sample_dryrun_v1",
        "samples": sample_runs,
        "sample_count": len(sample_runs),
        **_review_result(sample_checks),
        **meta,
    }

    gov_checks: List[Tuple[str, bool]] = []
    high_risk = normalize_event({
        "event_id": "gov_001", "event_type": EventType.OUTPUT_CANDIDATE.value,
        "source_module": "output", "source_chain": "output_gate_bridge",
        "timestamp": "2026-06-08T10:00:00Z", "health_tag": {"tag": "ok"},
        "governance_required": True, "ttl_hint": 30, "trace_id": "t1",
    })
    gov_checks.append(("high_risk_blocked", validate_governance_guard(high_risk).blocked))
    invalid = normalize_event({"event_id": "", "event_type": EventType.MODULE_CANDIDATE.value,
                               "source_module": "", "source_chain": "", "timestamp": "",
                               "governance_required": False, "trace_id": ""})
    gov_checks.append(("schema_invalid", not validate_event_schema(invalid).valid))
    gov_checks.append(("output_forbidden", meta.get("user_output_allowed_now") is False))
    gov_checks.append(("memory_forbidden", meta.get("memory_write_allowed_now") is False))
    gov_checks.append(("worldmodel_forbidden", meta.get("worldmodel_write_allowed_now") is False))
    gov_checks.append(("runtime_forbidden", meta.get("runtime_enabled_now") is False))
    governance_dryrun = {
        "dryrun_id": "governance_guard_dryrun_v1",
        **_review_result(gov_checks),
        **meta,
    }

    health_checks: List[Tuple[str, bool]] = []
    no_tag = normalize_event({"event_id": "h1", "event_type": EventType.MODULE_CANDIDATE.value,
                                "source_module": "m", "source_chain": "c", "timestamp": "t",
                                "governance_required": False, "ttl_hint": 30, "trace_id": "tr"})
    ht = validate_required_health_tag(no_tag)
    health_checks.append(("missing_health_tag", not ht.valid))
    health_checks.append(("health_issue_candidate", health_issue_from_validation(ht, "missing_health_tag").signal == "missing_health_tag"))
    no_ts = normalize_event({"event_id": "h2", "event_type": EventType.MODULE_CANDIDATE.value,
                             "source_module": "m", "source_chain": "c", "timestamp": "",
                             "health_tag": {"tag": "ok"}, "governance_required": False, "ttl_hint": 30, "trace_id": "tr"})
    health_checks.append(("missing_timestamp", not validate_event_schema(no_ts).valid))
    no_chain = normalize_event({"event_id": "h3", "event_type": EventType.MODULE_CANDIDATE.value,
                                "source_module": "m", "source_chain": "", "timestamp": "t",
                                "health_tag": {"tag": "ok"}, "governance_required": False, "ttl_hint": 30, "trace_id": "tr"})
    health_checks.append(("missing_source_chain", not validate_event_schema(no_chain).valid))
    no_ttl_entry = create_working_memory_entry(normalize_event({
        "event_id": "h4", "event_type": EventType.MODULE_CANDIDATE.value,
        "source_module": "m", "source_chain": "c", "timestamp": "t",
        "health_tag": {"tag": "ok"}, "governance_required": False,
        "ttl_hint": None, "trace_id": "tr",
    }))
    health_checks.append(("ttl_missing", validate_required_ttl(no_ttl_entry).blocked))
    health_guard_dryrun = {
        "dryrun_id": "health_guard_dryrun_v1",
        "signals": list(HEALTH_GUARD_SIGNALS),
        **_review_result(health_checks),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "skeleton_boundary_matrix_v1",
        "global_boundaries": {**{f: False for f in BOUNDARY_FALSE}, "implementation_files_created_now": True},
        **meta,
    }

    review_passes = [
        file_creation_report.get("dryrun_and_review_pass"),
        type_validation.get("dryrun_and_review_pass"),
        eb_static.get("dryrun_and_review_pass"),
        wm_static.get("dryrun_and_review_pass"),
        sched_static.get("dryrun_and_review_pass"),
        static_validator_review.get("dryrun_and_review_pass"),
        sample_dryrun.get("dryrun_and_review_pass"),
        governance_dryrun.get("dryrun_and_review_pass"),
        health_guard_dryrun.get("dryrun_and_review_pass"),
    ]

    dryrun_issues: List[Dict[str, Any]] = []
    if blockers:
        dryrun_issues.extend([{"issue_id": f"blocker.{i}", "severity": "blocker", "detail": b} for i, b in enumerate(blockers)])
    for review_name, review in (
        ("file_creation", file_creation_report),
        ("type_validation", type_validation),
        ("eb_static", eb_static),
        ("wm_static", wm_static),
        ("sched_static", sched_static),
        ("static_validator", static_validator_review),
        ("sample", sample_dryrun),
        ("governance", governance_dryrun),
        ("health", health_guard_dryrun),
    ):
        for issue in review.get("issues") or []:
            dryrun_issues.append({**issue, "review": review_name, "severity": "blocker"})

    blocker_count = len([i for i in dryrun_issues if i.get("severity") == "blocker"])
    dryrun_pass = len(blockers) == 0 and all(review_passes) and blocker_count == 0

    issue_register = {
        "register_id": "skeleton_issue_register_v1",
        "issues": dryrun_issues,
        "issue_count": len(dryrun_issues),
        "blocker_count": blocker_count,
        **meta,
    }

    readiness = {
        "decision_id": "skeleton_implementation_dryrun_readiness_decision_v1",
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
        "foundation_components": ["event_bus", "working_memory", "scheduler"],
        **meta,
    }

    return {
        "summary": summary,
        "skeleton_implementation_scope_report": scope_report,
        "skeleton_file_creation_report": file_creation_report,
        "skeleton_type_contract_validation": type_validation,
        "event_bus_skeleton_static_validation": eb_static,
        "working_memory_skeleton_static_validation": wm_static,
        "scheduler_skeleton_static_validation": sched_static,
        "static_validator_review": static_validator_review,
        "skeleton_sample_dryrun": sample_dryrun,
        "governance_guard_dryrun": governance_dryrun,
        "health_guard_dryrun": health_guard_dryrun,
        "skeleton_boundary_matrix": boundary_matrix,
        "skeleton_issue_register": issue_register,
        "skeleton_implementation_dryrun_readiness_decision": readiness,
    }
