#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Static-Readable-Region-Discovery-Runtime-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("static_readable_region_discovery_runtime_dryrun_v1_summary.json", "summary"),
    ("static_readable_region_runtime_input_intake_matrix_v1.json", "intake"),
    ("static_readable_region_ranked_source_area_intake_matrix_v1.json", "ranked_intake"),
    ("static_readable_region_candidate_collection_v1.json", "collection"),
    ("static_readable_region_runtime_classification_matrix_v1.json", "classification"),
    ("static_readable_region_runtime_readability_filtering_matrix_v1.json", "filtering"),
    ("static_readable_region_user_view_guidance_candidate_collection_v1.json", "guidance"),
    ("static_readable_region_static_capture_handoff_candidate_v1.json", "capture_handoff"),
    ("static_readable_region_ocrrequest_future_gate_candidate_v1.json", "ocr_gate"),
    ("static_readable_region_human_staff_assistance_region_candidate_v1.json", "human_assist"),
    ("static_readable_region_runtime_unresolved_expired_candidate_link_v1.json", "unresolved_link"),
    ("static_readable_region_runtime_decision_trace_v1.json", "trace"),
    ("static_readable_region_runtime_final_decision_v1.json", "final"),
    ("static_readable_region_runtime_boundary_report_v1.json", "boundary"),
    ("static_readable_region_runtime_metrics_candidate_report_v1.json", "metrics"),
    ("static_readable_region_runtime_benchmark_link_report_v1.json", "benchmark_link"),
    ("static_readable_region_runtime_system_health_link_report_v1.json", "health_link"),
    ("static_readable_region_runtime_no_write_boundary_report_v1.json", "no_write"),
    ("static_readable_region_runtime_simulation_context_report_v1.json", "sim_report"),
    ("static_readable_region_runtime_non_claims_report_v1.json", "non_claims"),
    ("static_readable_region_runtime_open_followups_v1.json", "followups"),
    ("static_readable_region_runtime_audit_report_v1.json", "audit"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
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
    ap.add_argument("--isrc-runtime-root", required=True)
    ap.add_argument("--tsc-reevaluation-root", required=True)
    ap.add_argument("--readable-region-policy-root", required=True)
    ap.add_argument("--information-source-policy-root", required=True)
    ap.add_argument("--task-scene-policy-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.static_readable_region_discovery_runtime_dryrun_v1 import (
        run_static_readable_region_discovery_runtime_dryrun_v1,
    )

    result = run_static_readable_region_discovery_runtime_dryrun_v1(
        isrc_runtime_root=str(_require_abs(args.isrc_runtime_root, "isrc")),
        tsc_reevaluation_root=str(_require_abs(args.tsc_reevaluation_root, "reeval")),
        readable_region_policy_root=str(_require_abs(args.readable_region_policy_root, "rrd")),
        information_source_policy_root=str(_require_abs(args.information_source_policy_root, "isrc_policy")),
        task_scene_policy_root=str(_require_abs(args.task_scene_policy_root, "tsc")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "static_readable_region_runtime_notes.md").write_text(
        "# RRD Runtime DryRun v1\n\n"
        "17 ranked source areas → readable region candidates; no camera/detector/OCR/bbox/fact.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": result["summary"].get("phase_verdict_hint")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
