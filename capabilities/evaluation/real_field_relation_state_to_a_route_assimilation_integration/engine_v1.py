"""Controlled Field relation state assimilation through the canonical A-Route."""

from __future__ import annotations

import copy
import dataclasses
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Mapping

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
    ARouteOrchestrationRequestV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.controlled_replay_runtime_fixture_v1 import (
    build_controlled_replay_gateway_request_v1,
)
from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME
from capabilities.midplatform.core.field_state_reducer.state_reduction.entity_field_relation_state_value_v1 import (
    EntityFieldRelationStateValueV1,
)
from capabilities.midplatform.core.field_state_reducer.state_reduction.state_reduction_types_v1 import (
    FieldStateCandidate,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)

from .adapter_v1 import (
    ENTITY_FIELD_OBSERVATION_RELATION_STATE,
    ENTITY_TO_FIELD_OBSERVATION_RELATION,
    OBSERVED_IN_FIELD,
    RelationStateAssimilationAdapterV1,
)


PHASE = "Phase-P1-Luna-Field-Relation-State-To-ARoute-Assimilation-Integration-v1-001"
SOURCE_MODE = "CONTROLLED_FIELD_RELATION_STATE_ASSIMILATION_TEST"
FIELD_REF = "field:visual-frame:v1"
SUBJECT_REF = "entity-candidate:controlled:visual-chair:001"
RELATION_REF = "relation-candidate:controlled:observed-in-field:001"
STATE_REF = "state_candidate:controlled:entity-field-observation:001"
EVIDENCE_REFS = ("visual-evidence:controlled:001", "visual-evidence:controlled:002")
SOURCE_REFS = (
    "controlled:relation-state-source:a:v1",
    "controlled:relation-state-source:b:v1",
)
PROVENANCE_REFS = (
    "trace:route-d:field-relation-state",
    "provenance:route-d:controlled-field-relation-state",
    "field:visual-frame:v1",
)


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def build_controlled_field_state_candidate_v1() -> FieldStateCandidate:
    """Build the already-governed ROUTE C shape without a provider call."""

    value = EntityFieldRelationStateValueV1(
        relation_candidate_ref=RELATION_REF,
        subject_ref=SUBJECT_REF,
        predicate=OBSERVED_IN_FIELD,
        object_ref=FIELD_REF,
        relation_semantic_kind=ENTITY_TO_FIELD_OBSERVATION_RELATION,
        evidence_refs=EVIDENCE_REFS,
        source_refs=SOURCE_REFS,
        trace_ref="trace:route-d:field-relation-state",
        provenance_refs=PROVENANCE_REFS,
    )
    return FieldStateCandidate(
        state_candidate_id=STATE_REF,
        field_id=FIELD_REF,
        state_type=ENTITY_FIELD_OBSERVATION_RELATION_STATE,
        candidate_status="candidate",
        candidate_value=asdict(value),
        temporal_status="active",
        confidence_snapshot={},
        supporting_event_refs=(
            "field-event:route-d:controlled-a:v1",
            "field-event:route-d:controlled-b:v1",
        ),
        conflicting_event_refs=(),
        overlay_refs=(),
        owner_correction_refs=(),
        provenance_refs=PROVENANCE_REFS,
        selected_policy_ids=("multi_event_consensus",),
        policy_application_plan_ref="plan:route-d:controlled-relation-state",
        previous_state_ref=None,
        transition_result={
            "requested_transition": "candidate->candidate",
            "transition_allowed": True,
            "transition_status": "candidate",
        },
        trace_ref="state-reduction-trace:route-d:controlled-relation-state",
        replay_key="replay:route-d:controlled-relation-state:v1",
        candidate_only=True,
        fact_admitted=False,
        persisted=False,
    )


def _negative_inputs(candidate: FieldStateCandidate) -> Dict[str, Dict[str, Any]]:
    base = asdict(candidate)

    def with_value(**changes: Any) -> Dict[str, Any]:
        item = copy.deepcopy(base)
        item["candidate_value"].update(changes)
        return item

    unsupported_state = copy.deepcopy(base)
    unsupported_state["state_type"] = "presence_state"
    raw_relation = {
        "relation_candidate_ref": RELATION_REF,
        "predicate": OBSERVED_IN_FIELD,
        "object_ref": FIELD_REF,
    }
    return {
        "unsupported_state_type": unsupported_state,
        "empty_candidate_value": {**copy.deepcopy(base), "candidate_value": {}},
        "predicate_missing": with_value(predicate=None),
        "object_ref_missing": with_value(object_ref=None),
        "candidate_only_false": with_value(candidate_only=False),
        "fact_admitted_true": with_value(fact_admitted=True),
        "truth_declared_true": with_value(truth_declared=True),
        "persistent_relation_declared_true": with_value(persistent_relation_declared=True),
        "belongs_to_field_predicate": with_value(predicate="BELONGS_TO_FIELD"),
        "raw_relation_without_field_state": raw_relation,
    }


class FieldRelationStateToARouteAssimilationEngineV1:
    """Run one controlled typed relation handoff through A-Route/CState."""

    def run(self) -> Dict[str, Any]:
        field_state = build_controlled_field_state_candidate_v1()
        adapter = RelationStateAssimilationAdapterV1()
        projection_result = adapter.project(field_state)

        gateway_request = build_controlled_replay_gateway_request_v1()
        gateway = ObservationGatewayEngineV1().run_case(gateway_request)
        observation = gateway.observation
        admission = gateway.replay_admission
        projection = projection_result.relation_interpretation_candidate

        route = None
        if observation is not None and admission is not None and projection is not None:
            route_request = ARouteOrchestrationRequestV1(
                scenario_id="route-d-field-relation-assimilation",
                ingress=ARouteIngressRefsV1(
                    observation_refs=(observation.observation_id,),
                    perception_refs=tuple(item.evidence_id for item in gateway.evidence),
                    field_refs=(field_state.state_candidate_id,),
                    relation_refs=(RELATION_REF,),
                ),
                context_ref="context:route-d:controlled-field-relation",
                pcn_ref="pcn:route-d:controlled-field-relation",
                intent_ref="intent:route-d:controlled-field-relation",
                execution_mode=CONTROLLED_REPLAY_RUNTIME,
                replay_admission=admission,
                synthetic_only=False,
                candidate_only=True,
                relation_interpretation_candidates=(projection,),
            )
            route = ARouteOrchestrationEngineV1().run_case(route_request)

        negative_cases = {}
        for case_id, invalid in _negative_inputs(field_state).items():
            result = adapter.project(invalid)
            negative_cases[case_id] = {
                "accepted": result.accepted,
                "reason": result.reason,
                "semantic_candidate_created": result.relation_interpretation_candidate is not None,
            }

        proof = route.cognitive_execution if route is not None else None
        semantic_candidates = (
            proof.relation_interpretation_semantic_candidates if proof else ()
        )
        current_world_refs = (
            proof.current_world_relation_interpretation_refs if proof else ()
        )
        validation_errors = []
        if not projection_result.accepted:
            validation_errors.append("adapter:positive_projection_rejected")
        if route is None:
            validation_errors.append("a_route:controlled_handoff_unavailable")
        if route is not None and route.errors:
            validation_errors.extend(f"a_route:{item.code}" for item in route.errors)
        if proof is None:
            validation_errors.append("a_route:cognitive_execution_missing")
        if not all(not item["accepted"] for item in negative_cases.values()):
            validation_errors.append("adapter:negative_guard_accepted_input")

        return {
            "phase": PHASE,
            "source_mode": SOURCE_MODE,
            "execution_mode": CONTROLLED_REPLAY_RUNTIME,
            "provider_invoked": False,
            "model_invoked": False,
            "recorded_provider_result_used": False,
            "field_state_candidate": _jsonable(field_state),
            "adapter_result": _jsonable(projection_result),
            "a_route_result": _jsonable(route) if route is not None else None,
            "cognitive_execution": _jsonable(proof) if proof else None,
            "typed_semantic_candidates": _jsonable(semantic_candidates),
            "current_world_relation_interpretation_refs": list(current_world_refs),
            "relation_ingress_ref": RELATION_REF,
            "field_ref": FIELD_REF,
            "subject_ref": SUBJECT_REF,
            "predicate": OBSERVED_IN_FIELD,
            "relation_semantic_kind": ENTITY_TO_FIELD_OBSERVATION_RELATION,
            "candidate_only": True,
            "fact_admitted": False,
            "truth_declared": False,
            "persistent_relation_declared": False,
            "identity_resolution_status": "UNRESOLVED",
            "field_mutation": False,
            "field_truth_promotion": False,
            "world_truth_declared": False,
            "memory_mutation": False,
            "pcn_mutation": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "negative_cases": negative_cases,
            "policy_trace_compatibility_gap": True,
            "policy_trace_compatibility_gap_status": "KNOWN_NON_BLOCKING_INDEPENDENT_DEBT",
            "forbidden_behaviors": {
                "raw_yolo_direct_a_route_relation": False,
                "raw_relation_direct_a_route_typed_assimilation": False,
                "field_mutation": False,
                "field_truth_promotion": False,
                "world_truth_declared": False,
                "memory_mutation": False,
                "pcn_mutation": False,
                "decision_execution": False,
                "task_execution": False,
                "action_execution": False,
                "device_control": False,
                "camera_control": False,
                "movement_control": False,
            },
            "validation_errors": validation_errors,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = [
    "PHASE",
    "SOURCE_MODE",
    "FieldRelationStateToARouteAssimilationEngineV1",
    "build_controlled_field_state_candidate_v1",
]
