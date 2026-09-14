#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-002 — Validate Chinese fonts for synthetic OCR generation v0.

Evaluation Tools only. Does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_chinese_font_registry_v0 import (  # noqa: E402
    PROBE_TEXT,
    scan_chinese_fonts_v0,
    select_best_cjk_font_v0,
    validate_cjk_font_visibility_v0,
)


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--font-dir", action="append", default=[], help="Optional extra font directories (repeatable)")
    args = ap.parse_args()

    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    reg = scan_chinese_fonts_v0(font_dirs=list(args.font_dir) if args.font_dir else None)
    sel = select_best_cjk_font_v0(reg)

    # Build probe images for the selected font (if any)
    probe_dir = out_root / "chinese_font_probe_images"
    probe_dir.mkdir(parents=True, exist_ok=True)
    visibility_report = None
    if sel.get("ok") and sel.get("selected"):
        font_path = str((sel["selected"] or {}).get("font_path") or "")
        visibility_report = validate_cjk_font_visibility_v0(font_path)
        # Render probe text image to visually inspect
        try:
            from PIL import Image
            from capabilities.evaluation.ocr.ocr_chinese_font_registry_v0 import _render_text_mask  # type: ignore

            img = _render_text_mask(font_path, PROBE_TEXT, size=30).convert("RGB")
            img.save(str(probe_dir / "probe_text.png"))
        except Exception as e:
            if visibility_report is None:
                visibility_report = {"error": repr(e), "validation_result": "NO_GO"}

    summary: Dict[str, Any] = {
        "phase": "Phase-EvaluationTools-OCR-002",
        "tool": "validate_chinese_fonts_for_ocr_synthetic_v0",
        "ts": _now_iso(),
        "output_root": str(out_root),
        "probe_text": PROBE_TEXT,
        "registry_count": int(reg.get("count") or 0),
        "selected_font": sel,
        "visibility_report": visibility_report,
        "hard_audit": {
            "ocr_provider_invoked": False,
            "network_request_invoked": False,
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "runtime_integration": False,
            "whitebox_integration": False,
        },
    }

    _write_json(out_root / "chinese_font_registry.json", reg)
    _write_json(out_root / "chinese_font_selection_report.json", sel)
    _write_json(out_root / "chinese_font_visibility_report.json", visibility_report or {"validation_result": "NO_GO"})
    _write_json(out_root / "font_validation_summary.json", summary)
    notes = "\n".join(
        [
            "# Chinese font validation (Evaluation Tools) v0",
            "",
            f"- **output_root:** `{summary['output_root']}`",
            f"- **registry_count:** `{summary['registry_count']}`",
            f"- **selected_ok:** `{bool(sel.get('ok'))}`",
            "",
            "## Boundary",
            "",
            "- Evaluation Tools only; no runtime/whitebox integration.",
            "- No OCR provider invocation.",
            "",
        ]
    )
    (out_root / "font_validation_notes.md").write_text(notes + "\n", encoding="utf-8")

    ok = bool(sel.get("ok")) and bool((visibility_report or {}).get("validation_result") == "GO")
    print(json.dumps({"ok": True, "output_root": str(out_root), "font_selected": bool(sel.get("ok")), "visible_cjk_passed": ok}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

