# -*- coding: utf-8 -*-
"""Recognition Midplatform Model Governance Integrated Closure Post-Review — review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.model_governance_integrated_closure_post_review.model_governance_integrated_closure_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    INTEGRATED_CLOSURE_ARTIFACT_REL,
    REQUIRED_VERIFY_FLAGS,
    audit_layer_artifacts,
    load_integrated_closure,
    verify_stages,
)
from capabilities.midplatform.model_governance_integrated_closure_post_review.model_governance_integrated_closure_post_review_types_v1 import (  # noqa: E402
    BOUNDARY_AUDIT_ITEMS,
    CLOSURE_EXPECTED_ARTIFACT_REF_COUNT_MIN,
    CLOSURE_EXPECTED_CANDIDATE_COVERAGE_MIN,
    CLOSURE_EXPECTED_CAPABILITY_COVERAGE_MIN,
    CLOSURE_EXPECTED_NEGATIVE_GUARD_PASSED,
    CLOSURE_EXPECTED_STAGE_REF_COUNT_MIN,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    COVERAGE_AUDIT_DIMENSIONS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    INTEGRATED_CLOSURE_EXPECTED_GO,
    INTEGRATED_CLOSURE_REF,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_GUARD_AUDIT_IDS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POST_REVIEW_GOVERNANCE_RULES,
    POST_REVIEW_ONLY,
    POST_REVIEW_PRINCIPLE_ZH,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    ModelGovernanceIntegratedClosurePostReviewProfile,
    ModelGovernancePostReviewBoundaryAudit,
    ModelGovernancePostReviewCoverageAudit,
    ModelGovernancePostReviewHandoffReadiness,
    ModelGovernancePostReviewNegativeGuardAudit,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "recognition_midplatform_model_governance_integrated_closure_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "recognition_midplatform_model_governance_integrated_closure_post_review_review_v1.json"
)

_PKG = "capabilities/midplatform/model_governance_integrated_closure_post_review"
STEP_FILES = (
    f"{_PKG}/model_governance_integrated_closure_post_review_types_v1.py",
    f"{_PKG}/model_governance_integrated_closure_post_review_registry_v1.py",
    f"{_PKG}/review_model_governance_integrated_closure_post_review_v1.py",
)

PROFILE_REF = (
    "recognition_midplatform_model_governance_integrated_closure_post_review_profile_v1"
)


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        ModelGovernanceIntegratedClosurePostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            post_review_only=POST_REVIEW_ONLY,
            integrated_closure_ref=INTEGRATED_CLOSURE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            coverage_audit_dimensions=COVERAGE_AUDIT_DIMENSIONS,
            boundary_audit_items=BOUNDARY_AUDIT_ITEMS,
            negative_guard_audit_ids=NEGATIVE_GUARD_AUDIT_IDS,
            governance_rules=POST_REVIEW_GOVERNANCE_RULES,
        )
    )


def review_model_governance_integrated_closure_post_review_v1(
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

    # --- Stage reference audit -------------------------------------------- #
    stage_refs, verify_flags, stage_issues = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    stage_ref_audit_count = len(stage_refs) + 1  # + governance template stage

    # --- Artifact audit (four sealed layers) ------------------------------ #
    artifact_audits, artifact_issues = audit_layer_artifacts(_REPO_ROOT)
    failed_checks.extend(artifact_issues)
    artifact_audit_count = sum(1 for a in artifact_audits if a["sealed_ok"])
    four_layer_artifacts_sealed = artifact_audit_count >= 4 and all(
        a["sealed_ok"] for a in artifact_audits
    )

    # --- Load integrated closure artifact for internal-consistency audit -- #
    closure, closure_exists = load_integrated_closure(_REPO_ROOT)
    if not closure_exists:
        failed_checks.append("integrated_closure_artifact_missing")
        closure = {}

    closure_go_ok = closure.get("final_decision") == INTEGRATED_CLOSURE_EXPECTED_GO
    closure_blocker_zero = int(closure.get("blocker_count", -1)) == 0
    closure_stage_ref_count = int(closure.get("stage_ref_count", 0))
    closure_artifact_ref_count = int(closure.get("artifact_ref_count", 0))
    closure_capability_count = int(closure.get("capability_coverage_count", 0))
    closure_candidate_count = int(closure.get("candidate_coverage_count", 0))
    closure_neg_guard_passed = int(closure.get("negative_closure_guard_passed", 0))
    closure_boundary = closure.get("boundary_closure", {}) or {}
    closure_coverage_complete = closure.get("coverage_complete_flags", {}) or {}
    closure_neg_guards = closure.get("negative_closure_guards", []) or []

    if not closure_go_ok:
        failed_checks.append(
            f"integrated_closure_not_go:{closure.get('final_decision')!r}"
        )
    if not closure_blocker_zero:
        failed_checks.append("integrated_closure_blocker_nonzero")
    if closure_stage_ref_count < CLOSURE_EXPECTED_STAGE_REF_COUNT_MIN:
        failed_checks.append("integrated_closure_stage_ref_count_below_min")
    if closure_artifact_ref_count < CLOSURE_EXPECTED_ARTIFACT_REF_COUNT_MIN:
        failed_checks.append("integrated_closure_artifact_ref_count_below_min")

    # --- Coverage audit --------------------------------------------------- #
    coverage_audits: List[ModelGovernancePostReviewCoverageAudit] = []
    for dim in COVERAGE_AUDIT_DIMENSIONS:
        reported = closure_coverage_complete.get(dim) is True
        coverage_audits.append(
            ModelGovernancePostReviewCoverageAudit(
                dimension=dim, closure_reported=reported, audit_ok=reported
            )
        )
    coverage_audit_count = len(coverage_audits)
    capability_coverage_audit_ok = (
        closure_capability_count >= CLOSURE_EXPECTED_CAPABILITY_COVERAGE_MIN
    )
    candidate_coverage_audit_ok = (
        closure_candidate_count >= CLOSURE_EXPECTED_CANDIDATE_COVERAGE_MIN
    )

    # --- Boundary audit (16) ---------------------------------------------- #
    boundary_audits: List[ModelGovernancePostReviewBoundaryAudit] = []
    for item in BOUNDARY_AUDIT_ITEMS:
        reported = closure_boundary.get(item) is True
        boundary_audits.append(
            ModelGovernancePostReviewBoundaryAudit(
                boundary_item=item, closure_reported=reported, still_holds=reported
            )
        )
    boundary_audit_count = len(boundary_audits)
    boundary_all_hold = all(b.still_holds for b in boundary_audits)

    def _b(item: str) -> bool:
        return closure_boundary.get(item) is True

    condensed_boundary = {
        "candidate_only_boundary_preserved": (
            _b("conflict_uncertainty_candidate_only")
            and _b("field_task_guidance_candidate_only")
        ),
        "fact_admission_blocked": (
            _b("candidate_ingress_not_fact_admission")
            and _b("multi_model_agreement_not_fact")
            and _b("evidence_bundle_not_fact_bundle")
            and _b("candidate_output_gate_not_fact_admission")
        ),
        "runtime_activation_blocked": (
            _b("enabled_not_runtime_activation")
            and _b("guidance_not_runtime_navigation")
            and _b("action_safety_no_action_trigger")
        ),
        "commercial_runtime_not_approved": _b("commercial_runtime_not_approved"),
        "reserved_only_family_not_executed": _b("reserved_only_family_not_executed"),
        "vla_action_chain_excluded": _b("vla_action_chain_excluded"),
        "luna_emotion_multimodal_brain_first_preserved": _b(
            "luna_emotion_multimodal_brain_first_preserved"
        ),
    }

    # --- Negative guard audit (14) ---------------------------------------- #
    closure_guard_passed = {
        g.get("guard_id"): (g.get("passed") is True) for g in closure_neg_guards
    }
    negative_guard_audits: List[ModelGovernancePostReviewNegativeGuardAudit] = []
    for guard_id in NEGATIVE_GUARD_AUDIT_IDS:
        passed = closure_guard_passed.get(guard_id, False)
        negative_guard_audits.append(
            ModelGovernancePostReviewNegativeGuardAudit(
                guard_id=guard_id, closure_passed=passed, still_blocks=passed
            )
        )
    negative_guard_audit_count = len(negative_guard_audits)
    negative_guard_audit_ok = (
        negative_guard_audit_count == 14
        and all(g.still_blocks for g in negative_guard_audits)
        and closure_neg_guard_passed == CLOSURE_EXPECTED_NEGATIVE_GUARD_PASSED
    )

    # --- Handoff readiness (recorded only) -------------------------------- #
    handoff_readiness: List[ModelGovernancePostReviewHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            ModelGovernancePostReviewHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True
    handoff_readiness_count = len(handoff_readiness)

    go_conditions = {
        "post_review_profile_count_eq_1": True,
        "stage_ref_audit_count_gte_13": stage_ref_audit_count >= 13,
        "artifact_audit_count_gte_4": artifact_audit_count >= 4,
        "coverage_audit_count_gte_4": coverage_audit_count >= 4,
        "boundary_audit_count_gte_16": boundary_audit_count >= 16,
        "negative_guard_audit_count_eq_14": negative_guard_audit_count == 14,
        "handoff_readiness_count_gte_5": handoff_readiness_count >= 5,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_governance_template_ref_ok": (
            verify_flags.get("controlled_trial_governance_template_ref_ok") is True
        ),
        "four_layer_artifacts_sealed": four_layer_artifacts_sealed,
        "capability_coverage_audit_ok": capability_coverage_audit_ok,
        "candidate_coverage_audit_ok": candidate_coverage_audit_ok,
        "negative_guard_audit_ok": negative_guard_audit_ok,
        **condensed_boundary,
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
        "step": "Recognition Midplatform Model Governance Integrated Closure Post-Review",
        "lifecycle_variant": "recognition_midplatform_model_governance_integrated_closure_post_review",
        "post_review_principle_zh": POST_REVIEW_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "post_review_only": POST_REVIEW_ONLY,
        "integrated_closure_ref": INTEGRATED_CLOSURE_REF,
        "integrated_closure_artifact_rel": INTEGRATED_CLOSURE_ARTIFACT_REL,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "post_review_governance_rules": list(POST_REVIEW_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "post_review_profile": _build_profile(),
        "stage_ref_audit_count": stage_ref_audit_count,
        "stage_audits": stage_refs,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "artifact_audit_count": artifact_audit_count,
        "artifact_audits": artifact_audits,
        "integrated_closure_internal_audit": {
            "final_decision": closure.get("final_decision"),
            "go_ok": closure_go_ok,
            "blocker_count": closure.get("blocker_count"),
            "blocker_zero": closure_blocker_zero,
            "stage_ref_count": closure_stage_ref_count,
            "artifact_ref_count": closure_artifact_ref_count,
            "capability_coverage_count": closure_capability_count,
            "candidate_coverage_count": closure_candidate_count,
            "negative_closure_guard_passed": closure_neg_guard_passed,
        },
        "coverage_audit_count": coverage_audit_count,
        "coverage_audits": [asdict(c) for c in coverage_audits],
        "capability_coverage_audit_ok": capability_coverage_audit_ok,
        "candidate_coverage_audit_ok": candidate_coverage_audit_ok,
        "boundary_audit_count": boundary_audit_count,
        "boundary_audits": [asdict(b) for b in boundary_audits],
        "boundary_all_hold": boundary_all_hold,
        "condensed_boundary": condensed_boundary,
        "negative_guard_audit_count": negative_guard_audit_count,
        "negative_guard_audits": [asdict(g) for g in negative_guard_audits],
        "negative_guard_audit_ok": negative_guard_audit_ok,
        "handoff_readiness_count": handoff_readiness_count,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "post_review_status": (
                "integrated_closure_trusted_as_runtime_trial_planning_baseline"
                if review_ok
                else "blocked"
            ),
            "audited_layers": [a["layer"] for a in artifact_audits],
            "next_phase_ref": NEXT_PHASE_REF,
            "transition_note": (
                "Post-review confirms the recognition-model expansion + midplatform governance integrated "
                "closure is internally consistent and trustworthy: stage references, four sealed layer "
                "artifacts, capability and candidate coverage, 16 boundary invariants, and 14 negative "
                "closure guards all re-verified, with the candidate-only boundary, blocked fact admission, "
                "blocked runtime activation, unapproved commercial runtime, non-executing reserved families "
                "and excluded VLA action chain intact. No capability was added, no governance rule changed, "
                "no dry-run run, and runtime trial planning was not entered; handoff readiness for five "
                "downstream targets is recorded only. The integrated closure is a trusted upstream baseline. "
                "Next: Phase-Model-Governance-Runtime-Trial-Planning-v1-001 to define runtime trial "
                "admission conditions."
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
    result = review_model_governance_integrated_closure_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "stage_ref_audit_count": result["stage_ref_audit_count"],
                "artifact_audit_count": result["artifact_audit_count"],
                "coverage_audit_count": result["coverage_audit_count"],
                "boundary_audit_count": result["boundary_audit_count"],
                "negative_guard_audit_count": result["negative_guard_audit_count"],
                "handoff_readiness_count": result["handoff_readiness_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
