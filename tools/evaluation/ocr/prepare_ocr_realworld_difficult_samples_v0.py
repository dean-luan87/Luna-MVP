#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-RealSamples-001 — Curate real-world difficult OCR samples (no OCR provider).

Copies fixtures (if any) + generates explicit placeholders for OCR-006 taxonomy gaps.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_dataset_registry_v0 import validate_ocr_dataset_registry_entry_v0  # noqa: E402
from capabilities.evaluation.ocr.ocr_realworld_human_review_pack_v0 import write_human_review_bundle_v0  # noqa: E402
from capabilities.evaluation.ocr.ocr_realworld_sample_registry_v0 import (  # noqa: E402
    ALL_CURATED_TYPES_V0,
    REQUIRED_CONTENT_TYPES_V0,
    build_ocr_realworld_dataset_registry_for_reeval_v0,
    build_realworld_annotation_template_v0,
    build_realworld_sample_manifest_row_v0,
    build_realworld_taxonomy_coverage_report_v0,
    image_dimensions_v0,
    sha256_file_v0,
    validate_realworld_sample_manifest_v0,
)


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _collect_images(input_dir: Path) -> List[Path]:
    out: List[Path] = []
    for p in sorted(input_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES:
            out.append(p)
    return out


def _write_placeholder_png(path: Path, content_type: str) -> None:
    from PIL import Image, ImageDraw

    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (360, 220), (230, 230, 240))
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, 356, 216], outline=(160, 0, 0), width=3)
    d.text((12, 12), "PLACEHOLDER — not a real capture", fill=(140, 0, 0))
    d.text((12, 44), f"type: {content_type}", fill=(0, 0, 0))
    d.text((12, 76), "sample_source=placeholder", fill=(0, 0, 0))
    d.text((12, 108), "Replace with real image before RealEval", fill=(40, 40, 40))
    img.save(str(path))


def _copy_or_placeholder(
    *,
    idx: int,
    content_type: str,
    img_files: List[Path],
    slot: int,
    images_dir: Path,
    annotations_dir: Path,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    sample_id = f"rw_{idx:06d}"
    ann_rel = f"annotations/{sample_id}.annotation.json"
    if slot < len(img_files):
        src = img_files[slot]
        ext = src.suffix.lower() or ".png"
        img_rel = f"images/{sample_id}{ext}"
        dst = images_dir.parent / img_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        sha = sha256_file_v0(dst)
        w, h = image_dimensions_v0(dst)
        row = build_realworld_sample_manifest_row_v0(
            sample_id=sample_id,
            image_rel_path=img_rel,
            annotation_rel_path=ann_rel,
            content_type=content_type,
            sample_source="user_fixture",
            language="unknown",
            has_ground_truth=False,
            ground_truth_quality="missing",
            sha256_hex=sha,
            width=w,
            height=h,
        )
    else:
        img_rel = f"images/{sample_id}.png"
        dst = images_dir.parent / img_rel
        _write_placeholder_png(dst, content_type)
        sha = sha256_file_v0(dst)
        w, h = image_dimensions_v0(dst)
        row = build_realworld_sample_manifest_row_v0(
            sample_id=sample_id,
            image_rel_path=img_rel,
            annotation_rel_path=ann_rel,
            content_type=content_type,
            sample_source="placeholder",
            language="unknown",
            has_ground_truth=False,
            ground_truth_quality="not_applicable",
            sha256_hex=sha,
            width=w,
            height=h,
        )
    ann = build_realworld_annotation_template_v0(sample_id=sample_id, content_type=content_type)
    (annotations_dir / f"{sample_id}.annotation.json").write_text(
        json.dumps(ann, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return row, ann


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    input_dir = _require_abs(args.input_dir, "--input-dir")
    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "datasets" / "evaluation" / f"ocr_realworld_difficult_v0_{stamp}").resolve()
    images_dir = out / "images"
    annotations_dir = out / "annotations"
    human_dir = out / "human_review"
    images_dir.mkdir(parents=True, exist_ok=True)
    annotations_dir.mkdir(parents=True, exist_ok=True)

    img_files = _collect_images(input_dir)
    rows: List[Dict[str, Any]] = []
    idx = 1
    # Required taxonomy: first use real images where available, else placeholder per slot
    for slot, ct in enumerate(REQUIRED_CONTENT_TYPES_V0):
        row, _ = _copy_or_placeholder(
            idx=idx,
            content_type=ct,
            img_files=img_files,
            slot=slot,
            images_dir=images_dir,
            annotations_dir=annotations_dir,
        )
        rows.append(row)
        idx += 1

    # Additional real images beyond first five: cycle curated types
    extra_cycle = list(ALL_CURATED_TYPES_V0)
    for j in range(len(REQUIRED_CONTENT_TYPES_V0), len(img_files)):
        ct = extra_cycle[(j - len(REQUIRED_CONTENT_TYPES_V0)) % len(extra_cycle)]
        row, _ = _copy_or_placeholder(
            idx=idx,
            content_type=ct,
            img_files=img_files,
            slot=j,
            images_dir=images_dir,
            annotations_dir=annotations_dir,
        )
        rows.append(row)
        idx += 1

    manifest_path = out / "manifest.jsonl"
    with manifest_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    tax = build_realworld_taxonomy_coverage_report_v0(rows=rows)
    val = validate_realworld_sample_manifest_v0(rows=rows)

    dataset_id = out.name
    reg_doc = build_ocr_realworld_dataset_registry_for_reeval_v0(
        dataset_id=dataset_id,
        dataset_root=str(out),
        manifest_rows=rows,
        taxonomy_report=tax,
    )
    reg_entry = reg_doc.get("entry") or {}
    reg_val = validate_ocr_dataset_registry_entry_v0(reg_entry)

    summary = {
        "phase": "Phase-EvaluationTools-OCR-RealSamples-001",
        "input_dir": str(input_dir),
        "output_root": str(out),
        "dataset_id": dataset_id,
        "sample_count": len(rows),
        "real_image_files_found": len(img_files),
        "manifest_validation": val,
        "dataset_registry_validation": reg_val,
        "readiness_posture": "CONDITIONAL_GO_pending_human_capture"
        if any(r.get("sample_source") == "placeholder" for r in rows)
        else "GO",
        "verdict": "GO" if val.get("validation_passed") else "NO_GO",
        "constraints": {
            "ocr_provider_invoked": False,
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "ocr_routing_changed": False,
            "paddleocr_trial": False,
        },
    }

    notes = out / "realworld_dataset_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# OCR Real-World Difficult Samples v0",
                "",
                f"- **input_dir**: `{input_dir}`",
                f"- **output_root**: `{out}`",
                "",
                "- Entries with `sample_source=placeholder` are **explicit non-real** stubs; do not treat as production captures.",
                "- No OCR provider invoked; evaluation / human-review only.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    write_human_review_bundle_v0(human_review_dir=human_dir, manifest_rows=rows, dataset_root=out)

    (out / "dataset_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "taxonomy_coverage_report.json").write_text(json.dumps(tax, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "ocr_realworld_dataset_registry.json").write_text(
        json.dumps(reg_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps({"output_root": str(out), "sample_count": len(rows), "verdict": summary["verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
