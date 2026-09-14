# -*- coding: utf-8 -*-
"""Scene Graph / Relation Model smoke IO decision review — evaluator helpers v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.scene_graph_relation_model_smoke_io_decision_review_items_v1 import (
    DECISION_CASES,
    INPUT_SOURCE_REVIEWS,
    NEW_PROTOCOL_REASON_REPORT,
    NON_EXECUTION_FLAGS,
    PREREQUISITE_CHAIN,
    PROTOCOL_REUSE_DECISION,
    SMOKE_IO_ELIGIBILITY_GATES,
)


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def evaluate_prerequisite_chain() -> Tuple[List[Dict[str, Any]], bool, int]:
    rows: List[Dict[str, Any]] = []
    go_count = 0
    for item in PREREQUISITE_CHAIN:
        root = Path(item["default_output"]).expanduser().resolve()
        summary = read_json(root / "summary.json")
        verifier = read_json(root / "verifier_report.json")
        pass_flag = item["pass_flag"]
        is_go = (
            summary.get("final_decision") == item["final_decision_go"]
            and summary.get(pass_flag) is True
            and verifier.get("verifier") == "GO"
            and root.is_dir()
        )
        if is_go:
            go_count += 1
        rows.append({
            "priority": item["priority"],
            "adapter_id": item["adapter_id"],
            "anchor_role": item["anchor_role"],
            "candidate_types": list(item.get("candidate_types") or ()),
            "output_root": str(root),
            "artifact_present": root.is_dir() and (root / "summary.json").is_file(),
            "task_collaboration_planning_go": is_go,
            "final_decision": summary.get("final_decision"),
            "pass_flag": pass_flag,
            "pass_flag_value": summary.get(pass_flag),
            "verifier": verifier.get("verifier"),
        })
    return rows, go_count == len(PREREQUISITE_CHAIN), go_count


def _priority_go(prerequisite_rows: List[Dict[str, Any]], priority: str) -> bool:
    row = next((r for r in prerequisite_rows if r["priority"] == priority), None)
    return bool(row and row.get("task_collaboration_planning_go"))


def _classify_input_source(
    review: Dict[str, Any],
    prerequisite_rows: List[Dict[str, Any]],
) -> str:
    priorities = tuple(review.get("upstream_priorities") or ())
    phase_hits = [p for p in priorities if p in ("P0", "P1", "P2", "P3")]
    field_hits = [p for p in priorities if p == "field"]
    phase_go = any(_priority_go(prerequisite_rows, p) for p in phase_hits)
    phase_partial = any(
        next((r for r in prerequisite_rows if r["priority"] == p), {}).get("artifact_present")
        for p in phase_hits
    )
    if phase_go:
        return "sufficient_for_smoke_io"
    if phase_partial or field_hits:
        return "partially_sufficient"
    return "insufficient"


def evaluate_input_sources(
    prerequisite_rows: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    rows: List[Dict[str, Any]] = []
    classifications: List[str] = []
    for review in INPUT_SOURCE_REVIEWS:
        classification = _classify_input_source(review, prerequisite_rows)
        classifications.append(classification)
        rows.append({
            "review_id": review["review_id"],
            "candidate_types": list(review["candidate_types"]),
            "upstream_sources": list(review["upstream_sources"]),
            "upstream_priorities": list(review["upstream_priorities"]),
            "relation_role": review["relation_role"],
            "classification": classification,
            "supports_relation_input": classification in ("sufficient_for_smoke_io", "partially_sufficient"),
        })
    if all(c == "sufficient_for_smoke_io" for c in classifications):
        overall = "sufficient_for_smoke_io"
    elif any(c == "insufficient" for c in classifications):
        overall = "insufficient"
    elif any(c == "partially_sufficient" for c in classifications):
        overall = "partially_sufficient"
    else:
        overall = "blocked"
    return rows, overall


def evaluate_eligibility_gates(
    input_source_rows: List[Dict[str, Any]],
    *,
    all_prereqs_go: bool,
) -> Tuple[List[Dict[str, Any]], bool]:
    by_id = {r["review_id"]: r for r in input_source_rows}
    gate_rows: List[Dict[str, Any]] = []
    all_passed = True
    for gate in SMOKE_IO_ELIGIBILITY_GATES:
        gid = gate["gate_id"]
        passed = False
        if gid == "protocol_reuse_gate":
            passed = (
                PROTOCOL_REUSE_DECISION.get("reuse_traceability_refs") is True
                and PROTOCOL_REUSE_DECISION.get("reuse_authorization_boundary") is True
                and NON_EXECUTION_FLAGS.get("candidate_only") is True
            )
        elif gid == "no_new_protocol_gate":
            passed = (
                PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False
                and NEW_PROTOCOL_REASON_REPORT.get("owner_approval_required") is False
            )
        else:
            review_ids = gate.get("source_review_ids") or ()
            required_any = set(gate.get("required_any") or ())
            available: set[str] = set()
            for rid in review_ids:
                row = by_id.get(rid)
                if row and row.get("classification") == "sufficient_for_smoke_io":
                    available.update(row.get("candidate_types") or [])
            passed = bool(required_any & available)
        gate_rows.append({"gate_id": gid, "passed": passed, "prereqs_go": all_prereqs_go})
        if not passed:
            all_passed = False
    return gate_rows, all_passed and all_prereqs_go


def evaluate_decision_cases(
    *,
    input_source_rows: List[Dict[str, Any]],
    overall_sufficiency: str,
    gate_decision: Dict[str, Any],
    owner_compliance_ok: bool,
) -> Tuple[List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_passed = True
    by_id = {r["review_id"]: r for r in input_source_rows}
    for case in DECISION_CASES:
        ok = False
        if case.get("source_review"):
            row = by_id.get(case["source_review"])
            ok = row is not None and bool(row.get("classification"))
        elif case.get("expect_sufficiency_assigned"):
            ok = overall_sufficiency in (
                "sufficient_for_smoke_io", "partially_sufficient", "insufficient", "blocked",
            )
        elif case.get("expect_no_relation"):
            ok = (
                NON_EXECUTION_FLAGS.get("no_relation_candidate_generated") is True
                and NON_EXECUTION_FLAGS.get("no_world_relation_candidate_generated") is True
            )
        elif case.get("expect_no_wm"):
            ok = NON_EXECUTION_FLAGS.get("no_world_model_assembly") is True
        elif case.get("expect_new_protocol") is False:
            ok = PROTOCOL_REUSE_DECISION.get("new_protocol_added") is False
        elif case.get("expect_gate_decision"):
            ok = gate_decision.get("selected_option") in (
                "remain_deferred", "ready_for_smoke_io", "blocked_pending_owner_decision",
            )
        elif case.get("expect_owner_compliance"):
            ok = owner_compliance_ok
        results.append({"case_id": case["case_id"], "case_passed": ok})
        if not ok:
            all_passed = False
    return results, all_passed
