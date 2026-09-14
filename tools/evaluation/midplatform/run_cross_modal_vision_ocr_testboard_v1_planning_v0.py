#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-Planning-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--v0-closure-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    v0 = _require_abs(args.v0_closure_root, "--v0-closure-root")

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_v1_planning_v0 import (
        run_cross_modal_vision_ocr_testboard_v1_planning_v0,
    )

    (
        summary,
        track_matrix,
        phase_roadmap,
        non_goals,
        risk_register,
        gate_policy,
        execution_order,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_testboard_v1_planning_v0(v0_closure_root=str(v0))

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_vision_ocr_testboard_v1_planning_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_track_matrix.json", track_matrix)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_phase_roadmap.json", phase_roadmap)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_non_goals_report.json", non_goals)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_risk_register.json", risk_register)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_gate_policy.json", gate_policy)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_execution_order.json", execution_order)
    _write_json(out / "cross_modal_vision_ocr_testboard_v1_planning_audit_report.json", audit)

    exec_steps = execution_order.get("recommended_execution_order") or []
    notes_lines = [
        "# CrossModal Vision OCR TestBoard v1 Planning",
        "",
        "Planning freeze only — no v1 implementation, no OCR, no Vision provider.",
        "",
        f"v0_closure_root: {v0}",
        "",
        "## Tracks",
        "- TVOCR_V1_A_REAL_VIDEO — real video frames / natural ROI",
        "- TVOCR_V1_B_POSTER_LAYOUT — governance → segmentation → regional OCR",
        "- TVOCR_V1_C_BENCHMARK_PERFORMANCE — metrics & regression",
        "",
        "## Recommended execution order (first 3)",
    ]
    for step in exec_steps[:3]:
        if isinstance(step, dict):
            notes_lines.append(f"- {step.get('order')}. {step.get('phase_id')} ({step.get('track_id')})")
    notes_lines.append("")
    (out / "cross_modal_vision_ocr_testboard_v1_planning_notes.md").write_text(
        "\n".join(notes_lines),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "planning_status": summary.get("planning_status"),
                "v1_scope_locked": summary.get("v1_scope_locked"),
                "v1_track_count": summary.get("v1_track_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
