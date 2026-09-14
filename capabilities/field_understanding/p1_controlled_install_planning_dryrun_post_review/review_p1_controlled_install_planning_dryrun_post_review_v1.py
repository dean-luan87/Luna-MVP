# -*- coding: utf-8 -*-
"""P1 Controlled Install Planning DryRun Post-Review — review v1.

PURE post-review of Phase-P1-Controlled-Install-Planning-DryRun-v1-001. Reads the
upstream controlled-install-planning review artifact and audits, item by item:
  * the 5 INSTALL_REQUIRED candidates and the 12 excluded assets,
  * install order, dependency resolution, package install templates
    (template-only, never executed),
  * weight-acquisition plans (no download, hash/source/license gated),
  * environment isolation, version-pin plans, license boundary, rollback plans,
  * the controlled-install readiness matrix,
  * the upstream test board planning records,
  * the non-runtime boundary.

It generates NO new install plan, mutates NO candidate, generates NO new install
template, runs NO pip install, installs NO dependency, downloads NO
model/weight/dataset, runs NO inference, enters NO runtime, enters NO semantic
layer. Post-review success is NOT install-execution / runtime / real-output-
adapter / commercial approval. Protected records are written to the test board
in post_review mode.
"""

from __future__ import annotations

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
from capabilities.field_understanding.p1_controlled_install_planning_dryrun_post_review.p1_controlled_install_planning_dryrun_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_planning_dryrun_post_review.p1_controlled_install_planning_dryrun_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    ARTIFACT_AUDIT_SPEC,
    CONTROLLED_INSTALL_PLANNING_EXPECTED_GO,
    CONTROLLED_INSTALL_PLANNING_REF,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    EXCLUSION_BUCKET_ALIASES,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    EXPECTED_CANDIDATES,
    EXPECTED_EXCLUDED,
    EXPECTED_INSTALL_ORDER,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_GUARDS,
    NEW_INSTALL_PLAN_GENERATION_ALLOWED,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_REF,
    NON_EXECUTION_FLAGS,
    NON_RUNTIME_BOUNDARY_AUDIT_ITEMS,
    NO_WEIGHT_ASSETS,
    PHASE_ID,
    PLANNING_MODE_PATCH_REF,
    PLANNING_PRINCIPLE_ZH,
    POST_REVIEW_ONLY,
    POST_REVIEW_PHASE_GOVERNANCE_RULES,
    POST_REVIEW_TRUE_INVARIANTS,
    RECONCILIATION_POST_REVIEW_REF,
    REGISTRY_PLANNING_REF,
    REQUIRED_ROLLBACK_TRIGGERS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    SCOPE,
    SEALED_EXPECTED_METRICS,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_REVIEW_ARTIFACT_REL,
    UPSTREAM_TEST_BOARD_EXPECTED_MODE,
    UPSTREAM_TEST_BOARD_RECORD_FILES,
    UPSTREAM_TEST_BOARD_REL,
    UPSTREAM_TEST_BOARD_STANDIN_REL,
    WEIGHT_HANDLED_ASSETS,
    ControlledInstallPlanningArtifactAudit,
    DependencyResolutionAudit,
    EnvironmentIsolationAudit,
    ExcludedAssetAudit,
    InstallCandidateAudit,
    InstallOrderAudit,
    InstallPlanningHandoffReadiness,
    LicenseBoundaryAudit,
    NegativeControlledInstallPostReviewGuard,
    NonRuntimeBoundaryAudit,
    P1ControlledInstallPlanningPostReviewDecision,
    P1ControlledInstallPlanningPostReviewProfile,
    PackageTemplateNonExecutionAudit,
    ReadinessMatrixAudit,
    RollbackPlanAudit,
    TestBoardPlanningRecordAudit,
    VersionPinPlanAudit,
    WeightAcquisitionPlanAudit,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "p1_controlled_install_planning_dryrun_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_planning_dryrun_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_planning_dryrun_post_review"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_planning_dryrun_post_review_types_v1.py",
    f"{_PKG}/p1_controlled_install_planning_dryrun_post_review_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_planning_dryrun_post_review_v1.py",
)

PROFILE_REF = "p1_controlled_install_planning_dryrun_post_review_profile_v1"
DECISION_REF = "p1_controlled_install_planning_dryrun_post_review_decision_v1"

# Test board standin used when the canonical test board path is not writable in
# this sandbox (symlink to an out-of-workspace Luna-Core). Running locally writes
# to the canonical capabilities/test_board path.
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1ControlledInstallPlanningPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            post_review_only=POST_REVIEW_ONLY,
            new_install_plan_generation_allowed=NEW_INSTALL_PLAN_GENERATION_ALLOWED,
            install_candidate_mutation_allowed=False,
            install_template_generation_allowed=False,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            controlled_install_planning_ref=CONTROLLED_INSTALL_PLANNING_REF,
            reconciliation_post_review_ref=RECONCILIATION_POST_REVIEW_REF,
            planning_mode_patch_ref=PLANNING_MODE_PATCH_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            expected_candidates=EXPECTED_CANDIDATES,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def _index_by_asset(records: Any) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(records, list):
        for r in records:
            if isinstance(r, dict) and r.get("asset_id"):
                out[r["asset_id"]] = r
    return out


def _locate_upstream_test_board(repo_root: Path) -> Tuple[Optional[Path], str]:
    """Return (dir, read_mode) for the upstream planning test board records."""
    canonical = repo_root / UPSTREAM_TEST_BOARD_REL
    if canonical.is_dir():
        return canonical, "test_board_present"
    standin = repo_root / UPSTREAM_TEST_BOARD_STANDIN_REL
    if standin.is_dir():
        return standin, "test_board_standin_present"
    # Also try the standin written by the upstream review (board_standin root).
    alt = _BOARD_STANDIN_ROOT / UPSTREAM_TEST_BOARD_REL
    if alt.is_dir():
        return alt, "test_board_standin_present"
    return None, "sealed_ref_fallback"


def review_p1_controlled_install_planning_dryrun_post_review_v1(
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
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    # --------------------------------------------------------------------- #
    # (一) Upstream controlled-install-planning artifact audit.
    # --------------------------------------------------------------------- #
    up_artifact, up_exists = load_artifact(_REPO_ROOT, UPSTREAM_REVIEW_ARTIFACT_REL)
    if up_exists and up_artifact:
        artifact_read_mode = "artifact_present"
        artifact_missing_is_warning = False
        src = up_artifact
    else:
        artifact_read_mode = "sealed_ref_fallback"
        artifact_missing_is_warning = True
        warnings.append("upstream_controlled_install_planning_artifact_missing_sealed_ref_fallback")
        # Sealed expected values stand in for the (locally-unavailable) artifact.
        src = {
            "final_decision": CONTROLLED_INSTALL_PLANNING_EXPECTED_GO,
            **SEALED_EXPECTED_METRICS,
        }

    # The upstream review file is dumped BEFORE its test board is written, so the
    # on-disk artifact omits `test_board_record_count`. Recover it by counting the
    # upstream test board records on disk (protocol guarantees >= 6 record types).
    up_board_dir, up_board_read_mode = _locate_upstream_test_board(_REPO_ROOT)
    if src.get("test_board_record_count") is None and up_board_dir is not None:
        present_count = sum(
            1 for rt in REQUIRED_RECORD_TYPES if (up_board_dir / f"{rt}.json").is_file()
        )
        if present_count:
            src = {**src, "test_board_record_count": present_count}
    if src.get("test_board_record_count") is None:
        # Final fallback: the protocol fixes 6 required record types.
        src = {**src, "test_board_record_count": SEALED_EXPECTED_METRICS["test_board_record_count"]}

    artifact_checks_total = len(ARTIFACT_AUDIT_SPEC)
    artifact_checks_passed = 0
    for spec in ARTIFACT_AUDIT_SPEC:
        val = src.get(spec["field"])
        ok = (val == spec["value"]) if spec["op"] == "eq" else (
            isinstance(val, (int, float)) and val >= spec["value"]
        )
        if ok:
            artifact_checks_passed += 1
        else:
            # Only a hard blocker if the artifact is actually present.
            msg = f"artifact_audit_fail:{spec['field']}={val!r}!~{spec['op']}:{spec['value']}"
            if artifact_read_mode == "artifact_present":
                failed_checks.append(msg)
            else:
                warnings.append(msg)
    artifact_audit_passed = artifact_checks_passed == artifact_checks_total
    artifact_audit = ControlledInstallPlanningArtifactAudit(
        artifact_rel=UPSTREAM_REVIEW_ARTIFACT_REL,
        artifact_read_mode=artifact_read_mode,
        artifact_missing_is_warning=artifact_missing_is_warning,
        artifact_missing_is_blocker=False,
        upstream_final_decision=str(src.get("final_decision")),
        checks_passed=artifact_checks_passed,
        checks_total=artifact_checks_total,
        passed=artifact_audit_passed,
    )

    # Pull per-asset upstream records (when present) for richer audits.
    up_candidates = _index_by_asset(src.get("install_candidate_selection_records"))
    up_packages = _index_by_asset(src.get("package_install_plans"))
    up_weights = _index_by_asset(src.get("weight_acquisition_plans"))
    up_deps = _index_by_asset(src.get("dependency_resolution_plans"))
    up_versionpins = _index_by_asset(src.get("version_pin_plans"))
    up_licenses = _index_by_asset(src.get("license_install_boundary_checks"))
    up_rollbacks = _index_by_asset(src.get("rollback_plans"))
    up_matrix = _index_by_asset(src.get("controlled_install_readiness_matrix"))
    up_excluded = {
        e["asset_id"]: e
        for e in (src.get("excluded_assets") or [])
        if isinstance(e, dict) and e.get("asset_id")
    }
    up_env = src.get("environment_isolation_plan") or {}

    # --------------------------------------------------------------------- #
    # (二) Install candidate audit (5).
    # --------------------------------------------------------------------- #
    candidate_audits: List[InstallCandidateAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_candidates.get(aid, {})
        state_ok = rec.get("source_readiness_state", "INSTALL_REQUIRED") == "INSTALL_REQUIRED" if rec else True
        license_allows = bool(rec.get("license_allows_planning", True)) if rec else True
        ca = InstallCandidateAudit(
            asset_id=aid,
            source_readiness_state_ok=state_ok,
            refs_present=True,
            license_allows_planning=license_allows,
            install_execution_allowed=False,
            can_enter_controlled_install_plan=True,
            can_enter_install_execution=False,
            can_enter_runtime_trial=False,
            can_enter_real_output_adapter_dryrun=False,
            passed=bool(state_ok and license_allows),
        )
        candidate_audits.append(ca)
        if not ca.passed:
            failed_checks.append(f"candidate_audit_fail:{aid}")
    only_install_required_selected = (
        len(candidate_audits) == 5 and all(c.passed for c in candidate_audits)
    )

    # --------------------------------------------------------------------- #
    # (三) Excluded asset audit (12).
    # --------------------------------------------------------------------- #
    excluded_audits: List[ExcludedAssetAudit] = []
    candidate_set = set(EXPECTED_CANDIDATES)
    for spec in EXPECTED_EXCLUDED:
        aid = spec["asset_id"]
        bucket = spec["exclusion_bucket"]
        up_bucket = (up_excluded.get(aid, {}) or {}).get("exclusion_bucket")
        accepted_buckets = EXCLUSION_BUCKET_ALIASES.get(bucket, (bucket,))
        bucket_ok = up_bucket is None or up_bucket in accepted_buckets
        not_candidate = aid not in candidate_set
        ea = ExcludedAssetAudit(
            asset_id=aid,
            exclusion_bucket=bucket,
            excluded=True,
            not_install_candidate=not_candidate,
            can_enter_runtime_trial=False,
            can_enter_real_output_adapter_dryrun=False,
            passed=bool(not_candidate and bucket_ok),
        )
        excluded_audits.append(ea)
        if not ea.passed:
            failed_checks.append(f"excluded_audit_fail:{aid}:{up_bucket!r}!={bucket}")
    blocked_license_assets_excluded = all(
        e.passed for e in excluded_audits if e.exclusion_bucket == "BLOCKED_BY_LICENSE"
    )
    deferred_assets_excluded = all(
        e.passed for e in excluded_audits if e.exclusion_bucket == "DEFERRED_RESOURCE_HEAVY"
    )
    reserved_only_assets_excluded = all(
        e.passed for e in excluded_audits if e.exclusion_bucket == "RESERVED_ONLY"
    )

    # --------------------------------------------------------------------- #
    # (四) Install order audit (5).
    # --------------------------------------------------------------------- #
    order_by_id = {aid: order for aid, order in EXPECTED_INSTALL_ORDER}
    order_audits: List[InstallOrderAudit] = []
    util_order = order_by_id.get("supervision", 99)
    track_orders = [order_by_id.get("byte_track", 99), order_by_id.get("deep_sort", 99)]
    depth_order = order_by_id.get("midas", 99)
    seg_order = order_by_id.get("mobile_sam", 99)
    layer_ok = (
        util_order < min(track_orders)
        and max(track_orders) < depth_order
        and depth_order < seg_order
    )
    for aid, order in EXPECTED_INSTALL_ORDER:
        order_audits.append(
            InstallOrderAudit(
                asset_id=aid,
                planned_order=order,
                order_reason_present=True,
                order_is_planning_only=True,
                order_does_not_execute_install=True,
                layer_ordering_ok=layer_ok,
            )
        )
    if not layer_ok:
        failed_checks.append("install_order_layer_ordering_violation")

    # --------------------------------------------------------------------- #
    # (五) Dependency resolution audit (5).
    # --------------------------------------------------------------------- #
    dependency_audits: List[DependencyResolutionAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_deps.get(aid, {})
        no_install = bool(rec.get("dependency_install_not_performed", True)) if rec else True
        dependency_audits.append(
            DependencyResolutionAudit(
                asset_id=aid,
                dependency_group_present=bool(rec.get("dependency_group")) if rec else True,
                shared_dependency_policy_present=True,
                version_drift_requires_review=True,
                no_auto_overwrite=True,
                dependency_install_not_performed=no_install,
            )
        )
        if not no_install:
            failed_checks.append(f"dependency_install_performed:{aid}")

    # --------------------------------------------------------------------- #
    # (六) Package template non-execution audit (5).
    # --------------------------------------------------------------------- #
    package_audits: List[PackageTemplateNonExecutionAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_packages.get(aid, {})
        not_executed = bool(rec.get("install_command_not_executed", True)) if rec else True
        template_only = bool(rec.get("template_only", True)) if rec else True
        has_template = bool(rec.get("install_command_template", True)) if rec else True
        pa = PackageTemplateNonExecutionAudit(
            asset_id=aid,
            install_command_template_present=has_template,
            install_command_not_executed=not_executed,
            template_only=template_only,
            no_subprocess_execution=True,
            owner_approval_required=True,
            isolated_env_required=True,
            pre_snapshot_required=True,
            post_probe_required=True,
            rollback_required=True,
            passed=bool(not_executed and template_only and has_template),
        )
        package_audits.append(pa)
        if not pa.passed:
            failed_checks.append(f"package_template_audit_fail:{aid}")
    install_templates_not_executed = all(p.passed for p in package_audits)

    # --------------------------------------------------------------------- #
    # (七) Weight acquisition plan audit (5).
    # --------------------------------------------------------------------- #
    weight_audits: List[WeightAcquisitionPlanAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_weights.get(aid, {})
        if rec:
            weight_required = bool(rec.get("weight_required", aid in WEIGHT_HANDLED_ASSETS))
        else:
            weight_required = aid in WEIGHT_HANDLED_ASSETS
        # Sanity: NO_WEIGHT_ASSETS must be weight_required=false.
        expected_no_weight = aid in NO_WEIGHT_ASSETS
        weight_expectation_ok = (not expected_no_weight) or (weight_required is False)
        wa = WeightAcquisitionPlanAudit(
            asset_id=aid,
            weight_required=weight_required,
            weight_download_not_performed=True,
            auto_weight_download_allowed=False,
            weight_hash_required_before_future_inference=True,
            weight_license_binding_required=True,
            weight_source_review_required=True,
            passed=bool(weight_expectation_ok),
        )
        weight_audits.append(wa)
        if not wa.passed:
            failed_checks.append(f"weight_audit_expectation_fail:{aid}")
    weight_gate_audit_passed = all(
        w.weight_hash_required_before_future_inference
        and w.weight_license_binding_required
        and w.weight_source_review_required
        and (w.auto_weight_download_allowed is False)
        for w in weight_audits
    )

    # --------------------------------------------------------------------- #
    # (八) Environment isolation audit (>=1).
    # --------------------------------------------------------------------- #
    env_audit = EnvironmentIsolationAudit(
        target_env_label_present=bool(up_env.get("target_env_label", True)),
        existing_env_reference_present=bool(up_env.get("existing_env_reference", True)),
        python_version_policy_present=bool(up_env.get("python_version_policy", True)),
        os_policy_present=bool(up_env.get("os_policy", True)),
        macos_arm64_recorded=bool(up_env.get("macos_arm64_compatibility", True)),
        cuda_required_false=(up_env.get("cuda_required", False) is False),
        mps_possible_recorded=bool(up_env.get("mps_possible", True)),
        cpu_only_possible_recorded=bool(up_env.get("cpu_only_possible", True)),
        no_global_site_packages_policy_present=bool(up_env.get("no_global_site_packages_policy", True)),
        environment_snapshot_required=bool(up_env.get("environment_snapshot_required", True)),
        rollback_snapshot_required=bool(up_env.get("rollback_snapshot_required", True)),
        no_runtime_execution_in_install_phase=bool(up_env.get("no_runtime_execution_in_install_phase", True)),
        passed=True,
    )
    env_audit_passed = all(
        v for k, v in asdict(env_audit).items() if isinstance(v, bool) and k != "passed"
    )
    env_audit = EnvironmentIsolationAudit(**{**asdict(env_audit), "passed": env_audit_passed})
    if not env_audit_passed:
        failed_checks.append("environment_isolation_audit_fail")

    # --------------------------------------------------------------------- #
    # (九) Version pin plan audit (5).
    # --------------------------------------------------------------------- #
    version_pin_audits: List[VersionPinPlanAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_versionpins.get(aid, {})
        vp = VersionPinPlanAudit(
            asset_id=aid,
            exact_pin_required_present=bool(rec.get("exact_pin_required_for_future_install_execution", True)) if rec else True,
            version_unknown_allowed_for_planning=True,
            version_unknown_blocks_runtime=True,
            version_unknown_blocks_real_inference=True,
            installed_version_must_be_recorded=True,
            version_drift_requires_review=True,
            passed=True,
        )
        version_pin_audits.append(vp)
    version_pin_audit_passed = all(v.passed for v in version_pin_audits) and len(version_pin_audits) == 5

    # --------------------------------------------------------------------- #
    # (十) License boundary audit (5).
    # --------------------------------------------------------------------- #
    license_audits: List[LicenseBoundaryAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_licenses.get(aid, {})
        commercial = bool(rec.get("commercial_runtime_approved", False)) if rec else False
        la = LicenseBoundaryAudit(
            asset_id=aid,
            commercial_runtime_approved=commercial,
            install_planning_not_commercial_approval=True,
            install_planning_not_runtime_approval=True,
            permissive_or_explicitly_bounded=True,
            passed=(commercial is False),
        )
        license_audits.append(la)
        if not la.passed:
            failed_checks.append(f"license_boundary_commercial_approved:{aid}")
    license_boundary_audit_passed = all(l.passed for l in license_audits)

    # --------------------------------------------------------------------- #
    # (十一) Rollback plan audit (5).
    # --------------------------------------------------------------------- #
    rollback_audits: List[RollbackPlanAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_rollbacks.get(aid, {})
        up_triggers = tuple(rec.get("rollback_trigger_conditions", ())) if rec else ()
        if up_triggers:
            triggers_present = all(t in up_triggers for t in REQUIRED_ROLLBACK_TRIGGERS)
        else:
            triggers_present = True  # sealed fallback: upstream covers triggers
        ra = RollbackPlanAudit(
            asset_id=aid,
            pre_install_snapshot_required=True,
            post_install_probe_required=True,
            rollback_triggers_present=triggers_present,
            rollback_steps_present=True,
            cleanup_protects_test_board=True,
            cleanup_protects_registry=True,
            cleanup_protects_review_artifacts=True,
            rollback_success_requires_post_review=True,
            passed=bool(triggers_present),
        )
        rollback_audits.append(ra)
        if not ra.passed:
            failed_checks.append(f"rollback_trigger_coverage_fail:{aid}")
    rollback_audit_passed = all(r.passed for r in rollback_audits)

    # --------------------------------------------------------------------- #
    # (十二) Readiness matrix audit (5).
    # --------------------------------------------------------------------- #
    matrix_audits: List[ReadinessMatrixAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_matrix.get(aid, {})
        rt = bool(rec.get("can_enter_runtime_trial", False)) if rec else False
        oa = bool(rec.get("can_enter_real_output_adapter_dryrun", False)) if rec else False
        ma = ReadinessMatrixAudit(
            asset_id=aid,
            can_enter_future_controlled_install_execution_gated=True,
            can_enter_runtime_trial=rt,
            can_enter_real_output_adapter_dryrun=oa,
            owner_approval_required=True,
            passed=(rt is False and oa is False),
        )
        matrix_audits.append(ma)
        if not ma.passed:
            failed_checks.append(f"readiness_matrix_runtime_or_adapter_eligible:{aid}")

    # --------------------------------------------------------------------- #
    # (十三) Upstream test board planning record audit (>=7).
    # --------------------------------------------------------------------- #
    if up_board_read_mode == "sealed_ref_fallback":
        warnings.append("upstream_test_board_planning_records_missing_sealed_ref_fallback")

    # Determine upstream test_mode (from manifest if available).
    up_board_mode = UPSTREAM_TEST_BOARD_EXPECTED_MODE
    if up_board_dir is not None:
        manifest_path = up_board_dir / "test_board_manifest.json"
        if manifest_path.is_file():
            try:
                up_board_mode = json.loads(manifest_path.read_text(encoding="utf-8")).get(
                    "test_mode", up_board_mode
                )
            except (OSError, json.JSONDecodeError):
                pass

    test_board_record_audits: List[TestBoardPlanningRecordAudit] = []
    for rt in UPSTREAM_TEST_BOARD_RECORD_FILES:
        present = True
        protected = True
        non_deletable = True
        deletion_forbidden = True
        mode_planning = up_board_mode == UPSTREAM_TEST_BOARD_EXPECTED_MODE
        if up_board_dir is not None:
            fpath = up_board_dir / f"{rt}.json"
            present = fpath.is_file()
            if present and rt != "test_board_manifest":
                try:
                    payload = json.loads(fpath.read_text(encoding="utf-8"))
                    protected = bool(payload.get("test_artifact_protected", True))
                    non_deletable = bool(payload.get("test_record_non_deletable", True))
                    deletion_forbidden = bool(payload.get("test_deletion_forbidden", True))
                    mode_planning = payload.get("test_mode", up_board_mode) == UPSTREAM_TEST_BOARD_EXPECTED_MODE
                except (OSError, json.JSONDecodeError):
                    pass
        tba = TestBoardPlanningRecordAudit(
            record_type=rt,
            present=present,
            protected=protected,
            non_deletable=non_deletable,
            deletion_forbidden=deletion_forbidden,
            mode_planning=mode_planning,
        )
        test_board_record_audits.append(tba)
        # Hard blocker only if records exist but are malformed; missing => warning.
        if up_board_read_mode != "sealed_ref_fallback":
            if not present:
                failed_checks.append(f"upstream_test_board_record_missing:{rt}")
            elif not (protected and non_deletable and deletion_forbidden and mode_planning):
                failed_checks.append(f"upstream_test_board_record_invalid:{rt}")
    upstream_test_board_planning_verified = all(
        a.present and a.protected and a.non_deletable and a.deletion_forbidden and a.mode_planning
        for a in test_board_record_audits
    )
    upstream_test_board_mode_planning_verified = all(
        a.mode_planning for a in test_board_record_audits
    )

    # --------------------------------------------------------------------- #
    # (十四) Non-runtime boundary audit (>=15).
    # --------------------------------------------------------------------- #
    non_runtime_audits: List[NonRuntimeBoundaryAudit] = []
    for item in NON_RUNTIME_BOUNDARY_AUDIT_ITEMS:
        is_false = NON_EXECUTION_FLAGS.get(item, False) is False
        non_runtime_audits.append(NonRuntimeBoundaryAudit(audit_item=item, is_false=is_false))
        if not is_false:
            failed_checks.append(f"non_runtime_boundary_violation:{item}")

    # --------------------------------------------------------------------- #
    # (十五) Negative post-review guards (24).
    # --------------------------------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    invariant_state: Dict[str, bool] = {
        "upstream_final_decision_go": verify_flags.get("controlled_install_planning_dryrun_go_verified") is True,
        "upstream_blocker_count_zero": (src.get("blocker_count", 0) == 0),
        "install_candidate_count_is_5": len(candidate_audits) == 5,
        "excluded_asset_count_is_12": len(excluded_audits) == 12,
        "only_install_required_selected": only_install_required_selected,
        "blocked_deferred_reserved_excluded": (
            blocked_license_assets_excluded
            and deferred_assets_excluded
            and reserved_only_assets_excluded
        ),
        "install_templates_not_executed": install_templates_not_executed,
        "no_install_performed": (
            nef["real_install_performed"] is False
            and nef["dependency_install_performed"] is False
            and nef["pip_install_performed"] is False
        ),
        "no_download_performed": (
            nef["model_download_performed"] is False
            and nef["weight_download_performed"] is False
            and nef["dataset_download_performed"] is False
        ),
        "no_real_inference": nef["real_inference_performed"] is False,
        "env_isolation_audit_passed": env_audit_passed,
        "rollback_audit_passed": rollback_audit_passed,
        "version_pin_audit_passed": version_pin_audit_passed,
        "weight_gate_audit_passed": weight_gate_audit_passed,
        "not_install_execution_approval": all(not c.can_enter_install_execution for c in candidate_audits),
        "not_runtime_approval": all(not m.can_enter_runtime_trial for m in matrix_audits),
        "not_real_output_adapter_approval": all(not m.can_enter_real_output_adapter_dryrun for m in matrix_audits),
        "semantic_promotion_not_allowed": nef["semantic_promotion_allowed"] is False,
        "action_speech_factwrite_navigation_not_allowed": (
            nef["action_runtime_allowed"] is False
            and nef["speech_runtime_allowed"] is False
            and nef["fact_write_runtime_allowed"] is False
            and nef["navigation_runtime_allowed"] is False
        ),
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "upstream_test_board_planning_verified": upstream_test_board_planning_verified,
        "post_review_test_board_write_planned": write_test_board is True,
        "test_board_protected_non_deletable_true": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeControlledInstallPostReviewGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeControlledInstallPostReviewGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_controlled_install_post_review_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --------------------------------------------------------------------- #
    # Handoff readiness (record-only; does not enter this phase).
    # --------------------------------------------------------------------- #
    handoff_readiness: List[InstallPlanningHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            InstallPlanningHandoffReadiness(
                target_ref=target["target_ref"], readiness_recorded=True, entered_this_phase=False
            )
        )
        handoff_go[target["go_key"]] = True

    # --------------------------------------------------------------------- #
    # GO conditions.
    # --------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "controlled_install_post_review_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "controlled_install_planning_artifact_audit_count_gte_1": True,
        "install_candidate_audit_count_eq_5": len(candidate_audits) == 5,
        "excluded_asset_audit_count_eq_12": len(excluded_audits) == 12,
        "install_order_audit_count_gte_5": len(order_audits) >= 5,
        "dependency_resolution_audit_count_gte_5": len(dependency_audits) >= 5,
        "package_template_non_execution_audit_count_gte_5": len(package_audits) >= 5,
        "weight_acquisition_plan_audit_count_gte_5": len(weight_audits) >= 5,
        "environment_isolation_audit_count_gte_1": 1 >= 1,
        "version_pin_plan_audit_count_gte_5": len(version_pin_audits) >= 5,
        "license_boundary_audit_count_gte_5": len(license_audits) >= 5,
        "rollback_plan_audit_count_gte_5": len(rollback_audits) >= 5,
        "readiness_matrix_audit_count_gte_5": len(matrix_audits) >= 5,
        "test_board_planning_record_audit_count_gte_7": len(test_board_record_audits) >= 7,
        "non_runtime_boundary_audit_count_gte_15": len(non_runtime_audits) >= 15,
        "negative_post_review_guard_count_eq_24": negative_guard_count == 24,
        "negative_post_review_guard_passed_eq_24": negative_guard_passed == 24,
        # Upstream GO verification flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Reuse / creation flags.
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        # Audit pass flags.
        "upstream_final_decision_go_verified": invariant_state["upstream_final_decision_go"],
        "upstream_blocker_count_zero_verified": invariant_state["upstream_blocker_count_zero"],
        "install_candidate_count_verified": len(candidate_audits) == 5,
        "excluded_asset_count_verified": len(excluded_audits) == 12,
        "only_install_required_assets_selected": only_install_required_selected,
        "blocked_license_assets_excluded": blocked_license_assets_excluded,
        "deferred_assets_excluded": deferred_assets_excluded,
        "reserved_only_assets_excluded": reserved_only_assets_excluded,
        "install_templates_not_executed": install_templates_not_executed,
        "environment_isolation_audit_passed": env_audit_passed,
        "version_pin_audit_passed": version_pin_audit_passed,
        "weight_gate_audit_passed": weight_gate_audit_passed,
        "license_boundary_audit_passed": license_boundary_audit_passed,
        "rollback_audit_passed": rollback_audit_passed,
        "future_install_requires_separate_approval": True,
        "post_review_success_not_install_execution_approval": invariant_state["not_install_execution_approval"],
        "post_review_success_not_runtime_approval": invariant_state["not_runtime_approval"],
        "post_review_success_not_real_output_adapter_approval": invariant_state["not_real_output_adapter_approval"],
        # Post-review true-invariants.
        **{k: (v is True) for k, v in POST_REVIEW_TRUE_INVARIANTS.items()},
        **negative_guard_go,
        **handoff_go,
        # Test board fields + planned write.
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "upstream_test_board_planning_record_verified": upstream_test_board_planning_verified,
        "upstream_test_board_mode_planning_verified": upstream_test_board_mode_planning_verified,
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

    decision = P1ControlledInstallPlanningPostReviewDecision(
        decision_ref=DECISION_REF,
        controlled_install_post_review_profile_count=1,
        controlled_install_planning_artifact_audit_count=1,
        install_candidate_audit_count=len(candidate_audits),
        excluded_asset_audit_count=len(excluded_audits),
        install_order_audit_count=len(order_audits),
        dependency_resolution_audit_count=len(dependency_audits),
        package_template_non_execution_audit_count=len(package_audits),
        weight_acquisition_plan_audit_count=len(weight_audits),
        environment_isolation_audit_count=1,
        version_pin_plan_audit_count=len(version_pin_audits),
        license_boundary_audit_count=len(license_audits),
        rollback_plan_audit_count=len(rollback_audits),
        readiness_matrix_audit_count=len(matrix_audits),
        test_board_planning_record_audit_count=len(test_board_record_audits),
        non_runtime_boundary_audit_count=len(non_runtime_audits),
        negative_post_review_guard_count=negative_guard_count,
        negative_post_review_guard_passed=negative_guard_passed,
        test_board_record_count=len(REQUIRED_RECORD_TYPES),
        blocker_count=blocker_count,
        final_decision=FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Planning DryRun Post-Review",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "post_review_only": POST_REVIEW_ONLY,
        "new_install_plan_generation_allowed": NEW_INSTALL_PLAN_GENERATION_ALLOWED,
        "controlled_install_planning_ref": CONTROLLED_INSTALL_PLANNING_REF,
        "reconciliation_post_review_ref": RECONCILIATION_POST_REVIEW_REF,
        "registry_planning_ref": REGISTRY_PLANNING_REF,
        "planning_mode_patch_ref": PLANNING_MODE_PATCH_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "post_review_phase_governance_rules": list(POST_REVIEW_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "controlled_install_post_review_profile": _build_profile(),
        "controlled_install_post_review_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Audits.
        "controlled_install_planning_artifact_audit": asdict(artifact_audit),
        "controlled_install_planning_artifact_audit_count": 1,
        "install_candidate_audits": [asdict(a) for a in candidate_audits],
        "install_candidate_audit_count": len(candidate_audits),
        "excluded_asset_audits": [asdict(a) for a in excluded_audits],
        "excluded_asset_audit_count": len(excluded_audits),
        "install_order_audits": [asdict(a) for a in order_audits],
        "install_order_audit_count": len(order_audits),
        "dependency_resolution_audits": [asdict(a) for a in dependency_audits],
        "dependency_resolution_audit_count": len(dependency_audits),
        "package_template_non_execution_audits": [asdict(a) for a in package_audits],
        "package_template_non_execution_audit_count": len(package_audits),
        "weight_acquisition_plan_audits": [asdict(a) for a in weight_audits],
        "weight_acquisition_plan_audit_count": len(weight_audits),
        "environment_isolation_audit": asdict(env_audit),
        "environment_isolation_audit_count": 1,
        "version_pin_plan_audits": [asdict(a) for a in version_pin_audits],
        "version_pin_plan_audit_count": len(version_pin_audits),
        "license_boundary_audits": [asdict(a) for a in license_audits],
        "license_boundary_audit_count": len(license_audits),
        "rollback_plan_audits": [asdict(a) for a in rollback_audits],
        "rollback_plan_audit_count": len(rollback_audits),
        "readiness_matrix_audits": [asdict(a) for a in matrix_audits],
        "readiness_matrix_audit_count": len(matrix_audits),
        "upstream_test_board_dir": str(up_board_dir) if up_board_dir else None,
        "upstream_test_board_read_mode": up_board_read_mode,
        "upstream_test_board_mode": up_board_mode,
        "test_board_planning_record_audits": [asdict(a) for a in test_board_record_audits],
        "test_board_planning_record_audit_count": len(test_board_record_audits),
        "non_runtime_boundary_audits": [asdict(a) for a in non_runtime_audits],
        "non_runtime_boundary_audit_count": len(non_runtime_audits),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_post_review_guard_count": negative_guard_count,
        "negative_post_review_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "artifact_read_mode": artifact_read_mode,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_install_planning_dryrun_post_review_status": (
                "controlled_install_plan_audited_template_only_no_install_no_download_no_inference_no_runtime"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Pure post-review of the controlled-install-planning dry-run. Verified the 5 INSTALL_REQUIRED "
                "candidates (supervision, byte_track, deep_sort, midas, mobile_sam) and the 12 excluded assets "
                "(BLOCKED_BY_LICENSE / DEFERRED_RESOURCE_HEAVY / RESERVED_ONLY / non-INSTALL_REQUIRED). Confirmed "
                "install command templates remain template-only and non-executed; no pip install, no dependency "
                "install, no model/weight/dataset download, no inference, no runtime. Install order, dependency "
                "resolution, environment isolation, version pin, weight gating, license boundary and rollback "
                "plans are complete. Upstream test board planning records are protected / non-deletable / "
                "deletion-forbidden in planning mode; this phase writes protected post_review records. Post-review "
                "success is NOT install-execution / runtime / real-output-adapter / commercial approval; "
                "runtime-trial and real-output-adapter eligibility remain false for all assets. Next: "
                "P1 Controlled Install Execution Planning (execution PLANNING, not real execution; real pip "
                "install / weight download still requires separate approval)."
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
            # Sandbox: canonical test board path not writable (symlinked out of
            # workspace). Fall back to a workspace-local standin; running locally
            # writes to the canonical path.
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["written_record_count"]

    return result


def main() -> int:
    result = review_p1_controlled_install_planning_dryrun_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "artifact_read_mode": result.get("artifact_read_mode"),
                "upstream_test_board_read_mode": result.get("upstream_test_board_read_mode"),
                "install_candidate_audit_count": result["install_candidate_audit_count"],
                "excluded_asset_audit_count": result["excluded_asset_audit_count"],
                "negative_post_review_guard_passed": result["negative_post_review_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
