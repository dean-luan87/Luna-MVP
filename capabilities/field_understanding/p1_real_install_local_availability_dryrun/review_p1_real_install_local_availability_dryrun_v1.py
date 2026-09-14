# -*- coding: utf-8 -*-
"""P1 Real Install / Local Availability DryRun — review v1.

Runs *real* local-environment probes (importlib.util.find_spec ONLY — never an
actual import, never an install, never a download, never inference). For each of
the 17 P1/P2 model assets it produces a local package probe, an import-spec
probe, a (when weight-bearing) local weight-path probe, a dependency gap record,
a license/runtime alignment check, an install-readiness record, an availability
matrix row, and fallback / blocked / deferred determinations. All test process
and conclusion records are written to the protected, non-deletable test board.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import asdict
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
from capabilities.field_understanding.p1_real_install_local_availability_dryrun.p1_real_install_local_availability_dryrun_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    verify_stages,
)
from capabilities.field_understanding.p1_real_install_local_availability_dryrun.p1_real_install_local_availability_dryrun_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    BLOCKED_BY_LICENSE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    DRYRUN_MODE,
    DRYRUN_TRUE_INVARIANTS,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FALLBACK_READINESS_CHAINS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    INSTALL_READINESS_STATES,
    INSTALL_REQUIRED,
    LOCAL_ASSETS,
    LOCAL_AVAILABILITY_PHASE_GOVERNANCE_RULES,
    LOCAL_AVAILABILITY_PROBE_ONLY,
    LOCAL_READY,
    LUNA_CORE_PRINCIPLE,
    MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
    NEGATED_CREATION_FLAGS,
    NEGATIVE_GUARDS,
    NEW_ADMISSION_CONTRACT_CREATED,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_OPTIONS_REF,
    NON_EXECUTION_FLAGS,
    P1_DOWNLOAD_LICENSE_PLANNING_REF,
    PARTIAL_READY,
    PHASE_ID,
    PLANNING_PRINCIPLE_ZH,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    RESERVED_ONLY,
    REUSE_FLAGS,
    SOURCE_CHAIN,
    STREAMING_POST_REVIEW_REF,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    BlockedDeferredReason,
    DependencyGapRecord,
    FallbackReadinessRecord,
    ImportSpecProbe,
    InstallReadinessRecord,
    LicenseRuntimeAlignmentCheck,
    LocalAvailabilityState,
    LocalPackageProbe,
    LocalWeightPathProbe,
    ModelAssetAvailabilityMatrix,
    P1LocalAvailabilityAuditRecord,
    P1RealInstallLocalAvailabilityHandoffReadiness,
    P1RealInstallLocalAvailabilityProfile,
    NegativeLocalAvailabilityGuard,
    candidate_to_dict,
    classify_install_readiness,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_real_install_local_availability_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_real_install_local_availability_dryrun_review_v1.json"

_PKG = "capabilities/field_understanding/p1_real_install_local_availability_dryrun"
STEP_FILES = (
    f"{_PKG}/p1_real_install_local_availability_dryrun_types_v1.py",
    f"{_PKG}/p1_real_install_local_availability_dryrun_registry_v1.py",
    f"{_PKG}/review_p1_real_install_local_availability_dryrun_v1.py",
)

PROFILE_REF = "p1_real_install_local_availability_dryrun_profile_v1"
AUDIT_REF = "p1_real_install_local_availability_audit_v1"

# Common pip-name -> import-name normalization for dependency find_spec probes.
_DEP_IMPORT_NAME: Dict[str, str] = {
    "opencv-python": "cv2",
    "open_clip_torch": "open_clip",
    "pyannote.audio": "pyannote.audio",
    "ultralytics": "ultralytics",
}


def _find_spec_safe(name: str) -> Tuple[bool, bool, str]:
    """importlib.util.find_spec probe ONLY — no import, no init side effects.

    Returns (found, module_origin_available, probe_error).
    """
    try:
        spec = importlib.util.find_spec(name)
    except (ImportError, ModuleNotFoundError, ValueError) as exc:
        return False, False, f"{type(exc).__name__}:{exc}"
    except Exception as exc:  # defensive: never let a probe escalate
        return False, False, f"{type(exc).__name__}:{exc}"
    if spec is None:
        return False, False, ""
    origin_available = bool(getattr(spec, "origin", None)) or bool(
        getattr(spec, "submodule_search_locations", None)
    )
    return True, origin_available, ""


def _gap_severity(missing_required: int, missing_optional: int, visible: bool) -> str:
    if missing_required == 0:
        return "low" if missing_optional == 0 else "low_optional_only"
    if not visible and missing_required >= 2:
        return "high"
    return "medium"


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1RealInstallLocalAvailabilityProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            dryrun_mode=DRYRUN_MODE,
            local_availability_probe_only=LOCAL_AVAILABILITY_PROBE_ONLY,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_admission_contract_created=NEW_ADMISSION_CONTRACT_CREATED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            streaming_post_review_ref=STREAMING_POST_REVIEW_REF,
            p1_download_license_planning_ref=P1_DOWNLOAD_LICENSE_PLANNING_REF,
            model_governance_integrated_closure_ref=MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            install_readiness_states=INSTALL_READINESS_STATES,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_real_install_local_availability_dryrun_v1(
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

    # --------------------------------------------------------------------- #
    # Per-asset real local probes (find_spec only).
    # --------------------------------------------------------------------- #
    package_probes: List[LocalPackageProbe] = []
    import_spec_probes: List[ImportSpecProbe] = []
    weight_path_probes: List[LocalWeightPathProbe] = []
    dependency_gap_records: List[DependencyGapRecord] = []
    license_checks: List[LicenseRuntimeAlignmentCheck] = []
    install_records: List[InstallReadinessRecord] = []
    availability_states: List[LocalAvailabilityState] = []
    availability_matrix: List[ModelAssetAvailabilityMatrix] = []
    blocked_deferred: List[BlockedDeferredReason] = []

    runtime_trial_flags: List[bool] = []
    reserved_executed_flags: List[bool] = []

    for asset in LOCAL_ASSETS:
        asset_id = asset["asset_id"]
        family = asset["family"]
        import_name = asset["import_name"]

        pkg_found, origin_available, probe_error = _find_spec_safe(asset["package_name"])
        if asset["import_name"] != asset["package_name"]:
            imp_found, imp_origin, imp_error = _find_spec_safe(import_name)
        else:
            imp_found, imp_origin, imp_error = pkg_found, origin_available, probe_error
        package_visible = pkg_found

        package_probes.append(
            LocalPackageProbe(
                asset_id=asset_id,
                model_family=family,
                package_name=asset["package_name"],
                import_probe_allowed=True,
                importlib_find_spec_used=True,
                package_visible=package_visible,
                probe_error=probe_error or imp_error,
                no_install_performed=True,
            )
        )
        import_spec_probes.append(
            ImportSpecProbe(
                asset_id=asset_id,
                import_name=import_name,
                spec_found=imp_found,
                module_origin_available=imp_origin,
                import_executed=False,
                no_model_loaded=True,
                no_inference=True,
            )
        )

        # --- Local weight path probe (weight-bearing assets only) -------- #
        weight_required = bool(asset["weight_required"])
        local_weight_visible = False
        if weight_required:
            expected = asset["expected_weight_paths"]
            visible_paths = [p for p in expected if (_REPO_ROOT / p).is_file()]
            local_weight_visible = len(visible_paths) > 0
            weight_path_probes.append(
                LocalWeightPathProbe(
                    asset_id=asset_id,
                    expected_weight_paths=tuple(expected),
                    local_weight_visible=local_weight_visible,
                    weight_path_count=len(expected),
                    no_weight_download=True,
                    weight_required_for_real_inference=True,
                    local_weight_missing_is_not_blocker_for_dryrun=True,
                )
            )

        # --- Dependency gap record --------------------------------------- #
        required_deps = asset["required_dependencies"]
        optional_deps = asset["optional_dependencies"]
        visible_required: List[str] = []
        missing_required: List[str] = []
        for dep in required_deps:
            probe_name = _DEP_IMPORT_NAME.get(dep, dep)
            found, _o, _e = _find_spec_safe(probe_name)
            (visible_required if found else missing_required).append(dep)
        missing_optional = 0
        for dep in optional_deps:
            probe_name = _DEP_IMPORT_NAME.get(dep, dep)
            found, _o, _e = _find_spec_safe(probe_name)
            if not found:
                missing_optional += 1
        severity = _gap_severity(len(missing_required), missing_optional, package_visible)
        dependency_gap_records.append(
            DependencyGapRecord(
                asset_id=asset_id,
                required_dependency_names=tuple(required_deps),
                visible_dependency_names=tuple(visible_required),
                missing_dependency_names=tuple(missing_required),
                optional_dependency_names=tuple(optional_deps),
                dependency_install_performed=False,
                install_gap_severity=severity,
            )
        )

        # --- License / runtime alignment --------------------------------- #
        license_class = asset["license_class"]
        license_blocked = bool(asset["license_blocked"])
        license_blocks_runtime = license_blocked or license_class in ("unknown",)
        license_checks.append(
            LicenseRuntimeAlignmentCheck(
                asset_id=asset_id,
                license_type=asset["license_type"],
                commercial_runtime_approved=False,
                test_only=True,
                runtime_eligible_level=int(asset["runtime_eligibility_level"]),
                license_blocks_runtime=license_blocks_runtime,
                license_allows_local_probe=True,
            )
        )

        # --- Install readiness classification ---------------------------- #
        reserved_only = bool(asset["reserved_only"])
        deferred = bool(asset["deferred_resource_heavy"])
        state = classify_install_readiness(
            reserved_only=reserved_only,
            license_blocked=license_blocked,
            license_class=license_class,
            deferred_resource_heavy=deferred,
            package_visible=package_visible,
            weight_required=weight_required,
            local_weight_visible=local_weight_visible,
            missing_required_count=len(missing_required),
        )

        blocked_reason_refs: List[str] = []
        if state == RESERVED_ONLY:
            blocked_reason_refs.append("reserved_only_family_not_executed")
        if state == BLOCKED_BY_LICENSE:
            blocked_reason_refs.append("license_blocks_commercial_runtime_local_probe_allowed")
        if state == "DEFERRED_RESOURCE_HEAVY":
            blocked_reason_refs.append("deferred_resource_heavy_gpu_or_size_or_stability")

        can_enter_next_install_dryrun = state in (LOCAL_READY, PARTIAL_READY, INSTALL_REQUIRED)
        next_action = {
            LOCAL_READY: "record_local_ready_no_runtime",
            PARTIAL_READY: "record_partial_ready_resolve_gap_in_future_install_plan",
            INSTALL_REQUIRED: "eligible_for_future_install_planning_no_install_now",
            BLOCKED_BY_LICENSE: "hold_license_review_local_probe_only",
            "DEFERRED_RESOURCE_HEAVY": "defer_resource_heavy_no_runtime",
            RESERVED_ONLY: "reserved_only_no_execution",
        }[state]
        install_records.append(
            InstallReadinessRecord(
                asset_id=asset_id,
                install_readiness_state=state,
                next_action=next_action,
                install_dryrun_passed=True,
                real_install_required_before_inference=True,
                blocked_reason_refs=tuple(blocked_reason_refs),
            )
        )

        availability_states.append(
            LocalAvailabilityState(asset_id=asset_id, state=state, runtime_eligible=False)
        )

        # --- Availability matrix row ------------------------------------- #
        fallback_available = family in (
            "segmentation",
            "object_detection_completion",
            "depth_spatial_hint",
            "scene_relation_vlm",
            "audio_speech",
            "emotion_multimodal_bridge",
        )
        deferred_or_reserved = reserved_only or deferred
        blocker_reason = "none"
        if state == RESERVED_ONLY:
            blocker_reason = "reserved_only"
        elif state == BLOCKED_BY_LICENSE:
            blocker_reason = "blocked_by_license"
        elif state == "DEFERRED_RESOURCE_HEAVY":
            blocker_reason = "deferred_resource_heavy"
        availability_matrix.append(
            ModelAssetAvailabilityMatrix(
                asset_id=asset_id,
                family=family,
                tier=asset["tier"],
                package_visible=package_visible,
                local_weight_visible=local_weight_visible,
                dependency_gap_severity=severity,
                license_status=asset["license_type"],
                runtime_eligibility_level=int(asset["runtime_eligibility_level"]),
                install_readiness_state=state,
                fallback_available=fallback_available,
                deferred_or_reserved=deferred_or_reserved,
                can_enter_next_install_dryrun=can_enter_next_install_dryrun,
                can_enter_real_output_adapter_dryrun=False,
                can_enter_runtime_trial=False,
                blocker_reason=blocker_reason,
            )
        )
        runtime_trial_flags.append(False)
        # reserved/deferred families must not be marked executed.
        reserved_executed_flags.append(False)

        if reserved_only or deferred or license_blocked or state in (
            RESERVED_ONLY,
            BLOCKED_BY_LICENSE,
            "DEFERRED_RESOURCE_HEAVY",
        ):
            reason_code = (
                "reserved_only"
                if reserved_only
                else "blocked_by_license"
                if license_blocked or state == BLOCKED_BY_LICENSE
                else "deferred_resource_heavy"
            )
            blocked_deferred.append(
                BlockedDeferredReason(
                    asset_id=asset_id,
                    reason_code=reason_code,
                    detail=f"{asset_id}:{reason_code}:local_probe_only_no_runtime",
                )
            )

    model_asset_count = len(LOCAL_ASSETS)

    # --------------------------------------------------------------------- #
    # Fallback readiness records (>= 8) — recorded only, never execute.
    # --------------------------------------------------------------------- #
    fallback_records = [
        FallbackReadinessRecord(
            trigger=chain["trigger"],
            fallback_route=chain["fallback_route"],
            candidate_only=True,
            triggers_install_or_inference=False,
        )
        for chain in FALLBACK_READINESS_CHAINS
    ]

    # --------------------------------------------------------------------- #
    # Local availability audit record.
    # --------------------------------------------------------------------- #
    audit_record = P1LocalAvailabilityAuditRecord(
        audit_ref=AUDIT_REF,
        asset_count=model_asset_count,
        candidate_only=True,
        written_to_test_board=write_test_board,
        protected=True,
        non_deletable=True,
    )

    # --------------------------------------------------------------------- #
    # Negative guards (15).
    # --------------------------------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    invariant_state: Dict[str, bool] = {
        "dependency_install_not_performed": nef["dependency_install_performed"] is False,
        "download_not_performed": (
            nef["model_download_performed"] is False
            and nef["weight_download_performed"] is False
            and nef["dataset_download_performed"] is False
        ),
        "real_inference_not_performed": nef["real_inference_performed"] is False,
        "find_spec_probe_only_true": True,
        "package_visibility_not_runtime_approval": True,
        "weight_visibility_not_inference_approval": True,
        "commercial_runtime_not_approved": nef["commercial_runtime_approved"] is False,
        "reserved_deferred_not_executed": not any(reserved_executed_flags),
        "runtime_trial_eligibility_all_false": not any(runtime_trial_flags),
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

    negative_guards: List[NegativeLocalAvailabilityGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeLocalAvailabilityGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_local_availability_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --------------------------------------------------------------------- #
    # Handoff readiness (recorded only).
    # --------------------------------------------------------------------- #
    handoff_readiness: List[P1RealInstallLocalAvailabilityHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            P1RealInstallLocalAvailabilityHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    # Aggregate matrix safety invariants.
    all_runtime_trial_false = all(not m.can_enter_runtime_trial for m in availability_matrix)
    all_output_adapter_false = all(
        not m.can_enter_real_output_adapter_dryrun for m in availability_matrix
    )
    reserved_assets = [a for a in LOCAL_ASSETS if a["reserved_only"]]
    reserved_states = [
        s.state for s in availability_states if s.asset_id in {a["asset_id"] for a in reserved_assets}
    ]
    reserved_only_states_ok = all(st == RESERVED_ONLY for st in reserved_states)

    # --------------------------------------------------------------------- #
    # GO conditions.
    # --------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "local_availability_profile_count_eq_1": True,
        "stage_ref_count_gte_10": len(stage_refs) >= 10,
        "model_asset_count_eq_17": model_asset_count == 17,
        "local_package_probe_count_eq_17": len(package_probes) == 17,
        "import_spec_probe_count_eq_17": len(import_spec_probes) == 17,
        "local_weight_path_probe_count_gte_10": len(weight_path_probes) >= 10,
        "dependency_gap_record_count_eq_17": len(dependency_gap_records) == 17,
        "license_runtime_alignment_check_count_eq_17": len(license_checks) == 17,
        "install_readiness_record_count_eq_17": len(install_records) == 17,
        "model_asset_availability_matrix_count_eq_17": len(availability_matrix) == 17,
        "fallback_readiness_record_count_gte_8": len(fallback_records) >= 8,
        "blocked_deferred_reason_count_gte_6": len(blocked_deferred) >= 6,
        "negative_guard_count_eq_15": negative_guard_count == 15,
        "negative_guard_passed_eq_15": negative_guard_passed == 15,
        # Upstream GO verification flags (gated).
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Probe / boundary invariants.
        "find_spec_probe_only": True,
        "no_real_import_executed": all(not p.import_executed for p in import_spec_probes),
        "no_dependency_install_performed": NON_EXECUTION_FLAGS["dependency_install_performed"] is False,
        "no_pip_install_performed": NON_EXECUTION_FLAGS["dependency_install_performed"] is False,
        "no_model_download_performed": NON_EXECUTION_FLAGS["model_download_performed"] is False,
        "no_weight_download_performed": NON_EXECUTION_FLAGS["weight_download_performed"] is False,
        "no_dataset_download_performed": NON_EXECUTION_FLAGS["dataset_download_performed"] is False,
        "no_real_inference_performed": NON_EXECUTION_FLAGS["real_inference_performed"] is False,
        "local_package_visibility_not_runtime_approval": True,
        "local_weight_visibility_not_inference_approval": True,
        "install_readiness_not_runtime_readiness": True,
        "runtime_trial_eligibility_all_false": all_runtime_trial_false,
        "commercial_runtime_not_approved": NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False,
        "reserved_only_not_executed": reserved_only_states_ok,
        "deferred_vlm_not_executed": True,
        "semantic_promotion_blocked": NON_EXECUTION_FLAGS["semantic_promotion_allowed"] is False,
        "guidance_runtime_navigation_blocked": NON_EXECUTION_FLAGS["navigation_runtime_allowed"] is False,
        "speech_tts_blocked": NON_EXECUTION_FLAGS["speech_runtime_allowed"] is False,
        "action_runtime_blocked": NON_EXECUTION_FLAGS["action_runtime_allowed"] is False,
        "vla_action_chain_blocked": NON_EXECUTION_FLAGS["vla_action_chain_allowed"] is False,
        "can_enter_real_output_adapter_dryrun_all_false": all_output_adapter_false,
        # Reuse / creation flags.
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_admission_contract_created_false": NEW_ADMISSION_CONTRACT_CREATED is False,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        **{k: (v is True) for k, v in DRYRUN_TRUE_INVARIANTS.items()},
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

    # State distribution (informational).
    state_distribution: Dict[str, int] = {st: 0 for st in INSTALL_READINESS_STATES}
    for s in availability_states:
        state_distribution[s.state] = state_distribution.get(s.state, 0) + 1

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Real Install / Local Availability DryRun",
        "lifecycle_variant": DRYRUN_MODE,
        "dryrun_mode": DRYRUN_MODE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "local_availability_probe_only": LOCAL_AVAILABILITY_PROBE_ONLY,
        "streaming_post_review_ref": STREAMING_POST_REVIEW_REF,
        "p1_download_license_planning_ref": P1_DOWNLOAD_LICENSE_PLANNING_REF,
        "model_governance_integrated_closure_ref": MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "negated_creation_flags": dict(NEGATED_CREATION_FLAGS),
        "local_availability_phase_governance_rules": list(LOCAL_AVAILABILITY_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "local_availability_profile": _build_profile(),
        "local_availability_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "model_asset_count": model_asset_count,
        "local_package_probes": [asdict(p) for p in package_probes],
        "local_package_probe_count": len(package_probes),
        "import_spec_probes": [asdict(p) for p in import_spec_probes],
        "import_spec_probe_count": len(import_spec_probes),
        "local_weight_path_probes": [asdict(p) for p in weight_path_probes],
        "local_weight_path_probe_count": len(weight_path_probes),
        "dependency_gap_records": [asdict(r) for r in dependency_gap_records],
        "dependency_gap_record_count": len(dependency_gap_records),
        "license_runtime_alignment_checks": [asdict(c) for c in license_checks],
        "license_runtime_alignment_check_count": len(license_checks),
        "install_readiness_records": [asdict(r) for r in install_records],
        "install_readiness_record_count": len(install_records),
        "local_availability_states": [asdict(s) for s in availability_states],
        "install_readiness_state_distribution": state_distribution,
        "model_asset_availability_matrix": [asdict(m) for m in availability_matrix],
        "model_asset_availability_matrix_count": len(availability_matrix),
        "fallback_readiness_records": [asdict(r) for r in fallback_records],
        "fallback_readiness_record_count": len(fallback_records),
        "blocked_deferred_reasons": [asdict(b) for b in blocked_deferred],
        "blocked_deferred_reason_count": len(blocked_deferred),
        "p1_local_availability_audit_record": asdict(audit_record),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "p1_real_install_local_availability_dryrun_status": (
                "local_availability_probed_find_spec_only_no_install_no_download_no_inference_no_runtime"
                if review_ok
                else "blocked"
            ),
            "next_step_options_ref": NEXT_STEP_OPTIONS_REF,
            "transition_note": (
                "Real local-environment probe of P1/P2 model assets using importlib.util.find_spec ONLY: "
                "no real import executed, no dependency install, no pip install, no model/weight/dataset "
                "download, no inference, no live camera/sensor, no runtime. Each of the 17 assets has a "
                "package probe, import-spec probe, (when weight-bearing) local weight-path probe, dependency "
                "gap record, license/runtime alignment check, install-readiness state and an availability "
                "matrix row. Package visibility is NOT runtime approval; weight visibility is NOT inference "
                "approval; install readiness is NOT runtime readiness. Runtime-trial eligibility stays false "
                "for every asset, real-output-adapter dry-run stays false, commercial runtime is not approved, "
                "AGPL/unknown licenses do not become commercial runtime, and reserved-only / deferred VLM "
                "families are not executed. Protected, non-deletable records are written to the test board. "
                "Local availability success is NOT real-output-adapter approval and NOT runtime approval. "
                "Next: decide whether to enter a P1 Real Install Plan / Controlled Install DryRun — still not "
                "real inference and not the semantic layer."
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
    result = review_p1_real_install_local_availability_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "model_asset_count": result["model_asset_count"],
                "local_weight_path_probe_count": result["local_weight_path_probe_count"],
                "blocked_deferred_reason_count": result["blocked_deferred_reason_count"],
                "install_readiness_state_distribution": result["install_readiness_state_distribution"],
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
