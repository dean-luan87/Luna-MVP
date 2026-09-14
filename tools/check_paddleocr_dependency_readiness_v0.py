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


def _now() -> str:
    return _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json")
    ap.add_argument("--output", default=None, help="default: logs/paddleocr_dependency_readiness_004b_<ts>.json")
    args = ap.parse_args()

    from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0

    ad = PaddleOCRAdapterV0(manifest_path=args.manifest)
    rd = ad.evaluate_readiness()

    out = {
        "phase": "Phase-ModelOCR-004B",
        "tool": "check_paddleocr_dependency_readiness_v0.py",
        "timestamp": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "manifest_readable": "manifest_missing" not in (rd.get("hard_blockers") or []),
        "dependency_status": rd.get("dependency_status"),
        "weights_status": rd.get("weights_status"),
        "raw_text_only": bool((rd.get("capability_boundary") or {}).get("raw_text_only") is True),
        "semantic_interpretation_enabled": bool((rd.get("capability_boundary") or {}).get("semantic_interpretation_enabled")),
        "fallback_candidates": rd.get("fallback_candidates"),
        "provider_available": rd.get("provider_available"),
        "readiness_status": rd.get("readiness_status"),
        "fail_closed": rd.get("fail_closed"),
        "hard_blockers": rd.get("hard_blockers"),
        "soft_followups": rd.get("soft_followups"),
    }

    out_path = args.output or f"logs/paddleocr_dependency_readiness_004b_{_now()}.json"
    out_abs = out_path if os.path.isabs(out_path) else os.path.abspath(os.path.join(REPO_ROOT, out_path))
    _write_json(out_abs, out)

    print(
        json.dumps(
            {
                "ok": len(out.get("hard_blockers") or []) == 0,
                "output": os.path.relpath(out_abs, REPO_ROOT) if out_abs.startswith(REPO_ROOT) else out_abs,
                "readiness_status": out.get("readiness_status"),
                "fail_closed": out.get("fail_closed"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if not out.get("hard_blockers") else 2


if __name__ == "__main__":
    raise SystemExit(main())
