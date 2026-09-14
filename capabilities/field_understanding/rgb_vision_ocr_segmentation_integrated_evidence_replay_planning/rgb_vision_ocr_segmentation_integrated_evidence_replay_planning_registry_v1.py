# -*- coding: utf-8 -*-
"""RGB Vision / OCR / Segmentation Integrated Evidence Replay Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.rgb_vision_ocr_segmentation_integrated_evidence_replay_planning.rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DECLARED_PRINCIPLES,
    DEPTH_HARDWARE_DEFAULT,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    FINAL_DECISION_GO,
    GENERIC_JSON_PARSER_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    NEXT_PHASE_REF,
    OBSERVATION_POOL_REFS,
    ORIGIN_METADATA_REQUIRED_FIELDS,
    PHASE_ID,
    PLANNING_GOVERNANCE_RULES,
    PLANNING_PRINCIPLE_ZH,
    REPLAY_SCENARIO_GO_KEYS,
    REPLAY_SCENARIO_REFS,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TOF_STEREO_DEPTH_ROLE,
    UNIVERSAL_BLOCKED_OPERATIONS,
    VISION_HARDWARE_BASELINE,
    VISION_SOURCE_GO_KEYS,
    VISION_SOURCE_REFS,
    ExternalVisionOutputSourcePolicy,
    OCRTextEvidenceMappingPolicy,
    RGBVisionHardwareBaselinePolicy,
    RGBVisionIntegratedEvidenceReplayPlanningDecision,
    RGBVisionIntegratedEvidenceReplayPlanningProfile,
    RGBVisionIntegratedReplayScenarioPolicy,
    RGBVisionSafetyBoundaryPolicy,
    SegmentationTrackingEvidenceMappingPolicy,
    VisionEvidenceCandidateMappingPolicy,
    candidate_to_dict,
)

REGISTRY_ID = "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_registry_v1"
PROFILE_REF = "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_profile_v1"

_RTAB_MULTI_EXPORT_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/rtab_map_multi_export_spatial_evidence_replay_integrated_closure_v1_smoke_v0/"
    "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_run_and_review_v1.json"
)
_FTG_SAFETY_CHAIN_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
    "field_task_guidance_safety_chain_closure_review_v1.json"
)
_GOVERNANCE_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
)
_INTERFACE_ARTIFACT_REL = (
    "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
    "interface_layer_governance_review_v1.json"
)
_MODEL_ADMISSION_ARTIFACT_REL = (
    "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
    "model_admission_governance_run_and_review_v1.json"
)

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": RTAB_MULTI_EXPORT_CLOSURE_REF,
        "artifact_rel": _RTAB_MULTI_EXPORT_CLOSURE_ARTIFACT_REL,
        "expected_go": "RTAB_MAP_MULTI_EXPORT_SPATIAL_EVIDENCE_REPLAY_INTEGRATED_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_multi_export_spatial_evidence_replay_integrated_closure/"
            "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
    },
    {
        "phase_ref": FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        "artifact_rel": _FTG_SAFETY_CHAIN_CLOSURE_ARTIFACT_REL,
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
            "field_task_guidance_safety_chain_closure_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
    },
    {
        "phase_ref": GOVERNANCE_CLOSURE_REF,
        "artifact_rel": _GOVERNANCE_CLOSURE_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_governance_closure/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": INTERFACE_LAYER_GOVERNANCE_REF,
        "artifact_rel": _INTERFACE_ARTIFACT_REL,
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "interface_layer_governance_verified",
    },
    {
        "phase_ref": MODEL_ADMISSION_GOVERNANCE_REF,
        "artifact_rel": _MODEL_ADMISSION_ARTIFACT_REL,
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "model_admission_governance_verified",
    },
)

_SOURCE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "source_ref": "rgb_frame_or_video_file",
        "source_zh": "RGB 图片 / 第一视角视频文件",
        "provider_examples": ("rgb_image_file", "first_person_video_file"),
        "output_candidate_type": "scene_observation_candidate",
        "purpose_zh": "场景、物体、动线、环境状态观察",
        "blocked_operations": ("live_camera_connect",),
    },
    {
        "source_ref": "object_detection_output",
        "source_zh": "YOLO / open-vocabulary detection / Grounded detection",
        "provider_examples": ("yolo", "open_vocabulary_detection", "grounded_detection"),
        "output_candidate_type": "object_evidence_candidate",
        "purpose_zh": "物体、入口、障碍、柜台、标识物",
        "blocked_operations": ("native_output_direct_to_field",),
    },
    {
        "source_ref": "segmentation_output",
        "source_zh": "Grounded SAM 2 / semantic segmentation / instance segmentation",
        "provider_examples": ("grounded_sam_2", "semantic_segmentation", "instance_segmentation"),
        "output_candidate_type": "region_evidence_candidate",
        "purpose_zh": "可通行区域、物体区域、语义区域、遮挡关系",
        "blocked_operations": ("route_activation_from_segmentation",),
    },
    {
        "source_ref": "tracking_output",
        "source_zh": "tracking / supervision adapter",
        "provider_examples": ("tracking_adapter", "supervision_adapter"),
        "output_candidate_type": "track_evidence_candidate",
        "purpose_zh": "行人/车辆/物体运动轨迹、动态风险",
        "blocked_operations": ("action_trigger_from_tracking", "direct_speech_tts"),
    },
    {
        "source_ref": "ocr_text_output",
        "source_zh": "OCR provider",
        "provider_examples": ("ocr_provider", "ocr_enhancement_candidate"),
        "output_candidate_type": "text_evidence_candidate",
        "purpose_zh": "标牌、门牌、路线提示、票务/入口文字",
        "blocked_operations": ("ocr_direct_fact_write",),
    },
    {
        "source_ref": "monocular_depth_or_vio_output",
        "source_zh": "RGB-based monocular depth / VIO / visual odometry",
        "provider_examples": ("monocular_depth_estimation", "rgb_vio", "visual_odometry"),
        "output_candidate_type": "spatial_hint_candidate",
        "purpose_zh": "相对距离、运动趋势、局部空间线索（不得替代 Field identity）",
        "blocked_operations": ("override_field_identity",),
    },
    {
        "source_ref": "scene_relation_output",
        "source_zh": "vision-language / scene graph / relation extractor",
        "provider_examples": ("vision_language", "scene_graph", "relation_extractor"),
        "output_candidate_type": "scene_relation_candidate",
        "purpose_zh": "物体关系、场景布局、人与物关系、任务相关性",
        "blocked_operations": ("final_interpretation_from_scene_relation",),
    },
)

_SCENARIO_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "scenario_ref": "rgb_scene_object_region_replay",
        "input_description": "RGB frame + object detection + segmentation",
        "output_planning_target": "scene_object_region_evidence_candidates",
        "scenario_requirements": ("candidate_only",),
        "blocked_operations": (),
        "allowed_next_step": "rgb_vision_integrated_evidence_replay_dryrun_planning_only",
        "go_key": "rgb_scene_object_region_replay_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rgb_ocr_scene_text_replay",
        "input_description": "RGB frame + OCR output",
        "output_planning_target": "text_evidence_candidate",
        "scenario_requirements": (
            "ocr_result_must_not_directly_write_fact",
            "source_chain_and_confidence_preserved",
        ),
        "blocked_operations": ("ocr_direct_fact_write",),
        "allowed_next_step": "rgb_vision_integrated_evidence_replay_dryrun_planning_only",
        "go_key": "rgb_ocr_scene_text_replay_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rgb_tracking_dynamic_risk_replay",
        "input_description": "tracking output",
        "output_planning_target": "track_evidence_plus_dynamic_risk_candidate",
        "scenario_requirements": ("tracking_must_not_directly_trigger_action_or_speech",),
        "blocked_operations": ("action_trigger_from_tracking", "direct_speech_tts"),
        "allowed_next_step": "rgb_vision_integrated_evidence_replay_dryrun_planning_only",
        "go_key": "rgb_tracking_dynamic_risk_replay_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rgb_monocular_depth_spatial_hint_replay",
        "input_description": "monocular depth / VIO output",
        "output_planning_target": "spatial_hint_candidate",
        "scenario_requirements": ("depth_odometry_aux_evidence_only_not_override_field_identity",),
        "blocked_operations": ("override_field_identity",),
        "allowed_next_step": "rgb_vision_integrated_evidence_replay_dryrun_planning_only",
        "go_key": "rgb_monocular_depth_spatial_hint_replay_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rgb_scene_relation_task_replay",
        "input_description": "object / region / text / relation candidates",
        "output_planning_target": (
            "task_context_candidate_task_evidence_need_candidate_task_risk_candidate"
        ),
        "scenario_requirements": ("task_interpretation_authority_in_midplatform_not_external_model",),
        "blocked_operations": ("final_interpretation_from_scene_relation",),
        "allowed_next_step": "rgb_vision_integrated_evidence_replay_dryrun_planning_only",
        "go_key": "rgb_scene_relation_task_replay_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "rgb_integrated_field_task_guidance_replay_path",
        "input_description": "vision evidence candidates",
        "output_planning_target": "field_task_guidance_candidate_replay_path",
        "scenario_requirements": (
            "guidance_candidate_not_runtime_navigation",
            "speech_gate_not_tts",
            "action_safety_candidate_must_exist",
            "candidate_only",
        ),
        "blocked_operations": ("real_navigation", "direct_speech_tts", "direct_action"),
        "allowed_next_step": "rgb_vision_integrated_evidence_replay_dryrun_planning_only",
        "go_key": "rgb_integrated_field_task_guidance_replay_path_supported",
        "blocked_scenario": False,
    },
    {
        "scenario_ref": "invalid_vision_output_blocked",
        "input_description": (
            "缺 source_chain / 低可信但试图直写 fact / 模型输出直接触发 action / OCR 直接改写场事实 / "
            "segmentation 直接 route activation"
        ),
        "output_planning_target": "blocked_rejected",
        "scenario_requirements": ("must_not_enter_adapter_or_parser_or_field_path",),
        "blocked_operations": (
            "ocr_direct_fact_write",
            "native_output_direct_to_field",
            "action_trigger_from_tracking",
            "route_activation_from_segmentation",
            "direct_action",
        ),
        "allowed_next_step": "rejection_only",
        "go_key": "invalid_vision_output_blocked",
        "blocked_scenario": True,
    },
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "vision_source_refs": VISION_SOURCE_REFS,
    "vision_source_go_keys": VISION_SOURCE_GO_KEYS,
    "replay_scenario_refs": REPLAY_SCENARIO_REFS,
    "replay_scenario_go_keys": REPLAY_SCENARIO_GO_KEYS,
    "observation_pool_refs": OBSERVATION_POOL_REFS,
    "origin_metadata_required_fields": ORIGIN_METADATA_REQUIRED_FIELDS,
    "planning_governance_rules": PLANNING_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "universal_blocked_operations": UNIVERSAL_BLOCKED_OPERATIONS,
}


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(VISION_SOURCE_REFS) != 7:
        issues.append("vision_source_refs_count_not_7")
    if len(VISION_SOURCE_GO_KEYS) != 7:
        issues.append("vision_source_go_keys_count_not_7")
    if len(REPLAY_SCENARIO_REFS) != 7:
        issues.append("replay_scenario_refs_count_not_7")
    if len(REPLAY_SCENARIO_GO_KEYS) != 7:
        issues.append("replay_scenario_go_keys_count_not_7")
    if len(_SOURCE_SPECS) != 7:
        issues.append("source_specs_count_not_7")
    if len(_SCENARIO_SPECS) != 7:
        issues.append("scenario_specs_count_not_7")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 5:
        issues.append("sealed_upstream_phase_refs_count_not_5")
    if len(PLANNING_GOVERNANCE_RULES) != 15:
        issues.append("planning_governance_rules_count_not_15")
    if len(OBSERVATION_POOL_REFS) != 8:
        issues.append("observation_pool_refs_count_not_8")
    if tuple(s["source_ref"] for s in _SOURCE_SPECS) != VISION_SOURCE_REFS:
        issues.append("source_spec_ref_order_mismatch")
    if tuple(s["scenario_ref"] for s in _SCENARIO_SPECS) != REPLAY_SCENARIO_REFS:
        issues.append("scenario_spec_ref_order_mismatch")
    return len(issues) == 0, issues


def _merge_blocked(*ops: str) -> Tuple[str, ...]:
    merged = list(UNIVERSAL_BLOCKED_OPERATIONS)
    for op in ops:
        if op not in merged:
            merged.append(op)
    return tuple(merged)


def build_planning_profile_v1() -> RGBVisionIntegratedEvidenceReplayPlanningProfile:
    return RGBVisionIntegratedEvidenceReplayPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_PARSER_REF,
        rtab_multi_export_closure_ref=RTAB_MULTI_EXPORT_CLOSURE_REF,
        field_task_guidance_safety_chain_closure_ref=FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        vision_hardware_baseline=VISION_HARDWARE_BASELINE,
        depth_hardware_default=DEPTH_HARDWARE_DEFAULT,
        tof_stereo_depth_role=TOF_STEREO_DEPTH_ROLE,
        system_objective=SYSTEM_OBJECTIVE,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        pipeline_stages=(
            "external_rgb_vision_model_output",
            "external_vision_interface_adapter",
            "generic_json_spatial_trace_or_evidence_candidate",
            "generic_json_spatial_trace_parser",
            "spatial_evidence_candidate_bundle",
            "field_task_guidance_candidate_replay_path",
        ),
        vision_source_refs=VISION_SOURCE_REFS,
        replay_scenario_refs=REPLAY_SCENARIO_REFS,
        observation_pool_refs=OBSERVATION_POOL_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=PLANNING_GOVERNANCE_RULES,
    )


def build_hardware_baseline_policy_v1() -> RGBVisionHardwareBaselinePolicy:
    return RGBVisionHardwareBaselinePolicy(
        policy_ref="rgb_vision_hardware_baseline_policy_v1",
        vision_hardware_baseline=VISION_HARDWARE_BASELINE,
        depth_hardware_default=DEPTH_HARDWARE_DEFAULT,
        tof_stereo_depth_role=TOF_STEREO_DEPTH_ROLE,
        system_objective=SYSTEM_OBJECTIVE,
        rgb_first_hardware_baseline_declared=True,
        tof_stereo_depth_optional_auxiliary_only=True,
        cognitive_world_reconstruction_objective_declared=True,
        depth_slam_vio_are_auxiliary_only=True,
        rgb_output_enters_evidence_candidate_only=True,
        declared_principles=DECLARED_PRINCIPLES,
        source_chain=SOURCE_CHAIN,
    )


def build_vision_output_source_policies_v1() -> Tuple[ExternalVisionOutputSourcePolicy, ...]:
    return tuple(
        ExternalVisionOutputSourcePolicy(
            policy_ref=f"external_vision_output_source_policy_{spec['source_ref']}_v1",
            source_ref=spec["source_ref"],
            source_zh=spec["source_zh"],
            provider_examples=spec["provider_examples"],
            output_candidate_type=spec["output_candidate_type"],
            purpose_zh=spec["purpose_zh"],
            requires_interface_adapter=True,
            requires_source_chain=True,
            requires_confidence=True,
            requires_origin_metadata=True,
            native_output_direct_to_field_blocked=True,
            blocked_operations=_merge_blocked(*spec["blocked_operations"]),
            source_chain=SOURCE_CHAIN,
            supported=True,
        )
        for spec in _SOURCE_SPECS
    )


def build_vision_source_go_map(
    sources: Tuple[ExternalVisionOutputSourcePolicy, ...],
) -> Dict[str, bool]:
    return {
        go_key: source.supported is True
        for go_key, source in zip(VISION_SOURCE_GO_KEYS, sources)
    }


def build_shared_mapping_policies_v1() -> Dict[str, Any]:
    return {
        "vision_evidence_candidate_mapping_policy": candidate_to_dict(
            VisionEvidenceCandidateMappingPolicy(
                policy_ref="vision_evidence_candidate_mapping_policy_v1",
                target_internal_format=TARGET_INTERNAL_FORMAT,
                interface_adapter_ref=INTERFACE_ADAPTER_REF,
                generic_json_output_required=True,
                generic_json_parser_required=True,
                parser_ref=GENERIC_JSON_PARSER_REF,
                target_entrypoint=TARGET_ENTRYPOINT,
                source_chain_required=True,
                confidence_required=True,
                origin_metadata_required=True,
                external_model_output_adapter_required=True,
                native_output_direct_to_field_blocked=True,
                candidate_only=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "ocr_text_evidence_mapping_policy": candidate_to_dict(
            OCRTextEvidenceMappingPolicy(
                policy_ref="ocr_text_evidence_mapping_policy_v1",
                output_candidate_type="text_evidence_candidate",
                ocr_output_not_fact=True,
                requires_source_chain=True,
                requires_confidence=True,
                scene_text_signage_supported=True,
                text_evidence_candidate_only=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "segmentation_tracking_evidence_mapping_policy": candidate_to_dict(
            SegmentationTrackingEvidenceMappingPolicy(
                policy_ref="segmentation_tracking_evidence_mapping_policy_v1",
                segmentation_output_candidate_type="region_evidence_candidate",
                tracking_output_candidate_type="track_evidence_candidate",
                segmentation_output_not_route_activation=True,
                tracking_output_not_action_trigger=True,
                monocular_depth_vio_not_field_identity=True,
                scene_relation_not_final_interpretation=True,
                region_evidence_candidate_only=True,
                track_evidence_candidate_only=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "safety_boundary_policy": candidate_to_dict(
            RGBVisionSafetyBoundaryPolicy(
                policy_ref="rgb_vision_safety_boundary_policy_v1",
                external_model_output_adapter_required=True,
                native_output_direct_to_field_blocked=True,
                ocr_output_not_fact=True,
                segmentation_output_not_route_activation=True,
                tracking_output_not_action_trigger=True,
                monocular_depth_vio_not_field_identity=True,
                scene_relation_not_final_interpretation=True,
                field_task_guidance_replay_candidate_only=True,
                guidance_candidate_not_runtime_navigation=True,
                speech_gate_candidate_not_tts=True,
                action_safety_candidate_required=True,
                no_live_camera=True,
                no_live_sensor=True,
                no_action_speech_fact_write=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_replay_scenario_policies_v1() -> Tuple[RGBVisionIntegratedReplayScenarioPolicy, ...]:
    return tuple(
        RGBVisionIntegratedReplayScenarioPolicy(
            scenario_ref=spec["scenario_ref"],
            input_description=spec["input_description"],
            output_planning_target=spec["output_planning_target"],
            scenario_requirements=spec["scenario_requirements"],
            blocked_operations=_merge_blocked(*spec["blocked_operations"]),
            allowed_next_step=spec["allowed_next_step"],
            source_chain=SOURCE_CHAIN,
            supported=not spec["blocked_scenario"],
            blocked_scenario=spec["blocked_scenario"],
        )
        for spec in _SCENARIO_SPECS
    )


def build_replay_scenario_go_map(
    scenarios: Tuple[RGBVisionIntegratedReplayScenarioPolicy, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for spec, scenario in zip(_SCENARIO_SPECS, scenarios):
        if spec["blocked_scenario"]:
            result[spec["go_key"]] = scenario.blocked_scenario is True
        else:
            result[spec["go_key"]] = scenario.supported is True
    return result


def build_planning_decision_v1(
    *,
    rtab_multi_export_spatial_evidence_replay_closure_go_verified: bool,
    field_task_guidance_safety_chain_closure_go_verified: bool,
    interface_layer_governance_verified: bool,
    model_admission_governance_verified: bool,
    controlled_trial_governance_template_ref_ok: bool,
) -> RGBVisionIntegratedEvidenceReplayPlanningDecision:
    return RGBVisionIntegratedEvidenceReplayPlanningDecision(
        decision_ref="rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_decision_v1",
        profile_ref=PROFILE_REF,
        planning_profile_count=1,
        vision_output_source_policy_count=len(VISION_SOURCE_REFS),
        integrated_replay_scenario_count=len(REPLAY_SCENARIO_REFS),
        rtab_multi_export_spatial_evidence_replay_closure_go_verified=rtab_multi_export_spatial_evidence_replay_closure_go_verified,
        field_task_guidance_safety_chain_closure_go_verified=field_task_guidance_safety_chain_closure_go_verified,
        interface_layer_governance_verified=interface_layer_governance_verified,
        model_admission_governance_verified=model_admission_governance_verified,
        controlled_trial_governance_template_ref_ok=controlled_trial_governance_template_ref_ok,
        rgb_first_hardware_baseline_declared=True,
        final_decision=FINAL_DECISION_GO,
    )


def build_rgb_vision_planning_matrix_v1() -> Dict[str, Any]:
    profile = build_planning_profile_v1()
    hardware_policy = build_hardware_baseline_policy_v1()
    sources = build_vision_output_source_policies_v1()
    scenarios = build_replay_scenario_policies_v1()
    shared = build_shared_mapping_policies_v1()
    decision = build_planning_decision_v1(
        rtab_multi_export_spatial_evidence_replay_closure_go_verified=True,
        field_task_guidance_safety_chain_closure_go_verified=True,
        interface_layer_governance_verified=True,
        model_admission_governance_verified=True,
        controlled_trial_governance_template_ref_ok=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "rgb_vision_planning_profile": candidate_to_dict(profile),
        "hardware_baseline_policy": candidate_to_dict(hardware_policy),
        "vision_output_source_policies": [candidate_to_dict(s) for s in sources],
        "replay_scenario_policies": [candidate_to_dict(s) for s in scenarios],
        "shared_mapping_policies": shared,
        "planning_decision": candidate_to_dict(decision),
        "vision_source_go_map": build_vision_source_go_map(sources),
        "replay_scenario_go_map": build_replay_scenario_go_map(scenarios),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "observation_pool_refs": list(OBSERVATION_POOL_REFS),
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
        "next_phase_ref": NEXT_PHASE_REF,
    }
