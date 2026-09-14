#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-OCRRequest-Gated-Submission-001 runner."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
            if (parent / "_eval_out").is_dir():
                return parent
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
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
    gov = out / "realvideo_ocr_request_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        fallback = ws / "configs/ocr/ocr_image_input_governance_v0.example.json"
        gov.write_text(fallback.read_text(encoding="utf-8"), encoding="utf-8")
    return _require_abs(str(gov), "governance under output-root")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--realvideo-roi-to-ocr-reference-root", required=True)
    ap.add_argument("--realvideo-frame-sample-root", required=True)
    ap.add_argument("--realvideo-case-registry-root", required=True)
    ap.add_argument("--vision-roi-proposal-root", required=True)
    ap.add_argument("--vision-roi-to-ocr-bridge-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    args = ap.parse_args()

    _apply_rapidocr_env()
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    ws = _require_abs(args.workspace_root, "--workspace-root")
    gov = _prepare_governance(ws, out, args.governance_config)
    work_root = out / "_work" / "submissions"

    from capabilities.ocr_runtime.realvideo_ocr_request_gated_submission_v0 import (
        run_realvideo_ocr_request_gated_submission_v0,
    )

    roots = {
        "roi_ref": _require_abs(args.realvideo_roi_to_ocr_reference_root, "roi-ref"),
        "frame_sample": _require_abs(args.realvideo_frame_sample_root, "frame-sample"),
        "case_registry": _require_abs(args.realvideo_case_registry_root, "case-registry"),
        "vision_proposal": _require_abs(args.vision_roi_proposal_root, "vision-proposal"),
        "vision_bridge": _require_abs(args.vision_roi_to_ocr_bridge_root, "vision-bridge"),
        "bench": _require_abs(args.benchmark_real_values_smoke_root, "bench"),
        "health": _require_abs(args.system_health_governance_root, "health"),
        "sim": _require_abs(args.simulation_lab_harness_root, "sim"),
    }

    (
        summary,
        submission_plan,
        rejected_guard,
        provider_gate,
        result_matrix,
        collection,
        source_chain,
        case_mapping,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_realvideo_ocr_request_gated_submission_v0(
        realvideo_roi_to_ocr_reference_root=str(roots["roi_ref"]),
        realvideo_frame_sample_root=str(roots["frame_sample"]),
        realvideo_case_registry_root=str(roots["case_registry"]),
        vision_roi_proposal_root=str(roots["vision_proposal"]),
        vision_roi_to_ocr_bridge_root=str(roots["vision_bridge"]),
        benchmark_real_values_smoke_root=str(roots["bench"]),
        system_health_governance_root=str(roots["health"]),
        simulation_lab_harness_root=str(roots["sim"]),
        workspace_root=str(ws),
        governance_config_path=str(gov),
        submission_work_root=str(work_root),
        output_root=str(out),
    )

    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if errs:
        summary["errors"] = errs

    _write_json(out / "realvideo_ocr_request_gated_submission_summary.json", summary)
    _write_json(out / "realvideo_ocr_request_submission_plan.json", submission_plan)
    _write_json(out / "realvideo_ocr_request_rejected_roi_guard_report.json", rejected_guard)
    _write_json(out / "realvideo_ocr_request_provider_gate_report.json", provider_gate)
    _write_json(out / "realvideo_ocr_request_submission_result_matrix.json", result_matrix)
    _write_json(out / "realvideo_ocr_request_submission_collection.json", collection)
    _write_json(out / "realvideo_ocr_request_submission_source_chain_report.json", source_chain)
    _write_json(out / "realvideo_ocr_request_submission_case_mapping_report.json", case_mapping)
    _write_json(out / "realvideo_ocr_request_submission_metrics_candidate_report.json", metrics)
    _write_json(out / "realvideo_ocr_request_submission_benchmark_link_report.json", benchmark_link)
    _write_json(out / "realvideo_ocr_request_submission_system_health_link_report.json", health_link)
    _write_json(out / "realvideo_ocr_request_submission_no_write_boundary_report.json", boundary)
    _write_json(out / "realvideo_ocr_request_submission_simulation_context_report.json", sim_report)
    _write_json(out / "realvideo_ocr_request_submission_non_claims_report.json", non_claims)
    _write_json(out / "realvideo_ocr_request_submission_open_followups.json", followups)
    _write_json(out / "realvideo_ocr_request_submission_audit_report.json", audit)

    (out / "realvideo_ocr_request_submission_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo OCRRequest Gated Submission",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- submission_scope: {summary.get('submission_scope')}",
                f"- success_count: {summary.get('success_count')} / {summary.get('selected_submission_count')}",
                f"- provider_unavailable: {summary.get('provider_unavailable')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Gated submission only; upper_sign_roi; no fusion, no writes.",
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
                "success_count": summary.get("success_count"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
