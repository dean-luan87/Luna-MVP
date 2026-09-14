#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _write(path: str, obj) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0

    adapter = PaddleOCRAdapterV0(manifest_path=args.manifest, enable_real_inference=True, config_profile="config_init_once")
    rd = adapter.evaluate_readiness()
    ev = {}
    lock_status = "unknown"
    reason = ""
    incompat = None
    try:
        ocr = adapter._build_engine()  # noqa: SLF001
        ev = adapter._runtime_model_evidence(ocr)  # noqa: SLF001
        lock_status = str(ev.get("model_path_lock_status") or "unknown")
        reason = str(ev.get("model_path_lock_reason") or "")
    except Exception as e:
        incompat = repr(e)
        reason = incompat
    out = {
        "phase": "Phase-ModelOCR-006C",
        "manifest": args.manifest,
        "readiness": rd,
        "runtime_model_evidence": ev,
        "model_path_lock_status": lock_status,
        "model_path_lock_reason": reason,
        "incompatibility_reason": incompat,
    }
    op = args.output if os.path.isabs(args.output) else os.path.abspath(os.path.join(REPO_ROOT, args.output))
    _write(op, out)
    print(json.dumps({"ok": True, "output": os.path.relpath(op, REPO_ROOT) if op.startswith(REPO_ROOT) else op}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
