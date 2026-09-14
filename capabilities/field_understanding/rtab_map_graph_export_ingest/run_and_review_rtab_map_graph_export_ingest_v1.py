# -*- coding: utf-8 -*-
"""RTAB-Map Graph Export Ingest — run + review (compressed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import write_json_file
from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_static_validators_v1 import (
    map_parsed_traces_to_candidate_bundle,
    parse_json_spatial_trace_item,
    validate_candidate_bundle_mapping,
)
from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT as JSON_PARSER_FIELD_SYNTHESIS_ENTRYPOINT,
    INPUT_FORMAT_REF as GENERIC_JSON_INPUT_FORMAT_REF,
    PARSER_REF as GENERIC_JSON_PARSER_REF,
)
from capabilities.field_understanding.rtab_map_graph_export_ingest.rtab_map_graph_export_ingest_fixture_v1 import (
    FIXTURE_REF,
    build_direct_bundle_bypass_fixture_v1,
    build_fixture_document_v1,
    build_negative_graph_fixtures_v1,
    build_valid_graph_edges_v1,
    build_valid_graph_nodes_v1,
)
from capabilities.field_understanding.rtab_map_graph_export_ingest.rtab_map_graph_export_ingest_static_validators_v1 import (
    convert_graph_export_to_json_spatial_trace_items,
    summarize_json_trace_items,
    validate_direct_candidate_bundle_bypass,
    validate_graph_edge_negative,
    validate_graph_node_negative,
    verify_gps_gnss_link_reserved,
    verify_runtime_trust_not_restored,
)
from capabilities.field_understanding.rtab_map_graph_export_ingest.rtab_map_graph_export_ingest_types_v1 import (
    ADAPTER_PROFILE_REF,
    DOMAIN_ID,
    EXPECTED_ANCHOR_ITEM_COUNT,
    EXPECTED_DRIFT_ITEM_COUNT,
    EXPECTED_GRAPH_EDGE_COUNT,
    EXPECTED_GRAPH_NODE_COUNT,
    EXPECTED_JSON_TRACE_ITEM_COUNT_MIN,
    EXPECTED_RELOCALIZATION_ITEM_COUNT,
    FINAL_DECISION_REVIEW_BLOCKED,
    FINAL_DECISION_REVIEW_GO,
    GENERIC_JSON_PARSER_MODULE_REF,
    INGEST_PRINCIPLE_ZH,
    INGEST_REF,
    INPUT_FORMAT_REF,
    INTERFACE_LAYER_PROTOCOL_REF,
    INTERNAL_STANDARD_FORMAT,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_FAMILY,
    MODEL_ID,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    NON_EXECUTION_FLAGS,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    PHASE_ID,
    SOURCE_INTERFACE_PROFILE,
    TARGET_ENTRYPOINT,
    TARGET_FORMAT_REF,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "rtab_map_graph_export_ingest_v1_smoke_v0"
)
OUTPUT_FILENAME = "rtab_map_graph_export_ingest_run_and_review_v1.json"


def run_and_review_rtab_map_graph_export_ingest_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    graph_nodes = list(build_valid_graph_nodes_v1())
    graph_edges = list(build_valid_graph_edges_v1())
    negative_fixtures = build_negative_graph_fixtures_v1()
    bypass_bundle = build_direct_bundle_bypass_fixture_v1()

    json_trace_items, convert_issues = convert_graph_export_to_json_spatial_trace_items(
        graph_nodes,
        graph_edges,
    )
    counts = summarize_json_trace_items(json_trace_items)

    parsed_items: List[Dict[str, Any]] = []
    json_parse_traces: List[Dict[str, Any]] = []
    json_parse_errors: List[str] = []

    for item in json_trace_items:
        parsed, errors = parse_json_spatial_trace_item(item)
        json_parse_traces.append(
            {
                "trace_id": item["trace_id"],
                "candidate_type": item["candidate_type"],
                "parsed_count": len(parsed),
                "errors": errors,
                "ok": len(errors) == 0 and len(parsed) > 0,
            }
        )
        if errors:
            json_parse_errors.extend([f"{item['trace_id']}:{err}" for err in errors])
        parsed_items.extend(parsed)

    candidate_bundle = map_parsed_traces_to_candidate_bundle(parsed_items)
    bundle_ok, bundle_issues = validate_candidate_bundle_mapping(candidate_bundle)

    missing_chain_ok, missing_chain_issues = validate_graph_node_negative(
        negative_fixtures["missing_source_chain"],
        expect_issue="missing_source_chain",
    )
    missing_node_ok, missing_node_issues = validate_graph_node_negative(
        negative_fixtures["missing_node_id"],
        expect_issue="missing_node_id",
    )
    loop_closure_trust_ok, loop_closure_trust_issues = validate_graph_edge_negative(
        negative_fixtures["loop_closure_runtime_trust_restore"],
        expect_issue="loop_closure_runtime_trust_restore",
    )
    bypass_rejected, bypass_issues = validate_direct_candidate_bundle_bypass(bypass_bundle)

    gps_link_ok, gps_link_issues = verify_gps_gnss_link_reserved(json_trace_items)
    runtime_trust_ok, runtime_trust_issues = verify_runtime_trust_not_restored(json_trace_items)

    model_binding = {
        "model_id": MODEL_ID,
        "model_family": MODEL_FAMILY,
        "domain_id": DOMAIN_ID,
        "model_management_protocol_ref": MODEL_MANAGEMENT_PROTOCOL_REF,
        "interface_layer_protocol_ref": INTERFACE_LAYER_PROTOCOL_REF,
        "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
        "source_interface_profile": SOURCE_INTERFACE_PROFILE,
        "internal_standard_format": INTERNAL_STANDARD_FORMAT,
        "adapter_profile_ref": ADAPTER_PROFILE_REF,
        "output_candidate_contract_ref": OUTPUT_CANDIDATE_CONTRACT_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
    }

    interface_layer_protocol_ref_ok = (
        model_binding["interface_layer_protocol_ref"] == INTERFACE_LAYER_PROTOCOL_REF
    )
    model_management_protocol_ref_ok = (
        model_binding["model_management_protocol_ref"] == MODEL_MANAGEMENT_PROTOCOL_REF
    )
    generic_json_spatial_trace_reused = TARGET_FORMAT_REF == INTERNAL_STANDARD_FORMAT
    generic_json_parser_reused = (
        GENERIC_JSON_PARSER_MODULE_REF.endswith("generic_json_spatial_trace_parser_static_validators_v1")
        and GENERIC_JSON_PARSER_REF == "generic_json_spatial_trace_parser_v1"
        and GENERIC_JSON_INPUT_FORMAT_REF == INTERNAL_STANDARD_FORMAT
        and len(parsed_items) > 0
        and not json_parse_errors
    )

    source_chain_required = all(bool(item.get("source_chain")) for item in json_trace_items) and all(
        bool(parsed.get("source_chain")) for parsed in parsed_items
    )
    field_synthesis_locked = (
        candidate_bundle.get("field_synthesis_entrypoint") == JSON_PARSER_FIELD_SYNTHESIS_ENTRYPOINT
        and all(
            item.get("field_synthesis_entrypoint") == JSON_PARSER_FIELD_SYNTHESIS_ENTRYPOINT
            for item in json_trace_items
        )
    )

    anchor_reloc_drift_bundle_ok = (
        len(candidate_bundle.get("spatial_anchor_candidates") or []) >= EXPECTED_ANCHOR_ITEM_COUNT
        and len(candidate_bundle.get("relocalization_candidates") or []) >= EXPECTED_RELOCALIZATION_ITEM_COUNT
        and len(candidate_bundle.get("map_drift_candidates") or []) >= EXPECTED_DRIFT_ITEM_COUNT
    )

    global_alignment_hint_candidate_only = gps_link_ok and all(
        (item.get("payload") or {}).get("metadata", {}).get("field_identity_mutation_allowed") is not True
        for item in json_trace_items
        if item.get("candidate_type") == "anchor"
    )

    runtime_activation_allowed = candidate_bundle.get("runtime_activation_allowed") is True
    commercial_runtime_approved = candidate_bundle.get("commercial_runtime_approved") is True

    failed_checks: List[str] = []
    if len(graph_nodes) != EXPECTED_GRAPH_NODE_COUNT:
        failed_checks.append(f"rtab_map_graph_node_count:{len(graph_nodes)}")
    if len(graph_edges) != EXPECTED_GRAPH_EDGE_COUNT:
        failed_checks.append(f"rtab_map_graph_edge_count:{len(graph_edges)}")
    if convert_issues:
        failed_checks.extend(convert_issues)
    if counts["json_trace_item_count"] < EXPECTED_JSON_TRACE_ITEM_COUNT_MIN:
        failed_checks.append(f"json_trace_item_count:{counts['json_trace_item_count']}")
    if counts["anchor_item_count"] < EXPECTED_ANCHOR_ITEM_COUNT:
        failed_checks.append(f"anchor_item_count:{counts['anchor_item_count']}")
    if counts["relocalization_item_count"] < EXPECTED_RELOCALIZATION_ITEM_COUNT:
        failed_checks.append(f"relocalization_item_count:{counts['relocalization_item_count']}")
    if counts["drift_item_count"] < EXPECTED_DRIFT_ITEM_COUNT:
        failed_checks.append(f"drift_item_count:{counts['drift_item_count']}")
    if json_parse_errors:
        failed_checks.extend(json_parse_errors)
    if not interface_layer_protocol_ref_ok:
        failed_checks.append("interface_layer_protocol_ref_ok=false")
    if not model_management_protocol_ref_ok:
        failed_checks.append("model_management_protocol_ref_ok=false")
    if not generic_json_spatial_trace_reused:
        failed_checks.append("generic_json_spatial_trace_reused=false")
    if not generic_json_parser_reused:
        failed_checks.append("generic_json_parser_reused=false")
    if not bundle_ok:
        failed_checks.extend(bundle_issues)
    if not anchor_reloc_drift_bundle_ok:
        failed_checks.append("anchor_reloc_drift_bundle_ok=false")
    if not source_chain_required:
        failed_checks.append("source_chain_required=false")
    if not field_synthesis_locked:
        failed_checks.append("field_synthesis_entrypoint_locked=false")
    if not gps_link_ok:
        failed_checks.extend(gps_link_issues)
    if not global_alignment_hint_candidate_only:
        failed_checks.append("global_alignment_hint_candidate_only=false")
    if not runtime_trust_ok:
        failed_checks.extend(runtime_trust_issues)
    if not missing_chain_ok:
        failed_checks.append("invalid_missing_source_chain_rejected=false")
    if not missing_node_ok:
        failed_checks.append("invalid_missing_node_id_rejected=false")
    if not loop_closure_trust_ok:
        failed_checks.append("invalid_loop_closure_runtime_trust_restore_rejected=false")
    if not bypass_rejected:
        failed_checks.append("invalid_direct_candidate_bundle_bypass_rejected=false")
    if runtime_activation_allowed:
        failed_checks.append("runtime_activation_allowed=true")
    if commercial_runtime_approved:
        failed_checks.append("commercial_runtime_approved=true")

    review_ok = len(failed_checks) == 0

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RTAB-Map Graph Export Ingest Run + Review",
        "lifecycle_variant": "compressed_interface_layer_graph_fixture_ingest_review",
        "ingest_principle_zh": INGEST_PRINCIPLE_ZH,
        "model_binding": model_binding,
        "pipeline": [
            "RTAB-Map graph export fixture",
            INGEST_REF,
            INTERNAL_STANDARD_FORMAT,
            GENERIC_JSON_PARSER_REF,
            "Anchor / Relocalization / Drift candidate bundle",
            JSON_PARSER_FIELD_SYNTHESIS_ENTRYPOINT,
        ],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "input_format_ref": INPUT_FORMAT_REF,
        "target_format_ref": TARGET_FORMAT_REF,
        "generic_json_parser_module_ref": GENERIC_JSON_PARSER_MODULE_REF,
        "generic_json_parser_ref": GENERIC_JSON_PARSER_REF,
        "fixture_ref": FIXTURE_REF,
        "rtab_map_graph_node_count": len(graph_nodes),
        "rtab_map_graph_edge_count": len(graph_edges),
        "graph_nodes": graph_nodes,
        "graph_edges": graph_edges,
        "json_trace_items": json_trace_items,
        "json_trace_item_count": counts["json_trace_item_count"],
        "anchor_item_count": counts["anchor_item_count"],
        "relocalization_item_count": counts["relocalization_item_count"],
        "drift_item_count": counts["drift_item_count"],
        "json_parser_parse_traces": json_parse_traces,
        "parsed_items": parsed_items,
        "spatial_evidence_candidate_bundle": candidate_bundle,
        "negative_validation": {
            "invalid_missing_source_chain_rejected": missing_chain_ok,
            "missing_source_chain_issues": missing_chain_issues,
            "invalid_missing_node_id_rejected": missing_node_ok,
            "missing_node_id_issues": missing_node_issues,
            "invalid_loop_closure_runtime_trust_restore_rejected": loop_closure_trust_ok,
            "loop_closure_runtime_trust_restore_issues": loop_closure_trust_issues,
            "invalid_direct_candidate_bundle_bypass_rejected": bypass_rejected,
            "direct_bundle_bypass_issues": bypass_issues,
        },
        "review_checkpoints": {
            "rtab_map_graph_node_count": len(graph_nodes),
            "rtab_map_graph_edge_count": len(graph_edges),
            "json_trace_item_count": counts["json_trace_item_count"],
            "anchor_item_count": counts["anchor_item_count"],
            "relocalization_item_count": counts["relocalization_item_count"],
            "drift_item_count": counts["drift_item_count"],
            "interface_layer_protocol_ref_ok": interface_layer_protocol_ref_ok,
            "model_management_protocol_ref_ok": model_management_protocol_ref_ok,
            "generic_json_spatial_trace_reused": generic_json_spatial_trace_reused,
            "generic_json_parser_reused": generic_json_parser_reused,
            "candidate_bundle_mapping_ok": bundle_ok,
            "anchor_reloc_drift_bundle_ok": anchor_reloc_drift_bundle_ok,
            "source_chain_required": source_chain_required,
            "field_synthesis_entrypoint_locked": JSON_PARSER_FIELD_SYNTHESIS_ENTRYPOINT
            if field_synthesis_locked
            else None,
            "gps_gnss_link_reserved": gps_link_ok,
            "global_alignment_hint_candidate_only": global_alignment_hint_candidate_only,
            "runtime_trust_not_restored_by_loop_closure": runtime_trust_ok,
            "invalid_missing_source_chain_rejected": missing_chain_ok,
            "invalid_missing_node_id_rejected": missing_node_ok,
            "invalid_loop_closure_runtime_trust_restore_rejected": loop_closure_trust_ok,
            "invalid_direct_candidate_bundle_bypass_rejected": bypass_rejected,
            "runtime_activation_allowed": runtime_activation_allowed,
            "commercial_runtime_approved": commercial_runtime_approved,
        },
        "fixture_document": build_fixture_document_v1(),
        "output_root": str(out_root),
        "output_file": str(out_path),
        "blocker_count": len(failed_checks),
        "failed_checks": failed_checks,
        "final_decision": (
            FINAL_DECISION_REVIEW_GO if review_ok else FINAL_DECISION_REVIEW_BLOCKED
        ),
    }

    if write_file:
        write_json_file(out_path, result)

    return result


def main() -> int:
    result = run_and_review_rtab_map_graph_export_ingest_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "rtab_map_graph_node_count": checkpoints["rtab_map_graph_node_count"],
                "rtab_map_graph_edge_count": checkpoints["rtab_map_graph_edge_count"],
                "json_trace_item_count": checkpoints["json_trace_item_count"],
                "anchor_item_count": checkpoints["anchor_item_count"],
                "relocalization_item_count": checkpoints["relocalization_item_count"],
                "drift_item_count": checkpoints["drift_item_count"],
                "anchor_reloc_drift_bundle_ok": checkpoints["anchor_reloc_drift_bundle_ok"],
                "generic_json_parser_reused": checkpoints["generic_json_parser_reused"],
                "gps_gnss_link_reserved": checkpoints["gps_gnss_link_reserved"],
                "runtime_trust_not_restored_by_loop_closure": checkpoints[
                    "runtime_trust_not_restored_by_loop_closure"
                ],
                "candidate_bundle_mapping_ok": checkpoints["candidate_bundle_mapping_ok"],
                "field_synthesis_entrypoint_locked": checkpoints["field_synthesis_entrypoint_locked"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_REVIEW_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
