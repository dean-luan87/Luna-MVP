#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelPerception-014
Build/update YOLO model manifest v0 (offline).

Hard boundaries:
- Does not run navigation actions or TTS.
- Does not integrate into runtime.
- Only inspects local environment and optional local weights file.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import platform
import sys
import time
from typing import Any, Dict, Optional


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _try_import_version(mod_name: str) -> Optional[str]:
    try:
        mod = importlib.import_module(mod_name)
        return getattr(mod, "__version__", None)
    except Exception:  # noqa: BLE001
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, help="Path to yolo_model_manifest_v0.json")
    ap.add_argument("--base-manifest", default="", help="Optional existing manifest to start from")
    ap.add_argument("--weights-source", required=True, choices=["pinned_local", "torch_hub_dev", "unavailable"])
    ap.add_argument("--weights-path", default="", help="Optional local weights path when weights-source=pinned_local")
    ap.add_argument("--model-config-id", default="yolo_shadow_v0", help="Stable model_config_id")
    ap.add_argument("--notes", default="", help="Optional notes")
    args = ap.parse_args()

    manifest: Dict[str, Any] = {}
    if args.base_manifest:
        if os.path.exists(args.base_manifest):
            manifest = _read_json(args.base_manifest)

    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    weights_path = args.weights_path or None

    weights_sha256 = None
    weights_size = None
    if args.weights_source == "pinned_local":
        if not weights_path or not os.path.exists(weights_path):
            raise SystemExit("pinned_local_requires_existing_weights_path")
        weights_sha256 = _sha256_file(weights_path)
        weights_size = os.path.getsize(weights_path)

    # Dependency versions (best-effort)
    dep_versions = {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "torch_version": _try_import_version("torch"),
        "torchvision_version": _try_import_version("torchvision"),
        "opencv_version": _try_import_version("cv2"),
        "numpy_version": _try_import_version("numpy"),
        "pandas_version": _try_import_version("pandas"),
        "seaborn_version": _try_import_version("seaborn"),
        "pillow_version": _try_import_version("PIL"),
    }

    manifest.update(
        {
            "manifest_version": "v0",
            "model_config_id": str(args.model_config_id),
            "model_family": "yolo",
            "model_name": "yolov5",
            "model_variant": "n",
            "model_task": "object_detection",
            "weights_source": args.weights_source,
            "weights_path": weights_path,
            "weights_sha256": weights_sha256,
            "weights_file_size_bytes": weights_size,
            "model_loader": "pinned_local_weights" if args.weights_source == "pinned_local" else "torch_hub_ultralytics_yolov5_pretrained",
            "expected_input_format": "numpy_bgr_or_rgb_image",
            "expected_output_format": "detections_xyxy_conf_cls",
            "dependency_profile_id": "yolo_shadow_v0_pinned" if args.weights_source == "pinned_local" else "yolo_shadow_v0_py_torchhub_dev",
            **dep_versions,
            "platform": f"{platform.system().lower()}-{platform.machine().lower()}",
            "created_at": manifest.get("created_at") or now_iso,
            "verified_at": manifest.get("verified_at") or None,
            "verification_status": manifest.get("verification_status") or "partial",
            "reproducibility_risk": True if args.weights_source == "torch_hub_dev" else False,
            "fallback_policy": "fallback_to_baseline_mock_on_any_mismatch_or_failure",
            "notes": (str(args.notes).strip() or manifest.get("notes") or ""),
        }
    )

    _write_json(args.output, manifest)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

