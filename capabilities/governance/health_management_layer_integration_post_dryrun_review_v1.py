# -*- coding: utf-8 -*-
"""Health Management Layer Integration Post-DryRun Review v1 — review-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_management_layer_integration_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    MODEL_HEALTH_TO_SIGNAL_TYPE,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
    SWITCHING_TO_OUTPUT,
)
from capabilities.governance.health_management_layer_integration_planning_v1 import (
    HEALTH_METRIC_DEFINITION_STATUS,
    HEALTH_STATUS_TAXONOMY,
    HEALTH_TO_DRIVE_ROUTES,
    METRIC_FORBIDDEN_NOW,
    SEVERITY_TAXONOMY,
)
from capabilities.governance.model_management_layer_recovery_planning_v1 import HEALTH_STATES
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Health-Management-Layer-Integration-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "health_management_layer_integration_post_dryrun_review_only"
SOURCE_CHAIN = "health_management_layer_integration_post_dryrun_review_v1"

UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "HEALTH_MANAGEMENT_LAYER_INTEGRATION_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_POST_HEALTH_ROADMAP_DECISION"
)
FINAL_DECISION_HOLD = "HEALTH_MANAGEMENT_LAYER_INTEGRATION_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Post-Health-Management-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Health-Management-Layer-Integration-Issue-Review-v1-001"

PREFERRED_ROUTE = "vision_ocr_voice_controlled_optimization"
ROUTE_OPTIONS: Tuple[Dict[str, str], ...] = (
    {
        "route_id": "vision_ocr_voice_controlled_optimization",
        "label": "Vision / OCR / Voice controlled optimization planning (preferred)",
    },
    {
        "route_id": "health_metric_baseline_planning",
        "label": "Health Metric Definition and Baseline Planning (deferred)",
    },
)

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_health_signal_candidate_generated_now",
    "new_fallback_candidate_generated_now",
    "new_degradation_candidate_generated_now",
    "new_survival_drive_candidate_generated_now",
    "health_runtime_monitor_enabled_now",
    "software_health_monitor_enabled_now",
    "hardware_health_monitor_enabled_now",
    "system_monitor_enabled_now",
    "health_score_generated_now",
    "health_threshold_policy_enabled_now",
    "fallback_executed_now",
    "degradation_executed_now",
    "survival_drive_executed_now",
    "active_drive_execution_enabled_now",
    "model_repair_executed_now",
    "model_switch_executed_now",
    "model_runtime_invoked_now",
    "model_provider_invoked_now",
    "hardware_control_executed_now",
    "camera_control_executed_now",
    "runtime_enabled_now",
    "task_state_committed_now",
    "user_facing_output_generated_now",
    "world_model_written_now",
    "memory_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ runtime monitor enabled",
    "health_signal_candidate ≠ health score",
    "survival_drive_candidate ≠ active drive execution",
    "fallback_candidate ≠ fallback executed",
    "degradation_candidate ≠ model degraded",
    "health management closure ≠ automatic recovery enabled",
    "health metric reserved ≠ metric definition completed",
    "next route readiness ≠ model/provider runtime enabled",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "health_management_layer_integration_post_dryrun_review_only": True,
        "review_only": True,
        "new_health_signal_candidate_generated_now": False,
        "new_fallback_candidate_generated_now": False,
        "new_degradation_candidate_generated_now": False,
        "new_survival_drive_candidate_generated_now": False,
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        "health_score_calculation_enabled_now": False,
        "health_threshold_policy_enabled_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        if field not in meta:
            meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _validate_signal_candidate(sample: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    if sample.get("candidate_only") is not True:
        issues.append("candidate_only")
    if sample.get("fact_status") != "not_fact":
        issues.append("fact_status")
    if sample.get("action_allowed") is not False:
        issues.append("action_allowed")
    if sample.get("user_facing_output_allowed") is not False:
        issues.append("user_facing_output_allowed")
    if sample.get("write_allowed") is not False:
        issues.append("write_allowed")
    sev = sample.get("severity")
    if sev and sev not in SEVERITY_TAXONOMY:
        issues.append("severity")
    hs = sample.get("health_status")
    if hs and hs not in HEALTH_STATUS_TAXONOMY:
        issues.append("health_status")
    for key in METRIC_FORBIDDEN_NOW:
        if key in sample:
            issues.append(key)
    return issues


def _validate_drive_candidate(sample: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    if sample.get("candidate_only") is not True:
        issues.append("candidate_only")
    if sample.get("executed_now") is True:
        issues.append("executed_now")
    if sample.get("action_allowed") is True:
        issues.append("action_allowed")
    for key in METRIC_FORBIDDEN_NOW:
        if key in sample:
            issues.append(key)
    return issues


def run_health_management_layer_integration_post_dryrun_review_v1(
    *,
    health_management_layer_integration_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(health_management_layer_integration_dryrun_root).expanduser().resolve()
    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "health_management_layer_integration_post_dryrun_review"
    )
    meta = {**_review_meta(), "upstream_dryrun_root": str(dryrun_root), "review_output_root": str(out_root)}

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    software = _try_read_json(dryrun_root / "software_health_signal_candidate_samples_v1.json") or {}
    hardware = _try_read_json(dryrun_root / "hardware_health_signal_candidate_samples_v1.json") or {}
    system = _try_read_json(dryrun_root / "system_health_signal_candidate_samples_v1.json") or {}
    fallback = _try_read_json(dryrun_root / "fallback_candidate_samples_v1.json") or {}
    degradation = _try_read_json(dryrun_root / "degradation_candidate_samples_v1.json") or {}
    survival = _try_read_json(dryrun_root / "survival_drive_candidate_samples_v1.json") or {}
    recovery = _try_read_json(dryrun_root / "recovery_plan_candidate_samples_v1.json") or {}
    bridge = _try_read_json(dryrun_root / "health_to_drive_bridge_dryrun_result_v1.json") or {}
    boundary_audit = _try_read_json(dryrun_root / "health_runtime_boundary_audit_v1.json") or {}
    metric_dryrun = _try_read_json(dryrun_root / "health_metric_reserved_dryrun_review_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "health_management_blocked_path_result_v1.json") or {}

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("software_signal_count", 0) != 6:
        blockers.append("software health signal count must be 6")
    if dryrun_sm.get("health_metric_definition_status") != HEALTH_METRIC_DEFINITION_STATUS:
        blockers.append("health_metric_definition_status must be reserved_not_defined")

    for field in BOUNDARY_FALSE_REVIEW:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    input_review = {
        "review_id": "health_management_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_phase": DRYRUN_PHASE,
        "upstream_scope": DRYRUN_SCOPE,
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "counts": {
            "software_signals": dryrun_sm.get("software_signal_count"),
            "hardware_signals": dryrun_sm.get("hardware_signal_count"),
            "system_signals": dryrun_sm.get("system_signal_count"),
            "fallback_samples": dryrun_sm.get("fallback_sample_count"),
            "degradation_samples": dryrun_sm.get("degradation_sample_count"),
            "survival_samples": dryrun_sm.get("survival_sample_count"),
            "recovery_samples": dryrun_sm.get("recovery_sample_count"),
        },
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    signal_issues: List[Dict[str, Any]] = []
    all_signals = (
        (software.get("samples") or [])
        + (hardware.get("samples") or [])
        + (system.get("samples") or [])
    )
    if not software.get("samples"):
        signal_issues.append({"issue_id": "software", "detail": "missing samples"})
    if not hardware.get("samples"):
        signal_issues.append({"issue_id": "hardware", "detail": "missing samples"})
    if not system.get("samples"):
        signal_issues.append({"issue_id": "system", "detail": "missing samples"})
    for state in HEALTH_STATES:
        stype = MODEL_HEALTH_TO_SIGNAL_TYPE[state]
        if not any(s.get("signal_type") == stype for s in software.get("samples") or []):
            signal_issues.append({"issue_id": state, "detail": f"missing {stype}"})
    for sample in all_signals:
        sid = sample.get("signal_id", "unknown")
        bad = _validate_signal_candidate(sample)
        if bad:
            signal_issues.append({"issue_id": sid, "detail": ",".join(bad)})

    signal_review = {
        "review_id": "health_signal_candidate_review_v1",
        "software_present": bool(software.get("samples")),
        "hardware_present": bool(hardware.get("samples")),
        "system_present": bool(system.get("samples")),
        "sample_total": len(all_signals),
        "model_health_signal_types": list(MODEL_HEALTH_TO_SIGNAL_TYPE.values()),
        "issues": signal_issues,
        "review_pass": len(signal_issues) == 0,
        **meta,
    }

    def _drive_review(
        review_id: str,
        artifact: Dict[str, Any],
        required_types: Optional[Tuple[str, ...]] = None,
    ) -> Dict[str, Any]:
        issues: List[Dict[str, Any]] = []
        samples = artifact.get("samples") or []
        if not samples:
            issues.append({"issue_id": "empty", "detail": "no samples"})
        if required_types:
            present = {s.get("candidate_type") for s in samples}
            for ctype in required_types:
                if ctype not in present:
                    issues.append({"issue_id": ctype, "detail": "missing type"})
        for sample in samples:
            cid = sample.get("candidate_id", "unknown")
            bad = _validate_drive_candidate(sample)
            if bad:
                issues.append({"issue_id": cid, "detail": ",".join(bad)})
        return {
            "review_id": review_id,
            "sample_count": len(samples),
            "issues": issues,
            "review_pass": len(issues) == 0,
            **meta,
        }

    fallback_review = _drive_review(
        "fallback_candidate_review_v1",
        fallback,
        ("fallback_candidate", "hold_candidate", "block_candidate", "candidate_only_policy_candidate"),
    )
    degradation_review = _drive_review(
        "degradation_candidate_review_v1",
        degradation,
        ("degradation_candidate", "lower_cost_model_candidate"),
    )
    survival_review = _drive_review(
        "survival_drive_candidate_review_v1",
        survival,
        ("survival_drive_candidate",),
    )
    recovery_review = _drive_review("recovery_plan_candidate_review_v1", recovery)

    bridge_issues: List[Dict[str, Any]] = []
    route_by_trigger = {r.get("trigger"): r for r in bridge.get("routes") or []}
    for route in HEALTH_TO_DRIVE_ROUTES:
        row = route_by_trigger.get(route["trigger"])
        if not row:
            bridge_issues.append({"issue_id": route["trigger"], "detail": "missing route"})
            continue
        if row.get("target_candidate") != route["target_candidate"]:
            bridge_issues.append({"issue_id": route["trigger"], "detail": "target mismatch"})
        if row.get("routed") is not True:
            bridge_issues.append({"issue_id": route["trigger"], "detail": "not routed"})
        if row.get("executed_now") is True:
            bridge_issues.append({"issue_id": route["trigger"], "detail": "executed_now true"})
        if row.get("task_commit_allowed") is True:
            bridge_issues.append({"issue_id": route["trigger"], "detail": "task_commit allowed"})

    if bridge.get("active_drive_execution_enabled") is not False:
        bridge_issues.append({"issue_id": "active_drive", "detail": "must be false"})
    if bridge.get("routing_pass") is not True:
        bridge_issues.append({"issue_id": "routing_pass", "detail": "must be true"})

    bridge_review = {
        "review_id": "health_to_drive_bridge_review_v1",
        "route_count": bridge.get("route_count"),
        "routes_expected": len(HEALTH_TO_DRIVE_ROUTES),
        "active_drive_execution_enabled": bridge.get("active_drive_execution_enabled"),
        "task_commit_allowed_now": False,
        "user_facing_output_allowed_now": False,
        "hardware_control_allowed_now": False,
        "issues": bridge_issues,
        "review_pass": len(bridge_issues) == 0,
        **meta,
    }

    runtime_issues: List[Dict[str, Any]] = []
    if boundary_audit.get("audit_pass") is not True:
        runtime_issues.append({"issue_id": "audit", "detail": "audit_pass false"})
    for check in boundary_audit.get("checks") or []:
        if check.get("passed") is not True:
            runtime_issues.append({"issue_id": check.get("check_id"), "detail": "failed"})

    runtime_review = {
        "review_id": "health_runtime_boundary_review_v1",
        "monitor_disabled": all(
            dryrun_sm.get(f) is False
            for f in (
                "health_runtime_monitor_enabled_now",
                "software_health_monitor_enabled_now",
                "hardware_health_monitor_enabled_now",
                "system_monitor_enabled_now",
            )
        ),
        "issues": runtime_issues,
        "review_pass": len(runtime_issues) == 0,
        **meta,
    }

    metric_issues: List[Dict[str, Any]] = []
    if metric_dryrun.get("health_metric_definition_status") != HEALTH_METRIC_DEFINITION_STATUS:
        metric_issues.append({"issue_id": "status", "detail": "reserved_not_defined required"})
    for flag in (
        "health_score_calculation_enabled_now",
        "health_threshold_policy_enabled_now",
        "health_metric_baseline_available_now",
        "health_metric_runtime_data_available_now",
    ):
        if metric_dryrun.get(flag) is not False:
            metric_issues.append({"issue_id": flag, "detail": "must be false"})
    if metric_dryrun.get("health_metric_requires_future_runtime_observation") is not True:
        metric_issues.append({"issue_id": "future_observation", "detail": "must be true"})

    combined_artifacts = all_signals + (
        (fallback.get("samples") or [])
        + (degradation.get("samples") or [])
        + (survival.get("samples") or [])
        + (recovery.get("samples") or [])
    )
    for artifact in combined_artifacts:
        for key in METRIC_FORBIDDEN_NOW:
            if key in artifact:
                metric_issues.append({"issue_id": key, "detail": "forbidden metric present"})

    metric_review = {
        "review_id": "health_metric_reserved_review_v1",
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        "health_score_calculation_enabled_now": False,
        "health_threshold_policy_enabled_now": False,
        "health_metric_baseline_available_now": False,
        "health_metric_runtime_data_available_now": False,
        "health_metric_requires_future_runtime_observation": True,
        "forbidden_metrics_absent": list(METRIC_FORBIDDEN_NOW),
        "issues": metric_issues,
        "review_pass": len(metric_issues) == 0 and metric_dryrun.get("review_pass") is True,
        **meta,
    }

    blocked_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in blocked.get("paths") or []}
    for pid in BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True:
            blocked_issues.append({"issue_id": pid, "detail": "must be blocked=true"})
        if row and row.get("observed_now") is True:
            blocked_issues.append({"issue_id": pid, "detail": "observed_now must be false"})

    blocked_review = {
        "review_id": "health_management_blocked_path_review_v1",
        "paths_total": len(BLOCKED_PATHS),
        "all_blocked": len(blocked_issues) == 0 and blocked.get("all_blocked") is True,
        "issues": blocked_issues,
        "review_pass": len(blocked_issues) == 0,
        **meta,
    }

    switching_present = all(
        any(
            s.get("candidate_type") == ctype
            for s in (
                (fallback.get("samples") or [])
                + (degradation.get("samples") or [])
                + (survival.get("samples") or [])
                + (recovery.get("samples") or [])
            )
        )
        for ctype in SWITCHING_TO_OUTPUT.values()
    )

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and signal_review.get("review_pass")
        and fallback_review.get("review_pass")
        and degradation_review.get("review_pass")
        and survival_review.get("review_pass")
        and recovery_review.get("review_pass")
        and bridge_review.get("review_pass")
        and runtime_review.get("review_pass")
        and metric_review.get("review_pass")
        and blocked_review.get("review_pass")
        and switching_present
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "health_management_integration_closure_decision_v1",
        "health_management_integration_dryrun_closed": boundary_ok,
        "health_signal_and_drive_candidates_consumable": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_readiness = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_post_health_roadmap_decision": boundary_ok,
        "preferred_route": PREFERRED_ROUTE,
        "preferred_route_label": ROUTE_OPTIONS[0]["label"],
        "defer_health_metric_baseline_planning": True,
        "route_options": list(ROUTE_OPTIONS),
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers + [i["issue_id"] for i in signal_issues + bridge_issues + blocked_issues],
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "health_signal_and_drive_candidates_consumable": boundary_ok,
        "health_management_integration_dryrun_closed": boundary_ok,
        **meta,
    }

    return {
        "health_management_dryrun_input_review": input_review,
        "health_signal_candidate_review": signal_review,
        "fallback_candidate_review": fallback_review,
        "degradation_candidate_review": degradation_review,
        "survival_drive_candidate_review": survival_review,
        "recovery_plan_candidate_review": recovery_review,
        "health_to_drive_bridge_review": bridge_review,
        "health_runtime_boundary_review": runtime_review,
        "health_metric_reserved_review": metric_review,
        "health_management_blocked_path_review": blocked_review,
        "health_management_integration_closure_decision": closure,
        "next_route_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
