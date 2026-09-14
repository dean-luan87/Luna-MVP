#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR → Scene Delta mock chain closure smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

EXPECTED_CONTRACT_MODE = "local_skeleton"


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

    sum_p = root / "ocr_to_scene_delta_chain_closure_summary.json"
    pm_p = root / "ocr_to_scene_delta_phase_matrix.json"
    lin_p = root / "ocr_to_scene_delta_lineage_matrix.json"
    nw_p = root / "ocr_to_scene_delta_no_write_boundary_matrix.json"
    cap_p = root / "ocr_to_scene_delta_capability_closure_report.json"
    nc_p = root / "ocr_to_scene_delta_non_claims_report.json"
    fo_p = root / "ocr_to_scene_delta_open_followups.json"

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
    narr: List[Any] = []

    if blockers:
        rep = {
            "schema": "ocr_to_scene_delta_chain_closure_verifier_report_v0",
            "phase": "Phase-OCR-to-SceneDelta-Mock-Chain-Closure-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": soft,
        }
        _write_json(root / "ocr_to_scene_delta_chain_closure_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(sum_p)
    roots = summary.get("roots") if isinstance(summary.get("roots"), dict) else {}
    for pid, rpath in roots.items():
        p = Path(str(rpath))
        if not p.is_dir():
            blockers.append(f"input_root_missing:{pid}")

    pm = _read_json(pm_p)
    rows = pm if isinstance(pm, list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        pid = row.get("phase_id")
        if row.get("verifier_verdict") != "GO":
            blockers.append(f"phase_not_go:{pid}:{row.get('verifier_verdict')}")
        if row.get("blockers"):
            blockers.append(f"phase_blockers_non_empty:{pid}")

    lin = _read_json(lin_p)
    if not isinstance(lin, dict):
        blockers.append("lineage_invalid")
    else:
        for key in ("ocr_text_joined", "contract_reference_mode", "trace_id", "mock_request_id", "mock_ack_id"):
            if not str(lin.get(key) or "").strip():
                blockers.append(f"lineage_missing:{key}")

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

    fo = _read_json(fo_p)
    items = fo.get("items") if isinstance(fo.get("items"), list) else []
    if len(items) < 6:
        blockers.append("open_followups_too_short")

    if isinstance(lin, dict) and str(lin.get("contract_reference_mode") or "") != EXPECTED_CONTRACT_MODE:
        blockers.append("contract_reference_mode_must_be_local_skeleton")

    narr_text = " ".join(str(x) for x in narr)
    if "NOT assert" not in narr_text and "does NOT" not in narr_text:
        blockers.append("non_claims_narrative_missing_disclaimer_phrase")

    if not blockers:
        verdict = "GO"
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "ocr_to_scene_delta_chain_closure_verifier_report_v0",
        "phase": "Phase-OCR-to-SceneDelta-Mock-Chain-Closure-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "ocr_to_scene_delta_chain_closure_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
