"""Core shared datatypes for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


ReverseLookupPairsV1 = Tuple[Tuple[str, Tuple[str, ...]], ...]


def _validate_reverse_lookup(value: object) -> None:
    if not isinstance(value, tuple):
        raise TypeError("reverse_lookup_must_be_tuple_of_pairs")
    keys = set()
    for item in value:
        if not isinstance(item, tuple) or len(item) != 2:
            raise TypeError("reverse_lookup_pair_must_be_two_tuple")
        key, refs = item
        if not isinstance(key, str) or not key.strip():
            raise ValueError("reverse_lookup_key_must_be_non_empty_string")
        if not isinstance(refs, tuple):
            raise TypeError("reverse_lookup_refs_must_be_tuple")
        if any(not isinstance(ref, str) or not ref.strip() for ref in refs):
            raise ValueError("reverse_lookup_refs_must_be_non_empty_strings")
        if key in keys:
            raise ValueError("reverse_lookup_duplicate_key")
        keys.add(key)


@dataclass(frozen=True)
class CognitiveReferenceSemanticV1:
    """Typed semantic payload paired with an opaque reference identity.

    ``source_ref`` remains an identity/provenance handle.  Semantic
    conditioning may use this record only when an upstream governed adapter
    supplies the payload explicitly.
    """

    source_ref: str
    semantic_kind: str
    semantic_value: str


@dataclass(frozen=True)
class SourceRefV1:
    owner: str
    source_ref: str
    schema_version: str
    trace_ref: str
    provenance_ref: str
    read_only: bool = True
    reference_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class NegativeGuardStatusV1:
    candidate_only: bool
    context_mutation: bool
    pcn_mutation: bool
    intent_mutation: bool
    field_mutation: bool
    causal_mutation: bool
    decision_output: bool
    action_output: bool
    task_output: bool
    database_write: bool
    device_control: bool
    scheduler_execution: bool
    runtime_side_effect: bool
    model_call: bool
    learning_update: bool
    self_regulation_update: bool
    dynamic_parameter_mutation: bool
    single_truth_collapse: bool


@dataclass(frozen=True)
class TraceEnvelopeV1:
    root_trace_id: str
    attention_trace_ref: str
    hypothesis_trace_ref: str
    current_world_trace_ref: str
    downstream_handoff_trace_ref: str
    revision_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    revocation_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    source_version_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    alternative_hypothesis_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ProvenanceEnvelopeV1:
    source_refs: Tuple[str, ...]
    owner_refs: Tuple[str, ...]
    version_refs: Tuple[str, ...]
    reverse_lookup: ReverseLookupPairsV1

    def __post_init__(self) -> None:
        _validate_reverse_lookup(self.reverse_lookup)


@dataclass(frozen=True)
class CognitiveStateVersionRecordV1:
    """Owner-issued immutable cognitive-state version record."""

    cognitive_state_ref: str
    version_ref: str
    source_version_refs: Tuple[Tuple[str, str], ...]
    source_identity_refs: Tuple[str, ...]
    alignment_basis_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    unknown_refs: Tuple[str, ...]
    stale_refs: Tuple[str, ...]
    profile_ref: str
    owner_ref: str
    status: str
    invalidation_reason_ref: str | None = None
    candidate_only: bool = False
    canonical: bool = True

    def __post_init__(self) -> None:
        scalar_fields = (
            self.cognitive_state_ref,
            self.version_ref,
            self.profile_ref,
            self.owner_ref,
            self.status,
        )
        if any(not isinstance(value, str) or not value.strip() for value in scalar_fields):
            raise ValueError("cognitive_state_version_record_scalar_invalid")
        if not isinstance(self.source_version_refs, tuple):
            raise TypeError("cognitive_state_version_source_versions_must_be_tuple")
        source_keys = set()
        for item in self.source_version_refs:
            if (
                not isinstance(item, tuple)
                or len(item) != 2
                or any(not isinstance(value, str) or not value.strip() for value in item)
            ):
                raise ValueError("cognitive_state_version_source_version_pair_invalid")
            if item[0] in source_keys:
                raise ValueError("cognitive_state_version_source_version_duplicate")
            source_keys.add(item[0])
        for name in (
            "source_identity_refs",
            "alignment_basis_refs",
            "provenance_refs",
            "unknown_refs",
            "stale_refs",
        ):
            value = getattr(self, name)
            if not isinstance(value, tuple) or any(
                not isinstance(item, str) or not item.strip() for item in value
            ):
                raise ValueError(f"cognitive_state_version_{name}_invalid")
        if self.invalidation_reason_ref is not None and (
            not isinstance(self.invalidation_reason_ref, str)
            or not self.invalidation_reason_ref.strip()
        ):
            raise ValueError("cognitive_state_version_invalidation_reason_invalid")
        if self.candidate_only is not False or self.canonical is not True:
            raise ValueError("cognitive_state_version_authority_flags_invalid")
