#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Capture-Governance-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("vision_capture_governance_v1_summary.json", "summary"),
    ("vision_capture_quality_gate_policy_v1.json", "quality_gate"),
    ("vision_frame_readiness_gate_v1.json", "frame_readiness"),
    ("vision_region_crop_text_readiness_gate_v1.json", "region_crop_text"),
    ("vision_dynamic_vs_static_capture_policy_v1.json", "dynamic_vs_static"),
    ("vision_capture_hardware_placeholder_contract_v1.json", "hardware"),
    ("vision_capture_system_self_adjustment_policy_v1.json", "system_self_adjustment"),
    ("vision_capture_user_guidance_policy_v1.json", "user_guidance"),
    ("vision_capture_failure_reason_taxonomy_v1.json", "failure_taxonomy"),
    ("vision_capture_retry_timeout_stale_policy_v1.json", "retry_stale"),
    ("vision_expired_capture_candidate_policy_v1.json", "expired_capture"),
    ("vision_long_term_context_candidate_routing_policy_v1.json", "long_term_routing"),
    ("vision_safety_marker_capture_path_policy_v1.json", "safety_path"),
    ("vision_task_triggered_capture_path_policy_v1.json", "task_path"),
    ("vision_capture_current_case_decision_dryrun_v1.json", "current_case"),
    ("vision_capture_ocr_activation_link_report_v1.json", "ocr_activation_link"),
    ("vision_capture_stc_link_report_v1.json", "stc_link"),
    ("vision_capture_governance_boundary_report_v1.json", "boundary"),
    ("vision_capture_governance_metrics_candidate_report_v1.json", "metrics"),
    ("vision_capture_governance_benchmark_link_report_v1.json", "benchmark_link"),
    ("vision_capture_governance_system_health_link_report_v1.json", "health_link"),
    ("vision_capture_governance_no_write_boundary_report_v1.json", "no_write"),
    ("vision_capture_governance_simulation_context_report_v1.json", "sim_report"),
    ("vision_capture_governance_non_claims_report_v1.json", "non_claims"),
    ("vision_capture_governance_open_followups_v1.json", "followups"),
    ("vision_capture_governance_audit_report_v1.json", "audit"),
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
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-sampling-guidance-root", required=True)
    ap.add_argument("--user-guidance-root", required=True)
    ap.add_argument("--ocr-v2-root", required=True)
    ap.add_argument("--multiframe-crop-v2-root", required=True)
    ap.add_argument("--bbox-adjustment-root", required=True)
    ap.add_argument("--text-detector-root", required=True)
    ap.add_argument("--crop-quality-root", required=True)
    ap.add_argument("--evidence-pack-v4-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    roots = {
        "ocr_activation_root": _require_abs(args.ocr_activation_root, "ocr_activation"),
        "stc_sampling_guidance_root": _require_abs(args.stc_sampling_guidance_root, "stc"),
        "user_guidance_root": _require_abs(args.user_guidance_root, "ug"),
        "ocr_v2_root": _require_abs(args.ocr_v2_root, "ocr_v2"),
        "multiframe_crop_v2_root": _require_abs(args.multiframe_crop_v2_root, "crop_v2"),
        "bbox_adjustment_root": _require_abs(args.bbox_adjustment_root, "bbox"),
        "text_detector_root": _require_abs(args.text_detector_root, "td"),
        "crop_quality_root": _require_abs(args.crop_quality_root, "cq"),
        "evidence_pack_v4_root": _require_abs(args.evidence_pack_v4_root, "ep4"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.vision_capture_governance_v1 import (
        run_vision_capture_governance_v1,
    )

    result = run_vision_capture_governance_v1(
        ocr_activation_root=str(roots["ocr_activation_root"]),
        stc_sampling_guidance_root=str(roots["stc_sampling_guidance_root"]),
        user_guidance_root=str(roots["user_guidance_root"]),
        ocr_v2_root=str(roots["ocr_v2_root"]),
        multiframe_crop_v2_root=str(roots["multiframe_crop_v2_root"]),
        bbox_adjustment_root=str(roots["bbox_adjustment_root"]),
        text_detector_root=str(roots["text_detector_root"]),
        crop_quality_root=str(roots["crop_quality_root"]),
        evidence_pack_v4_root=str(roots["evidence_pack_v4_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "vision_capture_governance_notes.md").write_text(
        "\n".join(
            [
                "# Vision Capture Governance v1",
                "",
                f"- Phase: {summary.get('phase')}",
                "- Input governance after OCR activation (not camera runtime)",
                "- Quality gate / readiness / dynamic-static / hardware placeholder",
                "- Stale capture → long-term candidate routing (not discard)",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Policy only; no camera/OCR/TTS/hardware/fact write.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": summary.get("phase_verdict_hint")},
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
