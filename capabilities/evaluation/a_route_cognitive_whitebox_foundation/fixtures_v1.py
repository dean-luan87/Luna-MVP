from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from .types_v1 import CognitiveWhiteBoxTraceNodeV1, CognitiveWhiteBoxTraceV1


OWNER_A = "owner:A"
OWNER_OBSERVATION = "owner:Observation/FPO"
OWNER_CAPABILITY = "owner:Capability Governance"
OWNER_GATEWAY = "owner:Observation Gateway"


@dataclass(frozen=True)
class CognitiveTraceScenarioV1:
    scenario_id: str
    title: str
    trace: CognitiveWhiteBoxTraceV1
    expected_process: Mapping[str, Any]


def _node(
    case_id: str,
    sequence: int,
    kind: str,
    owner: str,
    source: str,
    *,
    cycle: int | None = 0,
    parent_refs: Tuple[str, ...] = (),
    predecessor_refs: Tuple[str, ...] = (),
    successor_refs: Tuple[str, ...] = (),
    summary: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> CognitiveWhiteBoxTraceNodeV1:
    return CognitiveWhiteBoxTraceNodeV1(
        trace_node_id=f"{case_id}:node:{sequence:02d}",
        node_kind=kind,
        observability_status="currently_observable",
        owner_ref=owner,
        source_ref=source,
        parent_refs=parent_refs,
        predecessor_refs=predecessor_refs,
        successor_refs=successor_refs,
        task_ref=f"task:{case_id}",
        goal_ref=f"goal:{case_id}",
        concern_ref=f"concern:{case_id}",
        observation_cycle_index=cycle,
        sequence_index=sequence,
        timestamp_ref=None,
        provenance_refs=(f"provenance:{case_id}",),
        source_version_refs=(f"source-version:{case_id}:v1",),
        invalidation_refs=(),
        candidate_only=True,
        authoritative=False,
        summary=summary,
        bounded_metadata=dict(metadata or {}),
    )


def _trace(case_id: str, nodes: Tuple[CognitiveWhiteBoxTraceNodeV1, ...], transitions: Tuple[str, ...]) -> CognitiveWhiteBoxTraceV1:
    return CognitiveWhiteBoxTraceV1(
        trace_id=f"cognitive-trace:{case_id}:v1",
        test_case_ref=f"test-case:{case_id}:v1",
        task_ref=f"task:{case_id}",
        goal_ref=f"goal:{case_id}",
        concern_ref=f"concern:{case_id}",
        nodes=nodes,
        transition_refs=transitions,
        provenance_refs=(f"provenance:{case_id}",),
        source_version_refs=(f"source-version:{case_id}:v1",),
        invalidation_refs=(),
        test_board_refs=(f"test-board:cognitive-whitebox:{case_id}",),
    )


def _common(case_id: str, *, cycle: int = 0) -> Tuple[CognitiveWhiteBoxTraceNodeV1, ...]:
    return (
        _node(case_id, 0, "GOAL", OWNER_A, f"goal:{case_id}"),
        _node(case_id, 1, "CONCERN", OWNER_A, f"concern:{case_id}", predecessor_refs=(f"{case_id}:node:00",)),
        _node(case_id, 2, "ATTENTION", OWNER_A, f"attention:{case_id}:target", predecessor_refs=(f"{case_id}:node:01",)),
        _node(case_id, 3, "INFORMATION_NEED", OWNER_A, f"need:{case_id}", predecessor_refs=(f"{case_id}:node:02",)),
        _node(case_id, 4, "OBSERVATION_DEMAND", OWNER_OBSERVATION, f"observation-demand:{case_id}", predecessor_refs=(f"{case_id}:node:03",)),
        _node(case_id, 5, "OBSERVATION_REQUEST", OWNER_OBSERVATION, f"observation-request:{case_id}:cycle:{cycle}", cycle=cycle, predecessor_refs=(f"{case_id}:node:04",), metadata={"roi_ref": f"roi:{case_id}:cycle:{cycle}"}),
        _node(case_id, 6, "CAPABILITY_REQUIREMENT", OWNER_CAPABILITY, f"capability-requirement:{case_id}:cycle:{cycle}", cycle=cycle, predecessor_refs=(f"{case_id}:node:05",)),
        _node(case_id, 7, "OBSERVATION", OWNER_OBSERVATION, f"observation:{case_id}:cycle:{cycle}", cycle=cycle, predecessor_refs=(f"{case_id}:node:06",)),
    )


def build_synthetic_cognitive_trace_cases_v1() -> Tuple[CognitiveTraceScenarioV1, ...]:
    cases = []

    case_id = "obvious_target_single_cycle"
    nodes = _common(case_id) + (
        _node(case_id, 8, "EVIDENCE", OWNER_GATEWAY, f"evidence:{case_id}:1"),
        _node(case_id, 9, "EVIDENCE_RELEVANCE", OWNER_A, f"evidence-relevance:{case_id}:1", predecessor_refs=(f"{case_id}:node:08",)),
        _node(case_id, 10, "CURRENT_WORLD_CANDIDATE", OWNER_A, f"current-world:{case_id}:1"),
        _node(case_id, 11, "HYPOTHESIS", OWNER_A, f"hypothesis:{case_id}:1"),
        _node(case_id, 12, "SUFFICIENCY", OWNER_A, f"sufficiency:{case_id}:1", summary="SUFFICIENT"),
        _node(case_id, 13, "STOP_REASON", OWNER_A, f"stop:{case_id}:sufficient", summary="sufficient_evidence"),
        _node(case_id, 14, "DECISION_GOVERNANCE_HANDOFF", OWNER_A, f"handoff:Decision Governance:{case_id}", summary="handoff_only"),
    )
    cases.append(CognitiveTraceScenarioV1(case_id, "One cycle reaches sufficient candidate evidence", _trace(case_id, nodes, (f"transition:{case_id}:evidence-to-sufficiency",)), {"sufficiency": "SUFFICIENT", "reobservation": False, "handoff": True, "decision_node": False}))

    case_id = "missing_information_requires_reobservation"
    nodes = _common(case_id) + (
        _node(case_id, 8, "EVIDENCE", OWNER_GATEWAY, f"evidence:{case_id}:1"),
        _node(case_id, 9, "EVIDENCE_MISSING", OWNER_A, f"missing-evidence:{case_id}:ocr"),
        _node(case_id, 10, "CURRENT_WORLD_CANDIDATE", OWNER_A, f"current-world:{case_id}:1"),
        _node(case_id, 11, "HYPOTHESIS", OWNER_A, f"hypothesis:{case_id}:1"),
        _node(case_id, 12, "SUFFICIENCY", OWNER_A, f"sufficiency:{case_id}:1", summary="INSUFFICIENT"),
        _node(case_id, 13, "INFORMATION_GAP", OWNER_A, f"information-gap:{case_id}:ocr"),
        _node(case_id, 14, "REOBSERVATION", OWNER_OBSERVATION, f"reobserve:{case_id}:cycle:1", cycle=1, metadata={"reason_ref": f"information-gap:{case_id}:ocr", "target_ref": f"roi:{case_id}:target"}),
    )
    cases.append(CognitiveTraceScenarioV1(case_id, "Missing evidence creates a targeted next observation", _trace(case_id, nodes, (f"transition:{case_id}:gap-to-reobserve",)), {"sufficiency": "INSUFFICIENT", "reobservation": True, "handoff": False, "decision_node": False}))

    case_id = "hypothesis_revision"
    nodes = _common(case_id) + (
        _node(case_id, 8, "EVIDENCE", OWNER_GATEWAY, f"evidence:{case_id}:1"),
        _node(case_id, 9, "CURRENT_WORLD_CANDIDATE", OWNER_A, f"current-world:{case_id}:1"),
        _node(case_id, 10, "HYPOTHESIS", OWNER_A, f"hypothesis:{case_id}:1"),
        _node(case_id, 11, "OBSERVATION_REQUEST", OWNER_OBSERVATION, f"observation-request:{case_id}:cycle:1", cycle=1, metadata={"roi_ref": f"roi:{case_id}:followup"}),
        _node(case_id, 12, "EVIDENCE", OWNER_GATEWAY, f"evidence:{case_id}:2", cycle=1),
        _node(case_id, 13, "HYPOTHESIS_REVISION", OWNER_A, f"hypothesis:{case_id}:2", cycle=1, parent_refs=(f"{case_id}:node:10",), metadata={"revision_parent_ref": f"hypothesis:{case_id}:1"}),
        _node(case_id, 14, "CURRENT_WORLD_CANDIDATE", OWNER_A, f"current-world:{case_id}:2", cycle=1),
        _node(case_id, 15, "SUFFICIENCY", OWNER_A, f"sufficiency:{case_id}:2", cycle=1, summary="SUFFICIENT"),
    )
    cases.append(CognitiveTraceScenarioV1(case_id, "Later evidence revises a prior hypothesis", _trace(case_id, nodes, (f"transition:{case_id}:cycle-0-to-cycle-1",)), {"hypothesis_revision": True, "sufficiency": "SUFFICIENT", "decision_node": False}))

    case_id = "conflicting_evidence"
    nodes = _common(case_id) + (
        _node(case_id, 8, "EVIDENCE", OWNER_GATEWAY, f"evidence:{case_id}:a"),
        _node(case_id, 9, "EVIDENCE", OWNER_GATEWAY, f"evidence:{case_id}:b"),
        _node(case_id, 10, "EVIDENCE_CONFLICT", OWNER_A, f"evidence-conflict:{case_id}:1"),
        _node(case_id, 11, "CURRENT_WORLD_CANDIDATE", OWNER_A, f"current-world:{case_id}:1"),
        _node(case_id, 12, "HYPOTHESIS", OWNER_A, f"hypothesis:{case_id}:1"),
        _node(case_id, 13, "SUFFICIENCY", OWNER_A, f"sufficiency:{case_id}:1", summary="CONTESTED"),
        _node(case_id, 14, "INFORMATION_GAP", OWNER_A, f"information-gap:{case_id}:conflict"),
    )
    cases.append(CognitiveTraceScenarioV1(case_id, "Conflict remains a candidate conflict", _trace(case_id, nodes, (f"transition:{case_id}:conflict-to-gap",)), {"sufficiency": "CONTESTED", "conflict_preserved": True, "world_truth": False}))

    case_id = "premature_sufficiency_guard"
    nodes = _common(case_id) + (
        _node(case_id, 8, "EVIDENCE", OWNER_GATEWAY, f"evidence:{case_id}:partial"),
        _node(case_id, 9, "EVIDENCE_MISSING", OWNER_A, f"missing-evidence:{case_id}:required-kind"),
        _node(case_id, 10, "HYPOTHESIS", OWNER_A, f"hypothesis:{case_id}:1"),
        _node(case_id, 11, "SUFFICIENCY", OWNER_A, f"sufficiency:{case_id}:1", summary="INSUFFICIENT"),
        _node(case_id, 12, "INFORMATION_GAP", OWNER_A, f"information-gap:{case_id}:required-kind"),
    )
    cases.append(CognitiveTraceScenarioV1(case_id, "Incomplete evidence cannot be marked sufficient", _trace(case_id, nodes, (f"transition:{case_id}:missing-to-insufficient",)), {"sufficiency": "INSUFFICIENT", "current_world_candidate": False, "premature_sufficiency": False, "world_truth": False}))

    case_id = "decision_governance_handoff"
    nodes = _common(case_id) + (
        _node(case_id, 8, "EVIDENCE", OWNER_GATEWAY, f"evidence:{case_id}:1"),
        _node(case_id, 9, "CURRENT_WORLD_CANDIDATE", OWNER_A, f"current-world:{case_id}:1"),
        _node(case_id, 10, "HYPOTHESIS", OWNER_A, f"hypothesis:{case_id}:1"),
        _node(case_id, 11, "SUFFICIENCY", OWNER_A, f"sufficiency:{case_id}:1", summary="SUFFICIENT"),
        _node(case_id, 12, "STOP_REASON", OWNER_A, f"stop:{case_id}:handoff", summary="cognition_sufficient"),
        _node(case_id, 13, "DECISION_GOVERNANCE_HANDOFF", OWNER_A, f"handoff:Decision Governance:{case_id}", summary="Decision Governance owns next commitment"),
    )
    cases.append(CognitiveTraceScenarioV1(case_id, "Sufficient cognition hands off without creating Decision", _trace(case_id, nodes, (f"transition:{case_id}:sufficiency-to-handoff",)), {"sufficiency": "SUFFICIENT", "handoff": True, "decision_node": False}))
    return tuple(cases)
