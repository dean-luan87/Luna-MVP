from __future__ import annotations

from typing import Dict, Tuple

from .a_route_orchestration_core_types_v1 import (
    ARouteHandoffRecordV1,
    ARouteStageResultV1,
    HANDOFF_STATUSES,
)

STAGE_PRODUCERS: Tuple[Tuple[str, str, str], ...] = (
    ("INGRESS", "Perception / Observation Ingress", "Context Foundation"),
    ("CONTEXT", "Context Foundation", "Personal Cognitive Network Governance"),
    ("PCN", "Personal Cognitive Network Governance", "Intent Governance"),
    ("INTENT", "Intent Governance", "Cognitive State Formation Governance"),
    ("COGNITIVE_STATE", "Cognitive State Formation Governance", "Dynamic Cognitive Regulation Governance"),
    ("REGULATION", "Dynamic Cognitive Regulation Governance", "Decision Governance"),
    ("DECISION", "Decision Governance", "Task Manager"),
    ("TASK", "Task Manager", "Action Governance"),
    ("ACTION", "Action Governance", "Runtime Executor"),
    ("EXECUTION", "Runtime Executor", "Result Observation Boundary"),
    ("RESULT", "Result Observation Boundary", "Result Comparison Boundary"),
    ("FEEDBACK", "Result Comparison Boundary", "Memory / Experience Governance"),
    ("MEMORY_EXPERIENCE", "Memory / Experience Governance", "Cognitive Learning Governance"),
    ("LEARNING", "Cognitive Learning Governance", "Self Governance"),
    ("SELF_CONTINUITY", "Self Governance", "Personality Governance"),
    ("PERSONALITY_CONTEXT", "Personality Governance", "Next Cognitive Cycle"),
)


def stage_contract_ref(stage_id: str) -> str:
    return f"contract:a-route:{stage_id.lower()}:v1"


def stage_adapter_ref(stage_id: str) -> str:
    return f"adapter:a-route:{stage_id.lower()}:v1"


def build_handoff(
    scenario_id: str,
    stage_id: str,
    status: str,
    controlled: bool = True,
    runtime: bool = False,
) -> ARouteHandoffRecordV1:
    producer, consumer = next(
        item[1:] for item in STAGE_PRODUCERS if item[0] == stage_id
    )
    return ARouteHandoffRecordV1(
        handoff_id=f"handoff:{scenario_id}:{stage_id.lower()}",
        producer_owner=producer,
        consumer_owner=consumer,
        status=status,
        contract_ref=stage_contract_ref(stage_id),
        adapter_ref=stage_adapter_ref(stage_id),
        controlled_handoff_ready=controlled,
        runtime_handoff_ready=runtime,
        trace_ref=f"trace:{scenario_id}:handoff:{stage_id.lower()}",
        provenance_refs=(f"prov:{scenario_id}:handoff:{stage_id.lower()}",),
    )


def status_is_valid(status: str) -> bool:
    return status in HANDOFF_STATUSES


def handoff_status_map(handoffs: Tuple[ARouteHandoffRecordV1, ...]) -> Dict[str, str]:
    return {item.handoff_id: item.status for item in handoffs}
