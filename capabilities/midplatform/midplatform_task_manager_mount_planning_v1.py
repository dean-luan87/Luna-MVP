# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Mount Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_decision_center_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HEALTH_WATCHDOG_HANDOFF_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_information_integration_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_HANDOFF_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MICRO_OS_FREEZE_DRYRUN_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Mount-Planning-v1-001"
SCOPE = "midplatform_task_manager_mount_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_mount_planning_v1"

UPSTREAM_HEALTH_WATCHDOG_HANDOFF_DRYRUN_FINAL = HEALTH_WATCHDOG_HANDOFF_DRYRUN_FINAL_GO
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_MOUNT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_TASK_MANAGER_MOUNT_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Mount-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Mount-Issue-Review-v1-001"

FOUNDATIONS: Tuple[str, ...] = (
    "midplatform_micro_os_foundation_v1",
    "midplatform_information_integration_foundation_v1",
    "midplatform_decision_center_foundation_v1",
    "midplatform_health_watchdog_foundation_v1",
)

UPSTREAM_GO_CHAIN: Tuple[Dict[str, str], ...] = (
    {
        "phase": "micro_os_foundation_freeze_and_handoff_dryrun_and_review",
        "expected_final": MICRO_OS_FREEZE_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "information_integration_foundation_handoff_dryrun_and_review",
        "expected_final": II_HANDOFF_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "decision_center_foundation_handoff_dryrun_and_review",
        "expected_final": DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
    {
        "phase": "health_watchdog_foundation_handoff_dryrun_and_review",
        "expected_final": HEALTH_WATCHDOG_HANDOFF_DRYRUN_FINAL_GO,
        "pass_field": "dryrun_pass",
    },
)

DECISION_CENTER_INPUTS: Tuple[str, ...] = (
    "decision_candidate_refs",
    "decision_readiness_candidate_refs",
    "downstream_decision_handoff_candidate_refs",
)

HEALTH_WATCHDOG_INPUTS: Tuple[str, ...] = (
    "health_signal_candidate_refs",
    "degradation_candidate_refs",
    "recovery_recommendation_candidate_refs",
    "required_observation_candidate_refs",
    "module_health_review_candidate_refs",
    "watchdog_handoff_candidate_refs",
    "hold_refs",
    "blocked_refs",
    "safety_block_refs",
)

INPUT_TYPES: Tuple[str, ...] = (
    *DECISION_CENTER_INPUTS,
    *HEALTH_WATCHDOG_INPUTS,
    "task_context_refs",
    "trace_ref",
    "health_tag",
    "source_chain",
    "governance_ref_for_high_risk_task_candidate",
)

INPUT_REQUIRED_FIELDS: Tuple[str, ...] = (
    "candidate_not_fact",
    "trace",
    "health_tag",
    "source_chain",
    "governance_ref_for_high_risk_task_candidate",
)

OUTPUT_CANDIDATES: Tuple[str, ...] = (
    "task_candidate",
    "task_readiness_candidate",
    "task_block_candidate",
    "task_plan_candidate",
    "task_step_candidate",
    "task_handoff_candidate",
    "task_pause_candidate",
    "task_resume_candidate_later",
    "task_abort_candidate_later",
    "required_observation_handoff_candidate",
    "output_preparation_candidate_later",
)

FORBIDDEN_OUTPUTS: Tuple[str, ...] = (
    "real_task_execution",
    "tool_call",
    "runtime_command",
    "user_output",
    "fact",
    "memory_write",
    "worldmodel_write",
    "direct_mount",
)

RESPONSIBILITIES: Tuple[str, ...] = (
    "consume decision_candidate / decision_readiness_candidate",
    "consume health gate / hold / blocked / required observation / watchdog handoff candidates",
    "judge task candidate progression readiness",
    "generate task_candidate",
    "generate task_readiness_candidate",
    "generate task_block_candidate",
    "generate task_plan_candidate",
    "generate task_step_candidate",
    "generate task_handoff_candidate",
    "organize task phase / task state",
    "no task execution",
    "no tool call",
    "no user output",
    "no Memory / WorldModel write",
    "no model/provider invocation",
    "no Governance Gate bypass",
    "never treat task_candidate as real task execution result",
)

PROCESSING_STEPS: Tuple[str, ...] = (
    "consume Decision Center / Health Watchdog candidates",
    "validate trace / health_tag / candidate_not_fact / governance",
    "inspect decision readiness",
    "inspect health gate / hold / blocked",
    "inspect required observation",
    "classify task readiness",
    "generate task_candidate or task_block_candidate",
    "generate task_plan_candidate",
    "generate task_step_candidate",
    "generate downstream task handoff candidate",
)

TASK_STATES: Tuple[str, ...] = (
    "received",
    "validating",
    "health_gate_review",
    "governance_review",
    "decision_readiness_review",
    "observation_requirement_review",
    "task_candidate_generated",
    "task_plan_candidate_generated",
    "task_step_candidate_generated",
    "task_handoff_ready",
    "hold",
    "blocked",
    "paused",
    "not_ready",
    "requires_observation",
    "discarded_invalid",
)

MODEL_USES_LATER: Tuple[str, ...] = (
    "task plan explanation",
    "task step summarization",
    "complex task decomposition draft",
)

RULE_USES: Tuple[str, ...] = (
    "no task execution",
    "no tool call",
    "no output",
    "candidate/fact boundary",
    "high-risk task requires governance",
    "health gate blocks task readiness",
    "hold/blocked candidates prevent task progression",
    "output/write/runtime forbidden",
)

ALGORITHM_USES: Tuple[str, ...] = (
    "task readiness scoring",
    "task priority ranking",
    "task step ordering",
    "blocker severity ranking",
    "handoff route ranking",
)

GOVERNANCE_BOUNDARIES: Tuple[str, ...] = (
    "must not bypass L0",
    "high-risk task_candidate requires governance_ref",
    "unresolved health gate must not generate ready task",
    "unresolved decision block must not generate ready task",
    "task_candidate is not task execution",
    "task_step_candidate is not executed step",
    "task_handoff_candidate is not direct mount",
    "output/write/runtime/tool attempts are blocked",
)

HEALTH_WATCHDOG_DEPENDENCY_RULES: Tuple[str, ...] = (
    "only consume midplatform_health_watchdog_foundation_v1 frozen outputs",
    "must not redefine Health Watchdog",
    "must not modify Health Watchdog candidate type",
    "must not treat hold / blocked / safety_block as executed task",
    "must not treat recovery_recommendation_candidate as recovered",
    "must not require Health Watchdog runtime",
    "new fields require change_control",
)

DECISION_CENTER_DEPENDENCY_RULES: Tuple[str, ...] = (
    "only consume midplatform_decision_center_foundation_v1 frozen outputs",
    "must not redefine Decision Center",
    "must not modify DecisionCandidate",
    "must not treat decision_candidate as final action",
    "must not require Decision Center runtime",
    "new fields require change_control",
)

DOWNSTREAM_HANDOFFS: Tuple[Dict[str, Any], ...] = (
    {"target": "module_adapter", "payload": "required_observation_handoff_candidate", "direct_mount": False},
    {
        "target": "output_gate",
        "payload": "output_preparation_candidate only after Output Gate mount and output readiness",
        "direct_mount": False,
    },
    {
        "target": "worldmodel_memory_bridge",
        "payload": "task outcome/admission candidate only after actual execution and admission policy later",
        "direct_mount": False,
    },
    {"target": "decision_center_loopback", "payload": "task readiness/block result candidate", "direct_mount": False},
    {"target": "health_watchdog_loopback", "payload": "health gate / blocked / degraded task candidate", "direct_mount": False},
    {"target": "governance_gate", "payload": "high-risk task / blocked candidate", "direct_mount": False},
)

SAMPLE_FLOWS: Tuple[Dict[str, Any], ...] = (
    {
        "flow_id": "ready_decision_and_healthy_gate_generates_task_candidate",
        "input": ["decision_candidate", "healthy_gate"],
        "processing": ["validate_input", "classify_task_readiness"],
        "output_candidate": "task_candidate",
        "blocked_paths": ["task_execution"],
    },
    {
        "flow_id": "health_hold_blocks_task_candidate",
        "input": ["decision_candidate", "hold_candidate"],
        "processing": ["inspect_health_hold"],
        "output_candidate": "task_block_candidate",
        "blocked_paths": ["ready_task_candidate", "task_execution"],
    },
    {
        "flow_id": "required_observation_routes_to_module_adapter_candidate",
        "input": ["required_observation_candidate"],
        "processing": ["route_observation"],
        "output_candidate": "required_observation_handoff_candidate",
        "blocked_paths": ["direct_module_adapter_mount"],
    },
    {
        "flow_id": "high_risk_task_missing_governance_blocks",
        "input": ["high_risk_task_context", "missing_governance_ref"],
        "processing": ["governance_review"],
        "output_candidate": "task_block_candidate",
        "blocked_paths": ["task_candidate_ready"],
    },
    {
        "flow_id": "recovery_recommendation_not_treated_as_recovered",
        "input": ["recovery_recommendation_candidate"],
        "processing": ["recovery_boundary_review"],
        "output_candidate": "task_block_candidate",
        "blocked_paths": ["treat_recovered", "task_execution"],
    },
    {
        "flow_id": "task_candidate_does_not_execute_task",
        "input": ["ready_task_candidate"],
        "processing": ["candidate_output_only"],
        "output_candidate": "task_candidate",
        "blocked_paths": ["task_execution", "tool_call"],
    },
    {
        "flow_id": "output_preparation_does_not_output_user_result",
        "input": ["task_handoff_candidate"],
        "processing": ["output_preparation_candidate_later"],
        "output_candidate": "output_preparation_candidate_later",
        "blocked_paths": ["user_output", "output_gate_direct_mount"],
    },
)

FAILURE_ROUTES: Tuple[Dict[str, str], ...] = (
    {
        "route_id": "missing_decision_candidate",
        "detection_signal": "decision_candidate_refs empty",
        "impact": "cannot generate task candidate",
        "default_response": "not_ready",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "invent decision candidate",
    },
    {
        "route_id": "missing_health_gate",
        "detection_signal": "health gate missing",
        "impact": "task readiness unknown",
        "default_response": "hold",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "assume healthy",
    },
    {
        "route_id": "missing_trace",
        "detection_signal": "trace_ref missing",
        "impact": "untraceable task candidate",
        "default_response": "discarded_invalid",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "create synthetic trace as fact",
    },
    {
        "route_id": "missing_source_chain",
        "detection_signal": "source_chain missing",
        "impact": "lineage unclear",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "skip lineage",
    },
    {
        "route_id": "missing_governance_for_high_risk_task",
        "detection_signal": "high_risk without governance_ref",
        "impact": "governance pending",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "bypass L0",
    },
    {
        "route_id": "health_hold_active",
        "detection_signal": "hold refs present",
        "impact": "task progression blocked",
        "default_response": "hold",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "ignore hold",
    },
    {
        "route_id": "safety_block_active",
        "detection_signal": "safety_block refs present",
        "impact": "safety block",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "downgrade P0 safety",
    },
    {
        "route_id": "required_observation_unresolved",
        "detection_signal": "required_observation refs present",
        "impact": "observation needed",
        "default_response": "requires_observation",
        "hold_or_block_candidate": "required_observation_handoff_candidate",
        "forbidden_shortcut": "proceed without observation",
    },
    {
        "route_id": "recovery_recommendation_misused_as_recovered",
        "detection_signal": "recovery recommendation treated as recovered",
        "impact": "false recovery state",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "mark recovered",
    },
    {
        "route_id": "task_execution_attempted",
        "detection_signal": "task execution requested",
        "impact": "runtime boundary violation",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "execute task",
    },
    {
        "route_id": "tool_call_attempted",
        "detection_signal": "tool call requested",
        "impact": "tool boundary violation",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "call tool",
    },
    {
        "route_id": "output_attempted",
        "detection_signal": "user output requested",
        "impact": "output boundary violation",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "emit output",
    },
    {
        "route_id": "memory_write_attempted",
        "detection_signal": "memory write requested",
        "impact": "memory boundary violation",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "write memory",
    },
    {
        "route_id": "worldmodel_write_attempted",
        "detection_signal": "worldmodel write requested",
        "impact": "worldmodel boundary violation",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "write worldmodel",
    },
    {
        "route_id": "model_invocation_attempted_now",
        "detection_signal": "model invocation requested",
        "impact": "model boundary violation",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "invoke model",
    },
    {
        "route_id": "provider_invocation_attempted_now",
        "detection_signal": "provider invocation requested",
        "impact": "provider boundary violation",
        "default_response": "blocked",
        "hold_or_block_candidate": "task_block_candidate",
        "forbidden_shortcut": "invoke provider",
    },
)

HEALTH_METRICS: Tuple[str, ...] = (
    "task_candidate_input_count",
    "task_candidate_generated_count",
    "task_readiness_candidate_count",
    "task_block_candidate_count",
    "task_plan_candidate_count",
    "task_step_candidate_count",
    "task_handoff_candidate_count",
    "health_gate_block_count",
    "safety_block_count",
    "required_observation_count",
    "governance_pending_count",
    "task_execution_attempt_block_count",
    "tool_call_attempt_block_count",
    "output_attempt_block_count",
    "write_attempt_block_count",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "task_manager_mounted_now",
    "task_manager_runtime_enabled_now",
    "task_execution_now",
    "tool_call_now",
    "model_invoked_now",
    "provider_invoked_now",
    "runtime_enabled_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "module_adapter_mounted_now",
    "health_watchdog_runtime_enabled_now",
    "decision_center_runtime_enabled_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Mount Planning ≠ Task Manager implemented",
    "Mount Planning ≠ mounted now",
    "Mount Planning ≠ runtime enabled",
    "Mount Planning ≠ task execution",
    "Mount Planning ≠ tool call",
    "Mount Planning ≠ Output Gate ready",
    "Mount Planning ≠ user output",
    "Mount Planning ≠ Memory / WorldModel write",
    "Mount Planning ≠ full task pipeline",
)

DEFAULT_HEALTH_WATCHDOG_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_foundation_handoff_dryrun_and_review"
)
DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_II_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_MICRO_OS_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_task_manager_mount_planning"


def _meta(output_root: Path, hw_root: Path, dc_root: Path, ii_root: Path, micro_root: Path) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "module_id": "task_manager",
        "layer": "L6_task_candidate_management",
        "depends_on": "midplatform_health_watchdog_foundation_v1",
        "also_depends_on": [
            "midplatform_decision_center_foundation_v1",
            "midplatform_information_integration_foundation_v1",
            "midplatform_micro_os_foundation_v1",
        ],
        "foundations": list(FOUNDATIONS),
        "runtime_status": "not_enabled",
        "mount_planning_only": True,
        "output_root": str(output_root),
        "upstream_health_watchdog_handoff_dryrun_root": str(hw_root),
        "upstream_decision_center_handoff_dryrun_root": str(dc_root),
        "upstream_information_integration_handoff_dryrun_root": str(ii_root),
        "upstream_micro_os_freeze_dryrun_root": str(micro_root),
    }
    for flag in BOUNDARY_FALSE:
        meta[flag] = False
    return meta


def _try_read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _upstream_go(root: Path, expected_final: str) -> bool:
    summary = _try_read_json(root / "summary.json")
    verifier = _try_read_json(root / "verifier_report.json")
    return summary.get("final_decision") == expected_final and verifier.get("verifier") == "GO"


def run_midplatform_task_manager_mount_planning_v1(
    *,
    health_watchdog_handoff_dryrun_root: str,
    decision_center_handoff_dryrun_root: str,
    information_integration_handoff_dryrun_root: str,
    micro_os_freeze_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    hw_root = Path(health_watchdog_handoff_dryrun_root).expanduser().resolve()
    dc_root = Path(decision_center_handoff_dryrun_root).expanduser().resolve()
    ii_root = Path(information_integration_handoff_dryrun_root).expanduser().resolve()
    micro_root = Path(micro_os_freeze_dryrun_root).expanduser().resolve()
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = _meta(out, hw_root, dc_root, ii_root, micro_root)
    issues: List[str] = []

    upstream_roots = {
        "micro_os_foundation_freeze_and_handoff_dryrun_and_review": micro_root,
        "information_integration_foundation_handoff_dryrun_and_review": ii_root,
        "decision_center_foundation_handoff_dryrun_and_review": dc_root,
        "health_watchdog_foundation_handoff_dryrun_and_review": hw_root,
    }
    upstream_entries = []
    for chain in UPSTREAM_GO_CHAIN:
        root = upstream_roots[chain["phase"]]
        summary = _try_read_json(root / "summary.json")
        verifier = _try_read_json(root / "verifier_report.json")
        go = summary.get("final_decision") == chain["expected_final"] and verifier.get("verifier") == "GO"
        upstream_entries.append(
            {
                "phase": chain["phase"],
                "root": str(root),
                "expected_final": chain["expected_final"],
                "actual_final": summary.get("final_decision"),
                "verifier": verifier.get("verifier"),
                "go": go,
            }
        )
        if not go:
            issues.append(f"upstream_not_go:{chain['phase']}")

    hw_summary = _try_read_json(hw_root / "summary.json")
    dc_summary = _try_read_json(dc_root / "summary.json")
    ii_summary = _try_read_json(ii_root / "summary.json")
    micro_summary = _try_read_json(micro_root / "summary.json")
    if hw_summary.get("foundation_id") != "midplatform_health_watchdog_foundation_v1":
        issues.append("health_watchdog_foundation_id_mismatch")
    if hw_summary.get("runtime_status") != "not_enabled":
        issues.append("health_watchdog_runtime_status_not_enabled_mismatch")
    if dc_summary.get("foundation_id") != "midplatform_decision_center_foundation_v1":
        issues.append("decision_center_foundation_id_mismatch")
    if ii_summary.get("foundation_id") != "midplatform_information_integration_foundation_v1":
        issues.append("information_integration_foundation_id_mismatch")
    if micro_summary.get("foundation_id") != "midplatform_micro_os_foundation_v1":
        issues.append("micro_os_foundation_id_mismatch")

    mount_scope = {
        "object_id": "task_manager_mount_scope_v1",
        "module_id": "task_manager",
        "layer": "L6_task_candidate_management",
        "definition": (
            "Task Manager is Luna Midplatform Micro-OS task candidate management layer; "
            "it organizes task-level candidates and never executes real tasks."
        ),
        "allowed_upstream_foundations": [
            "midplatform_decision_center_foundation_v1",
            "midplatform_health_watchdog_foundation_v1",
        ],
        "decision_center_outputs_consumed": list(DECISION_CENTER_INPUTS),
        "health_watchdog_outputs_consumed": list(HEALTH_WATCHDOG_INPUTS),
        "allowed_outputs": list(OUTPUT_CANDIDATES),
        "responsibilities": list(RESPONSIBILITIES),
        "forbidden": [
            "real_task_execution",
            "tool_call",
            "model_provider_invocation",
            "memory_worldmodel_write",
            "user_output",
            "direct_mount",
        ],
        **meta,
    }
    mount_contract = {
        "object_id": "task_manager_mount_contract_v1",
        "sections": {
            section: {
                "section": section,
                "candidate_only": True,
                "runtime_enabled": False,
            }
            for section in TEMPLATE_SECTIONS
        },
        "template_sections": list(TEMPLATE_SECTIONS),
        "module_identity": {"module_id": "task_manager", "layer": "L6_task_candidate_management"},
        "upstream_sources": list(FOUNDATIONS),
        "downstream_targets": [h["target"] for h in DOWNSTREAM_HANDOFFS],
        "checks": [{"check_id": f"contract.section.{section}", "passed": True} for section in TEMPLATE_SECTIONS],
        **meta,
    }
    input_contract = {
        "object_id": "task_manager_input_contract_v1",
        "inputs": list(INPUT_TYPES),
        "required_fields": list(INPUT_REQUIRED_FIELDS),
        "decision_center_inputs": list(DECISION_CENTER_INPUTS),
        "health_watchdog_inputs": list(HEALTH_WATCHDOG_INPUTS),
        "candidate_not_fact_required": True,
        "trace_required": True,
        "health_tag_required": True,
        "source_chain_required": True,
        "governance_ref_required_for_high_risk_task_candidate": True,
        **meta,
    }
    output_contract = {
        "object_id": "task_manager_output_contract_v1",
        "outputs": list(OUTPUT_CANDIDATES),
        "forbidden_outputs": list(FORBIDDEN_OUTPUTS),
        "all_outputs_candidate_only": True,
        "task_candidate_is_not_task_execution": True,
        "task_step_candidate_is_not_executed_step": True,
        "task_handoff_candidate_is_not_direct_mount": True,
        **meta,
    }
    processing_model = {
        "object_id": "task_manager_processing_model_v1",
        "steps": list(PROCESSING_STEPS),
        "planning_only": True,
        "task_runtime_executed": False,
        **meta,
    }
    task_state_machine = {
        "object_id": "task_manager_task_state_machine_v1",
        "states": list(TASK_STATES),
        "state_count": len(TASK_STATES),
        "all_states_candidate_level": True,
        **meta,
    }
    model_rule_algorithm = {
        "object_id": "task_manager_model_rule_algorithm_placement_v1",
        "model_uses_later": list(MODEL_USES_LATER),
        "model_invoked_now": False,
        "rules": list(RULE_USES),
        "algorithms": list(ALGORITHM_USES),
        **{k: v for k, v in meta.items() if k != "model_invoked_now"},
    }
    governance_boundary = {
        "object_id": "task_manager_governance_boundary_v1",
        "rules": list(GOVERNANCE_BOUNDARIES),
        "rule_count": len(GOVERNANCE_BOUNDARIES),
        **meta,
    }
    hw_dependency_boundary = {
        "object_id": "task_manager_health_watchdog_dependency_boundary_v1",
        "rules": list(HEALTH_WATCHDOG_DEPENDENCY_RULES),
        "foundation_id": "midplatform_health_watchdog_foundation_v1",
        "must_not_redefine_health_watchdog": True,
        **meta,
    }
    dc_dependency_boundary = {
        "object_id": "task_manager_decision_center_dependency_boundary_v1",
        "rules": list(DECISION_CENTER_DEPENDENCY_RULES),
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "must_not_redefine_decision_center": True,
        **meta,
    }
    downstream_handoff_matrix = {
        "object_id": "task_manager_downstream_handoff_matrix_v1",
        "handoffs": list(DOWNSTREAM_HANDOFFS),
        "direct_mount": False,
        **meta,
    }
    sample_flow_plan = {
        "object_id": "task_manager_sample_flow_plan_v1",
        "samples": list(SAMPLE_FLOWS),
        "sample_count": len(SAMPLE_FLOWS),
        **meta,
    }
    failure_route_matrix = {
        "object_id": "task_manager_failure_route_matrix_v1",
        "routes": list(FAILURE_ROUTES),
        "route_count": len(FAILURE_ROUTES),
        **meta,
    }
    health_metric_scope = {
        "object_id": "task_manager_mount_health_metric_scope_v1",
        "metrics": list(HEALTH_METRICS),
        "metric_count": len(HEALTH_METRICS),
        "real_health_runtime_enabled": False,
        **meta,
    }
    boundary_matrix = {
        "object_id": "task_manager_boundary_matrix_v1",
        "global_boundaries": {flag: False for flag in BOUNDARY_FALSE},
        **meta,
    }
    non_claims = {
        "object_id": "task_manager_mount_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }
    planning_pass = len(issues) == 0
    readiness = {
        "object_id": "task_manager_mount_readiness_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "blocker_count": len(issues),
        "health_watchdog_foundation_consumed": True,
        "decision_center_foundation_consumed": True,
        "must_not_redefine_health_watchdog": True,
        "must_not_redefine_decision_center": True,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "blocker_count": len(issues),
        "violations": issues,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "upstream_go_chain": upstream_entries,
        **meta,
    }
    return {
        "summary": summary,
        "task_manager_mount_scope": mount_scope,
        "task_manager_mount_contract": mount_contract,
        "task_manager_input_contract": input_contract,
        "task_manager_output_contract": output_contract,
        "task_manager_processing_model": processing_model,
        "task_manager_task_state_machine": task_state_machine,
        "task_manager_model_rule_algorithm_placement": model_rule_algorithm,
        "task_manager_governance_boundary": governance_boundary,
        "task_manager_health_watchdog_dependency_boundary": hw_dependency_boundary,
        "task_manager_decision_center_dependency_boundary": dc_dependency_boundary,
        "task_manager_downstream_handoff_matrix": downstream_handoff_matrix,
        "task_manager_sample_flow_plan": sample_flow_plan,
        "task_manager_failure_route_matrix": failure_route_matrix,
        "task_manager_mount_health_metric_scope": health_metric_scope,
        "task_manager_boundary_matrix": boundary_matrix,
        "task_manager_mount_non_claims": non_claims,
        "task_manager_mount_readiness_decision": readiness,
    }
