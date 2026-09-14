"""Read-only B1 Current World adapter for B2 cognitive integration."""

from __future__ import annotations

from typing import Iterable, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_core_types_v1 import (
    CycleSnapshotV1,
    SourceRefV1 as FlowSourceRefV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_io_types_v1 import (
    CognitiveFlowInputV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_engine_v1 import (
    CognitiveFlowEngineV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
    CognitiveStateFormationOutputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (
    CognitiveStateFormationEngineV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_types_v1 import (
    ObservationControlDecisionV1,
)

from .b2_current_world_cognitive_state_flow_types_v1 import (
    B2CurrentWorldCognitiveFlowResultV1,
    B2ObservationNeedBridgeCandidateV1,
)


def _state_ref(owner: str, ref: str, case_id: str, schema: str = "v1") -> SourceRefV1:
    return SourceRefV1(
        owner=owner,
        source_ref=ref,
        schema_version=schema,
        trace_ref=f"trace:{case_id}:source:{ref}",
        provenance_ref=f"prov:{case_id}:source:{ref}",
        read_only=True,
        reference_only=True,
        source_mutation_allowed=False,
    )


def _flow_ref(owner: str, ref: str, case_id: str, ref_type: str) -> FlowSourceRefV1:
    return FlowSourceRefV1(
        owner=owner,
        ref_id=ref,
        ref_type=ref_type,
        version="v1",
        trace_ref=f"trace:{case_id}:flow:{ref_type}",
        provenance_ref=f"prov:{case_id}:flow:{ref_type}",
        read_only=True,
        candidate_only=True,
        source_mutation_allowed=False,
    )


def _refs(
    owner: str, values: Iterable[str], case_id: str, schema: str = "v1"
) -> Tuple[SourceRefV1, ...]:
    return tuple(_state_ref(owner, value, case_id, schema) for value in values if value)


def build_state_request_from_current_world_v1(
    current_world: CurrentWorldCandidateV1,
    case_id: str,
    *,
    engine_scenario_id: str = "S01",
    synthetic_only: bool = True,
) -> CognitiveStateFormationInputV1:
    """Map a candidate Current World without reconstructing Context."""

    if not current_world.candidate_only:
        raise ValueError("B2 requires candidate-only CurrentWorld input")
    current_world_ref = _state_ref(
        "Cognitive State Formation Governance",
        current_world.current_world_id,
        case_id,
        "current-world-candidate-v1",
    )
    return CognitiveStateFormationInputV1(
        scenario_id=engine_scenario_id,
        context_refs=_refs("Context Foundation", current_world.context_refs, case_id),
        pcn_refs=_refs(
            "Personal Cognitive Network Governance", current_world.pcn_refs, case_id
        ),
        intent_refs=_refs("Intent Governance", current_world.intent_refs, case_id),
        field_refs=_refs("Field State Reducer", current_world.field_state_refs, case_id),
        observation_refs=_refs(
            "Observation Manager / Reality Evidence Pipeline",
            current_world.observation_refs,
            case_id,
        ),
        current_world_ref=current_world_ref,
        uncertainty_refs=_refs(
            "Uncertainty Governance", current_world.uncertainty_refs, case_id
        ),
        synthetic_only=synthetic_only,
        candidate_only=True,
    )


def build_flow_request_v1(
    current_world: CurrentWorldCandidateV1,
    state_output: CognitiveStateFormationOutputV1,
    case_id: str,
    *,
    flow_scenario_id: str = "C01",
) -> CognitiveFlowInputV1:
    """Build the existing Flow input with the B1 world reference explicit."""

    world_ref = _flow_ref(
        "Cognitive State Formation Governance",
        current_world.current_world_id,
        case_id,
        "current-world",
    )
    state_ref = _flow_ref(
        "Cognitive State Formation Governance",
        state_output.current_world_candidate.current_world_id,
        case_id,
        "state-formation-world",
    )
    context_refs = tuple(
        _flow_ref("Context Foundation", ref, case_id, "context")
        for ref in current_world.context_refs
    )
    pcn_refs = tuple(
        _flow_ref("Personal Cognitive Network Governance", ref, case_id, "pcn")
        for ref in current_world.pcn_refs
    )
    intent_refs = tuple(
        _flow_ref("Intent Governance", ref, case_id, "intent")
        for ref in current_world.intent_refs
    )
    field_refs = tuple(
        _flow_ref("Field State Reducer", ref, case_id, "field")
        for ref in current_world.field_state_refs
    )
    attention_refs = tuple(
        _flow_ref("Cognitive State Formation Governance", ref, case_id, "attention")
        for ref in state_output.current_world_candidate.attention_refs
    )
    hypothesis_refs = tuple(
        _flow_ref("Cognitive State Formation Governance", ref, case_id, "hypothesis")
        for ref in state_output.current_world_candidate.active_hypothesis_refs
    )
    snapshot = CycleSnapshotV1(
        cycle_id=f"cycle:{case_id}",
        previous_cycle_id=None,
        context_refs=tuple(ref.ref_id for ref in context_refs),
        pcn_refs=tuple(ref.ref_id for ref in pcn_refs),
        intent_refs=tuple(ref.ref_id for ref in intent_refs),
        state_formation_refs=(state_ref.ref_id,),
        attention_refs=tuple(ref.ref_id for ref in attention_refs),
        hypothesis_refs=tuple(ref.ref_id for ref in hypothesis_refs),
        current_world_ref=world_ref.ref_id,
        cognitive_state_vector_ref=state_output.cognitive_state_vector_candidate.state_vector_id,
        regulation_candidate_ref=None,
        field_refs=tuple(ref.ref_id for ref in field_refs),
        causal_refs=(),
        snapshot_id=f"snapshot:{case_id}",
        trace_ref=f"trace:{case_id}:snapshot",
        provenance_refs=tuple(
            dict.fromkeys(
                (
                    *current_world.provenance_refs,
                    f"prov:{case_id}:snapshot",
                )
            )
        ),
    )
    return CognitiveFlowInputV1(
        scenario_id=flow_scenario_id,
        cycle_snapshot=snapshot,
        context_refs=context_refs,
        pcn_refs=pcn_refs,
        intent_refs=intent_refs,
        state_formation_refs=(state_ref,),
        attention_refs=attention_refs,
        hypothesis_refs=hypothesis_refs,
        current_world_ref=world_ref,
        cognitive_state_vector_ref=_flow_ref(
            "Cognitive State Formation Governance",
            state_output.cognitive_state_vector_candidate.state_vector_id,
            case_id,
            "state-vector",
        ),
        field_refs=field_refs,
        synthetic_only=True,
        candidate_only=True,
    )


def build_observation_need_bridge_v1(
    current_world: CurrentWorldCandidateV1,
    case_id: str,
) -> B2ObservationNeedBridgeCandidateV1 | None:
    """Express a candidate control need through the existing FPO type."""

    if not current_world.uncertainty_refs and not current_world.conflict_refs:
        return None
    decision = "RECONSIDER" if current_world.conflict_refs else "CONTINUE"
    reason = (
        "candidate contradiction requires reconsideration"
        if current_world.conflict_refs
        else "candidate uncertainty may require additional observation"
    )
    control = ObservationControlDecisionV1(
        decision_id=f"observation-control:{case_id}",
        decision=decision,
        reason=reason,
        source_refs=(current_world.current_world_id,),
        evidence_refs=current_world.observation_refs,
        budget_state={"provider_invocation": False},
        trace_ref=f"trace:{case_id}:observation-need",
        provenance_refs=tuple(
            dict.fromkeys(
                (
                    *current_world.provenance_refs,
                    *current_world.uncertainty_refs,
                    *current_world.conflict_refs,
                )
            )
        ),
        runtime_execution=False,
        provider_mutation=False,
        downstream_mutation=False,
        candidate_only=True,
    )
    return B2ObservationNeedBridgeCandidateV1(
        owner="Field Perception Orchestrator",
        control_decision=control,
        source_current_world_ref=current_world.current_world_id,
        candidate_only=True,
        provider_invocation=False,
    )


def run_b2_case(
    current_world: CurrentWorldCandidateV1,
    case_id: str,
    *,
    mode: str,
    engine_scenario_id: str = "S01",
    flow_scenario_id: str = "C01",
) -> B2CurrentWorldCognitiveFlowResultV1:
    state_request = build_state_request_from_current_world_v1(
        current_world,
        case_id,
        engine_scenario_id=engine_scenario_id,
        synthetic_only=True,
    )
    state_output = CognitiveStateFormationEngineV1().run_case(state_request)
    flow_request = build_flow_request_v1(
        current_world,
        state_output,
        case_id,
        flow_scenario_id=flow_scenario_id,
    )
    flow_output = CognitiveFlowEngineV1().run_case(flow_request)
    bridge = build_observation_need_bridge_v1(current_world, case_id)
    provenance_chain = tuple(
        dict.fromkeys(
            (
                current_world.current_world_id,
                *current_world.provenance_refs,
                current_world.trace_ref,
                state_output.trace.current_world_trace_ref,
                flow_output.trace.root_cycle_trace_id if flow_output.trace else "",
                flow_output.provenance.source_snapshot_ref
                if flow_output.provenance
                else "",
            )
        )
    )
    return B2CurrentWorldCognitiveFlowResultV1(
        case_id=case_id,
        mode=mode,
        source_current_world=current_world,
        state_request=state_request,
        state_output=state_output,
        flow_output=flow_output,
        observation_need_bridge=bridge,
        preserved_uncertainty_refs=current_world.uncertainty_refs,
        preserved_conflict_refs=current_world.conflict_refs,
        preserved_temporal_refs=current_world.temporal_refs,
        provenance_chain=provenance_chain,
        metadata={
            "source_current_world_ref": current_world.current_world_id,
            "derived_state_world_ref": state_output.current_world_candidate.current_world_id,
            "flow_current_world_ref": flow_request.current_world_ref.ref_id
            if flow_request.current_world_ref
            else "",
            "observation_need_owner": "Field Perception Orchestrator"
            if bridge
            else "",
        },
    )
