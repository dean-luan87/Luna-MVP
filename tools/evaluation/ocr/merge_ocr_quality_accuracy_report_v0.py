#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-005 — OCR Quality × Recognition Accuracy Correlation Report v0.

Merge-only:
- Does NOT invoke OCR providers
- Does NOT modify ground truth
- Evaluation Tools only; no runtime/whitebox integration; no mainline side effects
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


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


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        rows.append(json.loads(ln))
    return rows


def _pearson_corr(xs: List[float], ys: List[float]) -> Optional[float]:
    if len(xs) != len(ys) or len(xs) < 3:
        return None
    n = float(len(xs))
    mx = sum(xs) / n
    my = sum(ys) / n
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 1e-12 or vy <= 1e-12:
        return None
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(len(xs)))
    return float(cov / math.sqrt(vx * vy))


def _bucket(*, gate: str, cer: float, recall: Optional[float], pred_empty: bool, garbled_score: float) -> str:
    good_input = (gate == "GO")
    bad_input = (gate in ("CONDITIONAL_GO", "NO_GO"))
    bad_ocr = pred_empty or (cer >= 0.35) or (garbled_score >= 0.35) or (recall is not None and recall < 0.30)
    good_ocr = not bad_ocr
    if good_input and good_ocr:
        return "good_input_good_ocr"
    if good_input and bad_ocr:
        return "good_input_bad_ocr"
    if bad_input and bad_ocr:
        return "bad_input_bad_ocr"
    if bad_input and good_ocr:
        return "bad_input_good_ocr"
    return "review_required"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--accuracy-root", required=True)
    ap.add_argument("--quality-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--expected-count", type=int, default=0)
    args = ap.parse_args()

    acc_root = _require_abs(args.accuracy_root, "--accuracy-root")
    qual_root = _require_abs(args.quality_root, "--quality-root")
    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    acc_matrix_path = acc_root / "rapidocr_chinese_sample_eval_matrix.json"
    qual_matrix_path = qual_root / "ocr_input_quality_image_matrix.jsonl"
    if not acc_matrix_path.is_file():
        raise SystemExit(f"ERROR: missing accuracy matrix: {acc_matrix_path}")
    if not qual_matrix_path.is_file():
        raise SystemExit(f"ERROR: missing quality matrix: {qual_matrix_path}")

    acc_rows: List[Dict[str, Any]] = _load_json(acc_matrix_path)
    qual_rows: List[Dict[str, Any]] = _load_jsonl(qual_matrix_path)

    acc_by_id = {str(r.get("sample_id") or ""): r for r in acc_rows if str(r.get("sample_id") or "")}
    qual_by_id = {str(r.get("sample_id") or ""): r for r in qual_rows if str(r.get("sample_id") or "")}

    all_ids = sorted(set(acc_by_id.keys()) | set(qual_by_id.keys()))
    aligned: List[Dict[str, Any]] = []
    missing_acc: List[str] = []
    missing_qual: List[str] = []

    trace = out_root / "ocr_quality_accuracy_trace.jsonl"
    replay = out_root / "ocr_quality_accuracy_replay.jsonl"
    if trace.exists():
        trace.unlink()
    if replay.exists():
        replay.unlink()

    _append_jsonl(trace, {"type": "ocr_quality_accuracy_merge_trace_v0", "ts": _now_iso(), "event": "start", "count_ids": len(all_ids)})

    for sid in all_ids:
        a = acc_by_id.get(sid)
        q = qual_by_id.get(sid)
        if a is None:
            missing_acc.append(sid)
            continue
        if q is None:
            missing_qual.append(sid)
            continue

        cer = float(a.get("cer") or 0.0)
        recall = a.get("chinese_char_recall")
        recall_f = float(recall) if recall is not None else None
        pred_empty = bool(a.get("pred_empty"))
        garbled_score = float(a.get("garbled_score") or 0.0)
        gate = str(q.get("image_quality_gate") or "NO_GO")
        b = _bucket(gate=gate, cer=cer, recall=recall_f, pred_empty=pred_empty, garbled_score=garbled_score)

        row = {
            "sample_id": sid,
            # accuracy fields (subset)
            "provider": a.get("provider"),
            "cer": cer,
            "chinese_char_recall": recall_f,
            "pred_empty": pred_empty,
            "garbled_score": garbled_score,
            "case": a.get("case"),
            "provider_fail": bool(a.get("provider_fail")),
            # quality fields (subset)
            "image_quality_gate": gate,
            "scale_action": q.get("scale_action"),
            "blur_score": q.get("blur_score"),
            "contrast_score": q.get("contrast_score"),
            "brightness_mean": q.get("brightness_mean"),
            "brightness_status": q.get("brightness_status"),
            "text_area_ratio": q.get("text_area_ratio"),
            "text_scale_status": q.get("text_scale_status"),
            "skew_angle_deg": q.get("skew_angle_deg"),
            "recommended_preprocess": q.get("recommended_preprocess") or [],
            "quality_reasons": q.get("reason") or [],
            # bucket
            "quality_bucket": b,
        }
        aligned.append(row)

    # Failure classification: provider vs input
    provider_failure = [r for r in aligned if bool(r.get("provider_fail"))]
    input_quality_failure = [r for r in aligned if str(r.get("image_quality_gate")) == "NO_GO"]
    input_quality_risk = [r for r in aligned if str(r.get("image_quality_gate")) == "CONDITIONAL_GO"]
    good_input_bad_ocr = [r for r in aligned if r.get("quality_bucket") == "good_input_bad_ocr"]
    bad_input_good_ocr = [r for r in aligned if r.get("quality_bucket") == "bad_input_good_ocr"]

    # Correlation report (Pearson; best-effort)
    xs_blur = [float(r["blur_score"]) for r in aligned if r.get("blur_score") is not None]
    ys_cer_for_blur = [float(r["cer"]) for r in aligned if r.get("blur_score") is not None]
    xs_contrast = [float(r["contrast_score"]) for r in aligned if r.get("contrast_score") is not None]
    ys_cer_for_contrast = [float(r["cer"]) for r in aligned if r.get("contrast_score") is not None]
    xs_text_ratio = [float(r["text_area_ratio"]) for r in aligned if r.get("text_area_ratio") is not None]
    ys_cer_for_text_ratio = [float(r["cer"]) for r in aligned if r.get("text_area_ratio") is not None]

    corr = {
        "pearson": {
            "blur_score_vs_cer": _pearson_corr(xs_blur, ys_cer_for_blur),
            "contrast_score_vs_cer": _pearson_corr(xs_contrast, ys_cer_for_contrast),
            "text_area_ratio_vs_cer": _pearson_corr(xs_text_ratio, ys_cer_for_text_ratio),
        },
        "notes": "Correlation is best-effort; small N / low variance may yield None.",
    }

    bucket_counts: Dict[str, int] = {}
    for r in aligned:
        b = str(r.get("quality_bucket") or "unknown")
        bucket_counts[b] = int(bucket_counts.get(b, 0) + 1)

    bucket_report = {"count": len(aligned), "bucket_counts": bucket_counts}
    provider_vs_input = {
        "count": len(aligned),
        "provider_failure_count": len(provider_failure),
        "input_quality_no_go_count": len(input_quality_failure),
        "input_quality_conditional_count": len(input_quality_risk),
        "good_input_bad_ocr_count": len(good_input_bad_ocr),
        "bad_input_good_ocr_count": len(bad_input_good_ocr),
        "notes": "provider_fail comes from OCR-003; input gate from OCR-004. No new OCR executed.",
    }

    # Write outputs
    _write_json(out_root / "ocr_quality_accuracy_merge_summary.json", {
        "phase": "Phase-EvaluationTools-OCR-005",
        "tool": "merge_ocr_quality_accuracy_report_v0",
        "ts": _now_iso(),
        "accuracy_root": str(acc_root),
        "quality_root": str(qual_root),
        "output_root": str(out_root),
        "expected_count": int(args.expected_count),
        "aligned_count": len(aligned),
        "missing_accuracy_count": len(missing_acc),
        "missing_quality_count": len(missing_qual),
        "bucket_counts": bucket_counts,
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
    })
    _write_json(out_root / "ocr_quality_accuracy_sample_matrix.json", aligned)
    _write_json(out_root / "ocr_quality_bucket_report.json", bucket_report)
    _write_json(out_root / "ocr_quality_metric_correlation_report.json", corr)
    _write_json(out_root / "ocr_provider_vs_input_failure_report.json", provider_vs_input)
    _write_json(out_root / "ocr_quality_accuracy_missing_alignment.json", {
        "missing_accuracy_sample_ids": missing_acc[:200],
        "missing_quality_sample_ids": missing_qual[:200],
    })

    _append_jsonl(trace, {"type": "ocr_quality_accuracy_merge_trace_v0", "ts": _now_iso(), "event": "done", "aligned_count": len(aligned)})
    _append_jsonl(replay, {"type": "ocr_quality_accuracy_merge_replay_v0", "ts": _now_iso(), "hint": "Open bucket/correlation/provider_vs_input reports."})

    notes = "\n".join(
        [
            "# OCR quality × accuracy merge v0 (Evaluation Tools)",
            "",
            f"- **accuracy_root:** `{str(acc_root)}`",
            f"- **quality_root:** `{str(qual_root)}`",
            f"- **output_root:** `{str(out_root)}`",
            f"- **aligned_count:** `{len(aligned)}`",
            "",
            "## Boundary",
            "",
            "- Merge-only; no OCR provider invoked.",
            "- No runtime/whitebox integration; no mainline side effects.",
            "",
        ]
    )
    (out_root / "merge_notes.md").write_text(notes + "\n", encoding="utf-8")

    # Overall verdict for the merge
    if int(args.expected_count) > 0 and len(aligned) != int(args.expected_count):
        verdict = "CONDITIONAL_GO"
        reason = "count_mismatch"
    elif missing_acc or missing_qual:
        verdict = "CONDITIONAL_GO"
        reason = "missing_alignment"
    else:
        verdict = "GO"
        reason = None

    print(json.dumps({"ok": True, "output_root": str(out_root), "verdict": verdict, "reason": reason, "aligned_count": len(aligned)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

