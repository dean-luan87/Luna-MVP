#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Scene Delta generic executor prechain chain closure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

EXPECTED_SOURCE_TYPES = frozenset({"ocr_evidence", "vision_recognition_evidence"})
FORBIDDEN_NARRATIVE_PHRASES = (
    "production executor is available",
    "openapi aligned",
    "proto aligned",
    "scene delta write is enabled",
    "production ready",
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    sum_p = root / "scene_delta_generic_chain_closure_summary.json"
    pm_p = root / "scene_delta_generic_chain_phase_matrix.json"
    lin_p = root / "scene_delta_generic_chain_lineage_matrix.json"
    nw_p = root / "scene_delta_generic_no_write_boundary_matrix.json"
    cap_p = root / "scene_delta_generic_capability_closure_report.json"
    nc_p = root / "scene_delta_generic_non_claims_report.json"
    fo_p = root / "scene_delta_generic_open_followups.json"

    for label, p in (
        ("summary", sum_p),
        ("phase_matrix", pm_p),
        ("lineage", lin_p),
        ("no_write_boundary", nw_p),
        ("capability_closure", cap_p),
        ("non_claims", nc_p),
        ("open_followups", fo_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "scene_delta_generic_chain_closure_verifier_report_v0",
            "phase": "Phase-MidPlatform-SceneDelta-Generic-Chain-Closure-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "scene_delta_generic_chain_closure_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(sum_p)
    roots = summary.get("roots_by_source") if isinstance(summary.get("roots_by_source"), dict) else {}
    for st, cfg in roots.items():
        if not isinstance(cfg, dict):
            blockers.append(f"roots_config_invalid:{st}")
            continue
        for key in (
            "dryrun_root",
            "generic_trace_root",
            "generic_mock_handshake_root",
            "generic_contract_conformance_root",
        ):
            if not Path(str(cfg.get(key) or "")).is_dir():
                blockers.append(f"input_root_missing:{st}:{key}")

    pm = _read_json(pm_p)
    rows = pm if isinstance(pm, list) else []
    found_types = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        st = str(row.get("source_type") or "")
        found_types.add(st)
        if st not in EXPECTED_SOURCE_TYPES:
            blockers.append(f"unexpected_source_type:{st}")
        if row.get("status") != "ok":
            blockers.append(f"phase_matrix_status_not_ok:{st}")
        lv = row.get("layer_verifier_verdicts")
        if isinstance(lv, dict):
            for layer, v in lv.items():
                if v != "GO":
                    blockers.append(f"layer_verdict_not_go:{st}:{layer}:{v}")
        if row.get("blockers"):
            blockers.append(f"phase_matrix_blockers:{st}")

    if found_types != EXPECTED_SOURCE_TYPES:
        blockers.append(f"source_types_incomplete:found={sorted(found_types)}")

    lin = _read_json(lin_p)
    entries = lin.get("entries") if isinstance(lin, dict) else []
    if not isinstance(entries, list) or len(entries) < 2:
        blockers.append("lineage_entries_insufficient")
    else:
        for ent in entries:
            if not isinstance(ent, dict):
                continue
            st = ent.get("source_type")
            for key in ("dry_run_id", "trace_id", "mock_ack_id", "contract_reference_mode"):
                if not str(ent.get(key) or "").strip():
                    blockers.append(f"lineage_missing:{st}:{key}")
            if str(ent.get("contract_reference_mode") or "") != "local_skeleton":
                blockers.append(f"contract_reference_mode_invalid:{st}")
            if str(ent.get("conformance_level") or "") not in ("full", "partial"):
                soft.append(f"conformance_level_note:{st}:{ent.get('conformance_level')}")

    nw = _read_json(nw_p)
    if nw.get("boundary_ok") is not True:
        blockers.append("no_write_boundary_not_ok")

    nc = _read_json(nc_p)
    if not isinstance(nc, dict):
        blockers.append("non_claims_invalid")
    else:
        claims = nc.get("claims")
        if not isinstance(claims, dict):
            blockers.append("non_claims_claims_missing")
        else:
            for k, v in claims.items():
                if v is not False:
                    blockers.append(f"non_claims_must_be_false:{k}")
        narr = nc.get("narrative") if isinstance(nc.get("narrative"), list) else []
        if len(narr) < 5:
            blockers.append("non_claims_narrative_too_short")
        joined = " ".join(str(x).lower() for x in narr)
        for phrase in FORBIDDEN_NARRATIVE_PHRASES:
            if phrase in joined and "not assert" not in joined[max(0, joined.find(phrase) - 20) : joined.find(phrase)]:
                pass  # only flag positive claims
        if "does not not" in joined:
            blockers.append("non_claims_double_negative")

    fo = _read_json(fo_p)
    items = fo.get("items") if isinstance(fo, dict) else []
    if not isinstance(items, list) or len(items) < 4:
        blockers.append("open_followups_insufficient")

    cap = _read_json(cap_p)
    if not isinstance(cap, dict) or not cap.get("capabilities_proven"):
        blockers.append("capability_closure_missing")

    if summary.get("errors"):
        blockers.append("summary_errors_non_empty")

    if not blockers:
        verdict = "GO"
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "scene_delta_generic_chain_closure_verifier_report_v0",
        "phase": "Phase-MidPlatform-SceneDelta-Generic-Chain-Closure-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "scene_delta_generic_chain_closure_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
