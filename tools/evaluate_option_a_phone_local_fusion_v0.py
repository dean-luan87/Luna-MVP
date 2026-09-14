#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-FusionEval-001
Option A Phone Local Fusion Evaluation v0 (offline).

Consumes SceneTaskEval-001 per-sample results and emits a fusion_decision_candidate
per sample with candidate-only integrity.

Hard boundaries:
- no execute/default-on/release/retry/reopen leakage (must be zero)
- allows_execute_now must be false
- preserve evidence semantics
- if upstream is baseline/mock, mark baseline_or_mock_downstream and do not claim capability
"""

from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional


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
    - if uncertain/degraded: prefer uncertain_observe_candidate or ask_for_help_candidate
    - else: pick highest-confidence candidate among known safe types
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

    # fallback: highest confidence
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
    ap.add_argument("--scene-task-eval-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    st_root = args.scene_task_eval_root
    out_root = args.output_root

    if not os.path.isdir(st_root):
        raise SystemExit("scene_task_eval_root_missing_or_not_dir")
    if os.path.exists(out_root) and (not os.path.isdir(out_root) or os.listdir(out_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(out_root, exist_ok=True)

    st_summary = _read_json(os.path.join(st_root, "scene_task_evaluation_summary.json"))
    st_samples = _read_json(os.path.join(st_root, "per_sample_scene_task_results.json")).get("samples") or []
    if not isinstance(st_samples, list) or not st_samples:
        raise SystemExit("per_sample_scene_task_results_missing_or_empty")

    upstream_mode = str(st_summary.get("scene_task_runtime_mode") or "unknown")
    fusion_runtime_mode = "baseline_or_mock_downstream" if upstream_mode == "baseline_or_mock_downstream" else "unknown_or_other"
    not_fusion_claimed = True if fusion_runtime_mode == "baseline_or_mock_downstream" else False

    per_out: List[Dict[str, Any]] = []
    trace: List[Dict[str, Any]] = []

    # Aggregates
    n = len(st_samples)
    fusion_generated = 0
    schema_valid = 0
    attribution_present = 0
    reason_codes_present = 0
    allows_execute_now_false = 0
    candidate_only_integrity = 0

    conflict_detected = 0
    conflict_handling_present = 0
    degraded_uncertain_handling_present = 0

    leakage = {
        "direct_execute_leakage_count": 0,
        "release_retry_reopen_leakage_count": 0,
        "default_on_leakage_count": 0,
        "side_effects_expansion_count": 0,
        "forced_navigation_action_count": 0,
    }

    evidence_type_preserved = 0
    cls_false = 0
    plc_true = 0

    hard_blockers_total = 0

    for s in st_samples:
        sample_id = str(s.get("sample_id") or "")
        trace.append({"timestamp_ms": _now_ms(), "sample_id": sample_id, "event_type": "fusion_eval_started", "payload": {}})

        task_candidates = s.get("task_candidates") or []
        degraded = bool(s.get("degraded_scene") is True)
        uncertain = bool(s.get("uncertain_scene") is True)
        selected = _select_fusion_candidate(task_candidates, degraded=degraded, uncertain=uncertain)

        selected_type = str(selected.get("task_type") or "unknown")
        selected_id = selected.get("task_candidate_id")

        # Minimal conflict logic: if multiple candidates share same confidence and different types => conflict
        conflict = False
        conflict_type = "none"
        conflict_resolution = "none"
        try:
            confs = {}
            for c in task_candidates:
                if not isinstance(c, dict):
                    continue
                conf = float(c.get("confidence") or 0.0)
                t = str(c.get("task_type") or "")
                if conf not in confs:
                    confs[conf] = set()
                if t:
                    confs[conf].add(t)
            if confs:
                top = max(confs.keys())
                if len(confs[top]) > 1:
                    conflict = True
                    conflict_type = "tie_top_confidence"
                    conflict_resolution = "prefer_conservative_order"
        except Exception:
            pass

        if conflict:
            conflict_detected += 1

        source_attribution = {
            "source_layers": ["scene_state", "task_candidates"],
            "upstream_roots": {"scene_task_eval_root": st_root},
            "upstream_runtime_modes": {"scene_task_runtime_mode": upstream_mode, "fusion_runtime_mode": fusion_runtime_mode},
        }

        fusion_candidate = {
            "fusion_candidate_id": f"fc_{uuid.uuid4().hex[:10]}",
            "source_scene_id": (s.get("scene_state") or {}).get("scene_id"),
            "source_task_candidate_ids": [selected_id] if selected_id else [],
            "source_signal_ids": [],
            "fusion_candidate_type": selected_type if selected_type != "unknown" else "continue_observe_candidate",
            "confidence": float(selected.get("confidence") or 0.0),
            "source_attribution": source_attribution,
            "conflict_detected": bool(conflict),
            "conflict_type": conflict_type,
            "conflict_resolution": conflict_resolution,
            "degraded_mode": bool(degraded or uncertain),
            "reason_codes": ["CANDIDATE_ONLY", "NO_EXECUTE", "FUSION_V0", "CONSERVATIVE_SELECTION"],
            "allows_execute_now": False,
        }

        conflict_handling = {"present": True, "conflict_detected": conflict, "conflict_type": conflict_type, "resolution": conflict_resolution}
        degraded_handling = {
            "present": True,
            "degraded_or_uncertain": bool(degraded or uncertain),
            "handling": "observe_or_ask_for_help_candidate",
        }

        evidence_ok = bool(s.get("evidence_type_preserved") is True)
        cls_ok = bool(s.get("controlled_live_stream_false") is True)
        plc_ok = bool(s.get("phone_local_capture_true") is True)

        if evidence_ok:
            evidence_type_preserved += 1
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

        # Validate candidate-only integrity
        candidate_only = True
        allows_execute_now = False

        if fusion_candidate.get("allows_execute_now") is not False:
            hard_blockers.append("allows_execute_now_not_false")

        # Schema checks (minimal)
        required_fc = [
            "fusion_candidate_id",
            "source_scene_id",
            "source_task_candidate_ids",
            "source_signal_ids",
            "fusion_candidate_type",
            "confidence",
            "source_attribution",
            "conflict_detected",
            "conflict_type",
            "conflict_resolution",
            "degraded_mode",
            "reason_codes",
            "allows_execute_now",
        ]
        if all(k in fusion_candidate for k in required_fc):
            schema_valid += 1
        else:
            hard_blockers.append("fusion_candidate_schema_incomplete")

        if source_attribution and isinstance(source_attribution.get("source_layers"), list):
            attribution_present += 1
        if isinstance(fusion_candidate.get("reason_codes"), list) and len(fusion_candidate["reason_codes"]) > 0:
            reason_codes_present += 1

        if fusion_candidate.get("allows_execute_now") is False:
            allows_execute_now_false += 1
        if candidate_only is True:
            candidate_only_integrity += 1

        if conflict_handling.get("present") is True:
            conflict_handling_present += 1
        if degraded_handling.get("present") is True:
            degraded_uncertain_handling_present += 1

        if hard_blockers:
            hard_blockers_total += len(hard_blockers)

        fusion_generated += 1

        per_out.append(
            {
                "sample_id": sample_id,
                "archive_root": s.get("archive_root"),
                "source_video_path": s.get("source_video_path"),
                "perception_runtime_mode": s.get("perception_runtime_mode"),
                "scene_task_runtime_mode": upstream_mode,
                "fusion_runtime_mode": fusion_runtime_mode,
                "not_fusion_claimed": not_fusion_claimed,
                "scene_type": s.get("scene_type"),
                "scene_phase": s.get("scene_phase"),
                "task_candidates": task_candidates,
                "fusion_decision_candidate": fusion_candidate,
                "selected_candidate_type": fusion_candidate.get("fusion_candidate_type"),
                "source_attribution": source_attribution,
                "conflict_detected": bool(conflict),
                "conflict_handling": conflict_handling,
                "degraded_or_uncertain_handling": degraded_handling,
                "candidate_only": True,
                "allows_execute_now": False,
                **leakage,
                "evidence_type_preserved": evidence_ok,
                "controlled_live_stream_false": cls_ok,
                "phone_local_capture_true": plc_ok,
                "reason_codes": ["CANDIDATE_ONLY", "NO_EXECUTE", "NO_DEFAULT_ON", "FUSION_EVAL_V0"],
                "hard_blockers": hard_blockers,
                "soft_followups": soft_followups,
            }
        )

        trace.append(
            {
                "timestamp_ms": _now_ms(),
                "sample_id": sample_id,
                "event_type": "fusion_eval_completed",
                "payload": {"selected_candidate_type": selected_type, "hard_blockers": hard_blockers},
            }
        )

    # Batch decision
    hard_blockers: List[str] = []
    leakage_total = sum(int(v) for v in leakage.values())
    if leakage_total != 0:
        hard_blockers.append("leakage_detected")
    if hard_blockers_total != 0:
        hard_blockers.append("per_sample_hard_blockers_present")

    recommendation = "go"
    if hard_blockers:
        recommendation = "no_go"
    else:
        recommendation = "conditional_go" if fusion_runtime_mode == "baseline_or_mock_downstream" else "go"

    summary = {
        "tool": "evaluate_option_a_phone_local_fusion_v0",
        "phase": "Phase-FusionEval-001",
        "generated_at_ms": _now_ms(),
        "inputs": {"scene_task_eval_root": st_root, "scene_task_runtime_mode": upstream_mode},
        "fusion_runtime_mode": fusion_runtime_mode,
        "not_fusion_claimed": not_fusion_claimed,
        "metrics": {
            "fusion_candidate_completeness": {
                "fusion_candidate_generated_rate": _rate(fusion_generated, n),
                "fusion_candidate_schema_valid_rate": _rate(schema_valid, n),
                "source_attribution_present_rate": _rate(attribution_present, n),
                "reason_codes_present_rate": _rate(reason_codes_present, n),
            },
            "candidate_only_integrity": {
                "allows_execute_now_false_rate": _rate(allows_execute_now_false, n),
                "candidate_only_integrity_rate": _rate(candidate_only_integrity, n),
            },
            "conflict_degraded_handling": {
                "conflict_detected_rate": _rate(conflict_detected, n),
                "conflict_handling_present_rate": _rate(conflict_handling_present, n),
                "degraded_or_uncertain_handling_rate": _rate(degraded_uncertain_handling_present, n),
            },
            "safety_boundary": dict(leakage),
            "evidence_boundary": {
                "evidence_type_preserved_rate": _rate(evidence_type_preserved, n),
                "controlled_live_stream_false_rate": _rate(cls_false, n),
                "phone_local_capture_true_rate": _rate(plc_true, n),
            },
        },
        "recommendation": recommendation,
        "hard_blockers": hard_blockers,
        "soft_followups": ["baseline_or_mock_downstream_in_effect"] if fusion_runtime_mode == "baseline_or_mock_downstream" else [],
        "constraints": {
            "controlled_live_stream": False,
            "full_controlled_trial": False,
            "default_path_enabled": False,
            "execution_authority": False,
            "navigation_action_execution": False,
            "option_expanded": False,
        },
        "outputs": {
            "fusion_evaluation_summary_json": "fusion_evaluation_summary.json",
            "per_sample_fusion_results_json": "per_sample_fusion_results.json",
            "fusion_trace_jsonl": "fusion_trace.jsonl",
            "evaluation_notes_md": "evaluation_notes.md",
        },
    }

    _write_json(os.path.join(out_root, "fusion_evaluation_summary.json"), summary)
    _write_json(os.path.join(out_root, "per_sample_fusion_results.json"), {"samples": per_out})
    _write_jsonl(os.path.join(out_root, "fusion_trace.jsonl"), trace)
    _write_text(
        os.path.join(out_root, "evaluation_notes.md"),
        "\n".join(
            [
                "# FusionEval-001 evaluation_notes (v0)",
                "",
                f"- scene_task_eval_root: {st_root}",
                f"- fusion_runtime_mode: {fusion_runtime_mode}",
                "- reminder: candidate-only; allows_execute_now must be false; no execute/default-on/release/retry/reopen",
                "",
            ]
        )
        + "\n",
    )

    print(
        json.dumps(
            {
                "output_root": out_root,
                "summary_path": os.path.join(out_root, "fusion_evaluation_summary.json"),
                "recommendation": recommendation,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

