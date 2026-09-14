from __future__ import annotations

from typing import List, Tuple

from capabilities.midplatform.core.context_foundation.context_foundation_types_v1 import (
    ContextEnvelopeCandidateV1,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_types_v1 import (
    IntegrationScenarioDirectiveV1,
    PcnToIntentHandoffV1,
)
from capabilities.midplatform.core.intent_governance.intent_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.intent_governance.intent_io_types_v1 import (
    IntentGovernanceInputV1,
)
from capabilities.midplatform.core.personal_cognitive_network.personal_cognitive_network_skeleton_v1 import (
    SkeletonRunResult,
)


def _ref(owner: str, ref_id: str, ref_type: str) -> SourceRefV1:
    return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _context_refs(context: ContextEnvelopeCandidateV1) -> Tuple[SourceRefV1, ...]:
    return (_ref("Context Governance", context.context_id, "CONTEXT"),)


def _pcn_refs(pcn: SkeletonRunResult) -> Tuple[SourceRefV1, ...]:
    return (
        _ref(
            "Personal Cognitive Network Governance",
            pcn.projection.projection_id,
            "PCN_PROJECTION",
        ),
    )


def _source_refs(pcn: SkeletonRunResult) -> Tuple[SourceRefV1, ...]:
    refs: List[SourceRefV1] = []
    for rid in pcn.projection.active_reference_set:
        refs.append(
            _ref("Personal Cognitive Network Governance", rid, "PCN_ACTIVE_REF")
        )
    for lid in pcn.projection.active_link_set:
        refs.append(_ref("Personal Cognitive Network Governance", lid, "PCN_LINK_REF"))
    return tuple(refs)


def _self_role_context_refs(
    context: ContextEnvelopeCandidateV1,
    pcn: SkeletonRunResult,
) -> Tuple[SourceRefV1, ...]:
    refs: List[SourceRefV1] = []
    if context.self_projection_reference is not None:
        refs.append(
            _ref(
                "Self Layer / Self Governance",
                context.self_projection_reference.projection_id,
                "SELF",
            )
        )
    if context.role_projection_reference is not None:
        refs.append(
            _ref(
                "Social Self / Role Governance",
                context.role_projection_reference.projection_id,
                "ROLE",
            )
        )
    refs.append(_ref("Context Governance", context.context_id, "CONTEXT"))
    refs.append(
        _ref(
            "Personal Cognitive Network Governance",
            pcn.projection.projection_id,
            "PCN_PROJECTION",
        )
    )
    return tuple(refs)


def build_pcn_to_intent_handoff(
    context: ContextEnvelopeCandidateV1,
    pcn: SkeletonRunResult,
    directive: IntegrationScenarioDirectiveV1,
) -> PcnToIntentHandoffV1:
    trace_ref = "" if directive.force_missing_trace else pcn.trace.trace_id
    if directive.remove_pcn_required_ref:
        trace_ref = ""

    version = directive.pcn_to_intent_version_override or "candidate-v1"
    return PcnToIntentHandoffV1(
        handoff_id=f"pcn-intent:{pcn.case_id}",
        source_owner="Personal Cognitive Network Governance",
        target_owner="Intent Governance",
        pcn_candidate_ref=pcn.projection.projection_id,
        identity_self_role_context_refs=tuple(
            ref.ref_id for ref in _self_role_context_refs(context, pcn)
        ),
        trace_ref=trace_ref,
        provenance_ref=pcn.projection.provenance,
        version=version,
        candidate_only=True,
        source_mutation=False,
    )


def map_pcn_to_intent_input(
    context: ContextEnvelopeCandidateV1,
    pcn: SkeletonRunResult,
    directive: IntegrationScenarioDirectiveV1,
) -> IntentGovernanceInputV1:
    source_refs = _source_refs(pcn)
    if directive.force_intent_reject:
        source_refs = ()
    return IntentGovernanceInputV1(
        scenario_id=directive.scenario_id,
        context_refs=_context_refs(context),
        pcn_refs=_pcn_refs(pcn),
        source_refs=source_refs,
        self_refs=tuple(
            ref
            for ref in _self_role_context_refs(context, pcn)
            if ref.ref_type == "SELF"
        ),
        field_refs=tuple(
            _ref("Cognitive Field", rid, "FIELD")
            for rid in pcn.projection.active_reference_set
            if "field" in rid
        ),
        role_refs=tuple(
            ref
            for ref in _self_role_context_refs(context, pcn)
            if ref.ref_type == "ROLE"
        ),
        relationship_refs=tuple(
            _ref("Social Self / Relationship Governance", rid, "RELATIONSHIP")
            for rid in pcn.projection.active_reference_set
            if "rel" in rid or "relationship" in rid
        ),
        memory_refs=tuple(
            _ref("Memory Governance", rid, "MEMORY")
            for rid in pcn.projection.active_reference_set
            if "memory" in rid
        ),
        experience_refs=(),
        emotion_refs=tuple(
            _ref("Emotion / Integration Governance", rid, "EMOTION")
            for rid in pcn.projection.active_reference_set
            if "emotion" in rid
        ),
        unknowns=("unknown:pre-cognitive",),
        synthetic_only=True,
        candidate_only=True,
    )
