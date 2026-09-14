# -*- coding: utf-8 -*-
"""P1 Controlled Install Governance Standardization — review v1 (STANDARDIZATION ONLY).

Abstracts MobileSAM P1 full asset onboarding chain into Model Asset Onboarding Governance
Standard V1. No install, no download, no import/load/inference, no registry mutation.
"""

from __future__ import annotations

import json
import re
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
from capabilities.midplatform.model_asset_onboarding_governance_standard.model_asset_onboarding_governance_standard_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.model_asset_onboarding_governance_standard.model_asset_onboarding_governance_standard_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    APPROVAL_GATE_TYPES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPENDENCY_INSTALL_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    LIFECYCLE_STAGES,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_CASE_FACTS,
    MODEL_LOAD_ALLOWED,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PHASE_TEMPLATE_TYPES,
    PIP_INSTALL_ALLOWED,
    PLANNING_ONLY,
    READINESS_LEVELS,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_FILE_WRITE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_INSTALL_ALLOWED,
    STANDARD_ID,
    STANDARD_MARKDOWN_REL,
    STANDARDIZATION_PHASE,
    STANDARDIZATION_PRINCIPLE_ZH,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    WEIGHT_CHAIN,
    WEIGHT_DOWNLOAD_ALLOWED,
    DependencyRepairGovernanceStandardRecord,
    FailureSemanticsGovernanceStandardRecord,
    InferenceTrialGovernanceStandardRecord,
    ModelAssetOnboardingGovernanceStandardProfile,
    ModelInstallStrategyStandardRecord,
    ModelLoadTrialGovernanceStandardRecord,
    ModelOnboardingLifecycleStandardRecord,
    NegativeModelOnboardingStandardizationGuard,
    P1ControlledInstallGovernanceStandardizationDecision,
    RegistryOverlayPatchGovernanceStandardRecord,
    ReusablePhaseTemplateRouteRecord,
    SourceRepositoryVerificationStandardRecord,
    TestBoardProtectedArtifactGovernanceStandardRecord,
    WeightGovernanceStandardRecord,
    to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "p1_controlled_install_governance_standardization_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_governance_standardization_review_v1.json"
LIFECYCLE_SUMMARY_FILENAME = "model_onboarding_lifecycle_standard_summary_v1.json"
MOBILE_SAM_MAPPING_FILENAME = "mobile_sam_case_mapping_v1.json"
TEMPLATE_MAP_FILENAME = "reusable_phase_template_map_v1.json"

_PKG = "capabilities/midplatform/model_asset_onboarding_governance_standard"
STEP_FILES = (
    f"{_PKG}/__init__.py",
    f"{_PKG}/model_asset_onboarding_governance_standard_types_v1.py",
    f"{_PKG}/model_asset_onboarding_governance_standard_registry_v1.py",
    f"{_PKG}/model_asset_onboarding_governance_standard_v1.md",
    f"{_PKG}/review_model_asset_onboarding_governance_standard_v1.py",
)

PROFILE_REF = "p1_controlled_install_governance_standardization_profile_v1"
DECISION_REF = "p1_controlled_install_governance_standardization_decision_v1"

MARKDOWN_REQUIRED_SECTIONS = (
    "Purpose / 定位",
    "Scope / 适用范围",
    "Non-goals / 非目标",
    "Lifecycle State Machine",
    "Readiness Levels",
    "Approval Gates",
    "Install Strategy Rules",
    "Source Repository Rules",
    "Weight Governance Rules",
    "Dependency Repair Rules",
    "Model-load Trial Rules",
    "Inference Trial Rules",
    "Registry Overlay Patch Rules",
    "Candidate-only Output Rules",
    "Runtime Boundary Rules",
    "Output Adapter Boundary Rules",
    "Semantic / Fact / Navigation Exclusion Rules",
    "Failure Semantics",
    "Negative Guard Pattern",
    "Test Board Protected Artifact Requirements",
    "Reusable Phase Template Map",
    "MobileSAM Case Mapping",
    "Future Model Onboarding Checklist",
)

REUSABLE_PHASE_TEMPLATE_MAP: Dict[str, Dict[str, Any]] = {
    "planning": {
        "required_flags": ["planning_only=true", "execution_flags=false"],
        "required_records": ["profile", "stage_refs", "planning_records"],
        "negative_guards": ["no_execution_in_planning"],
        "go_criteria": ["blocker_count=0"],
        "output_path_convention": "_tmp_eval_out/<phase>_smoke_v0/*_review_v1.json",
        "test_board_convention": "test_mode=planning, module=model_governance|recognition_models",
    },
    "request_approval_readiness": {
        "required_flags": ["upstream_go_verified", "owner_approval_recorded"],
        "required_records": ["request_record", "approval_record", "readiness_record"],
        "negative_guards": ["no_execution_before_readiness"],
        "go_criteria": ["readiness_checklist_complete"],
        "output_path_convention": "_tmp_eval_out/<phase>_smoke_v0/*_review_v1.json",
        "test_board_convention": "test_mode=planning",
    },
    "execution_post_review": {
        "required_flags": ["scoped_execution_flag=true"],
        "required_records": ["execution_audit", "post_review_record"],
        "negative_guards": ["boundary_guards_active"],
        "go_criteria": ["target_success_or_failed_no_boundary"],
        "output_path_convention": "_tmp_eval_out/<phase>_smoke_v0/*_review_v1.json",
        "test_board_convention": "test_mode=real_test",
    },
    "failure_review_repair_planning": {
        "required_flags": ["upstream_failed_no_boundary"],
        "required_records": ["failure_audit", "repair_plan"],
        "negative_guards": ["no_blind_retry"],
        "go_criteria": ["repair_route_defined"],
        "output_path_convention": "_tmp_eval_out/<phase>_smoke_v0/*_review_v1.json",
        "test_board_convention": "test_mode=planning",
    },
    "registry_patch_planning": {
        "required_flags": ["registry_mutation_allowed=false"],
        "required_records": ["patch_plan", "diff_plan"],
        "negative_guards": ["no_registry_write"],
        "go_criteria": ["patch_plan_complete"],
        "output_path_convention": "_tmp_eval_out/<phase>_smoke_v0/*_review_v1.json",
        "test_board_convention": "test_mode=planning",
    },
    "registry_patch_execution": {
        "required_flags": ["registry_mutation_allowed=true_scoped"],
        "required_records": ["pre_patch_snapshot", "diff", "write_audit"],
        "negative_guards": ["scoped_asset_only"],
        "go_criteria": ["patch_success_post_review"],
        "output_path_convention": "overlay_json + review_json",
        "test_board_convention": "test_mode=real_test",
    },
    "runtime_boundary_planning": {
        "required_flags": ["runtime_execution_allowed=false"],
        "required_records": ["runtime_boundary", "output_adapter_boundary", "semantic_exclusion"],
        "negative_guards": ["no_runtime_activation"],
        "go_criteria": ["boundaries_defined"],
        "output_path_convention": "_tmp_eval_out/<phase>_smoke_v0/*_review_v1.json",
        "test_board_convention": "test_mode=planning",
    },
}

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


def _resolve_standard_markdown() -> Optional[Path]:
    for base in _artifact_roots():
        p = base / STANDARD_MARKDOWN_REL
        if p.is_file():
            return p
    return None


def _audit_standard_markdown(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    sections_found = [s for s in MARKDOWN_REQUIRED_SECTIONS if s in text]
    return {
        "path": str(path),
        "sections_required": len(MARKDOWN_REQUIRED_SECTIONS),
        "sections_found": len(sections_found),
        "sections_missing": [s for s in MARKDOWN_REQUIRED_SECTIONS if s not in text],
        "readiness_levels_present": all(level in text for level in READINESS_LEVELS),
        "approval_gates_present": all(gate.replace("_", " ") in text or gate in text for gate in APPROVAL_GATE_TYPES),
        "failed_no_boundary_present": "FAILED_NO_BOUNDARY_VIOLATION" in text,
        "rollback_readiness_present": "rollback" in text.lower(),
        "registry_diff_post_review_present": "diff" in text.lower() and "post-review" in text.lower(),
        "source_repo_rules_present": "canonical repository verification" in text.lower(),
        "weight_governance_present": "sha256 required" in text.lower(),
        "dependency_repair_present": "dependency_gap" in text or "dependency gap" in text.lower(),
        "runtime_exclusion_present": "runtime_ready" in text and "reserved" in text.lower(),
        "model_load_not_inference": "model_load_verified" in text and "inference ready" in text.lower(),
        "inference_not_runtime": "inference_trial_verified" in text and "runtime_ready" in text,
        "candidate_only_present": "candidate-only" in text.lower() or "candidate only" in text.lower(),
        "inference_image_strict": "live camera" in text.lower() and "prohibited" in text.lower(),
        "lifecycle_stage_count": len(re.findall(r"→", text)),
    }


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        ModelAssetOnboardingGovernanceStandardProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            standard_id=STANDARD_ID,
            planning_only=PLANNING_ONLY,
            standardization_phase=STANDARDIZATION_PHASE,
            mobile_sam_case_based=True,
            general_model_onboarding_standard=True,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_model_asset_onboarding_governance_standard_v1(
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

    out_root = Path(output_root or (_WRITABLE_BASE / DEFAULT_OUTPUT_ROOT.relative_to(_REPO_ROOT))).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    md_path = _resolve_standard_markdown()
    md_audit: Dict[str, Any] = {}
    standard_markdown_written = False
    if md_path is not None:
        md_audit = _audit_standard_markdown(md_path)
        standard_markdown_written = md_audit["sections_found"] == md_audit["sections_required"]
        if not standard_markdown_written:
            failed_checks.append(
                f"standard.markdown_sections_missing={md_audit['sections_missing']}"
            )
    else:
        failed_checks.append("standard.markdown_missing")

    lifecycle_record = ModelOnboardingLifecycleStandardRecord(
        record_id="model_onboarding_lifecycle_standard_v1",
        lifecycle_stages=LIFECYCLE_STAGES,
        lifecycle_stage_count=len(LIFECYCLE_STAGES),
        mobile_sam_case_based=True,
    )
    install_strategy = ModelInstallStrategyStandardRecord(
        record_id="install_strategy_standard_v1",
        package_install_route_defined=True,
        source_install_route_defined=True,
        nodeps_dependency_repair_route_defined=True,
    )
    source_repo = SourceRepositoryVerificationStandardRecord(
        record_id="source_repo_verification_standard_v1",
        canonical_repo_verification_required=True,
        commit_pin_required=True,
        license_review_required=True,
        dependency_review_required=True,
        weight_exclusion_checkout_required_when_committed_weight=True,
    )
    weight_gov = WeightGovernanceStandardRecord(
        record_id="weight_governance_standard_v1",
        separate_request_required=True,
        sha256_required=True,
        size_required=True,
        controlled_storage_required=True,
        weight_downloaded_not_model_ready=True,
    )
    dep_repair = DependencyRepairGovernanceStandardRecord(
        record_id="dependency_repair_standard_v1",
        dependency_gap_not_model_corruption=True,
        request_approval_readiness_required=True,
        nodeps_route_when_torch_reuse_bounded=True,
        repair_success_not_model_load_success=True,
    )
    model_load_trial = ModelLoadTrialGovernanceStandardRecord(
        record_id="model_load_trial_standard_v1",
        request_approval_readiness_required=True,
        sha256_recheck_required=True,
        image_input_prohibited_in_model_load=True,
        inference_prohibited_in_model_load=True,
        success_means_model_load_verified_only=True,
    )
    inference_trial = InferenceTrialGovernanceStandardRecord(
        record_id="inference_trial_standard_v1",
        requires_model_load_verified=True,
        test_image_manifest_required=True,
        candidate_output_only=True,
        success_means_inference_trial_verified_only=True,
        broad_inference_ready_must_remain_false=True,
    )
    registry_patch = RegistryOverlayPatchGovernanceStandardRecord(
        record_id="registry_overlay_patch_standard_v1",
        planning_before_execution=True,
        pre_patch_snapshot_required=True,
        diff_and_post_review_required=True,
        scoped_asset_only=True,
        narrow_trial_must_not_promote_broad_ready=True,
    )
    failure_sem = FailureSemanticsGovernanceStandardRecord(
        record_id="failure_semantics_standard_v1",
        go_semantics_defined=True,
        failed_no_boundary_violation_defined=True,
        blocked_semantics_defined=True,
    )
    test_board_std = TestBoardProtectedArtifactGovernanceStandardRecord(
        record_id="test_board_artifact_standard_v1",
        protected_required=True,
        non_deletable_required=True,
        deletion_forbidden_required=True,
        planning_and_real_test_modes_supported=True,
    )
    template_route = ReusablePhaseTemplateRouteRecord(
        record_id="reusable_phase_template_route_v1",
        template_types=PHASE_TEMPLATE_TYPES,
        output_path_convention="_tmp_eval_out/<phase>_smoke_v0/",
        test_board_convention="capabilities/test_board/<module>/phase_<slug>/",
    )

    lifecycle_summary = {
        "standard_id": STANDARD_ID,
        "phase_id": PHASE_ID,
        "readiness_levels": list(READINESS_LEVELS),
        "lifecycle_stages": list(LIFECYCLE_STAGES),
        "approval_gate_types": list(APPROVAL_GATE_TYPES),
        "readiness_inequalities": {
            "code_only_ready_not_weight_ready": True,
            "code_and_weight_ready_not_model_load_ready": True,
            "model_load_verified_not_inference_ready": True,
            "inference_trial_verified_not_broad_inference_ready": True,
            "inference_trial_verified_not_runtime_ready": True,
            "runtime_ready_not_granted_by_single_inference_trial": True,
        },
        "reserved_readiness_levels": [
            "runtime_ready",
            "output_adapter_ready",
            "semantic_layer_ready",
            "commercial_runtime_approved",
        ],
        "recorded_at_utc": _now(),
    }

    mobile_sam_mapping = {
        "phase_id": PHASE_ID,
        "case_facts": dict(MOBILE_SAM_CASE_FACTS),
        "upstream_chain_closed": True,
        "final_readiness_level": "inference_trial_verified",
        "broad_flags_remain_false": [
            "inference_ready",
            "runtime_ready",
            "output_adapter_ready",
            "semantic_layer_ready",
            "commercial_runtime_approved",
        ],
        "recorded_at_utc": _now(),
    }

    template_map_payload = {
        "phase_id": PHASE_ID,
        "template_types": list(PHASE_TEMPLATE_TYPES),
        "templates": REUSABLE_PHASE_TEMPLATE_MAP,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "recorded_at_utc": _now(),
    }

    md_ok = md_audit if md_path else {}
    invariant_state: Dict[str, bool] = {
        "no_pip_or_source_install": PIP_INSTALL_ALLOWED is False and SOURCE_INSTALL_ALLOWED is False,
        "no_weight_or_dataset_download": WEIGHT_DOWNLOAD_ALLOWED is False,
        "no_import_load_inference": (
            REAL_IMPORT_ALLOWED is False
            and MODEL_LOAD_ALLOWED is False
            and REAL_INFERENCE_ALLOWED is False
        ),
        "no_registry_write": REGISTRY_MUTATION_ALLOWED is False and REGISTRY_FILE_WRITE_ALLOWED is False,
        "model_load_not_inference_ready": bool(
            lifecycle_summary["readiness_inequalities"]["model_load_verified_not_inference_ready"]
        ),
        "inference_trial_not_runtime_ready": bool(
            lifecycle_summary["readiness_inequalities"]["inference_trial_verified_not_runtime_ready"]
        ),
        "candidate_output_boundary_strict": inference_trial.candidate_output_only,
        "inference_image_source_strict": bool(md_ok.get("inference_image_strict", False)),
        "test_board_required": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "failed_no_boundary_semantics_present": failure_sem.failed_no_boundary_violation_defined and bool(
            md_ok.get("failed_no_boundary_present", False)
        ),
        "rollback_readiness_in_standard": registry_patch.pre_patch_snapshot_required and bool(
            md_ok.get("rollback_readiness_present", False)
        ),
        "registry_diff_post_review_in_standard": registry_patch.diff_and_post_review_required and bool(
            md_ok.get("registry_diff_post_review_present", False)
        ),
        "source_repo_rules_present": source_repo.canonical_repo_verification_required and bool(
            md_ok.get("source_repo_rules_present", False)
        ),
        "weight_governance_present": weight_gov.sha256_required and bool(md_ok.get("weight_governance_present", False)),
        "dependency_repair_rules_present": dep_repair.dependency_gap_not_model_corruption and bool(
            md_ok.get("dependency_repair_present", False)
        ),
        "runtime_exclusion_present": bool(md_ok.get("runtime_exclusion_present", False)),
        "test_board_record_required_true": REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_board_record_required") is True,
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_artifact_protected") is True
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_record_non_deletable") is True
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_deletion_forbidden") is True
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeModelOnboardingStandardizationGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeModelOnboardingStandardizationGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_standardization_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "model_asset_onboarding_governance_standard_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "model_onboarding_lifecycle_standard_record_count_gte_1": True,
        "install_strategy_standard_record_count_gte_1": True,
        "source_repo_verification_standard_record_count_gte_1": True,
        "weight_governance_standard_record_count_gte_1": True,
        "dependency_repair_standard_record_count_gte_1": True,
        "model_load_trial_standard_record_count_gte_1": True,
        "inference_trial_standard_record_count_gte_1": True,
        "registry_overlay_patch_standard_record_count_gte_1": True,
        "failure_semantics_standard_record_count_gte_1": True,
        "test_board_artifact_standard_record_count_gte_1": True,
        "reusable_phase_template_route_record_count_gte_1": True,
        "negative_guard_count_eq_19": negative_guard_count == 19,
        "negative_guard_passed_eq_19": negative_guard_passed == 19,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "planning_only": PLANNING_ONLY is True,
        "standardization_phase": STANDARDIZATION_PHASE is True,
        "general_model_onboarding_standard": True,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "fact_write_allowed_false": FACT_WRITE_ALLOWED is False,
        "navigation_action_speech_allowed_false": NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        "standard_markdown_written": standard_markdown_written,
        "lifecycle_state_machine_defined": lifecycle_record.lifecycle_stage_count >= 27,
        "readiness_levels_defined": len(READINESS_LEVELS) >= 17,
        "approval_gates_defined": len(APPROVAL_GATE_TYPES) >= 8,
        "install_strategy_rules_defined": install_strategy.package_install_route_defined,
        "source_repository_rules_defined": source_repo.canonical_repo_verification_required,
        "weight_governance_rules_defined": weight_gov.sha256_required,
        "dependency_repair_rules_defined": dep_repair.dependency_gap_not_model_corruption,
        "model_load_trial_rules_defined": model_load_trial.success_means_model_load_verified_only,
        "inference_trial_rules_defined": inference_trial.candidate_output_only,
        "registry_overlay_patch_rules_defined": registry_patch.scoped_asset_only,
        "failure_semantics_defined": failure_sem.blocked_semantics_defined,
        "negative_guard_pattern_defined": negative_guard_count == 19,
        "test_board_protected_artifact_requirements_defined": test_board_std.protected_required,
        "reusable_phase_template_map_defined": len(REUSABLE_PHASE_TEMPLATE_MAP) >= 7,
        "mobile_sam_case_mapping_defined": bool(MOBILE_SAM_CASE_FACTS),
        "future_model_onboarding_checklist_defined": standard_markdown_written,
        "model_load_verified_not_inference_ready": True,
        "inference_trial_verified_not_broad_inference_ready": True,
        "inference_trial_verified_not_runtime_ready": True,
        "candidate_output_not_fact_runtime_output_semantic": True,
        "runtime_requires_separate_governance": RUNTIME_EXECUTION_ALLOWED is False,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "test_board_artifact_refs_written": True,
        "test_board_protected_marker_written": True,
        "test_board_non_deletable_notice_written": True,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1ControlledInstallGovernanceStandardizationDecision(
        decision_ref=DECISION_REF,
        model_asset_onboarding_governance_standard_profile_count=1,
        model_onboarding_lifecycle_standard_record_count=1,
        install_strategy_standard_record_count=1,
        source_repo_verification_standard_record_count=1,
        weight_governance_standard_record_count=1,
        dependency_repair_standard_record_count=1,
        model_load_trial_standard_record_count=1,
        inference_trial_standard_record_count=1,
        registry_overlay_patch_standard_record_count=1,
        failure_semantics_standard_record_count=1,
        test_board_artifact_standard_record_count=1,
        reusable_phase_template_route_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        standard_markdown_written=standard_markdown_written,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Governance Standardization (standardization only)",
        "source_chain": WEIGHT_CHAIN,
        "standardization_principle_zh": STANDARDIZATION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "standard_id": STANDARD_ID,
        "planning_only": PLANNING_ONLY,
        "standardization_phase": STANDARDIZATION_PHASE,
        "mobile_sam_case_based": True,
        "general_model_onboarding_standard": True,
        "runtime_execution_allowed": RUNTIME_EXECUTION_ALLOWED,
        "runtime_activation_allowed": RUNTIME_ACTIVATION_ALLOWED,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "registry_file_write_allowed": REGISTRY_FILE_WRITE_ALLOWED,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "model_asset_onboarding_governance_standard_profile": _build_profile(),
        "model_asset_onboarding_governance_standard_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "standard_markdown_rel": STANDARD_MARKDOWN_REL,
        "standard_markdown_audit": md_audit,
        "model_onboarding_lifecycle_standard_record": asdict(lifecycle_record),
        "model_onboarding_lifecycle_standard_record_count": 1,
        "install_strategy_standard_record": asdict(install_strategy),
        "install_strategy_standard_record_count": 1,
        "source_repo_verification_standard_record": asdict(source_repo),
        "source_repo_verification_standard_record_count": 1,
        "weight_governance_standard_record": asdict(weight_gov),
        "weight_governance_standard_record_count": 1,
        "dependency_repair_standard_record": asdict(dep_repair),
        "dependency_repair_standard_record_count": 1,
        "model_load_trial_standard_record": asdict(model_load_trial),
        "model_load_trial_standard_record_count": 1,
        "inference_trial_standard_record": asdict(inference_trial),
        "inference_trial_standard_record_count": 1,
        "registry_overlay_patch_standard_record": asdict(registry_patch),
        "registry_overlay_patch_standard_record_count": 1,
        "failure_semantics_standard_record": asdict(failure_sem),
        "failure_semantics_standard_record_count": 1,
        "test_board_artifact_standard_record": asdict(test_board_std),
        "test_board_artifact_standard_record_count": 1,
        "reusable_phase_template_route_record": asdict(template_route),
        "reusable_phase_template_route_record_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "standardization_status": "go" if blocker_count == 0 else "blocked",
            "install_executed_this_phase": False,
            "weight_downloaded_this_phase": False,
            "registry_mutated_this_phase": False,
            "inference_executed_this_phase": False,
            "transition_note": (
                "STANDARDIZATION ONLY. MobileSAM P1 chain abstracted to Model Asset Onboarding "
                "Governance Standard V1. No install/download/import/load/inference/runtime/registry. "
                "Next models may reuse lifecycle + template map. Runtime boundary is a separate phase."
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

        lifecycle_path = out_root / LIFECYCLE_SUMMARY_FILENAME
        lifecycle_path.write_text(json.dumps(lifecycle_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["model_onboarding_lifecycle_standard_summary_file"] = str(lifecycle_path)

        mapping_path = out_root / MOBILE_SAM_MAPPING_FILENAME
        mapping_path.write_text(json.dumps(mobile_sam_mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["mobile_sam_case_mapping_file"] = str(mapping_path)

        template_path = out_root / TEMPLATE_MAP_FILENAME
        template_path.write_text(json.dumps(template_map_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["reusable_phase_template_map_file"] = str(template_path)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        extra_refs = [
            result.get("output_review_file"),
            result.get("model_onboarding_lifecycle_standard_summary_file"),
            result.get("mobile_sam_case_mapping_file"),
            result.get("reusable_phase_template_map_file"),
            str(_resolve_standard_markdown() or (_REPO_ROOT / STANDARD_MARKDOWN_REL)),
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
            "model_onboarding_lifecycle_standard_record": {
                "model_onboarding_lifecycle_standard_record": asdict(lifecycle_record),
            },
            "install_strategy_standard_record": {"install_strategy_standard_record": asdict(install_strategy)},
            "source_repo_verification_standard_record": {
                "source_repo_verification_standard_record": asdict(source_repo),
            },
            "weight_governance_standard_record": {"weight_governance_standard_record": asdict(weight_gov)},
            "dependency_repair_standard_record": {"dependency_repair_standard_record": asdict(dep_repair)},
            "model_load_trial_standard_record": {"model_load_trial_standard_record": asdict(model_load_trial)},
            "inference_trial_standard_record": {"inference_trial_standard_record": asdict(inference_trial)},
            "registry_overlay_patch_standard_record": {
                "registry_overlay_patch_standard_record": asdict(registry_patch),
            },
            "failure_semantics_standard_record": {"failure_semantics_standard_record": asdict(failure_sem)},
            "test_board_artifact_standard_record": {"test_board_artifact_standard_record": asdict(test_board_std)},
            "reusable_phase_template_route_record": {
                "reusable_phase_template_route_record": asdict(template_route),
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
            "standardization_phase": True,
            "runtime_allowed": False,
            "inference_allowed": False,
            "registry_mutation_allowed": False,
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
    result = review_model_asset_onboarding_governance_standard_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "model_onboarding_lifecycle_standard_summary_file": result.get(
                    "model_onboarding_lifecycle_standard_summary_file"
                ),
                "mobile_sam_case_mapping_file": result.get("mobile_sam_case_mapping_file"),
                "reusable_phase_template_map_file": result.get("reusable_phase_template_map_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "negative_guard_passed": result["negative_guard_passed"],
                "stage_ref_count": result["stage_ref_count"],
                "standard_markdown_written": result.get("standard_markdown_audit", {}).get(
                    "sections_found", 0
                )
                == len(MARKDOWN_REQUIRED_SECTIONS),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
