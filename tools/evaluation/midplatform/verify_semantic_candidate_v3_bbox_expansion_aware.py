#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Semantic Candidate v3 BBoxExpansionAware."""

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
        "summary": "semantic_candidate_v3_bbox_expansion_aware_summary.json",
        "intake": "semantic_v3_ep_v3_intake_matrix.json",
        "rules": "semantic_v3_bbox_expansion_rule_matrix.json",
        "schema": "semantic_candidate_v3_bbox_expansion_schema.json",
        "collection": "semantic_candidate_v3_bbox_expansion_collection.json",
        "bank": "semantic_v3_bank_like_candidate_report.json",
        "noisy": "semantic_v3_noisy_english_ocr_noise_report.json",
        "repeat": "semantic_v3_strategy_repeat_consensus_guard_report.json",
        "entity": "semantic_v3_entity_candidate_boundary_report.json",
        "basis": "semantic_v3_interpretation_basis_report.json",
        "chain": "semantic_v3_source_chain_report.json",
        "routing": "semantic_v3_routing_report.json",
        "sv": "semantic_v3_source_validation_v2_readiness_plan.json",
        "review": "semantic_v3_review_policy_readiness_plan.json",
        "slot": "semantic_v3_unresolved_slot_linkage_plan.json",
        "boundary": "semantic_v3_boundary_report.json",
        "metrics": "semantic_v3_metrics_candidate_report.json",
        "bench": "semantic_v3_benchmark_link_report.json",
        "health": "semantic_v3_system_health_link_report.json",
        "no_write": "semantic_v3_no_write_boundary_report.json",
        "sim": "semantic_v3_simulation_context_report.json",
        "non_claims": "semantic_v3_non_claims_report.json",
        "followups": "semantic_v3_open_followups.json",
        "audit": "semantic_v3_audit_report.json",
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
            root / "semantic_v3_verifier_report.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    schema = data["schema"]
    collection = data["collection"]
    bank = data["bank"]
    noisy = data["noisy"]
    repeat = data["repeat"]
    entity = data["entity"]
    basis = data["basis"]
    chain = data["chain"]
    routing = data["routing"]
    sv = data["sv"]
    review = data["review"]
    slot = data["slot"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("generator_scope") == "semantic_candidate_v3_bbox_expansion_aware_dryrun_only", "scope")
    ok(s.get("based_on_evidence_pack_v3_bbox_expansion") is True, "based_ep_v3")
    ok(s.get("evidence_pack_v3_count_observed") == 4, "ep4")
    ok(s.get("semantic_candidate_v3_generated") is True, "sem_gen")
    ok(s.get("entity_confirmed_count") == 0, "no_entity_confirmed")
    ok(s.get("llm_invoked") is False, "no_llm")
    ok(s.get("vlm_invoked") is False, "no_vlm")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("source_validation_v2_invoked") is False, "no_sv")

    ok(intake.get("row_count") == 4 or len(intake.get("rows") or []) == 4, "intake_4")
    for row in intake.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("intake_status") == "accepted", "intake_accepted")
            ok(row.get("fact_status") == "not_fact", "intake_not_fact")
            ok(row.get("write_allowed") is False, "intake_no_write")
            break

    rule_ids = {r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)}
    ok("bank_like_text_generates_candidate_only" in rule_ids, "rule_bank")
    ok("repeated_strategy_output_not_consensus" in rule_ids, "rule_repeat")
    ok("same_frame_same_region_blocks_independent_consensus" in rule_ids, "rule_same_frame")

    tmpl = schema.get("template") or {}
    ok(tmpl.get("entity_candidate", {}).get("entity_confirmed") is False, "schema_entity_false")
    ok(tmpl.get("governance", {}).get("source_validation_v2_invoked_now") is False, "schema_no_sv_now")

    cands = collection.get("candidates") or []
    ok(collection.get("candidate_count") == 4 or len(cands) == 4, "collection_4")
    for c in cands:
        if isinstance(c, dict):
            ok(c.get("fact_status") == "not_fact", "cand_not_fact")
            ok(c.get("write_allowed") is False, "cand_no_write")
            gov = c.get("governance") or {}
            ok(gov.get("entity_confirmation_allowed") is False, "gov_no_confirm")
            ent = c.get("entity_candidate")
            if ent:
                ok(ent.get("entity_confirmed") is False, "ent_not_confirmed")
            ti = c.get("text_interpretation") or {}
            ok(ti.get("correction_committed") is False, "no_correction")
            ok(ti.get("completion_committed") is False, "no_completion")
            cc = ti.get("completion_candidate")
            ok(cc is None or "China Construction Bank" not in str(cc), "no_ccb_completion")
            break

    for row in bank.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("entity_confirmed") is False, "bank_not_confirmed")
            blockers_list = row.get("confirmation_blockers") or []
            ok("source_validation_v2_not_invoked" in blockers_list, "bank_sv_blocker")
            ok("same_frame_same_region_not_independent_consensus" in blockers_list, "bank_consensus_blocker")
            break

    for row in noisy.get("rows") or []:
        if isinstance(row, dict) and row.get("noisy_segments"):
            ok(row.get("correction_committed") is False, "noisy_no_correction")
            ok(row.get("completion_committed") is False, "noisy_no_completion")
            ok(row.get("completion_candidate") is None, "noisy_no_completion_cand")
            break

    ok(repeat.get("repeated_output_not_consensus") is True, "repeat_not_consensus")
    ok(repeat.get("independent_consensus_allowed") is False, "no_independent_consensus")
    ok(repeat.get("same_frame_same_region_not_independent_consensus") is True, "repeat_same_frame")

    for row in entity.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("entity_confirmation_allowed") is False, "entity_boundary_no_confirm")
            ok(row.get("entity_confirmed") is False, "entity_boundary_not_confirmed")
            break

    for row in basis.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("evidence_pack_v3_ref") is not None, "basis_ep_ref")
            break

    for row in chain.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_evidence_pack_v3") is True, "chain_ep")
            ok(row.get("traceable_to_ocrrequest_reference_v2") is True, "chain_ref_v2")
            ok(row.get("traceable_to_expanded_crop_artifact") is True, "chain_crop")
            ok(row.get("source_chain_preserved") is True, "chain_preserved")
            break

    ok(routing.get("entity_confirmed_count") == 0, "routing_no_entity")
    ok(routing.get("correction_committed_count") == 0, "routing_no_correction")
    ok(routing.get("completion_committed_count") == 0, "routing_no_completion")

    ok(sv.get("validation_not_invoked_in_this_phase") is True, "sv_not_invoked")
    ok(sv.get("not_in_current_phase") is True, "sv_not_current")

    ok(review.get("not_in_current_phase") is True, "review_not_current")

    ok(slot.get("slot_generation_allowed_in_this_phase") is False, "no_slot_gen")

    ok(boundary.get("world_model_attach_allowed") is False, "boundary_no_wm")
    ok(boundary.get("scene_delta_candidate_allowed") is False, "boundary_no_scene_delta")

    ok(metrics.get("fact_write_allowed_count") == 0, "metrics_no_fact_write")

    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")

    ok(health.get("provider_health_runtime_checked") is False, "health_no_runtime")

    ok(no_write.get("boundary_ok") is True, "no_write_ok")
    ok(no_write.get("violations") == [], "no_write_violations")

    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")

    ok(data["non_claims"].get("semantic_candidate_not_fact") is True, "non_claims_not_fact")
    ok(len(data["followups"].get("items") or []) >= 5, "followups_exist")

    ok(audit.get("world_model_attach_executed") is False, "audit_no_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_scene_delta")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("world_model_written") is False, "audit_no_wm_write")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_routing")

    verdict = "GO" if not blockers and checks >= 60 else ("CONDITIONAL_GO" if not blockers else "NO_GO")
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 68,
        "blockers": blockers,
        "phase": "Semantic-Candidate-v3-BBoxExpansionAware-001",
    }
    _write_json(root / "semantic_v3_verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
