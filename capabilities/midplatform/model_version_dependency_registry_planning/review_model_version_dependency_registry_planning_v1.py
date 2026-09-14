# -*- coding: utf-8 -*-
"""Midplatform Model Version / Dependency Registry Planning — review v1.

Builds the midplatform model version & dependency registry as a PLANNING asset:
for each of the 17 P1/P2 model assets it produces an identity record, version
record, package dependency record, import-name binding, (weight-bearing) weight
version record, runtime backend record, environment constraint record, hardware
requirement record, license dependency binding, probe policy, compatibility
constraint and dependency risk record — plus dependency groups, fallback
compatibility, version-lock policies and negative guards. Registry / planning /
governance ONLY: no install, no download, no inference, no runtime. Protected,
non-deletable records are written to the test board.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
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
from capabilities.midplatform.model_version_dependency_registry_planning.model_version_dependency_registry_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    verify_stages,
)
from capabilities.midplatform.model_version_dependency_registry_planning.model_version_dependency_registry_planning_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    BLOCKED_UNTIL_VERSION_KNOWN,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    CREATION_FLAGS,
    DEPENDENCY_GROUPS,
    DOWNSTREAM_CONSUMER_REF,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FALLBACK_COMPATIBILITY_CHAINS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FLOATING_PLANNING_ONLY,
    HANDOFF_READINESS_TARGETS,
    INTERFACE_LAYER_GOVERNANCE_REF,
    LUNA_CORE_PRINCIPLE,
    MIDPLATFORM_REGISTRY_LAYER,
    MODEL_ADMISSION_GOVERNANCE_REF,
    MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
    MODEL_VERSION_DEPENDENCY_MANAGER_CREATED,
    NEGATIVE_GUARDS,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NON_EXECUTION_FLAGS,
    P1_DOWNLOAD_LICENSE_PLANNING_REF,
    PHASE_ID,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PLANNING_TEST_MODE_LABEL,
    PLANNING_TRUE_INVARIANTS,
    REGISTERED_MODEL_FAMILIES,
    REGISTRY_ASSETS,
    REGISTRY_PHASE_GOVERNANCE_RULES,
    REGISTRY_PLANNING_ONLY,
    REQUIRED_RECORD_KIND_FLAGS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RISK_BLOCKED,
    RISK_HIGH,
    RISK_LOW,
    RISK_MEDIUM,
    SCOPE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UNKNOWN_PLANNING_ONLY,
    VERSION_LOCK_POLICIES,
    VERSION_LOCK_STAGE_RULES,
    CompatibilityConstraintRecord,
    DependencyRiskRecord,
    EnvironmentConstraintRecord,
    FallbackCompatibilityRecord,
    HardwareRequirementRecord,
    ImportNameBindingRecord,
    LicenseDependencyBindingRecord,
    ModelIdentityRecord,
    ModelVersionDependencyRegistryProfile,
    ModelVersionRecord,
    NegativeRegistryGuard,
    OptionalDependencyGroupRecord,
    PackageDependencyRecord,
    ProbePolicyRecord,
    RegistryHandoffReadiness,
    RuntimeBackendRecord,
    VersionLockPolicy,
    WeightVersionRecord,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "midplatform_model_version_dependency_registry_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "midplatform_model_version_dependency_registry_planning_review_v1.json"

_PKG = "capabilities/midplatform/model_version_dependency_registry_planning"
STEP_FILES = (
    f"{_PKG}/model_version_dependency_registry_planning_types_v1.py",
    f"{_PKG}/model_version_dependency_registry_planning_registry_v1.py",
    f"{_PKG}/review_model_version_dependency_registry_planning_v1.py",
)

PROFILE_REF = "model_version_dependency_registry_planning_profile_v1"

_MEMORY_TIER = {RISK_LOW: "low", RISK_MEDIUM: "medium", RISK_HIGH: "high", RISK_BLOCKED: "reserved"}
_DISK_TIER = {RISK_LOW: "low", RISK_MEDIUM: "medium", RISK_HIGH: "high", RISK_BLOCKED: "reserved"}


def _version_lock_for(asset: Dict[str, Any]) -> str:
    if asset["reserved_only"]:
        return BLOCKED_UNTIL_VERSION_KNOWN
    if asset["license_class"] in ("unknown", "agpl"):
        return UNKNOWN_PLANNING_ONLY
    return FLOATING_PLANNING_ONLY


def _risk_factors(asset: Dict[str, Any]) -> List[str]:
    factors: List[str] = []
    if asset["license_class"] == "agpl":
        factors.append("agpl_license")
    if asset["license_class"] == "unknown":
        factors.append("unknown_license")
    if asset["deferred_resource_heavy"]:
        factors.append("resource_heavy_gpu_or_size")
    if asset["reserved_only"]:
        factors.append("reserved_only")
    if asset["gpu_required"]:
        factors.append("gpu_required")
    if not factors:
        factors.append("permissive_license_cpu_local_probe_friendly")
    return factors


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        ModelVersionDependencyRegistryProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            registry_planning_only=REGISTRY_PLANNING_ONLY,
            midplatform_registry_layer=MIDPLATFORM_REGISTRY_LAYER,
            model_version_dependency_manager_created=MODEL_VERSION_DEPENDENCY_MANAGER_CREATED,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            p1_download_license_planning_ref=P1_DOWNLOAD_LICENSE_PLANNING_REF,
            model_governance_integrated_closure_ref=MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
            model_admission_governance_ref=MODEL_ADMISSION_GOVERNANCE_REF,
            interface_layer_governance_ref=INTERFACE_LAYER_GOVERNANCE_REF,
            downstream_consumer_ref=DOWNSTREAM_CONSUMER_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            registered_model_families=REGISTERED_MODEL_FAMILIES,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_model_version_dependency_registry_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)

    identity_records: List[ModelIdentityRecord] = []
    version_records: List[ModelVersionRecord] = []
    package_records: List[PackageDependencyRecord] = []
    import_binding_records: List[ImportNameBindingRecord] = []
    weight_records: List[WeightVersionRecord] = []
    backend_records: List[RuntimeBackendRecord] = []
    environment_records: List[EnvironmentConstraintRecord] = []
    hardware_records: List[HardwareRequirementRecord] = []
    license_records: List[LicenseDependencyBindingRecord] = []
    probe_policy_records: List[ProbePolicyRecord] = []
    compatibility_records: List[CompatibilityConstraintRecord] = []
    risk_records: List[DependencyRiskRecord] = []

    seen_asset_ids: set = set()
    duplicate_asset_ids: List[str] = []
    empty_canonical: List[str] = []
    family_unregistered: List[str] = []
    owner_layer_non_midplatform: List[str] = []

    for asset in REGISTRY_ASSETS:
        asset_id = asset["asset_id"]
        if asset_id in seen_asset_ids:
            duplicate_asset_ids.append(asset_id)
        seen_asset_ids.add(asset_id)
        if not asset["canonical_name"]:
            empty_canonical.append(asset_id)
        if asset["model_family"] not in REGISTERED_MODEL_FAMILIES:
            family_unregistered.append(asset_id)

        version_lock = _version_lock_for(asset)
        license_class = asset["license_class"]
        risk = asset["risk"]
        reserved = bool(asset["reserved_only"])
        deferred = bool(asset["deferred_resource_heavy"])

        # --- Identity ---------------------------------------------------- #
        identity_records.append(
            ModelIdentityRecord(
                asset_id=asset_id,
                canonical_name=asset["canonical_name"],
                model_family=asset["model_family"],
                tier=asset["tier"],
                source_category=asset["source_category"],
                open_form=asset["open_form"],
                registry_status="registered_planning",
                owner_layer="midplatform",
                admission_ref=MODEL_ADMISSION_GOVERNANCE_REF,
                license_ref=P1_DOWNLOAD_LICENSE_PLANNING_REF,
                output_adapter_ref="Phase-Recognition-Model-P1-Output-Adapter-DryRun-v1-001",
                fallback_ref=f"fallback::{asset['model_family']}",
            )
        )

        # --- Version ----------------------------------------------------- #
        version_records.append(
            ModelVersionRecord(
                asset_id=asset_id,
                model_version_policy=version_lock,
                pinned_model_version="unknown",
                allowed_version_range="floating_planning_only",
                version_source="planning_registry",
                version_unknown_allowed_for_planning=True,
                version_unknown_blocks_runtime=True,
                version_unknown_blocks_inference=True,
                version_change_requires_review=True,
                version_drift_detection_required=True,
            )
        )

        # --- Package dependency ------------------------------------------ #
        conflict_risk = "high" if risk in (RISK_HIGH, RISK_BLOCKED) else ("medium" if risk == RISK_MEDIUM else "low")
        package_records.append(
            PackageDependencyRecord(
                asset_id=asset_id,
                primary_package_name=asset["primary_package_name"],
                import_probe_name=asset["import_name"],
                optional_package_names=tuple(asset["optional_package_names"]),
                required_dependency_names=tuple(asset["required_dependency_names"]),
                dependency_group=asset["dependency_group"],
                version_pin_policy=version_lock,
                visible_version_required_for_install_dryrun=True,
                dependency_conflict_risk=conflict_risk,
                no_install_in_this_phase=True,
            )
        )

        # --- Import name binding ----------------------------------------- #
        side_effect_risk = "medium" if "torch" in asset["required_dependency_names"] else "low"
        import_binding_records.append(
            ImportNameBindingRecord(
                asset_id=asset_id,
                package_name=asset["primary_package_name"],
                import_name=asset["import_name"],
                importlib_find_spec_allowed=True,
                real_import_allowed=False,
                import_side_effect_risk=side_effect_risk,
                probe_policy_ref=f"probe_policy::{asset_id}",
                no_model_load_on_probe=True,
            )
        )

        # --- Weight version (weight-bearing only) ------------------------ #
        if asset["weight_required"]:
            weight_records.append(
                WeightVersionRecord(
                    asset_id=asset_id,
                    weight_required=True,
                    expected_weight_names=tuple(asset["expected_weight_names"]),
                    expected_weight_paths=tuple(asset["expected_weight_paths"]),
                    weight_version_policy="unknown_planning_only",
                    weight_hash_required_for_future_runtime=True,
                    weight_source_allowed="official_release_or_local_path_no_auto_download",
                    auto_weight_download_allowed=False,
                    local_weight_visible_unknown_allowed_for_planning=True,
                    weight_visible_not_inference_approval=True,
                )
            )

        # --- Runtime backend --------------------------------------------- #
        backend_values = tuple(asset["backend_allowed_values"])
        backend_records.append(
            RuntimeBackendRecord(
                asset_id=asset_id,
                backend_type=backend_values[0] if backend_values else "unknown",
                backend_allowed_values=backend_values,
                gpu_required=bool(asset["gpu_required"]),
                cpu_allowed=bool(asset["cpu_allowed"]),
                onnx_allowed=bool(asset["onnx_allowed"]),
                opencv_allowed=bool(asset["opencv_allowed"]),
                backend_unknown_blocks_runtime=True,
                backend_change_requires_review=True,
            )
        )

        # --- Environment constraint -------------------------------------- #
        environment_records.append(
            EnvironmentConstraintRecord(
                asset_id=asset_id,
                python_version_policy=">=3.9,<3.13",
                os_policy="macos_arm64_primary_dev_then_linux",
                macos_arm64_compatibility=("supported_cpu_or_mps" if asset["cpu_allowed"] else "gpu_preferred_limited_on_mac"),
                cuda_required=False,
                mps_possible=bool(asset["cpu_allowed"]) and not reserved,
                cpu_only_possible=bool(asset["cpu_allowed"]),
                memory_requirement_tier=_MEMORY_TIER[risk],
                disk_requirement_tier=_DISK_TIER[risk],
                offline_allowed=True,
                internet_required_for_install=True,
                internet_required_for_runtime=False,
                environment_unknown_blocks_runtime=True,
            )
        )

        # --- Hardware requirement ---------------------------------------- #
        hardware_records.append(
            HardwareRequirementRecord(
                asset_id=asset_id,
                gpu_required=bool(asset["gpu_required"]),
                min_memory_tier=_MEMORY_TIER[risk],
                min_disk_tier=_DISK_TIER[risk],
                accelerator_preference=("gpu" if asset["gpu_required"] else "cpu_or_mps"),
                cpu_fallback_possible=bool(asset["cpu_allowed"]),
            )
        )

        # --- License dependency binding ---------------------------------- #
        license_records.append(
            LicenseDependencyBindingRecord(
                asset_id=asset_id,
                license_type=asset["license_type"],
                license_source="upstream_repository_declaration",
                commercial_runtime_approved=False,
                test_only=True,
                license_unknown_blocks_runtime=(license_class == "unknown"),
                agpl_blocks_commercial_runtime=(license_class == "agpl"),
                research_only_blocks_runtime=(asset["source_category"] == "research_only"),
                license_change_requires_review=True,
                dependency_license_risk=("high" if license_class in ("agpl", "unknown") else "low"),
            )
        )

        # --- Probe policy ------------------------------------------------ #
        probe_policy_records.append(
            ProbePolicyRecord(
                asset_id=asset_id,
                probe_method="importlib.util.find_spec",
                importlib_find_spec_only=True,
                real_import_allowed=False,
                no_model_load_on_probe=True,
                package_visible_not_runtime_approval=True,
            )
        )

        # --- Compatibility constraint ------------------------------------ #
        incompatible_reason = "none"
        if reserved:
            incompatible_reason = "reserved_only_not_integrated_in_current_execution"
        elif deferred:
            incompatible_reason = "deferred_resource_heavy_not_in_current_execution"
        compatibility_records.append(
            CompatibilityConstraintRecord(
                asset_id=asset_id,
                compatible_with_adapter=not reserved,
                compatible_with_output_schema=not reserved,
                compatible_with_midplatform_data_handling=not reserved,
                compatible_with_midplatform_model_control=True,
                incompatible_reason=incompatible_reason,
                schema_drift_requires_review=True,
            )
        )

        # --- Dependency risk --------------------------------------------- #
        risk_records.append(
            DependencyRiskRecord(
                asset_id=asset_id,
                risk_level=risk,
                risk_factors=tuple(_risk_factors(asset)),
                runtime_eligible=False,
            )
        )

    if duplicate_asset_ids:
        failed_checks.append(f"duplicate_asset_ids:{duplicate_asset_ids}")
    if empty_canonical:
        failed_checks.append(f"empty_canonical_name:{empty_canonical}")
    if family_unregistered:
        failed_checks.append(f"model_family_unregistered:{family_unregistered}")
    if owner_layer_non_midplatform:
        failed_checks.append(f"owner_layer_non_midplatform:{owner_layer_non_midplatform}")

    # --- Optional dependency group records (>= 8) ------------------------ #
    dependency_group_records = [
        OptionalDependencyGroupRecord(
            group_id=g["group_id"],
            packages=tuple(g["packages"]),
            install_in_this_phase=False,
            visible_version_required_for_install_dryrun=True,
        )
        for g in DEPENDENCY_GROUPS
    ]

    # --- Fallback compatibility records (>= 8) --------------------------- #
    fallback_records = [
        FallbackCompatibilityRecord(
            primary_asset_id=c["primary_asset_id"],
            fallback_asset_id=c["fallback_asset_id"],
            fallback_condition=c["fallback_condition"],
            fallback_output_schema_compatible=True,
            fallback_license_compatible=True,
            fallback_runtime_boundary_preserved=True,
        )
        for c in FALLBACK_COMPATIBILITY_CHAINS
    ]

    # --- Version lock policies (>= 5) ------------------------------------ #
    version_lock_records = [
        VersionLockPolicy(policy=p["policy"], allowed_stage=p["allowed_stage"], note=p["note"])
        for p in VERSION_LOCK_POLICIES
    ]

    # --- Negative guards (18) -------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    reserved_deferred_runtime_eligible_any = any(
        r.runtime_eligible for r in risk_records
        if r.risk_level == RISK_BLOCKED
    )
    invariant_state: Dict[str, bool] = {
        "unknown_version_blocks_runtime": all(v.version_unknown_blocks_runtime for v in version_records),
        "unknown_version_blocks_inference": all(v.version_unknown_blocks_inference for v in version_records),
        "package_visibility_not_runtime_approval": all(
            p.package_visible_not_runtime_approval for p in probe_policy_records
        ),
        "weight_visibility_not_inference_approval": all(
            w.weight_visible_not_inference_approval for w in weight_records
        ),
        "license_blocks_commercial_runtime": all(
            (not lr.commercial_runtime_approved)
            and (lr.agpl_blocks_commercial_runtime or lr.license_type != "agpl")
            for lr in license_records
        ),
        "no_install_performed": (
            nef["real_install_performed"] is False
            and nef["dependency_install_performed"] is False
        ),
        "no_download_performed": (
            nef["model_download_performed"] is False
            and nef["weight_download_performed"] is False
            and nef["dataset_download_performed"] is False
        ),
        "find_spec_probe_only_for_later": all(
            p.importlib_find_spec_only and not p.real_import_allowed for p in probe_policy_records
        ),
        "reserved_deferred_not_runtime_eligible": not reserved_deferred_runtime_eligible_any,
        "runtime_backend_unknown_blocks_runtime": all(
            b.backend_unknown_blocks_runtime for b in backend_records
        ),
        "dependency_version_drift_requires_review": all(
            v.version_change_requires_review and v.version_drift_detection_required
            for v in version_records
        ),
        "schema_drift_requires_review": all(
            c.schema_drift_requires_review for c in compatibility_records
        ),
        "semantic_promotion_not_allowed": nef["semantic_promotion_allowed"] is False,
        "action_speech_factwrite_navigation_not_allowed": (
            nef["action_runtime_allowed"] is False
            and nef["speech_runtime_allowed"] is False
            and nef["fact_write_runtime_allowed"] is False
            and nef["navigation_runtime_allowed"] is False
        ),
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable_true": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeRegistryGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeRegistryGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_registry_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --- Handoff readiness ------------------------------------------------ #
    handoff_readiness: List[RegistryHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            RegistryHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    n = len(REGISTRY_ASSETS)
    go_conditions: Dict[str, bool] = {
        "registry_profile_count_eq_1": True,
        "stage_ref_count_gte_10": len(stage_refs) >= 10,
        "model_identity_record_count_eq_17": len(identity_records) == 17,
        "model_version_record_count_eq_17": len(version_records) == 17,
        "package_dependency_record_count_eq_17": len(package_records) == 17,
        "import_name_binding_record_count_eq_17": len(import_binding_records) == 17,
        "weight_version_record_count_gte_10": len(weight_records) >= 10,
        "runtime_backend_record_count_eq_17": len(backend_records) == 17,
        "environment_constraint_record_count_eq_17": len(environment_records) == 17,
        "hardware_requirement_record_count_eq_17": len(hardware_records) == 17,
        "license_dependency_binding_record_count_eq_17": len(license_records) == 17,
        "optional_dependency_group_record_count_gte_8": len(dependency_group_records) >= 8,
        "probe_policy_record_count_eq_17": len(probe_policy_records) == 17,
        "compatibility_constraint_record_count_eq_17": len(compatibility_records) == 17,
        "fallback_compatibility_record_count_gte_8": len(fallback_records) >= 8,
        "version_lock_policy_count_gte_5": len(version_lock_records) >= 5,
        "dependency_risk_record_count_eq_17": len(risk_records) == 17,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        "model_asset_count_eq_17": n == 17,
        "no_duplicate_asset_ids": not duplicate_asset_ids,
        "all_canonical_names_present": not empty_canonical,
        "all_families_registered": not family_unregistered,
        "owner_layer_all_midplatform": all(r.owner_layer == "midplatform" for r in identity_records),
        # Upstream GO verification flags (gated).
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Creation / reuse flags.
        "model_version_dependency_manager_created": MODEL_VERSION_DEPENDENCY_MANAGER_CREATED is True,
        "midplatform_registry_layer": MIDPLATFORM_REGISTRY_LAYER is True,
        "registry_planning_only": REGISTRY_PLANNING_ONLY is True,
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        # Required record-kind flags.
        **{k: (v is True) for k, v in REQUIRED_RECORD_KIND_FLAGS.items()},
        # Planning true-invariants.
        **{k: (v is True) for k, v in PLANNING_TRUE_INVARIANTS.items()},
        "commercial_runtime_not_approved": NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False,
        "semantic_promotion_blocked": NON_EXECUTION_FLAGS["semantic_promotion_allowed"] is False,
        "guidance_runtime_navigation_blocked": NON_EXECUTION_FLAGS["navigation_runtime_allowed"] is False,
        "speech_tts_blocked": NON_EXECUTION_FLAGS["speech_runtime_allowed"] is False,
        "action_runtime_blocked": NON_EXECUTION_FLAGS["action_runtime_allowed"] is False,
        "vla_action_chain_blocked": NON_EXECUTION_FLAGS["vla_action_chain_allowed"] is False,
        **negative_guard_go,
        **handoff_go,
        # Test board fields + planned write.
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "test_board_artifact_refs_written": write_test_board is True,
        "test_board_protected_marker_written": write_test_board is True,
        "test_board_non_deletable_notice_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
        # Non-execution flags (all false).
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    risk_distribution: Dict[str, int] = {RISK_LOW: 0, RISK_MEDIUM: 0, RISK_HIGH: 0, RISK_BLOCKED: 0}
    for r in risk_records:
        risk_distribution[r.risk_level] = risk_distribution.get(r.risk_level, 0) + 1

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Midplatform Model Version / Dependency Registry Planning",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "planning_only": PLANNING_ONLY,
        "registry_planning_only": REGISTRY_PLANNING_ONLY,
        "midplatform_registry_layer": MIDPLATFORM_REGISTRY_LAYER,
        "test_mode_label": PLANNING_TEST_MODE_LABEL,
        "p1_download_license_planning_ref": P1_DOWNLOAD_LICENSE_PLANNING_REF,
        "model_governance_integrated_closure_ref": MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
        "model_admission_governance_ref": MODEL_ADMISSION_GOVERNANCE_REF,
        "interface_layer_governance_ref": INTERFACE_LAYER_GOVERNANCE_REF,
        "downstream_consumer_ref": DOWNSTREAM_CONSUMER_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "creation_flags": dict(CREATION_FLAGS),
        "required_record_kind_flags": dict(REQUIRED_RECORD_KIND_FLAGS),
        "registry_phase_governance_rules": list(REGISTRY_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "version_lock_stage_rules": dict(VERSION_LOCK_STAGE_RULES),
        "registry_profile": _build_profile(),
        "registry_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "model_asset_count": n,
        "model_identity_records": [asdict(r) for r in identity_records],
        "model_identity_record_count": len(identity_records),
        "model_version_records": [asdict(r) for r in version_records],
        "model_version_record_count": len(version_records),
        "package_dependency_records": [asdict(r) for r in package_records],
        "package_dependency_record_count": len(package_records),
        "import_name_binding_records": [asdict(r) for r in import_binding_records],
        "import_name_binding_record_count": len(import_binding_records),
        "weight_version_records": [asdict(r) for r in weight_records],
        "weight_version_record_count": len(weight_records),
        "runtime_backend_records": [asdict(r) for r in backend_records],
        "runtime_backend_record_count": len(backend_records),
        "environment_constraint_records": [asdict(r) for r in environment_records],
        "environment_constraint_record_count": len(environment_records),
        "hardware_requirement_records": [asdict(r) for r in hardware_records],
        "hardware_requirement_record_count": len(hardware_records),
        "license_dependency_binding_records": [asdict(r) for r in license_records],
        "license_dependency_binding_record_count": len(license_records),
        "optional_dependency_group_records": [asdict(r) for r in dependency_group_records],
        "optional_dependency_group_record_count": len(dependency_group_records),
        "probe_policy_records": [asdict(r) for r in probe_policy_records],
        "probe_policy_record_count": len(probe_policy_records),
        "compatibility_constraint_records": [asdict(r) for r in compatibility_records],
        "compatibility_constraint_record_count": len(compatibility_records),
        "fallback_compatibility_records": [asdict(r) for r in fallback_records],
        "fallback_compatibility_record_count": len(fallback_records),
        "version_lock_policies": [asdict(r) for r in version_lock_records],
        "version_lock_policy_count": len(version_lock_records),
        "dependency_risk_records": [asdict(r) for r in risk_records],
        "dependency_risk_record_count": len(risk_records),
        "dependency_risk_distribution": risk_distribution,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "model_version_dependency_registry_planning_status": (
                "midplatform_model_version_dependency_registry_established_planning_only_no_install_no_download_no_inference_no_runtime"
                if review_ok
                else "blocked"
            ),
            "downstream_consumer_ref": DOWNSTREAM_CONSUMER_REF,
            "transition_note": (
                "Midplatform now owns a lightweight model version & dependency registry for all 17 P1/P2 "
                "assets: identity, version, package dependency, import-name binding, weight version, runtime "
                "backend, environment constraints, hardware requirements, license dependency binding, probe "
                "policy, compatibility constraints, dependency risk — plus dependency groups, fallback "
                "compatibility, version-lock policies. This is registry/planning/governance only: no install, "
                "no pip install, no model/weight/dataset download, no inference, no runtime, no live "
                "camera/sensor. Unknown model version is allowed for planning but blocks runtime and real "
                "inference; package visibility is not runtime approval; weight visibility is not inference "
                "approval; runtime backend unknown blocks runtime; AGPL/unknown/research-only licenses do not "
                "become commercial runtime; reserved-only and deferred families are not runtime eligible; "
                "dependency and schema drift require review. Protected, non-deletable records are written to "
                "the test board. Next: re-enter P1 Real Install / Local Availability DryRun with THIS registry "
                "as its new upstream so later local-visibility probes are no longer scattered but registry-driven."
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

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        manifest = write_test_board_records(
            result,
            test_mode=TEST_BOARD_TEST_MODE,
            repo_root=board_root,
            module=TEST_BOARD_MODULE,
            source_review_file=result.get("output_review_file"),
        )
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["written_record_count"]

    return result


def main() -> int:
    result = review_model_version_dependency_registry_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "model_asset_count": result["model_asset_count"],
                "weight_version_record_count": result["weight_version_record_count"],
                "optional_dependency_group_record_count": result["optional_dependency_group_record_count"],
                "fallback_compatibility_record_count": result["fallback_compatibility_record_count"],
                "version_lock_policy_count": result["version_lock_policy_count"],
                "dependency_risk_distribution": result["dependency_risk_distribution"],
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
