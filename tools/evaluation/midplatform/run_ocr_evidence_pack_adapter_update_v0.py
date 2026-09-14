#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Evidence-Pack-Adapter-Update-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


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
    ap.add_argument("--ocr-evidence-pack-contract-root", required=True)
    ap.add_argument("--realvideo-reference-closure-root", required=True)
    ap.add_argument("--realvideo-reference-update-root", required=True)
    ap.add_argument("--realvideo-readonly-consumer-root", required=True)
    ap.add_argument("--realvideo-gated-submission-root", required=True)
    ap.add_argument("--poster-reference-closure-root", required=True)
    ap.add_argument("--poster-reference-update-root", required=True)
    ap.add_argument("--poster-readonly-consumer-root", required=True)
    ap.add_argument("--poster-gated-execution-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    from capabilities.midplatform.ocr_evidence_pack_adapter_update_v0 import (
        run_ocr_evidence_pack_adapter_update_v0,
    )

    roots = {
        "ocr_evidence_pack_contract_root": _require_abs(args.ocr_evidence_pack_contract_root, "contract"),
        "realvideo_reference_closure_root": _require_abs(args.realvideo_reference_closure_root, "rv_closure"),
        "realvideo_reference_update_root": _require_abs(args.realvideo_reference_update_root, "rv_update"),
        "realvideo_readonly_consumer_root": _require_abs(args.realvideo_readonly_consumer_root, "rv_consumer"),
        "realvideo_gated_submission_root": _require_abs(args.realvideo_gated_submission_root, "rv_gated"),
        "poster_reference_closure_root": _require_abs(args.poster_reference_closure_root, "poster_closure"),
        "poster_reference_update_root": _require_abs(args.poster_reference_update_root, "poster_update"),
        "poster_readonly_consumer_root": _require_abs(args.poster_readonly_consumer_root, "poster_consumer"),
        "poster_gated_execution_root": _require_abs(args.poster_gated_execution_root, "poster_gated"),
        "benchmark_real_values_smoke_root": _require_abs(args.benchmark_real_values_smoke_root, "benchmark"),
        "system_health_governance_root": _require_abs(args.system_health_governance_root, "health"),
        "simulation_lab_harness_root": _require_abs(args.simulation_lab_harness_root, "sim"),
    }

    result = run_ocr_evidence_pack_adapter_update_v0(
        ocr_evidence_pack_contract_root=str(roots["ocr_evidence_pack_contract_root"]),
        realvideo_reference_closure_root=str(roots["realvideo_reference_closure_root"]),
        realvideo_reference_update_root=str(roots["realvideo_reference_update_root"]),
        realvideo_readonly_consumer_root=str(roots["realvideo_readonly_consumer_root"]),
        realvideo_gated_submission_root=str(roots["realvideo_gated_submission_root"]),
        poster_reference_closure_root=str(roots["poster_reference_closure_root"]),
        poster_reference_update_root=str(roots["poster_reference_update_root"]),
        poster_readonly_consumer_root=str(roots["poster_readonly_consumer_root"]),
        poster_gated_execution_root=str(roots["poster_gated_execution_root"]),
        benchmark_real_values_smoke_root=str(roots["benchmark_real_values_smoke_root"]),
        system_health_governance_root=str(roots["system_health_governance_root"]),
        simulation_lab_harness_root=str(roots["simulation_lab_harness_root"]),
        output_root=str(out),
    )

    names = [
        "summary",
        "poster_collection",
        "rv_collection",
        "unified",
        "field_matrix",
        "coord_report",
        "chain_report",
        "raw_preservation",
        "empty_guard",
        "readability_report",
        "sem_report",
        "wm_report",
        "compliance",
        "metrics",
        "benchmark_link",
        "health_link",
        "boundary",
        "sim_report",
        "non_claims",
        "followups",
        "audit",
        "errs",
    ]
    files = [
        "ocr_evidence_pack_adapter_update_summary.json",
        "ocr_evidence_pack_adapter_poster_collection.json",
        "ocr_evidence_pack_adapter_realvideo_collection.json",
        "ocr_evidence_pack_adapter_unified_index.json",
        "ocr_evidence_pack_adapter_field_completeness_matrix.json",
        "ocr_evidence_pack_adapter_coordinate_attachment_report.json",
        "ocr_evidence_pack_adapter_source_chain_preservation_report.json",
        "ocr_evidence_pack_adapter_raw_ocr_preservation_report.json",
        "ocr_evidence_pack_adapter_empty_text_guard_report.json",
        "ocr_evidence_pack_adapter_readability_quality_report.json",
        "ocr_evidence_pack_adapter_semantic_placeholder_report.json",
        "ocr_evidence_pack_adapter_world_model_attach_placeholder_report.json",
        "ocr_evidence_pack_adapter_contract_compliance_report.json",
        "ocr_evidence_pack_adapter_metrics_candidate_report.json",
        "ocr_evidence_pack_adapter_benchmark_link_report.json",
        "ocr_evidence_pack_adapter_system_health_link_report.json",
        "ocr_evidence_pack_adapter_no_write_boundary_report.json",
        "ocr_evidence_pack_adapter_simulation_context_report.json",
        "ocr_evidence_pack_adapter_non_claims_report.json",
        "ocr_evidence_pack_adapter_open_followups.json",
        "ocr_evidence_pack_adapter_audit_report.json",
    ]

    summary = result[0]
    errs = result[-1]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, obj in zip(files, result[:-1]):
        _write_json(out / fname, obj)

    (out / "ocr_evidence_pack_adapter_notes.md").write_text(
        "\n".join(
            [
                "# OCR Evidence Pack Adapter Update",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- total_pack_count: {summary.get('total_pack_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Adapter only; preserves raw OCR and source chains.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": summary.get("phase_verdict_hint"), "errors": errs},
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
