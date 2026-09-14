# -*- coding: utf-8 -*-
"""Model Profile Registry Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONTROLLED_RUNTIME_DR_FINAL_GO,
)
from capabilities.governance.scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as ROADMAP_DR_FINAL_GO,
)
from capabilities.governance.scenario_model_capability_roadmap_current_state_inventory_planning_v1 import (
    CAPABILITY_DOMAIN_IDS,
    MIDPLATFORM_BINDING_FIELDS,
    MODEL_SOURCE_TYPES,
    MODULE_PROFILE_FIELDS,
)

PHASE_ID = "Phase-Model-Profile-Registry-Planning-v1-001"
SCOPE = "model_profile_registry_planning_only"
SOURCE_CHAIN = "model_profile_registry_planning_v1"

FINAL_DECISION_GO = "MODEL_PROFILE_REGISTRY_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MODEL_PROFILE_REGISTRY_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Model-Profile-Registry-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Model-Profile-Registry-Issue-Review-v1-001"

MODEL_PROFILE_SCHEMA_FIELDS: Tuple[str, ...] = (
    "model_profile_id", "model_name_candidate", "model_family", "capability_domain",
    "goal_stage", "capability_stack_layer", "model_role", "model_source_strategy",
    "current_status", "provider_candidate_ref", "module_local_profile_ref",
    "midplatform_governance_binding_ref", "input_contract_refs", "output_contract_refs",
    "expected_output_type", "confidence_semantics", "ttl_semantics",
    "source_chain_required", "whitebox_trace_required", "version_metadata_ref",
    "license_metadata_ref", "update_policy_ref", "quality_acceptance_ref",
    "health_validation_whitebox_ref", "fallback_replacement_ref",
    "controlled_runtime_requirement_ref", "privacy_identity_requirement_ref",
    "memory_worldmodel_admission_requirement_ref", "no_direct_fact_action_output",
    "selected_now", "invoked_now", "runtime_enabled_now",
)

LIFECYCLE_STATES: Tuple[str, ...] = (
    "proposed", "candidate_registered", "profile_incomplete", "profile_complete_candidate",
    "license_review_required", "security_review_required", "benchmark_required",
    "governance_binding_required", "controlled_runtime_readiness_required",
    "selected_later", "deprecated_later", "blocked",
)

STATUS_TAXONOMY: Tuple[str, ...] = (
    "not_started", "planned_only", "candidate_registered", "profile_required",
    "profile_draft", "profile_complete_candidate", "blocked", "deferred",
    "selected_later", "invoked_later", "deprecated_later",
)

LICENSE_METADATA_FIELDS: Tuple[str, ...] = (
    "source_strategy", "source_origin_ref", "source_url_later", "model_author_or_org",
    "license_type", "license_ref", "commercial_use_allowed_unknown_by_default",
    "redistribution_allowed_unknown_by_default", "modification_allowed_unknown_by_default",
    "attribution_required_unknown_by_default", "license_review_status",
    "security_review_status", "data_policy_review_status", "update_tracking_required",
)

LAYER_BINDING_FIELDS: Tuple[str, ...] = (
    "capability_domain", "goal_stage", "capability_stack_ref", "capability_stack_layer",
    "lower_layer_dependencies", "layered_governance_mapping_ref", "allowed_layer_outputs",
    "forbidden_layer_outputs", "application_layer_flag", "foundation_layer_flag",
    "cannot_claim_higher_layer_without_lower_layer",
)

IO_INPUT_TYPES: Tuple[str, ...] = (
    "frame_candidate", "roi_candidate", "audio_candidate", "text_candidate",
    "map_context_candidate", "task_intent_candidate", "memory_context_candidate",
    "drive_signal_candidate", "integrated_context_candidate", "provider_context_candidate",
)

IO_OUTPUT_TYPES: Tuple[str, ...] = (
    "observation_candidate", "evidence_candidate", "recognition_candidate",
    "tracking_candidate", "transcript_candidate", "reading_candidate", "embedding_candidate",
    "scene_context_candidate", "risk_context_candidate", "proposal_candidate",
)

IO_FORBIDDEN: Tuple[str, ...] = (
    "direct_fact", "direct_action", "direct_user_output", "direct_memory_write",
    "direct_worldmodel_write", "direct_runtime_enable",
)

QUALITY_PROFILE_FIELDS: Tuple[str, ...] = (
    "accuracy_target_later", "precision_target_later", "recall_target_later", "latency_budget",
    "resource_budget", "memory_budget", "power_budget", "stability_requirement",
    "failure_rate_threshold_later", "confidence_calibration_requirement",
    "false_positive_control_requirement", "false_negative_control_requirement",
    "traceability_completeness_requirement", "candidate_contract_compliance_required",
    "degradation_behavior_required", "offline_capability_requirement",
    "privacy_compliance_requirement", "safety_critical_requirement",
)

HEALTH_VALIDATION_FIELDS: Tuple[str, ...] = (
    "health_metrics_required", "health_status_ref_required", "validation_tests_required",
    "validation_gate_ref", "whitebox_trace_required", "whitebox_explainability_level",
    "failure_route_required", "issue_trace_required", "health_oversight_external_to_bus",
    "bus_transports_health_ref_not_judges",
)

PROVIDER_RUNTIME_BINDING_FIELDS: Tuple[str, ...] = (
    "provider_abstraction_required", "provider_candidate_ref", "runtime_candidate_ref",
    "controlled_runtime_required", "authorization_required_later",
    "provider_readiness_required_later", "no_provider_auto_switch_without_policy",
    "runtime_invocation_allowed_now",
)

VERSION_REPLACEMENT_FIELDS: Tuple[str, ...] = (
    "model_id", "model_version", "provider_version", "registry_version", "release_date_later",
    "update_frequency", "compatibility_policy", "breaking_change_policy", "rollback_policy",
    "benchmark_revalidation_required", "security_review_required", "deprecation_policy",
    "replacement_trigger", "fallback_model_candidate_refs", "hold_instead_of_fallback_conditions",
    "owner_or_governance_review_required_for_high_risk_replacement",
)

SEED_CANDIDATE_IDS: Tuple[str, ...] = (
    "yolo_family_object_detection_candidate",
    "grounded_sam_style_grounding_segmentation_candidate",
    "rapidocr_candidate",
    "paddleocr_candidate",
    "qianwen_tts_candidate",
    "cosyvoice_v3_flash_candidate",
    "qwen_tts_flash_candidate",
    "moss_tts_style_candidate",
    "sensevoice_asr_candidate",
    "whisper_like_asr_candidate",
    "qwen_asr_style_candidate",
    "visual_tracking_candidate",
    "vlm_scene_understanding_candidate",
    "embedding_retrieval_candidate",
    "face_detection_recognition_later_candidate",
    "speaker_embedding_later_candidate",
)

SEED_CANDIDATE_REQUIRED: Tuple[str, ...] = (
    "model_profile_id", "model_name_candidate", "capability_domain", "goal_stage",
    "source_strategy", "current_status", "known_version_info_required_later",
    "license_review_required_later", "model_profile_required_later",
    "provider_abstraction_required", "selected_now", "invoked_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Model Profile Registry Planning GO ≠ model selected",
    "seed profile candidates ≠ license cleared",
    "profile registry planned ≠ model registry runtime implemented",
    "qianwen/yolo/ocr/asr candidates registered ≠ invoked",
    "next DryRunAndReview ≠ model benchmark",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("model_profile_registry_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "model_profile_registry_runtime_enabled_now", "model_profile_created_as_runtime_now",
    "model_selected_now", "model_downloaded_now", "model_invoked_now", "provider_invoked_now",
    "model_runtime_enabled_now", "benchmark_executed_now", "license_cleared_now",
    "security_review_completed_now", "training_started_now", "fine_tuning_started_now",
    "code_generation_executed_now", "skill_added_now", "memory_written_now",
    "world_model_written_now", "task_state_committed_now", "user_output_generated_now",
)

REGISTRY_NOT: Tuple[str, ...] = (
    "model_selector", "runtime_executor", "provider_invoker", "benchmark_runner",
    "license_clearing_authority", "training_system", "fine_tuning_system", "universal_brain",
)

REGISTRY_DUTIES: Tuple[str, ...] = (
    "store model candidate profiles",
    "bind model candidates to capability domains",
    "bind model candidates to capability stack layers",
    "record source strategy",
    "record version and license metadata",
    "record input/output contracts",
    "record quality acceptance criteria",
    "record health/validation/whitebox requirements",
    "record provider abstraction binding",
    "record controlled runtime requirement",
    "record replacement/fallback strategy",
    "expose profile refs to module-local model profile and midplatform governance binding",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
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


def _seed_candidate(
    profile_id: str,
    name: str,
    domain: str,
    goal_stage: str,
    source_strategy: str,
    status: str,
    *,
    model_family: str = "",
    layer: str = "layer_1_perception",
    role: str = "signal_provider",
) -> Dict[str, Any]:
    return {
        "model_profile_id": profile_id,
        "model_name_candidate": name,
        "model_family": model_family or name.split("_")[0],
        "capability_domain": domain,
        "goal_stage": goal_stage,
        "capability_stack_layer": layer,
        "model_role": role,
        "source_strategy": source_strategy,
        "current_status": status,
        "known_version_info_required_later": True,
        "license_review_required_later": True,
        "model_profile_required_later": True,
        "provider_abstraction_required": True,
        "selected_now": False,
        "invoked_now": False,
        "runtime_enabled_now": False,
        "no_direct_fact_action_output": True,
    }


def _tts_governance_overlay(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Phase-Voice-TTS-Model-Deprecation-Minimal-Patch-v1-001 TTS candidate governance fields."""
    out = dict(candidate)
    pid = str(out.get("model_profile_id") or "")
    overlays: Dict[str, Dict[str, Any]] = {
        "qianwen_tts_candidate": {
            "status": "deprecated_pending",
            "retirement_date": "2026-09-07",
            "preferred": False,
            "runtime_default_allowed": False,
            "dashscope_model_name": "qwen-tts",
        },
        "cosyvoice_v3_flash_candidate": {
            "status": "replacement_candidate",
            "preferred": True,
            "runtime_default_allowed": True,
            "dashscope_model_name": "cosyvoice-v3-flash",
        },
        "qwen_tts_flash_candidate": {
            "status": "transitional_candidate",
            "preferred": False,
            "runtime_default_allowed": False,
            "dashscope_model_name": "qwen-tts-flash",
        },
    }
    if pid in overlays:
        out.update(overlays[pid])
    return out


def run_model_profile_registry_planning_v1(
    *,
    scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_root: str,
    scenario_model_capability_roadmap_current_state_inventory_planning_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    roadmap_dr_root = Path(
        scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_root
    ).expanduser().resolve()
    roadmap_plan_root = Path(
        scenario_model_capability_roadmap_current_state_inventory_planning_root
    ).expanduser().resolve()
    stack_root = Path(layered_capability_stack_standard_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    roadmap_dr_vr = _try_read_json(roadmap_dr_root / "verifier_report.json") or {}
    roadmap_dr_sm = _try_read_json(roadmap_dr_root / "summary.json") or {}
    roadmap_plan_sm = _try_read_json(roadmap_plan_root / "summary.json") or {}
    stack_vr = _try_read_json(stack_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}
    module_contract = _try_read_json(roadmap_plan_root / "module_local_model_profile_contract_v1.json") or {}
    mid_contract = _try_read_json(
        roadmap_plan_root / "midplatform_model_governance_binding_contract_v1.json"
    ) or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "output_root": str(out_root),
        "upstream_roadmap_dryrun_root": str(roadmap_dr_root),
        "upstream_roadmap_planning_root": str(roadmap_plan_root),
    }

    if roadmap_dr_vr.get("verifier") != "GO":
        blockers.append("Roadmap DryRunAndReview must be GO")
    if roadmap_dr_sm.get("final_decision") != ROADMAP_DR_FINAL_GO:
        blockers.append("Roadmap DryRunAndReview final_decision mismatch")
    if roadmap_plan_sm.get("capability_domain_count") != 12:
        blockers.append("12 capability domains required")
    if not module_contract.get("required_fields"):
        blockers.append("module_local_model_profile_contract not planned")
    if not mid_contract.get("required_fields"):
        blockers.append("midplatform_governance_binding_contract not planned")
    for name, vr in (
        ("stack_std", stack_vr), ("constitution_bus", cb_vr),
        ("provider_abs", provider_vr), ("controlled_runtime", cr_vr),
    ):
        if vr.get("verifier") != "GO":
            blockers.append(f"{name} must be GO")

    input_ok = len(blockers) == 0

    roadmap_input_review = {
        "review_id": "roadmap_input_review_v1",
        "roadmap_dryrun_verifier": roadmap_dr_vr.get("verifier"),
        "roadmap_dryrun_final_decision": roadmap_dr_sm.get("final_decision"),
        "capability_domain_count": roadmap_plan_sm.get("capability_domain_count"),
        "module_local_profile_contract_planned": bool(module_contract.get("required_fields")),
        "midplatform_binding_contract_planned": bool(mid_contract.get("required_fields")),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    registry_definition = {
        "registry_id": "luna_model_profile_registry_v1",
        "registry_type": "model_candidate_profile_registry",
        "scope": "Luna 2.0 model candidate governance",
        "registry_runtime_enabled_now": False,
        "model_selection_allowed_now": False,
        "model_invocation_allowed_now": False,
        "benchmark_allowed_now": False,
        "candidate_only": True,
        "registry_duties": list(REGISTRY_DUTIES),
        "registry_is_not": list(REGISTRY_NOT),
        "stop_chain": [
            "Model Candidate",
            "Model Profile Registry",
            "Module-local Model Profile",
            "Midplatform Governance Binding",
            "Provider / Runtime Readiness later",
            "Controlled Runtime later",
        ],
        **meta,
    }

    model_profile_schema = {
        "schema_id": "model_profile_schema_v1",
        "required_fields": list(MODEL_PROFILE_SCHEMA_FIELDS),
        "defaults": {
            "source_chain_required": True,
            "whitebox_trace_required": True,
            "no_direct_fact_action_output": True,
            "selected_now": False,
            "invoked_now": False,
            "runtime_enabled_now": False,
        },
        **meta,
    }

    lifecycle_policy = {
        "policy_id": "model_profile_lifecycle_policy_v1",
        "lifecycle_states": list(LIFECYCLE_STATES),
        "rules": {
            "registered_ne_selected": True,
            "profile_complete_ne_runtime_ready": True,
            "benchmark_required_ne_benchmark_executed": True,
            "license_review_required_ne_license_cleared": True,
            "selected_later_not_allowed_now": True,
        },
        **meta,
    }

    status_taxonomy = {
        "taxonomy_id": "model_profile_status_taxonomy_v1",
        "status_types": list(STATUS_TAXONOMY),
        **meta,
    }

    license_schema = {
        "schema_id": "model_source_and_license_metadata_schema_v1",
        "source_strategies": {
            "A": "direct_open_source_or_external_provider",
            "B": "reference_inspired_rebuild",
            "C": "self_developed_core_capability",
        },
        "required_fields": list(LICENSE_METADATA_FIELDS),
        "defaults": {
            "commercial_use_allowed_unknown_by_default": True,
            "redistribution_allowed_unknown_by_default": True,
            "modification_allowed_unknown_by_default": True,
            "attribution_required_unknown_by_default": True,
            "update_tracking_required": True,
        },
        **meta,
    }

    layer_binding_schema = {
        "schema_id": "model_capability_layer_binding_schema_v1",
        "required_fields": list(LAYER_BINDING_FIELDS),
        "capability_stack_ref": UNIVERSAL_STACK_STANDARD_ID,
        "layered_governance_mapping_ref": ADDENDUM_ID,
        "cannot_claim_higher_layer_without_lower_layer": True,
        **meta,
    }

    io_profile_schema = {
        "schema_id": "model_input_output_profile_schema_v1",
        "input_types": list(IO_INPUT_TYPES),
        "output_types": list(IO_OUTPUT_TYPES),
        "forbidden_outputs": list(IO_FORBIDDEN),
        **meta,
    }

    quality_schema = {
        "schema_id": "model_quality_acceptance_profile_schema_v1",
        "required_fields": list(QUALITY_PROFILE_FIELDS),
        "defaults": {
            "candidate_contract_compliance_required": True,
            "degradation_behavior_required": True,
        },
        **meta,
    }

    health_schema = {
        "schema_id": "model_health_validation_whitebox_profile_schema_v1",
        "required_fields": list(HEALTH_VALIDATION_FIELDS),
        "defaults": {
            "health_oversight_external_to_bus": True,
            "bus_transports_health_ref_not_judges": True,
        },
        **meta,
    }

    provider_runtime_schema = {
        "schema_id": "model_provider_runtime_binding_profile_schema_v1",
        "required_fields": list(PROVIDER_RUNTIME_BINDING_FIELDS),
        "defaults": {
            "provider_abstraction_required": True,
            "controlled_runtime_required": True,
            "authorization_required_later": True,
            "provider_readiness_required_later": True,
            "no_provider_auto_switch_without_policy": True,
            "runtime_invocation_allowed_now": False,
        },
        **meta,
    }

    version_schema = {
        "schema_id": "model_version_update_replacement_profile_schema_v1",
        "required_fields": list(VERSION_REPLACEMENT_FIELDS),
        "defaults": {
            "benchmark_revalidation_required": True,
            "security_review_required": True,
            "owner_or_governance_review_required_for_high_risk_replacement": True,
        },
        **meta,
    }

    seed_candidates = [
        _seed_candidate("yolo_family_object_detection_candidate", "yolo_family", "first_person_vision_scene_understanding", "stage_1", "direct_open_source_or_external_provider", "candidate_registered", model_family="yolo", role="object_detection"),
        _seed_candidate("grounded_sam_style_grounding_segmentation_candidate", "grounded_sam_style", "first_person_vision_scene_understanding", "stage_1", "direct_open_source_or_external_provider", "planned_only", role="grounding_segmentation"),
        _seed_candidate("rapidocr_candidate", "rapidocr", "ocr_text_recognition_reading", "stage_1", "direct_open_source_or_external_provider", "candidate_registered"),
        _seed_candidate("paddleocr_candidate", "paddleocr", "ocr_text_recognition_reading", "stage_1", "direct_open_source_or_external_provider", "candidate_registered"),
        _seed_candidate("qianwen_tts_candidate", "qianwen_tts", "tts_voice_output", "stage_3", "direct_open_source_or_external_provider", "deprecated_pending", layer="layer_6_runtime_later"),
        _seed_candidate("cosyvoice_v3_flash_candidate", "cosyvoice_v3_flash", "tts_voice_output", "stage_3", "direct_open_source_or_external_provider", "candidate_registered", layer="layer_6_runtime_later"),
        _seed_candidate("qwen_tts_flash_candidate", "qwen_tts_flash", "tts_voice_output", "stage_3", "direct_open_source_or_external_provider", "candidate_registered", layer="layer_6_runtime_later"),
        _seed_candidate("moss_tts_style_candidate", "moss_tts_style", "tts_voice_output", "stage_3", "direct_open_source_or_external_provider", "deferred", layer="layer_6_runtime_later"),
        _seed_candidate("sensevoice_asr_candidate", "sensevoice", "asr_voice_input", "foundation", "direct_open_source_or_external_provider", "deferred"),
        _seed_candidate("whisper_like_asr_candidate", "whisper_like", "asr_voice_input", "foundation", "direct_open_source_or_external_provider", "deferred"),
        _seed_candidate("qwen_asr_style_candidate", "qwen_asr_style", "asr_voice_input", "foundation", "direct_open_source_or_external_provider", "planned_only"),
        _seed_candidate("visual_tracking_candidate", "visual_tracking", "first_person_vision_scene_understanding", "stage_1", "direct_open_source_or_external_provider", "planned_only", role="tracking"),
        _seed_candidate("vlm_scene_understanding_candidate", "vlm_scene", "first_person_vision_scene_understanding", "stage_1", "direct_open_source_or_external_provider", "planned_only", role="scene_understanding"),
        _seed_candidate("embedding_retrieval_candidate", "embedding_retrieval", "memory_personal_continuity", "stage_5", "direct_open_source_or_external_provider", "deferred", layer="layer_5_memory_later", role="retrieval_organ"),
        _seed_candidate("face_detection_recognition_later_candidate", "face_detection", "first_person_vision_scene_understanding", "stage_1", "direct_open_source_or_external_provider", "deferred", role="face_recognition_later"),
        _seed_candidate("speaker_embedding_later_candidate", "speaker_embedding", "asr_voice_input", "foundation", "direct_open_source_or_external_provider", "deferred", role="speaker_embedding_later"),
    ]

    vision_seeds = {
        "seed_id": "vision_model_profile_seed_candidates_v1",
        "candidates": [c for c in seed_candidates if c["capability_domain"] == "first_person_vision_scene_understanding"],
        "confirmations": [
            "all are candidates", "no camera/runtime", "no benchmark", "no selection",
        ],
        **meta,
    }

    ocr_seeds = {
        "seed_id": "ocr_model_profile_seed_candidates_v1",
        "candidates": [
            c for c in seed_candidates if c["capability_domain"] == "ocr_text_recognition_reading"
        ] + [{
            "model_profile_id": "other_ocr_provider_placeholder",
            "model_name_candidate": "other_ocr_provider",
            "capability_domain": "ocr_text_recognition_reading",
            "goal_stage": "stage_1",
            "source_strategy": "direct_open_source_or_external_provider",
            "current_status": "planned_only",
            "known_version_info_required_later": True,
            "license_review_required_later": True,
            "model_profile_required_later": True,
            "provider_abstraction_required": True,
            "selected_now": False,
            "invoked_now": False,
        }],
        "confirmations": ["OCR output candidate only", "not fact", "no OCR runtime now"],
        **meta,
    }

    tts_seeds = {
        "seed_id": "tts_model_profile_seed_candidates_v1",
        "candidates": [
            _tts_governance_overlay(c)
            for c in (
                [c for c in seed_candidates if c["capability_domain"] == "tts_voice_output"]
                + [{
                    "model_profile_id": "local_tts_placeholder",
                    "model_name_candidate": "local_tts",
                    "capability_domain": "tts_voice_output",
                    "goal_stage": "stage_3",
                    "source_strategy": "direct_open_source_or_external_provider",
                    "current_status": "planned_only",
                    "selected_now": False,
                    "invoked_now": False,
                }]
            )
        ],
        "confirmations": [
            "qianwen_tts_candidate deprecated_pending; cosyvoice_v3_flash preferred replacement",
            "qwen_tts_flash transitional only; explicit env/config required",
            "abstract TTS runtime ≠ provider",
            "no TTS invocation in this registry patch",
        ],
        **meta,
    }

    asr_seeds = {
        "seed_id": "asr_model_profile_seed_candidates_v1",
        "candidates": [c for c in seed_candidates if c["capability_domain"] == "asr_voice_input"],
        "confirmations": ["ASR not_started/planned_only/deferred", "no ASR runtime"],
        **meta,
    }

    map_seeds = {
        "seed_id": "map_navigation_model_profile_seed_candidates_v1",
        "candidates": [
            _seed_candidate("map_provider_placeholder", "map_provider", "map_location_navigation_application", "stage_3", "reference_inspired_rebuild", "planned_only", layer="layer_4_application"),
            _seed_candidate("route_reasoning_candidate", "route_reasoning", "map_location_navigation_application", "stage_3", "reference_inspired_rebuild", "planned_only", layer="layer_4_application"),
            _seed_candidate("indoor_facility_search_candidate", "facility_search", "map_location_navigation_application", "stage_3", "reference_inspired_rebuild", "planned_only", layer="layer_4_application"),
            _seed_candidate("transit_context_candidate", "transit_context", "map_location_navigation_application", "stage_3", "reference_inspired_rebuild", "planned_only", layer="layer_4_application"),
        ],
        "confirmations": [
            "navigation is Stage 3", "no map provider invocation", "no navigation action",
        ],
        **meta,
    }

    world_seeds = {
        "seed_id": "world_continuity_model_profile_seed_candidates_v1",
        "candidates": [
            _seed_candidate("scene_delta_candidate", "scene_delta", "spatiotemporal_world_continuity", "stage_2", "reference_inspired_rebuild", "candidate_registered"),
            _seed_candidate("temporal_tracking_candidate", "temporal_tracking", "spatiotemporal_world_continuity", "stage_2", "reference_inspired_rebuild", "planned_only"),
            _seed_candidate("visual_map_alignment_candidate", "visual_map_alignment", "spatiotemporal_world_continuity", "stage_2", "reference_inspired_rebuild", "planned_only"),
            _seed_candidate("missing_context_hypothesis_candidate", "missing_context_hypothesis", "spatiotemporal_world_continuity", "stage_2", "reference_inspired_rebuild", "planned_only"),
            {
                "model_profile_id": "stcm_self_developed_profile",
                "model_name_candidate": "spatiotemporal_consistency_manager",
                "capability_domain": "spatiotemporal_world_continuity",
                "goal_stage": "stage_2",
                "source_strategy": "self_developed_core_capability",
                "current_status": "profile_required",
                "selected_now": False,
                "invoked_now": False,
            },
        ],
        "confirmations": [
            "external models provide signals only", "Luna owns continuity governance",
        ],
        **meta,
    }

    mem_emo_evo_seeds = {
        "seed_id": "memory_emotion_evolution_model_profile_seed_candidates_v1",
        "candidates": [
            _seed_candidate("embedding_retrieval_candidate", "embedding_retrieval", "memory_personal_continuity", "stage_5", "direct_open_source_or_external_provider", "deferred", layer="layer_5_memory_later"),
            _seed_candidate("emotion_signal_model_candidate", "emotion_signal", "emotion_engine_social_adaptation", "stage_5", "direct_open_source_or_external_provider", "deferred"),
            _seed_candidate("relationship_context_model_candidate", "relationship_context", "emotion_engine_social_adaptation", "stage_5", "self_developed_core_capability", "profile_required"),
            _seed_candidate("market_feedback_analysis_candidate", "market_feedback_analysis", "evolutionary_recursion_self_improvement", "stage_6", "direct_open_source_or_external_provider", "deferred"),
            _seed_candidate("code_analysis_assistant_candidate", "code_analysis_assistant", "evolutionary_recursion_self_improvement", "stage_6", "direct_open_source_or_external_provider", "deferred"),
        ],
        "confirmations": [
            "Personal Continuity / Emotion governance / Evolutionary Recursion governance self-owned",
            "proposal_only for evolution",
            "no memory write / code modification / skill addition",
        ],
        **meta,
    }

    domain_index = {
        "index_id": "model_profile_registry_domain_index_v1",
        "by_capability_domain": {did: [c["model_profile_id"] for c in seed_candidates if c.get("capability_domain") == did] for did in CAPABILITY_DOMAIN_IDS},
        "by_goal_stage": {},
        "by_model_source_strategy": {st: [c["model_profile_id"] for c in seed_candidates if c.get("source_strategy") == st] for st in MODEL_SOURCE_TYPES},
        "by_provider_candidate": [c["model_profile_id"] for c in seed_candidates if c.get("provider_abstraction_required")],
        "by_status": {},
        "by_license_review_status": ["license_review_required_later"],
        "by_runtime_readiness_status": ["not_runtime_ready"],
        "by_layered_capability_stack_layer": {},
        "by_risk_level": {"high": ["qianwen_tts_candidate", "cosyvoice_v3_flash_candidate", "map_provider_placeholder"], "medium": ["yolo_family_object_detection_candidate"], "low": []},
        **meta,
    }
    for c in seed_candidates:
        domain_index["by_goal_stage"].setdefault(c["goal_stage"], []).append(c["model_profile_id"])
        domain_index["by_status"].setdefault(c["current_status"], []).append(c["model_profile_id"])
        domain_index["by_layered_capability_stack_layer"].setdefault(c.get("capability_stack_layer", "layer_1_perception"), []).append(c["model_profile_id"])

    module_binding_plan = {
        "plan_id": "model_profile_to_module_local_binding_plan_v1",
        "rules": [
            "every module must reference model_profile_id",
            "module-local profile cannot override registry",
            "module-local profile adds implementation context",
            "module-local profile must declare capability stack and governance mapping",
            "module-local profile cannot select/invoke model by itself",
        ],
        "module_local_profile_fields_ref": list(MODULE_PROFILE_FIELDS),
        **meta,
    }

    mid_binding_plan = {
        "plan_id": "model_profile_to_midplatform_governance_binding_plan_v1",
        "rules": [
            "every model profile must bind Constitution-Bus",
            "Provider Abstraction if provider-backed",
            "Validation requirement",
            "Health requirement",
            "Whitebox requirement",
            "Controlled Runtime requirement if runtime-capable",
            "Output Gate requirement if output-capable",
            "Memory/WorldModel admission if write-capable later",
            "Decision/Integration consumption policy",
        ],
        "midplatform_binding_fields_ref": list(MIDPLATFORM_BINDING_FIELDS),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "model_profile_registry_non_runtime_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "model_profile_registry_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "objectives": [
            "generate model_profile_registry_candidate",
            "verify model_profile_schema",
            "verify lifecycle/status taxonomy",
            "verify source/license metadata schema",
            "verify capability layer binding",
            "verify I/O, quality, health/validation/whitebox, provider/runtime, version/replacement schemas",
            "verify seed model profile candidates",
            "no model select/download/invoke/benchmark",
        ],
        **meta,
    }

    planning_pass = input_ok
    planning_decision = {
        "decision_id": "model_profile_registry_planning_decision_v1",
        "planning_pass": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "model_profile_registry_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "registry_planning_only": True,
        **meta,
    }

    non_claims = {"register_id": "non_claims_register_v1", "non_claims": list(NON_CLAIMS), **meta}

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "seed_candidate_count": len(SEED_CANDIDATE_IDS),
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "model_profile_registry_planning_policy": policy,
        "roadmap_input_review": roadmap_input_review,
        "model_profile_registry_definition": registry_definition,
        "model_profile_schema": model_profile_schema,
        "model_profile_lifecycle_policy": lifecycle_policy,
        "model_profile_status_taxonomy": status_taxonomy,
        "model_source_and_license_metadata_schema": license_schema,
        "model_capability_layer_binding_schema": layer_binding_schema,
        "model_input_output_profile_schema": io_profile_schema,
        "model_quality_acceptance_profile_schema": quality_schema,
        "model_health_validation_whitebox_profile_schema": health_schema,
        "model_provider_runtime_binding_profile_schema": provider_runtime_schema,
        "model_version_update_replacement_profile_schema": version_schema,
        "model_profile_registry_domain_index": domain_index,
        "seed_model_profile_candidates": {
            "seed_id": "seed_model_profile_candidates_v1",
            "candidates": seed_candidates,
            "candidate_count": len(seed_candidates),
            **meta,
        },
        "vision_model_profile_seed_candidates": vision_seeds,
        "ocr_model_profile_seed_candidates": ocr_seeds,
        "tts_model_profile_seed_candidates": tts_seeds,
        "asr_model_profile_seed_candidates": asr_seeds,
        "map_navigation_model_profile_seed_candidates": map_seeds,
        "world_continuity_model_profile_seed_candidates": world_seeds,
        "memory_emotion_evolution_model_profile_seed_candidates": mem_emo_evo_seeds,
        "model_profile_to_module_local_binding_plan": module_binding_plan,
        "model_profile_to_midplatform_governance_binding_plan": mid_binding_plan,
        "model_profile_registry_non_runtime_boundary_matrix": boundary_matrix,
        "model_profile_registry_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "model_profile_registry_planning_decision": planning_decision,
        "summary": summary,
    }
