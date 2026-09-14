#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Static-Reading-Task-Scene-Context-Reevaluation-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("static_reading_task_scene_context_reevaluation_dryrun_v1_summary.json", "summary"),
    ("static_reading_task_scene_reevaluation_input_intake_matrix_v1.json", "intake"),
    ("static_reading_task_scene_candidate_reevaluation_matrix_v1.json", "reeval_matrix"),
    ("static_reading_task_scene_completeness_summary_v1.json", "completeness"),
    ("static_reading_task_scene_confirmation_requirement_matrix_v1.json", "confirmation"),
    ("static_reading_information_source_query_candidate_collection_v1.json", "query_collection"),
    ("static_reading_isrc_runtime_readiness_candidate_v1.json", "isrc_readiness"),
    ("static_reading_rrd_runtime_readiness_candidate_v1.json", "rrd_readiness"),
    ("static_reading_task_scene_human_staff_reevaluation_v1.json", "human_reeval"),
    ("static_reading_task_scene_reevaluation_long_term_candidate_link_v1.json", "long_term"),
    ("static_reading_task_scene_reevaluation_decision_trace_v1.json", "trace"),
    ("static_reading_task_scene_reevaluation_final_decision_v1.json", "final"),
    ("static_reading_task_scene_reevaluation_boundary_report_v1.json", "boundary"),
    ("static_reading_task_scene_reevaluation_metrics_candidate_report_v1.json", "metrics"),
    ("static_reading_task_scene_reevaluation_benchmark_link_report_v1.json", "benchmark_link"),
    ("static_reading_task_scene_reevaluation_system_health_link_report_v1.json", "health_link"),
    ("static_reading_task_scene_reevaluation_no_write_boundary_report_v1.json", "no_write"),
    ("static_reading_task_scene_reevaluation_simulation_context_report_v1.json", "sim_report"),
    ("static_reading_task_scene_reevaluation_non_claims_report_v1.json", "non_claims"),
    ("static_reading_task_scene_reevaluation_open_followups_v1.json", "followups"),
    ("static_reading_task_scene_reevaluation_audit_report_v1.json", "audit"),
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
    ap.add_argument("--response-parsing-root", required=True)
    ap.add_argument("--clarification-runtime-root", required=True)
    ap.add_argument("--task-scene-runtime-root", required=True)
    ap.add_argument("--task-scene-policy-root", required=True)
    ap.add_argument("--information-source-root", required=True)
    ap.add_argument("--readable-region-policy-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.static_reading_task_scene_context_reevaluation_dryrun_v1 import (
        run_static_reading_task_scene_context_reevaluation_dryrun_v1,
    )

    result = run_static_reading_task_scene_context_reevaluation_dryrun_v1(
        response_parsing_root=str(_require_abs(args.response_parsing_root, "parsing")),
        clarification_runtime_root=str(_require_abs(args.clarification_runtime_root, "uclar_rt")),
        task_scene_runtime_root=str(_require_abs(args.task_scene_runtime_root, "tsc_rt")),
        task_scene_policy_root=str(_require_abs(args.task_scene_policy_root, "tsc")),
        information_source_root=str(_require_abs(args.information_source_root, "isrc")),
        readable_region_policy_root=str(_require_abs(args.readable_region_policy_root, "rrd")),
        benchmark_smoke_root=str(_require_abs(args.benchmark_smoke_root, "bench")),
        system_health_root=str(_require_abs(args.system_health_root, "health")),
        simulation_root=str(_require_abs(args.simulation_root, "sim")),
        workspace_root=str(WS_ROOT),
    )

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "static_reading_task_scene_reevaluation_notes.md").write_text(
        "# TSC Reevaluation DryRun v1\n\n"
        "Parsing candidates → ISRC query candidates; RRD blocked; no fact write.\n",
        encoding="utf-8",
    )
    print(json.dumps({"output_root": str(out), "phase_verdict_hint": result["summary"].get("phase_verdict_hint")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
