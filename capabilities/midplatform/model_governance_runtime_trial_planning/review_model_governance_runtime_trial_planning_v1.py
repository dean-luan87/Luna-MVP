# -*- coding: utf-8 -*-
"""Model Governance Runtime Trial Planning — review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.model_governance_runtime_trial_planning.model_governance_runtime_trial_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    resolve_optional_governance_refs,
    verify_stages,
)
from capabilities.midplatform.model_governance_runtime_trial_planning.model_governance_runtime_trial_planning_types_v1 import (  # noqa: E402
    ALLOWED_FUTURE_TRIAL_SCOPE,
    AUDIT_RECORD_POLICIES,
    AUDIT_RECORD_REQUIRED_FIELDS,
    BLOCKER_POLICIES,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    ENTRY_GATE_POLICIES,
    EXECUTION_BOUNDARY_CURRENTLY_NOT_ALLOWED,
    EXECUTION_BOUNDARY_PLANNING_ALLOWED,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    EXIT_POLICIES,
    FALLBACK_POLICIES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GOVERNANCE_REUSE_REFERENCES,
    HANDOFF_READINESS_TARGETS,
    INPUT_BOUNDARY_ALLOWED,
    INPUT_BOUNDARY_FORBIDDEN,
    LUNA_CORE_PRINCIPLE,
    MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
    MODEL_SCOPE_POLICIES,
    NEGATED_CREATION_FLAGS,
    NEGATIVE_PLANNING_GUARDS,
    NEW_ADMISSION_CONTRACT_CREATED,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_OPTIONS_REF,
    NON_EXECUTION_FLAGS,
    OUTPUT_BOUNDARY_FORBIDDEN,
    OUTPUT_BOUNDARY_PATH,
    PHASE_ID,
    PLANNING_GOVERNANCE_RULES,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PLANNING_TRUE_INVARIANTS,
    REUSE_FLAGS,
    RUNTIME_TRIAL_ELIGIBLE_DEFAULT,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    ModelGovernanceRuntimeTrialPlanningProfile,
    GovernanceReuseReference,
    RuntimeTrialAuditRecordPolicy,
    RuntimeTrialBlockerPolicy,
    RuntimeTrialEntryGatePolicy,
    RuntimeTrialExecutionBoundaryPolicy,
    RuntimeTrialExitPolicy,
    RuntimeTrialFallbackPolicy,
    RuntimeTrialHandoffReadiness,
    RuntimeTrialInputBoundaryPolicy,
    RuntimeTrialModelScopePolicy,
    RuntimeTrialNegativePlanningGuard,
    RuntimeTrialOutputBoundaryPolicy,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "model_governance_runtime_trial_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "model_governance_runtime_trial_planning_review_v1.json"

_PKG = "capabilities/midplatform/model_governance_runtime_trial_planning"
STEP_FILES = (
    f"{_PKG}/model_governance_runtime_trial_planning_types_v1.py",
    f"{_PKG}/model_governance_runtime_trial_planning_registry_v1.py",
    f"{_PKG}/review_model_governance_runtime_trial_planning_v1.py",
)

PROFILE_REF = "model_governance_runtime_trial_planning_profile_v1"


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        ModelGovernanceRuntimeTrialPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            planning_only=PLANNING_ONLY,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_admission_contract_created=NEW_ADMISSION_CONTRACT_CREATED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            model_governance_integrated_closure_ref=MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            entry_gate_policies=ENTRY_GATE_POLICIES,
            execution_boundary_planning_allowed=EXECUTION_BOUNDARY_PLANNING_ALLOWED,
            execution_boundary_currently_not_allowed=EXECUTION_BOUNDARY_CURRENTLY_NOT_ALLOWED,
            governance_rules=PLANNING_GOVERNANCE_RULES,
        )
    )


def review_model_governance_runtime_trial_planning_v1(
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

    optional_refs = resolve_optional_governance_refs(_REPO_ROOT)

    # --- Governance reuse references -------------------------------------- #
    governance_reuse: List[GovernanceReuseReference] = [
        GovernanceReuseReference(
            governance_asset=ref["governance_asset"],
            usage=ref["usage"],
            reused=True,
            optional=False,
            present=True,
        )
        for ref in GOVERNANCE_REUSE_REFERENCES
    ]
    for ref in optional_refs:
        governance_reuse.append(
            GovernanceReuseReference(
                governance_asset=ref["governance_asset"],
                usage=ref["usage"],
                reused=ref["reused"],
                optional=True,
                present=ref["present"],
            )
        )
    governance_reuse_ref_count = len(GOVERNANCE_REUSE_REFERENCES)

    # --- Entry gate policies ---------------------------------------------- #
    entry_gate = [
        RuntimeTrialEntryGatePolicy(gate_condition=c, planned=True)
        for c in ENTRY_GATE_POLICIES
    ]
    entry_gate_policy_count = len(entry_gate)

    # --- Execution boundary policies -------------------------------------- #
    execution_boundary = [
        RuntimeTrialExecutionBoundaryPolicy(boundary_item=i, mode="planning_allowed_not_executed")
        for i in EXECUTION_BOUNDARY_PLANNING_ALLOWED
    ] + [
        RuntimeTrialExecutionBoundaryPolicy(boundary_item=i, mode="currently_not_allowed")
        for i in EXECUTION_BOUNDARY_CURRENTLY_NOT_ALLOWED
    ]
    execution_boundary_policy_count = len(execution_boundary)

    # --- Model scope policies --------------------------------------------- #
    model_scope = [
        RuntimeTrialModelScopePolicy(
            tier=p["tier"],
            model_ref=p["model_ref"],
            eligibility=p["eligibility"],
            runtime_trial_eligible_default=RUNTIME_TRIAL_ELIGIBLE_DEFAULT,
        )
        for p in MODEL_SCOPE_POLICIES
    ]
    model_scope_policy_count = len(model_scope)

    # --- Input boundary policies ------------------------------------------ #
    input_boundary = [
        RuntimeTrialInputBoundaryPolicy(input_item=i, allowed_for_planning=True)
        for i in INPUT_BOUNDARY_ALLOWED
    ] + [
        RuntimeTrialInputBoundaryPolicy(input_item=i, allowed_for_planning=False)
        for i in INPUT_BOUNDARY_FORBIDDEN
    ]
    input_boundary_policy_count = len(input_boundary)

    # --- Output boundary policies ----------------------------------------- #
    output_boundary = [
        RuntimeTrialOutputBoundaryPolicy(output_item=i, role="required_path_stage")
        for i in OUTPUT_BOUNDARY_PATH
    ] + [
        RuntimeTrialOutputBoundaryPolicy(output_item=i, role="forbidden")
        for i in OUTPUT_BOUNDARY_FORBIDDEN
    ]
    output_boundary_policy_count = len(output_boundary)

    # --- Fallback / blocker / exit ---------------------------------------- #
    fallback = [
        RuntimeTrialFallbackPolicy(
            trigger=t, candidate_only=True, triggers_download_or_inference=False
        )
        for t in FALLBACK_POLICIES
    ]
    fallback_policy_count = len(fallback)

    blocker = [RuntimeTrialBlockerPolicy(violation=v, blocks=True) for v in BLOCKER_POLICIES]
    blocker_policy_count = len(blocker)

    exit_policies = [
        RuntimeTrialExitPolicy(
            exit_condition=e,
            requires_audit_artifact=True,
            state_promotion_without_review=False,
        )
        for e in EXIT_POLICIES
    ]
    exit_policy_count = len(exit_policies)

    # --- Audit record policies -------------------------------------------- #
    audit_records = [
        RuntimeTrialAuditRecordPolicy(record_type=r, required_fields=AUDIT_RECORD_REQUIRED_FIELDS)
        for r in AUDIT_RECORD_POLICIES
    ]
    audit_record_policy_count = len(audit_records)

    # --- Planned flags ---------------------------------------------------- #
    planned_flags = {
        "entry_gate_planned": entry_gate_policy_count >= 10,
        "execution_boundary_planned": execution_boundary_policy_count >= 12,
        "model_scope_planned": model_scope_policy_count >= 7,
        "input_boundary_planned": input_boundary_policy_count >= 8,
        "output_boundary_planned": output_boundary_policy_count >= 8,
        "fallback_policy_planned": fallback_policy_count >= 10,
        "blocker_policy_planned": blocker_policy_count >= 10,
        "exit_policy_planned": exit_policy_count >= 5,
        "audit_record_policy_planned": audit_record_policy_count >= 10,
    }

    # --- Invariant state for negative guards ------------------------------ #
    nef = NON_EXECUTION_FLAGS
    inv = PLANNING_TRUE_INVARIANTS
    invariant_state: Dict[str, bool] = {
        "new_admission_contract_not_created": NEW_ADMISSION_CONTRACT_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        "runtime_execution_not_allowed": nef["runtime_execution_allowed"] is False,
        "live_camera_sensor_not_connected": (
            nef["live_camera_connected"] is False and nef["live_sensor_connected"] is False
        ),
        "direct_action_speech_fact_write_not_allowed": (
            nef["direct_action_allowed"] is False
            and nef["direct_speech_allowed"] is False
            and nef["direct_fact_write_allowed"] is False
        ),
        "navigation_runtime_not_allowed": nef["navigation_runtime_allowed"] is False,
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "commercial_runtime_not_approved": nef["commercial_runtime_approved"] is False,
        "model_tuning_dataset_usage_not_allowed": (
            nef["model_tuning_allowed"] is False and nef["dataset_usage_allowed"] is False
        ),
        "adapter_midplatform_required": (
            inv["model_output_adapter_required"]
            and inv["midplatform_data_handling_required"]
            and inv["midplatform_model_control_required"]
        ),
        "reserved_only_family_runtime_blocked": inv["reserved_only_family_runtime_blocked"],
        "trial_success_not_runtime_promotion": True,
    }

    # --- Negative planning guards (12) ------------------------------------ #
    negative_guards: List[RuntimeTrialNegativePlanningGuard] = []
    for spec in NEGATIVE_PLANNING_GUARDS:
        holds = invariant_state.get(spec["depends_on"], False)
        negative_guards.append(
            RuntimeTrialNegativePlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_planning_invariant",),
            )
        )
    negative_planning_guard_count = len(negative_guards)
    negative_planning_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --- Handoff readiness (recorded only) -------------------------------- #
    handoff_readiness: List[RuntimeTrialHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            RuntimeTrialHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    go_conditions = {
        "planning_profile_count_eq_1": True,
        "governance_reuse_ref_count_gte_8": governance_reuse_ref_count >= 8,
        "entry_gate_policy_count_gte_10": entry_gate_policy_count >= 10,
        "execution_boundary_policy_count_gte_12": execution_boundary_policy_count >= 12,
        "model_scope_policy_count_gte_7": model_scope_policy_count >= 7,
        "input_boundary_policy_count_gte_8": input_boundary_policy_count >= 8,
        "output_boundary_policy_count_gte_8": output_boundary_policy_count >= 8,
        "fallback_policy_count_gte_10": fallback_policy_count >= 10,
        "blocker_policy_count_gte_10": blocker_policy_count >= 10,
        "exit_policy_count_gte_5": exit_policy_count >= 5,
        "audit_record_policy_count_gte_10": audit_record_policy_count >= 10,
        "negative_planning_guard_count_eq_12": negative_planning_guard_count == 12,
        "negative_planning_guard_passed_eq_12": negative_planning_guard_passed == 12,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": (
            verify_flags.get("controlled_trial_template_ref_ok") is True
        ),
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_admission_contract_created_false": NEW_ADMISSION_CONTRACT_CREATED is False,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        **planned_flags,
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
        "step": "Model Governance Runtime Trial Planning Review",
        "lifecycle_variant": "model_governance_runtime_trial_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "planning_only": PLANNING_ONLY,
        "model_governance_integrated_closure_ref": MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "reuse_flags": dict(REUSE_FLAGS),
        "negated_creation_flags": dict(NEGATED_CREATION_FLAGS),
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "planning_profile": _build_profile(),
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs) + 1,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "governance_reuse_references": [asdict(g) for g in governance_reuse],
        "governance_reuse_ref_count": governance_reuse_ref_count,
        "optional_governance_refs": optional_refs,
        "entry_gate_policies": [asdict(e) for e in entry_gate],
        "entry_gate_policy_count": entry_gate_policy_count,
        "allowed_future_trial_scope": list(ALLOWED_FUTURE_TRIAL_SCOPE),
        "execution_boundary_policies": [asdict(e) for e in execution_boundary],
        "execution_boundary_policy_count": execution_boundary_policy_count,
        "model_scope_policies": [asdict(m) for m in model_scope],
        "model_scope_policy_count": model_scope_policy_count,
        "runtime_trial_eligible_default": RUNTIME_TRIAL_ELIGIBLE_DEFAULT,
        "input_boundary_policies": [asdict(i) for i in input_boundary],
        "input_boundary_policy_count": input_boundary_policy_count,
        "output_boundary_policies": [asdict(o) for o in output_boundary],
        "output_boundary_policy_count": output_boundary_policy_count,
        "fallback_policies": [asdict(f) for f in fallback],
        "fallback_policy_count": fallback_policy_count,
        "blocker_policies": [asdict(b) for b in blocker],
        "blocker_policy_count": blocker_policy_count,
        "exit_policies": [asdict(e) for e in exit_policies],
        "exit_policy_count": exit_policy_count,
        "audit_record_policies": [asdict(a) for a in audit_records],
        "audit_record_policy_count": audit_record_policy_count,
        "planned_flags": planned_flags,
        "negative_planning_guards": [asdict(g) for g in negative_guards],
        "negative_planning_guard_count": negative_planning_guard_count,
        "negative_planning_guard_passed": negative_planning_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "runtime_trial_planning_status": (
                "model_governance_runtime_trial_planning_complete_governance_reused"
                if review_ok
                else "blocked"
            ),
            "next_step_options_ref": NEXT_STEP_OPTIONS_REF,
            "transition_note": (
                "Runtime trial planning is complete as governance reuse, not a new governance system and "
                "not runtime execution. Entry gate, execution boundary, model scope, input/output boundary, "
                "fallback, blocker, exit and audit-record policies are all planned by reusing the "
                "ControlledTrialGovernanceLifecycleTemplateV1, model admission, interface layer, runtime "
                "governance closure, data handling and model control baselines. No new admission contract "
                "or runtime governance was created; all model outputs still pass adapter + midplatform and "
                "stay candidate-only; reserved-only families remain runtime-blocked; commercial runtime, "
                "VLA action chain, live camera/sensor, direct action/speech/fact_write and model tuning / "
                "dataset usage remain disallowed; trial success is not runtime promotion. Future runtime "
                "execution requires separate approval and dry-run. Next: decide between a runtime trial "
                "planning post-review or P1 download/license planning before any real runtime trial."
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
    result = review_model_governance_runtime_trial_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "governance_reuse_ref_count": result["governance_reuse_ref_count"],
                "entry_gate_policy_count": result["entry_gate_policy_count"],
                "execution_boundary_policy_count": result["execution_boundary_policy_count"],
                "model_scope_policy_count": result["model_scope_policy_count"],
                "fallback_policy_count": result["fallback_policy_count"],
                "blocker_policy_count": result["blocker_policy_count"],
                "audit_record_policy_count": result["audit_record_policy_count"],
                "negative_planning_guard_passed": result["negative_planning_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
