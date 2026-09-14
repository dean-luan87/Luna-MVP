#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for MidPlatform OCR evidence read-only ingest candidate smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

EXPECTED_SCHEMA = "midplatform_ocr_evidence_ingest_candidate_v0"


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    cand_p = root / "midplatform_ocr_evidence_ingest_candidate.json"
    aud_p = root / "midplatform_ocr_evidence_ingest_audit_report.json"

    if not cand_p.is_file():
        blockers.append("missing:midplatform_ocr_evidence_ingest_candidate.json")
    if not aud_p.is_file():
        blockers.append("missing:midplatform_ocr_evidence_ingest_audit_report.json")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "midplatform_ocr_evidence_ingest_verifier_report_v0",
            "phase": "Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        }
        _write_json(root / "midplatform_ocr_evidence_ingest_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    cand: Dict[str, Any] = _read_json(cand_p)
    aud: Dict[str, Any] = _read_json(aud_p)

    if str(cand.get("schema_version") or "") != EXPECTED_SCHEMA:
        blockers.append("ingest_candidate_schema_version_mismatch")

    evc = int(cand.get("evidence_count") or 0)
    if evc < 1:
        blockers.append("evidence_count_must_be_ge_1")

    if not str(cand.get("text_joined") or "").strip():
        blockers.append("text_joined_must_be_non_empty")

    ebr = cand.get("evidence_by_roi")
    if not isinstance(ebr, dict) or not ebr:
        blockers.append("evidence_by_roi_must_exist")

    gm = cand.get("geometry_matrix")
    if not isinstance(gm, list) or not gm:
        blockers.append("geometry_matrix_must_exist")

    scs = cand.get("source_chain_summary")
    if not isinstance(scs, dict):
        blockers.append("source_chain_summary_must_exist")
    elif "chain" not in scs and "chain_item_count" not in scs:
        blockers.append("source_chain_summary_incomplete")

    ps = cand.get("provider_summary")
    if not isinstance(ps, dict) or not ps:
        blockers.append("provider_summary_must_exist")

    if str(cand.get("ingest_scope") or "") != "read_only_candidate":
        blockers.append("ingest_scope_must_be_read_only_candidate")

    for k in (
        "midplatform_fact_written",
        "scene_delta_written",
        "world_model_written",
        "ai_interpretation_invoked",
        "ocr_provider_invoked",
        "ocr_routing_changed",
    ):
        if aud.get(k) is not False:
            blockers.append(f"audit_must_be_false:{k}")

    soft: List[str] = []
    if not blockers:
        verdict = "GO"
        if isinstance(scs, dict) and int(scs.get("chain_item_count") or 0) == 0:
            verdict = "CONDITIONAL_GO"
            soft.append("source_chain_empty")
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "midplatform_ocr_evidence_ingest_verifier_report_v0",
        "phase": "Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "ingest_candidate_path": str(cand_p.resolve()),
        "evidence_count": evc,
    }
    _write_json(root / "midplatform_ocr_evidence_ingest_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
