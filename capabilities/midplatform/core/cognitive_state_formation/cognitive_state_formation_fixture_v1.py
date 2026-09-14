"""Synthetic fixtures for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)


@dataclass(frozen=True)
class CognitiveStateFormationFixtureCaseV1:
    case_id: str
    description: str
    request: CognitiveStateFormationInputV1
    expected_world_kind: str
    expected_hypothesis_state: str
    expected_min_attention_count: int
    expect_risk_override: bool
    expect_uncertainty_retention: bool
    expect_conflict_preservation: bool
    expect_revision: bool
    expect_revocation: bool
    synthetic_only: bool = True


def _ref(owner: str, sid: str, group: str, idx: int = 1) -> SourceRefV1:
    rid = f"{group}:{sid}:{idx}"
    return SourceRefV1(
        owner=owner,
        source_ref=rid,
        schema_version="v1",
        trace_ref=f"trace:{sid}:{group}",
        provenance_ref=f"prov:{sid}:{group}",
    )


def _mk_case(
    sid: str,
    description: str,
    expected_world_kind: str,
    expected_hypothesis_state: str,
    expected_min_attention_count: int,
    expect_risk_override: bool,
    expect_uncertainty_retention: bool,
    expect_conflict_preservation: bool,
    expect_revision: bool = False,
    expect_revocation: bool = False,
) -> CognitiveStateFormationFixtureCaseV1:
    request = CognitiveStateFormationInputV1(
        scenario_id=sid,
        context_refs=(_ref("Context Foundation", sid, "context"),),
        pcn_refs=(_ref("Personal Cognitive Network Governance", sid, "pcn"),),
        intent_refs=(_ref("Intent Governance", sid, "intent"),),
        field_refs=(
            _ref("Field State Reducer", sid, "field_state"),
            _ref("Field State Reducer", sid, "field_conflict", 2),
        ),
        observation_refs=(_ref("Observation Governance", sid, "observation"),),
        risk_refs=(_ref("Risk Governance", sid, "risk"),),
        uncertainty_refs=(_ref("Uncertainty Governance", sid, "unknown"),),
        task_refs=(_ref("Task Governance", sid, "task"),),
        role_refs=(_ref("Role Governance", sid, "role"),),
        memory_refs=(_ref("Memory Governance", sid, "memory"),),
        synthetic_only=True,
        candidate_only=True,
    )
    return CognitiveStateFormationFixtureCaseV1(
        case_id=sid,
        description=description,
        request=request,
        expected_world_kind=expected_world_kind,
        expected_hypothesis_state=expected_hypothesis_state,
        expected_min_attention_count=expected_min_attention_count,
        expect_risk_override=expect_risk_override,
        expect_uncertainty_retention=expect_uncertainty_retention,
        expect_conflict_preservation=expect_conflict_preservation,
        expect_revision=expect_revision,
        expect_revocation=expect_revocation,
    )


def get_cognitive_state_formation_fixtures_v1() -> Tuple[
    CognitiveStateFormationFixtureCaseV1, ...
]:
    return (
        _mk_case(
            "S01",
            "single high relevance attention",
            "STABLE_CANDIDATE",
            "SUPPORTED",
            1,
            False,
            False,
            False,
        ),
        _mk_case(
            "S02",
            "risk override intent relevance",
            "CONFLICTED",
            "CONTESTED",
            2,
            True,
            False,
            True,
        ),
        _mk_case(
            "S03",
            "multi attention with uncertainty retention",
            "MULTI_HYPOTHESIS",
            "CONTESTED",
            3,
            False,
            True,
            True,
        ),
        _mk_case(
            "S04",
            "missing attention source",
            "PARTIAL",
            "INSUFFICIENT_EVIDENCE",
            1,
            False,
            True,
            False,
        ),
        _mk_case(
            "S05",
            "single supported hypothesis",
            "STABLE_CANDIDATE",
            "SUPPORTED",
            1,
            False,
            False,
            False,
        ),
        _mk_case(
            "S06",
            "competing hypotheses",
            "MULTI_HYPOTHESIS",
            "CONTESTED",
            2,
            False,
            True,
            True,
        ),
        _mk_case(
            "S07",
            "support accumulation",
            "STABLE_CANDIDATE",
            "SUPPORTED",
            2,
            False,
            False,
            False,
        ),
        _mk_case(
            "S08", "opposition present", "CONFLICTED", "CONTESTED", 2, False, True, True
        ),
        _mk_case(
            "S09",
            "insufficient evidence",
            "UNKNOWN",
            "INSUFFICIENT_EVIDENCE",
            1,
            False,
            True,
            False,
        ),
        _mk_case(
            "S10",
            "hypothesis revision",
            "MULTI_HYPOTHESIS",
            "REVISED",
            2,
            False,
            True,
            True,
            expect_revision=True,
        ),
        _mk_case(
            "S11",
            "hypothesis revocation",
            "PARTIAL",
            "REVOKED",
            1,
            False,
            True,
            False,
            expect_revocation=True,
        ),
        _mk_case(
            "S12",
            "field context conflict",
            "CONFLICTED",
            "CONTESTED",
            2,
            True,
            True,
            True,
        ),
        _mk_case(
            "S13",
            "partial current world",
            "PARTIAL",
            "INSUFFICIENT_EVIDENCE",
            1,
            False,
            True,
            False,
        ),
        _mk_case(
            "S14",
            "unresolved conflict",
            "CONFLICTED",
            "SUSPENDED",
            2,
            False,
            True,
            True,
        ),
        _mk_case(
            "S15",
            "field update world refresh",
            "PARTIAL",
            "CONTESTED",
            2,
            False,
            True,
            True,
        ),
        _mk_case(
            "S16",
            "intent influence without ownership",
            "STABLE_CANDIDATE",
            "SUPPORTED",
            2,
            False,
            False,
            False,
        ),
        _mk_case(
            "S17",
            "cognitive hypothesis to causal handoff",
            "MULTI_HYPOTHESIS",
            "CONTESTED",
            2,
            False,
            True,
            True,
        ),
        _mk_case(
            "S18",
            "current world downstream reference",
            "STABLE_CANDIDATE",
            "SUPPORTED",
            1,
            False,
            False,
            False,
        ),
        _mk_case(
            "S19",
            "provenance reverse lookup",
            "MULTI_HYPOTHESIS",
            "CONTESTED",
            2,
            False,
            True,
            True,
        ),
        _mk_case(
            "S20",
            "source revocation propagation",
            "PARTIAL",
            "REVOKED",
            1,
            False,
            True,
            False,
            expect_revocation=True,
        ),
    )
