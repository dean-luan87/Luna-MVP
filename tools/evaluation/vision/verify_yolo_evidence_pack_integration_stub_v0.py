#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for YOLO evidence pack integration stub."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List

PACK_SCHEMA = "vision_recognition_evidence_pack_v0"
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
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    pack_p = root / "yolo_vision_recognition_evidence_pack.json"
    consumer_p = root / "yolo_evidence_consumer_compatibility_report.json"
    risk_p = root / "yolo_evidence_pack_risk_report.json"
    aud_p = root / "yolo_evidence_pack_audit_report.json"

    for label, p in (
        ("evidence_pack", pack_p),
        ("consumer_compatibility", consumer_p),
        ("risk_report", risk_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "yolo_evidence_pack_verifier_report_v0",
            "phase": "Phase-Vision-YOLO-Evidence-Pack-Integration-Stub-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "yolo_evidence_pack_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    pack = _read_json(pack_p)
    consumer = _read_json(consumer_p)
    risk = _read_json(risk_p)
    aud = _read_json(aud_p)

    if str(pack.get("schema_version") or "") != PACK_SCHEMA:
        blockers.append("pack_schema_version_mismatch")

    pt = pack.get("provider_trace") if isinstance(pack.get("provider_trace"), dict) else {}
    if str(pt.get("provider") or "") != "yolo_candidate_adapter":
        blockers.append("provider_trace_provider_mismatch")
    if str(pt.get("detector_mode") or "") != "real_yolo":
        blockers.append("provider_trace_detector_mode_must_be_real_yolo")
    if pt.get("real_provider_invoked") is not True:
        blockers.append("real_provider_invoked_must_be_true")
    if pt.get("fixture_used") is not False:
        blockers.append("fixture_used_must_be_false")

    items = pack.get("items") if isinstance(pack.get("items"), list) else []
    if len(items) <= 0:
        blockers.append("items_count_must_be_positive")

    for it in items:
        if not isinstance(it, dict):
            blockers.append("invalid_item")
            continue
        if str(it.get("fact_status") or "") != "not_fact":
            blockers.append("item_fact_status_must_be_not_fact")
        if it.get("synthetic") is not False:
            blockers.append("item_synthetic_must_be_false")
        if it.get("stub_provider") is not False:
            blockers.append("item_stub_provider_must_be_false")
        if not isinstance(it.get("bbox_in_frame"), list) or len(it.get("bbox_in_frame") or []) != 4:
            blockers.append("item_bbox_in_frame_required")
        label = str(it.get("label") or "")
        if label in ("confirmed_object", "confirmed_fact"):
            blockers.append("item_label_must_not_be_confirmed")

    forbidden = _scan_forbidden(pack)
    if forbidden:
        blockers.extend([f"forbidden_key:{h}" for h in forbidden])

    if consumer.get("consumer_compatible") is not True:
        soft.append("consumer_compatibility_not_fully_true")
        for g in consumer.get("gaps") or []:
            if not str(g).startswith("item_source_chain_optional"):
                blockers.append(f"consumer_gap:{g}")

    if risk.get("yolo_label_not_fact") is not True:
        blockers.append("risk_yolo_label_not_fact_required")
    if risk.get("no_navigation_decision") is not True and risk.get("detection_not_navigation_decision") is not True:
        blockers.append("risk_no_navigation_decision_required")

    for k, must in (
        ("vision_mainline_modified", False),
        ("vision_provider_registry_default_changed", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("supervision_mainline_invoked", False),
        ("vlm_invoked", False),
        ("ocr_invoked", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit:{k}")

    if aud.get("yolo_evidence_pack_integration_executed") is not True:
        blockers.append("yolo_evidence_pack_integration_executed_must_be_true")
    if aud.get("real_detector_invoked") is not True:
        blockers.append("audit_real_detector_invoked_must_be_true")
    if aud.get("yolo_invoked") is not True:
        blockers.append("audit_yolo_invoked_must_be_true")
    if aud.get("fixture_used") is not False:
        blockers.append("audit_fixture_used_must_be_false")

    if not blockers:
        verdict = "GO" if not soft else "CONDITIONAL_GO"
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "yolo_evidence_pack_verifier_report_v0",
        "phase": "Phase-Vision-YOLO-Evidence-Pack-Integration-Stub-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "yolo_evidence_pack_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
