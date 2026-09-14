# -*- coding: utf-8 -*-
"""Map / Navigation Module Model Profile + Governance Binding Planning v1 — qualification only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.asr_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as ASR_DR_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_output_chain_closure_review_v1 import (
    FINAL_DECISION_GO as SCENE_CLOSURE_FINAL_GO,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_BUS_DR_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONTROLLED_RUNTIME_DR_FINAL_GO,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as BINDING_DR_FINAL_GO,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    DECISION_CENTER_REF,
    INFORMATION_INTEGRATION_REF,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    STANDARD_ID as MIDPLATFORM_BINDING_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
)
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as REGISTRY_DR_FINAL_GO,
)
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
    DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
)
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DUAL_VALIDATION_MECHANISM_ID,
    DUAL_VALIDATION_NON_CLAIMS,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)
from capabilities.governance.ocr_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OCR_DR_FINAL_GO,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)
from capabilities.governance.tts_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as TTS_DR_FINAL_GO,
)
from capabilities.governance.vision_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VISION_DR_FINAL_GO,
)
from capabilities.governance.vision_module_model_profile_governance_binding_planning_v1 import (
    QUALIFICATION_CHECK_CRITERIA,
    QUALIFICATION_MODE,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID

PHASE_ID = "Phase-Map-Navigation-Module-Model-Profile-Governance-Binding-Planning-v1-001"
SCOPE = "map_navigation_module_model_profile_governance_binding_planning_only"
SOURCE_CHAIN = "map_navigation_module_model_profile_governance_binding_planning_v1"

FINAL_DECISION_GO = (
    "MAP_NAVIGATION_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "MAP_NAVIGATION_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Map-Navigation-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Map-Navigation-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"
)

MODULE_ID = "map_navigation_application_module"
MODULE_LOCAL_PROFILE_ID = "map_navigation_application_module_local_profile_v1"
MIDPLATFORM_BINDING_ID = "map_navigation_application_midplatform_binding_v1"
CAPABILITY_STACK_DEF_ID = "map_navigation_capability_stack_definition_v1"
LAYERED_GOV_MAPPING_ID = "map_navigation_layered_governance_mapping_v1"
CAPABILITY_BUS_CONTRACT_REF = "map_navigation_capability_bus_contract_v1"

MAP_NAV_REGISTRY_REFS: Tuple[str, ...] = (
    "map_provider_placeholder_candidate",
    "route_reasoning_candidate",
    "indoor_facility_search_candidate",
    "transit_context_candidate",
)
MAP_REGISTRY_PLACEHOLDER_REGISTRY_ID = "map_provider_placeholder"

REUSED_GOVERNANCE_STANDARDS: Tuple[str, ...] = (
    "Model Profile Registry",
    "Module-Local Model Profile Standard",
    "Midplatform Model Governance Binding Standard",
    "Dual Validation Mechanism",
    "Layered Capability Stack Standard",
    "Layered Governance Mapping",
    "Constitution-Bus v1.0",
    "Provider Abstraction Standard",
    "Controlled Runtime Framework",
    "Luna Gate Chain / Enforcement Gate System",
    "Candidate/Evidence Contract pattern",
    "Boundary Matrix / Blocked Path / Non-Claims pattern",
)

MAP_NAV_MIDPLATFORM_INTERACTION_CHECK_COVERAGE: Tuple[str, ...] = (
    "Constitution-Bus binding",
    "Capability Bus contract",
    "Provider Abstraction binding",
    "Information Integration handoff",
    "Decision Center handoff",
    "Navigation Action Gate boundary",
    "Validation requirement",
    "Health requirement / external oversight",
    "Whitebox trace",
    "Controlled Runtime requirement",
    "Memory / WorldModel non-write boundary",
    "source_chain / evidence / traceability preservation",
)

IO_FORBIDDEN: Tuple[str, ...] = (
    "direct_navigation_action",
    "safe_to_cross",
    "go_ahead",
    "direct_user_instruction",
    "direct_fact",
    "direct_memory_write",
    "direct_worldmodel_write",
    "direct_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Map / Navigation Module Planning GO ≠ map provider selected",
    "map provider ref ≠ map API invocation",
    "route proposal contract planned ≠ route planning executable",
    "route context candidate ≠ navigation permission",
    "Navigation Action Gate boundary declared ≠ navigation action enabled",
    "Map / Navigation binding feasible ≠ Constitution/Oversight fully integrated",
    "Health/Oversight refs attached ≠ health/supervision metrics finalized",
    "next DryRunAndReview ≠ map provider invocation/runtime/navigation action",
    "Module Governance Binding GO ≠ module fully integrated with Constitution",
    "Module Governance Binding GO ≠ module fully integrated with Health/Oversight",
    "Constitution binding feasible ≠ constitution effectiveness quantified",
    "Module Internal Self-Check GO ≠ Midplatform Interaction Check GO",
    "Midplatform Interaction Check GO ≠ Runtime Ready",
    "Layer 3 application dependency declared ≠ Layer 1/2 override permitted",
)

QUALIFICATION_FIELDS: Dict[str, bool] = {
    "qualification_check_only": True,
    "full_integration_certification_now": False,
    "constitution_binding_feasible": True,
    "oversight_binding_feasible": True,
    "constitution_effectiveness_quantified_now": False,
    "health_metrics_finalized_now": False,
    "supervision_metrics_finalized_now": False,
    "module_constitution_fully_integrated_now": False,
    "module_oversight_fully_integrated_now": False,
    "health_metric_detail_defined_now": False,
    "supervision_metric_detail_defined_now": False,
}

CLOSURE_CAN_SAY: Tuple[str, ...] = (
    "Map / Navigation module can reference Registry",
    "Map / Navigation module can bind Module-local Profile Standard",
    "Map / Navigation module can bind Midplatform Governance Standard",
    "Map / Navigation module can preserve candidate-only route/map outputs",
    "Map / Navigation module can attach Health/Oversight refs later",
    "Map / Navigation module can declare Layer 3 application dependency on Scene/Spatiotemporal layers",
    "Map / Navigation module can declare Navigation Action Gate boundary",
)

CLOSURE_CANNOT_SAY: Tuple[str, ...] = (
    "Map / Navigation runtime is ready",
    "map provider selected or invoked",
    "map API is callable",
    "route planning is available",
    "navigation action is available",
    "safe-to-cross / go-ahead output is allowed",
    "module is fully integrated with Constitution",
    "module is fully integrated with Health/Oversight",
    "health/supervision metrics finalized",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "map_navigation_module_model_profile_governance_binding_planning_only",
    "qualification_check_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "map_navigation_module_runtime_enabled_now",
    "map_provider_invoked_now",
    "map_api_called_now",
    "route_planning_executed_now",
    "navigation_action_generated_now",
    "navigation_instruction_generated_now",
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
    "map_navigation_module_model_profile_governance_binding_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
        "runtime_enabled_now": False,
        "map_provider_invoked_now": False,
        "map_api_called_now": False,
        "route_planning_executed_now": False,
        "navigation_action_generated_now": False,
        "navigation_instruction_generated_now": False,
        "location_fact_generated_now": False,
        "provider_invoked_now": False,
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


def _map_registry_ids_from_seeds(map_seeds: Dict[str, Any]) -> List[str]:
    return [
        c.get("model_profile_id")
        for c in (map_seeds.get("candidates") or [])
        if c.get("model_profile_id")
    ]


def _map_registry_refs_review_pass(
    map_registry_ids: List[str],
    map_seeds_review: Dict[str, Any],
) -> bool:
    direct_refs_ok = all(
        ref in map_registry_ids
        for ref in (
            "route_reasoning_candidate",
            "indoor_facility_search_candidate",
            "transit_context_candidate",
        )
    )
    placeholder_ok = (
        MAP_REGISTRY_PLACEHOLDER_REGISTRY_ID in map_registry_ids
        or map_seeds_review.get("review_pass") is True
    )
    return direct_refs_ok and placeholder_ok


def run_map_navigation_module_model_profile_governance_binding_planning_v1(
    *,
    asr_module_model_profile_governance_binding_dryrun_and_review_root: str,
    tts_module_model_profile_governance_binding_dryrun_and_review_root: str,
    ocr_module_model_profile_governance_binding_dryrun_and_review_root: str,
    vision_module_model_profile_governance_binding_dryrun_and_review_root: str,
    midplatform_model_governance_binding_standardization_dryrun_and_review_root: str,
    module_local_model_profile_standardization_dryrun_and_review_root: str,
    model_profile_registry_dryrun_and_review_root: str,
    first_person_scene_understanding_output_chain_closure_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    asr_dr_root = Path(
        asr_module_model_profile_governance_binding_dryrun_and_review_root
    ).expanduser().resolve()
    tts_dr_root = Path(
        tts_module_model_profile_governance_binding_dryrun_and_review_root
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_module_model_profile_governance_binding_dryrun_and_review_root
    ).expanduser().resolve()
    vision_dr_root = Path(
        vision_module_model_profile_governance_binding_dryrun_and_review_root
    ).expanduser().resolve()
    binding_dr_root = Path(
        midplatform_model_governance_binding_standardization_dryrun_and_review_root
    ).expanduser().resolve()
    ml_dr_root = Path(
        module_local_model_profile_standardization_dryrun_and_review_root
    ).expanduser().resolve()
    registry_dr_root = Path(model_profile_registry_dryrun_and_review_root).expanduser().resolve()
    registry_plan_root = registry_dr_root.parent / "model_profile_registry_planning"
    scene_closure_root = Path(
        first_person_scene_understanding_output_chain_closure_review_root
    ).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    asr_dr_vr = _try_read_json(asr_dr_root / "verifier_report.json") or {}
    asr_dr_sm = _try_read_json(asr_dr_root / "summary.json") or {}
    tts_dr_vr = _try_read_json(tts_dr_root / "verifier_report.json") or {}
    tts_dr_sm = _try_read_json(tts_dr_root / "summary.json") or {}
    ocr_dr_vr = _try_read_json(ocr_dr_root / "verifier_report.json") or {}
    ocr_dr_sm = _try_read_json(ocr_dr_root / "summary.json") or {}
    vision_dr_vr = _try_read_json(vision_dr_root / "verifier_report.json") or {}
    vision_dr_sm = _try_read_json(vision_dr_root / "summary.json") or {}
    binding_dr_vr = _try_read_json(binding_dr_root / "verifier_report.json") or {}
    ml_dr_vr = _try_read_json(ml_dr_root / "verifier_report.json") or {}
    registry_dr_vr = _try_read_json(registry_dr_root / "verifier_report.json") or {}
    registry_dr_sm = _try_read_json(registry_dr_root / "summary.json") or {}
    scene_closure_vr = _try_read_json(scene_closure_root / "verifier_report.json") or {}
    scene_closure_sm = _try_read_json(scene_closure_root / "summary.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}

    map_seeds = _try_read_json(
        registry_plan_root / "map_navigation_model_profile_seed_candidates_v1.json"
    ) or {}
    map_seeds_review = _try_read_json(
        registry_dr_root / "map_navigation_model_profile_seed_candidates_review_v1.json"
    ) or {}
    map_registry_ids = _map_registry_ids_from_seeds(map_seeds)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root)}

    if asr_dr_vr.get("verifier") != "GO":
        blockers.append("ASR Module DryRunAndReview must be GO")
    if asr_dr_sm.get("final_decision") != ASR_DR_FINAL_GO:
        blockers.append("ASR DryRun final_decision mismatch")
    if tts_dr_vr.get("verifier") != "GO":
        blockers.append("TTS Module DryRunAndReview must be GO")
    if tts_dr_sm.get("final_decision") != TTS_DR_FINAL_GO:
        blockers.append("TTS DryRun final_decision mismatch")
    if ocr_dr_vr.get("verifier") != "GO":
        blockers.append("OCR Module DryRunAndReview must be GO")
    if ocr_dr_sm.get("final_decision") != OCR_DR_FINAL_GO:
        blockers.append("OCR DryRun final_decision mismatch")
    if vision_dr_vr.get("verifier") != "GO":
        blockers.append("Vision Module DryRunAndReview must be GO")
    if vision_dr_sm.get("final_decision") != VISION_DR_FINAL_GO:
        blockers.append("Vision DryRun final_decision mismatch")
    if binding_dr_vr.get("verifier") != "GO":
        blockers.append("Midplatform Binding DryRunAndReview must be GO")
    if ml_dr_vr.get("verifier") != "GO":
        blockers.append("Module-Local DryRunAndReview must be GO")
    if registry_dr_vr.get("verifier") != "GO":
        blockers.append("Model Profile Registry DryRunAndReview must be GO")
    if registry_dr_sm.get("final_decision") != REGISTRY_DR_FINAL_GO:
        blockers.append("Registry DryRun final_decision mismatch")
    if scene_closure_vr.get("verifier") != "GO":
        blockers.append("First-Person Scene Understanding Output Chain Closure Review must be GO")
    if scene_closure_sm.get("final_decision") != SCENE_CLOSURE_FINAL_GO:
        blockers.append("Scene closure final_decision mismatch")
    if cb_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if provider_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction Standard must be GO")
    if cr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime Framework must be GO")

    if not _map_registry_refs_review_pass(map_registry_ids, map_seeds_review):
        blockers.append("map navigation registry refs must exist or be explicitly registered")

    input_ok = len(blockers) == 0
    registry_refs_pass = _map_registry_refs_review_pass(map_registry_ids, map_seeds_review)

    upstream_review = {
        "review_id": "upstream_asr_module_input_review_v1",
        "asr_dryrun_verifier": asr_dr_vr.get("verifier"),
        "asr_dryrun_final_decision": asr_dr_sm.get("final_decision"),
        "tts_dryrun_verifier": tts_dr_vr.get("verifier"),
        "tts_dryrun_final_decision": tts_dr_sm.get("final_decision"),
        "ocr_dryrun_verifier": ocr_dr_vr.get("verifier"),
        "ocr_dryrun_final_decision": ocr_dr_sm.get("final_decision"),
        "vision_dryrun_verifier": vision_dr_vr.get("verifier"),
        "vision_dryrun_final_decision": vision_dr_sm.get("final_decision"),
        "scene_closure_verifier": scene_closure_vr.get("verifier"),
        "scene_closure_final_decision": scene_closure_sm.get("final_decision"),
        "binding_dryrun_verifier": binding_dr_vr.get("verifier"),
        "module_local_dryrun_verifier": ml_dr_vr.get("verifier"),
        "registry_dryrun_verifier": registry_dr_vr.get("verifier"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_reuse = {
        "review_id": "governance_standard_reuse_review_v1",
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "reuse_rule_text": PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
        "reused_standards": list(REUSED_GOVERNANCE_STANDARDS),
        "new_governance_need_proven": False,
        "no_parallel_duplicate_governance_standard": True,
        "map_navigation_module_qualification_planning_not_new_framework": True,
        **meta,
    }

    module_definition = {
        "definition_id": "map_navigation_module_definition_v1",
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "Map / Navigation / Route Application",
        "primary_goal": "navigation_application_candidate_generation_later",
        "capability_layer": "Layer 3 Navigation Application",
        "depends_on_layer_1": "Current Scene Understanding",
        "depends_on_layer_2": "Spatiotemporal Continuity",
        "registry_ref": REGISTRY_REF,
        "runtime_enabled_now": False,
        "map_provider_invoked_now": False,
        "route_planning_executed_now": False,
        "navigation_action_generated_now": False,
        "candidate_only": True,
        "confirmations": [
            "Map / Navigation does not generate base scene facts",
            "Map / Navigation does not override Vision/OCR/ASR evidence",
            "Map / Navigation does not directly generate navigation actions",
            "Map / Navigation does not directly trigger user_output",
            "Map / Navigation does not write Memory/WorldModel",
            "Map / Navigation is Layer 3 application layer",
            "Map / Navigation cannot override Layer 1 Current Scene Understanding",
            "Map / Navigation cannot override Layer 2 Spatiotemporal Continuity",
        ],
        **meta,
    }

    capability_stack = {
        "definition_id": CAPABILITY_STACK_DEF_ID,
        "module_id": MODULE_ID,
        "universal_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layers": {
            "layer_1_dependency_input": {
                "inputs": [
                    "scene_context_candidate_ref",
                    "visual_observation_candidate_ref",
                    "obstacle_candidate_ref",
                    "risk_context_candidate_ref",
                ],
                "role": "consumes Layer 1 scene understanding candidates; cannot override perception",
            },
            "layer_2_dependency_input": {
                "inputs": [
                    "location_context_candidate",
                    "spatiotemporal_context_candidate",
                    "route_progress_context_candidate_later",
                    "map_vision_conflict_candidate_later",
                ],
                "role": "consumes Layer 2 spatiotemporal candidates; conflict/gap/freshness required",
            },
            "layer_3_navigation_application": {
                "outputs": [
                    "map_location_context_candidate",
                    "route_context_candidate",
                    "navigation_task_candidate",
                    "facility_search_candidate_later",
                    "transit_context_candidate_later",
                    "crossing_context_candidate_later",
                ],
                "role": "route/navigation context as candidate; safety priority; Decision Center handoff",
            },
            "layer_4_extended_application_later": {
                "outputs": [
                    "indoor_navigation_candidate_later",
                    "transport_assistance_candidate_later",
                    "social_facility_search_candidate_later",
                ],
                "status": "later",
            },
        },
        "forbidden": [
            "no base scene fact generation",
            "no Vision/OCR/ASR evidence override",
            "no direct navigation action",
            "no direct user_output",
            "no Memory/WorldModel write",
        ],
        **meta,
    }

    layered_governance = {
        "mapping_id": LAYERED_GOV_MAPPING_ID,
        "module_id": MODULE_ID,
        "universal_mapping_ref": ADDENDUM_ID,
        "layers": {
            "L1_dependency": {
                "requirements": [
                    "consumes scene/risk/obstacle candidates",
                    "cannot override perception",
                ],
            },
            "L2_dependency": {
                "requirements": [
                    "consumes location/spatiotemporal candidates",
                    "conflict/gap/freshness required",
                ],
            },
            "L3": {
                "requirements": [
                    "route/navigation context as candidate",
                    "safety priority",
                    "Decision Center handoff",
                    "Navigation Action Gate later",
                ],
            },
            "L4": {
                "requirements": [
                    "indoor/transport/social facility later",
                    "privacy/location sensitivity later",
                    "provider/runtime authorization later",
                ],
            },
        },
        "confirmations": [
            "navigation is application layer",
            "survival safety overrides task progress",
            "route context cannot override real-time risk context",
            "no navigation action without Decision + Action Gate + Controlled Runtime",
            "no weakened constitution by layer",
            "Layer 3 cannot override Layer 1 scene understanding",
            "Layer 3 cannot override Layer 2 spatiotemporal continuity",
        ],
        **meta,
    }

    module_local_profile = {
        "module_local_profile_id": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "Map / Navigation / Route Application",
        "capability_layer": "Layer 3 Navigation Application",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(MAP_NAV_REGISTRY_REFS),
        "capability_stack_ref": CAPABILITY_STACK_DEF_ID,
        "layered_governance_mapping_ref": LAYERED_GOV_MAPPING_ID,
        "model_role_in_module": [
            "map_location_context_candidate_later",
            "route_context_candidate_later",
            "route_reasoning_candidate_later",
            "facility_search_candidate_later",
            "transit_context_candidate_later",
        ],
        "model_source_strategy": "A_direct_open_source_or_external_provider",
        "candidate_output_type": "map_navigation_candidate/context/proposal",
        "midplatform_governance_binding_ref": MIDPLATFORM_BINDING_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "map_navigation_whitebox_trace_requirement_v1",
        "quality_acceptance_ref": "map_navigation_quality_acceptance_plan_v1",
        "no_registry_override": True,
        "no_model_selection_by_module": True,
        "no_model_invocation_by_profile": True,
        "no_direct_navigation_action": True,
        "no_direct_user_output": True,
        "model_selected_now": False,
        "model_invoked_now": False,
        **meta,
    }

    registry_refs_review = {
        "review_id": "map_navigation_model_profile_registry_refs_review_v1",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(MAP_NAV_REGISTRY_REFS),
        "registry_placeholder_registry_id": MAP_REGISTRY_PLACEHOLDER_REGISTRY_ID,
        "seed_candidates_in_registry": [
            {
                "ref": "map_provider_placeholder_candidate",
                "registry_id": MAP_REGISTRY_PLACEHOLDER_REGISTRY_ID,
                "explicitly_registered": MAP_REGISTRY_PLACEHOLDER_REGISTRY_ID in map_registry_ids,
                "candidate_only": True,
                "selected_now": False,
                "invoked_now": False,
            },
            {
                "ref": "route_reasoning_candidate",
                "in_registry": "route_reasoning_candidate" in map_registry_ids,
                "candidate_only": True,
                "selected_now": False,
                "invoked_now": False,
            },
            {
                "ref": "indoor_facility_search_candidate",
                "in_registry": "indoor_facility_search_candidate" in map_registry_ids,
                "candidate_only": True,
                "selected_now": False,
                "invoked_now": False,
            },
            {
                "ref": "transit_context_candidate",
                "in_registry": "transit_context_candidate" in map_registry_ids,
                "candidate_only": True,
                "selected_now": False,
                "invoked_now": False,
            },
        ],
        "confirmations": [
            "map_provider_placeholder_candidate exists or is explicitly registered",
            "route_reasoning_candidate exists or is explicitly registered",
            "indoor_facility_search_candidate exists or is explicitly registered",
            "transit_context_candidate exists or is explicitly registered",
            "all refs are candidate only",
            "none selected_now",
            "none invoked_now",
            "provider readiness later required",
            "route validation later required",
        ],
        "review_pass": registry_refs_pass,
        **meta,
    }

    role_assignment = {
        "plan_id": "map_navigation_model_role_assignment_plan_v1",
        "assignments": [
            {
                "registry_ref": "map_provider_placeholder_candidate",
                "registry_id": MAP_REGISTRY_PLACEHOLDER_REGISTRY_ID,
                "role": "map context provider role",
                "status": "placeholder_later",
            },
            {
                "registry_ref": "route_reasoning_candidate",
                "role": "route proposal role",
                "status": "deferred_later",
            },
            {
                "registry_ref": "indoor_facility_search_candidate",
                "role": "indoor/facility candidate role later",
                "status": "later",
            },
            {
                "registry_ref": "transit_context_candidate",
                "role": "public transport candidate role later",
                "status": "later",
            },
        ],
        "confirmations": [
            "map provider placeholder maps to map context provider role",
            "route reasoning maps to route proposal role",
            "indoor facility search maps to indoor/facility candidate role later",
            "transit context maps to public transport candidate role later",
            "no single model/provider owns navigation authority",
            "route candidate ≠ navigation permission",
            "navigation context ≠ safe-to-move instruction",
        ],
        **meta,
    }

    input_contract = {
        "contract_id": "map_navigation_input_contract_v1",
        "module_id": MODULE_ID,
        "allowed_inputs": [
            "integrated_context_candidate",
            "scene_context_candidate",
            "risk_context_candidate",
            "obstacle_candidate",
            "location_context_candidate",
            "route_request_candidate_later",
            "user_task_intent_candidate",
            "map_provider_context_candidate_later",
            "transit_context_candidate_later",
        ],
        "confirmations": [
            "raw map provider data not consumed now",
            "map API not called now",
            "route request not executed now",
            "real location fact not generated now",
        ],
        **meta,
    }

    output_contract = {
        "contract_id": "map_navigation_output_contract_v1",
        "module_id": MODULE_ID,
        "allowed_outputs": [
            "map_location_context_candidate",
            "route_context_candidate",
            "navigation_task_candidate",
            "route_proposal_candidate_later",
            "facility_search_candidate_later",
            "transit_context_candidate_later",
            "navigation_action_request_candidate_later",
            "navigation_risk_candidate_later",
        ],
        "forbidden_outputs": list(IO_FORBIDDEN),
        "handoff_target": INFORMATION_INTEGRATION_REF,
        **meta,
    }

    quality_plan = {
        "plan_id": "map_navigation_quality_acceptance_plan_v1",
        "requirements": [
            "route_accuracy_target_later",
            "location_context_confidence_later",
            "map_freshness_requirement_later",
            "route_safety_validation_required_later",
            "latency_budget_later",
            "resource_budget_later",
        ],
        "candidate_contract_compliance_required": True,
        "traceability_completeness_required": True,
        "degradation_behavior_required": True,
        "benchmark_required_later": True,
        "benchmark_executed_now": False,
        **meta,
    }

    health_validation_whitebox = {
        "plan_id": "map_navigation_health_validation_whitebox_plan_v1",
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "map_navigation_whitebox_trace_requirement_v1",
        "source_chain_required": True,
        "issue_trace_required": True,
        "map_source_freshness_trace_required_later": True,
        "health_status_ref_transport_only": True,
        "module_cannot_self_certify_health": True,
        "scope_note": "ref slots only; metric detail deferred",
        **meta,
    }

    provider_runtime_boundary = {
        "plan_id": "map_navigation_provider_runtime_boundary_plan_v1",
        "provider_abstraction_required": True,
        "controlled_runtime_required": True,
        "confirmations": [
            "provider_candidate ≠ selected ≠ invoked",
            "no provider auto-switch",
            "map API call requires provider readiness later",
            "navigation runtime requires Controlled Runtime later",
            "navigation action requires Navigation Action Gate later",
            "Map / Navigation runtime remains disabled now",
        ],
        **meta,
    }

    fallback_plan = {
        "plan_id": "map_navigation_fallback_replacement_plan_v1",
        "fallback_model_profile_refs": list(MAP_NAV_REGISTRY_REFS),
        "replacement_conditions": [
            "provider_unavailable",
            "map_stale_risk",
            "route_conflict_with_scene_risk",
            "location_uncertainty",
            "license_risk",
            "latency_budget_failure",
            "safety_uncertainty",
        ],
        "hold_instead_of_fallback_when": "safety/location confidence is insufficient",
        "no_auto_switch_without_governance_policy": True,
        "replacement_does_not_imply_invocation": True,
        **meta,
    }

    self_check_plan = {
        "plan_id": "map_navigation_module_internal_self_check_plan_v1",
        "mechanism_layer": "Module Internal Self-Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "Map / Navigation 模块内部是否按标准写好 profile / contract / binding refs",
        "self_check_coverage": list(MODULE_INTERNAL_SELF_CHECK_COVERAGE),
        "rules": [
            "自检不授权 Map / Navigation runtime",
            "自检不选择 map provider",
            "自检不调用 map API",
            "自检不执行 route planning",
            "自检不生成 navigation action",
            "自检不写 Memory / WorldModel",
            "自检不生成 user output / safe-to-cross / go-ahead",
        ],
        "does_not_replace": "Midplatform Interaction Check",
        **meta,
    }

    interaction_check_plan = {
        "plan_id": "map_navigation_midplatform_interaction_check_plan_v1",
        "mechanism_layer": "Midplatform Interaction Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "Map / Navigation 模块与中台交互是否合规、无绕路",
        "interaction_check_coverage": list(MAP_NAV_MIDPLATFORM_INTERACTION_CHECK_COVERAGE),
        "rules": [
            "中台检验不等于 Map / Navigation runtime 授权",
            "中台检验不等于 map provider 选择",
            "中台检验不等于 map API / route planning invocation",
            "中台检验不等于 navigation action generation",
        ],
        "does_not_replace": "Module Internal Self-Check",
        **meta,
    }

    midplatform_binding = {
        "midplatform_governance_binding_id": MIDPLATFORM_BINDING_ID,
        "module_local_profile_ref": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "registry_model_profile_refs": list(MAP_NAV_REGISTRY_REFS),
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "constitution_bus_ref": CONSTITUTION_BUS_REF,
        "capability_bus_contract_ref": CAPABILITY_BUS_CONTRACT_REF,
        "provider_abstraction_ref": PROVIDER_ABS_STANDARD_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "map_navigation_whitebox_trace_requirement_v1",
        "information_integration_consumption_policy_ref": (
            "map_navigation_information_integration_handoff_plan_v1"
        ),
        "decision_center_consumption_policy_ref": "map_navigation_decision_center_handoff_plan_v1",
        "navigation_action_gate_requirement_ref_later": "map_navigation_action_gate_boundary_plan_v1",
        "controlled_runtime_requirement_ref": CONTROLLED_RUNTIME_FRAMEWORK_REF,
        "memory_admission_requirement_ref_later": "memory_admission_gate_later",
        "worldmodel_admission_requirement_ref_later": "worldmodel_admission_gate_later",
        "source_chain_requirement_ref": "map_navigation_source_chain_requirement_v1",
        "issue_trace_requirement_ref": "map_navigation_issue_trace_requirement_v1",
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        "non_compliance_handling_policy_ref_later": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
        "model_selected_now": False,
        "model_invoked_now": False,
        "runtime_enabled_now": False,
        **meta,
    }

    ii_handoff = {
        "plan_id": "map_navigation_information_integration_handoff_plan_v1",
        "information_integration_ref": INFORMATION_INTEGRATION_REF,
        "consumes": [
            "map_location_context",
            "route_context",
            "navigation_task",
            "facility_search",
            "transit_context",
        ],
        "confirmations": [
            "Map / Navigation outputs go to Information Integration as candidate/context/proposal",
            "Information Integration consumes map_location_context / route_context / "
            "navigation_task / facility_search / transit_context",
            "Map / Navigation cannot bypass Information Integration to direct action",
            "no integrated_context generated now",
        ],
        **meta,
    }

    decision_handoff = {
        "plan_id": "map_navigation_decision_center_handoff_plan_v1",
        "decision_center_ref": DECISION_CENTER_REF,
        "handoff_via": ["integrated_context", "decision_request"],
        "confirmations": [
            "decision-relevant navigation outputs reach Decision Center only through "
            "integrated_context / decision_request",
            "Map / Navigation module cannot emit final movement decision",
            "route candidate cannot directly trigger navigation action",
            "no decision generated now",
        ],
        **meta,
    }

    action_gate_boundary = {
        "plan_id": "map_navigation_action_gate_boundary_plan_v1",
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        "confirmations": [
            "Navigation Action Gate required later for any movement/action instruction",
            "map route proposal ≠ movement permission",
            "safe_to_cross / go_ahead forbidden now",
            "no navigation action now",
            "no user instruction now",
        ],
        **meta,
    }

    memory_wm_boundary = {
        "plan_id": "map_navigation_memory_worldmodel_admission_boundary_plan_v1",
        "confirmations": [
            "Map / Navigation module cannot write Memory",
            "Map / Navigation module cannot write WorldModel",
            "location/route evidence may be admission candidate later",
            "map correction / route memory later requires Admission",
            "no memory/worldmodel write now",
        ],
        **meta,
    }

    layer_dependency_review = {
        "review_id": "map_navigation_layer_dependency_review_v1",
        "capability_layer": "Layer 3 Navigation Application",
        "depends_on_layer_1": "Current Scene Understanding",
        "depends_on_layer_2": "Spatiotemporal Continuity",
        "confirmations": [
            "Layer 3 Navigation depends on Layer 1 scene understanding",
            "Layer 3 Navigation depends on Layer 2 spatiotemporal continuity",
            "Layer 3 cannot override safety/risk candidates from lower layers",
            "route task progress cannot override survival risk",
            "navigation application cannot claim current scene understanding authority",
            "Map / Navigation is Layer 3 application layer",
            "Map / Navigation cannot override Layer 1 Current Scene Understanding",
            "Map / Navigation cannot override Layer 2 Spatiotemporal Continuity",
        ],
        "review_pass": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "map_navigation_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        **meta,
    }

    qualification_check = {
        "check_id": "map_navigation_module_qualification_check_v1",
        "qualification_mode": QUALIFICATION_MODE,
        "criteria": list(QUALIFICATION_CHECK_CRITERIA),
        "criteria_count": len(QUALIFICATION_CHECK_CRITERIA),
        "qualification_fields": dict(QUALIFICATION_FIELDS),
        "can_say": list(CLOSURE_CAN_SAY),
        "cannot_say": list(CLOSURE_CANNOT_SAY),
        "qualification_pass": input_ok and registry_refs_pass,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "map_navigation_module_model_profile_governance_binding_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "qualification_mode": QUALIFICATION_MODE,
        "objectives": [
            "qualification check only: verify Map / Navigation module sample is compliant",
            "generate map_navigation_module_model_profile_governance_binding_candidate",
            "verify Map / Navigation module definition / capability stack / layered governance mapping",
            "verify module-local model profile registry refs",
            "verify map provider / route reasoning / facility search / transit context role assignment",
            "verify input/output contracts",
            "verify quality / health / validation / whitebox / provider-runtime / fallback",
            "verify Navigation Action Gate boundary",
            "verify Layer 3 dependency on Layer 1/2",
            "execute Map / Navigation module internal self-check + midplatform interaction check",
            "no health/supervision metric detail expansion",
            "no model select/download/invoke/benchmark",
            "no map provider selection/invocation / map API / route planning / navigation action",
        ],
        **meta,
    }

    planning_pass = qualification_check.get("qualification_pass")
    planning_decision = {
        "decision_id": "map_navigation_module_model_profile_governance_binding_planning_decision_v1",
        "planning_pass": planning_pass,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "closure_can_say": list(CLOSURE_CAN_SAY),
        "closure_cannot_say": list(CLOSURE_CANNOT_SAY),
        **meta,
    }

    policy = {
        "policy_id": "map_navigation_module_model_profile_governance_binding_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "map_navigation_module_model_profile_governance_binding_planning_only": True,
        "qualification_check_only": True,
        "phase_goal": (
            "Map / Navigation module model profile + governance binding qualification planning "
            "confirmation only. Map / Navigation is Layer 3 application layer and cannot override "
            "Layer 1 scene understanding or Layer 2 spatiotemporal continuity. "
            "No health/supervision metric expansion. No map provider selection/invocation, "
            "no map API, no route planning, no navigation action, no navigation runtime."
        ),
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        "dual_validation_non_claims": list(DUAL_VALIDATION_NON_CLAIMS),
        "non_compliant_module_model_handling_policy_deferred": True,
        "recommended_future_phase": DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "module_id": MODULE_ID,
        "capability_layer": "Layer 3 Navigation Application",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_ref_count": len(MAP_NAV_REGISTRY_REFS),
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "map_navigation_module_model_profile_governance_binding_planning_policy": policy,
        "upstream_asr_module_input_review": upstream_review,
        "governance_standard_reuse_review": governance_reuse,
        "map_navigation_module_definition": module_definition,
        "map_navigation_capability_stack_definition": capability_stack,
        "map_navigation_layered_governance_mapping": layered_governance,
        "map_navigation_module_local_model_profile": module_local_profile,
        "map_navigation_model_profile_registry_refs_review": registry_refs_review,
        "map_navigation_model_role_assignment_plan": role_assignment,
        "map_navigation_input_contract": input_contract,
        "map_navigation_output_contract": output_contract,
        "map_navigation_quality_acceptance_plan": quality_plan,
        "map_navigation_health_validation_whitebox_plan": health_validation_whitebox,
        "map_navigation_provider_runtime_boundary_plan": provider_runtime_boundary,
        "map_navigation_fallback_replacement_plan": fallback_plan,
        "map_navigation_module_internal_self_check_plan": self_check_plan,
        "map_navigation_midplatform_interaction_check_plan": interaction_check_plan,
        "map_navigation_midplatform_governance_binding": midplatform_binding,
        "map_navigation_information_integration_handoff_plan": ii_handoff,
        "map_navigation_decision_center_handoff_plan": decision_handoff,
        "map_navigation_action_gate_boundary_plan": action_gate_boundary,
        "map_navigation_memory_worldmodel_admission_boundary_plan": memory_wm_boundary,
        "map_navigation_layer_dependency_review": layer_dependency_review,
        "map_navigation_module_qualification_check": qualification_check,
        "map_navigation_non_runtime_boundary_matrix": boundary_matrix,
        "map_navigation_module_model_profile_governance_binding_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "map_navigation_module_model_profile_governance_binding_planning_decision": planning_decision,
        "summary": summary,
    }
