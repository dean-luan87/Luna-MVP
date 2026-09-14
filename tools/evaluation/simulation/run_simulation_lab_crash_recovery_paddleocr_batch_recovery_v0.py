#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-SimulationLab-CrashRecovery-PaddleOCR-BatchRecovery-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities").is_dir() or (parent / "capabilities" / "evaluation").is_dir():
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
            if (parent / "_eval_out").is_dir():
                return parent
            return parent
    return here.parents[4]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))
core = WS_ROOT
if (WS_ROOT / "tools").is_symlink():
    core = (WS_ROOT / "tools").resolve().parent
if str(core) not in sys.path:
    sys.path.insert(0, str(core))


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
    ap.add_argument("--crash-recovery-harness-root", required=True)
    ap.add_argument("--developer-full-harness-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--benchmark-planning-root", required=True)
    ap.add_argument("--v1-track-closures-root", required=True)
    ap.add_argument("--child-summary", default="", help="Optional paddleocr_labeled_set_batch_recovery_summary.json")
    ap.add_argument("--workspace-root", default="", help="Luna-Workspace-Min root for command templates")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.evaluation.simulation_lab_crash_recovery_paddleocr_batch_recovery_v0 import (
        run_simulation_lab_crash_recovery_paddleocr_batch_recovery_v0,
    )

    ws = _require_abs(args.workspace_root, "--workspace-root") if args.workspace_root.strip() else WS_ROOT

    (
        summary,
        contract,
        cmd_md,
        merge_report,
        classification,
        action_matrix,
        merged_sim,
        rv_link,
        boundary,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_simulation_lab_crash_recovery_paddleocr_batch_recovery_v0(
        crash_recovery_harness_root=str(_require_abs(args.crash_recovery_harness_root, "--crash-recovery-harness-root")),
        developer_full_harness_root=str(_require_abs(args.developer_full_harness_root, "--developer-full-harness-root")),
        benchmark_real_values_smoke_root=str(
            _require_abs(args.benchmark_real_values_smoke_root, "--benchmark-real-values-smoke-root")
        ),
        benchmark_planning_root=str(_require_abs(args.benchmark_planning_root, "--benchmark-planning-root")),
        v1_track_closures_root=str(_require_abs(args.v1_track_closures_root, "--v1-track-closures-root")),
        child_summary_path=args.child_summary.strip() or None,
        workspace_root=str(ws),
    )

    summary["output_root"] = str(out)
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs else "NO_GO"

    _write_json(out / "simulation_lab_crash_recovery_paddleocr_batch_recovery_summary.json", summary)
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_contract.json", contract)
    (out / "simulation_lab_crash_recovery_paddleocr_child_command_suggestion.md").write_text(cmd_md + "\n", encoding="utf-8")
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_child_summary_merge_report.json", merge_report)
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_crash_signal_classification_report.json", classification)
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_recovery_action_matrix.json", action_matrix)
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_merged_simulation_summary.json", merged_sim)
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_real_values_link_report.json", rv_link)
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_boundary_report.json", boundary)
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_non_claims_report.json", non_claims)
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_open_followups.json", followups)
    _write_json(out / "simulation_lab_crash_recovery_paddleocr_audit_report.json", audit)
    (out / "simulation_lab_crash_recovery_paddleocr_notes.md").write_text(
        "\n".join(
            [
                "# Simulation Lab crash_recovery × PaddleOCR Batch Recovery",
                "",
                f"- phase: {summary.get('phase')}",
                f"- recovery_status: {summary.get('recovery_status')}",
                f"- child_summary_provided: {summary.get('child_summary_provided')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Does not auto-run PaddleOCR heavy. Engineering robustness only.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "recovery_status": summary.get("recovery_status"),
                "child_summary_provided": summary.get("child_summary_provided"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
