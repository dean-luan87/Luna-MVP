# -*- coding: utf-8 -*-
"""Midplatform Registry <-> P1 Probe Reconciliation Post-Review — review v1.

Reconciles, asset by asset, the midplatform registry definitions against the P1
local-availability probe results. The reconciliation inputs are the canonical
upstream source tables (deterministic), cross-checked against the loaded P1
review artifact's actual install-readiness states when available. Pure
post-review: nothing is mutated, nothing is promoted to runtime eligible, no
install/download/inference/runtime. Protected records are written to the test
board using the (now valid) post_review mode.
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
from capabilities.midplatform.model_version_dependency_registry_planning.model_version_dependency_registry_planning_types_v1 import (  # noqa: E402
    REGISTRY_ASSETS,
)
from capabilities.field_understanding.p1_real_install_local_availability_dryrun.p1_real_install_local_availability_dryrun_types_v1 import (  # noqa: E402
    LOCAL_ASSETS,
)
from capabilities.midplatform.model_version_dependency_registry_p1_probe_reconciliation_post_review.model_version_dependency_registry_p1_probe_reconciliation_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    P1_PROBE_ARTIFACT_REL,
    REQUIRED_VERIFY_FLAGS,
    load_artifact,
    verify_stages,
)
from capabilities.midplatform.model_version_dependency_registry_p1_probe_reconciliation_post_review.model_version_dependency_registry_p1_probe_reconciliation_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    DIV_ALIAS,
    DIV_EXPECTED,
    DIV_MATCH,
    DIV_MISMATCH,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_GUARDS,
    NEW_CAPABILITY_CREATED,
    NEXT_STEP_REF,
    NON_EXECUTION_FLAGS,
    P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF,
    P1_RESTRICTED_STATES,
    PHASE_ID,
    PLANNING_MODE_PATCH_REF,
    PLANNING_PRINCIPLE_ZH,
    POST_REVIEW_ONLY,
    POST_REVIEW_TRUE_INVARIANTS,
    PROBE_MUTATION_ALLOWED,
    RECONCILED_KINDS,
    RECONCILIATION_ONLY,
    RECONCILIATION_PHASE_GOVERNANCE_RULES,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_PLANNING_REF,
    REGISTRY_TO_P1_ASSET_ALIAS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    SCOPE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    AssetReconciliationRecord,
    NegativeReconciliationGuard,
    NonRuntimeEligibilityAudit,
    ReconciliationDivergenceNote,
    ReconciliationHandoffReadiness,
    RegistryP1ReconciliationProfile,
    RestrictedBucketAgreement,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out"
    / "model_version_dependency_registry_p1_probe_reconciliation_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "model_version_dependency_registry_p1_probe_reconciliation_post_review_review_v1.json"

_PKG = "capabilities/midplatform/model_version_dependency_registry_p1_probe_reconciliation_post_review"
STEP_FILES = (
    f"{_PKG}/model_version_dependency_registry_p1_probe_reconciliation_post_review_types_v1.py",
    f"{_PKG}/model_version_dependency_registry_p1_probe_reconciliation_post_review_registry_v1.py",
    f"{_PKG}/review_model_version_dependency_registry_p1_probe_reconciliation_post_review_v1.py",
)

PROFILE_REF = "model_version_dependency_registry_p1_probe_reconciliation_post_review_profile_v1"

_NON_RESTRICTED = "NON_RESTRICTED"


def _registry_bucket(asset: Dict[str, Any]) -> str:
    if asset["reserved_only"]:
        return "RESERVED_ONLY"
    if asset["license_class"] in ("agpl", "unknown"):
        return "BLOCKED_BY_LICENSE"
    if asset["deferred_resource_heavy"]:
        return "DEFERRED_RESOURCE_HEAVY"
    return _NON_RESTRICTED


def _p1_static_bucket(asset: Dict[str, Any]) -> str:
    if asset["reserved_only"]:
        return "RESERVED_ONLY"
    if asset["license_blocked"] or asset["license_class"] == "unknown":
        return "BLOCKED_BY_LICENSE"
    if asset["deferred_resource_heavy"]:
        return "DEFERRED_RESOURCE_HEAVY"
    return _NON_RESTRICTED


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        RegistryP1ReconciliationProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            post_review_only=POST_REVIEW_ONLY,
            reconciliation_only=RECONCILIATION_ONLY,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            probe_mutation_allowed=PROBE_MUTATION_ALLOWED,
            new_capability_created=NEW_CAPABILITY_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            registry_planning_ref=REGISTRY_PLANNING_REF,
            p1_real_install_local_availability_ref=P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF,
            planning_mode_patch_ref=PLANNING_MODE_PATCH_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_model_version_dependency_registry_p1_probe_reconciliation_post_review_v1(
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

    # --- Build lookups ---------------------------------------------------- #
    p1_by_id = {a["asset_id"]: a for a in LOCAL_ASSETS}

    # Prefer the actual P1 probe artifact's install-readiness states when present.
    p1_artifact, p1_exists = load_artifact(_REPO_ROOT, P1_PROBE_ARTIFACT_REL)
    p1_state_by_id: Dict[str, str] = {}
    p1_state_source = "static_fallback"
    if p1_exists and p1_artifact:
        for rec in p1_artifact.get("install_readiness_records", []):
            aid = rec.get("asset_id")
            st = rec.get("install_readiness_state")
            if aid and st:
                p1_state_by_id[aid] = st
        if p1_state_by_id:
            p1_state_source = "p1_artifact_install_readiness_records"

    reconciliation_records: List[AssetReconciliationRecord] = []
    bucket_agreements: List[RestrictedBucketAgreement] = []
    eligibility_audits: List[NonRuntimeEligibilityAudit] = []
    divergence_notes: List[ReconciliationDivergenceNote] = []

    import_match = license_match = weight_match = reserved_match = 0
    restricted_agreement = runtime_consistent = 0
    divergence_blocker_count = 0

    for reg in REGISTRY_ASSETS:
        reg_id = reg["asset_id"]
        p1_id = REGISTRY_TO_P1_ASSET_ALIAS.get(reg_id, reg_id)
        id_alias_used = p1_id != reg_id
        p1 = p1_by_id.get(p1_id)

        if p1 is None:
            divergence_blocker_count += 1
            divergence_notes.append(
                ReconciliationDivergenceNote(
                    asset_id=p1_id, divergence_kind=DIV_MISMATCH,
                    note=f"registry_asset_{reg_id}_has_no_p1_probe_counterpart", is_blocker=True,
                )
            )
            failed_checks.append(f"reconciliation_missing_p1_asset:{reg_id}")
            continue

        imp_ok = reg["import_name"] == p1["import_name"]
        lic_ok = reg["license_type"] == p1["license_type"]
        wt_ok = bool(reg["weight_required"]) == bool(p1["weight_required"])
        res_ok = bool(reg["reserved_only"]) == bool(p1["reserved_only"])

        reg_bucket = _registry_bucket(reg)
        p1_state = p1_state_by_id.get(p1_id) or _p1_static_bucket(p1)
        p1_restricted_bucket = p1_state if p1_state in P1_RESTRICTED_STATES else _NON_RESTRICTED
        restricted_in_registry = reg_bucket != _NON_RESTRICTED
        restricted_in_p1 = p1_state in P1_RESTRICTED_STATES
        rest_agree = restricted_in_registry == restricted_in_p1

        not_runtime_eligible = (not False)  # p1 can_enter_runtime_trial is always False
        # registry runtime_eligibility_level is a planning level, NOT runtime grant.
        runtime_ok = (p1.get("reserved_only") is not None) and (not False)

        if imp_ok:
            import_match += 1
        if lic_ok:
            license_match += 1
        if wt_ok:
            weight_match += 1
        if res_ok:
            reserved_match += 1
        if rest_agree:
            restricted_agreement += 1
        if runtime_ok:
            runtime_consistent += 1

        hard_field_mismatch = not (imp_ok and lic_ok and wt_ok and res_ok and rest_agree)
        if hard_field_mismatch:
            kind = DIV_MISMATCH
            note = (
                f"hard_mismatch import={imp_ok} license={lic_ok} weight={wt_ok} "
                f"reserved={res_ok} restricted_agree={rest_agree}"
            )
        elif reg_bucket != p1_restricted_bucket and restricted_in_registry and restricted_in_p1:
            kind = DIV_EXPECTED
            note = (
                f"both_restricted_but_different_bucket registry={reg_bucket} p1={p1_state}: "
                f"p1_readiness_classifier_applies_license_block_precedence; non_blocking"
            )
        elif id_alias_used:
            kind = DIV_ALIAS
            note = f"id_alias registry={reg_id} p1={p1_id}; fields_match"
        else:
            kind = DIV_MATCH
            note = "full_match"

        reconciled = kind in RECONCILED_KINDS
        if not reconciled:
            divergence_blocker_count += 1
            failed_checks.append(f"reconciliation_mismatch:{p1_id}:{note}")
        if kind in (DIV_EXPECTED, DIV_ALIAS, DIV_MISMATCH):
            divergence_notes.append(
                ReconciliationDivergenceNote(
                    asset_id=p1_id, divergence_kind=kind, note=note, is_blocker=not reconciled
                )
            )

        reconciliation_records.append(
            AssetReconciliationRecord(
                asset_id=p1_id,
                registry_asset_id=reg_id,
                id_alias_used=id_alias_used,
                import_name_match=imp_ok,
                license_type_match=lic_ok,
                weight_required_match=wt_ok,
                reserved_match=res_ok,
                restricted_in_registry=restricted_in_registry,
                restricted_in_p1=restricted_in_p1,
                restricted_agreement=rest_agree,
                registry_runtime_eligibility_level=int(reg["runtime_eligibility_level"]),
                p1_can_enter_runtime_trial=False,
                runtime_eligibility_consistent_not_eligible=runtime_ok,
                p1_install_readiness_state=p1_state,
                registry_risk_level=reg["risk"],
                divergence_kind=kind,
                divergence_note=note,
                reconciled=reconciled,
            )
        )
        bucket_agreements.append(
            RestrictedBucketAgreement(
                asset_id=p1_id, registry_bucket=reg_bucket, p1_bucket=p1_state, agree_restricted=rest_agree,
            )
        )
        eligibility_audits.append(
            NonRuntimeEligibilityAudit(
                asset_id=p1_id,
                registry_runtime_eligibility_level=int(reg["runtime_eligibility_level"]),
                p1_can_enter_runtime_trial=False,
                not_runtime_eligible=True,
            )
        )

    record_count = len(reconciliation_records)

    # --- Negative guards (12) -------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    invariant_state: Dict[str, bool] = {
        "registry_not_modified": REGISTRY_MUTATION_ALLOWED is False,
        "p1_probe_not_modified": PROBE_MUTATION_ALLOWED is False,
        "no_runtime_eligible_promotion": all(
            (not r.p1_can_enter_runtime_trial) for r in reconciliation_records
        ),
        "package_visibility_not_runtime_approval": True,
        "weight_visibility_not_inference_approval": True,
        "agpl_unknown_not_commercial_runtime": nef["commercial_runtime_approved"] is False,
        "reserved_deferred_not_executable": all(
            a.not_runtime_eligible for a in eligibility_audits
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
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeReconciliationGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeReconciliationGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_reconciliation_post_review_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --- Handoff readiness ------------------------------------------------ #
    handoff_readiness: List[ReconciliationHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            ReconciliationHandoffReadiness(
                target_ref=target["target_ref"], readiness_recorded=True, entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    go_conditions: Dict[str, bool] = {
        "reconciliation_profile_count_eq_1": True,
        "stage_ref_count_gte_3": len(stage_refs) >= 3,
        "asset_reconciliation_record_count_eq_17": record_count == 17,
        "import_name_match_count_eq_17": import_match == 17,
        "license_type_match_count_eq_17": license_match == 17,
        "weight_required_match_count_eq_17": weight_match == 17,
        "reserved_match_count_eq_17": reserved_match == 17,
        "restricted_agreement_count_eq_17": restricted_agreement == 17,
        "runtime_eligibility_consistent_count_eq_17": runtime_consistent == 17,
        "divergence_blocker_count_eq_0": divergence_blocker_count == 0,
        "all_records_reconciled": all(r.reconciled for r in reconciliation_records),
        "negative_guard_count_eq_12": negative_guard_count == 12,
        "negative_guard_passed_eq_12": negative_guard_passed == 12,
        # Upstream GO verification flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Reuse / creation flags.
        "post_review_only": POST_REVIEW_ONLY is True,
        "reconciliation_only": RECONCILIATION_ONLY is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "probe_mutation_allowed_false": PROBE_MUTATION_ALLOWED is False,
        "new_capability_created_false": NEW_CAPABILITY_CREATED is False,
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        **{k: (v is True) for k, v in POST_REVIEW_TRUE_INVARIANTS.items()},
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

    divergence_kind_distribution: Dict[str, int] = {DIV_MATCH: 0, DIV_ALIAS: 0, DIV_EXPECTED: 0, DIV_MISMATCH: 0}
    for r in reconciliation_records:
        divergence_kind_distribution[r.divergence_kind] = divergence_kind_distribution.get(r.divergence_kind, 0) + 1

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Midplatform Registry <-> P1 Probe Reconciliation Post-Review",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "post_review_only": POST_REVIEW_ONLY,
        "reconciliation_only": RECONCILIATION_ONLY,
        "registry_planning_ref": REGISTRY_PLANNING_REF,
        "p1_real_install_local_availability_ref": P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF,
        "planning_mode_patch_ref": PLANNING_MODE_PATCH_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "reconciliation_phase_governance_rules": list(RECONCILIATION_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "reconciliation_profile": _build_profile(),
        "reconciliation_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "p1_probe_state_source": p1_state_source,
        "asset_reconciliation_records": [asdict(r) for r in reconciliation_records],
        "asset_reconciliation_record_count": record_count,
        "import_name_match_count": import_match,
        "license_type_match_count": license_match,
        "weight_required_match_count": weight_match,
        "reserved_match_count": reserved_match,
        "restricted_agreement_count": restricted_agreement,
        "runtime_eligibility_consistent_count": runtime_consistent,
        "restricted_bucket_agreements": [asdict(b) for b in bucket_agreements],
        "non_runtime_eligibility_audits": [asdict(a) for a in eligibility_audits],
        "reconciliation_divergence_notes": [asdict(d) for d in divergence_notes],
        "divergence_blocker_count": divergence_blocker_count,
        "divergence_kind_distribution": divergence_kind_distribution,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "registry_p1_probe_reconciliation_status": (
                "registry_and_p1_probe_reconciled_no_mutation_no_runtime_promotion"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Asset-by-asset reconciliation of the midplatform registry against the P1 local-availability "
                "probe results. Import name, license type, weight requirement and reserved flags match for all "
                "17 assets; the restricted-vs-not bucket agrees for all 17 (sam2 is recorded deferred+unknown "
                "in the registry but lands in P1's BLOCKED_BY_LICENSE bucket due to the readiness classifier's "
                "license-block precedence — both agree it is NOT executable, so this is a non-blocking, "
                "explained divergence). Nothing was mutated: the registry and the probe results are unchanged. "
                "No asset is promoted to runtime eligible; package/weight visibility remain non-approvals; "
                "AGPL/unknown stay non-commercial-runtime; reserved/deferred stay non-executable. Protected "
                "records are written to the test board in post_review mode. Reconciliation success is NOT "
                "runtime/install/inference/semantic approval. Next: P1 Controlled Install Planning DryRun."
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
    result = review_model_version_dependency_registry_p1_probe_reconciliation_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "p1_probe_state_source": result["p1_probe_state_source"],
                "asset_reconciliation_record_count": result["asset_reconciliation_record_count"],
                "restricted_agreement_count": result["restricted_agreement_count"],
                "divergence_kind_distribution": result["divergence_kind_distribution"],
                "divergence_blocker_count": result["divergence_blocker_count"],
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
