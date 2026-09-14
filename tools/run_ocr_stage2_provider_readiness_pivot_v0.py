#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-011-Pivot — Provider Readiness (Static) v0.

Purpose:
- Static readiness probe for RapidOCR / PaddleOCR (no OCR invocation).
- Writes a single JSON report under an absolute --output-root.

Hard boundaries:
- MUST NOT invoke any OCR provider inference.
- MUST NOT make network requests.
- MUST NOT enter semantic interpretation / MidPlatform / SceneDelta / WorldContext.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import sys
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Dict, Optional


_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _require_abs_dir(p: str) -> Path:
    root = Path(p).expanduser()
    if not root.is_absolute():
        raise SystemExit("output_root_must_be_absolute")
    root.mkdir(parents=True, exist_ok=True)
    return root.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _spec_ok(name: str) -> Dict[str, Any]:
    t0 = time.perf_counter()
    spec = find_spec(name)
    return {
        "module": name,
        "spec_found": bool(spec is not None),
        "probe_ms": round((time.perf_counter() - t0) * 1000.0, 3),
    }


def _paddle_readiness_best_effort(repo_root: Optional[str]) -> Dict[str, Any]:
    try:
        from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0

        a = PaddleOCRAdapterV0(enable_real_inference=False)
        rd = a.evaluate_readiness()
        # sanitize: ensure we never accidentally claim inference
        rd["enable_real_inference"] = False
        return {"ok": True, "readiness": rd}
    except Exception as e:
        return {"ok": False, "error": repr(e)}


def _rapidocr_readiness_best_effort(repo_root: Optional[str]) -> Dict[str, Any]:
    try:
        from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

        a = RapidOCRAdapterV0()
        ok, err = a.is_available()
        ar = a.asset_report(repo_root=repo_root or os.getcwd())
        return {
            "ok": True,
            "available": bool(ok),
            "error": err,
            "asset_report": ar,
        }
    except Exception as e:
        return {"ok": False, "error": repr(e)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--repo-root", required=False, default=None)
    args = ap.parse_args()

    out_root = _require_abs_dir(args.output_root)
    repo_root = args.repo_root

    report: Dict[str, Any] = {
        "tool": "run_ocr_stage2_provider_readiness_pivot_v0",
        "mode": "static_readiness_only",
        "repo_root": repo_root,
        "output_root": str(out_root),
        "hard_boundaries": {
            "ocr_provider_invoked": False,
            "ocr_model_invoked": False,
            "network_request_invoked": False,
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
        },
        "python_module_specs": {
            "rapidocr_onnxruntime": _spec_ok("rapidocr_onnxruntime"),
            "onnxruntime": _spec_ok("onnxruntime"),
            "paddle": _spec_ok("paddle"),
            "paddleocr": _spec_ok("paddleocr"),
            "cv2": _spec_ok("cv2"),
            "PIL": _spec_ok("PIL"),
            "numpy": _spec_ok("numpy"),
        },
        "providers": {
            "rapidocr_onnxruntime_v0": _rapidocr_readiness_best_effort(repo_root),
            "paddleocr_ppocrv5_lightweight_v0": _paddle_readiness_best_effort(repo_root),
        },
        "recommendation": None,
        "soft_followups": [],
        "hard_blockers": [],
    }

    # Recommendation (static)
    spec_rapid = report["python_module_specs"]["rapidocr_onnxruntime"]["spec_found"]
    if spec_rapid:
        report["recommendation"] = "prefer_rapidocr_onnxruntime_v0"
    else:
        report["soft_followups"].append("install_rapidocr_onnxruntime_and_onnxruntime")
    pad_ok = bool(report["providers"]["paddleocr_ppocrv5_lightweight_v0"].get("ok"))
    if not pad_ok:
        report["soft_followups"].append("paddle_adapter_probe_failed")

    _write_json(out_root / "ocr_stage2_provider_readiness_pivot_report.json", report)
    print(json.dumps({"ok": True, "output_root": str(out_root)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

