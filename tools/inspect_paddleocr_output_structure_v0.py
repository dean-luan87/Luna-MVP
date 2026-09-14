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


def _keys_tree(obj: Any, prefix: str = "") -> List[str]:
    out: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            out.append(p)
            out.extend(_keys_tree(v, p))
    elif isinstance(obj, list) and obj:
        out.extend(_keys_tree(obj[0], f"{prefix}[]"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-manifest", required=True)
    ap.add_argument("--sample-ids", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    man = _load(args.dataset_manifest if os.path.isabs(args.dataset_manifest) else os.path.abspath(os.path.join(REPO_ROOT, args.dataset_manifest)))
    out = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))
    os.makedirs(out, exist_ok=True)
    sids = [x.strip() for x in str(args.sample_ids).split(",") if x.strip()]
    smap: Dict[str, Any] = {str(s.get("sample_id")): s for s in (man.get("samples") or []) if isinstance(s, dict)}

    from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0
    adapter = PaddleOCRAdapterV0(enable_real_inference=True, config_profile="config_init_once")

    raw_repr: Dict[str, str] = {}
    raw_json: Dict[str, Any] = {}
    keys: Dict[str, List[str]] = {}
    bbox_candidates: Dict[str, Any] = {}
    preview: Dict[str, Any] = {}
    for sid in sids:
        s = smap.get(sid)
        if not s:
            continue
        img = str(s.get("image_path") or "")
        img_abs = img if os.path.isabs(img) else os.path.abspath(os.path.join(REPO_ROOT, img))
        r = adapter.recognize_image(image_path=img_abs, frame_id=str(s.get("frame_id") or sid), timestamp_ms=int(s.get("timestamp_ms") or 0))
        raw_json[sid] = r
        raw_repr[sid] = repr(r)[:2000]
        keys[sid] = _keys_tree(r)
        pd = r.get("provider_details") or {}
        bbox_candidates[sid] = {
            "bbox_source_report": pd.get("bbox_source_report"),
            "coordinate_conversion_status": pd.get("coordinate_conversion_status"),
            "raw_output_shape_report": pd.get("raw_output_shape_report"),
        }
        preview[sid] = {
            "raw_text_joined": r.get("raw_text_joined"),
            "candidate_count": len(r.get("raw_text_candidates") or []),
            "first_candidates": (r.get("raw_text_candidates") or [])[:5],
        }

    with open(os.path.join(out, "raw_result_repr.txt"), "w", encoding="utf-8") as f:
        for sid in sids:
            if sid in raw_repr:
                f.write(f"## {sid}\n{raw_repr[sid]}\n\n")
    _write(os.path.join(out, "raw_result_json_attempt.json"), raw_json)
    _write(os.path.join(out, "raw_result_keys.json"), keys)
    _write(os.path.join(out, "bbox_field_candidates.json"), bbox_candidates)
    _write(os.path.join(out, "normalized_candidate_preview.json"), preview)
    print(json.dumps({"ok": True, "output_root": os.path.relpath(out, REPO_ROOT) if out.startswith(REPO_ROOT) else out}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
