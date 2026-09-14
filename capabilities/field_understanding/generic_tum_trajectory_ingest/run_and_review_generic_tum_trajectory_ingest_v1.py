# -*- coding: utf-8 -*-
"""Generic TUM Trajectory Ingest — run + review (compressed)."""

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
    PARSER_REF as GENERIC_JSON_PARSER_REF,
)
from capabilities.field_understanding.generic_tum_trajectory_ingest.generic_tum_trajectory_ingest_fixture_v1 import (
    FIXTURE_REF,
    build_fixture_document_v1,
    build_negative_tum_fixture_lines_v1,
    build_valid_tum_fixture_lines_v1,
)
from capabilities.field_understanding.generic_tum_trajectory_ingest.generic_tum_trajectory_ingest_static_validators_v1 import (
    convert_tum_lines_to_json_spatial_trace_items,
    summarize_json_trace_items,
    validate_tum_line_negative,
)
from capabilities.field_understanding.generic_tum_trajectory_ingest.generic_tum_trajectory_ingest_types_v1 import (
    EXPECTED_JSON_TRACE_ITEM_COUNT,
    EXPECTED_MOTION_ITEM_COUNT,
    EXPECTED_POSE_ITEM_COUNT,
    EXPECTED_TUM_FIXTURE_LINE_COUNT,
    FINAL_DECISION_REVIEW_BLOCKED,
    FINAL_DECISION_REVIEW_GO,
    GENERIC_JSON_PARSER_MODULE_REF,
    INGEST_PRINCIPLE_ZH,
    INGEST_REF,
    INPUT_FORMAT_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SOURCE_CHAIN,
    TARGET_FORMAT_REF,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "generic_tum_trajectory_ingest_v1_smoke_v0"
)
OUTPUT_FILENAME = "generic_tum_trajectory_ingest_run_and_review_v1.json"


def run_and_review_generic_tum_trajectory_ingest_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    tum_lines = list(build_valid_tum_fixture_lines_v1())
    negative_tum = build_negative_tum_fixture_lines_v1()
    source_chain_prefix = [SOURCE_CHAIN, FIXTURE_REF]

    json_trace_items, convert_issues = convert_tum_lines_to_json_spatial_trace_items(
        tum_lines,
        source_chain_prefix=source_chain_prefix,
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

    bad_column_ok, bad_column_issues = validate_tum_line_negative(
        negative_tum["bad_column_count"],
        expect_issue="bad_column_count",
    )
    bad_quat_ok, bad_quat_issues = validate_tum_line_negative(
        negative_tum["bad_quaternion_all_zero"],
        expect_issue="bad_quaternion",
    )
    _, missing_chain_issues = convert_tum_lines_to_json_spatial_trace_items(
        tum_lines,
        source_chain_prefix=[],
    )
    missing_chain_ok = any(issue == "source_chain_required" for issue in missing_chain_issues)

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
    runtime_activation_allowed = candidate_bundle.get("runtime_activation_allowed") is True

    generic_json_parser_reused = (
        GENERIC_JSON_PARSER_MODULE_REF.endswith("generic_json_spatial_trace_parser_static_validators_v1")
        and GENERIC_JSON_PARSER_REF == "generic_json_spatial_trace_parser_v1"
        and len(parsed_items) > 0
        and not json_parse_errors
    )

    failed_checks: List[str] = []
    if len(tum_lines) != EXPECTED_TUM_FIXTURE_LINE_COUNT:
        failed_checks.append(f"tum_fixture_line_count:{len(tum_lines)}")
    if convert_issues:
        failed_checks.extend(convert_issues)
    if counts["json_trace_item_count"] != EXPECTED_JSON_TRACE_ITEM_COUNT:
        failed_checks.append(f"json_trace_item_count:{counts['json_trace_item_count']}")
    if counts["pose_item_count"] != EXPECTED_POSE_ITEM_COUNT:
        failed_checks.append(f"pose_item_count:{counts['pose_item_count']}")
    if counts["motion_item_count"] != EXPECTED_MOTION_ITEM_COUNT:
        failed_checks.append(f"motion_item_count:{counts['motion_item_count']}")
    if json_parse_errors:
        failed_checks.extend(json_parse_errors)
    if not generic_json_parser_reused:
        failed_checks.append("generic_json_parser_reused=false")
    if not bundle_ok:
        failed_checks.extend(bundle_issues)
    if not source_chain_required:
        failed_checks.append("source_chain_required=false")
    if not field_synthesis_locked:
        failed_checks.append("field_synthesis_entrypoint_locked=false")
    if not bad_column_ok:
        failed_checks.append("invalid_bad_column_count_rejected=false")
    if not bad_quat_ok:
        failed_checks.append("invalid_bad_quaternion_rejected=false")
    if not missing_chain_ok:
        failed_checks.append("invalid_missing_source_chain_rejected=false")
    if runtime_activation_allowed:
        failed_checks.append("runtime_activation_allowed=true")

    review_ok = len(failed_checks) == 0

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Generic TUM Trajectory Ingest Run + Review",
        "lifecycle_variant": "compressed_tum_to_json_ingest_review",
        "ingest_principle_zh": INGEST_PRINCIPLE_ZH,
        "pipeline": [
            "TUM trajectory fixture",
            INGEST_REF,
            TARGET_FORMAT_REF,
            GENERIC_JSON_PARSER_REF,
            "spatial_evidence_candidate_bundle",
            JSON_PARSER_FIELD_SYNTHESIS_ENTRYPOINT,
        ],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "input_format_ref": INPUT_FORMAT_REF,
        "target_format_ref": TARGET_FORMAT_REF,
        "generic_json_parser_module_ref": GENERIC_JSON_PARSER_MODULE_REF,
        "generic_json_parser_ref": GENERIC_JSON_PARSER_REF,
        "fixture_ref": FIXTURE_REF,
        "tum_fixture_line_count": len(tum_lines),
        "tum_lines": tum_lines,
        "json_trace_items": json_trace_items,
        "json_trace_item_count": counts["json_trace_item_count"],
        "pose_item_count": counts["pose_item_count"],
        "motion_item_count": counts["motion_item_count"],
        "json_parser_parse_traces": json_parse_traces,
        "parsed_items": parsed_items,
        "spatial_evidence_candidate_bundle": candidate_bundle,
        "negative_validation": {
            "invalid_bad_column_count_rejected": bad_column_ok,
            "bad_column_issues": bad_column_issues,
            "invalid_bad_quaternion_rejected": bad_quat_ok,
            "bad_quaternion_issues": bad_quat_issues,
            "invalid_missing_source_chain_rejected": missing_chain_ok,
            "missing_source_chain_issues": missing_chain_issues,
        },
        "review_checkpoints": {
            "tum_fixture_line_count": len(tum_lines),
            "json_trace_item_count": counts["json_trace_item_count"],
            "pose_item_count": counts["pose_item_count"],
            "motion_item_count": counts["motion_item_count"],
            "generic_json_parser_reused": generic_json_parser_reused,
            "candidate_bundle_mapping_ok": bundle_ok,
            "source_chain_required": source_chain_required,
            "field_synthesis_entrypoint_locked": JSON_PARSER_FIELD_SYNTHESIS_ENTRYPOINT
            if field_synthesis_locked
            else None,
            "invalid_bad_column_count_rejected": bad_column_ok,
            "invalid_bad_quaternion_rejected": bad_quat_ok,
            "invalid_missing_source_chain_rejected": missing_chain_ok,
            "runtime_activation_allowed": runtime_activation_allowed,
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
    result = run_and_review_generic_tum_trajectory_ingest_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "tum_fixture_line_count": checkpoints["tum_fixture_line_count"],
                "json_trace_item_count": checkpoints["json_trace_item_count"],
                "pose_item_count": checkpoints["pose_item_count"],
                "motion_item_count": checkpoints["motion_item_count"],
                "generic_json_parser_reused": checkpoints["generic_json_parser_reused"],
                "candidate_bundle_mapping_ok": checkpoints["candidate_bundle_mapping_ok"],
                "source_chain_required": checkpoints["source_chain_required"],
                "field_synthesis_entrypoint_locked": checkpoints["field_synthesis_entrypoint_locked"],
                "invalid_bad_column_count_rejected": checkpoints["invalid_bad_column_count_rejected"],
                "invalid_bad_quaternion_rejected": checkpoints["invalid_bad_quaternion_rejected"],
                "invalid_missing_source_chain_rejected": checkpoints["invalid_missing_source_chain_rejected"],
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
