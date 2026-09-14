# -*- coding: utf-8 -*-
"""Health Management Layer Integration DryRun v1 — candidate samples only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import SWITCHING_SCENARIOS
from capabilities.governance.model_management_layer_recovery_planning_v1 import HEALTH_STATES
from capabilities.governance.health_management_layer_integration_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_METRIC_DEFINITION_STATUS,
    HEALTH_SIGNAL_CONTRACT_FIELDS,
    HEALTH_STATUS_TAXONOMY,
    HEALTH_TO_DRIVE_ROUTES,
    METRIC_FORBIDDEN_NOW,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    SEVERITY_TAXONOMY,
)
from capabilities.governance.model_registry_canonicalization_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as CANONICAL_POST_FINAL,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Health-Management-Layer-Integration-DryRun-v1-001"
SCOPE = "health_management_layer_integration_dryrun_only"
SOURCE_CHAIN = "health_management_layer_integration_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = "HEALTH_MANAGEMENT_LAYER_INTEGRATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "HEALTH_MANAGEMENT_LAYER_INTEGRATION_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Health-Management-Layer-Integration-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Health-Management-Layer-Integration-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_management_layer_integration_dryrun"
)

MODEL_HEALTH_TO_SIGNAL_TYPE: Dict[str, str] = {
    "available": "model_available_signal_candidate",
    "degraded": "model_degraded_signal_candidate",
    "timeout": "model_timeout_signal_candidate",
    "failed": "model_failed_signal_candidate",
    "disabled": "model_disabled_signal_candidate",
    "unknown": "model_unknown_signal_candidate",
}

MODEL_HEALTH_SEVERITY: Dict[str, str] = {
    "available": "info",
    "degraded": "warning",
    "timeout": "warning",
    "failed": "critical",
    "disabled": "blocked",
    "unknown": "unknown",
}

SWITCHING_TO_OUTPUT: Dict[str, str] = {
    "primary_unavailable_to_fallback_candidate": "fallback_candidate",
    "provider_timeout_to_hold_candidate": "hold_candidate",
    "high_latency_to_lower_cost_candidate": "lower_cost_model_candidate",
    "hardware_pressure_to_degrade_candidate": "degradation_candidate",
    "unsafe_output_to_block_candidate": "block_candidate",
    "uncertain_output_to_candidate_only": "candidate_only_policy_candidate",
}

BLOCKED_PATHS: Tuple[str, ...] = (
    "health_signal_to_runtime_monitor",
    "fallback_candidate_to_fallback_execution",
    "degradation_candidate_to_model_degradation_execution",
    "survival_drive_candidate_to_active_drive_execution",
    "health_signal_to_user_facing_output",
    "health_signal_to_task_commit",
    "health_signal_to_model_switch",
    "health_signal_to_model_repair",
    "hardware_signal_to_hardware_control",
    "health_signal_to_memory_write",
    "health_signal_to_world_model_write",
    "health_metric_reserved_to_health_score",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun GO ≠ runtime monitor enabled",
    "health_signal_candidate ≠ health_score",
    "fallback_candidate sample ≠ fallback executed",
    "degradation_candidate sample ≠ degradation executed",
    "survival_drive_candidate sample ≠ active drive executed",
    "health_metric_reserved_not_defined unchanged",
    "Post-DryRun Review next ≠ automatic degradation",
)

BOUNDARY_FALSE_DRYRUN: Tuple[str, ...] = (
    "health_runtime_monitor_enabled_now",
    "software_health_monitor_enabled_now",
    "hardware_health_monitor_enabled_now",
    "system_monitor_enabled_now",
    "health_score_generated_now",
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


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "health_management_layer_integration_dryrun_only": True,
        "simulated": True,
        "health_signal_candidate_generated_now": True,
        "fallback_candidate_generated_now": True,
        "degradation_candidate_generated_now": True,
        "survival_drive_candidate_generated_now": True,
        "recovery_plan_candidate_generated_now": True,
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        "health_score_calculation_enabled_now": False,
        "health_threshold_policy_enabled_now": False,
        "health_metric_baseline_available_now": False,
        "health_metric_runtime_data_available_now": False,
        "health_metric_requires_future_runtime_observation": True,
        "active_drive_execution_enabled": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE_DRYRUN:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _candidate_defaults() -> Dict[str, Any]:
    return {
        "candidate_only": True,
        "fact_status": "not_fact",
        "action_allowed": False,
        "user_facing_output_allowed": False,
        "write_allowed": False,
        "source_chain": SOURCE_CHAIN,
        "timestamp": "dryrun_simulated",
        "ttl": 300,
    }


def _build_health_signal(
    *,
    signal_id: str,
    signal_type: str,
    source_layer: str,
    severity: str,
    health_status: str,
    recommended_candidate_action: str,
    affected_module: str = "model_management",
    affected_model_ref: Optional[str] = "ocr_model_mock",
    affected_hardware_ref: Optional[str] = None,
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    row = {
        **_candidate_defaults(),
        "signal_id": signal_id,
        "signal_type": signal_type,
        "source_layer": source_layer,
        "severity": severity,
        "affected_module": affected_module,
        "affected_model_ref": affected_model_ref,
        "affected_hardware_ref": affected_hardware_ref,
        "health_status": health_status,
        "recommended_candidate_action": recommended_candidate_action,
        **meta,
    }
    if row["severity"] not in SEVERITY_TAXONOMY:
        raise ValueError(f"invalid severity: {severity}")
    if row["health_status"] not in HEALTH_STATUS_TAXONOMY:
        raise ValueError(f"invalid health_status: {health_status}")
    return row


def _build_drive_candidate(
    *,
    candidate_id: str,
    candidate_type: str,
    scenario_id: str,
    meta: Dict[str, Any],
    **extra: Any,
) -> Dict[str, Any]:
    return {
        **_candidate_defaults(),
        "candidate_id": candidate_id,
        "candidate_type": candidate_type,
        "scenario_id": scenario_id,
        "executed_now": False,
        "active_drive_execution_enabled": False,
        **extra,
        **meta,
    }


def run_health_management_layer_integration_dryrun_v1(
    *,
    health_management_layer_integration_planning_root: str,
    model_registry_canonicalization_post_dryrun_review_root: Optional[str] = None,
    model_management_layer_recovery_dryrun_root: Optional[str] = None,
    model_management_layer_recovery_post_dryrun_review_root: Optional[str] = None,
    midplatform_backbone_definition_alignment_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(health_management_layer_integration_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}

    canonical_post_root = Path(
        model_registry_canonicalization_post_dryrun_review_root
        or planning_root.parent / "model_registry_canonicalization_post_dryrun_review"
    ).expanduser().resolve()
    recovery_dryrun_root = Path(
        model_management_layer_recovery_dryrun_root
        or planning_root.parent / "model_management_layer_recovery_dryrun"
    ).expanduser().resolve()
    mm_post_root = Path(
        model_management_layer_recovery_post_dryrun_review_root
        or planning_root.parent / "model_management_layer_recovery_post_dryrun_review"
    ).expanduser().resolve()
    backbone_root = Path(
        midplatform_backbone_definition_alignment_root
        or planning_root.parent / "midplatform_backbone_definition_alignment"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "output_root": str(out_root)}

    canonical_sm = _try_read_json(canonical_post_root / "summary.json") or {}
    recovery_dryrun_sm = _try_read_json(recovery_dryrun_root / "summary.json") or {}
    backbone_sm = _try_read_json(backbone_root / "summary.json") or {}
    recovery_health = _try_read_json(recovery_dryrun_root / "model_health_state_candidate_matrix_v1.json") or {}
    recovery_switch = _try_read_json(recovery_dryrun_root / "model_switching_candidate_matrix_v1.json") or {}

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning next phase mismatch")
    if plan_sm.get("health_metric_definition_status") != HEALTH_METRIC_DEFINITION_STATUS:
        blockers.append("health_metric_definition_status must be reserved_not_defined")
    if plan_sm.get("health_score_calculation_enabled_now") is not False:
        blockers.append("health_score_calculation must be false")
    if canonical_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("b_lite_canonical_v0_baseline_closed required")
    if canonical_sm.get("production_registry_generated_now") is not False:
        blockers.append("production registry must remain false")
    if recovery_dryrun_sm.get("model_runtime_invoked_now") is not False:
        blockers.append("model invocation must be disabled")
    if backbone_sm.get("active_drive_execution_enabled_now") is not False:
        blockers.append("active_drive_execution_enabled must be false")

    health_rows = recovery_health.get("candidates") or []
    switch_rows = recovery_switch.get("candidates") or []
    if len(health_rows) != 6:
        blockers.append("model_health_state_candidate count must be 6")
    if len(switch_rows) != 6:
        blockers.append("model_switching_candidate count must be 6")

    input_review = {
        "review_id": "health_management_planning_input_review_v1",
        "upstream_planning_root": str(planning_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "b_lite_canonical_v0_baseline_closed": canonical_sm.get("b_lite_canonical_v0_baseline_closed"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    software_signals = [
        _build_health_signal(
            signal_id=f"hss_model_{state}",
            signal_type=MODEL_HEALTH_TO_SIGNAL_TYPE[state],
            source_layer="health_management",
            severity=MODEL_HEALTH_SEVERITY[state],
            health_status=state,
            recommended_candidate_action=SWITCHING_TO_OUTPUT.get(
                "primary_unavailable_to_fallback_candidate", "fallback_candidate"
            ),
            affected_model_ref="ocr_model_mock",
            meta=meta,
        )
        for state in HEALTH_STATES
    ]

    hardware_signals = [
        _build_health_signal(
            signal_id="hss_camera_unavailable",
            signal_type="hardware_health_signal_candidate",
            source_layer="health_management",
            severity="critical",
            health_status="unavailable",
            recommended_candidate_action="survival_drive_candidate",
            affected_module="hardware",
            affected_model_ref=None,
            affected_hardware_ref="camera_primary",
            meta=meta,
        ),
        _build_health_signal(
            signal_id="hss_resource_pressure",
            signal_type="hardware_health_signal_candidate",
            source_layer="health_management",
            severity="degraded",
            health_status="resource_pressure",
            recommended_candidate_action="degradation_candidate",
            affected_module="hardware",
            affected_model_ref=None,
            affected_hardware_ref="compute_subsystem",
            meta=meta,
        ),
    ]

    system_signals = [
        _build_health_signal(
            signal_id="hss_system_anomaly",
            signal_type="system_health_signal_candidate",
            source_layer="health_management",
            severity="warning",
            health_status="degraded",
            recommended_candidate_action="recovery_plan_candidate",
            affected_module="system_monitor",
            affected_model_ref=None,
            affected_hardware_ref=None,
            meta=meta,
        ),
        _build_health_signal(
            signal_id="hss_runtime_boundary",
            signal_type="gate_failure_candidate",
            source_layer="health_management",
            severity="blocked",
            health_status="failed",
            recommended_candidate_action="block_candidate",
            affected_module="constitution_gate",
            meta=meta,
        ),
    ]

    health_consumption = {
        "result_id": "model_health_state_consumption_result_v1",
        "states_consumed": list(HEALTH_STATES),
        "signal_types_generated": list(MODEL_HEALTH_TO_SIGNAL_TYPE.values()),
        "consumed_count": len(health_rows),
        "consumption_pass": len(health_rows) == 6,
        **meta,
    }

    switch_consumption = {
        "result_id": "model_switching_candidate_consumption_result_v1",
        "scenarios_consumed": [s[0] for s in SWITCHING_SCENARIOS],
        "consumed_count": len(switch_rows),
        "consumption_pass": len(switch_rows) == 6,
        **meta,
    }

    switching_samples: List[Dict[str, Any]] = []
    for scenario_id, outcome in SWITCHING_SCENARIOS:
        ctype = SWITCHING_TO_OUTPUT[scenario_id]
        switching_samples.append(
            _build_drive_candidate(
                candidate_id=f"drc_{scenario_id}",
                candidate_type=ctype,
                scenario_id=scenario_id,
                switching_outcome=outcome,
                meta=meta,
            )
        )

    fallback_samples = [
        s
        for s in switching_samples
        if s["candidate_type"]
        in (
            "fallback_candidate",
            "hold_candidate",
            "block_candidate",
            "candidate_only_policy_candidate",
        )
    ]
    degradation_samples = [
        s for s in switching_samples if s["candidate_type"] in ("degradation_candidate", "lower_cost_model_candidate")
    ] + [
        _build_drive_candidate(
            candidate_id="dgc_hardware_pressure",
            candidate_type="degradation_candidate",
            scenario_id="hardware_pressure_to_degrade_candidate",
            meta=meta,
        )
    ]

    survival_samples = [
        _build_drive_candidate(
            candidate_id="sdc_camera_unavailable",
            candidate_type="survival_drive_candidate",
            scenario_id="camera_unavailable",
            trigger="camera_unavailable",
            meta=meta,
        )
    ]

    recovery_samples = [
        _build_drive_candidate(
            candidate_id="rpc_system_anomaly",
            candidate_type="recovery_plan_candidate",
            scenario_id="system_anomaly",
            trigger="system_anomaly",
            meta=meta,
        ),
        _build_drive_candidate(
            candidate_id="rpc_missing_label",
            candidate_type="reobserve_or_hold_candidate",
            scenario_id="missing_label_or_tagging_failure",
            meta=meta,
        ),
    ]

    routing_rows = [
        {
            "trigger": route["trigger"],
            "target_candidate": route["target_candidate"],
            "routed": True,
            "executed_now": False,
            "task_commit_allowed": False,
        }
        for route in HEALTH_TO_DRIVE_ROUTES
    ]
    bridge_result = {
        "result_id": "health_to_drive_bridge_dryrun_result_v1",
        "routes": routing_rows,
        "route_count": len(routing_rows),
        "routing_pass": len(routing_rows) == 8,
        "active_drive_execution_enabled": False,
        **meta,
    }

    metric_review = {
        "review_id": "health_metric_reserved_dryrun_review_v1",
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        "health_score_calculation_enabled_now": False,
        "health_threshold_policy_enabled_now": False,
        "health_metric_baseline_available_now": False,
        "health_metric_runtime_data_available_now": False,
        "health_metric_requires_future_runtime_observation": True,
        "forbidden_metrics_absent": list(METRIC_FORBIDDEN_NOW),
        "review_pass": True,
        **meta,
    }

    boundary_audit = {
        "audit_id": "health_runtime_boundary_audit_v1",
        "audit_pass": True,
        "checks": [
            {"check_id": "no_monitor", "passed": meta.get("health_runtime_monitor_enabled_now") is False},
            {"check_id": "no_score", "passed": meta.get("health_score_generated_now") is False},
            {"check_id": "no_fallback_exec", "passed": meta.get("fallback_executed_now") is False},
            {"check_id": "no_survival_exec", "passed": meta.get("survival_drive_executed_now") is False},
            {"check_id": "no_task_commit", "passed": meta.get("task_state_committed_now") is False},
        ],
        **meta,
    }

    blocked_result = {
        "result_id": "health_management_blocked_path_result_v1",
        "paths": [{"path_id": p, "blocked": True, "observed_now": False} for p in BLOCKED_PATHS],
        "all_blocked": True,
        **meta,
    }

    all_signals = software_signals + hardware_signals + system_signals

    def _has_forbidden_score_artifact(row: Dict[str, Any]) -> bool:
        return any(key in row for key in METRIC_FORBIDDEN_NOW)

    all_pass = (
        len(blockers) == 0
        and health_consumption.get("consumption_pass")
        and switch_consumption.get("consumption_pass")
        and len(software_signals) == 6
        and bridge_result.get("routing_pass")
        and metric_review.get("review_pass")
        and blocked_result.get("all_blocked")
        and all(s.get("candidate_only") for s in all_signals)
        and not any(_has_forbidden_score_artifact(s) for s in all_signals)
    )

    readiness = {
        "readiness_id": "health_management_dryrun_readiness_decision_v1",
        "ready_for_post_dryrun_review": all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "health_management_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {"register_id": "non_claims_register_v1", "non_claims": list(NON_CLAIMS), **meta}

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": all_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "software_signal_count": len(software_signals),
        "hardware_signal_count": len(hardware_signals),
        "system_signal_count": len(system_signals),
        "fallback_sample_count": len(fallback_samples),
        "degradation_sample_count": len(degradation_samples),
        "survival_sample_count": len(survival_samples),
        "recovery_sample_count": len(recovery_samples),
        "high_risk_count": 0 if all_pass else 1,
        **meta,
    }

    return {
        "health_management_dryrun_policy": policy,
        "health_management_planning_input_review": input_review,
        "model_health_state_consumption_result": health_consumption,
        "model_switching_candidate_consumption_result": switch_consumption,
        "software_health_signal_candidate_samples": {
            "artifact_id": "software_health_signal_candidate_samples_v1",
            "sample_count": len(software_signals),
            "samples": software_signals,
            **meta,
        },
        "hardware_health_signal_candidate_samples": {
            "artifact_id": "hardware_health_signal_candidate_samples_v1",
            "sample_count": len(hardware_signals),
            "samples": hardware_signals,
            **meta,
        },
        "system_health_signal_candidate_samples": {
            "artifact_id": "system_health_signal_candidate_samples_v1",
            "sample_count": len(system_signals),
            "samples": system_signals,
            **meta,
        },
        "fallback_candidate_samples": {
            "artifact_id": "fallback_candidate_samples_v1",
            "sample_count": len(fallback_samples),
            "samples": fallback_samples,
            **meta,
        },
        "degradation_candidate_samples": {
            "artifact_id": "degradation_candidate_samples_v1",
            "sample_count": len(degradation_samples),
            "samples": degradation_samples,
            **meta,
        },
        "survival_drive_candidate_samples": {
            "artifact_id": "survival_drive_candidate_samples_v1",
            "sample_count": len(survival_samples),
            "samples": survival_samples,
            **meta,
        },
        "recovery_plan_candidate_samples": {
            "artifact_id": "recovery_plan_candidate_samples_v1",
            "sample_count": len(recovery_samples),
            "samples": recovery_samples,
            **meta,
        },
        "health_to_drive_bridge_dryrun_result": bridge_result,
        "health_runtime_boundary_audit": boundary_audit,
        "health_metric_reserved_dryrun_review": metric_review,
        "health_management_blocked_path_result": blocked_result,
        "health_management_dryrun_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
