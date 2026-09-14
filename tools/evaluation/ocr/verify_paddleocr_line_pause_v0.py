#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Phase-PaddleOCR-LinePause-001 outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pause-root", required=True)
    args = ap.parse_args()
    root = Path(args.pause_root).expanduser().resolve()
    blockers: List[str] = []

    required = [
        "paddleocr_line_pause_summary.json",
        "paddleocr_resume_criteria.json",
        "paddleocr_blocker_register.json",
        "paddleocr_next_allowed_action.json",
        "notes.md",
    ]
    for fn in required:
        if not (root / fn).is_file():
            blockers.append(f"missing:{fn}")

    if not blockers:
        sm = _read_json(root / "paddleocr_line_pause_summary.json")
        if sm.get("line_status") != "paused":
            blockers.append("pause_status_unclear")
        c = sm.get("constraints") or {}
        for k in (
            "weights_downloaded_in_this_phase",
            "paddleocr_constructor_invoked",
            "paddleocr_inference_invoked",
            "rapidocr_replaced",
            "ocr_routing_changed",
        ):
            if c.get(k) is not False:
                blockers.append(f"constraint:{k}")

    verdict = "GO" if not blockers else "NO_GO"
    rep = {"phase": "Phase-PaddleOCR-LinePause-001", "verdict": verdict, "blockers": blockers, "pause_root": str(root)}
    (root / "paddleocr_line_pause_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(rep, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
