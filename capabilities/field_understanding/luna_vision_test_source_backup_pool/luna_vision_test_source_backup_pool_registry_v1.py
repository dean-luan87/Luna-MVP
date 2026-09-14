# -*- coding: utf-8 -*-
"""Luna Vision Test Source Backup Pool — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.luna_vision_test_source_backup_pool.luna_vision_test_source_backup_pool_types_v1 import (
    ALLOWED_USE_BENCHMARK_ONLY,
    ALLOWED_USE_RESEARCH_TEST_ONLY,
    ALLOWED_USE_UNKNOWN,
    ALLOWED_USE_VALUES,
    COMMERCIAL_NON_COMMERCIAL,
    COMMERCIAL_PER_DATASET,
    COMMERCIAL_UNKNOWN,
    COMMERCIAL_USE_DEFAULT,
    COMMERCIAL_USE_VALUES,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GOVERNANCE_FIELDS,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    POOL_GOVERNANCE_RULES,
    REGISTRY_ITEM_REQUIRED_FIELDS,
    RGB_VISION_PLANNING_REF,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    SOURCE_IDS,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TEST_SOURCE_POOL_MODE,
    VISION_HARDWARE_BASELINE,
    VisionAnnotationFormatPolicy,
    VisionDatasetLicenseAdmissionPolicy,
    VisionEvidenceCandidateMappingPolicy,
    VisionTestSourceBackupPoolProfile,
    VisionTestSourceRegistryItem,
    VisionTestSourceRiskPolicy,
    candidate_to_dict,
)

REGISTRY_ID = "luna_vision_test_source_backup_pool_registry_v1"
PROFILE_REF = "luna_vision_test_source_backup_pool_profile_v1"

# --------------------------------------------------------------------------- #
# Registry items
# --------------------------------------------------------------------------- #
_REGISTRY_ITEMS: Tuple[VisionTestSourceRegistryItem, ...] = (
    # ----------------------------- P0 ----------------------------- #
    VisionTestSourceRegistryItem(
        source_id="roboflow_universe",
        source_name="Roboflow Universe",
        source_family="p0_general_vision_baseline",
        priority="P0",
        task_family=("object_detection", "segmentation", "format_export_testing"),
        annotation_types=("yolo", "coco", "voc", "json"),
        candidate_output_types=(
            "object_evidence_candidate",
            "region_evidence_candidate",
            "classification_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_PER_DATASET,
        allowed_use=ALLOWED_USE_UNKNOWN,
        integrated_replay_compatible=True,
        risk_notes="License varies per dataset; must run per-dataset license/source admission.",
        use_case="external dataset discovery / object detection / segmentation / format export testing",
        license_policy="per_dataset_license_required",
    ),
    VisionTestSourceRegistryItem(
        source_id="coco",
        source_name="COCO",
        source_family="p0_general_vision_baseline",
        priority="P0",
        task_family=("object_detection", "segmentation", "caption"),
        annotation_types=("coco_bbox", "coco_segmentation", "coco_caption"),
        candidate_output_types=(
            "object_evidence_candidate",
            "region_evidence_candidate",
            "scene_caption_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_UNKNOWN,
        allowed_use=ALLOWED_USE_BENCHMARK_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Annotations CC BY 4.0; source images carry their own licenses.",
        use_case="object detection / segmentation / caption baseline",
    ),
    VisionTestSourceRegistryItem(
        source_id="open_images_v7",
        source_name="Open Images V7",
        source_family="p0_general_vision_baseline",
        priority="P0",
        task_family=(
            "detection",
            "segmentation",
            "visual_relationship",
            "localized_narrative",
        ),
        annotation_types=(
            "image_level_labels",
            "boxes",
            "segmentation_masks",
            "visual_relationships",
            "localized_narratives",
        ),
        candidate_output_types=(
            "object_evidence_candidate",
            "region_evidence_candidate",
            "scene_relation_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_UNKNOWN,
        allowed_use=ALLOWED_USE_BENCHMARK_ONLY,
        integrated_replay_compatible=True,
        risk_notes="~9M images; annotations CC BY 4.0, images CC BY 2.0 but verify per image.",
        use_case="detection / segmentation / relationship / localized narrative",
    ),
    VisionTestSourceRegistryItem(
        source_id="lvis",
        source_name="LVIS",
        source_family="p0_general_vision_baseline",
        priority="P0",
        task_family=("long_tail_object", "instance_segmentation"),
        annotation_types=("instance_segmentation", "long_tail_categories"),
        candidate_output_types=(
            "object_evidence_candidate",
            "region_evidence_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_UNKNOWN,
        allowed_use=ALLOWED_USE_BENCHMARK_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Built on COCO images; inherits COCO image license caveats.",
        use_case="long-tail object / instance segmentation",
    ),
    VisionTestSourceRegistryItem(
        source_id="ade20k",
        source_name="ADE20K",
        source_family="p0_general_vision_baseline",
        priority="P0",
        task_family=("scene_parsing", "semantic_segmentation", "scene_layout"),
        annotation_types=("semantic_segmentation", "part_segmentation"),
        candidate_output_types=(
            "region_evidence_candidate",
            "scene_observation_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_UNKNOWN,
        allowed_use=ALLOWED_USE_RESEARCH_TEST_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Research-oriented scene parsing; verify license before commercial use.",
        use_case="scene parsing / semantic segmentation / indoor-outdoor scene layout",
    ),
    VisionTestSourceRegistryItem(
        source_id="textocr",
        source_name="TextOCR",
        source_family="p0_general_vision_baseline",
        priority="P0",
        task_family=("scene_text", "arbitrary_shaped_ocr"),
        annotation_types=("text_polygon", "text_transcription"),
        candidate_output_types=("text_evidence_candidate",),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_UNKNOWN,
        allowed_use=ALLOWED_USE_BENCHMARK_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Scene text over Open Images subset; verify image-level license.",
        use_case="scene text / arbitrary-shaped OCR",
    ),
    VisionTestSourceRegistryItem(
        source_id="visual_genome",
        source_name="Visual Genome",
        source_family="p0_general_vision_baseline",
        priority="P0",
        task_family=("object", "attribute", "relationship", "scene_graph"),
        annotation_types=("objects", "attributes", "relationships", "region_descriptions"),
        candidate_output_types=(
            "object_evidence_candidate",
            "attribute_candidate",
            "scene_relation_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_UNKNOWN,
        allowed_use=ALLOWED_USE_BENCHMARK_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Annotations CC BY 4.0; scene graph labels are evidence, not fact.",
        use_case="object / attribute / relationship / scene graph",
    ),
    # ----------------------------- P1 ----------------------------- #
    VisionTestSourceRegistryItem(
        source_id="bdd100k",
        source_name="BDD100K",
        source_family="p1_scene_specialized",
        priority="P1",
        task_family=("road", "vehicle", "pedestrian", "traffic_scene"),
        annotation_types=("boxes", "lane", "drivable_area", "segmentation", "tracking"),
        candidate_output_types=(
            "object_evidence_candidate",
            "track_placeholder_candidate",
            "road_scene_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_NON_COMMERCIAL,
        allowed_use=ALLOWED_USE_RESEARCH_TEST_ONLY,
        integrated_replay_compatible=True,
        risk_notes="BDD license restricts to non-commercial research; commercial use prohibited.",
        use_case="road / vehicle / pedestrian / traffic scene",
    ),
    VisionTestSourceRegistryItem(
        source_id="cityscapes",
        source_name="Cityscapes",
        source_family="p1_scene_specialized",
        priority="P1",
        task_family=("urban_street_segmentation", "walkable_region_proxy"),
        annotation_types=("semantic_segmentation", "instance_segmentation"),
        candidate_output_types=(
            "region_evidence_candidate",
            "road_scene_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_NON_COMMERCIAL,
        allowed_use=ALLOWED_USE_RESEARCH_TEST_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Cityscapes license is non-commercial / academic; commercial use prohibited.",
        use_case="urban street segmentation / walkable-region proxy",
    ),
    VisionTestSourceRegistryItem(
        source_id="mapillary_vistas",
        source_name="Mapillary Vistas",
        source_family="p1_scene_specialized",
        priority="P1",
        task_family=("street_level_segmentation", "signs", "sidewalk", "urban_objects"),
        annotation_types=("semantic_segmentation", "instance_segmentation", "panoptic"),
        candidate_output_types=(
            "region_evidence_candidate",
            "object_evidence_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_NON_COMMERCIAL,
        allowed_use=ALLOWED_USE_RESEARCH_TEST_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Official license CC BY-NC-SA; research/non-commercial only, commercial caution.",
        use_case="street-level semantic segmentation / signs / sidewalk / urban object classes",
        license_policy="non_commercial_caution",
    ),
    # ----------------------------- P2 ----------------------------- #
    VisionTestSourceRegistryItem(
        source_id="ego4d",
        source_name="Ego4D",
        source_family="p2_first_person_specialized",
        priority="P2",
        task_family=(
            "first_person_video",
            "episodic_memory",
            "hand_object",
            "social_scene",
            "activity_understanding",
        ),
        annotation_types=("video_annotations", "narrations", "moments", "hand_object"),
        candidate_output_types=(
            "scene_observation_candidate",
            "track_evidence_candidate",
            "task_context_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_UNKNOWN,
        allowed_use=ALLOWED_USE_RESEARCH_TEST_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Large-scale; Ego4D license agreement + access flow required before any use.",
        use_case="first-person video / episodic memory / hand-object / social scene / activity",
    ),
    VisionTestSourceRegistryItem(
        source_id="epic_kitchens",
        source_name="EPIC-KITCHENS",
        source_family="p2_first_person_specialized",
        priority="P2",
        task_family=("egocentric_daily_activity", "object_action_interaction"),
        annotation_types=("action_segments", "object_boxes", "narrations"),
        candidate_output_types=(
            "object_evidence_candidate",
            "action_context_candidate",
            "task_context_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_NON_COMMERCIAL,
        allowed_use=ALLOWED_USE_RESEARCH_TEST_ONLY,
        integrated_replay_compatible=True,
        risk_notes="CC BY-NC license; non-commercial research only.",
        use_case="egocentric daily activity / object-action interaction",
    ),
    VisionTestSourceRegistryItem(
        source_id="egotracks",
        source_name="EgoTracks",
        source_family="p2_first_person_specialized",
        priority="P2",
        task_family=("long_term_egocentric_object_tracking",),
        annotation_types=("long_term_tracks",),
        candidate_output_types=("track_evidence_candidate",),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_UNKNOWN,
        allowed_use=ALLOWED_USE_RESEARCH_TEST_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Built on Ego4D; inherits Ego4D license/access constraints.",
        use_case="long-term egocentric object tracking",
    ),
    VisionTestSourceRegistryItem(
        source_id="refego",
        source_name="RefEgo",
        source_family="p2_first_person_specialized",
        priority="P2",
        task_family=("first_person_referring_expression", "object_grounding"),
        annotation_types=("referring_expressions", "grounding_boxes"),
        candidate_output_types=(
            "scene_relation_candidate",
            "object_reference_candidate",
        ),
        license_ref_required=True,
        source_chain_required=True,
        annotation_origin_required=True,
        sample_origin_required=True,
        commercial_use_status=COMMERCIAL_UNKNOWN,
        allowed_use=ALLOWED_USE_RESEARCH_TEST_ONLY,
        integrated_replay_compatible=True,
        risk_notes="Built on Ego4D; referring expressions are evidence, not grounded fact.",
        use_case="first-person referring expression / object grounding",
    ),
)

# --------------------------------------------------------------------------- #
# Upstream sealed GO artifacts
# --------------------------------------------------------------------------- #
_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": RGB_VISION_PLANNING_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_v1_smoke_v0/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_review_v1.json"
        ),
        "expected_go": "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_ocr_segmentation_integrated_evidence_replay_planning/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "rgb_vision_planning_go_verified",
    },
    {
        "phase_ref": RTAB_MULTI_EXPORT_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_multi_export_spatial_evidence_replay_integrated_closure_v1_smoke_v0/"
            "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_run_and_review_v1.json"
        ),
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
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
            "field_task_guidance_safety_chain_closure_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
    },
    {
        "phase_ref": INTERFACE_LAYER_GOVERNANCE_REF,
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
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
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
        "require_go": True,
        "verify_flag": "model_admission_governance_verified",
    },
)

_RECOGNIZED_ANNOTATION_FAMILIES: Tuple[str, ...] = (
    "yolo",
    "coco",
    "voc",
    "json",
    "semantic_segmentation",
    "instance_segmentation",
    "panoptic",
    "boxes",
    "masks",
    "text_polygon",
    "scene_graph",
    "relationships",
    "video_annotations",
    "tracks",
    "referring_expressions",
)


def build_pool_profile_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        VisionTestSourceBackupPoolProfile(
            profile_ref=PROFILE_REF,
            phase_id="Phase-Luna-Vision-Test-Source-Backup-Pool-v1-001",
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            rgb_vision_planning_ref=RGB_VISION_PLANNING_REF,
            rtab_multi_export_closure_ref=RTAB_MULTI_EXPORT_CLOSURE_REF,
            field_task_guidance_safety_chain_closure_ref=FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            vision_hardware_baseline=VISION_HARDWARE_BASELINE,
            system_objective=SYSTEM_OBJECTIVE,
            test_source_pool_mode=TEST_SOURCE_POOL_MODE,
            commercial_use_default=COMMERCIAL_USE_DEFAULT,
            target_internal_format=TARGET_INTERNAL_FORMAT,
            target_entrypoint=TARGET_ENTRYPOINT,
            governance_fields=GOVERNANCE_FIELDS,
            governance_rules=POOL_GOVERNANCE_RULES,
        )
    )


def build_license_admission_policy_v1() -> Dict[str, Any]:
    roboflow = next(i for i in _REGISTRY_ITEMS if i.source_id == "roboflow_universe")
    non_commercial = [i for i in _REGISTRY_ITEMS if i.commercial_use_status == COMMERCIAL_NON_COMMERCIAL]
    return candidate_to_dict(
        VisionDatasetLicenseAdmissionPolicy(
            policy_ref="vision_dataset_license_admission_policy_v1",
            license_ref_required=all(i.license_ref_required for i in _REGISTRY_ITEMS),
            source_chain_required=all(i.source_chain_required for i in _REGISTRY_ITEMS),
            annotation_origin_required=all(i.annotation_origin_required for i in _REGISTRY_ITEMS),
            sample_origin_required=all(i.sample_origin_required for i in _REGISTRY_ITEMS),
            commercial_use_default=COMMERCIAL_USE_DEFAULT,
            per_dataset_license_required_for_roboflow=(
                roboflow.commercial_use_status == COMMERCIAL_PER_DATASET
            ),
            non_commercial_marked_research_test_only=all(
                i.allowed_use == ALLOWED_USE_RESEARCH_TEST_ONLY for i in non_commercial
            ),
            commercial_use_unknown_until_verified=(
                COMMERCIAL_USE_DEFAULT == "unknown_until_license_verified"
            ),
        )
    )


def build_annotation_format_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        VisionAnnotationFormatPolicy(
            policy_ref="vision_annotation_format_policy_v1",
            recognized_annotation_families=_RECOGNIZED_ANNOTATION_FAMILIES,
            annotation_as_evidence_candidate=True,
            dataset_label_not_fact=True,
        )
    )


def build_evidence_candidate_mapping_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        VisionEvidenceCandidateMappingPolicy(
            policy_ref="vision_evidence_candidate_mapping_policy_v1",
            interface_adapter_required=True,
            native_output_direct_to_field_blocked=True,
            candidate_only=True,
            integrated_replay_compatible_for_all=all(
                i.integrated_replay_compatible for i in _REGISTRY_ITEMS
            ),
        )
    )


def build_risk_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        VisionTestSourceRiskPolicy(
            policy_ref="vision_test_source_risk_policy_v1",
            backup_pool_not_training_admission=True,
            backup_pool_not_runtime_admission=True,
            dataset_download_blocked=True,
            training_use_blocked=True,
            runtime_activation_blocked=True,
            rgb_first_hardware_baseline_preserved=(
                VISION_HARDWARE_BASELINE == "rgb_first_first_person_camera"
            ),
            no_live_camera=True,
            no_navigation_action_speech_fact_write=True,
        )
    )


def build_source_registered_map() -> Dict[str, bool]:
    registered = {i.source_id for i in _REGISTRY_ITEMS}
    return {f"{sid}_registered": (sid in registered) for sid in SOURCE_IDS}


def build_backup_pool_matrix_v1() -> Dict[str, Any]:
    items = [candidate_to_dict(i) for i in _REGISTRY_ITEMS]
    p0 = [i for i in items if i["priority"] == "P0"]
    p1 = [i for i in items if i["priority"] == "P1"]
    p2 = [i for i in items if i["priority"] == "P2"]
    return {
        "registry_id": REGISTRY_ID,
        "backup_pool_profile": build_pool_profile_v1(),
        "registry_items": items,
        "registry_item_count": len(items),
        "p0_source_count": len(p0),
        "p1_source_count": len(p1),
        "p2_source_count": len(p2),
        "license_admission_policy": build_license_admission_policy_v1(),
        "annotation_format_policy": build_annotation_format_policy_v1(),
        "evidence_candidate_mapping_policy": build_evidence_candidate_mapping_policy_v1(),
        "risk_policy": build_risk_policy_v1(),
        "source_registered_map": build_source_registered_map(),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if len(_REGISTRY_ITEMS) < 14:
        issues.append("registry_item_count_lt_14")

    seen = set()
    for item in _REGISTRY_ITEMS:
        d = candidate_to_dict(item)
        for field in REGISTRY_ITEM_REQUIRED_FIELDS:
            value = d.get(field)
            if value is None or value == "" or value == ():
                issues.append(f"registry_item_missing_field:{item.source_id}:{field}")
        if item.source_id in seen:
            issues.append(f"duplicate_source_id:{item.source_id}")
        seen.add(item.source_id)
        if item.priority not in ("P0", "P1", "P2"):
            issues.append(f"invalid_priority:{item.source_id}:{item.priority}")
        if item.allowed_use not in ALLOWED_USE_VALUES:
            issues.append(f"invalid_allowed_use:{item.source_id}:{item.allowed_use}")
        if item.commercial_use_status not in COMMERCIAL_USE_VALUES:
            issues.append(
                f"invalid_commercial_use_status:{item.source_id}:{item.commercial_use_status}"
            )
        if not (
            item.license_ref_required
            and item.source_chain_required
            and item.annotation_origin_required
            and item.sample_origin_required
        ):
            issues.append(f"governance_required_flags_not_all_true:{item.source_id}")
        if not item.integrated_replay_compatible:
            issues.append(f"not_integrated_replay_compatible:{item.source_id}")
        if (
            item.commercial_use_status == COMMERCIAL_NON_COMMERCIAL
            and item.allowed_use != ALLOWED_USE_RESEARCH_TEST_ONLY
        ):
            issues.append(f"non_commercial_not_marked_research_test_only:{item.source_id}")

    expected = set(SOURCE_IDS)
    actual = {i.source_id for i in _REGISTRY_ITEMS}
    for sid in expected - actual:
        issues.append(f"expected_source_not_registered:{sid}")

    roboflow = next((i for i in _REGISTRY_ITEMS if i.source_id == "roboflow_universe"), None)
    if roboflow is None or roboflow.commercial_use_status != COMMERCIAL_PER_DATASET:
        issues.append("roboflow_per_dataset_license_not_enforced")

    return len(issues) == 0, issues
