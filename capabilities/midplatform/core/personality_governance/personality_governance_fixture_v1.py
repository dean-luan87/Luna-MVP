"""Deterministic synthetic P01-P36 fixture suite for Personality Governance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .personality_io_types_v1 import PersonalityGovernanceInputV1


@dataclass(frozen=True)
class PersonalityGovernanceFixtureCaseV1:
    scenario_id: str
    title: str
    request: PersonalityGovernanceInputV1
    expected_stability: str
    expected_admission_state: str
    expected_profile: bool = False
    expected_revision: bool = False
    expected_supersession: bool = False
    expected_revocation: bool = False
    expected_expiration: bool = False
    expected_sensitivity: str = "NORMAL"
    expected_duplicate_guard: bool = False
    expected_user_correction: bool = False
    expected_emotion_bridge: bool = False


def _request(
    sid: str,
    title: str,
    dimension: str = "interaction_style",
    value: str = "measured",
    evidence_kind: str = "behavior",
    *,
    source_refs: Tuple[str, ...] = (),
    evidence_refs: Tuple[str, ...] = (),
    memory_refs: Tuple[str, ...] = (),
    learning_refs: Tuple[str, ...] = (),
    self_refs: Tuple[str, ...] = (),
    emotion_refs: Tuple[str, ...] = (),
    regulation_refs: Tuple[str, ...] = (),
    interaction_refs: Tuple[str, ...] = (),
    context_refs: Tuple[str, ...] = ("context:general",),
    uncertainty_refs: Tuple[str, ...] = (),
    contradiction_refs: Tuple[str, ...] = (),
    counterexample_refs: Tuple[str, ...] = (),
    repetition: int = 1,
    temporal_span: int = 1,
    evidence_strength: str = "LOW",
    confidence_candidate: str = "LOW",
    sensitivity: str = "NORMAL",
    user_correction: bool = False,
    user_confirmed: bool = False,
    revision_parent_ref: str | None = None,
    supersedes_ref: str | None = None,
    revocation_refs: Tuple[str, ...] = (),
    expired: bool = False,
    profile_dimensions: Tuple[str, ...] = (),
    profile_trait_refs: Tuple[str, ...] = (),
    profile_context_refs: Tuple[str, ...] = (),
    duplicate_evidence: bool = False,
    duplicate_profile_update: bool = False,
    semantic_compression_ref: str | None = None,
    affective_memory_summary_ref: str | None = None,
    emotion_memory_summary_ref: str | None = None,
    personality_memory_fusion_ref: str | None = None,
) -> PersonalityGovernanceInputV1:
    return PersonalityGovernanceInputV1(
        scenario_id=sid,
        title=title,
        trait_dimension=dimension,
        trait_value_candidate=value,
        evidence_kind=evidence_kind,
        source_refs=source_refs or (f"source:{sid}",),
        evidence_refs=evidence_refs or (f"evidence:{sid}",),
        memory_refs=memory_refs,
        learning_refs=learning_refs,
        self_refs=self_refs,
        emotion_refs=emotion_refs,
        regulation_refs=regulation_refs,
        interaction_refs=interaction_refs,
        context_refs=context_refs,
        uncertainty_refs=uncertainty_refs,
        contradiction_refs=contradiction_refs,
        counterexample_refs=counterexample_refs,
        repetition=repetition,
        temporal_span=temporal_span,
        evidence_strength=evidence_strength,
        confidence_candidate=confidence_candidate,
        sensitivity=sensitivity,
        user_correction=user_correction,
        user_confirmed=user_confirmed,
        revision_parent_ref=revision_parent_ref,
        supersedes_ref=supersedes_ref,
        revocation_refs=revocation_refs,
        expired=expired,
        profile_dimensions=profile_dimensions,
        profile_trait_refs=profile_trait_refs,
        profile_context_refs=profile_context_refs,
        duplicate_evidence=duplicate_evidence,
        duplicate_profile_update=duplicate_profile_update,
        semantic_compression_ref=semantic_compression_ref,
        affective_memory_summary_ref=affective_memory_summary_ref,
        emotion_memory_summary_ref=emotion_memory_summary_ref,
        personality_memory_fusion_ref=personality_memory_fusion_ref,
    )


def get_personality_governance_fixture_v1() -> Tuple[PersonalityGovernanceFixtureCaseV1, ...]:
    return (
        PersonalityGovernanceFixtureCaseV1("P01", "basic trait evidence", _request("P01", "basic trait evidence", source_refs=("interaction:P01",), evidence_refs=("evidence:P01",), repetition=1), "EMERGING", "INSUFFICIENT_EVIDENCE"),
        PersonalityGovernanceFixtureCaseV1("P02", "single event does not become trait", _request("P02", "single event does not become trait", repetition=1), "EMERGING", "INSUFFICIENT_EVIDENCE"),
        PersonalityGovernanceFixtureCaseV1("P03", "repeated same-context behavior", _request("P03", "repeated same-context behavior", repetition=4, temporal_span=2, context_refs=("context:work",), evidence_strength="MEDIUM"), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P04", "cross-context behavior evidence", _request("P04", "cross-context behavior evidence", repetition=6, temporal_span=3, context_refs=("context:work", "context:home"), evidence_strength="HIGH", confidence_candidate="MEDIUM"), "STABLE_CANDIDATE", "ADMITTED_CANDIDATE"),
        PersonalityGovernanceFixtureCaseV1("P05", "long temporal span", _request("P05", "long temporal span", repetition=6, temporal_span=10, context_refs=("context:work", "context:home"), evidence_strength="HIGH"), "STABLE_CANDIDATE", "ADMITTED_CANDIDATE"),
        PersonalityGovernanceFixtureCaseV1("P06", "counterexample lowers stability", _request("P06", "counterexample lowers stability", repetition=5, temporal_span=4, context_refs=("context:work", "context:home"), counterexample_refs=("counterexample:P06",), evidence_strength="HIGH"), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P07", "contradiction preserved", _request("P07", "contradiction preserved", repetition=4, temporal_span=4, context_refs=("context:work", "context:home"), contradiction_refs=("contradiction:P07",), evidence_strength="HIGH"), "CONTESTED", "CONTESTED"),
        PersonalityGovernanceFixtureCaseV1("P08", "explicit user correction", _request("P08", "explicit user correction", repetition=4, temporal_span=4, context_refs=("context:work", "context:home"), user_correction=True, revision_parent_ref="trait:P08:prior", evidence_strength="HIGH"), "REVISING", "REVISED", expected_revision=True, expected_user_correction=True),
        PersonalityGovernanceFixtureCaseV1("P09", "preference != personality", _request("P09", "preference != personality", dimension="support_style_candidate", evidence_kind="preference", repetition=1), "EMERGING", "INSUFFICIENT_EVIDENCE"),
        PersonalityGovernanceFixtureCaseV1("P10", "role != personality", _request("P10", "role != personality", dimension="formality", evidence_kind="role_behavior", context_refs=("role:operator",), repetition=2), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P11", "relationship behavior != global personality", _request("P11", "relationship behavior != global personality", dimension="social_openness", evidence_kind="relationship_behavior", context_refs=("relationship:friend",), interaction_refs=("interaction:P11",), repetition=3), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P12", "self attribution != personality", _request("P12", "self attribution != personality", self_refs=("self:attribution:P12",), evidence_kind="self_evidence", repetition=2), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P13", "learning pattern evidence", _request("P13", "learning pattern evidence", learning_refs=("learning:P13",), evidence_kind="learning_pattern", repetition=2), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P14", "learning cannot activate trait", _request("P14", "learning cannot activate trait", learning_refs=("learning:P14",), evidence_kind="learning_pattern", repetition=4, temporal_span=2), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P15", "memory evidence", _request("P15", "memory evidence", memory_refs=("memory:P15",), evidence_kind="memory_behavior", repetition=2), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P16", "memory cannot mutate personality", _request("P16", "memory cannot mutate personality", memory_refs=("memory:P16",), evidence_kind="memory_behavior", repetition=3), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P17", "emotion evidence", _request("P17", "emotion evidence", dimension="empathy_expression_tendency", emotion_refs=("emotion:P17",), evidence_kind="emotion_evidence", repetition=2), "TENTATIVE", "EVIDENCE_ACCUMULATING", expected_emotion_bridge=True),
        PersonalityGovernanceFixtureCaseV1("P18", "temporary emotion not personality", _request("P18", "temporary emotion not personality", emotion_refs=("emotion:P18",), evidence_kind="temporary_mood", repetition=1), "EMERGING", "INSUFFICIENT_EVIDENCE", expected_emotion_bridge=True),
        PersonalityGovernanceFixtureCaseV1("P19", "repeated emotional pattern remains candidate", _request("P19", "repeated emotional pattern remains candidate", emotion_refs=("emotion:P19",), evidence_kind="repeated_emotion", repetition=5, temporal_span=5, context_refs=("context:work",), evidence_strength="HIGH"), "TENTATIVE", "EVIDENCE_ACCUMULATING", expected_emotion_bridge=True),
        PersonalityGovernanceFixtureCaseV1("P20", "regulation pattern evidence", _request("P20", "regulation pattern evidence", regulation_refs=("regulation:P20",), evidence_kind="regulation_pattern", repetition=2, temporal_span=4, context_refs=("context:work", "context:home"), evidence_strength="MEDIUM"), "SEMI_STABLE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P21", "regulation parameter not personality", _request("P21", "regulation parameter not personality", regulation_refs=("parameter:P21",), evidence_kind="regulation_parameter", repetition=1), "EMERGING", "INSUFFICIENT_EVIDENCE"),
        PersonalityGovernanceFixtureCaseV1("P22", "personality profile formation", _request("P22", "personality profile formation", dimension="interaction_style", repetition=4, temporal_span=4, context_refs=("context:work", "context:home"), profile_dimensions=("interaction_style", "reflection_tendency"), profile_trait_refs=("trait:P22:reflection_tendency",), evidence_strength="HIGH"), "STABLE_CANDIDATE", "ADMITTED_CANDIDATE", expected_profile=True),
        PersonalityGovernanceFixtureCaseV1("P23", "contested trait", _request("P23", "contested trait", contradiction_refs=("contradiction:P23",), profile_dimensions=("directness", "formality"), context_refs=("context:work", "context:home"), repetition=4, temporal_span=4), "CONTESTED", "CONTESTED", expected_profile=True),
        PersonalityGovernanceFixtureCaseV1("P24", "trait revision", _request("P24", "trait revision", revision_parent_ref="trait:P24:prior", repetition=3, temporal_span=3, context_refs=("context:work", "context:home")), "REVISING", "REVISED", expected_revision=True),
        PersonalityGovernanceFixtureCaseV1("P25", "supersession", _request("P25", "supersession", supersedes_ref="trait:P25:prior", repetition=4, temporal_span=3, context_refs=("context:work", "context:home")), "STABLE_CANDIDATE", "ADMITTED_CANDIDATE", expected_supersession=True),
        PersonalityGovernanceFixtureCaseV1("P26", "revocation", _request("P26", "revocation", revocation_refs=("revocation:P26",), repetition=3), "REVOKED", "REVOKED", expected_revocation=True),
        PersonalityGovernanceFixtureCaseV1("P27", "expiration", _request("P27", "expiration", expired=True, repetition=3), "EXPIRED", "EXPIRED", expected_expiration=True),
        PersonalityGovernanceFixtureCaseV1("P28", "sensitive trait", _request("P28", "sensitive trait", sensitivity="HIGH_SENSITIVITY", repetition=2, confidence_candidate="MEDIUM"), "TENTATIVE", "NEEDS_CONFIRMATION", expected_sensitivity="HIGH_SENSITIVITY"),
        PersonalityGovernanceFixtureCaseV1("P29", "do-not-transfer", _request("P29", "do-not-transfer", sensitivity="DO_NOT_TRANSFER", repetition=2), "TENTATIVE", "EVIDENCE_ACCUMULATING", expected_sensitivity="DO_NOT_TRANSFER"),
        PersonalityGovernanceFixtureCaseV1("P30", "trace reverse lookup", _request("P30", "trace reverse lookup", source_refs=("source:P30", "cycle:P30:source"), evidence_refs=("evidence:P30",), repetition=2), "TENTATIVE", "EVIDENCE_ACCUMULATING"),
        PersonalityGovernanceFixtureCaseV1("P31", "duplicate candidate guard", _request("P31", "duplicate candidate guard", evidence_refs=("evidence:P31", "evidence:P31"), duplicate_evidence=True, repetition=2), "TENTATIVE", "EVIDENCE_ACCUMULATING", expected_duplicate_guard=True),
        PersonalityGovernanceFixtureCaseV1("P32", "semantic compression absent but system remains valid", _request("P32", "semantic compression absent but system remains valid", memory_refs=("memory:P32",), evidence_kind="memory_experience", repetition=1), "EMERGING", "INSUFFICIENT_EVIDENCE"),
        PersonalityGovernanceFixtureCaseV1("P33", "user-confirmed personality evidence", _request("P33", "user-confirmed personality evidence", user_confirmed=True, sensitivity="USER_CONFIRMATION_REQUIRED", repetition=3, temporal_span=3, context_refs=("context:work", "context:home"), evidence_strength="HIGH"), "SEMI_STABLE", "ADMITTED_CANDIDATE", expected_sensitivity="USER_CONFIRMATION_REQUIRED"),
        PersonalityGovernanceFixtureCaseV1("P34", "personality-expression vs personality-structure distinction", _request("P34", "personality-expression vs personality-structure distinction", dimension="expressiveness", evidence_kind="expression_context", emotion_refs=("emotion:P34",), regulation_refs=("regulation:P34",), repetition=2), "TENTATIVE", "EVIDENCE_ACCUMULATING", expected_emotion_bridge=True),
        PersonalityGovernanceFixtureCaseV1("P35", "context-specific trait candidate", _request("P35", "context-specific trait candidate", dimension="conflict_style_candidate", context_refs=("pcn:role:reviewer",), sensitivity="DO_NOT_GENERALIZE", repetition=5, temporal_span=6, evidence_strength="HIGH"), "TENTATIVE", "EVIDENCE_ACCUMULATING", expected_sensitivity="DO_NOT_GENERALIZE"),
        PersonalityGovernanceFixtureCaseV1("P36", "unresolved personality candidate", _request("P36", "unresolved personality candidate", uncertainty_refs=("uncertainty:P36",), repetition=2), "EMERGING", "NEEDS_CONFIRMATION"),
    )
