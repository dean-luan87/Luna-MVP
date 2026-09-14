#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RealVideo OCRRequest Gated Submission v0."""

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
        "summary": root / "realvideo_ocr_request_gated_submission_summary.json",
        "plan": root / "realvideo_ocr_request_submission_plan.json",
        "rejected": root / "realvideo_ocr_request_rejected_roi_guard_report.json",
        "provider": root / "realvideo_ocr_request_provider_gate_report.json",
        "matrix": root / "realvideo_ocr_request_submission_result_matrix.json",
        "collection": root / "realvideo_ocr_request_submission_collection.json",
        "chain": root / "realvideo_ocr_request_submission_source_chain_report.json",
        "case_mapping": root / "realvideo_ocr_request_submission_case_mapping_report.json",
        "metrics": root / "realvideo_ocr_request_submission_metrics_candidate_report.json",
        "benchmark": root / "realvideo_ocr_request_submission_benchmark_link_report.json",
        "health": root / "realvideo_ocr_request_submission_system_health_link_report.json",
        "boundary": root / "realvideo_ocr_request_submission_no_write_boundary_report.json",
        "sim": root / "realvideo_ocr_request_submission_simulation_context_report.json",
        "non_claims": root / "realvideo_ocr_request_submission_non_claims_report.json",
        "followups": root / "realvideo_ocr_request_submission_open_followups.json",
        "audit": root / "realvideo_ocr_request_submission_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "realvideo_ocr_request_submission_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    plan = _read_json(paths["plan"])
    rejected = _read_json(paths["rejected"])
    provider = _read_json(paths["provider"])
    matrix = _read_json(paths["matrix"])
    collection = _read_json(paths["collection"])
    chain = _read_json(paths["chain"])
    case_mapping = _read_json(paths["case_mapping"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    verdict_hint = str(summary.get("phase_verdict_hint") or "").upper()
    provider_unavailable = summary.get("provider_unavailable") is True

    if summary.get("submission_scope") != "gated_ocr_request_submission_only":
        blockers.append("submission_scope")
    if summary.get("based_on_realvideo_roi_to_ocr_reference") is not True:
        blockers.append("based_on_roi_ref")
    if summary.get("ocr_request_reference_count") != 10:
        blockers.append("ocr_request_reference_count")
    if summary.get("selected_submission_count") != 10:
        blockers.append("selected_submission_count")
    if summary.get("non_text_roi_submission_count") != 0:
        blockers.append("non_text_roi_submission_count")
    if summary.get("paddleocr_invoked") is not False:
        blockers.append("paddleocr_invoked")
    if summary.get("direct_provider_bypass") is not False:
        blockers.append("direct_provider_bypass")
    if summary.get("fusion_invoked") is not False:
        blockers.append("fusion_invoked")
    if summary.get("scene_delta_candidate_generated") is not False:
        blockers.append("scene_delta")

    if verdict_hint not in ("GO", "CONDITIONAL_GO"):
        blockers.append("phase_verdict_hint")
    elif verdict_hint == "GO":
        if summary.get("submitted_count") != 10 or summary.get("success_count") != 10:
            blockers.append("go_requires_10_success")
    elif provider_unavailable:
        if audit.get("mock_text_substitution") is True:
            blockers.append("mock_on_conditional")
    elif summary.get("success_count") != 10:
        blockers.append("conditional_requires_provider_unavailable_or_success")

    plan_rows = plan.get("rows") if isinstance(plan.get("rows"), list) else []
    if len(plan_rows) != 10:
        blockers.append("plan_row_count")
    for row in plan_rows:
        if isinstance(row, dict):
            if row.get("roi_type") != "upper_sign_roi":
                blockers.append(f"plan_roi_type:{row.get('submission_plan_id')}")
            if row.get("selected_for_submission") is not True:
                blockers.append("plan_not_selected")

    if rejected.get("rejected_roi_count") != 40:
        blockers.append("rejected_roi_count")
    if rejected.get("full_frame_ocr_invoked") is not False:
        blockers.append("full_frame_ocr")

    if provider.get("ocr_mainline_bridge_required") is not True:
        blockers.append("bridge_required")
    if provider.get("paddleocr_allowed") is not False:
        blockers.append("paddleocr_allowed")
    if provider.get("fallback_to_mock_text_allowed") is not False:
        blockers.append("mock_allowed")

    mrows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    for row in mrows:
        if not isinstance(row, dict):
            continue
        tj = str(row.get("text_joined") or "")
        if "MOCK_TEXT" in tj:
            blockers.append("mock_text_in_matrix")
        if row.get("fact_status") != "not_fact":
            blockers.append("matrix_fact_status")
        if row.get("write_allowed") is not False:
            blockers.append("matrix_write_allowed")
        if row.get("paddleocr_invoked") is not False:
            blockers.append("matrix_paddleocr")
        if row.get("direct_provider_bypass") is not False:
            blockers.append("matrix_bypass")

    if collection.get("fact_status") != "not_fact":
        blockers.append("collection_fact_status")

    traces = chain.get("submission_traces") if isinstance(chain.get("submission_traces"), list) else []
    if len(traces) < 10 and verdict_hint == "GO":
        blockers.append("submission_traces_count")

    cmrows = case_mapping.get("rows") if isinstance(case_mapping.get("rows"), list) else []
    facility_ok = any(
        isinstance(r, dict) and r.get("requires_future_facility_specific_video") is True for r in cmrows
    )
    dup_ok = any(
        isinstance(r, dict) and r.get("requires_multi_frame_reference_later") is True for r in cmrows
    )
    if not facility_ok:
        blockers.append("facility_deferred")
    if not dup_ok:
        blockers.append("duplicate_conflict_later")

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

    if non_claims.get("not_realvideo_ocr_generalization_complete") is not True:
        blockers.append("not_generalization")
    if non_claims.get("not_benchmark") is not True:
        blockers.append("not_benchmark")

    items = followups.get("items") if isinstance(followups.get("items"), list) else []
    if len(items) < 8:
        blockers.append("followups_count")

    if audit.get("mock_text_substitution") is not False:
        blockers.append("audit_mock")
    if audit.get("paddleocr_invoked") is not False:
        blockers.append("audit_paddleocr")
    if audit.get("fusion_invoked") is not False:
        blockers.append("audit_fusion")
    if audit.get("midplatform_fact_written") is not False:
        blockers.append("audit_midplatform")
    if audit.get("world_model_written") is not False:
        blockers.append("audit_world_model")
    if audit.get("runtime_routing_changed") is not False:
        blockers.append("audit_routing")

    verdict = "GO" if not blockers else "NO_GO"

    report = {
        "schema_version": "realvideo_ocr_request_submission_verifier_report_v0",
        "verdict": verdict,
        "phase_verdict_hint": verdict_hint,
        "blockers": blockers,
        "checks_passed": 59 - len(blockers) if verdict == "GO" else max(0, 59 - len(blockers)),
        "smoke_root": str(root),
    }
    _write_json(root / "realvideo_ocr_request_submission_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers, "phase_verdict_hint": verdict_hint}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
