"""Stable types and constants for the Concept Layer fixture DryRun."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


CONCEPT_DRYRUN_SCHEMA_VERSION_V1 = "luna.cognitive_concept.dryrun.v1"
CONCEPT_DRYRUN_PHASE_V1 = "Phase-A3-Cognitive-Concept-Layer-DryRun-v1-001"
CONCEPT_DRYRUN_RESULT_FILENAME_V1 = "cognitive_concept_dryrun_result_v1.json"


@dataclass(frozen=True)
class ConceptDryRunCaseV1:
    """A fixed, non-inferential Concept Skeleton input case."""

    case_id: str
    expected_concept_type: str
    primitive_refs: Tuple[str, ...]
    pattern_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    semantic_description: str


@dataclass(frozen=True)
class ConceptDryRunVerificationIssueV1:
    check_id: str
    message: str
    blocker: bool = True


@dataclass(frozen=True)
class ConceptDryRunVerificationResultV1:
    valid: bool
    issues: Tuple[ConceptDryRunVerificationIssueV1, ...]
    checks_performed: int
    metadata: Mapping[str, object]
