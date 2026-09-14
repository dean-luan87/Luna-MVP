# -*- coding: utf-8 -*-
"""Vision Module Model Profile + Governance Binding Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_scene_understanding_output_chain_closure_review_v1 import (
    FINAL_DECISION_GO as FP_SCENE_CLOSURE_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as STACK_STD_DR_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
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
from capabilities.governance.model_profile_registry_planning_v1 import SEED_CANDIDATE_IDS
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
    DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
    FINAL_DECISION_GO as MODULE_LOCAL_DR_FINAL_GO,
)
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DUAL_VALIDATION_MECHANISM_ID,
    DUAL_VALIDATION_NON_CLAIMS,
    MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)

PHASE_ID = "Phase-Vision-Module-Model-Profile-Governance-Binding-Planning-v1-001"
SCOPE = "vision_module_model_profile_governance_binding_planning_only"
SOURCE_CHAIN = "vision_module_model_profile_governance_binding_planning_v1"

FINAL_DECISION_GO = (
    "VISION_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "VISION_MODULE_MODEL_PROFILE_GOVERNANCE_BINDING_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Vision-Module-Model-Profile-Governance-Binding-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Module-Model-Profile-Governance-Binding-Issue-Review-v1-001"

MODULE_ID = "vision_scene_understanding_module"
MODULE_LOCAL_PROFILE_ID = "vision_scene_understanding_module_local_profile_v1"
MIDPLATFORM_BINDING_ID = "vision_scene_understanding_midplatform_binding_v1"
CAPABILITY_STACK_DEF_ID = "vision_capability_stack_definition_v1"
LAYERED_GOV_MAPPING_ID = "vision_layered_governance_mapping_v1"
CAPABILITY_BUS_CONTRACT_REF = "vision_scene_understanding_capability_bus_contract_v1"

VISION_REGISTRY_REFS: Tuple[str, ...] = (
    "yolo_family_object_detection_candidate",
    "grounded_sam_style_grounding_segmentation_candidate",
    "visual_tracking_candidate",
    "vlm_scene_understanding_candidate",
)

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
    "Health Oversight Externality",
    "Whitebox Trace Standard",
    "Candidate/Evidence Contract pattern",
    "Boundary Matrix / Blocked Path / Non-Claims pattern",
)

IO_FORBIDDEN: Tuple[str, ...] = (
    "direct_fact",
    "direct_action",
    "direct_navigation_action",
    "direct_user_output",
    "direct_memory_write",
    "direct_worldmodel_write",
    "direct_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Vision Module Planning GO ≠ YOLO selected",
    "Grounded SAM candidate ref ≠ segmentation runtime",
    "VLM candidate ref ≠ scene model invoked",
    "Vision module profile planned ≠ camera/runtime enabled",
    "next DryRunAndReview ≠ model benchmark/runtime",
    "Vision Module Binding GO ≠ health metrics finalized",
    "Vision Module Binding GO ≠ supervision metrics finalized",
    "Module Governance Binding GO ≠ module fully integrated with Constitution",
    "Module Governance Binding GO ≠ module fully integrated with Health/Oversight",
    "Constitution binding feasible ≠ constitution effectiveness quantified",
    "Health/Oversight ref attached ≠ health metrics finalized",
    "Supervision ref attached ≠ supervision metrics finalized",
    "Module Internal Self-Check GO ≠ Midplatform Interaction Check GO",
    "Midplatform Interaction Check GO ≠ Runtime Ready",
)

QUALIFICATION_MODE = "Qualification Check, not Full Integration Certification"

QUALIFICATION_CHECK_CRITERIA: Tuple[str, ...] = (
    "references Model Profile Registry",
    "conforms to Module-local Model Profile Standard",
    "binds Midplatform Model Governance Binding",
    "Module Internal Self-Check planned",
    "Midplatform Interaction Check planned",
    "candidate_only maintained",
    "no model selected / invoked / runtime enabled",
    "no bypass of Constitution-Bus / Provider Abstraction / Validation / Health / "
    "Whitebox / Gate Chain / Controlled Runtime",
)

QUALIFICATION_FIELDS: Dict[str, bool] = {
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
    "module governance binding mechanism feasible",
    "Constitution-Bus constraints conveyable",
    "Health / Oversight supervision refs attachable",
    "Dual Validation mechanism executable",
)

CLOSURE_CANNOT_SAY: Tuple[str, ...] = (
    "module fully integrated with Constitution",
    "module fully integrated with Health/Oversight",
    "health metrics system completed",
    "supervision metrics system completed",
    "constitution execution effectiveness quantified",
    "oversight effectiveness quantified",
    "health score accuracy validated",
    "supervision intensity reasonableness validated",
    "model performance达标",
    "constitution execution behavior optimization validated",
    "long-term oversight anomaly detection validated",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "vision_module_model_profile_governance_binding_planning_only",
    "qualification_check_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "vision_module_runtime_enabled_now",
    "camera_invoked_now",
    "real_frame_read_now",
    "model_selected_now",
    "model_downloaded_now",
    "model_invoked_now",
    "provider_invoked_now",
    "benchmark_executed_now",
    "license_cleared_now",
    "security_review_completed_now",
    "visual_fact_generated_now",
    "visual_action_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
    "health_metric_detail_defined_now",
    "supervision_metric_detail_defined_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_module_model_profile_governance_binding_planning"
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


def run_vision_module_model_profile_governance_binding_planning_v1(
    *,
    midplatform_model_governance_binding_standardization_dryrun_and_review_root: str,
    midplatform_model_governance_binding_standardization_planning_root: str,
    module_local_model_profile_standardization_dryrun_and_review_root: str,
    model_profile_registry_dryrun_and_review_root: str,
    first_person_scene_understanding_output_chain_closure_review_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    binding_dr_root = Path(
        midplatform_model_governance_binding_standardization_dryrun_and_review_root
    ).expanduser().resolve()
    binding_plan_root = Path(
        midplatform_model_governance_binding_standardization_planning_root
    ).expanduser().resolve()
    ml_dr_root = Path(
        module_local_model_profile_standardization_dryrun_and_review_root
    ).expanduser().resolve()
    registry_dr_root = Path(model_profile_registry_dryrun_and_review_root).expanduser().resolve()
    fp_closure_root = Path(
        first_person_scene_understanding_output_chain_closure_review_root
    ).expanduser().resolve()
    stack_root = Path(layered_capability_stack_standard_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    binding_dr_vr = _try_read_json(binding_dr_root / "verifier_report.json") or {}
    binding_dr_sm = _try_read_json(binding_dr_root / "summary.json") or {}
    ml_dr_vr = _try_read_json(ml_dr_root / "verifier_report.json") or {}
    registry_dr_vr = _try_read_json(registry_dr_root / "verifier_report.json") or {}
    registry_dr_sm = _try_read_json(registry_dr_root / "summary.json") or {}
    fp_closure_vr = _try_read_json(fp_closure_root / "verifier_report.json") or {}
    fp_closure_sm = _try_read_json(fp_closure_root / "summary.json") or {}
    stack_vr = _try_read_json(stack_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}

    seeds_review = _try_read_json(registry_dr_root / "seed_model_profile_candidates_review_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {**_planning_meta(), "output_root": str(out_root)}

    if binding_dr_vr.get("verifier") != "GO":
        blockers.append("Midplatform Binding DryRunAndReview must be GO")
    if binding_dr_sm.get("final_decision") != BINDING_DR_FINAL_GO:
        blockers.append("Midplatform Binding DryRun final_decision mismatch")
    if ml_dr_vr.get("verifier") != "GO":
        blockers.append("Module-Local DryRunAndReview must be GO")
    if registry_dr_vr.get("verifier") != "GO":
        blockers.append("Model Profile Registry DryRunAndReview must be GO")
    if registry_dr_sm.get("final_decision") != REGISTRY_DR_FINAL_GO:
        blockers.append("Registry DryRun final_decision mismatch")
    if fp_closure_vr.get("verifier") != "GO":
        blockers.append("First-Person Scene Understanding Output Chain Closure Review must be GO")
    if fp_closure_sm.get("final_decision") != FP_SCENE_CLOSURE_FINAL_GO:
        blockers.append("FP Scene Closure final_decision mismatch")
    if stack_vr.get("verifier") != "GO":
        blockers.append("Layered Capability Stack Standard must be GO")
    if cb_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if provider_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction Standard must be GO")
    if cr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime Framework must be GO")

    for ref in VISION_REGISTRY_REFS:
        if ref not in SEED_CANDIDATE_IDS:
            blockers.append(f"registry ref {ref} not in seed candidates")

    input_ok = len(blockers) == 0 and seeds_review.get("review_pass") is not False

    upstream_review = {
        "review_id": "upstream_binding_standard_input_review_v1",
        "binding_dryrun_verifier": binding_dr_vr.get("verifier"),
        "binding_dryrun_final_decision": binding_dr_sm.get("final_decision"),
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "module_local_dryrun_verifier": ml_dr_vr.get("verifier"),
        "registry_dryrun_verifier": registry_dr_vr.get("verifier"),
        "fp_scene_closure_verifier": fp_closure_vr.get("verifier"),
        "fp_scene_closure_final_decision": fp_closure_sm.get("final_decision"),
        "stack_std_verifier": stack_vr.get("verifier"),
        "constitution_bus_verifier": cb_vr.get("verifier"),
        "provider_abs_verifier": provider_vr.get("verifier"),
        "controlled_runtime_verifier": cr_vr.get("verifier"),
        "non_compliant_module_model_handling_policy_deferred": True,
        "deferred_policy_ref": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
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
        "vision_module_planning_not_new_framework": True,
        **meta,
    }

    module_definition = {
        "definition_id": "vision_module_definition_v1",
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "First-Person Vision / Scene Understanding",
        "product_layer_relevance": ["Badge", "Glasses", "Phone", "Robot later"],
        "primary_goal": "Current Scene Understanding",
        "secondary_goal": "Spatiotemporal Continuity later",
        "application_dependency": "Navigation Application Layer later",
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "runtime_enabled_now": False,
        "provider_invoked_now": False,
        "candidate_only": True,
        "confirmations": [
            "Vision module does not directly output navigation action",
            "Vision module does not directly output fact",
            "Vision module does not write Memory/WorldModel",
            "Vision module outputs enter Information Integration",
        ],
        **meta,
    }

    capability_stack = {
        "definition_id": CAPABILITY_STACK_DEF_ID,
        "module_id": MODULE_ID,
        "universal_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layers": {
            "layer_1_current_scene_understanding": {
                "layer_id": "layer_1_perception",
                "outputs": [
                    "visual_observation_candidate",
                    "target_recognition_candidate",
                    "scene_context_candidate",
                    "risk_context_candidate",
                    "text_region_need_candidate",
                ],
                "status": "primary_now",
            },
            "layer_2_spatiotemporal_continuity_later": {
                "layer_id": "layer_2_spatiotemporal",
                "outputs": [
                    "target_tracking_candidate",
                    "scene_delta_candidate",
                    "visual_sequence_context_candidate",
                    "continuity_gap_candidate",
                ],
                "status": "later",
            },
            "layer_3_navigation_application_dependency_later": {
                "layer_id": "layer_3_navigation",
                "outputs": [
                    "route_visual_context_candidate",
                    "crossing_context_candidate",
                    "obstacle_context_candidate",
                ],
                "status": "dependency_later",
            },
            "layer_4_extended_later": {
                "layer_id": "layer_4_extended",
                "outputs": [
                    "person_recognition later",
                    "reading_visual_support later",
                ],
                "status": "later",
            },
        },
        "forbidden": [
            "no direct navigation action",
            "no direct fact",
            "no Memory/WorldModel write",
        ],
        **meta,
    }

    layered_governance = {
        "mapping_id": LAYERED_GOV_MAPPING_ID,
        "module_id": MODULE_ID,
        "universal_mapping_ref": ADDENDUM_ID,
        "layers": {
            "L1": {
                "requirements": ["source_chain", "confidence", "ttl", "candidate_only", "not_fact"],
            },
            "L2": {
                "requirements": [
                    "freshness", "conflict", "gap", "temporal consistency", "evidence chain",
                ],
            },
            "L3": {
                "requirements": [
                    "safety context", "forbidden navigation action", "Decision Center handoff",
                ],
            },
            "L4": {
                "requirements": ["privacy/identity gates later", "person recognition deferred"],
            },
        },
        "confirmations": [
            "governance principles consistent",
            "execution intensity layered",
            "no all-rules-to-all-layers overload",
            "no weakened constitution by layer",
        ],
        **meta,
    }

    module_local_profile = {
        "module_local_profile_id": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "module_type": "pluggable_capability_module",
        "capability_domain": "First-Person Vision / Scene Understanding",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(VISION_REGISTRY_REFS),
        "capability_stack_ref": CAPABILITY_STACK_DEF_ID,
        "layered_governance_mapping_ref": LAYERED_GOV_MAPPING_ID,
        "model_role_in_module": {
            "yolo_family_object_detection_candidate": "object_detection_candidate",
            "grounded_sam_style_grounding_segmentation_candidate": "grounding_segmentation_candidate_later",
            "visual_tracking_candidate": "visual_tracking_candidate_later",
            "vlm_scene_understanding_candidate": "scene_understanding_candidate_later",
        },
        "model_source_strategy": {
            "yolo_family_object_detection_candidate": "A_direct_open_source_or_external_provider",
            "grounded_sam_style_grounding_segmentation_candidate": "A_direct_open_source_or_external_provider",
            "visual_tracking_candidate": "A_direct_open_source_or_external_provider",
            "vlm_scene_understanding_candidate": "B_reference_inspired_rebuild",
        },
        "candidate_output_type": "visual_candidate/evidence/context",
        "model_profile_status": "candidate_registered",
        "midplatform_governance_binding_ref": MIDPLATFORM_BINDING_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "vision_whitebox_trace_requirement_v1",
        "provider_abstraction_ref": PROVIDER_ABS_STANDARD_ID,
        "controlled_runtime_requirement_ref": CONTROLLED_RUNTIME_FRAMEWORK_REF,
        "quality_acceptance_ref": "vision_quality_acceptance_plan_v1",
        "fallback_model_profile_refs": list(VISION_REGISTRY_REFS),
        "no_registry_override": True,
        "no_model_selection_by_module": True,
        "no_model_invocation_by_profile": True,
        "no_direct_fact_action_output": True,
        "model_selected_now": False,
        "model_invoked_now": False,
        **meta,
    }

    registry_refs_review = {
        "review_id": "vision_model_profile_registry_refs_review_v1",
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_refs": list(VISION_REGISTRY_REFS),
        "seed_candidates_in_registry": [
            {"ref": ref, "in_seed_list": ref in SEED_CANDIDATE_IDS, "candidate_only": True,
             "selected_now": False, "invoked_now": False}
            for ref in VISION_REGISTRY_REFS
        ],
        "confirmations": [
            "all registry refs exist in luna_model_profile_registry_v1 seed candidates",
            "yolo_family_object_detection_candidate is candidate only",
            "grounded_sam_style_grounding_segmentation_candidate is candidate only",
            "visual_tracking_candidate is candidate only",
            "vlm_scene_understanding_candidate is candidate only",
            "none selected_now",
            "none invoked_now",
            "license/version/profile completeness later",
        ],
        "review_pass": all(ref in SEED_CANDIDATE_IDS for ref in VISION_REGISTRY_REFS),
        **meta,
    }

    role_assignment = {
        "plan_id": "vision_model_role_assignment_plan_v1",
        "assignments": [
            {
                "registry_ref": "yolo_family_object_detection_candidate",
                "role": "object_detection_candidate",
                "capability_layer": "layer_1_current_scene_understanding",
                "status": "primary_candidate_now",
            },
            {
                "registry_ref": "grounded_sam_style_grounding_segmentation_candidate",
                "role": "grounding/segmentation later",
                "capability_layer": "layer_1_current_scene_understanding",
                "status": "later",
            },
            {
                "registry_ref": "visual_tracking_candidate",
                "role": "temporal target tracking later",
                "capability_layer": "layer_2_spatiotemporal_continuity_later",
                "status": "later",
            },
            {
                "registry_ref": "vlm_scene_understanding_candidate",
                "role": "scene understanding candidate later",
                "capability_layer": "layer_1_current_scene_understanding",
                "status": "later",
            },
        ],
        "confirmations": [
            "YOLO-family maps to object detection candidate role",
            "Grounded SAM style maps to grounding/segmentation later role",
            "visual tracking maps to temporal target tracking later role",
            "VLM maps to scene understanding candidate later role",
            "no single model owns full Vision module",
            "no universal vision brain",
            "roles are capability-layer specific",
        ],
        **meta,
    }

    input_contract = {
        "contract_id": "vision_input_contract_v1",
        "module_id": MODULE_ID,
        "allowed_inputs": [
            "frame_candidate_later",
            "roi_candidate_later",
            "task_intent_candidate",
            "required_observation_candidate",
            "drive_signal_candidate",
            "map_context_candidate_later",
            "provider_context_candidate_later",
        ],
        "forbidden_inputs_now": [
            "real_frame",
            "camera_source_direct",
        ],
        "confirmations": [
            "real_frame input not allowed now",
            "camera source not invoked now",
            "frame_candidate_later requires Controlled Runtime later",
        ],
        **meta,
    }

    output_contract = {
        "contract_id": "vision_output_contract_v1",
        "module_id": MODULE_ID,
        "allowed_outputs": [
            "visual_observation_candidate",
            "target_recognition_candidate",
            "scene_context_candidate",
            "risk_context_candidate",
            "obstacle_candidate",
            "text_region_need_candidate",
            "target_tracking_candidate_later",
            "visual_evidence_candidate",
            "visual_sequence_context_candidate_later",
        ],
        "forbidden_outputs": list(IO_FORBIDDEN),
        "handoff_target": INFORMATION_INTEGRATION_REF,
        **meta,
    }

    quality_plan = {
        "plan_id": "vision_quality_acceptance_plan_v1",
        "requirements": [
            "object_detection_precision_target_later",
            "false_positive_control_requirement",
            "false_negative_control_requirement",
            "latency_budget_later",
            "resource_budget_later",
            "confidence_calibration_required",
        ],
        "candidate_contract_compliance_required": True,
        "traceability_completeness_required": True,
        "degradation_behavior_required": True,
        "benchmark_required_later": True,
        "benchmark_executed_now": False,
        **meta,
    }

    health_validation_whitebox = {
        "plan_id": "vision_health_validation_whitebox_plan_v1",
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "vision_whitebox_trace_requirement_v1",
        "source_chain_required": True,
        "evidence_refs_required": True,
        "failure_route_required": True,
        "issue_trace_required": True,
        "health_status_ref_transport_only": True,
        "module_cannot_self_certify_health": True,
        "health_metric_detail_defined_now": False,
        "supervision_metric_detail_defined_now": False,
        "scope_note": "ref slots only; metric detail deferred to Health-and-Supervision-Metrics phase",
        **meta,
    }

    provider_runtime_boundary = {
        "plan_id": "vision_provider_runtime_boundary_plan_v1",
        "provider_abstraction_required": True,
        "controlled_runtime_required": True,
        "confirmations": [
            "provider_candidate ≠ selected ≠ invoked",
            "no provider auto-switch",
            "camera invocation requires Controlled Runtime later",
            "real frame read requires Controlled Runtime later",
            "Vision runtime remains disabled now",
        ],
        **meta,
    }

    fallback_plan = {
        "plan_id": "vision_fallback_replacement_plan_v1",
        "fallback_model_profile_refs": list(VISION_REGISTRY_REFS),
        "replacement_conditions": [
            "quality_regression",
            "provider_unavailable",
            "license_risk",
            "latency_budget_failure",
            "hardware_incompatibility",
            "safety_false_negative_risk",
        ],
        "hold_instead_of_fallback_when": "safety-critical uncertainty",
        "no_auto_switch_without_governance_policy": True,
        "replacement_does_not_imply_invocation": True,
        **meta,
    }

    self_check_plan = {
        "plan_id": "vision_module_internal_self_check_plan_v1",
        "mechanism_layer": "Module Internal Self-Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "Vision 模块内部是否按标准写好 profile / contract / binding refs",
        "self_check_coverage": list(MODULE_INTERNAL_SELF_CHECK_COVERAGE),
        "rules": [
            "自检不授权 runtime",
            "自检不选择模型",
            "自检不调用 camera/provider",
            "自检不写 Memory / WorldModel",
            "自检不生成 visual fact / action / user output",
        ],
        "does_not_replace": "Midplatform Interaction Check",
        **meta,
    }

    interaction_check_plan = {
        "plan_id": "vision_midplatform_interaction_check_plan_v1",
        "mechanism_layer": "Midplatform Interaction Check",
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "purpose": "Vision 模块与中台交互是否合规、无绕路",
        "interaction_check_coverage": list(MIDPLATFORM_INTERACTION_CHECK_COVERAGE),
        "rules": [
            "中台检验不等于 runtime 授权",
            "中台检验不等于模型选择",
            "中台检验不等于 camera/provider invocation",
        ],
        "does_not_replace": "Module Internal Self-Check",
        **meta,
    }

    midplatform_binding = {
        "midplatform_governance_binding_id": MIDPLATFORM_BINDING_ID,
        "module_local_profile_ref": MODULE_LOCAL_PROFILE_ID,
        "module_id": MODULE_ID,
        "registry_model_profile_refs": list(VISION_REGISTRY_REFS),
        "registry_ref": REGISTRY_REF,
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "capability_stack_ref": CAPABILITY_STACK_DEF_ID,
        "layered_governance_mapping_ref": LAYERED_GOV_MAPPING_ID,
        "constitution_bus_ref": CONSTITUTION_BUS_REF,
        "capability_bus_contract_ref": CAPABILITY_BUS_CONTRACT_REF,
        "provider_abstraction_ref": PROVIDER_ABS_STANDARD_ID,
        "validation_requirement_ref": "required_later",
        "health_requirement_ref": "required_later",
        "supervision_metric_ref": "required_later",
        "whitebox_trace_requirement_ref": "vision_whitebox_trace_requirement_v1",
        "information_integration_consumption_policy_ref": "vision_information_integration_handoff_plan_v1",
        "decision_center_consumption_policy_ref": "vision_decision_center_handoff_plan_v1",
        "gate_chain_requirement_ref_later": GATE_CHAIN_SYSTEM_ID,
        "controlled_runtime_requirement_ref": CONTROLLED_RUNTIME_FRAMEWORK_REF,
        "memory_admission_requirement_ref_later": "memory_admission_gate_later",
        "worldmodel_admission_requirement_ref_later": "worldmodel_admission_gate_later",
        "source_chain_requirement_ref": "vision_source_chain_requirement_v1",
        "evidence_requirement_ref": "vision_evidence_requirement_v1",
        "issue_trace_requirement_ref": "vision_issue_trace_requirement_v1",
        "non_compliance_handling_policy_ref_later": DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
        "model_selected_now": False,
        "model_invoked_now": False,
        "runtime_enabled_now": False,
        **meta,
    }

    ii_handoff = {
        "plan_id": "vision_information_integration_handoff_plan_v1",
        "information_integration_ref": INFORMATION_INTEGRATION_REF,
        "consumes": [
            "visual_observation_candidate",
            "target_recognition_candidate",
            "scene_context_candidate",
            "risk_context_candidate",
            "text_region_need_candidate",
        ],
        "confirmations": [
            "visual outputs go to Information Integration as candidate/context/evidence",
            "Vision module cannot bypass Information Integration to Decision Center unless policy later",
            "no integrated_context generated now",
        ],
        **meta,
    }

    decision_handoff = {
        "plan_id": "vision_decision_center_handoff_plan_v1",
        "decision_center_ref": DECISION_CENTER_REF,
        "handoff_via": ["integrated_context", "decision_request"],
        "confirmations": [
            "decision-relevant visual outputs reach Decision Center only through "
            "integrated_context / decision_request",
            "Vision module cannot emit decision",
            "no decision generated now",
        ],
        **meta,
    }

    gate_chain_boundary = {
        "plan_id": "vision_gate_chain_boundary_plan_v1",
        "gate_chain_system_ref": GATE_CHAIN_SYSTEM_ID,
        "output_capable_now": False,
        "confirmations": [
            "Vision module not output-capable now",
            "if visual output becomes user-facing later, Output/Gate chain required",
            "no user_output now",
            "Privacy/Identity gates later for person recognition",
        ],
        **meta,
    }

    memory_wm_boundary = {
        "plan_id": "vision_memory_worldmodel_admission_boundary_plan_v1",
        "confirmations": [
            "Vision module cannot write Memory",
            "Vision module cannot write WorldModel",
            "visual evidence may be admission candidate later",
            "WorldModel fact admission later required",
            "person recognition later requires Identity/Privacy gates",
        ],
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "vision_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "vision_module_model_profile_governance_binding_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "qualification_mode": QUALIFICATION_MODE,
        "objectives": [
            "qualification check only: verify Vision module sample is compliant",
            "verify registry / module-local standard / midplatform binding refs",
            "verify dual validation plans (self-check + interaction check)",
            "verify candidate-only and no runtime/model/provider/camera",
            "verify no bypass of Constitution-Bus / Provider / Validation / Health / Whitebox / Gate / CR",
            "verify health/supervision refs attached as required_later only",
            "no health metric detail expansion",
            "no supervision metric detail expansion",
            "no model capability roadmap expansion",
        ],
        **meta,
    }

    qualification_check = {
        "check_id": "vision_module_qualification_check_v1",
        "qualification_mode": QUALIFICATION_MODE,
        "criteria": list(QUALIFICATION_CHECK_CRITERIA),
        "criteria_count": len(QUALIFICATION_CHECK_CRITERIA),
        "qualification_fields": dict(QUALIFICATION_FIELDS),
        "can_say": list(CLOSURE_CAN_SAY),
        "cannot_say": list(CLOSURE_CANNOT_SAY),
        "qualification_pass": input_ok and registry_refs_review.get("review_pass"),
        **meta,
    }

    planning_pass = qualification_check.get("qualification_pass")
    planning_decision = {
        "decision_id": "vision_module_model_profile_governance_binding_planning_decision_v1",
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
        "policy_id": "vision_module_model_profile_governance_binding_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "vision_module_model_profile_governance_binding_planning_only": True,
        "qualification_check_only": True,
        "phase_goal": (
            "Vision module model profile + governance binding qualification planning confirmation only. "
            "Verify required refs and boundary declarations against closed standards. "
            "No health/supervision metric detail expansion. No new governance framework. No model/runtime."
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
        "registry_ref": REGISTRY_REF,
        "registry_model_profile_ref_count": len(VISION_REGISTRY_REFS),
        "midplatform_binding_standard_ref": MIDPLATFORM_BINDING_STANDARD_ID,
        "module_local_profile_standard_ref": MODULE_LOCAL_PROFILE_STANDARD_REF,
        "dual_validation_mechanism_ref": DUAL_VALIDATION_MECHANISM_ID,
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_check_only": True,
        "non_compliant_module_model_handling_policy_deferred": True,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "vision_module_model_profile_governance_binding_planning_policy": policy,
        "upstream_binding_standard_input_review": upstream_review,
        "governance_standard_reuse_review": governance_reuse,
        "vision_module_definition": module_definition,
        "vision_capability_stack_definition": capability_stack,
        "vision_layered_governance_mapping": layered_governance,
        "vision_module_local_model_profile": module_local_profile,
        "vision_model_profile_registry_refs_review": registry_refs_review,
        "vision_model_role_assignment_plan": role_assignment,
        "vision_input_contract": input_contract,
        "vision_output_contract": output_contract,
        "vision_quality_acceptance_plan": quality_plan,
        "vision_health_validation_whitebox_plan": health_validation_whitebox,
        "vision_provider_runtime_boundary_plan": provider_runtime_boundary,
        "vision_fallback_replacement_plan": fallback_plan,
        "vision_module_internal_self_check_plan": self_check_plan,
        "vision_midplatform_interaction_check_plan": interaction_check_plan,
        "vision_midplatform_governance_binding": midplatform_binding,
        "vision_information_integration_handoff_plan": ii_handoff,
        "vision_decision_center_handoff_plan": decision_handoff,
        "vision_gate_chain_boundary_plan": gate_chain_boundary,
        "vision_memory_worldmodel_admission_boundary_plan": memory_wm_boundary,
        "vision_non_runtime_boundary_matrix": boundary_matrix,
        "vision_module_qualification_check": qualification_check,
        "vision_module_model_profile_governance_binding_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "vision_module_model_profile_governance_binding_planning_decision": planning_decision,
        "summary": summary,
    }
