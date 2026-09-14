#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for WorldModel Unresolved Observation Slot Contract v0."""

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


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks_passed = 0

    def ok(cond: bool, name: str) -> None:
        nonlocal checks_passed
        if cond:
            checks_passed += 1
        else:
            blockers.append(name)

    paths = {
        "summary": root / "worldmodel_unresolved_slot_contract_summary.json",
        "schema": root / "worldmodel_unresolved_observation_slot_schema_v0.json",
        "registry": root / "worldmodel_unresolved_slot_type_registry_v0.json",
        "trigger": root / "worldmodel_unresolved_slot_trigger_condition_matrix.json",
        "reasons": root / "worldmodel_unresolved_reason_taxonomy_v0.json",
        "fill": root / "worldmodel_future_observation_fill_policy_v0.json",
        "ocr_ver": root / "worldmodel_ocr_as_verification_policy_v0.json",
        "accum": root / "worldmodel_unresolved_slot_evidence_accumulation_policy_v0.json",
        "examples": root / "worldmodel_unresolved_slot_examples_v0.json",
        "lifecycle": root / "worldmodel_unresolved_slot_lifecycle_state_machine_v0.json",
        "source_chain": root / "worldmodel_unresolved_slot_source_chain_requirement_report.json",
        "gate": root / "worldmodel_unresolved_slot_gate_boundary_report.json",
        "metrics": root / "worldmodel_unresolved_slot_metrics_binding_plan.json",
        "benchmark": root / "worldmodel_unresolved_slot_benchmark_link_report.json",
        "health": root / "worldmodel_unresolved_slot_system_health_link_report.json",
        "boundary": root / "worldmodel_unresolved_slot_no_write_boundary_report.json",
        "sim": root / "worldmodel_unresolved_slot_simulation_context_report.json",
        "non_claims": root / "worldmodel_unresolved_slot_non_claims_report.json",
        "followups": root / "worldmodel_unresolved_slot_open_followups.json",
        "audit": root / "worldmodel_unresolved_slot_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "worldmodel_unresolved_slot_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    schema_doc = _read_json(paths["schema"])
    registry = _read_json(paths["registry"])
    trigger = _read_json(paths["trigger"])
    reasons = _read_json(paths["reasons"])
    fill = _read_json(paths["fill"])
    ocr_ver = _read_json(paths["ocr_ver"])
    accum = _read_json(paths["accum"])
    examples = _read_json(paths["examples"])
    lifecycle = _read_json(paths["lifecycle"])
    source_chain = _read_json(paths["source_chain"])
    gate = _read_json(paths["gate"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    tmpl = schema_doc.get("slot_template") or {}
    wm_status = tmpl.get("world_model_status") or {}

    ok(summary.get("contract_scope") == "schema_and_governance_only", "contract_scope")
    ok(summary.get("unresolved_slot_contract_defined") is True, "contract_defined")
    ok(summary.get("unknown_slot_supported") is True, "unknown_slot")
    ok(summary.get("future_observation_fill_policy_defined") is True, "fill_policy_defined")
    ok(summary.get("ocr_as_verification_policy_defined") is True, "ocr_ver_defined")
    ok(summary.get("world_model_write_executed") is False, "wm_write_false")

    ok("source_refs" in tmpl and "source_chain" in (tmpl.get("source_refs") or {}), "source_chain")
    ok("image_coordinates" in tmpl, "image_coordinates")
    ok("temporal_coordinates" in tmpl, "temporal_coordinates")
    ok("spatial_anchor_candidate" in tmpl, "spatial_anchor")
    ok("future_fill_policy" in tmpl, "future_fill_policy")
    ok(wm_status.get("slot_not_fact") is True, "slot_not_fact")
    ok(wm_status.get("world_model_fact_write_allowed") is False, "wm_fact_write_false")

    types = registry.get("types") if isinstance(registry.get("types"), list) else []
    type_names = {t.get("slot_type") for t in types if isinstance(t, dict)}
    ok(len(types) >= 8, "slot_type_count")
    ok("unresolved_text_region" in type_names, "unresolved_text_region")
    ok("partial_entity_slot" in type_names, "partial_entity_slot")
    ok("unresolved_visual_symbol_slot" in type_names, "unresolved_visual_symbol_slot")

    t_rows = trigger.get("rows") if isinstance(trigger.get("rows"), list) else []
    t_ids = {r.get("trigger_id") for r in t_rows if isinstance(r, dict)}
    ok(any("empty" in str(x) for x in t_ids) or any(
        r.get("trigger_id") == "trg_ocr_empty_text_like" for r in t_rows if isinstance(r, dict)
    ), "ocr_empty_trigger")
    ok(any(r.get("trigger_id") == "trg_scan_pack_empty" for r in t_rows if isinstance(r, dict)), "scan_pack_empty")

    r_codes = {r.get("reason_code") for r in (reasons.get("reasons") or []) if isinstance(r, dict)}
    ok("source_quality_insufficient" in r_codes, "source_quality_reason")

    fill_sources = fill.get("fill_sources") if isinstance(fill.get("fill_sources"), list) else []
    ok(all(fs.get("auto_commit_allowed") is False for fs in fill_sources if isinstance(fs, dict)), "auto_commit_false")

    stages = ocr_ver.get("stages") if isinstance(ocr_ver.get("stages"), list) else []
    stage_names = {s.get("world_model_stage") for s in stages if isinstance(s, dict)}
    ok({"bootstrap", "established_environment", "maintenance"}.issubset(stage_names), "ocr_stages")
    ok(any(s.get("no_relearn_from_scratch_if_world_model_available") is True for s in stages if isinstance(s, dict)), "no_relearn")

    ok(accum.get("append_not_overwrite") is True, "append_not_overwrite")

    ex_list = examples.get("examples") if isinstance(examples.get("examples"), list) else []
    ex_text = json.dumps(ex_list, ensure_ascii=False)
    ok("建设银行" in ex_text or "construction" in ex_text.lower(), "bank_example")
    ok("GAP" in ex_text, "gap_example")
    ok(any(e.get("example_id") == "example_5_realvideo_scan_pack_empty" for e in ex_list if isinstance(e, dict)), "scan_empty_example")

    states = lifecycle.get("states") if isinstance(lifecycle.get("states"), list) else []
    promoted = next((s for s in states if isinstance(s, dict) and s.get("state") == "promoted_to_world_model_fact"), {})
    ok("write_gate" in str(lifecycle.get("promotion_rule", "")).lower(), "promotion_write_gate")
    ok(promoted.get("write_allowed") is True, "promoted_write_allowed_only_via_gate")

    ok(source_chain.get("rules", {}).get("forbid_fabricated_spatial_anchor") is True, "no_fake_anchor")

    ok(gate.get("unresolved_slot_not_fact") is True, "gate_unresolved_not_fact")
    ok(gate.get("write_gate_required") is True, "write_gate_required")

    ok(metrics.get("current_phase_collects_metrics") is False, "metrics_not_collected")
    ok(benchmark.get("benchmark_score_generated") is False, "bench_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_runtime")
    ok(boundary.get("boundary_ok") is True, "boundary_ok")
    ok(boundary.get("violations") == [], "violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(non_claims.get("no_world_model_write") is True, "non_claims_wm")
    ok(len(followups.get("items") or []) >= 5, "followups")
    ok(audit.get("world_model_write_executed") is False, "audit_wm_write")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_scene_delta")
    ok(audit.get("midplatform_fact_written") is False, "audit_fact")
    ok(audit.get("navigation_decision_invoked") is False, "audit_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {"schema_version": "worldmodel_unresolved_slot_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks_passed}
    _write_json(root / "worldmodel_unresolved_slot_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks_passed}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
