"""Candidate-only CSA and Official Capability Catalog contracts.

The catalog is a metadata projection under the existing Capability Registry /
Capability Governance owner.  It does not install, activate, invoke, or
rewrite any capability state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Tuple


ASSET_CLASS_VALUES = (
    "CAPABILITY_MODULE",
    "IMPLEMENTATION",
    "MODEL",
    "PROVIDER",
    "SUPPORTING_ASSET",
    "KNOWLEDGE_REFERENCE",
)
MAPPING_CONFIDENCE_VALUES = ("HIGH", "MEDIUM", "LOW", "MAPPING_REVIEW_REQUIRED")
CSA_SEMANTIC_DEPTH = "MINIMAL"


@dataclass(frozen=True)
class CapabilitySemanticAnnotationV1:
    capability_semantic_annotation_id: str
    module_ref: str
    semantic_purpose: str
    applicable_problem_classes: Tuple[str, ...]
    applicable_situation_descriptions: Tuple[str, ...]
    expected_contribution: Tuple[str, ...]
    capability_boundaries: Tuple[str, ...]
    known_non_capabilities: Tuple[str, ...]
    typical_requirement_hints: Tuple[str, ...]
    semantic_depth: str = CSA_SEMANTIC_DEPTH
    semantic_authority: bool = False
    world_truth_authority: bool = False
    action_authority: bool = False
    candidate_only: bool = True
    descriptive_only: bool = True
    srsk_consumption_deferred: bool = True
    dynamic_semantic_expansion: bool = False
    dynamic_semantic_folding: bool = False
    semantic_sufficiency_execution: bool = False


@dataclass(frozen=True)
class OfficialCapabilityCatalogEntryV1:
    catalog_entry_id: str
    module_ref: str
    capability_domain: str
    requirement_class: str
    csa_ref: str
    implementation_refs: Tuple[str, ...]
    model_refs: Tuple[str, ...]
    provider_refs: Tuple[str, ...]
    slot_compatibility_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    health_refs: Tuple[str, ...]
    recovery_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    lifecycle_refs: Tuple[str, ...]
    origin: str = "OFFICIAL"
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityAssetMappingV1:
    existing_asset: str
    current_owner: str
    classification: str
    mapped_capability_module: str
    implementation_ref: str
    model_ref: str
    provider_ref: str
    supporting_asset_ref: str
    csa_ref: str
    mapping_confidence: str
    mapping_reason: str
    conflict_or_gap: str


@dataclass(frozen=True)
class SlotCompatibilityMappingV1:
    module_ref: str
    slot_contract_ref: str
    compatibility_refs: Tuple[str, ...]
    generic_slot_only: bool = True
    safety_slot_specialization: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class OfficialCapabilityCatalogV1:
    catalog_id: str
    catalog_version: str
    entries: Tuple[OfficialCapabilityCatalogEntryV1, ...]
    annotations: Tuple[CapabilitySemanticAnnotationV1, ...]
    asset_mappings: Tuple[CapabilityAssetMappingV1, ...]
    slot_mappings: Tuple[SlotCompatibilityMappingV1, ...]
    market_governance_status: str = "DEFERRED"
    candidate_only: bool = True
    runtime_execution: bool = False
    provider_invocation: bool = False
    model_inference: bool = False


def to_dict(value: object) -> dict:
    return asdict(value)
