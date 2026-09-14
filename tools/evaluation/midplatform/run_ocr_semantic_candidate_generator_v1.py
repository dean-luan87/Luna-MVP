#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Semantic-Candidate-Generator-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("ocr_semantic_candidate_v1_summary.json", "summary"),
    ("ocr_semantic_candidate_v1_evidence_tier_input_matrix.json", "evidence_tier_matrix"),
    ("ocr_semantic_candidate_v1_gated_ocr_collection.json", "gated_collection"),
    ("ocr_semantic_candidate_v1_scan_observation_hint_report.json", "scan_hint_report"),
    ("ocr_semantic_candidate_v1_visual_symbol_route_report.json", "visual_route_report"),
    ("ocr_semantic_candidate_v1_sq_e_blocked_report.json", "sq_e_blocked_report"),
    ("ocr_semantic_candidate_v1_routing_decision_matrix.json", "routing_matrix"),
    ("ocr_semantic_candidate_v1_type_classification_report.json", "type_classification"),
    ("ocr_semantic_candidate_v1_raw_text_preservation_report.json", "raw_preservation"),
    ("ocr_semantic_candidate_v1_interpretation_basis_report.json", "interpretation_basis"),
    ("ocr_semantic_candidate_v1_governance_routing_report.json", "governance_routing"),
    ("ocr_semantic_candidate_v1_unresolved_slot_linkage_plan.json", "unresolved_linkage"),
    ("ocr_semantic_candidate_v1_quality_risk_report.json", "quality_risk"),
    ("ocr_semantic_candidate_v1_source_chain_report.json", "source_chain"),
    ("ocr_semantic_candidate_v1_metrics_candidate_report.json", "metrics"),
    ("ocr_semantic_candidate_v1_benchmark_link_report.json", "benchmark_link"),
    ("ocr_semantic_candidate_v1_system_health_link_report.json", "health_link"),
    ("ocr_semantic_candidate_v1_no_write_boundary_report.json", "boundary"),
    ("ocr_semantic_candidate_v1_simulation_context_report.json", "sim_report"),
    ("ocr_semantic_candidate_v1_non_claims_report.json", "non_claims"),
    ("ocr_semantic_candidate_v1_open_followups.json", "followups"),
    ("ocr_semantic_candidate_v1_audit_report.json", "audit"),
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
    ap.add_argument("--adapter-v1-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--contract-root", required=True)
    ap.add_argument("--readability-governance-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--worldmodel-unresolved-slot-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    roots = {
        "adapter_v1_root": _require_abs(args.adapter_v1_root, "adapter_v1"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "v2"),
        "contract_root": _require_abs(args.contract_root, "contract"),
        "readability_governance_root": _require_abs(args.readability_governance_root, "readability"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "worldmodel_unresolved_slot_root": _require_abs(args.worldmodel_unresolved_slot_root, "wm_slot"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "benchmark"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.ocr_semantic_candidate_generator_v1 import run_ocr_semantic_candidate_generator_v1

    result = run_ocr_semantic_candidate_generator_v1(
        output_root=str(out),
        adapter_v1_root=str(roots["adapter_v1_root"]),
        mixed_batch_v2_root=str(roots["mixed_batch_v2_root"]),
        contract_root=str(roots["contract_root"]),
        readability_governance_root=str(roots["readability_governance_root"]),
        linebox_sq_root=str(roots["linebox_sq_root"]),
        worldmodel_unresolved_slot_root=str(roots["worldmodel_unresolved_slot_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if result.get("errs"):
        summary["errors"] = result["errs"]

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "ocr_semantic_candidate_v1_notes.md").write_text(
        "\n".join(
            [
                "# OCR Semantic Candidate Generator v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- gated semantic candidates: {summary.get('input_gated_pack_count')}",
                f"- scan hints: {summary.get('input_scan_observation_count')}",
                f"- visual symbol routes: {summary.get('input_visual_symbol_route_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Tier-aware dry-run from Evidence Pack Adapter v1; no OCR/LLM/VLM/WM write.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": summary.get("phase_verdict_hint"), "errors": result.get("errs", [])},
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
