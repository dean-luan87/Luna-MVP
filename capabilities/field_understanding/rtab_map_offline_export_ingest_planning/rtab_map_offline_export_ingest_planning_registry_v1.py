# -*- coding: utf-8 -*-
"""RTAB-Map Offline Export Ingest Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.rtab_map_offline_export_ingest_planning.rtab_map_offline_export_ingest_planning_types_v1 import (
    ADAPTER_PROFILE_REF,
    EXPORT_SUBSET_REFS,
    FORBIDDEN_ARCHITECTURE_RULES,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_FAMILY,
    MODEL_ID,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    OBSERVATION_EXPORT_SUBSETS,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    P0_EXPORT_SUBSETS,
    P1_EXPORT_SUBSETS,
    P2_EXPORT_SUBSETS,
    SOURCE_INTERNAL_STANDARD,
    SUBSET_PLANNING_FIELDS,
    TARGET_ENTRYPOINT,
)

REGISTRY_ID = "rtab_map_offline_export_ingest_planning_registry_v1"
PLANNING_REF = "rtab_map_offline_export_ingest_planning_v1"

SUBSET_PLANNING_DIMENSIONS: Tuple[str, ...] = (
    "source_export_kind",
    "expected_fields",
    "required_fields",
    "optional_fields",
    "luna_candidate_mapping",
    "generic_json_trace_mapping",
    "lossy_conversion_notes",
    "unsupported_fields",
    "offline_feasibility",
    "parser_priority",
    "risk_level",
)

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "export_subset_refs": EXPORT_SUBSET_REFS,
    "subset_planning_dimensions": SUBSET_PLANNING_DIMENSIONS,
    "forbidden_architecture_rules": FORBIDDEN_ARCHITECTURE_RULES,
    "p0_export_subsets": P0_EXPORT_SUBSETS,
    "p1_export_subsets": P1_EXPORT_SUBSETS,
    "p2_export_subsets": P2_EXPORT_SUBSETS,
    "observation_export_subsets": OBSERVATION_EXPORT_SUBSETS,
}

MODEL_BINDING: Dict[str, str] = {
    "model_id": MODEL_ID,
    "model_family": MODEL_FAMILY,
    "domain_id": "spatial_evidence",
    "model_management_protocol_ref": MODEL_MANAGEMENT_PROTOCOL_REF,
    "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
    "adapter_profile_ref": ADAPTER_PROFILE_REF,
    "output_candidate_contract_ref": OUTPUT_CANDIDATE_CONTRACT_REF,
    "source_internal_standard": SOURCE_INTERNAL_STANDARD,
    "target_entrypoint": TARGET_ENTRYPOINT,
}

INGEST_PIPELINE: Tuple[str, ...] = (
    "RTAB-Map offline export subset",
    "rtab_map_offline_export_ingest_planning",
    SOURCE_INTERNAL_STANDARD,
    "generic_json_spatial_trace_parser_v1",
    OUTPUT_CANDIDATE_CONTRACT_REF,
    TARGET_ENTRYPOINT,
)


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(EXPORT_SUBSET_REFS) != 5:
        issues.append("export_subset_refs_count_not_5")
    if len(SUBSET_PLANNING_DIMENSIONS) < 11:
        issues.append("subset_planning_dimensions_incomplete")
    if set(P0_EXPORT_SUBSETS + P1_EXPORT_SUBSETS + P2_EXPORT_SUBSETS + OBSERVATION_EXPORT_SUBSETS) != set(
        EXPORT_SUBSET_REFS
    ):
        issues.append("priority_partition_incomplete")
    return len(issues) == 0, issues


def validate_subset_entry_shape(entry: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{field}" for field in SUBSET_PLANNING_FIELDS if field not in entry]
    subset_ref = entry.get("subset_ref")
    if subset_ref and not is_registered("export_subset_refs", str(subset_ref)):
        issues.append(f"subset_ref_not_registered:{subset_ref}")
    mapping = entry.get("luna_candidate_mapping") or {}
    if not mapping:
        issues.append("luna_candidate_mapping_required")
    trace_mapping = entry.get("generic_json_trace_mapping") or {}
    if not trace_mapping:
        issues.append("generic_json_trace_mapping_required")
    return len(issues) == 0, issues
