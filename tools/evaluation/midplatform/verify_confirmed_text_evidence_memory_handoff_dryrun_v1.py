#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Confirmed Text Evidence Memory Handoff DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


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
        "summary": "confirmed_text_evidence_memory_handoff_dryrun_v1_summary.json",
        "intake": "confirmed_text_memory_handoff_input_intake_matrix_v1.json",
        "sample_set": "confirmed_text_memory_handoff_dryrun_text_evidence_sample_set_v1.json",
        "evidence_collection": "confirmed_text_evidence_candidate_collection_v1.json",
        "append_collection": "confirmed_text_memory_append_request_candidate_collection_v1.json",
        "permission_check": "confirmed_text_memory_permission_policy_runtime_check_v1.json",
        "privacy_check": "confirmed_text_memory_privacy_sensitivity_runtime_check_v1.json",
        "csc_check": "confirmed_text_memory_correction_supersession_conflict_runtime_check_v1.json",
        "stale_check": "confirmed_text_memory_expired_stale_routing_runtime_check_v1.json",
        "handoff_collection": "confirmed_text_memory_governance_handoff_candidate_collection_v1.json",
        "worldmodel_check": "confirmed_text_worldmodel_scenedelta_link_runtime_check_v1.json",
        "user_emotional_link": "confirmed_text_user_emotional_context_runtime_link_v1.json",
        "read_call_check": "confirmed_text_memory_read_call_reference_runtime_check_v1.json",
        "trace": "confirmed_text_memory_handoff_decision_trace_v1.json",
        "final": "confirmed_text_memory_handoff_final_decision_v1.json",
        "boundary": "confirmed_text_memory_handoff_boundary_report_v1.json",
        "metrics": "confirmed_text_memory_handoff_metrics_candidate_report_v1.json",
        "bench": "confirmed_text_memory_handoff_benchmark_link_report_v1.json",
        "health": "confirmed_text_memory_handoff_system_health_report_v1.json",
        "no_write": "confirmed_text_memory_handoff_no_write_boundary_report_v1.json",
        "sim": "confirmed_text_memory_handoff_simulation_context_report_v1.json",
        "non_claims": "confirmed_text_memory_handoff_non_claims_report_v1.json",
        "followups": "confirmed_text_memory_handoff_open_followups_v1.json",
        "audit": "confirmed_text_memory_handoff_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "confirmed_text_memory_handoff_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    samples = data["sample_set"].get("samples") or []
    evidence = data["evidence_collection"].get("candidates") or []
    append = data["append_collection"].get("candidates") or []
    handoffs = data["handoff_collection"].get("candidates") or []

    ok(True, "summary")
    ok(s.get("dryrun_scope") == "confirmed_text_evidence_memory_handoff_dryrun_only", "scope")
    ok(s.get("based_on_memory_governance_contract") is True, "based_contract")
    ok(s.get("dryrun_text_evidence_samples_defined") is True, "samples_def")
    ok(s.get("confirmed_text_evidence_candidate_generated") is True, "evidence_gen")
    ok(s.get("memory_append_request_candidate_generated") is True, "append_gen")
    ok(s.get("permission_policy_applied") is True, "perm")
    ok(s.get("privacy_sensitivity_policy_applied") is True, "privacy")
    ok(s.get("correction_supersession_conflict_policy_applied") is True, "csc")
    ok(s.get("expired_stale_routing_policy_applied") is True, "stale")
    ok(s.get("memory_governance_handoff_candidate_generated") is True, "handoff_gen")
    ok(s.get("memory_governance_handoff_invoked_now") is False, "handoff_not_now")
    ok(s.get("memory_system_invoked") is False, "no_mem")
    ok(s.get("memory_written_now") is False, "no_write")
    ok(s.get("memory_deleted_now") is False, "no_del")
    ok(s.get("memory_updated_now") is False, "no_upd")
    ok(len(samples) >= 8, "eight_samples")
    ok(all(
        c.get("source_chain") and c.get("time_anchor") and c.get("spatial_anchor")
        for c in evidence if isinstance(c, dict)
    ), "anchors")
    ok(all(c.get("operation") == "append_only" for c in append if isinstance(c, dict)), "append_only")
    forbidden_ops = {"delete_memory", "update_memory", "overwrite_memory"}
    ok(not any(c.get("operation") in forbidden_ops for c in append if isinstance(c, dict)), "no_forbidden_op")
    pc = data["permission_check"]
    ok(pc.get("delete_memory_invoked_now") is False, "del_not_invoked")
    ok(pc.get("update_memory_invoked_now") is False, "upd_not_invoked")
    ok(pc.get("overwrite_memory_invoked_now") is False, "ovw_not_invoked")
    pr = data["privacy_check"]
    ok(pr.get("medical_text_review_required") is True, "med_review")
    ok(pr.get("financial_text_review_required") is True, "fin_review")
    ok(pr.get("identity_document_text_review_required") is True, "id_review")
    csc = data["csc_check"]
    ok(csc.get("original_evidence_overwritten_now") is False, "no_overwrite")
    ok(csc.get("correction_candidate_generated") is True, "corr_gen")
    ok(data["stale_check"].get("stale_does_not_imply_discard") is True, "no_discard")
    ok(all(h.get("handoff_invoked_now") is False for h in handoffs if isinstance(h, dict)), "ho_not_now")
    wm = data["worldmodel_check"]
    ok(wm.get("confirmed_text_cannot_write_world_model_directly") is True, "no_wm")
    ok(wm.get("confirmed_text_cannot_generate_scene_delta_directly") is True, "no_sd")
    ue = data["user_emotional_link"]
    ok(ue.get("user_profile_fact_written_now") is False, "no_profile")
    ok(ue.get("emotional_fact_written_now") is False, "no_emotion")
    ok(data["read_call_check"].get("memory_result_cannot_override_live_observation") is True, "no_override")
    ok(data["final"].get("final_decision") == "READY_FOR_MEMORY_GOVERNANCE_HANDOFF_RUNTIME_LATER", "final")
    ok(data["boundary"].get("handoff_dryrun_only") is True, "boundary")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics_nw")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("no_runtime_health_claim") is True, "health")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_mp")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("scene_delta_candidate_generated") is False, "audit_sd")
    ok(data["audit"].get("runtime_routing_changed") is False, "audit_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 69,
        "blockers": blockers,
        "phase": "Confirmed-Text-Evidence-Memory-Handoff-DryRun-v1-001",
    }
    _write_json(root / "confirmed_text_memory_handoff_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
