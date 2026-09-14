#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-PublicFacility-Runtime-DryRun-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
            if (parent / "_eval_out").is_dir():
                return parent
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
    ap.add_argument("--public-facility-governance-root", required=True)
    ap.add_argument("--v1-track-closures-root", required=True)
    ap.add_argument("--benchmark-real-values-planning-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.public_facility_runtime_dryrun_v0 import run_public_facility_runtime_dryrun_v0

    (
        summary,
        fixture_manifest,
        semantic,
        correction,
        evidence,
        gate,
        speak,
        risk,
        metrics,
        benchmark_link,
        sim_report,
        non_claims,
        audit,
        errs,
    ) = run_public_facility_runtime_dryrun_v0(
        public_facility_governance_root=str(_require_abs(args.public_facility_governance_root, "--public-facility-governance-root")),
        v1_track_closures_root=str(_require_abs(args.v1_track_closures_root, "--v1-track-closures-root")),
        benchmark_real_values_planning_root=str(
            _require_abs(args.benchmark_real_values_planning_root, "--benchmark-real-values-planning-root")
        ),
        simulation_lab_harness_root=str(_require_abs(args.simulation_lab_harness_root, "--simulation-lab-harness-root")),
        poster_track_b_closure_root=str(_require_abs(args.poster_track_b_closure_root, "--poster-track-b-closure-root")),
    )

    summary["output_root"] = str(out)
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs else "NO_GO"

    _write_json(out / "public_facility_runtime_dryrun_summary.json", summary)
    _write_json(out / "public_facility_runtime_fixture_manifest.json", fixture_manifest)
    _write_json(out / "public_facility_semantic_candidate_matrix.json", semantic)
    _write_json(out / "public_facility_correction_candidate_matrix.json", correction)
    _write_json(out / "public_facility_evidence_composition_matrix.json", evidence)
    _write_json(out / "public_facility_gate_evaluator_dryrun.json", gate)
    _write_json(out / "public_facility_cautious_speak_dryrun_report.json", speak)
    _write_json(out / "public_facility_runtime_risk_report.json", risk)
    _write_json(out / "public_facility_runtime_metrics_binding_report.json", metrics)
    _write_json(out / "public_facility_runtime_benchmark_link_report.json", benchmark_link)
    _write_json(out / "public_facility_runtime_simulation_context_report.json", sim_report)
    _write_json(out / "public_facility_runtime_non_claims_report.json", non_claims)
    _write_json(out / "public_facility_runtime_audit_report.json", audit)
    (out / "public_facility_runtime_notes.md").write_text(
        "\n".join(
            [
                "# Public Facility Runtime DryRun",
                "",
                f"- phase: {summary.get('phase')}",
                f"- runtime_scope: {summary.get('runtime_scope')}",
                f"- semantic_first_required: {summary.get('semantic_first_required')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Dry-run only; no OCR, no Vision, no fact writes, no TTS.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "runtime_scope": summary.get("runtime_scope"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
