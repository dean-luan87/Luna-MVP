#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-012-Improve-B — Layout/Symbol/Reading-Order governance eval v0.

For each sample image:
- 010 approval gate (freeze input)
- 011 controlled provider invocation (RapidOCR mainline)
- build OcrLayoutGovernanceEvidenceV0 (structure only; no semantic)

Absolute paths only.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.guarded_trial.ocr_layout_symbol_governance_v0 import (  # noqa: E402
    build_ocr_layout_governance_evidence_v0,
)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _run(cmd: List[str]) -> int:
    import subprocess

    return subprocess.run(cmd, check=False).returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-dir", required=True)
    ap.add_argument("--sample-regex", required=True)
    ap.add_argument("--static-config-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    sample_dir = _require_abs(args.sample_dir, "--sample-dir")
    static_root = _require_abs(args.static_config_root, "--static-config-root")
    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    rx = re.compile(str(args.sample_regex), re.IGNORECASE)
    samples = [p for p in sorted(sample_dir.iterdir(), key=lambda x: x.name) if p.is_file() and rx.fullmatch(p.name)]

    per_dir = out_root / "per_sample"
    per_dir.mkdir(parents=True, exist_ok=True)

    py = sys.executable
    tool_prepare = str(Path(REPO_ROOT) / "tools" / "prepare_ocr_stage2_provider_approval_gate_v0.py")
    tool_run = str(Path(REPO_ROOT) / "tools" / "run_ocr_stage2_controlled_provider_trial_v0.py")

    sample_matrix: List[Dict[str, Any]] = []
    all_symbols: Dict[str, Any] = {}
    all_glyphs: Dict[str, Any] = {}
    all_groups: Dict[str, Any] = {}
    all_orders: Dict[str, Any] = {}
    grouped_text_report: Dict[str, Any] = {}
    symbol_noise_report: Dict[str, Any] = {}

    for img in samples:
        sid = img.stem
        sroot = per_dir / sid
        sroot.mkdir(parents=True, exist_ok=True)
        r010 = sroot / "approval_010"
        r011 = sroot / "trial_011"
        r010.mkdir(parents=True, exist_ok=True)
        r011.mkdir(parents=True, exist_ok=True)

        rc0 = _run(
            [
                py,
                tool_prepare,
                "--static-config-root",
                str(static_root),
                "--input-image",
                str(img.resolve()),
                "--output-root",
                str(r010),
            ]
        )
        rc1 = _run([py, tool_run, "--approval-root", str(r010), "--output-root", str(r011)])

        provider_sel = {}
        payload = {}
        try:
            provider_sel = json.loads((r011 / "ocr_stage2_provider_selection.json").read_text(encoding="utf-8"))
        except Exception:
            provider_sel = {}
        try:
            payload = json.loads((r011 / "ocr_stage2_provider_invocation_result.json").read_text(encoding="utf-8"))
        except Exception:
            payload = {}

        provider = str(provider_sel.get("provider_selected") or "")
        evidence = build_ocr_layout_governance_evidence_v0(
            image_id=sid,
            provider=provider,
            raw_ocr_payload=payload,
            source_image_path=str(img.resolve()),
        )
        _write_json(sroot / "ocr_stage2_layout_governance_evidence.json", evidence)

        # Aggregate
        all_symbols[sid] = evidence.get("visual_symbol_candidates")
        all_glyphs[sid] = evidence.get("visual_glyph_candidates")
        all_groups[sid] = evidence.get("layout_groups")
        all_orders[sid] = evidence.get("reading_order_candidates")
        grouped_text_report[sid] = evidence.get("raw_text_joined_by_group")
        symbol_noise_report[sid] = evidence.get("symbol_noise_filter_report")

        sample_matrix.append(
            {
                "sample_id": sid,
                "image_path": str(img.resolve()),
                "provider_selected": provider,
                "prepare_rc": rc0,
                "trial_rc": rc1,
                "layout_groups": len(evidence.get("layout_groups") or []),
                "visual_symbols": len(evidence.get("visual_symbol_candidates") or []),
                "visual_glyphs": len(evidence.get("visual_glyph_candidates") or []),
                "reading_order_uncertain": (evidence.get("uncertainty") or {}).get("reading_order_uncertain"),
            }
        )

    # Write outputs
    summary = {
        "phase": "Phase-Mainline-GuardedTrial-012-Improve-B",
        "ts": _now_iso(),
        "sample_dir": str(sample_dir),
        "sample_regex": str(args.sample_regex),
        "static_config_root": str(static_root),
        "output_root": str(out_root),
        "sample_count": len(samples),
        "provider": "rapidocr_mainline_v0",
        "hard_audit": {
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "downstream_invocation_count": 0,
        },
    }
    _write_json(out_root / "ocr_stage2_layout_symbol_summary.json", summary)
    _write_json(out_root / "ocr_stage2_layout_symbol_sample_matrix.json", sample_matrix)
    _write_json(out_root / "ocr_stage2_visual_symbol_candidates.json", all_symbols)
    _write_json(out_root / "ocr_stage2_visual_glyph_candidates.json", all_glyphs)
    _write_json(out_root / "ocr_stage2_layout_groups.json", all_groups)
    _write_json(out_root / "ocr_stage2_reading_order_candidates.json", all_orders)
    _write_json(out_root / "ocr_stage2_grouped_raw_text_report.json", grouped_text_report)
    _write_json(out_root / "ocr_stage2_symbol_noise_filter_report.json", symbol_noise_report)

    # Minimal TRW for this tool
    _append_jsonl(out_root / "ocr_stage2_layout_symbol_trace.jsonl", {"type": "layout_symbol_trace_v0", "ts": _now_iso(), "count": len(samples)})
    _append_jsonl(out_root / "ocr_stage2_layout_symbol_replay.jsonl", {"type": "layout_symbol_replay_v0", "ts": _now_iso(), "count": len(samples)})
    _append_jsonl(
        out_root / "ocr_stage2_layout_symbol_whitebox.jsonl",
        {
            "type": "layout_symbol_whitebox_v0",
            "ts": _now_iso(),
            "count": len(samples),
            "hard_audit": summary["hard_audit"],
        },
    )

    notes = "\n".join(
        [
            "# OCR Stage-2 Layout/Symbol Governance Eval v0 (012-Improve-B)",
            "",
            f"- **sample_dir:** `{summary['sample_dir']}`",
            f"- **sample_regex:** `{summary['sample_regex']}`",
            f"- **output_root:** `{summary['output_root']}`",
            f"- **sample_count:** `{summary['sample_count']}`",
            "",
            "## Scope",
            "",
            "- No semantic interpretation; no MidPlatform/SceneDelta/WorldContext.",
            "- Evidence-only governance built around OCR raw candidates (bbox/conf/text).",
            "",
        ]
    )
    (out_root / "layout_symbol_eval_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "sample_count": len(samples)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

