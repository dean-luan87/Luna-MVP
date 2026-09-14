from __future__ import annotations

from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_types_v1 import (
    IntegrationExecutionRecordV1,
)


REQUIRED_NEGATIVE_FLAGS = {
    "integration_has_no_owner",
    "source_mutation",
    "runtime_side_effect",
    "database_write",
    "device_control",
    "scheduler_execution",
    "task_mutation",
    "field_mutation",
    "memory_mutation",
    "silent_retry",
    "owner_bypass",
    "runtime_bypass",
}


def validate_no_runtime_side_effects(record: IntegrationExecutionRecordV1) -> bool:
    return record.runtime_side_effect is False


def validate_no_owner_or_runtime_bypass(record: IntegrationExecutionRecordV1) -> bool:
    return record.owner_bypass is False and record.runtime_bypass is False


def validate_trace_continuity(record: IntegrationExecutionRecordV1) -> bool:
    t = record.end_to_end_trace
    return all(
        bool(item)
        for item in (
            t.root_trace_id,
            t.intent_trace_ref,
            t.causal_trace_ref,
            t.decision_trace_ref,
            t.action_trace_ref,
            t.execution_trace_ref,
        )
    )


def validate_provenance_reverse_locatability(
    record: IntegrationExecutionRecordV1,
) -> bool:
    p = record.provenance
    return (
        p.reverse_locatable
        and bool(p.execution_result_ref)
        and bool(p.action_candidate_ref)
        and bool(p.causal_hypothesis_refs)
        and bool(p.intent_candidate_refs)
        and bool(p.source_evidence_or_context_refs)
    )
