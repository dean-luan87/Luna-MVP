#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-006 — Verifier for capability boundary dataset v0.

Evaluation Tools only. Does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--min-cases", type=int, default=120)
    args = ap.parse_args()

    dr = Path(args.dataset_root).expanduser()
    if not dr.is_absolute():
        raise SystemExit("ERROR: --dataset-root must be absolute")
    root = dr.resolve()
    if not root.is_dir():
        raise SystemExit(f"NO_GO: dataset_root_missing:{root}")

    blockers: List[str] = []
    manifest = root / "boundary_case_manifest.jsonl"
    summary = root / "boundary_case_summary.json"
    imgs = root / "images"
    gt = root / "ground_truth"
    exp = root / "expected_routing"
    if not manifest.is_file():
        blockers.append("missing_manifest")
    if not summary.is_file():
        blockers.append("missing_summary")
    if not imgs.is_dir():
        blockers.append("missing_images_dir")
    if not gt.is_dir():
        blockers.append("missing_ground_truth_dir")
    if not exp.is_dir():
        blockers.append("missing_expected_routing_dir")

    case_count = 0
    content_types = set()
    manual_required = 0
    if manifest.is_file():
        for ln in manifest.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            case_count += 1
            r = json.loads(ln)
            content_types.add(str(r.get("content_type") or ""))
            if str(r.get("generation_status") or "") == "manual_sample_required":
                manual_required += 1
            ip = Path(str(r.get("image_path") or ""))
            gp = Path(str(r.get("ground_truth_path") or ""))
            if not ip.is_file():
                blockers.append(f"missing_image:{r.get('case_id')}")
            if not gp.is_file():
                blockers.append(f"missing_gt:{r.get('case_id')}")

    if case_count < int(args.min_cases):
        blockers.append(f"too_few_cases:{case_count}<{args.min_cases}")
    if len([ct for ct in content_types if ct]) < 12:
        blockers.append(f"insufficient_content_type_coverage:{len(content_types)}")

    # boundary flags in summary
    if summary.is_file():
        s = _read_json(summary)
        ha = (s.get("hard_audit") or {}) if isinstance(s, dict) else {}
        for k in ("ocr_provider_invoked", "runtime_integration", "whitebox_integration", "mainline_side_effect"):
            if ha.get(k) is not False:
                blockers.append(f"boundary_violation:{k}")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-EvaluationTools-OCR-006",
        "verifier": "verify_ocr_capability_boundary_dataset_v0",
        "dataset_root": str(root),
        "case_count": case_count,
        "content_type_count": len([ct for ct in content_types if ct]),
        "manual_sample_required_count": manual_required,
        "verdict": verdict,
        "blockers": blockers,
    }
    (root / "boundary_dataset_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "case_count": case_count, "content_type_count": report["content_type_count"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

