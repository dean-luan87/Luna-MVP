"""Revision/supersession/revocation/expiration types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningRevisionCandidateV1:
    revision_id: str
    prior_learning_candidate_ref: str
    new_learning_candidate_ref: str
    reason: str
    trace_ref: str


@dataclass(frozen=True)
class LearningSupersessionCandidateV1:
    supersession_id: str
    superseded_learning_candidate_ref: str
    superseding_learning_candidate_ref: str
    reason: str
    trace_ref: str


@dataclass(frozen=True)
class LearningRevocationCandidateV1:
    revocation_id: str
    learning_candidate_ref: str
    reason: str
    trace_ref: str


@dataclass(frozen=True)
class LearningExpirationCandidateV1:
    expiration_id: str
    learning_candidate_ref: str
    reason: str
    trace_ref: str
