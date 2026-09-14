#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-STC-Sampling-Guidance-Policy-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("stc_sampling_guidance_policy_v1_summary.json", "summary"),
    ("stc_safety_trigger_policy_v1.json", "safety_trigger"),
    ("stc_task_trigger_prediction_policy_v1.json", "task_trigger"),
    ("stc_geolocation_route_pre_activation_policy_v1.json", "geolocation_route"),
    ("stc_sampling_validity_window_policy_v1.json", "validity_window"),
    ("stc_motion_aware_ocr_downgrade_policy_v1.json", "motion_downgrade"),
    ("stc_ocr_retry_budget_timeout_policy_v1.json", "retry_budget"),
    ("stc_static_assisted_reading_trigger_policy_v1.json", "static_reading"),
    ("stc_dynamic_short_text_scope_policy_v1.json", "dynamic_short_text"),
    ("stc_ocr_activation_governance_link_report_v1.json", "ocr_activation_link"),
    ("stc_vision_capture_governance_link_report_v1.json", "vision_capture_link"),
    ("stc_current_case_decision_dryrun_v1.json", "current_case"),
    ("stc_sampling_guidance_boundary_report_v1.json", "boundary"),
    ("stc_sampling_guidance_metrics_candidate_report_v1.json", "metrics"),
    ("stc_sampling_guidance_benchmark_link_report_v1.json", "benchmark_link"),
    ("stc_sampling_guidance_system_health_link_report_v1.json", "health_link"),
    ("stc_sampling_guidance_no_write_boundary_report_v1.json", "no_write"),
    ("stc_sampling_guidance_simulation_context_report_v1.json", "sim_report"),
    ("stc_sampling_guidance_non_claims_report_v1.json", "non_claims"),
    ("stc_sampling_guidance_open_followups_v1.json", "followups"),
    ("stc_sampling_guidance_audit_report_v1.json", "audit"),
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

    from capabilities.midplatform.stc_sampling_guidance_policy_v1 import run_stc_sampling_guidance_policy_v1

    result = run_stc_sampling_guidance_policy_v1(
        user_guidance_root=str(roots["user_guidance_root"]),
        ocr_v2_root=str(roots["ocr_v2_root"]),
        multiframe_crop_v2_root=str(roots["multiframe_crop_v2_root"]),
        bbox_adjustment_root=str(roots["bbox_adjustment_root"]),
        text_detector_root=str(roots["text_detector_root"]),
        crop_quality_root=str(roots["crop_quality_root"]),
        evidence_pack_v4_root=str(roots["evidence_pack_v4_root"]),
        multiframe_ocr_v1_root=str(roots["ocr_v2_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "stc_sampling_guidance_notes.md").write_text(
        "\n".join(
            [
                "# STC Sampling Guidance Policy v1",
                "",
                f"- Phase: {summary.get('phase')}",
                "- Dual trigger: safety (background) + task (midplatform pre-activation)",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Policy only; no sampling/OCR/TTS/hardware.",
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
