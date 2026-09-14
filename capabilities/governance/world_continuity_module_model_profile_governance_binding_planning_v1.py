# -*- coding: utf-8 -*-
"""World Continuity Module Model Profile + Governance Binding Planning v1 — qualification only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.asr_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as ASR_DR_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_information_integration_chain_dryrun_v1 import (
    FINAL_DECISION_GO as II_CHAIN_DR_FINAL_GO,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_BUS_DR_FINAL_GO,
)
from capabilities.governance.map_navigation_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MAP_NAV_DR_FINAL_GO,
)
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

PHASE_ID = "Phase-World-Continuity-Module-Model-Profile-Governance-Binding-Planning-v1-001"
SCOPE = "world_continuity_module_model_profile_governance_binding_planning_only"
SOURCE_CHAIN = "world_continuity_module_model_profile_governance_binding_planning_v1"

FINAL_DECISION_GO = (
    "WORLD_CONTINUITY_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "WORLD_CONTINUITY_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-World-Continuity-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-World-Continuity-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"
)

MODULE_ID = "world_continuity_understanding_module"
MODULE_LOCAL_PROFILE_ID = "world_continuity_understanding_module_local_profile_v1"
MIDPLATFORM_BINDING_ID = "world_continuity_understanding_midplatform_binding_v1"
CAPABILITY_STACK_DEF_ID = "world_continuity_capability_stack_definition_v1"
LAYERED_GOV_MAPPING_ID = "world_continuity_layered_governance_mapping_v1"
CAPABILITY_BUS_CONTRACT_REF = "world_continuity_capability_bus_contract_v1"

WORLD_CONTINUITY_REGISTRY_REFS: Tuple[str, ...] = (
    "scene_delta_candidate",
    "temporal_tracking_candidate",
    "visual_map_alignment_candidate",
    "spatiotemporal_consistency_manager_self_developed",
)
STCM_REGISTRY_ID = "stcm_self_developed_profile"

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
    "Candidate/Evidence Contract pattern",
    "WorldModel/Memory Admission boundary pattern",
    "Boundary Matrix / Blocked Path / Non-Claims pattern",
)

WORLD_CONTINUITY_MIDPLATFORM_INTERACTION_CHECK_COVERAGE: Tuple[str, ...] = (
    "Constitution-Bus binding",
    "Capability Bus contract",
    "Provider Abstraction binding",
    "Information Integration handoff",
    "Decision Center handoff",
    "Validation requirement",
    "Health requirement / external oversight",
    "Whitebox trace",
    "Controlled Runtime requirement",
    "Memory / WorldModel Admission boundary",
    "source_chain / evidence / traceability preservation",
)

IO_FORBIDDEN: Tuple[str, ...] = (
    "direct_fact",
    "direct_worldmodel_write",
    "direct_memory_write",
    "direct_navigation_action",
    "direct_user_output",
    "direct_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "World Continuity Planning GO ≠ temporal tracking enabled",
    "scene_delta candidate ref ≠ scene delta runtime",
    "visual-map alignment ref ≠ alignment runtime",
    "continuity candidate ≠ WorldModel fact",
    "WorldModel Admission boundary declared ≠ WorldModel write enabled",
    "Memory Admission boundary declared ≠ Memory write enabled",
    "World Continuity binding feasible ≠ Constitution/Oversight fully integrated",
    "next DryRunAndReview ≠ WorldModel write/runtime",
    "Module Governance Binding GO ≠ module fully integrated with Constitution",
    "Module Governance Binding GO ≠ module fully integrated with Health/Oversight",
    "Constitution binding feasible ≠ constitution effectiveness quantified",
    "Module Internal Self-Check GO ≠ Midplatform Interaction Check GO",
    "Midplatform Interaction Check GO ≠ Runtime Ready",
    "Layer 2 continuity role declared ≠ Layer 1/3 override permitted",
    "World Continuity candidate ≠ confirmed reality",
    "scene_delta candidate ≠ Memory/WorldModel write",
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
    "World Continuity module can reference Registry",
    "World Continuity module can bind Module-local Profile Standard",
    "World Continuity module can bind Midplatform Governance Standard",
    "World Continuity module can preserve candidate-only continuity outputs",
    "World Continuity module can attach Health/Oversight refs later",
    "World Continuity module can declare Layer 2 continuity role",
    "World Continuity module can declare WorldModel/Memory Admission boundaries",
)

CLOSURE_CANNOT_SAY: Tuple[str, ...] = (
    "World Continuity runtime is ready",
    "temporal tracking is executing",
    "visual-map alignment is available",
    "WorldModel write is allowed",
    "Memory write is allowed",
    "continuity hypothesis is fact",
    "module is fully integrated with Constitution",
    "module is fully integrated with Health/Oversight",
    "health/supervision metrics finalized",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "world_continuity_module_model_profile_governance_binding_planning_only",
    "qualification_check_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "world_continuity_module_runtime_enabled_now",
    "temporal_tracking_executed_now",
    "scene_delta_generated_as_fact_now",
    "visual_map_alignment_executed_now",
    "spatiotemporal_consistency_runtime_enabled_now",
    "worldmodel_write_now",
    "memory_write_now",
    "world_fact_generated_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
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
    "world_continuity_module_model_profile_governance_binding_planning"
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
        "worldmodel_write_now": False,
        "memory_write_now": False,
        "temporal_tracking_executed_now": False,
        "scene_delta_generated_as_fact_now": False,
        "visual_map_alignment_executed_now": False,
        "world_fact_generated_now": False,
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


def _world_registry_ids_from_seeds(world_seeds: Dict[str, Any]) -> List[str]:
    return [
        c.get("model_profile_id")
        for c in (world_seeds.get("candidates") or [])
        if c.get("model_profile_id")
    ]


def _resolve_module_ref_to_registry(ref: str) -> str:
    if ref == "spatiotemporal_consistency_manager_self_developed":
        return STCM_REGISTRY_ID
    return ref


def _world_registry_refs_review_pass(
    world_registry_ids: List[str],
    world_seeds_review: Dict[str, Any],
) -> bool:
    required_registry_ids = (
        "scene_delta_candidate",
        "temporal_tracking_candidate",
        "visual_map_alignment_candidate",
        STCM_REGISTRY_ID,
    )
    direct_ok = all(rid in world_registry_ids for rid in required_registry_ids)
    review_ok = world_seeds_review.get("review_pass") is True
    return direct_ok or review_ok


def run_world_continuity_module_model_profile_governance_binding_planning_v1(
    *,
    map_navigation_module_model_profile_governance_binding_dryrun_and_review_root: str,
    asr_module_model_profile_governance_binding_dryrun_and_review_root: str,
    tts_module_model_profile_governance_binding_dryrun_and_review_root: str,
    ocr_module_model_profile_governance_binding_dryrun_and_review_root: str,
    vision_module_model_profile_governance_binding_dryrun_and_review_root: str,
    midplatform_model_governance_binding_standardization_dryrun_and_review_root: str,
    module_local_model_profile_standardization_dryrun_and_review_root: str,
    model_profile_registry_dryrun_and_review_root: str,
    first_person_scene_understanding_information_integration_chain_dryrun_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    map_dr_root = Path(
        map_navigation_module_model_profile_governance_binding_dryrun_and_review_root
    ).expanduser().resolve()
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
    ii_chain_root = Path(
        first_person_scene_understanding_information_integration_chain_dryrun_root
    ).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    map_dr_vr = _try_read_json(map_dr_root / "verifier_report.json") or {}
    map_dr_sm = _try_read_json(map_dr_root / "summary.json") or {}
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
    ii_chain_vr = _try_read_json(ii_chain_root / "verifier_report.json") or {}
    ii_chain_sm = _try_read_json(ii_chain_root / "summary.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}

    world_seeds = _try_read_json(
        registry_plan_root / "world_continuity_model_profile_seed_candidates_v1.json"
    ) or {}
    world_seeds_review = _try_read_json(
        registry_dr_root / "world_continuity_model_profile_seed_candidates_review_v1.json"
    ) or {}
    world_registry_ids = _world_registry_ids_from_seeds(world_seeds)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root)}

    if map_dr_vr.get("verifier") != "GO":
        blockers.append("Map / Navigation Module DryRunAndReview must be GO")
    if map_dr_sm.get("final_decision") != MAP_NAV_DR_FINAL_GO:
        blockers.append("Map / Navigation DryRun final_decision mismatch")
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
    if ii_chain_vr.get("verifier") != "GO":
        blockers.append("First-Person Scene Understanding II Chain DryRun must be GO")
    if ii_chain_sm.get("final_decision") != II_CHAIN_DR_FINAL_GO:
        blockers.append("II Chain DryRun final_decision mismatch")
    if cb_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if provider_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction Standard must be GO")
    if cr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime Framework must be GO")

    if not _world_registry_refs_review_pass(world_registry_ids, world_seeds_review):
        blockers.append("world continuity registry refs must exist or be explicitly registered")

    input_ok = len(blockers) == 0
    registry_refs_pass = _world_registry_refs_review_pass(world_registry_ids, world_seeds_review)

    upstream_review = {
        "review_id": "upstream_map_navigation_module_input_review_v1",
        "map_navigation_dryrun_verifier": map_dr_vr.get("verifier"),
        "map_navigation_dryrun_final_decision": map_dr_sm.get("final_decision"),
        "asr_dryrun_verifier": asr_dr_vr.get("verifier"),
        "asr_dryrun_final_decision": asr_dr_sm.get("final_decision"),
        "tts_dryrun_verifier": tts_dr_vr.get("verifier"),
        "tts_dryrun_final_decision": tts_dr_sm.get("final_decision"),
        "ocr_dryrun_verifier": ocr_dr_vr.get("verifier"),
        "ocr_dryrun_final_decision": ocr_dr_sm.get("final_decision"),
        "vision_dryrun_verifier": vision_dr_vr.get("verifier"),
        "vision_dryrun_final_decision": vision_dr_sm.get("final_decision"),
        "ii_chain_dryrun_verifier": ii_chain_vr.get("verifier"),
        "ii_chain_dryrun_final_decision": ii_chain_sm.get("final_decision"),
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
        "world_continuity_module_qualification_planning_not_new_framework": True,
        **meta,
    }

    module_definition = {
        "definition_id": "world_continuity_module_definition_v1",
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "World Continuity / Spatiotemporal Understanding",
        "capability_layer": "Layer 2 Spatiotemporal Continuity",
        "primary_goal": "spatiotemporal_continuity_candidate_generation",
        "supports_layer_1": "Current Scene Understanding",
        "supports_layer_3": "Navigation Application",
        "registry_ref": REGISTRY_REF,
        "runtime_enabled_now": False,
        "worldmodel_write_now": False,
        "memory_write_now": False,
        "candidate_only": True,
        "confirmations": [
            "World Continuity is Layer 2 Spatiotemporal Continuity",
            "World Continuity supports Layer 1 scene understanding and Layer 3 navigation",
            "World Continuity does not override Layer 1 or Layer 3 authority",
            "World Continuity candidate ≠ WorldModel fact",
            "scene_delta candidate ≠ Memory/WorldModel write",
            "temporal consistency candidate ≠ confirmed reality",
            "World Continuity does not directly write WorldModel",
            "World Continuity does not directly write Memory",
            "World Continuity does not directly generate fact",
            "World Continuity does not directly generate navigation action",
        ],
        **meta,
    }

    capability_stack = {
        "definition_id": CAPABILITY_STACK_DEF_ID,
        "module_id": MODULE_ID,
        "universal_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layers": {
            "layer_1_scene_input": {
                "inputs": [
                    "visual_observation_candidate_ref",
                    "scene_context_candidate_ref",
                    "target_recognition_candidate_ref",
                    "risk_context_candidate_ref",
                ],
                "role": "consumes Layer 1 scene candidates; cannot override raw evidence",
            },
            "layer_2_spatiotemporal_continuity": {
                "outputs": [
                    "scene_delta_candidate",
                    "temporal_tracking_candidate",
                    "continuity_gap_candidate",
                    "spatiotemporal_consistency_candidate",
                    "missing_context_hypothesis_candidate",
                    "visual_map_alignment_candidate_later",
                ],
                "role": "continuity hypothesis as candidate; not fact",
            },
            "layer_3_application_support": {
                "outputs": [
                    "navigation_context_support_candidate",
                    "route_progress_consistency_candidate_later",
                    "safety_context_continuity_candidate_later",
                ],
                "role": "assists navigation/safety/task context; cannot emit action",
            },
            "layer_4_long_term_worldmodel_admission_later": {
                "outputs": [
                    "worldmodel_admission_candidate_later",
                    "stable_environment_memory_candidate_later",
                ],
                "status": "later",
            },
        },
        "forbidden": [
            "no direct WorldModel write",
            "no direct Memory write",
            "no direct fact generation",
            "no direct navigation action",
            "outputs enter Information Integration only",
        ],
        **meta,
    }

    layered_governance = {
        "mapping_id": LAYERED_GOV_MAPPING_ID,
        "module_id": MODULE_ID,
        "universal_mapping_ref": ADDENDUM_ID,
        "layers": {
            "L1_input": {
                "requirements": [
                    "consumes scene candidates",
                    "cannot override raw evidence",
                ],
            },
            "L2_continuity": {
                "requirements": [
                    "freshness", "conflict", "gap", "temporal consistency",
                    "evidence chain", "not_fact",
                ],
            },
            "L3_support": {
                "requirements": [
                    "assists navigation / safety / task context",
                    "cannot emit action",
                ],
            },
            "L4_admission_later": {
                "requirements": [
                    "WorldModel Admission required",
                    "Memory Admission required",
                    "stable fact requires evidence chain and admission gate",
                ],
            },
        },
        "confirmations": [
            "governance principles consistent",
            "execution intensity layered",
            "continuity hypothesis is not fact",
            "no WorldModel write without admission",
            "no weakened constitution by layer",
            "World Continuity does not override Layer 1 scene understanding",
            "World Continuity does not override Layer 3 navigation authority",
        ],
        **meta,
    }

    module_local_profile = {
        "module_local_profile_id": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "World Continuity / Spatiotemporal Understanding",
        "capability_layer": "Layer 2 Spatiotemporal Continuity",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(WORLD_CONTINUITY_REGISTRY_REFS),
        "capability_stack_ref": CAPABILITY_STACK_DEF_ID,
        "layered_governance_mapping_ref": LAYERED_GOV_MAPPING_ID,
        "model_role_in_module": [
            "scene_delta_candidate_role",
            "temporal_tracking_candidate_role",
            "visual_map_alignment_candidate_later",
            "spatiotemporal_consistency_manager_self_developed_role",
        ],
        "model_source_strategy": "mixed_reference_and_self_developed",
        "candidate_output_type": "world_continuity_candidate/context/hypothesis",
        "midplatform_governance_binding_ref": MIDPLATFORM_BINDING_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "world_continuity_whitebox_trace_requirement_v1",
        "quality_acceptance_ref": "world_continuity_quality_acceptance_plan_v1",
        "no_registry_override": True,
        "no_model_selection_by_module": True,
        "no_model_invocation_by_profile": True,
        "no_direct_fact_output": True,
        "no_direct_worldmodel_write": True,
        "no_direct_memory_write": True,
        "model_selected_now": False,
        "model_invoked_now": False,
        **meta,
    }

    registry_refs_review = {
        "review_id": "world_continuity_model_profile_registry_refs_review_v1",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(WORLD_CONTINUITY_REGISTRY_REFS),
        "stcm_registry_id": STCM_REGISTRY_ID,
        "seed_candidates_in_registry": [
            {
                "ref": "scene_delta_candidate",
                "in_registry": "scene_delta_candidate" in world_registry_ids,
                "candidate_only": True,
                "selected_now": False,
                "invoked_now": False,
            },
            {
                "ref": "temporal_tracking_candidate",
                "in_registry": "temporal_tracking_candidate" in world_registry_ids,
                "candidate_only": True,
                "selected_now": False,
                "invoked_now": False,
            },
            {
                "ref": "visual_map_alignment_candidate",
                "in_registry": "visual_map_alignment_candidate" in world_registry_ids,
                "candidate_only": True,
                "selected_now": False,
                "invoked_now": False,
            },
            {
                "ref": "spatiotemporal_consistency_manager_self_developed",
                "registry_id": STCM_REGISTRY_ID,
                "explicitly_registered": STCM_REGISTRY_ID in world_registry_ids,
                "self_developed_governance_profile_candidate": True,
                "candidate_only": True,
                "selected_now": False,
                "invoked_now": False,
            },
        ],
        "confirmations": [
            "scene_delta_candidate exists or is explicitly registered",
            "temporal_tracking_candidate exists or is explicitly registered",
            "visual_map_alignment_candidate exists or is explicitly registered",
            "spatiotemporal_consistency_manager_self_developed exists or is explicitly registered",
            "all refs are candidate only",
            "self-developed governance profile remains candidate",
            "none selected_now",
            "none invoked_now",
            "provider/runtime readiness later required where applicable",
        ],
        "review_pass": registry_refs_pass,
        **meta,
    }

    role_assignment = {
        "plan_id": "world_continuity_model_role_assignment_plan_v1",
        "assignments": [
            {
                "registry_ref": "scene_delta_candidate",
                "role": "scene change candidate role",
                "status": "primary_candidate",
            },
            {
                "registry_ref": "temporal_tracking_candidate",
                "role": "continuity/tracking candidate role",
                "status": "deferred_later",
            },
            {
                "registry_ref": "visual_map_alignment_candidate",
                "role": "later alignment support role",
                "status": "later",
            },
            {
                "registry_ref": "spatiotemporal_consistency_manager_self_developed",
                "registry_id": STCM_REGISTRY_ID,
                "role": "governance-owned consistency manager role",
                "status": "self_developed_candidate",
            },
        ],
        "confirmations": [
            "scene_delta maps to scene change candidate role",
            "temporal tracking maps to continuity/tracking candidate role",
            "visual-map alignment maps to later alignment support role",
            "STCM self-developed maps to governance-owned consistency manager role",
            "external models provide signals only",
            "Luna owns continuity governance",
            "no single model owns WorldModel truth",
        ],
        **meta,
    }

    input_contract = {
        "contract_id": "world_continuity_input_contract_v1",
        "module_id": MODULE_ID,
        "allowed_inputs": [
            "visual_observation_candidate",
            "scene_context_candidate",
            "target_recognition_candidate",
            "risk_context_candidate",
            "ocr_result_candidate_later",
            "location_context_candidate_later",
            "route_context_candidate_later",
            "prior_continuity_candidate_later",
            "drive_signal_candidate_later",
        ],
        "confirmations": [
            "raw frame sequence not consumed now",
            "live tracking not executed now",
            "location/map provider data not consumed directly now",
        ],
        **meta,
    }

    output_contract = {
        "contract_id": "world_continuity_output_contract_v1",
        "module_id": MODULE_ID,
        "allowed_outputs": [
            "world_continuity_candidate",
            "scene_delta_candidate",
            "temporal_tracking_candidate",
            "continuity_gap_candidate",
            "spatiotemporal_consistency_candidate",
            "missing_context_hypothesis_candidate",
            "visual_map_alignment_candidate_later",
            "worldmodel_admission_candidate_later",
        ],
        "forbidden_outputs": list(IO_FORBIDDEN),
        "handoff_target": INFORMATION_INTEGRATION_REF,
        **meta,
    }

    quality_plan = {
        "plan_id": "world_continuity_quality_acceptance_plan_v1",
        "requirements": [
            "temporal_consistency_target_later",
            "scene_delta_precision_target_later",
            "tracking_stability_target_later",
            "freshness_requirement_later",
            "conflict_detection_requirement_later",
            "gap_detection_requirement_later",
        ],
        "candidate_contract_compliance_required": True,
        "traceability_completeness_required": True,
        "degradation_behavior_required": True,
        "benchmark_required_later": True,
        "benchmark_executed_now": False,
        **meta,
    }

    health_validation_whitebox = {
        "plan_id": "world_continuity_health_validation_whitebox_plan_v1",
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "world_continuity_whitebox_trace_requirement_v1",
        "source_chain_required": True,
        "evidence_chain_required": True,
        "issue_trace_required": True,
        "health_status_ref_transport_only": True,
        "module_cannot_self_certify_health": True,
        "scope_note": "ref slots only; metric detail deferred",
        **meta,
    }

    provider_runtime_boundary = {
        "plan_id": "world_continuity_provider_runtime_boundary_plan_v1",
        "provider_abstraction_required": True,
        "controlled_runtime_required": True,
        "confirmations": [
            "provider_candidate ≠ selected ≠ invoked",
            "no provider auto-switch",
            "real frame sequence requires Controlled Runtime later",
            "real temporal tracking / visual-map alignment requires Controlled Runtime later",
            "World Continuity runtime remains disabled now",
        ],
        **meta,
    }

    fallback_plan = {
        "plan_id": "world_continuity_fallback_replacement_plan_v1",
        "fallback_model_profile_refs": list(WORLD_CONTINUITY_REGISTRY_REFS),
        "replacement_conditions": [
            "tracking_quality_regression",
            "scene_delta_conflict",
            "temporal_gap_unresolved",
            "provider_unavailable",
            "license_risk",
            "latency_budget_failure",
            "safety_uncertainty",
        ],
        "hold_instead_of_fallback_when": "continuity uncertainty affects safety/navigation",
        "no_auto_switch_without_governance_policy": True,
        "replacement_does_not_imply_invocation": True,
        **meta,
    }

    self_check_plan = {
        "plan_id": "world_continuity_module_internal_self_check_plan_v1",
        "mechanism_layer": "Module Internal Self-Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "World Continuity 模块内部是否按标准写好 profile / contract / binding refs",
        "self_check_coverage": list(MODULE_INTERNAL_SELF_CHECK_COVERAGE),
        "rules": [
            "自检不授权 World Continuity runtime",
            "自检不执行 temporal tracking / scene delta / visual-map alignment",
            "自检不写 WorldModel / Memory",
            "自检不生成 world fact",
            "自检不生成 navigation action / user output",
        ],
        "does_not_replace": "Midplatform Interaction Check",
        **meta,
    }

    interaction_check_plan = {
        "plan_id": "world_continuity_midplatform_interaction_check_plan_v1",
        "mechanism_layer": "Midplatform Interaction Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "World Continuity 模块与中台交互是否合规、无绕路",
        "interaction_check_coverage": list(WORLD_CONTINUITY_MIDPLATFORM_INTERACTION_CHECK_COVERAGE),
        "rules": [
            "中台检验不等于 World Continuity runtime 授权",
            "中台检验不等于 temporal tracking / scene delta execution",
            "中台检验不等于 WorldModel / Memory write",
            "中台检验不等于 continuity hypothesis promoted to fact",
        ],
        "does_not_replace": "Module Internal Self-Check",
        **meta,
    }

    midplatform_binding = {
        "midplatform_governance_binding_id": MIDPLATFORM_BINDING_ID,
        "module_local_profile_ref": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "registry_model_profile_refs": list(WORLD_CONTINUITY_REGISTRY_REFS),
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "constitution_bus_ref": CONSTITUTION_BUS_REF,
        "capability_bus_contract_ref": CAPABILITY_BUS_CONTRACT_REF,
        "provider_abstraction_ref": PROVIDER_ABS_STANDARD_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "world_continuity_whitebox_trace_requirement_v1",
        "information_integration_consumption_policy_ref": (
            "world_continuity_information_integration_handoff_plan_v1"
        ),
        "decision_center_consumption_policy_ref": "world_continuity_decision_center_handoff_plan_v1",
        "controlled_runtime_requirement_ref": CONTROLLED_RUNTIME_FRAMEWORK_REF,
        "memory_admission_requirement_ref_later": "world_continuity_memory_admission_boundary_plan_v1",
        "worldmodel_admission_requirement_ref_later": (
            "world_continuity_worldmodel_admission_boundary_plan_v1"
        ),
        "source_chain_requirement_ref": "world_continuity_source_chain_requirement_v1",
        "evidence_chain_requirement_ref": "world_continuity_evidence_chain_requirement_v1",
        "issue_trace_requirement_ref": "world_continuity_issue_trace_requirement_v1",
        "non_compliance_handling_policy_ref_later": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
        "model_selected_now": False,
        "model_invoked_now": False,
        "runtime_enabled_now": False,
        **meta,
    }

    ii_handoff = {
        "plan_id": "world_continuity_information_integration_handoff_plan_v1",
        "information_integration_ref": INFORMATION_INTEGRATION_REF,
        "consumes": [
            "scene_delta",
            "continuity_gap",
            "spatiotemporal_consistency",
            "missing_context_hypothesis",
        ],
        "confirmations": [
            "World Continuity outputs go to Information Integration as candidate/context/hypothesis",
            "Information Integration consumes scene_delta / continuity_gap / "
            "spatiotemporal_consistency / missing_context_hypothesis",
            "World Continuity cannot bypass Information Integration to WorldModel write",
            "no integrated_context generated now",
        ],
        **meta,
    }

    decision_handoff = {
        "plan_id": "world_continuity_decision_center_handoff_plan_v1",
        "decision_center_ref": DECISION_CENTER_REF,
        "handoff_via": ["integrated_context", "decision_request"],
        "confirmations": [
            "decision-relevant continuity outputs reach Decision Center only through "
            "integrated_context / decision_request",
            "World Continuity module cannot emit final decision",
            "continuity candidate cannot directly trigger navigation action",
            "no decision generated now",
        ],
        **meta,
    }

    worldmodel_boundary = {
        "plan_id": "world_continuity_worldmodel_admission_boundary_plan_v1",
        "confirmations": [
            "World Continuity module cannot write WorldModel",
            "world_continuity_candidate may become WorldModel admission candidate later",
            "stable world fact requires WorldModel Admission Gate",
            "scene_delta candidate is not world fact",
            "World Continuity candidate ≠ WorldModel fact",
            "no WorldModel write now",
        ],
        **meta,
    }

    memory_boundary = {
        "plan_id": "world_continuity_memory_admission_boundary_plan_v1",
        "confirmations": [
            "World Continuity module cannot write Memory",
            "stable environment memory later requires Memory Admission",
            "repeated continuity patterns may become memory candidate later",
            "scene_delta candidate ≠ Memory/WorldModel write",
            "no Memory write now",
        ],
        **meta,
    }

    layer_dependency_review = {
        "review_id": "world_continuity_layer_dependency_review_v1",
        "capability_layer": "Layer 2 Spatiotemporal Continuity",
        "supports_layer_1": "Current Scene Understanding",
        "supports_layer_3": "Navigation Application",
        "confirmations": [
            "Layer 2 depends on Layer 1 scene observations",
            "Layer 2 supports Layer 3 navigation application",
            "Layer 2 cannot override raw perception evidence",
            "Layer 2 cannot emit navigation action",
            "Layer 2 cannot write WorldModel without admission",
            "continuity hypothesis cannot become fact without evidence/admission",
            "World Continuity supports Layer 1 and Layer 3 but does not override either",
        ],
        "review_pass": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "world_continuity_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        **meta,
    }

    qualification_check = {
        "check_id": "world_continuity_module_qualification_check_v1",
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
        "plan_id": "world_continuity_module_model_profile_governance_binding_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "qualification_mode": QUALIFICATION_MODE,
        "objectives": [
            "qualification check only: verify World Continuity module sample is compliant",
            "generate world_continuity_module_model_profile_governance_binding_candidate",
            "verify World Continuity module definition / capability stack / layered governance mapping",
            "verify module-local model profile registry refs",
            "verify scene_delta / temporal_tracking / visual_map_alignment / STCM role assignment",
            "verify input/output contracts",
            "verify quality / health / validation / whitebox / provider-runtime / fallback",
            "verify WorldModel/Memory Admission boundary",
            "verify Layer 2 dependency on L1 and support for L3",
            "execute World Continuity module internal self-check + midplatform interaction check",
            "no health/supervision metric detail expansion",
            "no model select/download/invoke/benchmark",
            "no tracking/scene delta/visual-map alignment execution",
            "no WorldModel/Memory write / world fact generation / runtime enable",
        ],
        **meta,
    }

    planning_pass = qualification_check.get("qualification_pass")
    planning_decision = {
        "decision_id": "world_continuity_module_model_profile_governance_binding_planning_decision_v1",
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
        "policy_id": "world_continuity_module_model_profile_governance_binding_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "world_continuity_module_model_profile_governance_binding_planning_only": True,
        "qualification_check_only": True,
        "phase_goal": (
            "World Continuity module model profile + governance binding qualification planning "
            "confirmation only. World Continuity is Layer 2 Spatiotemporal Continuity. "
            "World Continuity candidate ≠ WorldModel fact; scene_delta candidate ≠ Memory/WorldModel write. "
            "No health/supervision metric expansion. No tracking/scene delta/visual-map alignment, "
            "no WorldModel/Memory write, no world fact generation, no runtime."
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
        "capability_layer": "Layer 2 Spatiotemporal Continuity",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_ref_count": len(WORLD_CONTINUITY_REGISTRY_REFS),
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
        "world_continuity_module_model_profile_governance_binding_planning_policy": policy,
        "upstream_map_navigation_module_input_review": upstream_review,
        "governance_standard_reuse_review": governance_reuse,
        "world_continuity_module_definition": module_definition,
        "world_continuity_capability_stack_definition": capability_stack,
        "world_continuity_layered_governance_mapping": layered_governance,
        "world_continuity_module_local_model_profile": module_local_profile,
        "world_continuity_model_profile_registry_refs_review": registry_refs_review,
        "world_continuity_model_role_assignment_plan": role_assignment,
        "world_continuity_input_contract": input_contract,
        "world_continuity_output_contract": output_contract,
        "world_continuity_quality_acceptance_plan": quality_plan,
        "world_continuity_health_validation_whitebox_plan": health_validation_whitebox,
        "world_continuity_provider_runtime_boundary_plan": provider_runtime_boundary,
        "world_continuity_fallback_replacement_plan": fallback_plan,
        "world_continuity_module_internal_self_check_plan": self_check_plan,
        "world_continuity_midplatform_interaction_check_plan": interaction_check_plan,
        "world_continuity_midplatform_governance_binding": midplatform_binding,
        "world_continuity_information_integration_handoff_plan": ii_handoff,
        "world_continuity_decision_center_handoff_plan": decision_handoff,
        "world_continuity_worldmodel_admission_boundary_plan": worldmodel_boundary,
        "world_continuity_memory_admission_boundary_plan": memory_boundary,
        "world_continuity_layer_dependency_review": layer_dependency_review,
        "world_continuity_module_qualification_check": qualification_check,
        "world_continuity_non_runtime_boundary_matrix": boundary_matrix,
        "world_continuity_module_model_profile_governance_binding_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "world_continuity_module_model_profile_governance_binding_planning_decision": planning_decision,
        "summary": summary,
    }
