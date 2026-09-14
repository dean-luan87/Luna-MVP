#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-Fusion-Candidate-Review-Queue-001 runner."""

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
            "# CrossModal Fusion Review Queue — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- Queue items: {summary.get('queue_item_count')}",
            f"- Fusion dry-run root: `{summary.get('fusion_candidate_dryrun_root')}`",
            f"- all_candidates_pending_review: {policy.get('all_candidates_pending_review')}",
            "",
            "## Boundary",
            "",
            "- Review queue only; no auto-approve; no fact write.",
            f"- auto_approve_invoked: {audit.get('auto_approve_invoked')}",
            f"- approval_granted: {audit.get('approval_granted')}",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--fusion-candidate-dryrun-root",
        default=str(WS_ROOT / "_eval_out/cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0"),
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    dryrun_root = _require_abs(args.fusion_candidate_dryrun_root, "--fusion-candidate-dryrun-root")

    from capabilities.midplatform.cross_modal_fusion_review_queue_v0 import (
        run_cross_modal_fusion_review_queue_v0,
    )

    summary, candidates_doc, matrix_doc, risk_summary, policy, audit, errs = (
        run_cross_modal_fusion_review_queue_v0(
            fusion_candidate_dryrun_root=str(dryrun_root),
        )
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_fusion_review_queue_summary.json", summary)
    _write_json(out / "cross_modal_fusion_review_queue_candidates.json", candidates_doc)
    _write_json(out / "cross_modal_fusion_review_queue_matrix.json", matrix_doc)
    _write_json(out / "cross_modal_fusion_review_risk_summary.json", risk_summary)
    _write_json(out / "cross_modal_fusion_review_queue_policy_report.json", policy)
    _write_json(out / "cross_modal_fusion_review_queue_audit_report.json", audit)
    (out / "cross_modal_fusion_review_queue_notes.md").write_text(
        _notes_md(summary, policy, audit), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "queue_item_count": summary.get("queue_item_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if int(summary.get("queue_item_count") or 0) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
