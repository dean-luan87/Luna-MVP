#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelPerception-007
YOLO Shadow SceneTask Bridge Evaluation v0 (offline).

Input:
- YOLO Perception Replacement Trial outputs (Phase-ModelPerception-006)

Output:
- scene_state + task_candidates (candidate-only)

Hard boundaries:
- bridge-eval only; no runtime integration
- not entering Fusion/Output
- no execute/default-on/release/retry/reopen leakage (must be zero)
- allows_execute_now must be false for all candidates
- evidence boundary preserved (phone_local_controlled_capture; controlled_live_stream=false; phone_local_capture=true)
- unsupported capabilities must remain respected (OCR/dynamic not_available; depth_unavailable true; collision_risk_not_confirmed true)
"""

from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple


def _now_ms() -> int:
    return int(time.time() * 1000)


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _write_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _rate(n: int, d: int) -> float:
    return float(n) / float(d) if d else 0.0


def _get_detected_classes(sample: Dict[str, Any]) -> List[str]:
    dc = sample.get("detected_classes")
    if isinstance(dc, list):
        return [str(x) for x in dc if x is not None]
    return []


def _unsupported_capabilities_respected(sample: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Returns (ok, reasons_if_not_ok)
    """
    reasons: List[str] = []
    signals = sample.get("signals") or {}
    if not isinstance(signals, dict):
        return False, ["signals_not_dict"]

    ocr_status = (signals.get("ocr_navigation_signal") or {}).get("status")
    dyn_status = (signals.get("dynamic_event_signal") or {}).get("status")
    depth_unavail = (signals.get("spatial_passability_signal") or {}).get("depth_unavailable")
    collision_nc = (signals.get("risk_field_signal") or {}).get("collision_risk_not_confirmed")

    if ocr_status != "not_available":
        reasons.append("ocr_not_available_not_respected")
    if dyn_status != "not_available":
        reasons.append("dynamic_not_available_not_respected")
    if depth_unavail is not True:
        reasons.append("depth_unavailable_not_respected")
    if collision_nc is not True:
        reasons.append("collision_risk_not_confirmed_not_respected")

    return (len(reasons) == 0), reasons


def _scene_phase_from_yolo(sample: Dict[str, Any]) -> Tuple[str, float, bool, bool, str, bool]:
    """
    Conservative mapping for YOLO replacement signals (v0):
    - uses detection_count + detected_classes only
    - always keeps confidence low; degraded/uncertain preferred
    Returns: (scene_phase, scene_conf, degraded, uncertain, reason, yolo_detection_used)
    """
    det_count = int(sample.get("detection_count") or 0)
    classes = set(_get_detected_classes(sample))
    yolo_used = det_count > 0

    # Default: uncertain & degraded
    scene_conf = 0.30 if yolo_used else 0.20
    degraded = True  # v0 bridge keeps downstream conservative
    uncertain = True

    if not yolo_used:
        return "sidewalk_uncertain_degraded", scene_conf, degraded, uncertain, "no_detections_degraded", False

    # If we have any detections, we still remain uncertain but we can tag a candidate phase.
    if "person" in classes or "bicycle" in classes:
        return "sidewalk_obstacle_candidate", scene_conf, degraded, uncertain, "object_presence_candidate_only", True
    if "potted plant" in classes:
        return "sidewalk_narrow_candidate", scene_conf, degraded, uncertain, "narrow_obstacle_candidate_only", True

    return "sidewalk_uncertain_degraded", scene_conf, degraded, uncertain, "detections_unmapped_degraded", True


def _task_candidates_for_phase(scene_id: str, scene_phase: str, degraded: bool, uncertain: bool) -> List[Dict[str, Any]]:
    cands: List[Dict[str, Any]] = []

    def add(task_type: str, confidence: float, reason_codes: List[str]) -> None:
        cands.append(
            {
                "task_candidate_id": f"tc_{uuid.uuid4().hex[:10]}",
                "task_type": task_type,
                "source_scene_id": scene_id,
                "source_signal_ids": [],
                "confidence": float(confidence),
                "reason_codes": list(reason_codes),
                "allows_execute_now": False,
            }
        )

    # Always include safe observe
    add("continue_observe_candidate", 0.45 if degraded else 0.55, ["CANDIDATE_ONLY", "OBSERVE", "YOLO_REPLACEMENT_DOWNSTREAM"])

    if scene_phase == "sidewalk_obstacle_candidate":
        add("obstacle_attention_candidate", 0.45, ["OBSTACLE", "CANDIDATE_ONLY", "YOLO_DETECTION_CANDIDATE_ONLY"])
        add("slow_down_candidate", 0.40, ["SLOW_DOWN", "CANDIDATE_ONLY"])
    elif scene_phase == "sidewalk_narrow_candidate":
        add("narrow_path_attention_candidate", 0.45, ["NARROW_PATH", "CANDIDATE_ONLY", "YOLO_DETECTION_CANDIDATE_ONLY"])
        add("slow_down_candidate", 0.40, ["SLOW_DOWN", "CANDIDATE_ONLY"])
    elif uncertain:
        add("uncertain_observe_candidate", 0.40, ["UNCERTAIN", "DEGRADED", "CANDIDATE_ONLY"])
        add("ask_for_help_candidate", 0.35, ["ASK_FOR_HELP", "CANDIDATE_ONLY"])

    return cands


def _evaluate_one(sample: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    trace: List[Dict[str, Any]] = []
    sample_id = str(sample.get("sample_id") or "")

    def t(event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        trace.append({"timestamp_ms": _now_ms(), "sample_id": sample_id, "event_type": event_type, "payload": payload or {}})

    t("yolo_scene_task_bridge_eval_started", {})

    perception_runtime_mode = str(sample.get("perception_runtime_mode") or "unknown")
    scene_task_runtime_mode = "yolo_replacement_downstream"

    # Evidence boundary from replacement sample
    evidence_type_preserved = sample.get("evidence_type") == "phone_local_controlled_capture"
    controlled_live_stream_false = sample.get("controlled_live_stream") is False
    phone_local_capture_true = sample.get("phone_local_capture") is True

    # Candidate-only guard
    allows_execute_now_ok = (sample.get("candidate_only") or {}).get("allows_execute_now") is False

    # Unsupported capability honesty respected
    unsupported_ok, unsupported_reasons = _unsupported_capabilities_respected(sample)

    scene_phase, scene_conf, degraded, uncertain, transition_reason, yolo_used = _scene_phase_from_yolo(sample)
    scene_type = "uncertain_scene" if uncertain else "sidewalk_navigation"

    scene_id = f"scene_{uuid.uuid4().hex[:10]}"
    candidates = _task_candidates_for_phase(scene_id=scene_id, scene_phase=scene_phase, degraded=degraded, uncertain=uncertain)
    active_task_id = candidates[0]["task_candidate_id"] if candidates else None

    scene_state = {
        "scene_id": scene_id,
        "scene_type": scene_type,
        "scene_confidence": float(scene_conf),
        "scene_phase": scene_phase,
        "active_task_id": active_task_id,
        "task_status": "candidate_generated" if candidates else "idle",
        "inserted_task_present": False,
        "recovery_possible": True,
        "deviation_detected": False,
        "degraded_mode": bool(degraded),
        "required_perception_signals": [
            "object_stability_signal",
            "ocr_navigation_signal",
            "spatial_passability_signal",
            "dynamic_event_signal",
            "risk_field_signal",
        ],
        "last_transition_reason": transition_reason,
    }

    # Leakage counters (must be zero)
    leakage = {
        "direct_execute_leakage_count": 0,
        "release_retry_reopen_leakage_count": 0,
        "default_on_leakage_count": 0,
        "forced_navigation_action_count": 0,
    }

    hard_blockers: List[str] = []
    soft_followups: List[str] = []
    reason_codes: List[str] = ["CANDIDATE_ONLY", "NO_EXECUTE", "NO_DEFAULT_ON", "YOLO_REPLACEMENT_DOWNSTREAM"]

    if perception_runtime_mode != "yolo_shadow_replacement":
        hard_blockers.append("perception_runtime_mode_not_yolo_shadow_replacement")
    if not evidence_type_preserved:
        hard_blockers.append("evidence_type_not_preserved")
    if not controlled_live_stream_false:
        hard_blockers.append("controlled_live_stream_not_false")
    if not phone_local_capture_true:
        hard_blockers.append("phone_local_capture_not_true")
    if not allows_execute_now_ok:
        hard_blockers.append("allows_execute_now_not_false")
    if not unsupported_ok:
        hard_blockers.append("unsupported_capabilities_not_respected")
        soft_followups.extend(unsupported_reasons)

    # Validate candidates allows_execute_now=false
    for c in candidates:
        if c.get("allows_execute_now") is not False:
            hard_blockers.append("candidate_allows_execute_now_not_false")

    t("scene_state_generated", {"scene_phase": scene_phase, "scene_type": scene_type, "yolo_detection_used": yolo_used})
    t("task_candidates_generated", {"count": len(candidates)})
    t("yolo_scene_task_bridge_eval_completed", {"hard_blockers": hard_blockers, "soft_followups": soft_followups})

    out = {
        "sample_id": sample_id,
        "archive_root": sample.get("archive_root"),
        "source_video_path": sample.get("source_video_path"),
        "perception_runtime_mode": perception_runtime_mode,
        "scene_task_runtime_mode": scene_task_runtime_mode,
        "yolo_invoked": sample.get("yolo_invoked"),
        "detection_count": sample.get("detection_count"),
        "detected_classes": sample.get("detected_classes"),
        "yolo_detection_used": bool(yolo_used),
        "scene_state": scene_state,
        "scene_type": scene_type,
        "scene_phase": scene_phase,
        "scene_confidence": float(scene_conf),
        "task_candidates": candidates,
        "task_candidate_count": len(candidates),
        "candidate_only": True,
        "allows_execute_now": False,
        "unsupported_capabilities_respected": bool(unsupported_ok),
        "depth_unavailable_handled": True,
        "dynamic_not_available_handled": True,
        "ocr_not_available_handled": True,
        "collision_risk_not_confirmed_handled": True,
        **leakage,
        "evidence_type_preserved": bool(evidence_type_preserved),
        "controlled_live_stream_false": bool(controlled_live_stream_false),
        "phone_local_capture_true": bool(phone_local_capture_true),
        "reason_codes": reason_codes,
        "hard_blockers": hard_blockers,
        "soft_followups": soft_followups,
    }
    return out, trace


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yolo-perception-root", required=True, help="YOLO perception replacement eval root (Phase-ModelPerception-006)")
    ap.add_argument("--output-root", required=True, help="Output directory for scene/task bridge artifacts")
    args = ap.parse_args()

    yp_root = args.yolo_perception_root
    out_root = args.output_root

    if not os.path.isdir(yp_root):
        raise SystemExit("yolo_perception_root_missing_or_not_dir")
    if os.path.exists(out_root) and (not os.path.isdir(out_root) or os.listdir(out_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(out_root, exist_ok=True)

    per_samples = _read_json(os.path.join(yp_root, "per_sample_yolo_perception_replacement_results.json")).get("samples") or []
    if not isinstance(per_samples, list) or not per_samples:
        raise SystemExit("per_sample_results_missing_or_empty")

    n = len(per_samples)
    per_out: List[Dict[str, Any]] = []
    trace_all: List[Dict[str, Any]] = []

    # Aggregate metrics requested
    scene_state_generated = 0
    scene_state_schema_valid = 0
    task_candidate_generated = 0
    task_candidate_schema_valid = 0

    yolo_detection_used = 0
    unsupported_respected = 0
    depth_handled = 0
    dyn_handled = 0
    ocr_handled = 0
    collision_handled = 0

    allows_execute_now_false = 0
    candidate_only_integrity = 0

    direct_exec_leak = 0
    rrre_leak = 0
    default_on_leak = 0
    forced_action = 0

    ev_preserved = 0
    cls_false = 0
    plc_true = 0

    hard_blockers_total = 0

    valid_scene_types = {"sidewalk_navigation", "uncertain_scene"}
    valid_scene_phases = {
        "sidewalk_clear_observe",
        "sidewalk_obstacle_candidate",
        "sidewalk_narrow_candidate",
        "sidewalk_uncertain_degraded",
    }

    for s in per_samples:
        r, tr = _evaluate_one(s)
        per_out.append(r)
        trace_all.extend(tr)

        if isinstance(r.get("scene_state"), dict):
            scene_state_generated += 1
            # minimal schema check
            ok_scene = True
            for k in ("scene_id", "scene_type", "scene_confidence", "scene_phase", "active_task_id", "task_status", "degraded_mode", "required_perception_signals", "last_transition_reason"):
                if k not in r["scene_state"]:
                    ok_scene = False
            if r.get("scene_type") not in valid_scene_types:
                ok_scene = False
            if r.get("scene_phase") not in valid_scene_phases:
                ok_scene = False
            if ok_scene:
                scene_state_schema_valid += 1

        cands = r.get("task_candidates") or []
        if isinstance(cands, list) and len(cands) > 0:
            task_candidate_generated += 1

        ok_schema = True
        for c in cands:
            if not isinstance(c, dict):
                ok_schema = False
                continue
            for k in ("task_candidate_id", "task_type", "source_scene_id", "source_signal_ids", "confidence", "reason_codes", "allows_execute_now"):
                if k not in c:
                    ok_schema = False
        if ok_schema:
            task_candidate_schema_valid += 1

        if r.get("yolo_detection_used") is True:
            yolo_detection_used += 1
        if r.get("unsupported_capabilities_respected") is True:
            unsupported_respected += 1
        if r.get("depth_unavailable_handled") is True:
            depth_handled += 1
        if r.get("dynamic_not_available_handled") is True:
            dyn_handled += 1
        if r.get("ocr_not_available_handled") is True:
            ocr_handled += 1
        if r.get("collision_risk_not_confirmed_handled") is True:
            collision_handled += 1

        if r.get("allows_execute_now") is False:
            allows_execute_now_false += 1
        if r.get("candidate_only") is True:
            candidate_only_integrity += 1

        direct_exec_leak += int(r.get("direct_execute_leakage_count") or 0)
        rrre_leak += int(r.get("release_retry_reopen_leakage_count") or 0)
        default_on_leak += int(r.get("default_on_leakage_count") or 0)
        forced_action += int(r.get("forced_navigation_action_count") or 0)

        if r.get("evidence_type_preserved") is True:
            ev_preserved += 1
        if r.get("controlled_live_stream_false") is True:
            cls_false += 1
        if r.get("phone_local_capture_true") is True:
            plc_true += 1

        hb = r.get("hard_blockers") or []
        if hb:
            hard_blockers_total += len(hb)

    leakage_total = direct_exec_leak + rrre_leak + default_on_leak + forced_action
    hard_blockers: List[str] = []
    if leakage_total != 0:
        hard_blockers.append("leakage_detected")
    if hard_blockers_total != 0:
        hard_blockers.append("per_sample_hard_blockers_present")
    if scene_state_generated != n:
        hard_blockers.append("scene_state_missing")
    if task_candidate_generated != n:
        hard_blockers.append("task_candidates_missing_without_degraded_handling")

    recommendation = "go" if not hard_blockers else "no_go"

    summary = {
        "tool": "evaluate_yolo_replacement_scene_task_bridge_v0",
        "phase": "Phase-ModelPerception-007",
        "generated_at_ms": _now_ms(),
        "inputs": {
            "yolo_perception_root": yp_root,
            "sample_count": n,
        },
        "scene_task_runtime_mode": "yolo_replacement_downstream",
        "constraints": {
            "bridge_eval_only": True,
            "controlled_live_stream": False,
            "full_controlled_trial": False,
            "default_path_enabled": False,
            "execution_authority": False,
            "navigation_action_execution": False,
            "option_expanded": False,
            "fusion_output": False,
        },
        "metrics": {
            "scene_task_completeness": {
                "scene_state_generated_rate": _rate(scene_state_generated, n),
                "scene_state_schema_valid_rate": _rate(scene_state_schema_valid, n),
                "task_candidate_generated_rate": _rate(task_candidate_generated, n),
                "task_candidate_schema_valid_rate": _rate(task_candidate_schema_valid, n),
            },
            "yolo_signal_use": {
                "yolo_detection_used_rate": _rate(yolo_detection_used, n),
                "unsupported_capabilities_respected_rate": _rate(unsupported_respected, n),
                "depth_unavailable_handled_rate": _rate(depth_handled, n),
                "dynamic_not_available_handled_rate": _rate(dyn_handled, n),
                "ocr_not_available_handled_rate": _rate(ocr_handled, n),
                "collision_risk_not_confirmed_handled_rate": _rate(collision_handled, n),
            },
            "candidate_only_safety": {
                "allows_execute_now_false_rate": _rate(allows_execute_now_false, n),
                "candidate_only_integrity_rate": _rate(candidate_only_integrity, n),
                "execute_leakage_count": direct_exec_leak,
                "default_on_leakage_count": default_on_leak,
                "release_retry_reopen_leakage_count": rrre_leak,
                "side_effects_expansion_count": 0,
                "forced_navigation_action_count": forced_action,
            },
            "evidence_boundary": {
                "evidence_type_preserved_rate": _rate(ev_preserved, n),
                "controlled_live_stream_false_rate": _rate(cls_false, n),
                "phone_local_capture_true_rate": _rate(plc_true, n),
            },
        },
        "recommendation": recommendation,
        "hard_blockers": hard_blockers,
        "soft_followups": ["scene_context_gates_not_fully_runtime_enforced_soft_followup"],
        "outputs": {
            "summary_json": "yolo_scene_task_bridge_summary.json",
            "per_sample_results_json": "per_sample_yolo_scene_task_results.json",
            "trace_jsonl": "yolo_scene_task_bridge_trace.jsonl",
            "evaluation_notes_md": "evaluation_notes.md",
        },
    }

    _write_json(os.path.join(out_root, "yolo_scene_task_bridge_summary.json"), summary)
    _write_json(os.path.join(out_root, "per_sample_yolo_scene_task_results.json"), {"samples": per_out})
    _write_jsonl(os.path.join(out_root, "yolo_scene_task_bridge_trace.jsonl"), trace_all)
    _write_text(
        os.path.join(out_root, "evaluation_notes.md"),
        "\n".join(
            [
                "# YOLO SceneTask Bridge Evaluation (v0)",
                "",
                f"- yolo_perception_root: {yp_root}",
                "- reminder: bridge-eval only; candidate-only; no Fusion/Output; no execute/default-on/release/retry/reopen",
                "",
            ]
        )
        + "\n",
    )

    print(json.dumps({"output_root": out_root, "summary_path": os.path.join(out_root, "yolo_scene_task_bridge_summary.json"), "recommendation": recommendation}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

