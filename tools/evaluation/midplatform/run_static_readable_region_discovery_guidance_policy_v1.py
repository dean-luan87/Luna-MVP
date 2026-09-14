#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Static-Readable-Region-Discovery-Guidance-Policy-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("static_readable_region_discovery_guidance_policy_v1_summary.json", "summary"),
    ("static_readable_region_input_intake_matrix_v1.json", "intake"),
    ("static_readable_region_discovery_scope_policy_v1.json", "discovery_scope"),
    ("static_readable_region_candidate_schema_v1.json", "candidate_schema"),
    ("static_readable_region_readability_filtering_policy_v1.json", "readability_filter"),
    ("static_readable_region_classification_policy_v1.json", "classification"),
    ("static_readable_region_user_view_guidance_policy_v1.json", "view_guidance"),
    ("static_readable_region_ranking_selection_policy_v1.json", "ranking"),
    ("static_readable_region_static_capture_handoff_policy_v1.json", "capture_handoff"),
    ("static_readable_region_ocrrequest_future_gate_link_policy_v1.json", "ocr_gate_link"),
    ("static_readable_region_human_staff_assistance_preservation_policy_v1.json", "human_assist"),
    ("static_readable_region_unresolved_expired_candidate_policy_v1.json", "expired"),
    ("static_readable_region_current_case_dryrun_v1.json", "current"),
    ("static_readable_region_boundary_report_v1.json", "boundary"),
    ("static_readable_region_metrics_candidate_report_v1.json", "metrics"),
    ("static_readable_region_benchmark_link_report_v1.json", "benchmark_link"),
    ("static_readable_region_system_health_link_report_v1.json", "health_link"),
    ("static_readable_region_no_write_boundary_report_v1.json", "no_write"),
    ("static_readable_region_simulation_context_report_v1.json", "sim_report"),
    ("static_readable_region_non_claims_report_v1.json", "non_claims"),
    ("static_readable_region_open_followups_v1.json", "followups"),
    ("static_readable_region_audit_report_v1.json", "audit"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if (parent / "_eval_out").is_dir():
                return parent
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
    ap.add_argument("--information-source-root", required=True)
    ap.add_argument("--assisted-static-reading-runtime-root", required=True)
    ap.add_argument("--assisted-static-reading-mode-root", required=True)
    ap.add_argument("--vision-capture-runtime-root", required=True)
    ap.add_argument("--vision-capture-governance-root", required=True)
    ap.add_argument("--ocr-activation-root", required=True)
    ap.add_argument("--stc-sampling-guidance-root", required=True)
    ap.add_argument("--voice-output-plane-adapter-root", required=True)
    ap.add_argument("--voice-guidance-runtime-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.static_readable_region_discovery_guidance_policy_v1 import (
        run_static_readable_region_discovery_guidance_policy_v1,
    )

    result = run_static_readable_region_discovery_guidance_policy_v1(
        information_source_root=str(_require_abs(args.information_source_root, "isrc")),
        assisted_static_reading_runtime_root=str(_require_abs(args.assisted_static_reading_runtime_root, "asm_rt")),
        assisted_static_reading_mode_root=str(_require_abs(args.assisted_static_reading_mode_root, "asm")),
        vision_capture_runtime_root=str(_require_abs(args.vision_capture_runtime_root, "vc")),
        vision_capture_governance_root=str(_require_abs(args.vision_capture_governance_root, "vc_gov")),
        ocr_activation_root=str(_require_abs(args.ocr_activation_root, "ocr_act")),
        stc_sampling_guidance_root=str(_require_abs(args.stc_sampling_guidance_root, "stc")),
        voice_output_plane_adapter_root=str(_require_abs(args.voice_output_plane_adapter_root, "vop")),
        voice_guidance_runtime_root=str(_require_abs(args.voice_guidance_runtime_root, "vg")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "static_readable_region_notes.md").write_text(
        "# Static Readable Region Discovery Guidance Policy v1\n\nLocal discovery within ranked information source areas only; no global text search.\n",
        encoding="utf-8",
    )
    print(json.dumps({"output_root": str(out), "phase_verdict_hint": result["summary"].get("phase_verdict_hint")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
