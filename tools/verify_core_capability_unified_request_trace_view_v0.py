# -*- coding: utf-8 -*-
"""
Phase-CoreCapability-TRW-Unified-003
Verifier: Unified Core RequestTrace Extractor View v0 (offline/shadow only).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set


YOLO_REQUIRED_STAGES = {
    "request_trace.stage.perception.yolo.input_frame",
    "request_trace.stage.perception.yolo.detector_invocation",
    "request_trace.stage.perception.yolo.detection_result",
    "request_trace.stage.perception.yolo.risk_or_object_classification",
    "request_trace.stage.perception.yolo.observability_envelope",
}

OCR_REQUIRED_STAGES = {
    "request_trace.stage.perception.ocr.source_policy_selection",
    "request_trace.stage.perception.ocr.input_region",
    "request_trace.stage.perception.ocr.provider_invocation",
    "request_trace.stage.perception.ocr.raw_text_result",
    "request_trace.stage.perception.ocr.length_segmentation",
    "request_trace.stage.perception.ocr.reading_order",
    "request_trace.stage.perception.ocr.observability_envelope",
}

# Voice (Phase-005) historical mapping prefix; stage list is 12 in that phase.
VOICE_REQUIRED_STAGES = {
    "request_trace.stage.voice_output.candidate_input",
    "request_trace.stage.voice_output.speakable_guard",
    "request_trace.stage.voice_output.speech_gate",
    "request_trace.stage.voice_output.expiry_check",
    "request_trace.stage.voice_output.stale_check",
    "request_trace.stage.voice_output.cancellation_check",
    "request_trace.stage.voice_output.priority_check",
    "request_trace.stage.voice_output.interruption_check",
    "request_trace.stage.voice_output.suppression_check",
    "request_trace.stage.voice_output.provider_health_check",
    "request_trace.stage.voice_output.audit_envelope",
    "request_trace.stage.voice_output.final_governance_decision",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _non_empty_file(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def _require(cond: bool, msg: str, errors: List[str]) -> None:
    if not cond:
        errors.append(msg)


def _collect_stage_names(stage_ns_index: Dict[str, Any], capability: str) -> Set[str]:
    names: Set[str] = set()
    for ns, payload in stage_ns_index.items():
        if ns == "notes":
            continue
        if not isinstance(payload, dict):
            continue
        caps = payload.get("capabilities")
        if not isinstance(caps, dict) or capability not in caps:
            continue
        sn = payload.get("stage_names")
        if isinstance(sn, dict):
            for k in sn.keys():
                if isinstance(k, str):
                    names.add(k)
    return names


def _check_hard_audit_from_unified_jsonl(jsonl_path: Path, errors: List[str]) -> None:
    # Read line-by-line (avoid loading huge files). We only assert that forbidden flags are not true / non-null.
    # We keep checks lightweight and structural.
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except Exception:
                errors.append(f"invalid jsonl at {jsonl_path.name}:{line_no}")
                break
            ha = row.get("hard_audit")
            if not isinstance(ha, dict):
                errors.append(f"hard_audit missing/not dict at {jsonl_path.name}:{line_no}")
                break
            # Global invariants
            if ha.get("real_tts_invoked") not in (False, None):
                errors.append(f"real_tts_invoked must be false at {jsonl_path.name}:{line_no}")
                break
            if ha.get("navigation_action") not in (None, ""):
                errors.append(f"navigation_action must be null at {jsonl_path.name}:{line_no}")
                break
            if ha.get("downstream_invocation_count") not in (0, None):
                errors.append(f"downstream_invocation_count must be 0 at {jsonl_path.name}:{line_no}")
                break

            cap = row.get("capability")
            if cap == "yolo":
                if ha.get("runtime_invoked") not in (False, None):
                    errors.append(f"yolo runtime_invoked must be false at {jsonl_path.name}:{line_no}")
                    break
            if cap == "ocr":
                if ha.get("semantic_interpretation_enabled") not in (False, None):
                    errors.append(f"ocr semantic_interpretation_enabled must be false at {jsonl_path.name}:{line_no}")
                    break
                if ha.get("allows_execute_now") not in (False, None):
                    errors.append(f"ocr allows_execute_now must be false at {jsonl_path.name}:{line_no}")
                    break
            if cap == "voice":
                if ha.get("provider_invoked") not in (False, None):
                    errors.append(f"voice provider_invoked must be false at {jsonl_path.name}:{line_no}")
                    break
                if ha.get("playback_invoked") not in (False, None):
                    errors.append(f"voice playback_invoked must be false at {jsonl_path.name}:{line_no}")
                    break


def verify(output_root: Path, core_shadow_root: Path, voice_shadow_root: Path) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    _require(core_shadow_root.exists() and core_shadow_root.is_dir(), f"core shadow root not readable: {core_shadow_root}", errors)
    _require(voice_shadow_root.exists() and voice_shadow_root.is_dir(), f"voice shadow root not readable: {voice_shadow_root}", errors)

    # Output existence
    summary_p = output_root / "core_capability_unified_request_trace_summary.json"
    chains_p = output_root / "core_capability_unified_request_chains.json"
    ns_idx_p = output_root / "core_capability_stage_namespace_index.json"
    timeline_p = output_root / "core_capability_timeline_index.json"
    matrix_p = output_root / "core_capability_observability_matrix.json"
    src_idx_p = output_root / "core_capability_source_root_index.json"
    missing_p = output_root / "core_capability_missing_field_report.json"

    for p in (summary_p, chains_p, ns_idx_p, timeline_p, matrix_p, src_idx_p, missing_p):
        _require(p.exists(), f"missing output json: {p.name}", errors)

    # JSONL must be non-empty
    for p in (
        output_root / "core_capability_unified_trace.jsonl",
        output_root / "core_capability_unified_replay.jsonl",
        output_root / "core_capability_unified_whitebox.jsonl",
    ):
        _require(_non_empty_file(p), f"jsonl output missing/empty: {p.name}", errors)

    # Load indices
    chain_index = _read_json(chains_p) if chains_p.exists() else []
    ns_index = _read_json(ns_idx_p) if ns_idx_p.exists() else {}

    _require(isinstance(chain_index, list) and len(chain_index) > 0, "unified chain index not generated", errors)
    _require(isinstance(ns_index, dict) and len(ns_index) > 0, "stage namespace index not generated", errors)

    # Capability index includes yolo/ocr/voice
    caps = {x.get("capability") for x in chain_index if isinstance(x, dict)}
    _require("yolo" in caps, "capability index missing yolo", errors)
    _require("ocr" in caps, "capability index missing ocr", errors)
    _require("voice" in caps, "capability index missing voice", errors)

    # Required stages presence (from stage namespace index)
    yolo_seen = _collect_stage_names(ns_index, "yolo")
    ocr_seen = _collect_stage_names(ns_index, "ocr")
    voice_seen = _collect_stage_names(ns_index, "voice")

    missing_yolo = sorted(list(YOLO_REQUIRED_STAGES - yolo_seen))
    missing_ocr = sorted(list(OCR_REQUIRED_STAGES - ocr_seen))
    missing_voice = sorted(list(VOICE_REQUIRED_STAGES - voice_seen))

    if missing_yolo:
        errors.append(f"missing yolo required stages: {missing_yolo}")
    if missing_ocr:
        errors.append(f"missing ocr required stages: {missing_ocr}")
    if missing_voice:
        errors.append(f"missing voice required stages: {missing_voice}")

    # source_root refs preserved (index file should contain both roots)
    src_idx = _read_json(src_idx_p) if src_idx_p.exists() else {}
    if isinstance(src_idx, dict):
        _require(bool(src_idx.get("core_shadow_root")), "core_shadow_root missing in source_root_index", errors)
        _require(bool(src_idx.get("voice_shadow_root")), "voice_shadow_root missing in source_root_index", errors)
    else:
        errors.append("source_root_index invalid")

    # Hard audit checks from unified JSONL (trace stream is enough)
    trace_jsonl = output_root / "core_capability_unified_trace.jsonl"
    if trace_jsonl.exists():
        _check_hard_audit_from_unified_jsonl(trace_jsonl, errors)

    verdict = "GO" if not errors else "NO_GO"
    return {"verdict": verdict, "errors": errors, "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--core-shadow-root", required=True)
    ap.add_argument("--voice-shadow-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    report = verify(Path(args.output_root), Path(args.core_shadow_root), Path(args.voice_shadow_root))
    out_path = Path(args.output_root) / "core_capability_unified_request_trace_view_verify_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verdict"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

