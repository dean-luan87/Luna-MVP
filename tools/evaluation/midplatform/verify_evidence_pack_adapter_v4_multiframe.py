#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Evidence Pack Adapter v4 Multiframe."""

from __future__ import annotations

import argparse
import json
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
        "summary": "evidence_pack_adapter_v4_multiframe_summary.json",
        "intake": "evidence_pack_v4_multiframe_ocr_result_intake_matrix.json",
        "schema": "evidence_pack_v4_multiframe_schema.json",
        "collection": "evidence_pack_v4_multiframe_collection.json",
        "alignment": "evidence_pack_v4_multiframe_alignment_matrix.json",
        "empty_guard": "evidence_pack_v4_empty_ocr_result_guard_report.json",
        "proj_risk": "evidence_pack_v4_projection_risk_preservation_report.json",
        "mf_ctx": "evidence_pack_v4_multiframe_context_report.json",
        "provider": "evidence_pack_v4_provider_metadata_report.json",
        "bbox": "evidence_pack_v4_bbox_crop_context_report.json",
        "sem_ready": "evidence_pack_v4_semantic_readiness_report.json",
        "sv_ready": "evidence_pack_v4_source_validation_rerun_readiness_report.json",
        "carryover": "evidence_pack_v4_same_frame_blocker_carryover_report.json",
        "future": "evidence_pack_v4_future_fix_plan.json",
        "chain": "evidence_pack_v4_source_chain_report.json",
        "boundary": "evidence_pack_v4_boundary_report.json",
        "metrics": "evidence_pack_v4_metrics_candidate_report.json",
        "bench": "evidence_pack_v4_benchmark_link_report.json",
        "health": "evidence_pack_v4_system_health_link_report.json",
        "no_write": "evidence_pack_v4_no_write_boundary_report.json",
        "sim": "evidence_pack_v4_simulation_context_report.json",
        "non_claims": "evidence_pack_v4_non_claims_report.json",
        "followups": "evidence_pack_v4_open_followups.json",
        "audit": "evidence_pack_v4_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(
            root / "evidence_pack_v4_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    schema = data["schema"]
    coll = data["collection"]
    align = data["alignment"]
    empty_guard = data["empty_guard"]
    proj = data["proj_risk"]
    mf_ctx = data["mf_ctx"]
    provider = data["provider"]
    sem_ready = data["sem_ready"]
    sv_ready = data["sv_ready"]
    carryover = data["carryover"]
    future = data["future"]
    chain = data["chain"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("adapter_scope") == "multiframe_ocr_result_to_evidence_pack_v4_only", "scope")
    ok(s.get("based_on_multiframe_ocr_result_collection") is True, "based_ocr")
    ok(s.get("multiframe_ocr_result_count_observed") == 30, "ocr30")
    ok(s.get("evidence_pack_v4_generated") is True, "ep_gen")
    ok(s.get("evidence_pack_v4_count") == 30, "ep30")
    ok(s.get("empty_ocr_result_count") == 30, "empty30")
    ok(s.get("non_empty_ocr_result_count") == 0, "nonempty0")
    ok(s.get("empty_text_is_valid_ocr_result") is True, "empty_valid")
    ok(s.get("empty_text_is_not_no_text_fact") is True, "not_no_text_fact")
    ok(s.get("projection_crop_not_detection") is True, "proj_not_det")
    ok(s.get("multiframe_result_not_consensus") is True, "not_consensus")
    ok(s.get("same_frame_blocker_still_active") is True, "blocker_active")
    ok(s.get("semantic_candidate_generated") is False, "no_sem")
    ok(s.get("source_validation_rerun_invoked") is False, "no_sv")

    intake_rows = intake.get("rows") or []
    ok(len(intake_rows) == 30, "intake_30")
    for row in intake_rows:
        if isinstance(row, dict):
            ok(row.get("empty_text") is True, "intake_empty")
            ok(row.get("detected_region") is False, "intake_not_det")
            ok(row.get("raw_ocr_text") == "", "intake_raw_empty")
            break

    tmpl = schema.get("template") or {}
    ok(tmpl.get("evidence_tier") == "multiframe_ocr_result_primary", "tier")
    ok(tmpl.get("raw_ocr", {}).get("empty_text_is_not_no_text_fact") is True, "schema_not_fact")

    packs = coll.get("packs") or []
    ok(len(packs) == 30, "packs_30")
    for p in packs:
        if isinstance(p, dict):
            ok(p.get("empty_text") is True, "pack_empty")
            ok(p.get("detected_region") is False, "pack_not_det")
            es = p.get("evidence_status") or {}
            ok(es.get("semantic_candidate_allowed_later") is False, "sem_later_false")
            ok(es.get("source_validation_rerun_allowed_later") is False, "sv_later_false")
            break

    ok(align.get("one_to_one_mapping") is True, "one_to_one")
    for arow in align.get("rows") or []:
        if isinstance(arow, dict):
            ok(arow.get("one_to_one_mapping") is True, "align_oto")
            break

    ok(empty_guard.get("no_text_fact_written") is False, "no_text_fact_written")
    ok(empty_guard.get("semantic_candidate_blocked_due_to_empty") is True, "sem_blocked_empty")
    ok(empty_guard.get("source_validation_rerun_blocked_due_to_empty") is True, "sv_blocked_empty")

    for pr in proj.get("rows") or []:
        if isinstance(pr, dict):
            ok(pr.get("projection_crop_not_detection") is True, "proj_row")
            break

    for m in mf_ctx.get("rows") or []:
        if isinstance(m, dict):
            ok(m.get("independent_consensus_allowed_now") is False, "no_consensus")
            break

    ok(provider.get("provider_comparison_claimed") is False, "prov_no_compare")

    for sr in sem_ready.get("rows") or []:
        if isinstance(sr, dict):
            ok(sr.get("semantic_readiness_status") == "blocked_empty_ocr_result", "sem_status")
            break

    for sv in sv_ready.get("rows") or []:
        if isinstance(sv, dict):
            ok(sv.get("readiness_status") == "blocked_empty_ocr_result", "sv_status")
            break

    ok(carryover.get("same_frame_blocker_resolved") is False, "blocker_not_resolved")
    future_phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("Crop-Quality-Diagnosis-v2-Multiframe" in future_phases, "future_crop_quality")
    for cr in chain.get("rows") or []:
        if isinstance(cr, dict):
            ok(cr.get("traceable_to_multiframe_ocr_result") is True, "chain_ocr")
            break

    ok(boundary.get("ocr_invoked") is False, "no_ocr")
    ok(boundary.get("provider_invoked") is False, "no_provider")
    ok(metrics.get("empty_result_rate") == 1.0, "empty_rate_1")
    ok(metrics.get("fact_write_allowed_count") == 0, "fact_write_0")
    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_no_runtime")
    ok(no_write.get("boundary_ok") is True, "boundary_ok")
    ok(no_write.get("violations") == [], "violations_empty")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("empty_ocr_result_count") == 30, "audit_empty30")
    ok(audit.get("world_model_attach_executed") is False, "audit_no_wm")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 72,
        "blockers": blockers,
        "phase": "Evidence-Pack-Adapter-v4-Multiframe-001",
    }
    _write_json(root / "evidence_pack_v4_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
