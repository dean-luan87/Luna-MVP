#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-004 — Run OCR input image quality gate v0 (Evaluation Tools).

Inputs:
- --dataset-root: dataset with manifest.jsonl (preferred)
- --images-dir: evaluate images in a directory (e.g. fixtures)

Outputs (under --output-root):
- ocr_input_quality_summary.json
- ocr_input_quality_image_matrix.jsonl
- ocr_input_quality_gate_counts.json
- ocr_input_quality_notes.md

Hard boundaries: evaluation-only; does NOT invoke OCR providers; no runtime/whitebox integration.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_input_image_quality_gate_v0 import (  # noqa: E402
    ImageQualityGateConfigV0,
    assess_ocr_input_image_quality_v0,
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


def _load_manifest_rows(dataset_root: Path) -> List[Dict[str, Any]]:
    p = dataset_root / "manifest.jsonl"
    if not p.is_file():
        raise SystemExit(f"ERROR: manifest.jsonl missing: {p}")
    rows: List[Dict[str, Any]] = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        rows.append(json.loads(ln))
    return rows


def _list_images(images_dir: Path) -> List[Path]:
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    out: List[Path] = []
    for p in sorted(images_dir.iterdir(), key=lambda x: x.name):
        if p.is_file() and p.suffix.lower() in exts and not p.name.startswith("."):
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--dataset-root", default="")
    ap.add_argument("--images-dir", default="")
    ap.add_argument("--label", default="input_set_v0")
    args = ap.parse_args()

    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    dataset_root = None
    images_dir = None
    if str(args.dataset_root).strip():
        dataset_root = _require_abs(args.dataset_root, "--dataset-root")
    if str(args.images_dir).strip():
        images_dir = _require_abs(args.images_dir, "--images-dir")

    if dataset_root is None and images_dir is None:
        raise SystemExit("ERROR: provide --dataset-root or --images-dir")

    cfg = ImageQualityGateConfigV0()
    matrix_path = out_root / "ocr_input_quality_image_matrix.jsonl"
    if matrix_path.exists():
        matrix_path.unlink()

    count = 0
    gate_counts: Dict[str, int] = {"GO": 0, "CONDITIONAL_GO": 0, "NO_GO": 0}
    scale_action_counts: Dict[str, int] = {}
    reasons_top: Dict[str, int] = {}

    if dataset_root is not None:
        rows = _load_manifest_rows(dataset_root)
        for r in rows:
            img_path = str(r.get("image_path") or "")
            sid = str(r.get("sample_id") or "")
            rep = assess_ocr_input_image_quality_v0(image_path=img_path, cfg=cfg)
            rep["sample_id"] = sid
            rep["category"] = r.get("category")
            rep["language"] = r.get("language")
            rep["dataset_ref"] = str(dataset_root)
            _append_jsonl(matrix_path, rep)
            count += 1
            gate = str(rep.get("image_quality_gate") or "NO_GO")
            gate_counts[gate] = int(gate_counts.get(gate, 0) + 1)
            sa = str(rep.get("scale_action") or "unknown")
            scale_action_counts[sa] = int(scale_action_counts.get(sa, 0) + 1)
            for reason in (rep.get("reason") or [])[:8]:
                reasons_top[str(reason)] = int(reasons_top.get(str(reason), 0) + 1)
    else:
        assert images_dir is not None
        imgs = _list_images(images_dir)
        for p in imgs:
            rep = assess_ocr_input_image_quality_v0(image_path=str(p), cfg=cfg)
            rep["sample_id"] = p.stem
            rep["dataset_ref"] = str(images_dir)
            _append_jsonl(matrix_path, rep)
            count += 1
            gate = str(rep.get("image_quality_gate") or "NO_GO")
            gate_counts[gate] = int(gate_counts.get(gate, 0) + 1)
            sa = str(rep.get("scale_action") or "unknown")
            scale_action_counts[sa] = int(scale_action_counts.get(sa, 0) + 1)
            for reason in (rep.get("reason") or [])[:8]:
                reasons_top[str(reason)] = int(reasons_top.get(str(reason), 0) + 1)

    # Verdict for the whole input set: NO_GO if any NO_GO; CONDITIONAL if any CONDITIONAL; else GO
    if gate_counts.get("NO_GO", 0) > 0:
        overall = "NO_GO"
    elif gate_counts.get("CONDITIONAL_GO", 0) > 0:
        overall = "CONDITIONAL_GO"
    else:
        overall = "GO"

    summary = {
        "phase": "Phase-EvaluationTools-OCR-004",
        "tool": "run_ocr_input_image_quality_gate_v0",
        "ts": _now_iso(),
        "label": str(args.label),
        "dataset_root": str(dataset_root) if dataset_root is not None else None,
        "images_dir": str(images_dir) if images_dir is not None else None,
        "output_root": str(out_root),
        "count": int(count),
        "overall_verdict": overall,
        "gate_counts": gate_counts,
        "scale_action_counts": scale_action_counts,
        "top_reasons": dict(sorted(reasons_top.items(), key=lambda kv: kv[1], reverse=True)[:20]),
        "hard_audit": {
            "ocr_provider_invoked": False,
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "tts_invoked": False,
            "qwen_invoked": False,
        },
    }

    _write_json(out_root / "ocr_input_quality_summary.json", summary)
    _write_json(out_root / "ocr_input_quality_gate_counts.json", {"gate_counts": gate_counts, "scale_action_counts": scale_action_counts})

    notes = "\n".join(
        [
            "# OCR input image quality gate v0 (Evaluation Tools)",
            "",
            f"- **label:** `{summary['label']}`",
            f"- **count:** `{summary['count']}`",
            f"- **overall_verdict:** `{summary['overall_verdict']}`",
            "",
            "## Boundary",
            "",
            "- Evaluation-only; no runtime/mainline/whitebox integration.",
            "- No OCR provider invoked.",
            "",
        ]
    )
    (out_root / "ocr_input_quality_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "overall_verdict": overall, "count": count}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

