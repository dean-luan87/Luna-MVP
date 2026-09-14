# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-002 — Chinese font quality gate dataset generator v0.

Generate a small Chinese synthetic subset with a validated CJK-capable font.
Evaluation Tools only. Must NOT invoke OCR providers.
"""

from __future__ import annotations

import dataclasses
import json
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from capabilities.evaluation.ocr.ocr_chinese_font_registry_v0 import (
    PROBE_TEXT,
    scan_chinese_fonts_v0,
    select_best_cjk_font_v0,
    validate_cjk_font_visibility_v0,
)
from capabilities.evaluation.ocr.ocr_synthetic_dataset_generator_v0 import (
    SyntheticSampleSpecV0,
    compute_file_sha256_v0,
    _pillow_render_text_image_v0,
)


DEFAULT_CATEGORIES = [
    ("zh_plain_text_quality_gate", 20),
    ("mixed_zh_en_digit_quality_gate", 20),
    ("digits_with_chinese_context", 10),
]


def _ensure_abs_dir(p: Path) -> Path:
    pp = p.expanduser().resolve()
    if not pp.is_absolute():
        raise ValueError(f"path must be absolute: {p}")
    pp.mkdir(parents=True, exist_ok=True)
    return pp


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _build_chinese_specs_v0(*, seed: int) -> List[SyntheticSampleSpecV0]:
    rng = random.Random(int(seed))
    zh_phrases = [
        "上海地铁9号线",
        "防范电信网络诈骗",
        "请勿靠近车门",
        "下一站人民广场",
        "乘客请有序排队",
        "注意脚下安全",
        "紧急出口",
        "禁止吸烟",
        "请佩戴口罩",
        "保持车厢清洁",
        "文明乘车",
        "小心夹手",
        "请勿倚靠车门",
        "请保管好随身物品",
    ]
    en_words = ["STOP", "EXIT", "LINE", "METRO", "NOTICE", "NO", "SMOKING", "CAUTION"]
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    specs: List[SyntheticSampleSpecV0] = []
    idx = 0

    def mk(sample_id: str, language: str, category: str, text: str) -> None:
        nonlocal specs
        specs.append(SyntheticSampleSpecV0(sample_id=sample_id, language=language, category=category, text=text))

    # fixed counts
    for category, cnt in DEFAULT_CATEGORIES:
        for _ in range(cnt):
            idx += 1
            sid = f"zhq_{idx:06d}"
            if category == "zh_plain_text_quality_gate":
                text = rng.choice(zh_phrases)
                mk(sid, "zh", category, text)
            elif category == "mixed_zh_en_digit_quality_gate":
                text = f"{rng.choice(zh_phrases)} {rng.choice(en_words)} {rng.choice(digits)}{rng.choice(digits)}"
                mk(sid, "mixed", category, text)
            elif category == "digits_with_chinese_context":
                text = f"{rng.choice(digits)}{rng.choice(digits)}{rng.choice(digits)} {rng.choice(zh_phrases)}"
                mk(sid, "mixed", category, text)
            else:
                text = rng.choice(zh_phrases)
                mk(sid, "zh", category, text)
    return specs


def generate_ocr_chinese_font_quality_gate_dataset_v0(
    *,
    output_root: Path,
    seed: int,
    count: int,
    font_validation: Optional[Dict[str, Any]] = None,
    font_dirs: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """
    If `font_validation` provided, it should include a selected font_path.
    Otherwise, scan+select best visible CJK font locally.
    """
    out_root = _ensure_abs_dir(output_root)
    images_dir = _ensure_abs_dir(out_root / "images")
    gt_dir = _ensure_abs_dir(out_root / "ground_truth")
    probe_dir = _ensure_abs_dir(out_root / "font_probe")

    registry = None
    selection = None
    font_path = None
    if font_validation and isinstance(font_validation.get("selected_font"), dict):
        sel = font_validation.get("selected_font") or {}
        if sel.get("ok") and isinstance(sel.get("selected"), dict):
            font_path = str((sel.get("selected") or {}).get("font_path") or "") or None

    if not font_path:
        registry = scan_chinese_fonts_v0(font_dirs=font_dirs)
        selection = select_best_cjk_font_v0(registry)
        if not selection.get("ok"):
            return {
                "ok": False,
                "output_root": str(out_root),
                "reason": "no_cjk_visible_font_found",
                "registry": registry,
                "selection": selection,
            }
        font_path = str((selection.get("selected") or {}).get("font_path") or "") or None

    if not font_path:
        return {"ok": False, "output_root": str(out_root), "reason": "font_path_missing"}

    vis = validate_cjk_font_visibility_v0(font_path)
    if vis.get("validation_result") != "GO":
        _write_json(out_root / "font_visibility_report.json", vis)
        return {"ok": False, "output_root": str(out_root), "reason": "font_visibility_no_go", "visibility": vis}

    # Save probe image
    try:
        from capabilities.evaluation.ocr.ocr_chinese_font_registry_v0 import _render_text_mask  # type: ignore

        img = _render_text_mask(font_path, PROBE_TEXT, size=30).convert("RGB")
        img.save(str(probe_dir / "probe_text.png"))
    except Exception:
        pass

    specs = _build_chinese_specs_v0(seed=seed)
    specs = specs[: int(count)]

    manifest_path = out_root / "manifest.jsonl"
    lines: List[str] = []
    category_counts: Dict[str, int] = {}

    rng = random.Random(int(seed))
    width, height = 720, 220
    for spec in specs:
        img_path = images_dir / f"{spec.sample_id}.png"
        gt_path = gt_dir / f"{spec.sample_id}.txt"
        img = _pillow_render_text_image_v0(
            spec.text,
            width=width,
            height=height,
            rng=rng,
            font_path=font_path,
            font_size=46,
        )
        img.save(str(img_path))
        gt_path.write_text(spec.text, encoding="utf-8")
        sha = compute_file_sha256_v0(img_path)
        w, h = img.size  # type: ignore[attr-defined]
        rec = {
            "sample_id": spec.sample_id,
            "image_path": str(img_path),
            "ground_truth_path": str(gt_path),
            "ground_truth_text": spec.text,
            "language": spec.language,
            "category": spec.category,
            "font_id": f"font_{Path(font_path).stem}",
            "font_path": font_path,
            "font_validation_ref": None,
            "sha256": sha,
            "width": int(w),
            "height": int(h),
            "visible_cjk_passed": True,
            "tofu_suspected": False,
        }
        lines.append(json.dumps(rec, ensure_ascii=False))
        category_counts[spec.category] = int(category_counts.get(spec.category, 0) + 1)

    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    summary = {
        "phase": "Phase-EvaluationTools-OCR-002",
        "dataset": "ocr_chinese_font_quality_gate_v0",
        "output_root": str(out_root),
        "count": len(specs),
        "category_counts": category_counts,
        "font_path": font_path,
        "font_visibility": vis,
        "ts_unix": int(time.time()),
        "hard_audit": {
            "ocr_provider_invoked": False,
            "runtime_integration": False,
            "whitebox_integration": False,
        },
    }
    _write_json(out_root / "dataset_summary.json", summary)
    if registry:
        _write_json(out_root / "font_registry.json", registry)
    if selection:
        _write_json(out_root / "font_selection_report.json", selection)
    _write_json(out_root / "font_visibility_report.json", vis)

    notes = "\n".join(
        [
            "# OCR Chinese font quality gate dataset v0",
            "",
            "- Evaluation Tools only.",
            "- No OCR provider invoked.",
            f"- **count:** `{summary['count']}`",
            f"- **font_path:** `{font_path}`",
            "",
        ]
    )
    (out_root / "quality_gate_notes.md").write_text(notes + "\n", encoding="utf-8")

    return {"ok": True, "output_root": str(out_root), "summary": summary}

