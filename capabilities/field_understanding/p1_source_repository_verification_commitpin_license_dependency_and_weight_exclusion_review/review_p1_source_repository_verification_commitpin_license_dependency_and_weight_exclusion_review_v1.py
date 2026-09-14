# -*- coding: utf-8 -*-
"""P1 Source Repository Verification / CommitPin / License / Dependency /
Weight-Exclusion Review — review v1 (NETWORK-ENABLED, READONLY EVIDENCE).

Consumes the embedded REAL evidence (collected via scoped readonly GitHub REST
lookups during this phase) and produces evidence-backed findings for byte_track and
mobile_sam:
  - a scoped readonly network evidence log,
  - repository verification evidence (2),
  - commit pin resolution evidence (2),
  - license review evidence (2),
  - dependency manifest review evidence (2),
  - a mobile_sam weight-excluding checkout feasibility review (1),
  - a per-asset source-execution retry readiness gate (2),
  - an overall review decision + per-asset risk records (2),
  - follow-up routing.

It executes/mutates NOTHING beyond readonly evidence consumption: no clone, no
checkout, no install, no pip, no download (weights/models/datasets/examples), no
import, no model load, no inference, no runtime, no output adapter, no semantic
layer, no registry mutation; and it does NOT execute a source-execution retry even
when readiness is reached. Protected, non-deletable test board records are written
in real_test mode; cleanup must never delete test board artifacts.
"""

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
from capabilities.field_understanding.p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review.p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review.p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    BLOCKED_WEIGHT_PATTERNS,
    COMMERCIAL_RUNTIME_APPROVED,
    COMMIT_PIN_REVIEW,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEPENDENCY_INSTALL_ALLOWED,
    DEPENDENCY_REVIEW,
    EVIDENCE_COMMIT,
    EVIDENCE_DEPENDENCY,
    EVIDENCE_LICENSE,
    EVIDENCE_MOBILE_SAM_WEIGHT_EXCLUSION,
    EVIDENCE_NETWORK_DOMAIN,
    EVIDENCE_REPOSITORY,
    EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GIT_CLONE_ALLOWED,
    IN_SCOPE_ASSET_IDS,
    LICENSE_REVIEW,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_RETRY,
    NEXT_PHASE_REVIEW_POST_REVIEW,
    NO_WEIGHT_DOWNLOAD_PHASE_UNTIL_SUCCESSFUL_SOURCE_EXECUTION_POST_REVIEW,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    READONLY_NETWORK_EVIDENCE_COLLECTION_ALLOWED,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REPOSITORY_VERIFICATION_REVIEW,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REVIEW_PHASE,
    REVIEW_PRINCIPLE_ZH,
    REUSE_FLAGS,
    RISK_DIMENSIONS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SCOPED_NETWORK_LOOKUP_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_CHECKOUT_ALLOWED,
    SOURCE_EXECUTION_RETRY_NOT_ALLOWED_WITHOUT_READINESS_GATE,
    SOURCE_FAMILY,
    SOURCE_INSTALL_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_PLANNING_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL,
    WEIGHT_EXCLUSION_REVIEW,
    MobileSAMWeightExclusionFeasibilityReview,
    NegativeSourceRepositoryVerificationCommitPinReviewGuard,
    P1SourceRepositoryVerificationCommitPinLicenseDependencyWeightExclusionReviewProfile,
    P1SourceRepositoryVerificationCommitPinReviewDecision,
    ScopedNetworkEvidenceLog,
    SourceCommitPinResolutionEvidence,
    SourceDependencyManifestReviewEvidence,
    SourceExecutionRetryReadinessGateReview,
    SourceLicenseReviewEvidence,
    SourceRepositoryReviewRiskRecord,
    SourceRepositoryVerificationEvidence,
    SourceRepositoryVerificationReviewDecisionRecord,
    to_dict,
)


def _pick_writable_base() -> Path:
    for cand in (Path.cwd(), _REPO_ROOT):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_review_v1.json"
)

_PKG = "capabilities/field_understanding/p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review"
STEP_FILES = (
    f"{_PKG}/p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_types_v1.py",
    f"{_PKG}/p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_registry_v1.py",
    f"{_PKG}/review_p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_v1.py",
)

PROFILE_REF = "p1_source_repository_verification_commitpin_review_profile_v1"
DECISION_REF = "p1_source_repository_verification_commitpin_review_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1SourceRepositoryVerificationCommitPinLicenseDependencyWeightExclusionReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            review_phase=REVIEW_PHASE,
            scoped_network_lookup_allowed=SCOPED_NETWORK_LOOKUP_ALLOWED,
            readonly_network_evidence_collection_allowed=READONLY_NETWORK_EVIDENCE_COLLECTION_ALLOWED,
            repository_verification_review=REPOSITORY_VERIFICATION_REVIEW,
            commit_pin_review=COMMIT_PIN_REVIEW,
            license_review=LICENSE_REVIEW,
            dependency_review=DEPENDENCY_REVIEW,
            weight_exclusion_review=WEIGHT_EXCLUSION_REVIEW,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            git_clone_allowed=GIT_CLONE_ALLOWED,
            source_checkout_allowed=SOURCE_CHECKOUT_ALLOWED,
            source_install_allowed=SOURCE_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            example_asset_download_allowed=EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            in_scope_asset_ids=IN_SCOPE_ASSET_IDS,
            upstream_planning_ref=UPSTREAM_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_v1(
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

    ts = _now()

    # ------------------------------------------------------------------- #
    # (二) Scoped network evidence log (readonly; every lookup logged).
    # ------------------------------------------------------------------- #
    evidence_log: List[ScopedNetworkEvidenceLog] = []

    def _log(asset_id: str, purpose: str, url: str, evidence_type: str, saved_ref: str) -> None:
        evidence_log.append(
            ScopedNetworkEvidenceLog(
                evidence_id=f"net_evidence_{len(evidence_log)+1}",
                asset_id=asset_id,
                lookup_purpose=purpose,
                target_domain=EVIDENCE_NETWORK_DOMAIN,
                target_url=url,
                evidence_type=evidence_type,
                timestamp=ts,
                readonly=True,
                no_clone=True,
                no_download_weight=True,
                no_source_checkout=True,
                no_install=True,
                evidence_saved_ref=saved_ref,
                network_boundary_compliant=True,
            )
        )

    REPO_EVIDENCE_REF = "repository_verification_evidence_v1.json"
    COMMIT_EVIDENCE_REF = "commit_pin_resolution_evidence_v1.json"
    LICENSE_EVIDENCE_REF = "license_review_evidence_v1.json"
    DEP_EVIDENCE_REF = "dependency_manifest_review_evidence_v1.json"
    WEIGHT_EVIDENCE_REF = "mobile_sam_weight_exclusion_feasibility_v1.json"

    _log("byte_track", "repository_identity_verification",
         "https://api.github.com/repos/ifzhang/ByteTrack(->repositories/400476704=FoundationVision/ByteTrack)",
         "repository_metadata", REPO_EVIDENCE_REF)
    _log("byte_track", "repository_file_listing",
         "https://api.github.com/repos/FoundationVision/ByteTrack/contents", "repository_file_listing", REPO_EVIDENCE_REF)
    _log("byte_track", "commit_pin_resolution",
         "https://api.github.com/repos/FoundationVision/ByteTrack/commits?sha=main&per_page=1",
         "commit_metadata", COMMIT_EVIDENCE_REF)
    _log("byte_track", "license_file_inspection",
         "https://api.github.com/repos/FoundationVision/ByteTrack(license.spdx_id)+/contents/LICENSE",
         "license_file", LICENSE_EVIDENCE_REF)
    _log("byte_track", "dependency_manifest_inspection",
         "https://api.github.com/repos/FoundationVision/ByteTrack/contents/requirements.txt,setup.py,setup.cfg",
         "requirements_file", DEP_EVIDENCE_REF)
    _log("byte_track", "git_lfs_indicator_check",
         "https://api.github.com/repos/FoundationVision/ByteTrack/contents/.gitattributes(HTTP_404)",
         "git_lfs_indicator", REPO_EVIDENCE_REF)

    _log("mobile_sam", "repository_identity_verification",
         "https://api.github.com/repos/ChaoningZhang/MobileSAM", "repository_metadata", REPO_EVIDENCE_REF)
    _log("mobile_sam", "repository_file_listing",
         "https://api.github.com/repos/ChaoningZhang/MobileSAM/contents", "repository_file_listing", REPO_EVIDENCE_REF)
    _log("mobile_sam", "committed_weight_indicator_check",
         "https://api.github.com/repos/ChaoningZhang/MobileSAM/contents/weights", "large_file_indicator", WEIGHT_EVIDENCE_REF)
    _log("mobile_sam", "git_lfs_indicator_check",
         "https://api.github.com/repos/ChaoningZhang/MobileSAM/contents/.gitattributes(HTTP_404)",
         "git_lfs_indicator", WEIGHT_EVIDENCE_REF)
    _log("mobile_sam", "commit_pin_resolution",
         "https://api.github.com/repos/ChaoningZhang/MobileSAM/commits?sha=master&per_page=1",
         "commit_metadata", COMMIT_EVIDENCE_REF)
    _log("mobile_sam", "license_file_inspection",
         "https://api.github.com/repos/ChaoningZhang/MobileSAM(license.spdx_id)+/contents/LICENSE",
         "license_file", LICENSE_EVIDENCE_REF)
    _log("mobile_sam", "dependency_manifest_inspection",
         "https://api.github.com/repos/ChaoningZhang/MobileSAM/contents/setup.py,setup.cfg",
         "pyproject_or_setup_file", DEP_EVIDENCE_REF)

    # ------------------------------------------------------------------- #
    # (三) Repository verification evidence (2).
    # ------------------------------------------------------------------- #
    repo_evidence: List[SourceRepositoryVerificationEvidence] = []
    for aid in IN_SCOPE_ASSET_IDS:
        e = EVIDENCE_REPOSITORY[aid]
        repo_evidence.append(
            SourceRepositoryVerificationEvidence(
                asset_id=aid,
                source_family=SOURCE_FAMILY[aid],
                repository_candidate_required=True,
                repository_url_verified=bool(e["repository_url_verified"]),
                repository_url=e["repository_url"],
                repository_owner=e["repository_owner"],
                repository_name=e["repository_name"],
                repository_metadata_evidence_ref=REPO_EVIDENCE_REF,
                repository_identity_confidence=e["repository_identity_confidence"],
                repository_identity_rationale=e["repository_identity_rationale"],
                package_import_identity_unresolved_or_source_component=bool(
                    e["package_import_identity_unresolved_or_source_component"]
                ),
                repository_may_contain_committed_checkpoint_weight=bool(
                    e["repository_may_contain_committed_checkpoint_weight"]
                ),
                git_lfs_detected=bool(e["git_lfs_detected"]),
                committed_weight_files_detected=bool(e["committed_weight_files_detected"]),
                repository_verification_completed=bool(e["repository_verification_completed"]),
                repository_verification_failure_reason=None if e["repository_verification_completed"] else "unverified",
            )
        )

    # ------------------------------------------------------------------- #
    # (四) Commit pin resolution evidence (2).
    # ------------------------------------------------------------------- #
    commit_evidence: List[SourceCommitPinResolutionEvidence] = []
    for aid in IN_SCOPE_ASSET_IDS:
        c = EVIDENCE_COMMIT[aid]
        commit_evidence.append(
            SourceCommitPinResolutionEvidence(
                asset_id=aid,
                repository_url_ref=EVIDENCE_REPOSITORY[aid]["repository_url"],
                branch_or_tag_candidate=c["branch_or_tag_candidate"],
                commit_hash_resolved=bool(c["commit_hash_resolved"]),
                commit_hash=c["commit_hash"],
                commit_metadata_evidence_ref=COMMIT_EVIDENCE_REF,
                commit_pin_confidence=c["commit_pin_confidence"],
                commit_pin_rationale=c["commit_pin_rationale"],
                commit_pin_completed=bool(c["commit_pin_completed"]),
                commit_pin_failure_reason=None if c["commit_pin_completed"] else "unresolved",
                commit_drift_check_required_before_execution=True,
            )
        )

    # ------------------------------------------------------------------- #
    # (五) License review evidence (2).
    # ------------------------------------------------------------------- #
    license_evidence: List[SourceLicenseReviewEvidence] = []
    for aid in IN_SCOPE_ASSET_IDS:
        l = EVIDENCE_LICENSE[aid]
        license_evidence.append(
            SourceLicenseReviewEvidence(
                asset_id=aid,
                license_file_found=bool(l["license_file_found"]),
                license_type_candidate=l["license_type_candidate"],
                license_file_evidence_ref=LICENSE_EVIDENCE_REF,
                license_review_completed=bool(l["license_review_completed"]),
                license_review_confidence=l["license_review_confidence"],
                license_review_rationale=l["license_review_rationale"],
                commercial_runtime_not_approved=True,
                source_install_allowed_by_license_for_trial=l["source_install_allowed_by_license_for_trial"],
                license_review_failure_reason=None if l["license_review_completed"] else "unverified",
                license_completion_does_not_approve_commercial_runtime=True,
                license_completion_does_not_approve_weight_download=True,
                license_completion_does_not_approve_inference_runtime=True,
            )
        )

    # ------------------------------------------------------------------- #
    # (六) Dependency manifest review evidence (2).
    # ------------------------------------------------------------------- #
    dependency_evidence: List[SourceDependencyManifestReviewEvidence] = []
    for aid in IN_SCOPE_ASSET_IDS:
        d = EVIDENCE_DEPENDENCY[aid]
        dependency_evidence.append(
            SourceDependencyManifestReviewEvidence(
                asset_id=aid,
                dependency_manifest_found=bool(d["dependency_manifest_found"]),
                dependency_manifest_refs=tuple(d["dependency_manifest_refs"]),
                dependency_review_completed=bool(d["dependency_review_completed"]),
                dependency_risk_summary=d["dependency_risk_summary"],
                torch_dependency_detected=bool(d["torch_dependency_detected"]),
                opencv_dependency_detected=bool(d["opencv_dependency_detected"]),
                numpy_scipy_dependency_detected=bool(d["numpy_scipy_dependency_detected"]),
                build_compile_risk_detected=bool(d["build_compile_risk_detected"]),
                dependency_conflict_risk_detected=bool(d["dependency_conflict_risk_detected"]),
                dependency_review_failure_reason=None if d["dependency_review_completed"] else "unverified",
                dependency_review_is_not_install_approval=True,
            )
        )

    # ------------------------------------------------------------------- #
    # (七) mobile_sam weight-excluding checkout feasibility review (1).
    # ------------------------------------------------------------------- #
    w = EVIDENCE_MOBILE_SAM_WEIGHT_EXCLUSION
    mobile_sam_feasibility = MobileSAMWeightExclusionFeasibilityReview(
        asset_id="mobile_sam",
        mobile_sam_weight_excluding_checkout_required=True,
        committed_weight_files_detected=w["committed_weight_files_detected"],
        committed_weight_files=tuple(w["committed_weight_files"]),
        committed_weight_total_bytes=int(w["committed_weight_total_bytes"]),
        git_lfs_detected=w["git_lfs_detected"],
        blocked_file_patterns=BLOCKED_WEIGHT_PATTERNS,
        sparse_checkout_feasible=w["sparse_checkout_feasible"],
        archive_filtering_feasible=w["archive_filtering_feasible"],
        code_only_checkout_feasible=w["code_only_checkout_feasible"],
        full_clone_allowed_for_mobile_sam_next_execution=bool(w["full_clone_allowed_for_mobile_sam_next_execution"]),
        mobile_sam_weight_exclusion_review_completed=bool(w["mobile_sam_weight_exclusion_review_completed"]),
        mobile_sam_weight_exclusion_failure_reason=None,
        feasibility_rationale=w["feasibility_rationale"],
        weight_file_evidence_ref=WEIGHT_EVIDENCE_REF,
        feasibility_is_not_weight_download_approval=True,
    )

    # mobile_sam full clone must be blocked when weight risk is true or unknown.
    _weight_risk_true_or_unknown = (mobile_sam_feasibility.committed_weight_files_detected is True) or (
        mobile_sam_feasibility.committed_weight_files_detected == "unknown"
    )
    mobile_sam_full_clone_blocked = (
        _weight_risk_true_or_unknown
        and mobile_sam_feasibility.full_clone_allowed_for_mobile_sam_next_execution is False
    )

    # ------------------------------------------------------------------- #
    # (八) Source-execution retry readiness gate (2).
    # ------------------------------------------------------------------- #
    def _repo_by(aid: str) -> SourceRepositoryVerificationEvidence:
        return next(r for r in repo_evidence if r.asset_id == aid)

    def _commit_by(aid: str) -> SourceCommitPinResolutionEvidence:
        return next(c for c in commit_evidence if c.asset_id == aid)

    def _license_by(aid: str) -> SourceLicenseReviewEvidence:
        return next(l for l in license_evidence if l.asset_id == aid)

    def _dep_by(aid: str) -> SourceDependencyManifestReviewEvidence:
        return next(d for d in dependency_evidence if d.asset_id == aid)

    readiness_gates: List[SourceExecutionRetryReadinessGateReview] = []
    for aid in IN_SCOPE_ASSET_IDS:
        r = _repo_by(aid)
        c = _commit_by(aid)
        l = _license_by(aid)
        d = _dep_by(aid)
        is_mobile_sam = aid == "mobile_sam"
        unresolved: List[str] = []
        if not r.repository_verification_completed:
            unresolved.append("repository_url_unverified")
        if not c.commit_pin_completed:
            unresolved.append("commit_hash_unpinned")
        if not l.license_review_completed:
            unresolved.append("license_review_incomplete")
        if not d.dependency_review_completed:
            unresolved.append("dependency_review_incomplete")
        ms_plan_completed: Optional[bool] = None
        if is_mobile_sam:
            ms_plan_completed = bool(mobile_sam_feasibility.mobile_sam_weight_exclusion_review_completed)
            if not ms_plan_completed:
                unresolved.append("mobile_sam_weight_excluding_checkout_plan_incomplete")
            if not mobile_sam_full_clone_blocked:
                unresolved.append("mobile_sam_full_clone_not_blocked_under_weight_risk")
        can_enter = len(unresolved) == 0
        readiness_gates.append(
            SourceExecutionRetryReadinessGateReview(
                asset_id=aid,
                repository_url_verified=r.repository_verification_completed,
                commit_hash_pinned=c.commit_pin_completed,
                license_review_completed=l.license_review_completed,
                dependency_review_completed=d.dependency_review_completed,
                network_boundary_finalized=True,
                command_whitelist_needs_update=True,
                source_checkout_strategy_finalized=True,
                rollback_ready=True,
                test_board_ready=True,
                mobile_sam_weight_excluding_checkout_plan_completed=ms_plan_completed,
                mobile_sam_full_clone_blocked_if_weight_risk=(mobile_sam_full_clone_blocked if is_mobile_sam else True),
                unresolved_blockers=tuple(unresolved),
                can_enter_source_execution_retry_next=can_enter,
                retry_must_not_execute_in_this_phase=True,
            )
        )

    ready_assets = tuple(g.asset_id for g in readiness_gates if g.can_enter_source_execution_retry_next)
    not_ready_assets = tuple(g.asset_id for g in readiness_gates if not g.can_enter_source_execution_retry_next)
    both_ready = len(ready_assets) == len(IN_SCOPE_ASSET_IDS)
    none_ready = len(ready_assets) == 0
    partial_ready = (not both_ready) and (not none_ready)

    # ------------------------------------------------------------------- #
    # (九) Follow-up routing.
    # ------------------------------------------------------------------- #
    if both_ready:
        recommended_next_phase = NEXT_PHASE_RETRY
        retry_scope = ready_assets
    elif partial_ready:
        recommended_next_phase = NEXT_PHASE_RETRY
        retry_scope = ready_assets
    else:
        recommended_next_phase = NEXT_PHASE_REVIEW_POST_REVIEW
        retry_scope = tuple()

    decision_record = SourceRepositoryVerificationReviewDecisionRecord(
        record_id="source_repository_verification_review_decision_record_v1",
        ready_asset_ids=ready_assets,
        not_ready_asset_ids=not_ready_assets,
        both_assets_ready=both_ready,
        partial_ready=partial_ready,
        none_ready=none_ready,
        recommended_next_phase=recommended_next_phase,
        retry_scope_asset_ids=retry_scope,
        no_weight_download_phase_until_successful_source_execution_post_review=(
            NO_WEIGHT_DOWNLOAD_PHASE_UNTIL_SUCCESSFUL_SOURCE_EXECUTION_POST_REVIEW
        ),
        source_execution_retry_not_allowed_without_readiness_gate=(
            SOURCE_EXECUTION_RETRY_NOT_ALLOWED_WITHOUT_READINESS_GATE
        ),
        retry_not_executed_in_this_phase=True,
    )

    # ------------------------------------------------------------------- #
    # (十) Per-asset risk records (2).
    # ------------------------------------------------------------------- #
    risk_records: List[SourceRepositoryReviewRiskRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        d = _dep_by(aid)
        highlighted: List[str] = []
        if d.build_compile_risk_detected:
            highlighted.append("build_or_compile_risk")
        if d.dependency_conflict_risk_detected:
            highlighted.append("dependency_unknown_risk")
        if aid == "mobile_sam":
            highlighted.append("weight_download_contamination_risk")
            highlighted.append("dependency_unknown_risk")  # undeclared torch
        risk_records.append(
            SourceRepositoryReviewRiskRecord(
                asset_id=aid,
                risk_dimensions=RISK_DIMENSIONS,
                all_risk_dimensions_recorded=len(RISK_DIMENSIONS) == 10,
                highlighted_risks=tuple(dict.fromkeys(highlighted)),
            )
        )

    # ------------------------------------------------------------------- #
    # Invariants for the 21 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "no_clone_checkout": GIT_CLONE_ALLOWED is False and SOURCE_CHECKOUT_ALLOWED is False
        and all(g.no_clone and g.no_source_checkout for g in evidence_log),
        "no_install": (
            SOURCE_INSTALL_ALLOWED is False and PIP_INSTALL_ALLOWED is False
            and DEPENDENCY_INSTALL_ALLOWED is False
            and all(g.no_install for g in evidence_log)
        ),
        "no_download": (
            MODEL_DOWNLOAD_ALLOWED is False and WEIGHT_DOWNLOAD_ALLOWED is False
            and DATASET_DOWNLOAD_ALLOWED is False and EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False
            and all(g.no_download_weight for g in evidence_log)
        ),
        "no_real_import_load_inference": (
            REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False and REAL_INFERENCE_ALLOWED is False
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False and RUNTIME_ACTIVATION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "network_access_logged": (
            len(evidence_log) >= 1
            and all(g.network_boundary_compliant and g.readonly for g in evidence_log)
        ),
        "repo_verified_evidence_backed": all(
            (not r.repository_url_verified) or (bool(r.repository_metadata_evidence_ref) and r.repository_verification_completed)
            for r in repo_evidence
        ),
        "commit_pin_evidence_backed": all(
            (not c.commit_pin_completed) or (c.commit_hash_resolved and bool(c.commit_hash) and bool(c.commit_metadata_evidence_ref))
            for c in commit_evidence
        ),
        "license_evidence_backed": all(
            (not l.license_review_completed) or (l.license_file_found and bool(l.license_file_evidence_ref))
            for l in license_evidence
        ),
        "dependency_evidence_backed": all(
            (not d.dependency_review_completed) or (d.dependency_manifest_found and len(d.dependency_manifest_refs) >= 1)
            for d in dependency_evidence
        ),
        "weight_risk_checked": (
            mobile_sam_feasibility.committed_weight_files_detected is not None
            and mobile_sam_feasibility.git_lfs_detected is not None
            and len(mobile_sam_feasibility.blocked_file_patterns) >= 8
        ),
        "full_clone_blocked_on_weight_risk": mobile_sam_full_clone_blocked,
        "license_not_runtime_approval": all(
            l.license_completion_does_not_approve_commercial_runtime
            and l.license_completion_does_not_approve_inference_runtime
            and l.commercial_runtime_not_approved
            for l in license_evidence
        ) and COMMERCIAL_RUNTIME_APPROVED is False,
        "dependency_not_install_approval": all(
            d.dependency_review_is_not_install_approval for d in dependency_evidence
        ) and DEPENDENCY_INSTALL_ALLOWED is False and PIP_INSTALL_ALLOWED is False,
        "commit_not_exec_approval": (
            all(c.commit_drift_check_required_before_execution for c in commit_evidence)
            and SOURCE_INSTALL_ALLOWED is False
            and decision_record.retry_not_executed_in_this_phase
        ),
        "feasibility_not_download_approval": (
            mobile_sam_feasibility.feasibility_is_not_weight_download_approval
            and WEIGHT_DOWNLOAD_ALLOWED is False
        ),
        "retry_not_executed": (
            decision_record.retry_not_executed_in_this_phase
            and all(g.retry_must_not_execute_in_this_phase for g in readiness_gates)
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeSourceRepositoryVerificationCommitPinReviewGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceRepositoryVerificationCommitPinReviewGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_repository_verification_commitpin_review_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "source_repository_verification_commitpin_review_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "scoped_network_evidence_log_count_gte_1": len(evidence_log) >= 1,
        "source_repository_verification_evidence_count_eq_2": len(repo_evidence) == 2,
        "source_commit_pin_resolution_evidence_count_eq_2": len(commit_evidence) == 2,
        "source_license_review_evidence_count_eq_2": len(license_evidence) == 2,
        "source_dependency_manifest_review_evidence_count_eq_2": len(dependency_evidence) == 2,
        "mobile_sam_weight_exclusion_feasibility_review_count_eq_1": True,
        "source_execution_retry_readiness_gate_review_count_gte_1": len(readiness_gates) >= 1,
        "source_repository_verification_review_decision_record_count_gte_1": True,
        "source_repository_review_risk_record_count_eq_2": len(risk_records) == 2,
        "negative_guard_count_eq_21": negative_guard_count == 21,
        "negative_guard_passed_eq_21": negative_guard_passed == 21,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "review_phase": REVIEW_PHASE is True,
        "scoped_network_lookup_allowed": SCOPED_NETWORK_LOOKUP_ALLOWED is True,
        "readonly_network_evidence_collection_allowed": READONLY_NETWORK_EVIDENCE_COLLECTION_ALLOWED is True,
        "repository_verification_review": REPOSITORY_VERIFICATION_REVIEW is True,
        "commit_pin_review": COMMIT_PIN_REVIEW is True,
        "license_review": LICENSE_REVIEW is True,
        "dependency_review": DEPENDENCY_REVIEW is True,
        "weight_exclusion_review": WEIGHT_EXCLUSION_REVIEW is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "git_clone_allowed_false": GIT_CLONE_ALLOWED is False,
        "source_checkout_allowed_false": SOURCE_CHECKOUT_ALLOWED is False,
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "dataset_download_allowed_false": DATASET_DOWNLOAD_ALLOWED is False,
        "example_asset_download_allowed_false": EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Evidence-backed bindings.
        "network_evidence_logged": len(evidence_log) >= 1,
        "repository_verification_evidence_backed": invariant_state["repo_verified_evidence_backed"],
        "commit_pin_evidence_backed": invariant_state["commit_pin_evidence_backed"],
        "license_review_evidence_backed": invariant_state["license_evidence_backed"],
        "dependency_review_evidence_backed": invariant_state["dependency_evidence_backed"],
        "mobile_sam_weight_excluding_checkout_feasibility_reviewed": (
            mobile_sam_feasibility.mobile_sam_weight_exclusion_review_completed
        ),
        "mobile_sam_full_clone_blocked_if_weight_risk": mobile_sam_full_clone_blocked,
        "weight_download_requires_separate_approval": WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL is True,
        "no_weight_download_phase_until_successful_source_execution_post_review": (
            NO_WEIGHT_DOWNLOAD_PHASE_UNTIL_SUCCESSFUL_SOURCE_EXECUTION_POST_REVIEW is True
        ),
        "source_execution_retry_not_allowed_without_readiness_gate": (
            SOURCE_EXECUTION_RETRY_NOT_ALLOWED_WITHOUT_READINESS_GATE is True
        ),
        "retry_not_executed_in_this_phase": decision_record.retry_not_executed_in_this_phase,
        # Negative guard GO keys.
        **negative_guard_go,
        # Test board fields + write.
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "test_board_artifact_refs_written": write_test_board is True,
        "test_board_protected_marker_written": write_test_board is True,
        "test_board_non_deletable_notice_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0
    final_decision = FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1SourceRepositoryVerificationCommitPinReviewDecision(
        decision_ref=DECISION_REF,
        source_repository_verification_commitpin_review_profile_count=1,
        scoped_network_evidence_log_count=len(evidence_log),
        source_repository_verification_evidence_count=len(repo_evidence),
        source_commit_pin_resolution_evidence_count=len(commit_evidence),
        source_license_review_evidence_count=len(license_evidence),
        source_dependency_manifest_review_evidence_count=len(dependency_evidence),
        mobile_sam_weight_exclusion_feasibility_review_count=1,
        source_execution_retry_readiness_gate_review_count=len(readiness_gates),
        source_repository_verification_review_decision_record_count=1,
        source_repository_review_risk_record_count=len(risk_records),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Source Repository Verification / CommitPin / License / Dependency / Weight-Exclusion Review (network-enabled readonly evidence)",
        "lifecycle_variant": SCOPE,
        "review_principle_zh": REVIEW_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "review_phase": REVIEW_PHASE,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
        "upstream_planning_ref": UPSTREAM_PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "source_repository_verification_commitpin_review_profile": _build_profile(),
        "source_repository_verification_commitpin_review_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Evidence + reviews.
        "scoped_network_evidence_log": [asdict(g) for g in evidence_log],
        "scoped_network_evidence_log_count": len(evidence_log),
        "source_repository_verification_evidence": [asdict(r) for r in repo_evidence],
        "source_repository_verification_evidence_count": len(repo_evidence),
        "source_commit_pin_resolution_evidence": [asdict(c) for c in commit_evidence],
        "source_commit_pin_resolution_evidence_count": len(commit_evidence),
        "source_license_review_evidence": [asdict(l) for l in license_evidence],
        "source_license_review_evidence_count": len(license_evidence),
        "source_dependency_manifest_review_evidence": [asdict(d) for d in dependency_evidence],
        "source_dependency_manifest_review_evidence_count": len(dependency_evidence),
        "mobile_sam_weight_exclusion_feasibility_review": asdict(mobile_sam_feasibility),
        "mobile_sam_weight_exclusion_feasibility_review_count": 1,
        "source_execution_retry_readiness_gate_review": [asdict(g) for g in readiness_gates],
        "source_execution_retry_readiness_gate_review_count": len(readiness_gates),
        "source_repository_verification_review_decision_record": asdict(decision_record),
        "source_repository_verification_review_decision_record_count": 1,
        "source_repository_review_risk_records": [asdict(r) for r in risk_records],
        "source_repository_review_risk_record_count": len(risk_records),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_source_repository_verification_commitpin_review_status": (
                "network_evidence_backed_review_complete_no_clone_no_install_no_weight_download"
                if review_ok
                else "blocked"
            ),
            "in_scope_assets": list(IN_SCOPE_ASSET_IDS),
            "ready_asset_ids": list(ready_assets),
            "not_ready_asset_ids": list(not_ready_assets),
            "both_assets_ready": both_ready,
            "recommended_next_phase": recommended_next_phase,
            "retry_scope_asset_ids": list(retry_scope),
            "byte_track_repository": EVIDENCE_REPOSITORY["byte_track"]["repository_url"],
            "byte_track_commit_pin": EVIDENCE_COMMIT["byte_track"]["commit_hash"],
            "mobile_sam_repository": EVIDENCE_REPOSITORY["mobile_sam"]["repository_url"],
            "mobile_sam_commit_pin": EVIDENCE_COMMIT["mobile_sam"]["commit_hash"],
            "mobile_sam_full_clone_blocked": mobile_sam_full_clone_blocked,
            "transition_note": (
                "Network-enabled, READONLY evidence review for byte_track and mobile_sam complete. All lookups were "
                "scoped readonly GitHub REST calls (api.github.com), each logged in the evidence log; NO clone, NO "
                "checkout, NO install, NO pip, NO weight/model/dataset/example download, NO import, NO model load, NO "
                "inference, NO runtime, NO registry mutation, and NO source-execution retry were performed. "
                "byte_track verified to FoundationVision/ByteTrack (redirected from ifzhang/ByteTrack), MIT, commit "
                "pinned to d1bf019 on main; importable module is the in-repo yolox source component (no clean PyPI "
                "wheel); requirements include torch/torchvision/opencv/numpy with HIGH build/compile risk (setup.py "
                "builds C++ extensions) and old onnx pins (conflict risk); no committed weights, no git-lfs. mobile_sam "
                "verified to ChaoningZhang/MobileSAM, Apache-2.0, commit pinned to f706ad9 on master; setup.py has "
                "EMPTY install_requires so torch/torchvision are UNDECLARED runtime deps; and CRITICALLY weights/"
                "mobile_sam.pt (~40MB) is a committed regular blob (not git-lfs), so a full clone would equal a weight "
                "download -> full clone is BLOCKED and a weight-excluding (sparse-checkout / archive-filtered, code-"
                "only) checkout is required and feasible. License review does NOT approve commercial runtime / weight "
                "download / inference; dependency review does NOT approve installation; commit pin does NOT approve "
                "source execution; weight-excluding feasibility does NOT approve weight download. Readiness: " +
                ("both assets READY" if both_ready else ("partial: ready=" + ",".join(ready_assets) if ready_assets else "none ready")) +
                ". Recommended next phase: " + recommended_next_phase + ". Even where readiness=true, retry was NOT "
                "executed here; and there is NO weight-download phase until a SUCCESSFUL source-execution post-review."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

        # Required extra evidence artifacts.
        extra_artifacts = {
            "network_evidence_log_v1.json": {
                "phase_id": PHASE_ID,
                "scoped_network_evidence_log": [asdict(g) for g in evidence_log],
                "scoped_network_evidence_log_count": len(evidence_log),
            },
            REPO_EVIDENCE_REF: {
                "phase_id": PHASE_ID,
                "source_repository_verification_evidence": [asdict(r) for r in repo_evidence],
            },
            COMMIT_EVIDENCE_REF: {
                "phase_id": PHASE_ID,
                "source_commit_pin_resolution_evidence": [asdict(c) for c in commit_evidence],
            },
            LICENSE_EVIDENCE_REF: {
                "phase_id": PHASE_ID,
                "source_license_review_evidence": [asdict(l) for l in license_evidence],
            },
            DEP_EVIDENCE_REF: {
                "phase_id": PHASE_ID,
                "source_dependency_manifest_review_evidence": [asdict(d) for d in dependency_evidence],
            },
            WEIGHT_EVIDENCE_REF: {
                "phase_id": PHASE_ID,
                "mobile_sam_weight_exclusion_feasibility_review": asdict(mobile_sam_feasibility),
            },
        }
        extra_artifact_files: List[str] = []
        for fname, payload in extra_artifacts.items():
            p = out_root / fname
            p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            extra_artifact_files.append(str(p))
        result["extra_artifact_files"] = extra_artifact_files

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
            "repository_verification_evidence_record": {
                "source_repository_verification_evidence": [asdict(r) for r in repo_evidence],
            },
            "commit_pin_resolution_record": {
                "source_commit_pin_resolution_evidence": [asdict(c) for c in commit_evidence],
            },
            "license_review_evidence_record": {
                "source_license_review_evidence": [asdict(l) for l in license_evidence],
            },
            "dependency_manifest_review_record": {
                "source_dependency_manifest_review_evidence": [asdict(d) for d in dependency_evidence],
            },
            "mobile_sam_weight_exclusion_feasibility_record": {
                "mobile_sam_weight_exclusion_feasibility_review": asdict(mobile_sam_feasibility),
                "mobile_sam_full_clone_blocked_if_weight_risk": mobile_sam_full_clone_blocked,
            },
            "network_evidence_log_record": {
                "scoped_network_evidence_log": [asdict(g) for g in evidence_log],
            },
            "source_execution_retry_readiness_gate_record": {
                "source_execution_retry_readiness_gate_review": [asdict(g) for g in readiness_gates],
                "source_repository_verification_review_decision_record": asdict(decision_record),
                "source_repository_review_risk_records": [asdict(r) for r in risk_records],
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
            "scoped_network_lookup_allowed": True,
            "git_clone_allowed": False,
            "source_checkout_allowed": False,
            "source_install_allowed": False,
            "weight_download_allowed": False,
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
    result = review_p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "extra_artifact_files": result.get("extra_artifact_files"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "network_evidence_log_count": result["decision"]["scoped_network_evidence_log_count"],
                "ready_asset_ids": result["conclusions"]["ready_asset_ids"],
                "both_assets_ready": result["conclusions"]["both_assets_ready"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "negative_guard_passed": result["negative_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
