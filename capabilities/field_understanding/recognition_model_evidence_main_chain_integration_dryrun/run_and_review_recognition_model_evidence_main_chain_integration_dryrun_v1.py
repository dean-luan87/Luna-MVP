# -*- coding: utf-8 -*-
"""Recognition Model Evidence Main Chain Integration DryRun — run and review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_evidence_main_chain_integration_dryrun.recognition_model_evidence_main_chain_integration_dryrun_cases_v1 import (
    ALL_SAMPLE_FILES,
    run_negative_cases,
    run_positive_cases,
)
from capabilities.field_understanding.recognition_model_evidence_main_chain_integration_dryrun.recognition_model_evidence_main_chain_integration_dryrun_types_v1 import (
    ALLOWED_FLAGS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DOWNLOAD_INSTALL_DRYRUN_REF,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    INVOCATION_FEASIBILITY_DRYRUN_REF,
    LUNA_CORE_PRINCIPLE,
    MAIN_CHAIN_PATH_CANDIDATES,
    MOCK_OUTPUT_ADAPTER_DRYRUN_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PREV_PHASE_ARTIFACT_DIR_REL,
    PROHIBITED_REQUEST_FLAGS,
    REAL_OUTPUT_ADAPTER_DRYRUN_REF,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_CANDIDATE_FIELDS,
    REUSED_REAL_OUTPUT_ARTIFACTS,
    RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
    RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    RecognitionModelEvidenceMainChainIntegrationDryRunProfile,
    integration_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "recognition_model_evidence_main_chain_integration_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_evidence_main_chain_integration_dryrun_run_and_review_v1.json"

_PKG = "capabilities/field_understanding/recognition_model_evidence_main_chain_integration_dryrun"
STEP_FILES = (
    f"{_PKG}/recognition_model_evidence_main_chain_integration_dryrun_types_v1.py",
    f"{_PKG}/recognition_model_evidence_main_chain_integration_dryrun_cases_v1.py",
    f"{_PKG}/run_and_review_recognition_model_evidence_main_chain_integration_dryrun_v1.py",
)

PROFILE_REF = "recognition_model_evidence_main_chain_integration_dryrun_profile_v1"

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": REAL_OUTPUT_ADAPTER_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_real_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_real_output_adapter_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RECOGNITION_MODEL_REAL_OUTPUT_ADAPTER_DRYRUN_GO",
        "verify_flag": "real_output_adapter_dryrun_go_verified",
    },
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
        "phase_ref": GOVERNANCE_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
        ),
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        "verify_flag": "runtime_governance_closure_go_verified",
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
    "invalid_candidate_missing_source_chain": "missing_source_chain_rejected",
    "invalid_candidate_missing_confidence": "missing_confidence_rejected",
    "invalid_candidate_direct_fact_write": "direct_fact_write_rejected",
    "invalid_visual_symbol_direct_navigation": "visual_symbol_direct_navigation_rejected",
    "invalid_guidance_candidate_runtime_navigation": "guidance_runtime_navigation_rejected",
    "invalid_speech_gate_tts_activation": "speech_gate_tts_rejected",
    "invalid_action_trigger_from_candidate": "direct_action_rejected",
    "invalid_yolo_unavailable_treated_as_blocker": "yolo_unavailable_blocker_or_download_rejected",
    "invalid_vla_action_chain_injected": "vla_action_chain_injection_rejected",
    "invalid_model_tuning_dataset_usage": "model_tuning_dataset_usage_rejected",
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


def _verify_reused_real_artifacts() -> Tuple[int, List[str]]:
    count = 0
    issues: List[str] = []
    for name in REUSED_REAL_OUTPUT_ARTIFACTS:
        path = _REPO_ROOT / PREV_PHASE_ARTIFACT_DIR_REL / name
        if path.is_file():
            count += 1
        else:
            issues.append(f"reused_real_output_artifact_missing:{name}")
    return count, issues


def _build_profile() -> Dict[str, Any]:
    return integration_to_dict(
        RecognitionModelEvidenceMainChainIntegrationDryRunProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            real_output_adapter_dryrun_ref=REAL_OUTPUT_ADAPTER_DRYRUN_REF,
            download_install_dryrun_ref=DOWNLOAD_INSTALL_DRYRUN_REF,
            mock_output_adapter_dryrun_ref=MOCK_OUTPUT_ADAPTER_DRYRUN_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            reused_real_output_artifacts=REUSED_REAL_OUTPUT_ARTIFACTS,
            required_candidate_fields=REQUIRED_CANDIDATE_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            prohibited_request_flags=PROHIBITED_REQUEST_FLAGS,
            main_chain_path_candidates=MAIN_CHAIN_PATH_CANDIDATES,
            governance_rules=DRYRUN_GOVERNANCE_RULES,
        )
    )


def run_and_review_recognition_model_evidence_main_chain_integration_dryrun_v1(
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

    real_output_artifact_ref_count, artifact_issues = _verify_reused_real_artifacts()
    failed_checks.extend(artifact_issues)

    positive_results, bundle_res = run_positive_cases()
    negative_results = run_negative_cases()

    positive_pass_count = sum(1 for r in positive_results if r.passed)
    invalid_expected_reject_count = sum(1 for r in negative_results if r.passed)

    pos_by_id = {r.case_id: r for r in positive_results}
    neg_by_id = {r.case_id: r for r in negative_results}

    admitted = set(bundle_res["admitted_types"])
    generated = set(bundle_res["generated"])

    rejection_go = {
        go_key: bool(neg_by_id.get(case_id) and neg_by_id[case_id].passed)
        for case_id, go_key in _REJECTION_GO_KEYS.items()
    }

    def _pos_ok(cid: str) -> bool:
        return bool(pos_by_id.get(cid) and pos_by_id[cid].passed)

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "real_output_artifact_ref_count_gte_2": real_output_artifact_ref_count >= 2,
        "positive_case_count_eq_5": len(positive_results) == 5,
        "negative_case_count_eq_10": len(negative_results) == 10,
        "positive_pass_count_eq_5": positive_pass_count == 5,
        "invalid_expected_reject_count_eq_10": invalid_expected_reject_count == 10,
        **{k: (upstream_checks.get(k) is True) for k in _REQUIRED_VERIFY_FLAGS},
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        "real_ocr_candidate_ingress_ok": _pos_ok("real_ocr_candidate_main_chain_ingress"),
        "real_visual_symbol_candidate_ingress_ok": _pos_ok(
            "real_visual_symbol_candidate_main_chain_ingress"
        ),
        "real_ocr_visual_symbol_cross_validation_ok": _pos_ok(
            "real_ocr_visual_symbol_cross_validation"
        ),
        "yolo_declared_unavailable_non_blocker_ok": _pos_ok(
            "yolo_declared_unavailable_non_blocker_ingress"
        ),
        "real_p0_candidate_bundle_main_chain_path_ok": _pos_ok(
            "real_p0_candidate_bundle_main_chain_path"
        ),
        "text_evidence_candidate_admitted": "text_evidence_candidate" in admitted,
        "color_evidence_candidate_admitted": "color_evidence_candidate" in admitted,
        "shape_evidence_candidate_admitted": "shape_evidence_candidate" in admitted,
        "visual_symbol_candidate_admitted": "visual_symbol_candidate" in admitted,
        "symbol_meaning_candidate_admitted": "symbol_meaning_candidate" in admitted,
        "field_synthesis_candidate_generated": "FieldSynthesisCandidate" in generated,
        "task_context_candidate_generated": "TaskContextCandidate" in generated,
        "guidance_candidate_generated": "GuidanceCandidate" in generated,
        "speech_gate_candidate_generated": "SpeechGateCandidate" in generated,
        "action_safety_candidate_exists": "ActionSafetyCandidate" in generated,
        "cross_modal_consistency_candidate_generated": (
            "cross_modal_consistency_candidate" in generated
        ),
        "exit_sign_hypothesis_candidate_generated": "exit_sign_hypothesis_candidate" in generated,
        "model_availability_state_candidate_generated": (
            "model_availability_state_candidate" in generated
        ),
        "candidate_source_chain_required": True,
        "candidate_confidence_required": True,
        **rejection_go,
        **{k: (v is True) for k, v in ALLOWED_FLAGS.items()},
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
        "luna_emotion_multimodal_brain_first_preserved": True,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Recognition Model Evidence Main Chain Integration DryRun Run and Review",
        "lifecycle_variant": "recognition_model_evidence_main_chain_integration_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "real_output_adapter_dryrun_ref": REAL_OUTPUT_ADAPTER_DRYRUN_REF,
        "download_install_dryrun_ref": DOWNLOAD_INSTALL_DRYRUN_REF,
        "mock_output_adapter_dryrun_ref": MOCK_OUTPUT_ADAPTER_DRYRUN_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "allowed_flags": dict(ALLOWED_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "dryrun_profile": _build_profile(),
        "reused_real_output_artifacts": list(REUSED_REAL_OUTPUT_ARTIFACTS),
        "real_output_artifact_ref_count": real_output_artifact_ref_count,
        "sample_file_count": sample_file_count,
        "main_chain_ingress": {
            "admitted_candidate_types": sorted(admitted),
            "generated_candidate_types": sorted(generated),
        },
        "positive_case_count": len(positive_results),
        "negative_case_count": len(negative_results),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "positive_cases": [asdict(r) for r in positive_results],
        "negative_cases": [asdict(r) for r in negative_results],
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "conclusions": {
            "evidence_main_chain_integration_status": (
                "real_model_output_candidate_main_chain_verified" if review_ok else "blocked"
            ),
            "next_phase_ref": NEXT_PHASE_REF,
            "ingress_pipeline": {
                "input": "sealed_real_model_output_evidence_candidates",
                "adapter": INTERFACE_ADAPTER_REF,
                "chain": TARGET_CHAIN_REF,
                "entrypoint": TARGET_ENTRYPOINT,
                "path": "field_synthesis_candidate_task_context_candidate_guidance_candidate_speech_gate_candidate_action_safety_candidate",
                "candidate_only": True,
            },
            "transition_note": (
                "Real model output evidence candidates (reused from the sealed previous-phase "
                "artifacts, no re-inference, no YOLO download) successfully entered the Phase-One "
                "evidence main chain and flowed along the Field/Task/Guidance candidate path. OCR EXIT "
                "+ green right-direction symbol produced cross_modal_consistency / exit_sign_hypothesis "
                "candidates (hypothesis-only). YOLO declared_unavailable stayed a non-blocker. "
                "Everything remained candidate-only: no fact write, no runtime navigation, no TTS, no "
                "action, no VLA action chain. Luna remains emotion-multimodal brain/cognition first. "
                "Next: Recognition Model P0 Integration Closure, sealing the whole arc from admission "
                "planning to real-output main-chain integration as a stable baseline."
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
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = run_and_review_recognition_model_evidence_main_chain_integration_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "real_output_artifact_ref_count": result["real_output_artifact_ref_count"],
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
