#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR TestBoard expansion."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_EXECUTED_CASES = (
    "CM_VOCR_001_POSITIVE_TEXT_CLEAR",
    "CM_VOCR_002_EMPTY_TEXT_ROI",
    "CM_VOCR_006_MULTI_TEXT_LINES",
)


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return here.parents[3]


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
    soft: List[str] = []

    paths = {
        "summary": root / "cross_modal_vision_ocr_testboard_summary.json",
        "registry": root / "cross_modal_vision_ocr_testboard_registry.json",
        "fixture": root / "cross_modal_vision_ocr_testboard_fixture_manifest.json",
        "expected": root / "cross_modal_vision_ocr_testboard_expected_behavior_matrix.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_boundary_matrix.json",
        "execution": root / "cross_modal_vision_ocr_testboard_case_execution_matrix.json",
        "audit": root / "cross_modal_vision_ocr_testboard_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Expansion-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    registry = _read_json(paths["registry"])
    fixture = _read_json(paths["fixture"])
    expected = _read_json(paths["expected"])
    boundary = _read_json(paths["boundary"])
    execution = _read_json(paths["execution"])
    aud = _read_json(paths["audit"])

    case_count = int(registry.get("case_count") or 0)
    if case_count < 10:
        blockers.append("case_count_below_10")

    executed_count = int(summary.get("executed_case_count") or 0)
    planned_count = int(summary.get("planned_case_count") or 0)
    if executed_count < 3:
        soft.append("executed_case_count_below_3")
    if planned_count < 7:
        soft.append("planned_case_count_below_7")

    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    case_ids = {c.get("case_id") for c in cases if isinstance(c, dict)}
    for req in REQUIRED_EXECUTED_CASES:
        if req not in case_ids:
            blockers.append(f"missing_case:{req}")

    for c in cases:
        if not isinstance(c, dict):
            continue
        efs = c.get("expected_final_status") if isinstance(c.get("expected_final_status"), dict) else {}
        if efs.get("fact_status") != "not_fact":
            blockers.append(f"case_fact_status_not_not_fact:{c.get('case_id')}")
        if efs.get("write_status") != "no_write":
            blockers.append(f"case_write_status_not_no_write:{c.get('case_id')}")

    exec_rows = execution.get("rows") if isinstance(execution.get("rows"), list) else []
    exec_by_id = {r.get("case_id"): r for r in exec_rows if isinstance(r, dict)}

    for cid in REQUIRED_EXECUTED_CASES:
        row = exec_by_id.get(cid)
        if not row:
            blockers.append(f"execution_row_missing:{cid}")
            continue
        if row.get("case_execution_status") != "executed":
            blockers.append(f"required_case_not_executed:{cid}")
        if row.get("case_execution_status") == "planned_only":
            blockers.append(f"planned_only_disguised_as_executed:{cid}")

    for row in exec_rows:
        if not isinstance(row, dict):
            continue
        if row.get("execution_mode") == "planned_only" and row.get("case_execution_status") == "executed":
            blockers.append(f"planned_only_marked_executed:{row.get('case_id')}")

    if boundary.get("boundary_all_ok") is not True:
        blockers.append("boundary_all_ok_not_true")

    if summary.get("write_path_invoked") is True:
        blockers.append("write_path_invoked_true")

    if aud.get("real_scene_delta_executor_invoked") is not False:
        blockers.append("audit:real_scene_delta_executor_invoked")
    if aud.get("midplatform_fact_written") is not False:
        blockers.append("audit:midplatform_fact_written")
    if aud.get("auto_approve_invoked") is not False:
        blockers.append("audit:auto_approve_invoked")

    if aud.get("cross_modal_vision_ocr_testboard_expansion_executed") is not True:
        blockers.append("audit:expansion_not_executed")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif soft:
        verdict = "CONDITIONAL_GO"

    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_testboard_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Expansion-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "case_count": case_count,
        "executed_case_count": executed_count,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
