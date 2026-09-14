#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Poster-OCR-ReferenceOnly-001 verifier."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference-only-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.reference_only_root).expanduser().resolve()
    if args.verifier_output_root.strip():
        vout = Path(args.verifier_output_root).expanduser().resolve()
    else:
        vout = (root.parent / "cross_modal_poster_ocr_reference_only_verify_v0").resolve()
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("cross_modal_poster_ocr_reference_only_summary.json")
    cand_p = req("cross_modal_poster_reference_candidate.json")
    text_p = req("cross_modal_poster_text_plan_reference_matrix.json")
    vis_p = req("cross_modal_poster_visual_symbol_reference_matrix.json")
    align_p = req("cross_modal_poster_cross_track_alignment_matrix.json")
    risk_p = req("cross_modal_poster_reference_risk_report.json")
    gate_p = req("cross_modal_poster_reference_gate_policy.json")
    met_p = req("cross_modal_poster_reference_metrics_binding_report.json")
    chain_p = req("cross_modal_poster_reference_source_chain_summary.json")
    sim_p = req("cross_modal_poster_reference_simulation_context_report.json")
    audit_p = req("cross_modal_poster_reference_only_audit_report.json")

    if not blockers:
        sm = _read_json(sum_p)
        if sm.get("reference_scope") != "reference_only":
            blockers.append("summary_reference_scope_not_reference_only")
        if sm.get("text_plan_reference_count") != 4:
            blockers.append("text_plan_reference_count_not_4")
        if sm.get("visual_symbol_reference_count") != 4:
            blockers.append("visual_symbol_reference_count_not_4")
        if sm.get("simulation_context_attached") is not True:
            blockers.append("simulation_context_attached_not_true")
        for k in ("fusion_invoked", "ocr_invoked", "qr_decoded", "brand_identity_confirmed"):
            if sm.get(k) is not False:
                blockers.append(f"summary_{k}_not_false")

        align = _read_json(align_p)
        if align.get("overlap_count") != 0:
            blockers.append("overlap_count_not_0")
        if align.get("visual_regions_in_ocr_plan") is not False:
            blockers.append("visual_regions_in_ocr_plan_not_false")
        if align.get("logo_qr_in_text_plan") is not False:
            blockers.append("logo_qr_in_text_plan_not_false")
        if align.get("semantic_join_allowed") is not False:
            blockers.append("alignment_semantic_join_allowed_not_false")

        risk = _read_json(risk_p)
        flags = risk.get("risk_flags") or []
        for rf in (
            "text_plan_not_ocr_evidence",
            "visual_symbol_not_brand_fact",
            "qr_not_decoded",
        ):
            if rf not in flags:
                blockers.append(f"risk_missing:{rf}")

        gate = _read_json(gate_p)
        for k, val in (
            ("fusion_allowed", False),
            ("ocr_execution_allowed", False),
            ("qr_decode_allowed", False),
            ("brand_identity_confirm_allowed", False),
            ("semantic_join_allowed", False),
            ("midplatform_fact_write_allowed", False),
            ("scene_delta_write_allowed", False),
            ("world_model_write_allowed", False),
        ):
            if gate.get(k) is not val:
                blockers.append(f"gate_{k}_wrong")

        sim = _read_json(sim_p)
        if sim.get("simulation_profile_id") != "developer_full":
            blockers.append("simulation_profile_id_not_developer_full")
        if sim.get("run_model") is not False:
            blockers.append("simulation_run_model_not_false")
        if sim.get("runtime_routing_changed") is not False:
            blockers.append("simulation_runtime_routing_changed_not_false")

        audit = _read_json(audit_p)
        audit_checks = (
            ("ocr_invoked", False),
            ("qr_decoder_invoked", False),
            ("brand_database_invoked", False),
            ("visual_symbol_registry_invoked", False),
            ("fusion_invoked", False),
            ("semantic_join_invoked", False),
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
            ("navigation_decision_invoked", False),
            ("runtime_routing_changed", False),
        )
        for k, val in audit_checks:
            if audit.get(k) is not val:
                blockers.append(f"audit_{k}_wrong")

    verdict = "NO_GO" if blockers else "GO"
    rep = {
        "schema": "cross_modal_poster_reference_only_verifier_report_v0",
        "phase": "CrossModal-Poster-OCR-ReferenceOnly-001",
        "verdict": verdict,
        "reference_only_root": str(root),
        "verifier_output_root": str(vout),
        "blockers": sorted(set(blockers)),
    }
    _write_json(vout / "cross_modal_poster_reference_only_verifier_report.json", rep)
    print(json.dumps({"verifier_output_root": str(vout), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
