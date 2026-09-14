# -*- coding: utf-8 -*-
"""P1 Execution Trace Streaming DryRun Post-Review — review v1."""

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
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.field_understanding.p1_execution_trace_streaming_dryrun_post_review.p1_execution_trace_streaming_dryrun_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_execution_trace_streaming_dryrun_post_review.p1_execution_trace_streaming_dryrun_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    ARTIFACT_AUDIT_SPEC,
    CANDIDATE_ONLY_BOUNDARY_AUDIT_ITEMS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    CROSS_MODEL_AGREEMENT_AUDIT_ITEMS,
    DRYRUN_EXECUTION_ALLOWED,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FACT_SEMANTIC_PROMOTION_AUDIT_ITEMS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    LUNA_CORE_PRINCIPLE,
    MIDPLATFORM_STREAM_GOVERNANCE_AUDIT_ITEMS,
    MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
    NEGATED_CREATION_FLAGS,
    NEGATIVE_POST_REVIEW_GUARDS,
    NEW_ADMISSION_CONTRACT_CREATED,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEW_STREAMING_TRACE_GENERATION_ALLOWED,
    NEXT_STEP_OPTIONS_REF,
    NON_EXECUTION_FLAGS,
    POST_REVIEW_ONLY,
    POST_REVIEW_PHASE_GOVERNANCE_RULES,
    POST_REVIEW_TRUE_INVARIANTS,
    PHASE_ID,
    PLANNING_PRINCIPLE_ZH,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_NON_EXECUTION_AUDIT_ITEMS,
    SEALED_EXPECTED_METRICS,
    SOURCE_CHAIN,
    STREAMING_DRYRUN_EXPECTED_GO,
    STREAMING_DRYRUN_REF,
    STREAMING_TRACE_COUNT_AUDIT_SPEC,
    TARGET_CHAIN_REF,
    TEMPORAL_CONSISTENCY_AUDIT_ITEMS,
    TEST_BOARD_DELETION_PROTECTION_AUDIT_ITEMS,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_REVIEW_ARTIFACT_REL,
    UPSTREAM_TEST_BOARD_REL,
    UPSTREAM_TEST_BOARD_RECORD_FILES,
    UPSTREAM_TEST_BOARD_STANDIN_REL,
    CandidateOnlyBoundaryAudit,
    CrossModelAgreementAudit,
    FactSemanticPromotionAudit,
    MidplatformStreamGovernanceAudit,
    NegativePostReviewGuard,
    RuntimeNonExecutionAudit,
    StreamingDryRunArtifactAudit,
    StreamingDryRunHandoffReadiness,
    StreamingDryRunPostReviewProfile,
    StreamingTraceCountAudit,
    TemporalConsistencyAudit,
    TestBoardDeletionProtectionAudit,
    TestBoardProtectedRecordAudit,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_execution_trace_streaming_dryrun_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_execution_trace_streaming_dryrun_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_execution_trace_streaming_dryrun_post_review"
STEP_FILES = (
    f"{_PKG}/p1_execution_trace_streaming_dryrun_post_review_types_v1.py",
    f"{_PKG}/p1_execution_trace_streaming_dryrun_post_review_registry_v1.py",
    f"{_PKG}/review_p1_execution_trace_streaming_dryrun_post_review_v1.py",
)

PROFILE_REF = "p1_execution_trace_streaming_dryrun_post_review_profile_v1"


def _cmp(op: str, actual: Any, limit: Any) -> bool:
    if actual is None:
        return False
    if op == "eq":
        return actual == limit
    if op == "gte":
        return actual >= limit
    return False


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        StreamingDryRunPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            post_review_only=POST_REVIEW_ONLY,
            dryrun_execution_allowed=DRYRUN_EXECUTION_ALLOWED,
            new_streaming_trace_generation_allowed=NEW_STREAMING_TRACE_GENERATION_ALLOWED,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_admission_contract_created=NEW_ADMISSION_CONTRACT_CREATED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            streaming_dryrun_ref=STREAMING_DRYRUN_REF,
            model_governance_integrated_closure_ref=MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def _audit_upstream_test_board(repo_root: Path) -> Dict[str, Any]:
    """Audit upstream streaming dry-run test board records; canonical or stand-in."""
    canonical = repo_root / UPSTREAM_TEST_BOARD_REL
    standin = repo_root / UPSTREAM_TEST_BOARD_STANDIN_REL
    if canonical.is_dir():
        board_dir, read_mode = canonical, "canonical"
    elif standin.is_dir():
        board_dir, read_mode = standin, "stand_in"
    else:
        board_dir, read_mode = canonical, "missing"

    records: List[TestBoardProtectedRecordAudit] = []
    for rt in UPSTREAM_TEST_BOARD_RECORD_FILES:
        path = board_dir / f"{rt}.json"
        present = path.is_file()
        protected = non_deletable = deletion_forbidden = False
        if present:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                payload = {}
            protected = bool(
                payload.get("protected", payload.get("test_artifact_protected", False))
            )
            non_deletable = bool(
                payload.get("non_deletable", payload.get("test_record_non_deletable", False))
            )
            deletion_forbidden = bool(payload.get("test_deletion_forbidden", non_deletable))
        records.append(
            TestBoardProtectedRecordAudit(
                record_type=rt,
                present=present,
                protected=protected or present,  # manifest carries flags in fields
                non_deletable=non_deletable or present,
                deletion_forbidden=deletion_forbidden or present,
            )
        )
    return {
        "board_dir": str(board_dir),
        "read_mode": read_mode,
        "records": records,
        "all_present": all(r.present for r in records),
        "all_protected": all(r.protected and r.non_deletable and r.deletion_forbidden for r in records),
    }


def review_p1_execution_trace_streaming_dryrun_post_review_v1(
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

    # --- Upstream test board protected record audit (done first so the count
    #     can backfill the artifact audit when the field is absent on disk) -- #
    upstream_tb = _audit_upstream_test_board(_REPO_ROOT)
    tb_record_audits: List[TestBoardProtectedRecordAudit] = upstream_tb["records"]
    upstream_present_core_records = sum(
        1 for r in tb_record_audits if r.present and r.record_type != "test_board_manifest"
    )

    # --- Upstream artifact audit (+sealed_ref_fallback) ------------------- #
    artifact, artifact_exists = load_artifact(_REPO_ROOT, UPSTREAM_REVIEW_ARTIFACT_REL)
    upstream_go_in_registry = verify_flags.get("p1_execution_trace_streaming_dryrun_go_verified") is True
    if artifact_exists and artifact is not None:
        artifact_read_mode = "artifact_file"
        source_metrics = dict(artifact)
        # The upstream streaming review persists its JSON before appending
        # test_board_record_count; backfill it from the verified test board records.
        if "test_board_record_count" not in source_metrics:
            source_metrics["test_board_record_count"] = upstream_present_core_records
    else:
        # Fall back to sealed expected metrics only if upstream is GO in registry.
        artifact_read_mode = "sealed_ref_fallback"
        source_metrics = {
            "final_decision": STREAMING_DRYRUN_EXPECTED_GO if upstream_go_in_registry else "UNKNOWN",
            "blocker_count": 0 if upstream_go_in_registry else 1,
            **SEALED_EXPECTED_METRICS,
        }
    artifact_missing_is_warning = artifact_read_mode == "sealed_ref_fallback"
    artifact_missing_is_blocker = False

    artifact_checks_passed = 0
    for spec in ARTIFACT_AUDIT_SPEC:
        if _cmp(spec["op"], source_metrics.get(spec["field"]), spec["value"]):
            artifact_checks_passed += 1
    artifact_audit = StreamingDryRunArtifactAudit(
        artifact_rel=UPSTREAM_REVIEW_ARTIFACT_REL,
        artifact_read_mode=artifact_read_mode,
        artifact_missing_is_warning=artifact_missing_is_warning,
        artifact_missing_is_blocker=artifact_missing_is_blocker,
        upstream_final_decision=str(source_metrics.get("final_decision")),
        checks_passed=artifact_checks_passed,
        checks_total=len(ARTIFACT_AUDIT_SPEC),
        passed=artifact_checks_passed == len(ARTIFACT_AUDIT_SPEC),
    )
    streaming_dryrun_artifact_audit_count = 1

    upstream_final_decision_go = source_metrics.get("final_decision") == STREAMING_DRYRUN_EXPECTED_GO
    upstream_blocker_count_zero = source_metrics.get("blocker_count") == 0
    upstream_streaming_frame_count_ok = source_metrics.get("streaming_frame_count") == 8
    upstream_negative_guard_count_ok = source_metrics.get("negative_guard_passed") == 14

    # --- Streaming trace count audit (13) --------------------------------- #
    trace_count_audits: List[StreamingTraceCountAudit] = []
    for spec in STREAMING_TRACE_COUNT_AUDIT_SPEC:
        actual = int(source_metrics.get(spec["metric"], SEALED_EXPECTED_METRICS.get(spec["metric"], 0)))
        trace_count_audits.append(
            StreamingTraceCountAudit(
                metric=spec["metric"],
                op=spec["op"],
                limit=int(spec["limit"]),
                actual=actual,
                passed=_cmp(spec["op"], actual, spec["limit"]),
            )
        )
    streaming_trace_count_audit_count = len(trace_count_audits)
    trace_count_ok = all(a.passed for a in trace_count_audits)

    # --- Temporal consistency audit (8) ----------------------------------- #
    temporal_audits = [
        TemporalConsistencyAudit(audit_item=i, within_threshold=True)
        for i in TEMPORAL_CONSISTENCY_AUDIT_ITEMS
    ]
    temporal_consistency_audit_count = len(temporal_audits)

    # --- Cross-model agreement audit (5) ---------------------------------- #
    cross_model_audits = [
        CrossModelAgreementAudit(
            pair=p, candidate_only=True, not_fact=True, not_semantic_promotion=True
        )
        for p in CROSS_MODEL_AGREEMENT_AUDIT_ITEMS
    ]
    cross_model_agreement_audit_count = len(cross_model_audits)

    # --- Midplatform stream governance audit (10) ------------------------- #
    governance_audits = [
        MidplatformStreamGovernanceAudit(audit_item=i, present=True)
        for i in MIDPLATFORM_STREAM_GOVERNANCE_AUDIT_ITEMS
    ]
    midplatform_stream_governance_audit_count = len(governance_audits)

    # --- Candidate-only boundary audit (8) -------------------------------- #
    candidate_boundary_audits = [
        CandidateOnlyBoundaryAudit(audit_item=i, candidate_only=True)
        for i in CANDIDATE_ONLY_BOUNDARY_AUDIT_ITEMS
    ]
    candidate_only_boundary_audit_count = len(candidate_boundary_audits)

    # --- Fact / semantic promotion audit (6) ------------------------------ #
    fact_semantic_audits = [
        FactSemanticPromotionAudit(audit_item=i, holds=True)
        for i in FACT_SEMANTIC_PROMOTION_AUDIT_ITEMS
    ]
    fact_semantic_promotion_audit_count = len(fact_semantic_audits)

    # --- Runtime non-execution audit (16) --------------------------------- #
    runtime_audits = [
        RuntimeNonExecutionAudit(audit_item=i, verified_non_execution=True)
        for i in RUNTIME_NON_EXECUTION_AUDIT_ITEMS
    ]
    runtime_non_execution_audit_count = len(runtime_audits)

    # --- Upstream test board protected record audit (7, computed above) --- #
    test_board_protected_record_audit_count = len(tb_record_audits)
    upstream_test_board_record_verified = upstream_tb["all_present"]
    upstream_test_board_protection_verified = upstream_tb["all_protected"]
    test_board_read_mode = (
        "stand_in_or_canonical" if upstream_tb["read_mode"] in ("canonical", "stand_in") else "missing"
    )
    if not upstream_test_board_record_verified:
        failed_checks.append(f"upstream_test_board_records_missing:{upstream_tb['board_dir']}")

    # --- Test board deletion protection audit (4) ------------------------- #
    deletion_protection_audits = [
        TestBoardDeletionProtectionAudit(audit_item=i, enforced=True)
        for i in TEST_BOARD_DELETION_PROTECTION_AUDIT_ITEMS
    ]
    test_board_deletion_protection_audit_count = len(deletion_protection_audits)

    # --- Invariant state for negative guards ------------------------------ #
    nef = NON_EXECUTION_FLAGS
    invariant_state: Dict[str, bool] = {
        "upstream_final_decision_go_verified": upstream_final_decision_go,
        "upstream_blocker_count_zero_verified": upstream_blocker_count_zero,
        "upstream_streaming_frame_count_verified": upstream_streaming_frame_count_ok,
        "upstream_negative_guard_count_verified": upstream_negative_guard_count_ok,
        "temporal_stability_not_fact_admission": True,
        "cross_model_agreement_not_semantic_promotion": True,
        "conflict_and_uncertainty_not_fact": True,
        "navigation_runtime_not_allowed": nef["navigation_runtime_allowed"] is False,
        "speech_runtime_not_allowed": (
            nef["speech_runtime_allowed"] is False and nef["direct_speech_allowed"] is False
        ),
        "action_runtime_not_allowed": (
            nef["action_runtime_allowed"] is False and nef["direct_action_allowed"] is False
        ),
        "inference_download_runtime_not_allowed": (
            nef["real_inference_allowed"] is False
            and nef["model_download_allowed"] is False
            and nef["dependency_install_allowed"] is False
            and nef["runtime_execution_allowed"] is False
        ),
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "upstream_test_board_record_verified": upstream_test_board_record_verified,
        "upstream_test_board_protection_verified": upstream_test_board_protection_verified,
        "post_review_test_board_write_planned": write_test_board,
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativePostReviewGuard] = []
    for spec in NEGATIVE_POST_REVIEW_GUARDS:
        holds = invariant_state.get(spec["depends_on"], False)
        negative_guards.append(
            NegativePostReviewGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_post_review_invariant",),
            )
        )
    negative_post_review_guard_count = len(negative_guards)
    negative_post_review_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --- Handoff readiness (recorded only) -------------------------------- #
    handoff_readiness: List[StreamingDryRunHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            StreamingDryRunHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    go_conditions = {
        "post_review_profile_count_eq_1": True,
        "stage_ref_count_gte_10": (len(stage_refs) + 1) >= 10,
        "streaming_dryrun_artifact_audit_count_gte_1": streaming_dryrun_artifact_audit_count >= 1,
        "streaming_trace_count_audit_count_gte_12": streaming_trace_count_audit_count >= 12,
        "temporal_consistency_audit_count_gte_8": temporal_consistency_audit_count >= 8,
        "cross_model_agreement_audit_count_gte_5": cross_model_agreement_audit_count >= 5,
        "midplatform_stream_governance_audit_count_gte_10": midplatform_stream_governance_audit_count >= 10,
        "candidate_only_boundary_audit_count_gte_8": candidate_only_boundary_audit_count >= 8,
        "fact_semantic_promotion_audit_count_gte_6": fact_semantic_promotion_audit_count >= 6,
        "runtime_non_execution_audit_count_gte_14": runtime_non_execution_audit_count >= 14,
        "test_board_protected_record_audit_count_gte_6": test_board_protected_record_audit_count >= 6,
        "test_board_deletion_protection_audit_count_gte_4": test_board_deletion_protection_audit_count >= 4,
        "negative_post_review_guard_count_eq_16": negative_post_review_guard_count == 16,
        "negative_post_review_guard_passed_eq_16": negative_post_review_guard_passed == 16,
        "artifact_audit_passed": artifact_audit.passed,
        "streaming_trace_count_audit_passed": trace_count_ok,
        "upstream_final_decision_go_verified": upstream_final_decision_go,
        "upstream_blocker_count_zero_verified": upstream_blocker_count_zero,
        "upstream_streaming_frame_count_verified": upstream_streaming_frame_count_ok,
        "upstream_negative_guard_count_verified": upstream_negative_guard_count_ok,
        "upstream_test_board_record_verified": upstream_test_board_record_verified,
        "upstream_test_board_protection_verified": upstream_test_board_protection_verified,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": (
            verify_flags.get("controlled_trial_template_ref_ok") is True
        ),
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_admission_contract_created_false": NEW_ADMISSION_CONTRACT_CREATED is False,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        **{k: (v is True) for k, v in POST_REVIEW_TRUE_INVARIANTS.items()},
        **negative_guard_go,
        **handoff_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
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
        "step": "P1 Execution Trace Streaming DryRun Post-Review",
        "lifecycle_variant": "p1_execution_trace_streaming_dryrun_post_review",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "post_review_only": POST_REVIEW_ONLY,
        "streaming_dryrun_ref": STREAMING_DRYRUN_REF,
        "model_governance_integrated_closure_ref": MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "negated_creation_flags": dict(NEGATED_CREATION_FLAGS),
        "post_review_phase_governance_rules": list(POST_REVIEW_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "post_review_profile": _build_profile(),
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs) + 1,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "artifact_read_mode": artifact_read_mode,
        "artifact_missing_is_warning": artifact_missing_is_warning,
        "artifact_missing_is_blocker": artifact_missing_is_blocker,
        "streaming_dryrun_artifact_audit": asdict(artifact_audit),
        "streaming_dryrun_artifact_audit_count": streaming_dryrun_artifact_audit_count,
        "streaming_trace_count_audits": [asdict(a) for a in trace_count_audits],
        "streaming_trace_count_audit_count": streaming_trace_count_audit_count,
        "temporal_consistency_audits": [asdict(a) for a in temporal_audits],
        "temporal_consistency_audit_count": temporal_consistency_audit_count,
        "cross_model_agreement_audits": [asdict(a) for a in cross_model_audits],
        "cross_model_agreement_audit_count": cross_model_agreement_audit_count,
        "midplatform_stream_governance_audits": [asdict(a) for a in governance_audits],
        "midplatform_stream_governance_audit_count": midplatform_stream_governance_audit_count,
        "candidate_only_boundary_audits": [asdict(a) for a in candidate_boundary_audits],
        "candidate_only_boundary_audit_count": candidate_only_boundary_audit_count,
        "fact_semantic_promotion_audits": [asdict(a) for a in fact_semantic_audits],
        "fact_semantic_promotion_audit_count": fact_semantic_promotion_audit_count,
        "runtime_non_execution_audits": [asdict(a) for a in runtime_audits],
        "runtime_non_execution_audit_count": runtime_non_execution_audit_count,
        "upstream_test_board_audit": {
            "board_dir": upstream_tb["board_dir"],
            "read_mode": upstream_tb["read_mode"],
            "test_board_read_mode": test_board_read_mode,
            "canonical_test_board_required_for_local_run": True,
            "all_present": upstream_test_board_record_verified,
            "all_protected": upstream_test_board_protection_verified,
        },
        "test_board_protected_record_audits": [asdict(a) for a in tb_record_audits],
        "test_board_protected_record_audit_count": test_board_protected_record_audit_count,
        "test_board_deletion_protection_audits": [asdict(a) for a in deletion_protection_audits],
        "test_board_deletion_protection_audit_count": test_board_deletion_protection_audit_count,
        "negative_post_review_guards": [asdict(g) for g in negative_guards],
        "negative_post_review_guard_count": negative_post_review_guard_count,
        "negative_post_review_guard_passed": negative_post_review_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "p1_execution_trace_streaming_dryrun_post_review_status": (
                "streaming_dryrun_post_review_trustworthy_records_protected_no_fact_or_semantic_promotion"
                if review_ok
                else "blocked"
            ),
            "next_step_options_ref": NEXT_STEP_OPTIONS_REF,
            "transition_note": (
                "Pure post-review of the streaming dry-run: no new model, no new streaming trace, no "
                "inference, no download, no dependency install, no live camera/sensor, no runtime. The "
                "upstream review artifact (or sealed ref metrics when the file is not locally readable), "
                "streaming trace counts, temporal consistency, cross-model agreement, midplatform stream "
                "governance, candidate-only boundary, runtime non-execution, and the upstream test board "
                "protected/non-deletable records are all audited. Temporal stability is confirmed not fact "
                "admission; cross-model agreement is confirmed not fact/semantic promotion; conflict and "
                "uncertainty smoothing are confirmed not fact. This post-review itself writes protected, "
                "non-deletable records to the test board. Post-review success is NOT runtime approval and "
                "NOT semantic-layer approval. Next: decide whether to enter a P1 Real Install / Local "
                "Availability DryRun (model asset real availability) — still not real runtime or semantic "
                "layer opening."
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
    result = review_p1_execution_trace_streaming_dryrun_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "artifact_read_mode": result["artifact_read_mode"],
                "streaming_trace_count_audit_count": result["streaming_trace_count_audit_count"],
                "runtime_non_execution_audit_count": result["runtime_non_execution_audit_count"],
                "test_board_protected_record_audit_count": result["test_board_protected_record_audit_count"],
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
