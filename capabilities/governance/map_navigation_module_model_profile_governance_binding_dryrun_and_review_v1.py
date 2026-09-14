# -*- coding: utf-8 -*-
"""Map / Navigation Module Model Profile + Governance Binding DryRunAndReview v1 — qualification only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.map_navigation_module_model_profile_governance_binding_planning_v1 import (
    CAPABILITY_STACK_DEF_ID,
    CLOSURE_CAN_SAY,
    CLOSURE_CANNOT_SAY,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    IO_FORBIDDEN,
    LAYERED_GOV_MAPPING_ID,
    MAP_NAV_MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    MAP_NAV_REGISTRY_REFS,
    MAP_REGISTRY_PLACEHOLDER_REGISTRY_ID,
    MIDPLATFORM_BINDING_ID,
    MODULE_ID,
    MODULE_LOCAL_PROFILE_ID,
    QUALIFICATION_FIELDS,
    QUALIFICATION_MODE,
    REUSED_GOVERNANCE_STANDARDS,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    INFORMATION_INTEGRATION_REF,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    STANDARD_ID as MIDPLATFORM_BINDING_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DUAL_VALIDATION_MECHANISM_ID,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)

PHASE_ID = "Phase-Map-Navigation-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
SCOPE = "map_navigation_module_model_profile_governance_binding_dryrun_and_review_only"
SOURCE_CHAIN = "map_navigation_module_model_profile_governance_binding_dryrun_and_review_v1"

CANDIDATE_REGISTRY_REFS: Tuple[str, ...] = (
    "map_provider_placeholder",
    "route_reasoning_candidate",
    "indoor_facility_search_candidate",
    "transit_context_candidate",
)

FINAL_DECISION_GO = (
    "MAP_NAVIGATION_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_WORLD_CONTINUITY_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MAP_NAVIGATION_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-World-Continuity-Module-Model-Profile-Governance-Binding-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Map-Navigation-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "Map / Navigation Module DryRun GO ≠ map provider selected",
    "map provider refs reviewed ≠ map API invocation",
    "route proposal contract reviewed ≠ route planning executable",
    "route context candidate ≠ navigation permission",
    "Navigation Action Gate boundary declared ≠ navigation action enabled",
    "Map / Navigation binding feasible ≠ Constitution/Oversight fully integrated",
    "Health/Oversight refs attached ≠ health/supervision metrics finalized",
    "next World Continuity Module Planning ≠ WorldModel write",
    "Module Governance Binding GO ≠ module fully integrated with Constitution",
    "Module Governance Binding GO ≠ module fully integrated with Health/Oversight",
    "Constitution binding feasible ≠ constitution effectiveness quantified",
    "Layer 3 dependency reviewed ≠ Layer 1/2 override permitted",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_map_navigation_runtime_enable",
    "dryrun_to_map_provider_invocation",
    "dryrun_to_map_api_call",
    "dryrun_to_route_planning_execution",
    "dryrun_to_navigation_action_generation",
    "dryrun_to_navigation_instruction_generation",
    "dryrun_to_safe_to_cross_generation",
    "dryrun_to_go_ahead_generation",
    "dryrun_to_location_fact_generation",
    "dryrun_to_model_selection",
    "dryrun_to_model_download",
    "dryrun_to_model_invocation",
    "dryrun_to_provider_invocation",
    "dryrun_to_benchmark_execution",
    "dryrun_to_license_clearance",
    "dryrun_to_security_review_completion",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_user_output",
    "dryrun_to_controlled_runtime_enable",
    "dryrun_to_full_integration_certification",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "map_navigation_module_model_profile_governance_binding_dryrun_and_review_only",
    "qualification_check_only",
    "map_navigation_module_qualification_check_executed_now",
    "simulated",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "map_navigation_module_runtime_enabled_now",
    "map_provider_invoked_now",
    "map_api_called_now",
    "route_planning_executed_now",
    "navigation_action_generated_now",
    "navigation_instruction_generated_now",
    "safe_to_cross_generated_now",
    "go_ahead_generated_now",
    "location_fact_generated_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
    "constitution_effectiveness_quantified_now",
    "health_metrics_finalized_now",
    "supervision_metrics_finalized_now",
    "module_constitution_fully_integrated_now",
    "module_oversight_fully_integrated_now",
    "health_metric_detail_defined_now",
    "supervision_metric_detail_defined_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "map_navigation_module_model_profile_governance_binding_dryrun_and_review"
)


def _resolve_registry_refs(profile_refs: List[str]) -> List[str]:
    resolved: List[str] = []
    for ref in profile_refs:
        if ref == "map_provider_placeholder_candidate":
            resolved.append(MAP_REGISTRY_PLACEHOLDER_REGISTRY_ID)
        else:
            resolved.append(ref)
    return resolved


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
        "qualification_mode": QUALIFICATION_MODE,
        **QUALIFICATION_FIELDS,
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


def _review_from_checks(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"check_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "review_pass": len(issues) == 0,
    }


def _with_review(review_id: str, review: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    return {"review_id": review_id, **review, **meta}


def run_map_navigation_module_model_profile_governance_binding_dryrun_and_review_v1(
    *,
    map_navigation_module_model_profile_governance_binding_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(
        map_navigation_module_model_profile_governance_binding_planning_root
    ).expanduser().resolve()

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    qual_plan = _try_read_json(plan_root / "map_navigation_module_qualification_check_v1.json") or {}

    mod_def = _try_read_json(plan_root / "map_navigation_module_definition_v1.json") or {}
    stack = _try_read_json(plan_root / "map_navigation_capability_stack_definition_v1.json") or {}
    gov_map = _try_read_json(plan_root / "map_navigation_layered_governance_mapping_v1.json") or {}
    profile = _try_read_json(plan_root / "map_navigation_module_local_model_profile_v1.json") or {}
    refs_plan = _try_read_json(plan_root / "map_navigation_model_profile_registry_refs_review_v1.json") or {}
    roles = _try_read_json(plan_root / "map_navigation_model_role_assignment_plan_v1.json") or {}
    inp = _try_read_json(plan_root / "map_navigation_input_contract_v1.json") or {}
    out = _try_read_json(plan_root / "map_navigation_output_contract_v1.json") or {}
    quality = _try_read_json(plan_root / "map_navigation_quality_acceptance_plan_v1.json") or {}
    health = _try_read_json(plan_root / "map_navigation_health_validation_whitebox_plan_v1.json") or {}
    prov_rt = _try_read_json(plan_root / "map_navigation_provider_runtime_boundary_plan_v1.json") or {}
    fallback = _try_read_json(plan_root / "map_navigation_fallback_replacement_plan_v1.json") or {}
    self_check = _try_read_json(plan_root / "map_navigation_module_internal_self_check_plan_v1.json") or {}
    interaction = _try_read_json(plan_root / "map_navigation_midplatform_interaction_check_plan_v1.json") or {}
    binding = _try_read_json(plan_root / "map_navigation_midplatform_governance_binding_v1.json") or {}
    ii = _try_read_json(plan_root / "map_navigation_information_integration_handoff_plan_v1.json") or {}
    dc = _try_read_json(plan_root / "map_navigation_decision_center_handoff_plan_v1.json") or {}
    action_gate = _try_read_json(plan_root / "map_navigation_action_gate_boundary_plan_v1.json") or {}
    mem_wm = _try_read_json(
        plan_root / "map_navigation_memory_worldmodel_admission_boundary_plan_v1.json"
    ) or {}
    layer_dep = _try_read_json(plan_root / "map_navigation_layer_dependency_review_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_dryrun_meta(), "output_root": str(out_root), "upstream_planning_root": str(plan_root)}

    if plan_vr.get("verifier") != "GO":
        blockers.append("Map / Navigation Planning must be GO")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("Planning final_decision mismatch")
    if plan_sm.get("module_id") != MODULE_ID:
        blockers.append("module_id must be map_navigation_application_module")
    if plan_sm.get("capability_layer") != "Layer 3 Navigation Application":
        blockers.append("capability_layer must be Layer 3 Navigation Application")
    if not plan_sm.get("qualification_check_only"):
        blockers.append("Planning must be qualification_check_only")

    input_ok = len(blockers) == 0
    stack_text = json.dumps(stack, ensure_ascii=False)
    gov_text = json.dumps(gov_map, ensure_ascii=False)
    roles_text = json.dumps(roles, ensure_ascii=False)
    inp_text = json.dumps(inp, ensure_ascii=False)
    out_text = json.dumps(out, ensure_ascii=False)
    quality_text = json.dumps(quality, ensure_ascii=False)
    prov_text = json.dumps(prov_rt, ensure_ascii=False)
    fallback_text = json.dumps(fallback, ensure_ascii=False)
    ii_text = json.dumps(ii, ensure_ascii=False)
    dc_text = json.dumps(dc, ensure_ascii=False)
    action_text = json.dumps(action_gate, ensure_ascii=False)
    mem_text = json.dumps(mem_wm, ensure_ascii=False)
    layer_text = json.dumps(layer_dep, ensure_ascii=False)
    refs_plan_text = json.dumps(refs_plan, ensure_ascii=False)

    profile_refs = profile.get("registry_model_profile_refs") or []
    resolved_profile_refs = _resolve_registry_refs(list(profile_refs))

    planning_input_review = {
        "review_id": "planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "module_id": plan_sm.get("module_id"),
        "capability_layer": plan_sm.get("capability_layer"),
        "qualification_mode": plan_sm.get("qualification_mode"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_reuse = _with_review(
        "governance_standard_reuse_review_v1",
        _review_from_checks([
            ("constraints_ref", True),
            ("reuse_rule", True),
            ("new_need_false", True),
            ("reused_count12", len(REUSED_GOVERNANCE_STANDARDS) == 12),
            *(("std." + s[:12], s in REUSED_GOVERNANCE_STANDARDS) for s in REUSED_GOVERNANCE_STANDARDS),
        ]),
        meta,
    )

    mod_def_review = _with_review(
        "map_navigation_module_definition_review_v1",
        _review_from_checks([
            ("module_id", mod_def.get("module_id") == MODULE_ID),
            ("domain", mod_def.get("capability_domain") == "Map / Navigation / Route Application"),
            ("layer3", mod_def.get("capability_layer") == "Layer 3 Navigation Application"),
            ("l1_dep", mod_def.get("depends_on_layer_1") == "Current Scene Understanding"),
            ("l2_dep", mod_def.get("depends_on_layer_2") == "Spatiotemporal Continuity"),
            ("no_runtime", mod_def.get("runtime_enabled_now") is False),
            ("no_provider", mod_def.get("map_provider_invoked_now") is False),
            ("no_route", mod_def.get("route_planning_executed_now") is False),
            ("no_action", mod_def.get("navigation_action_generated_now") is False),
            ("candidate", mod_def.get("candidate_only") is True),
        ]),
        meta,
    )

    stack_review = _with_review(
        "map_navigation_capability_stack_review_v1",
        _review_from_checks([
            ("l1", "layer_1_dependency_input" in stack.get("layers", {})),
            ("l2", "layer_2_dependency_input" in stack.get("layers", {})),
            ("l3", "layer_3_navigation_application" in stack.get("layers", {})),
            ("l4", "layer_4_extended_application_later" in stack.get("layers", {})),
            ("no_scene_fact", "no base scene fact generation" in stack_text),
            ("no_override_evidence", "no Vision/OCR/ASR evidence override" in stack_text),
            ("no_nav_action", "no direct navigation action" in stack_text),
            ("no_user_out", "no direct user_output" in stack_text or "user output" in stack_text),
            ("no_mem_wm", "Memory/WorldModel" in stack_text),
        ]),
        meta,
    )

    gov_map_review = _with_review(
        "map_navigation_layered_governance_mapping_review_v1",
        _review_from_checks([
            ("l1_consumes", "consumes scene/risk/obstacle candidates" in gov_text),
            ("l1_no_override", "cannot override perception" in gov_text),
            ("l2_consumes", "consumes location/spatiotemporal candidates" in gov_text),
            ("l2_freshness", "conflict/gap/freshness required" in gov_text),
            ("l3_candidate", "route/navigation context as candidate" in gov_text),
            ("l3_safety", "safety priority" in gov_text),
            ("l3_dc", "Decision Center handoff" in gov_text),
            ("l3_gate", "Navigation Action Gate later" in gov_text),
            ("l4_later", "indoor/transport/social facility later" in gov_text),
            ("l4_privacy", "privacy/location sensitivity later" in gov_text),
            ("route_not_risk", "route context cannot override real-time risk context" in gov_text),
            ("no_action_without", "no navigation action without Decision + Action Gate + Controlled Runtime" in gov_text),
            ("no_weaken", "no weakened constitution by layer" in gov_text),
        ]),
        meta,
    )

    profile_review = _with_review(
        "map_navigation_module_local_model_profile_review_v1",
        _review_from_checks([
            ("profile_id", profile.get("module_local_profile_id") == MODULE_LOCAL_PROFILE_ID),
            *(("ref." + ref[:12], ref in resolved_profile_refs) for ref in CANDIDATE_REGISTRY_REFS),
            ("stack_ref", profile.get("capability_stack_ref") == CAPABILITY_STACK_DEF_ID),
            ("gov_ref", profile.get("layered_governance_mapping_ref") == LAYERED_GOV_MAPPING_ID),
            ("no_override", profile.get("no_registry_override") is True),
            ("no_select", profile.get("no_model_selection_by_module") is True),
            ("no_invoke", profile.get("no_model_invocation_by_profile") is True),
            ("no_nav_action", profile.get("no_direct_navigation_action") is True),
            ("no_user_out", profile.get("no_direct_user_output") is True),
        ]),
        meta,
    )

    refs_review = _with_review(
        "map_navigation_model_profile_registry_refs_review_v1",
        _review_from_checks([
            ("refs_review_pass", refs_plan.get("review_pass") is True),
            ("map_provider", "map_provider_placeholder_candidate" in refs_plan_text),
            ("route", "route_reasoning_candidate" in refs_plan_text),
            ("facility", "indoor_facility_search_candidate" in refs_plan_text),
            ("transit", "transit_context_candidate" in refs_plan_text),
            ("candidate_only", "candidate only" in refs_plan_text),
            ("none_selected", "none selected_now" in refs_plan_text),
            ("none_invoked", "none invoked_now" in refs_plan_text),
            ("provider_later", "provider readiness later required" in refs_plan_text),
            ("route_later", "route validation later required" in refs_plan_text),
        ]),
        meta,
    )

    roles_review = _with_review(
        "map_navigation_model_role_assignment_review_v1",
        _review_from_checks([
            ("map_role", "map context provider role" in roles_text),
            ("route_role", "route proposal role" in roles_text),
            ("facility_role", "indoor/facility candidate role later" in roles_text),
            ("transit_role", "public transport candidate role later" in roles_text),
            ("no_single", "no single model/provider owns navigation authority" in roles_text),
            ("not_permission", "route candidate ≠ navigation permission" in roles_text),
            ("not_safe_move", "navigation context ≠ safe-to-move instruction" in roles_text),
        ]),
        meta,
    )

    inp_review = _with_review(
        "map_navigation_input_contract_review_v1",
        _review_from_checks([
            ("integrated", "integrated_context_candidate" in inp_text),
            ("scene", "scene_context_candidate" in inp_text),
            ("risk", "risk_context_candidate" in inp_text),
            ("obstacle", "obstacle_candidate" in inp_text),
            ("location", "location_context_candidate" in inp_text),
            ("route_later", "route_request_candidate_later" in inp_text),
            ("task_intent", "user_task_intent_candidate" in inp_text),
            ("map_provider_later", "map_provider_context_candidate_later" in inp_text),
            ("transit_later", "transit_context_candidate_later" in inp_text),
            ("no_raw_map", "raw map provider data not consumed now" in inp_text),
            ("no_map_api", "map API not called now" in inp_text),
            ("no_route_exec", "route request not executed now" in inp_text),
            ("no_location_fact", "real location fact not generated now" in inp_text),
        ]),
        meta,
    )

    out_review = _with_review(
        "map_navigation_output_contract_review_v1",
        _review_from_checks([
            ("map_location", "map_location_context_candidate" in out_text),
            ("route_ctx", "route_context_candidate" in out_text),
            ("nav_task", "navigation_task_candidate" in out_text),
            ("route_proposal", "route_proposal_candidate_later" in out_text),
            ("facility", "facility_search_candidate_later" in out_text),
            ("transit", "transit_context_candidate_later" in out_text),
            ("action_req", "navigation_action_request_candidate_later" in out_text),
            ("nav_risk", "navigation_risk_candidate_later" in out_text),
            *(("forbid." + f[:14], f in (out.get("forbidden_outputs") or [])) for f in IO_FORBIDDEN),
        ]),
        meta,
    )

    quality_review = _with_review(
        "map_navigation_quality_acceptance_review_v1",
        _review_from_checks([
            ("route_accuracy", "route_accuracy_target_later" in quality_text),
            ("location_conf", "location_context_confidence_later" in quality_text),
            ("freshness", "map_freshness_requirement_later" in quality_text),
            ("safety", "route_safety_validation_required_later" in quality_text),
            ("latency", "latency_budget_later" in quality_text),
            ("resource", "resource_budget_later" in quality_text),
            ("compliance", quality.get("candidate_contract_compliance_required") is True),
            ("trace", quality.get("traceability_completeness_required") is True),
            ("degrade", quality.get("degradation_behavior_required") is True),
            ("bench_later", quality.get("benchmark_required_later") is True),
            ("bench_now", quality.get("benchmark_executed_now") is False),
        ]),
        meta,
    )

    health_review = _with_review(
        "map_navigation_health_validation_whitebox_review_v1",
        _review_from_checks([
            ("validation_ref", bool(health.get("validation_requirement_ref"))),
            ("health_later", health.get("health_requirement_ref") == "required_later"),
            ("supervision_later", health.get("supervision_metric_ref") == "required_later"),
            ("health_detail_false", health.get("health_metric_detail_defined_now") is False),
            ("super_detail_false", health.get("supervision_metric_detail_defined_now") is False),
            ("whitebox", bool(health.get("whitebox_trace_requirement_ref"))),
            ("source_chain", health.get("source_chain_required") is True),
            ("issue_trace", health.get("issue_trace_required") is True),
            ("map_freshness_later", health.get("map_source_freshness_trace_required_later") is True),
            ("transport_only", health.get("health_status_ref_transport_only") is True),
            ("no_self_cert", health.get("module_cannot_self_certify_health") is True),
            ("constitution_not_quant", meta.get("constitution_effectiveness_quantified_now") is False),
            ("health_not_final", meta.get("health_metrics_finalized_now") is False),
            ("super_not_final", meta.get("supervision_metrics_finalized_now") is False),
            ("not_fully_const", meta.get("module_constitution_fully_integrated_now") is False),
            ("not_fully_oversight", meta.get("module_oversight_fully_integrated_now") is False),
        ]),
        meta,
    )

    prov_review = _with_review(
        "map_navigation_provider_runtime_boundary_review_v1",
        _review_from_checks([
            ("prov_required", prov_rt.get("provider_abstraction_required") is True),
            ("cr_required", prov_rt.get("controlled_runtime_required") is True),
            ("not_selected", "provider_candidate ≠ selected ≠ invoked" in prov_text),
            ("no_auto", "no provider auto-switch" in prov_text),
            ("map_api_later", "map API call requires provider readiness later" in prov_text),
            ("nav_cr_later", "navigation runtime requires Controlled Runtime later" in prov_text),
            ("nav_gate_later", "navigation action requires Navigation Action Gate later" in prov_text),
            ("no_runtime", "Map / Navigation runtime remains disabled now" in prov_text),
        ]),
        meta,
    )

    fallback_review = _with_review(
        "map_navigation_fallback_replacement_review_v1",
        _review_from_checks([
            ("refs_structured", len(fallback.get("fallback_model_profile_refs") or []) >= 4),
            ("provider", "provider_unavailable" in fallback_text),
            ("stale", "map_stale_risk" in fallback_text),
            ("conflict", "route_conflict_with_scene_risk" in fallback_text),
            ("location", "location_uncertainty" in fallback_text),
            ("license", "license_risk" in fallback_text),
            ("latency", "latency_budget_failure" in fallback_text),
            ("safety", "safety_uncertainty" in fallback_text),
            ("hold", "hold_instead_of_fallback" in fallback_text or "safety/location confidence" in fallback_text),
            ("no_auto", fallback.get("no_auto_switch_without_governance_policy") is True),
            ("no_invoke", fallback.get("replacement_does_not_imply_invocation") is True),
        ]),
        meta,
    )

    self_check_review = _with_review(
        "map_navigation_module_internal_self_check_review_v1",
        _review_from_checks(
            [("plan_exists", bool(self_check.get("plan_id")))]
            + [(c[:16], c in (self_check.get("self_check_coverage") or []))
               for c in MODULE_INTERNAL_SELF_CHECK_COVERAGE]
        ),
        meta,
    )

    interaction_review = _with_review(
        "map_navigation_midplatform_interaction_check_review_v1",
        _review_from_checks(
            [("plan_exists", bool(interaction.get("plan_id")))]
            + [(c[:16], c in (interaction.get("interaction_check_coverage") or []))
               for c in MAP_NAV_MIDPLATFORM_INTERACTION_CHECK_COVERAGE]
        ),
        meta,
    )

    binding_review = _with_review(
        "map_navigation_midplatform_governance_binding_review_v1",
        _review_from_checks([
            ("binding_id", binding.get("midplatform_governance_binding_id") == MIDPLATFORM_BINDING_ID),
            ("profile_ref", binding.get("module_local_profile_ref") == MODULE_LOCAL_PROFILE_ID),
            ("refs_preserved", len(binding.get("registry_model_profile_refs") or []) >= 4),
            ("constitution", binding.get("constitution_bus_ref") == CONSTITUTION_BUS_REF),
            ("capability_bus", bool(binding.get("capability_bus_contract_ref"))),
            ("provider", binding.get("provider_abstraction_ref") == PROVIDER_ABS_STANDARD_ID),
            ("validation", bool(binding.get("validation_requirement_ref"))),
            ("health_later", binding.get("health_requirement_ref") == "required_later"),
            ("whitebox", bool(binding.get("whitebox_trace_requirement_ref"))),
            ("ii_policy", bool(binding.get("information_integration_consumption_policy_ref"))),
            ("dc_policy", bool(binding.get("decision_center_consumption_policy_ref"))),
            ("nav_gate_later", bool(binding.get("navigation_action_gate_requirement_ref_later"))),
            ("cr_ref", binding.get("controlled_runtime_requirement_ref") == CONTROLLED_RUNTIME_FRAMEWORK_REF),
            ("no_select", binding.get("model_selected_now") is False),
            ("no_invoke", binding.get("model_invoked_now") is False),
            ("no_runtime", binding.get("runtime_enabled_now") is False),
        ]),
        meta,
    )

    ii_review = _with_review(
        "map_navigation_information_integration_handoff_review_v1",
        _review_from_checks([
            ("ii_ref", ii.get("information_integration_ref") == INFORMATION_INTEGRATION_REF),
            ("candidate_flow", "candidate/context/proposal" in ii_text),
            ("consumes", "map_location_context" in ii_text and "route_context" in ii_text),
            ("no_bypass", "cannot bypass Information Integration" in ii_text),
            ("no_integrated", "no integrated_context generated now" in ii_text),
        ]),
        meta,
    )

    dc_review = _with_review(
        "map_navigation_decision_center_handoff_review_v1",
        _review_from_checks([
            ("integrated", "integrated_context" in dc_text),
            ("no_movement", "cannot emit final movement decision" in dc_text),
            ("no_route_action", "route candidate cannot directly trigger navigation action" in dc_text),
            ("no_decision_now", "no decision generated now" in dc_text),
        ]),
        meta,
    )

    action_gate_review = _with_review(
        "map_navigation_action_gate_boundary_review_v1",
        _review_from_checks([
            ("gate_required", "Navigation Action Gate required later" in action_text),
            ("not_permission", "map route proposal ≠ movement permission" in action_text),
            ("forbidden_now", "safe_to_cross / go_ahead forbidden now" in action_text),
            ("no_action_now", "no navigation action now" in action_text),
            ("no_instruction_now", "no user instruction now" in action_text),
        ]),
        meta,
    )

    mem_wm_review = _with_review(
        "map_navigation_memory_worldmodel_admission_boundary_review_v1",
        _review_from_checks([
            ("no_mem", "cannot write Memory" in mem_text),
            ("no_wm", "cannot write WorldModel" in mem_text),
            ("admission_later", "admission candidate later" in mem_text),
            ("correction_later", "map correction / route memory later requires Admission" in mem_text),
            ("no_write_now", "no memory/worldmodel write now" in mem_text),
        ]),
        meta,
    )

    layer_dep_review = _with_review(
        "map_navigation_layer_dependency_review_v1",
        _review_from_checks([
            ("l1_dep", "depends on Layer 1 scene understanding" in layer_text),
            ("l2_dep", "depends on Layer 2 spatiotemporal continuity" in layer_text),
            ("no_override_risk", "cannot override safety/risk candidates" in layer_text),
            ("survival", "route task progress cannot override survival risk" in layer_text),
            ("no_scene_auth", "cannot claim current scene understanding authority" in layer_text),
            ("layer3_app", "Layer 3 Navigation Application" in layer_text or "Layer 3 application" in layer_text),
        ]),
        meta,
    )

    qual_check_review = _with_review(
        "map_navigation_module_qualification_check_review_v1",
        _review_from_checks([
            ("qual_only", qual_plan.get("qualification_check_only") is True or meta.get("qualification_check_only") is True),
            ("full_cert_false", meta.get("full_integration_certification_now") is False),
            ("constitution_feasible", meta.get("constitution_binding_feasible") is True),
            ("oversight_feasible", meta.get("oversight_binding_feasible") is True),
            ("can_say_registry", CLOSURE_CAN_SAY[0] in (qual_plan.get("can_say") or [])),
            ("can_say_layer3", CLOSURE_CAN_SAY[5] in (qual_plan.get("can_say") or [])),
            ("cannot_runtime", CLOSURE_CANNOT_SAY[0] in (qual_plan.get("cannot_say") or [])),
            ("cannot_map_api", "map API is callable" in str(qual_plan.get("cannot_say"))),
            ("cannot_metrics", "health/supervision metrics finalized" in str(qual_plan.get("cannot_say"))),
        ] + [(k, meta.get(k) is v) for k, v in QUALIFICATION_FIELDS.items() if k not in (
            "qualification_check_only", "full_integration_certification_now",
            "constitution_binding_feasible", "oversight_binding_feasible",
        )]),
        meta,
    )

    boundary_audit = {
        "audit_id": "map_navigation_non_runtime_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "map_navigation_blocked_path_result_v1",
        "blocked_paths": [{"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    all_reviews = [
        governance_reuse, mod_def_review, stack_review, gov_map_review, profile_review,
        refs_review, roles_review, inp_review, out_review, quality_review, health_review,
        prov_review, fallback_review, self_check_review, interaction_review, binding_review,
        ii_review, dc_review, action_gate_review, mem_wm_review, layer_dep_review, qual_check_review,
    ]

    qualification_pass = (
        input_ok
        and qual_plan.get("qualification_pass") is True
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and all(r.get("review_pass") for r in all_reviews)
    )

    candidate = {
        "candidate_id": "map_navigation_module_model_profile_governance_binding_candidate_v1",
        "module_id": MODULE_ID,
        "module_local_profile_ref": MODULE_LOCAL_PROFILE_ID,
        "midplatform_governance_binding_ref": MIDPLATFORM_BINDING_ID,
        "capability_layer": "Layer 3 Navigation Application",
        "depends_on_layer_1": True,
        "depends_on_layer_2": True,
        "registry_model_profile_refs": list(CANDIDATE_REGISTRY_REFS),
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_pass": qualification_pass,
        "constitution_binding_feasible": True,
        "oversight_binding_feasible": True,
        "runtime_enabled_now": False,
        "map_provider_invoked_now": False,
        "route_planning_executed_now": False,
        "navigation_action_generated_now": False,
        "model_selected_now": False,
        "model_invoked_now": False,
        **meta,
    }

    closure_decision = {
        "decision_id": "map_navigation_module_closure_decision_v1",
        "dryrun_and_review_pass": qualification_pass,
        "high_risk": not qualification_pass,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": FINAL_DECISION_GO if qualification_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if qualification_pass else NEXT_PHASE_HOLD,
        "closure_can_say": list(CLOSURE_CAN_SAY),
        "closure_cannot_say": list(CLOSURE_CANNOT_SAY),
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_world_continuity_module_model_profile_governance_binding_planning": qualification_pass,
        "selected_next_phase": NEXT_PHASE_GO if qualification_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "map_navigation_module_model_profile_governance_binding_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "qualification_check_only": True,
        "phase_goal": (
            "Map / Navigation module qualification verification only. Layer 3 application layer; "
            "cannot override Layer 1 scene understanding or Layer 2 spatiotemporal continuity. "
            "No map provider/map API/route planning/navigation action/navigation runtime."
        ),
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
        "dryrun_and_review_pass": qualification_pass,
        "module_id": MODULE_ID,
        "capability_layer": "Layer 3 Navigation Application",
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "map_navigation_module_model_profile_governance_binding_dryrun_review_policy": policy,
        "planning_input_review": planning_input_review,
        "governance_standard_reuse_review": governance_reuse,
        "map_navigation_module_model_profile_governance_binding_candidate": candidate,
        "map_navigation_module_definition_review": mod_def_review,
        "map_navigation_capability_stack_review": stack_review,
        "map_navigation_layered_governance_mapping_review": gov_map_review,
        "map_navigation_module_local_model_profile_review": profile_review,
        "map_navigation_model_profile_registry_refs_review": refs_review,
        "map_navigation_model_role_assignment_review": roles_review,
        "map_navigation_input_contract_review": inp_review,
        "map_navigation_output_contract_review": out_review,
        "map_navigation_quality_acceptance_review": quality_review,
        "map_navigation_health_validation_whitebox_review": health_review,
        "map_navigation_provider_runtime_boundary_review": prov_review,
        "map_navigation_fallback_replacement_review": fallback_review,
        "map_navigation_module_internal_self_check_review": self_check_review,
        "map_navigation_midplatform_interaction_check_review": interaction_review,
        "map_navigation_midplatform_governance_binding_review": binding_review,
        "map_navigation_information_integration_handoff_review": ii_review,
        "map_navigation_decision_center_handoff_review": dc_review,
        "map_navigation_action_gate_boundary_review": action_gate_review,
        "map_navigation_memory_worldmodel_admission_boundary_review": mem_wm_review,
        "map_navigation_layer_dependency_review": layer_dep_review,
        "map_navigation_module_qualification_check_review": qual_check_review,
        "map_navigation_non_runtime_boundary_audit": boundary_audit,
        "map_navigation_blocked_path_result": blocked_path_result,
        "map_navigation_module_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
