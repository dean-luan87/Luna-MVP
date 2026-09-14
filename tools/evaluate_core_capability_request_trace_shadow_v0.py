# -*- coding: utf-8 -*-
"""
Phase-CoreCapability-TRW-Unified-002
Evaluate YOLO/OCR RequestTrace Shadow Adapter v0.

This tool is offline-only: it reads pre-existing local TRW/benchmark outputs
and emits unified RequestTrace-style shadow chains + shadow trace/replay/whitebox.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from capabilities.core_trw.ocr_request_trace_shadow_adapter_v0 import (  # noqa: E402
    run_ocr_request_trace_shadow_adapter_v0,
)
from capabilities.core_trw.yolo_request_trace_shadow_adapter_v0 import (  # noqa: E402
    run_yolo_request_trace_shadow_adapter_v0,
)


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _flatten_stage_records(chains: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for ch in chains:
        stages = ch.get("stages")
        if isinstance(stages, list):
            for st in stages:
                if isinstance(st, dict):
                    out.append(st)
    return out


def _build_stage_mapping_report(yolo_chains: List[Dict[str, Any]], ocr_chains: List[Dict[str, Any]]) -> Dict[str, Any]:
    def _summarize(chains: List[Dict[str, Any]]) -> Dict[str, Any]:
        stage_names = {}
        for st in _flatten_stage_records(chains):
            n = st.get("stage_name")
            if isinstance(n, str):
                stage_names[n] = stage_names.get(n, 0) + 1
        return {"stage_counts": stage_names, "unique_stage_count": len(stage_names)}

    return {
        "stage_namespace_expected": "core_capability_request_trace_v0",
        "yolo": _summarize(yolo_chains),
        "ocr": _summarize(ocr_chains),
        "notes": [
            "mapping report is structural (stage presence/counts)",
            "field-level mapping details live in adapter code + missing field report",
        ],
    }


def _build_missing_field_report(yolo_chains: List[Dict[str, Any]], ocr_chains: List[Dict[str, Any]]) -> Dict[str, Any]:
    def _summarize_missing(chains: List[Dict[str, Any]]) -> Dict[str, Any]:
        missing_counts: Dict[str, int] = {}
        missing_source_refs_counts: Dict[str, int] = {}
        for st in _flatten_stage_records(chains):
            mf = st.get("missing_fields")
            if isinstance(mf, list):
                for x in mf:
                    if isinstance(x, str):
                        missing_counts[x] = missing_counts.get(x, 0) + 1
            srefs = st.get("source_refs")
            if isinstance(srefs, dict):
                for k, v in srefs.items():
                    if v in (None, "", False):
                        missing_source_refs_counts[k] = missing_source_refs_counts.get(k, 0) + 1
        return {
            "missing_fields_counts": missing_counts,
            "missing_source_refs_counts": missing_source_refs_counts,
        }

    return {"yolo": _summarize_missing(yolo_chains), "ocr": _summarize_missing(ocr_chains)}


def _build_shadow_jsonl(kind: str, stage_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Minimal JSONL payloads; still extractor-friendly and strictly shadow-only.
    rows: List[Dict[str, Any]] = []
    for st in stage_records:
        rows.append(
            {
                "kind": kind,
                "stage_namespace": st.get("stage_namespace"),
                "stage_name": st.get("stage_name"),
                "stage_order": st.get("stage_order"),
                "request_id": st.get("request_id"),
                "trace_id": st.get("trace_id"),
                "session_id": st.get("session_id"),
                "source_run_id": st.get("source_run_id"),
                "shadow_only": True,
                "hard_audit": st.get("hard_audit"),
                "source_refs": st.get("source_refs"),
                "fields": st.get("fields"),
            }
        )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yolo-root", required=True)
    ap.add_argument("--ocr-root", required=True)
    ap.add_argument("--output-root", default=None)
    args = ap.parse_args()

    out_root = (
        Path(args.output_root)
        if args.output_root
        else (REPO_ROOT / "logs" / f"core_capability_request_trace_shadow_002_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    )
    out_root.mkdir(parents=True, exist_ok=True)

    yolo = run_yolo_request_trace_shadow_adapter_v0(args.yolo_root)
    ocr = run_ocr_request_trace_shadow_adapter_v0(args.ocr_root)

    yolo_chains = yolo.get("chains") if isinstance(yolo.get("chains"), list) else []
    ocr_chains = ocr.get("chains") if isinstance(ocr.get("chains"), list) else []

    stage_records = _flatten_stage_records(yolo_chains) + _flatten_stage_records(ocr_chains)

    summary = {
        "phase": "Phase-CoreCapability-TRW-Unified-002",
        "mode": "offline_shadow_only",
        "inputs": {"yolo_root": args.yolo_root, "ocr_root": args.ocr_root},
        "outputs": {
            "yolo_chain_count": len(yolo_chains),
            "ocr_chain_count": len(ocr_chains),
            "stage_record_count": len(stage_records),
        },
        "hard_audit_invariants": {
            "no_runtime": True,
            "no_navigation_action": True,
            "no_real_tts": True,
            "no_downstream_invocation": True,
        },
        "env_snapshot": {
            "pwd": os.getcwd(),
        },
    }

    mapping_report = _build_stage_mapping_report(yolo_chains, ocr_chains)
    missing_report = _build_missing_field_report(yolo_chains, ocr_chains)

    _write_json(out_root / "core_capability_request_trace_shadow_summary.json", summary)
    _write_json(out_root / "yolo_request_trace_chains.json", yolo_chains)
    _write_json(out_root / "ocr_request_trace_chains.json", ocr_chains)
    _write_json(out_root / "core_capability_stage_mapping_report.json", mapping_report)
    _write_json(out_root / "core_capability_missing_field_report.json", missing_report)

    _write_jsonl(out_root / "core_capability_shadow_trace.jsonl", _build_shadow_jsonl("trace", stage_records))
    _write_jsonl(out_root / "core_capability_shadow_replay.jsonl", _build_shadow_jsonl("replay", stage_records))
    _write_jsonl(out_root / "core_capability_shadow_whitebox.jsonl", _build_shadow_jsonl("whitebox", stage_records))

    (out_root / "evaluation_notes.md").write_text(
        "\n".join(
            [
                "# Core Capability RequestTrace Shadow Evaluation Notes (v0)",
                "",
                "- This run is offline/shadow only.",
                "- It maps YOLO/OCR local artifacts into unified RequestTrace stage records.",
                "- Missing trace_id/session_id are explicit; never fabricated.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

