# -*- coding: utf-8 -*-
"""RGB Vision / OCR / Segmentation Integrated Evidence Replay DryRun — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_cases_v1 import (
    run_all_cases_v1,
    samples_dir,
)
from capabilities.field_understanding.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPTH_HARDWARE_DEFAULT,
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
    PLANNING_REF,
    POSITIVE_CASE_REFS,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    SOURCE_TO_CANDIDATE_TYPE,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TOF_STEREO_DEPTH_ROLE,
    VISION_HARDWARE_BASELINE,
    RGBVisionIntegratedEvidenceReplayDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = (
    "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_run_and_review_v1.json"
)
PROFILE_REF = "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_profile_v1"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": PLANNING_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_v1_smoke_v0/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_review_v1.json"
        ),
        "expected_go": "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_ocr_segmentation_integrated_evidence_replay_planning/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_types_v1.py"
        ),
        "verify_flag": "planning_go_verified",
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
    "planning_go_verified",
    "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
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


def build_profile() -> RGBVisionIntegratedEvidenceReplayDryRunProfile:
    return RGBVisionIntegratedEvidenceReplayDryRunProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        planning_ref=PLANNING_REF,
        rtab_multi_export_closure_ref=RTAB_MULTI_EXPORT_CLOSURE_REF,
        field_task_guidance_safety_chain_closure_ref=FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        interface_adapter_ref=INTERFACE_ADAPTER_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_PARSER_REF,
        vision_hardware_baseline=VISION_HARDWARE_BASELINE,
        depth_hardware_default=DEPTH_HARDWARE_DEFAULT,
        tof_stereo_depth_role=TOF_STEREO_DEPTH_ROLE,
        system_objective=SYSTEM_OBJECTIVE,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        source_to_candidate_type=SOURCE_TO_CANDIDATE_TYPE,
        field_task_guidance_candidate_types=FIELD_TASK_GUIDANCE_CANDIDATE_TYPES,
        governance_rules=DRYRUN_GOVERNANCE_RULES,
    )


def _aggregate(case_run: Dict[str, Any]) -> Dict[str, Any]:
    positive = case_run.get("positive_cases") or []
    negative = case_run.get("negative_cases") or []
    by_ref = {c["case_ref"]: c for c in positive + negative}

    def chk(ref: str) -> Dict[str, Any]:
        return (by_ref.get(ref) or {}).get("checks") or {}

    scene = chk("rgb_scene_object_region_integrated_replay")
    ocr = chk("rgb_ocr_scene_text_integrated_replay")
    track = chk("rgb_tracking_dynamic_risk_integrated_replay")
    depth = chk("rgb_monocular_depth_vio_spatial_hint_replay")
    relation = chk("rgb_scene_relation_task_context_replay")
    ftg = chk("rgb_integrated_field_task_guidance_replay_path")
    observation = chk("rgb_observation_only_replay_scope")

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
        "track_evidence_candidate_generated": "track_evidence_candidate" in generated,
        "dynamic_risk_candidate_generated": "dynamic_risk_candidate" in generated,
        "text_evidence_candidate_generated": "text_evidence_candidate" in generated,
        "spatial_hint_candidate_generated": "spatial_hint_candidate" in generated,
        "scene_relation_candidate_generated": "scene_relation_candidate" in generated,
        "source_chain_preserved": scene.get("source_chain_preserved") is True
        and ocr.get("source_chain_preserved") is True,
        "confidence_preserved": ocr.get("confidence_preserved") is True,
        "origin_metadata_preserved": scene.get("origin_metadata_preserved") is True
        and ocr.get("origin_metadata_preserved") is True,
        "adapter_mapping_required": True,
        "native_output_direct_to_field_blocked": (
            chk("invalid_native_output_direct_to_field_rejected").get(
                "native_output_direct_to_field_rejected"
            )
            is True
        ),
        "ocr_output_not_fact": ocr.get("ocr_output_not_fact") is True,
        "segmentation_output_not_route_activation": (
            chk("invalid_segmentation_route_activation_rejected").get(
                "segmentation_route_activation_rejected"
            )
            is True
        ),
        "tracking_output_not_action_trigger": track.get("tracking_output_not_action_trigger")
        is True,
        "monocular_depth_vio_not_field_identity": depth.get(
            "monocular_depth_vio_not_field_identity"
        )
        is True,
        "scene_relation_not_final_interpretation": relation.get(
            "scene_relation_not_final_interpretation"
        )
        is True,
        "field_task_guidance_replay_path_ok": ftg.get("field_task_guidance_replay_path_ok")
        is True,
        "task_context_can_reference_relation_candidates": ftg.get(
            "task_context_can_reference_relation_candidates"
        )
        is True,
        "task_risk_can_reference_tracking_and_spatial_hint": ftg.get(
            "task_risk_can_reference_tracking_and_spatial_hint"
        )
        is True,
        "guidance_candidate_remains_candidate": ftg.get("guidance_candidate_remains_candidate")
        is True,
        "speech_gate_candidate_not_tts": ftg.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_exists": ftg.get("action_safety_candidate_exists") is True,
        "observation_only_scope_preserved": observation.get("observation_only_scope_preserved")
        is True,
        "missing_source_chain_rejected": chk("invalid_missing_source_chain_rejected").get(
            "missing_source_chain_rejected"
        )
        is True,
        "direct_fact_write_ocr_rejected": chk("invalid_direct_fact_write_ocr_rejected").get(
            "direct_fact_write_ocr_rejected"
        )
        is True,
        "segmentation_route_activation_rejected": chk(
            "invalid_segmentation_route_activation_rejected"
        ).get("segmentation_route_activation_rejected")
        is True,
        "tracking_direct_action_speech_rejected": chk(
            "invalid_tracking_direct_action_speech_rejected"
        ).get("tracking_direct_action_speech_rejected")
        is True,
        "depth_vio_field_identity_override_rejected": chk(
            "invalid_depth_vio_field_identity_override_rejected"
        ).get("depth_vio_field_identity_override_rejected")
        is True,
        "native_output_direct_to_field_rejected": chk(
            "invalid_native_output_direct_to_field_rejected"
        ).get("native_output_direct_to_field_rejected")
        is True,
    }


def run_and_review_rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_v1(
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
        "sample_file_count_gte_12": aggregate["sample_file_count"] >= 12,
        "positive_case_count_eq_7": aggregate["positive_case_count"] == 7,
        "negative_case_count_eq_6": aggregate["negative_case_count"] == 6,
        "positive_pass_count_eq_7": aggregate["positive_pass_count"] == 7,
        "invalid_expected_reject_count_eq_6": aggregate["invalid_expected_reject_count"] == 6,
        "planning_go_verified": upstream_checks.get("planning_go_verified") is True,
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": (
            upstream_checks.get("rtab_multi_export_spatial_evidence_replay_closure_go_verified")
            is True
        ),
        "field_task_guidance_safety_chain_closure_go_verified": (
            upstream_checks.get("field_task_guidance_safety_chain_closure_go_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        "interface_layer_governance_verified": (
            upstream_checks.get("interface_layer_governance_verified") is True
        ),
        "model_admission_governance_verified": (
            upstream_checks.get("model_admission_governance_verified") is True
        ),
        "rgb_first_hardware_baseline_preserved": (
            VISION_HARDWARE_BASELINE == "rgb_first_first_person_camera"
        ),
        "tof_stereo_depth_optional_auxiliary_only": (
            TOF_STEREO_DEPTH_ROLE == "optional_auxiliary_only"
        ),
        "cognitive_world_reconstruction_objective_preserved": (
            SYSTEM_OBJECTIVE == "cognitive_world_reconstruction"
        ),
        "scene_observation_candidate_generated": (
            aggregate["scene_observation_candidate_generated"] is True
        ),
        "object_evidence_candidate_generated": (
            aggregate["object_evidence_candidate_generated"] is True
        ),
        "region_evidence_candidate_generated": (
            aggregate["region_evidence_candidate_generated"] is True
        ),
        "track_evidence_candidate_generated": (
            aggregate["track_evidence_candidate_generated"] is True
        ),
        "dynamic_risk_candidate_generated": (
            aggregate["dynamic_risk_candidate_generated"] is True
        ),
        "text_evidence_candidate_generated": (
            aggregate["text_evidence_candidate_generated"] is True
        ),
        "spatial_hint_candidate_generated": (
            aggregate["spatial_hint_candidate_generated"] is True
        ),
        "scene_relation_candidate_generated": (
            aggregate["scene_relation_candidate_generated"] is True
        ),
        "source_chain_preserved": aggregate["source_chain_preserved"] is True,
        "confidence_preserved": aggregate["confidence_preserved"] is True,
        "origin_metadata_preserved": aggregate["origin_metadata_preserved"] is True,
        "adapter_mapping_required": aggregate["adapter_mapping_required"] is True,
        "native_output_direct_to_field_blocked": (
            aggregate["native_output_direct_to_field_blocked"] is True
        ),
        "ocr_output_not_fact": aggregate["ocr_output_not_fact"] is True,
        "segmentation_output_not_route_activation": (
            aggregate["segmentation_output_not_route_activation"] is True
        ),
        "tracking_output_not_action_trigger": (
            aggregate["tracking_output_not_action_trigger"] is True
        ),
        "monocular_depth_vio_not_field_identity": (
            aggregate["monocular_depth_vio_not_field_identity"] is True
        ),
        "scene_relation_not_final_interpretation": (
            aggregate["scene_relation_not_final_interpretation"] is True
        ),
        "field_task_guidance_replay_path_ok": (
            aggregate["field_task_guidance_replay_path_ok"] is True
        ),
        "task_context_can_reference_relation_candidates": (
            aggregate["task_context_can_reference_relation_candidates"] is True
        ),
        "task_risk_can_reference_tracking_and_spatial_hint": (
            aggregate["task_risk_can_reference_tracking_and_spatial_hint"] is True
        ),
        "guidance_candidate_remains_candidate": (
            aggregate["guidance_candidate_remains_candidate"] is True
        ),
        "speech_gate_candidate_not_tts": aggregate["speech_gate_candidate_not_tts"] is True,
        "action_safety_candidate_exists": aggregate["action_safety_candidate_exists"] is True,
        "observation_only_scope_preserved": (
            aggregate["observation_only_scope_preserved"] is True
        ),
        "missing_source_chain_rejected": aggregate["missing_source_chain_rejected"] is True,
        "direct_fact_write_ocr_rejected": aggregate["direct_fact_write_ocr_rejected"] is True,
        "segmentation_route_activation_rejected": (
            aggregate["segmentation_route_activation_rejected"] is True
        ),
        "tracking_direct_action_speech_rejected": (
            aggregate["tracking_direct_action_speech_rejected"] is True
        ),
        "depth_vio_field_identity_override_rejected": (
            aggregate["depth_vio_field_identity_override_rejected"] is True
        ),
        "native_output_direct_to_field_rejected": (
            aggregate["native_output_direct_to_field_rejected"] is True
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
        "depth_hardware_default": DEPTH_HARDWARE_DEFAULT,
        "tof_stereo_depth_role": TOF_STEREO_DEPTH_ROLE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "generated_evidence_candidate_types": case_run.get("generated_evidence_candidate_types"),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "rgb_first_hardware_baseline_preserved": True,
        "cognitive_world_reconstruction_objective_preserved": True,
        **NON_EXECUTION_FLAGS,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RGB Vision / OCR / Segmentation Integrated Evidence Replay DryRun Run + Review",
        "lifecycle_variant": "rgb_first_integrated_evidence_replay_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "depth_hardware_default": DEPTH_HARDWARE_DEFAULT,
        "tof_stereo_depth_role": TOF_STEREO_DEPTH_ROLE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "planning_ref": PLANNING_REF,
        "rtab_multi_export_closure_ref": RTAB_MULTI_EXPORT_CLOSURE_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_PARSER_REF,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
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
            "rgb_vision_integrated_evidence_replay_dryrun_status": (
                "rgb_vision_file_integrated_replay_baseline_sealed" if review_ok else "blocked"
            ),
            "rgb_first_baseline_preserved": True,
            "tof_stereo_depth_optional_auxiliary_only": True,
            "integrated_validation_mode_used": True,
            "adapter_mapping_enforced": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "local_rgb_frame_video_plus_mock_file_based_model_outputs",
                "adapter": INTERFACE_ADAPTER_REF,
                "evidence_candidates": list(
                    case_run.get("generated_evidence_candidate_types") or []
                ),
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "RGB vision / OCR / segmentation / tracking file-based integrated replay baseline "
                "sealed. Next: RGB vision evidence chain closure, or extend to real model output "
                "samples."
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
    result = run_and_review_rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_v1()
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
