"""Reference-only PCN network types for controlled skeleton implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class SourceObjectReference:
    """Reference to a source-owned object; payload/body is intentionally excluded."""

    owner: str
    object_id: str
    object_type: str
    version: str
    reference_uri: Optional[str] = None
    reference_key: Optional[str] = None
    provenance_reference: str = ""


@dataclass(frozen=True)
class CognitiveObjectReference:
    reference_id: str
    source_ref: SourceObjectReference
    confidence: str = "unknown"
    uncertainty: str = "unknown"


@dataclass(frozen=True)
class PCNContextReference:
    context_id: str
    context_version: str
    context_trace_ref: str


@dataclass(frozen=True)
class PCNVersion:
    major: int
    minor: int
    patch: int
    channel: str = "candidate"

    def as_string(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}-{self.channel}"


@dataclass(frozen=True)
class PCNSnapshotCandidate:
    snapshot_id: str
    version: PCNVersion
    source_refs: Tuple[SourceObjectReference, ...]
    context_ref: PCNContextReference
    candidate_only: bool = True
    skeleton_only: bool = True
    runtime_executed: bool = False
