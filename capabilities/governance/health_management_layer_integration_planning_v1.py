# -*- coding: utf-8 -*-
"""Health Management Layer Integration Planning v1 — planning only, no monitors or actions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import SWITCHING_SCENARIOS
from capabilities.governance.model_management_layer_recovery_planning_v1 import HEALTH_STATES
from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    REGISTRY_VERSION,
    ROUTE_C,
    SCHEMA_VERSION,
)
from capabilities.governance.model_registry_canonicalization_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Health-Management-Layer-Integration-Planning-v1-001"
SCOPE = "health_management_layer_integration_planning_only"
SOURCE_CHAIN = "health_management_layer_integration_planning_v1"

UPSTREAM_POST_REVIEW_FINAL = POST_REVIEW_FINAL_GO
UPSTREAM_POST_REVIEW_NEXT = POST_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = "HEALTH_MANAGEMENT_LAYER_INTEGRATION_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "HEALTH_MANAGEMENT_LAYER_INTEGRATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Health-Management-Layer-Integration-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Health-Management-Layer-Integration-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_management_layer_integration_planning"
)

SEVERITY_TAXONOMY: Tuple[str, ...] = (
    "info",
    "warning",
    "degraded",
    "critical",
    "blocked",
    "unknown",
)

HEALTH_STATUS_TAXONOMY: Tuple[str, ...] = (
    "available",
    "degraded",
    "timeout",
    "failed",
    "disabled",
    "unknown",
    "resource_pressure",
    "unavailable",
)

HEALTH_SIGNAL_CONTRACT_FIELDS: Tuple[str, ...] = (
    "signal_id",
    "signal_type",
    "source_layer",
    "source_chain",
    "severity",
    "affected_module",
    "affected_model_ref",
    "affected_hardware_ref",
    "timestamp",
    "ttl",
    "health_status",
    "recommended_candidate_action",
    "candidate_only",
    "fact_status",
    "action_allowed",
    "user_facing_output_allowed",
    "write_allowed",
)

SOFTWARE_OUTPUT_CANDIDATES: Tuple[str, ...] = (
    "software_health_signal_candidate",
    "provider_failure_candidate",
    "model_timeout_candidate",
    "gate_failure_candidate",
    "fallback_required_candidate",
)

HARDWARE_OUTPUT_CANDIDATES: Tuple[str, ...] = (
    "hardware_health_signal_candidate",
    "hardware_degradation_candidate",
    "camera_unavailable_candidate",
    "resource_pressure_candidate",
    "hardware_fallback_required_candidate",
)

SYSTEM_OUTPUT_CANDIDATES: Tuple[str, ...] = (
    "system_health_signal_candidate",
    "degraded_mode_candidate",
    "recovery_plan_candidate",
    "survival_drive_candidate",
    "fallback_path_candidate",
)

HEALTH_TO_DRIVE_ROUTES: Tuple[Dict[str, str], ...] = (
    {"trigger": "model_failure", "target_candidate": "fallback_candidate"},
    {"trigger": "provider_timeout", "target_candidate": "hold_candidate"},
    {"trigger": "hardware_pressure", "target_candidate": "degradation_candidate"},
    {"trigger": "camera_unavailable", "target_candidate": "survival_drive_candidate"},
    {"trigger": "system_anomaly", "target_candidate": "recovery_plan_candidate"},
    {"trigger": "missing_label_or_tagging_failure", "target_candidate": "reobserve_or_hold_candidate"},
    {"trigger": "runtime_boundary_violation", "target_candidate": "block_candidate"},
    {"trigger": "low_resource", "target_candidate": "lower_cost_model_candidate"},
)

RUNTIME_BOUNDARY_CHECKS: Tuple[Dict[str, str], ...] = (
    {"check_id": "health_signal_defined_not_monitor", "rule": "health signal defined ≠ runtime monitor enabled"},
    {"check_id": "fallback_defined_not_executed", "rule": "fallback candidate defined ≠ fallback executed"},
    {"check_id": "degradation_defined_not_executed", "rule": "degradation candidate defined ≠ model degraded"},
    {"check_id": "survival_defined_not_executed", "rule": "survival drive candidate defined ≠ active drive executed"},
    {"check_id": "hardware_contract_not_control", "rule": "hardware health contract defined ≠ hardware control allowed"},
    {"check_id": "system_monitor_not_running", "rule": "system monitor contract defined ≠ system monitor running"},
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "health_runtime_monitor_enabled_now",
    "software_health_monitor_enabled_now",
    "hardware_health_monitor_enabled_now",
    "system_monitor_enabled_now",
    "health_signal_generated_now",
    "survival_drive_candidate_generated_now",
    "fallback_executed_now",
    "degradation_executed_now",
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
    "health_score_calculation_enabled_now",
    "health_threshold_policy_enabled_now",
)

HEALTH_METRIC_DEFINITION_STATUS = "reserved_not_defined"
FUTURE_METRIC_DEFINITION_PHASE = "Phase-Health-Metric-Definition-and-Baseline-Planning-v1-001"

METRIC_NOT_DEFINED_REASONS: Tuple[str, ...] = (
    "no real runtime monitoring data yet",
    "no hardware runtime data yet",
    "no model latency / timeout / error-rate long-term baseline",
    "no battery / temperature / compute / storage / network pressure real distribution",
    "no user-scenario failure samples",
    "no real availability data across models and providers",
    "no multi-camera / voice / OCR / navigation runtime stability samples",
)

METRIC_ALLOWED_NOW: Tuple[str, ...] = (
    "health_signal_candidate",
    "software_health_signal_candidate",
    "hardware_health_signal_candidate",
    "system_health_signal_candidate",
    "fallback_required_candidate",
    "degradation_candidate",
    "survival_drive_candidate",
)

METRIC_FORBIDDEN_NOW: Tuple[str, ...] = (
    "global_health_score",
    "module_health_score",
    "model_health_score",
    "hardware_health_score",
    "system_health_score",
    "health_weight_formula",
    "numeric threshold",
    "automatic degradation threshold",
    "automatic repair threshold",
    "automatic model switch threshold",
)

HEALTH_OUTPUT_ALLOWED_FIELDS: Tuple[str, ...] = (
    "health_status",
    "severity",
    "recommended_candidate_action",
    "blocked_reason",
    "fallback_reason",
)

HEALTH_OUTPUT_FORBIDDEN_FIELDS: Tuple[str, ...] = (
    "score",
    "weight",
    "threshold",
    "automatic action decision",
)

_METRIC_RESERVED_FLAGS: Dict[str, Any] = {
    "metric_defined_now": False,
    "baseline_required": True,
    "runtime_observation_required": True,
    "threshold_policy_deferred": True,
    "automatic_action_binding_allowed": False,
}

FUTURE_METRIC_CATEGORIES: Tuple[Dict[str, Any], ...] = (
    {
        "category_id": "software_health_metrics",
        "label": "Software Health Metrics",
        "metrics": [
            "model_latency", "provider_timeout_rate", "error_count",
            "candidate_pipeline_failure_rate", "gate_failure_rate", "runtime_boundary_violation_count",
        ],
        **_METRIC_RESERVED_FLAGS,
    },
    {
        "category_id": "model_health_metrics",
        "label": "Model Health Metrics",
        "metrics": [
            "model_availability", "model_success_rate", "model_timeout_rate",
            "model_output_contract_pass_rate", "fallback_frequency", "degraded_status_duration",
        ],
        **_METRIC_RESERVED_FLAGS,
    },
    {
        "category_id": "hardware_health_metrics",
        "label": "Hardware Health Metrics",
        "metrics": [
            "battery_level", "temperature", "compute_pressure", "memory_pressure", "storage_pressure",
            "camera_availability", "microphone_availability", "speaker_availability",
            "sensor_availability", "network_quality",
        ],
        **_METRIC_RESERVED_FLAGS,
    },
    {
        "category_id": "system_health_metrics",
        "label": "System Health Metrics",
        "metrics": [
            "resource_allocation_pressure", "event_loop_delay", "task_queue_backlog",
            "degraded_mode_frequency", "recovery_success_rate", "survival_mode_entry_count",
        ],
        **_METRIC_RESERVED_FLAGS,
    },
    {
        "category_id": "candidate_flow_health_metrics",
        "label": "Candidate Flow Health Metrics",
        "metrics": [
            "candidate_intake_success_rate", "evidence_governance_pass_rate",
            "constitution_gate_block_rate", "output_arbitration_block_rate", "runtime_boundary_block_rate",
        ],
        **_METRIC_RESERVED_FLAGS,
    },
    {
        "category_id": "user_facing_reliability_metrics_later",
        "label": "User-Facing Reliability Metrics later",
        "metrics": [
            "speech_delivery_success_rate", "interruption_handling_success_rate",
            "navigation_guidance_hold_rate", "unsafe_output_block_rate",
        ],
        **_METRIC_RESERVED_FLAGS,
    },
)

NON_CLAIMS: Tuple[str, ...] = (
    "Health Integration Planning GO ≠ runtime monitor enabled",
    "Health signal contract defined ≠ health signal generated now",
    "Fallback candidate plan ≠ fallback executed",
    "Degradation candidate plan ≠ degradation executed",
    "Survival drive bridge plan ≠ active drive executed",
    "Hardware health contract ≠ hardware read or control",
    "DryRun plan next ≠ model repair or switch",
    "Route C planning ≠ model registry production publish",
    "Health Management Planning GO ≠ health metrics defined",
    "health_signal_candidate ≠ health_score",
    "severity enum ≠ numeric health score",
    "degradation_candidate ≠ automatic degradation execution",
    "health metric reserved ≠ monitoring enabled",
    "future metric list ≠ metric contract finalized",
)

PLANNING_FORBIDDEN: Tuple[str, ...] = (
    "real runtime monitor",
    "model invocation",
    "model switch",
    "model repair",
    "hardware control",
    "user-facing output",
    "memory write",
    "world model write",
    "health score calculation",
    "numeric health threshold policy",
    "automatic degradation/repair/switch thresholds",
)


def _metric_meta() -> Dict[str, Any]:
    return {
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        "health_score_calculation_enabled_now": False,
        "health_threshold_policy_enabled_now": False,
        "health_metric_baseline_available_now": False,
        "health_metric_runtime_data_available_now": False,
        "health_metric_requires_future_runtime_observation": True,
    }


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "health_management_layer_integration_planning_only": True,
        "active_drive_execution_enabled": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "registry_version": REGISTRY_VERSION,
        "schema_version": SCHEMA_VERSION,
        **_metric_meta(),
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_health_management_layer_integration_planning_v1(
    *,
    model_registry_canonicalization_post_dryrun_review_root: str,
    model_registry_canonicalization_dryrun_root: Optional[str] = None,
    model_management_layer_recovery_post_dryrun_review_root: Optional[str] = None,
    midplatform_backbone_definition_alignment_root: Optional[str] = None,
    midplatform_structure_cleanup_planning_root: Optional[str] = None,
    model_management_layer_roadmap_decision_root: Optional[str] = None,
    planning_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_root = Path(model_registry_canonicalization_post_dryrun_review_root).expanduser().resolve()
    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    next_route = _try_read_json(post_root / "next_route_readiness_decision_v1.json") or {}

    canonical_dryrun_root = Path(
        model_registry_canonicalization_dryrun_root
        or post_sm.get("upstream_dryrun_root")
        or post_root.parent / "model_registry_canonicalization_dryrun"
    ).expanduser().resolve()
    mm_post_root = Path(
        model_management_layer_recovery_post_dryrun_review_root
        or post_root.parent / "model_management_layer_recovery_post_dryrun_review"
    ).expanduser().resolve()
    backbone_root = Path(
        midplatform_backbone_definition_alignment_root
        or post_root.parent / "midplatform_backbone_definition_alignment"
    ).expanduser().resolve()
    cleanup_root = Path(
        midplatform_structure_cleanup_planning_root
        or post_root.parent / "midplatform_structure_cleanup_planning"
    ).expanduser().resolve()
    roadmap_root = Path(
        model_management_layer_roadmap_decision_root
        or post_root.parent / "model_management_layer_roadmap_decision"
    ).expanduser().resolve()

    out_root = (
        Path(planning_output_root).expanduser().resolve()
        if planning_output_root
        else post_root.parent / "health_management_layer_integration_planning"
    )

    meta = {
        **_planning_meta(),
        "upstream_post_review_root": str(post_root),
        "upstream_canonical_dryrun_root": str(canonical_dryrun_root),
        "upstream_mm_post_review_root": str(mm_post_root),
        "upstream_backbone_alignment_root": str(backbone_root),
        "upstream_structure_cleanup_root": str(cleanup_root),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "output_root": str(out_root),
    }

    mm_post_sm = _try_read_json(mm_post_root / "summary.json") or {}
    recovery_dryrun_root = Path(
        mm_post_sm.get("upstream_dryrun_root")
        or post_root.parent / "model_management_layer_recovery_dryrun"
    )
    recovery_dryrun_sm = _try_read_json(recovery_dryrun_root / "summary.json") or {}
    backbone_sm = _try_read_json(backbone_root / "summary.json") or {}
    cleanup_sm = _try_read_json(cleanup_root / "summary.json") or {}
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    health_layer = _try_read_json(backbone_root / "health_management_layer_contract_v1.json") or {}
    survival_contract = _try_read_json(backbone_root / "survival_drive_candidate_contract_v1.json") or {}

    post_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not post_go:
        blockers.append("post-dryrun review verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_POST_REVIEW_FINAL:
        blockers.append("post-review final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_POST_REVIEW_NEXT:
        blockers.append("post-review next phase mismatch")
    if post_sm.get("b_lite_canonical_v0_baseline_closed") is not True:
        blockers.append("b_lite_canonical_v0_baseline_closed must be true")
    if next_route.get("next_route") != ROUTE_C:
        blockers.append("next route must be Route C")
    if post_sm.get("production_registry_generated_now") is not False:
        blockers.append("production registry must remain false")
    if post_sm.get("model_runtime_invoked_now") is not False:
        blockers.append("model invocation must remain disabled")

    if recovery_dryrun_sm.get("health_candidate_count", 0) != 6:
        blockers.append("health candidate count must be 6 from recovery dryrun")
    if recovery_dryrun_sm.get("switching_candidate_count", 0) != 6:
        blockers.append("switching candidate count must be 6 from recovery dryrun")

    if backbone_sm.get("layer_count") != 8:
        blockers.append("8-layer backbone required")
    if not health_layer.get("contract_id"):
        blockers.append("health_management_layer_contract required")
    if survival_contract.get("candidate_type") != "survival_drive_candidate":
        blockers.append("survival_drive_candidate contract required")
    if backbone_sm.get("active_drive_execution_enabled_now") is not False:
        blockers.append("active_drive_execution must remain false")

    if roadmap_sm.get("next_route") != ROUTE_C:
        blockers.append("roadmap next_route must be Route C")

    input_review = {
        "review_id": "model_registry_canonical_input_review_v1",
        "upstream_post_review_root": str(post_root),
        "upstream_verifier_go": post_go,
        "b_lite_closed": post_sm.get("b_lite_canonical_v0_baseline_closed"),
        "registry_version": post_sm.get("registry_version"),
        "schema_version": post_sm.get("schema_version"),
        "production_registry": False,
        "model_invocation_disabled": post_sm.get("model_runtime_invoked_now") is False,
        "health_candidates_from_recovery": recovery_dryrun_sm.get("health_candidate_count"),
        "switching_candidates_from_recovery": recovery_dryrun_sm.get("switching_candidate_count"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    scope = {
        "scope_id": "health_management_layer_scope_v1",
        "layer_key": "health_management",
        "eight_layer_defined": backbone_sm.get("layer_count") == 8,
        "blocks": [
            {
                "block_id": "software_health_management",
                "responsibilities": [
                    "model health state consumption",
                    "provider timeout signal",
                    "gate health",
                    "module availability",
                    "candidate pipeline health",
                    "runtime boundary status",
                    "error_count / latency / timeout / degraded / disabled",
                ],
                "output_candidates": list(SOFTWARE_OUTPUT_CANDIDATES),
            },
            {
                "block_id": "hardware_health_management",
                "responsibilities": [
                    "camera availability",
                    "microphone availability",
                    "speaker availability",
                    "battery",
                    "temperature",
                    "storage",
                    "network",
                    "compute pressure",
                    "sensor status",
                    "multi-camera readiness later",
                ],
                "output_candidates": list(HARDWARE_OUTPUT_CANDIDATES),
                "no_hardware_control_in_planning": True,
            },
            {
                "block_id": "system_monitor_robustness",
                "responsibilities": [
                    "software + hardware + information channel monitoring",
                    "resource allocation candidate",
                    "degraded operating mode candidate",
                    "fallback route candidate",
                    "survival minimum operating mode candidate",
                    "missing label / failed tagging recovery candidate",
                    "partial failure recovery candidate",
                ],
                "output_candidates": list(SYSTEM_OUTPUT_CANDIDATES),
            },
        ],
        **meta,
    }

    software_contract = {
        "contract_id": "software_health_management_contract_v1",
        "block": "software_health_management",
        "consumes": list(HEALTH_STATES) + ["error_count", "latency_budget_ms"],
        "output_candidates": list(SOFTWARE_OUTPUT_CANDIDATES),
        "monitor_enabled_now": False,
        **meta,
    }

    hardware_contract = {
        "contract_id": "hardware_health_management_contract_v1",
        "block": "hardware_health_management",
        "monitors_planned": [
            "camera",
            "microphone",
            "speaker",
            "battery",
            "temperature",
            "storage",
            "network",
            "compute_pressure",
            "sensor_status",
        ],
        "output_candidates": list(HARDWARE_OUTPUT_CANDIDATES),
        "hardware_control_executed_now": False,
        "camera_control_executed_now": False,
        "no_real_hardware_read_in_planning": True,
        **meta,
    }

    system_contract = {
        "contract_id": "system_monitor_contract_v1",
        "block": "system_monitor_robustness",
        "channels": ["software", "hardware", "information"],
        "output_candidates": list(SYSTEM_OUTPUT_CANDIDATES),
        "system_monitor_enabled_now": False,
        **meta,
    }

    signal_contract = {
        "contract_id": "health_signal_candidate_contract_v1",
        "fields": list(HEALTH_SIGNAL_CONTRACT_FIELDS),
        "severity_taxonomy": list(SEVERITY_TAXONOMY),
        "health_status_taxonomy": list(HEALTH_STATUS_TAXONOMY),
        "defaults": {
            "candidate_only": True,
            "fact_status": "not_fact",
            "action_allowed": False,
            "user_facing_output_allowed": False,
            "write_allowed": False,
        },
        "allowed_output_fields": list(HEALTH_OUTPUT_ALLOWED_FIELDS),
        "forbidden_output_fields": list(HEALTH_OUTPUT_FORBIDDEN_FIELDS),
        "health_score_defined": False,
        **meta,
    }

    model_fallback_plan = {
        "plan_id": "model_health_to_fallback_candidate_plan_v1",
        "consumes_model_health_states": list(HEALTH_STATES),
        "consumes_switching_scenarios": [s[0] for s in SWITCHING_SCENARIOS],
        "routes": [
            {"from": "failed", "to": "fallback_candidate"},
            {"from": "timeout", "to": "hold_candidate"},
            {"from": "degraded", "to": "fallback_required_candidate"},
        ],
        "fallback_executed_now": False,
        "model_switch_executed_now": False,
        **meta,
    }

    hardware_degrade_plan = {
        "plan_id": "hardware_health_to_degradation_candidate_plan_v1",
        "routes": [
            {"from": "resource_pressure", "to": "hardware_degradation_candidate"},
            {"from": "camera_unavailable", "to": "camera_unavailable_candidate"},
            {"from": "compute_pressure", "to": "resource_pressure_candidate"},
        ],
        "degradation_executed_now": False,
        **meta,
    }

    survival_plan = {
        "plan_id": "system_monitor_to_survival_drive_candidate_plan_v1",
        "routes": [
            {"from": "system_anomaly", "to": "recovery_plan_candidate"},
            {"from": "critical_failure", "to": "survival_drive_candidate"},
            {"from": "partial_failure", "to": "degraded_mode_candidate"},
        ],
        "survival_drive_candidate_only": True,
        "active_drive_execution_enabled": False,
        **meta,
    }

    drive_bridge = {
        "plan_id": "health_to_drive_layer_bridge_plan_v1",
        "routes": list(HEALTH_TO_DRIVE_ROUTES),
        "constraints": [
            "active_drive_execution_enabled=false",
            "survival_drive_candidate is candidate only",
            "no task commit",
            "no user-facing output",
            "no hardware control",
        ],
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "health_runtime_boundary_matrix_v1",
        "checks": list(RUNTIME_BOUNDARY_CHECKS),
        "all_blocked_in_planning": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "health_management_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_goals": [
            "consume model_health_state_candidate 6 statuses",
            "consume model_switching_candidate 6 scenarios",
            "generate health_signal_candidate samples",
            "generate fallback_candidate / degradation_candidate / survival_drive_candidate samples",
            "route health signals to Drive Layer candidates",
            "keep all actions blocked",
        ],
        "dryrun_forbidden": list(PLANNING_FORBIDDEN),
        **meta,
    }

    metric_reserved_policy = {
        "policy_id": "health_metric_reserved_policy_v1",
        "health_metric_definition_status": HEALTH_METRIC_DEFINITION_STATUS,
        "formal_health_metrics_defined": False,
        "health_score_calculation_enabled_now": False,
        "health_threshold_policy_enabled_now": False,
        "reasons_not_to_define_now": list(METRIC_NOT_DEFINED_REASONS),
        "allowed_now": list(METRIC_ALLOWED_NOW),
        "forbidden_now": list(METRIC_FORBIDDEN_NOW),
        "allowed_health_outputs": list(HEALTH_OUTPUT_ALLOWED_FIELDS),
        "forbidden_health_outputs": list(HEALTH_OUTPUT_FORBIDDEN_FIELDS),
        "future_definition_phase": FUTURE_METRIC_DEFINITION_PHASE,
        **meta,
    }

    metric_future_plan = {
        "plan_id": "health_metric_future_definition_plan_v1",
        "future_definition_phase": FUTURE_METRIC_DEFINITION_PHASE,
        "categories": list(FUTURE_METRIC_CATEGORIES),
        "all_metrics_reserved": True,
        "notes": "future metric categories reserved — not_defined_now",
        **meta,
    }

    planning_ok = len(blockers) == 0

    planning_decision = {
        "decision_id": "health_management_integration_planning_decision_v1",
        "planning_complete": planning_ok,
        "selected_route": ROUTE_C,
        "final_decision": FINAL_DECISION_GO if planning_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "health_management_integration_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "route": ROUTE_C,
        "principles": [
            "planning_only_no_monitors_no_actions",
            "health_signals_as_candidates_only",
            "bridge_to_drive_without_execution",
            "health_metrics_reserved_not_defined",
        ],
        "forbidden_in_planning": list(PLANNING_FORBIDDEN),
        **meta,
    }

    non_claims = {
        "register_id": "health_management_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_ok,
        "violations": blockers,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "selected_route": ROUTE_C,
        "b_lite_canonical_v0_baseline_closed": post_sm.get("b_lite_canonical_v0_baseline_closed"),
        "health_candidate_count_upstream": recovery_dryrun_sm.get("health_candidate_count"),
        "switching_candidate_count_upstream": recovery_dryrun_sm.get("switching_candidate_count"),
        "high_risk_count": 0 if planning_ok else 1,
        **meta,
    }

    return {
        "health_management_integration_planning_policy": policy,
        "model_registry_canonical_input_review": input_review,
        "health_management_layer_scope": scope,
        "software_health_management_contract": software_contract,
        "hardware_health_management_contract": hardware_contract,
        "system_monitor_contract": system_contract,
        "health_signal_candidate_contract": signal_contract,
        "model_health_to_fallback_candidate_plan": model_fallback_plan,
        "hardware_health_to_degradation_candidate_plan": hardware_degrade_plan,
        "system_monitor_to_survival_drive_candidate_plan": survival_plan,
        "health_to_drive_layer_bridge_plan": drive_bridge,
        "health_runtime_boundary_matrix": boundary_matrix,
        "health_management_dryrun_plan": dryrun_plan,
        "health_metric_reserved_policy": metric_reserved_policy,
        "health_metric_future_definition_plan": metric_future_plan,
        "health_management_non_claims_register": non_claims,
        "health_management_integration_planning_decision": planning_decision,
        "summary": summary,
    }
