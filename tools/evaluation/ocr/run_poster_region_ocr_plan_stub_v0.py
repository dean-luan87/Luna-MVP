#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Poster-Region-OCR-Plan-Stub-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
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
    ap.add_argument("--poster-governance-root", required=True)
    ap.add_argument("--realvideo-registry-root", required=True)
    ap.add_argument("--metrics-collector-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.ocr_runtime.poster_region_ocr_plan_stub_v0 import run_poster_region_ocr_plan_stub_v0

    summary, plan, excluded, risk, provider, reading, metrics_binding, gate, audit, errs = (
        run_poster_region_ocr_plan_stub_v0(
            poster_governance_root=str(_require_abs(args.poster_governance_root, "--poster-governance-root")),
            realvideo_registry_root=str(_require_abs(args.realvideo_registry_root, "--realvideo-registry-root")),
            metrics_collector_root=str(_require_abs(args.metrics_collector_root, "--metrics-collector-root")),
        )
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "poster_region_ocr_plan_stub_summary.json", summary)
    _write_json(out / "poster_region_ocr_plan_stub.json", plan)
    _write_json(out / "poster_region_ocr_excluded_regions_report.json", excluded)
    _write_json(out / "poster_region_ocr_risk_matrix.json", risk)
    _write_json(out / "poster_region_ocr_provider_plan_matrix.json", provider)
    _write_json(out / "poster_region_ocr_reading_order_guard.json", reading)
    _write_json(out / "poster_region_ocr_metrics_binding_report.json", metrics_binding)
    _write_json(out / "poster_region_ocr_gate_policy_report.json", gate)
    _write_json(out / "poster_region_ocr_plan_stub_audit_report.json", audit)

    (out / "poster_region_ocr_plan_stub_notes.md").write_text(
        "\n".join(
            [
                "# Poster Region OCR Plan Stub",
                "",
                "Plan only — no OCR, no semantic join, no writes.",
                "",
                f"planned_regions: {plan.get('planned_region_count')}",
                f"excluded_regions: {excluded.get('excluded_region_count')}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "planned_region_count": plan.get("planned_region_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
