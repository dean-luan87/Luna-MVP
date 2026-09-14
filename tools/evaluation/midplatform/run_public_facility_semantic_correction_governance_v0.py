#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-PublicFacility-Semantic-Correction-Governance-001 runner."""

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
    ap.add_argument("--metrics-schema-root", default="")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    metrics = args.metrics_schema_root.strip() or None
    if metrics:
        metrics = str(_require_abs(metrics, "--metrics-schema-root"))

    from capabilities.midplatform.public_facility_semantic_correction_governance_v0 import (
        run_public_facility_semantic_correction_governance_v0,
    )

    (
        summary,
        manifest,
        taxonomy,
        routing,
        levels,
        pipeline,
        example,
        risks,
        gate,
        non_claims,
        audit,
        errs,
    ) = run_public_facility_semantic_correction_governance_v0(
        metrics_schema_root=metrics,
        work_dir=out / "_work",
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "public_facility_semantic_correction_governance_summary.json", summary)
    _write_json(out / "public_facility_synthetic_fixture_manifest.json", manifest)
    _write_json(out / "public_facility_taxonomy.json", taxonomy)
    _write_json(out / "public_facility_evidence_routing_policy.json", routing)
    _write_json(out / "public_facility_correction_levels.json", levels)
    _write_json(out / "public_facility_pipeline_layers.json", pipeline)
    _write_json(out / "public_facility_semantic_candidate_example.json", example)
    _write_json(out / "public_facility_governance_risk_report.json", risks)
    _write_json(out / "public_facility_gate_policy_report.json", gate)
    _write_json(out / "public_facility_governance_non_claims_report.json", non_claims)
    _write_json(out / "public_facility_governance_audit_report.json", audit)

    (out / "public_facility_governance_notes.md").write_text(
        "\n".join(
            [
                "# Public Facility Semantic Correction Governance",
                "",
                "Semantic-first; OCR auxiliary only. Hybrid arbitration stub (no runtime).",
                "",
                f"fixture: {summary.get('source_image_ref')}",
                "",
                "Parallel line: Poster = segment_first; Public Facility = semantic_first.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "default_ocr_mainline_allowed": summary.get("default_ocr_mainline_allowed"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
