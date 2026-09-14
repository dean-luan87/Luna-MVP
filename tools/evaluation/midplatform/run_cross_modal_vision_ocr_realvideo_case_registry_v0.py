#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001 runner."""

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
    ap.add_argument("--v1-planning-root", required=True)
    ap.add_argument("--metrics-collector-root", required=True)
    ap.add_argument("--poster-governance-root", required=True)
    ap.add_argument("--public-facility-governance-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.cross_modal_vision_ocr_realvideo_case_registry_v0 import (
        run_cross_modal_vision_ocr_realvideo_case_registry_v0,
    )

    (
        summary,
        registry,
        taxonomy,
        sampling,
        behavior,
        metrics_binding,
        gov_link,
        non_goals,
        risks,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_realvideo_case_registry_v0(
        v1_planning_root=str(_require_abs(args.v1_planning_root, "--v1-planning-root")),
        metrics_collector_root=str(_require_abs(args.metrics_collector_root, "--metrics-collector-root")),
        poster_governance_root=str(_require_abs(args.poster_governance_root, "--poster-governance-root")),
        public_facility_governance_root=str(
            _require_abs(args.public_facility_governance_root, "--public-facility-governance-root")
        ),
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "cross_modal_vision_ocr_realvideo_case_registry_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_realvideo_case_registry.json", registry)
    _write_json(out / "cross_modal_vision_ocr_realvideo_case_taxonomy.json", taxonomy)
    _write_json(out / "cross_modal_vision_ocr_realvideo_sampling_policy_stub.json", sampling)
    _write_json(out / "cross_modal_vision_ocr_realvideo_expected_behavior_matrix.json", behavior)
    _write_json(out / "cross_modal_vision_ocr_realvideo_metrics_binding_matrix.json", metrics_binding)
    _write_json(out / "cross_modal_vision_ocr_realvideo_governance_link_report.json", gov_link)
    _write_json(out / "cross_modal_vision_ocr_realvideo_non_goals_report.json", non_goals)
    _write_json(out / "cross_modal_vision_ocr_realvideo_risk_register.json", risks)
    _write_json(out / "cross_modal_vision_ocr_realvideo_case_registry_audit_report.json", audit)

    (out / "cross_modal_vision_ocr_realvideo_case_registry_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo Case Registry v0",
                "",
                "Registry only — no video load, no frames, no OCR.",
                "",
                f"case_count: {registry.get('case_count')}",
                f"taxonomy categories: {taxonomy.get('category_count')}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "case_count": registry.get("case_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
