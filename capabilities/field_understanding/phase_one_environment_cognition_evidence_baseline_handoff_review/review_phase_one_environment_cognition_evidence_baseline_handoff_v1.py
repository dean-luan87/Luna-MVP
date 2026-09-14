# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Evidence Baseline Handoff Review — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_evidence_baseline_handoff_review.phase_one_environment_cognition_evidence_baseline_handoff_review_types_v1 import (
    BASELINE_FINAL_DECISION,
    BASELINE_REF,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEFERRED_EXPANSION_IDS,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GOVERNANCE_CLOSURE_REF,
    HANDOFF_GOVERNANCE_RULES,
    HANDOFF_PRINCIPLE_ZH,
    HANDOFF_READINESS_FLAGS,
    HANDOFF_TARGET_REFS,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MAIN_CHAIN_CLOSURE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
    RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
    SOURCE_CHAIN,
    PhaseOneEvidenceBaselineDeferredExpansionSummary,
    PhaseOneEvidenceBaselineHandoffReviewProfile,
    PhaseOneEvidenceBaselineScopeSummary,
    PhaseOneEvidenceBaselineUpstreamRef,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_evidence_baseline_handoff_review_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_evidence_baseline_handoff_review_v1.json"

_PKG = (
    "capabilities/field_understanding/"
    "phase_one_environment_cognition_evidence_baseline_handoff_review"
)
STEP_FILES = (
    f"{_PKG}/phase_one_environment_cognition_evidence_baseline_handoff_review_types_v1.py",
    f"{_PKG}/review_phase_one_environment_cognition_evidence_baseline_handoff_v1.py",
)

PROFILE_REF = "phase_one_environment_cognition_evidence_baseline_handoff_review_profile_v1"

_UPSTREAM_REFS: Tuple[PhaseOneEvidenceBaselineUpstreamRef, ...] = (
    PhaseOneEvidenceBaselineUpstreamRef(
        upstream_ref=MAIN_CHAIN_CLOSURE_REF,
        artifact_rel=(
            "_tmp_eval_out/phase_one_environment_cognition_evidence_main_chain_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_evidence_main_chain_closure_review_v1.json"
        ),
        expected_final_decision=BASELINE_FINAL_DECISION,
        verify_flag="main_chain_closure_go_verified",
    ),
    PhaseOneEvidenceBaselineUpstreamRef(
        upstream_ref=RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
        artifact_rel=(
            "_tmp_eval_out/rgb_vision_evidence_chain_integrated_closure_v1_smoke_v0/"
            "rgb_vision_evidence_chain_integrated_closure_review_v1.json"
        ),
        expected_final_decision="RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        verify_flag="rgb_vision_chain_go_verified",
    ),
    PhaseOneEvidenceBaselineUpstreamRef(
        upstream_ref=SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
        artifact_rel=(
            "_tmp_eval_out/slam_backend_evidence_chain_integrated_closure_v1_smoke_v0/"
            "slam_backend_evidence_chain_integrated_closure_review_v1.json"
        ),
        expected_final_decision="SLAM_BACKEND_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        verify_flag="slam_backend_chain_go_verified",
    ),
    PhaseOneEvidenceBaselineUpstreamRef(
        upstream_ref=RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
        artifact_rel=(
            "_tmp_eval_out/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1_smoke_v0/"
            "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_review_v1.json"
        ),
        expected_final_decision="RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO",
        verify_flag="rgb_slam_cross_modal_go_verified",
    ),
    PhaseOneEvidenceBaselineUpstreamRef(
        upstream_ref=FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        artifact_rel=(
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
        expected_final_decision="FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        verify_flag="field_task_guidance_safety_chain_go_verified",
    ),
    PhaseOneEvidenceBaselineUpstreamRef(
        upstream_ref=GOVERNANCE_CLOSURE_REF,
        artifact_rel=(
            "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
        ),
        expected_final_decision=(
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        verify_flag="runtime_governance_closure_go_verified",
    ),
    PhaseOneEvidenceBaselineUpstreamRef(
        upstream_ref=INTERFACE_LAYER_GOVERNANCE_REF,
        artifact_rel=(
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        expected_final_decision="INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        verify_flag="interface_layer_governance_verified",
    ),
    PhaseOneEvidenceBaselineUpstreamRef(
        upstream_ref=MODEL_ADMISSION_GOVERNANCE_REF,
        artifact_rel=(
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        expected_final_decision="MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        verify_flag="model_admission_governance_verified",
    ),
)


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        PhaseOneEvidenceBaselineHandoffReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            baseline_ref=BASELINE_REF,
            baseline_final_decision=BASELINE_FINAL_DECISION,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            handoff_target_refs=HANDOFF_TARGET_REFS,
            governance_rules=HANDOFF_GOVERNANCE_RULES,
        )
    )


def review_phase_one_environment_cognition_evidence_baseline_handoff_v1(
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

    upstream_checks: Dict[str, bool] = {}
    upstream_review: List[Dict[str, Any]] = []
    for ref in _UPSTREAM_REFS:
        artifact, exists = _load_upstream_artifact(ref.artifact_rel)
        actual_go = (artifact or {}).get("final_decision") if exists else None
        go_ok = exists and actual_go == ref.expected_final_decision
        upstream_checks[ref.verify_flag] = go_ok
        upstream_review.append(
            {
                "upstream_ref": ref.upstream_ref,
                "expected_final_decision": ref.expected_final_decision,
                "actual_final_decision": actual_go,
                "artifact_present": exists,
                "go_sealed": go_ok,
                "verify_flag": ref.verify_flag,
            }
        )
        if not exists:
            failed_checks.append(f"upstream_artifact_missing:{ref.upstream_ref}")
        elif not go_ok:
            failed_checks.append(f"upstream_go_mismatch:{ref.upstream_ref}:{actual_go!r}")

    template_ok = CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID

    # Baseline scope frozen flags are anchored on the main-chain closure being GO.
    main_chain_go = upstream_checks.get("main_chain_closure_go_verified") is True
    scope_summary = candidate_to_dict(
        PhaseOneEvidenceBaselineScopeSummary(
            summary_ref="phase_one_evidence_baseline_scope_summary_v1",
            rgb_vision_evidence_baseline_frozen=main_chain_go
            and upstream_checks.get("rgb_vision_chain_go_verified") is True,
            slam_spatial_evidence_baseline_frozen=main_chain_go
            and upstream_checks.get("slam_backend_chain_go_verified") is True,
            cross_modal_alignment_baseline_frozen=main_chain_go
            and upstream_checks.get("rgb_slam_cross_modal_go_verified") is True,
            field_task_guidance_candidate_path_frozen=main_chain_go
            and upstream_checks.get("field_task_guidance_safety_chain_go_verified") is True,
            deferred_expansion_record_preserved=main_chain_go,
        )
    )
    deferred_summary = candidate_to_dict(
        PhaseOneEvidenceBaselineDeferredExpansionSummary(
            summary_ref="phase_one_evidence_baseline_deferred_expansion_summary_v1",
            deferred_expansion_ids=DEFERRED_EXPANSION_IDS,
            future_information_source_expansion_deferred=True,
            latent_relation_mechanism_deferred=True,
            hidden_object_relation_mechanism_deferred=True,
        )
    )

    profile = _build_profile()

    go_conditions = {
        "handoff_review_profile_count_eq_1": True,
        "upstream_ref_count_gte_7": len(_UPSTREAM_REFS) >= 7,
        "main_chain_closure_go_verified": (
            upstream_checks.get("main_chain_closure_go_verified") is True
        ),
        "rgb_vision_chain_go_verified": (
            upstream_checks.get("rgb_vision_chain_go_verified") is True
        ),
        "slam_backend_chain_go_verified": (
            upstream_checks.get("slam_backend_chain_go_verified") is True
        ),
        "rgb_slam_cross_modal_go_verified": (
            upstream_checks.get("rgb_slam_cross_modal_go_verified") is True
        ),
        "field_task_guidance_safety_chain_go_verified": (
            upstream_checks.get("field_task_guidance_safety_chain_go_verified") is True
        ),
        "runtime_governance_closure_go_verified": (
            upstream_checks.get("runtime_governance_closure_go_verified") is True
        ),
        "interface_layer_governance_verified": (
            upstream_checks.get("interface_layer_governance_verified") is True
        ),
        "model_admission_governance_verified": (
            upstream_checks.get("model_admission_governance_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": template_ok is True,
        "rgb_vision_evidence_baseline_frozen": (
            scope_summary["rgb_vision_evidence_baseline_frozen"] is True
        ),
        "slam_spatial_evidence_baseline_frozen": (
            scope_summary["slam_spatial_evidence_baseline_frozen"] is True
        ),
        "cross_modal_alignment_baseline_frozen": (
            scope_summary["cross_modal_alignment_baseline_frozen"] is True
        ),
        "field_task_guidance_candidate_path_frozen": (
            scope_summary["field_task_guidance_candidate_path_frozen"] is True
        ),
        "deferred_expansion_record_preserved": (
            scope_summary["deferred_expansion_record_preserved"] is True
        ),
        "future_information_source_expansion_deferred": (
            deferred_summary["future_information_source_expansion_deferred"] is True
        ),
        "latent_relation_mechanism_deferred": (
            deferred_summary["latent_relation_mechanism_deferred"] is True
        ),
        "hidden_object_relation_mechanism_deferred": (
            deferred_summary["hidden_object_relation_mechanism_deferred"] is True
        ),
        "ready_for_visual_symbol_evidence_dryrun": (
            HANDOFF_READINESS_FLAGS["ready_for_visual_symbol_evidence_dryrun"] is True
        ),
        "ready_for_real_recognition_dryrun_planning": (
            HANDOFF_READINESS_FLAGS["ready_for_real_recognition_dryrun_planning"] is True
        ),
        "ready_for_future_audio_evidence_planning_when_requested": (
            HANDOFF_READINESS_FLAGS["ready_for_future_audio_evidence_planning_when_requested"]
            is True
        ),
        "ready_for_future_relation_mechanism_planning_when_requested": (
            HANDOFF_READINESS_FLAGS[
                "ready_for_future_relation_mechanism_planning_when_requested"
            ]
            is True
        ),
        "new_capability_added_false": NON_EXECUTION_FLAGS["new_capability_added"] is False,
        "new_information_source_added_false": (
            NON_EXECUTION_FLAGS["new_information_source_added"] is False
        ),
        "deferred_expansion_expanded_false": (
            NON_EXECUTION_FLAGS["deferred_expansion_expanded"] is False
        ),
        "dryrun_execution_allowed_false": (
            NON_EXECUTION_FLAGS["dryrun_execution_allowed"] is False
        ),
        "runtime_activation_allowed_false": (
            NON_EXECUTION_FLAGS["runtime_activation_allowed"] is False
        ),
        "model_download_allowed_false": NON_EXECUTION_FLAGS["model_download_allowed"] is False,
        "dataset_download_allowed_false": NON_EXECUTION_FLAGS["dataset_download_allowed"] is False,
        "training_use_allowed_false": NON_EXECUTION_FLAGS["training_use_allowed"] is False,
        "live_camera_connected_false": NON_EXECUTION_FLAGS["live_camera_connected"] is False,
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "direct_action_allowed_false": NON_EXECUTION_FLAGS["direct_action_allowed"] is False,
        "direct_speech_allowed_false": NON_EXECUTION_FLAGS["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": (
            NON_EXECUTION_FLAGS["direct_fact_write_allowed"] is False
        ),
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
        "step": "Phase One Environment Cognition Evidence Baseline Handoff Review",
        "lifecycle_variant": "phase_one_environment_cognition_evidence_baseline_handoff_review",
        "handoff_principle_zh": HANDOFF_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "baseline_ref": BASELINE_REF,
        "baseline_final_decision": BASELINE_FINAL_DECISION,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "handoff_governance_rules": list(HANDOFF_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "handoff_readiness_flags": dict(HANDOFF_READINESS_FLAGS),
        "handoff_target_refs": list(HANDOFF_TARGET_REFS),
        "handoff_review_profile": profile,
        "upstream_ref_count": len(_UPSTREAM_REFS),
        "upstream_sealed_phase_review": upstream_review,
        "upstream_verify_flags": upstream_checks,
        "baseline_scope_summary": scope_summary,
        "deferred_expansion_summary": deferred_summary,
        "go_conditions": go_conditions,
        "conclusions": {
            "baseline_handoff_status": (
                "phase_one_environment_cognition_evidence_main_chain_baseline_handoff_ready"
                if review_ok
                else "blocked"
            ),
            "baseline_ref": BASELINE_REF,
            "baseline_final_decision": BASELINE_FINAL_DECISION,
            "downstream_ready_for": list(HANDOFF_TARGET_REFS),
            "transition_note": (
                "Phase-One environment cognition evidence main chain confirmed as the stable "
                "upstream baseline. No new capability or information source added; deferred "
                "expansions preserved as records. Downstream phases (Visual Symbol Evidence "
                "DryRun, real-recognition dry-run, future audio/behavior/memory/map/relation "
                "expansion) may reference this baseline. Next: choose Visual Symbol Evidence "
                "DryRun or real-recognition dry-run."
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
    result = review_phase_one_environment_cognition_evidence_baseline_handoff_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "upstream_ref_count": result["upstream_ref_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
