#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-User-Guidance-Recovery-Runtime-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("user_guidance_recovery_runtime_dryrun_v1_summary.json", "summary"),
    ("user_guidance_runtime_input_intake_matrix_v1.json", "intake"),
    ("user_guidance_trigger_evaluation_matrix_v1.json", "triggers"),
    ("user_guidance_runtime_plan_v1.json", "plan"),
    ("user_guidance_prompt_candidate_matrix_v1.json", "prompts"),
    ("user_guidance_response_state_transition_dryrun_v1.json", "transitions"),
    ("user_guidance_static_capture_entry_candidate_v1.json", "static_entry"),
    ("user_guidance_system_self_adjustment_escalation_candidate_v1.json", "system_escalation"),
    ("user_guidance_external_assistance_escalation_candidate_v1.json", "external_escalation"),
    ("user_guidance_visual_semantic_fallback_candidate_v1.json", "visual_fallback"),
    ("user_guidance_expired_long_term_context_candidate_v1.json", "expired_long_term"),
    ("user_guidance_runtime_decision_trace_v1.json", "trace"),
    ("user_guidance_final_dryrun_decision_v1.json", "final"),
    ("user_guidance_runtime_boundary_report_v1.json", "boundary"),
    ("user_guidance_runtime_metrics_candidate_report_v1.json", "metrics"),
    ("user_guidance_runtime_benchmark_link_report_v1.json", "benchmark_link"),
    ("user_guidance_runtime_system_health_link_report_v1.json", "health_link"),
    ("user_guidance_runtime_no_write_boundary_report_v1.json", "no_write"),
    ("user_guidance_runtime_simulation_context_report_v1.json", "sim_report"),
    ("user_guidance_runtime_non_claims_report_v1.json", "non_claims"),
    ("user_guidance_runtime_open_followups_v1.json", "followups"),
    ("user_guidance_runtime_audit_report_v1.json", "audit"),
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
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--vision-capture-governance-root", required=True)
    ap.add_argument("--user-guidance-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-sampling-guidance-root", required=True)
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
        "vision_capture_runtime_root": _require_abs(args.vision_capture_runtime_root, "vc_runtime"),
        "vision_capture_governance_root": _require_abs(args.vision_capture_governance_root, "vc_gov"),
        "user_guidance_root": _require_abs(args.user_guidance_root, "ug"),
        "ocr_activation_root": _require_abs(args.ocr_activation_root, "ocr_act"),
        "stc_sampling_guidance_root": _require_abs(args.stc_sampling_guidance_root, "stc"),
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

    from capabilities.midplatform.user_guidance_recovery_runtime_dryrun_v1 import (
        run_user_guidance_recovery_runtime_dryrun_v1,
    )

    result = run_user_guidance_recovery_runtime_dryrun_v1(
        vision_capture_runtime_root=str(roots["vision_capture_runtime_root"]),
        vision_capture_governance_root=str(roots["vision_capture_governance_root"]),
        user_guidance_root=str(roots["user_guidance_root"]),
        ocr_activation_root=str(roots["ocr_activation_root"]),
        stc_sampling_guidance_root=str(roots["stc_sampling_guidance_root"]),
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

    (out / "user_guidance_runtime_notes.md").write_text(
        "\n".join(
            [
                "# User Guidance Recovery Runtime DryRun v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- Vision capture decision: {summary.get('vision_capture_decision_observed')}",
                f"- Primary path: ASSISTED_STATIC_CAPTURE_GUIDANCE",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Dry-run only; no TTS/voice/guidance/camera/OCR/hardware/fact write.",
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
