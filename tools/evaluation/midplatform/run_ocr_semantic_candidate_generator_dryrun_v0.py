#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Semantic-Candidate-Generator-DryRun-001 runner."""

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
    ap.add_argument("--ocr-evidence-pack-adapter-update-root", required=True)
    ap.add_argument("--realvideo-readability-governance-root", required=True)
    ap.add_argument("--poster-fusion-gate-chain-closure-root", required=True)
    ap.add_argument("--public-facility-runtime-dryrun-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    roots = {
        "ocr_evidence_pack_contract_root": _require_abs(args.ocr_evidence_pack_contract_root, "contract"),
        "ocr_evidence_pack_adapter_update_root": _require_abs(args.ocr_evidence_pack_adapter_update_root, "adapter"),
        "realvideo_readability_governance_root": _require_abs(args.realvideo_readability_governance_root, "readability"),
        "poster_fusion_gate_chain_closure_root": _require_abs(args.poster_fusion_gate_chain_closure_root, "poster_closure"),
        "public_facility_runtime_dryrun_root": _require_abs(args.public_facility_runtime_dryrun_root, "public_facility"),
        "benchmark_real_values_smoke_root": _require_abs(args.benchmark_real_values_smoke_root, "benchmark"),
        "system_health_governance_root": _require_abs(args.system_health_governance_root, "health"),
        "simulation_lab_harness_root": _require_abs(args.simulation_lab_harness_root, "sim"),
    }

    from capabilities.midplatform.ocr_semantic_candidate_generator_dryrun_v0 import (
        run_ocr_semantic_candidate_generator_dryrun_v0,
    )

    (
        summary,
        collection,
        poster_matrix,
        rv_empty_matrix,
        type_report,
        enhancement,
        basis_report,
        gov_report,
        raw_preservation,
        empty_guard,
        quality_risk,
        wm_carryover,
        chain_report,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_ocr_semantic_candidate_generator_dryrun_v0(
        ocr_evidence_pack_contract_root=str(roots["ocr_evidence_pack_contract_root"]),
        ocr_evidence_pack_adapter_update_root=str(roots["ocr_evidence_pack_adapter_update_root"]),
        realvideo_readability_governance_root=str(roots["realvideo_readability_governance_root"]),
        poster_fusion_gate_chain_closure_root=str(roots["poster_fusion_gate_chain_closure_root"]),
        public_facility_runtime_dryrun_root=str(roots["public_facility_runtime_dryrun_root"]),
        benchmark_real_values_smoke_root=str(roots["benchmark_real_values_smoke_root"]),
        system_health_governance_root=str(roots["system_health_governance_root"]),
        simulation_lab_harness_root=str(roots["simulation_lab_harness_root"]),
        output_root=str(out),
    )

    report_writes = [
        ("ocr_semantic_candidate_collection.json", collection),
        ("ocr_semantic_candidate_poster_matrix.json", poster_matrix),
        ("ocr_semantic_candidate_realvideo_empty_matrix.json", rv_empty_matrix),
        ("ocr_semantic_candidate_type_classification_report.json", type_report),
        ("ocr_semantic_candidate_enhancement_report.json", enhancement),
        ("ocr_semantic_candidate_interpretation_basis_report.json", basis_report),
        ("ocr_semantic_candidate_governance_routing_report.json", gov_report),
        ("ocr_semantic_candidate_raw_text_preservation_report.json", raw_preservation),
        ("ocr_semantic_candidate_empty_text_guard_report.json", empty_guard),
        ("ocr_semantic_candidate_quality_risk_report.json", quality_risk),
        ("ocr_semantic_candidate_world_model_attach_placeholder_carryover_report.json", wm_carryover),
        ("ocr_semantic_candidate_source_chain_report.json", chain_report),
        ("ocr_semantic_candidate_metrics_candidate_report.json", metrics),
        ("ocr_semantic_candidate_benchmark_link_report.json", benchmark_link),
        ("ocr_semantic_candidate_system_health_link_report.json", health_link),
        ("ocr_semantic_candidate_no_write_boundary_report.json", boundary),
        ("ocr_semantic_candidate_simulation_context_report.json", sim_report),
        ("ocr_semantic_candidate_non_claims_report.json", non_claims),
        ("ocr_semantic_candidate_open_followups.json", followups),
        ("ocr_semantic_candidate_audit_report.json", audit),
    ]

    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    _write_json(out / "ocr_semantic_candidate_generator_summary.json", summary)
    for fname, obj in report_writes:
        _write_json(out / fname, obj)

    (out / "ocr_semantic_candidate_notes.md").write_text(
        "\n".join(
            [
                "# OCR Semantic Candidate Generator DryRun",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- semantic_candidate_count: {summary.get('semantic_candidate_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Rule/heuristic dry-run only; no LLM/VLM; raw OCR preserved.",
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
