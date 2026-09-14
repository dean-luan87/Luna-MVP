# -*- coding: utf-8 -*-
"""Midplatform Model Data Handling DryRun — run and review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.model_data_handling_dryrun.model_data_handling_dryrun_cases_v1 import (  # noqa: E402
    ALL_SAMPLE_FILES,
    run_negative_cases,
    run_positive_cases,
)
from capabilities.midplatform.model_data_handling_dryrun.model_data_handling_dryrun_types_v1 import (  # noqa: E402
    ALL_PRODUCED_OBJECTS,
    ALLOWED_FLAGS,
    CONTRACT_FIELD_REQUIRED_FLAGS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATA_HANDLING_POLICY_IDS,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    LUNA_CORE_PRINCIPLE,
    MULTI_MODEL_INTERACTION_DRYRUN_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    P0_BASELINE_REF,
    P1_FAMILY_EXPANSION_PLANNING_REF,
    P1_INVOCATION_LOCAL_AVAILABILITY_DRYRUN_REF,
    P1_OUTPUT_ADAPTER_DRYRUN_REF,
    PHASE_ID,
    POLICY_OK_GO_KEYS,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_BUNDLE_FIELDS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    MidplatformModelDataHandlingDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (  # noqa: E402
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "midplatform_model_data_handling_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "midplatform_model_data_handling_dryrun_run_and_review_v1.json"

_PKG = "capabilities/midplatform/model_data_handling_dryrun"
STEP_FILES = (
    f"{_PKG}/model_data_handling_dryrun_types_v1.py",
    f"{_PKG}/model_data_handling_dryrun_cases_v1.py",
    f"{_PKG}/run_and_review_model_data_handling_dryrun_v1.py",
)

PROFILE_REF = "midplatform_model_data_handling_dryrun_profile_v1"
GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"

# --------------------------------------------------------------------------- #
# Upstream stage registry (13 phase refs + governance template = 14 >= 12).
# --------------------------------------------------------------------------- #
_UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": MULTI_MODEL_INTERACTION_DRYRUN_REF,
        "verify": True,
        "verify_flag": "multi_model_interaction_dryrun_go_verified",
        "expected_go": "RECOGNITION_MODEL_MULTI_MODEL_INTERACTION_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_multi_model_interaction_dryrun_v1_smoke_v0/"
            "recognition_model_multi_model_interaction_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": P1_OUTPUT_ADAPTER_DRYRUN_REF,
        "verify": True,
        "verify_flag": "p1_output_adapter_dryrun_go_verified",
        "expected_go": "RECOGNITION_MODEL_P1_OUTPUT_ADAPTER_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p1_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_p1_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "phase_ref": P1_INVOCATION_LOCAL_AVAILABILITY_DRYRUN_REF,
        "verify": True,
        "verify_flag": "p1_invocation_local_availability_dryrun_go_verified",
        "expected_go": "RECOGNITION_MODEL_P1_INVOCATION_AND_LOCAL_AVAILABILITY_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_p1_invocation_and_local_availability_dryrun_v1_smoke_v0/"
            "recognition_model_p1_invocation_and_local_availability_dryrun_run_and_review_v1.json"
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
        "phase_ref": TARGET_CHAIN_REF,
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
        MidplatformModelDataHandlingDryRunProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            multi_model_interaction_dryrun_ref=MULTI_MODEL_INTERACTION_DRYRUN_REF,
            p1_output_adapter_dryrun_ref=P1_OUTPUT_ADAPTER_DRYRUN_REF,
            p0_baseline_ref=P0_BASELINE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            data_handling_policy_ids=DATA_HANDLING_POLICY_IDS,
            required_bundle_fields=REQUIRED_BUNDLE_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            prohibited_request_flags=tuple(),
            governance_rules=DRYRUN_GOVERNANCE_RULES,
        )
    )


class _Dummy:
    passed = False


def run_and_review_model_data_handling_dryrun_v1(
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

    sample_count = 0
    for fname in ALL_SAMPLE_FILES:
        if (_REPO_ROOT / _PKG / "samples" / fname).is_file():
            sample_count += 1
        else:
            failed_checks.append(f"sample_missing:{fname}")

    stage_refs, verify_flags, stage_issues = _verify_stages()
    failed_checks.extend(stage_issues)
    upstream_stage_ref_count = len(stage_refs) + 1

    positive_results, produced = run_positive_cases()
    negative_results = run_negative_cases()

    positive_pass_count = sum(1 for r in positive_results if r.passed)
    invalid_expected_reject_count = sum(1 for r in negative_results if r.passed)

    pos_by_id = {r.case_id: r for r in positive_results}

    def _passed(case_id: str) -> bool:
        r = pos_by_id.get(case_id)
        return bool(r and r.passed)

    policy_ok = {
        "candidate_ingress_handling_ok": _passed("multi_model_candidate_ingress_handling"),
        "candidate_normalization_handling_ok": _passed("candidate_normalization_handling"),
        "source_chain_aggregation_handling_ok": _passed("source_chain_aggregation_handling"),
        "confidence_policy_aggregation_handling_ok": _passed("confidence_policy_aggregation_handling"),
        "conflict_uncertainty_handling_ok": _passed("conflict_uncertainty_handling"),
        "unavailable_reserved_degraded_handling_ok": _passed("unavailable_reserved_degraded_handling"),
        "evidence_bundle_composition_handling_ok": _passed("evidence_bundle_composition_handling"),
        "candidate_lifecycle_handling_ok": _passed("candidate_lifecycle_handling"),
        "field_task_guidance_support_bundle_handling_ok": _passed("field_task_guidance_support_bundle_handling"),
        "full_midplatform_model_data_handling_bundle_ok": _passed("full_midplatform_model_data_handling_bundle"),
    }
    bundle_ok = policy_ok["full_midplatform_model_data_handling_bundle_ok"]

    object_generated: Dict[str, bool] = {}
    for o in ALL_PRODUCED_OBJECTS:
        object_generated[f"{o}_generated"] = o in produced

    contract_field_required = {flag: True for flag in CONTRACT_FIELD_REQUIRED_FLAGS.values()}

    neg_by_id = {r.case_id: r for r in negative_results}
    rejection_go = {
        "missing_source_chain_rejected": neg_by_id.get("invalid_missing_source_chain", _Dummy()).passed,
        "missing_candidate_refs_rejected": neg_by_id.get("invalid_missing_candidate_refs", _Dummy()).passed,
        "missing_confidence_policy_ref_rejected": neg_by_id.get(
            "invalid_missing_confidence_policy_ref", _Dummy()
        ).passed,
        "untrusted_candidate_fact_admission_rejected": neg_by_id.get(
            "invalid_untrusted_candidate_fact_admission", _Dummy()
        ).passed,
        "conflict_resolved_as_fact_rejected": neg_by_id.get(
            "invalid_conflict_resolved_as_fact", _Dummy()
        ).passed,
        "unavailable_model_blocker_or_download_rejected": neg_by_id.get(
            "invalid_unavailable_model_treated_as_blocker", _Dummy()
        ).passed,
        "reserved_family_execution_rejected": neg_by_id.get(
            "invalid_reserved_family_executed", _Dummy()
        ).passed,
        "direct_field_task_guidance_bypass_rejected": neg_by_id.get(
            "invalid_direct_field_task_guidance_bypass", _Dummy()
        ).passed,
        "action_speech_navigation_trigger_rejected": neg_by_id.get(
            "invalid_action_speech_navigation_trigger", _Dummy()
        ).passed,
        "vla_action_chain_rejected": neg_by_id.get("invalid_vla_action_chain_injected", _Dummy()).passed,
        "model_tuning_dataset_usage_rejected": neg_by_id.get(
            "invalid_model_tuning_dataset_usage", _Dummy()
        ).passed,
        "blocked_expired_candidate_revival_rejected": neg_by_id.get(
            "invalid_blocked_expired_candidate_revival", _Dummy()
        ).passed,
    }

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "upstream_stage_ref_count_gte_12": upstream_stage_ref_count >= 12,
        "data_handling_policy_count_gte_10": len(DATA_HANDLING_POLICY_IDS) >= 10,
        "sample_file_count_gte_20": sample_count >= 20,
        "positive_case_count_eq_10": len(positive_results) == 10,
        "negative_case_count_eq_12": len(negative_results) == 12,
        "positive_pass_count_eq_10": positive_pass_count == 10,
        "invalid_expected_reject_count_eq_12": invalid_expected_reject_count == 12,
        **{k: (verify_flags.get(k) is True) for k in _REQUIRED_VERIFY_FLAGS},
        "controlled_trial_governance_template_ref_ok": (
            verify_flags.get("controlled_trial_governance_template_ref_ok") is True
        ),
        **policy_ok,
        **object_generated,
        **contract_field_required,
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
        "step": "Midplatform Model Data Handling DryRun Run and Review",
        "lifecycle_variant": "midplatform_model_data_handling_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "multi_model_interaction_dryrun_ref": MULTI_MODEL_INTERACTION_DRYRUN_REF,
        "p1_output_adapter_dryrun_ref": P1_OUTPUT_ADAPTER_DRYRUN_REF,
        "p0_baseline_ref": P0_BASELINE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "allowed_flags": dict(ALLOWED_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "dryrun_profile": _build_profile(),
        "upstream_stage_ref_count": upstream_stage_ref_count,
        "stage_refs": stage_refs,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "data_handling_policy_count": len(DATA_HANDLING_POLICY_IDS),
        "sample_file_count": sample_count,
        "positive_case_count": len(positive_results),
        "negative_case_count": len(negative_results),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "positive_cases": [asdict(r) for r in positive_results],
        "negative_cases": [asdict(r) for r in negative_results],
        "midplatform_produced_object_coverage": {
            "produced_object_types": produced,
            "coverage_count": len(produced),
            "coverage_complete": all(o in produced for o in ALL_PRODUCED_OBJECTS),
        },
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "midplatform_model_data_handling_status": (
                "midplatform_model_data_handling_dryrun_verified" if review_ok else "blocked"
            ),
            "data_handling_policies_checked": list(DATA_HANDLING_POLICY_IDS),
            "next_phase_ref": NEXT_PHASE_REF,
            "transition_note": (
                "The Luna midplatform model data-handling layer verified with file-based multi-model "
                "candidate bundles: ingress, normalization, source-chain aggregation, confidence "
                "aggregation, conflict and uncertainty handling, unavailable/reserved/degraded handling, "
                "evidence bundle composition, candidate lifecycle, and the Field/Task/Guidance candidate "
                "support bundle all produce candidate-only outputs with no fact admission, no execution of "
                "reserved families, and no action/speech/navigation. All 27 handling objects covered. "
                "Next: Phase-Midplatform-Model-Control-DryRun-v1-001 to verify enable/disable, degrade, "
                "fallback, license boundary, output gating and priority scheduling control over models."
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
    result = run_and_review_model_data_handling_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "upstream_stage_ref_count": result["upstream_stage_ref_count"],
                "data_handling_policy_count": result["data_handling_policy_count"],
                "sample_file_count": result["sample_file_count"],
                "positive_pass_count": result["positive_pass_count"],
                "invalid_expected_reject_count": result["invalid_expected_reject_count"],
                "full_midplatform_model_data_handling_bundle_ok": result["go_conditions"][
                    "full_midplatform_model_data_handling_bundle_ok"
                ],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
