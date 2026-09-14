from __future__ import annotations

from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_types_v1 import (
    CompatibilityDecisionV1,
    ContextToPcnHandoffV1,
    PcnToIntentHandoffV1,
)


EXPECTED_CONTEXT_TO_PCN_VERSION = "candidate-v1"
EXPECTED_PCN_TO_INTENT_VERSION = "candidate-v1"


def validate_context_to_pcn_compatibility(
    handoff: ContextToPcnHandoffV1,
) -> CompatibilityDecisionV1:
    if not handoff.trace_ref or not handoff.provenance_ref:
        return CompatibilityDecisionV1(
            hop_id="H1",
            compatible=False,
            hard_block=False,
            reason="missing_required_ref",
            classification="A",
        )
    if handoff.version != EXPECTED_CONTEXT_TO_PCN_VERSION:
        return CompatibilityDecisionV1(
            hop_id="H1",
            compatible=False,
            hard_block=True,
            reason="version_mismatch",
            classification="A",
        )
    if handoff.source_owner != "Context Foundation":
        return CompatibilityDecisionV1(
            hop_id="H1",
            compatible=False,
            hard_block=True,
            reason="source_owner_mismatch",
            classification="C",
        )
    return CompatibilityDecisionV1(
        hop_id="H1",
        compatible=True,
        hard_block=False,
        reason="compatible",
        classification="A",
    )


def validate_pcn_to_intent_compatibility(
    handoff: PcnToIntentHandoffV1,
) -> CompatibilityDecisionV1:
    if not handoff.trace_ref or not handoff.provenance_ref:
        return CompatibilityDecisionV1(
            hop_id="H2",
            compatible=False,
            hard_block=False,
            reason="missing_required_ref",
            classification="A",
        )
    if handoff.version != EXPECTED_PCN_TO_INTENT_VERSION:
        return CompatibilityDecisionV1(
            hop_id="H2",
            compatible=False,
            hard_block=True,
            reason="version_mismatch",
            classification="A",
        )
    if handoff.source_owner != "Personal Cognitive Network Governance":
        return CompatibilityDecisionV1(
            hop_id="H2",
            compatible=False,
            hard_block=True,
            reason="source_owner_mismatch",
            classification="C",
        )
    if not handoff.identity_self_role_context_refs:
        return CompatibilityDecisionV1(
            hop_id="H2",
            compatible=False,
            hard_block=False,
            reason="identity_self_role_context_refs_missing",
            classification="A",
        )
    return CompatibilityDecisionV1(
        hop_id="H2",
        compatible=True,
        hard_block=False,
        reason="compatible",
        classification="A",
    )
