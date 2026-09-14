#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-002 — Cross validation for Chinese font quality gate dataset v0.

Evaluation Tools only:
- No runtime / whitebox integration
- No MidPlatform/SceneDelta/WorldContext/semantic/Qwen/TTS

Cross-validation includes:
1) Glyph diversity cross-check (font-level, pixel-based)
2) Tofu similarity heuristics on generated images (image-level, pixel-based)
3) RapidOCR probe cross-check (optional; evaluation-only; does NOT affect mainline)
4) Human review contact sheet (10 samples) + index

This tool writes evaluation-only trace/replay JSONL for auditing, not runtime RequestTrace.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import os
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_chinese_font_registry_v0 import (  # noqa: E402
    PROBE_TEXT,
    validate_cjk_font_visibility_v0,
)
from capabilities.evaluation.ocr.ocr_eval_metrics_v0 import compute_chinese_char_recall_v0  # noqa: E402


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


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def _load_font_validation_summary(font_root: Path) -> Dict[str, Any]:
    p = font_root / "font_validation_summary.json"
    if not p.is_file():
        raise SystemExit(f"ERROR: missing font_validation_summary.json at: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def _load_manifest(dataset_root: Path) -> List[Dict[str, Any]]:
    p = dataset_root / "manifest.jsonl"
    if not p.is_file():
        raise SystemExit(f"ERROR: missing manifest.jsonl at: {p}")
    rows: List[Dict[str, Any]] = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        rows.append(json.loads(ln))
    return rows


def _render_char_mask(font_path: str, ch: str, *, size: int = 46) -> "Any":
    from PIL import Image, ImageDraw, ImageFont

    font = ImageFont.truetype(font_path, size=size)
    img = Image.new("L", (160, 160), 255)
    d = ImageDraw.Draw(img)
    # center glyph using textbbox to reduce clipping/positional bias
    bbox = d.textbbox((0, 0), ch, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = int((img.width - w) * 0.5) - bbox[0]
    y = int((img.height - h) * 0.5) - bbox[1]
    d.text((x, y), ch, font=font, fill=0)
    return img


def _pairwise_min_mean_absdiff(masks: List["Any"]) -> Tuple[float, float]:
    import numpy as np

    if len(masks) < 2:
        return 0.0, 0.0
    arrs = [np.asarray(m, dtype=np.int16) for m in masks]
    diffs: List[float] = []
    for i in range(len(arrs)):
        for j in range(i + 1, len(arrs)):
            d = float(np.mean(np.abs(arrs[i] - arrs[j])))
            diffs.append(d)
    return float(min(diffs) if diffs else 0.0), float(sum(diffs) / max(1, len(diffs)))


def glyph_diversity_cross_check_v0(*, font_path: str, sampled_chars: List[str]) -> Dict[str, Any]:
    """
    Render each char individually and compute pairwise pixel differences.
    If many chars are identical (same mask signature), tofu is suspected.
    """
    import hashlib

    masks = []
    errors: List[str] = []
    sigs: List[str] = []
    per_char: List[Dict[str, Any]] = []
    for ch in sampled_chars:
        try:
            m = _render_char_mask(font_path, ch, size=46)
            # crop to ink bbox to avoid positional collisions, then normalize
            inv = m.point(lambda v: 255 - v)
            bb = inv.getbbox()
            if bb is None:
                cropped = m
                ink_ratio = 0.0
            else:
                cropped = m.crop(bb).resize((48, 48))
                data = list(cropped.getdata())
                ink_ratio = float(sum(1 for v in data if v < 245)) / float(max(1, len(data)))
            masks.append(cropped)
            sig = hashlib.sha256(cropped.tobytes()).hexdigest()
            sigs.append(sig)
            per_char.append({"ch": ch, "bbox": list(bb) if bb else None, "ink_ratio": ink_ratio, "sig": sig})
        except Exception as e:
            errors.append(f"{ch}:{e!r}")
    min_diff, mean_diff = _pairwise_min_mean_absdiff(masks)
    # Simple scoring: normalized by 255 range
    glyph_diversity_score = float(min(1.0, max(0.0, mean_diff / 40.0)))
    total = len(sigs)
    uniq = len(set(sigs))
    unique_ratio = float(uniq) / float(max(1, total))
    # Conservative tofu suspicion: lots of duplicates, not merely one collision.
    # Example failure mode: some chars missing -> rendered as identical tofu glyph.
    dup = total - uniq
    tofu_suspected = bool(total >= 8 and (unique_ratio < 0.70 or dup >= 4))
    if errors:
        result = "CONDITIONAL_GO"
    elif tofu_suspected:
        result = "NO_GO"
    elif glyph_diversity_score < 0.18:
        result = "CONDITIONAL_GO"
    else:
        result = "GO"
    return {
        "sampled_chars": sampled_chars,
        "glyph_diversity_score": glyph_diversity_score,
        "min_pairwise_difference": float(min_diff),
        "mean_pairwise_difference": float(mean_diff),
        "unique_signature_ratio": float(unique_ratio),
        "duplicate_signature_count": int(dup),
        "tofu_suspected": tofu_suspected,
        "per_char": per_char,
        "errors": errors,
        "cross_check_result": result,
    }


def _connected_components_bbox(binary: "Any") -> List[Tuple[int, int, int, int, int]]:
    """
    Very small CC implementation for binary image.
    Returns list of (x0,y0,x1,y1,area) for components.
    """
    import numpy as np

    a = np.asarray(binary, dtype=np.uint8)
    h, w = a.shape
    visited = np.zeros((h, w), dtype=np.uint8)
    comps: List[Tuple[int, int, int, int, int]] = []

    def nbrs(y: int, x: int) -> List[Tuple[int, int]]:
        out = []
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < h and 0 <= xx < w:
                out.append((yy, xx))
        return out

    for y in range(h):
        for x in range(w):
            if a[y, x] == 0 or visited[y, x]:
                continue
            # foreground=1
            stack = [(y, x)]
            visited[y, x] = 1
            x0 = x1 = x
            y0 = y1 = y
            area = 0
            while stack:
                cy, cx = stack.pop()
                area += 1
                x0 = min(x0, cx)
                x1 = max(x1, cx)
                y0 = min(y0, cy)
                y1 = max(y1, cy)
                for yy, xx in nbrs(cy, cx):
                    if a[yy, xx] == 1 and not visited[yy, xx]:
                        visited[yy, xx] = 1
                        stack.append((yy, xx))
            comps.append((x0, y0, x1, y1, area))
    return comps


def tofu_shape_similarity_report_v0(*, dataset_root: Path, manifest_rows: List[Dict[str, Any]], seed: int) -> Dict[str, Any]:
    """
    Weak tofu detection on actual generated images:
    - sample 10 images
    - binarize dark pixels; extract connected components; look for many near-square components with duplicated patch hashes
    """
    from PIL import Image
    import numpy as np
    import hashlib

    rng = random.Random(int(seed))
    rows = list(manifest_rows)
    rng.shuffle(rows)
    sample_rows = rows[:10]
    tofu_suspected_samples: List[str] = []
    per_sample: List[Dict[str, Any]] = []

    for r in sample_rows:
        sid = str(r.get("sample_id") or "")
        img_path = Path(str(r.get("image_path") or ""))
        if not img_path.is_file():
            per_sample.append({"sample_id": sid, "error": "missing_image"})
            continue
        img = Image.open(str(img_path)).convert("L")
        arr = np.asarray(img, dtype=np.uint8)
        # foreground mask: dark pixels
        fg = (arr < 200).astype(np.uint8)
        comps = _connected_components_bbox(fg)
        # filter medium components
        boxes = []
        for x0, y0, x1, y1, area in comps:
            w = (x1 - x0 + 1)
            h = (y1 - y0 + 1)
            if area < 30:
                continue
            if w < 8 or h < 8:
                continue
            if w > 90 or h > 90:
                continue
            boxes.append((x0, y0, x1, y1, area))
        # compute patch hashes for near-square boxes
        hashes: List[str] = []
        near_square = 0
        for x0, y0, x1, y1, area in boxes:
            w = (x1 - x0 + 1)
            h = (y1 - y0 + 1)
            ratio = float(w) / float(max(1, h))
            if 0.75 <= ratio <= 1.33:
                near_square += 1
                patch = img.crop((x0, y0, x1 + 1, y1 + 1)).resize((32, 32))
                ph = hashlib.sha256(patch.tobytes()).hexdigest()
                hashes.append(ph)
        dup = len(hashes) - len(set(hashes))
        dup_rate = float(dup) / float(max(1, len(hashes)))
        # heuristic: many near-square components and high duplication -> tofu suspected
        suspected = bool(near_square >= 6 and dup_rate >= 0.35)
        if suspected:
            tofu_suspected_samples.append(sid)
        per_sample.append(
            {
                "sample_id": sid,
                "near_square_components": int(near_square),
                "square_patch_count": int(len(hashes)),
                "duplicate_patch_count": int(dup),
                "duplicate_patch_rate": float(dup_rate),
                "tofu_suspected": suspected,
            }
        )

    rate = float(len(tofu_suspected_samples)) / float(max(1, len(sample_rows)))
    if rate >= 0.30:
        result = "NO_GO"
    elif rate > 0.0:
        result = "CONDITIONAL_GO"
    else:
        result = "GO"
    return {
        "checked_samples": len(sample_rows),
        "tofu_suspected_samples": tofu_suspected_samples,
        "tofu_suspected_rate": rate,
        "per_sample": per_sample,
        "result": result,
    }


def rapidocr_probe_cross_check_v0(*, manifest_rows: List[Dict[str, Any]], seed: int) -> Dict[str, Any]:
    """
    Optional RapidOCR probe on 10 samples (5 zh_plain_text + 5 mixed_zh_en_digit).
    This is evaluation-only cross-check; must not affect mainline provider decisions.
    """
    rng = random.Random(int(seed))
    zh = [r for r in manifest_rows if str(r.get("category") or "") == "zh_plain_text_quality_gate"]
    mixed = [r for r in manifest_rows if str(r.get("category") or "") == "mixed_zh_en_digit_quality_gate"]
    rng.shuffle(zh)
    rng.shuffle(mixed)
    pick = (zh[:5] + mixed[:5])[:10]

    if importlib.util.find_spec("rapidocr_onnxruntime") is None:
        return {
            "provider": "rapidocr_onnxruntime_v0",
            "rapidocr_available": False,
            "sample_count": len(pick),
            "result": "CONDITIONAL_GO",
            "notes": "rapidocr_onnxruntime not importable; skipped OCR probe cross-check.",
        }

    from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

    adapter = RapidOCRAdapterV0()
    ok, err = adapter.is_available()
    if not ok:
        return {
            "provider": adapter.provider_id,
            "rapidocr_available": False,
            "error": err,
            "sample_count": len(pick),
            "result": "CONDITIONAL_GO",
        }

    per: List[Dict[str, Any]] = []
    recalls: List[float] = []
    empty = 0
    for r in pick:
        img_path = str(r.get("image_path") or "")
        gt = str(r.get("ground_truth_text") or "")
        env = adapter.recognize_image(image_path=img_path, frame_id=str(r.get("sample_id") or "probe"), timestamp_ms=0)
        raw_text = ""
        try:
            cands = env.get("candidates") or []
            raw_text = "\n".join([str(c.get("text") or "") for c in cands if isinstance(c, dict)]).strip()
        except Exception:
            raw_text = ""
        if not raw_text:
            empty += 1
        rec = compute_chinese_char_recall_v0(raw_text, gt)
        if rec.get("chinese_char_recall") is not None:
            recalls.append(float(rec["chinese_char_recall"]))
        per.append(
            {
                "sample_id": r.get("sample_id"),
                "category": r.get("category"),
                "ground_truth_text": gt,
                "raw_text": raw_text,
                "chinese_recall": rec.get("chinese_char_recall"),
            }
        )

    avg = float(sum(recalls) / max(1, len(recalls))) if recalls else None
    # Important: even if OCR is weak, don't fail font visibility solely by OCR.
    if empty >= 8:
        result = "CONDITIONAL_GO"
        notes = "RapidOCR output mostly empty; treat as provider follow-up (not font failure)."
    else:
        result = "GO"
        notes = "RapidOCR probe executed; treat as supplementary evidence only."
    return {
        "provider": adapter.provider_id,
        "rapidocr_available": True,
        "sample_count": len(pick),
        "avg_chinese_recall": avg,
        "empty_output_count": int(empty),
        "per_sample": per,
        "result": result,
        "notes": notes,
    }


def build_human_review_contact_sheet_v0(*, manifest_rows: List[Dict[str, Any]], out_png: Path, out_index: Path, seed: int, font_path: str) -> Dict[str, Any]:
    from PIL import Image, ImageDraw, ImageFont

    rng = random.Random(int(seed))
    rows = list(manifest_rows)
    rng.shuffle(rows)
    pick = rows[:10]

    index = []
    thumbs: List[Tuple[str, "Any", str]] = []
    for r in pick:
        img_path = Path(str(r.get("image_path") or ""))
        if not img_path.is_file():
            continue
        img = Image.open(str(img_path)).convert("RGB")
        gt = str(r.get("ground_truth_text") or "")
        sid = str(r.get("sample_id") or "")
        thumbs.append((sid, img, gt))
        index.append(
            {
                "sample_id": sid,
                "image_path": str(img_path),
                "ground_truth_text": gt,
                "category": r.get("category"),
                "font_path": font_path,
            }
        )

    cols, rows_n = 2, 5
    cell_w, cell_h = 920, 360
    canvas = Image.new("RGB", (cols * cell_w, rows_n * cell_h), (245, 245, 245))
    d = ImageDraw.Draw(canvas)
    try:
        label_font = ImageFont.truetype(font_path, size=20)
    except Exception:
        try:
            label_font = ImageFont.load_default()
        except Exception:
            label_font = None

    for i, (sid, img, gt) in enumerate(thumbs[:10]):
        r_i = i // cols
        c_i = i % cols
        x0 = c_i * cell_w
        y0 = r_i * cell_h
        # image area
        thumb = img.copy()
        thumb.thumbnail((cell_w - 24, cell_h - 90))
        canvas.paste(thumb, (x0 + 12, y0 + 12))
        # labels
        d.text((x0 + 12, y0 + cell_h - 72), f"{sid}", fill=(10, 10, 10), font=label_font)
        d.text((x0 + 12, y0 + cell_h - 46), gt[:38], fill=(20, 20, 20), font=label_font)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(str(out_png))
    out_index.parent.mkdir(parents=True, exist_ok=True)
    out_index.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"sample_count": len(index), "output_png": str(out_png), "output_index": str(out_index)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--font-validation-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    dataset_root = _require_abs(args.dataset_root, "--dataset-root")
    font_root = _require_abs(args.font_validation_root, "--font-validation-root")
    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    font_summary = _load_font_validation_summary(font_root)
    selected_font = ((font_summary.get("selected_font") or {}).get("selected") or {}) if isinstance(font_summary, dict) else {}
    font_path = str((selected_font or {}).get("font_path") or "")
    if not font_path:
        raise SystemExit("ERROR: selected font_path missing in font_validation_summary.json")

    manifest_rows = _load_manifest(dataset_root)

    trace_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []

    # 1) glyph diversity cross-check
    sampled_chars = ["上", "海", "地", "铁", "防", "范", "电", "信", "网", "络", "诈", "骗"]
    glyph_report = glyph_diversity_cross_check_v0(font_path=font_path, sampled_chars=sampled_chars)
    _write_json(out_root / "glyph_diversity_cross_check.json", glyph_report)
    trace_rows.append({"ts": _now_iso(), "event": "glyph_diversity_cross_check", "report": glyph_report})

    # 2) tofu similarity on generated images
    tofu_report = tofu_shape_similarity_report_v0(dataset_root=dataset_root, manifest_rows=manifest_rows, seed=int(args.seed))
    _write_json(out_root / "tofu_shape_similarity_report.json", tofu_report)
    trace_rows.append({"ts": _now_iso(), "event": "tofu_shape_similarity_report", "report": tofu_report})

    # 3) RapidOCR probe (optional)
    rapidocr_report = rapidocr_probe_cross_check_v0(manifest_rows=manifest_rows, seed=int(args.seed))
    _write_json(out_root / "rapidocr_probe_cross_check.json", rapidocr_report)
    trace_rows.append({"ts": _now_iso(), "event": "rapidocr_probe_cross_check", "report": rapidocr_report})

    # 4) human review contact sheet
    contact_png = out_root / "human_review_contact_sheet.png"
    index_json = out_root / "human_review_index.json"
    human_pack = build_human_review_contact_sheet_v0(
        manifest_rows=manifest_rows, out_png=contact_png, out_index=index_json, seed=int(args.seed), font_path=font_path
    )
    trace_rows.append({"ts": _now_iso(), "event": "human_review_contact_sheet", "pack": human_pack})

    # font visibility (reuse primary font probe as extra context)
    vis = validate_cjk_font_visibility_v0(font_path)
    _write_json(out_root / "font_visibility_recheck.json", vis)

    # Compose overall cross verdict (conservative)
    parts = [glyph_report.get("cross_check_result"), tofu_report.get("result"), rapidocr_report.get("result")]
    if "NO_GO" in parts:
        cross_verdict = "NO_GO"
    elif "CONDITIONAL_GO" in parts:
        cross_verdict = "CONDITIONAL_GO"
    else:
        cross_verdict = "GO"

    summary = {
        "phase": "Phase-EvaluationTools-OCR-002",
        "tool": "cross_validate_ocr_chinese_font_quality_gate_v0",
        "ts": _now_iso(),
        "dataset_root": str(dataset_root),
        "font_validation_root": str(font_root),
        "output_root": str(out_root),
        "probe_text": PROBE_TEXT,
        "selected_font_path": font_path,
        "cross_verdict": cross_verdict,
        "glyph_diversity_cross_check": {"result": glyph_report.get("cross_check_result")},
        "tofu_shape_similarity_report": {"result": tofu_report.get("result")},
        "rapidocr_probe_cross_check": {"result": rapidocr_report.get("result"), "rapidocr_available": rapidocr_report.get("rapidocr_available")},
        "hard_audit": {
            "runtime_integration": False,
            "whitebox_integration": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "semantic_interpretation_enabled": False,
            "qwen_invoked": False,
            "tts_invoked": False,
        },
    }
    _write_json(out_root / "chinese_font_cross_validation_summary.json", summary)

    notes = "\n".join(
        [
            "# OCR Chinese font cross validation v0 (Evaluation Tools)",
            "",
            f"- **dataset_root:** `{summary['dataset_root']}`",
            f"- **font_validation_root:** `{summary['font_validation_root']}`",
            f"- **output_root:** `{summary['output_root']}`",
            f"- **selected_font_path:** `{summary['selected_font_path']}`",
            f"- **cross_verdict:** `{summary['cross_verdict']}`",
            "",
            "## Boundary",
            "",
            "- Evaluation Tools only; no runtime/whitebox integration.",
            "- RapidOCR probe is evaluation-only cross-check and does not mutate dataset or affect mainline decisions.",
            "",
        ]
    )
    (out_root / "cross_validation_notes.md").write_text(notes + "\n", encoding="utf-8")

    # trace/replay (minimal)
    replay_rows.append({"ts": _now_iso(), "event": "replay_hint", "howto": "Review JSON reports + contact sheet PNG."})
    _write_jsonl(out_root / "cross_validation_trace.jsonl", trace_rows)
    _write_jsonl(out_root / "cross_validation_replay.jsonl", replay_rows)

    print(json.dumps({"ok": True, "cross_verdict": cross_verdict, "output_root": str(out_root)}, ensure_ascii=False))
    return 0 if cross_verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

