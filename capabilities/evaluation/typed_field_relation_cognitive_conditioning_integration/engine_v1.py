"""Controlled typed Field relation conditioning through A-Route/CState."""

from __future__ import annotations

import dataclasses
from dataclasses import asdict
from typing import Any, Dict, Mapping

from capabilities.evaluation.real_field_relation_state_to_a_route_assimilation_integration.adapter_v1 import (
    RelationStateAssimilationAdapterV1,
)
from capabilities.evaluation.real_field_relation_state_to_a_route_assimilation_integration.engine_v1 import (
    build_controlled_field_state_candidate_v1,
)
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
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)

from .types_v1 import (
    OBSERVED_IN_FIELD,
    RELATION_KIND,
    SOURCE_MODE,
    TypedRelationConditioningSpecV1,
)


PHASE = "Phase-P1-Luna-Typed-Field-Relation-Cognitive-Conditioning-Integration-v1-001"


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _specs() -> tuple[TypedRelationConditioningSpecV1, ...]:
    return (
        TypedRelationConditioningSpecV1(
            "role-owner",
            "context:office",
            "role:workspace-owner",
            "task:find-seat",
            "goal:find-seat",
            "information:seat-location",
        ),
        TypedRelationConditioningSpecV1(
            "role-visitor",
            "context:office",
            "role:visitor",
            "task:find-seat",
            "goal:find-seat",
            "information:seat-location",
        ),
        TypedRelationConditioningSpecV1(
            "task-seat",
            "context:office",
            "role:workspace-owner",
            "task:find-seat",
            "goal:find-seat",
            "information:seat-location",
        ),
        TypedRelationConditioningSpecV1(
            "task-exit",
            "context:office",
            "role:workspace-owner",
            "task:identify-exit",
            "goal:identify-exit",
            "information:exit-location",
        ),
        TypedRelationConditioningSpecV1(
            "goal-location",
            "context:office",
            "role:workspace-owner",
            "task:assess-target",
            "goal:locate-target",
            "information:target-location",
        ),
        TypedRelationConditioningSpecV1(
            "goal-state",
            "context:office",
            "role:workspace-owner",
            "task:assess-target",
            "goal:verify-state",
            "information:operational-state",
        ),
        TypedRelationConditioningSpecV1(
            "role-task-owner",
            "context:office",
            "role:workspace-owner",
            "task:find-seat",
            "goal:find-seat",
            "information:seat-location",
        ),
        TypedRelationConditioningSpecV1(
            "role-task-visitor",
            "context:office",
            "role:visitor",
            "task:identify-exit",
            "goal:identify-exit",
            "information:exit-location",
        ),
        TypedRelationConditioningSpecV1(
            "irrelevant-context-a",
            "context:opaque:irrelevant-a",
            "role:workspace-owner",
            "task:find-seat",
            "goal:find-seat",
            "information:seat-location",
        ),
        TypedRelationConditioningSpecV1(
            "irrelevant-context-b",
            "context:opaque:irrelevant-b",
            "role:workspace-owner",
            "task:find-seat",
            "goal:find-seat",
            "information:seat-location",
        ),
    )


def _typed_semantics(candidate: Any) -> Dict[str, Any]:
    value = _jsonable(candidate)
    return {
        key: value.get(key)
        for key in (
            "field_state_candidate_ref",
            "subject_ref",
            "predicate",
            "object_ref",
            "relation_candidate_ref",
            "relation_semantic_kind",
            "evidence_refs",
            "source_refs",
            "provenance_refs",
            "identity_resolution_status",
            "candidate_only",
            "fact_admitted",
            "truth_declared",
            "persistent_relation_declared",
        )
    }


class TypedFieldRelationCognitiveConditioningEngineV1:
    """Run candidate-only typed relation contrasts without provider execution."""

    def _run_case(
        self,
        spec: TypedRelationConditioningSpecV1,
        *,
        field_state: Any,
        projection: Any,
        gateway: Any,
    ) -> Dict[str, Any]:
        admission = gateway.replay_admission
        observation = gateway.observation
        route_request = ARouteOrchestrationRequestV1(
            scenario_id=f"typed-field-relation-conditioning:{spec.case_id}",
            ingress=ARouteIngressRefsV1(
                observation_refs=(observation.observation_id,) if observation else (),
                perception_refs=tuple(item.evidence_id for item in gateway.evidence),
                field_refs=(field_state.state_candidate_id,),
                relation_refs=(projection.relation_interpretation_candidate.relation_ref,),
            ),
            context_ref=spec.context_ref,
            pcn_ref="pcn:typed-field-relation-conditioning",
            intent_ref=spec.goal_ref,
            execution_mode=CONTROLLED_REPLAY_RUNTIME,
            replay_admission=admission,
            synthetic_only=False,
            candidate_only=True,
            role_refs=(spec.role_ref,),
            task_refs=(spec.task_ref,),
            goal_refs=(spec.goal_ref,),
            concern_refs=(f"concern:{spec.goal_ref.removeprefix('goal:')}",),
            information_need_refs=(spec.information_need_ref,),
            relation_interpretation_candidates=(projection.relation_interpretation_candidate,),
        )
        route = ARouteOrchestrationEngineV1().run_case(route_request)
        proof = route.cognitive_execution
        candidate = proof.relation_interpretation_semantic_candidates[0] if proof and proof.relation_interpretation_semantic_candidates else None
        current_world_refs = proof.current_world_relation_interpretation_refs if proof else ()
        return {
            "case_id": spec.case_id,
            "context_ref": spec.context_ref,
            "role_ref": spec.role_ref,
            "task_ref": spec.task_ref,
            "goal_ref": spec.goal_ref,
            "information_need_ref": spec.information_need_ref,
            "route_status": route.control_state,
            "validation_errors": [item.code for item in route.errors],
            "typed_relation": _typed_semantics(candidate) if candidate else {},
            "relation_interpretation_ref": candidate.relation_interpretation_ref if candidate else None,
            "interpretation_candidate": candidate.interpretation_candidate if candidate else None,
            "relevance_state": candidate.relevance_state if candidate else None,
            "conditioning_refs": {
                "role_refs": list(candidate.role_refs) if candidate else [],
                "task_refs": list(candidate.task_refs) if candidate else [],
                "goal_refs": list(candidate.goal_refs) if candidate else [],
                "information_need_refs": list(candidate.information_need_refs) if candidate else [],
            },
            "current_world_ref": proof.current_world_ref if proof else None,
            "current_world_relation_interpretation_refs": list(current_world_refs),
            "conditioned_attention_priority_candidate": proof.conditioned_attention_priority_candidate if proof else None,
            "conditioned_hypothesis_statement": proof.conditioned_hypothesis_statement if proof else None,
            "conditioned_world_kind_candidate": proof.conditioned_world_kind_candidate if proof else None,
            "candidate_only": bool(candidate and candidate.candidate_only),
            "field_state_unchanged": _jsonable(field_state) == _jsonable(field_state),
            "raw_relation_direct_assimilation": False,
        }

    def run(self) -> Dict[str, Any]:
        field_state = build_controlled_field_state_candidate_v1()
        original_field_state = _jsonable(field_state)
        projection = RelationStateAssimilationAdapterV1().project(field_state)
        gateway = ObservationGatewayEngineV1().run_case(build_controlled_replay_gateway_request_v1())
        cases = [
            self._run_case(spec, field_state=field_state, projection=projection, gateway=gateway)
            for spec in _specs()
        ]
        by_id = {item["case_id"]: item for item in cases}
        typed_keys = (
            "field_state_candidate_ref", "subject_ref", "predicate", "object_ref",
            "relation_candidate_ref", "relation_semantic_kind", "evidence_refs",
            "source_refs", "provenance_refs", "identity_resolution_status",
            "candidate_only", "fact_admitted", "truth_declared",
            "persistent_relation_declared",
        )
        base_typed = by_id["role-owner"]["typed_relation"]
        same_typed_relation = all(
            all(item["typed_relation"].get(key) == base_typed.get(key) for key in typed_keys)
            for item in cases
        )
        negative_guards = {
            "predicate_preserved": all(item["typed_relation"].get("predicate") == OBSERVED_IN_FIELD for item in cases),
            "subject_preserved": same_typed_relation,
            "object_preserved": all(item["typed_relation"].get("object_ref") == "field:visual-frame:v1" for item in cases),
            "relation_kind_preserved": all(item["typed_relation"].get("relation_semantic_kind") == RELATION_KIND for item in cases),
            "candidate_only": all(item["typed_relation"].get("candidate_only") is True for item in cases),
            "fact_not_declared": all(item["typed_relation"].get("fact_admitted") is False for item in cases),
            "truth_not_declared": all(item["typed_relation"].get("truth_declared") is False for item in cases),
            "persistent_relation_not_declared": all(item["typed_relation"].get("persistent_relation_declared") is False for item in cases),
            "identity_unresolved": all(item["typed_relation"].get("identity_resolution_status") == "UNRESOLVED" for item in cases),
            "field_state_not_mutated": _jsonable(field_state) == original_field_state,
            "raw_relation_cannot_bypass_governance": all(not item["raw_relation_direct_assimilation"] for item in cases),
            "opaque_context_not_interpreted": all(
                item["context_ref"] not in (item["interpretation_candidate"] or "")
                for item in cases
            ),
            "observed_in_field_not_belongs_to_field": all(
                "BELONGS_TO_FIELD" not in (item["interpretation_candidate"] or "")
                for item in cases
            ),
        }
        return {
            "phase": PHASE,
            "source_mode": SOURCE_MODE,
            "execution_mode": CONTROLLED_REPLAY_RUNTIME,
            "provider_invoked": False,
            "model_invoked": False,
            "recorded_provider_result_used": False,
            "field_state_candidate_ref": field_state.state_candidate_id,
            "typed_relation_semantics_same_across_cases": same_typed_relation,
            "cases": cases,
            "negative_guards": negative_guards,
            "contrast_results": {
                "SAME_TYPED_RELATION_DIFFERENT_ROLE": by_id["role-owner"]["interpretation_candidate"] != by_id["role-visitor"]["interpretation_candidate"],
                "SAME_TYPED_RELATION_DIFFERENT_TASK": by_id["task-seat"]["interpretation_candidate"] != by_id["task-exit"]["interpretation_candidate"],
                "SAME_TYPED_RELATION_DIFFERENT_GOAL": by_id["goal-location"]["interpretation_candidate"] != by_id["goal-state"]["interpretation_candidate"],
                "SAME_TYPED_RELATION_DIFFERENT_ROLE_AND_TASK": by_id["role-task-owner"]["interpretation_candidate"] != by_id["role-task-visitor"]["interpretation_candidate"],
                "SAME_TYPED_RELATION_IRRELEVANT_CONDITION_CHANGE": by_id["irrelevant-context-a"]["interpretation_candidate"] == by_id["irrelevant-context-b"]["interpretation_candidate"] and by_id["irrelevant-context-a"]["typed_relation"] == by_id["irrelevant-context-b"]["typed_relation"],
            },
            "current_world_handoff_observed": all(
                item["current_world_ref"]
                and item["relation_interpretation_ref"] in item["current_world_relation_interpretation_refs"]
                for item in cases
            ),
            "validation_errors": [
                f"{item['case_id']}:{error}"
                for item in cases
                for error in item["validation_errors"]
            ],
            "candidate_only": True,
            "field_mutation": False,
            "field_truth_promotion": False,
            "world_truth_declared": False,
            "memory_mutation": False,
            "pcn_mutation": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "provider_model_reasoning": False,
            "cross_field_identity_resolution": False,
        }


__all__ = ["TypedFieldRelationCognitiveConditioningEngineV1"]
