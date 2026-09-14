#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-WorldModel-Unresolved-Observation-Slot-Contract-001 runner."""

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
    ap.add_argument("--ocr-evidence-pack-adapter-root", required=True)
    ap.add_argument("--ocr-semantic-candidate-root", required=True)
    ap.add_argument("--readability-governance-root", required=True)
    ap.add_argument("--realvideo-reference-closure-root", required=True)
    ap.add_argument("--mixed-video-poster-batch-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    roots = {
        "ocr_evidence_pack_contract_root": _require_abs(args.ocr_evidence_pack_contract_root, "contract"),
        "ocr_evidence_pack_adapter_root": _require_abs(args.ocr_evidence_pack_adapter_root, "adapter"),
        "ocr_semantic_candidate_root": _require_abs(args.ocr_semantic_candidate_root, "semantic"),
        "readability_governance_root": _require_abs(args.readability_governance_root, "readability"),
        "realvideo_reference_closure_root": _require_abs(args.realvideo_reference_closure_root, "closure"),
        "mixed_video_poster_batch_root": _require_abs(args.mixed_video_poster_batch_root, "mixed-batch"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "benchmark"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.worldmodel_unresolved_observation_slot_contract_v0 import (
        run_worldmodel_unresolved_observation_slot_contract_v0,
    )

    result = run_worldmodel_unresolved_observation_slot_contract_v0(
        output_root=str(out),
        ocr_evidence_pack_contract_root=str(roots["ocr_evidence_pack_contract_root"]),
        ocr_evidence_pack_adapter_root=str(roots["ocr_evidence_pack_adapter_root"]),
        ocr_semantic_candidate_root=str(roots["ocr_semantic_candidate_root"]),
        readability_governance_root=str(roots["readability_governance_root"]),
        realvideo_reference_closure_root=str(roots["realvideo_reference_closure_root"]),
        mixed_video_poster_batch_root=str(roots["mixed_video_poster_batch_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
    )

    (
        summary,
        slot_schema,
        type_registry,
        trigger_matrix,
        reason_taxonomy,
        future_fill_policy,
        ocr_verification,
        evidence_accumulation,
        examples,
        lifecycle,
        source_chain_req,
        gate_boundary,
        metrics_plan,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = result

    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if errs:
        summary["errors"] = errs

    writes = [
        ("worldmodel_unresolved_slot_contract_summary.json", summary),
        ("worldmodel_unresolved_observation_slot_schema_v0.json", slot_schema),
        ("worldmodel_unresolved_slot_type_registry_v0.json", type_registry),
        ("worldmodel_unresolved_slot_trigger_condition_matrix.json", trigger_matrix),
        ("worldmodel_unresolved_reason_taxonomy_v0.json", reason_taxonomy),
        ("worldmodel_future_observation_fill_policy_v0.json", future_fill_policy),
        ("worldmodel_ocr_as_verification_policy_v0.json", ocr_verification),
        ("worldmodel_unresolved_slot_evidence_accumulation_policy_v0.json", evidence_accumulation),
        ("worldmodel_unresolved_slot_examples_v0.json", examples),
        ("worldmodel_unresolved_slot_lifecycle_state_machine_v0.json", lifecycle),
        ("worldmodel_unresolved_slot_source_chain_requirement_report.json", source_chain_req),
        ("worldmodel_unresolved_slot_gate_boundary_report.json", gate_boundary),
        ("worldmodel_unresolved_slot_metrics_binding_plan.json", metrics_plan),
        ("worldmodel_unresolved_slot_benchmark_link_report.json", benchmark_link),
        ("worldmodel_unresolved_slot_system_health_link_report.json", health_link),
        ("worldmodel_unresolved_slot_no_write_boundary_report.json", boundary),
        ("worldmodel_unresolved_slot_simulation_context_report.json", sim_report),
        ("worldmodel_unresolved_slot_non_claims_report.json", non_claims),
        ("worldmodel_unresolved_slot_open_followups.json", followups),
        ("worldmodel_unresolved_slot_audit_report.json", audit),
    ]
    for name, obj in writes:
        _write_json(out / name, obj)

    (out / "worldmodel_unresolved_slot_notes.md").write_text(
        "\n".join(
            [
                "# WorldModel Unresolved Observation Slot Contract",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- contract_scope: {summary.get('contract_scope')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Contract only: schema / policy / examples / gate. No WM write, no OCR, no runtime slots.",
                "",
                "Principle: observed-but-unresolved regions are retained as future-fillable anchors, not facts.",
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
