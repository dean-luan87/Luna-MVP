#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Poster-Real-OCR-Gated-Execution-001 runner."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
            candidates.append(parent)
    for parent in candidates:
        if (parent / "_eval_out").is_dir():
            return parent
        sibling = parent.parent / "Luna-Workspace-Min"
        if (sibling / "_eval_out").is_dir():
            return sibling
    return candidates[0] if candidates else here.parents[3]


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


def _apply_rapidocr_env() -> None:
    os.environ["LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_REAL_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_STUB_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0"] = "false"
    os.environ["LUNA_OCR_SUBMISSION_EVAL_ONLY"] = "true"
    os.environ.setdefault("LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX", "512")


def _prepare_governance(ws: Path, out: Path, gov_arg: str) -> Path:
    gov_src = (
        Path(gov_arg).expanduser()
        if gov_arg.strip()
        else (ws / "configs/ocr/ocr_image_input_governance_lightweight_normalized_smoke_v0.example.json")
    )
    if not gov_src.is_absolute():
        gov_src = (ws / gov_src).resolve()
    gov = out / "poster_real_ocr_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        fallback = ws / "configs/ocr/ocr_image_input_governance_v0.example.json"
        gov.write_text(fallback.read_text(encoding="utf-8"), encoding="utf-8")
    return _require_abs(str(gov), "governance under output-root")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--poster-layout-governance-root", required=True)
    ap.add_argument("--poster-region-ocr-plan-root", required=True)
    ap.add_argument("--poster-visual-symbol-evidence-root", required=True)
    ap.add_argument("--poster-reference-only-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    ap.add_argument("--governance-config", default="")
    ap.add_argument("--workspace-root", default="")
    args = ap.parse_args()

    _apply_rapidocr_env()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    ws = _require_abs(args.workspace_root, "--workspace-root") if args.workspace_root.strip() else WS_ROOT
    gov = _prepare_governance(ws, out, args.governance_config)

    from capabilities.ocr_runtime.poster_real_ocr_gated_execution_v0 import (
        run_poster_real_ocr_gated_execution_v0,
    )

    (
        summary,
        exec_plan,
        excluded,
        provider_gate,
        result_matrix,
        evidence,
        reading,
        ttl_risk,
        metrics,
        benchmark,
        health,
        boundary,
        sim,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_poster_real_ocr_gated_execution_v0(
        poster_layout_governance_root=str(_require_abs(args.poster_layout_governance_root, "layout")),
        poster_region_ocr_plan_root=str(_require_abs(args.poster_region_ocr_plan_root, "plan")),
        poster_visual_symbol_evidence_root=str(_require_abs(args.poster_visual_symbol_evidence_root, "visual")),
        poster_reference_only_root=str(_require_abs(args.poster_reference_only_root, "ref")),
        poster_track_b_closure_root=str(_require_abs(args.poster_track_b_closure_root, "track_b")),
        benchmark_real_values_smoke_root=str(_require_abs(args.benchmark_real_values_smoke_root, "benchmark")),
        system_health_governance_root=str(_require_abs(args.system_health_governance_root, "health")),
        simulation_lab_harness_root=str(_require_abs(args.simulation_lab_harness_root, "sim")),
        output_root=str(out),
        workspace_root=str(ws),
        governance_config_path=str(gov),
    )

    summary["output_root"] = str(out.resolve())
    summary["input_roots"] = {
        "poster_layout_governance_root": str(_require_abs(args.poster_layout_governance_root, "layout")),
        "poster_region_ocr_plan_root": str(_require_abs(args.poster_region_ocr_plan_root, "plan")),
        "poster_visual_symbol_evidence_root": str(_require_abs(args.poster_visual_symbol_evidence_root, "visual")),
        "poster_reference_only_root": str(_require_abs(args.poster_reference_only_root, "ref")),
        "poster_track_b_closure_root": str(_require_abs(args.poster_track_b_closure_root, "track_b")),
        "benchmark_real_values_smoke_root": str(_require_abs(args.benchmark_real_values_smoke_root, "benchmark")),
        "system_health_governance_root": str(_require_abs(args.system_health_governance_root, "health")),
        "simulation_lab_harness_root": str(_require_abs(args.simulation_lab_harness_root, "sim")),
    }

    _write_json(out / "poster_real_ocr_gated_execution_summary.json", summary)
    _write_json(out / "poster_real_ocr_execution_plan.json", exec_plan)
    _write_json(out / "poster_real_ocr_excluded_visual_region_guard_report.json", excluded)
    _write_json(out / "poster_real_ocr_provider_gate_report.json", provider_gate)
    _write_json(out / "poster_real_ocr_result_matrix.json", result_matrix)
    _write_json(out / "poster_layout_text_evidence_candidate.json", evidence)
    _write_json(out / "poster_real_ocr_reading_order_guard_report.json", reading)
    _write_json(out / "poster_real_ocr_ttl_commercial_risk_report.json", ttl_risk)
    _write_json(out / "poster_real_ocr_metrics_binding_report.json", metrics)
    _write_json(out / "poster_real_ocr_benchmark_link_report.json", benchmark)
    _write_json(out / "poster_real_ocr_system_health_link_report.json", health)
    _write_json(out / "poster_real_ocr_no_write_boundary_report.json", boundary)
    _write_json(out / "poster_real_ocr_simulation_context_report.json", sim)
    _write_json(out / "poster_real_ocr_non_claims_report.json", non_claims)
    _write_json(out / "poster_real_ocr_open_followups.json", followups)
    _write_json(out / "poster_real_ocr_audit_report.json", audit)

    (out / "poster_real_ocr_notes.md").write_text(
        "\n".join(
            [
                "# Poster Real OCR Gated Execution",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- execution_scope: {summary.get('execution_scope')}",
                f"- real_ocr_invoked: {summary.get('real_ocr_invoked')}",
                f"- rapidocr_invoked: {summary.get('rapidocr_invoked')}",
                f"- provider_unavailable: {summary.get('provider_unavailable')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Gated text-region OCR only; no full-image OCR, no visual-symbol OCR, no writes.",
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
                "real_ocr_invoked": summary.get("real_ocr_invoked"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
