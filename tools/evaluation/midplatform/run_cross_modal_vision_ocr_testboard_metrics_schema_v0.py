#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001 runner."""

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
    ap.add_argument("--v1-planning-root", required=True)
    ap.add_argument("--poster-governance-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    v0 = _require_abs(args.v0_closure_root, "--v0-closure-root")
    v1 = _require_abs(args.v1_planning_root, "--v1-planning-root")
    poster = _require_abs(args.poster_governance_root, "--poster-governance-root")

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_metrics_schema_v0 import (
        run_cross_modal_vision_ocr_testboard_metrics_schema_v0,
    )

    summary, schema, matrix, source_map, gate, non_claims, collector, audit, errs = (
        run_cross_modal_vision_ocr_testboard_metrics_schema_v0(
            v0_closure_root=str(v0),
            v1_planning_root=str(v1),
            poster_governance_root=str(poster),
        )
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_schema_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_schema.json", schema)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_definition_matrix.json", matrix)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_source_map.json", source_map)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_gate_policy.json", gate)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_non_claims_report.json", non_claims)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_collector_contract_stub.json", collector)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_schema_audit_report.json", audit)

    groups = list((schema.get("metric_groups") or {}).keys())
    notes = [
        "# CrossModal Vision OCR TestBoard Metrics Schema",
        "",
        "Schema-only — no OCR, no benchmark values, no fact writes.",
        "",
        f"v0_closure_root: {v0}",
        f"v1_planning_root: {v1}",
        f"poster_governance_root: {poster}",
        "",
        f"metric_groups: {', '.join(groups)}",
        "",
        f"definition_matrix_rows: {matrix.get('row_count')}",
        "",
    ]
    (out / "cross_modal_vision_ocr_testboard_metrics_schema_notes.md").write_text(
        "\n".join(notes),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "metrics_scope": summary.get("metrics_scope"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
