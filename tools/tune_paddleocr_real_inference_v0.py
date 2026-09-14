#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _norm(s: str) -> str:
    return " ".join((s or "").strip().split())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-manifest", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--max-samples", type=int, default=12)
    args = ap.parse_args()
    mpath = args.dataset_manifest if os.path.isabs(args.dataset_manifest) else os.path.abspath(os.path.join(REPO_ROOT, args.dataset_manifest))
    out = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))
    os.makedirs(out, exist_ok=True)

    from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0

    man = _load(mpath)
    samples = list(man.get("samples") or [])[: int(args.max_samples)]
    profiles = [
        "config_baseline",
        "config_low_drop_score",
        "config_relaxed_det_box_thresh",
        "config_use_pinned_paths_explicit",
        "config_init_once",
    ]
    results: List[Dict[str, Any]] = []
    for p in profiles:
        force_pinned = p == "config_use_pinned_paths_explicit"
        adapter = PaddleOCRAdapterV0(enable_real_inference=True, config_profile=p, force_pinned_paths=force_pinned)
        exact = 0
        latency = 0.0
        n = len(samples) or 1
        nonempty = 0
        for s in samples:
            sid = str(s.get("sample_id") or "")
            img = str(s.get("image_path") or "")
            img_abs = img if os.path.isabs(img) else os.path.abspath(os.path.join(REPO_ROOT, img))
            gt = _load(str(s.get("gt_path")) if os.path.isabs(str(s.get("gt_path"))) else os.path.abspath(os.path.join(REPO_ROOT, str(s.get("gt_path")))))
            r = adapter.recognize_image(image_path=img_abs, frame_id=str(s.get("frame_id") or sid), timestamp_ms=int(s.get("timestamp_ms") or 0))
            pred = _norm(str(r.get("raw_text_joined") or ""))
            g = _norm(str(gt.get("raw_text_joined") or ""))
            if pred == g:
                exact += 1
            if pred:
                nonempty += 1
            latency += float(r.get("latency_ms") or 0.0)
        results.append(
            {
                "config_profile": p,
                "sample_count": n,
                "normalized_text_exact_match_rate": round(exact / n, 6),
                "non_empty_prediction_rate": round(nonempty / n, 6),
                "avg_latency_ms_per_frame": round(latency / n, 3),
            }
        )

    ranked = sorted(results, key=lambda x: (-x["normalized_text_exact_match_rate"], -x["non_empty_prediction_rate"], x["avg_latency_ms_per_frame"]))
    best = ranked[0] if ranked else None
    _write(os.path.join(out, "config_comparison.json"), results)
    _write(os.path.join(out, "best_config_candidate.json"), {"best_config_candidate": best, "no_default_decision_allowed": True})
    _write(os.path.join(out, "tuning_summary.json"), {"phase": "Phase-ModelOCR-006B", "tested_profiles": profiles, "best_config_candidate": best, "no_default_decision_allowed": True})
    print(json.dumps({"ok": True, "output_root": os.path.relpath(out, REPO_ROOT) if out.startswith(REPO_ROOT) else out, "best": best}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
