#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-MidPlatform-Gated-Runtime-Path-Alignment-001 runner."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
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


def _apply_ocr_bridge_env() -> None:
    os.environ["LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_REAL_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_STUB_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0"] = "false"
    os.environ["LUNA_OCR_SUBMISSION_EVAL_ONLY"] = "true"
    os.environ.setdefault("LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX", "512")


def _prepare_governance(ws: Path, out: Path, gov_arg: str) -> Path:
    gov_src = Path(gov_arg).expanduser() if gov_arg.strip() else (ws / "configs/ocr/ocr_provider_runtime_governance_v0.example.json")
    if not gov_src.is_absolute():
        gov_src = (ws / gov_src).resolve()
    gov = out / "ocr_midplatform_gated_runtime_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        gov.write_text(
            json.dumps(
                {
                    "schema_version": "ocr_image_input_governance_v0",
                    "size_limits": {"max_width_realtime": 2048, "max_height_realtime": 2048, "max_megapixels_realtime": 8.0},
                    "downscale_policy": {"enabled": True},
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    return gov.resolve()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--mixed-video-poster-batch-root", required=True)
    ap.add_argument("--mixedvideo-linebox-trace-root", required=True)
    ap.add_argument("--readability-governance-root", required=True)
    ap.add_argument("--ocr-evidence-pack-contract-root", required=True)
    ap.add_argument("--workspace-root", default="")
    ap.add_argument("--governance-config", default="")
    args = ap.parse_args()

    _apply_ocr_bridge_env()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    ws = _require_abs(args.workspace_root, "--workspace-root") if args.workspace_root.strip() else WS_ROOT
    gov = _prepare_governance(ws, out, args.governance_config)
    work = out / "submission_work"

    roots = {
        "mixed_video_poster_batch_root": _require_abs(args.mixed_video_poster_batch_root, "mixed-batch"),
        "mixedvideo_linebox_trace_root": _require_abs(args.mixedvideo_linebox_trace_root, "linebox"),
        "readability_governance_root": _require_abs(args.readability_governance_root, "readability"),
        "ocr_evidence_pack_contract_root": _require_abs(args.ocr_evidence_pack_contract_root, "contract"),
    }

    from capabilities.midplatform.ocr_midplatform_gated_runtime_path_alignment_v0 import (
        run_ocr_midplatform_gated_runtime_path_alignment_v0,
    )

    result = run_ocr_midplatform_gated_runtime_path_alignment_v0(
        output_root=str(out),
        mixed_video_poster_batch_root=str(roots["mixed_video_poster_batch_root"]),
        mixedvideo_linebox_trace_root=str(roots["mixedvideo_linebox_trace_root"]),
        readability_governance_root=str(roots["readability_governance_root"]),
        ocr_evidence_pack_contract_root=str(roots["ocr_evidence_pack_contract_root"]),
        workspace_root=str(ws),
        governance_config_path=str(gov),
        submission_work_root=str(work),
    )

    (
        summary,
        input_matrix,
        sq_matrix,
        read_matrix,
        roi_matrix,
        req_matrix,
        trace_doc,
        bypass_report,
        full_frame_boundary,
        pack_alignment,
        sem_alignment,
        boundary,
        audit,
        evidence_packs,
        semantic_candidates,
        errs,
    ) = result

    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if errs:
        summary["errors"] = errs

    writes = [
        ("ocr_midplatform_gated_runtime_path_summary.json", summary),
        ("ocr_input_candidate_matrix.json", input_matrix),
        ("ocr_source_quality_gate_decision_matrix.json", sq_matrix),
        ("ocr_readability_gate_decision_matrix.json", read_matrix),
        ("ocr_roi_crop_or_scan_observation_matrix.json", roi_matrix),
        ("ocr_request_candidate_matrix.json", req_matrix),
        ("ocr_request_gated_submission_trace.json", trace_doc),
        ("ocr_direct_provider_bypass_detection_report.json", bypass_report),
        ("ocr_full_frame_scan_observation_boundary_report.json", full_frame_boundary),
        ("ocr_evidence_pack_request_ref_alignment_report.json", pack_alignment),
        ("ocr_semantic_candidate_request_ref_alignment_report.json", sem_alignment),
        ("ocr_midplatform_gated_runtime_path_no_write_boundary_report.json", boundary),
        ("ocr_midplatform_gated_runtime_path_audit_report.json", audit),
        (
            "ocr_midplatform_gated_evidence_pack_collection.json",
            {
                "schema_version": "ocr_midplatform_gated_evidence_pack_collection_v0",
                "pack_count": len(evidence_packs),
                "packs": evidence_packs,
            },
        ),
        (
            "ocr_midplatform_gated_semantic_candidate_collection.json",
            {
                "schema_version": "ocr_midplatform_gated_semantic_candidate_collection_v0",
                "candidate_count": len(semantic_candidates),
                "candidates": semantic_candidates,
            },
        ),
    ]
    for name, obj in writes:
        _write_json(out / name, obj)

    (out / "ocr_midplatform_gated_runtime_path_notes.md").write_text(
        "\n".join(
            [
                "# OCR MidPlatform Gated Runtime Path Alignment",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- direct_provider_bypass: {summary.get('direct_provider_bypass')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Path: InputCandidate → SQ Gate → Readability Gate → ROI → OCRRequest → Bridge → Pack → Semantic",
                "",
                "Forbidden: harness direct RapidOCR as primary path.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": summary.get("phase_verdict_hint"), "errors": errs},
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
