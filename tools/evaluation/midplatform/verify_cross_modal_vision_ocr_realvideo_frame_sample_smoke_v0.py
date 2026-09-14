#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001 verifier."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame-sample-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.frame_sample_root).expanduser().resolve()
    vout = (
        Path(args.verifier_output_root).expanduser().resolve()
        if args.verifier_output_root.strip()
        else (root.parent / "cross_modal_vision_ocr_realvideo_frame_sample_verify_v0").resolve()
    )
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("cross_modal_vision_ocr_realvideo_frame_sample_summary.json")
    idx_p = req("cross_modal_vision_ocr_realvideo_frame_sample_index.json")
    qual_p = req("cross_modal_vision_ocr_realvideo_frame_quality_placeholder_matrix.json")
    cov_p = req("cross_modal_vision_ocr_realvideo_case_coverage_mapping.json")
    pf_p = req("cross_modal_vision_ocr_realvideo_poster_facility_candidate_mapping.json")
    met_p = req("cross_modal_vision_ocr_realvideo_frame_sample_metrics_binding_report.json")
    bnd_p = req("cross_modal_vision_ocr_realvideo_frame_sample_no_write_boundary_report.json")
    sim_p = req("cross_modal_vision_ocr_realvideo_frame_sample_simulation_context_report.json")
    nc_p = req("cross_modal_vision_ocr_realvideo_frame_sample_non_claims_report.json")
    aud_p = req("cross_modal_vision_ocr_realvideo_frame_sample_audit_report.json")

    if not blockers:
        sm = _read_json(sum_p)
        if sm.get("sample_scope") != "frame_sample_smoke_only":
            blockers.append("summary_sample_scope_wrong")
        for flag in (
            "based_on_realvideo_registry",
            "based_on_poster_track_b_closure",
            "based_on_metrics_collector",
            "based_on_simulation_lab",
        ):
            if sm.get(flag) is not True:
                blockers.append(f"summary_{flag}_not_true")
        for k, val in (
            ("real_camera_invoked", False),
            ("new_video_decoded", False),
            ("ocr_invoked", False),
            ("vision_provider_invoked", False),
        ):
            if sm.get(k) is not val:
                blockers.append(f"summary_{k}_wrong")

        idx = _read_json(idx_p)
        samples = idx.get("samples") if isinstance(idx.get("samples"), list) else []
        if len(samples) < 1:
            blockers.append("sample_count_lt_1")
        for s in samples:
            if not isinstance(s, dict):
                continue
            if s.get("eligible_for_recognition") is not False:
                blockers.append(f"eligible_for_recognition_not_false:{s.get('sample_id')}")
            if s.get("fact_status") != "not_fact":
                blockers.append(f"fact_status_not_not_fact:{s.get('sample_id')}")
            if s.get("write_allowed") is not False:
                blockers.append(f"write_allowed_not_false:{s.get('sample_id')}")
            chain = s.get("source_chain") or []
            if "realvideo_frame_sample_smoke_built" not in chain:
                blockers.append(f"missing_source_chain_marker:{s.get('sample_id')}")

        qual = _read_json(qual_p)
        for row in qual.get("rows") or []:
            if isinstance(row, dict) and row.get("quality_metrics_available") is not False:
                blockers.append("quality_metrics_available_not_false")
                break
        for row in qual.get("rows") or []:
            if isinstance(row, dict) and row.get("performance_claim_allowed") is not False:
                blockers.append("performance_claim_allowed_not_false")
                break

        cov = _read_json(cov_p)
        for row in cov.get("rows") or []:
            if isinstance(row, dict) and row.get("execution_status") != "sample_mapping_only":
                blockers.append(f"execution_status_not_sample_mapping_only:{row.get('case_id')}")

        pf = _read_json(pf_p)
        for k, val in (
            ("poster_track_b_closed", True),
            ("public_facility_governance_available", True),
            ("poster_like_detection_invoked", False),
            ("facility_detection_invoked", False),
        ):
            if pf.get(k) is not val:
                blockers.append(f"poster_facility_{k}_wrong")

        bnd = _read_json(bnd_p)
        if bnd.get("boundary_ok") is not True:
            blockers.append("boundary_ok_not_true")
        if bnd.get("violations"):
            blockers.append("boundary_violations_nonempty")

        sim = _read_json(sim_p)
        if sim.get("simulation_profile_id") != "developer_full":
            blockers.append("simulation_profile_id_not_developer_full")
        if sim.get("run_model") is not False:
            blockers.append("simulation_run_model_not_false")

        nc = _read_json(nc_p)
        if nc.get("no_realvideo_ocr_claim") is not True:
            blockers.append("non_claims_no_realvideo_ocr_not_true")
        if nc.get("no_benchmark_claim") is not True:
            blockers.append("non_claims_no_benchmark_not_true")

        audit = _read_json(aud_p)
        audit_checks = (
            ("ocr_request_generated", False),
            ("cross_modal_reference_generated", False),
            ("fusion_invoked", False),
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
            ("navigation_decision_invoked", False),
            ("runtime_routing_changed", False),
        )
        for k, val in audit_checks:
            if audit.get(k) is not val:
                blockers.append(f"audit_{k}_wrong")

    verdict = "NO_GO" if blockers else "GO"
    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_realvideo_frame_sample_verifier_report_v0",
        "phase": "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001",
        "verdict": verdict,
        "frame_sample_root": str(root),
        "verifier_output_root": str(vout),
        "blockers": sorted(set(blockers)),
    }
    _write_json(vout / "cross_modal_vision_ocr_realvideo_frame_sample_verifier_report.json", rep)
    print(json.dumps({"verifier_output_root": str(vout), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
