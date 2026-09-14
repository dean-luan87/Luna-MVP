#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Vision recognition ingest read-only bus replay smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set

EXPECTED_EVENT_SCHEMA = "vision_recognition_ingest_readonly_event_payload_v0"
EXPECTED_EVENT_TYPE = "midplatform.vision_recognition.readonly_ingest_candidate"
EXPECTED_STAGES: Set[str] = {
    "event_payload_created",
    "event_replayed",
    "readonly_consumer_received",
    "readonly_consumer_view_generated",
    "no_write_action_confirmed",
}
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

    pay_p = root / "vision_recognition_ingest_readonly_event_payload.json"
    log_p = root / "vision_recognition_ingest_readonly_replay_log.jsonl"
    view_p = root / "vision_recognition_ingest_readonly_replay_consumer_view.json"
    aud_p = root / "vision_recognition_ingest_readonly_replay_audit_report.json"

    for label, p in (
        ("event_payload", pay_p),
        ("replay_log", log_p),
        ("replay_consumer_view", view_p),
        ("replay_audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"

    if not blockers:
        pay: Dict[str, Any] = _read_json(pay_p)
        view: Dict[str, Any] = _read_json(view_p)
        aud: Dict[str, Any] = _read_json(aud_p)

        if str(pay.get("schema_version") or "") != EXPECTED_EVENT_SCHEMA:
            blockers.append("event_payload_schema_mismatch")
        if str(pay.get("event_type") or "") != EXPECTED_EVENT_TYPE:
            blockers.append("event_type_mismatch")

        if not str(pay.get("candidate_id") or "").strip():
            blockers.append("candidate_id_missing")
        if not str(pay.get("source_candidate_ref") or "").strip():
            blockers.append("source_candidate_ref_missing")

        if str(pay.get("payload_scope") or "") != "read_only_replay":
            blockers.append("payload_scope_not_read_only_replay")

        n = int(pay.get("evidence_count") or 0)
        if n <= 0:
            blockers.append("evidence_count_not_positive")

        if str(pay.get("provider") or "") != "vision_stub":
            blockers.append("provider_not_vision_stub")
        if str(pay.get("provider_level") or "") != "stub":
            blockers.append("provider_level_not_stub")

        fs = pay.get("fact_status_summary") or {}
        if int(fs.get("not_fact") or 0) != n:
            blockers.append("fact_status_summary_mismatch")

        syn = pay.get("synthetic_summary") or {}
        if int(syn.get("synthetic_count") or 0) != n:
            blockers.append("synthetic_count_mismatch")
        if int(syn.get("stub_provider_count") or 0) != n:
            blockers.append("stub_provider_count_mismatch")

        if not isinstance(pay.get("evidence_by_frame"), dict) or not pay.get("evidence_by_frame"):
            blockers.append("evidence_by_frame_missing")
        if not isinstance(pay.get("evidence_by_roi_type"), dict) or not pay.get("evidence_by_roi_type"):
            blockers.append("evidence_by_roi_type_missing")
        if not isinstance(pay.get("geometry_summary"), dict) or not pay.get("geometry_summary"):
            blockers.append("geometry_summary_missing")

        fa = pay.get("forbidden_actions") or {}
        if not isinstance(fa, dict):
            blockers.append("forbidden_actions_not_object")
        else:
            for k in FORBIDDEN_KEYS:
                if k not in fa or fa.get(k) is not True:
                    blockers.append(f"forbidden_actions_missing_or_not_true:{k}")

        stages: Set[str] = set()
        try:
            for line in log_p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                s = str(row.get("stage") or "")
                if s:
                    stages.add(s)
        except Exception:
            blockers.append("replay_log_invalid_jsonl")
        if not EXPECTED_STAGES.issubset(stages):
            blockers.append("replay_log_missing_stages")

        if str(view.get("schema_version") or "") != "vision_recognition_readonly_replay_consumer_view_v0":
            blockers.append("replay_view_schema_mismatch")

        val_errs = view.get("validation_errors")
        if not isinstance(val_errs, list) or len(val_errs) != 0:
            blockers.append("replay_consumer_validation_errors_not_empty")

        if aud.get("event_payload_created") is not True:
            blockers.append("audit_event_payload_created_not_true")
        if aud.get("replay_executed") is not True:
            blockers.append("audit_replay_executed_not_true")
        if aud.get("readonly_consumer_received") is not True:
            blockers.append("audit_readonly_consumer_received_not_true")

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
            ("database_write_invoked", False),
            ("external_bus_invoked", False),
        ):
            if aud.get(k) is not must:
                blockers.append(f"audit_flag_bad:{k}")

        scs = pay.get("source_chain_summary")
        if not isinstance(scs, dict) or not scs:
            soft.append("source_chain_summary_empty_or_weak")

    if blockers:
        verdict = "NO_GO"
    elif soft:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "vision_recognition_ingest_readonly_bus_replay_verifier_report_v0",
        "phase": "Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "vision_recognition_ingest_readonly_bus_replay_verifier_report.json", rep)
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
