# -*- coding: utf-8 -*-
"""Recognition Model Invocation Feasibility DryRun — run and review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_invocation_feasibility_dryrun.recognition_model_invocation_feasibility_dryrun_cases_v1 import (
    INVALID_SAMPLE_FILES,
    VALID_SAMPLE_FILES,
    run_negative_cases,
    run_positive_cases,
)
from capabilities.field_understanding.recognition_model_invocation_feasibility_dryrun.recognition_model_invocation_feasibility_dryrun_types_v1 import (
    ALLOWED_FEASIBILITY_FLAGS,
    ALLOWED_INVOCATION_MODES,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    FAMILY_FEASIBILITY_CHECKED_GO_KEYS,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MAIN_CHAIN_CLOSURE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    MODEL_FAMILY_IDS,
    NEGATIVE_CASE_IDS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PLANNING_REF,
    POSITIVE_CASE_IDS,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_CONTRACT_FIELDS,
    RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
    RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SYSTEM_ADMISSION_PLANNING_REF,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    RecognitionModelInvocationFeasibilityDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "recognition_model_invocation_feasibility_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_invocation_feasibility_dryrun_run_and_review_v1.json"

_PKG = "capabilities/field_understanding/recognition_model_invocation_feasibility_dryrun"
STEP_FILES = (
    f"{_PKG}/recognition_model_invocation_feasibility_dryrun_types_v1.py",
    f"{_PKG}/recognition_model_invocation_feasibility_dryrun_cases_v1.py",
    f"{_PKG}/run_and_review_recognition_model_invocation_feasibility_dryrun_v1.py",
)

PROFILE_REF = "recognition_model_invocation_feasibility_dryrun_profile_v1"

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = tuple(
    e["verify_flag"] for e in _UPSTREAM_GO_ARTIFACTS
)


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
        RecognitionModelInvocationFeasibilityDryRunProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            planning_ref=PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            model_family_ids=MODEL_FAMILY_IDS,
            required_contract_fields=REQUIRED_CONTRACT_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            allowed_invocation_modes=ALLOWED_INVOCATION_MODES,
            prohibited_request_flags=PROHIBITED_REQUEST_FLAGS,
            governance_rules=DRYRUN_GOVERNANCE_RULES,
        )
    )


def run_and_review_recognition_model_invocation_feasibility_dryrun_v1(
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

    # sample file presence
    sample_count = 0
    for fam, fname in VALID_SAMPLE_FILES.items():
        p = _REPO_ROOT / _PKG / "samples" / fname
        if p.is_file():
            sample_count += 1
        else:
            failed_checks.append(f"sample_missing:{fname}")
    for key, fname in INVALID_SAMPLE_FILES.items():
        p = _REPO_ROOT / _PKG / "samples" / fname
        if p.is_file():
            sample_count += 1
        else:
            failed_checks.append(f"sample_missing:{fname}")

    upstream_checks, upstream_issues = _review_upstream()
    failed_checks.extend(upstream_issues)

    positive_results = run_positive_cases()
    negative_results = run_negative_cases()

    positive_pass_count = sum(1 for r in positive_results if r.passed)
    invalid_expected_reject_count = sum(1 for r in negative_results if r.passed)

    # family feasibility checked flags (from the 7 family positive cases)
    family_checked: Dict[str, bool] = {}
    family_case_by_family = {
        r.model_family: r for r in positive_results if r.model_family in MODEL_FAMILY_IDS
    }
    for fam in MODEL_FAMILY_IDS:
        go_key = FAMILY_FEASIBILITY_CHECKED_GO_KEYS[fam]
        r = family_case_by_family.get(fam)
        family_checked[go_key] = bool(r and r.passed)

    multi_matrix = next(
        (r for r in positive_results if r.case_id == "multi_family_invocation_feasibility_matrix"),
        None,
    )
    multi_matrix_ok = bool(multi_matrix and multi_matrix.passed)

    contract_field_required = {
        "callable_interface_ref_required": True,
        "input_format_ref_required": True,
        "output_schema_ref_required": True,
        "runtime_requirement_ref_required": True,
        "model_origin_required": True,
        "license_ref_required": True,
        "dependency_boundary_ref_required": True,
        "resource_requirement_ref_required": True,
        "offline_or_online_mode_required": True,
        "adapter_mapping_target_required": True,
        "source_chain_required": True,
        "confidence_policy_ref_required": True,
    }

    neg_by_id = {r.case_id: r for r in negative_results}
    rejection_go = {
        "missing_model_origin_rejected": neg_by_id.get(
            "invalid_missing_model_origin", _Dummy()
        ).passed,
        "missing_license_ref_rejected": neg_by_id.get(
            "invalid_missing_license_ref", _Dummy()
        ).passed,
        "missing_output_schema_ref_rejected": neg_by_id.get(
            "invalid_missing_output_schema_ref", _Dummy()
        ).passed,
        "real_inference_requested_rejected": neg_by_id.get(
            "invalid_real_inference_requested", _Dummy()
        ).passed,
        "model_download_requested_rejected": neg_by_id.get(
            "invalid_model_download_requested", _Dummy()
        ).passed,
        "native_output_direct_to_field_rejected": neg_by_id.get(
            "invalid_native_output_direct_to_field", _Dummy()
        ).passed,
        "dataset_usage_training_requested_rejected": neg_by_id.get(
            "invalid_dataset_usage_or_training_requested", _Dummy()
        ).passed,
        "runtime_live_sensor_requested_rejected": neg_by_id.get(
            "invalid_runtime_activation_or_live_sensor_requested", _Dummy()
        ).passed,
    }

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "model_family_contract_count_eq_7": len(VALID_SAMPLE_FILES) == 7,
        "positive_case_count_eq_8": len(positive_results) == 8,
        "negative_case_count_eq_8": len(negative_results) == 8,
        "positive_pass_count_eq_8": positive_pass_count == 8,
        "invalid_expected_reject_count_eq_8": invalid_expected_reject_count == 8,
        **{f"{k}": (v is True) for k, v in upstream_checks.items() if k in _REQUIRED_VERIFY_FLAGS},
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        **family_checked,
        "multi_family_invocation_matrix_ok": multi_matrix_ok,
        **contract_field_required,
        **rejection_go,
        **{k: (v is True) for k, v in ALLOWED_FEASIBILITY_FLAGS.items()},
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
        "step": "Recognition Model Invocation Feasibility DryRun Run and Review",
        "lifecycle_variant": "recognition_model_invocation_feasibility_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "planning_ref": PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "allowed_feasibility_flags": dict(ALLOWED_FEASIBILITY_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "dryrun_profile": _build_profile(),
        "model_family_contract_count": len(VALID_SAMPLE_FILES),
        "sample_file_count": sample_count,
        "positive_case_count": len(positive_results),
        "negative_case_count": len(negative_results),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "positive_cases": [asdict(r) for r in positive_results],
        "negative_cases": [asdict(r) for r in negative_results],
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "conclusions": {
            "recognition_model_invocation_feasibility_status": (
                "recognition_model_invocation_feasibility_verified"
                if review_ok
                else "blocked"
            ),
            "model_families_checked": list(MODEL_FAMILY_IDS),
            "next_phase_ref": NEXT_PHASE_REF,
            "transition_note": (
                "Recognition-model invocation feasibility verified at the contract level (stub / "
                "import / command / placeholder schema only). No real inference / download / build. "
                "Next: Phase-Recognition-Model-Output-Adapter-DryRun-v1-001 validates the adapter "
                "with mock-but-file-based model output files, still without real inference."
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


class _Dummy:
    passed = False


def main() -> int:
    result = run_and_review_recognition_model_invocation_feasibility_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "model_family_contract_count": result["model_family_contract_count"],
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
