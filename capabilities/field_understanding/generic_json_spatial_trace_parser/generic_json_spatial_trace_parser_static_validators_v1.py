# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Parser — static validators + parse v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_types_v1 import (
    ADAPTER_PROFILE_REF,
    ALLOWED_CANDIDATE_TYPE_SLUGS,
    CANDIDATE_SLUG_TO_LUNA_TYPE,
    FIELD_SYNTHESIS_ENTRYPOINT,
    INPUT_FORMAT_REF,
    LUNA_CANDIDATE_BUNDLE_KEYS,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_ID,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    PARSER_REF,
    SOURCE_CHAIN,
    TRACE_ITEM_REQUIRED_FIELDS,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_trace_required_fields",
    "rule_02_time_ref_required",
    "rule_03_source_chain_required",
    "rule_04_candidate_type_allowed",
    "rule_05_field_synthesis_entrypoint_locked",
    "rule_06_confidence_range",
    "rule_07_candidate_only_default_true",
    "rule_08_unsupported_candidate_type_rejected",
    "rule_09_missing_source_chain_rejected",
    "rule_10_runtime_activation_forbidden",
    "rule_11_candidate_bundle_mapping",
    "rule_12_output_contract_spatial_evidence_bundle",
)


def _missing_fields(data: Dict[str, Any], fields: Tuple[str, ...]) -> List[str]:
    return [f"missing_{name}" for name in fields if name not in data]


def _has_time_ref(item: Dict[str, Any]) -> bool:
    if item.get("timestamp_ms") is not None:
        return True
    window = item.get("time_window_ms")
    return isinstance(window, (list, tuple)) and len(window) == 2


def validate_json_spatial_trace_item(item: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(item, TRACE_ITEM_REQUIRED_FIELDS)

    if not _has_time_ref(item):
        issues.append("timestamp_ms_or_time_window_ms_required")

    source_chain = item.get("source_chain")
    if not source_chain:
        issues.append("source_chain_required")

    candidate_type = item.get("candidate_type")
    if candidate_type not in ALLOWED_CANDIDATE_TYPE_SLUGS:
        issues.append(f"unsupported_candidate_type:{candidate_type!r}")

    if item.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("field_synthesis_entrypoint_bypass")

    confidence = item.get("confidence")
    if not isinstance(confidence, (int, float)) or not (0.0 <= float(confidence) <= 1.0):
        issues.append("confidence_out_of_range")

    if item.get("candidate_only", True) is not True:
        issues.append("candidate_only_required")

    return len(issues) == 0, issues


def _time_ref_from_item(item: Dict[str, Any]) -> Dict[str, Any]:
    if item.get("timestamp_ms") is not None:
        return {"kind": "timestamp_ms", "value": int(item["timestamp_ms"])}
    window = item.get("time_window_ms")
    return {"kind": "time_window_ms", "value": [int(window[0]), int(window[1])]}


def _companion_slugs(item: Dict[str, Any]) -> Tuple[str, ...]:
    payload = item.get("payload") or {}
    companions = payload.get("companion_candidate_types") or ()
    if isinstance(companions, list):
        companions = tuple(companions)
    return tuple(slug for slug in companions if slug in ALLOWED_CANDIDATE_TYPE_SLUGS)


def parse_json_spatial_trace_item(item: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[str]]:
    ok, issues = validate_json_spatial_trace_item(item)
    if not ok:
        return [], issues

    primary_slug = str(item["candidate_type"])
    slugs = (primary_slug,) + _companion_slugs(item)
    parsed_items: List[Dict[str, Any]] = []

    for slug in slugs:
        parsed_ref = f"parsed_{item['trace_id']}_{slug}"
        parsed_items.append(
            {
                "parsed_ref": parsed_ref,
                "trace_id": item["trace_id"],
                "source_chain": list(item["source_chain"]),
                "time_ref": _time_ref_from_item(item),
                "confidence": float(item["confidence"]),
                "candidate_type_slug": slug,
                "luna_candidate_type": CANDIDATE_SLUG_TO_LUNA_TYPE[slug],
                "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
                "normalized_payload": {
                    "input_format": INPUT_FORMAT_REF,
                    "parser_ref": PARSER_REF,
                    "primary_trace_id": item["trace_id"],
                    "payload": dict(item.get("payload") or {}),
                },
                "candidate_only": True,
            }
        )

    return parsed_items, []


def _bundle_key_for_luna_type(luna_type: str) -> str:
    mapping = {
        "PoseCandidate": "pose_candidates",
        "MotionCandidate": "motion_candidates",
        "SpatialAnchorCandidate": "spatial_anchor_candidates",
        "LocalMapCandidate": "local_map_candidates",
        "SLAMHealthCandidate": "slam_health_candidates",
        "MapDriftCandidate": "map_drift_candidates",
        "RelocalizationCandidate": "relocalization_candidates",
        "FieldGraphCandidate": "field_graph_candidates",
        "SemanticFieldObjectCandidate": "semantic_field_object_candidates",
    }
    return mapping[luna_type]


def _candidate_record(parsed: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "candidate_type": parsed["luna_candidate_type"],
        "candidate_ref": parsed["parsed_ref"],
        "trace_id": parsed["trace_id"],
        "source_chain": list(parsed["source_chain"]),
        "time_ref": parsed["time_ref"],
        "confidence": parsed["confidence"],
        "field_synthesis_entrypoint": parsed["field_synthesis_entrypoint"],
        "normalized_payload": parsed["normalized_payload"],
        "candidate_only": True,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
    }


def map_parsed_traces_to_candidate_bundle(
    parsed_items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    bundle: Dict[str, Any] = {
        "bundle_ref": "spatial_evidence_candidate_bundle_v1",
        "bundle_kind": OUTPUT_CANDIDATE_CONTRACT_REF,
        "model_id": MODEL_ID,
        "adapter_profile_ref": ADAPTER_PROFILE_REF,
        "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
        "input_format_ref": INPUT_FORMAT_REF,
        "parser_ref": PARSER_REF,
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "source_chain": [SOURCE_CHAIN, PARSER_REF, "parsed_bundle"],
        "output_candidate_types": [],
        "candidate_only": True,
        "runtime_activation_allowed": False,
        "commercial_runtime_approved": False,
    }
    for key in LUNA_CANDIDATE_BUNDLE_KEYS:
        bundle[key] = []

    output_types: List[str] = []
    for parsed in parsed_items:
        luna_type = parsed["luna_candidate_type"]
        key = _bundle_key_for_luna_type(luna_type)
        bundle[key].append(_candidate_record(parsed))
        if luna_type not in output_types:
            output_types.append(luna_type)

    bundle["output_candidate_types"] = output_types
    return bundle


def validate_candidate_bundle_mapping(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if bundle.get("bundle_kind") != OUTPUT_CANDIDATE_CONTRACT_REF:
        issues.append("bundle_kind_mismatch")
    if bundle.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("bundle_field_synthesis_entrypoint_bypass")
    if not bundle.get("source_chain"):
        issues.append("bundle_source_chain_required")
    if bundle.get("adapter_profile_ref") != ADAPTER_PROFILE_REF:
        issues.append("adapter_profile_ref_mismatch")
    if bundle.get("runtime_activation_allowed") is True:
        issues.append("runtime_activation_allowed_must_be_false")
    if bundle.get("commercial_runtime_approved") is True:
        issues.append("commercial_runtime_approved_must_be_false")

    total_candidates = sum(len(bundle.get(key) or []) for key in LUNA_CANDIDATE_BUNDLE_KEYS)
    if total_candidates == 0:
        issues.append("candidate_bundle_empty")

    for key in LUNA_CANDIDATE_BUNDLE_KEYS:
        for candidate in bundle.get(key) or ():
            if candidate.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
                issues.append(f"{key}.field_synthesis_entrypoint_bypass")
            if not candidate.get("source_chain"):
                issues.append(f"{key}.missing_source_chain")
            if candidate.get("direct_action_allowed") is True:
                issues.append(f"{key}.direct_action_forbidden")
            if candidate.get("direct_speech_allowed") is True:
                issues.append(f"{key}.direct_speech_forbidden")
            if candidate.get("direct_fact_write_allowed") is True:
                issues.append(f"{key}.direct_fact_write_forbidden")

    return len(issues) == 0, issues


def validate_negative_trace_item(item: Dict[str, Any], *, expect_issue: str) -> Tuple[bool, List[str]]:
    ok, issues = validate_json_spatial_trace_item(item)
    if expect_issue == "unsupported_candidate_type":
        return (not ok and any("unsupported_candidate_type" in issue for issue in issues)), issues
    if expect_issue == "missing_source_chain":
        return (not ok and any(issue == "source_chain_required" for issue in issues)), issues
    return False, issues
