#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Phase-Vision-Frame-Input-Governance-001."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame-trace-root", required=True)
    ap.add_argument("--smoke-root", required=True, help="Governance output root (same as --output-root from runner).")
    args = ap.parse_args()

    trace_root = _require_abs(args.frame_trace_root, "--frame-trace-root")
    root = _require_abs(args.smoke_root, "--smoke-root")

    blockers: List[str] = []
    soft: List[str] = []

    if not trace_root.is_dir():
        blockers.append("frame_trace_root_missing")

    sum_p = root / "vision_frame_input_governance_summary.json"
    mx_p = root / "vision_frame_input_governance_matrix.json"
    cand_p = root / "vision_provider_input_candidate.json"
    aud_p = root / "vision_frame_input_governance_audit_report.json"

    for label, p in (("summary", sum_p), ("matrix", mx_p), ("candidate", cand_p), ("audit", aud_p)):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    accepted = 0
    eligible_roi = 0

    if not blockers:
        summary = _read_json(sum_p)
        mx = _read_json(mx_p)
        cand = _read_json(cand_p)
        aud = _read_json(aud_p)

        total = int(summary.get("total_frames") or 0)
        if total <= 0:
            blockers.append("total_frames_not_positive")

        accepted = int(summary.get("accepted_frames") or 0)
        eligible_roi = int(summary.get("eligible_for_roi_proposal_count") or 0)
        elig_rec = summary.get("eligible_for_recognition_count")

        if accepted <= 0:
            soft.append("zero_accepted_frames")
        if eligible_roi <= 0:
            soft.append("zero_eligible_for_roi_proposal")

        if elig_rec != 0:
            blockers.append("eligible_for_recognition_count_must_be_zero")

        rows = mx.get("rows") if isinstance(mx.get("rows"), list) else []
        for r in rows:
            if r.get("eligible_for_recognition") is not False:
                blockers.append("matrix_row_eligible_for_recognition_must_be_false")

        if cand.get("schema_version") != "vision_frame_input_candidate_v0":
            blockers.append("candidate_schema_version_mismatch")
        if cand.get("candidate_scope") != "input_governance_only":
            blockers.append("candidate_scope_not_input_governance_only")

        forbidden = cand.get("forbidden_next_stages") or []
        if not isinstance(forbidden, list) or "vision_recognition_provider" not in forbidden:
            blockers.append("forbidden_next_stages_missing_vision_recognition_provider")

        for k in (
            "real_camera_invoked",
            "yolo_invoked",
            "ocr_invoked",
            "vlm_invoked",
            "supervision_mainline_invoked",
            "vision_recognition_provider_invoked",
            "navigation_decision_invoked",
            "midplatform_fact_written",
            "scene_delta_written",
            "world_model_written",
            "ai_interpretation_invoked",
        ):
            if aud.get(k) is not False:
                blockers.append(f"audit_flag_not_false:{k}")

        if aud.get("frame_input_governance_executed") is not True:
            blockers.append("frame_input_governance_executed_not_true")

    if blockers:
        verdict = "NO_GO"
    elif accepted <= 0 or eligible_roi <= 0:
        verdict = "CONDITIONAL_GO"
        soft.append("governance_degraded_accepted_or_roi_eligible_zero")
    else:
        verdict = "GO"

    rep = {
        "schema": "vision_frame_input_governance_verifier_report_v0",
        "phase": "Phase-Vision-Frame-Input-Governance-001",
        "frame_trace_root": str(trace_root),
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "vision_frame_input_governance_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
