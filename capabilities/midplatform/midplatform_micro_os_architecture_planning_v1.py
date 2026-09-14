# -*- coding: utf-8 -*-
"""Luna Midplatform 1.0 — Micro-OS Architecture Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE

PHASE_ID = "Phase-Midplatform-Micro-OS-Architecture-Planning-v1-001"
SCOPE = "midplatform_micro_os_architecture_planning_only"
SOURCE_CHAIN = "midplatform_micro_os_architecture_planning_v1"

MIDPLATFORM_1_0_NAME = "Luna Midplatform 1.0"
MIDPLATFORM_1_0_FORM = "Luna Midplatform Micro-OS Architecture"
MIDPLATFORM_1_0_LABEL_ZH = "中台 1.0 形态"

FINAL_DECISION_GO = "MIDPLATFORM_MICRO_OS_ARCHITECTURE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_MICRO_OS_ARCHITECTURE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Micro-OS-Architecture-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Micro-OS-Architecture-Issue-Review-v1-001"

LAYER_IDS: Tuple[str, ...] = tuple(f"L{i}" for i in range(9))

LAYER_COMMON_FIELDS: Tuple[str, ...] = (
    "layer_id",
    "layer_name",
    "layer_role",
    "upstream_inputs",
    "downstream_outputs",
    "forbidden_actions",
    "global_constraint_role",
)

MICRO_OS_LAYER_DEFINITIONS: Tuple[Dict[str, Any], ...] = (
    {
        "layer_id": "L0",
        "layer_name": "Constitution / Governance Kernel",
        "layer_role": "Global governance kernel constraining L1–L7",
        "global_constraint_role": "constitution_kernel",
        "upstream_inputs": ["constitution_refs", "governance_standard_refs", "migration_constraints"],
        "downstream_outputs": [
            "permission_boundary",
            "gate_requirement",
            "candidate_fact_boundary",
            "validation_requirement",
            "whitebox_requirement",
            "memory_worldmodel_write_boundary",
            "output_gate_boundary",
            "runtime_provider_call_boundary",
        ],
        "forbidden_actions": [
            "direct_task_execution",
            "direct_user_output",
            "direct_memory_write",
            "direct_worldmodel_write",
            "direct_provider_invocation",
        ],
        "placed_artifacts": [
            "Luna Safety Constitution",
            "Constitution-Bus",
            "Governance Gate",
            "Validation Standard",
            "Whitebox Standard",
            "Permission Boundary",
            "Candidate-Fact Boundary",
        ],
    },
    {
        "layer_id": "L1",
        "layer_name": "Hardware / Runtime / Resource Substrate",
        "layer_role": "Resource substrate for L2–L7; answers whether/how/degraded",
        "global_constraint_role": "resource_substrate",
        "upstream_inputs": ["device_state", "network_state", "provider_health", "model_candidate_availability"],
        "downstream_outputs": [
            "runtime_permission_hint",
            "resource_budget_hint",
            "fallback_condition",
            "degraded_capability_hint",
            "local_cloud_availability_hint",
        ],
        "forbidden_actions": ["task_arbitration", "decision_finalization", "user_output"],
        "placed_artifacts": [
            "Controlled Runtime",
            "Provider Abstraction availability",
            "Model Profile Registry availability signals",
            "Network/Battery/Temperature/Resource budget",
        ],
    },
    {
        "layer_id": "L2",
        "layer_name": "Module Adapter & Input Layer",
        "layer_role": "Convert module outputs to standardized_candidate/event",
        "global_constraint_role": "input_adapter",
        "upstream_inputs": ["module_raw_output", "sensor_input", "user_input", "external_api_input"],
        "downstream_outputs": [
            "standardized_candidate",
            "event",
            "source_chain",
            "timestamp",
            "confidence",
            "spatial_anchor_or_missing",
            "health_tag",
            "ttl",
            "allowed_usage",
        ],
        "forbidden_actions": ["direct_fact_commit", "direct_worldmodel_write", "direct_user_output"],
        "placed_artifacts": [
            "Vision Module Adapter",
            "OCR Module Adapter",
            "ASR Module Adapter",
            "TTS Module Adapter",
            "Map/Navigation Module Adapter",
            "World Continuity later adapter",
            "Sensor/User/API input adapters",
        ],
    },
    {
        "layer_id": "L3",
        "layer_name": "Event Bus & Working Memory Layer",
        "layer_role": "Midplatform RAM/cache/queue; not long-term Memory or WorldModel",
        "global_constraint_role": "working_memory_bus",
        "upstream_inputs": ["standardized_candidate", "event", "task_state_snapshot"],
        "downstream_outputs": [
            "working_memory_entry",
            "priority_queue_item",
            "ttl_cache_entry",
            "pending_candidate",
            "conflict_candidate",
            "gap_candidate",
            "recent_world_state_candidate",
        ],
        "forbidden_actions": [
            "long_term_memory_write",
            "worldmodel_fact_commit",
            "treat_working_memory_as_memory",
        ],
        "placed_artifacts": [
            "Event Bus",
            "Working Memory",
            "Priority Queue",
            "TTL Cache",
        ],
    },
    {
        "layer_id": "L4",
        "layer_name": "Spatiotemporal World State Layer",
        "layer_role": "Organize information by unified spatiotemporal coordinates",
        "global_constraint_role": "world_state_layer",
        "upstream_inputs": ["working_memory_entry", "spatial_anchor", "scene_slot_hint"],
        "downstream_outputs": [
            "spatiotemporal_binding",
            "scene_slot",
            "world_object_candidate",
            "freshness_status",
            "scene_delta_candidate",
            "change_candidate",
        ],
        "forbidden_actions": ["module_source_primary_organization", "direct_fact_commit"],
        "placed_artifacts": [
            "STCM / Spatiotemporal Consistency Manager",
            "World Continuity spatiotemporal bindings",
        ],
    },
    {
        "layer_id": "L5",
        "layer_name": "Drive / Goal / Task Scheduling Layer",
        "layer_role": "Drive signals and task chain state without bypassing Decision/Gate",
        "global_constraint_role": "drive_task_scheduler",
        "upstream_inputs": [
            "health_signal",
            "resource_hint",
            "world_state_candidate",
            "user_goal_candidate",
            "memory_recall_hint",
        ],
        "downstream_outputs": [
            "drive_signal_candidate",
            "priority_boost",
            "attention_target",
            "blocking_condition",
            "required_observation_candidate",
            "task_state",
            "task_phase",
            "task_priority",
            "task_chain_cache_resume_placeholder",
        ],
        "forbidden_actions": ["direct_action_execution", "bypass_decision_center", "bypass_output_gate"],
        "placed_artifacts": [
            "Survival Drive",
            "Task Drive",
            "Scheduler",
            "Task Manager",
            "Task Chain cache/resume placeholder",
        ],
    },
    {
        "layer_id": "L6",
        "layer_name": "Information Integration & Allocation Layer",
        "layer_role": "Model/rule/algorithm mixed integration and allocation",
        "global_constraint_role": "integration_allocation",
        "upstream_inputs": [
            "working_memory_entry",
            "spatiotemporal_binding",
            "drive_signal_candidate",
            "task_context",
            "health_context",
        ],
        "downstream_outputs": [
            "priority_attention_map",
            "task_world_slice_candidate",
            "information_allocation_result",
            "conflict_candidate",
            "gap_candidate",
            "required_observation_candidate",
            "decision_context_candidate",
        ],
        "forbidden_actions": ["final_decision", "direct_runtime_execution", "direct_user_output"],
        "placed_artifacts": [
            "Information Integration Layer",
            "Information Allocation Layer",
        ],
    },
    {
        "layer_id": "L7",
        "layer_name": "Decision Context / Output / Memory-WorldModel Bridge Layer",
        "layer_role": "Downstream handoff only; no direct user output or writes",
        "global_constraint_role": "bridge_handoff",
        "upstream_inputs": [
            "decision_context_candidate",
            "integrated_context_candidate",
            "constitution_refs",
            "validation_result",
        ],
        "downstream_outputs": [
            "decision_center_handoff",
            "task_chain_handoff",
            "output_queue_candidate",
            "speech_gate_candidate",
            "display_gate_candidate",
            "output_plane_candidate",
            "frontend_guidance_candidate",
            "memory_admission_candidate",
            "worldmodel_admission_candidate",
        ],
        "forbidden_actions": [
            "direct_user_output",
            "direct_memory_write",
            "direct_worldmodel_write",
            "direct_runtime_execution",
        ],
        "placed_artifacts": [
            "Decision Center handoff",
            "Task Chain handoff",
            "Output Queue",
            "Speech Gate",
            "Display Gate",
            "Output Plane",
            "Frontend Guidance",
            "Memory Admission Bridge",
            "WorldModel Admission Bridge",
        ],
    },
    {
        "layer_id": "L8",
        "layer_name": "Health / Watchdog / Recovery Supervisor",
        "layer_role": "Global supervisory bypass monitoring L1–L7",
        "global_constraint_role": "health_supervisor_bypass",
        "upstream_inputs": [
            "module_health",
            "provider_health",
            "midplatform_self_health",
            "queue_metrics",
            "schema_validation_results",
        ],
        "downstream_outputs": [
            "health_tag",
            "degraded_mode_signal",
            "safety_only_mode_signal",
            "hold_mode_signal",
            "recovery_mode_signal",
            "watchdog_alert",
            "recovery_flow_candidate",
        ],
        "forbidden_actions": ["replace_l0_constitution", "silent_bypass_of_gates"],
        "placed_artifacts": [
            "Health Manager",
            "SystemHealth",
            "Watchdog",
            "Recovery Supervisor",
            "Health Enforcement Supervisor",
        ],
    },
)

GOVERNANCE_RELOCATION_ENTRIES: Tuple[Dict[str, Any], ...] = (
    {"artifact_id": "luna_safety_constitution", "artifact_name": "Luna Safety Constitution", "target_layer": "L0", "phase_ref": "Phase-Luna-Constitution-Capability-Bus-Governance-Baseline"},
    {"artifact_id": "constitution_bus", "artifact_name": "Constitution-Bus", "target_layer": "L0", "phase_ref": "Phase-Luna-Constitution-Capability-Bus-Governance-Baseline"},
    {"artifact_id": "governance_gate", "artifact_name": "Governance Gate", "target_layer": "L0", "phase_ref": "Phase-Midplatform-Safety-Gate"},
    {"artifact_id": "validation_standard", "artifact_name": "Validation Engineering Standard", "target_layer": "L0", "phase_ref": "Phase-Midplatform-Validation-Engineering-Separation"},
    {"artifact_id": "whitebox_standard", "artifact_name": "Whitebox Inspection Standard", "target_layer": "L0", "phase_ref": "Phase-Midplatform-Whitebox-Inspection-Integration"},
    {"artifact_id": "permission_boundary", "artifact_name": "Permission Boundary", "target_layer": "L0", "phase_ref": "Phase-Midplatform-Constitution-Governance-Hierarchy"},
    {"artifact_id": "candidate_fact_boundary", "artifact_name": "Candidate-Fact Boundary", "target_layer": "L0", "phase_ref": "Phase-Midplatform-Candidate-Evidence-Flow-Integration"},
    {"artifact_id": "controlled_runtime", "artifact_name": "Controlled Runtime", "target_layer": "L1", "phase_ref": "Phase-Midplatform-Controlled-Runtime"},
    {"artifact_id": "provider_abstraction", "artifact_name": "Provider Abstraction Standard", "target_layer": "L1", "phase_ref": "Phase-Provider-Abstraction-Standard-Alignment"},
    {"artifact_id": "model_profile_registry", "artifact_name": "Model Profile Registry", "target_layer": "L1", "phase_ref": "Phase-Model-Profile-Registry"},
    {"artifact_id": "module_binding_standard", "artifact_name": "Module Binding / Module Local Profile Standard", "target_layer": "L0", "secondary_layer": "L2", "phase_ref": "Phase-Module-Local-Model-Profile-Standardization"},
    {"artifact_id": "vision_module_binding", "artifact_name": "Vision Module Governance Binding", "target_layer": "L2", "phase_ref": "Phase-Vision-Module-Model-Profile-Governance-Binding"},
    {"artifact_id": "ocr_module_binding", "artifact_name": "OCR Module Governance Binding", "target_layer": "L2", "phase_ref": "Phase-OCR-Module-Model-Profile-Governance-Binding"},
    {"artifact_id": "asr_module_binding", "artifact_name": "ASR Module Governance Binding", "target_layer": "L2", "phase_ref": "Phase-ASR-Module-Model-Profile-Governance-Binding"},
    {"artifact_id": "tts_module_binding", "artifact_name": "TTS Module Governance Binding", "target_layer": "L2", "phase_ref": "Phase-TTS-Module-Model-Profile-Governance-Binding"},
    {"artifact_id": "map_navigation_binding", "artifact_name": "Map/Navigation Module Governance Binding", "target_layer": "L2", "phase_ref": "Phase-Map-Navigation-Module-Model-Profile-Governance-Binding"},
    {"artifact_id": "world_continuity_binding", "artifact_name": "World Continuity / STCM Binding", "target_layer": "L4", "phase_ref": "Phase-World-Continuity-Module-Model-Profile-Governance-Binding"},
    {"artifact_id": "information_integration_layer", "artifact_name": "Information Integration Layer", "target_layer": "L6", "phase_ref": "Phase-Midplatform-Information-Integration-Layer"},
    {"artifact_id": "cognitive_zoning_architecture", "artifact_name": "Cognitive Zoning Architecture", "target_layer": "L2-L7 cross-layer mapping", "phase_ref": "Phase-Midplatform-Cognitive-Zoning-Architecture"},
    {"artifact_id": "seed_core_drive_contract", "artifact_name": "Seed Core Drive Signal Contract", "target_layer": "L5", "phase_ref": "Phase-Seed-Core-Drive-Signal-Contract"},
    {"artifact_id": "decision_center", "artifact_name": "Decision Center", "target_layer": "L7", "phase_ref": "Phase-Midplatform-Decision-Center"},
    {"artifact_id": "task_chain", "artifact_name": "Task Chain / Task Response Candidate", "target_layer": "L5", "secondary_layer": "L7", "phase_ref": "Phase-Midplatform-Task-Response-Candidate-Integration"},
    {"artifact_id": "speech_gate", "artifact_name": "Speech Gate", "target_layer": "L7", "phase_ref": "Phase-Midplatform-Speech-Gate"},
    {"artifact_id": "display_gate", "artifact_name": "Display Gate", "target_layer": "L7", "phase_ref": "Phase-Midplatform-Display-Gate"},
    {"artifact_id": "output_plane", "artifact_name": "Output Plane / User Output Constitution", "target_layer": "L7", "phase_ref": "Phase-Midplatform-User-Output-Constitution"},
    {"artifact_id": "memory_admission_bridge", "artifact_name": "Memory Admission Bridge", "target_layer": "L7", "phase_ref": "Phase-Memory-Admission-Bridge-Planning"},
    {"artifact_id": "worldmodel_admission_bridge", "artifact_name": "WorldModel Admission Bridge", "target_layer": "L7", "phase_ref": "Phase-WorldModel-Admission-Bridge-Planning"},
    {"artifact_id": "health_enforcement_supervisor", "artifact_name": "Health Enforcement Supervisor", "target_layer": "L8", "phase_ref": "Phase-Health-Enforcement-Supervisor"},
    {"artifact_id": "recovery_supervisor", "artifact_name": "Recovery Supervisor / Recovery Flow", "target_layer": "L8", "phase_ref": "Phase-Health-Management-Layer-Integration"},
)

INFORMATION_LIFECYCLE_STAGES: Tuple[str, ...] = (
    "raw_output",
    "standardized_candidate",
    "event",
    "working_memory_entry",
    "spatiotemporal_slot_binding",
    "relevance_priority_tagging",
    "integration_result",
    "allocation_result",
    "downstream_candidate",
    "expired",
    "confirmed",
    "deposit_candidate",
    "discarded",
)

COMPONENT_RESPONSIBILITIES: Tuple[Dict[str, Any], ...] = (
    {"component_id": "midplatform_kernel", "primary_layer": "L3", "role": "Orchestrate bus, working memory, and layer handoffs"},
    {"component_id": "event_bus", "primary_layer": "L3", "role": "Event routing and subscription"},
    {"component_id": "working_memory", "primary_layer": "L3", "role": "Short-lived candidate cache; not Memory/WorldModel"},
    {"component_id": "scheduler", "primary_layer": "L5", "role": "Priority-aware scheduling without decision bypass"},
    {"component_id": "task_manager", "primary_layer": "L5", "role": "Task chain state and resume placeholder"},
    {"component_id": "drive_manager", "primary_layer": "L5", "role": "Drive signal candidate generation"},
    {"component_id": "module_adapter_layer", "primary_layer": "L2", "role": "Module output normalization"},
    {"component_id": "health_resource_manager", "primary_layer": "L1", "secondary_layer": "L8", "role": "Resource and health substrate signals"},
    {"component_id": "governance_gate_manager", "primary_layer": "L0", "role": "Gate and boundary enforcement coordination"},
    {"component_id": "worldmodel_memory_bridge", "primary_layer": "L7", "role": "Admission candidate generation only"},
    {"component_id": "output_gate_bridge", "primary_layer": "L7", "role": "Speech/Display/Output plane handoff"},
    {"component_id": "watchdog_recovery_manager", "primary_layer": "L8", "role": "Watchdog, degraded modes, recovery flows"},
)

MODEL_PLACEMENTS: Tuple[str, ...] = (
    "L5 user goal/intent parsing",
    "L6 complex information integration",
    "L6 conflict/gap semantic explanation",
    "L6 task world slice",
    "L7 output candidate expression",
)

RULE_PLACEMENTS: Tuple[str, ...] = (
    "L0 Constitution/Gate/permission/candidate-fact/Memory-WorldModel admission/runtime-output permission",
    "L0 P0/P1 preemption policy hooks",
    "L8 health missing handling and degraded mode rules",
)

ALGORITHM_PLACEMENTS: Tuple[str, ...] = (
    "L3 queue/TTL/cache",
    "L4 spatiotemporal binding/change detection",
    "L6 relevance scoring/confidence fusion/conflict detection",
    "L8 health metrics/recovery trigger",
)

PRIORITY_LEVELS: Tuple[Dict[str, Any], ...] = (
    {"priority": "P0", "name": "Safety / Survival / System Fault", "policy": "preempt_all"},
    {"priority": "P1", "name": "Active User Task Critical Path", "policy": "suspend_review_on_fault"},
    {"priority": "P2", "name": "User Conversation / Current Instruction", "policy": "normal_scheduling"},
    {"priority": "P3", "name": "Scene Continuity / World State Maintenance", "policy": "delay_under_load"},
    {"priority": "P4", "name": "Memory / WorldModel Candidate", "policy": "delay_under_load"},
    {"priority": "P5", "name": "Background Low-Value Information", "policy": "discard_first"},
)

HEALTH_METRICS: Tuple[str, ...] = (
    "midplatform_alive",
    "event_loop_active",
    "core_bus_operational",
    "queue_processing_active",
    "latency",
    "pending_candidate_count",
    "stale_candidate_count",
    "health_tag_missing_count",
    "schema_invalid_count",
    "ttl_violation_count",
    "conflict_unresolved_count",
    "gap_unresolved_count",
    "fallback_trigger_count",
    "degraded_mode_active",
    "last_checkpoint_time",
)

REQUIRED_FAILURE_MODES: Tuple[str, ...] = (
    "response_timeout",
    "long_pending_candidate",
    "health_tag_missing",
    "queue_backlog",
    "schema_invalid_output",
    "spatiotemporal_stale_state",
    "conflict_unresolved",
    "task_chain_stuck",
    "module_unhealthy",
    "provider_unavailable",
    "resource_overload",
    "recovery_failed",
)

OPERATING_MODES: Tuple[str, ...] = (
    "Normal Mode",
    "Degraded Mode",
    "Safety-Only Mode",
    "Hold Mode",
    "Recovery Mode",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Micro-OS planning ≠ real operating system",
    "Micro-OS planning ≠ runtime enabled",
    "Micro-OS planning ≠ multi-threading implemented",
    "Micro-OS planning ≠ model selected or invoked",
    "Micro-OS planning ≠ Memory / WorldModel write allowed",
    "Micro-OS planning ≠ Decision Center fully implemented",
    "Micro-OS planning ≠ Output to user allowed",
    "Micro-OS planning ≠ Health monitoring runtime active",
    "Micro-OS planning ≠ full Luna OS productization",
    "Midplatform 1.0 Micro-OS planning ≠ device-level OS implementation",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("midplatform_micro_os_architecture_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "model_invoked_now",
    "model_download_now",
    "provider_invoked_now",
    "multi_threading_executed_now",
    "memory_written_now",
    "world_model_written_now",
    "user_output_generated_now",
    "real_task_chain_executed_now",
    "module_runtime_behavior_modified_now",
    "prior_phase_go_conclusions_changed_now",
    "planning_treated_as_implementation_now",
)

DEFAULT_OUTPUT_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_architecture_planning"


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "four_layer_architecture_legacy_ref": FOUR_LAYER_ARCHITECTURE,
        "midplatform_1_0_name": MIDPLATFORM_1_0_NAME,
        "midplatform_1_0_form": MIDPLATFORM_1_0_FORM,
        "midplatform_1_0_label_zh": MIDPLATFORM_1_0_LABEL_ZH,
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


def _layer_entry(defn: Dict[str, Any]) -> Dict[str, Any]:
    return {k: defn.get(k) for k in LAYER_COMMON_FIELDS if k in defn} | {
        "layer_id": defn["layer_id"],
        "layer_name": defn["layer_name"],
        "layer_role": defn["layer_role"],
        "global_constraint_role": defn["global_constraint_role"],
        "upstream_inputs": list(defn["upstream_inputs"]),
        "downstream_outputs": list(defn["downstream_outputs"]),
        "forbidden_actions": list(defn["forbidden_actions"]),
        "placed_artifacts": list(defn.get("placed_artifacts") or []),
    }


def run_midplatform_micro_os_architecture_planning_v1(
    *,
    output_root: Optional[str] = None,
    upstream_inventory_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    inv_root = Path(upstream_inventory_root or out_root.parent).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root), "upstream_inventory_root": str(inv_root)}

    layers = [_layer_entry(d) for d in MICRO_OS_LAYER_DEFINITIONS]
    if len(layers) != 9:
        blockers.append("must define exactly 9 layers L0-L8")
    l0 = next((x for x in layers if x["layer_id"] == "L0"), None)
    l8 = next((x for x in layers if x["layer_id"] == "L8"), None)
    if not l0 or l0.get("global_constraint_role") != "constitution_kernel":
        blockers.append("L0 must be constitution/governance kernel")
    if not l8 or l8.get("global_constraint_role") != "health_supervisor_bypass":
        blockers.append("L8 must be health/watchdog/recovery supervisor bypass")

    micro_os_definition = {
        "definition_id": "midplatform_micro_os_definition_v1",
        "midplatform_1_0": MIDPLATFORM_1_0_NAME,
        "midplatform_1_0_form": MIDPLATFORM_1_0_FORM,
        "midplatform_1_0_label_zh": MIDPLATFORM_1_0_LABEL_ZH,
        "core_positioning": (
            "Luna Midplatform 1.0 is Luna's midplatform micro-operating-system: an OS-like "
            "architecture planning kernel that eventizes, anchors, schedules, integrates, "
            "and hands off candidates under Constitution and Health supervision."
        ),
        "responsibilities": [
            "eventize module and system information",
            "anchor spatiotemporal world state candidates",
            "maintain working memory and queues",
            "schedule drives/tasks under governance",
            "integrate and allocate information",
            "hand off to Decision/Output/Memory-WorldModel bridges",
        ],
        "non_responsibilities": [
            "device-level OS implementation",
            "direct Memory/WorldModel writes",
            "direct user output",
            "direct provider/model runtime in this planning phase",
            "full Luna OS productization",
        ],
        "relationship_to_luna_os": "Micro-OS is the midplatform runtime kernel architecture; not the full Luna OS product shell.",
        **meta,
    }

    layer_architecture = {
        "architecture_id": "midplatform_micro_os_layer_architecture_v1",
        "layer_count": len(layers),
        "layers": layers,
        "l0_global_governance_constraint": True,
        "l8_global_supervisory_bypass": True,
        "l1_resource_substrate_for_l2_l7": True,
        "worldmodel_memory_bidirectional_note": (
            "L7 emits admission candidates; WorldModel/Memory recall enters L4/L5/L6 as context only."
        ),
        **meta,
    }

    relocation_matrix = {
        "matrix_id": "midplatform_existing_governance_relocation_matrix_v1",
        "entries": list(GOVERNANCE_RELOCATION_ENTRIES),
        "entry_count": len(GOVERNANCE_RELOCATION_ENTRIES),
        "covers_constitution_governance_validation_whitebox": True,
        "covers_health_module_binding_model_profile_output_task_worldmodel_memory": True,
        "prior_phase_go_conclusions_unchanged": True,
        **meta,
    }

    upstream_downstream = {
        "matrix_id": "midplatform_upstream_downstream_matrix_v1",
        "flow_summary": [
            "L0 constrains all layers",
            "L1 feeds resource/degraded signals to L2-L7",
            "L2 -> L3 -> L4 -> L5 -> L6 -> L7",
            "L8 monitors L1-L7 and can trigger degraded/hold/recovery",
            "WorldModel/Memory recall enters L4/L5/L6; admission exits L7",
        ],
        "layer_edges": [
            {"from": "L0", "to": "L1-L7", "relation": "global_governance_constraint"},
            {"from": "L1", "to": "L2-L7", "relation": "resource_substrate"},
            {"from": "L2", "to": "L3", "relation": "standardized_candidate/event"},
            {"from": "L3", "to": "L4", "relation": "working_memory_entry"},
            {"from": "L4", "to": "L5-L6", "relation": "spatiotemporal_world_state"},
            {"from": "L5", "to": "L6", "relation": "drive_task_context"},
            {"from": "L6", "to": "L7", "relation": "integration_allocation_handoff"},
            {"from": "L8", "to": "L1-L7", "relation": "health_watchdog_recovery_supervision"},
            {"from": "WorldModel/Memory", "to": "L4/L5/L6", "relation": "recall_context_only"},
            {"from": "L7", "to": "WorldModel/Memory", "relation": "admission_candidate_only"},
        ],
        **meta,
    }

    information_lifecycle = {
        "lifecycle_id": "midplatform_information_lifecycle_v1",
        "stages": list(INFORMATION_LIFECYCLE_STAGES),
        "stage_count": len(INFORMATION_LIFECYCLE_STAGES),
        "terminal_states": ["expired", "confirmed", "deposit_candidate", "discarded"],
        **meta,
    }

    component_map = {
        "map_id": "midplatform_component_responsibility_map_v1",
        "components": list(COMPONENT_RESPONSIBILITIES),
        "component_count": len(COMPONENT_RESPONSIBILITIES),
        **meta,
    }

    placement_matrix = {
        "matrix_id": "midplatform_model_rule_algorithm_placement_matrix_v1",
        "model_placements": list(MODEL_PLACEMENTS),
        "rule_placements": list(RULE_PLACEMENTS),
        "algorithm_placements": list(ALGORITHM_PLACEMENTS),
        "all_model_outputs_are_candidates": True,
        "all_model_outputs_require_schema_validation_and_governance_gate": True,
        **meta,
    }

    priority_policy = {
        "policy_id": "midplatform_priority_and_scheduling_policy_v1",
        "priorities": list(PRIORITY_LEVELS),
        "p0_preempt": True,
        "p5_discard": True,
        "p3_p4_delay": True,
        "p1_suspend_review_on_fault": True,
        **meta,
    }

    working_memory_policy = {
        "policy_id": "midplatform_working_memory_policy_v1",
        "working_memory_is_not_memory": True,
        "working_memory_is_not_worldmodel": True,
        "contents": [
            "pending_candidate",
            "conflict_candidate",
            "gap_candidate",
            "task_state_snapshot",
            "recent_world_state_candidate",
            "priority_queue_items",
            "ttl_cache_entries",
        ],
        "states": ["active", "stale", "expired", "compressed", "deposit_candidate", "discarded"],
        "ttl_required": True,
        "cleanup_rules": ["expire_by_ttl", "drop_p5_first", "compress_low_relevance", "deposit_candidate_requires_admission_path"],
        **meta,
    }

    health_scope = {
        "scope_id": "midplatform_health_metric_scope_v1",
        "metrics": list(HEALTH_METRICS),
        "metric_count": len(HEALTH_METRICS),
        "covers_midplatform_self_health": True,
        **meta,
    }

    failure_matrix = {
        "matrix_id": "midplatform_failure_mode_matrix_v1",
        "failure_modes": [
            {"mode_id": mode, "requires_traceable_response": True}
            for mode in REQUIRED_FAILURE_MODES
        ],
        "failure_mode_count": len(REQUIRED_FAILURE_MODES),
        **meta,
    }

    degraded_recovery = {
        "policy_id": "midplatform_degraded_and_recovery_mode_policy_v1",
        "modes": [
            {
                "mode": mode,
                "trigger_examples": _mode_triggers(mode),
                "allowed_paths": _mode_allowed(mode),
                "forbidden_paths": _mode_forbidden(mode),
                "recovery_condition": _mode_recovery(mode),
            }
            for mode in OPERATING_MODES
        ],
        **meta,
    }

    wm_memory_boundary = {
        "boundary_id": "midplatform_worldmodel_memory_feedback_boundary_v1",
        "midplatform_to_worldmodel_memory": {
            "allowed": ["admission_candidate"],
            "forbidden": ["direct_write", "direct_fact_commit"],
        },
        "worldmodel_memory_to_midplatform": {
            "allowed": [
                "recall_context",
                "hint",
                "known_state_candidate",
                "change_detection_reference",
            ],
            "forbidden": ["override_realtime_safety", "replace_current_observation"],
        },
        "deposited_info_must_not_override_realtime_safety": True,
        **meta,
    }

    local_cloud_boundary = {
        "boundary_id": "midplatform_local_cloud_model_routing_boundary_v1",
        "local_light_model_tasks": [
            "short_text_intent",
            "simple_routing",
            "low_value_filter",
            "simple_gap_conflict_prefilter",
        ],
        "cloud_complex_model_tasks": [
            "complex_dialogue",
            "long_context",
            "multi_turn_task_planning",
            "complex_conflict_explanation",
            "long_term_summary",
        ],
        "all_outputs_are_candidates": True,
        "requires_schema_validation_and_governance_gate": True,
        **meta,
    }

    non_claims = {
        "register_id": "midplatform_non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "midplatform_micro_os_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "verify L0-L8 layer completeness and boundaries",
            "verify governance relocation matrix coverage",
            "verify information lifecycle and component map",
            "verify model/rule/algorithm placement",
            "verify health/failure/degraded-recovery policies",
            "verify WorldModel/Memory bidirectional boundary",
            "no runtime enabled",
            "no model invocation",
        ],
        **meta,
    }

    planning_pass = len(blockers) == 0 and len(layers) == 9
    planning_decision = {
        "decision_id": "midplatform_micro_os_architecture_planning_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "architecture_summary": [
            f"{MIDPLATFORM_1_0_NAME} = {MIDPLATFORM_1_0_FORM}",
            "9-layer Micro-OS architecture L0-L8",
            "Constitution/Governance/Health/Module/Model/Output/Task/WorldModel-Memory relocated",
            "Planning only; no runtime/model/memory/output execution",
        ],
        **meta,
    }

    policy = {
        "policy_id": "midplatform_micro_os_architecture_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "layer_count": 9,
        "core_objects_count": 15,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "midplatform_1_0_form": MIDPLATFORM_1_0_FORM,
        "layer_count": len(layers),
        "relocation_entry_count": len(GOVERNANCE_RELOCATION_ENTRIES),
        "planning_pass": planning_pass,
        "violations": blockers,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "summary": summary,
        "midplatform_micro_os_architecture_planning_policy": policy,
        "midplatform_micro_os_definition": micro_os_definition,
        "midplatform_micro_os_layer_architecture": layer_architecture,
        "midplatform_existing_governance_relocation_matrix": relocation_matrix,
        "midplatform_upstream_downstream_matrix": upstream_downstream,
        "midplatform_information_lifecycle": information_lifecycle,
        "midplatform_component_responsibility_map": component_map,
        "midplatform_model_rule_algorithm_placement_matrix": placement_matrix,
        "midplatform_priority_and_scheduling_policy": priority_policy,
        "midplatform_working_memory_policy": working_memory_policy,
        "midplatform_health_metric_scope": health_scope,
        "midplatform_failure_mode_matrix": failure_matrix,
        "midplatform_degraded_and_recovery_mode_policy": degraded_recovery,
        "midplatform_worldmodel_memory_feedback_boundary": wm_memory_boundary,
        "midplatform_local_cloud_model_routing_boundary": local_cloud_boundary,
        "midplatform_non_claims_register": non_claims,
        "midplatform_micro_os_dryrun_plan": dryrun_plan,
        "midplatform_micro_os_architecture_planning_decision": planning_decision,
    }


def _mode_triggers(mode: str) -> List[str]:
    mapping = {
        "Normal Mode": ["all health metrics within threshold"],
        "Degraded Mode": ["provider_unavailable", "resource_overload", "queue_backlog"],
        "Safety-Only Mode": ["P0 fault", "schema_invalid_output", "health_tag_missing burst"],
        "Hold Mode": ["conflict_unresolved", "long_pending_candidate", "task_chain_stuck"],
        "Recovery Mode": ["watchdog_timeout", "recovery_flow_started"],
    }
    return mapping.get(mode, [])


def _mode_allowed(mode: str) -> List[str]:
    mapping = {
        "Normal Mode": ["L2-L7 candidate flow", "scheduled integration", "handoff to L7"],
        "Degraded Mode": ["local fallback paths", "reduced P3-P5 intake", "L8 supervised continuation"],
        "Safety-Only Mode": ["P0 paths", "health/safety observations", "hold non-critical output"],
        "Hold Mode": ["inspect/conflict review", "queue drain under L8 supervision"],
        "Recovery Mode": ["checkpoint restore", "queue cleanup", "supervised restart flow"],
    }
    return mapping.get(mode, [])


def _mode_forbidden(mode: str) -> List[str]:
    mapping = {
        "Normal Mode": [],
        "Degraded Mode": ["silent full-capability pretense", "un gated cloud escalation"],
        "Safety-Only Mode": ["P5 background intake", "unreviewed user output", "Memory/WorldModel write"],
        "Hold Mode": ["new P1 task start without review", "direct runtime execution"],
        "Recovery Mode": ["immediate full traffic restore without health clearance"],
    }
    return mapping.get(mode, [])


def _mode_recovery(mode: str) -> str:
    mapping = {
        "Normal Mode": "n/a",
        "Degraded Mode": "resource/provider health restored and L8 clearance",
        "Safety-Only Mode": "P0 cleared and validation/health tags restored",
        "Hold Mode": "conflict/gap resolved or expired with trace",
        "Recovery Mode": "recovery flow success + checkpoint valid + L8 clearance",
    }
    return mapping.get(mode, "supervised L8 clearance required")
