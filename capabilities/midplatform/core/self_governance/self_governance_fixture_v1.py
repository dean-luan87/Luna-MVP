"""Frozen synthetic fixture suite mapped one-to-one to planning scenarios."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .self_io_types_v1 import SelfGovernanceInputV1


_SCENARIO_TITLES: Tuple[Tuple[str, str], ...] = (
    ("S01", "basic self reference"),
    ("S02", "own intent attribution"),
    ("S03", "external person's intent not self"),
    ("S04", "preference evidence candidate"),
    ("S05", "repeated preference does not become immutable self fact"),
    ("S06", "explicit correction revises self attribution"),
    ("S07", "role attribution"),
    ("S08", "role expires"),
    ("S09", "relationship position reference"),
    ("S10", "relationship change revises self understanding"),
    ("S11", "capability attribution"),
    ("S12", "temporary resource limitation not permanent capability trait"),
    ("S13", "own experience attribution"),
    ("S14", "observed other's experience not self"),
    ("S15", "self-related memory influence"),
    ("S16", "memory contradiction"),
    ("S17", "learning self-evolution evidence"),
    ("S18", "learning cannot mutate self directly"),
    ("S19", "regulation tendency reference"),
    ("S20", "regulation parameter not self identity"),
    ("S21", "emotional evidence reference only"),
    ("S22", "emotion cannot mutate self directly"),
    ("S23", "personality evidence future boundary"),
    ("S24", "personality not implemented here"),
    ("S25", "contested identity attribution"),
    ("S26", "explicit user confirmation"),
    ("S27", "revocation"),
    ("S28", "provenance reverse lookup"),
    ("S29", "duplicate attribution guard"),
    ("S30", "continuity across cycle"),
    ("S31", "stale preference expiration"),
    ("S32", "sensitive self information"),
    ("S33", "do-not-transfer self evidence"),
    ("S34", "unresolved attribution remains uncertain"),
)

_BOUNDARIES: Dict[str, str] = {
    "S03": "OTHER", "S09": "SHARED", "S12": "SYSTEM", "S14": "OTHER",
    "S16": "CONTESTED", "S20": "SYSTEM", "S25": "CONTESTED", "S34": "UNKNOWN",
}
_DOMAINS: Dict[str, str] = {
    "S02": "OWN_INTENT", "S04": "PREFERENCE", "S05": "PREFERENCE",
    "S06": "PREFERENCE", "S07": "ROLE", "S08": "ROLE",
    "S09": "RELATIONSHIP_POSITION", "S10": "RELATIONSHIP_POSITION",
    "S11": "CAPABILITY", "S12": "LIMITATION", "S13": "AUTOBIOGRAPHICAL",
    "S14": "AUTOBIOGRAPHICAL", "S15": "OWN_MEMORY", "S16": "OWN_MEMORY",
    "S17": "OWN_LEARNING_PATTERN", "S18": "OWN_LEARNING_PATTERN",
    "S19": "OWN_REGULATION_TENDENCY", "S20": "RESOURCE_CONDITION",
    "S21": "OWN_EMOTIONAL_EVIDENCE", "S22": "OWN_EMOTIONAL_EVIDENCE",
    "S23": "OWN_PERSONALITY_EVIDENCE", "S24": "OWN_PERSONALITY_EVIDENCE",
    "S25": "IDENTITY", "S26": "IDENTITY", "S27": "IDENTITY",
    "S31": "PREFERENCE", "S32": "AUTOBIOGRAPHICAL", "S33": "AUTOBIOGRAPHICAL",
    "S34": "UNCERTAIN_SELF",
}
_STATES: Dict[str, str] = {
    "S03": "REJECTED", "S06": "REVISED", "S08": "EXPIRED", "S10": "REVISED",
    "S12": "TEMPORARY", "S14": "REJECTED", "S16": "CONTESTED", "S17": "PROPOSED",
    "S18": "PROPOSED", "S20": "PROPOSED", "S21": "PROPOSED", "S22": "PROPOSED",
    "S23": "NEEDS_CONFIRMATION", "S24": "PROPOSED", "S25": "CONTESTED",
    "S26": "ADMITTED_CANDIDATE", "S27": "REVOKED", "S31": "EXPIRED",
    "S32": "NEEDS_CONFIRMATION", "S33": "PROPOSED", "S34": "INSUFFICIENT_EVIDENCE",
}


@dataclass(frozen=True)
class SelfGovernanceFixtureCaseV1:
    scenario_id: str
    title: str
    request: SelfGovernanceInputV1
    expected_boundary_class: str
    expected_state: str
    expected_domain: str
    expected_continuity: bool
    expected_revision: bool
    expected_revocation: bool
    expected_supersession: bool
    expected_expiration: bool
    expected_influence_kinds: Tuple[str, ...]
    expected_sensitivity: str
    expected_duplicate_guard: bool = False
    expected_user_correction_precedence: bool = False


def get_self_governance_fixture_v1() -> Tuple[SelfGovernanceFixtureCaseV1, ...]:
    cases = []
    for sid, title in _SCENARIO_TITLES:
        boundary = _BOUNDARIES.get(sid, "SELF")
        domain = _DOMAINS.get(sid, "IDENTITY")
        sensitivity = "HIGH_SENSITIVITY" if sid == "S32" else "DO_NOT_TRANSFER" if sid == "S33" else "NORMAL"
        influence = {
            "S15": ("MEMORY_EVIDENCE",),
            "S17": ("SELF_EVOLUTION_EVIDENCE",),
            "S19": ("REGULATION_EVIDENCE",),
            "S20": ("REGULATION_PARAMETER_EVIDENCE",),
            "S21": ("EMOTION_EVIDENCE_TO_SELF",),
            "S23": ("PERSONALITY_EVIDENCE",),
        }.get(sid, ())
        request = SelfGovernanceInputV1(
            scenario_id=sid,
            statement=title,
            source_owner="Synthetic Fixture Source",
            source_refs=(f"source:{sid}",),
            evidence_refs=(f"evidence:{sid}",),
            provenance_refs=(f"provenance:{sid}",),
            root_cycle_trace_id=f"cycle:{sid}",
            temporal_validity="EXPIRED" if sid in {"S08", "S31"} else "TRANSIENT",
            uncertainty="HIGH" if sid == "S34" else "MEDIUM",
            sensitivity=sensitivity,
            boundary_class=boundary,
            requested_domain=domain,
            user_correction=sid == "S06",
            replayed_evidence=sid == "S29",
            duplicate_request=sid == "S29",
            prior_self_candidate_ref=f"attribution:{sid}:prior" if sid in {"S06", "S10"} else None,
            current_self_candidate_ref=f"attribution:{sid}:current" if sid == "S30" else None,
            source_intent_refs=(f"intent:{sid}",) if sid == "S02" else (),
            source_memory_refs=(f"memory:{sid}",) if sid in {"S15", "S16"} else (),
            source_learning_refs=(f"learning:{sid}",) if sid in {"S17", "S18"} else (),
            source_regulation_refs=(f"regulation:{sid}",) if sid in {"S19", "S20"} else (),
            source_context_refs=(f"context:{sid}",),
        )
        cases.append(SelfGovernanceFixtureCaseV1(
            scenario_id=sid,
            title=title,
            request=request,
            expected_boundary_class=boundary,
            expected_state=_STATES.get(sid, "PROPOSED"),
            expected_domain=domain,
            expected_continuity=sid == "S30",
            expected_revision=sid in {"S06", "S10"},
            expected_revocation=sid == "S27",
            expected_supersession=sid == "S10",
            expected_expiration=sid in {"S08", "S31"},
            expected_influence_kinds=influence,
            expected_sensitivity=sensitivity,
            expected_duplicate_guard=sid == "S29",
            expected_user_correction_precedence=sid == "S06",
        ))
    return tuple(cases)
