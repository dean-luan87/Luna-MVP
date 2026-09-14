#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Scene Delta write candidate from OCR ingest stub smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

EXPECTED_SCHEMA = "scene_delta_write_candidate_from_ocr_v0"
FORBIDDEN_KEYS = frozenset(
    {
        "semantic_summary",
        "inferred_meaning",
        "object_meaning",
        "business_meaning",
        "environment_interpretation",
        "user_facing_explanation",
    }
)
FORBIDDEN_ACTION_KEYS = (
    "write_scene_delta",
    "write_midplatform_fact",
    "write_world_model",
    "invoke_ai_interpretation",
)


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


def _forbidden_key_hits(obj: Any, path: str = "$") -> List[str]:
    hits: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            ks = str(k)
            if ks in FORBIDDEN_KEYS:
                hits.append(f"{path}.{ks}")
            hits.extend(_forbidden_key_hits(v, path=f"{path}.{ks}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits.extend(_forbidden_key_hits(v, path=f"{path}[{i}]"))
    return hits


def _has_original_geometry(it: Dict[str, Any]) -> bool:
    ob = it.get("original_bbox")
    if isinstance(ob, list) and len(ob) == 4:
        return True
    op = it.get("original_polygon")
    return isinstance(op, list) and len(op) > 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    cand_p = root / "scene_delta_write_candidate_from_ocr.json"
    gate_p = root / "scene_delta_write_candidate_gate_stub.json"
    aud_p = root / "scene_delta_write_candidate_audit_report.json"
    mat_p = root / "scene_delta_write_candidate_evidence_matrix.json"

    for label, p in (
        ("write_candidate", cand_p),
        ("gate_stub", gate_p),
        ("audit", aud_p),
        ("evidence_matrix", mat_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "scene_delta_write_candidate_from_ocr_verifier_report_v0",
            "phase": "Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        }
        _write_json(root / "scene_delta_write_candidate_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    cand: Dict[str, Any] = _read_json(cand_p)
    gate: Dict[str, Any] = _read_json(gate_p)
    aud: Dict[str, Any] = _read_json(aud_p)

    if str(cand.get("schema_version") or "") != EXPECTED_SCHEMA:
        blockers.append("schema_version_mismatch")
    if str(cand.get("candidate_scope") or "") != "write_candidate_only":
        blockers.append("candidate_scope_must_be_write_candidate_only")
    if cand.get("write_allowed") is not False:
        blockers.append("write_allowed_must_be_false")
    if cand.get("requires_gate_approval") is not True:
        blockers.append("requires_gate_approval_must_be_true")
    if int(cand.get("evidence_count") or 0) < 1:
        blockers.append("evidence_count_ge_1")

    items = cand.get("evidence_items")
    if not isinstance(items, list) or not items:
        blockers.append("evidence_items_must_exist")
    else:
        for i, it in enumerate(items):
            if not isinstance(it, dict):
                blockers.append(f"evidence_item_not_dict_{i}")
                continue
            if not str(it.get("text") or "").strip():
                blockers.append(f"evidence_missing_text_{i}")
            if not str(it.get("roi_id") or "").strip() and not str(it.get("unit_id") or "").strip():
                blockers.append(f"evidence_missing_roi_or_unit_{i}")
            if not _has_original_geometry(it):
                blockers.append(f"evidence_missing_original_geometry_{i}")
            if str(it.get("fact_status") or "") != "not_fact":
                blockers.append(f"fact_status_must_be_not_fact_{i}")
            if str(it.get("evidence_role") or "") != "observed_text":
                blockers.append(f"evidence_role_must_be_observed_text_{i}")

    fa = cand.get("forbidden_actions")
    if not isinstance(fa, dict):
        blockers.append("forbidden_actions_must_be_object")
    else:
        for k in FORBIDDEN_ACTION_KEYS:
            if k not in fa or fa.get(k) is not True:
                blockers.append(f"forbidden_actions_missing_or_not_true:{k}")

    hits = _forbidden_key_hits(cand)
    if hits:
        blockers.append(f"forbidden_interpretation_keys_present:{hits[0]}")

    if gate.get("gate_required") is not True:
        blockers.append("gate_required_must_be_true")
    if str(gate.get("gate_status") or "") != "not_evaluated":
        blockers.append("gate_status_must_be_not_evaluated")
    grc = gate.get("gate_reason_codes")
    if not isinstance(grc, list) or len(grc) < 1:
        blockers.append("gate_reason_codes_must_be_non_empty")
    else:
        need = {
            "ocr_evidence_requires_scene_delta_gate",
            "no_ai_interpretation",
            "no_world_fact_write",
        }
        have = {str(x) for x in grc}
        if not need.issubset(have):
            blockers.append("gate_reason_codes_incomplete")

    for k, must in (
        ("scene_delta_written", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("database_write_invoked", False),
        ("ocr_provider_invoked", False),
        ("ocr_routing_changed", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit_false_gate:{k}")

    if aud.get("external_bus_invoked") is not False:
        blockers.append("audit_external_bus_invoked_must_be_false")

    if aud.get("scene_delta_write_candidate_generated") is not True:
        blockers.append("audit_scene_delta_write_candidate_generated_must_be_true")

    soft: List[str] = []
    items = cand.get("evidence_items")
    if not blockers:
        verdict = "GO"
        scs = cand.get("source_chain_summary")
        if isinstance(scs, dict) and int(scs.get("chain_item_count") or 0) == 0 and not scs.get("chain"):
            verdict = "CONDITIONAL_GO"
            soft.append("source_chain_summary_empty")
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "scene_delta_write_candidate_from_ocr_verifier_report_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "write_candidate_path": str(cand_p.resolve()),
    }
    _write_json(root / "scene_delta_write_candidate_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
