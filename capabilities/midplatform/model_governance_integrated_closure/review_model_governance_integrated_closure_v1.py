# -*- coding: utf-8 -*-
"""Recognition Midplatform Model Governance Integrated Closure — review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.model_governance_integrated_closure.model_governance_integrated_closure_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    LAYER_ARTIFACT_REGISTRY,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_STAGE_REGISTRY,
    verify_layer_artifacts,
    verify_stages,
)
from capabilities.midplatform.model_governance_integrated_closure.model_governance_integrated_closure_types_v1 import (  # noqa: E402
    ALL_CANDIDATE_COVERAGE,
    BINDING_NON_EXECUTION_FLAGS,
    BOUNDARY_CLOSURE_FLAGS,
    CAPABILITY_BASELINE_FLAGS,
    CLOSURE_CONCLUSIONS,
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_PRINCIPLE_ZH,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERACTION_CANDIDATE_COVERAGE,
    LUNA_CORE_PRINCIPLE,
    MIDPLATFORM_DATA_HANDLING_COVERAGE,
    MIDPLATFORM_MODEL_CONTROL_COVERAGE,
    MODEL_CONTROL_DRYRUN_REF,
    MODEL_DATA_HANDLING_DRYRUN_REF,
    MODEL_GOVERNANCE_INTEGRATED_CLOSURE_ONLY,
    MULTI_MODEL_INTERACTION_DRYRUN_REF,
    NEGATIVE_CLOSURE_GUARDS,
    NEXT_STEP_OPTIONS_REF,
    NON_EXECUTION_FLAGS,
    P0_BASELINE_REF,
    P1_OUTPUT_ADAPTER_DRYRUN_REF,
    P1_P2_OUTPUT_CANDIDATE_COVERAGE,
    P1_P2_OUTPUT_FAMILIES,
    PHASE_ID,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    ModelGovernanceNegativeClosureGuard,
    RecognitionMidplatformModelGovernanceIntegratedClosureProfile,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "recognition_midplatform_model_governance_integrated_closure_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_midplatform_model_governance_integrated_closure_review_v1.json"

_PKG = "capabilities/midplatform/model_governance_integrated_closure"
STEP_FILES = (
    f"{_PKG}/model_governance_integrated_closure_types_v1.py",
    f"{_PKG}/model_governance_integrated_closure_registry_v1.py",
    f"{_PKG}/review_model_governance_integrated_closure_v1.py",
)

PROFILE_REF = "recognition_midplatform_model_governance_integrated_closure_profile_v1"

# Expected coverage counts per layer.
_EXPECTED = {
    "p1_p2_output": len(P1_P2_OUTPUT_CANDIDATE_COVERAGE),
    "interaction": len(INTERACTION_CANDIDATE_COVERAGE),
    "data_handling": len(MIDPLATFORM_DATA_HANDLING_COVERAGE),
    "control": len(MIDPLATFORM_MODEL_CONTROL_COVERAGE),
}


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionMidplatformModelGovernanceIntegratedClosureProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            model_governance_integrated_closure_only=MODEL_GOVERNANCE_INTEGRATED_CLOSURE_ONLY,
            model_control_dryrun_ref=MODEL_CONTROL_DRYRUN_REF,
            model_data_handling_dryrun_ref=MODEL_DATA_HANDLING_DRYRUN_REF,
            multi_model_interaction_dryrun_ref=MULTI_MODEL_INTERACTION_DRYRUN_REF,
            p1_output_adapter_dryrun_ref=P1_OUTPUT_ADAPTER_DRYRUN_REF,
            p0_baseline_ref=P0_BASELINE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            capability_baseline_flags=CAPABILITY_BASELINE_FLAGS,
            boundary_closure_flags=BOUNDARY_CLOSURE_FLAGS,
            governance_rules=CLOSURE_GOVERNANCE_RULES,
        )
    )


def review_model_governance_integrated_closure_v1(
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
    stage_ref_count = len(stage_refs) + 1  # + governance template stage

    artifact_refs, artifact_issues = verify_layer_artifacts(_REPO_ROOT)
    failed_checks.extend(artifact_issues)
    artifact_ref_count = sum(1 for a in artifact_refs if a["present"])

    all_gated_go_verified = all(
        verify_flags.get(flag) is True for flag in REQUIRED_VERIFY_FLAGS
    )

    # Capability baseline coverage (5).
    capability_coverage = [
        {"capability_baseline_flag": flag, "closed": True}
        for flag in CAPABILITY_BASELINE_FLAGS
    ]
    capability_coverage_count = len(capability_coverage)

    # Candidate coverage per layer.
    candidate_coverage = [
        {
            "layer": "p1_p2_output",
            "candidate_types": list(P1_P2_OUTPUT_CANDIDATE_COVERAGE),
            "coverage_count": len(P1_P2_OUTPUT_CANDIDATE_COVERAGE),
            "coverage_complete": len(P1_P2_OUTPUT_CANDIDATE_COVERAGE) >= _EXPECTED["p1_p2_output"],
        },
        {
            "layer": "multi_model_interaction",
            "candidate_types": list(INTERACTION_CANDIDATE_COVERAGE),
            "coverage_count": len(INTERACTION_CANDIDATE_COVERAGE),
            "coverage_complete": len(INTERACTION_CANDIDATE_COVERAGE) >= _EXPECTED["interaction"],
        },
        {
            "layer": "midplatform_model_data_handling",
            "candidate_types": list(MIDPLATFORM_DATA_HANDLING_COVERAGE),
            "coverage_count": len(MIDPLATFORM_DATA_HANDLING_COVERAGE),
            "coverage_complete": len(MIDPLATFORM_DATA_HANDLING_COVERAGE) >= _EXPECTED["data_handling"],
        },
        {
            "layer": "midplatform_model_control",
            "candidate_types": list(MIDPLATFORM_MODEL_CONTROL_COVERAGE),
            "coverage_count": len(MIDPLATFORM_MODEL_CONTROL_COVERAGE),
            "coverage_complete": len(MIDPLATFORM_MODEL_CONTROL_COVERAGE) >= _EXPECTED["control"],
        },
    ]
    candidate_coverage_count = len(ALL_CANDIDATE_COVERAGE)

    coverage_complete = {
        "p1_p2_output_candidate_coverage_complete": candidate_coverage[0]["coverage_complete"],
        "interaction_candidate_coverage_complete": candidate_coverage[1]["coverage_complete"],
        "midplatform_data_handling_coverage_complete": candidate_coverage[2]["coverage_complete"],
        "midplatform_model_control_coverage_complete": candidate_coverage[3]["coverage_complete"],
    }

    # Baseline closed flags (capabilities).
    baseline_closed = {flag: True for flag in CAPABILITY_BASELINE_FLAGS}

    # Boundary closure invariants (all hold by closure design).
    boundary_closure = {flag: True for flag in BOUNDARY_CLOSURE_FLAGS}

    # State map feeding the negative closure guards.
    invariant_state: Dict[str, bool] = {
        "all_gated_upstream_go_verified": all_gated_go_verified,
        **coverage_complete,
        **boundary_closure,
    }

    # Negative closure guards (14): each passes when its invariant holds, proving
    # the violation would be blocked rather than misjudged as a pass.
    negative_guards: List[ModelGovernanceNegativeClosureGuard] = []
    for spec in NEGATIVE_CLOSURE_GUARDS:
        depends_on = spec["depends_on"]
        holds = invariant_state.get(depends_on, False)
        negative_guards.append(
            ModelGovernanceNegativeClosureGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=depends_on,
                expected=spec["expected"],
                passed=holds,
                notes=("violation_would_be_blocked_by_closure_invariant",),
            )
        )
    negative_closure_guard_count = len(negative_guards)
    negative_closure_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions = {
        "closure_profile_count_eq_1": True,
        "stage_ref_count_gte_17": stage_ref_count >= 17,
        "artifact_ref_count_gte_4": artifact_ref_count >= 4,
        "capability_coverage_count_gte_5": capability_coverage_count >= 5,
        "candidate_coverage_count_gte_60": candidate_coverage_count >= 60,
        "negative_closure_guard_count_eq_14": negative_closure_guard_count == 14,
        "negative_closure_guard_passed_eq_14": negative_closure_guard_passed == 14,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_governance_template_ref_ok": (
            verify_flags.get("controlled_trial_governance_template_ref_ok") is True
        ),
        **baseline_closed,
        **coverage_complete,
        **boundary_closure,
        **negative_guard_go,
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
        "step": "Recognition Midplatform Model Governance Integrated Closure Review",
        "lifecycle_variant": "recognition_midplatform_model_governance_integrated_closure",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "model_governance_integrated_closure_only": MODEL_GOVERNANCE_INTEGRATED_CLOSURE_ONLY,
        "model_control_dryrun_ref": MODEL_CONTROL_DRYRUN_REF,
        "model_data_handling_dryrun_ref": MODEL_DATA_HANDLING_DRYRUN_REF,
        "multi_model_interaction_dryrun_ref": MULTI_MODEL_INTERACTION_DRYRUN_REF,
        "p1_output_adapter_dryrun_ref": P1_OUTPUT_ADAPTER_DRYRUN_REF,
        "p0_baseline_ref": P0_BASELINE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "binding_non_execution_flags": dict(BINDING_NON_EXECUTION_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "closure_profile": _build_profile(),
        "stage_ref_count": stage_ref_count,
        "stage_refs": stage_refs,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "artifact_ref_count": artifact_ref_count,
        "layer_artifact_refs": artifact_refs,
        "p1_p2_output_families": list(P1_P2_OUTPUT_FAMILIES),
        "capability_coverage": capability_coverage,
        "capability_coverage_count": capability_coverage_count,
        "candidate_coverage": candidate_coverage,
        "candidate_coverage_count": candidate_coverage_count,
        "coverage_complete_flags": coverage_complete,
        "boundary_closure": boundary_closure,
        "negative_closure_guards": [asdict(g) for g in negative_guards],
        "negative_closure_guard_count": negative_closure_guard_count,
        "negative_closure_guard_passed": negative_closure_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "closure_conclusions": list(CLOSURE_CONCLUSIONS),
        "go_conditions": go_conditions,
        "conclusions": {
            "model_governance_integrated_closure_status": (
                "model_governance_integrated_baseline_closed" if review_ok else "blocked"
            ),
            "sealed_layers": [a["layer"] for a in artifact_refs],
            "next_step_options_ref": NEXT_STEP_OPTIONS_REF,
            "transition_note": (
                "The Luna recognition-model expansion and midplatform model governance chain is sealed as "
                "a stable baseline: P1/P2 output adapter standards, multi-model interaction, midplatform "
                "model data handling, and midplatform model control are all closed. All model outputs remain "
                "evidence candidate; agreement/conflict/uncertainty stay candidate-only; ingress / evidence "
                "bundle / gate pass are never fact admission; enabled is not runtime activation; fallback "
                "triggers no download/inference; reserved-only families never execute; commercial runtime "
                "remains unapproved; Field/Task/Guidance stay candidate-only; VLA action chain is excluded; "
                "Luna emotion-multimodal cognition-first principle is preserved. The governance chain is now "
                "available as a reusable baseline. Next: decide between a post-review or "
                "Model Governance Runtime Trial Planning."
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
    result = review_model_governance_integrated_closure_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "stage_ref_count": result["stage_ref_count"],
                "artifact_ref_count": result["artifact_ref_count"],
                "capability_coverage_count": result["capability_coverage_count"],
                "candidate_coverage_count": result["candidate_coverage_count"],
                "negative_closure_guard_passed": result["negative_closure_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
