#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Public Facility Semantic Correction Governance v0."""

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
        "summary": root / "public_facility_semantic_correction_governance_summary.json",
        "routing": root / "public_facility_evidence_routing_policy.json",
        "levels": root / "public_facility_correction_levels.json",
        "example": root / "public_facility_semantic_candidate_example.json",
        "gate": root / "public_facility_gate_policy_report.json",
        "audit": root / "public_facility_governance_audit_report.json",
    }
    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "public_facility_governance_verifier_report.json",
            {
                "schema": "public_facility_governance_verifier_report_v0",
                "phase": "PublicFacility-Semantic-Correction-Governance-001",
                "verdict": "NO_GO",
                "blockers": blockers,
            },
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    routing = _read_json(paths["routing"])
    levels = _read_json(paths["levels"])
    example = _read_json(paths["example"])
    gate = _read_json(paths["gate"])
    aud = _read_json(paths["audit"])

    if summary.get("default_ocr_mainline_allowed") is not False:
        blockers.append("default_ocr_mainline")
    if summary.get("semantic_first_required") is not True:
        blockers.append("semantic_first")

    primary = routing.get("primary_evidence_types") if isinstance(routing.get("primary_evidence_types"), list) else []
    if "PublicFacilityEvidence" not in primary or "FacilitySemanticCandidate" not in primary:
        blockers.append("primary_evidence_types")
    if routing.get("default_ocr_mainline_allowed") is not False:
        blockers.append("routing_ocr_default")
    if routing.get("ocr_role") != "auxiliary_only":
        blockers.append("ocr_not_auxiliary")

    lvl = levels.get("levels") if isinstance(levels.get("levels"), list) else []
    if len(lvl) < 3:
        blockers.append("correction_levels")
    arb = levels.get("midplatform_arbitration") if isinstance(levels.get("midplatform_arbitration"), dict) else {}
    if arb.get("fact_status_default") != "not_fact":
        blockers.append("arbitration_not_fact")

    if example.get("raw_ocr_text_preserved") is not True:
        blockers.append("raw_ocr_not_preserved")
    if example.get("fact_status") != "not_fact":
        blockers.append("example_fact_status")
    if example.get("facility_semantic_candidate") != "restroom":
        blockers.append("example_semantic")

    if gate.get("ocr_text_evidence_primary_allowed") is not False:
        blockers.append("gate_ocr_primary")
    if gate.get("raw_ocr_text_must_be_preserved") is not True:
        blockers.append("gate_preserve_raw")
    if gate.get("navigation_output_requires_gate") is not True:
        blockers.append("gate_navigation")

    for key, expected in (
        ("ocr_invoked", False),
        ("vision_provider_invoked", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
    ):
        if aud.get(key) != expected:
            blockers.append(f"audit_{key}")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "public_facility_governance_verifier_report.json",
        {
            "schema": "public_facility_governance_verifier_report_v0",
            "phase": "PublicFacility-Semantic-Correction-Governance-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        },
    )
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
