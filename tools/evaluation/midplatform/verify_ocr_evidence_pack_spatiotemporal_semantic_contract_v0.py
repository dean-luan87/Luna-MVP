#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Evidence Pack SpatioTemporal Semantic Contract v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return here.parents[3]


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _op_allowed(ops: List[Any], name: str) -> bool:
    for o in ops:
        if isinstance(o, dict) and o.get("operation") == name:
            return o.get("allowed") is True
    return False


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "ocr_evidence_pack_contract_summary.json",
        "ocr_pack": root / "ocr_text_evidence_pack_schema_v0.json",
        "semantic": root / "ocr_semantic_candidate_schema_v0.json",
        "wm_attach": root / "ocr_world_model_attach_candidate_schema_v0.json",
        "coord": root / "ocr_evidence_coordinate_requirements_matrix.json",
        "meaning": root / "ocr_semantic_meaning_type_registry_v0.json",
        "enhancement": root / "ocr_enhancement_operation_matrix.json",
        "examples": root / "ocr_evidence_pack_examples_v0.json",
        "arbitration": root / "ocr_semantic_midplatform_arbitration_policy.json",
        "wm_gates": root / "ocr_world_model_attach_gate_policy.json",
        "metrics": root / "ocr_evidence_pack_metrics_binding_plan.json",
        "benchmark": root / "ocr_evidence_pack_benchmark_link_report.json",
        "health": root / "ocr_evidence_pack_system_health_link_report.json",
        "boundary": root / "ocr_evidence_pack_no_write_boundary_report.json",
        "sim": root / "ocr_evidence_pack_simulation_context_report.json",
        "non_claims": root / "ocr_evidence_pack_non_claims_report.json",
        "followups": root / "ocr_evidence_pack_open_followups.json",
        "audit": root / "ocr_evidence_pack_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "ocr_evidence_pack_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    ocr_pack = _read_json(paths["ocr_pack"])
    semantic = _read_json(paths["semantic"])
    wm_attach = _read_json(paths["wm_attach"])
    coord = _read_json(paths["coord"])
    meaning = _read_json(paths["meaning"])
    enhancement = _read_json(paths["enhancement"])
    examples = _read_json(paths["examples"])
    arbitration = _read_json(paths["arbitration"])
    wm_gates = _read_json(paths["wm_gates"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("contract_scope") != "schema_and_governance_only":
        blockers.append("contract_scope")
    if summary.get("image_coordinate_required") is not True:
        blockers.append("image_coordinate_required")
    if summary.get("spatiotemporal_coordinate_required") is not True:
        blockers.append("spatiotemporal_required")
    if summary.get("semantic_candidate_required") is not True:
        blockers.append("semantic_required")
    if summary.get("world_model_attach_candidate_required") is not True:
        blockers.append("wm_attach_required")
    if summary.get("runtime_execution") is not False:
        blockers.append("runtime_execution")
    if summary.get("ocr_invoked") is not False:
        blockers.append("ocr_invoked")

    tmpl = ocr_pack.get("template") if isinstance(ocr_pack.get("template"), dict) else {}
    defaults = ocr_pack.get("defaults") if isinstance(ocr_pack.get("defaults"), dict) else {}
    if defaults.get("raw_ocr.raw_ocr_text_preserved") is not True:
        blockers.append("raw_preserved_required")
    for key in ("image_coordinates", "temporal_coordinates", "spatial_coordinates", "source"):
        if key not in tmpl:
            blockers.append(f"ocr_pack_missing:{key}")
    src = tmpl.get("source") if isinstance(tmpl.get("source"), dict) else {}
    if "source_chain" not in src:
        blockers.append("source_chain")
    ev_st = tmpl.get("evidence_status") if isinstance(tmpl.get("evidence_status"), dict) else {}
    if ev_st.get("fact_status") != "not_fact":
        blockers.append("default_fact_status")

    sem_tpl = semantic.get("template") if isinstance(semantic.get("template"), dict) else {}
    sem_gov = sem_tpl.get("governance") if isinstance(sem_tpl.get("governance"), dict) else {}
    sem_pol = semantic.get("policies") if isinstance(semantic.get("policies"), dict) else {}
    if sem_gov.get("semantic_candidate_not_fact") is not True and sem_pol.get("semantic_candidate_not_fact") is not True:
        blockers.append("semantic_not_fact")
    if sem_gov.get("raw_text_overwritten") is not False:
        blockers.append("raw_text_overwritten")

    wm_tpl = wm_attach.get("template") if isinstance(wm_attach.get("template"), dict) else {}
    wm_st = wm_tpl.get("status") if isinstance(wm_tpl.get("status"), dict) else {}
    if wm_st.get("attach_candidate_not_fact") is not True:
        blockers.append("attach_not_fact")
    if wm_st.get("world_model_write_allowed") is not False:
        blockers.append("wm_write_allowed")

    coord_rows = coord.get("rows") or []
    coord_pol = coord.get("policies") if isinstance(coord.get("policies"), dict) else {}
    bbox_row = next((r for r in coord_rows if r.get("coordinate_type") == "image_pixel_bbox"), None)
    if not bbox_row or bbox_row.get("required") is not True:
        blockers.append("image_pixel_bbox_required")
    if coord_pol.get("spatial_coordinate_nullable") is not True:
        blockers.append("spatial_nullable")

    types = meaning.get("types") or []
    if len(types) < 10:
        blockers.append("semantic_type_count")
    price_ttl = next((t for t in types if t.get("semantic_type") == "price_discount_text"), None)
    if not price_ttl or price_ttl.get("requires_ttl") is not True:
        blockers.append("price_discount_ttl")

    ops = enhancement.get("operations") or []
    if _op_allowed(ops, "overwrite_raw_ocr_text"):
        blockers.append("overwrite_allowed")
    if _op_allowed(ops, "write_enhanced_text_as_fact"):
        blockers.append("write_fact_allowed")

    ex_ids = {e.get("example_id") for e in (examples.get("examples") or []) if isinstance(e, dict)}
    for eid in ("construction_bank_occluded", "gap_logo_sign", "no_smoking_sign"):
        if eid not in ex_ids:
            blockers.append(f"example:{eid}")

    steps = arbitration.get("steps") or []
    if not steps:
        blockers.append("arbitration_steps")
    if arbitration.get("write_allowed_until_write_gate") is not False:
        blockers.append("write_allowed_before_gate")
    for step in steps:
        if step.get("write_allowed_after_step") is not False:
            blockers.append("step_write_allowed")
            break

    gates = wm_gates.get("gates") or []
    if not gates:
        blockers.append("wm_gates")
    if not all(g.get("satisfied_in_this_phase") is False for g in gates if isinstance(g, dict)):
        blockers.append("gate_satisfied_in_phase")

    future_metrics = metrics.get("future_metrics") or []
    if "raw_text_preservation_rate" not in future_metrics:
        blockers.append("raw_text_preservation_metric")

    if benchmark.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_score")
    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("health_runtime")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    if boundary.get("violations") != []:
        blockers.append("violations")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("sim_profile")

    if non_claims.get("no_world_model_write") is not True:
        blockers.append("non_claims_wm")
    if non_claims.get("no_semantic_model_execution") is not True:
        blockers.append("non_claims_semantic")

    if not (followups.get("items") or []):
        blockers.append("followups")

    audit_checks = [
        ("semantic_model_invoked", False),
        ("world_model_attach_executed", False),
        ("scene_delta_candidate_generated", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("runtime_routing_changed", False),
    ]
    for key, expected in audit_checks:
        if audit.get(key) != expected:
            blockers.append(f"audit:{key}")

    if blockers:
        verdict = "NO_GO"
    elif summary.get("phase_verdict_hint") == "CONDITIONAL_GO":
        verdict = "CONDITIONAL_GO"
    else:
        verdict = str(summary.get("phase_verdict_hint") or "GO")

    report = {
        "schema_version": "ocr_evidence_pack_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 60 - len(blockers),
        "smoke_root": str(root),
    }
    _write_json(root / "ocr_evidence_pack_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
