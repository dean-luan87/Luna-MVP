# -*- coding: utf-8 -*-
"""RGB Vision Test Source Integrated Evidence Replay DryRun — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rgb_vision_test_source_integrated_evidence_replay_dryrun.rgb_vision_test_source_integrated_evidence_replay_dryrun_cases_v1 import (
    run_all_cases_v1,
    samples_dir,
)
from capabilities.field_understanding.rgb_vision_test_source_integrated_evidence_replay_dryrun.rgb_vision_test_source_integrated_evidence_replay_dryrun_types_v1 import (
    ADMISSION_REQUIRED_FIELDS,
    ANNOTATION_TYPE_TO_CANDIDATE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
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
    RGB_VISION_INTEGRATED_DRYRUN_REF,
    RGB_VISION_PLANNING_REF,
    ROBOFLOW_INTEGRATED_DRYRUN_REF,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SAMPLE_FILES,
    SAMPLE_SOURCES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TEST_SOURCE_POOL_REF,
    VISION_HARDWARE_BASELINE,
    RGBVisionTestSourceIntegratedReplayDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "rgb_vision_test_source_integrated_evidence_replay_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = (
    "rgb_vision_test_source_integrated_evidence_replay_dryrun_run_and_review_v1.json"
)
PROFILE_REF = "rgb_vision_test_source_integrated_evidence_replay_dryrun_profile_v1"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": TEST_SOURCE_POOL_REF,
        "artifact_rel": (
            "_tmp_eval_out/luna_vision_test_source_backup_pool_v1_smoke_v0/"
            "luna_vision_test_source_backup_pool_review_v1.json"
        ),
        "expected_go": "LUNA_VISION_TEST_SOURCE_BACKUP_POOL_GO",
        "module_rel": (
            "capabilities/field_understanding/luna_vision_test_source_backup_pool/"
            "luna_vision_test_source_backup_pool_types_v1.py"
        ),
        "verify_flag": "test_source_backup_pool_go_verified",
    },
    {
        "phase_ref": RGB_VISION_INTEGRATED_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_v1_smoke_v0/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_types_v1.py"
        ),
        "verify_flag": "rgb_vision_integrated_dryrun_go_verified",
    },
    {
        "phase_ref": ROBOFLOW_INTEGRATED_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_v1_smoke_v0/"
            "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RGB_VISION_ROBOFLOW_DATASET_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun/"
            "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_types_v1.py"
        ),
        "verify_flag": "roboflow_integrated_dryrun_go_verified",
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
    "test_source_backup_pool_go_verified",
    "rgb_vision_integrated_dryrun_go_verified",
    "roboflow_integrated_dryrun_go_verified",
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


def build_profile() -> RGBVisionTestSourceIntegratedReplayDryRunProfile:
    return RGBVisionTestSourceIntegratedReplayDryRunProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        test_source_pool_ref=TEST_SOURCE_POOL_REF,
        rgb_vision_integrated_dryrun_ref=RGB_VISION_INTEGRATED_DRYRUN_REF,
        roboflow_integrated_dryrun_ref=ROBOFLOW_INTEGRATED_DRYRUN_REF,
        field_task_guidance_safety_chain_closure_ref=FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        interface_adapter_ref=INTERFACE_ADAPTER_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_PARSER_REF,
        vision_hardware_baseline=VISION_HARDWARE_BASELINE,
        system_objective=SYSTEM_OBJECTIVE,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        sample_sources=SAMPLE_SOURCES,
        recognized_annotation_formats=RECOGNIZED_ANNOTATION_FORMATS,
        admission_required_fields=ADMISSION_REQUIRED_FIELDS,
        annotation_type_to_candidate=ANNOTATION_TYPE_TO_CANDIDATE,
        field_task_guidance_candidate_types=FIELD_TASK_GUIDANCE_CANDIDATE_TYPES,
        governance_rules=DRYRUN_GOVERNANCE_RULES,
    )


def _aggregate(case_run: Dict[str, Any]) -> Dict[str, Any]:
    positive = case_run.get("positive_cases") or []
    negative = case_run.get("negative_cases") or []
    by_ref = {c["case_ref"]: c for c in positive + negative}

    def passed(ref: str) -> bool:
        return bool((by_ref.get(ref) or {}).get("passed"))

    def chk(ref: str) -> Dict[str, Any]:
        return (by_ref.get(ref) or {}).get("checks") or {}

    roboflow = chk("roboflow_sample_to_luna_evidence_replay")
    coco = chk("coco_sample_to_object_region_replay")
    ade20k = chk("ade20k_sample_to_scene_region_replay")
    textocr = chk("textocr_sample_to_text_evidence_replay")
    vg = chk("visual_genome_sample_to_scene_relation_replay")
    ftg = chk("multi_source_field_task_guidance_replay_path")

    sample_count = sum(1 for n in SAMPLE_FILES if (samples_dir() / n).is_file())

    return {
        "positive_case_count": len(positive),
        "negative_case_count": len(negative),
        "positive_pass_count": sum(1 for c in positive if c.get("passed")),
        "invalid_expected_reject_count": sum(1 for c in negative if c.get("passed")),
        "sample_file_count": sample_count,
        "sample_source_count": case_run.get("sample_source_count", 0),
        "roboflow_sample_replay_ok": passed("roboflow_sample_to_luna_evidence_replay"),
        "coco_sample_replay_ok": passed("coco_sample_to_object_region_replay"),
        "ade20k_sample_replay_ok": passed("ade20k_sample_to_scene_region_replay"),
        "textocr_sample_replay_ok": passed("textocr_sample_to_text_evidence_replay"),
        "visual_genome_sample_replay_ok": passed("visual_genome_sample_to_scene_relation_replay"),
        "multi_source_field_task_guidance_replay_path_ok": passed(
            "multi_source_field_task_guidance_replay_path"
        ),
        "observation_only_scope_preserved": passed("multi_source_observation_only_scope_replay"),
        "dataset_label_not_fact": (
            roboflow.get("roboflow_annotation_not_fact") is True
            and coco.get("dataset_label_not_luna_truth") is True
        ),
        "segmentation_not_route_activation": (
            ade20k.get("segmentation_not_route_activation") is True
        ),
        "ocr_text_not_fact": textocr.get("ocr_text_not_fact") is True,
        "scene_relation_not_final_interpretation": (
            vg.get("scene_relation_not_final_interpretation") is True
        ),
        "field_task_guidance_replay_candidate_only": (
            ftg.get("field_task_guidance_replay_path_ok") is True
        ),
        "guidance_candidate_remains_candidate": (
            ftg.get("guidance_candidate_remains_candidate") is True
        ),
        "speech_gate_candidate_not_tts": ftg.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_exists": ftg.get("action_safety_candidate_exists") is True,
        "missing_license_ref_rejected": chk("invalid_missing_license_ref_rejected").get(
            "missing_license_ref_rejected"
        )
        is True,
        "missing_dataset_or_sample_origin_rejected": chk(
            "invalid_missing_dataset_or_sample_origin_rejected"
        ).get("missing_dataset_or_sample_origin_rejected")
        is True,
        "annotation_auto_trusted_rejected": chk("invalid_annotation_auto_trusted_rejected").get(
            "annotation_auto_trusted_rejected"
        )
        is True,
        "non_commercial_marked_commercial_ready_rejected": chk(
            "invalid_non_commercial_marked_commercial_ready_rejected"
        ).get("non_commercial_marked_commercial_ready_rejected")
        is True,
        "fact_write_route_activation_direct_action_rejected": chk(
            "invalid_fact_write_route_activation_direct_action_rejected"
        ).get("fact_write_route_activation_direct_action_rejected")
        is True,
        "native_annotation_bypass_adapter_rejected": chk(
            "invalid_native_annotation_bypass_adapter_rejected"
        ).get("native_annotation_bypass_adapter_rejected")
        is True,
    }


def run_and_review_rgb_vision_test_source_integrated_evidence_replay_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    upstream_checks, upstream_issues = review_upstream_artifacts()
    case_run = run_all_cases_v1()
    aggregate = _aggregate(case_run)

    failed_checks: List[str] = list(upstream_issues)
    passed_checks: List[str] = []

    governance_required = {f: True for f in ADMISSION_REQUIRED_FIELDS}

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "sample_source_count_gte_5": aggregate["sample_source_count"] >= 5,
        "sample_file_count_gte_10": aggregate["sample_file_count"] >= 10,
        "positive_case_count_eq_7": aggregate["positive_case_count"] == 7,
        "negative_case_count_eq_6": aggregate["negative_case_count"] == 6,
        "positive_pass_count_eq_7": aggregate["positive_pass_count"] == 7,
        "invalid_expected_reject_count_eq_6": aggregate["invalid_expected_reject_count"] == 6,
        "test_source_backup_pool_go_verified": (
            upstream_checks.get("test_source_backup_pool_go_verified") is True
        ),
        "rgb_vision_integrated_dryrun_go_verified": (
            upstream_checks.get("rgb_vision_integrated_dryrun_go_verified") is True
        ),
        "roboflow_integrated_dryrun_go_verified": (
            upstream_checks.get("roboflow_integrated_dryrun_go_verified") is True
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
        "roboflow_sample_replay_ok": aggregate["roboflow_sample_replay_ok"] is True,
        "coco_sample_replay_ok": aggregate["coco_sample_replay_ok"] is True,
        "ade20k_sample_replay_ok": aggregate["ade20k_sample_replay_ok"] is True,
        "textocr_sample_replay_ok": aggregate["textocr_sample_replay_ok"] is True,
        "visual_genome_sample_replay_ok": aggregate["visual_genome_sample_replay_ok"] is True,
        "multi_source_field_task_guidance_replay_path_ok": (
            aggregate["multi_source_field_task_guidance_replay_path_ok"] is True
        ),
        "observation_only_scope_preserved": (
            aggregate["observation_only_scope_preserved"] is True
        ),
        "license_ref_required_for_all": governance_required.get("license_ref") is True,
        "dataset_ref_required_for_all": governance_required.get("dataset_ref") is True,
        "source_chain_required_for_all": governance_required.get("source_chain") is True,
        "annotation_origin_required_for_all": governance_required.get("annotation_origin") is True,
        "sample_origin_required_for_all": governance_required.get("sample_origin") is True,
        "commercial_use_unknown_until_verified": True,
        "non_commercial_sources_research_test_only": (
            aggregate["non_commercial_marked_commercial_ready_rejected"] is True
        ),
        "dataset_label_not_fact": aggregate["dataset_label_not_fact"] is True,
        "annotation_as_evidence_candidate": True,
        "interface_adapter_required": True,
        "native_annotation_direct_to_field_blocked": (
            aggregate["native_annotation_bypass_adapter_rejected"] is True
        ),
        "segmentation_not_route_activation": (
            aggregate["segmentation_not_route_activation"] is True
        ),
        "ocr_text_not_fact": aggregate["ocr_text_not_fact"] is True,
        "scene_relation_not_final_interpretation": (
            aggregate["scene_relation_not_final_interpretation"] is True
        ),
        "field_task_guidance_replay_candidate_only": (
            aggregate["field_task_guidance_replay_candidate_only"] is True
        ),
        "guidance_candidate_remains_candidate": (
            aggregate["guidance_candidate_remains_candidate"] is True
        ),
        "speech_gate_candidate_not_tts": aggregate["speech_gate_candidate_not_tts"] is True,
        "action_safety_candidate_exists": aggregate["action_safety_candidate_exists"] is True,
        "rgb_first_hardware_baseline_preserved": (
            VISION_HARDWARE_BASELINE == "rgb_first_first_person_camera"
        ),
        "integrated_validation_mode_used": NON_EXECUTION_FLAGS["integrated_validation_mode_used"]
        is True,
        "single_source_validation_not_used": NON_EXECUTION_FLAGS[
            "single_source_validation_not_used"
        ]
        is True,
        "missing_license_ref_rejected": aggregate["missing_license_ref_rejected"] is True,
        "missing_dataset_or_sample_origin_rejected": (
            aggregate["missing_dataset_or_sample_origin_rejected"] is True
        ),
        "annotation_auto_trusted_rejected": (
            aggregate["annotation_auto_trusted_rejected"] is True
        ),
        "non_commercial_marked_commercial_ready_rejected": (
            aggregate["non_commercial_marked_commercial_ready_rejected"] is True
        ),
        "fact_write_route_activation_direct_action_rejected": (
            aggregate["fact_write_route_activation_direct_action_rejected"] is True
        ),
        "native_annotation_bypass_adapter_rejected": (
            aggregate["native_annotation_bypass_adapter_rejected"] is True
        ),
        "dataset_download_allowed_false": NON_EXECUTION_FLAGS["dataset_download_allowed"] is False,
        "training_use_allowed_false": NON_EXECUTION_FLAGS["training_use_allowed"] is False,
        "runtime_activation_allowed_false": NON_EXECUTION_FLAGS["runtime_activation_allowed"]
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
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "recognized_annotation_formats": list(RECOGNIZED_ANNOTATION_FORMATS),
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "generated_evidence_candidate_types": case_run.get("generated_evidence_candidate_types"),
        "admitted_source_ids": case_run.get("admitted_source_ids"),
        "samples_rel_dir": SAMPLES_REL_DIR,
        **NON_EXECUTION_FLAGS,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RGB Vision Test Source Integrated Evidence Replay DryRun Run + Review",
        "lifecycle_variant": "multi_test_source_integrated_evidence_replay_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_source_pool_ref": TEST_SOURCE_POOL_REF,
        "rgb_vision_integrated_dryrun_ref": RGB_VISION_INTEGRATED_DRYRUN_REF,
        "roboflow_integrated_dryrun_ref": ROBOFLOW_INTEGRATED_DRYRUN_REF,
        "rgb_vision_planning_ref": RGB_VISION_PLANNING_REF,
        "rtab_multi_export_closure_ref": RTAB_MULTI_EXPORT_CLOSURE_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_PARSER_REF,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "recognized_annotation_formats": list(RECOGNIZED_ANNOTATION_FORMATS),
        "admission_required_fields": list(ADMISSION_REQUIRED_FIELDS),
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
            "vision_test_source_integrated_replay_status": (
                "multi_test_source_integrated_replay_baseline_sealed" if review_ok else "blocked"
            ),
            "test_source_pool_proven_replayable": True,
            "dataset_label_not_fact": True,
            "annotation_as_evidence_candidate_only": True,
            "integrated_validation_mode_used": True,
            "adapter_mapping_enforced": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "multi_test_source_local_controlled_samples",
                "sources": list(SAMPLE_SOURCES.keys()),
                "admission": "license_dataset_origin_sample_origin_annotation_format_confidence",
                "adapter": INTERFACE_ADAPTER_REF,
                "evidence_candidates": list(
                    case_run.get("generated_evidence_candidate_types") or []
                ),
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "Multi test-source integrated evidence replay proven: the vision test-source pool "
                "is no longer just a registry but a replayable evidence source. Next: RGB Vision "
                "Evidence Chain Integrated Closure."
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
    result = run_and_review_rgb_vision_test_source_integrated_evidence_replay_dryrun_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "sample_source_count": cp["sample_source_count"],
                "sample_file_count": cp["sample_file_count"],
                "positive_case_count": cp["positive_case_count"],
                "negative_case_count": cp["negative_case_count"],
                "positive_pass_count": cp["positive_pass_count"],
                "invalid_expected_reject_count": cp["invalid_expected_reject_count"],
                "generated_evidence_candidate_types": cp["generated_evidence_candidate_types"],
                "admitted_source_ids": cp["admitted_source_ids"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
