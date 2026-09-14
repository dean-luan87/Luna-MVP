#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for YOLO evidence pack read-only consumer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List

FORBIDDEN_KEYS = {"confirmed_object", "confirmed_fact", "navigation_action"}


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


def _scan_forbidden(obj: Any, path: str = "$") -> List[str]:
    hits: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if str(k) in FORBIDDEN_KEYS:
                hits.append(f"{path}.{k}")
            hits.extend(_scan_forbidden(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits.extend(_scan_forbidden(v, f"{path}[{i}]"))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yolo-evidence-pack-root", required=True)
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    pack_root = _require_abs(args.yolo_evidence_pack_root, "--yolo-evidence-pack-root")
    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    if not (pack_root / "yolo_vision_recognition_evidence_pack.json").is_file():
        blockers.append("missing_input_yolo_evidence_pack")

    view_p = root / "yolo_evidence_readonly_consumer_view.json"
    aud_p = root / "yolo_evidence_readonly_consumer_audit_report.json"
    geom_p = root / "yolo_evidence_geometry_summary.json"

    for label, p in (("consumer_view", view_p), ("audit", aud_p), ("geometry_summary", geom_p)):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "yolo_evidence_readonly_consumer_verifier_report_v0",
            "phase": "Phase-Vision-YOLO-Evidence-Pack-ReadOnly-Consumer-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "yolo_evidence_readonly_consumer_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    view = _read_json(view_p)
    aud = _read_json(aud_p)
    geom = _read_json(geom_p)

    if view.get("schema_version") != "vision_recognition_evidence_readonly_consumer_view_v0":
        blockers.append("consumer_view_schema_mismatch")

    n = int(view.get("evidence_count_observed") or 0)
    if n <= 0:
        blockers.append("evidence_count_not_positive")

    if str(view.get("provider") or "") != "yolo_candidate_adapter":
        blockers.append("provider_must_be_yolo_candidate_adapter")
    if str(view.get("provider_level") or "") != "evaluation_candidate":
        blockers.append("provider_level_must_be_evaluation_candidate")

    fs = view.get("fact_status_summary") or {}
    if int(fs.get("not_fact") or 0) != n:
        blockers.append("fact_status_summary_not_fact_mismatch")

    syn = view.get("synthetic_summary") or {}
    if int(syn.get("synthetic_count") or 0) != 0:
        blockers.append("synthetic_count_must_be_zero")
    if int(syn.get("stub_provider_count") or 0) != 0:
        blockers.append("stub_provider_count_must_be_zero")

    rd = view.get("real_detector_summary") or {}
    if int(rd.get("real_detector_count") or 0) != n:
        blockers.append("real_detector_count_mismatch")
    if str(rd.get("detector_mode") or "") != "real_yolo":
        blockers.append("detector_mode_must_be_real_yolo")

    if not isinstance(view.get("label_summary"), dict) or not view.get("label_summary"):
        blockers.append("label_summary_required")

    vgeom = view.get("geometry_summary") or {}
    if int(vgeom.get("bbox_in_frame_count") or 0) <= 0:
        blockers.append("geometry_summary_bbox_count_not_positive")
    if int(geom.get("bbox_in_frame_count") or 0) <= 0:
        blockers.append("geometry_file_bbox_count_not_positive")

    forbidden = _scan_forbidden(view)
    if forbidden:
        blockers.extend([f"forbidden_key:{h}" for h in forbidden])

    for k, must in (
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("vision_mainline_modified", False),
        ("vision_provider_registry_default_changed", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit:{k}")

    if aud.get("yolo_evidence_readonly_consumer_executed") is not True:
        blockers.append("yolo_evidence_readonly_consumer_executed_must_be_true")
    if aud.get("evaluation_only") is not True:
        blockers.append("evaluation_only_must_be_true")
    if aud.get("real_detector_invoked_upstream") is not True:
        blockers.append("real_detector_invoked_upstream_must_be_true")
    if aud.get("yolo_invoked_upstream") is not True:
        blockers.append("yolo_invoked_upstream_must_be_true")

    if not blockers:
        verdict = "GO" if not soft else "CONDITIONAL_GO"
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "yolo_evidence_readonly_consumer_verifier_report_v0",
        "phase": "Phase-Vision-YOLO-Evidence-Pack-ReadOnly-Consumer-001",
        "yolo_evidence_pack_root": str(pack_root),
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "yolo_evidence_readonly_consumer_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
