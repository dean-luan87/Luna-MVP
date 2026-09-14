from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_types_v1 import (
    NegativeGuardFlagsV1,
)


def validate_owner_preservation(
    context_owner: str,
    pcn_owner: str,
    intent_owner: str,
) -> bool:
    return (
        context_owner == "Context Foundation"
        and pcn_owner == "Personal Cognitive Network Governance"
        and intent_owner == "Intent Governance"
    )


def validate_integration_has_no_owner(integration_has_no_owner: bool) -> bool:
    return integration_has_no_owner is True


def validate_negative_guards(flags: NegativeGuardFlagsV1) -> bool:
    return (
        flags.integration_has_no_owner is True
        and flags.context_mutation is False
        and flags.pcn_mutation is False
        and flags.intent_direct_mutation is False
        and flags.context_bypass_to_intent is False
        and flags.pcn_bypass_intent_governance is False
        and flags.database_write is False
        and flags.device_control is False
        and flags.scheduler_execution is False
        and flags.task_mutation is False
        and flags.runtime_side_effect is False
        and flags.model_call is False
    )


def validate_trace_continuity(
    root_trace_id: str,
    context_trace_ref: str,
    pcn_trace_ref: str,
    intent_trace_ref: str,
) -> bool:
    return all(
        bool(item)
        for item in (root_trace_id, context_trace_ref, pcn_trace_ref, intent_trace_ref)
    )


def validate_provenance_reverse_lookup(
    source_context_refs: Iterable[str],
    reverse_locatable: bool,
) -> bool:
    refs = tuple(source_context_refs)
    return bool(refs) and reverse_locatable is True
