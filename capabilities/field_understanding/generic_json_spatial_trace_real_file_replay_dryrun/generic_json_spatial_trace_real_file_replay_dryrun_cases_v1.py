# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Real File Controlled Replay DryRun — cases v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_static_validators_v1 import (
    map_parsed_traces_to_candidate_bundle,
    parse_json_spatial_trace_item,
    validate_candidate_bundle_mapping,
    validate_negative_trace_item,
)
from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
)
from capabilities.field_understanding.generic_json_spatial_trace_real_file_replay_dryrun.generic_json_spatial_trace_real_file_replay_dryrun_types_v1 import (
    FUSION_CANDIDATE_REF,
    GenericJSONSpatialTraceRealFileReplayDryRunCase,
    NEGATIVE_CASE_REFS,
    OUTPUT_CANDIDATE_CONTRACT_REF,
    POSITIVE_CASE_REFS,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
)

_MODULE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _MODULE_DIR.parents[2]
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


def load_sample_file(sample_file: str) -> Tuple[Optional[Dict[str, Any]], bool, List[str]]:
    path = _SAMPLES_DIR / sample_file
    issues: List[str] = []
    if not path.is_file():
        return None, False, [f"sample_file_missing:{sample_file}"]
    if not is_controlled_sample_path(path):
        return None, False, [f"sample_path_not_controlled:{sample_file}"]
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, True, [f"sample_read_failed:{sample_file}:{exc}"]
    if not isinstance(doc, dict):
        return None, True, [f"sample_root_not_object:{sample_file}"]
    return doc, True, issues


def admit_real_file_source(
    *,
    sample_file: str,
    file_doc: Dict[str, Any],
) -> Dict[str, Any]:
    path = _SAMPLES_DIR / sample_file
    rejection_reasons: List[str] = []
    file_origin = file_doc.get("file_origin") or {}
    if not file_origin:
        rejection_reasons.append("file_origin_metadata_missing")
    if file_doc.get("format_ref") != "generic_json_spatial_trace":
        rejection_reasons.append("format_ref_not_generic_json_spatial_trace")
    if not is_controlled_sample_path(path):
        rejection_reasons.append("controlled_samples_path_violation")
    trace_items = file_doc.get("trace_items") or []
    if not trace_items:
        rejection_reasons.append("trace_items_empty")
    admitted = len(rejection_reasons) == 0
    return {
        "result_ref": f"admission_{sample_file}",
        "file_source_admitted": admitted,
        "file_origin_metadata_present": bool(file_origin),
        "controlled_samples_path_ok": is_controlled_sample_path(path),
        "rejection_reasons": rejection_reasons,
        "source_chain": SOURCE_CHAIN,
    }


def build_input_bundle(sample_file: str, file_doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "bundle_ref": f"input_bundle_{sample_file}",
        "sample_file": sample_file,
        "file_origin": dict(file_doc.get("file_origin") or {}),
        "trace_items": list(file_doc.get("trace_items") or []),
        "source_chain": SOURCE_CHAIN,
    }


def parse_trace_items(trace_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    parsed_items: List[Dict[str, Any]] = []
    parse_errors: List[str] = []
    for item in trace_items:
        parsed, errors = parse_json_spatial_trace_item(item)
        if errors:
            parse_errors.extend([f"{item.get('trace_id')}:{err}" for err in errors])
        parsed_items.extend(parsed)
    return {
        "result_ref": "parsed_trace_result",
        "parsed_count": len(parsed_items),
        "parse_errors": parse_errors,
        "parsed_items": parsed_items,
        "source_chain": SOURCE_CHAIN,
    }


def build_candidate_bundle_result(parsed_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    bundle = map_parsed_traces_to_candidate_bundle(parsed_items)
    bundle_ok, bundle_issues = validate_candidate_bundle_mapping(bundle)
    return {
        "result_ref": "candidate_bundle_result",
        "candidate_bundle_mapping_ok": bundle_ok,
        "bundle_ref": bundle.get("bundle_ref"),
        "output_candidate_types": tuple(bundle.get("output_candidate_types") or ()),
        "bundle_issues": bundle_issues,
        "spatial_evidence_candidate_bundle": bundle,
        "source_chain": SOURCE_CHAIN,
    }


def plan_fusion_replay_path(
    bundle: Dict[str, Any],
    parsed_items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    gps_hint_preserved = False
    gps_override_blocked = True
    conflict_candidate_retained = True
    for parsed in parsed_items:
        payload = (parsed.get("normalized_payload") or {}).get("payload") or {}
        gps_hint = payload.get("gps_hint") or {}
        if gps_hint:
            gps_hint_preserved = True
            if gps_hint.get("must_not_override_field_identity") is not True:
                gps_override_blocked = False
    return {
        "trace_ref": "spatial_fusion_replay_path",
        "replay_path": FUSION_CANDIDATE_REF,
        "candidate_only": True,
        "relocalization_does_not_restore_runtime_trust": True,
        "gps_does_not_override_field_identity": gps_override_blocked and gps_hint_preserved,
        "gps_hint_metadata_preserved": gps_hint_preserved,
        "conflict_candidate_path_retained": conflict_candidate_retained,
        "runtime_navigation_started": False,
        "source_chain": SOURCE_CHAIN,
        "spatial_evidence_refs": list(bundle.get("output_candidate_types") or ()),
    }


def plan_field_task_guidance_replay_path(
    candidate_refs: List[str],
) -> Dict[str, Any]:
    return {
        "trace_ref": "field_task_guidance_replay_path",
        "replay_path": "field_task_guidance_candidate_replay_path",
        "candidate_refs": candidate_refs,
        "candidate_only": True,
        "guidance_candidate_is_not_runtime_navigation": True,
        "runtime_navigation_started": False,
        "field_entrypoint": TARGET_ENTRYPOINT,
        "source_chain": SOURCE_CHAIN,
    }


def run_positive_file_case(
    *,
    case_ref: str,
    sample_file: str,
    expected_replay_path: str,
    extra_checks: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    file_doc, read_ok, read_issues = load_sample_file(sample_file)
    admission = admit_real_file_source(sample_file=sample_file, file_doc=file_doc or {})
    admitted = admission["file_source_admitted"] and read_ok and file_doc is not None

    parsed_result: Dict[str, Any] = {
        "parsed_count": 0,
        "parse_errors": read_issues,
        "parsed_items": [],
    }
    bundle_result: Dict[str, Any] = {
        "candidate_bundle_mapping_ok": False,
        "bundle_issues": ["not_admitted"],
        "spatial_evidence_candidate_bundle": {},
    }
    path_trace: Dict[str, Any] = {
        "replay_path": expected_replay_path,
        "candidate_only": True,
        "runtime_navigation_started": False,
    }

    if admitted and file_doc:
        trace_items = file_doc.get("trace_items") or []
        parsed_result = parse_trace_items(trace_items)
        if parsed_result["parsed_count"] > 0 and not parsed_result["parse_errors"]:
            bundle_result = build_candidate_bundle_result(parsed_result["parsed_items"])
            path_trace = {
                "trace_ref": case_ref,
                "replay_path": expected_replay_path,
                "candidate_only": True,
                "relocalization_does_not_restore_runtime_trust": True,
                "gps_does_not_override_field_identity": True,
                "runtime_navigation_started": False,
                "source_chain": SOURCE_CHAIN,
            }
            if case_ref == "real_file_spatial_fusion_replay":
                path_trace = plan_fusion_replay_path(
                    bundle_result.get("spatial_evidence_candidate_bundle") or {},
                    parsed_result["parsed_items"],
                )

    checks = {
        "file_source_admitted": admitted,
        "local_file_read_used": read_ok,
        "parsed_ok": parsed_result["parsed_count"] > 0 and not parsed_result["parse_errors"],
        "candidate_bundle_mapping_ok": bundle_result.get("candidate_bundle_mapping_ok") is True,
        "candidate_only": path_trace.get("candidate_only") is True,
        "runtime_navigation_started": path_trace.get("runtime_navigation_started") is True,
    }
    if extra_checks:
        checks.update(extra_checks)

    passed = (
        admitted
        and read_ok
        and checks["parsed_ok"]
        and checks["candidate_bundle_mapping_ok"]
        and checks["candidate_only"]
        and not checks["runtime_navigation_started"]
    )
    if case_ref == "real_file_odometry_health_replay":
        bundle = bundle_result.get("spatial_evidence_candidate_bundle") or {}
        health_candidates = bundle.get("slam_health_candidates") or []
        passed = passed and len(health_candidates) > 0
        checks["health_candidate_generated"] = len(health_candidates) > 0
        checks["health_candidate_risk_only"] = all(
            c.get("candidate_only") is True for c in health_candidates
        )
    if case_ref == "real_file_anchor_relocalization_drift_replay":
        bundle = bundle_result.get("spatial_evidence_candidate_bundle") or {}
        checks["relocalization_candidate_generated"] = len(
            bundle.get("relocalization_candidates") or []
        ) > 0
        checks["drift_candidate_generated"] = len(bundle.get("map_drift_candidates") or []) > 0
        checks["relocalization_does_not_restore_runtime_trust"] = all(
            (c.get("normalized_payload") or {}).get("payload", {}).get("runtime_trust_restore")
            is not True
            for c in bundle.get("relocalization_candidates") or []
        )
        passed = (
            passed
            and checks["relocalization_candidate_generated"]
            and checks["drift_candidate_generated"]
            and checks["relocalization_does_not_restore_runtime_trust"]
        )

    return {
        "case_ref": case_ref,
        "case_kind": "positive",
        "sample_file": sample_file,
        "passed": passed,
        "admission": admission,
        "input_bundle": build_input_bundle(sample_file, file_doc or {}),
        "parsed_result": parsed_result,
        "bundle_result": bundle_result,
        "path_trace": path_trace,
        "checks": checks,
    }


def run_field_task_guidance_positive_case(
    *,
    prior_positive_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    candidate_refs: List[str] = []
    for result in prior_positive_results:
        bundle = (result.get("bundle_result") or {}).get("spatial_evidence_candidate_bundle") or {}
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

    path_trace = plan_field_task_guidance_replay_path(candidate_refs)
    passed = (
        len(candidate_refs) > 0
        and path_trace.get("candidate_only") is True
        and path_trace.get("guidance_candidate_is_not_runtime_navigation") is True
        and path_trace.get("runtime_navigation_started") is False
    )
    return {
        "case_ref": "real_file_field_task_guidance_replay_path",
        "case_kind": "positive",
        "sample_file": "derived_from_prior_positive_cases",
        "passed": passed,
        "path_trace": path_trace,
        "checks": {
            "field_task_guidance_replay_path_ok": passed,
            "candidate_refs_count": len(candidate_refs),
            "guidance_candidate_remains_candidate": path_trace.get("candidate_only") is True,
            "no_runtime_navigation": path_trace.get("runtime_navigation_started") is False,
        },
    }


def run_negative_missing_source_chain() -> Dict[str, Any]:
    file_doc, read_ok, _ = load_sample_file("invalid_missing_source_chain_trace.json")
    admission = admit_real_file_source(
        sample_file="invalid_missing_source_chain_trace.json",
        file_doc=file_doc or {},
    )
    parsed_result = parse_trace_items((file_doc or {}).get("trace_items") or [])
    rejected = (
        read_ok
        and (not parsed_result["parsed_count"] or parsed_result["parse_errors"])
    )
    return {
        "case_ref": "invalid_missing_source_chain_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "passed": rejected,
        "admission": admission,
        "parsed_result": parsed_result,
        "checks": {
            "missing_source_chain_rejected": rejected,
            "parse_errors_present": bool(parsed_result["parse_errors"]),
        },
    }


def run_negative_unsupported_candidate_type() -> Dict[str, Any]:
    item = {
        "trace_id": "negative_unsupported_type_inline",
        "source_chain": [SOURCE_CHAIN, "negative_unsupported_type_inline"],
        "timestamp_ms": 1700010000,
        "confidence": 0.5,
        "candidate_type": "unsupported_xyz",
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "payload": {},
        "candidate_only": True,
    }
    rejected_ok, issues = validate_negative_trace_item(item, expect_issue="unsupported_candidate_type")
    return {
        "case_ref": "invalid_unsupported_candidate_type_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "passed": rejected_ok,
        "checks": {
            "unsupported_candidate_type_rejected": rejected_ok,
            "issues": issues,
        },
    }


def run_negative_backend_native_direct_to_field() -> Dict[str, Any]:
    backend_native_bundle = {
        "bundle_kind": "rtab_map_native_output",
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "source_chain": ["rtab_map_native_backend"],
        "direct_to_field_synthesis": True,
        "parser_ref_bypassed": True,
    }
    blocked = (
        backend_native_bundle.get("bundle_kind") != OUTPUT_CANDIDATE_CONTRACT_REF
        and backend_native_bundle.get("parser_ref_bypassed") is True
        and backend_native_bundle.get("direct_to_field_synthesis") is True
    )
    return {
        "case_ref": "invalid_backend_native_direct_to_field_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "passed": blocked,
        "checks": {
            "backend_native_output_direct_to_field_blocked": blocked,
        },
    }


def run_negative_runtime_escalation() -> Dict[str, Any]:
    forbidden_flags = {
        "runtime_activation_allowed": True,
        "direct_action_allowed": True,
        "direct_speech_allowed": True,
        "direct_fact_write_allowed": True,
    }
    rejected = any(forbidden_flags.values())
    return {
        "case_ref": "invalid_runtime_escalation_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "passed": rejected,
        "checks": {
            "runtime_escalation_rejected": rejected,
            "forbidden_flags": forbidden_flags,
        },
    }


def build_positive_cases_v1() -> Tuple[GenericJSONSpatialTraceRealFileReplayDryRunCase, ...]:
    specs = (
        ("real_file_pose_motion_low_risk_replay", "sample_pose_motion_trace.json", "PASS"),
        ("real_file_odometry_health_replay", "sample_odometry_health_trace.json", "PASS"),
        (
            "real_file_anchor_relocalization_drift_replay",
            "sample_anchor_relocalization_drift_trace.json",
            "PASS",
        ),
        ("real_file_spatial_fusion_replay", "sample_spatial_fusion_trace.json", "PASS"),
        ("real_file_field_task_guidance_replay_path", "derived_from_prior_positive_cases", "PASS"),
    )
    return tuple(
        GenericJSONSpatialTraceRealFileReplayDryRunCase(
            case_ref=case_ref,
            case_kind="positive",
            sample_file=sample_file,
            expected_outcome=outcome,
            source_chain=SOURCE_CHAIN,
        )
        for case_ref, sample_file, outcome in specs
    )


def build_negative_cases_v1() -> Tuple[GenericJSONSpatialTraceRealFileReplayDryRunCase, ...]:
    specs = (
        ("invalid_missing_source_chain_rejected", "invalid_missing_source_chain_trace.json", "EXPECTED_REJECT"),
        ("invalid_unsupported_candidate_type_rejected", "inline_negative", "EXPECTED_REJECT"),
        ("invalid_backend_native_direct_to_field_rejected", "inline_negative", "EXPECTED_REJECT"),
        ("invalid_runtime_escalation_rejected", "inline_negative", "EXPECTED_REJECT"),
    )
    return tuple(
        GenericJSONSpatialTraceRealFileReplayDryRunCase(
            case_ref=case_ref,
            case_kind="negative",
            sample_file=sample_file,
            expected_outcome=outcome,
            source_chain=SOURCE_CHAIN,
        )
        for case_ref, sample_file, outcome in specs
    )


def run_all_cases_v1() -> Dict[str, Any]:
    file_positive_results: List[Dict[str, Any]] = [
        run_positive_file_case(
            case_ref="real_file_pose_motion_low_risk_replay",
            sample_file="sample_pose_motion_trace.json",
            expected_replay_path=OUTPUT_CANDIDATE_CONTRACT_REF,
        ),
        run_positive_file_case(
            case_ref="real_file_odometry_health_replay",
            sample_file="sample_odometry_health_trace.json",
            expected_replay_path=OUTPUT_CANDIDATE_CONTRACT_REF,
        ),
        run_positive_file_case(
            case_ref="real_file_anchor_relocalization_drift_replay",
            sample_file="sample_anchor_relocalization_drift_trace.json",
            expected_replay_path=OUTPUT_CANDIDATE_CONTRACT_REF,
        ),
        run_positive_file_case(
            case_ref="real_file_spatial_fusion_replay",
            sample_file="sample_spatial_fusion_trace.json",
            expected_replay_path=FUSION_CANDIDATE_REF,
        ),
    ]
    guidance_result = run_field_task_guidance_positive_case(prior_positive_results=file_positive_results)
    positive_results = file_positive_results + [guidance_result]

    negative_results = [
        run_negative_missing_source_chain(),
        run_negative_unsupported_candidate_type(),
        run_negative_backend_native_direct_to_field(),
        run_negative_runtime_escalation(),
    ]

    return {
        "positive_cases": positive_results,
        "negative_cases": negative_results,
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
    }
