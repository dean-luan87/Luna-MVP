#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Scene Delta write candidate from Vision ingest stub."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

EXPECTED_SCHEMA = "scene_delta_write_candidate_from_vision_v0"
FORBIDDEN_ACTION_KEYS = (
    "write_scene_delta",
    "write_midplatform_fact",
    "write_world_model",
    "invoke_ai_interpretation",
    "invoke_navigation_decision",
    "invoke_real_vision_provider",
)
FORBIDDEN_STRINGS_IN_ITEMS = ("confirmed_fact", "confirmed_object")


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _item_has_forbidden_confirmed(it: Dict[str, Any]) -> bool:
    for k, v in it.items():
        ks = str(k).lower()
        if ks in FORBIDDEN_STRINGS_IN_ITEMS:
            return True
        if isinstance(v, str) and v.lower() in FORBIDDEN_STRINGS_IN_ITEMS:
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    cand_p = root / "scene_delta_write_candidate_from_vision.json"
    gate_p = root / "scene_delta_write_candidate_vision_gate_stub.json"
    mx_p = root / "scene_delta_write_candidate_vision_evidence_matrix.json"
    aud_p = root / "scene_delta_write_candidate_vision_audit_report.json"

    for label, p in (
        ("write_candidate", cand_p),
        ("gate_stub", gate_p),
        ("evidence_matrix", mx_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"

    if not blockers:
        cand: Dict[str, Any] = _read_json(cand_p)
        gate: Dict[str, Any] = _read_json(gate_p)
        mx = _read_json(mx_p)
        aud: Dict[str, Any] = _read_json(aud_p)

        if str(cand.get("schema_version") or "") != EXPECTED_SCHEMA:
            blockers.append("schema_version_mismatch")

        if str(cand.get("candidate_scope") or "") != "write_candidate_only":
            blockers.append("candidate_scope_mismatch")

        if cand.get("write_allowed") is not False:
            blockers.append("write_allowed_must_be_false")

        if cand.get("requires_gate_approval") is not True:
            blockers.append("requires_gate_approval_must_be_true")

        n = int(cand.get("evidence_count") or 0)
        if n <= 0:
            blockers.append("evidence_count_not_positive")

        if str(cand.get("provider") or "") != "vision_stub":
            blockers.append("provider_not_vision_stub")
        if str(cand.get("provider_level") or "") != "stub":
            blockers.append("provider_level_not_stub")

        fs = cand.get("fact_status_summary") or {}
        if int(fs.get("not_fact") or 0) != n:
            blockers.append("fact_status_summary_mismatch")

        syn = cand.get("synthetic_summary") or {}
        if int(syn.get("synthetic_count") or 0) != n:
            blockers.append("synthetic_count_mismatch")
        if int(syn.get("stub_provider_count") or 0) != n:
            blockers.append("stub_provider_count_mismatch")

        items = cand.get("evidence_items")
        if not isinstance(items, list) or len(items) == 0:
            blockers.append("evidence_items_missing")
        else:
            for i, it in enumerate(items):
                if not isinstance(it, dict):
                    blockers.append(f"evidence_item_not_object_{i}")
                    continue
                if not str(it.get("source_frame_id") or "").strip():
                    blockers.append(f"missing_source_frame_id_{i}")
                rid = str(it.get("roi_id") or "").strip()
                uid = str(it.get("unit_id") or "").strip()
                if not rid and not uid:
                    blockers.append(f"missing_roi_and_unit_{i}")
                if it.get("synthetic") is not True:
                    blockers.append(f"synthetic_not_true_{i}")
                if it.get("stub_provider") is not True:
                    blockers.append(f"stub_provider_not_true_{i}")
                if str(it.get("fact_status") or "") != "not_fact":
                    blockers.append(f"fact_status_not_not_fact_{i}")
                if _item_has_forbidden_confirmed(it):
                    blockers.append(f"forbidden_confirmed_marker_{i}")

        scs = cand.get("source_chain_summary")
        if not isinstance(scs, dict) or not scs:
            soft.append("source_chain_summary_weak")

        fa = cand.get("forbidden_actions") or {}
        if not isinstance(fa, dict):
            blockers.append("forbidden_actions_not_object")
        else:
            for k in FORBIDDEN_ACTION_KEYS:
                if k not in fa or fa.get(k) is not True:
                    blockers.append(f"forbidden_actions_bad:{k}")

        if gate.get("gate_status") != "not_evaluated":
            blockers.append("gate_status_must_be_not_evaluated")

        if gate.get("gate_required") is not True:
            blockers.append("gate_required_must_be_true")

        if aud.get("scene_delta_write_candidate_generated") is not True:
            blockers.append("audit_candidate_generated_not_true")
        for k, must in (
            ("scene_delta_written", False),
            ("midplatform_fact_written", False),
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

        rows = mx.get("rows") if isinstance(mx.get("rows"), list) else []
        if len(rows) != n:
            soft.append("matrix_row_count_mismatch")

    if blockers:
        verdict = "NO_GO"
    elif soft:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "scene_delta_write_candidate_from_vision_verifier_report_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "scene_delta_write_candidate_from_vision_verifier_report.json", rep)
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
