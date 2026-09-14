#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-Scene-Delta-Gate-Evaluator-DryRun-001 runner."""

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


def _notes_md(summary: dict, policy: dict, audit: dict) -> str:
    return "\n".join(
        [
            "# CrossModal Scene Delta Gate Evaluator DryRun — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- Evaluations: {summary.get('evaluation_count')}",
            f"- Decision: hold_for_review (all)",
            f"- write_allowed: {policy.get('write_allowed')}",
            "",
            "## Boundary",
            "",
            "- Gate evaluator dry-run only; not an approver; no write.",
            f"- scene_delta_executor_invoked: {audit.get('scene_delta_executor_invoked')}",
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
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    sd_root = _require_abs(args.scene_delta_candidate_dryrun_root, "--scene-delta-candidate-dryrun-root")

    from capabilities.midplatform.cross_modal_scene_delta_gate_evaluator_dryrun_v0 import (
        run_cross_modal_scene_delta_gate_evaluator_dryrun_v0,
    )

    summary, result_doc, reason_matrix, policy, chain, audit, errs = (
        run_cross_modal_scene_delta_gate_evaluator_dryrun_v0(
            scene_delta_candidate_dryrun_root=str(sd_root),
        )
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_scene_delta_gate_evaluation_summary.json", summary)
    _write_json(out / "cross_modal_scene_delta_gate_evaluation_result.json", result_doc)
    _write_json(out / "cross_modal_scene_delta_gate_reason_matrix.json", reason_matrix)
    _write_json(out / "cross_modal_scene_delta_gate_policy_report.json", policy)
    _write_json(out / "cross_modal_scene_delta_gate_source_chain_summary.json", chain)
    _write_json(out / "cross_modal_scene_delta_gate_evaluator_audit_report.json", audit)
    (out / "cross_modal_scene_delta_gate_evaluator_notes.md").write_text(
        _notes_md(summary, policy, audit), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "evaluation_count": summary.get("evaluation_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if int(summary.get("evaluation_count") or 0) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
