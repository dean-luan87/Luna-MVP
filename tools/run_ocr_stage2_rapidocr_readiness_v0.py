#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-012 — RapidOCR provider readiness (static + import probe, no OCR inference).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _module_spec(name: str) -> Dict[str, Any]:
    sp = find_spec(name)
    return {"module": name, "importable": bool(sp is not None)}


def _build_dependency_snapshot() -> Dict[str, Any]:
    modules = ["rapidocr_onnxruntime", "onnxruntime", "cv2", "numpy", "PIL"]
    per = [_module_spec(m) for m in modules]
    rapidocr_probe: Dict[str, Any] = {"ok": False, "available": False, "error": None, "asset_report": None}
    try:
        from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

        a = RapidOCRAdapterV0()
        ok, err = a.is_available()
        ar = a.asset_report(repo_root=REPO_ROOT)
        rapidocr_probe = {"ok": True, "available": bool(ok), "error": err, "asset_report": ar, "provider_id": a.provider_id}
    except Exception as e:
        rapidocr_probe["error"] = repr(e)

    return {
        "phase": "Phase-Mainline-GuardedTrial-012",
        "ts": _now_iso(),
        "modules": {m["module"]: m["importable"] for m in per},
        "module_details": per,
        "rapidocr_adapter_probe": rapidocr_probe,
        "network_request_invoked": False,
        "provider_invoked": False,
        "ocr_model_invoked": False,
    }


def _provider_contract() -> Dict[str, Any]:
    return {
        "provider_id": "rapidocr_onnxruntime_v0",
        "model_config_id": "rapidocr_onnxruntime_v0",
        "adapter_module": "capabilities.model_ocr.rapidocr_adapter_v0.RapidOCRAdapterV0",
        "recognize_method": "recognize_image",
        "output_envelope_keys": [
            "sample_id",
            "provider_id",
            "model_config_id",
            "ocr_runtime_mode",
            "semantic_interpretation_enabled",
            "raw_text_candidates",
            "raw_text_joined",
            "hard_blockers",
            "provider_details",
        ],
        "semantic_interpretation_enabled_default": False,
        "midplatform_forward_default": False,
    }


def _fallback_policy() -> Dict[str, Any]:
    return {
        "phase": "Phase-Mainline-GuardedTrial-012",
        "mainline_order": ["rapidocr_onnxruntime_v0", "paddleocr_ppocrv5_lightweight_v0", "not_available"],
        "macos_vision_mainline": False,
        "notes": [
            "Controlled Stage-2 executor selects RapidOCR then PaddleOCR; macOS Vision is not a mainline selectable provider.",
            "When RapidOCR unavailable, fall through per executor (PaddleOCR / not_available).",
        ],
    }


def _readiness_summary(dep: Dict[str, Any]) -> Dict[str, Any]:
    ra = dep.get("rapidocr_adapter_probe") or {}
    mods = dep.get("modules") or {}
    ok_rr = bool(mods.get("rapidocr_onnxruntime"))
    ok_ort = bool(mods.get("onnxruntime"))
    avail = bool(ra.get("available"))
    gates_ok = ok_rr and ok_ort and avail
    return {
        "readiness_id": f"ocr_s2_rapidocr_ready_{_now_iso().replace(':', '')}",
        "readiness_result": "GO" if gates_ok else "NO_GO",
        "rapidocr_onnxruntime_importable": ok_rr,
        "onnxruntime_importable": ok_ort,
        "rapidocr_adapter_available": avail,
        "semantic_interpretation_enabled": False,
        "scene_delta_invoked": False,
        "world_context_invoked": False,
        "midplatform_invoked": False,
        "provider_invoked": False,
        "ocr_model_invoked": False,
        "network_request_invoked": False,
        "blockers": [] if gates_ok else ["rapidocr_readiness_not_met"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    dep = _build_dependency_snapshot()
    summary = _readiness_summary(dep)
    contract = _provider_contract()
    fb = _fallback_policy()

    _write_json(out_root / "ocr_stage2_rapidocr_readiness_summary.json", summary)
    _write_json(out_root / "ocr_stage2_rapidocr_dependency_snapshot.json", dep)
    _write_json(out_root / "ocr_stage2_rapidocr_provider_contract.json", contract)
    _write_json(out_root / "ocr_stage2_rapidocr_fallback_policy.json", fb)

    rid = summary.get("readiness_id") or "unknown"
    ha = {
        "semantic_interpretation_enabled": False,
        "midplatform_invoked": False,
        "scene_delta_invoked": False,
        "world_context_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_model_invoked": False,
        "network_request_invoked": False,
        "qwen_invoked": False,
        "real_tts_invoked": False,
        "playback_invoked": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "world_write_invoked": False,
        "hive_upload_invoked": False,
    }
    _append_jsonl(out_root / "ocr_stage2_rapidocr_trace.jsonl", {"type": "ocr_s2_rapidocr_trace_v0", "ts": _now_iso(), "readiness_id": rid, "hard_audit": ha})
    _append_jsonl(out_root / "ocr_stage2_rapidocr_replay.jsonl", {"type": "ocr_s2_rapidocr_replay_v0", "ts": _now_iso(), "readiness_id": rid})
    _append_jsonl(out_root / "ocr_stage2_rapidocr_whitebox.jsonl", {"type": "ocr_s2_rapidocr_whitebox_v0", "ts": _now_iso(), "readiness_id": rid, "hard_audit": ha})

    notes = "\n".join(
        [
            "# OCR Stage-2 RapidOCR Readiness v0 (Phase-012)",
            "",
            "- Static/import probes only; **no** OCR inference in this step.",
            "- No MidPlatform / semantic interpretation.",
            "",
            f"- **output_root:** `{out_root}`",
            f"- **readiness_result:** `{summary.get('readiness_result')}`",
            "",
        ]
    )
    (out_root / "readiness_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "readiness_result": summary.get("readiness_result")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
