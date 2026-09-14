#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-Mixed-Video-Poster-Batch-Smoke-001 runner."""

from __future__ import annotations

import argparse
import json
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


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--fixtures-root", required=True)
    ap.add_argument("--video", action="append", default=[], help="video_id=path")
    ap.add_argument("--image-id", action="append", default=[])
    ap.add_argument("--sample-interval-sec", type=float, default=3.0)
    ap.add_argument("--max-selected-frames", type=int, default=12)
    ap.add_argument("--min-selected-frames", type=int, default=10)
    ap.add_argument("--max-sample-frames", type=int, default=200)
    ap.add_argument("--ocr-evidence-pack-contract-root", default="")
    ap.add_argument("--ocr-evidence-pack-adapter-update-root", default="")
    ap.add_argument("--ocr-semantic-candidate-generator-root", default="")
    ap.add_argument("--realvideo-readability-governance-root", default="")
    ap.add_argument("--realvideo-text-bearing-planning-root", default="")
    ap.add_argument("--public-facility-runtime-dryrun-root", default="")
    ap.add_argument("--poster-fusion-gate-chain-closure-root", default="")
    ap.add_argument("--benchmark-real-values-smoke-root", default="")
    ap.add_argument("--system-health-governance-root", default="")
    ap.add_argument("--simulation-lab-harness-root", default="")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    fixtures = _require_abs(args.fixtures_root, "--fixtures-root")

    videos: List[Dict[str, str]] = []
    if args.video:
        for spec in args.video:
            if "=" not in spec:
                raise SystemExit(f"invalid --video: {spec}")
            vid, path = spec.split("=", 1)
            videos.append({"video_id": vid, "video_path": path, "priority": "P1", "purpose": "cli"})
    else:
        for vid, path, pri, purpose in DEFAULT_VIDEOS:
            videos.append({"video_id": vid, "video_path": path, "priority": pri, "purpose": purpose})

    image_ids = list(args.image_id) if args.image_id else list(DEFAULT_IMAGE_IDS)

    eval_root = out.parent
    input_roots = {
        "ocr_evidence_pack_contract_root": str(_require_abs(args.ocr_evidence_pack_contract_root or str(eval_root / "ocr_evidence_pack_spatiotemporal_semantic_contract_v0"), "contract")),
        "ocr_evidence_pack_adapter_update_root": str(_require_abs(args.ocr_evidence_pack_adapter_update_root or str(eval_root / "ocr_evidence_pack_adapter_update_smoke_v0"), "adapter")),
        "ocr_semantic_candidate_generator_root": str(_require_abs(args.ocr_semantic_candidate_generator_root or str(eval_root / "ocr_semantic_candidate_generator_dryrun_smoke_v0"), "semantic")),
        "realvideo_readability_governance_root": str(_require_abs(args.realvideo_readability_governance_root or str(eval_root / "realvideo_ocr_readability_governance_smoke_v0"), "readability")),
        "realvideo_text_bearing_planning_root": str(_require_abs(args.realvideo_text_bearing_planning_root or str(eval_root / "realvideo_ocr_text_bearing_sample_planning_smoke_v0"), "planning")),
        "public_facility_runtime_dryrun_root": str(_require_abs(args.public_facility_runtime_dryrun_root or str(eval_root / "public_facility_runtime_dryrun_v0"), "pf")),
        "poster_fusion_gate_chain_closure_root": str(_require_abs(args.poster_fusion_gate_chain_closure_root or str(eval_root / "poster_real_ocr_fusion_gate_chain_closure_smoke_v0"), "poster")),
        "benchmark_real_values_smoke_root": str(_require_abs(args.benchmark_real_values_smoke_root or str(eval_root / "cross_modal_vision_ocr_benchmark_real_values_smoke_v0"), "bench")),
        "system_health_governance_root": str(_require_abs(args.system_health_governance_root or str(eval_root / "system_health_center_governance_v0"), "health")),
        "simulation_lab_harness_root": str(_require_abs(args.simulation_lab_harness_root or str(eval_root / "simulation_lab_minimal_harness_v0/developer_full"), "sim")),
    }

    from capabilities.midplatform.cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0 import (
        run_cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0,
    )

    (
        summary,
        manifest,
        scan_report,
        frame_plan,
        image_ocr_report,
        pack_collection,
        sem_collection,
        readability_report,
        routing_report,
        uncertainty,
        chain_report,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_mixed_video_poster_batch_smoke_v0(
        output_root=str(out),
        fixtures_root=str(fixtures),
        videos=videos,
        image_ids=image_ids,
        input_roots=input_roots,
        sample_interval_sec=args.sample_interval_sec,
        max_sample_frames=args.max_sample_frames,
        max_selected_frames=args.max_selected_frames,
        min_selected_frames=args.min_selected_frames,
    )

    summary["output_root"] = str(out)
    summary["input_roots"] = input_roots

    writes = [
        ("mixed_video_poster_batch_summary.json", summary),
        ("mixed_video_poster_input_manifest.json", manifest),
        ("mixed_video_candidate_scan_report.json", scan_report),
        ("mixed_video_selected_text_bearing_frame_plan.json", frame_plan),
        ("mixed_poster_image_ocr_execution_report.json", image_ocr_report),
        ("mixed_ocr_evidence_pack_collection.json", pack_collection),
        ("mixed_ocr_semantic_candidate_collection.json", sem_collection),
        ("mixed_ocr_readability_evaluation_report.json", readability_report),
        ("mixed_visual_symbol_public_facility_routing_report.json", routing_report),
        ("mixed_ocr_uncertainty_guard_report.json", uncertainty),
        ("mixed_ocr_source_chain_report.json", chain_report),
        ("mixed_ocr_metrics_candidate_report.json", metrics),
        ("mixed_ocr_benchmark_link_report.json", benchmark_link),
        ("mixed_ocr_system_health_link_report.json", health_link),
        ("mixed_ocr_no_write_boundary_report.json", boundary),
        ("mixed_ocr_simulation_context_report.json", sim_report),
        ("mixed_ocr_non_claims_report.json", non_claims),
        ("mixed_ocr_open_followups.json", followups),
        ("mixed_ocr_audit_report.json", audit),
    ]
    for fname, obj in writes:
        _write_json(out / fname, obj)

    (out / "mixed_ocr_notes.md").write_text(
        f"# Mixed Video Poster Batch Smoke\n\n- phase_verdict_hint: {summary.get('phase_verdict_hint')}\n- packs: {summary.get('ocr_evidence_pack_count')}\n",
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "phase_verdict_hint": summary.get("phase_verdict_hint"), "errors": errs}, ensure_ascii=False))
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
