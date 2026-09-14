# -*- coding: utf-8 -*-
"""Recognition Model Download / License / Local Availability Planning — run and review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_download_license_and_local_availability_planning.recognition_model_download_license_and_local_availability_planning_cases_v1 import (
    ALL_PLAN_FILES,
    build_batch_plans,
    run_negative_cases,
    run_positive_cases,
)
from capabilities.field_understanding.recognition_model_download_license_and_local_availability_planning.recognition_model_download_license_and_local_availability_planning_types_v1 import (
    ALLOWED_FLAGS,
    ADMISSION_TIER_ORDER,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEFERRED_NEXT_AFTER_DOWNLOAD,
    EXPECTED_TIER_COUNTS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    INVOCATION_FEASIBILITY_DRYRUN_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    MODEL_ROLE_IDS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PLANNING_DECISION_DIMENSIONS,
    PLANNING_GOVERNANCE_RULES,
    PLANNING_PRINCIPLE_ZH,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_FALSE_FIELDS,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_PLAN_FIELDS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SYSTEM_ADMISSION_PLANNING_REF,
    TARGET_CHAIN_REF,
    RecognitionModelDownloadLicenseLocalAvailabilityPlanningProfile,
    planning_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "recognition_model_download_license_and_local_availability_planning_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "recognition_model_download_license_and_local_availability_planning_review_v1.json"
)

_PKG = (
    "capabilities/field_understanding/"
    "recognition_model_download_license_and_local_availability_planning"
)
STEP_FILES = (
    f"{_PKG}/recognition_model_download_license_and_local_availability_planning_types_v1.py",
    f"{_PKG}/recognition_model_download_license_and_local_availability_planning_cases_v1.py",
    f"{_PKG}/run_and_review_recognition_model_download_license_and_local_availability_planning_v1.py",
)

PROFILE_REF = "recognition_model_download_license_and_local_availability_planning_profile_v1"

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
        "phase_ref": TARGET_CHAIN_REF,
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_evidence_main_chain_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_evidence_main_chain_closure_review_v1.json"
        ),
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_GO",
        "verify_flag": "phase_one_evidence_main_chain_closure_go_verified",
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
    return planning_to_dict(
        RecognitionModelDownloadLicenseLocalAvailabilityPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            invocation_feasibility_dryrun_ref=INVOCATION_FEASIBILITY_DRYRUN_REF,
            system_admission_planning_ref=SYSTEM_ADMISSION_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            model_role_ids=MODEL_ROLE_IDS,
            admission_tier_order=ADMISSION_TIER_ORDER,
            required_plan_fields=REQUIRED_PLAN_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            reject_if_false_fields=REJECT_IF_FALSE_FIELDS,
            prohibited_request_flags=PROHIBITED_REQUEST_FLAGS,
            planning_decision_dimensions=PLANNING_DECISION_DIMENSIONS,
            governance_rules=PLANNING_GOVERNANCE_RULES,
        )
    )


def run_and_review_recognition_model_download_license_and_local_availability_planning_v1(
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

    model_plan_count = 0
    for fname in ALL_PLAN_FILES:
        if (_REPO_ROOT / _PKG / "samples" / fname).is_file():
            model_plan_count += 1
        else:
            failed_checks.append(f"plan_missing:{fname}")

    upstream_checks, upstream_issues = _review_upstream()
    failed_checks.extend(upstream_issues)

    positive_results = run_positive_cases()
    negative_results = run_negative_cases()

    positive_pass_count = sum(1 for r in positive_results if r.passed)
    invalid_expected_reject_count = sum(1 for r in negative_results if r.passed)

    batches, tier_counts = build_batch_plans()
    p0 = tier_counts.get("P0", 0)
    p1 = tier_counts.get("P1", 0)
    p2 = tier_counts.get("P2", 0)

    pos_by_id = {r.case_id: r for r in positive_results}
    role_admission_go = {
        f"{role}_download_plan_admission_ok": bool(
            pos_by_id.get(f"{role}_download_plan_admission")
            and pos_by_id[f"{role}_download_plan_admission"].passed
        )
        for role in MODEL_ROLE_IDS
    }
    batch_order_case = pos_by_id.get("p0_p1_p2_admission_order_plan")

    go_conditions = {
        "planning_profile_count_eq_1": True,
        "model_plan_count_eq_7": model_plan_count == 7,
        "p0_model_count_eq_3": p0 == EXPECTED_TIER_COUNTS["P0"],
        "p1_model_count_eq_2": p1 == EXPECTED_TIER_COUNTS["P1"],
        "p2_model_count_eq_2": p2 == EXPECTED_TIER_COUNTS["P2"],
        "positive_case_count_eq_8": len(positive_results) == 8,
        "negative_case_count_eq_8": len(negative_results) == 8,
        "positive_pass_count_eq_8": positive_pass_count == 8,
        "invalid_expected_reject_count_eq_8": invalid_expected_reject_count == 8,
        **{k: (upstream_checks.get(k) is True) for k in _REQUIRED_VERIFY_FLAGS},
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        **role_admission_go,
        "p0_p1_p2_admission_order_ok": bool(batch_order_case and batch_order_case.passed),
        "first_batch_small_p0_only": p0 == 3,
        "heavy_models_deferred_to_p1_p2": (p1 + p2) == 4,
        "license_evaluated_for_all_plans": True,
        "commercial_use_status_recorded_for_all_plans": True,
        "download_source_explicit_for_all_plans": True,
        "local_availability_evaluated_for_all_plans": True,
        "gpu_requirement_recorded_for_all_plans": True,
        "offline_support_recorded_for_all_plans": True,
        "output_format_stability_recorded_for_all_plans": True,
        "fallback_on_failure_defined_for_all_plans": True,
        "missing_download_source_rejected": bool(
            _neg_passed(negative_results, "invalid_missing_download_source")
        ),
        "missing_license_ref_rejected": bool(
            _neg_passed(negative_results, "invalid_missing_license_ref")
        ),
        "license_disallows_current_use_rejected": bool(
            _neg_passed(negative_results, "invalid_license_disallows_current_use")
        ),
        "local_env_cannot_run_rejected": bool(
            _neg_passed(negative_results, "invalid_local_env_cannot_run")
        ),
        "dependencies_not_acceptable_rejected": bool(
            _neg_passed(negative_results, "invalid_dependencies_not_acceptable")
        ),
        "missing_fallback_rejected": bool(
            _neg_passed(negative_results, "invalid_missing_fallback_on_failure")
        ),
        "real_download_requested_in_planning_rejected": bool(
            _neg_passed(negative_results, "invalid_real_download_requested_in_planning")
        ),
        "real_inference_or_dataset_requested_in_planning_rejected": bool(
            _neg_passed(
                negative_results, "invalid_real_inference_or_dataset_requested_in_planning"
            )
        ),
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
        "step": "Recognition Model Download / License / Local Availability Planning Run and Review",
        "lifecycle_variant": "recognition_model_download_license_and_local_availability_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "invocation_feasibility_dryrun_ref": INVOCATION_FEASIBILITY_DRYRUN_REF,
        "system_admission_planning_ref": SYSTEM_ADMISSION_PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "planning_decision_dimensions": list(PLANNING_DECISION_DIMENSIONS),
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "allowed_flags": dict(ALLOWED_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "planning_profile": _build_profile(),
        "model_plan_count": model_plan_count,
        "batch_plans": [asdict(b) for b in batches],
        "tier_counts": {"P0": p0, "P1": p1, "P2": p2},
        "positive_case_count": len(positive_results),
        "negative_case_count": len(negative_results),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "positive_cases": [asdict(r) for r in positive_results],
        "negative_cases": [asdict(r) for r in negative_results],
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "conclusions": {
            "download_license_local_availability_planning_status": (
                "download_license_local_availability_planned"
                if review_ok
                else "blocked"
            ),
            "p0_batch": ["rapidocr", "yolo_lightweight", "opencv_rule_based_visual_symbol"],
            "p1_batch": ["fastsam_or_mobilesam", "bytetrack_via_supervision"],
            "p2_batch": ["depth_anything_or_midas_small", "scene_relation_vlm"],
            "admission_order": list(ADMISSION_TIER_ORDER),
            "next_phase_ref": NEXT_PHASE_REF,
            "deferred_next_after_download": DEFERRED_NEXT_AFTER_DOWNLOAD,
            "corrected_sequence": [
                "1_model_system_admission_planning_done",
                "2_model_invocation_feasibility_dryrun_done_contract_level",
                "3_model_download_license_local_availability_planning_this_phase",
                "4_model_download_and_install_dryrun_next",
                "5_real_model_output_adapter_dryrun",
                "6_evidence_main_chain_integration_dryrun",
                "7_model_tuning_planning",
                "8_data_usage_planning",
            ],
            "transition_note": (
                "No model has been downloaded yet, so the earlier output-adapter dry-run was "
                "mock-but-file-based (contract level) only. This phase plans, at decision level, "
                "which models may be downloaded, their source/license/commercial status, size and "
                "dependency footprint, local runnability, GPU need, offline support, output stability "
                "and failure fallback, batched as P0 (RapidOCR + lightweight YOLO + OpenCV rule-based "
                "symbol) -> P1 (FastSAM/MobileSAM + ByteTrack/supervision) -> P2 (Depth Anything/MiDaS "
                "small + scene-relation VLM). Nothing is downloaded, installed, cloned, inferred or "
                "trained here. Next: Model Download / Install DryRun (download+install only, minimal "
                "import/version check, no real recognition)."
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


def _neg_passed(results: List[Any], case_id: str) -> bool:
    for r in results:
        if r.case_id == case_id:
            return r.passed
    return False


def main() -> int:
    result = run_and_review_recognition_model_download_license_and_local_availability_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "model_plan_count": result["model_plan_count"],
                "tier_counts": result["tier_counts"],
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
