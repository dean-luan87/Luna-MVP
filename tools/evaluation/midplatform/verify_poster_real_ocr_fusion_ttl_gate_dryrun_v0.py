#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Real OCR Fusion TTL Gate DryRun v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


FORBIDDEN_ALLOWED = frozenset({"world_model_write", "auto_approve", "scene_delta_write", "navigation_decision"})


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
        "summary": root / "poster_real_ocr_fusion_ttl_gate_dryrun_summary.json",
        "candidate": root / "poster_real_ocr_fusion_ttl_gate_candidate.json",
        "region_matrix": root / "poster_real_ocr_fusion_ttl_region_evaluation_matrix.json",
        "risk": root / "poster_real_ocr_fusion_ttl_risk_classification_report.json",
        "policy": root / "poster_real_ocr_fusion_ttl_policy_requirement_report.json",
        "carryover": root / "poster_real_ocr_fusion_ttl_review_queue_carryover_report.json",
        "decision": root / "poster_real_ocr_fusion_ttl_gate_decision_matrix.json",
        "chain": root / "poster_real_ocr_fusion_ttl_source_chain_report.json",
        "metrics": root / "poster_real_ocr_fusion_ttl_metrics_candidate_report.json",
        "benchmark": root / "poster_real_ocr_fusion_ttl_benchmark_link_report.json",
        "health": root / "poster_real_ocr_fusion_ttl_system_health_link_report.json",
        "boundary": root / "poster_real_ocr_fusion_ttl_no_write_boundary_report.json",
        "sim": root / "poster_real_ocr_fusion_ttl_simulation_context_report.json",
        "non_claims": root / "poster_real_ocr_fusion_ttl_non_claims_report.json",
        "followups": root / "poster_real_ocr_fusion_ttl_open_followups.json",
        "audit": root / "poster_real_ocr_fusion_ttl_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_real_ocr_fusion_ttl_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    candidate = _read_json(paths["candidate"])
    region_matrix = _read_json(paths["region_matrix"])
    risk = _read_json(paths["risk"])
    policy = _read_json(paths["policy"])
    carryover = _read_json(paths["carryover"])
    decision = _read_json(paths["decision"])
    chain = _read_json(paths["chain"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("gate_scope") != "ttl_gate_dryrun_only":
        blockers.append("gate_scope")
    if summary.get("ttl_gate_evaluated") is not True:
        blockers.append("ttl_gate_evaluated")
    if summary.get("ttl_candidate_count") != 1:
        blockers.append("ttl_candidate_count")
    if summary.get("ttl_required_region_count") != 2:
        blockers.append("ttl_required_region_count")
    if summary.get("ttl_gate_passed_count") != 0:
        blockers.append("ttl_gate_passed_count")
    if summary.get("ttl_gate_hold_count") != 1:
        blockers.append("ttl_gate_hold_count")
    if summary.get("approval_granted_count") != 0:
        blockers.append("approval_granted_count")
    if summary.get("auto_approve_invoked") is not False:
        blockers.append("auto_approve_invoked")
    if summary.get("fusion_committed") is not False:
        blockers.append("fusion_committed")
    if summary.get("scene_delta_candidate_generated") is not False:
        blockers.append("scene_delta")

    if candidate.get("ttl_gate_status") != "evaluated_dryrun":
        blockers.append("ttl_gate_status")
    if candidate.get("ttl_gate_decision") != "hold_for_review":
        blockers.append("ttl_gate_decision")
    if candidate.get("ttl_gate_passed") is not False:
        blockers.append("ttl_gate_passed")
    if candidate.get("approval_status") != "not_approved":
        blockers.append("approval_status")
    if candidate.get("write_allowed") is not False:
        blockers.append("write_allowed")
    allowed = candidate.get("allowed_next_steps") if isinstance(candidate.get("allowed_next_steps"), list) else []
    for step in allowed:
        if str(step) in FORBIDDEN_ALLOWED or "world_model" in str(step):
            blockers.append(f"forbidden_allowed_step:{step}")

    region_ids = set()
    for row in region_matrix.get("rows") or []:
        if not isinstance(row, dict):
            continue
        region_ids.add(str(row.get("source_region_id") or row.get("region_type") or ""))
        if row.get("write_allowed") is not False:
            blockers.append(f"region_write_allowed:{row.get('source_region_id')}")
    if "price_or_promo_area" not in region_ids:
        blockers.append("missing_price_or_promo_area")
    if "time_location_area" not in region_ids:
        blockers.append("missing_time_location_area")

    if risk.get("commercial_text_may_expire") is not True:
        blockers.append("commercial_text_may_expire")
    if risk.get("temporal_text_requires_ttl") is not True:
        blockers.append("temporal_text_requires_ttl")

    reqs = policy.get("requirements") if isinstance(policy.get("requirements"), list) else []
    if not reqs:
        blockers.append("policy_requirements_empty")
    for req in reqs:
        if isinstance(req, dict):
            if req.get("required_before_write") is not True:
                blockers.append(f"required_before_write:{req.get('requirement_id')}")
            if req.get("satisfied_in_this_phase") is not False:
                blockers.append(f"satisfied_in_phase:{req.get('requirement_id')}")

    if carryover.get("approval_status_unchanged") is not True:
        blockers.append("approval_status_unchanged")
    if carryover.get("review_status_unchanged") is not True:
        blockers.append("review_status_unchanged")

    drows = decision.get("rows") if isinstance(decision.get("rows"), list) else []
    for row in drows:
        if isinstance(row, dict):
            if row.get("scene_delta_candidate_allowed") is not False:
                blockers.append("scene_delta_candidate_allowed")
            if row.get("world_model_write_allowed") is not False:
                blockers.append("world_model_write_allowed")

    trace = chain.get("ttl_region_evidence_trace") if isinstance(chain.get("ttl_region_evidence_trace"), list) else []
    if len(trace) < 2:
        blockers.append("ttl_region_evidence_trace")
    for t in trace:
        if isinstance(t, dict) and not t.get("real_ocr_evidence_ref"):
            blockers.append(f"missing_ocr_evidence:{t.get('source_region_id')}")

    if metrics.get("ttl_gate_hold_count") != 1:
        blockers.append("metrics_hold_count")
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

    if non_claims.get("not_ttl_approval") is not True:
        blockers.append("not_ttl_approval")
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
        "schema_version": "poster_real_ocr_fusion_ttl_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 60 - len(blockers) if verdict == "GO" else max(0, 60 - len(blockers)),
        "smoke_root": str(root),
    }
    _write_json(root / "poster_real_ocr_fusion_ttl_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
