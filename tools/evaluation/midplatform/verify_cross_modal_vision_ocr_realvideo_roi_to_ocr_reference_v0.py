#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001 verifier."""

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
    ap.add_argument("--reference-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.reference_root).expanduser().resolve()
    vout = (
        Path(args.verifier_output_root).expanduser().resolve()
        if args.verifier_output_root.strip()
        else (root.parent / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_verify_v0").resolve()
    )
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json")
    cand_p = req("cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_candidate.json")
    froi_p = req("cross_modal_vision_ocr_realvideo_frame_to_roi_reference_matrix.json")
    ocr_p = req("cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix.json")
    case_p = req("cross_modal_vision_ocr_realvideo_case_to_reference_mapping.json")
    gov_p = req("cross_modal_vision_ocr_realvideo_poster_facility_governance_reference_report.json")
    risk_p = req("cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_risk_report.json")
    met_p = req("cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_metrics_binding_report.json")
    bnd_p = req("cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_no_write_boundary_report.json")
    sim_p = req("cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_simulation_context_report.json")
    nc_p = req("cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_non_claims_report.json")
    aud_p = req("cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_audit_report.json")

    if not blockers:
        sm = _read_json(sum_p)
        if sm.get("reference_scope") != "reference_only":
            blockers.append("summary_reference_scope_wrong")
        for flag in (
            "based_on_frame_sample",
            "based_on_case_registry",
            "based_on_roi_proposal",
            "based_on_ocr_bridge",
        ):
            if sm.get(flag) is not True:
                blockers.append(f"summary_{flag}_not_true")
        for k, val in (
            ("ocr_request_submitted", False),
            ("ocr_invoked", False),
            ("rapidocr_invoked", False),
            ("vision_provider_invoked", False),
        ):
            if sm.get(k) is not val:
                blockers.append(f"summary_{k}_wrong")

        cand = _read_json(cand_p)
        if cand.get("reference_scope") != "reference_only":
            blockers.append("candidate_reference_scope_wrong")
        if cand.get("ocr_submission_status") != "not_submitted":
            blockers.append("candidate_ocr_submission_status_wrong")

        froi = _read_json(froi_p)
        rows = froi.get("rows") if isinstance(froi.get("rows"), list) else []
        if len(rows) < 1:
            blockers.append("frame_to_roi_sample_count_lt_1")

        ocrm = _read_json(ocr_p)
        for row in ocrm.get("rows") or []:
            if not isinstance(row, dict):
                continue
            if row.get("submission_status") != "not_submitted":
                blockers.append("ocr_submission_status_not_not_submitted")
                break
            if row.get("evidence_generated") is not False:
                blockers.append("ocr_evidence_generated_not_false")
                break

        case_doc = _read_json(case_p)
        for row in case_doc.get("rows") or []:
            if not isinstance(row, dict):
                continue
            if row.get("execution_status") != "reference_mapping_only":
                blockers.append(f"case_execution_status:{row.get('case_id')}")
            if row.get("should_write_fact") is not False:
                blockers.append(f"case_should_write_fact:{row.get('case_id')}")

        gov = _read_json(gov_p)
        for k, val in (
            ("poster_track_b_closed", True),
            ("public_facility_governance_available", True),
            ("facility_detection_invoked", False),
        ):
            if gov.get(k) is not val:
                blockers.append(f"gov_{k}_wrong")

        risk = _read_json(risk_p)
        flags = risk.get("risk_flags") or []
        for rf in ("ocr_request_not_submitted", "ocr_evidence_not_generated"):
            if rf not in flags:
                blockers.append(f"risk_missing:{rf}")

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
        if nc.get("no_ocr_evidence_claim") is not True:
            blockers.append("non_claims_no_ocr_evidence_not_true")
        if nc.get("no_benchmark_claim") is not True:
            blockers.append("non_claims_no_benchmark_not_true")

        audit = _read_json(aud_p)
        audit_checks = (
            ("ocr_request_submitted", False),
            ("ocr_invoked", False),
            ("rapidocr_invoked", False),
            ("paddleocr_invoked", False),
            ("vision_provider_invoked", False),
            ("fusion_invoked", False),
            ("scene_delta_candidate_generated", False),
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
        "schema": "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_verifier_report_v0",
        "phase": "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001",
        "verdict": verdict,
        "reference_root": str(root),
        "verifier_output_root": str(vout),
        "blockers": sorted(set(blockers)),
    }
    _write_json(vout / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_verifier_report.json", rep)
    print(json.dumps({"verifier_output_root": str(vout), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
