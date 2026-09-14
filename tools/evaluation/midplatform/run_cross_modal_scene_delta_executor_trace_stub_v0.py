#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-Scene-Delta-Executor-Trace-Stub-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            candidates.append(parent)
    for parent in candidates:
        if (parent / "_eval_out").is_dir():
            return parent
        sibling = parent.parent / "Luna-Workspace-Min"
        if (sibling / "_eval_out").is_dir():
            return sibling
    return candidates[0] if candidates else here.parents[3]


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


def _notes_md(summary: dict, blocked: dict, audit: dict) -> str:
    return "\n".join(
        [
            "# CrossModal Scene Delta Executor Trace Stub — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- Traces: {summary.get('trace_count')}",
            f"- execution_status: blocked_by_gate",
            f"- Blocked flags: {blocked.get('blocked_reason_flags')}",
            "",
            "## Boundary",
            "",
            "- Trace stub only; not a real executor invocation.",
            f"- real_scene_delta_executor_invoked: {audit.get('real_scene_delta_executor_invoked')}",
            f"- scene_delta_written: {audit.get('scene_delta_written')}",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--scene-delta-candidate-dryrun-root",
        default=str(WS_ROOT / "_eval_out/cross_modal_scene_delta_candidate_dryrun_smoke_v0"),
    )
    ap.add_argument(
        "--gate-evaluator-dryrun-root",
        default=str(WS_ROOT / "_eval_out/cross_modal_scene_delta_gate_evaluator_dryrun_smoke_v0"),
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    sd_root = _require_abs(args.scene_delta_candidate_dryrun_root, "--scene-delta-candidate-dryrun-root")
    gate_root = _require_abs(args.gate_evaluator_dryrun_root, "--gate-evaluator-dryrun-root")

    from capabilities.midplatform.cross_modal_scene_delta_executor_trace_stub_v0 import (
        run_cross_modal_scene_delta_executor_trace_stub_v0,
    )

    summary, traces_doc, matrix_doc, blocked, compat_doc, audit, errs = (
        run_cross_modal_scene_delta_executor_trace_stub_v0(
            scene_delta_candidate_dryrun_root=str(sd_root),
            gate_evaluator_dryrun_root=str(gate_root),
        )
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_scene_delta_executor_trace_stub_summary.json", summary)
    _write_json(out / "cross_modal_scene_delta_executor_trace_stub.json", traces_doc)
    _write_json(out / "cross_modal_scene_delta_executor_planned_step_matrix.json", matrix_doc)
    _write_json(out / "cross_modal_scene_delta_executor_blocked_reason_report.json", blocked)
    _write_json(out / "cross_modal_scene_delta_executor_input_compatibility_report.json", compat_doc)
    _write_json(out / "cross_modal_scene_delta_executor_trace_stub_audit_report.json", audit)
    (out / "cross_modal_scene_delta_executor_trace_stub_notes.md").write_text(
        _notes_md(summary, blocked, audit), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "trace_count": summary.get("trace_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if int(summary.get("trace_count") or 0) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
