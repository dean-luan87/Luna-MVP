#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-RealSamples-001 — Verifier for real-world difficult sample dataset bundle.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-root", required=True)
    args = ap.parse_args()

    root = Path(args.dataset_root).expanduser().resolve()
    blockers: List[str] = []

    if not root.is_dir():
        blockers.append("A_root_not_dir")

    required_files = [
        "manifest.jsonl",
        "dataset_summary.json",
        "taxonomy_coverage_report.json",
        "realworld_dataset_notes.md",
        "human_review/contact_sheet.png",
        "human_review/human_review_index.json",
        "human_review/review_annotations_template.json",
        "ocr_realworld_dataset_registry.json",
    ]
    for rel in required_files:
        if not (root / rel).is_file():
            blockers.append(f"A_missing:{rel}")

    manifest_rows: List[Dict[str, Any]] = []
    if not blockers and (root / "manifest.jsonl").is_file():
        for ln, line in enumerate((root / "manifest.jsonl").read_text(encoding="utf-8").splitlines()):
            line = line.strip()
            if not line:
                continue
            try:
                manifest_rows.append(json.loads(line))
            except json.JSONDecodeError:
                blockers.append(f"B_bad_manifest_line:{ln}")

    if not blockers and not manifest_rows:
        blockers.append("C_empty_manifest")

    images_dir = root / "images"
    if not blockers:
        if not images_dir.is_dir():
            blockers.append("C_no_images_dir")
        elif not any(images_dir.iterdir()):
            blockers.append("C_images_dir_empty")

    if not blockers:
        for i, row in enumerate(manifest_rows):
            sid = str(row.get("sample_id") or "")
            src = str(row.get("sample_source") or "")
            if src == "placeholder":
                if row.get("has_ground_truth") is True:
                    blockers.append(f"H_placeholder_truth:{sid}")
                if str(row.get("ground_truth_quality") or "") not in ("missing", "not_applicable"):
                    blockers.append(f"H_placeholder_gtq:{sid}")
            rel_img = str(row.get("image_path") or "")
            if rel_img and not (root / rel_img).is_file():
                blockers.append(f"C_missing_image:{sid}")
            rel_ann = str(row.get("annotation_path") or "")
            if rel_ann and not (root / rel_ann).is_file():
                blockers.append(f"D_missing_annotation:{sid}")

    summ_path = root / "dataset_summary.json"
    if not blockers and summ_path.is_file():
        sm = _read_json(summ_path)
        c = sm.get("constraints") or {}
        if c.get("ocr_provider_invoked") is not False:
            blockers.append("I_ocr_provider")
        for k, tag in (
            ("runtime_integration", "J_runtime"),
            ("whitebox_integration", "K_whitebox"),
            ("mainline_side_effect", "L_mainline"),
            ("midplatform_invoked", "M_midplatform"),
            ("scene_delta_invoked", "M_scene_delta"),
            ("world_context_invoked", "M_world_context"),
        ):
            if c.get(k) is not False:
                blockers.append(tag)
        if c.get("ocr_routing_changed") is not False:
            blockers.append("N_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-EvaluationTools-OCR-RealSamples-001",
        "verdict": verdict,
        "blockers": blockers,
        "dataset_root": str(root),
    }
    (root / "ocr_realworld_difficult_samples_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
