# -*- coding: utf-8 -*-
"""Generic TUM Real File Loader DryRun — cases v1.

Reuses:
- generic_tum_trajectory_ingest.parse_tum_trajectory_line (TUM row parsing / quaternion validation)
- generic_json_spatial_trace_parser.parse_json_spatial_trace_item
- generic_json_spatial_trace_parser.map_parsed_traces_to_candidate_bundle
- generic_json_spatial_trace_parser.validate_candidate_bundle_mapping

It does NOT reimplement the Generic JSON parser.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_static_validators_v1 import (
    map_parsed_traces_to_candidate_bundle,
    parse_json_spatial_trace_item,
    validate_candidate_bundle_mapping,
)
from capabilities.field_understanding.generic_tum_trajectory_ingest.generic_tum_trajectory_ingest_static_validators_v1 import (
    parse_tum_trajectory_line,
)
from capabilities.field_understanding.generic_tum_real_file_loader_dryrun.generic_tum_real_file_loader_dryrun_types_v1 import (
    GenericTUMRealFileLoaderDryRunCase,
    NEGATIVE_CASE_REFS,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    POSE_CONFIDENCE,
    POSITIVE_CASE_REFS,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    SOURCE_FORMAT,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
)

_MODULE_DIR = Path(__file__).resolve().parent
_SAMPLES_DIR = _MODULE_DIR / "samples"


def samples_dir() -> Path:
    return _SAMPLES_DIR


def is_controlled_sample_path(path: Path) -> bool:
    try:
        resolved = path.resolve()
        samples_resolved = _SAMPLES_DIR.resolve()
        return samples_resolved in resolved.parents or resolved == samples_resolved
    except OSError:
        return False


def _build_loader_policy(sample_file: str) -> Dict[str, Any]:
    return {
        "policy_ref": f"tum_loader_policy_{sample_file}",
        "sample_file": sample_file,
        "source_format": SOURCE_FORMAT,
        "file_origin": {
            "sample_file": sample_file,
            "samples_rel_dir": SAMPLES_REL_DIR,
            "loader": "generic_tum_real_file_loader_dryrun_v1",
        },
        "source_chain_prefix": [SOURCE_CHAIN, f"tum_real_file:{sample_file}"],
    }


def read_local_tum_file(sample_file: str) -> Tuple[Optional[List[str]], bool, List[str]]:
    path = _SAMPLES_DIR / sample_file
    if not is_controlled_sample_path(path):
        return None, False, [f"sample_path_not_controlled:{sample_file}"]
    if not path.is_file():
        return None, False, [f"sample_file_missing:{sample_file}"]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, True, [f"sample_read_failed:{sample_file}:{exc}"]
    return text.splitlines(), True, []


def admit_tum_file_source(*, sample_file: str, policy: Dict[str, Any]) -> Dict[str, Any]:
    path = _SAMPLES_DIR / sample_file
    rejection_reasons: List[str] = []

    controlled_ok = is_controlled_sample_path(path)
    if not controlled_ok:
        rejection_reasons.append("controlled_samples_path_violation")

    file_origin = policy.get("file_origin") or {}
    file_origin_present = bool(file_origin)
    if not file_origin_present:
        rejection_reasons.append("file_origin_metadata_missing")

    source_chain_prefix = policy.get("source_chain_prefix") or []
    source_chain_present = bool(source_chain_prefix)
    if not source_chain_present:
        rejection_reasons.append("source_chain_missing")

    source_format_ok = policy.get("source_format") == SOURCE_FORMAT
    if not source_format_ok:
        rejection_reasons.append("source_format_not_tum_trajectory_file")

    admitted = len(rejection_reasons) == 0
    return {
        "result_ref": f"tum_admission_{sample_file}",
        "file_source_admitted": admitted,
        "controlled_samples_path_ok": controlled_ok,
        "file_origin_metadata_present": file_origin_present,
        "source_chain_present": source_chain_present,
        "source_format_ok": source_format_ok,
        "rejection_reasons": rejection_reasons,
        "source_chain": SOURCE_CHAIN,
    }


def parse_tum_rows(lines: List[str]) -> Dict[str, Any]:
    valid_rows: List[Dict[str, Any]] = []
    parse_errors: List[str] = []
    skipped = 0
    hard_errors = 0

    for index, line in enumerate(lines):
        parsed, issues = parse_tum_trajectory_line(line, line_index=index)
        if parsed is not None:
            valid_rows.append(parsed)
            continue
        if any("empty_or_comment" in issue for issue in issues):
            skipped += 1
            continue
        hard_errors += 1
        parse_errors.extend(issues)

    return {
        "result_ref": "tum_row_parse_result",
        "valid_rows": valid_rows,
        "valid_row_count": len(valid_rows),
        "skipped_line_count": skipped,
        "hard_error_count": hard_errors,
        "parse_errors": parse_errors,
        "source_chain": SOURCE_CHAIN,
    }


def _pose_trace_item(
    row: Dict[str, Any],
    *,
    row_index: int,
    policy: Dict[str, Any],
) -> Dict[str, Any]:
    trace_id = f"tum_pose_{row_index}"
    metadata = {
        "file_origin": dict(policy.get("file_origin") or {}),
        "source_format": SOURCE_FORMAT,
        "row_index": row_index,
    }
    return {
        "trace_id": trace_id,
        "source_chain": list(policy.get("source_chain_prefix") or []) + [trace_id],
        "timestamp_ms": row["timestamp_ms"],
        "confidence": POSE_CONFIDENCE,
        "candidate_type": "pose",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "metadata": metadata,
        "payload": {
            "source_format": SOURCE_FORMAT,
            "pose": dict(row["pose"]),
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def _motion_trace_item(
    prev_row: Dict[str, Any],
    curr_row: Dict[str, Any],
    *,
    from_index: int,
    to_index: int,
    prev_conf: float,
    next_conf: float,
    policy: Dict[str, Any],
) -> Dict[str, Any]:
    trace_id = f"tum_motion_{from_index}_{to_index}"
    p0 = prev_row["pose"]
    p1 = curr_row["pose"]
    delta_translation = [p1["tx"] - p0["tx"], p1["ty"] - p0["ty"], p1["tz"] - p0["tz"]]
    dot = (
        p0["qx"] * p1["qx"]
        + p0["qy"] * p1["qy"]
        + p0["qz"] * p1["qz"]
        + p0["qw"] * p1["qw"]
    )
    dot = max(-1.0, min(1.0, abs(dot)))
    delta_rotation_hint = round(1.0 - dot, 6)
    metadata = {
        "file_origin": dict(policy.get("file_origin") or {}),
        "source_format": SOURCE_FORMAT,
        "from_row_index": from_index,
        "to_row_index": to_index,
    }
    return {
        "trace_id": trace_id,
        "source_chain": list(policy.get("source_chain_prefix") or []) + [trace_id],
        "time_window_ms": [prev_row["timestamp_ms"], curr_row["timestamp_ms"]],
        "confidence": min(prev_conf, next_conf),
        "candidate_type": "motion",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "metadata": metadata,
        "payload": {
            "source_format": SOURCE_FORMAT,
            "delta_translation": delta_translation,
            "delta_rotation_hint": delta_rotation_hint,
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def convert_tum_rows_to_json_spatial_trace(
    valid_rows: List[Dict[str, Any]],
    *,
    policy: Dict[str, Any],
) -> Dict[str, Any]:
    conversion_issues: List[str] = []
    if not policy.get("source_chain_prefix"):
        conversion_issues.append("source_chain_required")
    if not policy.get("file_origin"):
        conversion_issues.append("file_origin_required")
    if conversion_issues:
        return {
            "result_ref": "tum_to_json_conversion_result",
            "conversion_ok": False,
            "json_trace_items": [],
            "json_trace_item_count": 0,
            "pose_item_count": 0,
            "motion_item_count": 0,
            "target_internal_format": TARGET_INTERNAL_FORMAT,
            "file_origin_preserved": False,
            "source_chain_preserved": False,
            "conversion_issues": conversion_issues,
            "source_chain": SOURCE_CHAIN,
        }

    json_items: List[Dict[str, Any]] = []
    for row_index, row in enumerate(valid_rows):
        json_items.append(_pose_trace_item(row, row_index=row_index, policy=policy))

    for from_index in range(len(valid_rows) - 1):
        to_index = from_index + 1
        json_items.append(
            _motion_trace_item(
                valid_rows[from_index],
                valid_rows[to_index],
                from_index=from_index,
                to_index=to_index,
                prev_conf=POSE_CONFIDENCE,
                next_conf=POSE_CONFIDENCE,
                policy=policy,
            )
        )

    pose_count = sum(1 for item in json_items if item.get("candidate_type") == "pose")
    motion_count = sum(1 for item in json_items if item.get("candidate_type") == "motion")
    file_origin_preserved = all(
        bool((item.get("metadata") or {}).get("file_origin")) for item in json_items
    )
    source_chain_preserved = all(bool(item.get("source_chain")) for item in json_items)

    return {
        "result_ref": "tum_to_json_conversion_result",
        "conversion_ok": bool(json_items),
        "json_trace_items": json_items,
        "json_trace_item_count": len(json_items),
        "pose_item_count": pose_count,
        "motion_item_count": motion_count,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "file_origin_preserved": file_origin_preserved,
        "source_chain_preserved": source_chain_preserved,
        "conversion_issues": [],
        "source_chain": SOURCE_CHAIN,
    }


def replay_via_generic_json_parser(json_trace_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    parsed_items: List[Dict[str, Any]] = []
    parse_errors: List[str] = []
    for item in json_trace_items:
        parsed, errors = parse_json_spatial_trace_item(item)
        if errors:
            parse_errors.extend([f"{item.get('trace_id')}:{err}" for err in errors])
        parsed_items.extend(parsed)

    bundle = map_parsed_traces_to_candidate_bundle(parsed_items)
    bundle_ok, bundle_issues = validate_candidate_bundle_mapping(bundle)
    return {
        "result_ref": "tum_real_file_replay_result",
        "generic_json_parser_reused": True,
        "parsed_count": len(parsed_items),
        "parse_errors": parse_errors,
        "candidate_bundle_mapping_ok": bundle_ok and not parse_errors,
        "output_candidate_types": list(bundle.get("output_candidate_types") or ()),
        "bundle_issues": bundle_issues,
        "spatial_evidence_candidate_bundle": bundle,
        "source_chain": SOURCE_CHAIN,
    }


def _load_tum_pipeline(sample_file: str) -> Dict[str, Any]:
    policy = _build_loader_policy(sample_file)
    lines, read_ok, read_issues = read_local_tum_file(sample_file)
    admission = admit_tum_file_source(sample_file=sample_file, policy=policy)

    row_result: Dict[str, Any] = {
        "valid_rows": [],
        "valid_row_count": 0,
        "skipped_line_count": 0,
        "hard_error_count": 0,
        "parse_errors": read_issues,
    }
    conversion: Dict[str, Any] = {
        "conversion_ok": False,
        "json_trace_items": [],
        "json_trace_item_count": 0,
        "pose_item_count": 0,
        "motion_item_count": 0,
        "file_origin_preserved": False,
        "source_chain_preserved": False,
        "conversion_issues": ["pipeline_not_admitted"],
    }
    replay: Dict[str, Any] = {
        "candidate_bundle_mapping_ok": False,
        "generic_json_parser_reused": True,
        "output_candidate_types": [],
        "bundle_issues": ["pipeline_not_admitted"],
        "spatial_evidence_candidate_bundle": {},
        "parsed_count": 0,
    }

    admitted = admission["file_source_admitted"] and read_ok and lines is not None
    if admitted:
        row_result = parse_tum_rows(lines or [])
        if row_result["hard_error_count"] == 0 and row_result["valid_row_count"] > 0:
            conversion = convert_tum_rows_to_json_spatial_trace(
                row_result["valid_rows"], policy=policy
            )
            if conversion["conversion_ok"]:
                replay = replay_via_generic_json_parser(conversion["json_trace_items"])

    return {
        "policy": policy,
        "read_ok": read_ok,
        "admission": admission,
        "row_result": row_result,
        "conversion": conversion,
        "replay": replay,
        "admitted": admitted,
    }


def run_positive_valid_file_case() -> Dict[str, Any]:
    sample_file = "sample_tum_valid_trajectory.txt"
    pipe = _load_tum_pipeline(sample_file)
    conv = pipe["conversion"]
    replay = pipe["replay"]
    row = pipe["row_result"]
    checks = {
        "local_file_read_used": pipe["read_ok"] is True,
        "file_source_admitted": pipe["admission"]["file_source_admitted"] is True,
        "tum_row_count": row["valid_row_count"],
        "json_trace_item_count": conv["json_trace_item_count"],
        "pose_item_count": conv["pose_item_count"],
        "motion_item_count": conv["motion_item_count"],
        "tum_to_json_trace_conversion_ok": conv["conversion_ok"] is True,
        "generic_json_parser_reused": replay["generic_json_parser_reused"] is True,
        "candidate_bundle_mapping_ok": replay["candidate_bundle_mapping_ok"] is True,
    }
    passed = (
        checks["local_file_read_used"]
        and checks["file_source_admitted"]
        and checks["tum_row_count"] == 3
        and checks["json_trace_item_count"] == 5
        and checks["pose_item_count"] == 3
        and checks["motion_item_count"] == 2
        and checks["tum_to_json_trace_conversion_ok"]
        and checks["candidate_bundle_mapping_ok"]
    )
    return {
        "case_ref": "tum_valid_file_to_pose_motion_json_trace",
        "case_kind": "positive",
        "sample_file": sample_file,
        "passed": passed,
        "admission": pipe["admission"],
        "row_result": {k: v for k, v in row.items() if k != "valid_rows"},
        "conversion_result": {k: v for k, v in conv.items() if k != "json_trace_items"},
        "replay_result": {
            k: v for k, v in replay.items() if k != "spatial_evidence_candidate_bundle"
        },
        "checks": checks,
        "_internal": pipe,
    }


def run_positive_comments_file_case() -> Dict[str, Any]:
    sample_file = "sample_tum_valid_with_comments.txt"
    pipe = _load_tum_pipeline(sample_file)
    conv = pipe["conversion"]
    replay = pipe["replay"]
    row = pipe["row_result"]
    checks = {
        "comment_empty_line_handling_ok": row["skipped_line_count"] > 0
        and row["hard_error_count"] == 0,
        "valid_row_count": row["valid_row_count"],
        "json_trace_item_count": conv["json_trace_item_count"],
        "parser_replay_ok": replay["candidate_bundle_mapping_ok"] is True,
    }
    passed = (
        checks["comment_empty_line_handling_ok"]
        and checks["valid_row_count"] == 3
        and checks["json_trace_item_count"] == 5
        and checks["parser_replay_ok"]
    )
    return {
        "case_ref": "tum_valid_file_with_comments_and_empty_lines",
        "case_kind": "positive",
        "sample_file": sample_file,
        "passed": passed,
        "admission": pipe["admission"],
        "row_result": {k: v for k, v in row.items() if k != "valid_rows"},
        "conversion_result": {k: v for k, v in conv.items() if k != "json_trace_items"},
        "replay_result": {
            k: v for k, v in replay.items() if k != "spatial_evidence_candidate_bundle"
        },
        "checks": checks,
    }


def run_positive_field_task_guidance_case(prior_pipe: Dict[str, Any]) -> Dict[str, Any]:
    bundle = (prior_pipe.get("replay") or {}).get("spatial_evidence_candidate_bundle") or {}
    candidate_refs: List[str] = []
    for key in (
        "pose_candidates",
        "motion_candidates",
        "spatial_anchor_candidates",
        "slam_health_candidates",
        "map_drift_candidates",
        "relocalization_candidates",
    ):
        for candidate in bundle.get(key) or ():
            ref = candidate.get("candidate_ref")
            if ref:
                candidate_refs.append(ref)

    path_trace = {
        "trace_ref": "tum_field_task_guidance_replay_path",
        "replay_path": "field_task_guidance_candidate_replay_path",
        "candidate_only": True,
        "candidate_refs": candidate_refs,
        "guidance_candidate_is_not_runtime_navigation": True,
        "runtime_navigation_started": False,
        "field_entrypoint": TARGET_ENTRYPOINT,
        "source_chain": SOURCE_CHAIN,
    }
    checks = {
        "spatial_evidence_candidate_bundle_generated": bool(bundle),
        "candidate_refs_count": len(candidate_refs),
        "replay_path_candidate_only": path_trace["candidate_only"] is True,
        "no_runtime_navigation": path_trace["runtime_navigation_started"] is False,
    }
    passed = (
        checks["spatial_evidence_candidate_bundle_generated"]
        and checks["candidate_refs_count"] > 0
        and checks["replay_path_candidate_only"]
        and checks["no_runtime_navigation"]
    )
    return {
        "case_ref": "tum_file_to_field_task_guidance_replay_path",
        "case_kind": "positive",
        "sample_file": "derived_from_positive_case_1",
        "passed": passed,
        "path_trace": path_trace,
        "checks": checks,
    }


def run_positive_file_origin_source_chain_case() -> Dict[str, Any]:
    sample_file = "sample_tum_valid_trajectory.txt"
    pipe = _load_tum_pipeline(sample_file)
    conv = pipe["conversion"]
    replay = pipe["replay"]
    items = conv.get("json_trace_items") or []

    file_origin_preserved = bool(items) and all(
        bool((item.get("metadata") or {}).get("file_origin")) for item in items
    )
    source_chain_preserved = bool(items) and all(
        bool(item.get("source_chain")) for item in items
    )
    bundle = replay.get("spatial_evidence_candidate_bundle") or {}
    upstream_refs_preserved = True
    for key in ("pose_candidates", "motion_candidates"):
        for candidate in bundle.get(key) or ():
            if not candidate.get("source_chain"):
                upstream_refs_preserved = False

    checks = {
        "file_origin_metadata_preserved": file_origin_preserved,
        "source_chain_preserved_in_every_item": source_chain_preserved,
        "upstream_refs_preserved": upstream_refs_preserved,
    }
    passed = (
        file_origin_preserved
        and source_chain_preserved
        and upstream_refs_preserved
    )
    return {
        "case_ref": "tum_file_origin_and_source_chain_preserved",
        "case_kind": "positive",
        "sample_file": sample_file,
        "passed": passed,
        "admission": pipe["admission"],
        "conversion_result": {k: v for k, v in conv.items() if k != "json_trace_items"},
        "checks": checks,
    }


def run_negative_bad_column_count() -> Dict[str, Any]:
    sample_file = "invalid_tum_bad_column_count.txt"
    pipe = _load_tum_pipeline(sample_file)
    row = pipe["row_result"]
    conv = pipe["conversion"]
    rejected = (
        row["hard_error_count"] > 0
        and any("bad_column_count" in err for err in row["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {
        "case_ref": "invalid_bad_column_count_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "sample_file": sample_file,
        "passed": rejected,
        "checks": {
            "bad_column_count_rejected": rejected,
            "parse_errors": row["parse_errors"],
        },
    }


def run_negative_zero_quaternion() -> Dict[str, Any]:
    sample_file = "invalid_tum_zero_quaternion.txt"
    pipe = _load_tum_pipeline(sample_file)
    row = pipe["row_result"]
    conv = pipe["conversion"]
    rejected = (
        row["hard_error_count"] > 0
        and any("bad_quaternion_all_zero" in err for err in row["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {
        "case_ref": "invalid_zero_quaternion_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "sample_file": sample_file,
        "passed": rejected,
        "checks": {
            "zero_quaternion_rejected": rejected,
            "parse_errors": row["parse_errors"],
        },
    }


def run_negative_missing_source_chain_policy() -> Dict[str, Any]:
    import json

    sample_file = "invalid_tum_missing_source_chain_policy.json"
    path = _SAMPLES_DIR / sample_file
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        policy = {"_load_error": str(exc)}

    admission = admit_tum_file_source(
        sample_file=policy.get("sample_file", sample_file),
        policy=policy,
    )
    rejected = (
        admission["file_source_admitted"] is False
        and (
            "source_chain_missing" in admission["rejection_reasons"]
            or "file_origin_metadata_missing" in admission["rejection_reasons"]
        )
    )
    return {
        "case_ref": "invalid_missing_source_chain_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "sample_file": sample_file,
        "passed": rejected,
        "admission": admission,
        "checks": {
            "missing_source_chain_rejected": rejected,
            "rejection_reasons": admission["rejection_reasons"],
        },
    }


def run_negative_direct_candidate_bundle_bypass() -> Dict[str, Any]:
    backend_native_bundle = {
        "bundle_kind": "tum_native_direct_bundle",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "source_chain": ["tum_native_backend"],
        "direct_to_field_synthesis": True,
        "parser_ref_bypassed": True,
    }
    blocked = (
        backend_native_bundle.get("bundle_kind") != OUTPUT_CANDIDATE_CONTRACT_REF
        and backend_native_bundle.get("parser_ref_bypassed") is True
        and backend_native_bundle.get("direct_to_field_synthesis") is True
    )
    return {
        "case_ref": "invalid_direct_candidate_bundle_bypass_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "sample_file": "inline_negative",
        "passed": blocked,
        "checks": {
            "direct_candidate_bundle_bypass_rejected": blocked,
        },
    }


def build_positive_cases_v1() -> Tuple[GenericTUMRealFileLoaderDryRunCase, ...]:
    specs = (
        ("tum_valid_file_to_pose_motion_json_trace", "sample_tum_valid_trajectory.txt", "PASS"),
        (
            "tum_valid_file_with_comments_and_empty_lines",
            "sample_tum_valid_with_comments.txt",
            "PASS",
        ),
        (
            "tum_file_to_field_task_guidance_replay_path",
            "derived_from_positive_case_1",
            "PASS",
        ),
        (
            "tum_file_origin_and_source_chain_preserved",
            "sample_tum_valid_trajectory.txt",
            "PASS",
        ),
    )
    return tuple(
        GenericTUMRealFileLoaderDryRunCase(
            case_ref=case_ref,
            case_kind="positive",
            sample_file=sample_file,
            expected_outcome=outcome,
            source_chain=SOURCE_CHAIN,
        )
        for case_ref, sample_file, outcome in specs
    )


def build_negative_cases_v1() -> Tuple[GenericTUMRealFileLoaderDryRunCase, ...]:
    specs = (
        ("invalid_bad_column_count_rejected", "invalid_tum_bad_column_count.txt", "EXPECTED_REJECT"),
        ("invalid_zero_quaternion_rejected", "invalid_tum_zero_quaternion.txt", "EXPECTED_REJECT"),
        (
            "invalid_missing_source_chain_rejected",
            "invalid_tum_missing_source_chain_policy.json",
            "EXPECTED_REJECT",
        ),
        ("invalid_direct_candidate_bundle_bypass_rejected", "inline_negative", "EXPECTED_REJECT"),
    )
    return tuple(
        GenericTUMRealFileLoaderDryRunCase(
            case_ref=case_ref,
            case_kind="negative",
            sample_file=sample_file,
            expected_outcome=outcome,
            source_chain=SOURCE_CHAIN,
        )
        for case_ref, sample_file, outcome in specs
    )


def run_all_cases_v1() -> Dict[str, Any]:
    case1 = run_positive_valid_file_case()
    case2 = run_positive_comments_file_case()
    case3 = run_positive_field_task_guidance_case(case1.get("_internal") or {})
    case4 = run_positive_file_origin_source_chain_case()

    case1_public = {k: v for k, v in case1.items() if k != "_internal"}

    positive_results = [case1_public, case2, case3, case4]
    negative_results = [
        run_negative_bad_column_count(),
        run_negative_zero_quaternion(),
        run_negative_missing_source_chain_policy(),
        run_negative_direct_candidate_bundle_bypass(),
    ]

    return {
        "positive_cases": positive_results,
        "negative_cases": negative_results,
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "primary_positive_case": case1_public,
    }
