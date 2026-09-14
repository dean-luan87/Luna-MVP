from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.core.context_foundation.context_foundation_types_v1 import (
    ContextEnvelopeCandidateV1,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_types_v1 import (
    ContextToPcnHandoffV1,
    IntegrationScenarioDirectiveV1,
)


def _projection_refs(context: ContextEnvelopeCandidateV1) -> Tuple[str, ...]:
    refs = []
    if context.field_projection_reference is not None:
        refs.append(context.field_projection_reference.projection_id)
    if context.observation_projection_reference is not None:
        refs.append(context.observation_projection_reference.projection_id)
    if context.memory_projection_reference is not None:
        refs.append(context.memory_projection_reference.projection_id)
    if context.self_projection_reference is not None:
        refs.append(context.self_projection_reference.projection_id)
    if context.role_projection_reference is not None:
        refs.append(context.role_projection_reference.projection_id)
    if context.relationship_projection_reference is not None:
        refs.append(context.relationship_projection_reference.projection_id)
    if context.emotion_projection_reference is not None:
        refs.append(context.emotion_projection_reference.projection_id)
    return tuple(refs)


def build_context_to_pcn_handoff(
    context: ContextEnvelopeCandidateV1,
    directive: IntegrationScenarioDirectiveV1,
) -> ContextToPcnHandoffV1:
    version = directive.context_to_pcn_version_override or "candidate-v1"
    trace_ref = "" if directive.force_missing_trace else context.trace_reference
    if directive.remove_context_required_ref:
        trace_ref = ""

    return ContextToPcnHandoffV1(
        handoff_id=f"ctx-pcn:{context.context_id}",
        source_owner="Context Foundation",
        target_owner="Personal Cognitive Network Governance",
        context_candidate_ref=context.context_id,
        context_schema_ref=context.version,
        field_context_refs=_projection_refs(context),
        trace_ref=trace_ref,
        provenance_ref=context.provenance[0] if context.provenance else "",
        version=version,
        candidate_only=True,
        source_mutation=False,
    )


def map_context_to_pcn_case(
    context: ContextEnvelopeCandidateV1,
    directive: IntegrationScenarioDirectiveV1,
) -> dict[str, object]:
    refs = list(_projection_refs(context))
    if directive.force_pcn_incomplete:
        refs = []
    return {
        "case_id": directive.scenario_id,
        "title": directive.description,
        "synthetic_only": True,
        "context_id": context.context_id,
        "resource_label": "LOW" if "LOW" in directive.scenario_id else "HIGH",
        "source_refs": refs,
        "interaction_refs": [],
    }
