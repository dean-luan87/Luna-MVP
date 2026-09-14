#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Mixed-Video-Poster-Batch-Smoke-v2-Gated-Path-Only-001 runner."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List


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

DEFAULT_VIDEOS = [
    ("test_video_complex_6m42s", "/Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4", "P0", "text_bearing_realvideo_main"),
    ("phone_batch001_clear_path", "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_001/phone_local_001_clear_path.mp4", "P1", "phone_local_clear_path"),
    ("phone_batch002_narrow_path", "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_002/phone_local_003_narrow_path.mp4", "P1", "phone_local_narrow_path"),
    ("phone_batch002_clear_path", "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_002/phone_local_001_clear_path.mp4", "P1", "phone_local_clear_path_duplicate_batch"),
    ("phone_batch002_minor_obstacle", "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_002/phone_local_002_minor_obstacle.mp4", "P1", "phone_local_minor_obstacle"),
    ("sidewalk_minor_obstacle", "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/sidewalk/sidewalk_002_minor_obstacle.mp4", "P1", "sidewalk_minor_obstacle"),
    ("sidewalk_narrow_path", "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/sidewalk/sidewalk_003_narrow_path.mp4", "P1", "sidewalk_narrow_path"),
    ("sidewalk_clear_path", "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/sidewalk/sidewalk_001_clear_path.mp4", "P1", "sidewalk_clear_path"),
]
DEFAULT_IMAGE_IDS = ["ocr_1", "ocr_2", "ocr_3", "ocr_4", "ocr_5", "ocr_6", "ocr_7", "ocr_8", "ocr_10", "ocr_12"]

WRITES = [
    ("mixed_batch_v2_gated_path_summary.json", "summary"),
    ("mixed_batch_v2_input_manifest.json", "manifest"),
    ("mixed_batch_v2_input_candidate_matrix.json", "input_matrix"),
    ("mixed_batch_v2_source_quality_gate_decision_matrix.json", "sq_matrix"),
    ("mixed_batch_v2_readability_gate_decision_matrix.json", "read_matrix"),
    ("mixed_batch_v2_routing_matrix.json", "routing_matrix"),
    ("mixed_batch_v2_ocr_request_candidate_matrix.json", "ocr_request_matrix"),
    ("mixed_batch_v2_ocr_request_gated_submission_trace.json", "submission_trace"),
    ("mixed_batch_v2_direct_provider_bypass_detection_report.json", "bypass_report"),
    ("mixed_batch_v2_full_frame_scan_boundary_report.json", "full_frame_boundary"),
    ("mixed_batch_v2_ocr_evidence_pack_collection.json", "pack_collection"),
    ("mixed_batch_v2_evidence_pack_request_alignment_report.json", "pack_alignment"),
    ("mixed_batch_v2_ocr_semantic_candidate_collection.json", "semantic_collection"),
    ("mixed_batch_v2_semantic_candidate_request_alignment_report.json", "semantic_alignment"),
    ("mixed_batch_v2_scan_observation_report.json", "scan_observation_report"),
    ("mixed_batch_v2_visual_symbol_public_facility_routing_report.json", "vs_pf_routing"),
    ("mixed_batch_v2_source_quality_rejection_degrade_report.json", "sq_rejection"),
    ("mixed_batch_v2_uncertainty_guard_report.json", "uncertainty_guard"),
    ("mixed_batch_v2_metrics_candidate_report.json", "metrics"),
    ("mixed_batch_v2_benchmark_link_report.json", "benchmark_link"),
    ("mixed_batch_v2_system_health_link_report.json", "health_link"),
    ("mixed_batch_v2_no_write_boundary_report.json", "boundary"),
    ("mixed_batch_v2_simulation_context_report.json", "sim_report"),
    ("mixed_batch_v2_non_claims_report.json", "non_claims"),
    ("mixed_batch_v2_open_followups.json", "followups"),
    ("mixed_batch_v2_audit_report.json", "audit"),
]


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
    os.environ["LUNA_OCR_SUBMISSION_EVAL_ONLY"] = "true"
    os.environ.setdefault("LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX", "512")


def _prepare_governance(ws: Path, out: Path, gov_arg: str) -> Path:
    gov_src = Path(gov_arg).expanduser() if gov_arg.strip() else (ws / "configs/ocr/ocr_provider_runtime_governance_v0.example.json")
    if not gov_src.is_absolute():
        gov_src = (ws / gov_src).resolve()
    gov = out / "mixed_batch_v2_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        gov.write_text('{"schema_version":"ocr_image_input_governance_v0","size_limits":{"max_width_realtime":2048,"max_height_realtime":2048,"max_megapixels_realtime":8.0}}\n', encoding="utf-8")
    return gov.resolve()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--fixtures-root", required=True)
    ap.add_argument("--mixed-batch-v1-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--readability-governance-root", required=True)
    ap.add_argument("--evidence-pack-contract-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--governance-config", default="")
    ap.add_argument("--workspace-root", default="")
    ap.add_argument("--video", action="append", default=[])
    ap.add_argument("--image-id", action="append", default=[])
    args = ap.parse_args()

    _apply_ocr_bridge_env()
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    fixtures = _require_abs(args.fixtures_root, "--fixtures-root")
    ws = _require_abs(args.workspace_root, "--workspace-root") if args.workspace_root.strip() else WS_ROOT
    gov = _prepare_governance(ws, out, args.governance_config)
    work = out / "submission_work"

    videos: List[Dict[str, str]] = []
    if args.video:
        for spec in args.video:
            vid, path = spec.split("=", 1)
            videos.append({"video_id": vid, "video_path": path, "priority": "P1", "purpose": "cli"})
    else:
        for vid, path, pri, purpose in DEFAULT_VIDEOS:
            videos.append({"video_id": vid, "video_path": path, "priority": pri, "purpose": purpose})
    image_ids = list(args.image_id) if args.image_id else list(DEFAULT_IMAGE_IDS)

    roots = {
        "mixed_batch_v1_root": _require_abs(args.mixed_batch_v1_root, "v1"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "readability_governance_root": _require_abs(args.readability_governance_root, "readability"),
        "evidence_pack_contract_root": _require_abs(args.evidence_pack_contract_root, "contract"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "benchmark"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.mixed_video_poster_batch_smoke_v2_gated_path_only_v0 import (
        run_mixed_video_poster_batch_smoke_v2_gated_path_only_v0,
    )

    result = run_mixed_video_poster_batch_smoke_v2_gated_path_only_v0(
        output_root=str(out),
        fixtures_root=str(fixtures),
        videos=videos,
        image_ids=image_ids,
        mixed_batch_v1_root=str(roots["mixed_batch_v1_root"]),
        linebox_sq_root=str(roots["linebox_sq_root"]),
        readability_governance_root=str(roots["readability_governance_root"]),
        evidence_pack_contract_root=str(roots["evidence_pack_contract_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
        workspace_root=str(ws),
        governance_config_path=str(gov),
        submission_work_root=str(work),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {**{k: str(v) for k, v in roots.items()}, "fixtures_root": str(fixtures)}
    if result.get("errs"):
        summary["errors"] = result["errs"]

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "mixed_batch_v2_notes.md").write_text(
        "\n".join(
            [
                "# Mixed Video Poster Batch Smoke v2 — Gated Path Only",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- provider_call_count: {summary.get('provider_call_count')}",
                f"- evidence_pack_count: {summary.get('evidence_pack_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "No direct RapidOCR in capability; provider via ocr_mainline_bridge only.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "phase_verdict_hint": summary.get("phase_verdict_hint"), "errors": result.get("errs", [])}, ensure_ascii=False))
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
