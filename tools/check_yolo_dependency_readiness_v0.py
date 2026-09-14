#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-ModelPerceptionFix-002

Check YOLO dependency & weight readiness for the YOLOv5 torch.hub path used by:
- Luna_Badge_MVP/vision/yolov5_detector.py

Hard boundaries:
- This tool does not run inference on user media.
- Optional dry-run model load is allowed (initialize only).
- Produces structured JSON output for audit.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


DEFAULT_MODULES = [
    "torch",
    "torchvision",
    "cv2",
    "numpy",
    "pandas",
    "seaborn",
    "PIL",
]


def _try_import(name: str) -> Dict[str, Any]:
    try:
        mod = importlib.import_module(name)
        ver = getattr(mod, "__version__", None)
        path = getattr(mod, "__file__", None)
        return {"module": name, "ok": True, "version": ver, "file": path, "error": None}
    except Exception as e:  # noqa: BLE001
        return {"module": name, "ok": False, "version": None, "file": None, "error": f"{type(e).__name__}:{e}"}


def _dry_run_model_load(model_path: str) -> Dict[str, Any]:
    """
    Attempt to import and initialize YOLOv5Detector.
    This may trigger torch.hub to use local cache; it should not run inference.
    """
    try:
        from Luna_Badge_MVP.vision.yolov5_detector import YOLOv5Detector  # type: ignore

        det = YOLOv5Detector()
        ok = bool(det.initialize(model_path=model_path))
        info = det.get_model_info() if hasattr(det, "get_model_info") else {}
        return {"attempted": True, "ok": ok, "model_info": info, "error": None}
    except Exception as e:  # noqa: BLE001
        return {"attempted": True, "ok": False, "model_info": {}, "error": f"{type(e).__name__}:{e}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-json", required=True)
    ap.add_argument("--modules", nargs="*", default=DEFAULT_MODULES)
    ap.add_argument("--dry-run-model-load", default="false", choices=["true", "false"])
    ap.add_argument("--model-path", default="yolov5n.pt")
    args = ap.parse_args()

    modules = [str(m) for m in (args.modules or [])]
    checks = [_try_import(m) for m in modules]

    dry = None
    if str(args.dry_run_model_load).lower() == "true":
        dry = _dry_run_model_load(model_path=str(args.model_path))

    report: Dict[str, Any] = {
        "phase": "Phase-ModelPerceptionFix-002",
        "tool": "check_yolo_dependency_readiness_v0.py",
        "generated_at_s": time.time(),
        "python": {
            "executable": sys.executable,
            "version": sys.version,
        },
        "modules_checked": checks,
        "dry_run_model_load": dry,
        "summary": {
            "import_ok_count": sum(1 for c in checks if c["ok"]),
            "import_fail_count": sum(1 for c in checks if not c["ok"]),
            "missing_modules": [c["module"] for c in checks if not c["ok"]],
            "dry_run_attempted": bool(dry and dry.get("attempted")),
            "dry_run_ok": bool(dry and dry.get("ok")),
        },
        "notes": [
            "This is a readiness check only; it does not run inference on user media.",
            "If dry-run is enabled, it only attempts to initialize the YOLOv5Detector model loader.",
        ],
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=False)

    print(args.output_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

