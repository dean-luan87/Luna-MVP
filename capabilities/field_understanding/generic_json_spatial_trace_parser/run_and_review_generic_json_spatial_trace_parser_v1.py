# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Parser — run + review (compressed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import write_json_file
from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_fixture_v1 import (
    FIXTURE_REF,
    build_fixture_document_v1,
    build_fixture_trace_items_v1,
    build_negative_fixture_items_v1,
)
from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_static_validators_v1 import (
    map_parsed_traces_to_candidate_bundle,
    parse_json_spatial_trace_item,
    validate_candidate_bundle_mapping,
    validate_negative_trace_item,
)
from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_types_v1 import (
    ADAPTER_PROFILE_REF,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_REVIEW_BLOCKED,
    FINAL_DECISION_REVIEW_GO,
    INPUT_FORMAT_REF,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_ID,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    NON_EXECUTION_FLAGS,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    PARSER_PRINCIPLE_ZH,
    PARSER_REF,
    PHASE_ID,
    REQUIRED_CANDIDATE_TYPE_SLUGS,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "generic_json_spatial_trace_parser_v1_smoke_v0"
)
OUTPUT_FILENAME = "generic_json_spatial_trace_parser_run_and_review_v1.json"

MIN_FIXTURE_COUNT = 5


def run_and_review_generic_json_spatial_trace_parser_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    fixture_items = list(build_fixture_trace_items_v1())
    negative_items = build_negative_fixture_items_v1()

    parsed_items: List[Dict[str, Any]] = []
    parse_traces: List[Dict[str, Any]] = []
    parse_errors: List[str] = []

    for item in fixture_items:
        parsed, errors = parse_json_spatial_trace_item(item)
        parse_traces.append(
            {
                "trace_id": item["trace_id"],
                "candidate_type": item["candidate_type"],
                "parsed_count": len(parsed),
                "errors": errors,
                "ok": len(errors) == 0 and len(parsed) > 0,
            }
        )
        if errors:
            parse_errors.extend([f"{item['trace_id']}:{err}" for err in errors])
        parsed_items.extend(parsed)

    candidate_bundle = map_parsed_traces_to_candidate_bundle(parsed_items)
    bundle_ok, bundle_issues = validate_candidate_bundle_mapping(candidate_bundle)

    unsupported_ok, unsupported_issues = validate_negative_trace_item(
        negative_items["unsupported_candidate_type"],
        expect_issue="unsupported_candidate_type",
    )
    missing_chain_ok, missing_chain_issues = validate_negative_trace_item(
        negative_items["missing_source_chain"],
        expect_issue="missing_source_chain",
    )

    source_chain_required = all(
        bool(item.get("source_chain")) for item in fixture_items
    ) and all(bool(parsed.get("source_chain")) for parsed in parsed_items)

    field_synthesis_locked = (
        candidate_bundle.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
        and all(
            parsed.get("field_synthesis_entrypoint") == FIELD_SYNTHESIS_ENTRYPOINT
            for parsed in parsed_items
        )
    )

    runtime_activation_allowed = candidate_bundle.get("runtime_activation_allowed") is True

    failed_checks: List[str] = []
    if len(fixture_items) < MIN_FIXTURE_COUNT:
        failed_checks.append(f"fixture_count:{len(fixture_items)}")
    if len(parsed_items) < MIN_FIXTURE_COUNT:
        failed_checks.append(f"parsed_item_count:{len(parsed_items)}")
    if parse_errors:
        failed_checks.extend(parse_errors)
    if not bundle_ok:
        failed_checks.extend(bundle_issues)
    if not source_chain_required:
        failed_checks.append("source_chain_required=false")
    if not field_synthesis_locked:
        failed_checks.append("field_synthesis_entrypoint_locked=false")
    if not unsupported_ok:
        failed_checks.append("unsupported_candidate_type_rejected=false")
    if not missing_chain_ok:
        failed_checks.append("missing_source_chain_rejected=false")
    if runtime_activation_allowed:
        failed_checks.append("runtime_activation_allowed=true")

    review_ok = (
        len(fixture_items) >= MIN_FIXTURE_COUNT
        and len(parsed_items) >= MIN_FIXTURE_COUNT
        and not parse_errors
        and bundle_ok
        and source_chain_required
        and field_synthesis_locked
        and unsupported_ok
        and missing_chain_ok
        and not runtime_activation_allowed
        and len(failed_checks) == 0
    )

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Generic JSON Spatial Trace Parser Run + Review",
        "lifecycle_variant": "compressed_parser_fixture_review",
        "parser_principle_zh": PARSER_PRINCIPLE_ZH,
        "model_binding": {
            "model_id": MODEL_ID,
            "model_family": "slam",
            "domain_id": "spatial_evidence",
            "model_management_protocol_ref": MODEL_MANAGEMENT_PROTOCOL_REF,
            "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
            "adapter_profile_ref": ADAPTER_PROFILE_REF,
            "output_candidate_contract_ref": OUTPUT_CANDIDATE_CONTRACT_REF,
            "input_format_ref": INPUT_FORMAT_REF,
            "parser_ref": PARSER_REF,
        },
        "pipeline": [
            "Generic JSON Spatial Trace",
            PARSER_REF,
            "normalized_parsed_trace",
            OUTPUT_CANDIDATE_CONTRACT_REF,
            FIELD_SYNTHESIS_ENTRYPOINT,
        ],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "fixture_ref": FIXTURE_REF,
        "fixture_count": len(fixture_items),
        "parsed_item_count": len(parsed_items),
        "required_candidate_type_slugs": list(REQUIRED_CANDIDATE_TYPE_SLUGS),
        "fixture_document": build_fixture_document_v1(),
        "parse_traces": parse_traces,
        "parsed_items": parsed_items,
        "spatial_evidence_candidate_bundle": candidate_bundle,
        "negative_validation": {
            "unsupported_candidate_type_rejected": unsupported_ok,
            "unsupported_issues": unsupported_issues,
            "missing_source_chain_rejected": missing_chain_ok,
            "missing_source_chain_issues": missing_chain_issues,
        },
        "review_checkpoints": {
            "fixture_count_ok": len(fixture_items) >= MIN_FIXTURE_COUNT,
            "parsed_item_count_ok": len(parsed_items) >= MIN_FIXTURE_COUNT,
            "candidate_bundle_mapping_ok": bundle_ok,
            "source_chain_required": source_chain_required,
            "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT
            if field_synthesis_locked
            else None,
            "unsupported_candidate_type_rejected": unsupported_ok,
            "missing_source_chain_rejected": missing_chain_ok,
            "runtime_activation_allowed": runtime_activation_allowed,
        },
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
    result = run_and_review_generic_json_spatial_trace_parser_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "fixture_count": result["fixture_count"],
                "parsed_item_count": result["parsed_item_count"],
                "candidate_bundle_mapping_ok": checkpoints["candidate_bundle_mapping_ok"],
                "source_chain_required": checkpoints["source_chain_required"],
                "field_synthesis_entrypoint_locked": checkpoints["field_synthesis_entrypoint_locked"],
                "unsupported_candidate_type_rejected": checkpoints["unsupported_candidate_type_rejected"],
                "missing_source_chain_rejected": checkpoints["missing_source_chain_rejected"],
                "runtime_activation_allowed": checkpoints["runtime_activation_allowed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_REVIEW_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
