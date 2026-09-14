#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RealVideo OCR Reference Update v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


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
        "summary": root / "realvideo_ocr_reference_update_summary.json",
        "candidate": root / "realvideo_ocr_updated_reference_candidate.json",
        "alignment": root / "realvideo_ocr_reference_update_alignment_matrix.json",
        "rejected": root / "realvideo_ocr_reference_update_rejected_roi_preservation_report.json",
        "empty_guard": root / "realvideo_ocr_reference_update_empty_text_guard_report.json",
        "case_mapping": root / "realvideo_ocr_reference_update_case_mapping_report.json",
        "chain": root / "realvideo_ocr_reference_update_source_chain_report.json",
        "metrics": root / "realvideo_ocr_reference_update_metrics_candidate_report.json",
        "benchmark": root / "realvideo_ocr_reference_update_benchmark_link_report.json",
        "health": root / "realvideo_ocr_reference_update_system_health_link_report.json",
        "boundary": root / "realvideo_ocr_reference_update_no_write_boundary_report.json",
        "sim": root / "realvideo_ocr_reference_update_simulation_context_report.json",
        "non_claims": root / "realvideo_ocr_reference_update_non_claims_report.json",
        "followups": root / "realvideo_ocr_reference_update_open_followups.json",
        "audit": root / "realvideo_ocr_reference_update_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    followups_path = root / "realvideo_ocr_reference_update_open_followups.json"
    if not followups_path.is_file():
        blockers.append("missing:followups")

    if blockers:
        _write_json(
            root / "realvideo_ocr_reference_update_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    candidate = _read_json(paths["candidate"])
    alignment = _read_json(paths["alignment"])
    rejected = _read_json(paths["rejected"])
    empty_guard = _read_json(paths["empty_guard"])
    case_mapping = _read_json(paths["case_mapping"])
    chain = _read_json(paths["chain"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(followups_path)
    audit = _read_json(paths["audit"])

    if summary.get("reference_scope") != "reference_only_update":
        blockers.append("reference_scope")
    if summary.get("based_on_roi_to_ocr_reference") is not True:
        blockers.append("based_on_roi")
    if summary.get("based_on_gated_submission") is not True:
        blockers.append("based_on_gated")
    if summary.get("based_on_readonly_consumer") is not True:
        blockers.append("based_on_consumer")
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
    if summary.get("ocr_reinvoked") is not False:
        blockers.append("ocr_reinvoked")
    if summary.get("rapidocr_reinvoked") is not False:
        blockers.append("rapidocr_reinvoked")
    if summary.get("fusion_invoked") is not False:
        blockers.append("fusion_invoked")

    frame_refs = candidate.get("frame_sample_refs") or []
    roi_refs = candidate.get("roi_reference_refs") or []
    ocr_req_refs = candidate.get("ocr_request_refs") or []
    ocr_sub_refs = candidate.get("ocr_submission_refs") or []
    ocr_ev_refs = candidate.get("ocr_evidence_refs") or []
    if len(frame_refs) < 10:
        blockers.append("frame_sample_refs")
    if len(roi_refs) != 50:
        blockers.append("roi_reference_refs")
    if len(ocr_req_refs) != 10:
        blockers.append("ocr_request_refs")
    if len(ocr_sub_refs) != 10:
        blockers.append("ocr_submission_refs")
    if len(ocr_ev_refs) != 10:
        blockers.append("ocr_evidence_refs")

    etg = candidate.get("empty_text_guard") if isinstance(candidate.get("empty_text_guard"), dict) else {}
    if etg.get("empty_text_is_not_no_text_fact") is not True:
        blockers.append("empty_text_is_not_no_text_fact")

    align_rows = alignment.get("rows") or []
    if len(align_rows) != 10:
        blockers.append("alignment_row_count")
    for row in align_rows:
        if row.get("roi_type") != "upper_sign_roi":
            blockers.append("roi_type_not_upper_sign")
            break
        if row.get("alignment_status") != "aligned_by_ocr_request_candidate_id":
            blockers.append("alignment_status")
            break

    if rejected.get("rejected_roi_count") != 40:
        blockers.append("rejected_roi_count")
    if rejected.get("rejected_roi_evidence_generated") is not False:
        blockers.append("rejected_roi_evidence_generated")

    if empty_guard.get("empty_text_is_valid_ocr_result") is not True:
        blockers.append("empty_text_valid")
    if empty_guard.get("no_text_fact_written") is not False:
        blockers.append("no_text_fact_written")

    case_rows = case_mapping.get("rows") or []
    if len(case_rows) != 16:
        blockers.append("case_count")
    facility_ok = any(r.get("requires_future_facility_specific_video") for r in case_rows)
    multi_later_ok = any(r.get("requires_multi_frame_reference_later") for r in case_rows)
    if not facility_ok:
        blockers.append("facility_deferred")
    if not multi_later_ok:
        blockers.append("duplicate_conflict_later")

    chain_rows = chain.get("evidence_chain_rows") or []
    if len(chain_rows) != 10:
        blockers.append("evidence_chain_rows")
    for cr in chain_rows:
        sc = cr.get("source_chain") if isinstance(cr.get("source_chain"), list) else []
        if len(sc) < 6:
            blockers.append("incomplete_source_chain")
            break

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
        "schema_version": "realvideo_ocr_reference_update_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 62 - len(blockers),
        "smoke_root": str(root),
    }
    _write_json(root / "realvideo_ocr_reference_update_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
