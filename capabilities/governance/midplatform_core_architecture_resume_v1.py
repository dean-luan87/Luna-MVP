# -*- coding: utf-8 -*-
"""Midplatform Core Architecture Resume v1 — restore mainline after whitebox integration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as AUTH_EXT_DR_FINAL_GO,
)
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL_GO,
)
from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as WHITEBOX_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_v1 import (
    FINAL_DECISION_FAIL as OCR_EXEC_FAIL,
    FINAL_DECISION_PASS as OCR_EXEC_PASS,
    FINAL_DECISION_VIOLATION as OCR_EXEC_VIOLATION,
)

PHASE_ID = "Phase-Midplatform-Core-Architecture-Resume-v1-001"
SCOPE = "midplatform_core_architecture_resume_only"
SOURCE_CHAIN = "midplatform_core_architecture_resume_v1"

UPSTREAM_WHITEBOX_DR_FINAL = WHITEBOX_DR_FINAL_GO
UPSTREAM_VALIDATION_SEP_DR_FINAL = VALIDATION_SEP_DR_FINAL_GO
UPSTREAM_CONSTITUTION_DR_FINAL = CONSTITUTION_DR_FINAL_GO
UPSTREAM_AUTH_EXT_DR_FINAL = AUTH_EXT_DR_FINAL_GO

OCR_EXEC_VALID_FINALS: Tuple[str, ...] = (
    OCR_EXEC_PASS,
    OCR_EXEC_FAIL,
    OCR_EXEC_VIOLATION,
)

FINAL_DECISION_GO = "MIDPLATFORM_CORE_ARCHITECTURE_RESUME_READY_FOR_DECISION_CENTER_PLANNING"
FINAL_DECISION_HOLD = "MIDPLATFORM_CORE_ARCHITECTURE_RESUME_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Decision-Center-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Core-Architecture-Resume-Issue-Review-v1-001"

MIDPLATFORM_CORE_RESPONSIBILITIES: Tuple[str, ...] = (
    "consume candidate objects",
    "consume evidence packages",
    "consume validation results",
    "consume health signals",
    "consume constitution / domain standard references",
    "run decision logic later",
    "assemble task_response_candidate later",
    "route failure / violation / issue trace",
    "decide output eligibility later",
)

MIDPLATFORM_NOT: Tuple[str, ...] = (
    "provider runtime",
    "OCR runtime",
    "model runtime",
    "constitution author",
    "validation rule author",
    "memory writer by default",
    "world model writer by default",
    "user output plane by default",
)

MIDPLATFORM_BOUNDARIES: Tuple[Dict[str, str], ...] = (
    {"boundary": "consume_upstream_not_invoke_provider", "rule": "中台消费上游，不直接调用 provider"},
    {"boundary": "decide_not_equal_user_output", "rule": "中台裁决，不直接等于用户输出"},
    {"boundary": "assemble_candidate_not_write_fact", "rule": "中台可组装候选，不直接写事实"},
    {"boundary": "read_health_not_invent_metrics", "rule": "中台可读取健康度，不自造健康指标"},
    {"boundary": "consume_whitebox_not_replace", "rule": "中台可消费白盒可见性，不替代白盒"},
    {
        "boundary": "consume_validation_factory_not_replace",
        "rule": "中台可消费 Validation Factory pass/fail，不替代 Validation Engineering",
    },
)

OBJECT_FLOW_TYPES: Tuple[str, ...] = (
    "domain_config",
    "observation_candidate",
    "ocr_result_candidate",
    "speech_candidate",
    "emotion_candidate",
    "evidence_pack",
    "validation_result",
    "health_signal_candidate",
    "issue_trace",
    "violation_report",
    "decision_candidate",
    "task_response_candidate",
    "user_output_candidate",
)

CEVDR_FLOW_STEPS: Tuple[Dict[str, Any], ...] = (
    {"step": 1, "action": "domain / factory produces candidate"},
    {"step": 2, "action": "evidence pack binds source_chain"},
    {"step": 3, "action": "Validation Engineering executes gate later"},
    {"step": 4, "action": "Whitebox exposes visibility"},
    {"step": 5, "action": "Health provides pressure/risk context"},
    {"step": 6, "action": "Decision Center creates decision_candidate"},
    {"step": 7, "action": "Midplatform assembles task_response_candidate"},
    {"step": 8, "action": "Output plane later decides user-facing output"},
)

DECISION_CENTER_DUTIES: Tuple[str, ...] = (
    "consume constitution constraints",
    "consume validation results",
    "consume health signals",
    "consume task context",
    "consume evidence confidence",
    "decide allow / block / hold / degrade / reobserve / escalate",
    "emit decision_candidate",
    "never bypass validation / constitution",
)

CHV_CONSUMPTION: Tuple[Dict[str, str], ...] = (
    {"layer": "Constitution Engineering", "role": "rule source"},
    {"layer": "Health Management", "role": "pressure / status signal"},
    {"layer": "Validation Engineering", "role": "enforcement result"},
    {"layer": "Whitebox Engineering", "role": "visibility / explainability layer"},
    {
        "layer": "Decision Center",
        "role": "consumes all four but does not replace them",
    },
)

FACTORY_MARKET_FLOW: Tuple[Dict[str, str], ...] = (
    {"actor": "capability factory", "role": "produces candidate"},
    {"actor": "machine/provider", "role": "produces raw candidate"},
    {"actor": "factory internal control", "role": "handles provider readiness"},
    {"actor": "Validation Factory", "role": "market inspection center"},
    {"actor": "Midplatform", "role": "market / assembly / decision center"},
    {"actor": "user", "role": "consumer"},
    {
        "actor": "output gate",
        "role": "only inspected / validated / decision-approved candidate may become output candidate",
    },
)

DOMAIN_CONFIG_DOMAINS: Tuple[str, ...] = (
    "OCR",
    "Vision",
    "Voice",
    "Map",
    "Memory",
    "Library",
    "Hive",
)

FAILURE_ROUTES: Tuple[Dict[str, str], ...] = (
    {"trigger": "validation fail", "route": "hold / block / issue_trace"},
    {"trigger": "boundary violation", "route": "violation_report"},
    {"trigger": "low confidence", "route": "reobserve / ask user / hold"},
    {"trigger": "health pressure", "route": "degrade / hold / route later"},
    {"trigger": "missing evidence", "route": "evidence request candidate"},
    {"trigger": "provider failure", "route": "factory/harness issue trace"},
    {"trigger": "severe violation", "route": "Hive escalation later"},
)

RUNTIME_BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "decision_center_executed_now",
    "provider_invoked_now",
    "model_invoked_now",
    "validation_runtime_enforced_now",
    "whitebox_runtime_enabled_now",
    "output_generated_now",
    "fact_written_now",
    "memory_written_now",
    "world_model_written_now",
)

DEFERRED_ROUTES: Tuple[Dict[str, str], ...] = (
    {"route_id": "Route B", "label": "Candidate/Evidence Flow Integration", "status": "defer"},
    {"route_id": "Route C", "label": "Task Response Candidate Output Chain", "status": "defer"},
    {"route_id": "Route D", "label": "Runtime Planning", "status": "defer"},
    {"route_id": "Route E", "label": "Return OCR Provider Work", "status": "defer"},
)

NON_CLAIMS: Tuple[str, ...] = (
    "Core Architecture Resume GO ≠ Midplatform runtime enabled",
    "Decision Center planned next ≠ decision executed",
    "candidate flow defined ≠ user output allowed",
    "OCR local evidence consumed ≠ OCR provider selected",
    "Whitebox closed ≠ runtime inspection enabled",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("midplatform_core_architecture_resume_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "midplatform_runtime_enabled_now",
    "decision_center_runtime_enabled_now",
    "provider_invoked_now",
    "ocr_reexecuted_now",
    "model_runtime_invoked_now",
    "validation_runtime_enabled_now",
    "whitebox_runtime_enabled_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_core_architecture_resume"
)


def _resume_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
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


def run_midplatform_core_architecture_resume_v1(
    *,
    midplatform_whitebox_inspection_integration_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: str,
    ocr_real_dependency_real_minimal_controlled_execution_root: str,
    ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    whitebox_root = Path(
        midplatform_whitebox_inspection_integration_dryrun_and_review_root
    ).expanduser().resolve()
    val_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    const_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()
    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
    ).expanduser().resolve()
    ocr_exec_root = Path(
        ocr_real_dependency_real_minimal_controlled_execution_root
    ).expanduser().resolve()
    ocr_ready_root = Path(
        ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_root
    ).expanduser().resolve()

    whitebox_sm = _try_read_json(whitebox_root / "summary.json") or {}
    whitebox_vr = _try_read_json(whitebox_root / "verifier_report.json") or {}
    whitebox_model = _try_read_json(whitebox_root / "whitebox_inspection_model_candidate_v1.json") or {}
    whitebox_no_parallel = _try_read_json(whitebox_root / "no_parallel_whitebox_review_v1.json") or {}
    whitebox_ocr = _try_read_json(whitebox_root / "ocr_real_dep_local_evidence_review_v1.json") or {}

    val_vr = _try_read_json(val_root / "verifier_report.json") or {}
    val_sm = _try_read_json(val_root / "summary.json") or {}
    const_vr = _try_read_json(const_root / "verifier_report.json") or {}
    const_sm = _try_read_json(const_root / "summary.json") or {}
    auth_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}
    auth_sm = _try_read_json(auth_ext_root / "summary.json") or {}

    ocr_sm = _try_read_json(ocr_exec_root / "summary.json") or {}
    ocr_vr = _try_read_json(ocr_exec_root / "verifier_report.json") or {}
    ocr_ready_vr = _try_read_json(ocr_ready_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_resume_meta(),
        "upstream_whitebox_dryrun_root": str(whitebox_root),
        "upstream_validation_separation_dryrun_root": str(val_root),
        "upstream_constitution_explanation_dryrun_root": str(const_root),
        "upstream_auth_extension_dryrun_root": str(auth_ext_root),
        "upstream_ocr_real_execution_root": str(ocr_exec_root),
        "upstream_ocr_final_ready_check_root": str(ocr_ready_root),
        "output_root": str(out_root),
    }

    if whitebox_vr.get("verifier") != "GO":
        blockers.append("Whitebox Integration DryRunAndReview verifier must be GO")
    if whitebox_sm.get("final_decision") != UPSTREAM_WHITEBOX_DR_FINAL:
        blockers.append("whitebox dryrun final_decision mismatch")
    if whitebox_model.get("creates_parallel_system") is True:
        blockers.append("whitebox must not create parallel system")
    if whitebox_model.get("absorbs_existing_detection_chain") is not True:
        blockers.append("whitebox must absorb existing detection chain")
    if whitebox_no_parallel.get("no_new_parallel_whitebox_system") is not True:
        blockers.append("no_new_parallel_whitebox_system must be true")
    if whitebox_ocr.get("does_not_finalize_provider") is not True:
        blockers.append("OCR real-dep must not finalize provider")
    if val_vr.get("verifier") != "GO":
        blockers.append("Validation Engineering Separation must be GO")
    if val_sm.get("final_decision") != UPSTREAM_VALIDATION_SEP_DR_FINAL:
        blockers.append("validation separation final_decision mismatch")
    if const_vr.get("verifier") != "GO":
        blockers.append("Constitution Governance Explanation must be GO")
    if const_sm.get("final_decision") != UPSTREAM_CONSTITUTION_DR_FINAL:
        blockers.append("constitution explanation final_decision mismatch")
    if auth_vr.get("verifier") != "GO":
        blockers.append("Factory Authorization Standard Extension must be GO")
    if auth_sm.get("final_decision") != UPSTREAM_AUTH_EXT_DR_FINAL:
        blockers.append("auth extension final_decision mismatch")
    if ocr_vr.get("verifier") != "GO":
        blockers.append("OCR real execution verifier must be GO")
    if ocr_sm.get("boundary_ok") is not True:
        blockers.append("OCR execution boundary_ok must be true")
    if ocr_sm.get("final_decision") not in OCR_EXEC_VALID_FINALS:
        blockers.append("OCR execution final_decision invalid")
    if ocr_ready_vr.get("verifier") != "GO":
        blockers.append("OCR final ready check must be GO")

    input_ok = len(blockers) == 0

    upstream_review = {
        "review_id": "upstream_governance_input_review_v1",
        "whitebox_verifier": whitebox_vr.get("verifier"),
        "whitebox_final_decision": whitebox_sm.get("final_decision"),
        "whitebox_absorption_not_parallel": whitebox_model.get("creates_parallel_system") is False,
        "validation_engineering_remains_gatekeeper": True,
        "constitution_remains_rule_source": True,
        "health_remains_pressure_signal_source": True,
        "factory_authorization_standard_positioned": auth_vr.get("verifier") == "GO",
        "ocr_real_dep_node_level_read_only": True,
        "ocr_evidence_root": str(ocr_exec_root),
        "upstream_roots": {
            "whitebox_dryrun": str(whitebox_root),
            "validation_separation": str(val_root),
            "constitution_explanation": str(const_root),
            "auth_extension": str(auth_ext_root),
            "ocr_real_execution": str(ocr_exec_root),
            "ocr_final_ready_check": str(ocr_ready_root),
        },
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    core_role = {
        "definition_id": "midplatform_core_role_definition_v1",
        "midplatform_core_responsibilities": list(MIDPLATFORM_CORE_RESPONSIBILITIES),
        "midplatform_is_not": list(MIDPLATFORM_NOT),
        "ocr_local_check_status": "sealed_as_node_level_read_only_evidence",
        "whitebox_status": "absorption_integration_complete_not_parallel",
        **meta,
    }

    boundary_def = {
        "definition_id": "midplatform_boundary_definition_v1",
        "boundaries": list(MIDPLATFORM_BOUNDARIES),
        "all_boundaries_acknowledged": True,
        **meta,
    }

    object_flow = {
        "model_id": "midplatform_object_flow_model_v1",
        "object_types": list(OBJECT_FLOW_TYPES),
        "unified_flow": True,
        "candidate_evidence_validation_decision_response": True,
        **meta,
    }

    cevdr_flow = {
        "flow_id": "candidate_evidence_validation_decision_response_flow_v1",
        "steps": list(CEVDR_FLOW_STEPS),
        "default_entry": "system_level_midplatform",
        "node_level_evidence_drilldown_only": True,
        **meta,
    }

    decision_center_plan = {
        "plan_id": "decision_center_role_plan_v1",
        "future_duties": list(DECISION_CENTER_DUTIES),
        "runtime_enabled_now": False,
        "decision_center_runtime_enabled_now": False,
        "never_bypass_validation_constitution": True,
        "emit_decision_candidate_only": True,
        **meta,
    }

    chv_consumption = {
        "plan_id": "constitution_health_validation_consumption_plan_v1",
        "layers": list(CHV_CONSUMPTION),
        "constitution_is_rule_source": True,
        "health_is_pressure_signal": True,
        "validation_is_enforcement": True,
        "whitebox_is_visibility_layer": True,
        "decision_center_consumes_all_does_not_replace": True,
        **meta,
    }

    factory_market = {
        "plan_id": "factory_validation_market_flow_plan_v1",
        "factory_analogy": list(FACTORY_MARKET_FLOW),
        "validation_factory_is_market_inspection": True,
        "midplatform_is_assembly_decision_center": True,
        **meta,
    }

    domain_config_plan = {
        "plan_id": "domain_config_consumption_plan_v1",
        "domains_submit_domain_config": list(DOMAIN_CONFIG_DOMAINS),
        "no_parallel_standards_by_new_modules": True,
        "common_rules_via": [
            "Constitution",
            "Standard",
            "Harness",
            "Validation Factory",
        ],
        "midplatform_consumes_domain_config_after_validation": True,
        **meta,
    }

    task_response_plan = {
        "plan_id": "task_response_candidate_integration_plan_v1",
        "task_response_candidate_is_not_user_output": True,
        "task_response_requires_decision_pass": True,
        "user_output_candidate_requires_output_plane_later": True,
        "evidence_and_validation_refs_preserved": True,
        "uncertainty_preserved": True,
        **meta,
    }

    evidence_trace_plan = {
        "plan_id": "evidence_and_traceability_flow_plan_v1",
        "evidence_pack_binds_source_chain": True,
        "issue_trace_preserved": True,
        "violation_report_preserved": True,
        "whitebox_visibility_consumed_not_replaced": True,
        "ocr_node_evidence_ref": str(ocr_exec_root / "execution_evidence_package_v1.json"),
        **meta,
    }

    failure_route_plan = {
        "plan_id": "failure_route_and_escalation_plan_v1",
        "routes": list(FAILURE_ROUTES),
        **meta,
    }

    runtime_boundary = {
        "matrix_id": "midplatform_runtime_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in RUNTIME_BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    next_route = {
        "decision_id": "next_mainline_route_decision_v1",
        "selected_route": "Route A — Midplatform Decision Center Planning",
        "selected_route_id": "Route A",
        "recommended_next_phase": NEXT_PHASE_GO,
        "deferred_routes": list(DEFERRED_ROUTES),
        "ocr_provider_work_deferred": True,
        "runtime_planning_deferred": True,
        **meta,
    }

    resume_pass = input_ok

    resume_decision = {
        "decision_id": "midplatform_core_architecture_resume_decision_v1",
        "resume_pass": resume_pass,
        "high_risk": not resume_pass,
        "final_decision": FINAL_DECISION_GO if resume_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if resume_pass else NEXT_PHASE_HOLD,
        "mainline_restored": resume_pass,
        "ocr_local_check_sealed": True,
        "whitebox_integration_sealed": True,
        **meta,
    }

    policy = {
        "policy_id": "midplatform_core_architecture_resume_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "architecture_resume_not_runtime": True,
        "ocr_branch_sealed": True,
        "whitebox_absorption_sealed": True,
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
        "boundary_ok": resume_pass,
        "violations": list(blockers),
        "resume_pass": resume_pass,
        "final_decision": resume_decision["final_decision"],
        "recommended_next_phase": resume_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "midplatform_core_architecture_resume_policy": policy,
        "upstream_governance_input_review": upstream_review,
        "midplatform_core_role_definition": core_role,
        "midplatform_boundary_definition": boundary_def,
        "midplatform_object_flow_model": object_flow,
        "candidate_evidence_validation_decision_response_flow": cevdr_flow,
        "decision_center_role_plan": decision_center_plan,
        "constitution_health_validation_consumption_plan": chv_consumption,
        "factory_validation_market_flow_plan": factory_market,
        "domain_config_consumption_plan": domain_config_plan,
        "task_response_candidate_integration_plan": task_response_plan,
        "evidence_and_traceability_flow_plan": evidence_trace_plan,
        "failure_route_and_escalation_plan": failure_route_plan,
        "midplatform_runtime_boundary_matrix": runtime_boundary,
        "next_mainline_route_decision": next_route,
        "non_claims_register": non_claims,
        "midplatform_core_architecture_resume_decision": resume_decision,
        "summary": summary,
    }
