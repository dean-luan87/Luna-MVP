"""Synthetic fixture suite for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_core_types_v1 import (
    CycleSnapshotV1,
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_io_types_v1 import (
    CognitiveFlowInputV1,
)


@dataclass(frozen=True)
class CognitiveFlowFixtureCaseV1:
    case_id: str
    description: str
    request: CognitiveFlowInputV1
    expected_final_state: str
    expected_transition_kind: str
    expected_reconsideration: bool
    expected_suspended: bool
    expected_aborted: bool
    expected_inheritance: bool
    expected_memory_candidate: bool
    expected_learning_candidate: bool
    expected_negative_guards: Dict[str, bool]
    synthetic_only: bool = True


def _ref(owner: str, sid: str, group: str, idx: int = 1) -> SourceRefV1:
    return SourceRefV1(
        owner=owner,
        ref_id=f"{group}:{sid}:{idx}",
        ref_type=group.upper(),
        version="v1",
        trace_ref=f"trace:{sid}:{group}",
        provenance_ref=f"prov:{sid}:{group}",
    )


def _snapshot(sid: str) -> CycleSnapshotV1:
    return CycleSnapshotV1(
        cycle_id=f"cycle:{sid}",
        previous_cycle_id=f"cycle:{sid}:prev" if sid in {"C02", "C18"} else None,
        context_refs=(f"context:{sid}:1",),
        pcn_refs=(f"pcn:{sid}:1",),
        intent_refs=(f"intent:{sid}:1", f"intent:{sid}:2")
        if sid == "C23"
        else (f"intent:{sid}:1",),
        state_formation_refs=(f"state_formation:{sid}:1",),
        attention_refs=(f"attention:{sid}:1",),
        hypothesis_refs=(f"hypothesis:{sid}:1", f"hypothesis:{sid}:2")
        if sid in {"C05", "C18"}
        else (f"hypothesis:{sid}:1",),
        current_world_ref=f"current_world:{sid}:1",
        cognitive_state_vector_ref=f"state_vector:{sid}:1",
        regulation_candidate_ref=f"regulation:{sid}:1" if sid not in {"C08"} else None,
        field_refs=(f"field:{sid}:1",),
        causal_refs=(f"causal:{sid}:1",) if sid == "C21" else (),
        snapshot_id=f"snapshot:{sid}",
        trace_ref=f"trace:{sid}:snapshot",
        provenance_refs=(f"prov:{sid}:snapshot",),
    )


def _request(sid: str) -> CognitiveFlowInputV1:
    snapshot = _snapshot(sid)
    return CognitiveFlowInputV1(
        scenario_id=sid,
        cycle_snapshot=snapshot,
        context_refs=(_ref("Context Foundation", sid, "context"),),
        pcn_refs=(_ref("Personal Cognitive Network Governance", sid, "pcn"),),
        intent_refs=(
            _ref("Intent Governance", sid, "intent", 1),
            _ref("Intent Governance", sid, "intent", 2),
        )
        if sid == "C23"
        else (_ref("Intent Governance", sid, "intent"),),
        state_formation_refs=(
            _ref("Cognitive State Formation Governance", sid, "state_formation"),
        ),
        attention_refs=(
            _ref("Cognitive State Formation Governance", sid, "attention"),
        ),
        hypothesis_refs=(
            _ref("Cognitive State Formation Governance", sid, "hypothesis", 1),
            _ref("Cognitive State Formation Governance", sid, "hypothesis", 2),
        )
        if sid in {"C05", "C18"}
        else (_ref("Cognitive State Formation Governance", sid, "hypothesis"),),
        current_world_ref=_ref(
            "Cognitive State Formation Governance", sid, "current_world"
        ),
        cognitive_state_vector_ref=_ref(
            "Cognitive State Formation Governance", sid, "state_vector"
        ),
        regulation_candidate_ref=None
        if sid == "C08"
        else _ref("Dynamic Cognitive Regulation Governance", sid, "regulation"),
        field_refs=(_ref("Field State Reducer", sid, "field"),),
        causal_refs=(_ref("Causal Governance", sid, "causal"),) if sid == "C21" else (),
        synthetic_only=True,
        candidate_only=True,
    )


def _neg_guards() -> Dict[str, bool]:
    return {
        "runtime_execution": False,
        "database_write": False,
        "device_control": False,
        "scheduler_execution": False,
        "task_mutation": False,
        "model_call": False,
        "source_owner_mutation": False,
        "real_side_effect": False,
        "synthetic_only": True,
    }


def get_cognitive_flow_fixtures_v1() -> Tuple[CognitiveFlowFixtureCaseV1, ...]:
    definitions = (
        (
            "C01",
            "normal complete cognitive cycle",
            "COMPLETED",
            "STRICT_SEQUENCE",
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        (
            "C02",
            "persistent intent across two cycles",
            "COMPLETED",
            "CYCLE_INHERITANCE",
            False,
            False,
            False,
            True,
            False,
            False,
        ),
        (
            "C03",
            "context update triggers reconsideration",
            "RECONSIDERING",
            "RECONSIDERATION_FEEDBACK",
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        (
            "C04",
            "field update during state formation",
            "RECONSIDERING",
            "READ_ONLY_PARALLEL",
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        (
            "C05",
            "conflicting hypotheses",
            "RECONSIDERING",
            "RECONSIDERATION_FEEDBACK",
            True,
            False,
            False,
            True,
            False,
            False,
        ),
        (
            "C06",
            "unresolved uncertainty retained",
            "COMPLETED",
            "CYCLE_INHERITANCE",
            False,
            False,
            False,
            True,
            False,
            False,
        ),
        (
            "C07",
            "regulation requests reconsideration",
            "RECONSIDERING",
            "RECONSIDERATION_FEEDBACK",
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        (
            "C08",
            "no regulation change required",
            "COMPLETED",
            "OPTIONAL_REFERENCE",
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        (
            "C09",
            "duplicate cycle start",
            "ABORTED",
            "STRICT_SEQUENCE",
            False,
            False,
            True,
            False,
            False,
            False,
        ),
        (
            "C10",
            "duplicate transition request",
            "ABORTED",
            "STRICT_SEQUENCE",
            False,
            False,
            True,
            False,
            False,
            False,
        ),
        (
            "C11",
            "intent cancellation",
            "ABORTED",
            "RECONSIDERATION_FEEDBACK",
            False,
            False,
            True,
            False,
            False,
            False,
        ),
        (
            "C12",
            "required ref revoked",
            "SUSPENDED",
            "OPTIONAL_REFERENCE",
            False,
            True,
            False,
            False,
            False,
            False,
        ),
        (
            "C13",
            "safety interrupt",
            "SUSPENDED",
            "READ_ONLY_PARALLEL",
            False,
            True,
            False,
            False,
            False,
            False,
        ),
        (
            "C14",
            "resource-driven suspension",
            "SUSPENDED",
            "READ_ONLY_PARALLEL",
            False,
            True,
            False,
            False,
            False,
            False,
        ),
        (
            "C15",
            "controlled resume",
            "INITIALIZING",
            "STRICT_SEQUENCE",
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        (
            "C16",
            "abort after invalid evidence",
            "ABORTED",
            "RECONSIDERATION_FEEDBACK",
            False,
            False,
            True,
            False,
            False,
            False,
        ),
        (
            "C17",
            "completed cycle immutable",
            "COMPLETED",
            "STRICT_SEQUENCE",
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        (
            "C18",
            "next-cycle inheritance",
            "COMPLETED",
            "CYCLE_INHERITANCE",
            False,
            False,
            False,
            True,
            False,
            False,
        ),
        (
            "C19",
            "future memory observation boundary",
            "COMPLETED",
            "DEFERRED_ASYNC_REFERENCE",
            False,
            False,
            False,
            False,
            True,
            False,
        ),
        (
            "C20",
            "future learning boundary",
            "COMPLETED",
            "DEFERRED_ASYNC_REFERENCE",
            False,
            False,
            False,
            False,
            False,
            True,
        ),
        (
            "C21",
            "causal candidate arrives during cycle",
            "COMPLETED",
            "OPTIONAL_REFERENCE",
            False,
            False,
            False,
            False,
            False,
            False,
        ),
        (
            "C22",
            "field state version advances",
            "RECONSIDERING",
            "READ_ONLY_PARALLEL",
            True,
            False,
            False,
            False,
            False,
            False,
        ),
        (
            "C23",
            "multiple intents with one temporary dominant intent",
            "COMPLETED",
            "OPTIONAL_REFERENCE",
            False,
            False,
            False,
            True,
            False,
            False,
        ),
        (
            "C24",
            "regulation candidate rejected by bounds",
            "COMPLETED",
            "RECONSIDERATION_FEEDBACK",
            True,
            False,
            False,
            False,
            False,
            False,
        ),
    )
    return tuple(
        CognitiveFlowFixtureCaseV1(
            case_id=sid,
            description=desc,
            request=_request(sid),
            expected_final_state=state,
            expected_transition_kind=kind,
            expected_reconsideration=reconsider,
            expected_suspended=suspended,
            expected_aborted=aborted,
            expected_inheritance=inheritance,
            expected_memory_candidate=memory,
            expected_learning_candidate=learning,
            expected_negative_guards=_neg_guards(),
        )
        for sid, desc, state, kind, reconsider, suspended, aborted, inheritance, memory, learning in definitions
    )
