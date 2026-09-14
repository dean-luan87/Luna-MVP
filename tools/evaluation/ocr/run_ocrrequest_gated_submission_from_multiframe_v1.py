#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCRRequest-Gated-Submission-from-Multiframe-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

WRITES = [
    ("ocrrequest_gated_submission_from_multiframe_v1_summary.json", "summary"),
    ("multiframe_ocrrequest_crop_intake_matrix_v1.json", "intake_matrix"),
    ("multiframe_ocrrequest_gate_policy_v1.json", "gate_policy"),
    ("multiframe_ocrrequest_submission_plan_v1.json", "submission_plan"),
    ("multiframe_ocrrequest_bridge_invocation_trace_v1.json", "bridge_trace"),
    ("multiframe_ocrrequest_direct_provider_bypass_audit_v1.json", "bypass_audit"),
    ("multiframe_ocr_result_collection_v1.json", "result_collection"),
    ("multiframe_ocr_result_matrix_v1.json", "result_matrix"),
    ("multiframe_ocr_output_grouping_report_v1.json", "grouping"),
    ("multiframe_ocr_low_information_repeated_guard_v1.json", "low_information_guard"),
    ("multiframe_ocr_same_frame_blocker_carryover_report_v1.json", "same_frame_carryover"),
    ("multiframe_ocr_projection_crop_risk_report_v1.json", "projection_risk"),
    ("multiframe_ocr_future_ep_v4_plan.json", "future_ep_plan"),
    ("multiframe_ocr_source_chain_report_v1.json", "source_chain_report"),
    ("multiframe_ocr_provider_summary_v1.json", "provider_summary"),
    ("multiframe_ocr_boundary_report_v1.json", "boundary"),
    ("multiframe_ocr_metrics_candidate_report_v1.json", "metrics"),
    ("multiframe_ocr_benchmark_link_report_v1.json", "benchmark_link"),
    ("multiframe_ocr_system_health_link_report_v1.json", "health_link"),
    ("multiframe_ocr_no_write_boundary_report_v1.json", "no_write"),
    ("multiframe_ocr_simulation_context_report_v1.json", "sim_report"),
    ("multiframe_ocr_non_claims_report_v1.json", "non_claims"),
    ("multiframe_ocr_open_followups_v1.json", "followups"),
    ("multiframe_ocr_audit_report_v1.json", "audit"),
]


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
    gov = out / "multiframe_gated_submission_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        fallback = ws / "configs/ocr/ocr_image_input_governance_v0.example.json"
        gov.write_text(fallback.read_text(encoding="utf-8"), encoding="utf-8")
    return _require_abs(str(gov), "governance under output-root")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--multiframe-crop-root", required=True)
    ap.add_argument("--text-region-tracklet-root", required=True)
    ap.add_argument("--better-frame-root", required=True)
    ap.add_argument("--multiframe-merge-proposal-root", required=True)
    ap.add_argument("--source-validation-v2-root", required=True)
    ap.add_argument("--semantic-v3-root", required=True)
    ap.add_argument("--evidence-pack-v3-root", required=True)
    ap.add_argument("--ocrrequest-gated-submission-v2-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-v2-root", required=True)
    ap.add_argument("--roi-crop-v2-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    args = ap.parse_args()

    _apply_rapidocr_env()
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    ws = _require_abs(args.workspace_root, "--workspace-root")
    gov = _prepare_governance(ws, out, args.governance_config)
    work_root = out / "_work" / "submissions"

    roots = {
        "multiframe_crop_root": _require_abs(args.multiframe_crop_root, "mf_crop"),
        "text_region_tracklet_root": _require_abs(args.text_region_tracklet_root, "tr"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "multiframe_merge_proposal_root": _require_abs(args.multiframe_merge_proposal_root, "mf"),
        "source_validation_v2_root": _require_abs(args.source_validation_v2_root, "sv2"),
        "semantic_v3_root": _require_abs(args.semantic_v3_root, "sem_v3"),
        "evidence_pack_v3_root": _require_abs(args.evidence_pack_v3_root, "ep_v3"),
        "ocrrequest_gated_submission_v2_root": _require_abs(args.ocrrequest_gated_submission_v2_root, "ocr_v2"),
        "roi_ocrrequest_reference_v2_root": _require_abs(args.roi_ocrrequest_reference_v2_root, "ref_v2"),
        "roi_crop_v2_root": _require_abs(args.roi_crop_v2_root, "crop_v2"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "mixed"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    cap_path = ws / "capabilities/ocr_runtime/ocrrequest_gated_submission_from_multiframe_v1.py"

    from capabilities.ocr_runtime.ocrrequest_gated_submission_from_multiframe_v1 import (
        run_ocrrequest_gated_submission_from_multiframe_v1,
    )

    result = run_ocrrequest_gated_submission_from_multiframe_v1(
        multiframe_crop_root=str(roots["multiframe_crop_root"]),
        text_region_tracklet_root=str(roots["text_region_tracklet_root"]),
        better_frame_root=str(roots["better_frame_root"]),
        multiframe_merge_proposal_root=str(roots["multiframe_merge_proposal_root"]),
        source_validation_v2_root=str(roots["source_validation_v2_root"]),
        semantic_v3_root=str(roots["semantic_v3_root"]),
        evidence_pack_v3_root=str(roots["evidence_pack_v3_root"]),
        ocrrequest_gated_submission_v2_root=str(roots["ocrrequest_gated_submission_v2_root"]),
        roi_ocrrequest_reference_v2_root=str(roots["roi_ocrrequest_reference_v2_root"]),
        roi_crop_v2_root=str(roots["roi_crop_v2_root"]),
        linebox_sq_root=str(roots["linebox_sq_root"]),
        mixed_batch_v2_root=str(roots["mixed_batch_v2_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
        workspace_root=str(ws),
        governance_config_path=str(gov),
        submission_work_root=str(work_root),
        capability_path=str(cap_path),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "multiframe_ocr_notes.md").write_text(
        "\n".join(
            [
                "# OCRRequest Gated Submission from Multiframe v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- crops: {summary.get('multiframe_crop_artifact_count_observed')}",
                f"- submitted: {summary.get('ocrrequest_submitted_count')}",
                f"- success: {summary.get('ocrrequest_success_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Multiframe projection crops only; bridge-only; not_fact.",
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
                "ocrrequest_submitted_count": summary.get("ocrrequest_submitted_count"),
                "ocrrequest_success_count": summary.get("ocrrequest_success_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
