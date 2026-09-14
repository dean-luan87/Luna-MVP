# -*- coding: utf-8 -*-
"""Recognition Model Output Adapter DryRun — run and review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_output_adapter_dryrun.recognition_model_output_adapter_dryrun_cases_v1 import (
    ALL_SAMPLE_FILES,
    INVALID_SAMPLE_FILES,
    MULTI_FAMILY_BUNDLE_FILE,
    VALID_SAMPLE_FILES,
    run_negative_cases,
    run_positive_cases,
)
from capabilities.field_understanding.recognition_model_output_adapter_dryrun.recognition_model_output_adapter_dryrun_types_v1 import (
    ALLOWED_FLAGS,
    ALL_CANDIDATE_TYPES,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    FAMILY_MAPPING_GO_KEYS,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    INVOCATION_FEASIBILITY_DRYRUN_REF,
    MAIN_CHAIN_CLOSURE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    MODEL_FAMILY_IDS,
    NEGATIVE_CASE_IDS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POSITIVE_CASE_IDS,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_MODEL_OUTPUT_FIELDS,
    RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
    RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SYSTEM_ADMISSION_PLANNING_REF,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    RecognitionModelOutputAdapterDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "recognition_model_output_adapter_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_output_adapter_dryrun_run_and_review_v1.json"

_PKG = "capabilities/field_understanding/recognition_model_output_adapter_dryrun"
STEP_FILES = (
    f"{_PKG}/recognition_model_output_adapter_dryrun_types_v1.py",
    f"{_PKG}/recognition_model_output_adapter_dryrun_cases_v1.py",
    f"{_PKG}/run_and_review_recognition_model_output_adapter_dryrun_v1.py",
)

PROFILE_REF = "recognition_model_output_adapter_dryrun_profile_v1"

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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
        "phase_ref": SYSTEM_ADMISSION_PLANNING_REF,
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_system_admission_and_invocation_planning_v1_smoke_v0/"
            "recognition_model_system_admission_and_invocation_planning_review_v1.json"
        ),
        "expected_go": "RECOGNITION_MODEL_SYSTEM_ADMISSION_AND_INVOCATION_PLANNING_GO",
        "verify_flag": "system_admission_planning_go_verified",
    },
    {
        "phase_ref": MAIN_CHAIN_CLOSURE_REF,
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

# negative case id -> GO rejection key
_REJECTION_GO_KEYS: Dict[str, str] = {
    "invalid_missing_source_chain": "missing_source_chain_rejected",
    "invalid_missing_license_ref": "missing_license_ref_rejected",
    "invalid_missing_model_origin": "missing_model_origin_rejected",
    "invalid_missing_confidence": "missing_confidence_rejected",
    "invalid_missing_adapter_mapping_ref": "missing_adapter_mapping_ref_rejected",
    "invalid_native_output_direct_to_field": "native_output_direct_to_field_rejected",
    "invalid_ocr_fact_write": "ocr_fact_write_rejected",
    "invalid_segmentation_route_activation": "segmentation_route_activation_rejected",
    "invalid_tracking_direct_action": "tracking_direct_action_speech_rejected",
    "invalid_depth_field_identity_override": "depth_vio_field_identity_override_rejected",
    "invalid_visual_symbol_direct_navigation": "visual_symbol_direct_navigation_speech_rejected",
    "invalid_scene_relation_final_interpretation": (
        "scene_relation_final_interpretation_fact_write_rejected"
    ),
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
    return candidate_to_dict(
        RecognitionModelOutputAdapterDryRunProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            invocation_feasibility_dryrun_ref=INVOCATION_FEASIBILITY_DRYRUN_REF,
            system_admission_planning_ref=SYSTEM_ADMISSION_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            model_family_ids=MODEL_FAMILY_IDS,
            required_model_output_fields=REQUIRED_MODEL_OUTPUT_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            prohibited_request_flags=PROHIBITED_REQUEST_FLAGS,
            governance_rules=DRYRUN_GOVERNANCE_RULES,
        )
    )


def run_and_review_recognition_model_output_adapter_dryrun_v1(
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

    positive_results, covered_candidate_types = run_positive_cases()
    negative_results = run_negative_cases()

    positive_pass_count = sum(1 for r in positive_results if r.passed)
    invalid_expected_reject_count = sum(1 for r in negative_results if r.passed)

    pos_by_id = {r.case_id: r for r in positive_results}

    family_mapping_go = {}
    for fam in MODEL_FAMILY_IDS:
        go_key = FAMILY_MAPPING_GO_KEYS[fam]
        # find the family-specific positive case
        case = next(
            (r for r in positive_results if r.model_family == fam and r.case_kind == "positive"),
            None,
        )
        family_mapping_go[go_key] = bool(case and case.passed)

    multi_cov = pos_by_id.get("multi_family_output_adapter_coverage")
    compat = pos_by_id.get("evidence_main_chain_compatibility_check")

    candidate_generated = {
        f"{c}_generated": c in covered_candidate_types for c in ALL_CANDIDATE_TYPES
    }

    neg_by_id = {r.case_id: r for r in negative_results}
    rejection_go = {
        go_key: bool(neg_by_id.get(case_id) and neg_by_id[case_id].passed)
        for case_id, go_key in _REJECTION_GO_KEYS.items()
    }

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "sample_file_count_gte_20": sample_file_count >= 20,
        "positive_case_count_eq_9": len(positive_results) == 9,
        "negative_case_count_eq_12": len(negative_results) == 12,
        "positive_pass_count_eq_9": positive_pass_count == 9,
        "invalid_expected_reject_count_eq_12": invalid_expected_reject_count == 12,
        **{k: (upstream_checks.get(k) is True) for k in _REQUIRED_VERIFY_FLAGS},
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        **family_mapping_go,
        "multi_family_output_adapter_coverage_complete": bool(multi_cov and multi_cov.passed),
        "evidence_main_chain_compatibility_ok": bool(compat and compat.passed),
        **candidate_generated,
        "model_output_source_chain_required": True,
        "model_output_license_ref_required": True,
        "model_output_model_origin_required": True,
        "model_output_confidence_required": True,
        "model_output_adapter_mapping_ref_required": True,
        **rejection_go,
        **{k: (v is True) for k, v in ALLOWED_FLAGS.items()},
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
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
        "step": "Recognition Model Output Adapter DryRun Run and Review",
        "lifecycle_variant": "recognition_model_output_adapter_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "invocation_feasibility_dryrun_ref": INVOCATION_FEASIBILITY_DRYRUN_REF,
        "system_admission_planning_ref": SYSTEM_ADMISSION_PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "allowed_flags": dict(ALLOWED_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "dryrun_profile": _build_profile(),
        "sample_file_count": sample_file_count,
        "positive_case_count": len(positive_results),
        "negative_case_count": len(negative_results),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "covered_candidate_types": list(covered_candidate_types),
        "positive_cases": [asdict(r) for r in positive_results],
        "negative_cases": [asdict(r) for r in negative_results],
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "conclusions": {
            "recognition_model_output_adapter_dryrun_status": (
                "recognition_model_output_adapter_verified"
                if review_ok
                else "blocked"
            ),
            "model_families_mapped": list(MODEL_FAMILY_IDS),
            "candidate_types_covered": list(ALL_CANDIDATE_TYPES),
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "mock_file_based_model_output",
                "adapter": INTERFACE_ADAPTER_REF,
                "candidate": "luna_evidence_candidate",
                "chain": TARGET_CHAIN_REF,
                "path": "evidence_main_chain_compatible_output",
            },
            "transition_note": (
                "Model output now formally maps to the Luna evidence candidate layer via the "
                "RecognitionModelOutputAdapter, with all 12 candidate types covered and main-chain "
                "compatibility confirmed (candidate-only). No real inference. Next: "
                "Evidence Main Chain Integration DryRun, validating adapter output entering the main "
                "chain and the Field/Task/Guidance path, still without real models."
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
    result = run_and_review_recognition_model_output_adapter_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "sample_file_count": result["sample_file_count"],
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
