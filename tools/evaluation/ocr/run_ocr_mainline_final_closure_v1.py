#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Mainline Final Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.ocr_mainline_final_closure_v1 import (
    run_ocr_mainline_final_closure_v1,
)


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run OCR mainline final closure v1")
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--ocr-regression-route-compliance-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_staticreading_poster_realvideo_regression_route_compliance_v1_smoke_v0"),
    )
    parser.add_argument(
        "--roi-to-ocrrequest-reference-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "roi_to_ocrrequest_reference_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-evidence-pack-adapter-v1-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_evidence_pack_adapter_v1_scan_observation_alignment_v0"),
    )
    parser.add_argument(
        "--mixed-batch-v2-gated-path-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "mixed_video_poster_batch_smoke_v2_gated_path_only_v0"),
    )
    parser.add_argument(
        "--realvideo-text-bearing-planning-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "realvideo_ocr_text_bearing_sample_planning_smoke_v0"),
    )
    parser.add_argument(
        "--static-readable-region-discovery-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "static_readable_region_discovery_guidance_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--worldmodel-lookup-reading-framework-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "worldmodel_lookup_for_reading_framework_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-integration-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--roi-crop-rerun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "roi_crop_execution_dryrun_v1_rerun_better_frames_smoke_v0"),
    )
    parser.add_argument(
        "--roi-bbox-expansion-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "roi_bbox_expansion_proposal_v1_smoke_v0"),
    )
    parser.add_argument(
        "--better-frame-extraction-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "better_frame_extraction_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--bbox-adjustment-multiframe-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "bbox_adjustment_proposal_v2_multiframe_smoke_v0"),
    )
    parser.add_argument(
        "--hardware-camera-control-contract-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "hardware_camera_control_contract_v1_smoke_v0"),
    )
    parser.add_argument(
        "--voice-interruption-governance-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "voice_interruption_governance_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--basic-navigation-stabilization-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_guidance_loop_stabilization_test_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_ocr_mainline_final_closure_v1(
        ocr_regression_route_compliance_root=args.ocr_regression_route_compliance_root,
        roi_to_ocrrequest_reference_root=args.roi_to_ocrrequest_reference_root,
        ocr_evidence_pack_adapter_v1_root=args.ocr_evidence_pack_adapter_v1_root,
        mixed_batch_v2_gated_path_root=args.mixed_batch_v2_gated_path_root,
        realvideo_text_bearing_planning_root=args.realvideo_text_bearing_planning_root,
        static_readable_region_discovery_root=args.static_readable_region_discovery_root,
        worldmodel_lookup_reading_framework_root=args.worldmodel_lookup_reading_framework_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        roi_crop_rerun_root=args.roi_crop_rerun_root,
        roi_bbox_expansion_root=args.roi_bbox_expansion_root,
        better_frame_extraction_root=args.better_frame_extraction_root,
        bbox_adjustment_multiframe_root=args.bbox_adjustment_multiframe_root,
        hardware_camera_control_contract_root=args.hardware_camera_control_contract_root,
        voice_interruption_governance_root=args.voice_interruption_governance_root,
        basic_navigation_stabilization_root=args.basic_navigation_stabilization_root,
        workspace_root=args.workspace_root,
    )

    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "ocr_mainline_final_closure_report",
        "ocr_completed_phase_matrix",
        "ocr_validated_capability_summary",
        "ocr_runtime_disabled_summary",
        "ocr_non_claims_register",
        "deferred_ocr_capability_pool",
        "ocr_to_vision_handoff_plan",
        "next_phase_recommendation",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
