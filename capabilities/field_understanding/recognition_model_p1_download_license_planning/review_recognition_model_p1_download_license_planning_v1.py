# -*- coding: utf-8 -*-
"""Recognition Model P1 Download / License Planning — review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_p1_download_license_planning.recognition_model_p1_download_license_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    verify_stages,
)
from capabilities.field_understanding.recognition_model_p1_download_license_planning.recognition_model_p1_download_license_planning_types_v1 import (  # noqa: E402
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    DOWNLOAD_ELIGIBILITY_POLICY,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FALLBACK_STRATEGIES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    LICENSE_DECISION_MATRIX,
    LUNA_CORE_PRINCIPLE,
    MODEL_ASSET_MATRIX,
    MODEL_FAMILY_TIERS,
    MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
    NEGATED_CREATION_FLAGS,
    NEGATIVE_GUARDS,
    NEW_ADMISSION_CONTRACT_CREATED,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_OPTIONS_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PLANNING_GOVERNANCE_RULES,
    PLANNING_MODE,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PLANNING_TRUE_INVARIANTS,
    REUSE_FLAGS,
    RUNTIME_ELIGIBILITY_LEVELS,
    RUNTIME_TRIAL_PLANNING_REF,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TIER_LEVEL_SNAPSHOT,
    AvailabilityState,
    DependencyProfile,
    DownloadEligibility,
    ExecutionConstraint,
    FallbackStrategy,
    LicenseContract,
    ModelAsset,
    P1DownloadLicensePlanningHandoffReadiness,
    P1DownloadLicensePlanningNegativeGuard,
    RecognitionModelP1DownloadLicensePlanningProfile,
    RuntimeEligibilityLevel,
    RuntimeFeasibility,
    candidate_to_dict,
    license_class_for,
    license_decision_for,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "recognition_model_p1_download_license_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_p1_download_license_planning_review_v1.json"

_PKG = "capabilities/field_understanding/recognition_model_p1_download_license_planning"
STEP_FILES = (
    f"{_PKG}/recognition_model_p1_download_license_planning_types_v1.py",
    f"{_PKG}/recognition_model_p1_download_license_planning_registry_v1.py",
    f"{_PKG}/review_recognition_model_p1_download_license_planning_v1.py",
)

PROFILE_REF = "recognition_model_p1_download_license_planning_profile_v1"

_LEVEL_LABEL: Dict[int, str] = {row["level"]: row["label"] for row in RUNTIME_ELIGIBILITY_LEVELS}


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelP1DownloadLicensePlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_mode=PLANNING_MODE,
            planning_only=PLANNING_ONLY,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_admission_contract_created=NEW_ADMISSION_CONTRACT_CREATED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            runtime_trial_planning_ref=RUNTIME_TRIAL_PLANNING_REF,
            model_governance_integrated_closure_ref=MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            download_eligibility_policy=dict(DOWNLOAD_ELIGIBILITY_POLICY),
            tier_level_snapshot=dict(TIER_LEVEL_SNAPSHOT),
            governance_rules=PLANNING_GOVERNANCE_RULES,
        )
    )


def review_recognition_model_p1_download_license_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
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

    # --- Runtime eligibility levels (5) ----------------------------------- #
    eligibility_levels = [
        RuntimeEligibilityLevel(
            level=row["level"],
            label=row["label"],
            description=row["description"],
            runtime_now=False,
        )
        for row in RUNTIME_ELIGIBILITY_LEVELS
    ]
    runtime_eligibility_level_count = len(eligibility_levels)

    # --- Per-asset derived records ---------------------------------------- #
    model_assets: List[ModelAsset] = []
    license_contracts: List[LicenseContract] = []
    runtime_feasibilities: List[RuntimeFeasibility] = []
    download_eligibilities: List[DownloadEligibility] = []
    dependency_profiles: List[DependencyProfile] = []
    execution_constraints: List[ExecutionConstraint] = []
    availability_states: List[AvailabilityState] = []

    matrix_issues: List[str] = []
    for row in MODEL_ASSET_MATRIX:
        mid = row["model_id"]
        decision = license_decision_for(row["license_type"])
        klass = license_class_for(row["license_type"])
        level = int(row["runtime_eligibility_level"])
        is_reserved = row["availability_state"] == "reserved_only"

        # runtime_eligible flag = license-eligible AND not reserved AND level>=2.
        runtime_eligible = bool(decision["runtime_eligible"]) and (not is_reserved) and level >= 2

        model_assets.append(
            ModelAsset(
                model_id=mid,
                tier_code=row["tier_code"],
                family=row["family"],
                license_type=row["license_type"],
                availability_state=row["availability_state"],
                runtime_eligibility_level=level,
                runtime_eligibility_label=_LEVEL_LABEL.get(level, "unknown"),
                download_allowed=bool(DOWNLOAD_ELIGIBILITY_POLICY["download_allowed"]),
                runtime_eligible=runtime_eligible,
                note=row["note"],
            )
        )
        license_contracts.append(
            LicenseContract(
                model_id=mid,
                license_type=row["license_type"],
                license_class=klass,
                runtime_eligible=bool(decision["runtime_eligible"]),
                commercial_runtime_allowed=bool(decision["commercial_runtime_allowed"]),
                decision=decision["decision"],
            )
        )
        runtime_feasibilities.append(
            RuntimeFeasibility(
                model_id=mid,
                runtime_eligibility_level=level,
                cpu_runnable=bool(row["cpu_runnable"]),
                gpu_preferred=bool(row["gpu_preferred"]),
                feasible_for_test_only=level >= 2,
                runtime_execution_now=False,
            )
        )
        download_eligibilities.append(
            DownloadEligibility(
                model_id=mid,
                download_allowed=bool(DOWNLOAD_ELIGIBILITY_POLICY["download_allowed"]),
                auto_download=False,
                requires_review=(klass == "unknown" or row["availability_state"] == "requires_license_review"),
                only_planning_state_transition=True,
            )
        )
        dependency_profiles.append(
            DependencyProfile(
                model_id=mid,
                dependency_weight=row["dependency_weight"],
                dependency_stable=bool(row["dependency_stable"]),
                deferred_for_dependency=row["availability_state"] == "deferred",
            )
        )
        execution_constraints.append(
            ExecutionConstraint(
                model_id=mid,
                no_runtime_execution=True,
                no_real_inference=True,
                no_auto_download=True,
                must_pass_adapter_and_midplatform=True,
                candidate_only=True,
            )
        )
        availability_states.append(
            AvailabilityState(
                model_id=mid,
                state=row["availability_state"],
                runtime_eligibility_level=level,
            )
        )

        # Matrix consistency guards.
        if is_reserved and level != 0:
            matrix_issues.append(f"reserved_only_not_level0:{mid}")
        if klass == "unknown" and runtime_eligible:
            matrix_issues.append(f"unknown_license_runtime_eligible:{mid}")
        if klass == "agpl" and decision["commercial_runtime_allowed"]:
            matrix_issues.append(f"agpl_commercial_runtime_allowed:{mid}")
        if level == 4:
            matrix_issues.append(f"level4_full_runtime_now:{mid}")

    failed_checks.extend(matrix_issues)

    model_asset_count = len(model_assets)
    license_contract_count = len(license_contracts)
    runtime_feasibility_count = len(runtime_feasibilities)
    download_eligibility_count = len(download_eligibilities)
    dependency_profile_count = len(dependency_profiles)
    execution_constraint_count = len(execution_constraints)
    availability_state_count = len(availability_states)
    model_family_tier_count = len(MODEL_FAMILY_TIERS)
    license_decision_matrix_count = len(LICENSE_DECISION_MATRIX)

    # --- Fallback strategies ---------------------------------------------- #
    fallback_strategies = [
        FallbackStrategy(
            trigger=f["trigger"],
            fallback_route=f["fallback_route"],
            candidate_only=True,
            triggers_download_or_inference=False,
        )
        for f in FALLBACK_STRATEGIES
    ]
    fallback_strategy_count = len(fallback_strategies)

    # --- Invariant state for negative guards ------------------------------ #
    nef = NON_EXECUTION_FLAGS
    inv = PLANNING_TRUE_INVARIANTS
    invariant_state: Dict[str, bool] = {
        "real_inference_not_allowed": nef["real_inference_allowed"] is False,
        "dataset_download_not_allowed": (
            nef["dataset_download_allowed"] is False and nef["dataset_pull_allowed"] is False
        ),
        "auto_model_pull_not_allowed": (
            nef["auto_model_pull_allowed"] is False and nef["auto_download_allowed"] is False
        ),
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "semantic_promotion_not_allowed": nef["semantic_promotion_allowed"] is False,
        "runtime_escalation_not_allowed": (
            nef["runtime_escalation_allowed"] is False and nef["runtime_execution_allowed"] is False
        ),
        "governance_reuse_preserved": (
            inv["governance_reuse_preserved"]
            and inv["model_output_adapter_required"]
            and inv["midplatform_data_handling_required"]
            and inv["midplatform_model_control_required"]
            and NEW_ADMISSION_CONTRACT_CREATED is False
            and NEW_RUNTIME_GOVERNANCE_CREATED is False
        ),
    }

    negative_guards: List[P1DownloadLicensePlanningNegativeGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = invariant_state.get(spec["depends_on"], False)
        negative_guards.append(
            P1DownloadLicensePlanningNegativeGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --- Handoff readiness (recorded only) -------------------------------- #
    handoff_readiness: List[P1DownloadLicensePlanningHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            P1DownloadLicensePlanningHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    go_conditions = {
        "planning_profile_count_eq_1": True,
        "model_family_tier_count_eq_7": model_family_tier_count == 7,
        "model_asset_count_gte_15": model_asset_count >= 15,
        "license_contract_count_eq_asset_count": license_contract_count == model_asset_count,
        "license_decision_matrix_count_eq_4": license_decision_matrix_count == 4,
        "runtime_eligibility_level_count_eq_5": runtime_eligibility_level_count == 5,
        "runtime_feasibility_count_eq_asset_count": runtime_feasibility_count == model_asset_count,
        "download_eligibility_count_eq_asset_count": download_eligibility_count == model_asset_count,
        "dependency_profile_count_eq_asset_count": dependency_profile_count == model_asset_count,
        "execution_constraint_count_eq_asset_count": execution_constraint_count == model_asset_count,
        "availability_state_count_eq_asset_count": availability_state_count == model_asset_count,
        "fallback_strategy_count_gte_6": fallback_strategy_count >= 6,
        "negative_guard_count_eq_7": negative_guard_count == 7,
        "negative_guard_passed_eq_7": negative_guard_passed == 7,
        "matrix_consistency_ok": len(matrix_issues) == 0,
        "download_allowed_true": DOWNLOAD_ELIGIBILITY_POLICY["download_allowed"] is True,
        "no_auto_download": DOWNLOAD_ELIGIBILITY_POLICY["no_auto_download"] is True,
        "no_runtime_execution": DOWNLOAD_ELIGIBILITY_POLICY["no_runtime_execution"] is True,
        "no_dataset_pull": DOWNLOAD_ELIGIBILITY_POLICY["no_dataset_pull"] is True,
        "only_planning_state_transition": DOWNLOAD_ELIGIBILITY_POLICY["only_planning_state_transition"] is True,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": (
            verify_flags.get("controlled_trial_template_ref_ok") is True
        ),
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_admission_contract_created_false": NEW_ADMISSION_CONTRACT_CREATED is False,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        **{k: (v is True) for k, v in PLANNING_TRUE_INVARIANTS.items()},
        **negative_guard_go,
        **handoff_go,
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Recognition Model P1 Download / License Planning Review",
        "lifecycle_variant": "recognition_model_p1_download_license_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "planning_mode": PLANNING_MODE,
        "planning_only": PLANNING_ONLY,
        "runtime_trial_planning_ref": RUNTIME_TRIAL_PLANNING_REF,
        "model_governance_integrated_closure_ref": MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "reuse_flags": dict(REUSE_FLAGS),
        "negated_creation_flags": dict(NEGATED_CREATION_FLAGS),
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "download_eligibility_policy": dict(DOWNLOAD_ELIGIBILITY_POLICY),
        "tier_level_snapshot": dict(TIER_LEVEL_SNAPSHOT),
        "planning_profile": _build_profile(),
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs) + 1,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "model_family_tiers": [dict(t) for t in MODEL_FAMILY_TIERS],
        "model_family_tier_count": model_family_tier_count,
        "model_assets": [asdict(m) for m in model_assets],
        "model_asset_count": model_asset_count,
        "license_decision_matrix": [dict(r) for r in LICENSE_DECISION_MATRIX],
        "license_decision_matrix_count": license_decision_matrix_count,
        "license_contracts": [asdict(c) for c in license_contracts],
        "license_contract_count": license_contract_count,
        "runtime_eligibility_levels": [asdict(l) for l in eligibility_levels],
        "runtime_eligibility_level_count": runtime_eligibility_level_count,
        "runtime_feasibilities": [asdict(r) for r in runtime_feasibilities],
        "runtime_feasibility_count": runtime_feasibility_count,
        "download_eligibilities": [asdict(d) for d in download_eligibilities],
        "download_eligibility_count": download_eligibility_count,
        "dependency_profiles": [asdict(d) for d in dependency_profiles],
        "dependency_profile_count": dependency_profile_count,
        "execution_constraints": [asdict(e) for e in execution_constraints],
        "execution_constraint_count": execution_constraint_count,
        "availability_states": [asdict(a) for a in availability_states],
        "availability_state_count": availability_state_count,
        "fallback_strategies": [asdict(f) for f in fallback_strategies],
        "fallback_strategy_count": fallback_strategy_count,
        "matrix_issues": matrix_issues,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "p1_download_license_planning_status": (
                "p1_p2_models_converged_into_runnable_asset_list_planning_only"
                if review_ok
                else "blocked"
            ),
            "next_step_options_ref": NEXT_STEP_OPTIONS_REF,
            "transition_note": (
                "P1/P2 recognition models are converged from a planning state into a runnable-asset list. "
                "Each ModelAsset carries its LicenseContract, RuntimeFeasibility, DownloadEligibility, "
                "DependencyProfile, ExecutionConstraint, FallbackStrategy and AvailabilityState. This is "
                "planning-only convergence: download_allowed is a planning decision (no auto-download, no "
                "runtime execution, no dataset pull, only a planning state transition). License decides "
                "runtime eligibility (Apache/MIT runtime eligible; AGPL test-only/no commercial runtime; "
                "Unknown blocked until review; research-only datasets no runtime ingestion). Reserved-only "
                "families stay runtime-blocked; full runtime (Level 4) is not now. All model outputs still "
                "pass adapter + midplatform and stay candidate-only; governance is reused with no bypass. "
                "Next: Phase-P1-Execution-DryRun-Foundation-v1-001 (P1 runnable-environment simulator, "
                "dependency-graph verification, runtime-feasibility mock executor, model switching & "
                "fallback simulation) — still a dry-run, no real download/inference/runtime."
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

    return result


def main() -> int:
    result = review_recognition_model_p1_download_license_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "model_family_tier_count": result["model_family_tier_count"],
                "model_asset_count": result["model_asset_count"],
                "license_contract_count": result["license_contract_count"],
                "license_decision_matrix_count": result["license_decision_matrix_count"],
                "runtime_eligibility_level_count": result["runtime_eligibility_level_count"],
                "fallback_strategy_count": result["fallback_strategy_count"],
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
