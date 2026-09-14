#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())


def _load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--previous-root", default=None)
    ap.add_argument("--real-root", default=None)
    ap.add_argument("--previous-benchmark-root", default=None)
    ap.add_argument("--paddle-real-root", default=None)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    prev_arg = args.previous_root or args.previous_benchmark_root
    real_arg = args.real_root or args.paddle_real_root
    if not prev_arg or not real_arg:
        raise SystemExit("must_provide_previous_and_real_roots")
    prev = prev_arg if os.path.isabs(prev_arg) else os.path.abspath(os.path.join(REPO_ROOT, prev_arg))
    real = real_arg if os.path.isabs(real_arg) else os.path.abspath(os.path.join(REPO_ROOT, real_arg))
    out = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))
    os.makedirs(out, exist_ok=True)

    rapid = _load(os.path.join(prev, "provider_summaries", "rapidocr_summary.json"))
    vision = _load(os.path.join(prev, "provider_summaries", "macos_vision_summary.json"))
    paddle_prev = _load(os.path.join(prev, "provider_summaries", "paddleocr_summary.json"))
    paddle_real = _load(os.path.join(real, "paddleocr_real_inference_summary.json"))

    cmp_obj: Dict[str, Any] = {
        "phase": "Phase-ModelOCR-006B",
        "previous_root": os.path.relpath(prev, REPO_ROOT) if prev.startswith(REPO_ROOT) else prev,
        "real_root": os.path.relpath(real, REPO_ROOT) if real.startswith(REPO_ROOT) else real,
        "baseline_rapidocr_metrics": rapid.get("metrics"),
        "baseline_macos_vision_metrics": vision.get("metrics"),
        "previous_paddle_skeleton_metrics": paddle_prev.get("metrics"),
        "real_paddle_metrics": paddle_real.get("metrics"),
        "notes": [
            "rapidocr and macos_vision metrics are reused from 005B baseline",
            "paddle metrics updated with real inference evaluation",
            "this comparison does not set default provider",
        ],
    }
    _write(os.path.join(out, "paddleocr_real_vs_previous_comparison.json"), cmp_obj)

    revised = {
        "rapidocr_005b_baseline": rapid.get("metrics"),
        "macos_vision_005b_baseline": vision.get("metrics"),
        "paddleocr_006a_real_inference": paddle_real.get("metrics"),
    }
    _write(os.path.join(out, "provider_comparison_revised_matrix.json"), revised)

    fairness = {
        "phase": "Phase-ModelOCR-006B",
        "paddleocr_fairness_status": {
            "unfair_current_path": False,
            "real_inference_path_evaluated": True,
            "needs_same_input_same_gt": True,
            "no_default_decision_allowed": True,
        },
        "decision_boundary": "provider default decision remains out of scope for 006A",
    }
    _write(os.path.join(out, "fairness_review_update.json"), fairness)
    print(json.dumps({"ok": True, "output_root": os.path.relpath(out, REPO_ROOT) if out.startswith(REPO_ROOT) else out}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
