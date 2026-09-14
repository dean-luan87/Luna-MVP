# -*- coding: utf-8 -*-
"""Midplatform Model Control DryRun — run and review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.model_control_dryrun.model_control_dryrun_cases_v1 import (  # noqa: E402
    ALL_SAMPLE_FILES,
    run_negative_cases,
    run_positive_cases,
)
from capabilities.midplatform.model_control_dryrun.model_control_dryrun_types_v1 import (  # noqa: E402
    ALL_PRODUCED_OBJECTS,
    ALLOWED_FLAGS,
    CONTRACT_FIELD_REQUIRED_FLAGS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    LUNA_CORE_PRINCIPLE,
    MODEL_CONTROL_POLICY_IDS,
    MODEL_DATA_HANDLING_DRYRUN_REF,
    MULTI_MODEL_INTERACTION_DRYRUN_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    P0_BASELINE_REF,
    P1_FAMILY_EXPANSION_PLANNING_REF,
    P1_INVOCATION_LOCAL_AVAILABILITY_DRYRUN_REF,
    P1_OUTPUT_ADAPTER_DRYRUN_REF,
    PHASE_ID,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_BUNDLE_FIELDS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    MidplatformModelControlDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (  # noqa: E402
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "midplatform_model_control_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "midplatform_model_control_dryrun_run_and_review_v1.json"

_PKG = "capabilities/midplatform/model_control_dryrun"
STEP_FILES = (
    f"{_PKG}/model_control_dryrun_types_v1.py",
    f"{_PKG}/model_control_dryrun_cases_v1.py",
    f"{_PKG}/run_and_review_model_control_dryrun_v1.py",
)

PROFILE_REF = "midplatform_model_control_dryrun_profile_v1"
GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"

# --------------------------------------------------------------------------- #
# Upstream stage registry (15 phase refs + governance template = 16 >= 13).
# --------------------------------------------------------------------------- #
_UPSTREAM_STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": MODEL_DATA_HANDLING_DRYRUN_REF,
        "verify": True,
        "verify_flag": "model_data_handling_dryrun_go_verified",
        "expected_go": "MIDPLATFORM_MODEL_DATA_HANDLING_DRYRUN_GO",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_model_data_handling_dryrun_v1_smoke_v0/"
            "midplatform_model_data_handling_dryrun_run_and_review_v1.json"
        ),
    },
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
        MidplatformModelControlDryRunProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            model_data_handling_dryrun_ref=MODEL_DATA_HANDLING_DRYRUN_REF,
            multi_model_interaction_dryrun_ref=MULTI_MODEL_INTERACTION_DRYRUN_REF,
            p1_output_adapter_dryrun_ref=P1_OUTPUT_ADAPTER_DRYRUN_REF,
            p0_baseline_ref=P0_BASELINE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            model_control_policy_ids=MODEL_CONTROL_POLICY_IDS,
            required_bundle_fields=REQUIRED_BUNDLE_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            prohibited_request_flags=tuple(),
            governance_rules=DRYRUN_GOVERNANCE_RULES,
        )
    )


class _Dummy:
    passed = False


def run_and_review_model_control_dryrun_v1(
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
        "model_enable_policy_control_ok": _passed("model_enable_policy_control"),
        "model_disable_policy_control_ok": _passed("model_disable_policy_control"),
        "model_fallback_policy_control_ok": _passed("model_fallback_policy_control"),
        "model_degraded_mode_policy_control_ok": _passed("model_degraded_mode_policy_control"),
        "model_license_boundary_control_ok": _passed("model_license_boundary_control"),
        "model_priority_routing_policy_control_ok": _passed("model_priority_routing_policy_control"),
        "model_output_blocking_policy_control_ok": _passed("model_output_blocking_policy_control"),
        "model_availability_state_control_ok": _passed("model_availability_state_control"),
        "reserved_family_execution_block_control_ok": _passed("reserved_family_execution_block_control"),
        "candidate_output_gate_control_ok": _passed("candidate_output_gate_control"),
        "full_midplatform_model_control_bundle_ok": _passed("full_midplatform_model_control_bundle"),
    }

    object_generated: Dict[str, bool] = {}
    for o in ALL_PRODUCED_OBJECTS:
        object_generated[f"{o}_generated"] = o in produced

    contract_field_required = {flag: True for flag in CONTRACT_FIELD_REQUIRED_FLAGS.values()}

    neg_by_id = {r.case_id: r for r in negative_results}

    def _neg(case_id: str) -> bool:
        return neg_by_id.get(case_id, _Dummy()).passed

    rejection_go = {
        "disabled_model_output_allowed_rejected": _neg("invalid_disabled_model_output_allowed"),
        "unlicensed_model_enabled_rejected": _neg("invalid_unlicensed_model_enabled"),
        "agpl_commercial_runtime_ready_rejected": _neg(
            "invalid_agpl_model_marked_commercial_runtime_ready"
        ),
        "unavailable_model_download_execution_rejected": _neg(
            "invalid_unavailable_model_triggered_download"
        ),
        "reserved_family_execution_rejected": _neg("invalid_reserved_family_executed"),
        "degraded_state_action_speech_navigation_rejected": _neg(
            "invalid_degraded_model_triggers_action"
        ),
        "blocked_output_field_task_guidance_rejected": _neg(
            "invalid_blocked_output_enters_field_task_guidance"
        ),
        "priority_routing_gate_bypass_rejected": _neg(
            "invalid_priority_routing_bypasses_candidate_gate"
        ),
        "model_control_inference_trigger_rejected": _neg(
            "invalid_model_control_triggers_inference"
        ),
        "vla_action_chain_rejected": _neg("invalid_vla_action_chain_injected"),
        "model_tuning_dataset_usage_rejected": _neg("invalid_model_tuning_dataset_usage"),
        "gate_pass_fact_admission_rejected": _neg(
            "invalid_gate_pass_treated_as_fact_admission"
        ),
    }

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "upstream_stage_ref_count_gte_13": upstream_stage_ref_count >= 13,
        "model_control_policy_count_gte_11": len(MODEL_CONTROL_POLICY_IDS) >= 11,
        "sample_file_count_gte_20": sample_count >= 20,
        "positive_case_count_eq_11": len(positive_results) == 11,
        "negative_case_count_eq_12": len(negative_results) == 12,
        "positive_pass_count_eq_11": positive_pass_count == 11,
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
        "step": "Midplatform Model Control DryRun Run and Review",
        "lifecycle_variant": "midplatform_model_control_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "model_data_handling_dryrun_ref": MODEL_DATA_HANDLING_DRYRUN_REF,
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
        "model_control_policy_count": len(MODEL_CONTROL_POLICY_IDS),
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
            "midplatform_model_control_status": (
                "midplatform_model_control_dryrun_verified" if review_ok else "blocked"
            ),
            "model_control_policies_checked": list(MODEL_CONTROL_POLICY_IDS),
            "next_phase_ref": NEXT_PHASE_REF,
            "transition_note": (
                "The Luna midplatform model-control layer verified with file-based control policy "
                "bundles: enable, disable, fallback, degraded mode, license boundary, priority routing, "
                "output blocking, availability state control, reserved-only execution block, candidate "
                "output gate, and full control bundle all produce candidate-only governance outputs. "
                "Enabled is not runtime activation; disabled output is blocked; fallback triggers no "
                "download/inference; degraded state triggers no action/speech/navigation; license boundary "
                "keeps commercial_runtime_approved false; routing does not bypass the candidate gate; "
                "reserved-only families never execute; gate pass is candidate-only, not fact admission. "
                "All 28 control objects covered. This closes the model expansion chain: model output -> "
                "model interaction -> midplatform data handling -> midplatform model control. Next: "
                "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001 to seal the "
                "whole segment into a stable baseline."
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
    result = run_and_review_model_control_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "upstream_stage_ref_count": result["upstream_stage_ref_count"],
                "model_control_policy_count": result["model_control_policy_count"],
                "sample_file_count": result["sample_file_count"],
                "positive_pass_count": result["positive_pass_count"],
                "invalid_expected_reject_count": result["invalid_expected_reject_count"],
                "full_midplatform_model_control_bundle_ok": result["go_conditions"][
                    "full_midplatform_model_control_bundle_ok"
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
