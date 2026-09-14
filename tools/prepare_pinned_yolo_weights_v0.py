#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelPerception-015
Prepare pinned-local YOLO weights and update manifest.

Hard boundaries:
- Offline only; does not enable runtime
- Does not modify YOLO shadow adapter safety boundaries
- Does not run navigation actions or real TTS

This tool:
- Validates a source weights file exists (no auto-download, no fabrication)
- Copies it to a target path (or validates in-place if source==target)
- Computes sha256 + file size
- Updates manifest fields for pinned_local readiness metadata
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import time
from typing import Any, Dict


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-weights", required=True, help="Existing yolov5*.pt path (must exist)")
    ap.add_argument("--target-weights", required=True, help="Pinned local weights target path (e.g. models/yolo/yolov5n.pt)")
    ap.add_argument("--manifest", required=True, help="Path to configs/models/yolo/yolo_model_manifest_v0.json")
    ap.add_argument("--source-notes", default="", help="Human-readable provenance notes (e.g. download URL)")
    args = ap.parse_args()

    src = os.path.abspath(os.path.expanduser(str(args.source_weights)))
    dst = os.path.abspath(os.path.expanduser(str(args.target_weights)))
    manifest_path = os.path.abspath(os.path.expanduser(str(args.manifest)))

    if not os.path.exists(src):
        raise SystemExit("source_weights_not_found")
    if not os.path.isfile(src):
        raise SystemExit("source_weights_not_a_file")

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.normpath(src) != os.path.normpath(dst):
        shutil.copy2(src, dst)

    sha = _sha256_file(dst)
    size = os.path.getsize(dst)

    manifest = _read_json(manifest_path)
    manifest["weights_source"] = "pinned_local"
    manifest["weights_path"] = os.path.relpath(dst, os.path.dirname(os.path.dirname(os.path.abspath(manifest_path))))
    manifest["weights_sha256"] = sha
    manifest["weights_file_size_bytes"] = size
    manifest["model_loader"] = "torch_hub_yolov5_custom_local_weights"
    manifest["dependency_profile_id"] = "yolo_shadow_v0_pinned_local"
    manifest["reproducibility_risk"] = False
    manifest["verification_status"] = "partial"
    manifest["verified_at"] = None

    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest["notes"] = (manifest.get("notes") or "").strip()
    extra = (str(args.source_notes).strip() or "")
    if extra:
        manifest["notes"] = (manifest["notes"] + " | " + extra).strip(" |")
    if not manifest.get("created_at"):
        manifest["created_at"] = now_iso

    _write_json(manifest_path, manifest)

    out = {
        "phase": "Phase-ModelPerception-015",
        "tool": "prepare_pinned_yolo_weights_v0.py",
        "target_weights_path": dst,
        "target_weights_sha256": sha,
        "target_weights_file_size_bytes": size,
        "manifest_updated": manifest_path,
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

