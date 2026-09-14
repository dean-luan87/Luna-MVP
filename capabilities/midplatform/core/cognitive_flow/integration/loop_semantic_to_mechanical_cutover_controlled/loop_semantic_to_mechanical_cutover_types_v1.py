"""Candidate-only inputs for supplying semantic decisions to Loop mechanics.

The types in this module deliberately carry supplied semantic references.  They
do not calculate resume, local disposition, continuity meaning, or closure
reasons.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class LoopResumeMechanicalInputV1:
    loop_ref: str
    work_ref: str
    concern_ref: str
    source_state_version_ref: str
    target_state_version_ref: str
    supplied_resume_decision_ref: str
    supplied_resume_disposition: str
    issuing_owner_ref: str
    grant_ref: str
    reason_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True
    compatibility_source_only: bool = False


@dataclass(frozen=True)
class LoopLocalDispositionRecordV1:
    loop_ref: str
    source_semantic_decision_ref: str
    supplied_local_disposition: str
    source_owner_ref: str
    source_state_version_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True
    compatibility_source_only: bool = False


@dataclass(frozen=True)
class LoopClosureMechanicalInputV1:
    loop_ref: str
    concern_ref: str
    work_ref: str
    source_state_version_ref: str
    closure_request_ref: str
    supplied_closure_reason_ref: str
    supplied_closure_disposition: str
    issuing_owner_ref: str
    grant_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True
    compatibility_source_only: bool = False


@dataclass(frozen=True)
class CutoverCommandResultV1:
    source_ref: str
    supplied_semantic_kind: str
    command_refs: Tuple[str, ...]
    command_kinds: Tuple[str, ...]
    accepted: bool
    semantic_authority_supplied: bool
    mechanical_only: bool
    validation_failure_refs: Tuple[str, ...]
    state_version_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True
