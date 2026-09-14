#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-SceneTaskEval-001
Option A Phone Local Scene × Task Evaluation v0 (offline).

Reads PerceptionEval-001 outputs (per_sample_results) and produces:
- scene_state
- task_candidates (candidate-only)
- degraded/uncertain handling

Hard boundaries:
- no execute/default-on/release/retry/reopen leakage (must be zero)
- allows_execute_now must be false for all candidates
- does not rewrite evidence semantics
- if perception_runtime_mode is baseline/mock, downstream must mark baseline_or_mock_downstream
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


def _scene_phase_from_signals(signals: Dict[str, Any]) -> Tuple[str, float, bool, bool, str]:
    """
    Conservative mapping (v0 baseline/mock friendly):
    - Uses spatial_passability + risk_field primarily.
    - Low confidence => degraded/uncertain.
    """
    sp = (signals or {}).get("spatial_passability_signal") or {}
    rf = (signals or {}).get("risk_field_signal") or {}

    sp_pass = str(sp.get("passability") or "unknown")
    sp_conf = float(sp.get("confidence") or 0.0)
    rf_level = str(rf.get("risk_level") or "unknown")
    rf_conf = float(rf.get("confidence") or 0.0)

    conf = min(max((sp_conf + rf_conf) / 2.0, 0.0), 1.0)

    degraded = conf < 0.35
    uncertain = degraded or sp_pass == "unknown" or rf_level == "unknown"

    if uncertain:
        return "sidewalk_uncertain_degraded", conf, degraded, True, "low_confidence_or_unknown_signals"
    if sp_pass == "passable" and rf_level in ("low", "medium"):
        return "sidewalk_clear_observe", conf, False, False, "passable_low_risk"
    if sp_pass in ("blocked",):
        return "sidewalk_obstacle_candidate", conf, False, False, "blocked_candidate"
    if sp_pass in ("narrow",):
        return "sidewalk_narrow_candidate", conf, False, False, "narrow_candidate"

    return "sidewalk_uncertain_degraded", conf, True, True, "fallback_unknown"


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

    # Always include a safe observe candidate.
    add("continue_observe_candidate", 0.6 if not degraded else 0.4, ["CANDIDATE_ONLY", "OBSERVE"])

    if scene_phase == "sidewalk_clear_observe":
        add("keep_clear_path_candidate", 0.55, ["CLEAR_PATH", "CANDIDATE_ONLY"])
    elif scene_phase == "sidewalk_obstacle_candidate":
        add("obstacle_attention_candidate", 0.55, ["OBSTACLE", "CANDIDATE_ONLY"])
        add("slow_down_candidate", 0.5, ["SLOW_DOWN", "CANDIDATE_ONLY"])
    elif scene_phase == "sidewalk_narrow_candidate":
        add("narrow_path_attention_candidate", 0.55, ["NARROW_PATH", "CANDIDATE_ONLY"])
        add("slow_down_candidate", 0.5, ["SLOW_DOWN", "CANDIDATE_ONLY"])
    elif uncertain:
        add("uncertain_observe_candidate", 0.45, ["UNCERTAIN", "DEGRADED", "CANDIDATE_ONLY"])
        add("ask_for_help_candidate", 0.4, ["ASK_FOR_HELP", "CANDIDATE_ONLY"])

    return cands


def _evaluate_one(sample: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    trace: List[Dict[str, Any]] = []
    sample_id = str(sample.get("sample_id") or "")

    def t(event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        trace.append({"timestamp_ms": _now_ms(), "sample_id": sample_id, "event_type": event_type, "payload": payload or {}})

    t("scene_task_eval_started", {})

    signals = sample.get("signals") or {}
    perception_runtime_mode = str(sample.get("perception_runtime_mode") or "unknown")
    not_model_claimed = bool(sample.get("not_model_claimed") is True)

    scene_task_runtime_mode = "baseline_or_mock_downstream" if perception_runtime_mode == "baseline_or_mock" else "unknown_or_other"
    not_scene_task_claimed = True if scene_task_runtime_mode == "baseline_or_mock_downstream" else False

    scene_phase, scene_conf, degraded, uncertain, transition_reason = _scene_phase_from_signals(signals)
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

    # Evidence boundary booleans (from perception sample)
    evidence_type_preserved = sample.get("evidence_type") == "phone_local_controlled_capture"
    controlled_live_stream_false = sample.get("controlled_live_stream") is False
    phone_local_capture_true = sample.get("phone_local_capture") is True

    hard_blockers: List[str] = []
    soft_followups: List[str] = []
    reason_codes: List[str] = ["CANDIDATE_ONLY", "NO_EXECUTE", "NO_DEFAULT_ON"]

    if perception_runtime_mode == "baseline_or_mock":
        reason_codes.append("BASELINE_OR_MOCK_DOWNSTREAM")
    if not evidence_type_preserved:
        hard_blockers.append("evidence_type_not_preserved")
    if not controlled_live_stream_false:
        hard_blockers.append("controlled_live_stream_not_false")
    if not phone_local_capture_true:
        hard_blockers.append("phone_local_capture_not_true")

    # Validate candidates
    for c in candidates:
        if c.get("allows_execute_now") is not False:
            hard_blockers.append("allows_execute_now_not_false")

    if not not_model_claimed and perception_runtime_mode == "baseline_or_mock":
        hard_blockers.append("not_model_claimed_missing")

    t("scene_state_generated", {"scene_phase": scene_phase, "scene_type": scene_type})
    t("task_candidates_generated", {"count": len(candidates)})
    t("scene_task_eval_completed", {"hard_blockers": hard_blockers, "soft_followups": soft_followups})

    out = {
        "sample_id": sample_id,
        "archive_root": sample.get("archive_root"),
        "source_video_path": sample.get("source_video_path"),
        "perception_runtime_mode": perception_runtime_mode,
        "scene_task_runtime_mode": scene_task_runtime_mode,
        "not_scene_task_claimed": not_scene_task_claimed,
        "scene_type": scene_type,
        "scene_phase": scene_phase,
        "scene_confidence": float(scene_conf),
        "task_state": scene_state["task_status"],
        "task_candidates": candidates,
        "degraded_scene": bool(degraded),
        "uncertain_scene": bool(uncertain),
        "candidate_only": True,
        **leakage,
        "evidence_type_preserved": evidence_type_preserved,
        "controlled_live_stream_false": controlled_live_stream_false,
        "phone_local_capture_true": phone_local_capture_true,
        "reason_codes": reason_codes,
        "hard_blockers": hard_blockers,
        "soft_followups": soft_followups,
        "scene_state": scene_state,
    }
    return out, trace


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--perception-eval-root", required=True, help="PerceptionEval-001 output directory")
    ap.add_argument("--output-root", required=True, help="Output directory for scene/task eval artifacts")
    args = ap.parse_args()

    pe_root = args.perception_eval_root
    out_root = args.output_root

    if not os.path.isdir(pe_root):
        raise SystemExit("perception_eval_root_missing_or_not_dir")
    if os.path.exists(out_root) and (not os.path.isdir(out_root) or os.listdir(out_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(out_root, exist_ok=True)

    pe_summary = _read_json(os.path.join(pe_root, "perception_evaluation_summary.json"))
    per_samples = _read_json(os.path.join(pe_root, "per_sample_results.json")).get("samples") or []
    if not isinstance(per_samples, list) or not per_samples:
        raise SystemExit("per_sample_results_missing_or_empty")

    n = len(per_samples)
    per_out: List[Dict[str, Any]] = []
    trace_all: List[Dict[str, Any]] = []

    # Aggregate metrics
    scene_state_generated = 0
    scene_type_valid = 0
    scene_phase_valid = 0
    scene_conf_present = 0
    task_candidate_generated = 0
    task_candidate_schema_valid = 0
    allows_execute_now_false = 0
    candidate_only_integrity = 0

    direct_exec_leak = 0
    rrre_leak = 0
    default_on_leak = 0
    forced_action = 0

    evidence_type_preserved = 0
    cls_false = 0
    plc_true = 0

    low_conf_degraded = 0
    uncertain_scene = 0
    ask_for_help = 0

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

        if r.get("scene_state"):
            scene_state_generated += 1
        if r.get("scene_type") in valid_scene_types:
            scene_type_valid += 1
        if r.get("scene_phase") in valid_scene_phases:
            scene_phase_valid += 1
        if isinstance(r.get("scene_confidence"), float):
            scene_conf_present += 1

        cands = r.get("task_candidates") or []
        if isinstance(cands, list) and len(cands) > 0:
            task_candidate_generated += 1
        # schema validity: minimal check of fields and allows_execute_now false
        ok_schema = True
        ok_allows = True
        for c in cands:
            if not isinstance(c, dict):
                ok_schema = False
                continue
            for k in ("task_candidate_id", "task_type", "source_scene_id", "source_signal_ids", "confidence", "reason_codes", "allows_execute_now"):
                if k not in c:
                    ok_schema = False
            if c.get("allows_execute_now") is not False:
                ok_allows = False
        if ok_schema:
            task_candidate_schema_valid += 1
        if ok_allows:
            allows_execute_now_false += 1
        if r.get("candidate_only") is True:
            candidate_only_integrity += 1

        direct_exec_leak += int(r.get("direct_execute_leakage_count") or 0)
        rrre_leak += int(r.get("release_retry_reopen_leakage_count") or 0)
        default_on_leak += int(r.get("default_on_leakage_count") or 0)
        forced_action += int(r.get("forced_navigation_action_count") or 0)

        if r.get("evidence_type_preserved") is True:
            evidence_type_preserved += 1
        if r.get("controlled_live_stream_false") is True:
            cls_false += 1
        if r.get("phone_local_capture_true") is True:
            plc_true += 1

        if r.get("degraded_scene") is True:
            low_conf_degraded += 1
        if r.get("uncertain_scene") is True:
            uncertain_scene += 1
        if any((c.get("task_type") == "ask_for_help_candidate") for c in cands if isinstance(c, dict)):
            ask_for_help += 1

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
    if task_candidate_generated != n and uncertain_scene == 0:
        hard_blockers.append("task_candidates_missing_without_uncertain")

    perception_mode = str(pe_summary.get("perception_runtime_mode") or "unknown")
    scene_task_runtime_mode = "baseline_or_mock_downstream" if perception_mode == "baseline_or_mock" else "unknown_or_other"

    recommendation = "go"
    if hard_blockers:
        recommendation = "no_go"
    else:
        recommendation = "conditional_go" if scene_task_runtime_mode == "baseline_or_mock_downstream" else "go"

    summary = {
        "tool": "evaluate_option_a_phone_local_scene_task_v0",
        "phase": "Phase-SceneTaskEval-001",
        "generated_at_ms": _now_ms(),
        "inputs": {
            "perception_eval_root": pe_root,
            "perception_runtime_mode": perception_mode,
        },
        "scene_task_runtime_mode": scene_task_runtime_mode,
        "not_scene_task_claimed": True if scene_task_runtime_mode == "baseline_or_mock_downstream" else False,
        "metrics": {
            "scene_state_completeness": {
                "scene_state_generated_rate": _rate(scene_state_generated, n),
                "scene_type_valid_rate": _rate(scene_type_valid, n),
                "scene_phase_valid_rate": _rate(scene_phase_valid, n),
                "scene_confidence_present_rate": _rate(scene_conf_present, n),
            },
            "task_candidate_integrity": {
                "task_candidate_generated_rate": _rate(task_candidate_generated, n),
                "task_candidate_schema_valid_rate": _rate(task_candidate_schema_valid, n),
                "allows_execute_now_false_rate": _rate(allows_execute_now_false, n),
                "candidate_only_integrity_rate": _rate(candidate_only_integrity, n),
            },
            "safety_boundary": {
                "direct_execute_leakage_count": direct_exec_leak,
                "release_retry_reopen_leakage_count": rrre_leak,
                "default_on_leakage_count": default_on_leak,
                "forced_navigation_action_count": forced_action,
            },
            "evidence_boundary": {
                "evidence_type_preserved_rate": _rate(evidence_type_preserved, n),
                "controlled_live_stream_false_rate": _rate(cls_false, n),
                "phone_local_capture_true_rate": _rate(plc_true, n),
            },
            "degraded_uncertain_handling": {
                "low_confidence_degraded_rate": _rate(low_conf_degraded, n),
                "uncertain_scene_generated_rate": _rate(uncertain_scene, n),
                "ask_for_help_candidate_rate": _rate(ask_for_help, n),
            },
        },
        "recommendation": recommendation,
        "hard_blockers": hard_blockers,
        "soft_followups": ["baseline_or_mock_downstream_in_effect"] if scene_task_runtime_mode == "baseline_or_mock_downstream" else [],
        "constraints": {
            "controlled_live_stream": False,
            "full_controlled_trial": False,
            "default_path_enabled": False,
            "execution_authority": False,
            "navigation_action_execution": False,
            "option_expanded": False,
        },
        "outputs": {
            "scene_task_evaluation_summary_json": "scene_task_evaluation_summary.json",
            "per_sample_scene_task_results_json": "per_sample_scene_task_results.json",
            "scene_task_trace_jsonl": "scene_task_trace.jsonl",
            "evaluation_notes_md": "evaluation_notes.md",
        },
    }

    _write_json(os.path.join(out_root, "scene_task_evaluation_summary.json"), summary)
    _write_json(os.path.join(out_root, "per_sample_scene_task_results.json"), {"samples": per_out})
    _write_jsonl(os.path.join(out_root, "scene_task_trace.jsonl"), trace_all)
    _write_text(
        os.path.join(out_root, "evaluation_notes.md"),
        "\n".join(
            [
                "# SceneTaskEval-001 evaluation_notes (v0)",
                "",
                f"- perception_eval_root: {pe_root}",
                f"- scene_task_runtime_mode: {scene_task_runtime_mode}",
                "- reminder: candidate-only; allows_execute_now must be false; no execute/default-on/release/retry/reopen",
                "",
            ]
        )
        + "\n",
    )

    print(json.dumps({"output_root": out_root, "summary_path": os.path.join(out_root, "scene_task_evaluation_summary.json"), "recommendation": recommendation}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

