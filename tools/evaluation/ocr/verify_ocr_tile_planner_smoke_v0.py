#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR tile planner smoke (Phase-OCR-Tile-Planner-And-Coordinate-Reconstruction-001)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

WS_ROOT = Path(__file__).resolve().parents[3]
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


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


def _forbidden_audit_true(aud: Dict[str, Any]) -> List[str]:
    bad: List[str] = []
    for k in (
        "real_provider_invoked",
        "paddleocr_invoked",
        "rapidocr_replaced",
        "ocr_routing_changed",
        "midplatform_invoked",
        "world_model_written",
    ):
        if aud.get(k) is True:
            bad.append(f"audit_forbidden_true:{k}")
    return bad


def _parse_ct(unit: Dict[str, Any]) -> Dict[str, Any]:
    raw = unit.get("coordinate_transform")
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            o = json.loads(raw)
            return o if isinstance(o, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    res_p = root / "ocr_mainline_bridge_result.json"
    plan_p = root / "ocr_tile_plan.json"
    pack_p = root / "ocr_provider_input_pack.json"
    mtx_p = root / "ocr_tile_coordinate_transform_matrix.json"
    aud_p = root / "ocr_tile_planner_audit_report.json"

    for name, p in (("result", res_p), ("tile_plan", plan_p), ("provider_pack", pack_p), ("coord_matrix", mtx_p), ("audit", aud_p)):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    if blockers:
        rep = {"schema": "ocr_tile_planner_verifier_report_v0", "smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}
        _write_json(root / "ocr_tile_planner_verifier_report.json", rep)
        print(json.dumps(rep, ensure_ascii=False))
        return 2

    res: Dict[str, Any] = _read_json(res_p)
    plan: Dict[str, Any] = _read_json(plan_p)
    pack: Dict[str, Any] = _read_json(pack_p)
    mtx: Dict[str, Any] = _read_json(mtx_p)
    aud: Dict[str, Any] = _read_json(aud_p)

    if not plan.get("schema_version"):
        blockers.append("tile_plan_missing_schema")

    from capabilities.ocr_runtime.ocr_provider_input_pack_v0 import validate_provider_input_pack_v0

    blockers.extend([f"pack:{e}" for e in validate_provider_input_pack_v0(pack)])

    pol = pack.get("processing_policy") if isinstance(pack.get("processing_policy"), dict) else {}
    if str(pol.get("strategy") or "") != "tile":
        blockers.append("processing_policy_strategy_must_be_tile")

    units = pack.get("input_units") if isinstance(pack.get("input_units"), list) else []
    if len(units) <= 1:
        blockers.append("input_units_need_multiple_tiles")

    schain = pack.get("source_chain")
    if not isinstance(schain, list):
        blockers.append("source_chain_missing")
    else:
        for token in (
            "original_image_ref:",
            "tile_plan_created",
            "tile_generated",
            "coordinate_transform_recorded",
            "tile_plan_raw_count:",
            "tile_materialized_count:",
            "tile_truncated_to_budget:",
            "coverage_complete:",
        ):
            if not any(isinstance(s, str) and token in s for s in schain):
                blockers.append(f"source_chain_missing:{token}")

    for i, u in enumerate(units):
        if not isinstance(u, dict):
            blockers.append(f"unit_{i}_not_dict")
            continue
        if u.get("unit_type") != "tile":
            blockers.append(f"unit_{i}_type_not_tile")
        bbox = u.get("bbox_in_original")
        if not isinstance(bbox, list) or len(bbox) != 4:
            blockers.append(f"unit_{i}_bbox_invalid")
        if u.get("overlap_ratio") is None:
            blockers.append(f"unit_{i}_missing_overlap_ratio")
        ct = _parse_ct(u)
        for k in ("original_width", "original_height", "tile_bbox_in_original", "offset_x", "offset_y", "scale_x", "scale_y"):
            if k not in ct:
                blockers.append(f"unit_{i}_ct_missing:{k}")

    if not isinstance(mtx.get("units"), list) or len(mtx.get("units") or []) != len(units):
        blockers.append("coordinate_matrix_units_mismatch")

    if aud.get("original_image_used_directly") is True:
        blockers.append("must_not_original_image_direct")

    if aud.get("coordinate_transform_recorded") is not True:
        blockers.append("coordinate_transform_recorded_must_be_true")

    if aud.get("tile_applied") is not True:
        blockers.append("tile_applied_must_be_true")

    blockers.extend(_forbidden_audit_true(aud))

    prov = res.get("provider_result") if isinstance(res.get("provider_result"), dict) else {}
    if str(res.get("status")) != "success":
        blockers.append("bridge_status_must_be_success")
    if int(prov.get("input_unit_count") or 0) != len(units):
        blockers.append("stub_input_unit_count_mismatch")
    if not str(prov.get("input_pack_id") or "").strip():
        blockers.append("stub_missing_input_pack_id")
    if prov.get("first_unit_type") != "tile":
        blockers.append("stub_first_unit_type_must_be_tile")
    if not isinstance(prov.get("unit_type_counts"), dict) or prov["unit_type_counts"].get("tile", 0) < 2:
        blockers.append("stub_unit_type_counts_invalid")

    verdict = "GO" if not blockers else "NO_GO"
    rep = {
        "schema": "ocr_tile_planner_verifier_report_v0",
        "phase": "Phase-OCR-Tile-Planner-And-Coordinate-Reconstruction-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "ocr_tile_planner_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
