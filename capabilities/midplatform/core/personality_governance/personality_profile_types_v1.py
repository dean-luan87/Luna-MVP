"""Non-flattened Personality Profile Candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class PersonalityProfileCandidateV1:
    profile_candidate_id: str
    trait_candidate_refs: Tuple[str, ...]
    uncertain_trait_refs: Tuple[str, ...]
    contested_trait_refs: Tuple[str, ...]
    contradictory_trait_groups: Tuple[Tuple[str, ...], ...]
    context_scope_refs: Tuple[str, ...]
    temporal_scope: str
    confidence_candidate: str
    stability_summary_candidate: str
    revision_parent_ref: Optional[str]
    supersedes_ref: Optional[str]
    revocation_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    sensitivity: str
    candidate_only: bool = True
    activated: bool = False
    persisted: bool = False
    truth_declared: bool = False
    immutable_identity: bool = False
    single_personality_score: Optional[float] = None
    direct_action_control: bool = False


@dataclass(frozen=True)
class PersonalityProfileUpdateCandidateV1:
    update_id: str
    prior_profile_ref: Optional[str]
    next_profile_ref: str
    changed_trait_refs: Tuple[str, ...]
    duplicate_guard_triggered: bool
    trace_ref: str
    candidate_only: bool = True
