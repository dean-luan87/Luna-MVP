#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RealVideo OCR Reference Closure v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List

CORE_PHASE_KEYS = (
    "realvideo_case_registry",
    "realvideo_frame_sample",
    "realvideo_roi_to_ocr_reference",
    "realvideo_ocr_request_gated_submission",
    "realvideo_ocr_evidence_readonly_consumer",
    "realvideo_ocr_reference_update",
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
        "summary": root / "realvideo_ocr_reference_closure_summary.json",
        "phase_matrix": root / "realvideo_ocr_reference_closure_phase_matrix.json",
        "lineage": root / "realvideo_ocr_reference_lineage_closure_report.json",
        "alignment": root / "realvideo_ocr_reference_alignment_closure_report.json",
        "rejected": root / "realvideo_ocr_reference_rejected_roi_closure_report.json",
        "empty": root / "realvideo_ocr_reference_empty_text_closure_report.json",
        "case_mapping": root / "realvideo_ocr_reference_case_mapping_closure_report.json",
        "provider": root / "realvideo_ocr_reference_provider_closure_report.json",
        "metrics": root / "realvideo_ocr_reference_metrics_closure_candidate_report.json",
        "benchmark": root / "realvideo_ocr_reference_closure_benchmark_link_report.json",
        "health": root / "realvideo_ocr_reference_closure_system_health_link_report.json",
        "boundary": root / "realvideo_ocr_reference_closure_no_write_boundary_report.json",
        "sim": root / "realvideo_ocr_reference_closure_simulation_context_report.json",
        "non_claims": root / "realvideo_ocr_reference_closure_non_claims_report.json",
        "followups": root / "realvideo_ocr_reference_closure_open_followups.json",
        "audit": root / "realvideo_ocr_reference_closure_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "realvideo_ocr_reference_closure_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    phase_matrix = _read_json(paths["phase_matrix"])
    lineage = _read_json(paths["lineage"])
    alignment = _read_json(paths["alignment"])
    rejected = _read_json(paths["rejected"])
    empty = _read_json(paths["empty"])
    case_mapping = _read_json(paths["case_mapping"])
    provider = _read_json(paths["provider"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("closure_scope") != "reference_chain_closure_only":
        blockers.append("closure_scope")
    if summary.get("realvideo_ocr_reference_status") != "closed_for_reference_evaluation":
        blockers.append("reference_status")
    if summary.get("based_on_gated_submission") is not True:
        blockers.append("based_on_gated")
    if summary.get("based_on_readonly_consumer") is not True:
        blockers.append("based_on_consumer")
    if summary.get("based_on_reference_update") is not True:
        blockers.append("based_on_update")
    if summary.get("case_count") != 16:
        blockers.append("case_count")
    if summary.get("frame_sample_count") != 10:
        blockers.append("frame_sample_count")
    if summary.get("roi_reference_count") != 50:
        blockers.append("roi_reference_count")
    if summary.get("ocr_request_reference_count") != 10:
        blockers.append("ocr_request_count")
    if summary.get("ocr_submission_ref_count") != 10:
        blockers.append("ocr_submission_count")
    if summary.get("ocr_evidence_ref_count") != 10:
        blockers.append("ocr_evidence_count")
    if summary.get("aligned_ocr_evidence_count") != 10:
        blockers.append("aligned_count")
    if summary.get("empty_text_count") != 10:
        blockers.append("empty_text_count")
    if summary.get("non_empty_text_count") != 0:
        blockers.append("non_empty_text_count")
    if summary.get("rejected_roi_count") != 40:
        blockers.append("rejected_roi_count")
    if summary.get("semantic_join_invoked") is not False:
        blockers.append("semantic_join")
    if summary.get("fusion_invoked") is not False:
        blockers.append("fusion")
    if summary.get("scene_delta_candidate_generated") is not False:
        blockers.append("scene_delta")

    core_rows = {
        r.get("phase_key"): r
        for r in (phase_matrix.get("rows") or [])
        if isinstance(r, dict) and r.get("core_phase")
    }
    for key in CORE_PHASE_KEYS:
        row = core_rows.get(key)
        if not row:
            blockers.append(f"missing_core_phase:{key}")
            continue
        if row.get("source_status") != "ok":
            blockers.append(f"core_source_status:{key}")
        if row.get("blockers") != []:
            blockers.append(f"core_blockers:{key}")
        if row.get("routing_changed") is not False:
            blockers.append(f"core_routing:{key}")

    if lineage.get("evidence_lineage_count") != 10:
        blockers.append("evidence_lineage_count")
    for row in lineage.get("evidence_lineage_rows") or []:
        if not isinstance(row, dict):
            continue
        steps = row.get("source_chain_steps") if isinstance(row.get("source_chain_steps"), list) else []
        if len(steps) < 7:
            blockers.append("incomplete_source_chain")
            break

    if alignment.get("all_ocr_requests_aligned") is not True:
        blockers.append("all_ocr_requests_aligned")
    if alignment.get("accuracy_computed") is not False:
        blockers.append("accuracy_computed")
    if alignment.get("empty_text_not_no_text_fact") is not True:
        blockers.append("empty_text_not_no_text_fact")

    if rejected.get("rejected_roi_evidence_generated") is not False:
        blockers.append("rejected_roi_evidence")
    if empty.get("empty_text_is_valid_ocr_result") is not True:
        blockers.append("empty_text_valid")
    if empty.get("no_text_fact_written") is not False:
        blockers.append("no_text_fact_written")

    case_rows = case_mapping.get("rows") or []
    if len(case_rows) != 16:
        blockers.append("case_mapping_count")
    facility_ok = any(r.get("closure_status") == "deferred_requires_future_facility_specific_video" for r in case_rows)
    multi_ok = any(r.get("closure_status") == "deferred_requires_multi_frame_reference_later" for r in case_rows)
    if not facility_ok:
        blockers.append("facility_deferred")
    if not multi_ok:
        blockers.append("duplicate_conflict_later")
    for cr in case_rows:
        if cr.get("fact_complete") is True or cr.get("navigation_ready") is True:
            blockers.append("case_fact_or_nav")
            break

    if provider.get("rapidocr_invoked_upstream") is not True:
        blockers.append("rapidocr_upstream")
    if provider.get("rapidocr_reinvoked_in_this_phase") is not False:
        blockers.append("rapidocr_reinvoked")

    if metrics.get("ocr_accuracy_computed") is not False:
        blockers.append("ocr_accuracy")
    if metrics.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_score")

    if benchmark.get("current_phase_updates_benchmark_values") is not False:
        blockers.append("benchmark_update")

    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("health_runtime")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    if boundary.get("violations") != []:
        blockers.append("violations")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("sim_profile")

    if non_claims.get("empty_text_not_means_no_text") is not True:
        blockers.append("non_claims_empty_text")
    if non_claims.get("not_benchmark") is not True:
        blockers.append("non_claims_benchmark")

    if not (followups.get("items") or []):
        blockers.append("followups_empty")

    audit_checks = [
        ("ocr_reinvoked", False),
        ("rapidocr_reinvoked", False),
        ("fusion_invoked", False),
        ("scene_delta_candidate_generated", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("runtime_routing_changed", False),
    ]
    for key, expected in audit_checks:
        if audit.get(key) != expected:
            blockers.append(f"audit:{key}")

    if blockers:
        verdict = "NO_GO"
    elif summary.get("phase_verdict_hint") == "CONDITIONAL_GO":
        verdict = "CONDITIONAL_GO"
    else:
        verdict = str(summary.get("phase_verdict_hint") or "GO")

    report = {
        "schema_version": "realvideo_ocr_reference_closure_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 67 - len(blockers),
        "smoke_root": str(root),
    }
    _write_json(root / "realvideo_ocr_reference_closure_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
