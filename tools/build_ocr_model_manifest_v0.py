#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-003: Build/update OCR model manifest (v0).

Hard boundaries:
- Does not download weights.
- Does not run OCR.
- Does not connect to runtime / downstream chains.
- Does not enable semantic interpretation.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import platform
import sys
from typing import Any, Dict, Optional, Tuple


REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _sha256_file(path: str) -> Tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            size += len(b)
            h.update(b)
    return h.hexdigest(), size


def _maybe_file_digest(path: Optional[str]) -> Tuple[Optional[str], Optional[int], Optional[str]]:
    """
    Returns (sha256, size_bytes, status_reason).
    If path is missing or is a directory, does not fake hash.
    """
    if not path:
        return None, None, "missing_path"
    p = os.path.abspath(os.path.join(REPO_ROOT, path)) if not os.path.isabs(path) else path
    if not os.path.exists(p):
        return None, None, "path_not_exists"
    if os.path.isdir(p):
        return None, None, "path_is_dir"
    try:
        sha, size = _sha256_file(p)
        return sha, size, "ok"
    except Exception as e:
        return None, None, f"hash_error:{e}"


def _import_versions() -> Dict[str, Optional[str]]:
    """
    Best-effort dependency version snapshot. Missing deps are left None.
    """
    versions: Dict[str, Optional[str]] = {
        "python_version": ".".join(map(str, sys.version_info[:3])),
        "paddleocr_version": None,
        "paddlepaddle_version": None,
        "opencv_version": None,
        "numpy_version": None,
        "pillow_version": None,
        "platform": platform.platform(),
    }
    try:
        from importlib import metadata as _md  # py>=3.8

        for pkg, key in [
            ("paddleocr", "paddleocr_version"),
            ("paddlepaddle", "paddlepaddle_version"),
            ("opencv-python", "opencv_version"),
            ("numpy", "numpy_version"),
            ("Pillow", "pillow_version"),
        ]:
            try:
                versions[key] = _md.version(pkg)
            except Exception:
                pass
    except Exception:
        pass
    return versions


def _base_manifest(
    *,
    model_config_id: str,
    model_family: str,
    model_name: str,
    model_variant: str,
    candidate_tier: str,
    provider_kind: str,
    weights_source: str,
) -> Dict[str, Any]:
    v = _import_versions()
    return {
        "manifest_version": "v0",
        "model_config_id": model_config_id,
        "model_family": model_family,
        "model_name": model_name,
        "model_variant": model_variant,
        "model_task": "ocr_raw_text_candidates",
        "candidate_tier": candidate_tier,
        "provider_kind": provider_kind,
        "weights_source": weights_source,
        "weights_paths": {
            "det_model_path": None,
            "rec_model_path": None,
            "cls_model_path": None,
            "tokenizer_path": None,
            "other_assets": [],
        },
        "weights_sha256": {},
        "weights_file_size_bytes": {},
        "dependency_profile_id": None,
        "python_version": v.get("python_version"),
        "paddleocr_version": v.get("paddleocr_version"),
        "paddlepaddle_version": v.get("paddlepaddle_version"),
        "opencv_version": v.get("opencv_version"),
        "numpy_version": v.get("numpy_version"),
        "pillow_version": v.get("pillow_version"),
        "platform": platform.system().lower(),
        "supported_languages": ["zh", "en"],
        "supports_chinese": True,
        "supports_english": True,
        "supports_digits": True,
        "supports_bbox": True,
        "supports_confidence": True,
        "supports_orientation": True,
        "supports_layout": False,
        "supports_video_frame_input": True,
        "expected_input_format": "image/frame",
        "expected_output_format": "raw_text_candidates(text,bbox,confidence,frame_id,model_config_id,line_order,raw_text_joined)",
        "raw_text_only": True,
        "semantic_interpretation_enabled": False,
        "allows_execute_now": False,
        "real_tts_invoked": False,
        "created_at": _now_iso(),
        "verified_at": None,
        "verification_status": "pending",
        "fallback_policy": {},
        "risks": [],
        "notes": "",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-family", required=True, choices=["paddleocr", "macos_vision_ocr", "paddleocr_vl", "deepseek_ocr"])
    ap.add_argument("--model-config-id", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--candidate-tier", required=True, choices=["lightweight_navigation_ocr", "complex_layout_ocr", "system_fallback", "comparison_only"])
    ap.add_argument("--provider-kind", default=None, choices=["local_model", "system_provider", "online_or_service", "unavailable"])
    ap.add_argument("--weights-source", default=None, choices=["pinned_local", "pinned_partial", "system_builtin", "manual_download_required", "unavailable"])
    ap.add_argument("--dependency-profile-id", default=None)
    ap.add_argument("--det-path", default=None)
    ap.add_argument("--rec-path", default=None)
    ap.add_argument("--cls-path", default=None)
    ap.add_argument("--tokenizer-path", default=None)
    ap.add_argument("--other-asset", action="append", default=[])
    ap.add_argument("--model-name", default=None)
    ap.add_argument("--model-variant", default=None)
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    mf = str(args.model_family)
    default_name = {
        "paddleocr": "PaddleOCR",
        "macos_vision_ocr": "Apple Vision OCR",
        "paddleocr_vl": "PaddleOCR-VL",
        "deepseek_ocr": "DeepSeek-OCR",
    }[mf]
    default_variant = {
        "paddleocr": "ppocrv5_pipeline",
        "macos_vision_ocr": "VNRecognizeTextRequest",
        "paddleocr_vl": "vl_candidate",
        "deepseek_ocr": "ocr_candidate",
    }[mf]
    provider_kind = args.provider_kind or ("system_provider" if mf == "macos_vision_ocr" else "local_model")
    weights_source = args.weights_source or ("system_builtin" if mf == "macos_vision_ocr" else "manual_download_required")

    manifest = _base_manifest(
        model_config_id=str(args.model_config_id),
        model_family=mf,
        model_name=str(args.model_name or default_name),
        model_variant=str(args.model_variant or default_variant),
        candidate_tier=str(args.candidate_tier),
        provider_kind=str(provider_kind),
        weights_source=str(weights_source),
    )
    manifest["dependency_profile_id"] = args.dependency_profile_id
    manifest["weights_paths"] = {
        "det_model_path": args.det_path,
        "rec_model_path": args.rec_path,
        "cls_model_path": args.cls_path,
        "tokenizer_path": args.tokenizer_path,
        "other_assets": [x for x in (args.other_asset or []) if x],
    }
    manifest["notes"] = str(args.notes or "")

    # Best-effort digests: only compute when a path points to a file.
    sha256: Dict[str, str] = {}
    sizes: Dict[str, int] = {}
    digest_reasons: Dict[str, str] = {}
    for key, path in [
        ("det_model_path", args.det_path),
        ("rec_model_path", args.rec_path),
        ("cls_model_path", args.cls_path),
        ("tokenizer_path", args.tokenizer_path),
    ]:
        h, sz, reason = _maybe_file_digest(path)
        if h and sz is not None:
            sha256[key] = h
            sizes[key] = int(sz)
        if reason:
            digest_reasons[key] = reason
    manifest["weights_sha256"] = sha256
    manifest["weights_file_size_bytes"] = sizes

    # verification_status: never fake pass
    missing_any = any(r in ("missing_path", "path_not_exists") for r in digest_reasons.values())
    if mf == "macos_vision_ocr":
        # system provider: allow pending until checked by readiness tool
        manifest["verification_status"] = "pending"
    else:
        if missing_any:
            manifest["verification_status"] = "pending"
        elif sha256:
            manifest["verification_status"] = "partial"
        else:
            manifest["verification_status"] = "pending"

    out_path = os.path.abspath(os.path.join(REPO_ROOT, str(args.output))) if not os.path.isabs(str(args.output)) else str(args.output)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(
        json.dumps(
            {
                "ok": True,
                "output": os.path.relpath(out_path, REPO_ROOT),
                "model_config_id": manifest["model_config_id"],
                "verification_status": manifest["verification_status"],
                "weights_digests_computed": list(sha256.keys()),
                "digest_reasons": digest_reasons,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

