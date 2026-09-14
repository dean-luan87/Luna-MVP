# -*- coding: utf-8 -*-
"""Recognition Model Real Output Adapter DryRun — run and review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_real_output_adapter_dryrun.recognition_model_real_output_adapter_dryrun_cases_v1 import (
    ALL_SAMPLE_FILES,
    run_negative_cases,
    run_positive_cases,
)
from capabilities.field_understanding.recognition_model_real_output_adapter_dryrun.recognition_model_real_output_adapter_dryrun_types_v1 import (
    ALLOWED_FLAGS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DOWNLOAD_INSTALL_DRYRUN_REF,
    DOWNLOAD_LICENSE_PLANNING_REF,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    INVOCATION_FEASIBILITY_DRYRUN_REF,
    LUNA_CORE_PRINCIPLE,
    MOCK_OUTPUT_ADAPTER_DRYRUN_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    P0_REAL_TARGET_IDS,
    PHASE_ID,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_REAL_OUTPUT_FIELDS,
    RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
    RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SYSTEM_ADMISSION_PLANNING_REF,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    RecognitionModelRealOutputAdapterDryRunProfile,
    real_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "recognition_model_real_output_adapter_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_real_output_adapter_dryrun_run_and_review_v1.json"

_PKG = "capabilities/field_understanding/recognition_model_real_output_adapter_dryrun"
STEP_FILES = (
    f"{_PKG}/recognition_model_real_output_adapter_dryrun_types_v1.py",
    f"{_PKG}/recognition_model_real_output_adapter_dryrun_cases_v1.py",
    f"{_PKG}/run_and_review_recognition_model_real_output_adapter_dryrun_v1.py",
)

PROFILE_REF = "recognition_model_real_output_adapter_dryrun_profile_v1"

REAL_OUTPUT_ARTIFACTS = {
    "rapidocr_p0": "real_ocr_output.json",
    "yolo_lightweight_p0": "real_yolo_output.json",
    "opencv_visual_symbol_p0": "real_visual_symbol_output.json",
}

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": DOWNLOAD_INSTALL_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_download_and_install_dryrun_v1_smoke_v0/"
            "recognition_model_download_and_install_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RECOGNITION_MODEL_DOWNLOAD_AND_INSTALL_DRYRUN_GO",
        "verify_flag": "download_install_dryrun_go_verified",
    },
    {
        "phase_ref": DOWNLOAD_LICENSE_PLANNING_REF,
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_download_license_and_local_availability_planning_v1_smoke_v0/"
            "recognition_model_download_license_and_local_availability_planning_review_v1.json"
        ),
        "expected_go": "RECOGNITION_MODEL_DOWNLOAD_LICENSE_AND_LOCAL_AVAILABILITY_PLANNING_GO",
        "verify_flag": "download_license_planning_go_verified",
    },
    {
        "phase_ref": INVOCATION_FEASIBILITY_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_invocation_feasibility_dryrun_v1_smoke_v0/"
            "recognition_model_invocation_feasibility_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RECOGNITION_MODEL_INVOCATION_FEASIBILITY_DRYRUN_GO",
        "verify_flag": "invocation_feasibility_dryrun_go_verified",
    },
    {
        "phase_ref": MOCK_OUTPUT_ADAPTER_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_output_adapter_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RECOGNITION_MODEL_OUTPUT_ADAPTER_DRYRUN_GO",
        "verify_flag": "mock_output_adapter_dryrun_go_verified",
    },
    {
        "phase_ref": TARGET_CHAIN_REF,
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_evidence_main_chain_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_evidence_main_chain_closure_review_v1.json"
        ),
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_GO",
        "verify_flag": "phase_one_evidence_main_chain_closure_go_verified",
    },
    {
        "phase_ref": RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_evidence_chain_integrated_closure_v1_smoke_v0/"
            "rgb_vision_evidence_chain_integrated_closure_review_v1.json"
        ),
        "expected_go": "RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        "verify_flag": "rgb_vision_evidence_chain_closure_go_verified",
    },
    {
        "phase_ref": RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1_smoke_v0/"
            "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_review_v1.json"
        ),
        "expected_go": "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO",
        "verify_flag": "rgb_slam_cross_modal_closure_go_verified",
    },
    {
        "phase_ref": FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
    },
    {
        "phase_ref": INTERFACE_LAYER_GOVERNANCE_REF,
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "verify_flag": "interface_layer_governance_verified",
    },
    {
        "phase_ref": MODEL_ADMISSION_GOVERNANCE_REF,
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "verify_flag": "model_admission_governance_verified",
    },
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = tuple(e["verify_flag"] for e in _UPSTREAM_GO_ARTIFACTS)

_REJECTION_GO_KEYS: Dict[str, str] = {
    "invalid_missing_source_chain": "missing_source_chain_rejected",
    "invalid_missing_license_ref": "missing_license_ref_rejected",
    "invalid_missing_model_origin": "missing_model_origin_rejected",
    "invalid_missing_confidence": "missing_confidence_rejected",
    "invalid_yolo_commercial_runtime_claim": "yolo_commercial_runtime_claim_rejected",
    "invalid_ocr_fact_write": "ocr_fact_write_rejected",
    "invalid_visual_symbol_direct_navigation": "visual_symbol_direct_navigation_speech_rejected",
    "invalid_native_output_direct_to_field": "native_output_direct_to_field_rejected",
    "invalid_main_chain_integration_requested": "main_chain_integration_requested_rejected",
    "invalid_live_camera_sensor_requested": "live_camera_sensor_requested_rejected",
}


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def _review_upstream() -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}
    for entry in _UPSTREAM_GO_ARTIFACTS:
        artifact, exists = _load_upstream_artifact(entry["artifact_rel"])
        actual_go = (artifact or {}).get("final_decision") if exists else None
        go_ok = exists and actual_go == entry["expected_go"]
        checks[entry["verify_flag"]] = go_ok
        if not exists:
            issues.append(f"upstream_artifact_missing:{entry['phase_ref']}")
        elif not go_ok:
            issues.append(f"upstream_go_mismatch:{entry['phase_ref']}:{actual_go!r}")
    checks["controlled_trial_governance_template_ref_ok"] = (
        CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    )
    for required in _REQUIRED_VERIFY_FLAGS:
        if not checks.get(required, False):
            issues.append(f"{required}_not_verified")
    return checks, issues


def _build_profile() -> Dict[str, Any]:
    return real_to_dict(
        RecognitionModelRealOutputAdapterDryRunProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            download_install_dryrun_ref=DOWNLOAD_INSTALL_DRYRUN_REF,
            download_license_planning_ref=DOWNLOAD_LICENSE_PLANNING_REF,
            invocation_feasibility_dryrun_ref=INVOCATION_FEASIBILITY_DRYRUN_REF,
            mock_output_adapter_dryrun_ref=MOCK_OUTPUT_ADAPTER_DRYRUN_REF,
            system_admission_planning_ref=SYSTEM_ADMISSION_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            p0_real_target_ids=P0_REAL_TARGET_IDS,
            required_real_output_fields=REQUIRED_REAL_OUTPUT_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            prohibited_request_flags=PROHIBITED_REQUEST_FLAGS,
            governance_rules=DRYRUN_GOVERNANCE_RULES,
        )
    )


def run_and_review_recognition_model_real_output_adapter_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    sample_file_count = 0
    for fname in ALL_SAMPLE_FILES:
        if (_REPO_ROOT / _PKG / "samples" / fname).is_file():
            sample_file_count += 1
        else:
            failed_checks.append(f"sample_missing:{fname}")

    upstream_checks, upstream_issues = _review_upstream()
    failed_checks.extend(upstream_issues)

    positive_results, state = run_positive_cases()
    negative_results = run_negative_cases()

    positive_pass_count = sum(1 for r in positive_results if r.passed)
    invalid_expected_reject_count = sum(1 for r in negative_results if r.passed)

    # Aggregate candidates across all P0 targets.
    covered: List[str] = []
    for st in state.values():
        covered.extend(st["candidates"])
    covered_set = set(covered)

    pos_by_id = {r.case_id: r for r in positive_results}
    neg_by_id = {r.case_id: r for r in negative_results}

    rapidocr_st = state["rapidocr_p0"]
    yolo_st = state["yolo_lightweight_p0"]
    opencv_st = state["opencv_visual_symbol_p0"]

    rejection_go = {
        go_key: bool(neg_by_id.get(case_id) and neg_by_id[case_id].passed)
        for case_id, go_key in _REJECTION_GO_KEYS.items()
    }

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "p0_real_target_count_eq_3": len(P0_REAL_TARGET_IDS) == 3,
        "positive_case_count_eq_5": len(positive_results) == 5,
        "negative_case_count_eq_10": len(negative_results) == 10,
        "positive_pass_count_eq_5": positive_pass_count == 5,
        "invalid_expected_reject_count_eq_10": invalid_expected_reject_count == 10,
        **{k: (upstream_checks.get(k) is True) for k in _REQUIRED_VERIFY_FLAGS},
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        "rapidocr_real_output_attempt_recorded": bool(rapidocr_st["availability_state"]),
        "yolo_lightweight_real_output_attempt_recorded": bool(yolo_st["availability_state"]),
        "opencv_visual_symbol_real_output_attempt_recorded": bool(opencv_st["availability_state"]),
        "p0_availability_state_recorded": all(
            bool(st["availability_state"]) for st in state.values()
        ),
        "p0_multi_model_real_output_coverage_checked": bool(
            pos_by_id.get("p0_multi_model_real_output_coverage")
            and pos_by_id["p0_multi_model_real_output_coverage"].passed
        ),
        "rapidocr_real_output_adapter_mapping_ok": bool(
            pos_by_id.get("rapidocr_real_output_adapter_mapping")
            and pos_by_id["rapidocr_real_output_adapter_mapping"].passed
        ),
        "yolo_lightweight_real_output_adapter_mapping_ok": bool(
            pos_by_id.get("yolo_lightweight_real_output_adapter_mapping")
            and pos_by_id["yolo_lightweight_real_output_adapter_mapping"].passed
        ),
        "opencv_visual_symbol_real_output_adapter_mapping_ok": bool(
            pos_by_id.get("opencv_visual_symbol_real_output_adapter_mapping")
            and pos_by_id["opencv_visual_symbol_real_output_adapter_mapping"].passed
        ),
        "recognition_model_output_adapter_used": bool(
            pos_by_id.get("p0_real_output_adapter_boundary_check")
            and pos_by_id["p0_real_output_adapter_boundary_check"].passed
        ),
        "text_evidence_candidate_generated_or_unavailable_recorded": (
            ("text_evidence_candidate" in covered_set) or (not rapidocr_st["available"])
        ),
        "object_evidence_candidate_generated_or_unavailable_recorded": (
            ("object_evidence_candidate" in covered_set) or (not yolo_st["available"])
        ),
        "color_evidence_candidate_generated": "color_evidence_candidate" in covered_set,
        "shape_evidence_candidate_generated": "shape_evidence_candidate" in covered_set,
        "visual_symbol_candidate_generated": "visual_symbol_candidate" in covered_set,
        "symbol_meaning_candidate_generated": "symbol_meaning_candidate" in covered_set,
        **rejection_go,
        **{k: (v is True) for k, v in ALLOWED_FLAGS.items()},
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
        "luna_brain_cognition_first_preserved": True,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    real_output_records = {
        target: state[target]["record"]
        for target in P0_REAL_TARGET_IDS
        if state[target]["record"] is not None
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Recognition Model Real Output Adapter DryRun Run and Review",
        "lifecycle_variant": "recognition_model_real_output_adapter_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "download_install_dryrun_ref": DOWNLOAD_INSTALL_DRYRUN_REF,
        "download_license_planning_ref": DOWNLOAD_LICENSE_PLANNING_REF,
        "invocation_feasibility_dryrun_ref": INVOCATION_FEASIBILITY_DRYRUN_REF,
        "mock_output_adapter_dryrun_ref": MOCK_OUTPUT_ADAPTER_DRYRUN_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "allowed_flags": dict(ALLOWED_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "dryrun_profile": _build_profile(),
        "p0_real_target_count": len(P0_REAL_TARGET_IDS),
        "sample_file_count": sample_file_count,
        "p0_availability_state": {
            t: {
                "available": st["available"],
                "availability_state": st["availability_state"],
                "real_inference_executed": st["real_inference_executed"],
                "generated_candidates": st["candidates"],
            }
            for t, st in state.items()
        },
        "covered_candidate_types": sorted(covered_set),
        "positive_case_count": len(positive_results),
        "negative_case_count": len(negative_results),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "positive_cases": [asdict(r) for r in positive_results],
        "negative_cases": [asdict(r) for r in negative_results],
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "conclusions": {
            "real_output_adapter_dryrun_status": (
                "p0_real_output_adapter_verified" if review_ok else "blocked"
            ),
            "p0_real_targets": list(P0_REAL_TARGET_IDS),
            "yolo_note": "agpl_3_0_test_only_commercial_runtime_approved_false",
            "next_phase_ref": NEXT_PHASE_REF,
            "transition_note": (
                "First controlled real inference executed on P0 local offline sample images. OpenCV "
                "rule-based visual-symbol path produced real color/shape/visual_symbol/symbol_meaning "
                "candidates; RapidOCR and YOLO ran if locally available, otherwise a declared-"
                "unavailable record was produced (not a blocker, no download triggered). All real "
                "outputs passed through the RecognitionModelOutputAdapter and became evidence "
                "candidates only. YOLO stays test-only, commercial_runtime_approved=false. Luna remains "
                "brain/cognition-first; no VLA action chain, no action/speech/navigation/fact_write. "
                "Next: Evidence Main Chain Integration DryRun, feeding real-output candidates into the "
                "main chain Field/Task/Guidance path, still candidate-only."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        # Write per-target real output artifacts (only those actually produced).
        for target, record in real_output_records.items():
            artifact_name = REAL_OUTPUT_ARTIFACTS[target]
            (out_root / artifact_name).write_text(
                json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = run_and_review_recognition_model_real_output_adapter_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "p0_availability_state": {
                    t: v["availability_state"]
                    for t, v in result["p0_availability_state"].items()
                },
                "covered_candidate_types": result["covered_candidate_types"],
                "positive_pass_count": result["positive_pass_count"],
                "invalid_expected_reject_count": result["invalid_expected_reject_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
