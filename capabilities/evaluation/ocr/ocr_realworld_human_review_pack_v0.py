# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-RealSamples-001 — Human review contact sheet + index (evaluation-only).

Uses PIL contact sheet generator from Foundation-001 human review package.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.evaluation.ocr.ocr_human_review_package_v0 import generate_contact_sheet_v0


def _items_for_contact_sheet(manifest_rows: List[Dict[str, Any]], dataset_root: Path) -> List[Dict[str, Any]]:
    root = dataset_root.resolve()
    out: List[Dict[str, Any]] = []
    for row in manifest_rows:
        rel = str(row.get("image_path") or "")
        abs_path = (root / rel) if rel else Path("")
        out.append(
            {
                "sample_id": row.get("sample_id"),
                "image_path": str(abs_path.resolve()) if rel and abs_path.is_file() else "",
                "ground_truth_text": "",
                "category": f"{row.get('content_type')} | {row.get('sample_source')}",
            }
        )
    return out


def build_realworld_human_review_index_v0(*, manifest_rows: List[Dict[str, Any]], dataset_root: str) -> Dict[str, Any]:
    return {
        "schema": "human_review_index_realworld_v0",
        "phase": "Phase-EvaluationTools-OCR-RealSamples-001",
        "dataset_root": dataset_root,
        "sample_count": len(manifest_rows),
        "items": [
            {
                "sample_id": r.get("sample_id"),
                "content_type": r.get("content_type"),
                "sample_source": r.get("sample_source"),
                "image_path": r.get("image_path"),
                "annotation_path": r.get("annotation_path"),
                "human_review_status": "pending",
            }
            for r in manifest_rows
        ],
    }


def build_realworld_review_annotation_template_v0(*, manifest_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema": "review_annotations_template_realworld_v0",
        "phase": "Phase-EvaluationTools-OCR-RealSamples-001",
        "items": [
            {
                "sample_id": r.get("sample_id"),
                "content_type": r.get("content_type"),
                "sample_source": r.get("sample_source"),
                "labels": {
                    "image_readable": None,
                    "taxonomy_correct": None,
                    "needs_additional_real_capture": None,
                    "reject_as_non_text": None,
                },
                "notes": "",
            }
            for r in manifest_rows
        ],
    }


def build_realworld_human_review_contact_sheet_v0(
    *,
    manifest_rows: List[Dict[str, Any]],
    dataset_root: Path,
    output_png: Path,
    font_path: Optional[str] = None,
) -> Dict[str, Any]:
    dataset_root = dataset_root.resolve()
    items = _items_for_contact_sheet(manifest_rows, dataset_root)
    # Filter to rows that have a readable image for thumbnail; still draw sheet (may skip missing)
    generate_contact_sheet_v0(items=items, output_png=output_png, font_path=font_path, cols=2, rows=8)
    return {"output_png": str(output_png.resolve()), "item_count": len(items)}


def write_human_review_bundle_v0(
    *,
    human_review_dir: Path,
    manifest_rows: List[Dict[str, Any]],
    dataset_root: Path,
    font_path: Optional[str] = None,
) -> Dict[str, Any]:
    human_review_dir.mkdir(parents=True, exist_ok=True)
    idx = build_realworld_human_review_index_v0(manifest_rows=manifest_rows, dataset_root=str(dataset_root.resolve()))
    tpl = build_realworld_review_annotation_template_v0(manifest_rows=manifest_rows)
    (human_review_dir / "human_review_index.json").write_text(
        json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (human_review_dir / "review_annotations_template.json").write_text(
        json.dumps(tpl, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    cs = human_review_dir / "contact_sheet.png"
    build_realworld_human_review_contact_sheet_v0(
        manifest_rows=manifest_rows, dataset_root=dataset_root, output_png=cs, font_path=font_path
    )
    return {
        "human_review_dir": str(human_review_dir.resolve()),
        "contact_sheet_png": str(cs.resolve()),
        "human_review_index_json": str((human_review_dir / "human_review_index.json").resolve()),
        "review_annotations_template_json": str((human_review_dir / "review_annotations_template.json").resolve()),
    }


__all__ = [
    "build_realworld_human_review_contact_sheet_v0",
    "build_realworld_human_review_index_v0",
    "build_realworld_review_annotation_template_v0",
    "write_human_review_bundle_v0",
]
