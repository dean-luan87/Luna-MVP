# -*- coding: utf-8 -*-
"""
Phase-CoreCapability-TRW-Unified-004
Export package generator for Unified Core RequestTrace shadow view (Phase-003).

Outputs:
- capability/stage/hard_audit/missing_fields tables
- field-level mapping report (best-effort, without fabricating missing fields)
- markdown export report for whitebox backend / architecture review

Hard boundaries:
- offline/shadow only
- no runtime invocation
- preserve source_root/source_refs
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if isinstance(obj, dict):
                yield obj


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _mk_out_root(p: Optional[str]) -> Path:
    out = Path(p) if p else (Path("logs") / f"core_capability_unified_export_004_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    if not out.is_absolute():
        out = Path.cwd() / out
    out.mkdir(parents=True, exist_ok=True)
    return out


def _collect_stage_records(input_root: Path) -> List[Dict[str, Any]]:
    trace_jsonl = input_root / "core_capability_unified_trace.jsonl"
    if not trace_jsonl.exists():
        raise FileNotFoundError(f"missing unified jsonl: {trace_jsonl}")
    return list(_iter_jsonl(trace_jsonl))


def _load_chain_index(input_root: Path) -> List[Dict[str, Any]]:
    p = input_root / "core_capability_unified_request_chains.json"
    return _read_json(p) if p.exists() else []


def _table_capability(chain_index: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    agg: Dict[str, Dict[str, Any]] = {}
    for row in chain_index:
        if not isinstance(row, dict):
            continue
        cap = row.get("capability")
        if not isinstance(cap, str):
            continue
        agg.setdefault(cap, {"capability": cap, "chain_count": 0, "total_stage_count": 0, "stage_per_chain_max": 0})
        agg[cap]["chain_count"] += 1
        sc = row.get("stage_count") if isinstance(row.get("stage_count"), int) else 0
        agg[cap]["total_stage_count"] += sc
        agg[cap]["stage_per_chain_max"] = max(int(agg[cap]["stage_per_chain_max"]), sc)
    return sorted(list(agg.values()), key=lambda x: x["capability"])


def _table_stage(stage_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    agg: Dict[Tuple[str, str], int] = {}
    for r in stage_records:
        cap = r.get("capability")
        sn = r.get("stage_name")
        if isinstance(cap, str) and isinstance(sn, str):
            agg[(cap, sn)] = agg.get((cap, sn), 0) + 1
    out = [{"capability": cap, "stage_name": sn, "record_count": c} for (cap, sn), c in agg.items()]
    return sorted(out, key=lambda x: (x["capability"], x["stage_name"]))


def _table_missing_fields(stage_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    agg: Dict[Tuple[str, str], int] = {}
    for r in stage_records:
        cap = r.get("capability")
        mf = r.get("missing_fields")
        if not isinstance(cap, str) or not isinstance(mf, list):
            continue
        for x in mf:
            if isinstance(x, str):
                agg[(cap, x)] = agg.get((cap, x), 0) + 1
    out = [{"capability": cap, "missing_field": f, "record_count": c} for (cap, f), c in agg.items()]
    return sorted(out, key=lambda x: (x["capability"], x["missing_field"]))


def _hard_audit_anomaly_flags(ha: Dict[str, Any], cap: str) -> Dict[str, bool]:
    def _bad(v: Any, allowed: Tuple[Any, ...]) -> bool:
        return v not in allowed

    flags = {
        "real_tts_invoked_bad": _bad(ha.get("real_tts_invoked"), (False, None)),
        "navigation_action_bad": _bad(ha.get("navigation_action"), (None, "")),
        "downstream_invocation_count_bad": _bad(ha.get("downstream_invocation_count"), (0, None)),
    }
    if cap == "yolo":
        flags["runtime_invoked_bad"] = _bad(ha.get("runtime_invoked"), (False, None))
    if cap == "ocr":
        flags["semantic_interpretation_enabled_bad"] = _bad(ha.get("semantic_interpretation_enabled"), (False, None))
        flags["allows_execute_now_bad"] = _bad(ha.get("allows_execute_now"), (False, None))
    if cap == "voice":
        flags["provider_invoked_bad"] = _bad(ha.get("provider_invoked"), (False, None))
        flags["playback_invoked_bad"] = _bad(ha.get("playback_invoked"), (False, None))
    return flags


def _table_hard_audit(stage_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for r in stage_records:
        cap = r.get("capability")
        if not isinstance(cap, str):
            continue
        ha = r.get("hard_audit")
        if not isinstance(ha, dict):
            ha = {}
        flags = _hard_audit_anomaly_flags(ha, cap)
        any_bad = any(flags.values())
        rows.append(
            {
                "capability": cap,
                "request_id": r.get("request_id"),
                "stage_name": r.get("stage_name"),
                "any_anomaly": any_bad,
                "flags": flags,
                "hard_audit": ha,
                "source_root": r.get("source_root"),
                "source_refs": r.get("source_refs"),
            }
        )
    return rows


def _field_level_mapping_report(input_root: Path, source_root_index: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Best-effort field mapping report.
    - Lists what we can map (fields in unified stage record) and where it originated from.
    - Does not fabricate missing fields; missing/not_applicable are explicit.
    """
    core_shadow_root = source_root_index.get("core_shadow_root")
    voice_shadow_root = source_root_index.get("voice_shadow_root")
    core_shadow_root = str(core_shadow_root) if isinstance(core_shadow_root, str) else None
    voice_shadow_root = str(voice_shadow_root) if isinstance(voice_shadow_root, str) else None

    rows: List[Dict[str, Any]] = []

    def add(cap: str, source_file: str, source_field: str, unified_field: str, stage_name: str, status: str, notes: str) -> None:
        rows.append(
            {
                "capability": cap,
                "source_file": source_file,
                "source_field": source_field,
                "unified_field": unified_field,
                "stage_name": stage_name,
                "mapping_status": status,
                "notes": notes,
            }
        )

    # YOLO (Phase-002 chain stage fields)
    yolo_source = f"{core_shadow_root}/yolo_request_trace_chains.json" if core_shadow_root else "core_shadow:yolo_request_trace_chains.json"
    for stage in (
        "request_trace.stage.perception.yolo.input_frame",
        "request_trace.stage.perception.yolo.detection_result",
        "request_trace.stage.perception.yolo.observability_envelope",
    ):
        add("yolo", yolo_source, "fields.frame_id", "fields.frame_id", stage, "mapped", "from Phase-002 yolo stage fields")
        add("yolo", yolo_source, "fields.model_config_id", "fields.model_config_id", stage, "mapped", "from Phase-002 yolo stage fields")
        add("yolo", yolo_source, "fields.detection_count", "fields.detection_count", stage, "mapped", "from Phase-002 yolo stage fields")
        add("yolo", yolo_source, "(not present)", "fields.image_ref", stage, "missing", "Phase-002 YOLO shadow did not carry image_ref")
        add("yolo", yolo_source, "(not present)", "fields.confidence_summary", stage, "missing", "Phase-002 YOLO shadow may omit confidence_summary")
        add("yolo", yolo_source, "(not present)", "fields.bbox_summary", stage, "missing", "Phase-002 YOLO shadow may omit bbox_summary")
        add("yolo", yolo_source, "source_refs.trace_ref", "source_refs.trace_ref", stage, "mapped", "preserved local TRW ref")
        add("yolo", yolo_source, "source_refs.replay_ref", "source_refs.replay_ref", stage, "mapped", "preserved local TRW ref")
        add("yolo", yolo_source, "source_refs.whitebox_ref", "source_refs.whitebox_ref", stage, "mapped", "preserved local TRW ref")

    # OCR
    ocr_source = f"{core_shadow_root}/ocr_request_trace_chains.json" if core_shadow_root else "core_shadow:ocr_request_trace_chains.json"
    for stage in (
        "request_trace.stage.perception.ocr.source_policy_selection",
        "request_trace.stage.perception.ocr.raw_text_result",
        "request_trace.stage.perception.ocr.observability_envelope",
    ):
        add("ocr", ocr_source, "provider_selected", "provider_selected", stage, "mapped", "from Phase-002 OCR chain/stage fields")
        add("ocr", ocr_source, "source_policy_id", "source_policy_id", stage, "mapped", "from Phase-002 OCR chain/stage fields")
        add("ocr", ocr_source, "fields.raw_text_candidate_count", "fields.raw_text_candidate_count", stage, "mapped", "from OCR raw_outputs-derived count")
        add("ocr", ocr_source, "(not present)", "fields.raw_text_joined_length", stage, "missing", "not computed in Phase-002 adapter (shadow-only)")
        add("ocr", ocr_source, "(not present)", "fields.raw_text_segments_count", stage, "missing", "not computed in Phase-002 adapter (shadow-only)")
        add("ocr", ocr_source, "(not present)", "fields.reading_order_confidence", stage, "missing", "not available in Phase-002 adapter")
        add("ocr", ocr_source, "source_refs.trace_ref", "source_refs.trace_ref", stage, "mapped", "preserved local TRW ref")
        add("ocr", ocr_source, "source_refs.replay_ref", "source_refs.replay_ref", stage, "mapped", "preserved local TRW ref")
        add("ocr", ocr_source, "source_refs.whitebox_ref", "source_refs.whitebox_ref", stage, "mapped", "preserved local TRW ref")

    # Voice (Phase-005)
    voice_source = f"{voice_shadow_root}/voice_output_request_chains.json" if voice_shadow_root else "voice_shadow:voice_output_request_chains.json"
    for stage in (
        "request_trace.stage.voice_output.speakable_guard",
        "request_trace.stage.voice_output.speech_gate",
        "request_trace.stage.voice_output.expiry_check",
        "request_trace.stage.voice_output.cancellation_check",
        "request_trace.stage.voice_output.provider_health_check",
        "request_trace.stage.voice_output.final_governance_decision",
        "request_trace.stage.voice_output.audit_envelope",
    ):
        add("voice", voice_source, "stages[].key_fields.whitebox_extension", "fields.key_fields.whitebox_extension", stage, "mapped", "available in unified stage record fields.key_fields")
        add("voice", voice_source, "stages[].key_fields.audit_envelope_ref", "fields.key_fields.audit_envelope_ref", stage, "mapped", "voice chain key_fields")
        add("voice", voice_source, "stages[].key_fields.decision_ref", "fields.key_fields.decision_ref", stage, "mapped", "voice chain key_fields")
        add("voice", voice_source, "voice_output_extractor_shadow_trace.jsonl", "source_refs.trace_ref", stage, "derived", "attached at unified view level from voice root")
        add("voice", voice_source, "voice_output_extractor_shadow_replay.jsonl", "source_refs.replay_ref", stage, "derived", "attached at unified view level from voice root")
        add("voice", voice_source, "voice_output_extractor_shadow_whitebox.jsonl", "source_refs.whitebox_ref", stage, "derived", "attached at unified view level from voice root")

    return rows


def _build_md_report(summary: Dict[str, Any]) -> str:
    return (
        "# Core Capability Unified Export Report (v0)\n\n"
        "## Summary\n\n"
        "```json\n"
        + json.dumps(summary, ensure_ascii=False, indent=2)
        + "\n```\n\n"
        "## Notes\n\n"
        "- Offline/shadow only; no runtime invocation.\n"
        "- Field-level mapping report is best-effort and never fabricates missing fields.\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--output-root", default=None)
    args = ap.parse_args()

    input_root = Path(args.input_root)
    if not input_root.exists() or not input_root.is_dir():
        raise SystemExit(f"input root not readable: {args.input_root}")

    out_root = _mk_out_root(args.output_root)

    chain_index = _load_chain_index(input_root)
    stage_records = _collect_stage_records(input_root)
    source_root_index = _read_json(input_root / "core_capability_source_root_index.json") if (input_root / "core_capability_source_root_index.json").exists() else {}

    capability_table = _table_capability(chain_index if isinstance(chain_index, list) else [])
    stage_table = _table_stage(stage_records)
    hard_audit_table = _table_hard_audit(stage_records)
    missing_fields_table = _table_missing_fields(stage_records)
    mapping_report = _field_level_mapping_report(input_root, source_root_index if isinstance(source_root_index, dict) else {})

    summary = {
        "phase": "Phase-CoreCapability-TRW-Unified-004",
        "tool": "export_core_capability_unified_observability_view_v0.py",
        "input_root": str(input_root),
        "output_root": str(out_root),
        "counts": {
            "chain_index_count": len(chain_index) if isinstance(chain_index, list) else 0,
            "stage_record_count": len(stage_records),
            "capability_table_rows": len(capability_table),
            "stage_table_rows": len(stage_table),
            "hard_audit_table_rows": len(hard_audit_table),
            "missing_fields_table_rows": len(missing_fields_table),
            "field_level_mapping_rows": len(mapping_report),
        },
        "notes": [
            "offline/shadow export only",
            "does not claim cross-capability linkage",
        ],
    }

    _write_json(out_root / "core_capability_unified_export_summary.json", summary)
    _write_json(out_root / "core_capability_unified_capability_table.json", capability_table)
    _write_json(out_root / "core_capability_unified_stage_table.json", stage_table)
    _write_json(out_root / "core_capability_unified_hard_audit_table.json", hard_audit_table)
    _write_json(out_root / "core_capability_unified_missing_fields_table.json", missing_fields_table)
    _write_json(out_root / "core_capability_unified_field_level_mapping_report.json", mapping_report)

    (out_root / "core_capability_unified_export_report.md").write_text(_build_md_report(summary), encoding="utf-8")

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

