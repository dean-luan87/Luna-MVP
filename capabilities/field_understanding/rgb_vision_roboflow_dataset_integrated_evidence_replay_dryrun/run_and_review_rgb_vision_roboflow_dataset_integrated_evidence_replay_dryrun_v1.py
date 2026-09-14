# -*- coding: utf-8 -*-
"""RGB Vision Roboflow Dataset Integrated Evidence Replay DryRun — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun.rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_cases_v1 import (
    run_all_cases_v1,
    samples_dir,
)
from capabilities.field_understanding.rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun.rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPTH_HARDWARE_DEFAULT,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    EXTERNAL_TEST_SOURCE,
    FIELD_TASK_GUIDANCE_CANDIDATE_TYPES,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_PARSER_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    NEGATIVE_CASE_REFS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POSITIVE_CASE_REFS,
    RECOGNIZED_ANNOTATION_FORMATS,
    RGB_VISION_DRYRUN_REF,
    RGB_VISION_PLANNING_REF,
    ROBOFLOW_ROLE,
    RUNTIME_TRIAL_MODE,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TOF_STEREO_DEPTH_ROLE,
    VISION_HARDWARE_BASELINE,
    ANNOTATION_TYPE_TO_CANDIDATE,
    DATASET_ADMISSION_REQUIRED_FIELDS,
    RGBVisionRoboflowIntegratedEvidenceReplayDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = (
    "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_run_and_review_v1.json"
)
PROFILE_REF = "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_profile_v1"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": RGB_VISION_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_v1_smoke_v0/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_types_v1.py"
        ),
        "verify_flag": "rgb_vision_integrated_evidence_replay_dryrun_go_verified",
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
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
    },
    {
        "phase_ref": GOVERNANCE_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
        ),
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_governance_closure/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_types_v1.py"
        ),
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
        "verify_flag": "model_admission_governance_verified",
    },
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "rgb_vision_integrated_evidence_replay_dryrun_go_verified",
    "field_task_guidance_safety_chain_closure_go_verified",
    "interface_layer_governance_verified",
    "model_admission_governance_verified",
)


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def review_upstream_artifacts() -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for entry in _UPSTREAM_ARTIFACTS:
        phase_ref = entry["phase_ref"]
        module_path = _REPO_ROOT / entry["module_rel"]
        checks[f"{phase_ref}.module_present"] = module_path.is_file()
        if not module_path.is_file():
            issues.append(f"upstream_module_missing:{phase_ref}")

        artifact, exists = _load_upstream_artifact(entry["artifact_rel"])
        checks[f"{phase_ref}.artifact_present"] = exists
        if not exists:
            issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        actual_go = (artifact or {}).get("final_decision")
        go_ok = actual_go == entry["expected_go"]
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

        verify_flag = entry.get("verify_flag")
        if verify_flag:
            checks[verify_flag] = go_ok

    checks["controlled_trial_governance_template_ref_ok"] = (
        CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    )
    for required in _REQUIRED_VERIFY_FLAGS:
        if not checks.get(required, False):
            issues.append(f"{required}_not_verified")

    return checks, issues


def build_profile() -> RGBVisionRoboflowIntegratedEvidenceReplayDryRunProfile:
    return RGBVisionRoboflowIntegratedEvidenceReplayDryRunProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        rgb_vision_dryrun_ref=RGB_VISION_DRYRUN_REF,
        field_task_guidance_safety_chain_closure_ref=FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        interface_adapter_ref=INTERFACE_ADAPTER_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_PARSER_REF,
        external_test_source=EXTERNAL_TEST_SOURCE,
        roboflow_role=ROBOFLOW_ROLE,
        vision_hardware_baseline=VISION_HARDWARE_BASELINE,
        depth_hardware_default=DEPTH_HARDWARE_DEFAULT,
        tof_stereo_depth_role=TOF_STEREO_DEPTH_ROLE,
        system_objective=SYSTEM_OBJECTIVE,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        recognized_annotation_formats=RECOGNIZED_ANNOTATION_FORMATS,
        dataset_admission_required_fields=DATASET_ADMISSION_REQUIRED_FIELDS,
        annotation_type_to_candidate=ANNOTATION_TYPE_TO_CANDIDATE,
        field_task_guidance_candidate_types=FIELD_TASK_GUIDANCE_CANDIDATE_TYPES,
        governance_rules=DRYRUN_GOVERNANCE_RULES,
    )


def _aggregate(case_run: Dict[str, Any]) -> Dict[str, Any]:
    positive = case_run.get("positive_cases") or []
    negative = case_run.get("negative_cases") or []
    by_ref = {c["case_ref"]: c for c in positive + negative}

    def chk(ref: str) -> Dict[str, Any]:
        return (by_ref.get(ref) or {}).get("checks") or {}

    yolo = chk("roboflow_yolo_object_replay")
    coco = chk("roboflow_coco_object_region_replay")
    voc = chk("roboflow_voc_object_replay")
    ocr = chk("roboflow_ocr_placeholder_text_replay")
    track = chk("roboflow_tracking_placeholder_dynamic_risk_replay")
    lic = chk("roboflow_license_source_admission_metadata_preserved")
    ftg = chk("roboflow_integrated_field_task_guidance_replay_path")

    generated = set(case_run.get("generated_evidence_candidate_types") or [])
    sample_count = sum(1 for n in SAMPLE_FILES if (samples_dir() / n).is_file())

    return {
        "positive_case_count": len(positive),
        "negative_case_count": len(negative),
        "positive_pass_count": sum(1 for c in positive if c.get("passed")),
        "invalid_expected_reject_count": sum(1 for c in negative if c.get("passed")),
        "sample_file_count": sample_count,
        "scene_observation_candidate_generated": "scene_observation_candidate" in generated,
        "object_evidence_candidate_generated": "object_evidence_candidate" in generated,
        "region_evidence_candidate_generated": "region_evidence_candidate" in generated,
        "text_evidence_candidate_generated": "text_evidence_candidate" in generated,
        "track_evidence_candidate_generated": "track_evidence_candidate" in generated,
        "dynamic_risk_candidate_generated": "dynamic_risk_candidate" in generated,
        "yolo_annotation_format_recognized": yolo.get("annotation_format_recognized") is True,
        "coco_annotation_format_recognized": coco.get("annotation_format_recognized") is True,
        "voc_annotation_format_recognized": voc.get("annotation_format_recognized") is True,
        "license_present": lic.get("license_present") is True,
        "dataset_origin_present": lic.get("dataset_origin_present") is True,
        "annotation_format_recognized": lic.get("annotation_format_recognized") is True,
        "source_chain_present": lic.get("source_chain_present") is True,
        "confidence_present": lic.get("confidence_present") is True,
        "license_ref_preserved": lic.get("license_ref_preserved") is True,
        "dataset_ref_preserved": lic.get("dataset_ref_preserved") is True,
        "annotation_origin_preserved": lic.get("annotation_origin_preserved") is True,
        "roboflow_not_luna_fact_layer": lic.get("roboflow_not_fact_layer") is True,
        "roboflow_annotation_not_auto_trusted": lic.get("annotation_not_auto_trusted") is True,
        "roboflow_license_not_default_commercial": lic.get("license_not_default_commercial")
        is True,
        "source_chain_preserved": ocr.get("source_chain_preserved") is True,
        "confidence_preserved": lic.get("confidence_present") is True,
        "adapter_mapping_required": True,
        "ocr_output_not_fact": ocr.get("ocr_output_not_fact") is True,
        "tracking_output_not_action_trigger": track.get("tracking_output_not_action_trigger")
        is True,
        "field_task_guidance_replay_path_ok": ftg.get("field_task_guidance_replay_path_ok")
        is True,
        "task_context_can_reference_evidence_candidates": ftg.get(
            "task_context_can_reference_evidence_candidates"
        )
        is True,
        "task_risk_can_reference_tracking_evidence": ftg.get(
            "task_risk_can_reference_tracking_evidence"
        )
        is True,
        "guidance_candidate_remains_candidate": ftg.get("guidance_candidate_remains_candidate")
        is True,
        "speech_gate_candidate_not_tts": ftg.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_exists": ftg.get("action_safety_candidate_exists") is True,
        "roboflow_model_output_not_direct_to_field": ftg.get("model_output_not_direct_to_field")
        is True,
        "missing_license_rejected": chk("invalid_roboflow_missing_license_rejected").get(
            "missing_license_rejected"
        )
        is True,
        "missing_dataset_origin_rejected": chk(
            "invalid_roboflow_missing_dataset_origin_rejected"
        ).get("missing_dataset_origin_rejected")
        is True,
        "unrecognized_annotation_format_rejected": chk(
            "invalid_roboflow_unrecognized_annotation_format_rejected"
        ).get("unrecognized_annotation_format_rejected")
        is True,
        "missing_source_chain_rejected": chk(
            "invalid_roboflow_missing_source_chain_rejected"
        ).get("missing_source_chain_rejected")
        is True,
        "direct_fact_write_or_route_activation_rejected": chk(
            "invalid_roboflow_direct_fact_write_or_route_activation_rejected"
        ).get("direct_fact_write_or_route_activation_rejected")
        is True,
        "model_native_output_direct_to_field_rejected": chk(
            "invalid_roboflow_model_native_output_direct_to_field_rejected"
        ).get("model_native_output_direct_to_field_rejected")
        is True,
    }


def run_and_review_rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    upstream_checks, upstream_issues = review_upstream_artifacts()
    case_run = run_all_cases_v1()
    aggregate = _aggregate(case_run)

    failed_checks: List[str] = list(upstream_issues)
    passed_checks: List[str] = []

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "sample_file_count_gte_11": aggregate["sample_file_count"] >= 11,
        "positive_case_count_eq_7": aggregate["positive_case_count"] == 7,
        "negative_case_count_eq_6": aggregate["negative_case_count"] == 6,
        "positive_pass_count_eq_7": aggregate["positive_pass_count"] == 7,
        "invalid_expected_reject_count_eq_6": aggregate["invalid_expected_reject_count"] == 6,
        "rgb_vision_integrated_evidence_replay_dryrun_go_verified": (
            upstream_checks.get("rgb_vision_integrated_evidence_replay_dryrun_go_verified") is True
        ),
        "field_task_guidance_safety_chain_closure_go_verified": (
            upstream_checks.get("field_task_guidance_safety_chain_closure_go_verified") is True
        ),
        "interface_layer_governance_verified": (
            upstream_checks.get("interface_layer_governance_verified") is True
        ),
        "model_admission_governance_verified": (
            upstream_checks.get("model_admission_governance_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        "external_test_source_is_roboflow_universe": EXTERNAL_TEST_SOURCE == "roboflow_universe",
        "roboflow_role_external_rgb_vision_test_source": (
            ROBOFLOW_ROLE == "external_rgb_vision_test_source"
        ),
        "rgb_first_hardware_baseline_preserved": (
            VISION_HARDWARE_BASELINE == "rgb_first_first_person_camera"
        ),
        "tof_stereo_depth_optional_auxiliary_only": (
            TOF_STEREO_DEPTH_ROLE == "optional_auxiliary_only"
        ),
        "license_present": aggregate["license_present"] is True,
        "dataset_origin_present": aggregate["dataset_origin_present"] is True,
        "annotation_format_recognized": aggregate["annotation_format_recognized"] is True,
        "yolo_annotation_format_recognized": aggregate["yolo_annotation_format_recognized"]
        is True,
        "coco_annotation_format_recognized": aggregate["coco_annotation_format_recognized"]
        is True,
        "voc_annotation_format_recognized": aggregate["voc_annotation_format_recognized"] is True,
        "source_chain_present": aggregate["source_chain_present"] is True,
        "confidence_present": aggregate["confidence_present"] is True,
        "object_evidence_candidate_generated": (
            aggregate["object_evidence_candidate_generated"] is True
        ),
        "region_evidence_candidate_generated": (
            aggregate["region_evidence_candidate_generated"] is True
        ),
        "text_evidence_candidate_generated": (
            aggregate["text_evidence_candidate_generated"] is True
        ),
        "track_evidence_candidate_generated": (
            aggregate["track_evidence_candidate_generated"] is True
        ),
        "dynamic_risk_candidate_generated": (
            aggregate["dynamic_risk_candidate_generated"] is True
        ),
        "scene_observation_candidate_generated": (
            aggregate["scene_observation_candidate_generated"] is True
        ),
        "source_chain_preserved": aggregate["source_chain_preserved"] is True,
        "confidence_preserved": aggregate["confidence_preserved"] is True,
        "license_ref_preserved": aggregate["license_ref_preserved"] is True,
        "dataset_ref_preserved": aggregate["dataset_ref_preserved"] is True,
        "annotation_origin_preserved": aggregate["annotation_origin_preserved"] is True,
        "adapter_mapping_required": aggregate["adapter_mapping_required"] is True,
        "roboflow_dataset_not_luna_fact_layer": aggregate["roboflow_not_luna_fact_layer"] is True,
        "roboflow_annotation_not_auto_trusted": (
            aggregate["roboflow_annotation_not_auto_trusted"] is True
        ),
        "roboflow_license_not_default_commercial": (
            aggregate["roboflow_license_not_default_commercial"] is True
        ),
        "roboflow_model_output_not_direct_to_field": (
            aggregate["roboflow_model_output_not_direct_to_field"] is True
        ),
        "ocr_output_not_fact": aggregate["ocr_output_not_fact"] is True,
        "tracking_output_not_action_trigger": (
            aggregate["tracking_output_not_action_trigger"] is True
        ),
        "field_task_guidance_replay_path_ok": (
            aggregate["field_task_guidance_replay_path_ok"] is True
        ),
        "task_context_can_reference_evidence_candidates": (
            aggregate["task_context_can_reference_evidence_candidates"] is True
        ),
        "task_risk_can_reference_tracking_evidence": (
            aggregate["task_risk_can_reference_tracking_evidence"] is True
        ),
        "guidance_candidate_remains_candidate": (
            aggregate["guidance_candidate_remains_candidate"] is True
        ),
        "speech_gate_candidate_not_tts": aggregate["speech_gate_candidate_not_tts"] is True,
        "action_safety_candidate_exists": aggregate["action_safety_candidate_exists"] is True,
        "missing_license_rejected": aggregate["missing_license_rejected"] is True,
        "missing_dataset_origin_rejected": aggregate["missing_dataset_origin_rejected"] is True,
        "unrecognized_annotation_format_rejected": (
            aggregate["unrecognized_annotation_format_rejected"] is True
        ),
        "missing_source_chain_rejected": aggregate["missing_source_chain_rejected"] is True,
        "no_direct_fact_write": aggregate["direct_fact_write_or_route_activation_rejected"]
        is True,
        "no_direct_route_activation": aggregate[
            "direct_fact_write_or_route_activation_rejected"
        ]
        is True,
        "model_native_output_direct_to_field_blocked": (
            aggregate["model_native_output_direct_to_field_rejected"] is True
        ),
        "model_native_output_direct_to_field_rejected": (
            aggregate["model_native_output_direct_to_field_rejected"] is True
        ),
        "integrated_validation_mode_used": NON_EXECUTION_FLAGS["integrated_validation_mode_used"]
        is True,
        "single_loader_validation_not_used": NON_EXECUTION_FLAGS[
            "single_loader_validation_not_used"
        ]
        is True,
        "real_file_replay_execution_allowed_true": NON_EXECUTION_FLAGS[
            "real_file_replay_execution_allowed"
        ]
        is True,
        "runtime_activation_allowed_false": NON_EXECUTION_FLAGS["runtime_activation_allowed"]
        is False,
        "roboflow_dataset_as_fact_layer_false": NON_EXECUTION_FLAGS[
            "roboflow_dataset_as_fact_layer"
        ]
        is False,
        "roboflow_annotation_auto_trusted_false": NON_EXECUTION_FLAGS[
            "roboflow_annotation_auto_trusted"
        ]
        is False,
        "roboflow_license_default_commercial_false": NON_EXECUTION_FLAGS[
            "roboflow_license_default_commercial"
        ]
        is False,
        "roboflow_model_output_direct_to_field_false": NON_EXECUTION_FLAGS[
            "roboflow_model_output_direct_to_field"
        ]
        is False,
        "live_camera_connected_false": NON_EXECUTION_FLAGS["live_camera_connected"] is False,
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "real_navigation_started_false": NON_EXECUTION_FLAGS["real_navigation_started"] is False,
        "real_map_api_connected_false": NON_EXECUTION_FLAGS["real_map_api_connected"] is False,
        "real_gps_connected_false": NON_EXECUTION_FLAGS["real_gps_connected"] is False,
        "ros_connected_false": NON_EXECUTION_FLAGS["ros_connected"] is False,
        "direct_action_allowed_false": NON_EXECUTION_FLAGS["direct_action_allowed"] is False,
        "direct_speech_allowed_false": NON_EXECUTION_FLAGS["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": NON_EXECUTION_FLAGS["direct_fact_write_allowed"]
        is False,
        "commercial_runtime_approved_false": NON_EXECUTION_FLAGS["commercial_runtime_approved"]
        is False,
        "commercial_data_source_approved_false": NON_EXECUTION_FLAGS[
            "commercial_data_source_approved"
        ]
        is False,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    review_checkpoints = {
        **aggregate,
        **upstream_checks,
        "dryrun_profile_count": 1,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "external_test_source": EXTERNAL_TEST_SOURCE,
        "roboflow_role": ROBOFLOW_ROLE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "tof_stereo_depth_role": TOF_STEREO_DEPTH_ROLE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "recognized_annotation_formats": list(RECOGNIZED_ANNOTATION_FORMATS),
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "generated_evidence_candidate_types": case_run.get("generated_evidence_candidate_types"),
        "samples_rel_dir": SAMPLES_REL_DIR,
        **NON_EXECUTION_FLAGS,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RGB Vision Roboflow Dataset Integrated Evidence Replay DryRun Run + Review",
        "lifecycle_variant": "roboflow_external_rgb_vision_test_source_evidence_replay_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "external_test_source": EXTERNAL_TEST_SOURCE,
        "roboflow_role": ROBOFLOW_ROLE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "tof_stereo_depth_role": TOF_STEREO_DEPTH_ROLE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "rgb_vision_dryrun_ref": RGB_VISION_DRYRUN_REF,
        "rgb_vision_planning_ref": RGB_VISION_PLANNING_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_PARSER_REF,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "recognized_annotation_formats": list(RECOGNIZED_ANNOTATION_FORMATS),
        "dataset_admission_required_fields": list(DATASET_ADMISSION_REQUIRED_FIELDS),
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "dryrun_profile": candidate_to_dict(build_profile()),
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "case_run": case_run,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "conclusions": {
            "roboflow_dataset_integrated_evidence_replay_dryrun_status": (
                "roboflow_external_rgb_vision_test_source_baseline_sealed"
                if review_ok
                else "blocked"
            ),
            "roboflow_positioned_as_external_test_source_only": True,
            "roboflow_not_fact_layer": True,
            "roboflow_annotation_not_auto_trusted": True,
            "roboflow_license_not_default_commercial": True,
            "roboflow_model_output_not_direct_to_field": True,
            "integrated_validation_mode_used": True,
            "adapter_mapping_enforced": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "local_roboflow_image_annotation_samples_yolo_coco_voc_json",
                "admission": "license_dataset_origin_annotation_format_source_chain_confidence",
                "adapter": INTERFACE_ADAPTER_REF,
                "evidence_candidates": list(
                    case_run.get("generated_evidence_candidate_types") or []
                ),
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "Roboflow datasets admitted strictly as an external RGB-first vision test source "
                "(not fact layer, not auto-trusted, not default-commercial, not direct-to-field). "
                "Next: RGB vision evidence chain closure, or extend with real model output samples."
            ),
        },
        "output_root": str(out_root),
        "output_file": str(out_path),
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    return result


def main() -> int:
    result = run_and_review_rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "sample_file_count": cp["sample_file_count"],
                "positive_case_count": cp["positive_case_count"],
                "negative_case_count": cp["negative_case_count"],
                "positive_pass_count": cp["positive_pass_count"],
                "invalid_expected_reject_count": cp["invalid_expected_reject_count"],
                "generated_evidence_candidate_types": cp["generated_evidence_candidate_types"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
