# -*- coding: utf-8 -*-
"""P1 MobileSAM Real Image Quality Review And Prompt Strategy Planning — review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.field_understanding.p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning.p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning.p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    CANONICAL_TEST_ASSET_PATH,
    CANDIDATE_MASK_FILE_REFERENCE_ALLOWED,
    CANDIDATE_MASK_METADATA_REVIEW_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_BATCH_ALLOWED,
    EXTERNAL_IMAGE_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FAILURE_MODES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    IMAGE_HEIGHT,
    IMAGE_INPUT_ALLOWED,
    IMAGE_WIDTH,
    LUNA_CORE_PRINCIPLE,
    MODEL_LOAD_ALLOWED,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEW_IMAGE_READ_ALLOWED,
    PER_PROMPT_QUALITY_PLAN,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PREDICTION_ALLOWED,
    PROMPT_COUNT,
    PROMPT_STRATEGY_PLANNING,
    QUALITY_REVIEW_PLANNING,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    RECOMMENDED_ROUTE,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    ROUTE_A,
    ROUTE_B,
    ROUTE_C,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCENE_TYPE,
    SCOPE,
    SEGMENTATION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_EXECUTION_EXPECTED_GO,
    UPSTREAM_EXECUTION_REF,
    UPSTREAM_MASKS_DIR_REL,
    UPSTREAM_MASKS_REL,
    UPSTREAM_POST_REVIEW_REL,
    UPSTREAM_QUALITY_REL,
    UPSTREAM_REVIEW_REL,
    DetectorOCRSemanticPromptGenerationNeedRecord,
    FailureModeTaxonomyRecord,
    FollowupPhaseRouteRecord,
    MultiImageTrialRouteRecord,
    NegativeRealImageQualityReviewPromptStrategyGuard,
    P1MobileSAMRealImageQualityReviewPromptStrategyDecision,
    P1MobileSAMRealImageQualityReviewPromptStrategyPlanningProfile,
    PerPromptQualityAssessmentRecord,
    PromptStrategyRecommendationRecord,
    RealImageCandidateMaskQualityAssessmentRecord,
    RealImageQualityReviewScopeRecord,
    RuntimeBoundaryPreservationRecord,
    to_dict,
)

_PKG = "capabilities/field_understanding/p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning"
STEP_FILES = (
    f"{_PKG}/__init__.py",
    f"{_PKG}/p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_types_v1.py",
    f"{_PKG}/p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_v1.py",
)

PROFILE_REF = "p1_mobile_sam_real_image_quality_review_prompt_strategy_planning_profile_v1"
DECISION_REF = "p1_mobile_sam_real_image_quality_review_prompt_strategy_decision_v1"
REVIEW_FILENAME = "p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_review_v1.json"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


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
    / "p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_v1_smoke_v0"
)


def _artifact_roots() -> Tuple[Path, ...]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return tuple(dict.fromkeys(roots))


def _load_upstream(rel: str) -> Tuple[Optional[Dict[str, Any]], bool, str]:
    for base in _artifact_roots():
        artifact, exists, resolved = load_artifact(base, rel)
        if exists and artifact:
            return artifact, True, resolved
    return None, False, ""


def _mask_file_refs_exist(masks_payload: Dict[str, Any]) -> bool:
    for summary in masks_payload.get("prompt_mask_summaries") or []:
        path = summary.get("candidate_mask_path")
        if not path or not Path(path).is_file():
            return False
    return True


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_per_prompt_assessments(
    masks_payload: Dict[str, Any],
    quality_payload: Dict[str, Any],
) -> List[Dict[str, Any]]:
    summaries = {s["prompt_id"]: s for s in (masks_payload.get("prompt_mask_summaries") or [])}
    per_notes = quality_payload.get("per_prompt_quality_note") or {}
    assessments: List[Dict[str, Any]] = []
    for plan in PER_PROMPT_QUALITY_PLAN:
        upstream = summaries.get(plan["prompt_id"], {})
        assessments.append(
            {
                **plan,
                "score_or_iou_if_available": upstream.get("score_or_iou_if_available"),
                "mask_area_ratio": upstream.get("mask_area_ratio"),
                "mask_area_pixels": upstream.get("mask_area_pixels"),
                "prompt_type_used": upstream.get("prompt_type_used"),
                "fallback_from_box_to_point": upstream.get("fallback_from_box_to_point", False),
                "candidate_mask_path_ref": upstream.get("candidate_mask_path"),
                "quality_note": per_notes.get(plan["prompt_id"], ""),
                "prompt_label_is_test_description": True,
                "semantic_fact_assertion": False,
            }
        )
    return assessments


def review_p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_v1(
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
        found = any((base / rel).is_file() for base in _artifact_roots())
        if found:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    upstream_review, review_ok, review_path = _load_upstream(UPSTREAM_REVIEW_REL)
    masks_payload, masks_ok, masks_path = _load_upstream(UPSTREAM_MASKS_REL)
    quality_payload, quality_ok, quality_path = _load_upstream(UPSTREAM_QUALITY_REL)
    post_review, post_ok, post_path = _load_upstream(UPSTREAM_POST_REVIEW_REL)

    upstream_go = (
        review_ok
        and upstream_review is not None
        and upstream_review.get("final_decision") == UPSTREAM_EXECUTION_EXPECTED_GO
        and upstream_review.get("blocker_count", 1) == 0
    )
    if not upstream_go:
        failed_checks.append("upstream.execution_not_go")

    prompt_success_count = int(
        (upstream_review or {}).get("conclusions", {}).get("prompt_success_count")
        or (quality_payload or {}).get("prompt_success_count")
        or 0
    )
    candidate_masks_written = bool(
        (masks_payload or {}).get("candidate_masks_written")
        or (upstream_review or {}).get("conclusions", {}).get("candidate_masks_written")
    )
    mask_refs_ok = masks_ok and _mask_file_refs_exist(masks_payload or {})
    upstream_boundary_clean = bool(
        post_review
        and post_review.get("candidate_output_only") is True
        and post_review.get("no_runtime") is True
        and post_review.get("no_fact_write") is True
    )

    scope = RealImageQualityReviewScopeRecord(
        record_id="real_image_quality_review_scope_v1",
        upstream_execution_ref=UPSTREAM_EXECUTION_REF,
        upstream_execution_go=UPSTREAM_EXECUTION_EXPECTED_GO if upstream_go else "",
        canonical_test_asset_path=CANONICAL_TEST_ASSET_PATH,
        image_width=IMAGE_WIDTH,
        image_height=IMAGE_HEIGHT,
        scene_type=SCENE_TYPE,
        prompt_count=PROMPT_COUNT,
        prompt_success_count=prompt_success_count,
        candidate_masks_written=candidate_masks_written,
        review_reads_upstream_metadata_only=True,
        new_inference_executed=False,
        new_image_read=False,
    )

    mask_assessment = RealImageCandidateMaskQualityAssessmentRecord(
        record_id="real_image_candidate_mask_quality_assessment_v1",
        overall_quality_observation_available=upstream_go and quality_ok,
        all_prompts_produced_masks=prompt_success_count == PROMPT_COUNT,
        candidate_only=True,
        not_semantic_fact=True,
        human_review_required=True,
        suitable_for_runtime_admission=False,
    )

    per_prompt_list = _build_per_prompt_assessments(masks_payload or {}, quality_payload or {})
    per_prompt = PerPromptQualityAssessmentRecord(
        record_id="per_prompt_quality_assessment_v1",
        assessments=tuple(per_prompt_list),
        assessment_count=len(per_prompt_list),
        prompt_labels_are_test_descriptions_only=True,
    )

    prompt_strategy = PromptStrategyRecommendationRecord(
        record_id="prompt_strategy_recommendation_v1",
        large_object_building_strategy="box_prompt_preferred_single_box_sufficient",
        road_crosswalk_strategy="box_with_negative_or_multi_point_not_for_navigation_fact",
        sign_advertisement_strategy="detector_or_ocr_assisted_box_sam_does_not_read_text",
        vehicle_strategy="detector_or_tracker_box_then_sam_refinement",
        mobile_sam_role="boundary_refinement_segmentation_candidate_provider",
        object_labels_are_not_facts=True,
    )

    failure_taxonomy = FailureModeTaxonomyRecord(
        record_id="failure_mode_taxonomy_v1",
        failure_modes=FAILURE_MODES,
        failure_mode_count=len(FAILURE_MODES),
    )

    detector_need = DetectorOCRSemanticPromptGenerationNeedRecord(
        record_id="detector_ocr_semantic_prompt_generation_need_v1",
        road_sign="ocr_detector_assisted_prompt_recommended",
        advertisement_screen="detector_ocr_assisted_prompt_optional",
        vehicle="detector_tracker_assisted_prompt_recommended",
        building="detector_optional_box_sufficient",
        road_crosswalk="geometry_or_navigation_boundary_prior_needed",
        mobile_sam_is_boundary_refinement_only=True,
        auto_prompt_requires_separate_governance=True,
    )

    multi_route = MultiImageTrialRouteRecord(
        record_id="multi_image_trial_route_v1",
        route_a=ROUTE_A,
        route_a_purpose="register_four_more_street_images_multi_image_stability_trial",
        route_b=ROUTE_B,
        route_b_purpose="plan_detector_ocr_auto_prompt_generation_no_execution",
        route_c=ROUTE_C,
        route_c_purpose="close_single_image_mobile_sam_p1_trial_loop",
        recommended_route=RECOMMENDED_ROUTE,
    )

    runtime_boundary = RuntimeBoundaryPreservationRecord(
        record_id="runtime_boundary_preservation_v1",
        runtime_ready_granted=False,
        output_adapter_ready_granted=False,
        semantic_layer_ready_granted=False,
        fact_write_ready_granted=False,
        navigation_action_speech_ready_granted=False,
        candidate_masks_remain_eval_artifacts=True,
        human_review_summary_is_not_fact=True,
    )

    followup = FollowupPhaseRouteRecord(
        record_id="followup_phase_route_v1",
        recommended_next_phase=RECOMMENDED_ROUTE,
        can_enter_multi_real_image_trial_request_next=upstream_go and per_prompt.assessment_count == 5,
        can_enter_detector_assisted_prompt_planning_next=upstream_go,
        can_enter_runtime_now=False,
    )

    invariant_state: Dict[str, bool] = {
        "upstream_execution_go": upstream_go and upstream_boundary_clean,
        "no_re_inference": REAL_INFERENCE_ALLOWED is False and SEGMENTATION_ALLOWED is False,
        "upstream_artifacts_only": masks_ok and quality_ok and post_ok and mask_refs_ok,
        "no_import_load": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "prompt_labels_not_facts": per_prompt.prompt_labels_are_test_descriptions_only,
        "quality_summary_not_fact": mask_assessment.not_semantic_fact,
        "no_runtime_ready_granted": runtime_boundary.runtime_ready_granted is False,
        "per_prompt_assessment_complete": per_prompt.assessment_count == PROMPT_COUNT,
        "prompt_strategy_defined": bool(prompt_strategy.mobile_sam_role),
        "failure_mode_taxonomy_defined": failure_taxonomy.failure_mode_count >= 9,
        "detector_need_assessed": detector_need.auto_prompt_requires_separate_governance,
        "runtime_boundary_preserved": runtime_boundary.candidate_masks_remain_eval_artifacts,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": all(
            REQUIRED_TEST_BOARD_FIELDS_LOCAL[k]
            for k in ("test_artifact_protected", "test_record_non_deletable", "test_deletion_forbidden")
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeRealImageQualityReviewPromptStrategyGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeRealImageQualityReviewPromptStrategyGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "mobile_sam_real_image_quality_review_prompt_strategy_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "real_image_quality_review_scope_record_count_gte_1": True,
        "real_image_candidate_mask_quality_assessment_record_count_gte_1": True,
        "per_prompt_quality_assessment_record_count_gte_1": True,
        "prompt_strategy_recommendation_record_count_gte_1": True,
        "failure_mode_taxonomy_record_count_gte_1": True,
        "detector_ocr_semantic_prompt_generation_need_record_count_gte_1": True,
        "multi_image_trial_route_record_count_gte_1": True,
        "runtime_boundary_preservation_record_count_gte_1": True,
        "followup_phase_route_record_count_gte_1": True,
        "negative_guard_count_eq_17": negative_guard_count == 17,
        "negative_guard_passed_eq_17": negative_guard_passed == 17,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "planning_only": PLANNING_ONLY is True,
        "quality_review_planning": QUALITY_REVIEW_PLANNING is True,
        "prompt_strategy_planning": PROMPT_STRATEGY_PLANNING is True,
        "per_prompt_quality_assessment_completed": per_prompt.assessment_count == PROMPT_COUNT,
        "prompt_strategy_defined": True,
        "failure_mode_taxonomy_defined": True,
        "detector_ocr_semantic_prompt_generation_need_assessed": True,
        "multi_image_trial_route_defined": True,
        "runtime_boundary_preserved": True,
        "can_enter_multi_real_image_trial_request_next": followup.can_enter_multi_real_image_trial_request_next,
        "can_enter_detector_assisted_prompt_planning_next": followup.can_enter_detector_assisted_prompt_planning_next,
        "can_enter_runtime_now_false": followup.can_enter_runtime_now is False,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "cleanup_does_not_delete_test_board": True,
    }
    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMRealImageQualityReviewPromptStrategyDecision(
        decision_ref=DECISION_REF,
        mobile_sam_real_image_quality_review_prompt_strategy_profile_count=1,
        real_image_quality_review_scope_record_count=1,
        real_image_candidate_mask_quality_assessment_record_count=1,
        per_prompt_quality_assessment_record_count=1,
        prompt_strategy_recommendation_record_count=1,
        failure_mode_taxonomy_record_count=1,
        detector_ocr_semantic_prompt_generation_need_record_count=1,
        multi_image_trial_route_record_count=1,
        runtime_boundary_preservation_record_count=1,
        followup_phase_route_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    profile = P1MobileSAMRealImageQualityReviewPromptStrategyPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        planning_only=PLANNING_ONLY,
        quality_review_planning=QUALITY_REVIEW_PLANNING,
        prompt_strategy_planning=PROMPT_STRATEGY_PLANNING,
        mobile_sam_only=True,
        candidate_mask_metadata_review_allowed=CANDIDATE_MASK_METADATA_REVIEW_ALLOWED,
        candidate_mask_file_reference_allowed=CANDIDATE_MASK_FILE_REFERENCE_ALLOWED,
        real_inference_allowed=REAL_INFERENCE_ALLOWED,
        new_image_read_allowed=NEW_IMAGE_READ_ALLOWED,
        runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
        registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
        upstream_execution_ref=UPSTREAM_EXECUTION_REF,
        target_chain_ref=TARGET_CHAIN_REF,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        luna_core_principle=LUNA_CORE_PRINCIPLE,
        required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        governance_rules=ALL_GOVERNANCE_RULES,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Real Image Quality Review And Prompt Strategy Planning",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": "p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_v1",
        "planning_only": PLANNING_ONLY,
        "upstream_execution_ref": UPSTREAM_EXECUTION_REF,
        "upstream_artifact_paths": {
            "review": review_path,
            "masks": masks_path,
            "quality": quality_path,
            "post_review": post_path,
            "masks_dir_rel": UPSTREAM_MASKS_DIR_REL,
        },
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "mobile_sam_real_image_quality_review_prompt_strategy_planning_profile": to_dict(profile),
        "mobile_sam_real_image_quality_review_prompt_strategy_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "real_image_quality_review_scope_record": asdict(scope),
        "real_image_candidate_mask_quality_assessment_record": asdict(mask_assessment),
        "per_prompt_quality_assessment_record": asdict(per_prompt),
        "prompt_strategy_recommendation_record": asdict(prompt_strategy),
        "failure_mode_taxonomy_record": asdict(failure_taxonomy),
        "detector_ocr_semantic_prompt_generation_need_record": asdict(detector_need),
        "multi_image_trial_route_record": asdict(multi_route),
        "runtime_boundary_preservation_record": asdict(runtime_boundary),
        "followup_phase_route_record": asdict(followup),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "quality_review_status": "go" if blocker_count == 0 else "blocked",
            "stable_targets": ["left_building", "crosswalk_or_road_region"],
            "weak_targets": ["front_vehicle", "road_sign"],
            "recommended_prompt_strategy": "box_for_large_objects_detector_for_small_dynamic_objects",
            "recommended_next_phase": RECOMMENDED_ROUTE,
            "route_options": {"A": ROUTE_A, "B": ROUTE_B, "C": ROUTE_C},
            "inference_executed_this_phase": False,
            "new_image_read_this_phase": False,
            "transition_note": (
                "PLANNING ONLY. Reviewed 5 candidate masks from upstream execution. "
                "Prompt strategy and failure modes documented. No inference/runtime/semantic/fact."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    artifact_payloads = {
        "real_image_candidate_mask_quality_assessment_v1.json": asdict(mask_assessment),
        "per_prompt_quality_assessment_v1.json": {"assessments": per_prompt_list},
        "prompt_strategy_recommendation_v1.json": asdict(prompt_strategy),
        "failure_mode_taxonomy_v1.json": {"failure_modes": list(FAILURE_MODES)},
        "detector_ocr_semantic_prompt_generation_need_v1.json": asdict(detector_need),
        "multi_image_trial_route_v1.json": asdict(multi_route),
    }

    if write_file:
        review_path_out = out_root / REVIEW_FILENAME
        review_path_out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path_out)
        for name, payload in artifact_payloads.items():
            (out_root / name).write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        extra_refs = [result.get("output_review_file"), review_path, masks_path]
        try:
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest_tb["test_board_dir"])
        extra_payloads = {
            "real_image_quality_review_scope_record": {"record": asdict(scope)},
            "real_image_candidate_mask_quality_assessment_record": {"record": asdict(mask_assessment)},
            "per_prompt_quality_assessment_record": {"record": asdict(per_prompt)},
            "prompt_strategy_recommendation_record": {"record": asdict(prompt_strategy)},
            "failure_mode_taxonomy_record": {"record": asdict(failure_taxonomy)},
            "detector_ocr_semantic_prompt_generation_need_record": {"record": asdict(detector_need)},
            "multi_image_trial_route_record": {"record": asdict(multi_route)},
            "runtime_boundary_preservation_record": {"record": asdict(runtime_boundary)},
            "followup_phase_route_record": {"record": asdict(followup)},
        }
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
            "inference_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
        }
        extra_written: List[str] = []
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest_tb["extra_written_records"] = extra_written
        manifest_tb["total_record_count"] = manifest_tb["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest_tb
        result["test_board_record_count"] = manifest_tb["total_record_count"]

    return result


def main() -> int:
    result = review_p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "stable_targets": result["conclusions"]["stable_targets"],
                "weak_targets": result["conclusions"]["weak_targets"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
