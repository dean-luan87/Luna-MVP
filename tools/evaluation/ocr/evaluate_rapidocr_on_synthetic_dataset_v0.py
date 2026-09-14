#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-001 — Evaluate RapidOCR on synthetic dataset v0 (Evaluation Tools).

Hard boundaries:
- Evaluation only; must NOT integrate into runtime/mainline/whitebox.
- No semantic interpretation / MidPlatform / SceneDelta / WorldContext.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0  # noqa: E402
from capabilities.evaluation.ocr.ocr_eval_metrics_v0 import (  # noqa: E402
    classify_ocr_eval_result_v0,
    compute_cer_v0,
    compute_chinese_char_recall_v0,
    compute_garbled_score_v0,
    normalize_ocr_text_for_eval_v0,
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


def _load_manifest(dataset_root: Path) -> List[Dict[str, Any]]:
    p = dataset_root / "manifest.jsonl"
    rows: List[Dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--limit", type=int, default=0, help="0 = no limit")
    args = ap.parse_args()

    dataset_root = _require_abs(args.dataset_root, "--dataset-root")
    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    rows = _load_manifest(dataset_root)
    if int(args.limit) > 0:
        rows = rows[: int(args.limit)]

    adapter = RapidOCRAdapterV0()
    ok, err = adapter.is_available()
    if not ok:
        raise SystemExit(f"ERROR: RapidOCR unavailable: {err}")

    per: List[Dict[str, Any]] = []
    t0 = time.perf_counter()

    for r in rows:
        sid = str(r.get("sample_id") or "")
        img = str(r.get("image_path") or "")
        truth = str(r.get("ground_truth_text") or "")
        cat = str(r.get("category") or "unknown")
        lang = str(r.get("language") or "unknown")

        o = adapter.recognize_image(image_path=img, frame_id=sid, timestamp_ms=int(time.time() * 1000))
        pred = str(o.get("raw_text_joined") or "")

        cer_d = compute_cer_v0(pred, truth)
        zh_d = compute_chinese_char_recall_v0(pred, truth)
        gar_d = compute_garbled_score_v0(pred)
        raw_empty = not bool(normalize_ocr_text_for_eval_v0(pred))
        q = classify_ocr_eval_result_v0(cer=float(cer_d["cer"]), garbled_score=float(gar_d["garbled_score"]), raw_text_empty=raw_empty)

        per.append(
            {
                "sample_id": sid,
                "category": cat,
                "language": lang,
                "image_path": img,
                "truth_text": truth,
                "pred_text": pred,
                **cer_d,
                **zh_d,
                **gar_d,
                "quality_class": q,
                "provider": "rapidocr_onnxruntime_v0",
            }
        )

    elapsed = (time.perf_counter() - t0) * 1000.0

    # Summaries
    cat_map: Dict[str, List[float]] = {}
    zh_rec: List[float] = []
    gar: List[float] = []
    empty_cnt = 0
    fail_ids: List[str] = []
    for r in per:
        cat_map.setdefault(r["category"], []).append(float(r["cer"]))
        if r.get("chinese_char_recall") is not None:
            zh_rec.append(float(r["chinese_char_recall"]))
        gar.append(float(r["garbled_score"]))
        if not normalize_ocr_text_for_eval_v0(str(r.get("pred_text") or "")):
            empty_cnt += 1
        if r.get("quality_class") in ("fail", "review_pending"):
            fail_ids.append(str(r.get("sample_id")))

    category_cer_summary = {k: {"avg_cer": sum(v) / max(1, len(v)), "count": len(v)} for k, v in cat_map.items()}
    chinese_recall_summary = {
        "count": len(zh_rec),
        "avg_recall": (sum(zh_rec) / max(1, len(zh_rec))) if zh_rec else None,
        "min_recall": min(zh_rec) if zh_rec else None,
    }
    garbled_report = {"avg_garbled_score": sum(gar) / max(1, len(gar)), "empty_pred_count": empty_cnt}

    summary = {
        "phase": "Phase-EvaluationTools-OCR-001",
        "tool": "evaluate_rapidocr_on_synthetic_dataset_v0",
        "ts": _now_iso(),
        "dataset_root": str(dataset_root),
        "output_root": str(out_root),
        "provider": "rapidocr_onnxruntime_v0",
        "count": len(per),
        "avg_cer": sum(float(r["cer"]) for r in per) / max(1, len(per)),
        "elapsed_ms": round(elapsed, 3),
        "hard_audit": {
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "runtime_integration": False,
        },
    }

    _write_json(out_root / "synthetic_eval_summary.json", summary)
    _write_json(out_root / "synthetic_sample_eval_matrix.json", per)
    _write_json(out_root / "category_cer_summary.json", category_cer_summary)
    _write_json(out_root / "chinese_recall_summary.json", chinese_recall_summary)
    _write_json(out_root / "garbled_report.json", garbled_report)
    _write_json(out_root / "failure_cases.json", {"count": len(fail_ids), "sample_ids": fail_ids[:200]})

    # Eval-local trace/replay/whitebox (NOT runtime)
    _append_jsonl(out_root / "rapidocr_synthetic_trace.jsonl", {"type": "rapidocr_synth_trace_v0", "ts": _now_iso(), "count": len(per)})
    _append_jsonl(out_root / "rapidocr_synthetic_replay.jsonl", {"type": "rapidocr_synth_replay_v0", "ts": _now_iso(), "count": len(per)})
    _append_jsonl(out_root / "rapidocr_synthetic_whitebox.jsonl", {"type": "rapidocr_synth_whitebox_v0", "ts": _now_iso(), "hard_audit": summary["hard_audit"]})

    notes = "\n".join(
        [
            "# RapidOCR synthetic eval v0 (Evaluation Tools)",
            "",
            f"- **dataset_root:** `{summary['dataset_root']}`",
            f"- **output_root:** `{summary['output_root']}`",
            f"- **provider:** `{summary['provider']}`",
            f"- **count:** `{summary['count']}`",
            f"- **avg_cer:** `{summary['avg_cer']:.4f}`",
            "",
            "## Boundary",
            "",
            "- Evaluation-only; no runtime/mainline/whitebox integration.",
            "- No semantic interpretation / MidPlatform / SceneDelta / WorldContext.",
            "",
        ]
    )
    (out_root / "synthetic_eval_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "count": len(per), "avg_cer": summary["avg_cer"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

