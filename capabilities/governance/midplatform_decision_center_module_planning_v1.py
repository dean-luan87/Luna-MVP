# -*- coding: utf-8 -*-
"""Midplatform Decision Center Module Planning v1 — bind decision center to governance layers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as HEALTH_POST_DR_FINAL_GO,
)
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_core_architecture_resume_v1 import (
    FINAL_DECISION_GO as CORE_RESUME_FINAL_GO,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL_GO,
)
from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as WHITEBOX_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Decision-Center-Module-Planning-v1-001"
SCOPE = "decision_center_module_planning_only"
SOURCE_CHAIN = "midplatform_decision_center_module_planning_v1"

UPSTREAM_CORE_RESUME_FINAL = CORE_RESUME_FINAL_GO
UPSTREAM_WHITEBOX_DR_FINAL = WHITEBOX_DR_FINAL_GO
UPSTREAM_VALIDATION_SEP_DR_FINAL = VALIDATION_SEP_DR_FINAL_GO
UPSTREAM_CONSTITUTION_DR_FINAL = CONSTITUTION_DR_FINAL_GO
UPSTREAM_HEALTH_POST_DR_FINAL = HEALTH_POST_DR_FINAL_GO

FINAL_DECISION_GO = "MIDPLATFORM_DECISION_CENTER_MODULE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_DECISION_CENTER_MODULE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Decision-Center-Module-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Decision-Center-Module-Planning-Issue-Review-v1-001"

CORE_PRINCIPLE = "宪法定法，检测执法，健康度给压力数据，裁决中心作综合裁决"

DECISION_CENTER_NOT: Tuple[str, ...] = (
    "Constitution author",
    "Validation executor",
    "Health metric author",
    "Whitebox runtime",
    "Provider runtime",
    "Model runtime",
    "User output plane",
    "Memory writer",
    "WorldModel writer",
)

GOVERNANCE_BINDINGS: Tuple[Dict[str, Any], ...] = (
    {
        "binding_id": "constitution_binding",
        "label": "Constitution Binding",
        "role": "规则来源、不可越界底线、层级优先级、冲突裁决底线",
        "source_layer": "Constitution Engineering",
        "decision_center_consumes": True,
        "decision_center_authors": False,
    },
    {
        "binding_id": "validation_binding",
        "label": "Validation Binding",
        "role": "gate pass/fail、boundary violation、evidence integrity、issue trace、violation report",
        "source_layer": "Validation Engineering",
        "decision_center_consumes": True,
        "decision_center_authors": False,
    },
    {
        "binding_id": "health_binding",
        "label": "Health Binding",
        "role": "pressure signal、degradation signal、hold/fallback context、system stress context",
        "source_layer": "Health Management",
        "note": "健康度当前仍不定义数字分，只作为 signal/context",
        "decision_center_consumes": True,
        "decision_center_authors": False,
    },
    {
        "binding_id": "whitebox_binding",
        "label": "Whitebox Binding",
        "role": "visibility、rationale、source_chain、traceability、explainability",
        "source_layer": "Whitebox Engineering",
        "decision_center_consumes": True,
        "decision_center_authors": False,
    },
    {
        "binding_id": "factory_binding",
        "label": "Factory Binding",
        "role": "候选来源、生产链、provider 状态",
        "source_layer": "Factory / Domain",
        "decision_center_consumes": True,
        "decision_center_authors": False,
    },
)

INPUT_CONTRACT_FIELDS: Tuple[str, ...] = (
    "decision_request_id",
    "source_candidate_refs",
    "domain_config_refs",
    "evidence_pack_refs",
    "validation_result_refs",
    "health_signal_refs",
    "constitution_constraint_refs",
    "domain_standard_refs",
    "whitebox_visibility_refs",
    "task_context_ref",
    "uncertainty_ref",
    "issue_trace_refs",
    "violation_report_refs",
    "source_chain",
    "ttl",
    "candidate_only",
)

OUTPUT_CONTRACT_FIELDS: Tuple[str, ...] = (
    "decision_candidate_id",
    "decision_type",
    "decision_scope",
    "input_refs",
    "rationale_refs",
    "evidence_refs",
    "validation_refs",
    "health_refs",
    "constitution_refs",
    "whitebox_refs",
    "selected_action",
    "blocked_reason",
    "hold_reason",
    "degradation_reason",
    "escalation_reason",
    "uncertainty_level",
    "downstream_allowed_targets",
    "candidate_only",
    "task_response_generation_allowed",
    "user_output_allowed",
    "memory_write_allowed",
    "world_model_write_allowed",
)

DECISION_ACTIONS: Tuple[str, ...] = (
    "allow_candidate_forward",
    "block_candidate",
    "hold_candidate",
    "request_more_evidence",
    "request_validation",
    "request_reobserve",
    "degrade_mode_candidate",
    "fallback_candidate",
    "escalate_to_hive_later",
    "escalate_to_owner_later",
    "emit_issue_trace_candidate",
    "emit_violation_report_candidate",
    "reject_candidate",
)

PRIORITY_LAYERS: Tuple[Dict[str, Any], ...] = (
    {"priority": 1, "layer": "Luna General Constitution"},
    {
        "priority": 2,
        "layer": "Safety / survival / privacy / fact admission / user output constraints",
    },
    {"priority": 3, "layer": "Domain Constitution"},
    {"priority": 4, "layer": "Domain Standard"},
    {"priority": 5, "layer": "Validation result"},
    {"priority": 6, "layer": "Health signal / system pressure"},
    {"priority": 7, "layer": "Evidence confidence"},
    {"priority": 8, "layer": "Task context"},
    {"priority": 9, "layer": "User preference"},
)

CONFLICT_RULES: Tuple[str, ...] = (
    "constitution block overrides all lower signals",
    "validation fail blocks or holds unless explicit constitution-permitted recovery exists",
    "severe health pressure may hold/degrade but not override constitution",
    "missing evidence triggers hold/request_more_evidence",
    "low confidence triggers reobserve/hold",
    "violation triggers block/escalate",
    "user preference cannot override constitution/validation/safety",
    "whitebox evidence explains decision but does not decide",
)

RATIONALE_REQUIREMENTS: Tuple[str, ...] = (
    "every decision_candidate must include rationale_refs",
    "every block must include blocked_reason",
    "every hold must include hold_reason",
    "every degrade must include degradation_reason",
    "every escalation must include escalation_reason",
    "source_chain preserved",
    "evidence refs preserved",
    "validation refs preserved",
    "health refs preserved",
    "constitution refs preserved",
    "whitebox refs preserved",
)

RUNTIME_BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "decision_center_runtime_enabled_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "validation_runtime_enabled_now",
    "whitebox_runtime_enabled_now",
    "health_metric_defined_now",
    "constitution_rule_written_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Decision Center Planning GO ≠ decision runtime enabled",
    "governance binding defined ≠ decision executed",
    "decision_candidate contract ≠ task_response generated",
    "health binding planned ≠ health metric defined",
    "allow action planned ≠ user output allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("decision_center_module_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "decision_center_runtime_enabled_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "validation_runtime_enabled_now",
    "whitebox_runtime_enabled_now",
    "health_metric_defined_now",
    "constitution_rule_written_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_decision_center_module_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "core_principle": CORE_PRINCIPLE,
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


def run_midplatform_decision_center_module_planning_v1(
    *,
    midplatform_core_architecture_resume_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    health_management_layer_integration_post_dryrun_review_root: str,
    midplatform_whitebox_inspection_integration_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    core_root = Path(midplatform_core_architecture_resume_root).expanduser().resolve()
    const_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()
    val_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    health_root = Path(
        health_management_layer_integration_post_dryrun_review_root
    ).expanduser().resolve()
    whitebox_root = Path(
        midplatform_whitebox_inspection_integration_dryrun_and_review_root
    ).expanduser().resolve()

    core_sm = _try_read_json(core_root / "summary.json") or {}
    core_vr = _try_read_json(core_root / "verifier_report.json") or {}
    core_decision = _load_or_empty(core_root, "midplatform_core_architecture_resume_decision_v1.json")
    const_vr = _try_read_json(const_root / "verifier_report.json") or {}
    const_sm = _try_read_json(const_root / "summary.json") or {}
    val_vr = _try_read_json(val_root / "verifier_report.json") or {}
    val_sm = _try_read_json(val_root / "summary.json") or {}
    health_vr = _try_read_json(health_root / "verifier_report.json") or {}
    health_sm = _try_read_json(health_root / "summary.json") or {}
    whitebox_vr = _try_read_json(whitebox_root / "verifier_report.json") or {}
    whitebox_sm = _try_read_json(whitebox_root / "summary.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_core_resume_root": str(core_root),
        "upstream_constitution_explanation_dryrun_root": str(const_root),
        "upstream_validation_separation_dryrun_root": str(val_root),
        "upstream_health_post_dryrun_root": str(health_root),
        "upstream_whitebox_dryrun_root": str(whitebox_root),
        "output_root": str(out_root),
    }

    if core_vr.get("verifier") != "GO":
        blockers.append("Midplatform Core Architecture Resume verifier must be GO")
    if core_sm.get("final_decision") != UPSTREAM_CORE_RESUME_FINAL:
        blockers.append("core resume final_decision mismatch")
    if const_vr.get("verifier") != "GO":
        blockers.append("Constitution Governance Explanation must be GO")
    if const_sm.get("final_decision") != UPSTREAM_CONSTITUTION_DR_FINAL:
        blockers.append("constitution explanation final_decision mismatch")
    if val_vr.get("verifier") != "GO":
        blockers.append("Validation Engineering Separation must be GO")
    if val_sm.get("final_decision") != UPSTREAM_VALIDATION_SEP_DR_FINAL:
        blockers.append("validation separation final_decision mismatch")
    if health_vr.get("verifier") != "GO":
        blockers.append("Health Management Layer Integration Post DryRun must be GO")
    if health_sm.get("final_decision") != UPSTREAM_HEALTH_POST_DR_FINAL:
        blockers.append("health post dryrun final_decision mismatch")
    if whitebox_vr.get("verifier") != "GO":
        blockers.append("Whitebox Integration DryRunAndReview must be GO")
    if whitebox_sm.get("final_decision") != UPSTREAM_WHITEBOX_DR_FINAL:
        blockers.append("whitebox dryrun final_decision mismatch")

    input_ok = len(blockers) == 0

    resume_input_review = {
        "review_id": "midplatform_core_resume_input_review_v1",
        "core_resume_verifier": core_vr.get("verifier"),
        "core_resume_final_decision": core_sm.get("final_decision"),
        "constitution_remains_rule_source": True,
        "validation_remains_executor_gatekeeper": True,
        "health_remains_pressure_signal_source": True,
        "whitebox_remains_visibility_layer": True,
        "decision_center_does_not_replace_upstream": True,
        "ocr_local_check_sealed": core_decision.get("ocr_local_check_sealed"),
        "whitebox_integration_sealed": core_decision.get("whitebox_integration_sealed"),
        "upstream_roots": {
            "core_resume": str(core_root),
            "constitution_explanation": str(const_root),
            "validation_separation": str(val_root),
            "health_post_dryrun": str(health_root),
            "whitebox_dryrun": str(whitebox_root),
        },
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    module_definition = {
        "definition_id": "decision_center_module_definition_v1",
        "module_id": "midplatform_decision_center_v1",
        "module_type": "core_midplatform_governance_module",
        "role": "decision_arbitration_and_candidate_routing",
        "runtime_enabled_now": False,
        "consumes_constitution": True,
        "consumes_validation": True,
        "consumes_health": True,
        "consumes_whitebox_visibility": True,
        "consumes_candidate_and_evidence": True,
        "emits_decision_candidate_later": True,
        "decision_center_is_not": list(DECISION_CENTER_NOT),
        "not_independent_kingdom": True,
        "consumes_governance_layers": True,
        **meta,
    }

    binding_model = {
        "model_id": "decision_center_governance_binding_model_v1",
        "core_principle": CORE_PRINCIPLE,
        "governance_layers": {
            "constitution_engineering": "法律来源 — 什么绝对不能做、什么必须优先、冲突时谁压过谁",
            "validation_engineering": "执法结果 — 候选是否通过门禁、哪里违规、证据链是否完整",
            "health_management": "运行压力 / 系统经济数据 — 是否承压、是否应降级/暂停/延后",
            "decision_center": "裁决机关 — 根据三类输入决定 allow/block/hold/degrade/reobserve/escalate",
        },
        "bindings": list(GOVERNANCE_BINDINGS),
        "decision_center_consumes_bindings": True,
        "decision_center_does_not_author_bindings": True,
        "decision_center_cannot_override_constitution": True,
        "failed_validation_cannot_become_allow_without_higher_rule": True,
        "decision_center_cannot_invent_health_score": True,
        **meta,
    }

    constitution_binding = {
        "plan_id": "constitution_to_decision_binding_plan_v1",
        "general_constitution_highest_priority": True,
        "domain_constitution_constrains_domain_candidate": True,
        "domain_standard_constrains_io_evidence_auth_provider": True,
        "personalized_constitution_overlay_only": True,
        "constitution_block_action": "block_candidate",
        "constitution_uncertain_action": "hold_candidate or request_more_evidence",
        "constitution_conflict_conservative_decision": True,
        "user_task_preference_cannot_override_constitution": True,
        **meta,
    }

    validation_binding = {
        "plan_id": "validation_to_decision_binding_plan_v1",
        "validation_pass_may_proceed_if_no_higher_block": True,
        "validation_fail_action": "block_candidate or hold_candidate",
        "boundary_violation_action": "violation_report_candidate + block",
        "evidence_chain_invalid_action": "hold/request_more_evidence",
        "no_validation_result_action": "hold/request_validation",
        "issue_trace_informs_escalation": True,
        "decision_center_does_not_execute_validation_gate": True,
        **meta,
    }

    health_binding = {
        "plan_id": "health_to_decision_binding_plan_v1",
        "health_signal_is_pressure_status_context": True,
        "health_metric_definition_status": health_sm.get("health_metric_definition_status", "reserved_not_defined"),
        "no_numeric_health_score_invented": True,
        "severe_health_pressure_action": "hold_candidate / degrade_mode_candidate",
        "provider_pressure_action": "fallback_candidate / hold",
        "hardware_risk_action": "hold / escalation later",
        "health_does_not_authorize_execution_by_itself": True,
        "health_cannot_override_constitution_validation": True,
        **meta,
    }

    whitebox_binding = {
        "plan_id": "whitebox_to_decision_binding_plan_v1",
        "whitebox_visibility_provides_rationale_refs": True,
        "whitebox_exposes_chain_node_evidence_boundary": True,
        "whitebox_does_not_decide": True,
        "node_level_evidence_cannot_define_global_health": True,
        "decision_center_attaches_whitebox_refs_for_explainability": True,
        **meta,
    }

    factory_binding = {
        "plan_id": "factory_domain_candidate_to_decision_binding_plan_v1",
        "capability_factory_produces_candidate": True,
        "validation_factory_inspects_candidate": True,
        "domain_config_gives_domain_constraints": True,
        "provider_readiness_is_input_not_final_decision": True,
        "domain_binding_pattern": ["OCR", "Vision", "Voice", "Map", "Memory"],
        "no_module_specific_decision_logic_outside_decision_center": True,
        **meta,
    }

    input_contract = {
        "contract_id": "decision_center_input_contract_v1",
        "required_fields": list(INPUT_CONTRACT_FIELDS),
        "candidate_only": True,
        **meta,
    }

    output_contract = {
        "contract_id": "decision_center_output_contract_v1",
        "output_type": "decision_candidate",
        "required_fields": list(OUTPUT_CONTRACT_FIELDS),
        "defaults": {
            "candidate_only": True,
            "task_response_generation_allowed": False,
            "user_output_allowed": False,
            "memory_write_allowed": False,
            "world_model_write_allowed": False,
        },
        **meta,
    }

    action_taxonomy = {
        "taxonomy_id": "decision_action_taxonomy_v1",
        "actions": list(DECISION_ACTIONS),
        "action_count": len(DECISION_ACTIONS),
        **meta,
    }

    priority_conflict = {
        "policy_id": "decision_priority_and_conflict_policy_v1",
        "priority_layers": list(PRIORITY_LAYERS),
        "conflict_rules": list(CONFLICT_RULES),
        **meta,
    }

    rationale_trace = {
        "plan_id": "decision_rationale_and_traceability_plan_v1",
        "requirements": list(RATIONALE_REQUIREMENTS),
        **meta,
    }

    task_response_boundary = {
        "plan_id": "decision_to_task_response_boundary_plan_v1",
        "decision_candidate_not_task_response_candidate": True,
        "allow_candidate_forward_not_user_output": True,
        "task_response_requires_separate_integration_phase": True,
        "user_output_requires_output_plane_later": True,
        "memory_world_model_requires_separate_write_policy": True,
        "decision_center_cannot_directly_speak_to_user": True,
        **meta,
    }

    runtime_boundary = {
        "matrix_id": "decision_center_runtime_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in RUNTIME_BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "decision_center_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate decision_center_model_candidate",
            "generate sample decision_request_candidate",
            "generate sample decision_candidate",
            "verify Constitution / Validation / Health / Whitebox / Candidate / Evidence bindings",
            "verify priority/conflict policy",
            "verify decision_candidate ≠ task_response ≠ user_output",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok

    planning_decision = {
        "decision_id": "decision_center_module_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "decision_center_module_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "module_planning_not_runtime": True,
        "decision_center_is_governance_consumer_not_author": True,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "decision_center_module_planning_policy": policy,
        "midplatform_core_resume_input_review": resume_input_review,
        "decision_center_module_definition": module_definition,
        "decision_center_governance_binding_model": binding_model,
        "constitution_to_decision_binding_plan": constitution_binding,
        "validation_to_decision_binding_plan": validation_binding,
        "health_to_decision_binding_plan": health_binding,
        "whitebox_to_decision_binding_plan": whitebox_binding,
        "factory_domain_candidate_to_decision_binding_plan": factory_binding,
        "decision_center_input_contract": input_contract,
        "decision_center_output_contract": output_contract,
        "decision_action_taxonomy": action_taxonomy,
        "decision_priority_and_conflict_policy": priority_conflict,
        "decision_rationale_and_traceability_plan": rationale_trace,
        "decision_to_task_response_boundary_plan": task_response_boundary,
        "decision_center_runtime_boundary_matrix": runtime_boundary,
        "decision_center_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "decision_center_module_planning_decision": planning_decision,
        "summary": summary,
    }


def _load_or_empty(root: Path, fname: str) -> Dict[str, Any]:
    data = _try_read_json(root / fname)
    return data if isinstance(data, dict) else {}
