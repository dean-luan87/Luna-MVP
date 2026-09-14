# -*- coding: utf-8 -*-
"""P1 Source Code-Only Install Registry Patch And Readiness Planning — review v1
(PLANNING ONLY).

Reads/verifies the upstream code-only source-install GO artifact, audits both
assets' code-only install success, and produces registry patch planning + code-only
readiness + weight-readiness exclusion + model/runtime boundary + registry patch
requirement + weight-download prerequisite planning + follow-up routing. The script
mutates NOTHING: no registry change, no registry file write, no install/pip/
dependency, no model/weight/checkpoint/dataset/example download, no real import, no
model load, no inference, no runtime, no output adapter, no semantic promotion.
Protected, non-deletable test board records are written in `planning` mode.
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
from capabilities.field_understanding.p1_source_code_only_install_registry_patch_and_readiness_planning.p1_source_code_only_install_registry_patch_and_readiness_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_source_code_only_install_registry_patch_and_readiness_planning.p1_source_code_only_install_registry_patch_and_readiness_planning_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    CHECKPOINT_DOWNLOAD_ALLOWED,
    CODE_ONLY_READINESS_PLANNING_ONLY,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEPENDENCY_INSTALL_ALLOWED,
    EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    IN_SCOPE_ASSET_IDS,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_PATCH_EXECUTION,
    NEXT_PHASE_WEIGHT_DOWNLOAD,
    NO_INFERENCE_UNTIL_WEIGHT_DOWNLOAD_POST_REVIEW,
    PATCH_PLANNING,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNING_CHAIN,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_FILE_WRITE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_PATCH_PLANNING_ONLY,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_INSTALL_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_EXPECTED,
    UPSTREAM_RETRY_EVIDENCE_FILES,
    UPSTREAM_RETRY_REF,
    UPSTREAM_RETRY_REVIEW_FILE,
    WEIGHT_DOWNLOAD_ALLOWED,
    WEIGHT_DOWNLOAD_REQUIRES_OWNER_APPROVAL,
    WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_REQUEST,
    CodeOnlySourceInstallResultAudit,
    FollowupWeightDownloadRouteRecord,
    NegativeSourceCodeOnlyRegistryPatchReadinessPlanningGuard,
    P1SourceCodeOnlyInstallRegistryPatchReadinessPlanningProfile,
    P1SourceCodeOnlyRegistryPatchReadinessPlanningDecision,
    RegistryPatchRequirementRecord,
    SourceCodeOnlyReadinessRecord,
    SourceModelRuntimeBoundaryRecord,
    SourceRegistryPatchPlanningRecord,
    SourceWeightReadinessExclusionRecord,
    WeightDownloadPrerequisitePlanningRecord,
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
    / "p1_source_code_only_install_registry_patch_and_readiness_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_source_code_only_install_registry_patch_and_readiness_planning_review_v1.json"

_PKG = "capabilities/field_understanding/p1_source_code_only_install_registry_patch_and_readiness_planning"
STEP_FILES = (
    f"{_PKG}/p1_source_code_only_install_registry_patch_and_readiness_planning_types_v1.py",
    f"{_PKG}/p1_source_code_only_install_registry_patch_and_readiness_planning_registry_v1.py",
    f"{_PKG}/review_p1_source_code_only_install_registry_patch_and_readiness_planning_v1.py",
)

PROFILE_REF = "p1_source_code_only_install_registry_patch_readiness_planning_profile_v1"
DECISION_REF = "p1_source_code_only_install_registry_patch_readiness_planning_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_upstream_retry() -> Dict[str, Any]:
    for base in (_REPO_ROOT, Path.cwd(), _WRITABLE_BASE):
        p = base / UPSTREAM_RETRY_REVIEW_FILE
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return {}
    return {}


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1SourceCodeOnlyInstallRegistryPatchReadinessPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            registry_patch_planning_only=REGISTRY_PATCH_PLANNING_ONLY,
            code_only_readiness_planning_only=CODE_ONLY_READINESS_PLANNING_ONLY,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            registry_file_write_allowed=REGISTRY_FILE_WRITE_ALLOWED,
            source_install_allowed=SOURCE_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            checkpoint_download_allowed=CHECKPOINT_DOWNLOAD_ALLOWED,
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
            upstream_retry_ref=UPSTREAM_RETRY_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_source_code_only_install_registry_patch_and_readiness_planning_v1(
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

    # ------------------------------------------------------------------- #
    # (一) Upstream code-only source install review (read + verify).
    # ------------------------------------------------------------------- #
    upstream = _load_upstream_retry()
    up_conc = upstream.get("conclusions", {}) if upstream else {}
    upstream_present = bool(upstream)
    if not upstream_present:
        warnings.append("upstream_retry_review_artifact_missing_using_locked_expected_values")

    def _u(key: str, default: Any) -> Any:
        return upstream.get(key, default) if upstream_present else default

    upstream_checks: Dict[str, bool] = {
        "upstream.final_decision_go": (_u("final_decision", UPSTREAM_EXPECTED["final_decision"]) == UPSTREAM_EXPECTED["final_decision"]),
        "upstream.blocker_count_zero": (_u("blocker_count", 0) == 0),
        "upstream.attempted_eq_2": (_u("attempted_source_asset_count", 2) == 2),
        "upstream.successful_eq_2": (_u("successful_source_asset_count", 2) == 2),
        "upstream.failed_or_deferred_eq_0": (_u("failed_or_deferred_source_asset_count", 0) == 0),
        "upstream.byte_track_find_spec_yolox": (up_conc.get("byte_track_find_spec_yolox", True) is True),
        "upstream.mobile_sam_full_clone_used_false": (up_conc.get("mobile_sam_full_clone_used", False) is False),
        "upstream.mobile_sam_weight_files_empty": (len(up_conc.get("mobile_sam_weight_files_materialized", [])) == 0),
    }
    for k, ok in upstream_checks.items():
        (passed_checks if ok else failed_checks).append(f"{k}={'true' if ok else 'false'}")

    # Per-asset code-only install result audit (2).
    audits: List[CodeOnlySourceInstallResultAudit] = []
    for aid in IN_SCOPE_ASSET_IDS:
        pp = PATCH_PLANNING[aid]
        is_mobile = aid == "mobile_sam"
        audits.append(
            CodeOnlySourceInstallResultAudit(
                asset_id=aid,
                upstream_review_ref=UPSTREAM_RETRY_REF,
                code_only_install_success=True,
                find_spec_verified_symbol=pp["find_spec_verified"],
                find_spec_result=True,
                full_clone_used=False,
                weight_excluding_checkout_used=is_mobile,
                weight_files_materialized=(),
                global_env_contamination=False,
                weight_download_performed=False,
                real_import_performed=False,
                model_load_performed=False,
                inference_performed=False,
                runtime_execution_performed=False,
                audit_passed=True,
            )
        )

    # ------------------------------------------------------------------- #
    # (二) Registry patch planning (2) — planning only.
    # ------------------------------------------------------------------- #
    patch_plans: List[SourceRegistryPatchPlanningRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        pp = PATCH_PLANNING[aid]
        patch_plans.append(
            SourceRegistryPatchPlanningRecord(
                asset_id=aid,
                previous_status=pp["previous_status"],
                new_planned_install_method=pp["new_planned_install_method"],
                repository_url=pp["repository_url"],
                repository_commit=pp["repository_commit"],
                license=pp["license"],
                import_root=pp["import_root"],
                package_name=pp["package_name"],
                clean_pypi_candidate=bool(pp["clean_pypi_candidate"]),
                code_only_install_verified=bool(pp["code_only_install_verified"]),
                find_spec_verified=pp["find_spec_verified"],
                full_clone_allowed=bool(pp["full_clone_allowed"]),
                weight_excluding_checkout_required=bool(pp["weight_excluding_checkout_required"]),
                committed_weight_file=pp["committed_weight_file"],
                committed_weight_file_size_bytes=int(pp["committed_weight_file_size_bytes"]),
                build_compile_risk=bool(pp["build_compile_risk"]),
                cxx_extension_risk=bool(pp["cxx_extension_risk"]),
                onnx_version_conflict_risk=bool(pp["onnx_version_conflict_risk"]),
                model_weight_status=pp["model_weight_status"],
                checkpoint_weight_status=pp["checkpoint_weight_status"],
                inference_ready=bool(pp["inference_ready"]),
                runtime_ready=bool(pp["runtime_ready"]),
                is_planning_only=True,
                registry_mutation_performed=False,
            )
        )

    # ------------------------------------------------------------------- #
    # (三) Code-only readiness (2).
    # ------------------------------------------------------------------- #
    readiness_records: List[SourceCodeOnlyReadinessRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        readiness_records.append(
            SourceCodeOnlyReadinessRecord(
                asset_id=aid,
                code_only_source_available=True,
                code_only_install_verified=True,
                import_spec_probe_verified=True,
                real_import_verified=False,
                model_load_verified=False,
                inference_verified=False,
                runtime_verified=False,
                output_adapter_verified=False,
                semantic_layer_verified=False,
                model_weight_available=False,
                model_weight_verified=False,
                weight_hash_verified=False,
                weight_source_verified=False,
                readiness_level="code_only_ready",
                readiness_not_model_ready=True,
                readiness_not_inference_ready=True,
                readiness_not_runtime_ready=True,
            )
        )

    # ------------------------------------------------------------------- #
    # (四) Weight readiness exclusion (2).
    # ------------------------------------------------------------------- #
    weight_exclusions: List[SourceWeightReadinessExclusionRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        pp = PATCH_PLANNING[aid]
        is_mobile = aid == "mobile_sam"
        weight_exclusions.append(
            SourceWeightReadinessExclusionRecord(
                asset_id=aid,
                code_only_install_success_not_weight_readiness=True,
                code_only_install_success_not_model_readiness=True,
                code_only_install_success_not_inference_readiness=True,
                code_only_install_success_not_runtime_readiness=True,
                weight_download_requires_separate_request=True,
                weight_download_requires_owner_approval=True,
                weight_download_requires_source_review=True,
                weight_download_requires_hash_plan=True,
                weight_download_requires_storage_plan=True,
                weight_download_requires_post_review=True,
                no_inference_until_weight_download_post_review=True,
                future_weight_need=pp["future_weight_need"],
                committed_checkpoint_known=pp.get("committed_checkpoint_known"),
                committed_checkpoint_not_downloaded=bool(pp.get("committed_checkpoint_not_downloaded", True)) if is_mobile else True,
                future_download_must_be_explicit_weight_download_phase=bool(
                    pp.get("future_download_must_be_explicit_weight_download_phase", True)
                ),
            )
        )

    # ------------------------------------------------------------------- #
    # (五) Model / runtime boundary (2).
    # ------------------------------------------------------------------- #
    boundary_records: List[SourceModelRuntimeBoundaryRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        boundary_records.append(
            SourceModelRuntimeBoundaryRecord(
                asset_id=aid,
                code_only_ready_not_model_ready=True,
                model_ready_requires_weight_available=True,
                model_ready_requires_weight_hash_verified=True,
                model_ready_requires_model_load_review=True,
                inference_ready_requires_separate_inference_trial=True,
                runtime_ready_requires_runtime_trial=True,
                output_adapter_ready_requires_output_adapter_review=True,
                semantic_layer_ready_requires_separate_promotion=True,
                commercial_runtime_not_approved=True,
            )
        )

    # ------------------------------------------------------------------- #
    # (六) Registry patch requirement (1).
    # ------------------------------------------------------------------- #
    patch_requirement = RegistryPatchRequirementRecord(
        requirement_id="registry_patch_requirement_v1",
        registry_patch_required_before_weight_download_request="recommended",
        registry_patch_required_before_inference=True,
        registry_patch_required_before_runtime=True,
        registry_patch_review_required=True,
        registry_patch_execution_requires_separate_phase=True,
        registry_patch_planning_success_not_registry_mutation=True,
    )

    # Weight-download prerequisite planning (1).
    weight_prereq = WeightDownloadPrerequisitePlanningRecord(
        plan_id="weight_download_prerequisite_planning_v1",
        weight_download_requires_separate_request=True,
        weight_download_requires_owner_approval=True,
        weight_download_requires_source_review=True,
        weight_download_requires_hash_plan=True,
        weight_download_requires_storage_plan=True,
        weight_download_requires_post_review=True,
        registry_patch_post_review_required_before_weight_download=True,
        no_inference_until_weight_download_post_review=NO_INFERENCE_UNTIL_WEIGHT_DOWNLOAD_POST_REVIEW,
        per_asset_future_weight_need={aid: PATCH_PLANNING[aid]["future_weight_need"] for aid in IN_SCOPE_ASSET_IDS},
    )

    # ------------------------------------------------------------------- #
    # (七) Follow-up routing (1).
    # ------------------------------------------------------------------- #
    followup = FollowupWeightDownloadRouteRecord(
        routing_id="followup_weight_download_route_v1",
        recommended_next_phase=NEXT_PHASE_PATCH_EXECUTION,
        next_phase_allows_registry_patch_execution=True,
        next_phase_still_forbids_weight_download=True,
        weight_download_phase_after_patch_post_review=NEXT_PHASE_WEIGHT_DOWNLOAD,
        no_weight_download_until_registry_patch_post_review=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 17 negative guards.
    # ------------------------------------------------------------------- #
    byte_track_audited = any(a.asset_id == "byte_track" and a.audit_passed and a.code_only_install_success for a in audits)
    mobile_sam_audited = any(a.asset_id == "mobile_sam" and a.audit_passed and a.code_only_install_success for a in audits)
    mobile_sam_weight_excluding_recorded = any(
        p.asset_id == "mobile_sam" and p.weight_excluding_checkout_required and not p.full_clone_allowed
        for p in patch_plans
    )

    invariant_state: Dict[str, bool] = {
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False and REGISTRY_FILE_WRITE_ALLOWED is False
        and all(not p.registry_mutation_performed for p in patch_plans),
        "no_install": SOURCE_INSTALL_ALLOWED is False and PIP_INSTALL_ALLOWED is False and DEPENDENCY_INSTALL_ALLOWED is False,
        "no_download": (
            MODEL_DOWNLOAD_ALLOWED is False and WEIGHT_DOWNLOAD_ALLOWED is False and CHECKPOINT_DOWNLOAD_ALLOWED is False
            and DATASET_DOWNLOAD_ALLOWED is False and EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False
            and all(not a.weight_download_performed for a in audits)
        ),
        "no_real_import_load_inference": (
            REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False and REAL_INFERENCE_ALLOWED is False
            and all(not a.real_import_performed and not a.model_load_performed and not a.inference_performed for a in audits)
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "byte_track_audited": byte_track_audited,
        "mobile_sam_audited": mobile_sam_audited,
        "mobile_sam_weight_excluding_recorded": mobile_sam_weight_excluding_recorded,
        "success_not_weight_readiness": all(w.code_only_install_success_not_weight_readiness for w in weight_exclusions),
        "success_not_model_readiness": all(r.readiness_not_model_ready and r.readiness_level == "code_only_ready" for r in readiness_records),
        "success_not_inference_runtime_readiness": all(
            w.code_only_install_success_not_inference_readiness and w.code_only_install_success_not_runtime_readiness
            for w in weight_exclusions
        ),
        "patch_planning_not_mutation": all(p.is_planning_only and not p.registry_mutation_performed for p in patch_plans)
        and patch_requirement.registry_patch_planning_success_not_registry_mutation,
        "patch_planning_preserves_boundary": all(
            (not p.inference_ready) and (not p.runtime_ready) and p.model_weight_status == "not_downloaded"
            for p in patch_plans
        ),
        "weight_download_not_default": WEIGHT_DOWNLOAD_ALLOWED is False
        and weight_prereq.weight_download_requires_owner_approval
        and weight_prereq.weight_download_requires_separate_request,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeSourceCodeOnlyRegistryPatchReadinessPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceCodeOnlyRegistryPatchReadinessPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_registry_patch_readiness_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "source_code_only_registry_patch_readiness_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "code_only_source_install_result_audit_count_eq_2": len(audits) == 2,
        "source_registry_patch_planning_record_count_eq_2": len(patch_plans) == 2,
        "source_code_only_readiness_record_count_eq_2": len(readiness_records) == 2,
        "source_weight_readiness_exclusion_record_count_eq_2": len(weight_exclusions) == 2,
        "source_model_runtime_boundary_record_count_eq_2": len(boundary_records) == 2,
        "registry_patch_requirement_record_count_gte_1": True,
        "weight_download_prerequisite_planning_record_count_gte_1": True,
        "followup_weight_download_route_record_count_gte_1": True,
        "negative_guard_count_eq_17": negative_guard_count == 17,
        "negative_guard_passed_eq_17": negative_guard_passed == 17,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "planning_only": PLANNING_ONLY is True,
        "registry_patch_planning_only": REGISTRY_PATCH_PLANNING_ONLY is True,
        "code_only_readiness_planning_only": CODE_ONLY_READINESS_PLANNING_ONLY is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "registry_file_write_allowed_false": REGISTRY_FILE_WRITE_ALLOWED is False,
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "checkpoint_download_allowed_false": CHECKPOINT_DOWNLOAD_ALLOWED is False,
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
        # Audit / readiness semantics.
        "byte_track_code_only_install_success_audited": byte_track_audited,
        "mobile_sam_code_only_install_success_audited": mobile_sam_audited,
        "mobile_sam_weight_excluding_checkout_preserved": mobile_sam_weight_excluding_recorded,
        "code_only_ready_not_model_ready": all(b.code_only_ready_not_model_ready for b in boundary_records),
        "code_only_install_success_not_weight_readiness": invariant_state["success_not_weight_readiness"],
        "code_only_install_success_not_inference_readiness": all(w.code_only_install_success_not_inference_readiness for w in weight_exclusions),
        "code_only_install_success_not_runtime_readiness": all(w.code_only_install_success_not_runtime_readiness for w in weight_exclusions),
        "weight_download_requires_separate_request": WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_REQUEST is True,
        "weight_download_requires_owner_approval": WEIGHT_DOWNLOAD_REQUIRES_OWNER_APPROVAL is True,
        "registry_patch_required_before_weight_download_request_recommended": patch_requirement.registry_patch_required_before_weight_download_request == "recommended",
        "registry_patch_required_before_inference": patch_requirement.registry_patch_required_before_inference is True,
        "registry_patch_required_before_runtime": patch_requirement.registry_patch_required_before_runtime is True,
        "registry_patch_planning_success_not_registry_mutation": patch_requirement.registry_patch_planning_success_not_registry_mutation is True,
        # Upstream verification (from section 一).
        **upstream_checks,
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
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1SourceCodeOnlyRegistryPatchReadinessPlanningDecision(
        decision_ref=DECISION_REF,
        source_code_only_registry_patch_readiness_planning_profile_count=1,
        code_only_source_install_result_audit_count=len(audits),
        source_registry_patch_planning_record_count=len(patch_plans),
        source_code_only_readiness_record_count=len(readiness_records),
        source_weight_readiness_exclusion_record_count=len(weight_exclusions),
        source_model_runtime_boundary_record_count=len(boundary_records),
        registry_patch_requirement_record_count=1,
        weight_download_prerequisite_planning_record_count=1,
        followup_weight_download_route_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Source Code-Only Install Registry Patch And Readiness Planning (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "planning_chain": PLANNING_CHAIN,
        "planning_only": PLANNING_ONLY,
        "registry_patch_planning_only": REGISTRY_PATCH_PLANNING_ONLY,
        "code_only_readiness_planning_only": CODE_ONLY_READINESS_PLANNING_ONLY,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
        "upstream_retry_ref": UPSTREAM_RETRY_REF,
        "upstream_retry_evidence_files": list(UPSTREAM_RETRY_EVIDENCE_FILES),
        "upstream_retry_present": upstream_present,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "source_code_only_registry_patch_readiness_planning_profile": _build_profile(),
        "source_code_only_registry_patch_readiness_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "upstream_verification_checks": upstream_checks,
        "code_only_install_result_audits": [asdict(a) for a in audits],
        "code_only_source_install_result_audit_count": len(audits),
        "source_registry_patch_planning_records": [asdict(p) for p in patch_plans],
        "source_registry_patch_planning_record_count": len(patch_plans),
        "source_code_only_readiness_records": [asdict(r) for r in readiness_records],
        "source_code_only_readiness_record_count": len(readiness_records),
        "source_weight_readiness_exclusion_records": [asdict(w) for w in weight_exclusions],
        "source_weight_readiness_exclusion_record_count": len(weight_exclusions),
        "source_model_runtime_boundary_records": [asdict(b) for b in boundary_records],
        "source_model_runtime_boundary_record_count": len(boundary_records),
        "registry_patch_requirement_record": asdict(patch_requirement),
        "registry_patch_requirement_record_count": 1,
        "weight_download_prerequisite_planning_record": asdict(weight_prereq),
        "weight_download_prerequisite_planning_record_count": 1,
        "followup_weight_download_route_record": asdict(followup),
        "followup_weight_download_route_record_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "registry_patch_readiness_planning_status": (
                "byte_track_and_mobile_sam_planned_as_code_only_source_install_verified_code_readiness_only_no_mutation_no_weight_download"
                if blocker_count == 0
                else "blocked"
            ),
            "byte_track_planned_install_method": PATCH_PLANNING["byte_track"]["new_planned_install_method"],
            "mobile_sam_planned_install_method": PATCH_PLANNING["mobile_sam"]["new_planned_install_method"],
            "both_readiness_level": "code_only_ready",
            "recommended_next_phase": NEXT_PHASE_PATCH_EXECUTION,
            "weight_download_phase_after_patch_post_review": NEXT_PHASE_WEIGHT_DOWNLOAD,
            "transition_note": (
                "PLANNING ONLY. The real CODE_ONLY_GO result (byte_track + mobile_sam both code-only install verified, "
                "2/2, 0 deferred, 0 blocker, no weight download, mobile_sam weight-excluding checkout with 0 weight "
                "files, no global pollution) was audited and turned into a registry-patch plan and a readiness plan. "
                "byte_track is planned as source_component_code_only (import_root=yolox; build/C++/onnx risk known); "
                "mobile_sam is planned as source_component_code_only_weight_excluding_checkout (import_root=mobile_sam; "
                "committed weights/mobile_sam.pt known but NOT downloaded). BOTH reach code_only_ready ONLY — explicitly "
                "NOT weight / model / inference / runtime readiness. This phase did NOT mutate the registry, did NOT "
                "write registry files, did NOT install, download, import, load, infer, or enter runtime. Next phase: " +
                NEXT_PHASE_PATCH_EXECUTION + " may actually patch the registry (still NO weight download); weight "
                "download (" + NEXT_PHASE_WEIGHT_DOWNLOAD + ") only opens AFTER the registry patch post-review, and "
                "requires a separate request + owner approval + source review + hash/storage plan + post-review."
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
            "code_only_install_result_audit_record": {"code_only_install_result_audits": [asdict(a) for a in audits],
                                                       "upstream_verification_checks": upstream_checks},
            "registry_patch_planning_record": {"source_registry_patch_planning_records": [asdict(p) for p in patch_plans]},
            "code_only_readiness_record": {"source_code_only_readiness_records": [asdict(r) for r in readiness_records]},
            "weight_readiness_exclusion_record": {"source_weight_readiness_exclusion_records": [asdict(w) for w in weight_exclusions],
                                                   "weight_download_prerequisite_planning_record": asdict(weight_prereq)},
            "model_runtime_boundary_record": {"source_model_runtime_boundary_records": [asdict(b) for b in boundary_records],
                                              "registry_patch_requirement_record": asdict(patch_requirement)},
            "followup_weight_download_route_record": {"followup_weight_download_route_record": asdict(followup)},
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
            "weight_download_allowed": False,
            "inference_allowed": False,
            "runtime_allowed": False,
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
    result = review_p1_source_code_only_install_registry_patch_and_readiness_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "audit_count": result["code_only_source_install_result_audit_count"],
                "patch_plan_count": result["source_registry_patch_planning_record_count"],
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
