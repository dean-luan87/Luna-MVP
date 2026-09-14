#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-003 — RapidOCR Chinese Quality Gate Evaluation v0 (Evaluation Tools).

Hard boundaries:
- Evaluation-only; must NOT integrate into runtime/mainline/whitebox.
- Must NOT mutate ground truth.
- No MidPlatform/SceneDelta/WorldContext/Qwen/TTS/navigation actions.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0  # noqa: E402
from capabilities.evaluation.ocr.ocr_eval_metrics_v0 import (  # noqa: E402
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
    if not p.is_file():
        raise SystemExit(f"ERROR: manifest missing: {p}")
    rows: List[Dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def _classify_case(
    *,
    provider_fail: bool,
    visible_cjk_passed: bool,
    pred_empty: bool,
    recall: Optional[float],
    garbled_score: float,
) -> str:
    if provider_fail:
        return "provider_fail"
    if visible_cjk_passed and pred_empty:
        return "font_visible_but_ocr_empty"
    if recall is not None and recall < 0.30:
        return "low_recall"
    if garbled_score >= 0.35:
        return "garbled_output"
    return "acceptable_output"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--cross-validation-root", required=False, default="")
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    dataset_root = _require_abs(args.dataset_root, "--dataset-root")
    cross_root = Path(args.cross_validation_root).expanduser()
    if str(args.cross_validation_root or "").strip():
        if not cross_root.is_absolute():
            raise SystemExit(f"ERROR: --cross-validation-root must be absolute, got: {args.cross_validation_root}")
        cross_root = cross_root.resolve()
    else:
        cross_root = Path()

    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    rows = _load_manifest(dataset_root)
    adapter = RapidOCRAdapterV0()
    ok, err = adapter.is_available()
    if not ok:
        raise SystemExit(f"ERROR: RapidOCR unavailable: {err}")

    t0 = time.perf_counter()
    per: List[Dict[str, Any]] = []
    failure_cases: List[Dict[str, Any]] = []

    trace_path = out_root / "rapidocr_chinese_eval_trace.jsonl"
    replay_path = out_root / "rapidocr_chinese_eval_replay.jsonl"
    wb_path = out_root / "rapidocr_chinese_eval_whitebox.jsonl"

    _append_jsonl(
        trace_path,
        {
            "type": "rapidocr_chinese_eval_trace_v0",
            "ts": _now_iso(),
            "event": "start",
            "dataset_root": str(dataset_root),
            "count": len(rows),
        },
    )

    for r in rows:
        sid = str(r.get("sample_id") or "")
        img = str(r.get("image_path") or "")
        truth = str(r.get("ground_truth_text") or "")
        cat = str(r.get("category") or "unknown")
        lang = str(r.get("language") or "unknown")
        visible_cjk_passed = bool(r.get("visible_cjk_passed") is True)
        tofu_suspected = bool(r.get("tofu_suspected") is True)
        font_path = str(r.get("font_path") or "")

        env = adapter.recognize_image(image_path=img, frame_id=sid, timestamp_ms=int(time.time() * 1000))
        provider_fail = bool(env.get("provider_status") in ("not_available", "failed")) or bool(env.get("hard_blockers"))
        pred = str(env.get("raw_text_joined") or "")
        pred_norm = normalize_ocr_text_for_eval_v0(pred)
        pred_empty = not bool(pred_norm)

        cer_d = compute_cer_v0(pred, truth)
        zh_d = compute_chinese_char_recall_v0(pred, truth)
        gar_d = compute_garbled_score_v0(pred)

        recall = zh_d.get("chinese_char_recall")
        recall_f = float(recall) if recall is not None else None
        garbled_score = float(gar_d.get("garbled_score") or 0.0)

        case = _classify_case(
            provider_fail=provider_fail,
            visible_cjk_passed=visible_cjk_passed,
            pred_empty=pred_empty,
            recall=recall_f,
            garbled_score=garbled_score,
        )

        row = {
            "sample_id": sid,
            "category": cat,
            "language": lang,
            "image_path": img,
            "font_path": font_path,
            "visible_cjk_passed": visible_cjk_passed,
            "tofu_suspected": tofu_suspected,
            "truth_text": truth,
            "pred_text": pred,
            "pred_empty": pred_empty,
            "provider": "rapidocr_onnxruntime_v0",
            "provider_fail": provider_fail,
            "hard_blockers": env.get("hard_blockers") or [],
            "soft_followups": env.get("soft_followups") or [],
            **cer_d,
            **zh_d,
            **gar_d,
            "case": case,
        }
        per.append(row)

        if case != "acceptable_output":
            failure_cases.append(
                {
                    "sample_id": sid,
                    "case": case,
                    "category": cat,
                    "image_path": img,
                    "truth_text": truth,
                    "pred_text": pred_norm[:800],
                    "cer": float(cer_d["cer"]),
                    "chinese_char_recall": recall_f,
                    "garbled_score": garbled_score,
                }
            )

        _append_jsonl(
            trace_path,
            {
                "type": "rapidocr_chinese_eval_trace_v0",
                "ts": _now_iso(),
                "event": "sample_done",
                "sample_id": sid,
                "case": case,
                "pred_empty": pred_empty,
                "cer": float(cer_d["cer"]),
                "chinese_char_recall": recall_f,
            },
        )

    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    # Summaries
    cers = [float(r["cer"]) for r in per]
    empty_cnt = sum(1 for r in per if bool(r.get("pred_empty")))
    gar = [float(r.get("garbled_score") or 0.0) for r in per]
    zh_rec = [float(r["chinese_char_recall"]) for r in per if r.get("chinese_char_recall") is not None]

    cer_summary = {
        "count": len(per),
        "avg_cer": (sum(cers) / max(1, len(cers))) if cers else None,
        "min_cer": min(cers) if cers else None,
        "max_cer": max(cers) if cers else None,
    }
    recall_summary = {
        "count": len(zh_rec),
        "avg_chinese_recall": (sum(zh_rec) / max(1, len(zh_rec))) if zh_rec else None,
        "min_chinese_recall": min(zh_rec) if zh_rec else None,
    }
    empty_report = {"count": len(per), "empty_output_count": int(empty_cnt), "empty_output_rate": float(empty_cnt) / float(max(1, len(per)))}
    garbled_report = {"count": len(per), "avg_garbled_score": (sum(gar) / max(1, len(gar))) if gar else None}

    case_counts: Dict[str, int] = {}
    for r in per:
        case_counts[str(r.get("case") or "unknown")] = int(case_counts.get(str(r.get("case") or "unknown"), 0) + 1)

    summary = {
        "phase": "Phase-EvaluationTools-OCR-003",
        "tool": "evaluate_rapidocr_on_chinese_quality_gate_dataset_v0",
        "ts": _now_iso(),
        "dataset_root": str(dataset_root),
        "cross_validation_root": str(cross_root) if str(args.cross_validation_root or "").strip() else None,
        "output_root": str(out_root),
        "provider": "rapidocr_onnxruntime_v0",
        "sample_count": len(per),
        "elapsed_ms": round(elapsed_ms, 3),
        "case_counts": case_counts,
        "cer_summary": cer_summary,
        "chinese_recall_summary": recall_summary,
        "empty_output_report": empty_report,
        "garbled_report": garbled_report,
        "hard_audit": {
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "tts_invoked": False,
            "qwen_invoked": False,
        },
    }

    _write_json(out_root / "rapidocr_chinese_quality_eval_summary.json", summary)
    _write_json(out_root / "rapidocr_chinese_sample_eval_matrix.json", per)
    _write_json(out_root / "rapidocr_chinese_cer_summary.json", cer_summary)
    _write_json(out_root / "rapidocr_chinese_recall_summary.json", recall_summary)
    _write_json(out_root / "rapidocr_chinese_empty_output_report.json", empty_report)
    _write_json(out_root / "rapidocr_chinese_garbled_report.json", garbled_report)
    _write_json(out_root / "rapidocr_chinese_failure_cases.json", {"count": len(failure_cases), "cases": failure_cases[:500]})

    # replay + whitebox (evaluation-only)
    _append_jsonl(replay_path, {"type": "rapidocr_chinese_eval_replay_v0", "ts": _now_iso(), "output_root": str(out_root)})
    _append_jsonl(wb_path, {"type": "rapidocr_chinese_eval_whitebox_v0", "ts": _now_iso(), "hard_audit": summary["hard_audit"]})

    notes = "\n".join(
        [
            "# RapidOCR Chinese quality gate eval v0 (Evaluation Tools)",
            "",
            f"- **dataset_root:** `{summary['dataset_root']}`",
            f"- **output_root:** `{summary['output_root']}`",
            f"- **provider:** `{summary['provider']}`",
            f"- **sample_count:** `{summary['sample_count']}`",
            f"- **empty_output_rate:** `{empty_report['empty_output_rate']:.3f}`",
            "",
            "## Boundary",
            "",
            "- Evaluation-only; no runtime/mainline/whitebox integration.",
            "- Does not mutate ground truth or dataset.",
            "",
        ]
    )
    (out_root / "rapidocr_chinese_eval_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "sample_count": len(per), "empty_output_count": empty_cnt}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

