#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Phase-Vision-Recognition-Evidence-Pack-Stub-001."""

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
    ap.add_argument("--smoke-root", required=True, help="Evidence pack output root.")
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")

    blockers: List[str] = []
    soft: List[str] = []

    pack_p = root / "vision_recognition_evidence_pack.json"
    aud_p = root / "vision_recognition_evidence_audit_report.json"

    for label, p in (("evidence_pack", pack_p), ("audit", aud_p)):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    item_count = 0

    if not blockers:
        ep = _read_json(pack_p)
        if ep.get("schema_version") != "vision_recognition_evidence_pack_v0":
            blockers.append("evidence_pack_schema_version_mismatch")

        items = ep.get("items") if isinstance(ep.get("items"), list) else []
        item_count = len(items)
        if item_count <= 0:
            blockers.append("evidence_items_empty")

        pt = ep.get("provider_trace") or {}
        if str(pt.get("provider") or "") != "vision_stub":
            blockers.append("provider_trace_provider_not_vision_stub")
        if pt.get("real_provider_invoked") is not False:
            blockers.append("provider_trace_real_provider_invoked_not_false")

        for it in items:
            if not isinstance(it, dict):
                blockers.append("evidence_item_not_object")
                continue
            if not str(it.get("source_frame_id") or "").strip():
                blockers.append("evidence_item_missing_source_frame_id")
            rid = str(it.get("roi_id") or "").strip()
            uid = str(it.get("unit_id") or "").strip()
            if not rid and not uid:
                blockers.append("evidence_item_missing_roi_id_and_unit_id")
            if it.get("synthetic") is not True:
                blockers.append("evidence_item_synthetic_not_true")
            if it.get("stub_provider") is not True:
                blockers.append("evidence_item_stub_provider_not_true")
            if str(it.get("fact_status") or "") != "not_fact":
                blockers.append("evidence_item_fact_status_not_not_fact")
            bb = it.get("bbox_in_frame")
            if not isinstance(bb, list) or len(bb) != 4:
                soft.append("evidence_item_bbox_in_frame_incomplete")
            elif all(int(x) == 0 for x in bb):
                soft.append("evidence_item_bbox_in_frame_all_zero")

        if str(ep.get("fact_status") or "") != "not_fact":
            blockers.append("pack_fact_status_not_not_fact")

        aud = _read_json(aud_p)
        if aud.get("vision_evidence_pack_generated") is not True:
            blockers.append("audit_vision_evidence_pack_generated_not_true")
        for k, must in (
            ("real_provider_invoked", False),
            ("yolo_invoked", False),
            ("supervision_mainline_invoked", False),
            ("vlm_invoked", False),
            ("ocr_invoked", False),
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
            ("ai_interpretation_invoked", False),
            ("navigation_decision_invoked", False),
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
        "schema": "vision_recognition_evidence_pack_verifier_report_v0",
        "phase": "Phase-Vision-Recognition-Evidence-Pack-Stub-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "evidence_items_count": item_count,
    }
    _write_json(root / "vision_recognition_evidence_pack_verifier_report.json", rep)
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
