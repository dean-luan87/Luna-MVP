# -*- coding: utf-8 -*-
"""
Phase-CoreCapability-TRW-Unified-002
Verifier: YOLO/OCR RequestTrace Shadow Adapter v0.

Checks strict offline/shadow invariants and required stage presence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


REQ_STAGE_NAMESPACE = "core_capability_request_trace_v0"

YOLO_REQUIRED_STAGES = [
    "request_trace.stage.perception.yolo.input_frame",
    "request_trace.stage.perception.yolo.detector_invocation",
    "request_trace.stage.perception.yolo.detection_result",
    "request_trace.stage.perception.yolo.risk_or_object_classification",
    "request_trace.stage.perception.yolo.observability_envelope",
]

OCR_REQUIRED_STAGES = [
    "request_trace.stage.perception.ocr.source_policy_selection",
    "request_trace.stage.perception.ocr.input_region",
    "request_trace.stage.perception.ocr.provider_invocation",
    "request_trace.stage.perception.ocr.raw_text_result",
    "request_trace.stage.perception.ocr.length_segmentation",
    "request_trace.stage.perception.ocr.reading_order",
    "request_trace.stage.perception.ocr.observability_envelope",
]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_stage_records(chains: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for ch in chains:
        stages = ch.get("stages")
        if isinstance(stages, list):
            for st in stages:
                if isinstance(st, dict):
                    out.append(st)
    return out


def _non_empty_file(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def _require(cond: bool, msg: str, errors: List[str]) -> None:
    if not cond:
        errors.append(msg)


def _check_stage_set(records: List[Dict[str, Any]], required: List[str], errors: List[str], label: str) -> None:
    seen: Set[str] = set()
    for r in records:
        n = r.get("stage_name")
        if isinstance(n, str):
            seen.add(n)
    missing = [x for x in required if x not in seen]
    if missing:
        errors.append(f"{label}: missing required stages: {missing}")


def _check_hard_audit(records: List[Dict[str, Any]], errors: List[str], label: str) -> None:
    for r in records:
        ha = r.get("hard_audit")
        if not isinstance(ha, dict):
            errors.append(f"{label}: hard_audit missing/not dict at stage={r.get('stage_name')}")
            continue
        # Common no-go conditions
        if ha.get("real_tts_invoked") not in (False, None):
            errors.append(f"{label}: real_tts_invoked must be false at stage={r.get('stage_name')}")
        if ha.get("navigation_action") not in (None, ""):
            errors.append(f"{label}: navigation_action must be null at stage={r.get('stage_name')}")
        if ha.get("downstream_invocation_count") not in (0, None):
            errors.append(f"{label}: downstream_invocation_count must be 0 at stage={r.get('stage_name')}")

        if label == "yolo":
            if ha.get("runtime_invoked") not in (False, None):
                errors.append(f"{label}: runtime_invoked must be false at stage={r.get('stage_name')}")
        if label == "ocr":
            if ha.get("semantic_interpretation_enabled") not in (False, None):
                errors.append(
                    f"{label}: semantic_interpretation_enabled must be false at stage={r.get('stage_name')}"
                )
            if ha.get("allows_execute_now") not in (False, None):
                errors.append(f"{label}: allows_execute_now must be false at stage={r.get('stage_name')}")


def _check_missing_fields_policy(records: List[Dict[str, Any]], errors: List[str], label: str) -> None:
    for r in records:
        # trace_id/session_id must not be fabricated
        if r.get("trace_id") not in (None, ""):
            errors.append(f"{label}: trace_id must be null (no fabrication) at stage={r.get('stage_name')}")
        if r.get("session_id") not in (None, ""):
            errors.append(f"{label}: session_id must be null (no fabrication) at stage={r.get('stage_name')}")
        mf = r.get("missing_fields")
        if not (isinstance(mf, list) and "trace_id" in mf and "session_id" in mf):
            errors.append(
                f"{label}: missing_fields must include trace_id and session_id at stage={r.get('stage_name')}"
            )


def _check_refs(records: List[Dict[str, Any]], errors: List[str], label: str) -> None:
    for r in records:
        srefs = r.get("source_refs")
        _require(isinstance(srefs, dict), f"{label}: source_refs missing/not dict at stage={r.get('stage_name')}", errors)
        if isinstance(srefs, dict):
            # Must preserve original refs keys (may be null but must exist)
            for k in ("trace_ref", "replay_ref", "whitebox_ref", "original_summary_ref", "source_root"):
                if k not in srefs:
                    errors.append(f"{label}: source_refs missing key {k} at stage={r.get('stage_name')}")


def verify(output_root: Path, yolo_root: Path, ocr_root: Path) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    _require(yolo_root.exists() and yolo_root.is_dir(), f"yolo root not readable: {yolo_root}", errors)
    _require(ocr_root.exists() and ocr_root.is_dir(), f"ocr root not readable: {ocr_root}", errors)

    yolo_chains_path = output_root / "yolo_request_trace_chains.json"
    ocr_chains_path = output_root / "ocr_request_trace_chains.json"
    _require(yolo_chains_path.exists(), "missing yolo_request_trace_chains.json", errors)
    _require(ocr_chains_path.exists(), "missing ocr_request_trace_chains.json", errors)

    yolo_chains = _read_json(yolo_chains_path) if yolo_chains_path.exists() else []
    ocr_chains = _read_json(ocr_chains_path) if ocr_chains_path.exists() else []

    _require(isinstance(yolo_chains, list) and len(yolo_chains) > 0, "yolo chains not generated", errors)
    _require(isinstance(ocr_chains, list) and len(ocr_chains) > 0, "ocr chains not generated", errors)

    yolo_records = _iter_stage_records(yolo_chains) if isinstance(yolo_chains, list) else []
    ocr_records = _iter_stage_records(ocr_chains) if isinstance(ocr_chains, list) else []

    _check_stage_set(yolo_records, YOLO_REQUIRED_STAGES, errors, "yolo")
    _check_stage_set(ocr_records, OCR_REQUIRED_STAGES, errors, "ocr")

    # namespace + identity
    for label, records in (("yolo", yolo_records), ("ocr", ocr_records)):
        for r in records:
            _require(
                r.get("stage_namespace") == REQ_STAGE_NAMESPACE,
                f"{label}: stage_namespace mismatch at stage={r.get('stage_name')}",
                errors,
            )
            _require(bool(r.get("request_id")), f"{label}: request_id missing at stage={r.get('stage_name')}", errors)
            _require(bool(r.get("source_run_id")), f"{label}: source_run_id missing at stage={r.get('stage_name')}", errors)

    _check_missing_fields_policy(yolo_records, errors, "yolo")
    _check_missing_fields_policy(ocr_records, errors, "ocr")
    _check_refs(yolo_records, errors, "yolo")
    _check_refs(ocr_records, errors, "ocr")
    _check_hard_audit(yolo_records, errors, "yolo")
    _check_hard_audit(ocr_records, errors, "ocr")

    # shadow JSONL outputs must exist and be non-empty
    for p in (
        output_root / "core_capability_shadow_trace.jsonl",
        output_root / "core_capability_shadow_replay.jsonl",
        output_root / "core_capability_shadow_whitebox.jsonl",
    ):
        _require(_non_empty_file(p), f"jsonl output missing/empty: {p.name}", errors)

    # best-effort: ensure we didn't write into source roots (we never should)
    # We can only warn if output_root is within yolo_root/ocr_root.
    try:
        if str(output_root.resolve()).startswith(str(yolo_root.resolve())):
            warnings.append("output_root is inside yolo_root; this is discouraged (but not a runtime boundary breach).")
        if str(output_root.resolve()).startswith(str(ocr_root.resolve())):
            warnings.append("output_root is inside ocr_root; this is discouraged (but not a runtime boundary breach).")
    except Exception:
        pass

    verdict = "GO" if not errors else "NO_GO"
    return {"verdict": verdict, "errors": errors, "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--yolo-root", required=True)
    ap.add_argument("--ocr-root", required=True)
    args = ap.parse_args()

    report = verify(Path(args.output_root), Path(args.yolo_root), Path(args.ocr_root))
    out_path = Path(args.output_root) / "core_capability_request_trace_shadow_verify_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verdict"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

