#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Luna Basic Functional Loop Stabilization Plan v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


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
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks = 0

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "luna_basic_functional_loop_stabilization_plan_v1_summary.json",
        "intake": "luna_basic_loop_input_intake_matrix_v1.json",
        "capability_matrix": "luna_basic_loop_current_capability_status_matrix_v1.json",
        "loop_definition": "luna_basic_functional_loop_definition_v1.json",
        "module_boundary": "luna_basic_loop_module_responsibility_boundary_v1.json",
        "info_source_standard": "luna_basic_loop_information_source_standard_v1.json",
        "task_state_policy": "luna_basic_loop_task_state_stabilization_policy_v1.json",
        "voice_plan": "luna_basic_loop_voice_dialogue_minimal_capability_plan_v1.json",
        "vision_ocr_ingest": "luna_basic_loop_vision_ocr_evidence_ingest_plan_v1.json",
        "isrc_handoff": "luna_basic_loop_isrc_handoff_policy_v1.json",
        "rrd_handoff": "luna_basic_loop_rrd_handoff_policy_v1.json",
        "classification": "luna_basic_loop_candidate_classification_policy_v1.json",
        "no_write_policy": "luna_basic_loop_no_write_boundary_policy_v1.json",
        "nav_plan": "luna_basic_loop_navigation_guidance_plan_v1.json",
        "seg_policy": "luna_basic_loop_future_segmentation_entry_policy_v1.json",
        "tracking_policy": "luna_basic_loop_future_object_tracking_entry_policy_v1.json",
        "map_policy": "luna_basic_loop_future_navigation_map_entry_policy_v1.json",
        "deferred": "luna_basic_loop_deferred_capability_matrix_v1.json",
        "test_plan": "luna_basic_loop_stabilization_test_plan_v1.json",
        "roadmap": "luna_basic_loop_recommended_phase_roadmap_v1.json",
        "trace": "luna_basic_loop_stabilization_decision_trace_v1.json",
        "final": "luna_basic_loop_stabilization_final_decision_v1.json",
        "boundary": "luna_basic_loop_stabilization_boundary_report_v1.json",
        "metrics": "luna_basic_loop_stabilization_metrics_candidate_report_v1.json",
        "bench": "luna_basic_loop_stabilization_benchmark_link_report_v1.json",
        "health": "luna_basic_loop_stabilization_system_health_report_v1.json",
        "no_write": "luna_basic_loop_stabilization_no_write_boundary_report_v1.json",
        "sim": "luna_basic_loop_stabilization_simulation_context_report_v1.json",
        "non_claims": "luna_basic_loop_stabilization_non_claims_report_v1.json",
        "followups": "luna_basic_loop_stabilization_open_followups_v1.json",
        "audit": "luna_basic_loop_stabilization_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "luna_basic_loop_stabilization_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("plan_scope") == "basic_functional_loop_stabilization_plan_only", "scope")
    ok(s.get("worldmodel_runtime_deferred") is True, "wm_deferred")
    ok(s.get("ocr_mainline_closed_for_governance") is True, "ocr_closed")
    ok(s.get("basic_functional_loop_defined") is True, "loop_def")
    ok(s.get("segmentation_future_entry_defined") is True, "seg_entry")
    ok(s.get("runtime_action_committed") is False, "no_rt")

    vp = data["voice_plan"]
    ok(vp.get("all_voice_output_requires_speech_gate") is True, "speech_gate")
    ok(vp.get("direct_tts_bypass_forbidden") is True, "no_tts_bypass")

    ok(data["isrc_handoff"].get("isrc_runtime_invoked_now") is False, "isrc_now")
    ok(data["rrd_handoff"].get("readable_region_discovery_invoked_now") is False, "rrd_now")

    cls_ids = [c.get("classification") for c in data["classification"].get("classifications") or [] if isinstance(c, dict)]
    ok("DO_NOT_USE_FOR_ACTION" in cls_ids, "dnu_class")
    ok(data["no_write_policy"].get("world_model_written") is False, "nwp_wm")

    nav = data["nav_plan"]
    ok(nav.get("map_dependency_required_now") is False, "no_map_now")
    ok(nav.get("worldmodel_dependency_required_now") is False, "no_wm_nav")

    seg = data["seg_policy"]
    ok(seg.get("segmentation_allowed_now") is False, "seg_now")
    ok(seg.get("segmentation_allowed_later") is True, "seg_later")

    trk = data["tracking_policy"]
    ok(trk.get("tracking_allowed_now") is False, "trk_now")
    ok(trk.get("tracker_id_is_not_identity_fact") is True, "trk_not_id")

    mp = data["map_policy"]
    ok(mp.get("map_integration_allowed_now") is False, "map_now")
    ok(mp.get("map_cannot_override_live_observation") is True, "map_no_override")

    deferred = [d.get("capability") for d in data["deferred"].get("deferred_capabilities") or [] if isinstance(d, dict)]
    ok(any("WorldModel runtime" in str(c) for c in deferred), "wm_deferred_list")

    p0 = data["roadmap"].get("p0_phases") or []
    ok("Voice-Dialogue-Task-Control-Contract-v1" in p0, "p0_voice")

    final = data["final"]
    ok(final.get("final_decision") == "BASIC_FUNCTIONAL_LOOP_STABILIZATION_PLAN_READY", "final")

    ok(data["boundary"].get("plan_only") is True, "plan_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["bench"].get("benchmark_score_generated") is False, "no_bench")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 63,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "Luna-Basic-Functional-Loop-Stabilization-Plan-v1-001",
    }
    _write_json(root / "luna_basic_loop_stabilization_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
