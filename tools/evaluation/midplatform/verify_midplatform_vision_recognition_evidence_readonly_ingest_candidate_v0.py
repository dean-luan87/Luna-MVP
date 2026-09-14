#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for MidPlatform Vision recognition read-only ingest candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

EXPECTED_SCHEMA = "midplatform_vision_recognition_ingest_candidate_v0"
FORBIDDEN_KEYS = (
    "write_midplatform_fact",
    "write_scene_delta",
    "write_world_model",
    "invoke_ai_interpretation",
    "invoke_navigation_decision",
    "invoke_real_vision_provider",
)


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
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    cand_p = root / "midplatform_vision_recognition_ingest_candidate.json"
    aud_p = root / "midplatform_vision_recognition_ingest_audit_report.json"
    mx_p = root / "midplatform_vision_recognition_ingest_matrix.json"
    scsum_p = root / "midplatform_vision_recognition_ingest_source_chain_summary.json"

    for label, p in (
        ("ingest_candidate", cand_p),
        ("audit", aud_p),
        ("ingest_matrix", mx_p),
        ("source_chain_summary", scsum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"

    if not blockers:
        cand: Dict[str, Any] = _read_json(cand_p)
        aud: Dict[str, Any] = _read_json(aud_p)
        mx = _read_json(mx_p)
        scsum = _read_json(scsum_p)

        if str(cand.get("schema_version") or "") != EXPECTED_SCHEMA:
            blockers.append("ingest_candidate_schema_version_mismatch")

        if str(cand.get("ingest_scope") or "") != "read_only_candidate":
            blockers.append("ingest_scope_not_read_only_candidate")

        n = int(cand.get("evidence_count") or 0)
        if n <= 0:
            blockers.append("evidence_count_not_positive")

        if str(cand.get("provider") or "") != "vision_stub":
            blockers.append("provider_not_vision_stub")
        if str(cand.get("provider_level") or "") != "stub":
            blockers.append("provider_level_not_stub")

        fs = cand.get("fact_status_summary") or {}
        if int(fs.get("not_fact") or 0) != n:
            blockers.append("fact_status_summary_not_fact_mismatch")

        syn = cand.get("synthetic_summary") or {}
        if int(syn.get("synthetic_count") or 0) != n:
            blockers.append("synthetic_count_mismatch")
        if int(syn.get("stub_provider_count") or 0) != n:
            blockers.append("stub_provider_count_mismatch")

        if not isinstance(cand.get("evidence_by_frame"), dict) or not cand.get("evidence_by_frame"):
            blockers.append("evidence_by_frame_missing")
        if not isinstance(cand.get("evidence_by_roi_type"), dict) or not cand.get("evidence_by_roi_type"):
            blockers.append("evidence_by_roi_type_missing")

        if not isinstance(cand.get("geometry_summary"), dict) or not cand.get("geometry_summary"):
            blockers.append("geometry_summary_missing")

        fa = cand.get("forbidden_actions") or {}
        if not isinstance(fa, dict):
            blockers.append("forbidden_actions_not_object")
        else:
            for k in FORBIDDEN_KEYS:
                if k not in fa or fa.get(k) is not True:
                    blockers.append(f"forbidden_actions_missing_or_not_true:{k}")

        rows = mx.get("rows") if isinstance(mx.get("rows"), list) else []
        if len(rows) != n:
            soft.append("ingest_matrix_row_count_mismatch_evidence_count")

        if not isinstance(scsum, dict) or not scsum.get("schema"):
            soft.append("source_chain_summary_schema_soft")

        if aud.get("midplatform_vision_ingest_candidate_generated") is not True:
            blockers.append("audit_candidate_generated_not_true")
        for k, must in (
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
            ("ai_interpretation_invoked", False),
            ("navigation_decision_invoked", False),
            ("real_vision_provider_invoked", False),
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
        "schema": "midplatform_vision_recognition_ingest_verifier_report_v0",
        "phase": "Phase-MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "midplatform_vision_recognition_ingest_verifier_report.json", rep)
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
