"""Compatibility computation and A interpretation, with no new semantic owner."""

from __future__ import annotations

from typing import Optional

from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    DynamicCognitiveLoopOutputV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_adapter_v1 import (
    _base_a_grant,
    _binding,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_engine_v1 import (
    wrap_dynamic_flow_output,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_types_v1 import (
    ASemanticDecisionBundleV1,
    ASemanticDecisionContextV1,
)

from .dynamic_flow_semantic_compatibility_registry_v1 import A_OWNER, SOURCE_OWNER
from .dynamic_flow_semantic_compatibility_types_v1 import (
    DynamicFlowAInterpretationV1,
    DynamicFlowCompatibilityOutputV1,
)


def _last_state_ref(output: DynamicCognitiveLoopOutputV1) -> Optional[str]:
    return output.state_versions[-1].state_version_ref if output.state_versions else None


def _computed_sufficiency(output: DynamicCognitiveLoopOutputV1) -> str:
    if output.sufficiency_candidates:
        return output.sufficiency_candidates[-1].status
    if output.final_disposition == "RECONSIDER" or output.reconsiderations:
        return "REQUIRES_RECONSIDERATION"
    return "INSUFFICIENT"


def build_compatibility_output(
    output: DynamicCognitiveLoopOutputV1,
) -> DynamicFlowCompatibilityOutputV1:
    """Expose Dynamic Flow calculations as traceable, non-authoritative data."""
    return DynamicFlowCompatibilityOutputV1(
        compatibility_ref=f"dynamic-compatibility:{output.scenario_id}",
        source_flow_ref=f"dynamic-flow:{output.scenario_id}",
        source_state_version_refs=tuple(item.state_version_ref for item in output.state_versions),
        computed_need_ref=output.current_minimum_need_ref,
        computed_sufficiency_status=_computed_sufficiency(output),
        computed_reconsideration_refs=tuple(
            item.trace_ref for item in output.reconsiderations
        ),
        computed_next_step_disposition=output.next_step_disposition,
        evidence_refs=tuple(output.evidence_update_refs),
        trace_refs=tuple(output.trace_refs),
        provenance_refs=tuple(output.provenance_refs),
        source_owner_ref=SOURCE_OWNER,
    )


def build_a_interpretation_context(
    output: DynamicCognitiveLoopOutputV1,
    *,
    concern_ref: Optional[str] = None,
    work_ref: Optional[str] = None,
    a_grant_ref: Optional[str] = None,
) -> ASemanticDecisionContextV1:
    state_ref = _last_state_ref(output) or f"state:{output.scenario_id}:v1"
    concern = concern_ref or f"concern:{output.scenario_id}"
    work = work_ref or f"work:{output.scenario_id}"
    return ASemanticDecisionContextV1(
        work_ref=work,
        concern_ref=concern,
        a_grant_ref=a_grant_ref or f"grant:a:{output.scenario_id}",
        source_state_version_ref=state_ref,
        goal_refs=(output.goal.goal_ref,),
        intent_refs=output.goal.intent_refs,
        role_refs=(f"role:{output.scenario_id}",),
        perspective_refs=(),
        field_refs=(f"field:{output.scenario_id}",),
        context_refs=output.goal.context_refs,
        current_world_refs=(f"current-world:{output.scenario_id}",),
        task_behavior_refs=(),
        emotion_modulation_refs=(),
        experience_refs=(),
        safety_refs=(),
        permission_refs=(),
        resource_envelope_refs=(),
        evidence_refs=tuple(output.evidence_update_refs),
        prior_need_refs=(output.current_minimum_need_ref,) if output.current_minimum_need_ref else (),
        prior_hypothesis_refs=tuple(
            ref for state in output.state_versions for ref in state.active_hypothesis_refs
        ),
        prior_requirement_refs=tuple(output.requirement_refs),
        trace_refs=tuple(output.trace_refs),
        provenance_refs=tuple(output.provenance_refs),
    )


def interpret_for_a(
    output: DynamicCognitiveLoopOutputV1,
    *,
    grant=None,
    binding=None,
    concern_ref: Optional[str] = None,
    work_ref: Optional[str] = None,
) -> DynamicFlowAInterpretationV1:
    """Use the verified A bridge; Dynamic Flow remains only the source computation."""
    state_ref = _last_state_ref(output) or f"state:{output.scenario_id}:v1"
    concern = concern_ref or f"concern:{output.scenario_id}"
    work = work_ref or f"work:{output.scenario_id}"
    active_grant = grant or _base_a_grant(
        output.scenario_id,
        concern_ref=concern,
        work_ref=work,
        state_ref=state_ref,
    )
    active_binding = binding or _binding(
        f"binding:dynamic-compatibility:{output.scenario_id}",
        "SELECT_CURRENT_NEED",
    )
    context = build_a_interpretation_context(
        output,
        concern_ref=concern,
        work_ref=work,
        a_grant_ref=active_grant.grant_ref,
    )
    bundle: ASemanticDecisionBundleV1 = wrap_dynamic_flow_output(
        context,
        output,
        grant=active_grant,
        binding=active_binding,
    )
    compatibility = build_compatibility_output(output)
    return DynamicFlowAInterpretationV1(
        compatibility_output=compatibility,
        a_decisions=bundle,
        compatibility_source_ref=compatibility.compatibility_ref,
    )


def interpretation_is_a_owned(interpretation: DynamicFlowAInterpretationV1) -> bool:
    bundle = interpretation.a_decisions
    decisions = (
        bundle.need_decision,
        bundle.sufficiency_decision,
        bundle.reconsideration_decision,
        bundle.next_step_decision,
    )
    return (
        all(item is not None and item.decision_owner_ref == A_OWNER for item in decisions)
        and all(item.accepted for item in bundle.validations)
        and bundle.compatibility_wrapper_only
        and not interpretation.compatibility_output.semantic_authority
    )


__all__ = [
    "build_a_interpretation_context",
    "build_compatibility_output",
    "interpret_for_a",
    "interpretation_is_a_owned",
]
