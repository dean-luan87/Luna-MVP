# -*- coding: utf-8 -*-
"""Midplatform Whitebox Inspection Integration Planning v1 — absorb existing detection into whitebox."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as AUTH_EXT_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL_GO,
)
from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_v1 import (
    FINAL_DECISION_FAIL as OCR_EXEC_FAIL,
    FINAL_DECISION_PASS as OCR_EXEC_PASS,
    FINAL_DECISION_VIOLATION as OCR_EXEC_VIOLATION,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MINIMAL_DRYRUN_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Whitebox-Inspection-Integration-Planning-v1-001"
SCOPE = "whitebox_inspection_integration_planning_only"
SOURCE_CHAIN = "midplatform_whitebox_inspection_integration_planning_v1"

UPSTREAM_VALIDATION_SEP_DR_FINAL = VALIDATION_SEP_DR_FINAL_GO
UPSTREAM_CONSTITUTION_DR_FINAL = CONSTITUTION_DR_FINAL_GO
UPSTREAM_AUTH_EXT_DR_FINAL = AUTH_EXT_DR_FINAL_GO
UPSTREAM_MINIMAL_DRYRUN_FINAL = MINIMAL_DRYRUN_FINAL_GO

OCR_EXEC_VALID_FINALS: Tuple[str, ...] = (
    OCR_EXEC_PASS,
    OCR_EXEC_FAIL,
    OCR_EXEC_VIOLATION,
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_WHITEBOX_INSPECTION_INTEGRATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_WHITEBOX_INSPECTION_INTEGRATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Whitebox-Inspection-Integration-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Whitebox-Inspection-Integration-Planning-Issue-Review-v1-001"

WHITEBOX_VISIBILITY_DOMAINS: Tuple[str, ...] = (
    "Constitution Rule Visibility",
    "Health Signal Visibility",
    "Validation Gate Visibility",
    "Authorization Chain Visibility",
    "Factory / Machine / Provider Visibility",
    "Evidence Chain Visibility",
    "Boundary Audit Visibility",
    "Issue Traceback Visibility",
    "Violation Report Visibility",
    "Post-Review / Route Decision Visibility",
)

VALIDATION_ABSORPTION: Tuple[Dict[str, str], ...] = (
    {"component": "ValidationFactory", "whitebox_node": "Whitebox inspection node"},
    {
        "component": "ControlledProviderReadinessHarness",
        "whitebox_node": "Whitebox provider readiness visibility",
    },
    {"component": "NoRuntimeBoundaryAudit", "whitebox_node": "Whitebox boundary visibility"},
    {
        "component": "AuthorizationValidationGate",
        "whitebox_node": "Whitebox authorization gate visibility",
    },
    {"component": "EvidenceChainValidator", "whitebox_node": "Whitebox evidence visibility"},
    {"component": "HealthCheckValidator", "whitebox_node": "Whitebox health pressure visibility"},
    {"component": "IssueTracebackEngine", "whitebox_node": "Whitebox root-cause visibility"},
    {"component": "ViolationReportEngine", "whitebox_node": "Whitebox violation visibility"},
)

CHV_MAPPING: Tuple[Dict[str, str], ...] = (
    {"layer": "Constitution Engineering", "role": "rule source visibility"},
    {"layer": "Health Management", "role": "system pressure / economic indicator visibility"},
    {"layer": "Validation Engineering", "role": "enforcement / gatekeeping visibility"},
    {
        "layer": "Whitebox Engineering",
        "role": "integrated observability over Constitution + Health + Validation",
    },
)

FACTORY_AUTH_MAPPING: Tuple[Dict[str, str], ...] = (
    {"artifact": "Factory Standard", "visibility": "production rule visibility"},
    {"artifact": "Authorization Standard", "visibility": "authorization chain visibility"},
    {"artifact": "domain_config", "visibility": "domain compliance visibility"},
    {"artifact": "Validation Factory", "visibility": "market inspection visibility"},
    {"artifact": "Midplatform Decision Center", "visibility": "decision visibility (later)"},
)

EVIDENCE_TRACE_MAPPING: Tuple[Dict[str, str], ...] = (
    {"artifact": "evidence_package", "visibility": "evidence visibility"},
    {"artifact": "boundary_audit", "visibility": "boundary visibility"},
    {"artifact": "failure_route", "visibility": "failure path visibility"},
    {"artifact": "rollback_result", "visibility": "rollback visibility"},
    {"artifact": "issue_traceback", "visibility": "root-cause visibility"},
    {"artifact": "violation_report", "visibility": "enforcement visibility"},
    {"artifact": "post_review", "visibility": "closure visibility"},
    {"artifact": "route_decision", "visibility": "downstream decision visibility"},
)

INSPECTION_LAYERS: Tuple[Dict[str, Any], ...] = (
    {
        "level": 1,
        "layer_id": "system_level_whitebox",
        "label": "System-level whitebox",
        "scope": "midplatform chain, responsibilities, constitution/health/validation coordination",
        "default_entry": True,
    },
    {
        "level": 2,
        "layer_id": "chain_level_whitebox",
        "label": "Chain-level whitebox",
        "scope": "candidate → evidence → validation → decision → response",
    },
    {
        "level": 3,
        "layer_id": "factory_level_whitebox",
        "label": "Factory-level whitebox",
        "scope": "factory, machine, provider, production line, market inspection center",
    },
    {
        "level": 4,
        "layer_id": "domain_level_whitebox",
        "label": "Domain-level whitebox",
        "scope": "Vision / OCR / Voice / Map domain chains",
    },
    {
        "level": 5,
        "layer_id": "node_level_whitebox",
        "label": "Node-level whitebox",
        "scope": "package / cache / hash / import local nodes",
        "drilldown_only": True,
    },
)

GLOBAL_TO_LOCAL_PRINCIPLES: Tuple[str, ...] = (
    "inspect_system_before_module=true",
    "inspect_chain_before_node=true",
    "inspect_responsibility_before_implementation=true",
    "inspect_midplatform_decision_before_provider_detail=true",
    "local_check_requires_upstream_signal=true",
    "package/cache/hash/provider checks are drilldown evidence, not primary entrypoint",
    "no direct local provider inspection without system-level reason",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Whitebox Integration Planning GO ≠ whitebox runtime enabled",
    "whitebox integration ≠ previous validation chain invalidated",
    "OCR real-dep evidence mapped ≠ provider selection finalized",
    "node-level evidence ≠ global system health conclusion",
    "next DryRunAndReview ≠ runtime inspection enabled",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "whitebox_runtime_enabled_now",
    "new_parallel_whitebox_system_created_now",
    "validation_engineering_replaced_now",
    "existing_detection_chain_invalidated_now",
    "ocr_real_dep_reexecuted_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_whitebox_inspection_integration_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "whitebox_inspection_integration_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_whitebox_inspection_integration_planning_v1(
    *,
    ocr_real_dependency_real_minimal_controlled_execution_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: str,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: str,
    ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    ocr_exec_root = Path(
        ocr_real_dependency_real_minimal_controlled_execution_root
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
    ocr_factory_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
    ).expanduser().resolve()
    minimal_dr_root = Path(
        ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root
        or ocr_exec_root.parent / "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
    ).expanduser().resolve()

    ocr_sm = _try_read_json(ocr_exec_root / "summary.json") or {}
    ocr_vr = _try_read_json(ocr_exec_root / "verifier_report.json") or {}
    val_sm = _try_read_json(val_root / "summary.json") or {}
    val_vr = _try_read_json(val_root / "verifier_report.json") or {}
    const_sm = _try_read_json(const_root / "summary.json") or {}
    const_vr = _try_read_json(const_root / "verifier_report.json") or {}
    auth_sm = _try_read_json(auth_ext_root / "summary.json") or {}
    auth_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}
    ocr_factory_vr = _try_read_json(ocr_factory_root / "verifier_report.json") or {}
    minimal_dr_vr = _try_read_json(minimal_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_ocr_real_execution_root": str(ocr_exec_root),
        "upstream_validation_separation_dryrun_root": str(val_root),
        "upstream_constitution_explanation_dryrun_root": str(const_root),
        "upstream_auth_extension_dryrun_root": str(auth_ext_root),
        "upstream_ocr_via_factory_dryrun_root": str(ocr_factory_root),
        "upstream_minimal_controlled_dryrun_root": str(minimal_dr_root),
        "output_root": str(out_root),
    }

    if ocr_vr.get("verifier") != "GO":
        blockers.append("OCR real minimal execution verifier must be GO")
    if ocr_sm.get("boundary_ok") is not True:
        blockers.append("OCR execution boundary_ok must be true")
    if ocr_sm.get("execution_completed") is not True:
        blockers.append("OCR execution_completed must be true")
    if ocr_sm.get("final_decision") not in OCR_EXEC_VALID_FINALS:
        blockers.append("OCR execution final_decision invalid")
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
    if ocr_factory_vr.get("verifier") != "GO":
        blockers.append("OCR via factory dryrun should be GO")
    if minimal_dr_vr.get("verifier") != "GO":
        blockers.append("minimal controlled dryrun should be GO")

    input_ok = len(blockers) == 0

    chain_input = {
        "review_id": "existing_detection_chain_input_review_v1",
        "upstream_roots": {
            "ocr_real_minimal_execution": str(ocr_exec_root),
            "validation_separation": str(val_root),
            "constitution_explanation": str(const_root),
            "auth_extension": str(auth_ext_root),
            "ocr_via_factory": str(ocr_factory_root),
            "minimal_controlled_dryrun": str(minimal_dr_root),
        },
        "ocr_execution_checks_passed": ocr_sm.get("checks_passed"),
        "ocr_record_failure_only_ok": ocr_sm.get("checks_passed") is False
        and ocr_sm.get("boundary_ok") is True,
        "detection_chain_preserved": True,
        "detection_chain_absorbed_into_whitebox": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    role_definition = {
        "definition_id": "whitebox_engineering_role_definition_v1",
        "whitebox_engineering_is": "transparent inspection and explainable governance engineering",
        "whitebox_does_not_redraft_constitution": True,
        "whitebox_does_not_replace_validation_engineering": True,
        "whitebox_does_not_reinvent_authorization_standard": True,
        "whitebox_does_not_execute_provider_directly": True,
        "whitebox_responsibility": (
            "visualize and audit rules, health, validation, evidence, boundaries, "
            "traceback, and decisions end-to-end"
        ),
        "visibility_domains": list(WHITEBOX_VISIBILITY_DOMAINS),
        **meta,
    }

    validation_absorption = {
        "mapping_id": "validation_engineering_absorption_mapping_v1",
        "absorbed_not_replaced": True,
        "mappings": list(VALIDATION_ABSORPTION),
        "validation_engineering_remains_enforcement_layer": True,
        "whitebox_provides_visibility_layer": True,
        **meta,
    }

    chv_mapping = {
        "mapping_id": "constitution_health_validation_whitebox_mapping_v1",
        "mappings": list(CHV_MAPPING),
        "whitebox_integrates_observability": True,
        "whitebox_replaces_none": True,
        **meta,
    }

    factory_auth_mapping = {
        "mapping_id": "factory_authorization_whitebox_mapping_v1",
        "mappings": list(FACTORY_AUTH_MAPPING),
        **meta,
    }

    evidence_trace_mapping = {
        "mapping_id": "evidence_boundary_traceback_whitebox_mapping_v1",
        "mappings": list(EVIDENCE_TRACE_MAPPING),
        "ocr_real_execution_evidence_ref": str(ocr_exec_root / "execution_evidence_package_v1.json"),
        **meta,
    }

    global_local = {
        "principle_id": "global_to_local_inspection_principle_v1",
        "hard_principles": list(GLOBAL_TO_LOCAL_PRINCIPLES),
        "default_entry_level": "system_level_whitebox",
        "node_level_drilldown_only": True,
        **meta,
    }

    layer_model = {
        "model_id": "whitebox_inspection_layer_model_v1",
        "layers": list(INSPECTION_LAYERS),
        "default_start_level": 1,
        "node_level_requires_upstream_signal": True,
        **meta,
    }

    drilldown_policy = {
        "policy_id": "whitebox_drilldown_policy_v1",
        "drilldown_allowed_when": [
            "upper_layer_anomaly_detected",
            "route_decision_points_to_local",
            "authorization_chain_requires_node_evidence",
        ],
        "drilldown_forbidden_when": [
            "no_system_level_reason",
            "direct_provider_inspection_without_midplatform_decision",
        ],
        "ocr_real_dep_is_drilldown_target": True,
        **meta,
    }

    ocr_local_mapping = {
        "mapping_id": "ocr_real_dep_as_local_evidence_mapping_v1",
        "evidence_level": "node_level_whitebox",
        "is_local_evidence_not_global_entry": True,
        "uses_for_future": [
            "provider_selection",
            "dependency_readiness",
            "execution_readiness",
        ],
        "must_not_expand_as_main_detection_chain": True,
        "read_only_evidence_source": True,
        "failure_does_not_trigger_install_download_repair": True,
        "ocr_execution_root": str(ocr_exec_root),
        "checks_executed": ocr_sm.get("real_execution_started_now") is True,
        "checks_passed": ocr_sm.get("checks_passed"),
        **meta,
    }

    no_parallel = {
        "policy_id": "no_parallel_whitebox_policy_v1",
        "no_new_parallel_whitebox_system": True,
        "existing_validation_engineering_absorbed": True,
        "existing_authorization_chain_absorbed": True,
        "existing_evidence_boundary_traceback_absorbed": True,
        "historical_detection_artifacts_preserved": True,
        "previous_work_not_invalidated": True,
        "future_whitebox_phases_must_reference_existing_validation_artifacts": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "whitebox_integration_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate whitebox_inspection_model_candidate",
            "verify existing detection chain absorbed into whitebox",
            "verify system → chain → factory → domain → node drilldown",
            "verify OCR real-dep as node-level evidence",
            "verify no parallel whitebox system created",
            "no runtime enabled",
        ],
        **meta,
    }

    planning_pass = input_ok and chain_input.get("review_pass") is True

    planning_decision = {
        "decision_id": "whitebox_inspection_integration_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "whitebox_inspection_integration_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "integration_not_rebuild": True,
        "whitebox_is_observability_not_new_rules": True,
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
        "violations": blockers,
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "whitebox_inspection_integration_planning_policy": policy,
        "existing_detection_chain_input_review": chain_input,
        "whitebox_engineering_role_definition": role_definition,
        "validation_engineering_absorption_mapping": validation_absorption,
        "constitution_health_validation_whitebox_mapping": chv_mapping,
        "factory_authorization_whitebox_mapping": factory_auth_mapping,
        "evidence_boundary_traceback_whitebox_mapping": evidence_trace_mapping,
        "global_to_local_inspection_principle": global_local,
        "whitebox_inspection_layer_model": layer_model,
        "whitebox_drilldown_policy": drilldown_policy,
        "ocr_real_dep_as_local_evidence_mapping": ocr_local_mapping,
        "no_parallel_whitebox_policy": no_parallel,
        "whitebox_integration_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "whitebox_inspection_integration_planning_decision": planning_decision,
        "summary": summary,
    }
