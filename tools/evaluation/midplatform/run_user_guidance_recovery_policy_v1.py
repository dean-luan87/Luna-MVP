#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-User-Guidance-Recovery-Policy-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("user_guidance_recovery_policy_v1_summary.json", "summary"),
    ("ocr_input_readiness_scope_v1.json", "readiness_scope"),
    ("ocr_activation_recovery_level_policy_v1.json", "activation_levels"),
    ("user_guidance_task_criticality_matrix_v1.json", "task_criticality"),
    ("ocr_input_failure_reason_taxonomy_v1.json", "failure_taxonomy"),
    ("ocr_repairability_classification_policy_v1.json", "repairability"),
    ("user_guidance_action_candidate_policy_v1.json", "user_guidance_actions"),
    ("system_self_adjustment_candidate_policy_v1.json", "system_self_adjustment"),
    ("external_assistance_candidate_policy_v1.json", "external_assistance"),
    ("ocr_not_recoverable_or_not_worth_policy_v1.json", "not_worth_ocr"),
    ("user_guidance_current_case_recovery_decision_v1.json", "current_case"),
    ("ocr_guidance_hardware_placeholder_contract_v1.json", "hardware_placeholder"),
    ("ocr_guidance_stc_vision_capture_link_report_v1.json", "stc_link"),
    ("user_guidance_recovery_boundary_report_v1.json", "boundary"),
    ("user_guidance_recovery_metrics_candidate_report_v1.json", "metrics"),
    ("user_guidance_recovery_benchmark_link_report_v1.json", "benchmark_link"),
    ("user_guidance_recovery_system_health_link_report_v1.json", "health_link"),
    ("user_guidance_recovery_no_write_boundary_report_v1.json", "no_write"),
    ("user_guidance_recovery_simulation_context_report_v1.json", "sim_report"),
    ("user_guidance_recovery_non_claims_report_v1.json", "non_claims"),
    ("user_guidance_recovery_open_followups_v1.json", "followups"),
    ("user_guidance_recovery_audit_report_v1.json", "audit"),
]


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--ocr-v2-root", required=True)
    ap.add_argument("--multiframe-crop-v2-root", required=True)
    ap.add_argument("--bbox-adjustment-root", required=True)
    ap.add_argument("--text-detector-root", required=True)
    ap.add_argument("--crop-quality-root", required=True)
    ap.add_argument("--evidence-pack-v4-root", required=True)
    ap.add_argument("--multiframe-ocr-v1-root", required=True)
    ap.add_argument("--multiframe-crop-v1-root", required=True)
    ap.add_argument("--text-region-tracklet-root", required=True)
    ap.add_argument("--better-frame-root", required=True)
    ap.add_argument("--multiframe-merge-proposal-root", required=True)
    ap.add_argument("--source-validation-v2-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    roots = {
        "ocr_v2_root": _require_abs(args.ocr_v2_root, "ocr_v2"),
        "multiframe_crop_v2_root": _require_abs(args.multiframe_crop_v2_root, "crop_v2"),
        "bbox_adjustment_root": _require_abs(args.bbox_adjustment_root, "bbox"),
        "text_detector_root": _require_abs(args.text_detector_root, "td"),
        "crop_quality_root": _require_abs(args.crop_quality_root, "cq"),
        "evidence_pack_v4_root": _require_abs(args.evidence_pack_v4_root, "ep4"),
        "multiframe_ocr_v1_root": _require_abs(args.multiframe_ocr_v1_root, "ocr_v1"),
        "multiframe_crop_v1_root": _require_abs(args.multiframe_crop_v1_root, "crop_v1"),
        "text_region_tracklet_root": _require_abs(args.text_region_tracklet_root, "tr"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "multiframe_merge_proposal_root": _require_abs(args.multiframe_merge_proposal_root, "mf"),
        "source_validation_v2_root": _require_abs(args.source_validation_v2_root, "sv2"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.user_guidance_recovery_policy_v1 import (
        run_user_guidance_recovery_policy_v1,
    )

    result = run_user_guidance_recovery_policy_v1(
        ocr_v2_root=str(roots["ocr_v2_root"]),
        multiframe_crop_v2_root=str(roots["multiframe_crop_v2_root"]),
        bbox_adjustment_root=str(roots["bbox_adjustment_root"]),
        text_detector_root=str(roots["text_detector_root"]),
        crop_quality_root=str(roots["crop_quality_root"]),
        evidence_pack_v4_root=str(roots["evidence_pack_v4_root"]),
        multiframe_ocr_v1_root=str(roots["multiframe_ocr_v1_root"]),
        multiframe_crop_v1_root=str(roots["multiframe_crop_v1_root"]),
        text_region_tracklet_root=str(roots["text_region_tracklet_root"]),
        better_frame_root=str(roots["better_frame_root"]),
        multiframe_merge_proposal_root=str(roots["multiframe_merge_proposal_root"]),
        source_validation_v2_root=str(roots["source_validation_v2_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "user_guidance_recovery_notes.md").write_text(
        "\n".join(
            [
                "# User Guidance Recovery Policy v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- v2 empty: {summary.get('ocr_v2_empty_result_count_observed')}",
                f"- policy_only: true",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "OCR input readiness + repairability + action candidates; no TTS/hardware/OCR.",
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
                "ocr_v2_empty_result_count_observed": summary.get("ocr_v2_empty_result_count_observed"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
