"""Controlled contrast fixtures for the cognitive-logic regression.

The fixtures supply immutable conditioning references and frozen replay inputs;
the runner executes the canonical Observation Gateway → A-Route → Cognitive
State Formation path and records the observed result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    CognitiveReferenceSemanticV1,
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
    ARouteOrchestrationRequestV1,
)
from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    ControlledReplayInputV1,
)
from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import GoalContextV1
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_engine_v1 import (
    ARouteRequiredCognitiveConditionFormationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
    ARouteRequiredCognitiveConditionFormationRequestV1,
    CurrentCognitiveSituationV1,
    GovernedObjectiveConditionRuleV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
    requirement_establishment_from_condition_formation_status_v1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    ObservationIngressRequestV1,
)


PHYSICAL_FIELD = ("field:office:desk", "field:office:document", "field:office:door")
EVIDENCE_BASELINE = ("evidence:office:document-location", "evidence:office:door-location")
RELATION_BASELINE = ("relation:office:document-on-desk", "relation:office:door-shared-area")


@dataclass(frozen=True)
class ContrastSpecV1:
    contrast_id: str
    category: str
    scenario_id: str
    role_ref: str
    task_ref: str
    goal_ref: str
    intent_ref: str
    required_information_refs: Tuple[str, ...]
    available_information_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...] = PHYSICAL_FIELD
    evidence_refs: Tuple[str, ...] = EVIDENCE_BASELINE
    relation_refs: Tuple[str, ...] = RELATION_BASELINE


def _ref(owner: str, source_ref: str, ref_type: str, contrast_id: str) -> SourceRefV1:
    return SourceRefV1(
        owner=owner,
        source_ref=source_ref,
        schema_version="v1",
        trace_ref=f"trace:{contrast_id}:{ref_type.lower()}",
        provenance_ref=f"provenance:{contrast_id}:{ref_type.lower()}",
    )


def _information_need_ref(spec: ContrastSpecV1) -> str:
    if "information:operational-state" in spec.required_information_refs:
        return "information-need:verify-state"
    if "information:exit-location" in spec.required_information_refs or "identify-exit" in spec.goal_ref:
        return "information-need:identify-exit"
    if "locate-target" in spec.goal_ref:
        return "information-need:locate-target"
    return f"information-need:{spec.task_ref.removeprefix('task:')}"


def _semantic_values(spec: ContrastSpecV1) -> Tuple[CognitiveReferenceSemanticV1, ...]:
    target_by_goal = {
        "goal:find-document": "document",
        "goal:identify-exit": "exit",
        "goal:locate-target": "location",
        "goal:verify-state": "operational_state",
        "goal:assess-document": "document",
    }
    task_by_ref = {
        "task:find-document": "find-document",
        "task:identify-exit": "identify-exit",
        "task:assess-target": "assess-target",
        "task:assess-document": "assess-document",
    }
    values = [
        CognitiveReferenceSemanticV1(spec.role_ref, "ROLE", "workspace-owner" if spec.role_ref == "role:workspace-owner" else "visitor"),
        CognitiveReferenceSemanticV1(spec.goal_ref, "TARGET", target_by_goal.get(spec.goal_ref, "unknown")),
        CognitiveReferenceSemanticV1(spec.task_ref, "TASK_LABEL", task_by_ref.get(spec.task_ref, "unknown-task")),
    ]
    topic_by_evidence = {
        "evidence:office:document-location": ("document", "location"),
        "evidence:office:door-location": ("exit", "location"),
        "evidence:office:document-present": ("document",),
        "evidence:office:document-absent": ("document",),
    }
    for ref in spec.evidence_refs:
        for topic in topic_by_evidence.get(ref, ("unknown",)):
            values.append(
                CognitiveReferenceSemanticV1(
                    ref,
                    "EVIDENCE_TOPIC",
                    topic,
                )
            )
        if ref.endswith(":document-absent"):
            values.append(CognitiveReferenceSemanticV1(ref, "EVIDENCE_STATE", "absent"))
    return tuple(values)


def _canonical_establishment_proof(
    spec: ContrastSpecV1,
):
    rules = (
        GovernedObjectiveConditionRuleV1(
            rule_ref=f"rule:full-e2e:{spec.contrast_id}:v1",
            condition_ref=f"condition:full-e2e:{spec.contrast_id}:v1",
            objective_refs=(spec.goal_ref,),
            satisfaction_coverage_refs=spec.required_information_refs,
            source_refs=(f"governance:full-e2e:{spec.contrast_id}:v1",),
            provenance_refs=(f"provenance:full-e2e:{spec.contrast_id}:v1",),
        ),
    ) if spec.required_information_refs else ()
    return ARouteRequiredCognitiveConditionFormationEngineV1().form(
        ARouteRequiredCognitiveConditionFormationRequestV1(
            goal_context=GoalContextV1(
                goal_ref=spec.goal_ref,
                primary_goal=spec.goal_ref,
                secondary_goal_refs=(),
                success_condition_refs=(),
                stop_condition_refs=(),
                provenance={"source": "controlled-full-e2e-fixture"},
                trace=f"trace:full-e2e:{spec.contrast_id}:v1",
            ),
            governed_condition_rules=rules,
            current_situation=CurrentCognitiveSituationV1(
                current_cognitive_coverage_refs=spec.available_information_refs,
            ),
            intent_ref=spec.intent_ref,
            concern_ref=f"concern:{spec.goal_ref.removeprefix('goal:')}",
            context_ref="context:office",
            field_ref="field:office",
            formation_trace_ref=f"trace:full-e2e:required-conditions:{spec.contrast_id}:v1",
        )
    )


def build_request_v1(spec: ContrastSpecV1) -> CognitiveStateFormationInputV1:
    """Retain a direct CState adapter for compatibility with local readers."""
    establishment_status, establishment_basis = requirement_establishment_from_condition_formation_status_v1(
        "CONDITIONS_FORMED"
    )
    return CognitiveStateFormationInputV1(
        scenario_id=spec.scenario_id,
        context_refs=(_ref("Context Foundation", "context:office", "CONTEXT", spec.contrast_id),),
        pcn_refs=(_ref("Personal Cognitive Network Governance", "pcn:office", "PCN", spec.contrast_id),),
        intent_refs=(_ref("Intent Governance", spec.intent_ref, "INTENT", spec.contrast_id),),
        field_refs=tuple(
            _ref("Field State Reducer", ref, "FIELD", spec.contrast_id)
            for ref in spec.field_refs
        ),
        observation_refs=(_ref("Observation Gateway Governance", "observation:office:replay", "OBSERVATION", spec.contrast_id),),
        evidence_refs=tuple(
            _ref("Observation Gateway Governance", ref, "EVIDENCE", spec.contrast_id)
            for ref in spec.evidence_refs
        ),
        task_refs=(_ref("Task Manager", spec.task_ref, "TASK", spec.contrast_id),),
        role_refs=(_ref("Social Self / Role Governance", spec.role_ref, "ROLE", spec.contrast_id),),
        required_information_refs=spec.required_information_refs,
        available_information_refs=spec.available_information_refs,
        requirement_establishment_status=establishment_status,
        requirement_establishment_ref=f"required-conditions:{spec.contrast_id}:v1",
        requirement_establishment_basis=establishment_basis,
        required_cognitive_condition_formation_result=_canonical_establishment_proof(spec),
        semantic_reference_values=_semantic_values(spec),
        synthetic_only=True,
        candidate_only=True,
        execution_ref=f"cognitive-logic-contrast:{spec.contrast_id}",
        goal_refs=(_ref("Goal Governance", spec.goal_ref, "GOAL", spec.contrast_id),),
        concern_refs=(_ref("Concern Governance", f"concern:{spec.goal_ref.removeprefix('goal:')}", "CONCERN", spec.contrast_id),),
        information_need_refs=(_ref("OWNER_UNRESOLVED", _information_need_ref(spec), "INFORMATION_NEED", spec.contrast_id),),
        relation_refs=tuple(
            _ref("Field State Reducer", ref, "RELATION", spec.contrast_id)
            for ref in spec.relation_refs
        ),
    )


def build_replay_inputs_v1(
    spec: ContrastSpecV1,
) -> tuple[ObservationIngressRequestV1, ARouteOrchestrationRequestV1]:
    """Build the real Gateway→A-Route request surface for one contrast."""
    establishment_status, establishment_basis = requirement_establishment_from_condition_formation_status_v1(
        "CONDITIONS_FORMED"
    )
    execution_identity = f"full-e2e-cognitive-logic:{spec.contrast_id}"
    replay = ControlledReplayInputV1(
        replay_input_ref=f"replay-input:full-e2e-cognitive-logic:{spec.contrast_id}:v1",
        replay_version="v1",
        origin_class="CONTROLLED_RECORDED_FIXTURE",
        source_ref=f"controlled-recorded-fixture:full-e2e-cognitive-logic:{spec.contrast_id}",
        evidence_refs=spec.evidence_refs,
        provenance_refs=(
            "provenance:controlled-recorded-fixture:full-e2e-cognitive-logic:v1",
            f"source-version:full-e2e-cognitive-logic:{spec.contrast_id}:v1",
        ),
        ordering_refs=tuple(
            f"order:{spec.contrast_id}:{index:04d}"
            for index, _ in enumerate(spec.evidence_refs, start=1)
        ),
        required_information_refs=spec.required_information_refs,
        available_information_refs=spec.available_information_refs,
        requirement_establishment_status=establishment_status,
        requirement_establishment_ref=f"required-conditions:{spec.contrast_id}:v1",
        requirement_establishment_basis=establishment_basis,
        required_cognitive_condition_formation_result=_canonical_establishment_proof(spec),
    )
    gateway_request = ObservationIngressRequestV1(
        scenario_id=spec.scenario_id,
        ingress_type="VISION",
        provider_ref="recorded-evidence-origin:controlled-fixture",
        source_ref=replay.source_ref,
        payload_ref=replay.replay_input_ref,
        temporal_ref=f"recorded-time:full-e2e-cognitive-logic:{spec.contrast_id}",
        observed_at=f"recorded-time:full-e2e-cognitive-logic:{spec.contrast_id}",
        valid_from_candidate=f"recorded-time:full-e2e-cognitive-logic:{spec.contrast_id}",
        evidence_refs=spec.evidence_refs,
        routing_targets=("Context", "A Route Orchestration"),
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        execution_identity_ref=execution_identity,
        replay_input=replay,
        synthetic_only=False,
        controlled_integration_only=True,
        candidate_only=True,
        multi_evidence_contradiction=any(
            token in ref.lower() for ref in spec.evidence_refs for token in ("absent", "contradict")
        ),
    )
    route_request = ARouteOrchestrationRequestV1(
        scenario_id=spec.scenario_id,
        ingress=ARouteIngressRefsV1(
            field_refs=spec.field_refs,
            relation_refs=spec.relation_refs,
        ),
        context_ref="context:office",
        pcn_ref="pcn:office",
        intent_ref=spec.intent_ref,
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        execution_identity_ref=execution_identity,
        replay_admission=None,
        synthetic_only=False,
        candidate_only=True,
        role_refs=(spec.role_ref,),
        task_refs=(spec.task_ref,),
        goal_refs=(spec.goal_ref,),
        concern_refs=(f"concern:{spec.goal_ref.removeprefix('goal:')}",),
        information_need_refs=(_information_need_ref(spec),),
        semantic_reference_values=_semantic_values(spec),
    )
    return gateway_request, route_request


def get_contrast_specs_v1() -> Tuple[ContrastSpecV1, ...]:
    """Return the minimum controlled contrast set requested by the doctrine."""
    available = ("information:target-identity", "information:target-location")
    return (
        ContrastSpecV1(
            "role-owner", "SAME_FIELD_DIFFERENT_ROLE", "S01", "role:workspace-owner", "task:find-document",
            "goal:find-document", "intent:find-document", available, available,
        ),
        ContrastSpecV1(
            "role-visitor", "SAME_FIELD_DIFFERENT_ROLE", "S01", "role:visitor", "task:find-document",
            "goal:find-document", "intent:find-document", available, available,
        ),
        ContrastSpecV1(
            "task-document", "SAME_FIELD_DIFFERENT_TASK", "S01", "role:workspace-owner", "task:find-document",
            "goal:find-document", "intent:find-document", available, available,
        ),
        ContrastSpecV1(
            "task-exit", "SAME_FIELD_DIFFERENT_TASK", "S01", "role:workspace-owner", "task:identify-exit",
            "goal:identify-exit", "intent:identify-exit", ("information:exit-location",), available,
        ),
        ContrastSpecV1(
            "role-task-owner", "SAME_FIELD_DIFFERENT_ROLE_AND_TASK", "S01", "role:workspace-owner", "task:find-document",
            "goal:find-document", "intent:find-document", available, available,
        ),
        ContrastSpecV1(
            "role-task-visitor", "SAME_FIELD_DIFFERENT_ROLE_AND_TASK", "S01", "role:visitor", "task:identify-exit",
            "goal:identify-exit", "intent:identify-exit", available, available,
        ),
        ContrastSpecV1(
            "goal-locate", "SAME_EVIDENCE_DIFFERENT_GOAL", "S01", "role:workspace-owner", "task:assess-target",
            "goal:locate-target", "intent:locate-target", ("information:target-location",), available,
        ),
        ContrastSpecV1(
            "goal-operational-state", "SAME_EVIDENCE_DIFFERENT_GOAL", "S01", "role:workspace-owner", "task:assess-target",
            "goal:verify-state", "intent:verify-state", ("information:operational-state",), available,
        ),
        ContrastSpecV1(
            "irrelevant-clutter", "SAME_ROLE_TASK_IRRELEVANT_FIELD_CHANGE", "S01", "role:workspace-owner", "task:find-document",
            "goal:find-document", "intent:find-document", available, available,
            field_refs=PHYSICAL_FIELD + ("field:office:irrelevant-clutter",),
        ),
        ContrastSpecV1(
            "missing-evidence", "SAME_GOAL_MISSING_EVIDENCE", "S04", "role:workspace-owner", "task:find-document",
            "goal:find-document", "intent:find-document", available, ("information:target-identity",),
        ),
        ContrastSpecV1(
            "conflicting-evidence", "S02", "S02", "role:workspace-owner", "task:assess-document",
            "goal:assess-document", "intent:assess-document", available, available,
            evidence_refs=("evidence:office:document-present", "evidence:office:document-absent"),
        ),
    )
