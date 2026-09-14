#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Multiframe-Merge-Proposal-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("multiframe_merge_proposal_v1_summary.json", "summary"),
    ("multiframe_sv2_blocker_intake_matrix.json", "blocker_intake"),
    ("multiframe_merge_proposal_rule_matrix.json", "rule_matrix"),
    ("multiframe_candidate_region_schema_v1.json", "region_schema"),
    ("multiframe_candidate_region_collection_v1.json", "region_collection"),
    ("multiframe_target_frame_window_plan_v1.json", "target_frame_window"),
    ("multiframe_neighbor_frame_selection_plan_v1.json", "neighbor_plan"),
    ("multiframe_tracklet_hint_plan_v1.json", "tracklet_plan"),
    ("multiframe_merge_strategy_matrix_v1.json", "merge_strategy"),
    ("multiframe_expected_evidence_gain_report_v1.json", "evidence_gain"),
    ("multiframe_merge_risk_report_v1.json", "risk"),
    ("multiframe_future_extraction_plan_v1.json", "future_extraction"),
    ("multiframe_same_frame_blocker_carryover_report_v1.json", "same_frame_carryover"),
    ("multiframe_source_chain_report_v1.json", "source_chain"),
    ("multiframe_review_unresolved_readiness_report_v1.json", "review_readiness"),
    ("multiframe_boundary_report_v1.json", "boundary"),
    ("multiframe_metrics_candidate_report_v1.json", "metrics"),
    ("multiframe_benchmark_link_report_v1.json", "benchmark_link"),
    ("multiframe_system_health_link_report_v1.json", "health_link"),
    ("multiframe_no_write_boundary_report_v1.json", "no_write"),
    ("multiframe_simulation_context_report_v1.json", "sim_report"),
    ("multiframe_non_claims_report_v1.json", "non_claims"),
    ("multiframe_open_followups_v1.json", "followups"),
    ("multiframe_audit_report_v1.json", "audit"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if (parent / "_eval_out").is_dir():
                return parent
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--source-validation-v2-root", required=True)
    ap.add_argument("--semantic-v3-root", required=True)
    ap.add_argument("--evidence-pack-v3-root", required=True)
    ap.add_argument("--ocrrequest-gated-submission-v2-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-v2-root", required=True)
    ap.add_argument("--roi-crop-v2-root", required=True)
    ap.add_argument("--roi-bbox-expansion-root", required=True)
    ap.add_argument("--roi-crop-diversity-root", required=True)
    ap.add_argument("--roi-ocr-quality-diagnosis-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--worldmodel-unresolved-slot-contract-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    roots = {
        "source_validation_v2_root": _require_abs(args.source_validation_v2_root, "sv2"),
        "semantic_v3_root": _require_abs(args.semantic_v3_root, "sem_v3"),
        "evidence_pack_v3_root": _require_abs(args.evidence_pack_v3_root, "ep_v3"),
        "ocrrequest_gated_submission_v2_root": _require_abs(
            args.ocrrequest_gated_submission_v2_root, "ocr_v2"
        ),
        "roi_ocrrequest_reference_v2_root": _require_abs(
            args.roi_ocrrequest_reference_v2_root, "ref_v2"
        ),
        "roi_crop_v2_root": _require_abs(args.roi_crop_v2_root, "crop_v2"),
        "roi_bbox_expansion_root": _require_abs(args.roi_bbox_expansion_root, "bbox"),
        "roi_crop_diversity_root": _require_abs(args.roi_crop_diversity_root, "div"),
        "roi_ocr_quality_diagnosis_root": _require_abs(args.roi_ocr_quality_diagnosis_root, "diag"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "mixed"),
        "worldmodel_unresolved_slot_contract_root": _require_abs(
            args.worldmodel_unresolved_slot_contract_root, "wm_slot"
        ),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.multiframe_merge_proposal_v1 import run_multiframe_merge_proposal_v1

    result = run_multiframe_merge_proposal_v1(
        source_validation_v2_root=str(roots["source_validation_v2_root"]),
        semantic_v3_root=str(roots["semantic_v3_root"]),
        evidence_pack_v3_root=str(roots["evidence_pack_v3_root"]),
        ocrrequest_gated_submission_v2_root=str(roots["ocrrequest_gated_submission_v2_root"]),
        roi_ocrrequest_reference_v2_root=str(roots["roi_ocrrequest_reference_v2_root"]),
        roi_crop_v2_root=str(roots["roi_crop_v2_root"]),
        roi_bbox_expansion_root=str(roots["roi_bbox_expansion_root"]),
        roi_crop_diversity_root=str(roots["roi_crop_diversity_root"]),
        roi_ocr_quality_diagnosis_root=str(roots["roi_ocr_quality_diagnosis_root"]),
        linebox_sq_root=str(roots["linebox_sq_root"]),
        mixed_batch_v2_root=str(roots["mixed_batch_v2_root"]),
        worldmodel_unresolved_slot_contract_root=str(roots["worldmodel_unresolved_slot_contract_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "multiframe_notes.md").write_text(
        "\n".join(
            [
                "# Multiframe Merge Proposal v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- validation candidates observed: {summary.get('validation_candidate_count_observed')}",
                f"- multiframe regions: {summary.get('multiframe_candidate_region_count')}",
                f"- same-frame blocker still active (carryover)",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "multiframe_candidate_region_count": summary.get("multiframe_candidate_region_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
