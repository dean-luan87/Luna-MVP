#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Readiness-001 — Dependency / import probe only (no OCR inference, no PaddleOCR()).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tools.evaluation.ocr.verify_paddleocr_model_manifest_v0 import (  # noqa: E402
    validate_paddleocr_evaluation_readiness_manifest_v0,
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _try_import_module(name: str) -> Tuple[bool, Optional[str], Optional[str]]:
    try:
        m = __import__(name)
        ver = getattr(m, "__version__", None)
        if ver is None and name == "cv2":
            ver = getattr(m, "version", None)
            if callable(ver):
                ver = ver()
        return True, str(ver) if ver is not None else None, None
    except Exception as e:
        return False, None, f"{type(e).__name__}: {e}"


def _try_import_paddleocr_class() -> Tuple[bool, Optional[str]]:
    try:
        from paddleocr import PaddleOCR  # noqa: F401

        return True, None
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def _dependency_matrix() -> List[Dict[str, Any]]:
    rows = []
    for name, label in (
        ("paddleocr", "paddleocr"),
        ("paddle", "paddlepaddle"),
        ("cv2", "opencv-python"),
        ("numpy", "numpy"),
        ("PIL", "pillow"),
    ):
        ok, ver, err = _try_import_module(name)
        rows.append({"import_name": name, "label": label, "import_ok": ok, "version": ver, "error": err})
    p_ok, p_err = _try_import_paddleocr_class()
    rows.append(
        {
            "import_name": "paddleocr.PaddleOCR",
            "label": "paddleocr_class",
            "import_ok": p_ok,
            "version": None,
            "error": p_err,
        }
    )
    return rows


def _import_probe_report(matrix: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "phase": "Phase-PaddleOCR-Readiness-001",
        "policy": "import_only_no_PaddleOCR_constructor_no_inference",
        "rows": matrix,
    }


def _runtime_environment_report() -> Dict[str, Any]:
    cuda_visible = os.environ.get("CUDA_VISIBLE_DEVICES")
    cuda_compiled: Any = None
    try:
        import paddle

        fn = getattr(paddle.device, "is_compiled_with_cuda", None)
        cuda_compiled = bool(fn()) if callable(fn) else None
    except Exception:
        pass
    return {
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "executable": sys.executable,
        "cpu_count": os.cpu_count(),
        "CUDA_VISIBLE_DEVICES": cuda_visible,
        "paddle_cuda_compiled": cuda_compiled,
        "note": "GPU optional; Readiness-001 records environment only.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default="")
    ap.add_argument("--repo-root", default=REPO_ROOT)
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_readiness_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    matrix = _dependency_matrix()
    _write_json(out / "paddleocr_dependency_matrix.json", {"dependencies": matrix})
    _write_json(out / "paddleocr_import_probe_report.json", _import_probe_report(matrix))
    _write_json(out / "paddleocr_runtime_environment_report.json", _runtime_environment_report())

    man_path = repo / "configs" / "models" / "ocr" / "paddleocr_evaluation_readiness_manifest_v0.json"
    manifest_ok = man_path.is_file()
    man_val: Dict[str, Any] = {"verdict": "SKIPPED", "blockers": ["manifest_missing"]}
    if manifest_ok:
        man_val = validate_paddleocr_evaluation_readiness_manifest_v0(
            json.loads(man_path.read_text(encoding="utf-8"))
        )

    paddleocr_pkg_ok = next((r["import_ok"] for r in matrix if r["import_name"] == "paddleocr"), False)
    paddleocr_class_ok = next((r["import_ok"] for r in matrix if r["import_name"] == "paddleocr.PaddleOCR"), False)

    summary = {
        "phase": "Phase-PaddleOCR-Readiness-001",
        "repo_root": str(repo),
        "output_root": str(out),
        "manifest_path": str(man_path),
        "manifest_present": manifest_ok,
        "manifest_validation": man_val,
        "paddleocr_package_import_ok": paddleocr_pkg_ok,
        "paddleocr_class_import_ok": paddleocr_class_ok,
        "readiness_posture": "GO"
        if paddleocr_pkg_ok and paddleocr_class_ok and man_val.get("verdict") == "GO"
        else "CONDITIONAL_GO_dependency_or_manifest_gap",
        "verdict": "GO"
        if man_val.get("verdict") == "GO" and paddleocr_pkg_ok and paddleocr_class_ok
        else "CONDITIONAL_GO",
        "constraints": {
            "paddleocr_inference_invoked": False,
            "paddleocr_constructor_invoked": False,
            "ocr_provider_trial_executed": False,
            "rapidocr_replaced": False,
            "mainline_routing_changed": False,
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "midplatform_invoked": False,
        },
    }
    _write_json(out / "paddleocr_readiness_summary.json", summary)

    notes = out / "paddleocr_readiness_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# PaddleOCR Readiness (Evaluation-001)",
                "",
                f"- **output_root**: `{out}`",
                "",
                "- **No OCR inference**: import probes only; `PaddleOCR()` not called.",
                "- **RapidOCR remains mainline**; `mainline_provider=false` in evaluation readiness manifest.",
                "",
                f"- **verdict**: `{summary['verdict']}`",
                f"- **readiness_posture**: `{summary['readiness_posture']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": summary["verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
