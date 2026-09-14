#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from typing import Any, Dict

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _rel(p: str) -> str:
    return os.path.relpath(p, REPO_ROOT) if p.startswith(REPO_ROOT) else p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json")
    ap.add_argument("--output-root", required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-only", action="store_true")
    mode.add_argument("--init-only", action="store_true")
    args = ap.parse_args()

    out_root = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))
    os.makedirs(out_root, exist_ok=True)

    from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0

    ad = PaddleOCRAdapterV0(manifest_path=args.manifest)
    readiness = ad.evaluate_readiness()
    init_out: Dict[str, Any] = {"attempted": False, "ok": False, "error": "check_only_mode"}
    if args.init_only:
        init_out = ad.dry_init_only()

    sample = ad.recognize_image(
        image_path="__not_used_in_004b__",
        frame_id="smoke_000",
        timestamp_ms=0,
    )
    # 004B hard boundary
    sample["semantic_interpretation_enabled"] = False
    sample["allows_execute_now"] = False
    sample["real_tts_invoked"] = False

    trace_path = os.path.join(out_root, "paddleocr_adapter_trace.jsonl")
    whitebox_path = os.path.join(out_root, "paddleocr_adapter_whitebox.jsonl")
    readiness_path = os.path.join(out_root, "paddleocr_adapter_readiness.json")
    summary_path = os.path.join(out_root, "paddleocr_adapter_skeleton_summary.json")

    with open(trace_path, "w", encoding="utf-8") as tf:
        tf.write(
            json.dumps(
                {
                    "event": "paddleocr_adapter_skeleton",
                    "mode": "init-only" if args.init_only else "check-only",
                    "provider_id": sample.get("provider_id"),
                    "ts": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
                },
                ensure_ascii=False,
            )
            + "\n"
        )
    with open(whitebox_path, "w", encoding="utf-8") as wf:
        wf.write(
            json.dumps(
                {
                    "readiness": readiness,
                    "init_only": init_out,
                    "sample": {
                        "provider_available": sample.get("provider_details", {}).get("provider_available"),
                        "fail_closed": sample.get("provider_details", {}).get("fail_closed"),
                    },
                },
                ensure_ascii=False,
            )
            + "\n"
        )
    _write_json(readiness_path, readiness)

    summary = {
        "phase": "Phase-ModelOCR-004B",
        "tool": "smoke_paddleocr_adapter_skeleton_v0.py",
        "mode": "init-only" if args.init_only else "check-only",
        "manifest": args.manifest,
        "provider_id": sample.get("provider_id"),
        "model_config_id": sample.get("model_config_id"),
        "ocr_runtime_mode": sample.get("ocr_runtime_mode"),
        "provider_available": readiness.get("provider_available"),
        "readiness_status": readiness.get("readiness_status"),
        "fail_closed": readiness.get("fail_closed"),
        "dependency_status": readiness.get("dependency_status"),
        "weights_status": readiness.get("weights_status"),
        "capability_boundary": readiness.get("capability_boundary"),
        "fallback_candidates": readiness.get("fallback_candidates"),
        "init_only": init_out,
        "sample_contract": {
            "raw_text_candidates_count": len(sample.get("raw_text_candidates") or []),
            "semantic_interpretation_enabled": sample.get("semantic_interpretation_enabled"),
            "allows_execute_now": sample.get("allows_execute_now"),
            "real_tts_invoked": sample.get("real_tts_invoked"),
        },
        "artifacts": {
            "trace": _rel(trace_path),
            "whitebox": _rel(whitebox_path),
            "readiness": _rel(readiness_path),
            "summary": _rel(summary_path),
        },
        "hard_blockers": readiness.get("hard_blockers") or [],
        "soft_followups": readiness.get("soft_followups") or [],
    }
    _write_json(summary_path, summary)
    print(json.dumps({"ok": True, "output_root": _rel(out_root), "mode": summary["mode"], "fail_closed": summary["fail_closed"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
