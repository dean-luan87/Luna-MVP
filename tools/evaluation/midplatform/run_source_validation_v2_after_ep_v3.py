#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Source-Validation-v2-after-EP-v3-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("source_validation_v2_after_ep_v3_summary.json", "summary"),
    ("source_validation_v2_candidate_intake_matrix.json", "intake_matrix"),
    ("source_validation_v2_rule_matrix.json", "rule_matrix"),
    ("source_validation_v2_source_chain_completeness_report.json", "chain_completeness"),
    ("source_validation_v2_same_frame_consensus_blocker_report.json", "same_frame_blocker"),
    ("source_validation_v2_strategy_repeat_validation_report.json", "strategy_repeat"),
    ("source_validation_v2_noisy_segment_blocker_report.json", "noisy_blocker"),
    ("source_validation_v2_external_support_missing_report.json", "external_support"),
    ("source_validation_v2_entity_validation_boundary_report.json", "entity_boundary"),
    ("source_validation_v2_decision_matrix.json", "decision_matrix"),
    ("source_validation_v2_routing_report.json", "routing"),
    ("source_validation_v2_future_validation_plan.json", "future_plan"),
    ("source_validation_v2_review_policy_readiness_report.json", "review_readiness"),
    ("source_validation_v2_unresolved_slot_readiness_report.json", "unresolved_slot"),
    ("source_validation_v2_boundary_report.json", "boundary"),
    ("source_validation_v2_metrics_candidate_report.json", "metrics"),
    ("source_validation_v2_benchmark_link_report.json", "benchmark_link"),
    ("source_validation_v2_system_health_link_report.json", "health_link"),
    ("source_validation_v2_no_write_boundary_report.json", "no_write"),
    ("source_validation_v2_simulation_context_report.json", "sim_report"),
    ("source_validation_v2_non_claims_report.json", "non_claims"),
    ("source_validation_v2_open_followups.json", "followups"),
    ("source_validation_v2_audit_report.json", "audit"),
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
    ap.add_argument("--semantic-v3-root", required=True)
    ap.add_argument("--evidence-pack-v3-root", required=True)
    ap.add_argument("--ocrrequest-gated-submission-v2-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-v2-root", required=True)
    ap.add_argument("--roi-crop-v2-root", required=True)
    ap.add_argument("--roi-bbox-expansion-root", required=True)
    ap.add_argument("--roi-crop-diversity-root", required=True)
    ap.add_argument("--roi-ocr-quality-diagnosis-root", required=True)
    ap.add_argument("--semantic-v2-root", required=True)
    ap.add_argument("--evidence-pack-v2-root", required=True)
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
        "semantic_v3_root": _require_abs(args.semantic_v3_root, "sem_v3"),
        "evidence_pack_v3_root": _require_abs(args.evidence_pack_v3_root, "ep_v3"),
        "ocrrequest_gated_submission_v2_root": _require_abs(args.ocrrequest_gated_submission_v2_root, "ocr_v2"),
        "roi_ocrrequest_reference_v2_root": _require_abs(args.roi_ocrrequest_reference_v2_root, "ref_v2"),
        "roi_crop_v2_root": _require_abs(args.roi_crop_v2_root, "crop_v2"),
        "roi_bbox_expansion_root": _require_abs(args.roi_bbox_expansion_root, "bbox"),
        "roi_crop_diversity_root": _require_abs(args.roi_crop_diversity_root, "div"),
        "roi_ocr_quality_diagnosis_root": _require_abs(args.roi_ocr_quality_diagnosis_root, "diag"),
        "semantic_v2_root": _require_abs(args.semantic_v2_root, "sem_v2"),
        "evidence_pack_v2_root": _require_abs(args.evidence_pack_v2_root, "ep_v2"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "mixed"),
        "worldmodel_unresolved_slot_contract_root": _require_abs(
            args.worldmodel_unresolved_slot_contract_root, "wm_slot"
        ),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.source_validation_v2_after_ep_v3 import run_source_validation_v2_after_ep_v3

    result = run_source_validation_v2_after_ep_v3(
        semantic_v3_root=str(roots["semantic_v3_root"]),
        evidence_pack_v3_root=str(roots["evidence_pack_v3_root"]),
        ocrrequest_gated_submission_v2_root=str(roots["ocrrequest_gated_submission_v2_root"]),
        roi_ocrrequest_reference_v2_root=str(roots["roi_ocrrequest_reference_v2_root"]),
        roi_crop_v2_root=str(roots["roi_crop_v2_root"]),
        roi_bbox_expansion_root=str(roots["roi_bbox_expansion_root"]),
        roi_crop_diversity_root=str(roots["roi_crop_diversity_root"]),
        roi_ocr_quality_diagnosis_root=str(roots["roi_ocr_quality_diagnosis_root"]),
        semantic_v2_root=str(roots["semantic_v2_root"]),
        evidence_pack_v2_root=str(roots["evidence_pack_v2_root"]),
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

    (out / "source_validation_v2_notes.md").write_text(
        "\n".join(
            [
                "# Source Validation v2 after EP v3",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- validation candidates: {summary.get('validation_candidate_count')}",
                f"- passed: {summary.get('source_validation_passed_count')}",
                f"- blocked: {summary.get('source_validation_blocked_count')}",
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
                "source_validation_passed_count": summary.get("source_validation_passed_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
