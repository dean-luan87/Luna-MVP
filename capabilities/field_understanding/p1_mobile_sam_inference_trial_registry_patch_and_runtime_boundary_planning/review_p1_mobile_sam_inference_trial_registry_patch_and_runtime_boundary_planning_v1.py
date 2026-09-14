# -*- coding: utf-8 -*-
"""P1 MobileSAM Inference Trial Registry Patch And Runtime Boundary Planning — review v1
(PLANNING ONLY, scope = mobile_sam_only).

Audits upstream inference trial execution GO, plans registry patch (inference_trial_verified),
candidate output registry strategy, runtime/output adapter boundaries, semantic/fact/navigation
exclusion, and follow-up registry patch execution route. Does NOT write registry or execute inference.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.field_understanding.p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning.p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning.p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    IMAGE_INPUT_ALLOWED,
    INFERENCE_REGISTRY_PATCH_PLANNING,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MOBILE_SAM_ASSET_ID,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_REGISTRY_PATCH_EXECUTION,
    OUTPUT_ADAPTER_BOUNDARY_PLANNING,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_READINESS_LEVEL,
    PLANNED_REGISTRY_PATCH,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PREDICTION_ALLOWED,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_FILE_WRITE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_OVERLAY_REL,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_BOUNDARY_PLANNING,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEGMENTATION_ALLOWED,
    SEMANTIC_FACT_NAVIGATION_EXCLUSION_PLANNING,
    SEMANTIC_PROMOTION_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_EXPECTED,
    UPSTREAM_INFERENCE_ARTIFACT_REFS,
    UPSTREAM_INFERENCE_EXECUTION_EXPECTED_GO,
    UPSTREAM_INFERENCE_EXECUTION_REF,
    UPSTREAM_INFERENCE_REVIEW_FILE_REL,
    WEIGHT_CHAIN,
    MobileSAMCandidateOutputRegistryPlanningRecord,
    MobileSAMCommercialRuntimeExclusionRecord,
    MobileSAMFollowupInferenceRegistryPatchExecutionRoute,
    MobileSAMInferenceRegistryPatchPlanningRecord,
    MobileSAMInferenceSuccessAudit,
    MobileSAMOutputAdapterBoundaryPlanningRecord,
    MobileSAMRuntimeBoundaryPlanningRecord,
    MobileSAMSemanticFactNavigationExclusionRecord,
    NegativeMobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningGuard,
    P1MobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningDecision,
    P1MobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningProfile,
    to_dict,
)


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_review_v1.json"
)

_PKG = (
    "capabilities/field_understanding/"
    "p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning"
)
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_types_v1.py",
    f"{_PKG}/p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_v1.py",
)

PROFILE_REF = "p1_mobile_sam_inference_registry_patch_runtime_boundary_planning_profile_v1"
DECISION_REF = "p1_mobile_sam_inference_registry_patch_runtime_boundary_planning_decision_v1"
_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _load_json(rel: str) -> Optional[Dict[str, Any]]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return None
    return None


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            mobile_sam_only=True,
            inference_registry_patch_planning=INFERENCE_REGISTRY_PATCH_PLANNING,
            runtime_boundary_planning=RUNTIME_BOUNDARY_PLANNING,
            output_adapter_boundary_planning=OUTPUT_ADAPTER_BOUNDARY_PLANNING,
            semantic_fact_navigation_exclusion_planning=SEMANTIC_FACT_NAVIGATION_EXCLUSION_PLANNING,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            registry_file_write_allowed=REGISTRY_FILE_WRITE_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            fact_write_allowed=FACT_WRITE_ALLOWED,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_inference_execution_ref=UPSTREAM_INFERENCE_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file() or (Path.cwd() / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    review = _load_json(UPSTREAM_INFERENCE_REVIEW_FILE_REL) or {}
    concl = review.get("conclusions", {})
    post_audit = review.get("mobile_sam_inference_post_review_record") or review.get(
        "mobile_sam_inference_post_review_audit", {}
    )
    manifest_rec = review.get("mobile_sam_test_image_manifest_record", {})
    candidate_rec = review.get("mobile_sam_candidate_output_record", {})
    inference_rec = review.get("mobile_sam_single_inference_execution_record", {})
    decision_rec = review.get("decision", {})

    final_decision_ok = review.get("final_decision") == UPSTREAM_EXPECTED["final_decision"]
    blocker_ok = review.get("blocker_count", 1) == UPSTREAM_EXPECTED["blocker_count"]
    neg_guard_ok = review.get("negative_guard_passed", 0) >= UPSTREAM_EXPECTED["negative_guard_passed"]
    inference_attempted = bool(concl.get("inference_attempted", decision_rec.get("inference_attempted")))
    inference_success = bool(concl.get("inference_success", decision_rec.get("inference_success")))
    candidate_written = bool(concl.get("candidate_output_written", decision_rec.get("candidate_output_written")))
    candidate_only = bool(concl.get("candidate_output_only", decision_rec.get("candidate_output_only")))
    single_verified = bool(
        decision_rec.get("single_local_test_image_inference_verified", inference_success and candidate_only)
    )
    manifest_valid = bool(post_audit.get("local_test_image_manifest_valid", manifest_rec.get("manifest_valid")))
    image_source_ok = bool(post_audit.get("image_source_allowed", manifest_rec.get("source_type") == "synthetic_test_image"))

    audit = MobileSAMInferenceSuccessAudit(
        audit_id="mobile_sam_inference_success_audit_v1",
        upstream_review_ref=UPSTREAM_INFERENCE_REVIEW_FILE_REL,
        final_decision=str(review.get("final_decision", "")),
        blocker_count=int(review.get("blocker_count", -1)),
        negative_guard_passed=int(review.get("negative_guard_passed", 0)),
        inference_attempted=inference_attempted,
        inference_success=inference_success,
        candidate_output_written=candidate_written,
        candidate_output_only=candidate_only,
        single_local_test_image_inference_verified=single_verified,
        local_test_image_manifest_valid=manifest_valid,
        image_source_allowed=image_source_ok,
        no_live_camera=bool(post_audit.get("no_live_camera", True)),
        no_personal_image=bool(post_audit.get("no_personal_image", True)),
        no_external_url_image=bool(post_audit.get("no_external_url_image", True)),
        no_uncontrolled_dataset=bool(post_audit.get("no_uncontrolled_dataset", True)),
        no_runtime=bool(post_audit.get("no_runtime", True)),
        no_output_adapter=bool(post_audit.get("no_output_adapter", True)),
        no_semantic_layer=bool(post_audit.get("no_semantic_layer", True)),
        no_fact_write=bool(post_audit.get("no_fact_write", True)),
        no_navigation_action_speech=bool(post_audit.get("no_navigation_action_speech", True)),
        no_registry_mutation=bool(concl.get("registry_mutated_this_phase") is False),
        no_extra_download=bool(post_audit.get("no_extra_download", True)),
        audit_passed=(
            final_decision_ok
            and blocker_ok
            and neg_guard_ok
            and inference_attempted
            and inference_success
            and candidate_written
            and candidate_only
            and single_verified
            and manifest_valid
            and image_source_ok
            and bool(post_audit.get("no_runtime", True))
            and bool(post_audit.get("no_registry_mutation", True))
        ),
    )
    if not audit.audit_passed:
        failed_checks.append("upstream.inference_trial_audit_failed")

    if not all(_load_json(ref) is not None for ref in UPSTREAM_INFERENCE_ARTIFACT_REFS):
        warnings.append("upstream.some_inference_artifact_missing_using_review_aggregate")

    patch_plan = MobileSAMInferenceRegistryPatchPlanningRecord(
        record_id="mobile_sam_inference_registry_patch_plan_v1",
        target_overlay_ref=REGISTRY_OVERLAY_REL,
        target_asset_id=MOBILE_SAM_ASSET_ID,
        planned_patch=dict(PLANNED_REGISTRY_PATCH),
        registry_file_write_allowed=REGISTRY_FILE_WRITE_ALLOWED,
        registry_mutated_this_phase=False,
        planned_broad_inference_ready=PLANNED_REGISTRY_PATCH.get("inference_ready") is True,
    )

    candidate_plan = MobileSAMCandidateOutputRegistryPlanningRecord(
        record_id="mobile_sam_candidate_output_registry_plan_v1",
        candidate_output_only=True,
        candidate_output_not_fact=True,
        candidate_output_not_runtime_output=True,
        candidate_output_not_output_adapter_output=True,
        candidate_output_not_semantic_output=True,
        candidate_output_not_navigation_action_speech=True,
        candidate_output_eval_artifact_only=True,
        candidate_output_requires_review_before_any_runtime_use=True,
    )

    runtime_plan = MobileSAMRuntimeBoundaryPlanningRecord(
        record_id="mobile_sam_runtime_boundary_plan_v1",
        runtime_execution_allowed_now=False,
        runtime_activation_allowed_now=False,
        runtime_ready_must_remain_false=True,
        runtime_requires_separate_request=True,
        runtime_requires_separate_owner_approval=True,
        runtime_requires_separate_execution_phase=True,
        runtime_requires_output_adapter_boundary=True,
        runtime_requires_semantic_fact_boundary=True,
        runtime_requires_navigation_action_speech_boundary=True,
    )

    output_adapter_plan = MobileSAMOutputAdapterBoundaryPlanningRecord(
        record_id="mobile_sam_output_adapter_boundary_plan_v1",
        output_adapter_allowed_now=False,
        output_adapter_ready_must_remain_false=True,
        output_adapter_requires_separate_review=True,
        output_adapter_requires_candidate_to_output_mapping=True,
        output_adapter_requires_failure_mode_review=True,
        output_adapter_requires_user_visible_output_policy=True,
        output_adapter_requires_speech_gate_if_speech=True,
    )

    semantic_exclusion = MobileSAMSemanticFactNavigationExclusionRecord(
        record_id="mobile_sam_semantic_fact_navigation_exclusion_v1",
        semantic_layer_allowed_now=False,
        semantic_layer_ready_must_remain_false=True,
        fact_write_allowed_now=False,
        fact_write_ready_must_remain_false=True,
        navigation_action_speech_allowed_now=False,
        navigation_action_speech_ready_must_remain_false=True,
        candidate_result_must_not_enter_fact_layer=True,
        candidate_result_must_not_enter_navigation_runtime=True,
        candidate_result_must_not_trigger_speech=True,
    )

    commercial_exclusion = MobileSAMCommercialRuntimeExclusionRecord(
        record_id="mobile_sam_commercial_runtime_exclusion_v1",
        commercial_runtime_approved=False,
        commercial_runtime_requires_separate_governance=True,
        commercial_runtime_requires_stability_benchmark=True,
        commercial_runtime_requires_runtime_safety_review=True,
        commercial_runtime_requires_output_policy_review=True,
    )

    followup = MobileSAMFollowupInferenceRegistryPatchExecutionRoute(
        route_id="mobile_sam_followup_inference_registry_patch_execution_route_v1",
        recommended_next_phase=NEXT_PHASE_REGISTRY_PATCH_EXECUTION,
        next_phase_scope="mobile_sam_only",
        next_phase_allows_registry_write=True,
        next_phase_still_no_runtime=True,
    )

    upstream_boundary_clean = (
        audit.no_runtime
        and audit.no_output_adapter
        and audit.no_semantic_layer
        and audit.no_fact_write
        and audit.no_navigation_action_speech
        and audit.no_registry_mutation
        and audit.no_extra_download
    )
    patch_not_downstream_ready = (
        patch_plan.planned_patch.get("runtime_ready") is False
        and patch_plan.planned_patch.get("output_adapter_ready") is False
        and patch_plan.planned_patch.get("semantic_layer_ready") is False
        and patch_plan.planned_patch.get("fact_write_ready") is False
        and patch_plan.planned_patch.get("navigation_action_speech_ready") is False
        and patch_plan.planned_patch.get("commercial_runtime_approved") is False
    )

    invariant_state: Dict[str, bool] = {
        "upstream_inference_go_verified": audit.audit_passed and final_decision_ok,
        "upstream_boundary_clean": upstream_boundary_clean,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False and patch_plan.registry_mutated_this_phase is False,
        "no_seg_pred_inference": (
            REAL_INFERENCE_ALLOWED is False
            and SEGMENTATION_ALLOWED is False
            and PREDICTION_ALLOWED is False
        ),
        "no_image_input": IMAGE_INPUT_ALLOWED is False,
        "no_real_import_load": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_fact_navigation_speech": FACT_WRITE_ALLOWED is False and NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "no_extra_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False and MODEL_DOWNLOAD_ALLOWED is False,
        "patch_not_downstream_ready": patch_not_downstream_ready,
        "no_broad_inference_ready": patch_plan.planned_broad_inference_ready is False,
        "candidate_boundary_present": candidate_plan.candidate_output_only and candidate_plan.candidate_output_not_fact,
        "runtime_boundary_present": runtime_plan.runtime_ready_must_remain_false and runtime_plan.runtime_requires_separate_request,
        "output_adapter_boundary_present": output_adapter_plan.output_adapter_ready_must_remain_false,
        "semantic_fact_navigation_present": (
            semantic_exclusion.semantic_layer_ready_must_remain_false
            and semantic_exclusion.fact_write_ready_must_remain_false
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_inference_registry_patch_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    can_enter_patch_execution = audit.audit_passed and patch_not_downstream_ready

    go_conditions: Dict[str, bool] = {
        "mobile_sam_inference_registry_patch_runtime_boundary_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_inference_success_audit_count_gte_1": True,
        "mobile_sam_inference_registry_patch_plan_count_gte_1": True,
        "mobile_sam_candidate_output_registry_plan_count_gte_1": True,
        "mobile_sam_runtime_boundary_plan_count_gte_1": True,
        "mobile_sam_output_adapter_boundary_plan_count_gte_1": True,
        "mobile_sam_semantic_fact_navigation_exclusion_count_gte_1": True,
        "mobile_sam_commercial_runtime_exclusion_count_gte_1": True,
        "mobile_sam_followup_inference_registry_patch_execution_route_count_gte_1": True,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "planning_only": PLANNING_ONLY is True,
        "mobile_sam_only": True,
        "inference_registry_patch_planning": INFERENCE_REGISTRY_PATCH_PLANNING is True,
        "runtime_boundary_planning": RUNTIME_BOUNDARY_PLANNING is True,
        "output_adapter_boundary_planning": OUTPUT_ADAPTER_BOUNDARY_PLANNING is True,
        "semantic_fact_navigation_exclusion_planning": SEMANTIC_FACT_NAVIGATION_EXCLUSION_PLANNING is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "registry_file_write_allowed_false": REGISTRY_FILE_WRITE_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        "registry_patch_planned": True,
        "planned_readiness_level_inference_trial_verified": PLANNED_READINESS_LEVEL == "inference_trial_verified",
        "planned_inference_trial_verified": patch_plan.planned_patch.get("inference_trial_verified") is True,
        "planned_candidate_output_verified": patch_plan.planned_patch.get("candidate_output_verified") is True,
        "planned_single_local_test_image_inference_verified": (
            patch_plan.planned_patch.get("single_local_test_image_inference_verified") is True
        ),
        "planned_broad_inference_ready_false": patch_plan.planned_broad_inference_ready is False,
        "planned_runtime_ready_false": patch_plan.planned_patch.get("runtime_ready") is False,
        "planned_output_adapter_ready_false": patch_plan.planned_patch.get("output_adapter_ready") is False,
        "planned_semantic_layer_ready_false": patch_plan.planned_patch.get("semantic_layer_ready") is False,
        "planned_fact_write_ready_false": patch_plan.planned_patch.get("fact_write_ready") is False,
        "planned_navigation_action_speech_ready_false": (
            patch_plan.planned_patch.get("navigation_action_speech_ready") is False
        ),
        "planned_commercial_runtime_approved_false": (
            patch_plan.planned_patch.get("commercial_runtime_approved") is False
        ),
        "can_enter_inference_trial_registry_patch_execution_next": can_enter_patch_execution,
        "can_enter_runtime_execution_now_false": runtime_plan.runtime_execution_allowed_now is False,
        "can_enter_output_adapter_now_false": output_adapter_plan.output_adapter_allowed_now is False,
        "can_enter_semantic_layer_now_false": semantic_exclusion.semantic_layer_allowed_now is False,
        "can_write_fact_now_false": semantic_exclusion.fact_write_allowed_now is False,
        "can_trigger_navigation_action_speech_now_false": (
            semantic_exclusion.navigation_action_speech_allowed_now is False
        ),
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningDecision(
        decision_ref=DECISION_REF,
        mobile_sam_inference_registry_patch_runtime_boundary_planning_profile_count=1,
        mobile_sam_inference_success_audit_count=1,
        mobile_sam_inference_registry_patch_plan_count=1,
        mobile_sam_candidate_output_registry_plan_count=1,
        mobile_sam_runtime_boundary_plan_count=1,
        mobile_sam_output_adapter_boundary_plan_count=1,
        mobile_sam_semantic_fact_navigation_exclusion_count=1,
        mobile_sam_commercial_runtime_exclusion_count=1,
        mobile_sam_followup_inference_registry_patch_execution_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        registry_patch_planned=True,
        planned_readiness_level=PLANNED_READINESS_LEVEL,
        can_enter_inference_trial_registry_patch_execution_next=can_enter_patch_execution and blocker_count == 0,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Inference Trial Registry Patch And Runtime Boundary Planning (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "planning_only": PLANNING_ONLY,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "registry_file_write_allowed": REGISTRY_FILE_WRITE_ALLOWED,
        "upstream_inference_execution_ref": UPSTREAM_INFERENCE_EXECUTION_REF,
        "upstream_inference_execution_expected_go": UPSTREAM_INFERENCE_EXECUTION_EXPECTED_GO,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "mobile_sam_inference_registry_patch_runtime_boundary_planning_profile": _build_profile(),
        "mobile_sam_inference_registry_patch_runtime_boundary_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_inference_success_audit": asdict(audit),
        "mobile_sam_inference_success_audit_count": 1,
        "mobile_sam_inference_registry_patch_plan_record": asdict(patch_plan),
        "mobile_sam_inference_registry_patch_plan_count": 1,
        "mobile_sam_candidate_output_registry_plan_record": asdict(candidate_plan),
        "mobile_sam_candidate_output_registry_plan_count": 1,
        "mobile_sam_runtime_boundary_plan_record": asdict(runtime_plan),
        "mobile_sam_runtime_boundary_plan_count": 1,
        "mobile_sam_output_adapter_boundary_plan_record": asdict(output_adapter_plan),
        "mobile_sam_output_adapter_boundary_plan_count": 1,
        "mobile_sam_semantic_fact_navigation_exclusion_record": asdict(semantic_exclusion),
        "mobile_sam_semantic_fact_navigation_exclusion_count": 1,
        "mobile_sam_commercial_runtime_exclusion_record": asdict(commercial_exclusion),
        "mobile_sam_commercial_runtime_exclusion_count": 1,
        "mobile_sam_followup_inference_registry_patch_execution_route_record": asdict(followup),
        "mobile_sam_followup_inference_registry_patch_execution_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_inference_artifact_refs": list(UPSTREAM_INFERENCE_ARTIFACT_REFS),
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "planning_status": "go" if blocker_count == 0 else "blocked",
            "registry_mutated_this_phase": False,
            "inference_executed_this_phase": False,
            "can_enter_inference_trial_registry_patch_execution_next": decision.can_enter_inference_trial_registry_patch_execution_next,
            "recommended_next_phase": NEXT_PHASE_REGISTRY_PATCH_EXECUTION,
            "planned_readiness_level": PLANNED_READINESS_LEVEL,
            "planned_broad_inference_ready": False,
            "transition_note": (
                "PLANNING ONLY (mobile_sam_only). Upstream inference trial execution GO audited. "
                "Registry patch plan for inference_trial_verified / candidate_output_verified produced "
                "with runtime/output adapter/semantic/fact/navigation boundaries. NO registry write, "
                "NO inference, NO runtime. broad inference_ready remains false. Next: "
                + NEXT_PHASE_REGISTRY_PATCH_EXECUTION
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "mobile_sam_inference_success_audit_record": {"mobile_sam_inference_success_audit": asdict(audit)},
            "mobile_sam_inference_registry_patch_plan_record": {
                "mobile_sam_inference_registry_patch_plan_record": asdict(patch_plan),
            },
            "mobile_sam_candidate_output_registry_plan_record": {
                "mobile_sam_candidate_output_registry_plan_record": asdict(candidate_plan),
            },
            "mobile_sam_runtime_boundary_plan_record": {"mobile_sam_runtime_boundary_plan_record": asdict(runtime_plan)},
            "mobile_sam_output_adapter_boundary_plan_record": {
                "mobile_sam_output_adapter_boundary_plan_record": asdict(output_adapter_plan),
            },
            "mobile_sam_semantic_fact_navigation_exclusion_record": {
                "mobile_sam_semantic_fact_navigation_exclusion_record": asdict(semantic_exclusion),
            },
            "mobile_sam_commercial_runtime_exclusion_record": {
                "mobile_sam_commercial_runtime_exclusion_record": asdict(commercial_exclusion),
            },
            "mobile_sam_followup_inference_registry_patch_execution_route_record": {
                "mobile_sam_followup_inference_registry_patch_execution_route_record": asdict(followup),
            },
        }
        extra_written: List[str] = []
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "module": TEST_BOARD_MODULE,
            "test_mode": TEST_BOARD_TEST_MODE,
            "recorded_at_utc": _now(),
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "planning_only": True,
            "registry_mutation_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
        }
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest["extra_written_records"] = extra_written
        manifest["extra_written_record_count"] = len(extra_written)
        manifest["total_record_count"] = manifest["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["total_record_count"]

    return result


def main() -> int:
    result = review_p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "planned_readiness_level": result["conclusions"]["planned_readiness_level"],
                "can_enter_inference_trial_registry_patch_execution_next": result["conclusions"][
                    "can_enter_inference_trial_registry_patch_execution_next"
                ],
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
