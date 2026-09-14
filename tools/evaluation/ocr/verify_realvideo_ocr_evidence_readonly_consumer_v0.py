#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RealVideo OCR Evidence ReadOnly Consumer v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
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
        "summary": root / "realvideo_ocr_evidence_readonly_consumer_summary.json",
        "by_candidate": root / "realvideo_ocr_evidence_by_candidate_index.json",
        "by_frame": root / "realvideo_ocr_evidence_by_frame_index.json",
        "by_roi": root / "realvideo_ocr_evidence_by_roi_index.json",
        "by_case": root / "realvideo_ocr_evidence_by_case_index.json",
        "empty_guard": root / "realvideo_ocr_empty_text_interpretation_guard_report.json",
        "rejected": root / "realvideo_ocr_readonly_rejected_roi_carryover_report.json",
        "provider": root / "realvideo_ocr_readonly_provider_summary_report.json",
        "chain": root / "realvideo_ocr_readonly_source_chain_report.json",
        "metrics": root / "realvideo_ocr_readonly_metrics_candidate_report.json",
        "benchmark": root / "realvideo_ocr_readonly_benchmark_link_report.json",
        "health": root / "realvideo_ocr_readonly_system_health_link_report.json",
        "boundary": root / "realvideo_ocr_readonly_no_write_boundary_report.json",
        "sim": root / "realvideo_ocr_readonly_simulation_context_report.json",
        "non_claims": root / "realvideo_ocr_readonly_non_claims_report.json",
        "followups": root / "realvideo_ocr_readonly_open_followups.json",
        "audit": root / "realvideo_ocr_readonly_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "realvideo_ocr_readonly_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    by_candidate = _read_json(paths["by_candidate"])
    by_frame = _read_json(paths["by_frame"])
    by_roi = _read_json(paths["by_roi"])
    by_case = _read_json(paths["by_case"])
    empty_guard = _read_json(paths["empty_guard"])
    rejected = _read_json(paths["rejected"])
    provider = _read_json(paths["provider"])
    chain = _read_json(paths["chain"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("consumer_scope") != "readonly_consumer":
        blockers.append("consumer_scope")
    if summary.get("based_on_gated_submission") is not True:
        blockers.append("based_on_gated_submission")
    if summary.get("submission_count_observed") != 10:
        blockers.append("submission_count_observed")
    if summary.get("success_count_observed") != 10:
        blockers.append("success_count_observed")
    if summary.get("evidence_count_observed") != 10:
        blockers.append("evidence_count_observed")
    if summary.get("empty_text_count") != 10:
        blockers.append("empty_text_count")
    if summary.get("non_empty_text_count") != 0:
        blockers.append("non_empty_text_count")
    if summary.get("ocr_reinvoked") is not False:
        blockers.append("ocr_reinvoked")
    if summary.get("rapidocr_reinvoked") is not False:
        blockers.append("rapidocr_reinvoked")
    if summary.get("paddleocr_invoked") is not False:
        blockers.append("paddleocr_invoked")
    if summary.get("fusion_invoked") is not False:
        blockers.append("fusion_invoked")

    entries = by_candidate.get("entries") if isinstance(by_candidate.get("entries"), list) else []
    if by_candidate.get("index_count") != 10:
        blockers.append("index_count")
    if len(entries) != 10:
        blockers.append("entries_len")
    for ent in entries:
        if isinstance(ent, dict):
            if ent.get("roi_type") != "upper_sign_roi":
                blockers.append(f"roi_type:{ent.get('ocr_request_candidate_id')}")
            if ent.get("fact_status") != "not_fact":
                blockers.append("candidate_fact_status")

    frames = by_frame.get("frames") if isinstance(by_frame.get("frames"), list) else []
    if by_frame.get("frame_count") != 10:
        blockers.append("frame_count")
    for fr in frames:
        if isinstance(fr, dict) and len(fr.get("evidence_refs") or []) != 1:
            blockers.append(f"frame_evidence_count:{fr.get('source_frame_id')}")

    rois = by_roi.get("rois") if isinstance(by_roi.get("rois"), list) else []
    if by_roi.get("roi_count") != 10:
        blockers.append("roi_count")
    for r in rois:
        if isinstance(r, dict) and r.get("roi_type") != "upper_sign_roi":
            blockers.append("roi_index_type")

    cases = by_case.get("cases") if isinstance(by_case.get("cases"), list) else []
    facility_deferred = any(
        isinstance(c, dict) and c.get("requires_future_facility_specific_video") is True for c in cases
    )
    dup_later = any(
        isinstance(c, dict) and c.get("requires_multi_frame_reference_later") is True for c in cases
    )
    if not facility_deferred:
        blockers.append("facility_deferred")
    if not dup_later:
        blockers.append("duplicate_conflict_later")

    if empty_guard.get("empty_text_is_valid_ocr_result") is not True:
        blockers.append("empty_text_is_valid_ocr_result")
    if empty_guard.get("empty_text_is_not_failure") is not True:
        blockers.append("empty_text_is_not_failure")
    if empty_guard.get("empty_text_is_not_no_text_fact") is not True:
        blockers.append("empty_text_is_not_no_text_fact")

    if rejected.get("rejected_roi_count") != 40:
        blockers.append("rejected_roi_count")
    if rejected.get("non_text_roi_submission_count") != 0:
        blockers.append("non_text_roi_submission_count")
    if rejected.get("full_frame_ocr_invoked") is not False:
        blockers.append("full_frame_ocr_invoked")

    if provider.get("rapidocr_invoked_upstream") is not True:
        blockers.append("rapidocr_invoked_upstream")
    if provider.get("rapidocr_reinvoked_in_this_phase") is not False:
        blockers.append("rapidocr_reinvoked_in_phase")
    if provider.get("mock_text_substitution") is not False:
        blockers.append("mock_text_substitution")

    traces = chain.get("evidence_traces") if isinstance(chain.get("evidence_traces"), list) else []
    if len(traces) < 10:
        blockers.append("evidence_traces")
    for t in traces:
        if isinstance(t, dict) and not t.get("bridge_pack_ref"):
            blockers.append(f"missing_chain:{t.get('ocr_evidence_id')}")

    if metrics.get("ocr_accuracy_computed") is not False:
        blockers.append("ocr_accuracy_computed")
    if metrics.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_score_generated")
    if benchmark.get("current_phase_updates_benchmark_values") is not False:
        blockers.append("benchmark_updates")
    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("provider_health_runtime_checked")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    if boundary.get("violations") != []:
        blockers.append("violations")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("simulation_profile_id")

    if non_claims.get("empty_text_not_means_no_text") is not True:
        blockers.append("empty_text_not_means_no_text")
    if non_claims.get("not_benchmark") is not True:
        blockers.append("not_benchmark")

    items = followups.get("items") if isinstance(followups.get("items"), list) else []
    if len(items) < 8:
        blockers.append("followups_count")

    if audit.get("ocr_reinvoked") is not False:
        blockers.append("audit_ocr_reinvoked")
    if audit.get("rapidocr_reinvoked") is not False:
        blockers.append("audit_rapidocr")
    if audit.get("fusion_invoked") is not False:
        blockers.append("audit_fusion")
    if audit.get("scene_delta_candidate_generated") is not False:
        blockers.append("audit_scene_delta")
    if audit.get("midplatform_fact_written") is not False:
        blockers.append("audit_midplatform")
    if audit.get("world_model_written") is not False:
        blockers.append("audit_world_model")
    if audit.get("navigation_decision_invoked") is not False:
        blockers.append("audit_navigation")
    if audit.get("runtime_routing_changed") is not False:
        blockers.append("audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "schema_version": "realvideo_ocr_readonly_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 63 - len(blockers) if verdict == "GO" else max(0, 63 - len(blockers)),
        "smoke_root": str(root),
    }
    _write_json(root / "realvideo_ocr_readonly_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
