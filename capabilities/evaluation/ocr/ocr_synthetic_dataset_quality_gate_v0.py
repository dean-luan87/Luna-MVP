# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-002 — Synthetic dataset quality gate v0 (Chinese font visibility + GT consistency).

Evaluation Tools only. Must not invoke OCR providers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def validate_manifest_ground_truth_consistency_v0(*, dataset_root: Path) -> Dict[str, Any]:
    dataset_root = dataset_root.expanduser().resolve()
    manifest = dataset_root / "manifest.jsonl"
    blockers: List[str] = []
    if not manifest.is_file():
        return {"ok": False, "blockers": ["manifest_missing"]}

    mismatches = 0
    rows = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows += 1
        r = json.loads(line)
        gt_text = str(r.get("ground_truth_text") or "")
        gt_path = Path(str(r.get("ground_truth_path") or ""))
        if not gt_path.is_file():
            mismatches += 1
            continue
        file_txt = gt_path.read_text(encoding="utf-8").strip("\n")
        if file_txt != gt_text.strip("\n"):
            mismatches += 1
    if mismatches:
        blockers.append(f"ground_truth_text_mismatch:{mismatches}")
    return {"ok": not blockers, "rows": rows, "mismatches": mismatches, "blockers": blockers}


def validate_all_samples_have_visible_cjk_font_v0(*, dataset_root: Path) -> Dict[str, Any]:
    manifest = (dataset_root.expanduser().resolve() / "manifest.jsonl")
    blockers: List[str] = []
    if not manifest.is_file():
        return {"ok": False, "blockers": ["manifest_missing"]}

    bad = 0
    rows = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows += 1
        r = json.loads(line)
        if r.get("language") != "zh" and not str(r.get("category") or "").startswith("zh"):
            continue
        if r.get("visible_cjk_passed") is not True:
            bad += 1
        if r.get("tofu_suspected") is True:
            bad += 1
        if not r.get("font_path"):
            bad += 1
    if bad:
        blockers.append(f"cjk_visibility_not_passed:{bad}")
    return {"ok": not blockers, "rows": rows, "bad": bad, "blockers": blockers}


def build_chinese_dataset_quality_gate_report_v0(*, dataset_root: Path) -> Dict[str, Any]:
    dataset_root = dataset_root.expanduser().resolve()
    gt = validate_manifest_ground_truth_consistency_v0(dataset_root=dataset_root)
    cjk = validate_all_samples_have_visible_cjk_font_v0(dataset_root=dataset_root)
    ok = bool(gt.get("ok")) and bool(cjk.get("ok"))
    return {"ok": ok, "dataset_root": str(dataset_root), "ground_truth_consistency": gt, "cjk_visibility": cjk}

