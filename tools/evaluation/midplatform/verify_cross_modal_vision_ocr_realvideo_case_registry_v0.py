#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RealVideo Case Registry v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


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
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "cross_modal_vision_ocr_realvideo_case_registry_summary.json",
        "registry": root / "cross_modal_vision_ocr_realvideo_case_registry.json",
        "taxonomy": root / "cross_modal_vision_ocr_realvideo_case_taxonomy.json",
        "sampling": root / "cross_modal_vision_ocr_realvideo_sampling_policy_stub.json",
        "behavior": root / "cross_modal_vision_ocr_realvideo_expected_behavior_matrix.json",
        "binding": root / "cross_modal_vision_ocr_realvideo_metrics_binding_matrix.json",
        "gov": root / "cross_modal_vision_ocr_realvideo_governance_link_report.json",
        "non_goals": root / "cross_modal_vision_ocr_realvideo_non_goals_report.json",
        "risks": root / "cross_modal_vision_ocr_realvideo_risk_register.json",
        "audit": root / "cross_modal_vision_ocr_realvideo_case_registry_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "cross_modal_vision_ocr_realvideo_case_registry_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    registry = _read_json(paths["registry"])
    sampling = _read_json(paths["sampling"])
    behavior = _read_json(paths["behavior"])
    binding = _read_json(paths["binding"])
    gov = _read_json(paths["gov"])
    risks_doc = _read_json(paths["risks"])
    aud = _read_json(paths["audit"])

    if summary.get("registry_scope") != "case_registry_only":
        blockers.append("registry_scope")
    for flag in ("real_video_loaded", "frame_sampled", "ocr_invoked", "vision_provider_invoked"):
        if summary.get(flag) is not False:
            blockers.append(flag)

    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    if len(cases) < 15:
        blockers.append("case_count")

    ids = {c.get("case_id") for c in cases if isinstance(c, dict)}
    if not any("POSTER" in (i or "") for i in ids):
        blockers.append("poster_cases")
    if not any("FACILITY" in (i or "") for i in ids):
        blockers.append("facility_cases")
    if "RV_DUPLICATE_TEXT_ACROSS_FRAMES" not in ids or "RV_CONFLICTING_TEXT_ACROSS_REGIONS" not in ids:
        blockers.append("duplicate_conflict_cases")

    if sampling.get("sample_mode") != "registry_only_no_sampling":
        blockers.append("sample_mode")

    brows = behavior.get("rows") if isinstance(behavior.get("rows"), list) else []
    for row in brows:
        if isinstance(row, dict):
            if row.get("should_write_fact") is not False:
                blockers.append("should_write_fact")
                break
            if row.get("should_invoke_navigation") is not False:
                blockers.append("should_invoke_navigation")
                break

    bind_rows = binding.get("rows") if isinstance(binding.get("rows"), list) else []
    if not bind_rows:
        blockers.append("metrics_binding_empty")
    else:
        has_boundary = any(
            isinstance(r, dict) and "no_write_boundary_pass_rate" in (r.get("bound_metrics") or [])
            for r in bind_rows
        )
        if not has_boundary:
            blockers.append("no_write_boundary_binding")

    if gov.get("poster_governance_linked") is not True:
        blockers.append("poster_governance_linked")
    if gov.get("public_facility_governance_linked") is not True:
        blockers.append("public_facility_governance_linked")
    if gov.get("metrics_schema_linked") is not True:
        blockers.append("metrics_schema_linked")

    risk_ids = {r.get("risk_id") for r in (risks_doc.get("risks") or []) if isinstance(r, dict)}
    for req in ("motion_blur", "poster_layout_complexity", "public_facility_symbol_text_mismatch"):
        if req not in risk_ids:
            blockers.append(f"risk_{req}")

    for key in (
        "midplatform_fact_written",
        "scene_delta_written",
        "world_model_written",
        "navigation_decision_invoked",
        "auto_approve_invoked",
    ):
        if aud.get(key) is not False:
            blockers.append(f"audit_{key}")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "cross_modal_vision_ocr_realvideo_case_registry_verifier_report.json",
        {
            "schema": "cross_modal_vision_ocr_realvideo_case_registry_verifier_report_v0",
            "phase": "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        },
    )
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
