#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RealVideo OCR Text-Bearing Sample Planning v0."""

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
        "summary": root / "realvideo_ocr_text_bearing_sample_planning_summary.json",
        "diagnosis": root / "realvideo_ocr_text_bearing_prior_closure_diagnosis_report.json",
        "definition": root / "realvideo_ocr_text_bearing_sample_definition.json",
        "case_matrix": root / "realvideo_ocr_text_bearing_planned_case_matrix.json",
        "frame_sampling": root / "realvideo_ocr_text_bearing_frame_sampling_strategy_plan.json",
        "roi_selection": root / "realvideo_ocr_text_bearing_roi_selection_strategy_plan.json",
        "gt": root / "realvideo_ocr_text_bearing_ground_truth_requirement_plan.json",
        "quality": root / "realvideo_ocr_text_bearing_quality_risk_label_plan.json",
        "chain": root / "realvideo_ocr_text_bearing_future_execution_chain_plan.json",
        "metrics": root / "realvideo_ocr_text_bearing_metrics_binding_plan.json",
        "governance": root / "realvideo_ocr_text_bearing_governance_link_plan.json",
        "checklist": root / "realvideo_ocr_text_bearing_sample_acquisition_checklist.json",
        "benchmark": root / "realvideo_ocr_text_bearing_benchmark_link_report.json",
        "health": root / "realvideo_ocr_text_bearing_system_health_link_report.json",
        "boundary": root / "realvideo_ocr_text_bearing_no_write_boundary_report.json",
        "sim": root / "realvideo_ocr_text_bearing_simulation_context_report.json",
        "non_claims": root / "realvideo_ocr_text_bearing_non_claims_report.json",
        "followups": root / "realvideo_ocr_text_bearing_open_followups.json",
        "audit": root / "realvideo_ocr_text_bearing_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "realvideo_ocr_text_bearing_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    diagnosis = _read_json(paths["diagnosis"])
    definition = _read_json(paths["definition"])
    case_matrix = _read_json(paths["case_matrix"])
    frame_sampling = _read_json(paths["frame_sampling"])
    roi_selection = _read_json(paths["roi_selection"])
    gt = _read_json(paths["gt"])
    quality = _read_json(paths["quality"])
    chain = _read_json(paths["chain"])
    metrics = _read_json(paths["metrics"])
    governance = _read_json(paths["governance"])
    checklist = _read_json(paths["checklist"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("planning_scope") != "text_bearing_sample_planning_only":
        blockers.append("planning_scope")
    if summary.get("prior_realvideo_reference_verdict") != "CONDITIONAL_GO":
        blockers.append("prior_verdict")
    if summary.get("prior_empty_text_count") != 10:
        blockers.append("prior_empty_text_count")
    if summary.get("prior_non_empty_text_count") != 0:
        blockers.append("prior_non_empty_text_count")
    if summary.get("runtime_execution") is not False:
        blockers.append("runtime_execution")
    if summary.get("video_loaded") is not False:
        blockers.append("video_loaded")
    if summary.get("frame_sampled") is not False:
        blockers.append("frame_sampled")
    if summary.get("ocr_invoked") is not False:
        blockers.append("ocr_invoked")

    if diagnosis.get("limitation_type") != "sample_limitation_not_chain_failure":
        blockers.append("limitation_type")

    defs = definition.get("definitions") or []
    if len(defs) < 4:
        blockers.append("definition_count")

    rows = case_matrix.get("rows") or []
    if len(rows) < 12:
        blockers.append("case_matrix_count")

    facility_ok = any(r.get("semantic_first_governance_link") for r in rows if isinstance(r, dict))
    ttl_ok = any(r.get("ttl_risk") for r in rows if isinstance(r, dict))
    multi_ok = any(r.get("multi_frame_requirement") for r in rows if isinstance(r, dict))
    if not facility_ok:
        blockers.append("facility_governance")
    if not ttl_ok:
        blockers.append("ttl_risk")
    if not multi_ok:
        blockers.append("multi_frame")

    if frame_sampling.get("frame_sampling_enabled") is not False:
        blockers.append("frame_sampling_enabled")

    if roi_selection.get("full_frame_ocr_default") != "forbidden":
        blockers.append("full_frame_ocr")

    if gt.get("ground_truth_required") is not True:
        blockers.append("ground_truth_required")
    req_fields = gt.get("required_fields") or []
    if "text_ground_truth" not in req_fields:
        blockers.append("text_ground_truth_field")

    if not (quality.get("label_groups") or []):
        blockers.append("quality_labels")

    if chain.get("fusion_optional") is not True:
        blockers.append("fusion_optional")
    excluded = chain.get("excluded_from_default_chain") or []
    if not any("Scene" in str(x) for x in excluded):
        blockers.append("scene_delta_excluded")

    if metrics.get("t2_metrics_require_ground_truth") is not True:
        blockers.append("t2_gt")
    if metrics.get("current_phase_collects_metrics") is not False:
        blockers.append("collects_metrics")

    if governance.get("poster_governance_linked") is not True:
        blockers.append("poster_governance")
    if governance.get("public_facility_governance_linked") is not True:
        blockers.append("facility_governance_link")

    for item in checklist.get("items") or []:
        if item.get("satisfied_in_this_phase") is not False:
            blockers.append("checklist_satisfied")
            break

    if benchmark.get("current_phase_updates_benchmark_values") is not False:
        blockers.append("benchmark_update")

    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("health_runtime")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    if boundary.get("violations") != []:
        blockers.append("violations")
    if boundary.get("planning_only") is not True:
        blockers.append("planning_only")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("sim_profile")

    if non_claims.get("no_video_loaded") is not True:
        blockers.append("non_claims_video")
    if non_claims.get("no_ocr_execution") is not True:
        blockers.append("non_claims_ocr")
    if non_claims.get("not_benchmark") is not True:
        blockers.append("non_claims_benchmark")

    if not (followups.get("items") or []):
        blockers.append("followups")

    audit_checks = [
        ("video_loaded", False),
        ("frame_sampled", False),
        ("ocr_invoked", False),
        ("rapidocr_invoked", False),
        ("fusion_invoked", False),
        ("scene_delta_candidate_generated", False),
        ("midplatform_fact_written", False),
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
        "schema_version": "realvideo_ocr_text_bearing_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 62 - len(blockers),
        "smoke_root": str(root),
    }
    _write_json(root / "realvideo_ocr_text_bearing_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
