#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Review Queue Runtime DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

FORBIDDEN_STATES = {"approved", "committed", "written_to_fact", "attached_to_world_model", "scene_delta_generated"}
REQUIRED_QUEUE_TYPES = {
    "ttl_review_queue",
    "roi_retry_queue",
    "visual_symbol_registry_queue",
    "better_source_queue",
    "unresolved_slot_later_queue",
}


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
        "summary": "ocr_review_queue_runtime_dryrun_v1_summary.json",
        "schema": "ocr_review_queue_runtime_item_schema_v1.json",
        "intake": "ocr_review_queue_runtime_intake_report.json",
        "classification": "ocr_review_queue_runtime_classification_matrix.json",
        "priority_policy": "ocr_review_queue_runtime_priority_policy_v1.json",
        "priority_sort": "ocr_review_queue_runtime_priority_sort_report.json",
        "state_plan": "ocr_review_queue_runtime_state_transition_plan.json",
        "state_trace": "ocr_review_queue_runtime_state_transition_trace.json",
        "dequeue": "ocr_review_queue_runtime_dequeue_dryrun_report.json",
        "handlers": "ocr_review_queue_runtime_handler_dryrun_matrix.json",
        "placeholders": "ocr_review_queue_runtime_decision_placeholder_report.json",
        "boundary": "ocr_review_queue_runtime_boundary_report.json",
        "chain": "ocr_review_queue_runtime_source_chain_report.json",
        "metrics": "ocr_review_queue_runtime_metrics_candidate_report.json",
        "bench": "ocr_review_queue_runtime_benchmark_link_report.json",
        "health": "ocr_review_queue_runtime_system_health_link_report.json",
        "no_write": "ocr_review_queue_runtime_no_write_boundary_report.json",
        "sim": "ocr_review_queue_runtime_simulation_context_report.json",
        "non_claims": "ocr_review_queue_runtime_non_claims_report.json",
        "followups": "ocr_review_queue_runtime_open_followups.json",
        "audit": "ocr_review_queue_runtime_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "ocr_review_queue_runtime_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    schema = data["schema"]
    intake = data["intake"]
    classification = data["classification"]
    priority_policy = data["priority_policy"]
    priority_sort = data["priority_sort"]
    state_plan = data["state_plan"]
    state_trace = data["state_trace"]
    dequeue = data["dequeue"]
    handlers = data["handlers"]
    placeholders = data["placeholders"]
    boundary = data["boundary"]
    chain = data["chain"]
    metrics = data["metrics"]
    audit = data["audit"]

    ok(s.get("runtime_scope") == "review_queue_runtime_dryrun_only", "scope")
    ok(s.get("queue_runtime_enabled") is True, "runtime_enabled")
    ok(s.get("enqueue_simulated") is True, "enqueue")
    ok(s.get("dequeue_simulated") is True, "dequeue")
    ok(s.get("priority_sort_simulated") is True, "sort")
    ok(s.get("state_transition_simulated") is True, "transition")
    ok(s.get("decision_committed") is False, "no_decision")
    ok(s.get("approval_granted") is False, "no_approval")

    defaults = schema.get("defaults") or {}
    ok(defaults.get("decision_status") == "not_committed", "schema_decision")
    ok(defaults.get("approval_status") == "not_approved", "schema_approval")

    ok(intake.get("input_queue_candidate_count") == 47, "intake_count_47")
    ok(intake.get("accepted_into_runtime_queue_count") == 47, "accepted_47")

    cat_types = {c.get("queue_type") for c in (classification.get("categories") or []) if isinstance(c, dict)}
    for qt in REQUIRED_QUEUE_TYPES:
        ok(qt in cat_types, f"class_{qt}")

    for rule in priority_policy.get("rules") or []:
        if isinstance(rule, dict):
            ok(rule.get("auto_escalation_committed") is False, "no_auto_escalation")

    for row in priority_sort.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("decision_committed") is False, "sort_no_decision")
            ok(row.get("approval_status") == "not_approved", "sort_no_approval")

    forbidden_in_plan = set()
    for st in state_plan.get("states") or []:
        if isinstance(st, dict):
            forbidden_in_plan.update(st.get("forbidden_transition") or [])
    ok(FORBIDDEN_STATES.issubset(forbidden_in_plan), "plan_forbidden_states")

    for row in state_trace.get("rows") or []:
        if isinstance(row, dict):
            steps = row.get("transition_steps") or []
            for step in steps:
                ok(step not in FORBIDDEN_STATES, f"trace_no_{step}")
            ok(row.get("decision_status") == "not_committed", "trace_decision")

    ok(dequeue.get("decision_committed") is False, "dequeue_no_decision")
    ok(dequeue.get("approval_granted") is False, "dequeue_no_approval")

    for h in handlers.get("handlers") or []:
        if isinstance(h, dict):
            ok(h.get("decision_commit_allowed") is False, f"handler_{h.get('handler_id')}")

    ok(placeholders.get("all_not_committed") is True, "placeholder_not_committed")
    ok(boundary.get("approval_granted_count") == 0, "boundary_approval")
    ok(chain.get("all_traceable_to_semantic_v1") is True, "chain_semantic")
    ok(metrics.get("decision_committed_count") == 0, "metrics_decision")
    ok(metrics.get("fact_write_allowed_count") == 0, "metrics_fact")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["no_write"].get("violations") == [], "violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["non_claims"].get("no_review_decision_commit") is True, "non_claims")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("review_decision_committed") is False, "audit_decision")
    ok(audit.get("approval_granted") is False, "audit_approval")
    ok(audit.get("runtime_routing_changed") is False, "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "ocr_review_queue_runtime_verifier_report.json",
        {"schema_version": "ocr_review_queue_runtime_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
