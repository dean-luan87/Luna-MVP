#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Phase-Vision-Lightweight-Recognition-Adapter-Selection-001."""

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


def _collect_packs(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(bundle.get("packs"), list):
        return [p for p in bundle["packs"] if isinstance(p, dict)]
    if bundle.get("schema_version") == "vision_provider_input_pack_v0" and isinstance(bundle.get("input_units"), list):
        return [bundle]
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--roi-proposal-root",
        required=True,
        help="Absolute path to vision_roi_proposal_stub output (input pack source).",
    )
    ap.add_argument("--smoke-root", required=True, help="Adapter selection output root.")
    args = ap.parse_args()

    roi_root = _require_abs(args.roi_proposal_root, "--roi-proposal-root")
    root = _require_abs(args.smoke_root, "--smoke-root")

    blockers: List[str] = []
    soft: List[str] = []

    pack_in = roi_root / "vision_provider_input_pack.json"
    if not pack_in.is_file():
        blockers.append("missing_input_vision_provider_input_pack")

    sum_p = root / "vision_recognition_adapter_selection_summary.json"
    reg_p = root / "vision_provider_registry_snapshot.json"
    sel_p = root / "vision_provider_selection_report.json"
    stub_p = root / "vision_provider_stub_result.json"
    mx_p = root / "vision_recognition_candidate_matrix.json"
    aud_p = root / "vision_recognition_adapter_selection_audit_report.json"

    for label, p in (
        ("summary", sum_p),
        ("registry_snapshot", reg_p),
        ("selection_report", sel_p),
        ("stub_result", stub_p),
        ("candidate_matrix", mx_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    input_units_count = 0
    item_count = 0

    if not blockers:
        pack_bundle = _read_json(pack_in)
        packs = _collect_packs(pack_bundle)
        input_units_count = sum(len(p.get("input_units") or []) for p in packs)
        if input_units_count <= 0:
            blockers.append("input_units_count_not_positive")

        reg = _read_json(reg_p)
        if reg.get("schema_version") != "vision_provider_registry_v0":
            blockers.append("registry_schema_version_mismatch")

        sel = _read_json(sel_p)
        if sel.get("selected_provider") != "vision_stub":
            blockers.append("selected_provider_not_vision_stub")
        if sel.get("selected_provider_level") != "stub":
            blockers.append("selected_provider_level_not_stub")
        if sel.get("real_provider_invoked") is not False:
            blockers.append("real_provider_invoked_not_false")

        stub = _read_json(stub_p)
        items = stub.get("items") if isinstance(stub.get("items"), list) else []
        item_count = len(items)
        if item_count <= 0:
            blockers.append("stub_result_items_empty")

        for it in items:
            if not isinstance(it, dict):
                blockers.append("stub_item_not_object")
                continue
            if not str(it.get("unit_id") or "").strip():
                blockers.append("stub_item_missing_unit_id")
            rid = str(it.get("roi_id") or "").strip()
            sur = str(it.get("source_unit_ref") or "").strip()
            if not rid and not sur:
                blockers.append("stub_item_missing_roi_id_and_source_unit_ref")
            if stub.get("synthetic") is not True:
                soft.append("stub_result_synthetic_flag_not_true")

        aud = _read_json(aud_p)
        if aud.get("full_frame_direct_to_provider") is not False:
            blockers.append("full_frame_direct_to_provider_not_false")
        for k, must in (
            ("vision_provider_selection_executed", True),
            ("selected_provider", "vision_stub"),
            ("real_provider_invoked", False),
            ("yolo_invoked", False),
            ("supervision_mainline_invoked", False),
            ("vlm_invoked", False),
            ("ocr_invoked", False),
            ("ai_interpretation_invoked", False),
            ("navigation_decision_invoked", False),
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
        ):
            if aud.get(k) != must:
                blockers.append(f"audit_flag_bad:{k}")

        mx = _read_json(mx_p)
        rows = mx.get("rows") if isinstance(mx.get("rows"), list) else []
        if len(rows) != input_units_count and input_units_count > 0:
            soft.append("candidate_matrix_row_count_mismatch_input_units")

        for r in rows:
            if isinstance(r, dict) and r.get("stub_label") is None and r.get("stub_confidence") is None:
                soft.append("matrix_row_missing_stub_fields")
                break

    if blockers:
        verdict = "NO_GO"
    elif soft:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "vision_recognition_adapter_selection_verifier_report_v0",
        "phase": "Phase-Vision-Lightweight-Recognition-Adapter-Selection-001",
        "roi_proposal_root": str(roi_root),
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "input_units_count": input_units_count,
        "stub_result_items_count": item_count,
    }
    _write_json(root / "vision_recognition_adapter_selection_verifier_report.json", rep)
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
