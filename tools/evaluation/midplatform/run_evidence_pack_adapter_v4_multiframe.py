#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Evidence-Pack-Adapter-v4-Multiframe-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("evidence_pack_adapter_v4_multiframe_summary.json", "summary"),
    ("evidence_pack_v4_multiframe_ocr_result_intake_matrix.json", "intake_matrix"),
    ("evidence_pack_v4_multiframe_schema.json", "schema_doc"),
    ("evidence_pack_v4_multiframe_collection.json", "collection"),
    ("evidence_pack_v4_multiframe_alignment_matrix.json", "alignment_matrix"),
    ("evidence_pack_v4_empty_ocr_result_guard_report.json", "empty_guard"),
    ("evidence_pack_v4_projection_risk_preservation_report.json", "projection_risk"),
    ("evidence_pack_v4_multiframe_context_report.json", "multiframe_context_report"),
    ("evidence_pack_v4_provider_metadata_report.json", "provider_metadata_report"),
    ("evidence_pack_v4_bbox_crop_context_report.json", "bbox_crop_context"),
    ("evidence_pack_v4_semantic_readiness_report.json", "semantic_readiness"),
    ("evidence_pack_v4_source_validation_rerun_readiness_report.json", "sv_readiness"),
    ("evidence_pack_v4_same_frame_blocker_carryover_report.json", "same_frame_carryover"),
    ("evidence_pack_v4_future_fix_plan.json", "future_fix_plan"),
    ("evidence_pack_v4_source_chain_report.json", "source_chain_report"),
    ("evidence_pack_v4_boundary_report.json", "boundary"),
    ("evidence_pack_v4_metrics_candidate_report.json", "metrics"),
    ("evidence_pack_v4_benchmark_link_report.json", "benchmark_link"),
    ("evidence_pack_v4_system_health_link_report.json", "health_link"),
    ("evidence_pack_v4_no_write_boundary_report.json", "no_write"),
    ("evidence_pack_v4_simulation_context_report.json", "sim_report"),
    ("evidence_pack_v4_non_claims_report.json", "non_claims"),
    ("evidence_pack_v4_open_followups.json", "followups"),
    ("evidence_pack_v4_audit_report.json", "audit"),
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
    ap.add_argument("--multiframe-ocr-root", required=True)
    ap.add_argument("--multiframe-crop-root", required=True)
    ap.add_argument("--text-region-tracklet-root", required=True)
    ap.add_argument("--better-frame-root", required=True)
    ap.add_argument("--multiframe-merge-proposal-root", required=True)
    ap.add_argument("--source-validation-v2-root", required=True)
    ap.add_argument("--semantic-v3-root", required=True)
    ap.add_argument("--evidence-pack-v3-root", required=True)
    ap.add_argument("--ocrrequest-gated-submission-v2-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-v2-root", required=True)
    ap.add_argument("--roi-crop-v2-root", required=True)
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
        "multiframe_ocr_root": _require_abs(args.multiframe_ocr_root, "ocr"),
        "multiframe_crop_root": _require_abs(args.multiframe_crop_root, "crop"),
        "text_region_tracklet_root": _require_abs(args.text_region_tracklet_root, "tr"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "multiframe_merge_proposal_root": _require_abs(args.multiframe_merge_proposal_root, "mf"),
        "source_validation_v2_root": _require_abs(args.source_validation_v2_root, "sv2"),
        "semantic_v3_root": _require_abs(args.semantic_v3_root, "sem_v3"),
        "evidence_pack_v3_root": _require_abs(args.evidence_pack_v3_root, "ep_v3"),
        "ocrrequest_gated_submission_v2_root": _require_abs(args.ocrrequest_gated_submission_v2_root, "ocr_v2"),
        "roi_ocrrequest_reference_v2_root": _require_abs(args.roi_ocrrequest_reference_v2_root, "ref_v2"),
        "roi_crop_v2_root": _require_abs(args.roi_crop_v2_root, "crop_v2"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "mixed"),
        "worldmodel_unresolved_slot_contract_root": _require_abs(
            args.worldmodel_unresolved_slot_contract_root, "wm"
        ),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.evidence_pack_adapter_v4_multiframe import (
        run_evidence_pack_adapter_v4_multiframe,
    )

    result = run_evidence_pack_adapter_v4_multiframe(
        multiframe_ocr_root=str(roots["multiframe_ocr_root"]),
        multiframe_crop_root=str(roots["multiframe_crop_root"]),
        text_region_tracklet_root=str(roots["text_region_tracklet_root"]),
        better_frame_root=str(roots["better_frame_root"]),
        multiframe_merge_proposal_root=str(roots["multiframe_merge_proposal_root"]),
        source_validation_v2_root=str(roots["source_validation_v2_root"]),
        semantic_v3_root=str(roots["semantic_v3_root"]),
        evidence_pack_v3_root=str(roots["evidence_pack_v3_root"]),
        ocrrequest_gated_submission_v2_root=str(roots["ocrrequest_gated_submission_v2_root"]),
        roi_ocrrequest_reference_v2_root=str(roots["roi_ocrrequest_reference_v2_root"]),
        roi_crop_v2_root=str(roots["roi_crop_v2_root"]),
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

    (out / "evidence_pack_v4_notes.md").write_text(
        "\n".join(
            [
                "# Evidence Pack Adapter v4 Multiframe",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- OCR results: {summary.get('multiframe_ocr_result_count_observed')}",
                f"- EP v4 packs: {summary.get('evidence_pack_v4_count')}",
                f"- empty OCR: {summary.get('empty_ocr_result_count')}",
                "",
                "Empty OCR preserved as valid result, not no-text fact; Semantic/SV blocked.",
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
                "evidence_pack_v4_count": summary.get("evidence_pack_v4_count"),
                "empty_ocr_result_count": summary.get("empty_ocr_result_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
