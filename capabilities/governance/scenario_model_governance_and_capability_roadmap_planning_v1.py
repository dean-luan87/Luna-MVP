# -*- coding: utf-8 -*-
"""Scenario Model Governance and Capability Roadmap Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_scene_understanding_output_chain_closure_review_v1 import (
    FINAL_DECISION_GO as CLOSURE_REVIEW_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_user_output_gate_chain_dryrun_v1 import (
    FINAL_DECISION_GO as GATE_CHAIN_DR_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import (
    GOVERNANCE_ADDENDUM_ID,
    STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID,
)
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_PLUG_DR_FINAL_GO,
)

PHASE_ID = "Phase-Scenario-Model-Governance-and-Capability-Roadmap-Planning-v1-001"
SCOPE = "scenario_model_roadmap_planning_only"
SOURCE_CHAIN = "scenario_model_governance_and_capability_roadmap_planning_v1"

FINAL_DECISION_GO = (
    "SCENARIO_MODEL_GOVERNANCE_AND_CAPABILITY_ROADMAP_PLANNING_"
    "READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "SCENARIO_MODEL_GOVERNANCE_AND_CAPABILITY_ROADMAP_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Scenario-Model-Governance-and-Capability-Roadmap-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Scenario-Model-Governance-Issue-Review-v1-001"

GOAL_STAGES: Tuple[Dict[str, str], ...] = (
    {"stage_id": "stage_1", "stage_name": "Current Scene Understanding", "capability_layer": "layer_1"},
    {"stage_id": "stage_2", "stage_name": "Spatiotemporal Continuity / World Continuity", "capability_layer": "layer_2"},
    {"stage_id": "stage_3", "stage_name": "Navigation Application Layer", "capability_layer": "layer_3"},
    {"stage_id": "stage_4", "stage_name": "Extended Application Capabilities", "capability_layer": "layer_4"},
    {"stage_id": "stage_5", "stage_name": "Long-Term Social / Personal Capability", "capability_layer": "layer_5"},
    {"stage_id": "stage_6", "stage_name": "Evolutionary Recursion / Self-Improvement Proposal", "capability_layer": "layer_6_evolution"},
)

STAGE_CAPABILITIES: Dict[str, Tuple[str, ...]] = {
    "stage_1": (
        "object_detection", "target_recognition", "text_region_detection", "ocr_text_recognition",
        "scene_classification", "target_tracking", "visual_grounding",
        "task_intent_to_target_binding", "risk_candidate_detection",
    ),
    "stage_2": (
        "frame_sequence_understanding", "scene_delta", "temporal_tracking",
        "spatial_localization_candidate", "visual_map_alignment", "world_continuity_hypothesis",
        "missing_context_completion", "freshness_conflict_gap_detection", "survival_context_interpretation",
    ),
    "stage_3": (
        "route_context_reasoning", "location_context_alignment", "waypoint_facility_search",
        "crossing_obstacle_path_safety", "transit_indoor_navigation_context",
        "navigation_decision_readiness", "navigation_action_candidate_later",
    ),
    "stage_4": (
        "person_recognition_later", "multimodal_identity_candidate", "reading_text_capability",
        "document_signage_long_text_structure", "sensitive_scene_recognition", "privacy_aware_recognition",
    ),
    "stage_5": (
        "relationship_context_modeling", "personal_continuity_context", "emotion_state_modeling",
        "preference_habit_pattern_candidate", "long_term_identity_memory_linkage",
        "social_rhythm_expression_adaptation",
    ),
    "stage_6": (
        "product_feedback_analysis", "capability_gap_detection", "skill_expansion_proposal",
        "logic_revision_proposal", "code_optimization_proposal", "market_expectation_adaptation",
        "model_replacement_recommendation", "proposal_only_self_improvement",
    ),
}

MODEL_SOURCE_TYPES: Tuple[str, ...] = (
    "direct_open_source_or_external_provider",
    "reference_inspired_rebuild",
    "self_developed_core_capability",
)

MODULE_PROFILE_FIELDS: Tuple[str, ...] = (
    "module_id", "capability_domain", "capability_stack_ref", "model_profile_id", "model_role",
    "model_source_strategy", "model_name_candidate", "model_version", "model_license_ref",
    "model_update_policy_ref", "input_contract_ref", "output_contract_ref", "candidate_output_type",
    "confidence_semantics", "latency_budget", "resource_budget", "health_metrics_required",
    "validation_tests_required", "fallback_model_refs", "replacement_conditions",
    "provider_abstraction_ref", "governance_binding_ref", "no_direct_fact_action_output",
)

MIDPLATFORM_BINDING_FIELDS: Tuple[str, ...] = (
    "model_profile_ref", "capability_bus_contract_ref", "provider_abstraction_ref",
    "constitution_bus_ref", "layered_capability_stack_ref", "layered_governance_mapping_ref",
    "validation_requirement_ref", "health_requirement_ref", "whitebox_trace_requirement_ref",
    "decision_center_consumption_policy", "information_integration_consumption_policy",
    "controlled_runtime_requirement_ref", "memory_worldmodel_admission_policy_ref",
    "output_gate_requirement_ref", "version_compatibility_ref",
)

IO_INPUT_TYPES: Tuple[str, ...] = (
    "frame_candidate", "roi_candidate", "audio_candidate", "text_candidate", "map_context_candidate",
    "task_intent_candidate", "memory_context_candidate", "drive_signal_candidate",
    "integrated_context_candidate",
)

IO_OUTPUT_TYPES: Tuple[str, ...] = (
    "observation_candidate", "evidence_candidate", "recognition_candidate", "tracking_candidate",
    "transcript_candidate", "reading_candidate", "embedding_candidate", "scene_context_candidate",
    "risk_context_candidate", "proposal_candidate",
)

IO_FORBIDDEN_OUTPUTS: Tuple[str, ...] = (
    "direct_fact", "direct_action", "direct_user_output", "direct_memory_write",
    "direct_worldmodel_write", "direct_runtime_enable",
)

SCENARIO_IDS: Tuple[str, ...] = (
    "street_crossing_scene", "indoor_mall_facility_search", "hospital_department_search",
    "transit_bus_or_metro_navigation", "object_search_by_voice_task", "text_reading_scene",
    "person_recognition_later_scene", "home_host_assistant_scene", "emergency_risk_scene",
    "market_feedback_evolution_scene",
)

SCENARIO_STAGE_MAP: Dict[str, str] = {
    "street_crossing_scene": "stage_1",
    "indoor_mall_facility_search": "stage_3",
    "hospital_department_search": "stage_3",
    "transit_bus_or_metro_navigation": "stage_3",
    "object_search_by_voice_task": "stage_1",
    "text_reading_scene": "stage_4",
    "person_recognition_later_scene": "stage_4",
    "home_host_assistant_scene": "stage_5",
    "emergency_risk_scene": "stage_1",
    "market_feedback_evolution_scene": "stage_6",
}

ROADMAP_RISKS: Tuple[str, ...] = (
    "dependency_risk", "license_risk", "model_update_breakage", "provider_lock_in",
    "hallucination_false_recognition_risk", "identity_privacy_risk", "unsafe_navigation_risk",
    "memory_worldmodel_contamination", "auto_switch_instability", "overfitting_market_feedback",
    "model_becoming_universal_brain_risk", "module_bypassing_governance_risk",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Model Roadmap Planning GO ≠ model selected",
    "model candidate register ≠ provider invoked",
    "source strategy planned ≠ license cleared",
    "model version policy planned ≠ model registry implemented",
    "next DryRunAndReview ≠ benchmark or runtime",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("scenario_model_roadmap_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "model_selected_now", "model_downloaded_now", "model_invoked_now", "provider_invoked_now",
    "model_runtime_enabled_now", "benchmark_executed_now", "training_started_now",
    "fine_tuning_started_now", "code_generation_executed_now", "skill_added_now",
    "runtime_enabled_now", "memory_written_now", "world_model_written_now",
    "task_state_committed_now", "user_output_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "scenario_model_governance_and_capability_roadmap_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "mainline": "first_person_scene_understanding",
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


def run_scenario_model_governance_and_capability_roadmap_planning_v1(
    *,
    first_person_scene_understanding_output_chain_closure_review_root: str,
    first_person_scene_understanding_user_output_gate_chain_dryrun_root: str,
    first_person_scene_understanding_output_candidate_dryrun_root: str,
    first_person_scene_understanding_task_response_candidate_dryrun_root: str,
    first_person_scene_understanding_decision_chain_candidate_dryrun_root: str,
    first_person_scene_understanding_information_integration_chain_dryrun_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    seed_core_pluggable_layer_architecture_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    closure_pending = False

    closure_root = Path(
        first_person_scene_understanding_output_chain_closure_review_root
    ).expanduser().resolve()
    gate_root = Path(
        first_person_scene_understanding_user_output_gate_chain_dryrun_root
    ).expanduser().resolve()
    stack_root = Path(
        layered_capability_stack_standard_dryrun_and_review_root
    ).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    ds_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    sc_plug_root = Path(
        seed_core_pluggable_layer_architecture_dryrun_and_review_root
    ).expanduser().resolve()

    closure_vr = _try_read_json(closure_root / "verifier_report.json") or {}
    closure_sm = _try_read_json(closure_root / "summary.json") or {}
    gate_vr = _try_read_json(gate_root / "verifier_report.json") or {}
    stack_vr = _try_read_json(stack_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    ds_vr = _try_read_json(ds_root / "verifier_report.json") or {}
    sc_plug_vr = _try_read_json(sc_plug_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_closure_review_root": str(closure_root),
        "upstream_gate_chain_dryrun_root": str(gate_root),
        "output_root": str(out_root),
    }

    if closure_vr.get("verifier") == "GO":
        if closure_sm.get("final_decision") != CLOSURE_REVIEW_FINAL_GO:
            blockers.append("closure review final_decision mismatch")
    elif gate_vr.get("verifier") == "GO":
        closure_pending = True
        meta["closure_pending"] = True
    else:
        blockers.append("Output Chain Closure Review or Gate Chain DryRun must be GO")

    if stack_vr.get("verifier") != "GO":
        blockers.append("Layered Capability Stack Standard must be GO")
    if cb_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus must be GO")
    if provider_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction Standard must be GO")
    if ds_vr.get("verifier") != "GO":
        blockers.append("Seed Core Drive Signal Contract must be GO")
    if sc_plug_vr.get("verifier") != "GO":
        blockers.append("Seed Core Pluggable Layer Architecture must be GO")

    input_ok = len(blockers) == 0

    upstream_input = {
        "review_id": "upstream_output_chain_input_review_v1",
        "review_pass": input_ok,
        "closure_review_verifier": closure_vr.get("verifier"),
        "closure_review_final_decision": closure_sm.get("final_decision"),
        "closure_pending": closure_pending,
        "gate_chain_verifier": gate_vr.get("verifier"),
        "four_goal_priority_confirmed": True,
        "layered_stack_standard_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layered_governance_mapping_ref": ADDENDUM_ID,
        "constitution_bus_go": cb_vr.get("verifier") == "GO",
        "provider_abstraction_go": provider_vr.get("verifier") == "GO",
        "blockers": list(blockers),
        **meta,
    }

    luna_roadmap = {
        "roadmap_id": "luna_model_capability_roadmap_v1",
        "roadmap_name": "Luna Model Capability Roadmap",
        "principles": [
            "no immediate model integration",
            "build long-term model capability map first",
            "each model binds capability layer",
            "each model binds module-local model profile",
            "each model binds midplatform governance binding",
            "each model declares input/output contract",
            "each model declares version/update/replacement policy",
            "default output is candidate/evidence/signal/context not fact/action/user_output",
            "models are capability organs not Seed Core not Universal Brain",
        ],
        "goal_stages": list(GOAL_STAGES),
        "stage_count": len(GOAL_STAGES),
        **meta,
    }

    goal_matrix = {
        "matrix_id": "goal_stage_to_model_capability_matrix_v1",
        "stages": [
            {"stage_id": s["stage_id"], "stage_name": s["stage_name"], "required_capabilities": list(STAGE_CAPABILITIES[s["stage_id"]])}
            for s in GOAL_STAGES
        ],
        **meta,
    }

    source_taxonomy = {
        "taxonomy_id": "model_source_strategy_taxonomy_v1",
        "source_types": list(MODEL_SOURCE_TYPES),
        "direct_open_source_or_external_provider": {
            "description": "可直接使用或改造接入",
            "applies_to": [
                "object_detection", "ocr", "asr", "tts", "segmentation", "embedding",
                "face_detection_later", "tracking", "speech_diarization", "vlm_scene_captioning_candidate",
            ],
        },
        "reference_inspired_rebuild": {
            "description": "参考研究/产品机制，Luna 自己实现",
            "applies_to": [
                "world_continuity_reasoning", "spatiotemporal_consistency_manager", "scene_delta_governance",
                "target_search_orchestration", "multimodal_identity_fusion", "reading_comprehension_pipeline",
                "personal_continuity_protocol",
            ],
        },
        "self_developed_core_capability": {
            "description": "无外部模型可替代，必须 Luna 自研",
            "applies_to": [
                "seed_core", "survival_drive", "drive_signal_contract", "constitution_bus_governance",
                "layered_capability_stack_standard", "layered_governance_mapping", "personal_continuity_module",
                "evolutionary_recursion_governance", "luna_information_integration", "decision_center_governance",
                "capability_bus_governance",
            ],
        },
        **meta,
    }

    external_register = {
        "register_id": "external_open_source_candidate_register_v1",
        "register_only": True,
        "no_model_selected": True,
        "no_provider_invoked": True,
        "no_download": True,
        "no_benchmark_now": True,
        "candidates": [
            {"category": "object_detection", "candidates": ["yolo_family_candidate"]},
            {"category": "grounding_segmentation", "candidates": ["grounded_sam_style_candidate", "grounded_sam2_style_candidate"]},
            {"category": "ocr", "candidates": ["paddleocr_candidate", "rapidocr_candidate", "other_ocr_provider_candidate"]},
            {"category": "asr", "candidates": ["sensevoice_candidate", "whisper_like_candidate", "qwen_asr_style_candidate"]},
            {"category": "tts", "candidates": ["qianwen_tts_candidate", "moss_tts_style_candidate", "local_tts_candidate"]},
            {"category": "tracking", "candidates": ["object_tracking_candidate", "visual_tracker_candidate"]},
            {"category": "face_person_later", "candidates": ["face_detection_candidate", "embedding_candidate", "reid_candidate", "speaker_embedding_candidate"]},
            {"category": "vlm", "candidates": ["scene_understanding_candidate", "image_text_reasoning_candidate"]},
            {"category": "embedding_retrieval", "candidates": ["memory_library_embedding_candidate"]},
        ],
        "license_version_update_required_later": True,
        **meta,
    }

    reference_register = {
        "register_id": "reference_research_product_candidate_register_v1",
        "reference_not_dependency": True,
        "inspired_by_not_copied": True,
        "requires_later_source_review": True,
        "references": [
            "world_model_future_scene_prediction_inspiration",
            "first_person_video_understanding_inspiration",
            "embodied_agent_task_chain_inspiration",
            "mcp_tool_protocol_inspiration",
            "multimodal_memory_personal_continuity_inspiration",
            "scene_graph_spatial_semantic_map_inspiration",
            "dynamic_order_resource_allocation_inspiration",
            "ai_glasses_assistant_workflow_inspiration",
        ],
        **meta,
    }

    self_dev_register = {
        "register_id": "self_developed_core_capability_register_v1",
        "capabilities": [
            "luna_seed_core", "survival_drive", "emotion_engine_as_survival_submodule",
            "evolutionary_recursion_proposal_system", "personal_continuity_module",
            "constitution_bus_v1", "capability_bus_governance",
            "layered_capability_stack_standard", "layered_governance_mapping",
            "information_integration_layer", "decision_center_module",
            "whitebox_traceability_governance", "controlled_runtime_admission_governance",
            "memory_worldmodel_write_admission_governance",
        ],
        **meta,
    }

    scenario_matrix = {
        "matrix_id": "scene_model_requirement_matrix_v1",
        "scenarios": [
            {
                "scenario_id": sid,
                "goal_stage": SCENARIO_STAGE_MAP[sid],
                "required_capability_layers": [SCENARIO_STAGE_MAP[sid]],
                "required_model_roles": list(STAGE_CAPABILITIES.get(SCENARIO_STAGE_MAP[sid], ())[:4]),
                "candidate_model_sources": ["direct_open_source_or_external_provider", "reference_inspired_rebuild"],
                "input_contracts": ["frame_candidate", "task_intent_candidate"],
                "output_contracts": ["observation_candidate", "evidence_candidate"],
                "supervision_requirements": ["validation", "health", "whitebox"],
                "health_requirements": ["latency_budget", "failure_rate"],
                "validation_requirements": ["candidate_contract_compliance"],
                "whitebox_requirements": ["source_chain", "confidence", "ttl"],
                "controlled_runtime_requirements": ["admission_later_not_now"],
                "acceptance_criteria": ["candidate_only_compliance"],
                "fallback_strategy": "hold_or_degrade_candidate",
                "replacement_policy": "governance_review_required",
            }
            for sid in SCENARIO_IDS
        ],
        **meta,
    }

    module_profile_contract = {
        "contract_id": "module_local_model_profile_contract_v1",
        "required_fields": list(MODULE_PROFILE_FIELDS),
        "field_count": len(MODULE_PROFILE_FIELDS),
        "no_direct_fact_action_output_default": True,
        **meta,
    }

    midplatform_binding = {
        "contract_id": "midplatform_model_governance_binding_contract_v1",
        "required_fields": list(MIDPLATFORM_BINDING_FIELDS),
        "field_count": len(MIDPLATFORM_BINDING_FIELDS),
        "constitution_bus_ref": "luna_constitution_capability_bus_governance_v1",
        "layered_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layered_governance_ref": ADDENDUM_ID,
        "gate_chain_ref": GATE_CHAIN_SYSTEM_ID,
        **meta,
    }

    io_contract = {
        "standard_id": "model_input_output_contract_standard_v1",
        "input_types": list(IO_INPUT_TYPES),
        "output_types": list(IO_OUTPUT_TYPES),
        "required_output_metadata": ["confidence", "uncertainty", "ttl", "source_chain", "whitebox_trace"],
        "forbidden_outputs": list(IO_FORBIDDEN_OUTPUTS),
        **meta,
    }

    supervision_matrix = {
        "matrix_id": "model_supervision_requirement_matrix_v1",
        "requirements": [
            "constitution_constraints", "validation_tests", "health_metrics", "whitebox_trace",
            "provider_readiness", "controlled_runtime_admission", "privacy_identity_gate_if_applicable",
            "memory_worldmodel_admission_if_applicable", "layered_governance_mapping_by_layer",
        ],
        **meta,
    }

    acceptance_criteria = {
        "criteria_id": "model_quality_acceptance_criteria_v1",
        "criteria": [
            "accuracy_precision_recall_where_applicable", "latency_budget", "resource_cost", "stability",
            "failure_rate", "confidence_calibration", "hallucination_false_positive_control",
            "traceability_completeness", "candidate_contract_compliance", "degradation_behavior",
            "offline_capability_if_required", "privacy_compliance", "safety_critical_pass_criteria",
        ],
        **meta,
    }

    versioning_policy = {
        "policy_id": "model_versioning_and_update_policy_v1",
        "fields": [
            "model_id", "model_version", "provider_version", "registry_version",
            "source_url_or_origin_ref_later", "license_ref", "release_date_if_known_later",
            "update_frequency", "compatibility_policy", "breaking_change_policy", "rollback_policy",
            "benchmark_revalidation_required", "security_review_required", "deprecation_policy",
            "migration_notes",
        ],
        **meta,
    }

    replacement_policy = {
        "policy_id": "model_replacement_and_fallback_policy_v1",
        "replacement_triggers": [
            "health_degradation", "provider_unavailable", "license_risk", "performance_regression",
            "safety_failure", "latency_budget_failure", "hardware_incompatibility",
        ],
        "fallback_model_candidate": True,
        "hold_instead_of_fallback": True,
        "owner_governance_review_for_high_risk": True,
        "no_auto_switch_without_policy": True,
        **meta,
    }

    stack_mapping = {
        "mapping_id": "model_to_capability_stack_mapping_v1",
        "rules": [
            "each model maps to specific capability layer",
            "model cannot claim higher layer without lower-layer candidates",
            "application ability requires lower-layer model chain readiness",
            "navigation model roles are Stage 3 not Stage 1",
            "person recognition reading are Stage 4+",
            "evolutionary recursion proposal model is Stage 6 proposal-only",
        ],
        **meta,
    }

    governance_mapping = {
        "mapping_id": "model_to_governance_layer_mapping_v1",
        "rules": [
            "low-level perception → source_chain/confidence/ttl/validation",
            "continuity model → freshness/conflict/gap/evidence chain",
            "application model → decision/safety/task boundary",
            "identity/person model → privacy/identity/personal continuity gates",
            "long-term model → memory/worldmodel admission",
            "evolution model → owner/governance/validation/rollback",
        ],
        **meta,
    }

    def _stage_roadmap(stage_id: str, roadmap_id: str, items: Tuple[Tuple[str, str], ...]) -> Dict[str, Any]:
        return {
            "roadmap_id": roadmap_id,
            "goal_stage": stage_id,
            "model_roles": [
                {"role": role, "source_strategy": strategy} for role, strategy in items
            ],
            **meta,
        }

    fp_roadmap = _stage_roadmap(
        "stage_1", "first_person_scene_understanding_model_roadmap_v1",
        (
            ("object_detection_candidate", "direct_open_source_or_external_provider"),
            ("target_recognition_candidate", "direct_open_source_or_external_provider"),
            ("ocr_text_recognition_candidate", "direct_open_source_or_external_provider"),
            ("target_tracking_candidate", "direct_open_source_or_external_provider"),
            ("scene_classification_candidate", "direct_open_source_or_external_provider"),
            ("visual_grounding_candidate", "direct_open_source_or_external_provider"),
            ("voice_task_intent_binding", "reference_inspired_rebuild"),
            ("risk_candidate_detection", "reference_inspired_rebuild"),
        ),
    )

    st_roadmap = _stage_roadmap(
        "stage_2", "spatiotemporal_world_continuity_model_roadmap_v1",
        (
            ("temporal_tracking", "direct_open_source_or_external_provider"),
            ("scene_delta", "reference_inspired_rebuild"),
            ("visual_map_continuity", "reference_inspired_rebuild"),
            ("missing_context_hypothesis", "reference_inspired_rebuild"),
            ("world_continuity_candidate", "reference_inspired_rebuild"),
            ("spatiotemporal_consistency_manager", "self_developed_core_capability"),
        ),
    )
    st_roadmap["note"] = "多项需要 Luna 自研治理/整合，不是单模型替代"

    nav_roadmap = _stage_roadmap(
        "stage_3", "navigation_application_model_roadmap_v1",
        (
            ("route_reasoning", "reference_inspired_rebuild"),
            ("facility_search", "direct_open_source_or_external_provider"),
            ("transit_context", "reference_inspired_rebuild"),
            ("path_safety", "reference_inspired_rebuild"),
            ("navigation_readiness", "self_developed_core_capability"),
            ("navigation_action_candidate_later", "self_developed_core_capability"),
        ),
    )
    nav_roadmap["depends_on"] = ["stage_1", "stage_2"]

    ext_roadmap = _stage_roadmap(
        "stage_4", "extended_capability_model_roadmap_v1",
        (
            ("person_recognition_later", "direct_open_source_or_external_provider"),
            ("multimodal_identity_candidate", "reference_inspired_rebuild"),
            ("reading_capability", "direct_open_source_or_external_provider"),
            ("sensitive_scene_privacy_detection", "reference_inspired_rebuild"),
            ("long_text_document_structure", "direct_open_source_or_external_provider"),
        ),
    )
    ext_roadmap["requires_gates"] = ["privacy_gate", "identity_gate", "memory_admission_gate"]

    seed_boundary = {
        "boundary_id": "seed_core_and_evolution_model_boundary_v1",
        "confirmations": [
            "Seed Core not replaceable by external model",
            "Survival Drive not replaceable by external model",
            "Emotion Engine may use external signals but governance self-owned",
            "Evolutionary Recursion may use analysis models but proposal/governance self-owned",
            "external model cannot self-modify Luna",
            "code optimization proposal does not equal code modification",
            "skill expansion proposal does not equal skill added",
        ],
        **meta,
    }

    risk_register = {
        "register_id": "roadmap_risk_register_v1",
        "risks": list(ROADMAP_RISKS),
        "risk_count": len(ROADMAP_RISKS),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "roadmap_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate scenario_model_roadmap_candidate",
            "verify goal_stage_to_model_capability_matrix",
            "verify three model source strategies",
            "verify scene model requirement matrix",
            "verify module-local model profile + midplatform governance binding",
            "verify model version/update/replacement policies",
            "no model select/invoke/download",
        ],
        **meta,
    }

    planning_pass = input_ok
    planning_decision = {
        "decision_id": "scenario_model_roadmap_planning_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "scenario_model_roadmap_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "roadmap_planning_only_not_model_integration": True,
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
        "planning_pass": planning_pass,
        "closure_pending": closure_pending,
        "violations": list(blockers),
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "scenario_model_roadmap_planning_policy": policy,
        "upstream_output_chain_input_review": upstream_input,
        "luna_model_capability_roadmap": luna_roadmap,
        "goal_stage_to_model_capability_matrix": goal_matrix,
        "model_source_strategy_taxonomy": source_taxonomy,
        "external_open_source_candidate_register": external_register,
        "reference_research_product_candidate_register": reference_register,
        "self_developed_core_capability_register": self_dev_register,
        "scene_model_requirement_matrix": scenario_matrix,
        "module_local_model_profile_contract": module_profile_contract,
        "midplatform_model_governance_binding_contract": midplatform_binding,
        "model_input_output_contract_standard": io_contract,
        "model_supervision_requirement_matrix": supervision_matrix,
        "model_quality_acceptance_criteria": acceptance_criteria,
        "model_versioning_and_update_policy": versioning_policy,
        "model_replacement_and_fallback_policy": replacement_policy,
        "model_to_capability_stack_mapping": stack_mapping,
        "model_to_governance_layer_mapping": governance_mapping,
        "first_person_scene_understanding_model_roadmap": fp_roadmap,
        "spatiotemporal_world_continuity_model_roadmap": st_roadmap,
        "navigation_application_model_roadmap": nav_roadmap,
        "extended_capability_model_roadmap": ext_roadmap,
        "seed_core_and_evolution_model_boundary": seed_boundary,
        "roadmap_risk_register": risk_register,
        "roadmap_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "scenario_model_roadmap_planning_decision": planning_decision,
        "summary": summary,
    }
