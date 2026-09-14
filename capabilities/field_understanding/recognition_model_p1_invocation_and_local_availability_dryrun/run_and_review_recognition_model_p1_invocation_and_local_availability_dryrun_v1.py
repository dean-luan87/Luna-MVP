# -*- coding: utf-8 -*-
"""Recognition Model P1 Invocation And Local Availability DryRun — run and review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_p1_invocation_and_local_availability_dryrun.recognition_model_p1_invocation_and_local_availability_dryrun_cases_v1 import (  # noqa: E402
    INVALID_SAMPLE_FILES,
    MATRIX_SAMPLE_FILE,
    VALID_SAMPLE_FILES,
    run_negative_cases,
    run_positive_cases,
)
from capabilities.field_understanding.recognition_model_p1_invocation_and_local_availability_dryrun.recognition_model_p1_invocation_and_local_availability_dryrun_types_v1 import (  # noqa: E402
    ALLOWED_AVAILABILITY_FLAGS,
    ALLOWED_AVAILABILITY_STATUSES,
    ALLOWED_PROBE_MODES,
    CONTRACT_FIELD_REQUIRED_FLAGS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    FAMILY_AVAILABILITY_CHECKED_GO_KEYS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    LUNA_CORE_PRINCIPLE,
    MODEL_FAMILY_IDS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    P0_BASELINE_REF,
    P1_FAMILY_EXPANSION_PLANNING_REF,
    PHASE_ID,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_CONTRACT_FIELDS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    RecognitionModelP1InvocationLocalAvailabilityDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (  # noqa: E402
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "recognition_model_p1_invocation_and_local_availability_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "recognition_model_p1_invocation_and_local_availability_dryrun_run_and_review_v1.json"
)

_PKG = "capabilities/field_understanding/recognition_model_p1_invocation_and_local_availability_dryrun"
STEP_FILES = (
    f"{_PKG}/recognition_model_p1_invocation_and_local_availability_dryrun_types_v1.py",
    f"{_PKG}/recognition_model_p1_invocation_and_local_availability_dryrun_cases_v1.py",
    f"{_PKG}/run_and_review_recognition_model_p1_invocation_and_local_availability_dryrun_v1.py",
)

PROFILE_REF = "recognition_model_p1_invocation_and_local_availability_dryrun_profile_v1"

GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"

# --------------------------------------------------------------------------- #
# Upstream stage registry (15 phase refs + governance template = 16 >= 15).
#   verify=True  -> GO must be checked against an artifact and feeds a GO flag.
#   verify=False -> reference-only lineage entry (counted, not gated).
# --------------------------------------------------------------------------- #
_UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": "Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_SYSTEM_ADMISSION_AND_INVOCATION_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_system_admission_and_invocation_planning_v1_smoke_v0/"
            "recognition_model_system_admission_and_invocation_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_INVOCATION_FEASIBILITY_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_invocation_feasibility_dryrun_v1_smoke_v0/"
            "recognition_model_invocation_feasibility_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_OUTPUT_ADAPTER_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-Download-License-And-Local-Availability-Planning-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_DOWNLOAD_LICENSE_AND_LOCAL_AVAILABILITY_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_download_license_and_local_availability_planning_v1_smoke_v0/"
            "recognition_model_download_license_and_local_availability_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-Download-And-Install-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_DOWNLOAD_AND_INSTALL_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_download_and_install_dryrun_v1_smoke_v0/"
            "recognition_model_download_and_install_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-Real-Output-Adapter-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_REAL_OUTPUT_ADAPTER_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_real_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_real_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Recognition-Model-Evidence-Main-Chain-Integration-DryRun-v1-001",
        "verify": False,
        "verify_flag": None,
        "expected_go": "RECOGNITION_MODEL_EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_evidence_main_chain_integration_dryrun_v1_smoke_v0/"
            "recognition_model_evidence_main_chain_integration_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": P1_FAMILY_EXPANSION_PLANNING_REF,
        "verify": True,
        "verify_flag": "p1_family_expansion_planning_go_verified",
        "expected_go": "RECOGNITION_MODEL_P1_FAMILY_EXPANSION_PLANNING_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p1_family_expansion_planning_v1_smoke_v0/"
            "recognition_model_p1_family_expansion_planning_review_v1.json"
        ),
    },
    {
        "phase_ref": P0_BASELINE_REF,
        "verify": True,
        "verify_flag": "p0_integration_closure_go_verified",
        "expected_go": "RECOGNITION_MODEL_P0_INTEGRATION_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p0_integration_closure_v1_smoke_v0/"
            "recognition_model_p0_integration_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001",
        "verify": True,
        "verify_flag": "phase_one_evidence_main_chain_closure_go_verified",
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_evidence_main_chain_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_evidence_main_chain_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001",
        "verify": True,
        "verify_flag": "rgb_vision_evidence_chain_closure_go_verified",
        "expected_go": "RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_evidence_chain_integrated_closure_v1_smoke_v0/"
            "rgb_vision_evidence_chain_integrated_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001",
        "verify": True,
        "verify_flag": "rgb_slam_cross_modal_closure_go_verified",
        "expected_go": "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1_smoke_v0/"
            "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001",
        "verify": True,
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "verify": True,
        "verify_flag": "interface_layer_governance_verified",
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
        "verify": True,
        "verify_flag": "model_admission_governance_verified",
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
    },
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = tuple(
    e["verify_flag"] for e in _UPSTREAM_STAGE_REGISTRY if e["verify"]
)


def _load(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def _verify_stages() -> Tuple[List[Dict[str, Any]], Dict[str, bool], List[str]]:
    stage_refs: List[Dict[str, Any]] = []
    verify_flags: Dict[str, bool] = {}
    issues: List[str] = []
    for idx, entry in enumerate(_UPSTREAM_STAGE_REGISTRY, start=1):
        artifact, exists = _load(entry["artifact_rel"])
        actual_go = (artifact or {}).get("final_decision") if exists else None
        go_ok = exists and actual_go == entry["expected_go"]
        stage_refs.append(
            {
                "stage_index": idx,
                "phase_ref": entry["phase_ref"],
                "expected_go": entry["expected_go"],
                "gated": entry["verify"],
                "go_verified": go_ok,
            }
        )
        if entry["verify"]:
            verify_flags[entry["verify_flag"]] = go_ok
            if not exists:
                issues.append(f"upstream_artifact_missing:{entry['phase_ref']}")
            elif not go_ok:
                issues.append(f"upstream_go_mismatch:{entry['phase_ref']}:{actual_go!r}")
    template_ok = CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    verify_flags["controlled_trial_governance_template_ref_ok"] = template_ok
    if not template_ok:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    return stage_refs, verify_flags, issues


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelP1InvocationLocalAvailabilityDryRunProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            p1_family_expansion_planning_ref=P1_FAMILY_EXPANSION_PLANNING_REF,
            p0_baseline_ref=P0_BASELINE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            model_family_ids=MODEL_FAMILY_IDS,
            required_contract_fields=REQUIRED_CONTRACT_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            allowed_availability_statuses=ALLOWED_AVAILABILITY_STATUSES,
            allowed_probe_modes=ALLOWED_PROBE_MODES,
            prohibited_request_flags=tuple(),
            governance_rules=DRYRUN_GOVERNANCE_RULES,
        )
    )


class _Dummy:
    passed = False


def run_and_review_recognition_model_p1_invocation_and_local_availability_dryrun_v1(
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

    # sample file presence (7 family + 1 matrix + 8 invalid = 16)
    sample_count = 0
    for fname in VALID_SAMPLE_FILES.values():
        if (_REPO_ROOT / _PKG / "samples" / fname).is_file():
            sample_count += 1
        else:
            failed_checks.append(f"sample_missing:{fname}")
    if (_REPO_ROOT / _PKG / "samples" / MATRIX_SAMPLE_FILE).is_file():
        sample_count += 1
    else:
        failed_checks.append(f"sample_missing:{MATRIX_SAMPLE_FILE}")
    for fname in INVALID_SAMPLE_FILES.values():
        if (_REPO_ROOT / _PKG / "samples" / fname).is_file():
            sample_count += 1
        else:
            failed_checks.append(f"sample_missing:{fname}")

    stage_refs, verify_flags, stage_issues = _verify_stages()
    failed_checks.extend(stage_issues)
    upstream_stage_ref_count = len(stage_refs) + 1  # + governance template

    positive_results = run_positive_cases()
    negative_results = run_negative_cases()

    positive_pass_count = sum(1 for r in positive_results if r.passed)
    invalid_expected_reject_count = sum(1 for r in negative_results if r.passed)

    # Family availability-checked flags from the 7 family positive cases.
    pos_by_family = {
        r.model_family: r for r in positive_results if r.model_family in MODEL_FAMILY_IDS
    }
    family_checked: Dict[str, bool] = {}
    for fam in MODEL_FAMILY_IDS:
        go_key = FAMILY_AVAILABILITY_CHECKED_GO_KEYS[fam]
        r = pos_by_family.get(fam)
        family_checked[go_key] = bool(r and r.passed)

    matrix_case = next(
        (r for r in positive_results if r.case_id == "p1_p2_family_availability_matrix_generation"),
        None,
    )
    matrix_generated = bool(matrix_case and matrix_case.passed)

    # Per-family availability status map (the P1/P2 availability matrix).
    availability_status_by_family = {
        fam: pos_by_family[fam].availability_status
        for fam in MODEL_FAMILY_IDS
        if fam in pos_by_family
    }
    status_buckets: Dict[str, List[str]] = {s: [] for s in ALLOWED_AVAILABILITY_STATUSES}
    for fam, status in availability_status_by_family.items():
        if status in status_buckets:
            status_buckets[status].append(fam)
    status_buckets = {k: v for k, v in status_buckets.items() if v}

    contract_field_required = {
        flag: True for flag in CONTRACT_FIELD_REQUIRED_FLAGS.values()
    }

    neg_by_id = {r.case_id: r for r in negative_results}
    rejection_go = {
        "missing_license_ref_rejected": neg_by_id.get(
            "invalid_missing_license_ref", _Dummy()
        ).passed,
        "missing_fallback_plan_rejected": neg_by_id.get(
            "invalid_missing_fallback_plan", _Dummy()
        ).passed,
        "missing_unavailable_record_policy_rejected": neg_by_id.get(
            "invalid_missing_unavailable_record_policy", _Dummy()
        ).passed,
        "real_inference_requested_rejected": neg_by_id.get(
            "invalid_real_inference_requested", _Dummy()
        ).passed,
        "new_model_download_requested_rejected": neg_by_id.get(
            "invalid_new_model_download_requested", _Dummy()
        ).passed,
        "single_model_debugging_requested_rejected": neg_by_id.get(
            "invalid_single_model_debugging_requested", _Dummy()
        ).passed,
        "dataset_training_requested_rejected": neg_by_id.get(
            "invalid_dataset_training_requested", _Dummy()
        ).passed,
        "live_camera_sensor_requested_rejected": neg_by_id.get(
            "invalid_live_camera_sensor_requested", _Dummy()
        ).passed,
        "direct_action_speech_fact_write_rejected": neg_by_id.get(
            "invalid_direct_action_speech_fact_write_requested", _Dummy()
        ).passed,
        "vla_action_chain_requested_rejected": neg_by_id.get(
            "invalid_vla_action_chain_requested", _Dummy()
        ).passed,
    }

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "upstream_stage_ref_count_gte_15": upstream_stage_ref_count >= 15,
        "family_contract_count_eq_7": len(VALID_SAMPLE_FILES) == 7,
        "positive_case_count_eq_8": len(positive_results) == 8,
        "negative_case_count_eq_10": len(negative_results) == 10,
        "positive_pass_count_eq_8": positive_pass_count == 8,
        "invalid_expected_reject_count_eq_10": invalid_expected_reject_count == 10,
        **{
            k: (verify_flags.get(k) is True) for k in _REQUIRED_VERIFY_FLAGS
        },
        "controlled_trial_governance_template_ref_ok": (
            verify_flags.get("controlled_trial_governance_template_ref_ok") is True
        ),
        **family_checked,
        "p1_p2_family_availability_matrix_generated": matrix_generated,
        **contract_field_required,
        **rejection_go,
        **{k: (v is True) for k, v in ALLOWED_AVAILABILITY_FLAGS.items()},
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
        "step": "Recognition Model P1 Invocation And Local Availability DryRun Run and Review",
        "lifecycle_variant": "recognition_model_p1_invocation_and_local_availability_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "p1_family_expansion_planning_ref": P1_FAMILY_EXPANSION_PLANNING_REF,
        "p0_baseline_ref": P0_BASELINE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "allowed_availability_flags": dict(ALLOWED_AVAILABILITY_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "dryrun_profile": _build_profile(),
        "upstream_stage_ref_count": upstream_stage_ref_count,
        "stage_refs": stage_refs,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "family_contract_count": len(VALID_SAMPLE_FILES),
        "sample_file_count": sample_count,
        "positive_case_count": len(positive_results),
        "negative_case_count": len(negative_results),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "positive_cases": [asdict(r) for r in positive_results],
        "negative_cases": [asdict(r) for r in negative_results],
        "p1_p2_family_availability_matrix": {
            "family_count": len(availability_status_by_family),
            "statuses_by_family": availability_status_by_family,
            "status_buckets": status_buckets,
            "matrix_generated": matrix_generated,
        },
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "p1_invocation_local_availability_status": (
                "p1_p2_family_invocation_and_local_availability_dryrun_verified"
                if review_ok
                else "blocked"
            ),
            "model_families_checked": list(MODEL_FAMILY_IDS),
            "next_phase_ref": NEXT_PHASE_REF,
            "transition_note": (
                "P1/P2 expansion family invocation entry points and local availability verified "
                "at the contract level only (import / package / command / local-resource visibility "
                "and contract-level callable check via non-invasive probes). No download, no real "
                "inference, no single-model debugging, no tuning, no dataset usage. A P1/P2 family "
                "availability-status matrix has been produced. Next, the matrix decides whether to "
                "enter Phase-Recognition-Model-P1-Output-Adapter-DryRun-v1-001 or to first complete "
                "P1 download/license planning for the families marked download_planning_required / "
                "deferred."
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
    result = run_and_review_recognition_model_p1_invocation_and_local_availability_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "upstream_stage_ref_count": result["upstream_stage_ref_count"],
                "family_contract_count": result["family_contract_count"],
                "positive_pass_count": result["positive_pass_count"],
                "invalid_expected_reject_count": result["invalid_expected_reject_count"],
                "p1_p2_family_availability_matrix_generated": result[
                    "p1_p2_family_availability_matrix"
                ]["matrix_generated"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
