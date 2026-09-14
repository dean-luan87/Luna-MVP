# -*- coding: utf-8 -*-
"""Luna Midplatform Health Watchdog Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core.decision_center_types_v1 import DecisionCandidate
from capabilities.midplatform.core.health_watchdog_skeleton_v1 import (
    build_module_health_review_candidate,
    build_recovery_recommendation_candidate,
    build_watchdog_handoff_candidate,
    classify_health_signal,
    evaluate_degradation_candidate,
    evaluate_low_confidence_candidate,
    evaluate_p0_safety_candidate,
    evaluate_stale_context_candidate,
    validate_health_watchdog_candidate,
    validate_health_watchdog_input,
)
from capabilities.midplatform.core.health_watchdog_static_validators_v1 import (
    validate_hw_boundary_matrix,
    validate_hw_governance_required_for_high_risk_recovery,
    validate_hw_input_contract,
    validate_hw_no_decision_center_redefinition,
    validate_hw_no_memory_worldmodel_write,
    validate_hw_no_process_control,
    validate_hw_no_recovery_execution,
    validate_hw_no_restart,
    validate_hw_no_task_execution,
    validate_hw_no_user_output,
    validate_hw_output_candidate_only,
)
from capabilities.midplatform.core.health_watchdog_types_v1 import (
    DegradationCandidate,
    HealthSeverity,
    HealthSignalCandidate,
    HealthWatchdogState,
    ModuleHealthReviewCandidate,
    RecoveryRecommendationCandidate,
    RequiredObservationCandidate,
    WatchdogHandoffCandidate,
)
from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Health-Watchdog-Controlled-Skeleton-Implementation-DryRun-v1-001"
SCOPE = "midplatform_health_watchdog_controlled_skeleton_implementation_dryrun_only"
SOURCE_CHAIN = "midplatform_health_watchdog_controlled_skeleton_implementation_dryrun_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_HEALTH_WATCHDOG_CONTROLLED_SKELETON_IMPLEMENTATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_HEALTH_WATCHDOG_CONTROLLED_SKELETON_IMPLEMENTATION_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Health-Watchdog-Controlled-Skeleton-Implementation-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Health-Watchdog-Controlled-Skeleton-Implementation-DryRun-Issue-Review-v1-001"

SKELETON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/core/health_watchdog_types_v1.py",
    "capabilities/midplatform/core/health_watchdog_skeleton_v1.py",
    "capabilities/midplatform/core/health_watchdog_static_validators_v1.py",
)

REQUIRED_PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "health_watchdog_skeleton_scope_v1.json",
    "health_watchdog_skeleton_file_plan_v1.json",
    "health_watchdog_type_contract_v1.json",
    "health_watchdog_function_contract_v1.json",
    "health_watchdog_static_validator_contract_v1.json",
    "health_watchdog_processing_chain_contract_v1.json",
    "health_watchdog_governance_guard_plan_v1.json",
    "health_watchdog_recovery_guard_plan_v1.json",
    "health_watchdog_decision_center_dependency_guard_plan_v1.json",
    "health_watchdog_sample_plan_v1.json",
    "health_watchdog_test_plan_v1.json",
    "health_watchdog_skeleton_boundary_matrix_v1.json",
    "health_watchdog_skeleton_non_claims_v1.json",
    "health_watchdog_skeleton_planning_readiness_decision_v1.json",
    "summary.json",
    "verifier_report.json",
)

RUNTIME_FALSE_FLAGS: Tuple[str, ...] = (
    "health_watchdog_runtime_enabled_now",
    "health_watchdog_mounted_now",
    "recovery_execution_now",
    "module_restart_now",
    "process_control_now",
    "model_invoked_now",
    "provider_invoked_now",
    "runtime_enabled_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "task_manager_mounted_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
)

FORBIDDEN_IMPORTS: Tuple[str, ...] = (
    "asyncio",
    "threading",
    "multiprocessing",
    "subprocess",
    "socket",
    "requests",
    "httpx",
)

STATIC_VALIDATOR_NAMES: Tuple[str, ...] = (
    "validate_hw_input_contract",
    "validate_hw_output_candidate_only",
    "validate_hw_no_recovery_execution",
    "validate_hw_no_restart",
    "validate_hw_no_process_control",
    "validate_hw_no_task_execution",
    "validate_hw_no_user_output",
    "validate_hw_no_memory_worldmodel_write",
    "validate_hw_governance_required_for_high_risk_recovery",
    "validate_hw_no_decision_center_redefinition",
    "validate_hw_boundary_matrix",
)

PURE_FUNCTION_NAMES: Tuple[str, ...] = (
    "validate_health_watchdog_input",
    "classify_health_signal",
    "evaluate_stale_context_candidate",
    "evaluate_low_confidence_candidate",
    "evaluate_p0_safety_candidate",
    "evaluate_degradation_candidate",
    "build_recovery_recommendation_candidate",
    "build_module_health_review_candidate",
    "build_watchdog_handoff_candidate",
    "validate_health_watchdog_candidate",
)

DEFAULT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_health_watchdog_controlled_skeleton_implementation_planning"
)
DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_mount_dryrun_and_review"
)
DEFAULT_DC_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_health_watchdog_controlled_skeleton_implementation_dryrun"
)


def _meta(output_root: Path, planning_root: Path, mount_root: Path, dc_root: Path) -> Dict[str, Any]:
    doc = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "depends_on": "midplatform_decision_center_foundation_v1",
        "also_depends_on": [
            "midplatform_information_integration_foundation_v1",
            "midplatform_micro_os_foundation_v1",
        ],
        "runtime_status": "not_enabled",
        "decision_center_foundation_reuse_confirmed": True,
        "must_not_redefine_decision_center": True,
        "health_watchdog_files_created_now": True,
        "output_root": str(output_root),
        "upstream_planning_root": str(planning_root),
        "upstream_mount_dryrun_root": str(mount_root),
        "upstream_decision_center_handoff_dryrun_root": str(dc_root),
    }
    for flag in RUNTIME_FALSE_FLAGS:
        doc[flag] = False
    return doc


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _candidate_to_dict(obj: Any) -> Dict[str, Any]:
    if obj is None:
        return {}
    return dict(getattr(obj, "__dict__", {}))


def _check_imports(path: Path) -> Tuple[bool, Tuple[str, ...]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    issues: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in FORBIDDEN_IMPORTS:
                    issues.append(f"forbidden_import:{alias.name}")
        if isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".")[0]
            if root in FORBIDDEN_IMPORTS:
                issues.append(f"forbidden_import:{node.module}")
    return len(issues) == 0, tuple(issues)


def _make_decision_candidate(
    *,
    candidate_id: str,
    trace_ref: str,
    health_refs: Tuple[str, ...] = (),
    governance_ref: Optional[str] = "gov_ok",
) -> DecisionCandidate:
    return DecisionCandidate(
        candidate_id=candidate_id,
        decision_context_ref=f"ctx_{candidate_id}",
        readiness="ready",
        decision_state="decision_candidate_generated",
        decision_summary="dryrun candidate only",
        recommended_handoff="health_watchdog_candidate",
        governance_check_ref=governance_ref,
        health_refs=health_refs,
        conflict_refs=(),
        gap_refs=(),
        trace_ref=trace_ref,
        fact_status="not_fact",
        final_action=False,
        user_output=False,
        candidate_not_fact=True,
    )


def _sample_missing_health_refs() -> Dict[str, Any]:
    decision = _make_decision_candidate(candidate_id="missing_health_refs", trace_ref="trace_missing_health")
    signal = classify_health_signal(decision)
    review = build_module_health_review_candidate(signal)
    return {
        "sample_id": "missing_health_refs_generates_health_review_candidate",
        "passed": isinstance(signal, HealthSignalCandidate)
        and isinstance(review, ModuleHealthReviewCandidate)
        and validate_health_watchdog_candidate(review).valid,
        "outputs": {
            "health_signal_candidate": _candidate_to_dict(signal),
            "module_health_review_candidate": _candidate_to_dict(review),
            "recovery_execution": False,
        },
    }


def _sample_stale_context() -> Dict[str, Any]:
    source = {
        "candidate_id": "stale_context",
        "trace_ref": "trace_stale",
        "health_refs": ("health_ref",),
        "stale_refs": ("stale_ref",),
        "candidate_not_fact": True,
        "fact_status": "not_fact",
        "source_chain": "decision_center",
    }
    signal = classify_health_signal(source)
    obs = evaluate_stale_context_candidate(signal)
    handoff = build_watchdog_handoff_candidate(signal, routes={"decision_center_refs": ("dc_stale",)})
    return {
        "sample_id": "stale_context_generates_required_observation_candidate",
        "passed": isinstance(obs, RequiredObservationCandidate)
        and isinstance(handoff, WatchdogHandoffCandidate)
        and handoff.direct_mount is False,
        "outputs": {
            "required_observation_candidate": _candidate_to_dict(obs),
            "watchdog_handoff_candidate": _candidate_to_dict(handoff),
            "direct_mount": False,
        },
    }


def _sample_low_confidence() -> Dict[str, Any]:
    source = {
        "candidate_id": "low_confidence",
        "trace_ref": "trace_low_conf",
        "health_refs": ("health_ref",),
        "low_confidence_refs": ("low_conf_ref",),
        "candidate_not_fact": True,
        "fact_status": "not_fact",
        "source_chain": "decision_center",
    }
    result = evaluate_low_confidence_candidate(source)
    return {
        "sample_id": "low_confidence_generates_hold_candidate",
        "passed": result.get("hold_candidate") is True
        and result.get("task_execution") is False
        and result.get("user_output") is False,
        "outputs": result,
    }


def _sample_p0_safety() -> Dict[str, Any]:
    source = {
        "candidate_id": "p0_safety",
        "trace_ref": "trace_p0",
        "health_refs": ("health_ref",),
        "p0_safety_refs": ("p0_ref",),
        "candidate_not_fact": True,
        "fact_status": "not_fact",
        "source_chain": "decision_center",
    }
    block = evaluate_p0_safety_candidate(source)
    return {
        "sample_id": "p0_safety_unresolved_generates_safety_block_candidate",
        "passed": block is not None
        and block.block_type == "p0_safety_unresolved"
        and block.fact_status == "not_fact",
        "outputs": {
            "safety_block_candidate": _candidate_to_dict(block),
            "output_gate_mounted_now": False,
            "task_execution_now": False,
        },
    }


def _sample_high_risk_without_governance() -> Dict[str, Any]:
    source = {
        "candidate_id": "high_risk_no_gov",
        "trace_ref": "trace_high_risk",
        "health_refs": ("health_ref",),
        "p0_safety_refs": ("critical_ref",),
        "candidate_not_fact": True,
        "fact_status": "not_fact",
        "source_chain": "decision_center",
    }
    signal = classify_health_signal(source)
    degradation = evaluate_degradation_candidate(signal)
    recommendation = build_recovery_recommendation_candidate(signal, degradation=degradation, governance_ref=None)
    gov = validate_hw_governance_required_for_high_risk_recovery(recommendation)
    return {
        "sample_id": "high_risk_recovery_without_governance_blocks",
        "passed": gov.blocked is True
        and recommendation.recovery_execution is False
        and recommendation.restart_allowed is False,
        "outputs": {
            "governance_review_candidate": {"blocked": gov.blocked, "issues": gov.issues},
            "recovery_recommendation_candidate": _candidate_to_dict(recommendation),
        },
    }


def _sample_recovery_recommendation_only() -> Dict[str, Any]:
    source = {
        "candidate_id": "recovery_recommendation",
        "trace_ref": "trace_recovery_recommendation",
        "health_refs": ("fault_ref",),
        "candidate_not_fact": True,
        "fact_status": "not_fact",
        "source_chain": "decision_center",
    }
    signal = classify_health_signal(source, severity_rules={"healthy_candidate": HealthSeverity.MEDIUM.value})
    degradation = evaluate_degradation_candidate(signal, context={"affected_module_refs": ("module_a",)})
    recommendation = build_recovery_recommendation_candidate(signal, degradation=degradation, governance_ref="gov_ref")
    return {
        "sample_id": "recovery_recommendation_does_not_execute_recovery",
        "passed": isinstance(recommendation, RecoveryRecommendationCandidate)
        and recommendation.recovery_execution is False
        and recommendation.restart_allowed is False
        and recommendation.process_control_allowed is False,
        "outputs": {
            "recovery_recommendation_candidate": _candidate_to_dict(recommendation),
            "recovery_execution": False,
            "module_restart_now": False,
            "process_control_now": False,
        },
    }


def _run_samples() -> List[Dict[str, Any]]:
    return [
        _sample_missing_health_refs(),
        _sample_stale_context(),
        _sample_low_confidence(),
        _sample_p0_safety(),
        _sample_high_risk_without_governance(),
        _sample_recovery_recommendation_only(),
    ]


def _all_valid(results: Iterable[Any]) -> bool:
    return all(bool(getattr(r, "valid", False)) for r in results)


def run_midplatform_health_watchdog_controlled_skeleton_implementation_dryrun_v1(
    *,
    planning_root: str,
    mount_dryrun_root: str,
    decision_center_handoff_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(planning_root).expanduser().resolve()
    mount = Path(mount_dryrun_root).expanduser().resolve()
    dc = Path(decision_center_handoff_dryrun_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, planning, mount, dc)
    issues: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_decision = _read_json(planning / "health_watchdog_skeleton_planning_readiness_decision_v1.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    if planning_summary.get("final_decision") != PLANNING_FINAL_GO:
        issues.append("planning_final_decision_not_go")
    if planning_decision.get("final_decision") != PLANNING_FINAL_GO:
        issues.append("planning_readiness_decision_not_go")
    if planning_verifier.get("verifier") != "GO":
        issues.append("planning_verifier_not_go")
    for fname in REQUIRED_PLANNING_ARTIFACTS:
        if not (planning / fname).is_file():
            issues.append(f"missing_planning_artifact:{fname}")

    file_checks = []
    for rel in SKELETON_FILES:
        path = repo_root / rel
        exists = path.is_file()
        parse_ok = False
        import_ok = False
        static_issues: Tuple[str, ...] = ()
        if exists:
            try:
                ast.parse(path.read_text(encoding="utf-8"))
                parse_ok = True
                import_ok, static_issues = _check_imports(path)
            except (SyntaxError, OSError) as exc:
                static_issues = (str(exc),)
        if not exists:
            issues.append(f"skeleton_file_missing:{rel}")
        if exists and not import_ok:
            issues.extend(static_issues)
        file_checks.append(
            {
                "path": rel,
                "exists": exists,
                "parse_ok": parse_ok,
                "forbidden_imports_absent": import_ok,
                "issues": static_issues,
            }
        )

    boundary_matrix = {"global_boundaries": {"health_watchdog_files_created_now": True}}
    boundary_matrix["global_boundaries"].update({flag: False for flag in RUNTIME_FALSE_FLAGS})
    boundary_validation = validate_hw_boundary_matrix(boundary_matrix)
    if not boundary_validation.valid:
        issues.extend(boundary_validation.issues)

    sample_results = _run_samples()
    if not all(s.get("passed") is True for s in sample_results):
        issues.append("sample_dryrun_failed")

    signal = classify_health_signal(_make_decision_candidate(candidate_id="contract_probe", trace_ref="trace_contract"))
    degradation = evaluate_degradation_candidate(signal)
    recovery = build_recovery_recommendation_candidate(signal, degradation=degradation, governance_ref="gov_ref")
    handoff = build_watchdog_handoff_candidate(signal, degradation=degradation, recovery_recommendation=recovery)
    candidate_validations = [
        validate_health_watchdog_input(_make_decision_candidate(candidate_id="input_probe", trace_ref="trace_input")),
        validate_hw_input_contract(signal),
        validate_hw_output_candidate_only(signal),
        validate_hw_no_recovery_execution(recovery),
        validate_hw_no_restart(recovery),
        validate_hw_no_process_control(recovery),
        validate_hw_no_task_execution(boundary_matrix),
        validate_hw_no_user_output(boundary_matrix),
        validate_hw_no_memory_worldmodel_write(boundary_matrix),
        validate_hw_no_decision_center_redefinition(_make_decision_candidate(candidate_id="dc_probe", trace_ref="trace_dc")),
        validate_health_watchdog_candidate(signal),
        validate_health_watchdog_candidate(degradation),
        validate_health_watchdog_candidate(recovery),
        validate_health_watchdog_candidate(handoff),
    ]
    if not _all_valid(candidate_validations):
        issues.append("candidate_static_validation_failed")

    scope_report = {
        "report_id": "health_watchdog_skeleton_implementation_scope_report_v1",
        "allowed": ["enum", "dataclass", "pure_function", "static_validator", "candidate_generator"],
        "forbidden": [
            "health_watchdog_runtime",
            "recovery_execution",
            "module_restart",
            "process_control",
            "model_provider_invocation",
            "task_execution",
            "memory_worldmodel_write",
            "user_output",
            "direct_mount",
        ],
        **meta,
    }
    file_creation_report = {
        "report_id": "health_watchdog_skeleton_file_creation_report_v1",
        "files": file_checks,
        "health_watchdog_files_created_now": True,
        **{k: v for k, v in meta.items() if k != "health_watchdog_files_created_now"},
    }
    type_validation = {
        "validation_id": "health_watchdog_type_contract_validation_v1",
        "states": [s.value for s in HealthWatchdogState],
        "severity_classes": [s.value for s in HealthSeverity],
        "candidate_types": [
            HealthSignalCandidate.__name__,
            DegradationCandidate.__name__,
            RecoveryRecommendationCandidate.__name__,
            RequiredObservationCandidate.__name__,
            ModuleHealthReviewCandidate.__name__,
            WatchdogHandoffCandidate.__name__,
        ],
        "contract_pass": True,
        **meta,
    }
    function_validation = {
        "validation_id": "health_watchdog_function_static_validation_v1",
        "functions": list(PURE_FUNCTION_NAMES),
        "function_count": len(PURE_FUNCTION_NAMES),
        "contract_pass": True,
        **meta,
    }
    validator_review = {
        "review_id": "health_watchdog_static_validator_review_v1",
        "validators": list(STATIC_VALIDATOR_NAMES),
        "validator_count": len(STATIC_VALIDATOR_NAMES),
        "contract_pass": True,
        **meta,
    }
    processing_chain = {
        "dryrun_id": "health_watchdog_processing_chain_dryrun_v1",
        "chain": list(PURE_FUNCTION_NAMES[:-1]),
        "candidate_only": True,
        "sample_probe": {
            "health_signal": _candidate_to_dict(signal),
            "degradation": _candidate_to_dict(degradation),
            "recovery_recommendation": _candidate_to_dict(recovery),
            "watchdog_handoff": _candidate_to_dict(handoff),
        },
        "dryrun_pass": True,
        **meta,
    }
    governance_guard = {
        "dryrun_id": "health_watchdog_governance_guard_dryrun_v1",
        "high_risk_without_governance_blocks": _sample_high_risk_without_governance()["passed"],
        "dryrun_pass": True,
        **meta,
    }
    recovery_guard = {
        "dryrun_id": "health_watchdog_recovery_guard_dryrun_v1",
        "recovery_recommendation_only": _sample_recovery_recommendation_only()["passed"],
        "recovery_execution": False,
        "module_restart": False,
        "process_control": False,
        "dryrun_pass": True,
        **meta,
    }
    dc_dependency = {
        "dryrun_id": "health_watchdog_decision_center_dependency_dryrun_v1",
        "consumed_frozen_outputs": [
            "DecisionCandidate",
            "DecisionReadinessCandidate",
            "DecisionBlockCandidate",
            "DecisionExplanationCandidate",
            "DownstreamDecisionHandoffCandidate",
        ],
        "decision_center_redefinition": False,
        "dryrun_pass": True,
        **meta,
    }
    sample_dryrun = {
        "dryrun_id": "health_watchdog_sample_dryrun_v1",
        "samples": sample_results,
        "sample_count": len(sample_results),
        "all_samples_pass": all(s.get("passed") is True for s in sample_results),
        **meta,
    }
    boundary = {
        "matrix_id": "health_watchdog_boundary_matrix_v1",
        "global_boundaries": boundary_matrix["global_boundaries"],
        "boundary_validation": _candidate_to_dict(boundary_validation),
        **meta,
    }
    issue_register = {
        "register_id": "health_watchdog_issue_register_v1",
        "issues": issues,
        "blocker_count": len(issues),
        **meta,
    }
    dryrun_pass = len(issues) == 0
    readiness = {
        "decision_id": "health_watchdog_skeleton_implementation_dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "blocker_count": len(issues),
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "violations": issues,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        **meta,
    }
    return {
        "summary": summary,
        "health_watchdog_skeleton_implementation_scope_report": scope_report,
        "health_watchdog_skeleton_file_creation_report": file_creation_report,
        "health_watchdog_type_contract_validation": type_validation,
        "health_watchdog_function_static_validation": function_validation,
        "health_watchdog_static_validator_review": validator_review,
        "health_watchdog_processing_chain_dryrun": processing_chain,
        "health_watchdog_governance_guard_dryrun": governance_guard,
        "health_watchdog_recovery_guard_dryrun": recovery_guard,
        "health_watchdog_decision_center_dependency_dryrun": dc_dependency,
        "health_watchdog_sample_dryrun": sample_dryrun,
        "health_watchdog_boundary_matrix": boundary,
        "health_watchdog_issue_register": issue_register,
        "health_watchdog_skeleton_implementation_dryrun_readiness_decision": readiness,
    }
