# -*- coding: utf-8 -*-
"""Provider Manager Runtime Skeleton — compressed Step 4: Verify + Post-DryRun Review."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import (
    DRYRUN_LIFECYCLE_RULES,
    build_outcome_doc,
    load_json_file,
    verify_invalid_cases_expected_reject,
    verify_summary_boolean_flags,
    verify_summary_counts,
    verify_trace_decision_distribution,
    verify_trace_list,
    write_json_file,
)
from capabilities.midplatform.provider_manager_runtime_skeleton.provider_manager_runtime_skeleton_types_v1 import (
    FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER,
    FINAL_DECISION_POST_DRYRUN_REVIEW_BLOCKED,
    FINAL_DECISION_POST_DRYRUN_REVIEW_GO,
    PHASE_ID,
)

DEFAULT_INPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "provider_manager_runtime_skeleton_dryrun_v1_smoke_v0"
)
TRACE_FILENAME = "provider_manager_runtime_skeleton_dryrun_trace_v1.json"
SUMMARY_FILENAME = "provider_manager_runtime_skeleton_dryrun_summary_v1.json"
OUTPUT_FILENAME = "provider_manager_runtime_skeleton_verification_and_review_v1.json"

EXPECTED_TRACE_COUNT = 17
EXPECTED_POSITIVE_PASS = 9
EXPECTED_INVALID_REJECT = 8

INVALID_CASE_IDS = (
    "invalid_a_runtime_execution_allowed",
    "invalid_b_provider_activation_allowed",
    "invalid_c_fallback_execution_allowed",
    "invalid_d_output_dispatch_allowed",
    "invalid_e_real_provider_connected",
    "invalid_f_health_loop_direct_disable",
    "invalid_g_direct_output_paths",
    "invalid_h_vision_ocr_spatial_pollution",
)

STEP_LABEL = "Step 4 Verify + Post-DryRun Review"


def verify_and_review_provider_manager_runtime_skeleton_dryrun_v1(
    *,
    input_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    root = Path(input_root or DEFAULT_INPUT_ROOT).expanduser().resolve()
    trace_path = root / TRACE_FILENAME
    summary_path = root / SUMMARY_FILENAME

    trace_doc = load_json_file(trace_path)
    summary = load_json_file(summary_path)
    failed_checks: List[str] = []

    count_ok, count_failed = verify_summary_counts(
        summary,
        {
            "trace_count": EXPECTED_TRACE_COUNT,
            "positive_pass_count": EXPECTED_POSITIVE_PASS,
            "invalid_expected_reject_count": EXPECTED_INVALID_REJECT,
            "unexpected_pass_count": 0,
            "unexpected_fail_count": 0,
        },
    )
    failed_checks.extend(count_failed)

    flags_ok, flags_failed = verify_summary_boolean_flags(
        summary,
        flags_false=(
            "runtime_execution_allowed",
            "provider_activation_allowed",
            "fallback_execution_allowed",
            "output_dispatch_allowed",
            "real_provider_connected",
        ),
        flags_true=(
            "spatial_evidence_boundary_preserved",
            "vision_ocr_boundary_preserved",
            "no_domain_specific_manager_duplication",
            "candidate_only_enforced",
        ),
    )
    failed_checks.extend(flags_failed)

    trace_list_ok, traces, trace_list_failed = verify_trace_list(
        trace_doc,
        expected_count=EXPECTED_TRACE_COUNT,
        phase_id=PHASE_ID,
    )
    failed_checks.extend(trace_list_failed)

    decision_ok, unexpected_pass, unexpected_fail, decision_failed = (
        verify_trace_decision_distribution(
            traces,
            expected_positive_pass=EXPECTED_POSITIVE_PASS,
            expected_invalid_reject=EXPECTED_INVALID_REJECT,
        )
    )
    failed_checks.extend(decision_failed)

    invalid_ok, invalid_failed = verify_invalid_cases_expected_reject(
        traces,
        INVALID_CASE_IDS,
    )
    failed_checks.extend(invalid_failed)

    verification_ok = (
        count_ok
        and flags_ok
        and trace_list_ok
        and decision_ok
        and invalid_ok
        and unexpected_pass == 0
        and unexpected_fail == 0
    )

    review_failed: List[str] = []
    if summary.get("final_decision") != FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER:
        review_failed.append(
            "summary.final_decision_upstream: "
            f"expected={FINAL_DECISION_DRYRUN_TRACE_READY_FOR_VERIFIER!r}, "
            f"actual={summary.get('final_decision')!r}"
        )
    if summary.get("phase_id") != PHASE_ID:
        review_failed.append(
            f"summary.phase_id: expected={PHASE_ID!r}, actual={summary.get('phase_id')!r}"
        )
    failed_checks.extend(review_failed)
    review_ok = len(review_failed) == 0

    out_path = root / OUTPUT_FILENAME
    outcome = build_outcome_doc(
        phase_id=PHASE_ID,
        step=STEP_LABEL,
        input_root=str(root),
        input_trace_file=str(trace_path),
        input_summary_file=str(summary_path),
        output_file=str(out_path),
        verification_ok=verification_ok,
        review_ok=review_ok,
        summary=summary,
        trace_count=len(traces),
        unexpected_pass_count=unexpected_pass,
        unexpected_fail_count=unexpected_fail,
        failed_checks=failed_checks,
        go_decision=FINAL_DECISION_POST_DRYRUN_REVIEW_GO,
        blocked_decision=FINAL_DECISION_POST_DRYRUN_REVIEW_BLOCKED,
        extra_fields={
            "invalid_case_ids_checked": list(INVALID_CASE_IDS),
            "phase_sealed": verification_ok and review_ok and len(failed_checks) == 0,
            "dryrun_lifecycle_rules": list(DRYRUN_LIFECYCLE_RULES),
        },
    )

    if write_file:
        write_json_file(out_path, outcome)

    return outcome


def main() -> int:
    try:
        outcome = verify_and_review_provider_manager_runtime_skeleton_dryrun_v1()
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    print(
        json.dumps(
            {
                "input_root": outcome.get("input_root"),
                "output_file": outcome.get("output_file"),
                "verification_ok": outcome["verification_ok"],
                "review_ok": outcome["review_ok"],
                "trace_count": outcome["trace_count"],
                "positive_pass_count": outcome["positive_pass_count"],
                "invalid_expected_reject_count": outcome["invalid_expected_reject_count"],
                "unexpected_pass_count": outcome["unexpected_pass_count"],
                "unexpected_fail_count": outcome["unexpected_fail_count"],
                "blocker_count": outcome["blocker_count"],
                "final_decision": outcome["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if outcome["final_decision"] == FINAL_DECISION_POST_DRYRUN_REVIEW_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
