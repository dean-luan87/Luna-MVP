# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-Foundation-001 — Human review package v0 (Evaluation Tools).

Generate a small, manual-review-friendly bundle:
- contact sheet PNG (sample image thumbnails + labels)
- review index JSON
- annotation template JSON

This is evaluation-only and must not integrate into runtime or whitebox.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


def build_review_annotations_template_v0(*, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema": "human_review_annotations_template_v0",
        "items": [
            {
                "sample_id": it.get("sample_id"),
                "labels": {
                    "image_readable": None,  # true/false
                    "ground_truth_correct": None,  # true/false/partial
                    "ocr_output_acceptable": None,  # true/false/partial
                    "category_override": None,  # optional
                },
                "notes": "",
            }
            for it in items
        ],
    }


def generate_contact_sheet_v0(
    *,
    items: List[Dict[str, Any]],
    output_png: Path,
    font_path: Optional[str] = None,
    cols: int = 2,
    rows: int = 5,
) -> Dict[str, Any]:
    from PIL import Image, ImageDraw, ImageFont

    output_png.parent.mkdir(parents=True, exist_ok=True)
    cell_w, cell_h = 920, 360
    canvas = Image.new("RGB", (cols * cell_w, rows * cell_h), (245, 245, 245))
    d = ImageDraw.Draw(canvas)

    label_font = None
    if font_path:
        try:
            label_font = ImageFont.truetype(str(font_path), size=20)
        except Exception:
            label_font = None
    if label_font is None:
        try:
            label_font = ImageFont.load_default()
        except Exception:
            label_font = None

    for i, it in enumerate(items[: cols * rows]):
        img_path = Path(str(it.get("image_path") or ""))
        if not img_path.is_file():
            continue
        img = Image.open(str(img_path)).convert("RGB")
        sid = str(it.get("sample_id") or "")
        gt = str(it.get("ground_truth_text") or "")
        cat = str(it.get("category") or "")

        r_i = i // cols
        c_i = i % cols
        x0 = c_i * cell_w
        y0 = r_i * cell_h

        thumb = img.copy()
        thumb.thumbnail((cell_w - 24, cell_h - 90))
        canvas.paste(thumb, (x0 + 12, y0 + 12))

        d.text((x0 + 12, y0 + cell_h - 72), f"{sid}  [{cat}]", fill=(10, 10, 10), font=label_font)
        d.text((x0 + 12, y0 + cell_h - 46), gt[:44], fill=(20, 20, 20), font=label_font)

    canvas.save(str(output_png))
    return {"output_png": str(output_png), "items": len(items)}


def write_human_review_package_v0(
    *,
    output_root: Path,
    items: List[Dict[str, Any]],
    font_path: Optional[str] = None,
) -> Dict[str, Any]:
    output_root = output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    contact_png = output_root / "human_review_contact_sheet.png"
    index_json = output_root / "human_review_index.json"
    ann_json = output_root / "review_annotations_template.json"

    generate_contact_sheet_v0(items=items, output_png=contact_png, font_path=font_path)
    index_json.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ann = build_review_annotations_template_v0(items=items)
    ann_json.write_text(json.dumps(ann, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "output_root": str(output_root),
        "contact_sheet_png": str(contact_png),
        "human_review_index_json": str(index_json),
        "review_annotations_template_json": str(ann_json),
    }

