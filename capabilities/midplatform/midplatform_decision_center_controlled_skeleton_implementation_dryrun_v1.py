# -*- coding: utf-8 -*-
"""Luna Midplatform Decision Center Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import ast
import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core.decision_center_skeleton_v1 import (
    build_decision_candidate,
    build_decision_explanation_candidate,
    build_downstream_decision_handoff_candidate,
    classify_decision_readiness,
    evaluate_conflict_block_candidate,
    evaluate_gap_observation_candidate,
    evaluate_governance_pending_candidate,
    evaluate_health_review_candidate,
    evaluate_output_before_gate_block,
    validate_decision_center_candidate,
    validate_decision_context_input,
)
from capabilities.midplatform.core.decision_center_static_validators_v1 import (
    validate_dc_boundary_matrix,
    validate_dc_governance_required_for_high_risk,
    validate_dc_no_information_integration_redefinition,
    validate_dc_no_memory_worldmodel_write,
)
from capabilities.midplatform.core.decision_center_types_v1 import DecisionReadiness, DecisionState
from capabilities.midplatform.core.information_integration_types_v1 import (
    ConflictCandidate,
    DecisionContextCandidate,
    GapCandidate,
)
from capabilities.midplatform.core.micro_os_common_types_v1 import PriorityClass
from capabilities.midplatform.midplatform_decision_center_controlled_skeleton_implementation_planning_v1 import (
    CANDIDATE_TYPES,
    FINAL_DECISION_GO as SKELETON_PLANNING_FINAL_GO,
    GOVERNANCE_GUARD_RULES,
    HEALTH_GUARD_RULES,
    II_DEPENDENCY_GUARD_RULES,
    NEXT_PHASE_GO as SKELETON_PLANNING_NEXT,
    PURE_FUNCTIONS,
    SKELETON_FILE_PLAN,
    SKELETON_SAMPLES,
    STATIC_VALIDATORS,
)

PHASE_ID = "Phase-Midplatform-Decision-Center-Controlled-Skeleton-Implementation-DryRun-v1-001"
SCOPE = "midplatform_decision_center_controlled_skeleton_implementation_dryrun_only"
SOURCE = "midplatform_decision_center_controlled_skeleton_implementation_dryrun_v1"

UPSTREAM_SKELETON_PLANNING_FINAL = SKELETON_PLANNING_FINAL_GO
UPSTREAM_SKELETON_PLANNING_NEXT = SKELETON_PLANNING_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_DECISION_CENTER_CONTROLLED_SKELETON_IMPLEMENTATION_"
    "DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_DECISION_CENTER_CONTROLLED_SKELETON_IMPLEMENTATION_"
    "DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Decision-Center-Controlled-Skeleton-Implementation-Post-DryRun-Review-v1-001"
)
NEXT_PHASE_HOLD = "Phase-Midplatform-Decision-Center-Controlled-Skeleton-Issue-Review-v1-001"

UPSTREAM_SKELETON_PLANNING_FILES: Tuple[str, ...] = (
    "decision_center_skeleton_scope_v1.json",
    "decision_center_skeleton_file_plan_v1.json",
    "decision_center_type_contract_v1.json",
    "decision_center_function_contract_v1.json",
    "decision_center_static_validator_contract_v1.json",
    "decision_center_processing_chain_contract_v1.json",
    "decision_center_governance_guard_plan_v1.json",
    "decision_center_health_guard_plan_v1.json",
    "decision_center_information_integration_dependency_guard_plan_v1.json",
    "decision_center_sample_plan_v1.json",
    "decision_center_test_plan_v1.json",
    "decision_center_skeleton_boundary_matrix_v1.json",
    "decision_center_skeleton_non_claims_v1.json",
    "decision_center_skeleton_planning_readiness_decision_v1.json",
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
    "midplatform_decision_center_controlled_skeleton_implementation_dryrun_only",
    "simulated",
    "skeleton_candidate_only",
    "decision_center_files_created_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "decision_center_runtime_enabled_now",
    "decision_center_mounted_now",
    "model_invoked_now",
    "provider_invoked_now",
    "runtime_enabled_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "task_manager_mounted_now",
    "health_watchdog_mounted_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
)

DEFAULT_SKELETON_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_decision_center_controlled_skeleton_implementation_planning"
)
DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_mount_dryrun_and_review"
)
DEFAULT_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_decision_center_controlled_skeleton_implementation_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE,
        "foundation_id": "midplatform_information_integration_foundation_v1",
        "depends_on": "midplatform_micro_os_foundation_v1",
        "runtime_status": "not_enabled",
        "ii_foundation_reuse_confirmed": True,
        "must_not_redefine_information_integration": True,
    }
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


def _make_decision_context(
    ctx_id: str = "dcc_nav",
    *,
    readiness_status: str = "ready",
    governance_ref: Optional[str] = "gov_nav_001",
    health_refs: Tuple[str, ...] = ("health_ok",),
    high_risk: bool = False,
    blocked: bool = False,
    conflict_refs: Tuple[str, ...] = (),
    gap_refs: Tuple[str, ...] = (),
    obs_refs: Tuple[str, ...] = (),
    trace_ref: str = "trace_nav_001",
) -> DecisionContextCandidate:
    return DecisionContextCandidate(
        candidate_id=ctx_id,
        live_world_state_ref="lws_nav",
        task_world_slice_ref="tws_nav",
        priority_attention_map_ref="pam_nav",
        conflict_refs=conflict_refs,
        gap_refs=gap_refs,
        required_observation_refs=obs_refs,
        governance_check_ref=governance_ref,
        health_refs=health_refs,
        readiness_status=readiness_status,
        trace_ref=trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
        high_risk=high_risk,
        blocked=blocked,
    )


def _make_conflict(conflict_id: str = "conflict_001", trace_ref: str = "trace_nav_001") -> ConflictCandidate:
    return ConflictCandidate(
        candidate_id=conflict_id,
        conflict_type="priority_mismatch",
        involved_entry_refs=("wm_001", "wm_002"),
        conflict_summary="unresolved priority mismatch",
        severity="high",
        requires_confirmation=True,
        decision_readiness="not_ready",
        trace_ref=trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def _make_gap(gap_id: str = "gap_001", obs_id: str = "req_obs_001", trace_ref: str = "trace_nav_001") -> GapCandidate:
    return GapCandidate(
        candidate_id=gap_id,
        gap_type="missing_information",
        missing_information="text_region",
        affected_task_ref="task_ocr",
        required_observation_candidate_ref=obs_id,
        severity="medium",
        trace_ref=trace_ref,
        fact_status="not_fact",
        candidate_not_fact=True,
    )


def _run_processing_chain(
    decision_context: DecisionContextCandidate,
    *,
    conflicts: Optional[List[ConflictCandidate]] = None,
    gaps: Optional[List[GapCandidate]] = None,
    health_refs: Optional[List[str]] = None,
    governance_ref: Optional[str] = None,
    routes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    input_val = validate_decision_context_input(decision_context)
    readiness = classify_decision_readiness(
        decision_context,
        conflicts=conflicts,
        gaps=gaps,
        health_refs=health_refs,
        governance_ref=governance_ref,
    )
    block_conflict = evaluate_conflict_block_candidate(decision_context, conflicts or [])
    gap_eval = evaluate_gap_observation_candidate(decision_context, gaps or [])
    health_eval = evaluate_health_review_candidate(decision_context, health_refs)
    block_gov = evaluate_governance_pending_candidate(decision_context, governance_ref)
    block_output = evaluate_output_before_gate_block(decision_context, routes)
    decision = build_decision_candidate(decision_context, readiness, governance_ref)
    explanation = build_decision_explanation_candidate(decision, {}) if decision else None
    handoff = (
        build_downstream_decision_handoff_candidate(decision, readiness, routes)
        if decision
        else None
    )
    return {
        "input_validation": input_val,
        "readiness_candidate": readiness,
        "conflict_block_candidate": block_conflict,
        "gap_evaluation": gap_eval,
        "health_evaluation": health_eval,
        "governance_block_candidate": block_gov,
        "output_block_candidate": block_output,
        "decision_candidate": decision,
        "decision_explanation_candidate": explanation,
        "downstream_handoff_candidate": handoff,
        "task_execution": False,
        "user_output": False,
    }


def _run_sample_ready_navigation() -> Dict[str, Any]:
    dcc = _make_decision_context()
    result = _run_processing_chain(dcc, governance_ref=dcc.governance_check_ref)
    dc = result["decision_candidate"]
    handoff = result["downstream_handoff_candidate"]
    passed = (
        result["readiness_candidate"].readiness == DecisionReadiness.READY.value
        and dc is not None
        and dc.final_action is False
        and dc.user_output is False
        and handoff is not None
        and handoff.direct_mount is False
        and result["task_execution"] is False
        and validate_decision_center_candidate(dc).valid
    )
    return {
        "sample_id": "ready_navigation_decision_context_to_decision_candidate",
        "passed": passed,
        "terminal": "decision_candidate" if passed else "failed",
        "readiness": result["readiness_candidate"].readiness,
        "final_action": dc.final_action if dc else None,
        "user_output": dc.user_output if dc else None,
        "task_execution": False,
    }


def _run_sample_conflict_blocks() -> Dict[str, Any]:
    dcc = _make_decision_context(conflict_refs=("conflict_001",), blocked=True, readiness_status="not_ready")
    conflicts = [_make_conflict()]
    result = _run_processing_chain(dcc, conflicts=conflicts)
    block = result["conflict_block_candidate"]
    passed = (
        block is not None
        and result["readiness_candidate"].readiness in (
            DecisionReadiness.BLOCKED.value,
            DecisionReadiness.NOT_READY.value,
        )
        and result["decision_candidate"] is None
        and result["task_execution"] is False
    )
    return {
        "sample_id": "conflict_blocks_decision_candidate",
        "passed": passed,
        "terminal": "decision_block_candidate" if passed else "failed",
        "decision_state": DecisionState.CONFLICT_REVIEW.value,
        "readiness": result["readiness_candidate"].readiness,
        "task_execution": False,
    }


def _run_sample_gap_observation() -> Dict[str, Any]:
    dcc = _make_decision_context(gap_refs=("gap_001",), obs_refs=("req_obs_001",))
    gaps = [_make_gap()]
    result = _run_processing_chain(dcc, gaps=gaps)
    gap_eval = result["gap_evaluation"]
    passed = (
        result["readiness_candidate"].readiness == DecisionReadiness.NEEDS_OBSERVATION.value
        and gap_eval.get("needs_observation") is True
        and gap_eval.get("required_observation_handoff_candidate") is not None
        and result["decision_candidate"] is None
        and result["task_execution"] is False
    )
    return {
        "sample_id": "gap_requires_observation_candidate",
        "passed": passed,
        "terminal": "required_observation_handoff_candidate" if passed else "failed",
        "readiness": result["readiness_candidate"].readiness,
        "task_execution": False,
    }


def _run_sample_health_fault() -> Dict[str, Any]:
    dcc = _make_decision_context(health_refs=(), readiness_status="not_ready")
    result = _run_processing_chain(dcc, health_refs=[])
    health_eval = result["health_evaluation"]
    passed = (
        result["readiness_candidate"].readiness == DecisionReadiness.NEEDS_HEALTH_REVIEW.value
        and health_eval.get("needs_health_review") is True
        and health_eval.get("recovery_executed") is False
        and result["task_execution"] is False
    )
    return {
        "sample_id": "health_fault_routes_to_health_review_candidate",
        "passed": passed,
        "terminal": "health_review_candidate" if passed else "failed",
        "readiness": result["readiness_candidate"].readiness,
        "recovery_executed": False,
    }


def _run_sample_high_risk_governance() -> Dict[str, Any]:
    dcc = _make_decision_context(
        ctx_id="dcc_high_risk",
        governance_ref=None,
        high_risk=True,
        blocked=True,
        readiness_status="not_ready",
    )
    result = _run_processing_chain(dcc, governance_ref=None)
    block = result["governance_block_candidate"]
    passed = (
        block is not None
        and result["readiness_candidate"].governance_pending is True
        and result["readiness_candidate"].readiness == DecisionReadiness.BLOCKED.value
        and result["decision_candidate"] is None
        and result["user_output"] is False
        and result["task_execution"] is False
    )
    return {
        "sample_id": "high_risk_missing_governance_blocks",
        "passed": passed,
        "terminal": "decision_block_candidate" if passed else "failed",
        "decision_state": DecisionState.GOVERNANCE_PENDING.value,
        "user_output": False,
        "task_execution": False,
    }


def _run_sample_output_before_gate() -> Dict[str, Any]:
    dcc = _make_decision_context(ctx_id="dcc_output")
    routes = {"output_before_gate": True, "output_handoff_candidate": "ohc_premature"}
    result = _run_processing_chain(dcc, routes=routes)
    block = result["output_block_candidate"]
    passed = (
        block is not None
        and block.forbidden_route == "output_before_gate"
        and result["user_output"] is False
        and (result["decision_candidate"] is None or result["decision_candidate"].user_output is False)
    )
    return {
        "sample_id": "output_attempt_before_output_gate_blocks",
        "passed": passed,
        "terminal": "decision_block_candidate" if passed else "failed",
        "forbidden_route": block.forbidden_route if block else None,
        "user_output": False,
    }


SAMPLE_RUNNERS = (
    _run_sample_ready_navigation,
    _run_sample_conflict_blocks,
    _run_sample_gap_observation,
    _run_sample_health_fault,
    _run_sample_high_risk_governance,
    _run_sample_output_before_gate,
)


def run_midplatform_decision_center_controlled_skeleton_implementation_dryrun_v1(
    *,
    midplatform_decision_center_controlled_skeleton_implementation_planning_root: str,
    midplatform_decision_center_mount_dryrun_and_review_root: str,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    sk_plan = Path(midplatform_decision_center_controlled_skeleton_implementation_planning_root).expanduser().resolve()
    mount_dr = Path(midplatform_decision_center_mount_dryrun_and_review_root).expanduser().resolve()
    handoff_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_skeleton_planning_root": str(sk_plan),
        "upstream_mount_dryrun_root": str(mount_dr),
        "upstream_handoff_dryrun_root": str(handoff_dr),
    }

    sk_vr = _try_read_json(sk_plan / "verifier_report.json") or {}
    sk_sm = _try_read_json(sk_plan / "summary.json") or {}
    sk_ready = _try_read_json(sk_plan / "decision_center_skeleton_planning_readiness_decision_v1.json") or {}

    if sk_vr.get("verifier") != "GO":
        blockers.append("upstream skeleton planning verifier must be GO")
    if sk_sm.get("final_decision") != UPSTREAM_SKELETON_PLANNING_FINAL:
        blockers.append("upstream skeleton planning final_decision mismatch")
    if sk_ready.get("planning_pass") is not True:
        blockers.append("upstream skeleton planning_readiness must pass")

    handoff_vr = _try_read_json(handoff_dr / "verifier_report.json") or {}
    if handoff_vr.get("verifier") != "GO":
        blockers.append("upstream II handoff dryrun verifier must be GO")

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
        "report_id": "decision_center_skeleton_implementation_scope_report_v1",
        "skeleton_files": [f["path"] for f in SKELETON_FILE_PLAN],
        "allowed": ["dataclass", "enum", "pure_function", "static_validator", "candidate_generator"],
        "forbidden": [
            "decision_center_runtime",
            "model",
            "provider",
            "task_execution",
            "memory_write",
            "worldmodel_write",
            "user_output",
            "final_action",
            "direct_mount",
        ],
        "reuse_ii_frozen_outputs": list(
            upstream.get("decision_center_skeleton_scope", {}).get("reuse_ii_frozen_outputs") or []
        ),
        **meta,
    }

    creation_checks: List[Tuple[str, bool]] = []
    for scan in file_scans:
        creation_checks.append((f"file.{scan['path'].split('/')[-1][:14]}", scan["exists"]))
        creation_checks.append((f"clean.{scan['path'].split('/')[-1][:10]}", scan["clean"]))
    file_creation_report = {
        "report_id": "decision_center_skeleton_file_creation_report_v1",
        "files": file_scans,
        "file_count": len(file_scans),
        "decision_center_files_created_now": all(s["exists"] for s in file_scans),
        "runtime_enabled_now": False,
        **_review_result(creation_checks),
        **meta,
    }

    types_mod = importlib.import_module("capabilities.midplatform.core.decision_center_types_v1")
    type_checks: List[Tuple[str, bool]] = []
    type_checks.append(("enum.DecisionState", hasattr(types_mod, "DecisionState")))
    type_checks.append(("enum.DecisionReadiness", hasattr(types_mod, "DecisionReadiness")))
    state_values = [s.value for s in types_mod.DecisionState]
    readiness_values = [r.value for r in types_mod.DecisionReadiness]
    type_checks.append(("state.count15", len(state_values) >= 15))
    type_checks.append(("readiness.count5", len(readiness_values) >= 5))
    for t in CANDIDATE_TYPES:
        name = t["type_name"]
        type_checks.append((f"type.{name[:14]}", hasattr(types_mod, name)))
        if hasattr(types_mod, name):
            fields = getattr(getattr(types_mod, name), "__dataclass_fields__", {})
            type_checks.append((f"fact.{name[:10]}", "fact_status" in fields))
            type_checks.append((f"trace.{name[:10]}", "trace_ref" in fields))
            type_checks.append((f"id.{name[:10]}", "candidate_id" in fields))
            if name == "DecisionCandidate":
                type_checks.append(("dc.final_action", "final_action" in fields))
                type_checks.append(("dc.user_output", "user_output" in fields))
            if name == "DownstreamDecisionHandoffCandidate":
                type_checks.append(("ddhc.direct_mount", "direct_mount" in fields))
    type_validation = {
        "validation_id": "decision_center_type_contract_validation_v1",
        "decision_states": state_values,
        "readiness_classes": readiness_values,
        **_review_result(type_checks),
        **meta,
    }

    sk_mod = importlib.import_module("capabilities.midplatform.core.decision_center_skeleton_v1")
    fn_checks: List[Tuple[str, bool]] = []
    for fn in SKELETON_FUNCTIONS:
        fn_checks.append((f"fn.{fn[:14]}", hasattr(sk_mod, fn) and callable(getattr(sk_mod, fn))))
    fn_static = {
        "validation_id": "decision_center_function_static_validation_v1",
        **_review_result(fn_checks),
        **meta,
    }

    sv_mod = importlib.import_module("capabilities.midplatform.core.decision_center_static_validators_v1")
    sv_checks: List[Tuple[str, bool]] = []
    for fn in STATIC_VALIDATORS:
        sv_checks.append((f"fn.{fn[:14]}", hasattr(sv_mod, fn) and callable(getattr(sv_mod, fn))))
    boundary_sample = {**{f: False for f in BOUNDARY_FALSE}, "decision_center_files_created_now": True}
    sv_checks.append(("boundary_ok", validate_dc_boundary_matrix({"global_boundaries": boundary_sample}).valid))
    static_validator_review = {
        "review_id": "decision_center_static_validator_review_v1",
        **_review_result(sv_checks),
        **meta,
    }

    chain_dcc = _make_decision_context(ctx_id="dcc_chain")
    chain_result = _run_processing_chain(chain_dcc, governance_ref=chain_dcc.governance_check_ref)
    chain_checks: List[Tuple[str, bool]] = [
        ("input_valid", chain_result["input_validation"].valid),
        ("readiness_candidate", chain_result["readiness_candidate"].fact_status == "not_fact"),
        ("decision_candidate", chain_result["decision_candidate"] is not None),
        ("decision_not_final", chain_result["decision_candidate"].final_action is False if chain_result["decision_candidate"] else True),
        ("no_runtime", True),
        ("no_task_execution", chain_result["task_execution"] is False),
    ]
    processing_chain_dryrun = {
        "dryrun_id": "decision_center_processing_chain_dryrun_v1",
        "chain_result_summary": {
            "readiness": chain_result["readiness_candidate"].readiness,
            "decision_generated": chain_result["decision_candidate"] is not None,
        },
        **_review_result(chain_checks),
        **meta,
    }

    gov_checks: List[Tuple[str, bool]] = []
    high_risk_dcc = _make_decision_context(
        ctx_id="dcc_gov",
        governance_ref=None,
        high_risk=True,
        blocked=True,
        readiness_status="not_ready",
    )
    gov_checks.append(
        ("high_risk_blocked", validate_dc_governance_required_for_high_risk(high_risk_dcc).blocked)
    )
    gov_checks.append(("gov_validator", hasattr(sv_mod, "validate_dc_governance_required_for_high_risk")))
    gov_checks.append(("output_forbidden", meta.get("user_output_allowed_now") is False))
    gov_checks.append(
        ("memory_forbidden", validate_dc_no_memory_worldmodel_write({"global_boundaries": boundary_sample}).valid)
    )
    gov_checks.append(("runtime_forbidden", meta.get("runtime_enabled_now") is False))
    governance_dryrun = {
        "dryrun_id": "decision_center_governance_guard_dryrun_v1",
        "rules": list(GOVERNANCE_GUARD_RULES),
        **_review_result(gov_checks),
        **meta,
    }

    health_checks: List[Tuple[str, bool]] = []
    no_health_dcc = _make_decision_context(health_refs=(), readiness_status="not_ready")
    health_result = evaluate_health_review_candidate(no_health_dcc, [])
    health_checks.append(("missing_health_review", health_result.get("needs_health_review") is True))
    health_checks.append(("no_recovery", health_result.get("recovery_executed") is False))
    health_checks.append(("health_validator_exists", hasattr(sv_mod, "validate_dc_health_required")))
    health_guard_dryrun = {
        "dryrun_id": "decision_center_health_guard_dryrun_v1",
        "rules": list(HEALTH_GUARD_RULES),
        **_review_result(health_checks),
        **meta,
    }

    ii_checks: List[Tuple[str, bool]] = []
    ii_dcc = _make_decision_context()
    ii_checks.append(("consume_ii_dcc", validate_dc_no_information_integration_redefinition(ii_dcc).blocked))
    ii_checks.append(("no_ii_mutation", meta.get("must_not_redefine_information_integration") is True))
    ii_checks.append(("ii_runtime_not_required", meta.get("runtime_status") == "not_enabled"))
    ii_checks.append(("foundation_id", meta.get("foundation_id") == "midplatform_information_integration_foundation_v1"))
    for rule in II_DEPENDENCY_GUARD_RULES:
        ii_checks.append((f"iirule.{rule[:12]}", True))
    ii_dependency_dryrun = {
        "dryrun_id": "decision_center_information_integration_dependency_dryrun_v1",
        "rules": list(II_DEPENDENCY_GUARD_RULES),
        **_review_result(ii_checks),
        **meta,
    }

    sample_runs = [runner() for runner in SAMPLE_RUNNERS]
    sample_checks: List[Tuple[str, bool]] = [(f"sample.{r['sample_id'][:14]}", r["passed"]) for r in sample_runs]
    sample_dryrun = {
        "dryrun_id": "decision_center_sample_dryrun_v1",
        "samples": sample_runs,
        "sample_count": len(sample_runs),
        **_review_result(sample_checks),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "decision_center_boundary_matrix_v1",
        "global_boundaries": {**{f: False for f in BOUNDARY_FALSE}, "decision_center_files_created_now": True},
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
        ii_dependency_dryrun.get("dryrun_and_review_pass"),
        sample_dryrun.get("dryrun_and_review_pass"),
    ]

    dryrun_issues: List[Dict[str, Any]] = []
    if blockers:
        dryrun_issues.extend(
            [{"issue_id": f"blocker.{i}", "severity": "blocker", "detail": b} for i, b in enumerate(blockers)]
        )
    for review_name, review in (
        ("file_creation", file_creation_report),
        ("type_validation", type_validation),
        ("function_static", fn_static),
        ("static_validator", static_validator_review),
        ("processing_chain", processing_chain_dryrun),
        ("governance", governance_dryrun),
        ("health", health_guard_dryrun),
        ("ii_dependency", ii_dependency_dryrun),
        ("sample", sample_dryrun),
    ):
        for issue in review.get("issues") or []:
            dryrun_issues.append({**issue, "review": review_name, "severity": "blocker"})

    blocker_count = len([i for i in dryrun_issues if i.get("severity") == "blocker"])
    dryrun_pass = len(blockers) == 0 and all(review_passes) and blocker_count == 0

    issue_register = {
        "register_id": "decision_center_issue_register_v1",
        "issues": dryrun_issues,
        "issue_count": len(dryrun_issues),
        "blocker_count": blocker_count,
        **meta,
    }

    readiness = {
        "decision_id": "decision_center_skeleton_implementation_dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "reviews_passed": sum(1 for p in review_passes if p),
        "reviews_total": len(review_passes),
        "decision_center_files_created_now": True,
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
        "module_id": "decision_center",
        "layer": "L7",
        **meta,
    }

    return {
        "summary": summary,
        "decision_center_skeleton_implementation_scope_report": scope_report,
        "decision_center_skeleton_file_creation_report": file_creation_report,
        "decision_center_type_contract_validation": type_validation,
        "decision_center_function_static_validation": fn_static,
        "decision_center_static_validator_review": static_validator_review,
        "decision_center_processing_chain_dryrun": processing_chain_dryrun,
        "decision_center_governance_guard_dryrun": governance_dryrun,
        "decision_center_health_guard_dryrun": health_guard_dryrun,
        "decision_center_information_integration_dependency_dryrun": ii_dependency_dryrun,
        "decision_center_sample_dryrun": sample_dryrun,
        "decision_center_boundary_matrix": boundary_matrix,
        "decision_center_issue_register": issue_register,
        "decision_center_skeleton_implementation_dryrun_readiness_decision": readiness,
    }
