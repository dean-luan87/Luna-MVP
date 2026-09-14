# -*- coding: utf-8 -*-
"""Recognition Model P1 Family Expansion Planning — registry v1.

Static planning registry: upstream stage references (15), tier policies, the 7
expandable/reserved model families, the deferred expansion sequence, and the
deferred-but-planned multi-model interaction / midplatform data-handling /
midplatform control test surfaces.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

# --------------------------------------------------------------------------- #
# Upstream stage registry (15 references).
#   verify=True  -> GO must be checked against an artifact and feeds a GO flag.
#   verify=False -> reference-only lineage entry (counted, not gated).
# --------------------------------------------------------------------------- #
STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "stage_index": 1,
        "phase_ref": "Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_SYSTEM_ADMISSION_AND_INVOCATION_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_system_admission_and_invocation_planning_v1_smoke_v0/"
            "recognition_model_system_admission_and_invocation_planning_review_v1.json"
        ),
    },
    {
        "stage_index": 2,
        "phase_ref": "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_INVOCATION_FEASIBILITY_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_invocation_feasibility_dryrun_v1_smoke_v0/"
            "recognition_model_invocation_feasibility_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 3,
        "phase_ref": "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_OUTPUT_ADAPTER_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 4,
        "phase_ref": "Phase-Recognition-Model-Download-License-And-Local-Availability-Planning-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_DOWNLOAD_LICENSE_AND_LOCAL_AVAILABILITY_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_download_license_and_local_availability_planning_v1_smoke_v0/"
            "recognition_model_download_license_and_local_availability_planning_review_v1.json"
        ),
    },
    {
        "stage_index": 5,
        "phase_ref": "Phase-Recognition-Model-Download-And-Install-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_DOWNLOAD_AND_INSTALL_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_download_and_install_dryrun_v1_smoke_v0/"
            "recognition_model_download_and_install_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 6,
        "phase_ref": "Phase-Recognition-Model-Real-Output-Adapter-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_REAL_OUTPUT_ADAPTER_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_real_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_real_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 7,
        "phase_ref": "Phase-Recognition-Model-Evidence-Main-Chain-Integration-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_evidence_main_chain_integration_dryrun_v1_smoke_v0/"
            "recognition_model_evidence_main_chain_integration_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 8,
        "phase_ref": "Phase-Recognition-Model-P0-Integration-Closure-v1-001",
        "verify": True,
        "verify_flag": "p0_integration_closure_go_verified",
        "expected_go": "RECOGNITION_MODEL_P0_INTEGRATION_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p0_integration_closure_v1_smoke_v0/"
            "recognition_model_p0_integration_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 9,
        "phase_ref": "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001",
        "verify": True,
        "verify_flag": "phase_one_evidence_main_chain_closure_go_verified",
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_evidence_main_chain_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_evidence_main_chain_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 10,
        "phase_ref": "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001",
        "verify": True,
        "verify_flag": "rgb_vision_evidence_chain_closure_go_verified",
        "expected_go": "RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_evidence_chain_integrated_closure_v1_smoke_v0/"
            "rgb_vision_evidence_chain_integrated_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 11,
        "phase_ref": "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001",
        "verify": True,
        "verify_flag": "rgb_slam_cross_modal_closure_go_verified",
        "expected_go": "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1_smoke_v0/"
            "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 12,
        "phase_ref": "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001",
        "verify": True,
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 13,
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "verify": True,
        "verify_flag": "interface_layer_governance_verified",
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
    },
    {
        "stage_index": 14,
        "phase_ref": "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
        "verify": True,
        "verify_flag": "model_admission_governance_verified",
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
    },
)

GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"
TOTAL_STAGE_REF_COUNT = len(STAGE_REGISTRY) + 1  # 14 phases + template = 15

# --------------------------------------------------------------------------- #
# Tier policies.
# --------------------------------------------------------------------------- #
TIER_POLICIES: Tuple[Dict[str, str], ...] = (
    {
        "tier": "P0",
        "description": "frozen_stable_baseline_rapidocr_opencv_visual_symbol_yolo_test_only",
        "execution_status": "frozen_baseline",
    },
    {
        "tier": "P1",
        "description": "next_wave_segmentation_tracking_depth_object_detection_completion",
        "execution_status": "planned_for_expansion",
    },
    {
        "tier": "P1+",
        "description": "high_capability_open_vocab_and_grounded_candidates_observation_only",
        "execution_status": "observation_candidate",
    },
    {
        "tier": "P2",
        "description": "scene_relation_vlm_audio_speech_emotion_multimodal_bridge",
        "execution_status": "reserved_contract_or_placeholder",
    },
)

# --------------------------------------------------------------------------- #
# Model family registry (7): 5 planned + 2 reserved.
# --------------------------------------------------------------------------- #
FAMILY_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "family_id": "p1_a_segmentation",
        "family_name": "Segmentation family",
        "tier": "P1",
        "execution_status": "planned",
        "candidate_models": ("MobileSAM", "FastSAM"),
        "high_tier_observation": ("SAM", "SAM2", "GroundedSAM2"),
        "target_candidates": (
            "region_evidence_candidate",
            "object_region_alignment_candidate",
            "mask_boundary_candidate",
        ),
        "boundaries": (
            "segmentation_is_not_route_activation",
            "mask_is_not_fact",
            "grounded_sam2_not_in_p1_a_execution_layer_listed_as_p1plus_p2_observation_candidate",
        ),
    },
    {
        "family_id": "p1_b_tracking",
        "family_name": "Tracking family",
        "tier": "P1",
        "execution_status": "planned",
        "candidate_models": ("supervision_tracking", "ByteTrack", "DeepSORT"),
        "high_tier_observation": (),
        "target_candidates": (
            "track_evidence_candidate",
            "dynamic_risk_candidate",
            "temporal_consistency_candidate",
        ),
        "boundaries": (
            "tracking_is_not_action_trigger",
            "moving_object_does_not_directly_trigger_speech_or_action",
        ),
    },
    {
        "family_id": "p1_c_depth_spatial_hint",
        "family_name": "Depth / spatial hint family",
        "tier": "P1",
        "execution_status": "planned",
        "candidate_models": ("MiDaS_small", "DepthAnything_small", "ZoeDepth_small"),
        "high_tier_observation": (),
        "target_candidates": (
            "spatial_hint_candidate",
            "distance_uncertainty_candidate",
            "depth_consistency_candidate",
        ),
        "boundaries": (
            "depth_is_not_field_identity",
            "depth_is_auxiliary_only",
            "no_navigation_activation",
        ),
    },
    {
        "family_id": "p1_d_object_detection_completion",
        "family_name": "Object detection completion family",
        "tier": "P1",
        "execution_status": "planned",
        "candidate_models": ("YOLO_lightweight_local_weight_path", "RT_DETR_lightweight_optional"),
        "high_tier_observation": ("GroundingDINO",),
        "target_candidates": (
            "object_evidence_candidate",
            "open_vocab_object_candidate",
        ),
        "boundaries": (
            "yolo_remains_test_only_if_agpl_or_commercial_uncleared",
            "object_identity_is_not_fact",
        ),
    },
    {
        "family_id": "p2_scene_relation_vlm",
        "family_name": "Scene relation / VLM family",
        "tier": "P2",
        "execution_status": "planned",
        "candidate_models": (
            "lightweight_vlm_structured_output",
            "scene_graph_extractor",
            "relation_extractor",
        ),
        "high_tier_observation": (),
        "target_candidates": (
            "scene_relation_candidate",
            "attribute_candidate",
            "relation_hypothesis_candidate",
        ),
        "boundaries": (
            "scene_relation_is_not_final_interpretation",
            "vlm_output_must_be_structured_and_adapter_controlled",
            "no_direct_reasoning_authority",
        ),
    },
    {
        "family_id": "p2_audio_speech_evidence",
        "family_name": "Audio / speech evidence family",
        "tier": "P2",
        "execution_status": "reserved_placeholder_not_executed",
        "candidate_models": ("SenseVoice", "pyannote", "asr_speaker_diarization_identity"),
        "high_tier_observation": (),
        "target_candidates": (
            "audio_text_candidate",
            "speaker_turn_candidate",
            "speaker_identity_candidate",
            "emotion_audio_hint_candidate",
        ),
        "boundaries": (
            "audio_evidence_is_candidate_only",
            "identity_requires_consent_or_confirmation",
            "not_part_of_current_visual_recognition_expansion_execution",
        ),
    },
    {
        "family_id": "p2_emotion_multimodal_bridge",
        "family_name": "Emotion multimodal bridge",
        "tier": "P2",
        "execution_status": "reserved_placeholder_not_executed",
        "candidate_models": ("emotion_multimodal_fusion_interface_reserved",),
        "high_tier_observation": (),
        "target_candidates": (
            "affective_scene_hint_candidate",
            "user_state_hint_candidate",
            "social_context_hint_candidate",
        ),
        "boundaries": (
            "no_psychological_judgment_fact_write",
            "no_behavior_manipulation",
            "only_future_emotion_multimodal_evidence_bridge",
        ),
    },
)

# --------------------------------------------------------------------------- #
# Deferred expansion sequence.
# --------------------------------------------------------------------------- #
EXPANSION_SEQUENCE: Tuple[str, ...] = (
    "p1_family_expansion_planning",
    "p1_invocation_local_availability_dryrun",
    "p1_output_adapter_dryrun",
    "p1_real_output_adapter_dryrun_only_if_model_locally_available",
    "multi_model_interaction_dryrun",
    "midplatform_model_data_handling_dryrun",
    "midplatform_model_control_dryrun",
    "model_tuning_planning",
    "data_usage_planning",
)

# --------------------------------------------------------------------------- #
# Deferred-but-planned multi-model interaction tests (8).
# --------------------------------------------------------------------------- #
INTERACTION_TESTS: Tuple[Dict[str, str], ...] = (
    {
        "interaction_id": "ocr_plus_visual_symbol",
        "description": "p0_verified_baseline_ocr_and_visual_symbol_consistency",
    },
    {
        "interaction_id": "object_detection_plus_segmentation",
        "description": "verify_object_bbox_and_mask_region_alignment",
    },
    {
        "interaction_id": "object_detection_plus_tracking",
        "description": "verify_same_object_cross_frame_track_stability",
    },
    {
        "interaction_id": "tracking_plus_depth",
        "description": "verify_dynamic_risk_combined_with_distance_uncertainty",
    },
    {
        "interaction_id": "ocr_plus_segmentation",
        "description": "verify_text_region_and_visual_region_consistency",
    },
    {
        "interaction_id": "visual_symbol_plus_scene_context",
        "description": "verify_symbol_meaning_with_scene_no_direct_navigation_trigger",
    },
    {
        "interaction_id": "scene_relation_plus_object_region",
        "description": "verify_relation_triple_refs_object_and_region_not_interpretation_fact",
    },
    {
        "interaction_id": "conflict_or_uncertainty",
        "description": "verify_model_conflict_enters_uncertainty_conflict_candidate_no_fact_write",
    },
)

# --------------------------------------------------------------------------- #
# Deferred-but-planned midplatform model data-handling checks (10).
# --------------------------------------------------------------------------- #
DATA_HANDLING_CHECKS: Tuple[Dict[str, str], ...] = (
    {"check_id": "multi_model_output_normalization", "description": "normalize_outputs_across_families"},
    {"check_id": "source_chain_aggregation", "description": "aggregate_source_chain_across_models"},
    {"check_id": "confidence_policy_aggregation", "description": "aggregate_confidence_under_policy"},
    {"check_id": "conflict_candidate_generation", "description": "generate_conflict_candidate_on_disagreement"},
    {"check_id": "uncertainty_candidate_generation", "description": "generate_uncertainty_candidate"},
    {"check_id": "unavailable_record_handling", "description": "handle_declared_unavailable_records"},
    {"check_id": "evidence_bundle_composition", "description": "compose_multi_model_evidence_bundle"},
    {"check_id": "candidate_lifecycle", "description": "manage_candidate_lifecycle"},
    {"check_id": "no_fact_admission_without_evidence_chain", "description": "block_fact_without_evidence_chain"},
    {"check_id": "no_direct_field_task_guidance_bypass", "description": "block_direct_ftg_bypass"},
)

# --------------------------------------------------------------------------- #
# Deferred-but-planned midplatform model control checks (11).
# --------------------------------------------------------------------------- #
CONTROL_CHECKS: Tuple[Dict[str, str], ...] = (
    {"check_id": "model_admission_control", "description": "control_model_admission"},
    {"check_id": "model_availability_control", "description": "control_model_availability"},
    {"check_id": "model_fallback_control", "description": "control_model_fallback"},
    {"check_id": "model_disable_enable_policy", "description": "control_disable_enable_policy"},
    {"check_id": "model_license_boundary_control", "description": "control_license_boundary"},
    {"check_id": "model_output_gate", "description": "gate_model_output"},
    {"check_id": "model_priority_routing_policy", "description": "control_priority_and_routing"},
    {"check_id": "degraded_mode", "description": "support_degraded_mode"},
    {"check_id": "blocked_model_output_handling", "description": "handle_blocked_model_output"},
    {"check_id": "no_direct_action_speech_navigation_fact_write", "description": "block_all_direct_side_effects"},
    {"check_id": "vla_action_chain_excluded", "description": "exclude_vla_action_chain"},
)
