#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Phase-Vision-Recognition-Evidence-ReadOnly-Consumer-001."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List


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
    ap.add_argument(
        "--evidence-pack-root",
        required=True,
        help="Absolute path to evidence pack stub output (input pack source).",
    )
    ap.add_argument("--smoke-root", required=True, help="Readonly consumer output root.")
    args = ap.parse_args()

    ev_root = _require_abs(args.evidence_pack_root, "--evidence-pack-root")
    root = _require_abs(args.smoke_root, "--smoke-root")

    blockers: List[str] = []
    soft: List[str] = []

    pack_in = ev_root / "vision_recognition_evidence_pack.json"
    if not pack_in.is_file():
        blockers.append("missing_input_vision_recognition_evidence_pack")

    view_p = root / "vision_recognition_evidence_readonly_consumer_view.json"
    aud_p = root / "vision_recognition_evidence_readonly_consumer_audit_report.json"

    for label, p in (("consumer_view", view_p), ("audit", aud_p)):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"

    if not blockers:
        view = _read_json(view_p)
        if view.get("schema_version") != "vision_recognition_evidence_readonly_consumer_view_v0":
            blockers.append("consumer_view_schema_mismatch")

        n = int(view.get("evidence_count_observed") or 0)
        if n <= 0:
            blockers.append("evidence_count_not_positive")

        if str(view.get("provider") or "") != "vision_stub":
            blockers.append("provider_not_vision_stub")

        fs = view.get("fact_status_summary") or {}
        if int(fs.get("not_fact") or 0) != n:
            blockers.append("fact_status_summary_not_fact_mismatch")

        syn = view.get("synthetic_summary") or {}
        if int(syn.get("synthetic_count") or 0) != n:
            blockers.append("synthetic_count_mismatch")
        if int(syn.get("stub_provider_count") or 0) != n:
            blockers.append("stub_provider_count_mismatch")

        by_f = view.get("evidence_by_frame")
        if not isinstance(by_f, dict) or len(by_f) == 0:
            blockers.append("evidence_by_frame_empty")

        by_r = view.get("evidence_by_roi_type")
        if not isinstance(by_r, dict) or len(by_r) == 0:
            blockers.append("evidence_by_roi_type_empty")

        geom = view.get("geometry_summary") or {}
        if int(geom.get("bbox_in_frame_count") or 0) <= 0:
            blockers.append("bbox_in_frame_count_not_positive")

        if not isinstance(view.get("source_chain_summary"), dict):
            soft.append("source_chain_summary_missing_or_non_object")

        aud = _read_json(aud_p)
        if aud.get("vision_evidence_readonly_consumer_executed") is not True:
            blockers.append("audit_consumer_executed_not_true")
        for k, must in (
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
            ("ai_interpretation_invoked", False),
            ("navigation_decision_invoked", False),
            ("yolo_invoked", False),
            ("supervision_mainline_invoked", False),
            ("vlm_invoked", False),
            ("ocr_invoked", False),
        ):
            if aud.get(k) is not must:
                blockers.append(f"audit_flag_bad:{k}")

    if blockers:
        verdict = "NO_GO"
    elif soft:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "vision_recognition_evidence_readonly_consumer_verifier_report_v0",
        "phase": "Phase-Vision-Recognition-Evidence-ReadOnly-Consumer-001",
        "evidence_pack_root": str(ev_root),
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "vision_recognition_evidence_readonly_consumer_verifier_report.json", rep)
    print(
        json.dumps(
            {"smoke_root": str(root), "verdict": verdict, "blockers": blockers, "soft_notes": soft},
            ensure_ascii=False,
        )
    )
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
