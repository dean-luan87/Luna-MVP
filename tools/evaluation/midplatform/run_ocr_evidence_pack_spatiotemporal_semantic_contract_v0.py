#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Evidence-Pack-SpatioTemporal-Semantic-Contract-001 runner."""

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
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    bench = _require_abs(args.benchmark_real_values_smoke_root, "benchmark")
    health = _require_abs(args.system_health_governance_root, "health")
    sim = _require_abs(args.simulation_lab_harness_root, "sim")

    from capabilities.midplatform.ocr_evidence_pack_spatiotemporal_semantic_contract_v0 import (
        run_ocr_evidence_pack_spatiotemporal_semantic_contract_v0,
    )

    (
        summary,
        ocr_pack_schema,
        semantic_schema,
        wm_attach_schema,
        coord_matrix,
        meaning_registry,
        enhancement_matrix,
        examples,
        arbitration,
        wm_gates,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_ocr_evidence_pack_spatiotemporal_semantic_contract_v0(
        benchmark_real_values_smoke_root=str(bench),
        system_health_governance_root=str(health),
        simulation_lab_harness_root=str(sim),
        output_root=str(out),
    )

    summary["output_root"] = str(out.resolve())
    summary["input_roots"] = {
        "benchmark_real_values_smoke_root": str(bench),
        "system_health_governance_root": str(health),
        "simulation_lab_harness_root": str(sim),
    }
    if errs:
        summary["errors"] = errs

    _write_json(out / "ocr_evidence_pack_contract_summary.json", summary)
    _write_json(out / "ocr_text_evidence_pack_schema_v0.json", ocr_pack_schema)
    _write_json(out / "ocr_semantic_candidate_schema_v0.json", semantic_schema)
    _write_json(out / "ocr_world_model_attach_candidate_schema_v0.json", wm_attach_schema)
    _write_json(out / "ocr_evidence_coordinate_requirements_matrix.json", coord_matrix)
    _write_json(out / "ocr_semantic_meaning_type_registry_v0.json", meaning_registry)
    _write_json(out / "ocr_enhancement_operation_matrix.json", enhancement_matrix)
    _write_json(out / "ocr_evidence_pack_examples_v0.json", examples)
    _write_json(out / "ocr_semantic_midplatform_arbitration_policy.json", arbitration)
    _write_json(out / "ocr_world_model_attach_gate_policy.json", wm_gates)
    _write_json(out / "ocr_evidence_pack_metrics_binding_plan.json", metrics)
    _write_json(out / "ocr_evidence_pack_benchmark_link_report.json", benchmark_link)
    _write_json(out / "ocr_evidence_pack_system_health_link_report.json", health_link)
    _write_json(out / "ocr_evidence_pack_no_write_boundary_report.json", boundary)
    _write_json(out / "ocr_evidence_pack_simulation_context_report.json", sim_report)
    _write_json(out / "ocr_evidence_pack_non_claims_report.json", non_claims)
    _write_json(out / "ocr_evidence_pack_open_followups.json", followups)
    _write_json(out / "ocr_evidence_pack_audit_report.json", audit)

    (out / "ocr_evidence_pack_contract_notes.md").write_text(
        "\n".join(
            [
                "# OCR Evidence Pack SpatioTemporal Semantic Contract",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- contract_scope: {summary.get('contract_scope')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "OCRTextEvidence -> OCRSemanticCandidate -> WorldModelAttachCandidate -> Gate",
                "",
                "Contract only; no OCR/semantic/WM writes.",
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
