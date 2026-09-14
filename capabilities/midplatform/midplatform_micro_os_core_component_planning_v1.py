# -*- coding: utf-8 -*-
"""Luna Midplatform 1.0 Micro-OS Core Component Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_micro_os_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
)
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import (
    COMPONENT_RESPONSIBILITIES,
    HEALTH_METRICS,
)

PHASE_ID = "Phase-Midplatform-Micro-OS-Core-Component-Planning-v1-001"
SCOPE = "midplatform_micro_os_core_component_planning_only"
SOURCE_CHAIN = "midplatform_micro_os_core_component_planning_v1"

UPSTREAM_DRYRUN_FINAL = DRYRUN_FINAL_GO
UPSTREAM_DRYRUN_NEXT = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_MICRO_OS_CORE_COMPONENT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_MICRO_OS_CORE_COMPONENT_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Micro-OS-Core-Component-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Micro-OS-Core-Component-Issue-Review-v1-001"

CORE_COMPONENT_IDS: Tuple[str, ...] = tuple(c["component_id"] for c in COMPONENT_RESPONSIBILITIES)

INFORMATION_TYPES: Tuple[str, ...] = (
    "standardized_candidate",
    "event",
    "working_memory_entry",
    "task_state_snapshot",
    "drive_signal_candidate",
    "health_report_candidate",
    "resource_state_candidate",
    "governance_check_result",
    "spatiotemporal_slot_ref",
    "priority_assignment",
    "integration_result_candidate",
    "allocation_result_candidate",
    "decision_context_candidate",
    "output_candidate",
    "admission_candidate",
    "recall_context",
    "recovery_candidate",
)

COMPONENT_EDGES: Tuple[Dict[str, str], ...] = (
    {"from": "module_adapter_layer", "to": "event_bus", "relation": "standardized_candidate/event"},
    {"from": "event_bus", "to": "working_memory", "relation": "working_memory_entry"},
    {"from": "event_bus", "to": "scheduler", "relation": "event/priority_hint"},
    {"from": "event_bus", "to": "health_resource_manager", "relation": "health_report_candidate"},
    {"from": "working_memory", "to": "task_manager", "relation": "task_state_snapshot"},
    {"from": "working_memory", "to": "worldmodel_memory_bridge", "relation": "recall_context/admission_candidate"},
    {"from": "scheduler", "to": "task_manager", "relation": "priority_assignment"},
    {"from": "scheduler", "to": "watchdog_recovery_manager", "relation": "long_pending_signal"},
    {"from": "drive_manager", "to": "scheduler", "relation": "drive_signal_candidate"},
    {"from": "drive_manager", "to": "task_manager", "relation": "goal_attention_profile"},
    {"from": "health_resource_manager", "to": "scheduler", "relation": "resource_state_candidate"},
    {"from": "health_resource_manager", "to": "watchdog_recovery_manager", "relation": "degraded_mode_hint"},
    {"from": "governance_gate_manager", "to": "midplatform_kernel", "relation": "governance_check_result"},
    {"from": "governance_gate_manager", "to": "output_gate_bridge", "relation": "output_permission"},
    {"from": "governance_gate_manager", "to": "worldmodel_memory_bridge", "relation": "admission_permission"},
    {"from": "worldmodel_memory_bridge", "to": "working_memory", "relation": "recall_context"},
    {"from": "output_gate_bridge", "to": "governance_gate_manager", "relation": "output_candidate_precheck"},
    {"from": "watchdog_recovery_manager", "to": "midplatform_kernel", "relation": "recovery_candidate"},
    {"from": "midplatform_kernel", "to": "event_bus", "relation": "orchestration_signal"},
)

MANAGEMENT_LOGIC: Dict[str, str] = {
    "permission": "governance_gate_manager",
    "resource": "health_resource_manager",
    "information_state": "event_bus + working_memory",
    "task_state": "task_manager",
    "priority": "scheduler",
    "drive_signal": "drive_manager",
    "deposit_boundary": "worldmodel_memory_bridge",
    "output_boundary": "output_gate_bridge",
    "anomaly": "watchdog_recovery_manager",
    "kernel_consistency": "midplatform_kernel",
}

HEALTH_METRIC_COMPONENT_MAP: Dict[str, str] = {
    "midplatform_alive": "midplatform_kernel",
    "event_loop_active": "midplatform_kernel",
    "core_bus_operational": "event_bus",
    "queue_processing_active": "event_bus",
    "pending_candidate_count": "event_bus",
    "stale_candidate_count": "working_memory",
    "latency": "event_bus",
    "health_tag_missing_count": "module_adapter_layer",
    "schema_invalid_count": "governance_gate_manager",
    "ttl_violation_count": "working_memory",
    "conflict_unresolved_count": "working_memory",
    "gap_unresolved_count": "working_memory",
    "fallback_trigger_count": "health_resource_manager",
    "degraded_mode_active": "watchdog_recovery_manager",
    "last_checkpoint_time": "watchdog_recovery_manager",
}

MODEL_RULE_ALGORITHM_MAP: Dict[str, Dict[str, str]] = {
    "midplatform_kernel": {"primary": "rule / state machine", "model": "none", "algorithm": "orchestration state machine"},
    "event_bus": {"primary": "rule / schema", "model": "none", "algorithm": "queue routing algorithm"},
    "working_memory": {"primary": "state machine", "model": "none", "algorithm": "TTL / cache policy"},
    "scheduler": {"primary": "priority algorithm / rule", "model": "none", "algorithm": "P0-P5 scheduling"},
    "task_manager": {"primary": "task state machine / rule", "model": "optional local text classifier input later", "algorithm": "phase transition rules"},
    "drive_manager": {"primary": "drive rule / goal template", "model": "optional local intent parse later", "algorithm": "priority_boost rules"},
    "module_adapter_layer": {"primary": "schema / adapter rule", "model": "none", "algorithm": "normalization validation"},
    "health_resource_manager": {"primary": "metrics / rule", "model": "none", "algorithm": "health aggregation"},
    "governance_gate_manager": {"primary": "rule / gate / validation", "model": "none", "algorithm": "permission evaluation"},
    "worldmodel_memory_bridge": {"primary": "admission / recall rule", "model": "optional summarization later", "algorithm": "admission boundary check"},
    "output_gate_bridge": {"primary": "output gate rule", "model": "optional expression model later", "algorithm": "gate handoff routing"},
    "watchdog_recovery_manager": {"primary": "health rule", "model": "none", "algorithm": "timeout / recovery state machine"},
}

NON_CLAIMS: Tuple[str, ...] = (
    "Core Component Planning ≠ implementation",
    "Core Component Planning ≠ runtime enabled",
    "Core Component Planning ≠ real Event Bus enabled",
    "Core Component Planning ≠ real Working Memory enabled",
    "Core Component Planning ≠ real Scheduler enabled",
    "Core Component Planning ≠ task chain execution",
    "Core Component Planning ≠ model invoked",
    "Core Component Planning ≠ provider invoked",
    "Core Component Planning ≠ Memory / WorldModel write",
    "Core Component Planning ≠ user output",
    "Core Component Planning ≠ real health monitoring runtime",
    "Core Component Planning ≠ real recovery executed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("midplatform_micro_os_core_component_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "model_invoked_now",
    "provider_invoked_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
    "real_task_chain_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "real_health_monitoring_enabled_now",
    "recovery_executed_now",
    "module_runtime_modified_now",
)

DEFAULT_PLANNING_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_architecture_planning"
DEFAULT_DRYRUN_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_architecture_dryrun_and_review"
DEFAULT_OUTPUT_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_core_component_planning"


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "module_definition_template_ref": TEMPLATE_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
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


def _failure_routes(component_id: str) -> List[Dict[str, Any]]:
    common = [
        {
            "route_id": f"{component_id}_schema_invalid",
            "detection_signal": "schema_invalid_count",
            "impact": "candidate rejected at component boundary",
            "default_response": "discard + governance_check_result",
            "recovery_candidate": "revalidate_after_gate_clearance",
            "forbidden_shortcut": "coerce_invalid_schema",
        },
        {
            "route_id": f"{component_id}_health_tag_missing",
            "detection_signal": "health_tag_missing_count",
            "impact": "intake throttled or held",
            "default_response": "hold_mode_candidate",
            "recovery_candidate": "health_resource_clearance",
            "forbidden_shortcut": "assume_healthy",
        },
        {
            "route_id": f"{component_id}_queue_backlog",
            "detection_signal": "pending_candidate_count_high",
            "impact": "processing delay",
            "default_response": "degraded_mode_candidate",
            "recovery_candidate": "queue_drain_supervised",
            "forbidden_shortcut": "silent_drop_without_trace",
        },
    ]
    extras: Dict[str, List[Dict[str, Any]]] = {
        "watchdog_recovery_manager": [
            {
                "route_id": "recovery_failed",
                "detection_signal": "recovery_flow_failed",
                "impact": "system-wide hold",
                "default_response": "safety_only_mode_candidate",
                "recovery_candidate": "manual_supervised_recovery",
                "forbidden_shortcut": "auto_full_restore",
            },
        ],
        "governance_gate_manager": [
            {
                "route_id": "unauthorized_runtime_attempt",
                "detection_signal": "runtime_permission_denied",
                "impact": "blocked execution path",
                "default_response": "violation_report_candidate",
                "recovery_candidate": "governance_review",
                "forbidden_shortcut": "bypass_gate",
            },
        ],
        "working_memory": [
            {
                "route_id": "ttl_violation",
                "detection_signal": "ttl_violation_count",
                "impact": "stale entries",
                "default_response": "expire_entry",
                "recovery_candidate": "re_ingest_observation",
                "forbidden_shortcut": "treat_wm_as_memory",
            },
        ],
    }
    return common + extras.get(component_id, [])


def _build_component_contract(spec: Dict[str, Any]) -> Dict[str, Any]:
    cid = spec["component_id"]
    return {
        "contract_id": f"{cid}_core_component_contract_v1",
        "template_id": TEMPLATE_ID,
        "template_sections": list(TEMPLATE_SECTIONS),
        "micro_os_layers": spec.get("layers", []),
        "module_identity": {
            "module_id": cid,
            "module_type": "midplatform_micro_os_core_component",
            "role": spec["role"],
            "system_layer": spec.get("system_layer", "Domain"),
            "one_liner": spec.get("one_liner", spec["role"]),
        },
        "upstream_sources": {
            "upstream_modules": spec.get("upstream_modules", []),
            "upstream_object_types": spec.get("upstream_object_types", []),
            "required_inputs": spec.get("required_inputs", ["source_chain"]),
            "optional_inputs": spec.get("optional_inputs", []),
            "forbidden_inputs": spec.get("forbidden_inputs", ["direct_fact", "user_output_directive"]),
        },
        "downstream_targets": {
            "downstream_modules": spec.get("downstream_modules", []),
            "downstream_object_types": spec.get("downstream_object_types", []),
            "allowed_outputs": spec.get("allowed_outputs", []),
            "forbidden_outputs": spec.get("forbidden_outputs", ["fact", "user_output", "memory_write", "worldmodel_write"]),
        },
        "input_contract": {
            "input_contract": f"{cid}_input_contract_v1",
            "source_chain": "required",
            "evidence_ref": "required_when_forwarding",
            "ttl": "required",
            "confidence": "required_where_applicable",
            "risk_flag": "optional",
            "candidate_only": True,
        },
        "processing_scope": {
            "processing_scope": spec.get("processing_scope", spec["role"]),
            "allowed_transformation": spec.get("allowed_transformation", []),
            "forbidden_transformation": spec.get("forbidden_transformation", []),
            "arbitration_allowed": spec.get("arbitration_allowed", False),
            "write_allowed": False,
            "provider_invocation_allowed": False,
        },
        "output_contract": {
            "output_contract": f"{cid}_output_contract_v1",
            "output_object_type": spec.get("primary_output", "candidate"),
            "decision_refs": "preserved_when_applicable",
            "evidence_refs": "preserved",
            "validation_refs": "preserved",
            "fact_status": "candidate_not_fact",
            "write_allowed": False,
            "user_output_allowed": False,
        },
        "module_principles": {
            "module_principles": spec.get("principles", []),
            "priority_policy": "midplatform_priority_and_scheduling_policy_v1",
            "conflict_policy": "governance_gate_manager_resolves_hard_boundaries",
            "fallback_policy": spec.get("fallback_policy", "degraded_mode_candidate"),
            "rollback_policy": "candidate_only_no_commit",
        },
        "external_constraints": {
            "constitution_constraints": "consume L0 refs; cannot override",
            "domain_standard_constraints": "consume governance standards; no parallel governance",
            "validation_gate_constraints": "pass through governance_gate_manager",
            "health_signal_constraints": "consume health_report_candidate",
            "whitebox_visibility_constraints": "trace_refs required",
            "decision_center_constraints": "handoff only; no direct decision commit",
        },
        "runtime_boundaries": {
            "runtime_enabled_now": False,
            "write_allowed_now": False,
            "provider_invocation_allowed_now": False,
            "user_output_allowed_now": False,
            "memory_allowed_now": False,
            "world_model_allowed_now": False,
        },
        "failure_and_traceability": {
            "failure_route": _failure_routes(cid),
            "issue_trace": "issue_trace_candidate",
            "violation_report": "violation_report_candidate",
            "escalation_path": "watchdog_recovery_manager",
            "audit_required": True,
        },
        "forbidden_actions": spec.get("forbidden_actions", []),
    }


COMPONENT_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "component_id": "midplatform_kernel",
        "layers": ["L0", "L3", "L6"],
        "system_layer": "Decision",
        "role": "Micro-OS core coordination entry connecting Governance, Event Bus, Scheduler, Health Supervisor",
        "one_liner": "协调入口；不直接执行/输出/写/调模型",
        "upstream_modules": ["governance_gate_manager", "health_resource_manager", "watchdog_recovery_manager"],
        "downstream_modules": ["event_bus", "scheduler", "working_memory"],
        "allowed_outputs": ["orchestration_signal", "handoff_candidate"],
        "processing_scope": "coordinate core component handoffs under L0/L8 constraints",
        "forbidden_transformation": ["direct_model_call", "direct_task_execution", "direct_user_output", "memory_write", "worldmodel_write"],
        "forbidden_actions": ["direct model invocation", "direct task execution", "direct output", "direct Memory/WorldModel write"],
        "principles": ["kernel coordinates; does not sovereignly decide or execute"],
    },
    {
        "component_id": "event_bus",
        "layers": ["L3"],
        "system_layer": "Assembly",
        "role": "Distribute standardized_candidate / signal / event / health_report / feedback",
        "upstream_modules": ["module_adapter_layer", "midplatform_kernel", "health_resource_manager"],
        "downstream_modules": ["working_memory", "scheduler", "health_resource_manager"],
        "upstream_object_types": ["standardized_candidate", "event", "health_report_candidate"],
        "downstream_object_types": ["event", "working_memory_entry", "priority_hint"],
        "allowed_outputs": ["event", "routed_candidate_ref"],
        "forbidden_transformation": ["semantic_arbitration", "candidate_rewrite", "fact_generation"],
        "forbidden_actions": ["semantic ruling", "rewrite candidates", "generate facts", "bypass governance"],
        "principles": ["route only; preserve candidate integrity"],
    },
    {
        "component_id": "working_memory",
        "layers": ["L3"],
        "system_layer": "Assembly",
        "role": "Runtime candidate cache; Working Memory ≠ Memory ≠ WorldModel",
        "upstream_modules": ["event_bus", "worldmodel_memory_bridge", "task_manager"],
        "downstream_modules": ["scheduler", "task_manager", "worldmodel_memory_bridge"],
        "allowed_outputs": ["working_memory_entry", "task_state_snapshot", "pending_candidate", "conflict_candidate", "gap_candidate"],
        "forbidden_transformation": ["long_term_persist", "fact_commit", "replace_worldmodel"],
        "forbidden_actions": ["long-term deposit", "write facts", "substitute WorldModel/Memory"],
        "principles": ["Working Memory ≠ Memory", "Working Memory ≠ WorldModel", "TTL required"],
    },
    {
        "component_id": "scheduler",
        "layers": ["L5", "L6"],
        "system_layer": "Decision",
        "role": "P0-P5 priority scheduling using TTL, health, resource, task state",
        "upstream_modules": ["event_bus", "working_memory", "drive_manager", "health_resource_manager", "task_manager"],
        "downstream_modules": ["task_manager", "watchdog_recovery_manager"],
        "allowed_outputs": ["priority_assignment", "schedule_plan_candidate"],
        "forbidden_transformation": ["direct_runtime_execution", "p3_p4_p5_block_p0_p1"],
        "forbidden_actions": ["direct task execution", "direct runtime call", "allow P3/P4/P5 to block P0/P1"],
        "principles": ["P0 preempts; P5 discardable; P1 not blocked by P3-P5"],
    },
    {
        "component_id": "task_manager",
        "layers": ["L5"],
        "system_layer": "Decision",
        "role": "Maintain task_state, task_phase, task_blocker, task_resume, task_handoff_candidate",
        "upstream_modules": ["scheduler", "working_memory", "drive_manager"],
        "downstream_modules": ["scheduler", "output_gate_bridge"],
        "allowed_outputs": ["task_state_snapshot", "task_handoff_candidate", "task_resume_placeholder"],
        "forbidden_transformation": ["execute_task_chain", "bypass_decision_center", "bypass_gate_chain"],
        "forbidden_actions": ["execute task chain", "bypass Decision Center", "bypass Gate Chain"],
        "principles": ["task state only; execution requires downstream gates"],
    },
    {
        "component_id": "drive_manager",
        "layers": ["L5"],
        "system_layer": "Decision",
        "role": "Survival/Task Drive signals: drive_signal_candidate, goal_attention_profile, priority_boost",
        "upstream_modules": ["health_resource_manager", "working_memory"],
        "downstream_modules": ["scheduler", "task_manager"],
        "allowed_outputs": ["drive_signal_candidate", "goal_attention_profile", "priority_boost", "blocking_condition"],
        "forbidden_transformation": ["action_command", "user_output"],
        "forbidden_actions": ["direct action commands", "direct user output"],
        "principles": ["drive influences attention; does not execute"],
    },
    {
        "component_id": "module_adapter_layer",
        "layers": ["L2"],
        "system_layer": "Domain",
        "role": "Normalize Vision/OCR/ASR/TTS/Map/Sensor/User/WorldContinuity outputs to standardized_candidate",
        "upstream_modules": ["external_modules_later"],
        "downstream_modules": ["event_bus", "governance_gate_manager"],
        "allowed_outputs": ["standardized_candidate", "event"],
        "forbidden_transformation": ["provider_runtime", "model_inference", "fact_generation", "direct_decision_center"],
        "forbidden_actions": ["invoke provider", "run model", "generate fact", "enter Decision Center directly"],
        "principles": ["adapter normalizes; does not decide"],
    },
    {
        "component_id": "health_resource_manager",
        "layers": ["L1", "L8"],
        "system_layer": "Health",
        "role": "Module/provider health, resource state, local/cloud availability, latency, queue backlog",
        "upstream_modules": ["module_adapter_layer", "event_bus"],
        "downstream_modules": ["scheduler", "watchdog_recovery_manager", "midplatform_kernel"],
        "allowed_outputs": ["health_report_candidate", "resource_state_candidate", "degraded_capability_hint"],
        "forbidden_transformation": ["final_task_arbitration", "replace_governance_gate"],
        "forbidden_actions": ["final task ruling", "replace Governance Gate"],
        "principles": ["health/resource signals only; not sovereign arbitrator"],
    },
    {
        "component_id": "governance_gate_manager",
        "layers": ["L0"],
        "system_layer": "Constitution",
        "role": "Constitution/Validation/Whitebox/Permission/Candidate-Fact/Output/Runtime/Memory-WorldModel gates",
        "upstream_modules": ["constitution_bus_later", "all_executable_paths"],
        "downstream_modules": ["midplatform_kernel", "output_gate_bridge", "worldmodel_memory_bridge", "module_adapter_layer"],
        "allowed_outputs": ["governance_check_result", "gate_result_candidate"],
        "forbidden_transformation": ["business_candidate_generation", "semantic_reasoning", "unauthorized_runtime_write_output"],
        "forbidden_actions": ["generate business candidates", "semantic reasoning", "authorize runtime/write/output without policy"],
        "principles": ["hard boundary for all executable/writable/output paths"],
        "arbitration_allowed": True,
    },
    {
        "component_id": "worldmodel_memory_bridge",
        "layers": ["L7"],
        "system_layer": "Assembly",
        "role": "admission_candidate out; recall_context/hint/known_state_candidate/change_detection_reference in",
        "upstream_modules": ["working_memory", "governance_gate_manager"],
        "downstream_modules": ["working_memory"],
        "allowed_outputs": ["admission_candidate", "recall_context"],
        "forbidden_transformation": ["direct_memory_write", "direct_worldmodel_write", "override_realtime_safety"],
        "forbidden_actions": ["direct Memory/WorldModel write", "historical deposit overrides realtime safety"],
        "principles": ["admission candidate only outbound; recall context only inbound"],
    },
    {
        "component_id": "output_gate_bridge",
        "layers": ["L7"],
        "system_layer": "Output",
        "role": "Hand off output_candidate / speech_candidate / display_candidate to gates later",
        "upstream_modules": ["task_manager", "governance_gate_manager"],
        "downstream_modules": ["governance_gate_manager"],
        "allowed_outputs": ["output_candidate", "speech_candidate", "display_candidate"],
        "forbidden_transformation": ["user_output", "tts_runtime", "bypass_speech_gate"],
        "forbidden_actions": ["direct user output", "bypass Speech Gate", "direct TTS runtime"],
        "principles": ["handoff only; gated output later"],
    },
    {
        "component_id": "watchdog_recovery_manager",
        "layers": ["L8"],
        "system_layer": "Health",
        "role": "Monitor failure modes; emit degraded/safety-only/hold/recovery candidates",
        "upstream_modules": ["health_resource_manager", "scheduler", "event_bus", "working_memory"],
        "downstream_modules": ["midplatform_kernel", "health_resource_manager"],
        "allowed_outputs": ["recovery_candidate", "degraded_mode_candidate", "hold_mode_candidate", "watchdog_alert"],
        "forbidden_transformation": ["real_restart", "real_recovery_execution"],
        "forbidden_actions": ["execute real restart", "execute real recovery"],
        "principles": ["recovery_candidate only; no real recovery in planning phase"],
    },
)


def run_midplatform_micro_os_core_component_planning_v1(
    *,
    midplatform_micro_os_architecture_planning_root: str,
    midplatform_micro_os_architecture_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(midplatform_micro_os_architecture_planning_root).expanduser().resolve()
    dr_root = Path(midplatform_micro_os_architecture_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root), "upstream_planning_root": str(plan_root), "upstream_dryrun_root": str(dr_root)}

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    dr_vr = _try_read_json(dr_root / "verifier_report.json") or {}
    dr_sm = _try_read_json(dr_root / "summary.json") or {}
    dr_decision = _try_read_json(dr_root / "dryrun_readiness_decision_v1.json") or {}

    if plan_vr.get("verifier") != "GO":
        blockers.append("upstream architecture planning verifier must be GO")
    if dr_vr.get("verifier") != "GO":
        blockers.append("upstream dryrun verifier must be GO")
    if dr_sm.get("final_decision") != UPSTREAM_DRYRUN_FINAL:
        blockers.append("upstream dryrun final_decision mismatch")
    if dr_decision.get("architecture_consumable") is not True:
        blockers.append("dryrun architecture_consumable must be true")

    contracts: List[Dict[str, Any]] = []
    contract_issues: List[str] = []
    for spec in COMPONENT_SPECS:
        contract = _build_component_contract(spec)
        ok, issues = validate_module_definition(contract)
        if not ok:
            contract_issues.extend([f"{spec['component_id']}:{i}" for i in issues])
        contracts.append(contract)

    if contract_issues:
        blockers.extend(contract_issues[:5])
        if len(contract_issues) > 5:
            blockers.append(f"...and {len(contract_issues) - 5} more contract issues")

    scope = {
        "scope_id": "midplatform_core_component_scope_v1",
        "phase": PHASE_ID,
        "component_count": len(CORE_COMPONENT_IDS),
        "component_ids": list(CORE_COMPONENT_IDS),
        "planning_only": True,
        "implementation_later": True,
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    contract_collection = {
        "collection_id": "midplatform_core_component_contract_collection_v1",
        "template_ref": TEMPLATE_ID,
        "contracts": contracts,
        "contract_count": len(contracts),
        "all_ten_sections": all(
            all(s in c for s in TEMPLATE_SECTIONS) for c in contracts
        ),
        **meta,
    }

    updown_matrix = {
        "matrix_id": "midplatform_core_component_upstream_downstream_matrix_v1",
        "edges": list(COMPONENT_EDGES),
        "edge_count": len(COMPONENT_EDGES),
        "watchdog_monitors_all": True,
        "governance_gate_hard_boundary": True,
        **meta,
    }

    information_contract = {
        "contract_id": "midplatform_core_component_information_contract_v1",
        "information_types": list(INFORMATION_TYPES),
        "type_count": len(INFORMATION_TYPES),
        **meta,
    }

    management_logic = {
        "logic_id": "midplatform_core_component_management_logic_v1",
        "assignments": MANAGEMENT_LOGIC,
        **meta,
    }

    mra_map = {
        "map_id": "midplatform_core_component_model_rule_algorithm_map_v1",
        "components": MODEL_RULE_ALGORITHM_MAP,
        "no_model_in_governance_gate": MODEL_RULE_ALGORITHM_MAP["governance_gate_manager"]["model"] == "none",
        "no_model_in_watchdog": MODEL_RULE_ALGORITHM_MAP["watchdog_recovery_manager"]["model"] == "none",
        **meta,
    }

    failure_matrix = {
        "matrix_id": "midplatform_core_component_failure_route_matrix_v1",
        "components": {
            c["component_id"]: _failure_routes(c["component_id"]) for c in COMPONENT_SPECS
        },
        "min_routes_per_component": 3,
        **meta,
    }

    health_mapping = {
        "mapping_id": "midplatform_core_component_health_metric_mapping_v1",
        "metric_to_component": HEALTH_METRIC_COMPONENT_MAP,
        "metric_count": len(HEALTH_METRICS),
        "all_metrics_mapped": all(m in HEALTH_METRIC_COMPONENT_MAP for m in HEALTH_METRICS),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "midplatform_core_component_boundary_matrix_v1",
        "components": {cid: {f: False for f in BOUNDARY_FALSE} for cid in CORE_COMPONENT_IDS},
        "global_boundaries": {f: False for f in BOUNDARY_FALSE},
        **meta,
    }

    planning_pass = len(blockers) == 0 and len(contracts) == 12 and contract_collection["all_ten_sections"]
    readiness = {
        "decision_id": "midplatform_core_component_planning_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "contracts_validated": len(contract_issues) == 0,
        "upstream_consumed": dr_decision.get("architecture_consumable") is True,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "component_count": len(contracts),
        "planning_pass": planning_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        **meta,
    }

    return {
        "summary": summary,
        "midplatform_core_component_scope": scope,
        "midplatform_core_component_contract_collection": contract_collection,
        "midplatform_core_component_upstream_downstream_matrix": updown_matrix,
        "midplatform_core_component_information_contract": information_contract,
        "midplatform_core_component_management_logic": management_logic,
        "midplatform_core_component_model_rule_algorithm_map": mra_map,
        "midplatform_core_component_failure_route_matrix": failure_matrix,
        "midplatform_core_component_health_metric_mapping": health_mapping,
        "midplatform_core_component_boundary_matrix": boundary_matrix,
        "midplatform_core_component_planning_readiness_decision": readiness,
        "midplatform_core_component_non_claims_register": {
            "register_id": "midplatform_core_component_non_claims_register_v1",
            "non_claims": list(NON_CLAIMS),
            **meta,
        },
    }
