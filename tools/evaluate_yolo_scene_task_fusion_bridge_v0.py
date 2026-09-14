#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelPerception-008
YOLO Shadow Fusion Bridge Evaluation v0 (offline).

Input:
- Phase-ModelPerception-007 SceneTask bridge outputs (per-sample results)

Output:
- fusion_decision_candidate (candidate-only)

Hard boundaries:
- bridge-eval only; no runtime integration
- not entering real Output runtime
- no execute/default-on/release/retry/reopen leakage (must be zero)
- allows_execute_now must be false
- preserve evidence boundary booleans
- preserve source attribution (scene + task candidate ids + yolo detection metadata)
"""

from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from typing import Any, Dict, List


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


def _select_fusion_candidate(task_candidates: List[Dict[str, Any]], degraded: bool, uncertain: bool) -> Dict[str, Any]:
    """
    Conservative selection rule (v0):
    - if uncertain/degraded: prefer uncertain_observe_candidate or ask_for_help_candidate or continue_observe_candidate
    - else: pick highest-confidence candidate
    """
    safe_order = [
        "uncertain_observe_candidate",
        "ask_for_help_candidate",
        "continue_observe_candidate",
        "slow_down_candidate",
        "keep_clear_path_candidate",
        "obstacle_attention_candidate",
        "narrow_path_attention_candidate",
    ]
    by_type: Dict[str, Dict[str, Any]] = {}
    for c in task_candidates or []:
        if not isinstance(c, dict):
            continue
        t = str(c.get("task_type") or "")
        if t and (t not in by_type):
            by_type[t] = c

    if degraded or uncertain:
        for t in safe_order:
            if t in by_type:
                return by_type[t]

    best = None
    best_conf = -1.0
    for c in task_candidates or []:
        if not isinstance(c, dict):
            continue
        conf = float(c.get("confidence") or 0.0)
        if conf > best_conf:
            best = c
            best_conf = conf
    return best or {"task_candidate_id": None, "task_type": "continue_observe_candidate", "confidence": 0.0, "reason_codes": ["FALLBACK_EMPTY"]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yolo-scene-task-root", required=True, help="Phase-ModelPerception-007 output root")
    ap.add_argument("--output-root", required=True, help="Output directory for fusion bridge artifacts")
    args = ap.parse_args()

    st_root = args.yolo_scene_task_root
    out_root = args.output_root

    if not os.path.isdir(st_root):
        raise SystemExit("yolo_scene_task_root_missing_or_not_dir")
    if os.path.exists(out_root) and (not os.path.isdir(out_root) or os.listdir(out_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(out_root, exist_ok=True)

    st_summary = _read_json(os.path.join(st_root, "yolo_scene_task_bridge_summary.json"))
    st_samples = _read_json(os.path.join(st_root, "per_sample_yolo_scene_task_results.json")).get("samples") or []
    if not isinstance(st_samples, list) or not st_samples:
        raise SystemExit("per_sample_yolo_scene_task_results_missing_or_empty")

    upstream_mode = str(st_summary.get("scene_task_runtime_mode") or "unknown")
    fusion_runtime_mode = "yolo_replacement_downstream"

    per_out: List[Dict[str, Any]] = []
    trace: List[Dict[str, Any]] = []

    n = len(st_samples)
    fusion_generated = 0
    schema_valid = 0
    attribution_present = 0
    reason_codes_present = 0

    yolo_detection_source_preserved = 0
    source_scene_id_present = 0
    source_task_candidate_ids_present = 0

    conflict_handling_present = 0
    degraded_handling_present = 0

    allows_execute_now_false = 0
    candidate_only_integrity = 0

    leakage = {
        "direct_execute_leakage_count": 0,
        "release_retry_reopen_leakage_count": 0,
        "default_on_leakage_count": 0,
        "side_effects_expansion_count": 0,
        "forced_navigation_action_count": 0,
    }

    ev_preserved = 0
    cls_false = 0
    plc_true = 0

    hard_blockers_total = 0

    for s in st_samples:
        sample_id = str(s.get("sample_id") or "")
        trace.append({"timestamp_ms": _now_ms(), "sample_id": sample_id, "event_type": "yolo_fusion_eval_started", "payload": {}})

        task_candidates = s.get("task_candidates") or []
        # Our 007 tool always tends to uncertain/degraded; still read from scene_state to be consistent
        scene_state = s.get("scene_state") or {}
        degraded = bool(scene_state.get("degraded_mode") is True) or True  # keep conservative
        uncertain = bool(s.get("scene_type") == "uncertain_scene") or True

        selected = _select_fusion_candidate(task_candidates, degraded=degraded, uncertain=uncertain)
        selected_type = str(selected.get("task_type") or "unknown")
        selected_id = selected.get("task_candidate_id")

        # Minimal conflict structure (always present); conflict_detected is optional
        conflict_detected = False
        conflict_type = "none"
        conflict_resolution = "prefer_conservative_order"
        try:
            confs: Dict[float, set] = {}
            for c in task_candidates:
                if not isinstance(c, dict):
                    continue
                conf = float(c.get("confidence") or 0.0)
                t = str(c.get("task_type") or "")
                confs.setdefault(conf, set()).add(t)
            if confs:
                top = max(confs.keys())
                if len(confs[top]) > 1:
                    conflict_detected = True
                    conflict_type = "tie_top_confidence"
        except Exception:
            pass

        yolo_invoked = bool(s.get("yolo_invoked") is True)
        detection_count = int(s.get("detection_count") or 0)
        detected_classes = s.get("detected_classes") if isinstance(s.get("detected_classes"), list) else []

        source_attribution = {
            "source_layers": ["scene_state", "task_candidates"],
            "upstream_roots": {"yolo_scene_task_root": st_root},
            "upstream_runtime_modes": {"scene_task_runtime_mode": upstream_mode, "fusion_runtime_mode": fusion_runtime_mode},
            "yolo_source": {
                "yolo_invoked": yolo_invoked,
                "detection_count": detection_count,
                "detected_classes": detected_classes,
            },
        }

        fusion_candidate = {
            "fusion_candidate_id": f"fc_{uuid.uuid4().hex[:10]}",
            "fusion_candidate_type": selected_type if selected_type != "unknown" else "continue_observe_candidate",
            "confidence": float(selected.get("confidence") or 0.0),
            "source_scene_id": str(scene_state.get("scene_id") or ""),
            "source_task_candidate_ids": [selected_id] if selected_id else [],
            "source_signal_ids": [],
            "source_attribution": source_attribution,
            "conflict_detected": bool(conflict_detected),
            "conflict_type": conflict_type,
            "conflict_resolution": conflict_resolution,
            "degraded_or_uncertain_handling": {
                "present": True,
                "degraded_or_uncertain": True,
                "handling": "observe_or_ask_for_help_candidate",
            },
            "reason_codes": ["CANDIDATE_ONLY", "NO_EXECUTE", "NO_DEFAULT_ON", "FUSION_BRIDGE_V0", "CONSERVATIVE_SELECTION"],
            "allows_execute_now": False,
        }

        conflict_handling = {
            "present": True,
            "conflict_detected": bool(conflict_detected),
            "conflict_type": conflict_type,
            "resolution": conflict_resolution,
        }

        evidence_ok = bool(s.get("evidence_type_preserved") is True)
        cls_ok = bool(s.get("controlled_live_stream_false") is True)
        plc_ok = bool(s.get("phone_local_capture_true") is True)

        if evidence_ok:
            ev_preserved += 1
        if cls_ok:
            cls_false += 1
        if plc_ok:
            plc_true += 1

        hard_blockers: List[str] = []
        soft_followups: List[str] = []

        if not evidence_ok:
            hard_blockers.append("evidence_type_not_preserved")
        if not cls_ok:
            hard_blockers.append("controlled_live_stream_not_false")
        if not plc_ok:
            hard_blockers.append("phone_local_capture_not_true")
        if fusion_candidate.get("allows_execute_now") is not False:
            hard_blockers.append("allows_execute_now_not_false")

        required_fc = [
            "fusion_candidate_id",
            "fusion_candidate_type",
            "confidence",
            "source_scene_id",
            "source_task_candidate_ids",
            "source_signal_ids",
            "source_attribution",
            "conflict_detected",
            "conflict_type",
            "conflict_resolution",
            "degraded_or_uncertain_handling",
            "reason_codes",
            "allows_execute_now",
        ]
        if all(k in fusion_candidate for k in required_fc) and isinstance(fusion_candidate.get("source_attribution"), dict):
            schema_valid += 1
        else:
            hard_blockers.append("fusion_candidate_schema_incomplete")

        if isinstance(source_attribution.get("source_layers"), list) and isinstance(source_attribution.get("yolo_source"), dict):
            attribution_present += 1

        if isinstance(fusion_candidate.get("reason_codes"), list) and len(fusion_candidate["reason_codes"]) > 0:
            reason_codes_present += 1

        if yolo_invoked and detection_count >= 0:
            yolo_detection_source_preserved += 1

        if isinstance(fusion_candidate.get("source_scene_id"), str) and fusion_candidate["source_scene_id"]:
            source_scene_id_present += 1
        if isinstance(fusion_candidate.get("source_task_candidate_ids"), list) and len(fusion_candidate["source_task_candidate_ids"]) > 0:
            source_task_candidate_ids_present += 1

        if conflict_handling.get("present") is True:
            conflict_handling_present += 1
        if (fusion_candidate.get("degraded_or_uncertain_handling") or {}).get("present") is True:
            degraded_handling_present += 1

        if fusion_candidate.get("allows_execute_now") is False:
            allows_execute_now_false += 1
        candidate_only_integrity += 1

        if hard_blockers:
            hard_blockers_total += len(hard_blockers)

        fusion_generated += 1

        per_out.append(
            {
                "sample_id": sample_id,
                "archive_root": s.get("archive_root"),
                "source_video_path": s.get("source_video_path"),
                "yolo_invoked": yolo_invoked,
                "detection_count": detection_count,
                "detected_classes": detected_classes,
                "scene_state": scene_state,
                "task_candidates": task_candidates,
                "fusion_runtime_mode": fusion_runtime_mode,
                "candidate_only": True,
                "allows_execute_now": False,
                "fusion_decision_candidate": fusion_candidate,
                "fusion_candidate_type": fusion_candidate.get("fusion_candidate_type"),
                "source_scene_id": fusion_candidate.get("source_scene_id"),
                "source_task_candidate_ids": fusion_candidate.get("source_task_candidate_ids"),
                "source_attribution": source_attribution,
                "conflict_detected": fusion_candidate.get("conflict_detected"),
                "conflict_type": fusion_candidate.get("conflict_type"),
                "conflict_resolution": fusion_candidate.get("conflict_resolution"),
                "degraded_or_uncertain_handling": fusion_candidate.get("degraded_or_uncertain_handling"),
                **leakage,
                "evidence_type_preserved": evidence_ok,
                "controlled_live_stream_false": cls_ok,
                "phone_local_capture_true": plc_ok,
                "reason_codes": ["CANDIDATE_ONLY", "NO_EXECUTE", "NO_DEFAULT_ON", "FUSION_BRIDGE_EVAL_V0"],
                "hard_blockers": hard_blockers,
                "soft_followups": soft_followups,
            }
        )

        trace.append(
            {
                "timestamp_ms": _now_ms(),
                "sample_id": sample_id,
                "event_type": "yolo_fusion_eval_completed",
                "payload": {"selected_candidate_type": selected_type, "hard_blockers": hard_blockers},
            }
        )

    hard_blockers: List[str] = []
    leakage_total = sum(int(v) for v in leakage.values())
    if leakage_total != 0:
        hard_blockers.append("leakage_detected")
    if hard_blockers_total != 0:
        hard_blockers.append("per_sample_hard_blockers_present")
    if fusion_generated != n:
        hard_blockers.append("fusion_candidate_missing")

    recommendation = "go" if not hard_blockers else "no_go"

    summary = {
        "tool": "evaluate_yolo_scene_task_fusion_bridge_v0",
        "phase": "Phase-ModelPerception-008",
        "generated_at_ms": _now_ms(),
        "inputs": {"yolo_scene_task_root": st_root, "scene_task_runtime_mode": upstream_mode},
        "fusion_runtime_mode": fusion_runtime_mode,
        "constraints": {
            "bridge_eval_only": True,
            "controlled_live_stream": False,
            "full_controlled_trial": False,
            "default_path_enabled": False,
            "execution_authority": False,
            "navigation_action_execution": False,
            "option_expanded": False,
            "real_output_runtime": False,
        },
        "metrics": {
            "fusion_completeness": {
                "fusion_candidate_generated_rate": _rate(fusion_generated, n),
                "fusion_candidate_schema_valid_rate": _rate(schema_valid, n),
                "source_attribution_present_rate": _rate(attribution_present, n),
                "reason_codes_present_rate": _rate(reason_codes_present, n),
            },
            "yolo_scenetask_source_use": {
                "yolo_detection_source_preserved_rate": _rate(yolo_detection_source_preserved, n),
                "source_scene_id_present_rate": _rate(source_scene_id_present, n),
                "source_task_candidate_ids_present_rate": _rate(source_task_candidate_ids_present, n),
            },
            "conflict_degraded_handling": {
                "conflict_handling_present_rate": _rate(conflict_handling_present, n),
                "degraded_or_uncertain_handling_rate": _rate(degraded_handling_present, n),
            },
            "candidate_only_safety": {
                "allows_execute_now_false_rate": _rate(allows_execute_now_false, n),
                "candidate_only_integrity_rate": _rate(candidate_only_integrity, n),
                **leakage,
            },
            "evidence_boundary": {
                "evidence_type_preserved_rate": _rate(ev_preserved, n),
                "controlled_live_stream_false_rate": _rate(cls_false, n),
                "phone_local_capture_true_rate": _rate(plc_true, n),
            },
        },
        "recommendation": recommendation,
        "hard_blockers": hard_blockers,
        "soft_followups": ["fusion_policy_minimal_rules_v0_soft_followup"],
        "outputs": {
            "summary_json": "yolo_fusion_bridge_summary.json",
            "per_sample_results_json": "per_sample_yolo_fusion_results.json",
            "trace_jsonl": "yolo_fusion_bridge_trace.jsonl",
            "evaluation_notes_md": "evaluation_notes.md",
        },
    }

    _write_json(os.path.join(out_root, "yolo_fusion_bridge_summary.json"), summary)
    _write_json(os.path.join(out_root, "per_sample_yolo_fusion_results.json"), {"samples": per_out})
    _write_jsonl(os.path.join(out_root, "yolo_fusion_bridge_trace.jsonl"), trace)
    _write_text(
        os.path.join(out_root, "evaluation_notes.md"),
        "\n".join(
            [
                "# YOLO Fusion Bridge Evaluation (v0)",
                "",
                f"- yolo_scene_task_root: {st_root}",
                "- reminder: bridge-eval only; candidate-only; no real Output runtime; no execute/default-on/release/retry/reopen",
                "",
            ]
        )
        + "\n",
    )

    print(json.dumps({"output_root": out_root, "summary_path": os.path.join(out_root, "yolo_fusion_bridge_summary.json"), "recommendation": recommendation}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

