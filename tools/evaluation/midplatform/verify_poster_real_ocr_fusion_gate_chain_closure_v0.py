#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Real OCR Fusion Gate Chain Closure v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


CORE_PHASE_KEYS = frozenset(
    {
        "fusion_candidate_dryrun",
        "fusion_review_queue",
        "fusion_ttl_gate_dryrun",
        "fusion_policy_gate_dryrun",
    }
)
REQUIRED_BLOCKING_REASONS = frozenset(
    {
        "review_decision_missing",
        "ttl_policy_required",
        "source_validation_required",
        "user_visible_uncertainty_required",
    }
)


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
        "summary": root / "poster_real_ocr_fusion_gate_chain_closure_summary.json",
        "phase_matrix": root / "poster_real_ocr_fusion_gate_chain_phase_matrix.json",
        "lineage": root / "poster_real_ocr_fusion_gate_chain_lineage_report.json",
        "decision": root / "poster_real_ocr_fusion_gate_chain_decision_matrix.json",
        "blocking": root / "poster_real_ocr_fusion_gate_chain_blocking_reasons_rollup.json",
        "review_approval": root / "poster_real_ocr_fusion_gate_chain_review_approval_closure_report.json",
        "ttl": root / "poster_real_ocr_fusion_gate_chain_ttl_closure_report.json",
        "policy": root / "poster_real_ocr_fusion_gate_chain_policy_closure_report.json",
        "commercial": root / "poster_real_ocr_fusion_gate_chain_commercial_temporal_closure_report.json",
        "visual": root / "poster_real_ocr_fusion_gate_chain_visual_symbol_boundary_report.json",
        "scene_delta": root / "poster_real_ocr_fusion_gate_chain_scene_delta_non_eligibility_report.json",
        "metrics": root / "poster_real_ocr_fusion_gate_chain_metrics_closure_candidate_report.json",
        "benchmark": root / "poster_real_ocr_fusion_gate_chain_benchmark_link_report.json",
        "health": root / "poster_real_ocr_fusion_gate_chain_system_health_link_report.json",
        "boundary": root / "poster_real_ocr_fusion_gate_chain_no_write_boundary_report.json",
        "sim": root / "poster_real_ocr_fusion_gate_chain_simulation_context_report.json",
        "non_claims": root / "poster_real_ocr_fusion_gate_chain_non_claims_report.json",
        "followups": root / "poster_real_ocr_fusion_gate_chain_open_followups.json",
        "audit": root / "poster_real_ocr_fusion_gate_chain_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_real_ocr_fusion_gate_chain_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    phase_matrix = _read_json(paths["phase_matrix"])
    lineage = _read_json(paths["lineage"])
    decision = _read_json(paths["decision"])
    blocking = _read_json(paths["blocking"])
    review_approval = _read_json(paths["review_approval"])
    ttl = _read_json(paths["ttl"])
    policy = _read_json(paths["policy"])
    commercial = _read_json(paths["commercial"])
    visual = _read_json(paths["visual"])
    scene_delta = _read_json(paths["scene_delta"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("closure_scope") != "fusion_gate_chain_closure_only":
        blockers.append("closure_scope")
    if summary.get("gate_chain_status") != "closed_for_gate_chain_evaluation":
        blockers.append("gate_chain_status")
    if summary.get("fusion_candidate_count") != 1:
        blockers.append("fusion_candidate_count")
    if summary.get("queue_item_count") != 1:
        blockers.append("queue_item_count")
    if summary.get("ttl_gate_evaluated_count") != 1:
        blockers.append("ttl_gate_evaluated_count")
    if summary.get("policy_gate_evaluated_count") != 1:
        blockers.append("policy_gate_evaluated_count")
    if summary.get("approval_granted_count") != 0:
        blockers.append("approval_granted_count")
    if summary.get("auto_approve_invoked") is not False:
        blockers.append("auto_approve_invoked")
    if summary.get("fusion_committed") is not False:
        blockers.append("fusion_committed")
    if summary.get("scene_delta_candidate_generated") is not False:
        blockers.append("scene_delta")

    core_seen = set()
    for row in phase_matrix.get("rows") or []:
        if not isinstance(row, dict):
            continue
        key = row.get("phase_key")
        if key in CORE_PHASE_KEYS:
            core_seen.add(key)
            if row.get("source_status") != "ok":
                blockers.append(f"core_source_status:{key}")
            if row.get("blockers") != []:
                blockers.append(f"core_blockers:{key}")
            if row.get("write_status") != "no_write":
                blockers.append(f"core_write_status:{key}")
            if row.get("routing_changed") is not False:
                blockers.append(f"core_routing:{key}")
    if core_seen != CORE_PHASE_KEYS:
        blockers.append("core_phase_keys_incomplete")

    trace = lineage.get("gate_item_trace") if isinstance(lineage.get("gate_item_trace"), dict) else {}
    for field in ("fusion_candidate_id", "queue_item_id", "ttl_gate_candidate_id", "policy_gate_candidate_id"):
        if not trace.get(field):
            blockers.append(f"missing_trace:{field}")
    if not trace.get("real_ocr_evidence_refs"):
        blockers.append("missing_ocr_refs")
    if len(trace.get("ttl_region_refs") or []) < 2:
        blockers.append("ttl_region_refs")

    drows = decision.get("rows") if isinstance(decision.get("rows"), list) else []
    if not drows:
        blockers.append("decision_rows_empty")
    for row in drows:
        if isinstance(row, dict):
            if row.get("final_gate_chain_decision") != "hold_for_review":
                blockers.append("final_gate_chain_decision")
            if row.get("ttl_gate_decision") != "hold_for_review":
                blockers.append("ttl_gate_decision")
            if row.get("policy_gate_decision") != "hold_for_review":
                blockers.append("policy_gate_decision")
            if row.get("approval_status") != "not_approved":
                blockers.append("approval_status")

    reason_codes = {r.get("reason_code") for r in (blocking.get("rows") or []) if isinstance(r, dict)}
    for req in REQUIRED_BLOCKING_REASONS:
        if req not in reason_codes:
            blockers.append(f"missing_blocking_reason:{req}")

    if review_approval.get("approval_granted") is not False:
        blockers.append("approval_granted")
    if review_approval.get("review_decision_available") is not False:
        blockers.append("review_decision_available")

    if ttl.get("ttl_gate_passed") is not False:
        blockers.append("ttl_gate_passed")
    if ttl.get("ttl_required_region_count") != 2:
        blockers.append("ttl_required_region_count")

    if policy.get("policy_gate_passed") is not False:
        blockers.append("policy_gate_passed")
    if policy.get("scene_delta_candidate_allowed") is not False:
        blockers.append("policy_scene_delta_allowed")
    if (policy.get("blocking_requirement_count") or 0) < 4:
        blockers.append("blocking_requirement_count")

    if commercial.get("commercial_claim_status") != "candidate_only":
        blockers.append("commercial_claim_status")
    if commercial.get("temporal_claim_status") != "candidate_only":
        blockers.append("temporal_claim_status")

    if visual.get("visual_context_consumed_as_text") is not False:
        blockers.append("visual_context_consumed_as_text")
    if visual.get("brand_identity_confirmed") is not False:
        blockers.append("brand_identity_confirmed")
    if visual.get("qr_decoded") is not False:
        blockers.append("qr_decoded")

    if scene_delta.get("eligibility_status") != "not_eligible_after_gate_chain":
        blockers.append("eligibility_status")
    if scene_delta.get("scene_delta_candidate_allowed") is not False:
        blockers.append("scene_delta_allowed")
    if scene_delta.get("scene_delta_candidate_generated") is not False:
        blockers.append("scene_delta_generated")

    if metrics.get("final_hold_for_review_count") != 1:
        blockers.append("final_hold_for_review_count")
    if benchmark.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_score_generated")
    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("provider_health_runtime_checked")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    violations = boundary.get("violations") if isinstance(boundary.get("violations"), list) else None
    if violations != []:
        blockers.append("violations")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("simulation_profile_id")

    if non_claims.get("not_scene_delta_candidate_ready") is not True:
        blockers.append("not_scene_delta_ready")
    if non_claims.get("not_world_model_write_readiness") is not True:
        blockers.append("not_world_model_readiness")

    items = followups.get("items") if isinstance(followups.get("items"), list) else []
    if len(items) < 8:
        blockers.append("followups_count")

    if audit.get("auto_approve_invoked") is not False:
        blockers.append("audit_auto_approve")
    if audit.get("fusion_committed") is not False:
        blockers.append("audit_fusion_committed")
    if audit.get("scene_delta_candidate_generated") is not False:
        blockers.append("audit_scene_delta")
    if audit.get("midplatform_fact_written") is not False:
        blockers.append("audit_midplatform")
    if audit.get("scene_delta_written") is not False:
        blockers.append("audit_scene_delta_written")
    if audit.get("world_model_written") is not False:
        blockers.append("audit_world_model")
    if audit.get("navigation_decision_invoked") is not False:
        blockers.append("audit_navigation")
    if audit.get("runtime_routing_changed") is not False:
        blockers.append("audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "schema_version": "poster_real_ocr_fusion_gate_chain_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 70 - len(blockers) if verdict == "GO" else max(0, 70 - len(blockers)),
        "smoke_root": str(root),
    }
    _write_json(root / "poster_real_ocr_fusion_gate_chain_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
