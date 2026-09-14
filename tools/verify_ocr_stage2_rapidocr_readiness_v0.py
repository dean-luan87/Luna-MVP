#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Phase-012 RapidOCR readiness artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty_jsonl(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = Path(args.output_root).expanduser().resolve()
    if not Path(args.output_root).expanduser().is_absolute():
        raise SystemExit("ERROR: --output-root must be absolute")

    results: List[Dict[str, Any]] = []
    results.append(_case("A_output_exists", out_root.is_dir(), {"output_root": str(out_root)}))

    files = [
        "ocr_stage2_rapidocr_readiness_summary.json",
        "ocr_stage2_rapidocr_dependency_snapshot.json",
        "ocr_stage2_rapidocr_provider_contract.json",
        "ocr_stage2_rapidocr_fallback_policy.json",
        "ocr_stage2_rapidocr_trace.jsonl",
        "ocr_stage2_rapidocr_replay.jsonl",
        "ocr_stage2_rapidocr_whitebox.jsonl",
        "readiness_notes.md",
    ]
    for fn in files:
        p = out_root / fn
        ok = p.is_file()
        if fn.endswith(".jsonl"):
            ok = ok and _nonempty_jsonl(p)
        elif fn.endswith(".md"):
            ok = ok and _nonempty_jsonl(p)
        results.append(_case(f"file_{fn}", ok, {"path": str(p)}))

    dep = _read_json(out_root / "ocr_stage2_rapidocr_dependency_snapshot.json")
    mods = dep.get("modules") or {}
    results.append(_case("rapidocr_importable", bool(mods.get("rapidocr_onnxruntime")), {"modules": mods}))
    results.append(_case("onnxruntime_importable", bool(mods.get("onnxruntime")), {"modules": mods}))

    summ = _read_json(out_root / "ocr_stage2_rapidocr_readiness_summary.json")
    results.append(_case("provider_invoked_false", summ.get("provider_invoked") is False, {"summary": summ}))
    results.append(_case("ocr_model_invoked_false", summ.get("ocr_model_invoked") is False, {"summary": summ}))
    results.append(_case("network_false", summ.get("network_request_invoked") is False, {"summary": summ}))
    results.append(_case("semantic_false", summ.get("semantic_interpretation_enabled") is False, {"summary": summ}))
    results.append(_case("midplatform_false", summ.get("midplatform_invoked") is False, {"summary": summ}))

    fb = _read_json(out_root / "ocr_stage2_rapidocr_fallback_policy.json")
    results.append(_case("macos_vision_not_mainline", fb.get("macos_vision_mainline") is False, {"fallback": fb}))

    all_ok = all(r["ok"] for r in results)
    verdict = "GO" if all_ok else "NO_GO"
    print(json.dumps({"verifier": "verify_ocr_stage2_rapidocr_readiness_v0", "verdict": verdict, "output_root": str(out_root), "results": results}, ensure_ascii=False, indent=2))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
