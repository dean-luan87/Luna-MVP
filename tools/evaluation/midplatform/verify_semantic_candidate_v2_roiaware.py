#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Semantic Candidate v2 ROIAware."""

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
        "summary": "semantic_candidate_v2_roiaware_summary.json",
        "intake": "semantic_v2_evidence_pack_intake_matrix.json",
        "rules": "semantic_v2_roiaware_rule_matrix.json",
        "schema": "semantic_candidate_v2_roiaware_schema.json",
        "collection": "semantic_candidate_v2_roiaware_collection.json",
        "risk": "semantic_v2_risk_consumption_report.json",
        "guard": "semantic_v2_low_information_guard_report.json",
        "repeated": "semantic_v2_repeated_same_text_diagnostic_report.json",
        "blocking": "semantic_v2_blocking_matrix.json",
        "basis": "semantic_v2_interpretation_basis_report.json",
        "chain": "semantic_v2_source_chain_report.json",
        "routing": "semantic_v2_routing_report.json",
        "future": "semantic_v2_future_review_validation_plan.json",
        "boundary": "semantic_v2_boundary_report.json",
        "metrics": "semantic_v2_metrics_candidate_report.json",
        "bench": "semantic_v2_benchmark_link_report.json",
        "health": "semantic_v2_system_health_link_report.json",
        "no_write": "semantic_v2_no_write_boundary_report.json",
        "sim": "semantic_v2_simulation_context_report.json",
        "non_claims": "semantic_v2_non_claims_report.json",
        "followups": "semantic_v2_open_followups.json",
        "audit": "semantic_v2_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "semantic_v2_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    collection = data["collection"]
    rules = data["rules"]
    schema = data["schema"]
    repeated = data["repeated"]
    audit = data["audit"]

    ok(s.get("generator_scope") == "semantic_candidate_v2_roiaware_dryrun_only", "scope")
    ok(s.get("based_on_evidence_pack_v2_roiref") is True, "based")
    ok(s.get("evidence_pack_v2_count_observed") == 12, "ep_12")
    ok(s.get("semantic_candidate_v2_generated") is True, "sem_gen")
    ok(s.get("semantic_candidate_v2_count") == 12, "sem_12")
    ok(s.get("strong_semantic_generated_count") == 0, "no_strong")
    ok(s.get("risk_flags_consumed") is True, "risk_consumed")
    ok(s.get("repeated_same_text_consumed") is True, "repeated_consumed")
    ok(s.get("low_information_text_consumed") is True, "low_consumed")

    ok(data["intake"].get("row_count") == 12, "intake_12")
    rule_ids = [r.get("rule_id") for r in (rules.get("rules") or []) if isinstance(r, dict)]
    ok("low_information_text_blocks_strong_semantic" in rule_ids, "rule_low")
    ok("repeated_same_text_blocks_entity_confirmation" in rule_ids, "rule_repeat")
    ok("one_character_text_blocks_entity_semantic" in rule_ids, "rule_one_char")

    tmpl = schema.get("template") or {}
    gov = tmpl.get("governance") or {}
    ok(gov.get("strong_semantic_allowed") is False, "schema_strong")
    ok(gov.get("entity_confirmation_allowed") is False, "schema_entity")
    ok(gov.get("completion_allowed") is False, "schema_completion")
    ok(gov.get("correction_allowed") is False, "schema_correction")

    ok(collection.get("candidate_count") == 12, "coll_12")
    for cand in collection.get("candidates") or []:
        if isinstance(cand, dict):
            ok(cand.get("semantic_strength") != "strong", "not_strong")
            ok(cand.get("entity_candidate") is None, "entity_null")
            rc = cand.get("risk_consumption") or {}
            ok(rc.get("repeated_same_text_consumed") is True, "rc_repeat")
            ok(rc.get("low_information_text_consumed") is True, "rc_low")
            break

    risk_rows = data["risk"].get("rows") or []
    ok(sum(1 for r in risk_rows if r.get("repeated_same_text")) >= 1, "risk_repeat")
    ok(sum(1 for r in risk_rows if r.get("low_information_text")) >= 1, "risk_low")

    for row in data["guard"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("strong_semantic_allowed") is False, "guard_strong")
            break

    ok(repeated.get("diagnostic_status") == "requires_roi_quality_diagnosis", "diag_status")

    for row in data["blocking"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("blocked_world_model_attach") is True, "block_wm")
            ok(row.get("blocked_scene_delta_candidate") is True, "block_sd")
            break

    ok(data["basis"].get("basis_complete_not_semantic_valid") is True, "basis_note")
    ok(data["chain"].get("all_traceable_to_evidence_pack_v2") is True, "chain_ep")
    for row in data["chain"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_ocrrequest_reference") is True, "chain_ref")
            break

    ok(data["routing"].get("strong_semantic_generated_count") == 0, "route_strong")
    ok(data["routing"].get("entity_candidate_generated_count") == 0, "route_entity")

    phases = [p.get("future_phase") for p in (data["future"].get("phases") or []) if isinstance(p, dict)]
    ok("ROI-OCR-Quality-Diagnosis-v1" in phases, "future_quality")

    ok(data["boundary"].get("llm_invoked") is False, "boundary_llm")
    ok(data["boundary"].get("vlm_invoked") is False, "boundary_vlm")
    ok(data["boundary"].get("ocr_invoked") is False, "boundary_ocr")
    ok(data["metrics"].get("fact_write_allowed_count") == 0, "metrics_fact")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("semantic_candidate_v2_roiaware_executed") is True, "audit")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "semantic_v2_verifier_report.json",
        {"schema_version": "semantic_v2_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
