#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Evidence Pack Adapter v3 BBoxExpansion."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path):
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
    checks = 0

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "evidence_pack_adapter_v3_bbox_expansion_summary.json",
        "intake": "evidence_pack_v3_expanded_roi_result_intake_matrix.json",
        "schema": "evidence_pack_v3_bbox_expansion_schema.json",
        "collection": "evidence_pack_v3_bbox_expansion_collection.json",
        "alignment": "evidence_pack_v3_bbox_expansion_alignment_matrix.json",
        "strategy_pres": "evidence_pack_v3_strategy_preservation_report.json",
        "raw_pres": "evidence_pack_v3_raw_text_preservation_report.json",
        "text_pres": "evidence_pack_v3_text_item_confidence_preservation_report.json",
        "strategy_risk": "evidence_pack_v3_strategy_output_risk_report.json",
        "coord": "evidence_pack_v3_bbox_coordinate_attachment_report.json",
        "strategy_cmp": "evidence_pack_v3_strategy_comparison_candidate_report.json",
        "provider": "evidence_pack_v3_provider_metadata_report.json",
        "chain": "evidence_pack_v3_source_chain_report.json",
        "readiness": "evidence_pack_v3_semantic_readiness_report.json",
        "sv_ready": "evidence_pack_v3_source_validation_v2_readiness_report.json",
        "boundary": "evidence_pack_v3_boundary_report.json",
        "metrics": "evidence_pack_v3_metrics_candidate_report.json",
        "bench": "evidence_pack_v3_benchmark_link_report.json",
        "health": "evidence_pack_v3_system_health_link_report.json",
        "no_write": "evidence_pack_v3_no_write_boundary_report.json",
        "sim": "evidence_pack_v3_simulation_context_report.json",
        "non_claims": "evidence_pack_v3_non_claims_report.json",
        "followups": "evidence_pack_v3_open_followups.json",
        "audit": "evidence_pack_v3_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "evidence_pack_v3_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    collection = data["collection"]
    alignment = data["alignment"]
    coord = data["coord"]
    boundary = data["boundary"]
    audit = data["audit"]

    ok(s.get("adapter_scope") == "expanded_roi_ocr_result_to_evidence_pack_v3_only", "scope")
    ok(s.get("based_on_expanded_roi_ocr_result_v2") is True, "based")
    ok(s.get("expanded_roi_ocr_result_count_observed") == 4, "result_12")
    ok(s.get("evidence_pack_v3_generated") is True, "ep_gen")
    ok(s.get("evidence_pack_v3_count") == 4, "ep_4")
    ok(s.get("raw_ocr_text_preserved") is True, "raw_preserved")
    ok(s.get("text_items_preserved") is True, "items_preserved")
    ok(s.get("ocrrequest_reference_v2_ref_preserved") is True, "ref_preserved")
    ok(s.get("expanded_crop_artifact_ref_preserved") is True, "crop_preserved")
    ok(s.get("semantic_candidate_generated") is False, "no_semantic")

    ok(s.get("expansion_strategy_preserved") is True, "strategy_preserved")
    ok(s.get("source_bbox_preserved") is True, "source_bbox")
    ok(s.get("expanded_bbox_preserved") is True, "expanded_bbox")
    ok(s.get("strategy_comparison_ref_preserved") is True, "strategy_ref")
    ok(s.get("source_validation_v2_invoked") is False, "no_sv")

    for row in data["strategy_pres"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("strategy_comparison_candidate_only") is True, "strat_cmp_only")
            ok(row.get("benchmark_claimed") is False, "no_bench")
            break

    raw_pres = data["raw_pres"]
    for row in raw_pres.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("correction_committed") is False, "no_correction")
            ok(row.get("completion_committed") is False, "no_completion")
            break

    strat_risk = data["strategy_risk"]
    ok(strat_risk.get("non_empty_text_not_accuracy") is True, "risk_accuracy")
    for row in strat_risk.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("same_frame_same_region_not_independent_consensus") is True, "same_frame")
            break

    ok(data["strategy_cmp"]["rows"][0].get("comparison_candidate_only") is True, "cmp_only")
    ok(data["strategy_cmp"]["rows"][0].get("benchmark_score_generated") is False, "cmp_bench")

    chain = data["chain"]
    ok(chain.get("all_traceable_to_expanded_roi_ocr_result_v2") is True, "chain_ocr_v2")
    for row in chain.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_expanded_crop_artifact") is True, "chain_crop")
            ok(row.get("traceable_to_bbox_expansion_candidate") is True, "chain_bbox")
            break

    ok(data["sv_ready"].get("source_validation_v2_invoked_now") is False, "sv_now")
    ok(data["readiness"].get("semantic_candidate_generated_now") is False, "sem_now")


    ok(data["intake"].get("row_count") == 4, "intake_4")
    tmpl = data["schema"].get("template") or {}
    ok(tmpl.get("evidence_tier") == "expanded_roi_ocr_primary", "tier")

    ok(collection.get("pack_count") == 4, "pack_4")
    for pack in collection.get("packs") or []:
        if isinstance(pack, dict):
            ok(pack.get("fact_status") == "not_fact", "pack_not_fact")
            ok(pack.get("write_allowed") is False, "pack_no_write")
            ok(pack.get("raw_ocr", {}).get("raw_ocr_text_preserved") is True, "pack_raw_preserved")
            rf = pack.get("risk_flags") or {}
            ok(rf.get("non_empty_text_not_accuracy") is True, "risk_not_accuracy")
            ok(pack.get("expansion_strategy") is not None, "pack_strategy")
            break

    ok(alignment.get("all_one_to_one_mapping") is True, "one_to_one")
    ok(alignment.get("orphan_pack") is False, "no_orphan")

    for row in data["text_pres"].get("rows") or []:
        if isinstance(row, dict) and row.get("text_item_count", 0) > 0:
            ok(row.get("text_items_have_bbox") is True, "has_bbox")
            ok(row.get("text_items_have_confidence") is True, "has_conf")
            break

    ok(strat_risk.get("global_repeated_same_text_detected") is True, "repeated_detected")
    repeated_rows = sum(1 for r in (strat_risk.get("rows") or []) if r.get("repeated_with_other_strategy"))
    ok(repeated_rows >= 2, "repeated_strategy_rows")

    for row in coord.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("coordinate_fabrication_detected") is False, "no_fabrication")
            ok(row.get("gps_lat") is None, "gps_lat")
            ok(row.get("gps_lng") is None, "gps_lng")
            break

    ok(data["provider"].get("rows"), "provider_rows")
    for row in data["provider"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("provider_comparison_claimed") is False, "no_comparison")
            break

    ok(boundary.get("ocr_invoked") is False, "boundary_no_ocr")
    ok(boundary.get("provider_invoked") is False, "boundary_no_provider")
    ok(boundary.get("world_model_attach_allowed") is False, "boundary_wm")
    ok(boundary.get("scene_delta_candidate_allowed") is False, "boundary_sd")
    ok(data["no_write"].get("violations") == [], "violations_empty")
    ok(data["metrics"].get("fact_write_allowed_count") == 0, "metrics_fact")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("evidence_pack_adapter_v3_bbox_expansion_executed") is True, "audit")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "evidence_pack_v3_verifier_report.json",
        {"schema_version": "evidence_pack_v3_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
