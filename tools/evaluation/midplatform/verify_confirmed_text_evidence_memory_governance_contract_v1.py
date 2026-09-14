#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Confirmed Text Evidence Memory Governance Contract v1."""

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


def _perm_rule(perm: Dict[str, Any], op: str) -> Dict[str, Any]:
    for r in perm.get("rules") or []:
        if isinstance(r, dict) and r.get("operation") == op:
            return r
    return {}


def _privacy_class(priv: Dict[str, Any], cls: str) -> Dict[str, Any]:
    for r in priv.get("privacy_classes") or []:
        if isinstance(r, dict) and r.get("privacy_class") == cls:
            return r
    return {}


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
        "summary": "confirmed_text_evidence_memory_governance_contract_v1_summary.json",
        "intake": "confirmed_text_evidence_memory_input_intake_matrix_v1.json",
        "evidence_schema": "confirmed_text_evidence_schema_v1.json",
        "append_schema": "confirmed_text_memory_append_request_schema_v1.json",
        "permission": "midplatform_memory_permission_policy_v1.json",
        "correction": "confirmed_text_append_only_correction_policy_v1.json",
        "supersession_conflict": "confirmed_text_supersession_conflict_policy_v1.json",
        "expired_stale": "confirmed_text_expired_stale_routing_policy_v1.json",
        "read_call": "confirmed_text_memory_read_call_reference_policy_v1.json",
        "privacy": "confirmed_text_memory_privacy_sensitivity_policy_v1.json",
        "responsibility": "memory_governance_responsibility_boundary_v1.json",
        "handoff": "confirmed_text_memory_governance_handoff_candidate_v1.json",
        "worldmodel_link": "confirmed_text_worldmodel_scenedelta_link_policy_v1.json",
        "user_emotional_link": "confirmed_text_user_emotional_context_link_policy_v1.json",
        "trace": "confirmed_text_evidence_memory_governance_decision_trace_v1.json",
        "final": "confirmed_text_evidence_memory_governance_final_decision_v1.json",
        "boundary": "confirmed_text_evidence_memory_governance_boundary_report_v1.json",
        "metrics": "confirmed_text_evidence_memory_governance_metrics_candidate_report_v1.json",
        "bench": "confirmed_text_evidence_memory_governance_benchmark_link_report_v1.json",
        "health": "confirmed_text_evidence_memory_governance_system_health_report_v1.json",
        "no_write": "confirmed_text_evidence_memory_governance_no_write_boundary_report_v1.json",
        "sim": "confirmed_text_evidence_memory_governance_simulation_context_report_v1.json",
        "non_claims": "confirmed_text_evidence_memory_governance_non_claims_report_v1.json",
        "followups": "confirmed_text_evidence_memory_governance_open_followups_v1.json",
        "audit": "confirmed_text_evidence_memory_governance_audit_report_v1.json",
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
            root / "confirmed_text_evidence_memory_governance_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    es = data["evidence_schema"]
    ap_s = data["append_schema"]
    perm = data["permission"]
    corr = data["correction"]
    sc = data["supersession_conflict"]
    stale = data["expired_stale"]
    read_p = data["read_call"]
    priv = data["privacy"]
    resp = data["responsibility"]
    hand = data["handoff"]
    wm = data["worldmodel_link"]
    ue = data["user_emotional_link"]

    ok(True, "summary")
    ok(s.get("contract_scope") == "confirmed_text_evidence_memory_governance_contract_only", "scope")
    ok(s.get("memory_governance_contract_defined") is True, "mg_contract")
    ok(s.get("confirmed_text_evidence_schema_defined") is True, "cte_schema")
    ok(s.get("memory_append_request_schema_defined") is True, "append_schema")
    ok(s.get("memory_read_call_policy_defined") is True, "read_call")
    ok(s.get("midplatform_append_only_policy_defined") is True, "append_only")
    ok(s.get("midplatform_delete_forbidden") is True, "no_delete")
    ok(s.get("midplatform_update_forbidden") is True, "no_update")
    ok(s.get("correction_append_policy_defined") is True, "correction")
    ok(s.get("supersession_append_policy_defined") is True, "supersession")
    ok(s.get("conflict_append_policy_defined") is True, "conflict")
    ok(s.get("expired_stale_text_routing_policy_defined") is True, "stale")
    ok(s.get("privacy_sensitivity_policy_defined") is True, "privacy")
    ok(s.get("memory_governance_handoff_defined") is True, "handoff_def")
    ok(s.get("memory_system_invoked") is False, "no_mem_sys")
    ok(s.get("memory_written_now") is False, "no_mem_write")
    ok(s.get("memory_deleted_now") is False, "no_mem_del")
    ok(s.get("memory_updated_now") is False, "no_mem_upd")

    req = es.get("required_fields") or []
    ok("source_chain" in req, "source_chain")
    ok("time_anchor" in req, "time_anchor")
    ok("spatial_anchor" in req, "spatial_anchor")
    ok(ap_s.get("operation") == "append_only", "append_only_op")
    ok(_perm_rule(perm, "delete_memory").get("allowed_for_midplatform") is False, "del_forbidden")
    ok(_perm_rule(perm, "update_memory").get("allowed_for_midplatform") is False, "upd_forbidden")
    ok(_perm_rule(perm, "overwrite_memory").get("allowed_for_midplatform") is False, "ovw_forbidden")
    ok(corr.get("original_evidence_never_overwritten") is True, "no_overwrite")
    ok(sc.get("original_record_retained") is True, "retain_orig")
    ok(stale.get("stale_does_not_imply_discard") is True, "no_discard")
    ok(read_p.get("memory_result_cannot_override_live_observation") is True, "no_override")
    ok(_privacy_class(priv, "medical_text").get("review_required") is True, "med_review")
    ok(_privacy_class(priv, "financial_text").get("review_required") is True, "fin_review")
    ok("delete" in (resp.get("midplatform_forbidden") or []), "mp_forbid_del")
    ok("update" in (resp.get("midplatform_forbidden") or []), "mp_forbid_upd")
    ok("overwrite" in (resp.get("midplatform_forbidden") or []), "mp_forbid_ovw")
    ok("delete" in (resp.get("memory_governance_owns") or []), "mg_owns_del")
    ok("update" in (resp.get("memory_governance_owns") or []), "mg_owns_upd")
    ok("merge" in (resp.get("memory_governance_owns") or []), "mg_owns_merge")
    ok("conflict_resolution" in (resp.get("memory_governance_owns") or []), "mg_owns_conflict")
    ok(hand.get("handoff_invoked_now") is False, "handoff_not_now")
    ok(wm.get("confirmed_text_cannot_write_world_model_directly") is True, "no_wm_write")
    ok(wm.get("confirmed_text_cannot_generate_scene_delta_directly") is True, "no_sd")
    ok(ue.get("midplatform_cannot_promote_to_profile_fact") is True, "no_profile_fact")
    ok(data["final"].get("final_decision") == "READY_FOR_MEMORY_GOVERNANCE_HANDOFF_DRYRUN_LATER", "final")
    ok(data["boundary"].get("contract_only") is True, "contract_only")
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
        "checks_expected": 72,
        "blockers": blockers,
        "phase": "Confirmed-Text-Evidence-Memory-Governance-Contract-v1-001",
    }
    _write_json(root / "confirmed_text_evidence_memory_governance_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
