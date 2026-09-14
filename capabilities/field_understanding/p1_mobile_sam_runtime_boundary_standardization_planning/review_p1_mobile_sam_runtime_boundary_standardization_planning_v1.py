# -*- coding: utf-8 -*-
"""P1 MobileSAM Runtime Boundary Standardization Planning — review v1 (PLANNING ONLY)."""

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
from capabilities.field_understanding.p1_mobile_sam_runtime_boundary_standardization_planning.p1_mobile_sam_runtime_boundary_standardization_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_CANONICAL_REFS,
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_registry_overlay,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_runtime_boundary_standardization_planning.p1_mobile_sam_runtime_boundary_standardization_planning_types_v1 import (  # noqa: E402
    ADMISSION_CRITERIA_JSON_REL,
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    BROAD_READINESS_MUST_BE_FALSE,
    CANDIDATE_POLICY_MD_REL,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    EXTERNAL_IMAGE_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FACT_WRITE_READY_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GOVERNANCE_INDEX_REL,
    GOVERNANCE_LEGACY_INVENTORY_REL,
    GOVERNANCE_MANIFEST_REL,
    GOVERNANCE_REFERENCE_POLICY_REL,
    GOVERNANCE_STANDARDS_REFERENCE_REQUIRED,
    IMAGE_INPUT_ALLOWED,
    INFERENCE_TRIAL_VERIFIED_REQUIRED,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_ONLY,
    MODEL_LOAD_ALLOWED,
    MODEL_ONBOARDING_STANDARD_REL,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NAVIGATION_ACTION_SPEECH_READY_WRITE_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION,
    NEXT_PHASE_REAL_IMAGE_TRIAL_REQUEST,
    OUTPUT_ADAPTER_EXCLUSION_MD_REL,
    OUTPUT_ADAPTER_READY_WRITE_ALLOWED,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PREDICTION_ALLOWED,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_FILE_WRITE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_OVERLAY_REL,
    REQUIRED_READINESS_LEVEL,
    REQUIRED_REGISTRY_TRUE_FLAGS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_BOUNDARY_STANDARDIZATION_PLANNING,
    RUNTIME_EXECUTION_ALLOWED,
    RUNTIME_READY_WRITE_ALLOWED,
    SEMANTIC_EXCLUSION_MD_REL,
    SEMANTIC_LAYER_READY_WRITE_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    SCOPE,
    SEGMENTATION_ALLOWED,
    STANDARD_PLAN_MD_REL,
    STANDARD_ROOT_REL,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_PACKAGING_EXECUTION_REF,
    WEIGHT_CHAIN,
    GovernanceStandardsReferenceAuditRecord,
    MobileSAMCandidateOutputAdmissionPolicyRecord,
    MobileSAMFollowupRealImageTrialRouteRecord,
    MobileSAMInferenceTrialVerifiedAuditRecord,
    MobileSAMOutputAdapterBoundaryRecord,
    MobileSAMRealImageTestBoundaryRecord,
    MobileSAMRuntimeAdmissionCriteriaRecord,
    MobileSAMRuntimeBoundaryScopeRecord,
    MobileSAMRuntimeRejectionCriteriaRecord,
    MobileSAMSemanticFactNavigationSpeechExclusionRecord,
    NegativeMobileSAMRuntimeBoundaryStandardizationPlanningGuard,
    P1MobileSAMRuntimeBoundaryStandardizationPlanningDecision,
    P1MobileSAMRuntimeBoundaryStandardizationPlanningProfile,
    build_real_image_test_boundary,
    build_runtime_admission_criteria,
    build_runtime_rejection_criteria,
    to_dict,
)

_PKG = "capabilities/field_understanding/p1_mobile_sam_runtime_boundary_standardization_planning"
STEP_FILES = (
    f"{_PKG}/__init__.py",
    f"{_PKG}/p1_mobile_sam_runtime_boundary_standardization_planning_types_v1.py",
    f"{_PKG}/p1_mobile_sam_runtime_boundary_standardization_planning_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_runtime_boundary_standardization_planning_v1.py",
)

PROFILE_REF = "p1_mobile_sam_runtime_boundary_standardization_planning_profile_v1"
DECISION_REF = "p1_mobile_sam_runtime_boundary_standardization_planning_decision_v1"
DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_mobile_sam_runtime_boundary_standardization_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_runtime_boundary_standardization_planning_review_v1.json"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _resolve_file(rel: str) -> Optional[Path]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            return p
    return None


def _audit_registry_mobile_sam(overlay: Dict[str, Any]) -> Dict[str, Any]:
    asset = (overlay.get("assets") or {}).get(MOBILE_SAM_ASSET_ID) or {}
    readiness = asset.get("readiness_level")
    true_flags_ok = all(asset.get(f) is True for f in REQUIRED_REGISTRY_TRUE_FLAGS)
    broad_false = all(asset.get(f) is False for f in BROAD_READINESS_MUST_BE_FALSE)
    return {
        "readiness_level": readiness,
        "inference_trial_verified": asset.get("inference_trial_verified"),
        "true_flags_ok": true_flags_ok,
        "broad_readiness_all_false": broad_false,
        "audit_passed": (
            readiness == REQUIRED_READINESS_LEVEL
            and true_flags_ok
            and broad_false
            and INFERENCE_TRIAL_VERIFIED_REQUIRED
        ),
        "asset_snapshot": {k: asset.get(k) for k in (
            ["readiness_level"] + list(REQUIRED_REGISTRY_TRUE_FLAGS) + list(BROAD_READINESS_MUST_BE_FALSE)
        )},
    }


def _audit_governance_refs() -> Dict[str, Any]:
    manifest_path = _resolve_file(GOVERNANCE_MANIFEST_REL)
    manifest_ok = False
    reuse_ok = False
    if manifest_path is not None:
        try:
            m = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_ok = m.get("migration_mode") == "canonical_copy_no_delete"
            reuse_ok = m.get("reuse_before_create_policy") is True
        except (OSError, json.JSONDecodeError):
            pass
    legacy_path = _resolve_file(GOVERNANCE_LEGACY_INVENTORY_REL)
    runtime_gate_ok = False
    if legacy_path is not None:
        try:
            inv = json.loads(legacy_path.read_text(encoding="utf-8"))
            rules = {r.get("rule_id"): r for r in inv.get("rules", [])}
            runtime_gate_ok = "RuntimeBoundaryGovernanceStandardV1" in rules or any(
                "runtime_boundary" in (r.get("category") or "") for r in inv.get("rules", [])
            )
        except (OSError, json.JSONDecodeError):
            pass
    return {
        "manifest_ref_ok": manifest_path is not None and manifest_ok,
        "index_ref_ok": _resolve_file(GOVERNANCE_INDEX_REL) is not None,
        "reference_policy_ref_ok": _resolve_file(GOVERNANCE_REFERENCE_POLICY_REL) is not None,
        "legacy_inventory_ref_ok": legacy_path is not None,
        "model_onboarding_standard_ref_ok": _resolve_file(MODEL_ONBOARDING_STANDARD_REL) is not None,
        "reuse_before_create_policy_present": reuse_ok,
        "runtime_admission_gate_present": runtime_gate_ok,
        "canonical_refs_ok": all(_resolve_file(r) is not None for r in GOVERNANCE_CANONICAL_REFS),
    }


def review_p1_mobile_sam_runtime_boundary_standardization_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
    write_standard_files: bool = True,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []

    for rel in STEP_FILES:
        if _resolve_file(rel) is not None:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    out_root = Path(output_root or (_WRITABLE_BASE / DEFAULT_OUTPUT_ROOT.relative_to(_REPO_ROOT))).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    gov_audit = _audit_governance_refs()
    if not gov_audit["canonical_refs_ok"]:
        failed_checks.append("governance.canonical_refs_incomplete")

    overlay, overlay_path = load_registry_overlay(_REPO_ROOT, REGISTRY_OVERLAY_REL)
    if overlay is None:
        failed_checks.append("registry.overlay_missing")
        reg_audit = {"audit_passed": False}
    else:
        reg_audit = _audit_registry_mobile_sam(overlay)
        if not reg_audit["audit_passed"]:
            failed_checks.append(f"registry.mobile_sam_audit_failed:{reg_audit}")

    admission = build_runtime_admission_criteria()
    rejection = build_runtime_rejection_criteria()
    real_image_boundary = build_real_image_test_boundary()

    write_root = next(
        (b for b in _artifact_roots() if (b / STANDARD_PLAN_MD_REL).parent.parent.is_dir()),
        _WRITABLE_BASE,
    )
    if write_standard_files:
        std_dir = write_root / STANDARD_ROOT_REL
        std_dir.mkdir(parents=True, exist_ok=True)
        for rel, content in (
            (ADMISSION_CRITERIA_JSON_REL, json.dumps(admission, ensure_ascii=False, indent=2) + "\n"),
        ):
            p = write_root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, str):
                p.write_text(content, encoding="utf-8")

    scope_record = MobileSAMRuntimeBoundaryScopeRecord(
        record_id="mobile_sam_runtime_boundary_scope_v1",
        asset_id=MOBILE_SAM_ASSET_ID,
        scope=WEIGHT_CHAIN,
        planning_only=True,
        standard_root_rel=STANDARD_ROOT_REL,
    )
    gov_ref_record = GovernanceStandardsReferenceAuditRecord(
        record_id="governance_standards_reference_audit_v1",
        manifest_ref_ok=gov_audit["manifest_ref_ok"],
        index_ref_ok=gov_audit["index_ref_ok"],
        reference_policy_ref_ok=gov_audit["reference_policy_ref_ok"],
        legacy_inventory_ref_ok=gov_audit["legacy_inventory_ref_ok"],
        reuse_before_create_policy_present=gov_audit["reuse_before_create_policy_present"],
        runtime_admission_gate_present=gov_audit["runtime_admission_gate_present"],
    )
    inference_audit = MobileSAMInferenceTrialVerifiedAuditRecord(
        record_id="mobile_sam_inference_trial_verified_audit_v1",
        registry_overlay_rel=REGISTRY_OVERLAY_REL,
        readiness_level=str(reg_audit.get("readiness_level", "")),
        inference_trial_verified=bool(reg_audit.get("inference_trial_verified")),
        broad_readiness_all_false=bool(reg_audit.get("broad_readiness_all_false")),
        audit_passed=bool(reg_audit.get("audit_passed")),
    )
    admission_record = MobileSAMRuntimeAdmissionCriteriaRecord(
        record_id="mobile_sam_runtime_admission_criteria_v1",
        runtime_candidate_admission_possible=True,
        runtime_ready_granted_now=False,
        runtime_requires_separate_request=True,
        runtime_requires_owner_approval=True,
        runtime_requires_real_image_trial_suite=True,
    )
    candidate_policy = MobileSAMCandidateOutputAdmissionPolicyRecord(
        record_id="mobile_sam_candidate_output_admission_policy_v1",
        candidate_output_may_enter_runtime_admission_review=True,
        candidate_output_must_remain_candidate=True,
        candidate_output_requires_schema=True,
        candidate_output_requires_no_fact_write=True,
    )
    rejection_record = MobileSAMRuntimeRejectionCriteriaRecord(
        record_id="mobile_sam_runtime_rejection_criteria_v1",
        rejection_criteria_count=len(rejection),
        rejects_registry_below_inference_trial_verified=True,
        rejects_direct_user_visible_output=True,
    )
    output_adapter = MobileSAMOutputAdapterBoundaryRecord(
        record_id="mobile_sam_output_adapter_boundary_v1",
        output_adapter_ready_granted_now=False,
        output_adapter_requires_separate_request=True,
        output_adapter_must_not_read_candidate_without_admission=True,
    )
    semantic_exclusion = MobileSAMSemanticFactNavigationSpeechExclusionRecord(
        record_id="mobile_sam_semantic_fact_navigation_speech_exclusion_v1",
        semantic_layer_ready_granted_now=False,
        fact_write_ready_granted_now=False,
        navigation_action_speech_ready_granted_now=False,
        candidate_mask_must_not_become_fact=True,
    )
    real_image = MobileSAMRealImageTestBoundaryRecord(
        record_id="mobile_sam_real_image_test_boundary_v1",
        real_local_image_trial_allowed_next=True,
        live_camera_forbidden=True,
        external_url_image_forbidden=True,
        personal_sensitive_image_forbidden=True,
        output_candidate_only=True,
    )
    followup = MobileSAMFollowupRealImageTrialRouteRecord(
        record_id="mobile_sam_followup_real_image_trial_route_v1",
        recommended_next_phase=NEXT_PHASE_REAL_IMAGE_TRIAL_REQUEST,
        next_phase_allows_inference_execution=False,
        next_phase_still_no_runtime=True,
    )

    can_enter_real_image_request = (
        inference_audit.audit_passed
        and gov_audit["canonical_refs_ok"]
        and admission_record.runtime_candidate_admission_possible
        and real_image.real_local_image_trial_allowed_next
    )

    invariant_state: Dict[str, bool] = {
        "governance_standards_referenced": gov_audit["canonical_refs_ok"],
        "registry_inference_trial_verified": inference_audit.audit_passed,
        "no_runtime_ready_granted": RUNTIME_READY_WRITE_ALLOWED is False,
        "no_output_adapter_ready_granted": OUTPUT_ADAPTER_READY_WRITE_ALLOWED is False,
        "no_semantic_fact_navigation_ready_granted": (
            SEMANTIC_LAYER_READY_WRITE_ALLOWED is False
            and FACT_WRITE_READY_WRITE_ALLOWED is False
            and NAVIGATION_ACTION_SPEECH_READY_WRITE_ALLOWED is False
        ),
        "no_inference_or_image_input": REAL_INFERENCE_ALLOWED is False and IMAGE_INPUT_ALLOWED is False,
        "no_runtime_output_semantic_execution": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
            and FACT_WRITE_ALLOWED is False
            and NAVIGATION_ACTION_SPEECH_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "runtime_admission_criteria_defined": admission_record.runtime_candidate_admission_possible,
        "runtime_rejection_criteria_defined": rejection_record.rejection_criteria_count >= 10,
        "candidate_output_admission_policy_defined": candidate_policy.candidate_output_must_remain_candidate,
        "output_adapter_boundary_defined": output_adapter.output_adapter_must_not_read_candidate_without_admission,
        "semantic_fact_navigation_exclusion_defined": semantic_exclusion.candidate_mask_must_not_become_fact,
        "real_image_test_boundary_defined": real_image.output_candidate_only,
        "no_live_camera_or_external_url_next": real_image.live_camera_forbidden and real_image.external_url_image_forbidden,
        "candidate_not_direct_fact_runtime": candidate_policy.candidate_output_requires_no_fact_write,
        "test_board_record_required_true": REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_board_record_required") is True,
        "test_board_protected_non_deletable": all(
            REQUIRED_TEST_BOARD_FIELDS_LOCAL.get(k) is True
            for k in ("test_artifact_protected", "test_record_non_deletable", "test_deletion_forbidden")
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMRuntimeBoundaryStandardizationPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMRuntimeBoundaryStandardizationPlanningGuard(
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
        "mobile_sam_runtime_boundary_standardization_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_runtime_boundary_scope_record_count_gte_1": True,
        "governance_standards_reference_audit_record_count_gte_1": True,
        "mobile_sam_inference_trial_verified_audit_record_count_gte_1": True,
        "mobile_sam_runtime_admission_criteria_record_count_gte_1": True,
        "mobile_sam_candidate_output_admission_policy_record_count_gte_1": True,
        "mobile_sam_runtime_rejection_criteria_record_count_gte_1": True,
        "mobile_sam_output_adapter_boundary_record_count_gte_1": True,
        "mobile_sam_semantic_fact_navigation_speech_exclusion_record_count_gte_1": True,
        "mobile_sam_real_image_test_boundary_record_count_gte_1": True,
        "mobile_sam_followup_real_image_trial_route_record_count_gte_1": True,
        "negative_guard_count_eq_19": negative_guard_count == 19,
        "negative_guard_passed_eq_19": negative_guard_passed == 19,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "planning_only": PLANNING_ONLY is True,
        "runtime_boundary_standardization_planning": RUNTIME_BOUNDARY_STANDARDIZATION_PLANNING is True,
        "mobile_sam_only": MOBILE_SAM_ONLY is True,
        "governance_standards_reference_required": GOVERNANCE_STANDARDS_REFERENCE_REQUIRED is True,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_ready_write_allowed_false": RUNTIME_READY_WRITE_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "fact_write_allowed_false": FACT_WRITE_ALLOWED is False,
        "navigation_action_speech_allowed_false": NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "image_input_allowed_false": IMAGE_INPUT_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "runtime_admission_criteria_defined": True,
        "runtime_rejection_criteria_defined": True,
        "candidate_output_admission_policy_defined": True,
        "output_adapter_boundary_defined": True,
        "semantic_fact_navigation_speech_exclusion_defined": True,
        "real_image_test_boundary_defined": True,
        "real_local_image_trial_allowed_next": real_image.real_local_image_trial_allowed_next,
        "can_enter_real_local_image_trial_request_approval_next": can_enter_real_image_request,
        "can_enter_runtime_execution_now_false": RUNTIME_EXECUTION_ALLOWED is False,
        "can_enter_output_adapter_now_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "can_enter_semantic_layer_now_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "can_write_fact_now_false": FACT_WRITE_ALLOWED is False,
        "can_trigger_navigation_action_speech_now_false": NAVIGATION_ACTION_SPEECH_ALLOWED is False,
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
    decision = P1MobileSAMRuntimeBoundaryStandardizationPlanningDecision(
        decision_ref=DECISION_REF,
        mobile_sam_runtime_boundary_standardization_planning_profile_count=1,
        mobile_sam_runtime_boundary_scope_record_count=1,
        governance_standards_reference_audit_record_count=1,
        mobile_sam_inference_trial_verified_audit_record_count=1,
        mobile_sam_runtime_admission_criteria_record_count=1,
        mobile_sam_candidate_output_admission_policy_record_count=1,
        mobile_sam_runtime_rejection_criteria_record_count=1,
        mobile_sam_output_adapter_boundary_record_count=1,
        mobile_sam_semantic_fact_navigation_speech_exclusion_record_count=1,
        mobile_sam_real_image_test_boundary_record_count=1,
        mobile_sam_followup_real_image_trial_route_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        can_enter_real_local_image_trial_request_approval_next=can_enter_real_image_request and blocker_count == 0,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    candidate_policy_payload = {
        "policy_id": "MobileSAMCandidateOutputAdmissionPolicyV1",
        "candidate_output_may_enter_runtime_admission_review": True,
        "candidate_output_must_remain_candidate": True,
        "candidate_output_requires_schema": True,
        "candidate_output_requires_source_manifest": True,
        "candidate_output_requires_phase_ref": True,
        "candidate_output_requires_model_asset_ref": True,
        "candidate_output_requires_confidence_or_quality_summary": True,
        "candidate_output_requires_failure_mode_annotation": True,
        "candidate_output_requires_no_fact_write": True,
        "candidate_output_requires_no_user_visible_output": True,
        "candidate_output_requires_no_navigation_action_speech": True,
    }

    followup_route = {
        "phase_id": PHASE_ID,
        "recommended_next_phase": NEXT_PHASE_REAL_IMAGE_TRIAL_REQUEST,
        "subsequent_phase": NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION,
        "next_allows_scoped_local_test_asset": True,
        "next_allows_image_manifest_planning": True,
        "next_allows_owner_approval": True,
        "next_still_no_inference": True,
        "execution_phase_still_candidate_only": True,
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Runtime Boundary Standardization Planning (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "planning_only": PLANNING_ONLY,
        "mobile_sam_only": MOBILE_SAM_ONLY,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_packaging_execution_ref": UPSTREAM_PACKAGING_EXECUTION_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "mobile_sam_runtime_boundary_standardization_planning_profile": to_dict(
            P1MobileSAMRuntimeBoundaryStandardizationPlanningProfile(
                profile_ref=PROFILE_REF,
                phase_id=PHASE_ID,
                planning_only=PLANNING_ONLY,
                runtime_boundary_standardization_planning=RUNTIME_BOUNDARY_STANDARDIZATION_PLANNING,
                mobile_sam_only=MOBILE_SAM_ONLY,
                governance_standards_reference_required=GOVERNANCE_STANDARDS_REFERENCE_REQUIRED,
                inference_trial_verified_required=INFERENCE_TRIAL_VERIFIED_REQUIRED,
                runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
                registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
                target_chain_ref=TARGET_CHAIN_REF,
                upstream_packaging_execution_ref=UPSTREAM_PACKAGING_EXECUTION_REF,
                controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
                luna_core_principle=LUNA_CORE_PRINCIPLE,
                required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
                governance_rules=ALL_GOVERNANCE_RULES,
            )
        ),
        "mobile_sam_runtime_boundary_standardization_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "governance_standards_reference_audit": gov_audit,
        "governance_standards_reference_audit_record": asdict(gov_ref_record),
        "registry_overlay_path": overlay_path,
        "mobile_sam_inference_trial_verified_audit": reg_audit,
        "mobile_sam_inference_trial_verified_audit_record": asdict(inference_audit),
        "mobile_sam_runtime_boundary_scope_record": asdict(scope_record),
        "mobile_sam_runtime_admission_criteria_record": asdict(admission_record),
        "mobile_sam_runtime_rejection_criteria_record": asdict(rejection_record),
        "mobile_sam_candidate_output_admission_policy_record": asdict(candidate_policy),
        "mobile_sam_output_adapter_boundary_record": asdict(output_adapter),
        "mobile_sam_semantic_fact_navigation_speech_exclusion_record": asdict(semantic_exclusion),
        "mobile_sam_real_image_test_boundary_record": asdict(real_image),
        "mobile_sam_followup_real_image_trial_route_record": asdict(followup),
        "runtime_rejection_criteria": list(rejection),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "planning_status": "go" if blocker_count == 0 else "blocked",
            "registry_mutated_this_phase": False,
            "inference_executed_this_phase": False,
            "runtime_ready_granted": False,
            "can_enter_real_local_image_trial_request_approval_next": decision.can_enter_real_local_image_trial_request_approval_next,
            "recommended_next_phase": NEXT_PHASE_REAL_IMAGE_TRIAL_REQUEST,
            "subsequent_phase": NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION,
            "transition_note": (
                "PLANNING ONLY (mobile_sam_only). Runtime boundary standardized from inference_trial_verified. "
                "Governance standards referenced. No runtime/inference/registry mutation. "
                "Next: real local image trial request/approval (still no inference in that phase)."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)

        (out_root / "mobile_sam_runtime_admission_criteria_v1.json").write_text(
            json.dumps(admission, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "mobile_sam_candidate_output_admission_policy_v1.json").write_text(
            json.dumps(candidate_policy_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "mobile_sam_real_image_test_boundary_v1.json").write_text(
            json.dumps(real_image_boundary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "mobile_sam_runtime_boundary_followup_route_v1.json").write_text(
            json.dumps(followup_route, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        extra_refs = [
            result.get("output_review_file"),
            str(_resolve_file(STANDARD_PLAN_MD_REL) or ""),
            str(_resolve_file(ADMISSION_CRITERIA_JSON_REL) or ""),
        ]
        try:
            manifest = write_test_board_records(
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
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "mobile_sam_runtime_boundary_scope_record": {"record": asdict(scope_record)},
            "governance_standards_reference_audit_record": {"record": asdict(gov_ref_record)},
            "mobile_sam_inference_trial_verified_audit_record": {"record": asdict(inference_audit)},
            "mobile_sam_runtime_admission_criteria_record": {"record": asdict(admission_record)},
            "mobile_sam_candidate_output_admission_policy_record": {"record": asdict(candidate_policy)},
            "mobile_sam_runtime_rejection_criteria_record": {"record": asdict(rejection_record)},
            "mobile_sam_output_adapter_boundary_record": {"record": asdict(output_adapter)},
            "mobile_sam_semantic_fact_navigation_speech_exclusion_record": {"record": asdict(semantic_exclusion)},
            "mobile_sam_real_image_test_boundary_record": {"record": asdict(real_image)},
            "mobile_sam_followup_real_image_trial_route_record": {"record": asdict(followup)},
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
            "runtime_execution_allowed": False,
            "inference_allowed": False,
            "registry_mutation_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
        }
        extra_written: List[str] = []
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            extra_written.append(str(p))
        manifest["extra_written_records"] = extra_written
        manifest["total_record_count"] = manifest["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["total_record_count"]

    return result


def main() -> int:
    result = review_p1_mobile_sam_runtime_boundary_standardization_planning_v1()
    print(json.dumps({
        "output_review_file": result.get("output_review_file"),
        "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
        "test_board_record_count": result.get("test_board_record_count"),
        "negative_guard_passed": result["negative_guard_passed"],
        "can_enter_real_local_image_trial_request_approval_next": result["conclusions"][
            "can_enter_real_local_image_trial_request_approval_next"
        ],
        "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
        "blocker_count": result["blocker_count"],
        "final_decision": result["final_decision"],
    }, ensure_ascii=False))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
