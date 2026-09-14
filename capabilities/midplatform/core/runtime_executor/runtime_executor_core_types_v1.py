"""Core source reference types for Runtime Executor controlled implementation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceRefV1:
    owner: str
    ref_id: str
    ref_type: str
    read_only: bool = True
    reference_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class OwnerIdentityV1:
    canonical_owner: str
    legacy_alias: str | None = None
    mutation_authority: bool = False
