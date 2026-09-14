# -*- coding: utf-8 -*-
"""Recognition Model Download And Install DryRun — run and review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_download_and_install_dryrun.recognition_model_download_and_install_dryrun_cases_v1 import (
    ALL_PLAN_FILES,
    INSTALL_PLAN_FILES,
    run_negative_cases,
    run_positive_cases,
)
from capabilities.field_understanding.recognition_model_download_and_install_dryrun.recognition_model_download_and_install_dryrun_types_v1 import (
    ALLOWED_CHECK_KINDS,
    ALLOWED_FLAGS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DOWNLOAD_LICENSE_PLANNING_REF,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INSTALL_CHECK_GO_KEYS,
    INSTALL_TARGET_GO_KEYS,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    INVOCATION_FEASIBILITY_DRYRUN_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    OUTPUT_ADAPTER_DRYRUN_REF,
    P0_INSTALL_TARGET_IDS,
    PHASE_ID,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_INSTALL_PLAN_FIELDS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SYSTEM_ADMISSION_PLANNING_REF,
    TARGET_CHAIN_REF,
    RecognitionModelDownloadInstallDryRunProfile,
    install_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "recognition_model_download_and_install_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_download_and_install_dryrun_run_and_review_v1.json"

_PKG = "capabilities/field_understanding/recognition_model_download_and_install_dryrun"
STEP_FILES = (
    f"{_PKG}/recognition_model_download_and_install_dryrun_types_v1.py",
    f"{_PKG}/recognition_model_download_and_install_dryrun_cases_v1.py",
    f"{_PKG}/run_and_review_recognition_model_download_and_install_dryrun_v1.py",
)

PROFILE_REF = "recognition_model_download_and_install_dryrun_profile_v1"

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": DOWNLOAD_LICENSE_PLANNING_REF,
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_download_license_and_local_availability_planning_v1_smoke_v0/"
            "recognition_model_download_license_and_local_availability_planning_review_v1.json"
        ),
        "expected_go": "RECOGNITION_MODEL_DOWNLOAD_LICENSE_AND_LOCAL_AVAILABILITY_PLANNING_GO",
        "verify_flag": "download_license_local_availability_planning_go_verified",
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
        "phase_ref": INVOCATION_FEASIBILITY_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_invocation_feasibility_dryrun_v1_smoke_v0/"
            "recognition_model_invocation_feasibility_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RECOGNITION_MODEL_INVOCATION_FEASIBILITY_DRYRUN_GO",
        "verify_flag": "invocation_feasibility_dryrun_go_verified",
    },
    {
        "phase_ref": OUTPUT_ADAPTER_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_output_adapter_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RECOGNITION_MODEL_OUTPUT_ADAPTER_DRYRUN_GO",
        "verify_flag": "output_adapter_dryrun_go_verified",
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

_REJECTION_GO_KEYS: Dict[str, str] = {
    "invalid_missing_license_ref": "missing_license_ref_rejected",
    "invalid_missing_download_source": "missing_download_source_rejected",
    "invalid_commercial_runtime_for_agpl_yolo": "agpl_commercial_runtime_ready_rejected",
    "invalid_real_inference_requested": "real_inference_requested_rejected",
    "invalid_dataset_download_requested": "dataset_download_requested_rejected",
    "invalid_adapter_dryrun_requested": "adapter_dryrun_requested_rejected",
    "invalid_live_camera_sensor_requested": "live_camera_sensor_requested_rejected",
    "invalid_direct_action_speech_fact_write": "direct_action_speech_fact_write_rejected",
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
    return install_to_dict(
        RecognitionModelDownloadInstallDryRunProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            download_license_planning_ref=DOWNLOAD_LICENSE_PLANNING_REF,
            system_admission_planning_ref=SYSTEM_ADMISSION_PLANNING_REF,
            invocation_feasibility_dryrun_ref=INVOCATION_FEASIBILITY_DRYRUN_REF,
            output_adapter_dryrun_ref=OUTPUT_ADAPTER_DRYRUN_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            p0_install_target_ids=P0_INSTALL_TARGET_IDS,
            required_install_plan_fields=REQUIRED_INSTALL_PLAN_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            prohibited_request_flags=PROHIBITED_REQUEST_FLAGS,
            allowed_check_kinds=ALLOWED_CHECK_KINDS,
            governance_rules=DRYRUN_GOVERNANCE_RULES,
        )
    )


def run_and_review_recognition_model_download_and_install_dryrun_v1(
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
    for fname in ALL_PLAN_FILES:
        if (_REPO_ROOT / _PKG / "samples" / fname).is_file():
            sample_file_count += 1
        else:
            failed_checks.append(f"sample_missing:{fname}")

    upstream_checks, upstream_issues = _review_upstream()
    failed_checks.extend(upstream_issues)

    positive_results = run_positive_cases()
    negative_results = run_negative_cases()

    positive_pass_count = sum(1 for r in positive_results if r.passed)
    invalid_expected_reject_count = sum(1 for r in negative_results if r.passed)

    pos_by_id = {r.case_id: r for r in positive_results}
    neg_by_id = {r.case_id: r for r in negative_results}

    # target coverage / install check GO keys
    target_covered = {}
    install_check_ok = {}
    for target in P0_INSTALL_TARGET_IDS:
        from capabilities.field_understanding.recognition_model_download_and_install_dryrun.recognition_model_download_and_install_dryrun_cases_v1 import (
            POSITIVE_CASE_BY_TARGET,
        )
        case = pos_by_id.get(POSITIVE_CASE_BY_TARGET[target])
        covered = bool(case and case.accepted)
        target_covered[INSTALL_TARGET_GO_KEYS[target]] = covered
        install_check_ok[INSTALL_CHECK_GO_KEYS[target]] = bool(case and case.passed)

    matrix_case = pos_by_id.get("p0_install_matrix_check")
    yolo_case = pos_by_id.get("yolo_lightweight_download_install_check")
    opencv_plan = json.loads(
        (_REPO_ROOT / _PKG / "samples" / INSTALL_PLAN_FILES["opencv_visual_symbol_p0"]).read_text(
            encoding="utf-8"
        )
    )

    rejection_go = {
        go_key: bool(neg_by_id.get(case_id) and neg_by_id[case_id].passed)
        for case_id, go_key in _REJECTION_GO_KEYS.items()
    }

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "p0_install_target_count_eq_3": len(P0_INSTALL_TARGET_IDS) == 3,
        "positive_case_count_eq_4": len(positive_results) == 4,
        "negative_case_count_eq_8": len(negative_results) == 8,
        "positive_pass_count_eq_4": positive_pass_count == 4,
        "invalid_expected_reject_count_eq_8": invalid_expected_reject_count == 8,
        **{k: (upstream_checks.get(k) is True) for k in _REQUIRED_VERIFY_FLAGS},
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        **target_covered,
        "p0_install_matrix_ok": bool(matrix_case and matrix_case.passed),
        "download_source_required": True,
        "license_ref_required": True,
        "package_name_required": True,
        "allowed_use_required": True,
        "commercial_use_status_required": True,
        "source_chain_required": True,
        "fallback_plan_required": True,
        **install_check_ok,
        "yolo_commercial_runtime_not_approved": bool(
            yolo_case and yolo_case.passed
        )
        and (NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False),
        "opencv_no_model_weight_required": opencv_plan.get("model_weight_required") is False,
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
        "step": "Recognition Model Download And Install DryRun Run and Review",
        "lifecycle_variant": "recognition_model_download_and_install_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "download_license_planning_ref": DOWNLOAD_LICENSE_PLANNING_REF,
        "system_admission_planning_ref": SYSTEM_ADMISSION_PLANNING_REF,
        "invocation_feasibility_dryrun_ref": INVOCATION_FEASIBILITY_DRYRUN_REF,
        "output_adapter_dryrun_ref": OUTPUT_ADAPTER_DRYRUN_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "allowed_check_kinds": list(ALLOWED_CHECK_KINDS),
        "allowed_flags": dict(ALLOWED_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "dryrun_profile": _build_profile(),
        "p0_install_target_count": len(P0_INSTALL_TARGET_IDS),
        "sample_file_count": sample_file_count,
        "positive_case_count": len(positive_results),
        "negative_case_count": len(negative_results),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "positive_cases": [asdict(r) for r in positive_results],
        "negative_cases": [asdict(r) for r in negative_results],
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "conclusions": {
            "download_and_install_dryrun_status": (
                "p0_download_and_install_dryrun_verified" if review_ok else "blocked"
            ),
            "p0_install_targets": list(P0_INSTALL_TARGET_IDS),
            "yolo_license_note": "agpl_3_0_test_only_commercial_runtime_not_approved",
            "opencv_note": "rule_runtime_no_model_weight_required",
            "next_phase_ref": NEXT_PHASE_REF,
            "transition_note": (
                "P0 install plans (RapidOCR / lightweight YOLO / OpenCV rule-based symbol) are admitted "
                "and the allowed non-destructive checks (package/import/version/local-resource) are "
                "planned. No real inference, no real image/video recognition, no adapter dry-run, no "
                "main-chain integration, no dataset/training. YOLO stays test-only with "
                "commercial_runtime_approved=false; OpenCV requires no model weights. Next: Real Model "
                "Output Adapter DryRun, running P0 real models on small samples and feeding output "
                "through the Luna adapter."
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
    result = run_and_review_recognition_model_download_and_install_dryrun_v1()
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
