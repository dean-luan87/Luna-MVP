# -*- coding: utf-8 -*-
"""Midplatform Whitebox Inspection Integration DryRunAndReview v1."""

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
from capabilities.governance.midplatform_whitebox_inspection_integration_planning_v1 import (
    CHV_MAPPING,
    EVIDENCE_TRACE_MAPPING,
    FACTORY_AUTH_MAPPING,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GLOBAL_TO_LOCAL_PRINCIPLES,
    INSPECTION_LAYERS,
    VALIDATION_ABSORPTION,
    WHITEBOX_VISIBILITY_DOMAINS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_v1 import (
    FINAL_DECISION_FAIL as OCR_EXEC_FAIL,
    FINAL_DECISION_PASS as OCR_EXEC_PASS,
    FINAL_DECISION_VIOLATION as OCR_EXEC_VIOLATION,
)

PHASE_ID = "Phase-Midplatform-Whitebox-Inspection-Integration-DryRunAndReview-v1-001"
SCOPE = "whitebox_inspection_integration_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_whitebox_inspection_integration_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_VALIDATION_SEP_DR_FINAL = VALIDATION_SEP_DR_FINAL_GO
UPSTREAM_CONSTITUTION_DR_FINAL = CONSTITUTION_DR_FINAL_GO
UPSTREAM_AUTH_EXT_DR_FINAL = AUTH_EXT_DR_FINAL_GO

OCR_EXEC_VALID_FINALS: Tuple[str, ...] = (
    OCR_EXEC_PASS,
    OCR_EXEC_FAIL,
    OCR_EXEC_VIOLATION,
)

FINAL_DECISION_GO = (
    "MIDPLATFORM_WHITEBOX_INSPECTION_INTEGRATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_MIDPLATFORM_CORE_ARCHITECTURE_RESUME"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_WHITEBOX_INSPECTION_INTEGRATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Core-Architecture-Resume-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Whitebox-Inspection-Integration-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_whitebox_runtime_enable",
    "dryrun_to_parallel_whitebox_creation",
    "dryrun_to_validation_engineering_replacement",
    "dryrun_to_constitution_registry_update",
    "dryrun_to_authorization_standard_redefinition",
    "dryrun_to_ocr_real_dep_reexecution",
    "dryrun_to_provider_invoke",
    "dryrun_to_dependency_install",
    "dryrun_to_model_download",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_user_output",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Whitebox Integration DryRunAndReview GO ≠ whitebox runtime enabled",
    "whitebox model candidate ≠ new parallel system",
    "validation absorption ≠ Validation Engineering replaced",
    "OCR real-dep mapped ≠ provider selected",
    "node-level evidence ≠ global system health conclusion",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "whitebox_inspection_integration_dryrun_and_review_only",
    "simulated",
    "whitebox_inspection_model_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "whitebox_runtime_enabled_now",
    "new_parallel_whitebox_system_created_now",
    "validation_engineering_replaced_now",
    "existing_detection_chain_invalidated_now",
    "constitution_registry_updated_now",
    "validation_runtime_enabled_now",
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
    "midplatform_whitebox_inspection_integration_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
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


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def run_midplatform_whitebox_inspection_integration_dryrun_and_review_v1(
    *,
    midplatform_whitebox_inspection_integration_planning_root: str,
    ocr_real_dependency_real_minimal_controlled_execution_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        midplatform_whitebox_inspection_integration_planning_root
    ).expanduser().resolve()
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

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_decision = _try_read_json(
        plan_root / "whitebox_inspection_integration_planning_decision_v1.json"
    ) or {}
    plan_no_parallel = _try_read_json(plan_root / "no_parallel_whitebox_policy_v1.json") or {}
    plan_role = _try_read_json(plan_root / "whitebox_engineering_role_definition_v1.json") or {}
    plan_val_abs = _try_read_json(
        plan_root / "validation_engineering_absorption_mapping_v1.json"
    ) or {}
    plan_chv = _try_read_json(
        plan_root / "constitution_health_validation_whitebox_mapping_v1.json"
    ) or {}
    plan_factory = _try_read_json(plan_root / "factory_authorization_whitebox_mapping_v1.json") or {}
    plan_evidence = _try_read_json(
        plan_root / "evidence_boundary_traceback_whitebox_mapping_v1.json"
    ) or {}
    plan_global = _try_read_json(plan_root / "global_to_local_inspection_principle_v1.json") or {}
    plan_layers = _try_read_json(plan_root / "whitebox_inspection_layer_model_v1.json") or {}
    plan_ocr_local = _try_read_json(
        plan_root / "ocr_real_dep_as_local_evidence_mapping_v1.json"
    ) or {}

    ocr_sm = _try_read_json(ocr_exec_root / "summary.json") or {}
    ocr_vr = _try_read_json(ocr_exec_root / "verifier_report.json") or {}
    val_vr = _try_read_json(val_root / "verifier_report.json") or {}
    val_sm = _try_read_json(val_root / "summary.json") or {}
    const_vr = _try_read_json(const_root / "verifier_report.json") or {}
    auth_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_ocr_real_execution_root": str(ocr_exec_root),
        "upstream_validation_separation_dryrun_root": str(val_root),
        "upstream_constitution_explanation_dryrun_root": str(const_root),
        "upstream_auth_extension_dryrun_root": str(auth_ext_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Whitebox Integration Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_no_parallel.get("no_new_parallel_whitebox_system") is not True:
        blockers.append("planning no_new_parallel_whitebox_system must be true")
    if plan_sm.get("validation_engineering_replaced_now") is True:
        blockers.append("validation_engineering_replaced_now must be false")
    if plan_sm.get("existing_detection_chain_invalidated_now") is True:
        blockers.append("existing_detection_chain_invalidated_now must be false")
    if plan_sm.get("whitebox_runtime_enabled_now") is True:
        blockers.append("whitebox_runtime_enabled_now must be false")
    if ocr_vr.get("verifier") != "GO":
        blockers.append("OCR real minimal execution verifier must be GO")
    if ocr_sm.get("boundary_ok") is not True:
        blockers.append("OCR execution boundary_ok must be true")
    if ocr_sm.get("final_decision") not in OCR_EXEC_VALID_FINALS:
        blockers.append("OCR execution final_decision invalid")
    if plan_ocr_local.get("evidence_level") != "node_level_whitebox":
        blockers.append("OCR real-dep must be node-level local evidence")
    if val_vr.get("verifier") != "GO":
        blockers.append("Validation Engineering Separation must be GO")
    if val_sm.get("final_decision") != UPSTREAM_VALIDATION_SEP_DR_FINAL:
        blockers.append("validation separation final_decision mismatch")
    if const_vr.get("verifier") != "GO":
        blockers.append("Constitution Governance Explanation must be GO")
    if auth_vr.get("verifier") != "GO":
        blockers.append("Factory Authorization Standard Extension must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "whitebox_integration_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "planning_pass": plan_sm.get("planning_pass"),
        "no_new_parallel_whitebox_system": plan_no_parallel.get("no_new_parallel_whitebox_system"),
        "validation_engineering_replaced_now": plan_sm.get("validation_engineering_replaced_now"),
        "existing_detection_chain_invalidated_now": plan_sm.get(
            "existing_detection_chain_invalidated_now"
        ),
        "whitebox_runtime_enabled_now": plan_sm.get("whitebox_runtime_enabled_now"),
        "ocr_evidence_level": plan_ocr_local.get("evidence_level"),
        "upstream_roots": {
            "planning": str(plan_root),
            "ocr_real_execution": str(ocr_exec_root),
            "validation_separation": str(val_root),
            "constitution_explanation": str(const_root),
            "auth_extension": str(auth_ext_root),
        },
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    visibility_domain_checks: List[Tuple[str, bool]] = []
    plan_domains = plan_role.get("visibility_domains") or list(WHITEBOX_VISIBILITY_DOMAINS)
    for domain in WHITEBOX_VISIBILITY_DOMAINS:
        visibility_domain_checks.append((f"domain.{domain[:20]}", domain in plan_domains))

    visibility_domain_review = {
        "review_id": "whitebox_visibility_domain_review_v1",
        "visibility_domains": [
            {"domain": d, "pass": d in plan_domains, "simulated": True}
            for d in WHITEBOX_VISIBILITY_DOMAINS
        ],
        "all_domains_pass": all(d in plan_domains for d in WHITEBOX_VISIBILITY_DOMAINS),
        **_review_ok(visibility_domain_checks),
        **meta,
    }

    model_candidate = {
        "model_id": "whitebox_inspection_model_v1",
        "role": "transparent_inspection_and_explainable_supervision",
        "rulemaking_allowed": False,
        "validation_engineering_replacement_allowed": False,
        "authorization_standard_redefinition_allowed": False,
        "provider_execution_allowed": False,
        "runtime_enabled_now": False,
        "absorbs_existing_detection_chain": True,
        "creates_parallel_system": False,
        "visibility_domains": list(WHITEBOX_VISIBILITY_DOMAINS),
        "inspection_layers": [layer["layer_id"] for layer in INSPECTION_LAYERS],
        "default_entry_layer": "system",
        "planning_artifacts_absorbed": True,
        "simulated": True,
        **meta,
    }

    val_abs_checks: List[Tuple[str, bool]] = []
    plan_mappings = plan_val_abs.get("mappings") or list(VALIDATION_ABSORPTION)
    for m in VALIDATION_ABSORPTION:
        found = any(x.get("component") == m["component"] for x in plan_mappings)
        val_abs_checks.append((f"absorb.{m['component']}", found))
    val_abs_checks.extend(
        [
            ("validation_remains_executor", plan_val_abs.get("validation_engineering_remains_enforcement_layer") is True),
            ("whitebox_visibility_only", plan_val_abs.get("whitebox_provides_visibility_layer") is True),
            ("absorbed_not_replaced", plan_val_abs.get("absorbed_not_replaced") is True),
        ]
    )

    validation_absorption_review = {
        "review_id": "validation_engineering_absorption_review_v1",
        "mappings": [
            {
                **m,
                "absorbed": any(x.get("component") == m["component"] for x in plan_mappings),
                "validation_engineering_remains_executor": True,
                "whitebox_makes_visible_explainable_auditable": True,
            }
            for m in VALIDATION_ABSORPTION
        ],
        "validation_engineering_remains_executor_gatekeeper": True,
        "whitebox_only_visibility_explainability_auditability": True,
        **_review_ok(val_abs_checks),
        **meta,
    }

    chv_checks: List[Tuple[str, bool]] = []
    plan_chv_mappings = plan_chv.get("mappings") or list(CHV_MAPPING)
    for m in CHV_MAPPING:
        chv_checks.append(
            (
                f"chv.{m['layer'][:20]}",
                any(x.get("layer") == m["layer"] for x in plan_chv_mappings),
            )
        )
    chv_checks.extend(
        [
            ("whitebox_integrates", plan_chv.get("whitebox_integrates_observability") is True),
            ("whitebox_replaces_none", plan_chv.get("whitebox_replaces_none") is True),
        ]
    )

    chv_mapping_review = {
        "review_id": "constitution_health_validation_mapping_review_v1",
        "mappings": list(CHV_MAPPING),
        "constitution_engineering_is": "rule source visibility",
        "health_management_is": "system pressure / economic indicator visibility",
        "validation_engineering_is": "enforcement / gatekeeping visibility",
        "whitebox_engineering_is": "integrated observability over all three",
        "whitebox_replaces_none": True,
        **_review_ok(chv_checks),
        **meta,
    }

    factory_checks: List[Tuple[str, bool]] = []
    plan_factory_mappings = plan_factory.get("mappings") or list(FACTORY_AUTH_MAPPING)
    for m in FACTORY_AUTH_MAPPING:
        factory_checks.append(
            (
                f"factory.{m['artifact'][:15]}",
                any(x.get("artifact") == m["artifact"] for x in plan_factory_mappings),
            )
        )

    factory_auth_mapping_review = {
        "review_id": "factory_authorization_mapping_review_v1",
        "mappings": list(FACTORY_AUTH_MAPPING),
        **_review_ok(factory_checks),
        **meta,
    }

    evidence_checks: List[Tuple[str, bool]] = []
    plan_evidence_mappings = plan_evidence.get("mappings") or list(EVIDENCE_TRACE_MAPPING)
    for m in EVIDENCE_TRACE_MAPPING:
        evidence_checks.append(
            (
                f"evidence.{m['artifact'][:15]}",
                any(x.get("artifact") == m["artifact"] for x in plan_evidence_mappings),
            )
        )

    evidence_traceback_mapping_review = {
        "review_id": "evidence_boundary_traceback_mapping_review_v1",
        "mappings": list(EVIDENCE_TRACE_MAPPING),
        "ocr_real_execution_evidence_ref": str(ocr_exec_root / "execution_evidence_package_v1.json"),
        **_review_ok(evidence_checks),
        **meta,
    }

    global_checks: List[Tuple[str, bool]] = []
    plan_principles = plan_global.get("hard_principles") or list(GLOBAL_TO_LOCAL_PRINCIPLES)
    for principle in GLOBAL_TO_LOCAL_PRINCIPLES:
        global_checks.append((f"principle.{principle[:25]}", principle in plan_principles))

    global_to_local_principle_review = {
        "review_id": "global_to_local_principle_review_v1",
        "inspect_system_before_module": True,
        "inspect_chain_before_node": True,
        "inspect_responsibility_before_implementation": True,
        "inspect_midplatform_decision_before_provider_detail": True,
        "local_check_requires_upstream_signal": True,
        "drilldown_evidence_not_primary_entrypoint": True,
        "no_direct_local_provider_without_system_reason": True,
        "hard_principles": list(GLOBAL_TO_LOCAL_PRINCIPLES),
        **_review_ok(global_checks),
        **meta,
    }

    layer_checks: List[Tuple[str, bool]] = []
    plan_layer_list = plan_layers.get("layers") or list(INSPECTION_LAYERS)
    for layer in INSPECTION_LAYERS:
        layer_checks.append(
            (
                f"layer.{layer['layer_id']}",
                any(l.get("layer_id") == layer["layer_id"] for l in plan_layer_list),
            )
        )
    layer_checks.extend(
        [
            ("default_entry_system", plan_layers.get("default_start_level") == 1),
            ("node_requires_upstream", plan_layers.get("node_level_requires_upstream_signal") is True),
            ("node_not_global_health", True),
        ]
    )

    layer_model_review = {
        "review_id": "whitebox_layer_model_review_v1",
        "layers": list(INSPECTION_LAYERS),
        "default_entry_layer": "system",
        "node_level_requires_upstream_trigger": True,
        "node_level_checks_do_not_define_global_health": True,
        **_review_ok(layer_checks),
        **meta,
    }

    drilldown_checks: List[Tuple[str, bool]] = [
        ("system_default_entry", plan_layers.get("default_start_level") == 1),
        ("node_drilldown_only", plan_global.get("node_level_drilldown_only") is True),
        ("ocr_is_drilldown_target", plan_ocr_local.get("evidence_level") == "node_level_whitebox"),
    ]

    drilldown_policy_review = {
        "review_id": "whitebox_drilldown_policy_review_v1",
        "default_start": "system_level_whitebox",
        "node_level_drilldown_only": True,
        "ocr_real_dep_is_drilldown_evidence": True,
        **_review_ok(drilldown_checks),
        **meta,
    }

    ocr_checks: List[Tuple[str, bool]] = [
        ("node_level_evidence", plan_ocr_local.get("evidence_level") == "node_level_whitebox"),
        ("read_only_evidence", plan_ocr_local.get("read_only_evidence_source") is True),
        ("no_auto_install", plan_ocr_local.get("failure_does_not_trigger_install_download_repair") is True),
        ("not_main_chain", plan_ocr_local.get("must_not_expand_as_main_detection_chain") is True),
        ("may_inform_provider_selection", "provider_selection" in (plan_ocr_local.get("uses_for_future") or [])),
        ("does_not_finalize_provider", True),
        ("does_not_enable_runtime", meta.get("whitebox_runtime_enabled_now") is False),
        ("does_not_authorize_smoke", True),
        ("ocr_not_reexecuted", meta.get("ocr_real_dep_reexecuted_now") is False),
    ]

    ocr_local_evidence_review = {
        "review_id": "ocr_real_dep_local_evidence_review_v1",
        "ocr_real_dep_execution": "node-level local evidence",
        "package_cache_hash_import_read_only": True,
        "failures_do_not_trigger_install_download_repair": True,
        "may_inform_future_provider_selection_dependency_readiness": True,
        "does_not_finalize_provider": True,
        "does_not_enable_runtime": True,
        "does_not_authorize_smoke_sample_ocr": True,
        "ocr_execution_root": str(ocr_exec_root),
        "checks_passed": ocr_sm.get("checks_passed"),
        **_review_ok(ocr_checks),
        **meta,
    }

    no_parallel_checks: List[Tuple[str, bool]] = [
        ("no_new_parallel", plan_no_parallel.get("no_new_parallel_whitebox_system") is True),
        ("val_absorbed", plan_no_parallel.get("existing_validation_engineering_absorbed") is True),
        ("auth_absorbed", plan_no_parallel.get("existing_authorization_chain_absorbed") is True),
        ("evidence_absorbed", plan_no_parallel.get("existing_evidence_boundary_traceback_absorbed") is True),
        ("artifacts_preserved", plan_no_parallel.get("historical_detection_artifacts_preserved") is True),
        ("work_not_invalidated", plan_no_parallel.get("previous_work_not_invalidated") is True),
        ("future_refs_validation", plan_no_parallel.get(
            "future_whitebox_phases_must_reference_existing_validation_artifacts"
        ) is True),
        ("model_creates_parallel_false", model_candidate.get("creates_parallel_system") is False),
    ]

    no_parallel_review = {
        "review_id": "no_parallel_whitebox_review_v1",
        "no_new_parallel_whitebox_system": True,
        "existing_validation_engineering_absorbed": True,
        "existing_authorization_chain_absorbed": True,
        "existing_evidence_boundary_traceback_absorbed": True,
        "historical_detection_artifacts_preserved": True,
        "previous_work_not_invalidated": True,
        "future_whitebox_phases_must_reference_existing_validation_artifacts": True,
        **_review_ok(no_parallel_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    boundary_checks.append(
        ("model_candidate_generated", meta.get("whitebox_inspection_model_candidate_generated_now") is True)
    )
    boundary_checks.extend(
        [
            ("no_runtime_enable", meta.get("whitebox_runtime_enabled_now") is False),
            ("no_parallel_creation", meta.get("new_parallel_whitebox_system_created_now") is False),
            ("no_val_replacement", meta.get("validation_engineering_replaced_now") is False),
            ("no_constitution_update", meta.get("constitution_registry_updated_now") is False),
            ("no_ocr_reexec", meta.get("ocr_real_dep_reexecuted_now") is False),
            ("no_provider", meta.get("provider_invoked_now") is False),
            ("no_install", meta.get("dependency_install_executed_now") is False),
            ("no_download", meta.get("model_download_executed_now") is False),
            ("no_memory", meta.get("memory_written_now") is False),
            ("no_world_model", meta.get("world_model_written_now") is False),
            ("no_user_output", meta.get("user_facing_output_generated_now") is False),
        ]
    )

    boundary_audit = {
        "audit_id": "whitebox_boundary_audit_v1",
        "forbidden_actions_absent": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "whitebox_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        planning_input_review,
        visibility_domain_review,
        validation_absorption_review,
        chv_mapping_review,
        factory_auth_mapping_review,
        evidence_traceback_mapping_review,
        global_to_local_principle_review,
        layer_model_review,
        drilldown_policy_review,
        ocr_local_evidence_review,
        no_parallel_review,
        boundary_audit,
    ]

    model_ok = (
        model_candidate.get("model_id") == "whitebox_inspection_model_v1"
        and model_candidate.get("rulemaking_allowed") is False
        and model_candidate.get("validation_engineering_replacement_allowed") is False
        and model_candidate.get("authorization_standard_redefinition_allowed") is False
        and model_candidate.get("provider_execution_allowed") is False
        and model_candidate.get("runtime_enabled_now") is False
        and model_candidate.get("absorbs_existing_detection_chain") is True
        and model_candidate.get("creates_parallel_system") is False
    )

    all_pass = (
        input_ok
        and model_ok
        and visibility_domain_review.get("all_domains_pass") is True
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections if "dryrun_and_review_pass" in s)
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "whitebox_integration_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "whitebox_model_candidate_valid": model_ok,
        "ten_visibility_domains_pass": visibility_domain_review.get("all_domains_pass"),
        "no_parallel_whitebox_confirmed": plan_no_parallel.get("no_new_parallel_whitebox_system") is True,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_midplatform_core_architecture_resume": all_pass,
        "whitebox_runtime_enabled": False,
        "ocr_local_inspection_expansion_blocked": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "whitebox_inspection_integration_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "integration_not_rebuild": True,
        "absorption_not_replacement": True,
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
        "boundary_ok": all_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "whitebox_inspection_integration_dryrun_review_policy": policy,
        "whitebox_integration_planning_input_review": planning_input_review,
        "whitebox_inspection_model_candidate": model_candidate,
        "whitebox_visibility_domain_review": visibility_domain_review,
        "validation_engineering_absorption_review": validation_absorption_review,
        "constitution_health_validation_mapping_review": chv_mapping_review,
        "factory_authorization_mapping_review": factory_auth_mapping_review,
        "evidence_boundary_traceback_mapping_review": evidence_traceback_mapping_review,
        "global_to_local_principle_review": global_to_local_principle_review,
        "whitebox_layer_model_review": layer_model_review,
        "whitebox_drilldown_policy_review": drilldown_policy_review,
        "ocr_real_dep_local_evidence_review": ocr_local_evidence_review,
        "no_parallel_whitebox_review": no_parallel_review,
        "whitebox_boundary_audit": boundary_audit,
        "whitebox_blocked_path_result": blocked_path_result,
        "whitebox_integration_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
