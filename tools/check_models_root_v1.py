#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check external Luna-Models root layout and pinned assets."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.model_paths_v1 import (
    MODEL_CATEGORIES,
    MODEL_LAYOUT,
    get_models_root,
    resolve_model_path,
)

PINNED_REFS = (
    "vision/detection/yolo/yolov5n.pt",
    "vision/detection/yolo/yolov8n.pt",
    "speech/tts/piper/zh_CN-huayan-medium.onnx",
)


def main() -> int:
    root = get_models_root()
    print(json.dumps({"models_root": str(root), "categories": MODEL_CATEGORIES}, ensure_ascii=False, indent=2))

    missing_layout = [p for p in MODEL_LAYOUT if not (root / p).is_dir()]
    if missing_layout:
        print("layout_dirs_missing:", missing_layout)

    results = []
    ok = True
    for ref in PINNED_REFS:
        path = resolve_model_path(ref, must_exist=True)
        exists = path is not None and path.exists()
        results.append({"ref": ref, "path": str(path), "exists": exists})
        if not exists:
            ok = False

    manifest = root / "manifest_v1.json"
    if manifest.is_file():
        print("manifest:", str(manifest))
    else:
        print("manifest: missing (optional)")

    print(json.dumps({"pinned_assets": results, "all_pinned_present": ok}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
