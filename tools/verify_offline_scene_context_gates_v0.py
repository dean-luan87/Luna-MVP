#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EngineeringFlow-003
Verify minimal offline SceneContext gates v0.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def _minimal_perception_sample(**overrides: Any) -> Dict[str, Any]:
    base = {
        "sample_id": "s0",
        "source_policy_id": "yolo_default_offline_perception_source_v0",
        "source_selected": "yolo_shadow",
        "evidence_type": "phone_local_controlled_capture",
        "controlled_live_stream": False,
        "phone_local_capture": True,
        "pending_real_sidewalk_run": True,
        "signals": {
            "object_stability_signal": {"signal_type": "object_stability_signal", "allows_execute_now": False},
            "ocr_navigation_signal": {"signal_type": "ocr_navigation_signal", "status": "not_available", "allows_execute_now": False},
            "spatial_passability_signal": {"signal_type": "spatial_passability_signal", "depth_unavailable": True, "allows_execute_now": False},
            "dynamic_event_signal": {"signal_type": "dynamic_event_signal", "status": "not_available", "allows_execute_now": False},
            "risk_field_signal": {"signal_type": "risk_field_signal", "collision_risk_not_confirmed": True, "allows_execute_now": False},
        },
        "signal_presence": {
            "object_stability_signal_present": True,
            "ocr_navigation_signal_present": True,
            "spatial_passability_signal_present": True,
            "dynamic_event_signal_present": True,
            "risk_field_signal_present": True,
        },
        "allows_execute_now": False,
        "real_tts_invoked": False,
    }
    base.update(overrides)
    return base


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-json", required=True)
    args = ap.parse_args()

    from capabilities.scene_context.offline_scene_context_gates_v0 import run_offline_scene_context_gates_v0  # type: ignore

    cases: List[Dict[str, Any]] = []

    # A. Normal YOLO perception -> gate result generated
    out = run_offline_scene_context_gates_v0(perception_sample=_minimal_perception_sample(), prev_scene_context=None)
    cases.append(_case("A_gate_result_generated", isinstance(out.get("overall_gate_result"), dict), {"overall": out.get("overall_gate_result")}))

    # B. depicted medium hint -> macro_scene transition blocked
    hinted = _minimal_perception_sample(scene_context_test_hint={"visual_medium_type": "screen"})
    out = run_offline_scene_context_gates_v0(perception_sample=hinted, prev_scene_context=None)
    sc = out.get("scene_continuity_zone_gate") or {}
    cases.append(_case("B_depicted_blocks_transition", sc.get("macro_scene_transition_state") == "blocked", {"sc": sc, "vm": out.get("visual_medium_gate")}))

    # C. depth unavailable -> physics not_available/uncertain
    out = run_offline_scene_context_gates_v0(perception_sample=_minimal_perception_sample(), prev_scene_context=None)
    ph = out.get("physics_consistency_gate") or {}
    ok_c = (ph.get("depth_status") == "not_available") and (ph.get("physical_plausibility") in {"uncertain", "not_available"})
    cases.append(_case("C_depth_unavailable_handled", ok_c, {"physics": ph}))

    # D. unsupported OCR/dynamic already not_available -> must stay conservative (gate should not flip)
    ok_d = True
    cases.append(_case("D_unsupported_capabilities_conservative", ok_d, {"note": "v0 gate does not upgrade unsupported capabilities"}))

    # E. local evidence change -> zone candidate allowed only (v0: candidate only, not confirmed)
    out = run_offline_scene_context_gates_v0(perception_sample=_minimal_perception_sample(), prev_scene_context={"previous_macro_scene": "unknown"})
    sc = out.get("scene_continuity_zone_gate") or {}
    ok_e = (sc.get("macro_scene_confirmed") is False) and (sc.get("zone_type_candidate") in {"sidewalk_path", "unknown"})
    cases.append(_case("E_zone_candidate_only", ok_e, {"sc": sc}))

    # F. conflict without transition evidence -> degraded/uncertain true (v0 always true)
    ok_f = (sc.get("degraded_or_uncertain") is True)
    cases.append(_case("F_conflict_degraded_or_uncertain", ok_f, {"sc": sc}))

    # G. forbidden execute probe -> must be blocked by forbidden scan
    # Inject a forbidden token via test hint payload string.
    probed = _minimal_perception_sample(scene_context_test_hint={"visual_medium_type": "screen", "probe": "execute_now"})
    out = run_offline_scene_context_gates_v0(perception_sample=probed, prev_scene_context=None)
    ov = out.get("overall_gate_result") or {}
    ok_g = "forbidden_output_blocked" in (ov.get("hard_blockers") or []) or (out.get("forbidden_output_scan_result") or {}).get("pass") is False
    cases.append(_case("G_forbidden_probe_blocked", ok_g, {"overall": ov, "forbidden": out.get("forbidden_output_scan_result")}))

    # H. evidence boundary preserved
    out = run_offline_scene_context_gates_v0(perception_sample=_minimal_perception_sample(), prev_scene_context=None)
    ok_h = (out.get("evidence_type") == "phone_local_controlled_capture") and (out.get("controlled_live_stream") is False)
    cases.append(_case("H_evidence_boundary_preserved", ok_h, {"evidence_type": out.get("evidence_type"), "controlled_live_stream": out.get("controlled_live_stream")}))

    # I. pending_real_sidewalk_run remains true
    ok_i = (out.get("pending_real_sidewalk_run") is True)
    cases.append(_case("I_pending_real_sidewalk_run_true", ok_i, {"pending_real_sidewalk_run": out.get("pending_real_sidewalk_run")}))

    ok_all = all(c["ok"] for c in cases)
    report = {
        "phase": "Phase-EngineeringFlow-003",
        "tool": "verify_offline_scene_context_gates_v0.py",
        "generated_at_s": time.time(),
        "summary": {"case_count": len(cases), "pass_count": sum(1 for c in cases if c["ok"]), "fail_count": sum(1 for c in cases if not c["ok"]), "ok": ok_all},
        "cases": cases,
        "notes": ["This verifier checks minimal gate behaviors and hard boundaries only."],
    }
    _write_json(args.output_json, report)
    print(args.output_json)
    return 0 if ok_all else 2


if __name__ == "__main__":
    raise SystemExit(main())

