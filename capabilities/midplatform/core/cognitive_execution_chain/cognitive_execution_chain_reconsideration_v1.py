from __future__ import annotations

from typing import List, Tuple

from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_types_v1 import (
    ReconsiderationCandidateV1,
)


def build_runtime_feedback_reconsideration(
    scenario_id: str,
    runtime_status: str,
    runtime_result_ref: str,
    runtime_failure_ref: str | None,
) -> Tuple[ReconsiderationCandidateV1, ...]:
    if runtime_status not in {
        "FAILED_CANDIDATE",
        "TIMEOUT_CANDIDATE",
        "PARTIAL_RESULT_CANDIDATE",
        "REJECTED_CANDIDATE",
    }:
        return ()

    reason = "runtime_result_feedback"
    if runtime_status == "TIMEOUT_CANDIDATE":
        reason = "runtime_timeout_feedback"
    elif runtime_status == "PARTIAL_RESULT_CANDIDATE":
        reason = "runtime_partial_feedback"
    elif runtime_status == "REJECTED_CANDIDATE":
        reason = "runtime_admission_reject_feedback"

    refs: List[str] = [runtime_result_ref]
    if runtime_failure_ref:
        refs.append(runtime_failure_ref)

    return (
        ReconsiderationCandidateV1(
            route_id=f"reconsider:{scenario_id}:runtime-to-action",
            source_owner="Runtime Executor",
            target_owner="Action Governance",
            reason=reason,
            related_refs=tuple(refs),
        ),
    )


def build_action_feedback_reconsideration(
    scenario_id: str,
    action_state: str,
    action_candidate_ref: str,
) -> Tuple[ReconsiderationCandidateV1, ...]:
    if action_state != "CANCELLED":
        return ()

    return (
        ReconsiderationCandidateV1(
            route_id=f"reconsider:{scenario_id}:action-to-decision",
            source_owner="Action Governance",
            target_owner="Decision Governance",
            reason="action_cancelled_feedback",
            related_refs=(action_candidate_ref,),
        ),
    )
