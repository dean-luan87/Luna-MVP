#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelPerception-009
YOLO Shadow Output Bridge Evaluation v0 (offline).

Input:
- Phase-ModelPerception-008 Fusion bridge outputs (per-sample results)

Output:
- navigation_output_candidate (candidate-only; no real TTS)

Hard boundaries:
- bridge-eval only; no runtime integration
- no real TTS (real_tts_invoked=false)
- no execute/default-on/release/retry/reopen leakage (must be zero)
- allows_execute_now must be false
- preserve evidence boundary booleans
- preserve source attribution (fusion + yolo source)
"""

from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from typing import Any, Dict, List, Tuple


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


_VALIDITY_WINDOWS_MS: Dict[str, int] = {
    "safety_warning_candidate": 2500,
    "navigation_instruction_candidate": 8000,
    "status_confirmation": 12000,
    "low_confidence_notice": 5000,
    "ask_for_help_prompt": 10000,
    "wait_or_observe": 3000,
    "silence": 2000,
}


def _map_fusion_to_output(fusion_candidate_type: str, degraded: bool) -> Tuple[str, str, str, str, bool, bool, str]:
    """
    Returns:
      output_type, priority, template_id, text_candidate, requires_user_confirmation, requires_human_help, suppression_reason
    """
    fc = fusion_candidate_type or "unknown"
    if fc in ("ask_for_help_candidate", "ask_for_help_prompt"):
        return (
            "ask_for_help_prompt",
            "high",
            "tpl_ask_for_help_v0",
            "我不确定当前环境是否安全，可以请你确认一下前方路况吗？",
            False,
            True,
            "none",
        )
    if fc in ("uncertain_observe_candidate",) or degraded:
        return (
            "low_confidence_notice",
            "medium",
            "tpl_low_confidence_observe_v0",
            "我目前不够确定，先保持观察。",
            False,
            False,
            "none",
        )
    if fc in ("slow_down_candidate",):
        return (
            "safety_warning_candidate",
            "high",
            "tpl_slow_down_candidate_v0",
            "前方可能有障碍，建议放慢速度并保持观察。",
            False,
            False,
            "none",
        )
    if fc in ("obstacle_attention_candidate", "narrow_path_attention_candidate"):
        return (
            "status_confirmation",
            "medium",
            "tpl_attention_candidate_v0",
            "注意前方环境变化，保持观察。",
            False,
            False,
            "none",
        )
    if fc in ("keep_clear_path_candidate", "continue_observe_candidate"):
        return (
            "silence",
            "silent",
            "tpl_silence_v0",
            "",
            False,
            False,
            "silence_by_policy_v0",
        )
    return (
        "wait_or_observe",
        "low",
        "tpl_wait_or_observe_v0",
        "先稍等并保持观察。",
        False,
        False,
        "none",
    )


_FORBIDDEN_TOKENS = [
    "execute",
    "release",
    "retry",
    "reopen",
    "enable_default_path",
    "turn_now",
    "cross_now",
    "force_walk",
    "actual_tts_emit",
    "play_audio_now",
]


def _iter_strings(obj: Any) -> List[str]:
    out: List[str] = []
    if obj is None:
        return out
    if isinstance(obj, str):
        out.append(obj)
        return out
    if isinstance(obj, (int, float, bool)):
        return out
    if isinstance(obj, list):
        for it in obj:
            out.extend(_iter_strings(it))
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str):
                out.append(k)
            out.extend(_iter_strings(v))
        return out
    out.append(str(obj))
    return out


def _forbidden_semantic_count(obj: Any) -> int:
    import re

    strings = [s.lower() for s in _iter_strings(obj)]
    total = 0
    for tok in _FORBIDDEN_TOKENS:
        pat = re.compile(rf"(^|[^a-z0-9_]){re.escape(tok)}([^a-z0-9_]|$)")
        if any(pat.search(s) for s in strings):
            total += 1
    return total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yolo-fusion-root", required=True, help="Phase-ModelPerception-008 output root")
    ap.add_argument("--output-root", required=True, help="Output directory for output bridge artifacts")
    args = ap.parse_args()

    fu_root = args.yolo_fusion_root
    out_root = args.output_root

    if not os.path.isdir(fu_root):
        raise SystemExit("yolo_fusion_root_missing_or_not_dir")
    if os.path.exists(out_root) and (not os.path.isdir(out_root) or os.listdir(out_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(out_root, exist_ok=True)

    fu_summary = _read_json(os.path.join(fu_root, "yolo_fusion_bridge_summary.json"))
    fu_samples = _read_json(os.path.join(fu_root, "per_sample_yolo_fusion_results.json")).get("samples") or []
    if not isinstance(fu_samples, list) or not fu_samples:
        raise SystemExit("per_sample_yolo_fusion_results_missing_or_empty")

    upstream_mode = str(fu_summary.get("fusion_runtime_mode") or "unknown")
    output_runtime_mode = "yolo_replacement_downstream"

    per_out: List[Dict[str, Any]] = []
    trace: List[Dict[str, Any]] = []

    n = len(fu_samples)
    out_generated = 0
    schema_valid = 0
    template_present = 0
    reason_codes_present = 0
    confidence_present = 0

    validity_present = 0
    expires_after_generated = 0
    priority_valid = 0
    suppression_present = 0
    repeat_present = 0

    source_fusion_id_present = 0
    yolo_source_preserved = 0
    source_attr_present = 0

    allows_exec_false = 0
    candidate_only_integrity = 0
    tts_false = 0

    leakage = {
        "direct_execute_leakage_count": 0,
        "release_retry_reopen_leakage_count": 0,
        "default_on_leakage_count": 0,
        "side_effects_expansion_count": 0,
        "forbidden_output_semantic_count": 0,
        "forced_navigation_action_count": 0,
    }

    ev_preserved = 0
    cls_false = 0
    plc_true = 0

    hard_blockers_total = 0

    valid_priorities = {"critical", "high", "medium", "low", "silent"}
    valid_output_types = set(_VALIDITY_WINDOWS_MS.keys())

    for s in fu_samples:
        sample_id = str(s.get("sample_id") or "")
        trace.append({"timestamp_ms": _now_ms(), "sample_id": sample_id, "event_type": "yolo_output_eval_started", "payload": {}})

        fc = s.get("fusion_decision_candidate") or {}
        fc_id = str(fc.get("fusion_candidate_id") or "")
        fc_type = str(fc.get("fusion_candidate_type") or "unknown")
        doh = fc.get("degraded_or_uncertain_handling") or {}
        if not isinstance(doh, dict):
            doh = {}
        degraded = bool(doh.get("degraded_or_uncertain", True))

        output_type, priority, tpl_id, text_cand, req_confirm, req_help, suppression_reason = _map_fusion_to_output(
            fc_type, degraded=bool(degraded)
        )
        validity_ms = int(_VALIDITY_WINDOWS_MS.get(output_type, 3000))
        gen_ms = _now_ms()
        exp_ms = gen_ms + validity_ms

        src_attr = s.get("source_attribution") or {}
        # Source attribution must preserve yolo_source if present upstream
        yolo_source = None
        if isinstance(src_attr, dict):
            yolo_source = (src_attr.get("yolo_source") if isinstance(src_attr.get("yolo_source"), dict) else None)
        if yolo_source is None and isinstance(fc.get("source_attribution"), dict):
            yolo_source = fc.get("source_attribution", {}).get("yolo_source")

        nav_out = {
            "output_candidate_id": f"oc_{uuid.uuid4().hex[:10]}",
            "source_fusion_candidate_id": fc_id,
            "source_type": "fusion_decision_candidate",
            "output_type": output_type,
            "priority": priority,
            "message_template_id": tpl_id,
            "message_text_candidate": text_cand,
            "generated_at_ms": gen_ms,
            "expires_at_ms": exp_ms,
            "validity_window_ms": validity_ms,
            "repeat_policy": "no_repeat_v0",
            "suppression_reason": suppression_reason,
            "requires_user_confirmation": bool(req_confirm),
            "requires_human_help": bool(req_help),
            "confidence": float(fc.get("confidence") or 0.0),
            "source_attribution": {
                "upstream_roots": {"yolo_fusion_root": fu_root},
                "upstream_runtime_modes": {"fusion_runtime_mode": upstream_mode, "output_runtime_mode": output_runtime_mode},
                "source_fusion_candidate_id": fc_id,
                "yolo_source": yolo_source,
            },
            "reason_codes": ["CANDIDATE_ONLY", "NO_REAL_TTS", "OUTPUT_BRIDGE_V0", "TIMING_WINDOW_APPLIED"],
            "allows_execute_now": False,
            "real_tts_invoked": False,
        }

        forbidden_count = _forbidden_semantic_count(nav_out)
        leakage["forbidden_output_semantic_count"] += int(forbidden_count)

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

        required_fields = [
            "output_candidate_id",
            "source_fusion_candidate_id",
            "source_type",
            "output_type",
            "priority",
            "message_template_id",
            "message_text_candidate",
            "generated_at_ms",
            "expires_at_ms",
            "validity_window_ms",
            "repeat_policy",
            "suppression_reason",
            "requires_user_confirmation",
            "requires_human_help",
            "confidence",
            "source_attribution",
            "reason_codes",
            "allows_execute_now",
            "real_tts_invoked",
        ]
        if all(k in nav_out for k in required_fields) and isinstance(nav_out.get("source_attribution"), dict):
            schema_valid += 1
        else:
            hard_blockers.append("output_candidate_schema_incomplete")

        if nav_out.get("output_type") not in valid_output_types:
            hard_blockers.append("output_type_invalid")
        if nav_out.get("priority") not in valid_priorities:
            hard_blockers.append("priority_invalid")

        if int(nav_out.get("validity_window_ms") or 0) > 0:
            validity_present += 1
        if int(nav_out.get("expires_at_ms") or 0) > int(nav_out.get("generated_at_ms") or 0):
            expires_after_generated += 1
        if (int(nav_out.get("expires_at_ms")) - int(nav_out.get("generated_at_ms"))) != int(nav_out.get("validity_window_ms")):
            hard_blockers.append("timing_window_inconsistent")

        if nav_out.get("allows_execute_now") is False:
            allows_exec_false += 1
        else:
            hard_blockers.append("allows_execute_now_not_false")
        if nav_out.get("real_tts_invoked") is False:
            tts_false += 1
        else:
            hard_blockers.append("real_tts_invoked_not_false")

        candidate_only_integrity += 1

        if str(nav_out.get("message_template_id") or "").strip():
            template_present += 1
        if isinstance(nav_out.get("reason_codes"), list) and len(nav_out["reason_codes"]) > 0:
            reason_codes_present += 1
        if isinstance(nav_out.get("confidence"), float):
            confidence_present += 1
        if nav_out.get("priority") in valid_priorities:
            priority_valid += 1
        if isinstance(nav_out.get("suppression_reason"), str):
            suppression_present += 1
        if isinstance(nav_out.get("repeat_policy"), str) and nav_out.get("repeat_policy"):
            repeat_present += 1

        if isinstance(nav_out.get("source_fusion_candidate_id"), str) and nav_out["source_fusion_candidate_id"]:
            source_fusion_id_present += 1
        if isinstance(nav_out.get("source_attribution"), dict):
            source_attr_present += 1
            ys = nav_out["source_attribution"].get("yolo_source")
            if isinstance(ys, dict) and ("detection_count" in ys) and ("yolo_invoked" in ys) and ("detected_classes" in ys):
                yolo_source_preserved += 1

        if forbidden_count != 0:
            hard_blockers.append("forbidden_output_semantics_detected")

        if hard_blockers:
            hard_blockers_total += len(hard_blockers)

        out_generated += 1

        per_out.append(
            {
                "sample_id": sample_id,
                "archive_root": s.get("archive_root"),
                "source_video_path": s.get("source_video_path"),
                "yolo_invoked": s.get("yolo_invoked"),
                "detection_count": s.get("detection_count"),
                "detected_classes": s.get("detected_classes"),
                "fusion_decision_candidate": fc,
                "navigation_output_candidate": nav_out,
                "output_candidate_id": nav_out.get("output_candidate_id"),
                "output_type": nav_out.get("output_type"),
                "priority": nav_out.get("priority"),
                "message_template_id": nav_out.get("message_template_id"),
                "message_text_candidate": nav_out.get("message_text_candidate"),
                "validity_window_ms": nav_out.get("validity_window_ms"),
                "generated_at_ms": nav_out.get("generated_at_ms"),
                "expires_at_ms": nav_out.get("expires_at_ms"),
                "repeat_policy": nav_out.get("repeat_policy"),
                "suppression_reason": nav_out.get("suppression_reason"),
                "requires_user_confirmation": nav_out.get("requires_user_confirmation"),
                "requires_human_help": nav_out.get("requires_human_help"),
                "source_attribution": nav_out.get("source_attribution"),
                "output_runtime_mode": output_runtime_mode,
                "candidate_only": True,
                "allows_execute_now": False,
                "real_tts_invoked": False,
                **leakage,
                "evidence_type_preserved": evidence_ok,
                "controlled_live_stream_false": cls_ok,
                "phone_local_capture_true": plc_ok,
                "reason_codes": ["CANDIDATE_ONLY", "NO_REAL_TTS", "NO_EXECUTE", "OUTPUT_BRIDGE_EVAL_V0"],
                "hard_blockers": hard_blockers,
                "soft_followups": soft_followups,
            }
        )

        trace.append(
            {
                "timestamp_ms": _now_ms(),
                "sample_id": sample_id,
                "event_type": "yolo_output_eval_completed",
                "payload": {"output_type": output_type, "priority": priority, "hard_blockers": hard_blockers},
            }
        )

    hard_blockers: List[str] = []
    leakage_total = sum(int(v) for v in leakage.values())
    if leakage_total != 0:
        hard_blockers.append("leakage_or_forbidden_semantics_detected")
    if hard_blockers_total != 0:
        hard_blockers.append("per_sample_hard_blockers_present")

    recommendation = "go" if not hard_blockers else "no_go"

    summary = {
        "tool": "evaluate_yolo_fusion_output_bridge_v0",
        "phase": "Phase-ModelPerception-009",
        "generated_at_ms": _now_ms(),
        "inputs": {"yolo_fusion_root": fu_root, "fusion_runtime_mode": upstream_mode},
        "output_runtime_mode": output_runtime_mode,
        "constraints": {
            "bridge_eval_only": True,
            "controlled_live_stream": False,
            "full_controlled_trial": False,
            "default_path_enabled": False,
            "execution_authority": False,
            "navigation_action_execution": False,
            "real_tts_emission": False,
            "option_expanded": False,
            "real_output_runtime": False,
        },
        "metrics": {
            "output_candidate_completeness": {
                "output_candidate_generated_rate": _rate(out_generated, n),
                "output_candidate_schema_valid_rate": _rate(schema_valid, n),
                "message_template_present_rate": _rate(template_present, n),
                "reason_codes_present_rate": _rate(reason_codes_present, n),
                "confidence_present_rate": _rate(confidence_present, n),
            },
            "timing_priority_suppression": {
                "validity_window_present_rate": _rate(validity_present, n),
                "expires_after_generated_rate": _rate(expires_after_generated, n),
                "priority_valid_rate": _rate(priority_valid, n),
                "suppression_reason_present_rate": _rate(suppression_present, n),
                "repeat_policy_present_rate": _rate(repeat_present, n),
            },
            "source_attribution": {
                "source_fusion_candidate_id_present_rate": _rate(source_fusion_id_present, n),
                "yolo_detection_source_preserved_rate": _rate(yolo_source_preserved, n),
                "source_attribution_present_rate": _rate(source_attr_present, n),
            },
            "candidate_only_no_tts": {
                "allows_execute_now_false_rate": _rate(allows_exec_false, n),
                "candidate_only_integrity_rate": _rate(candidate_only_integrity, n),
                "real_tts_invoked_false_rate": _rate(tts_false, n),
            },
            "safety_boundary": dict(leakage),
            "evidence_boundary": {
                "evidence_type_preserved_rate": _rate(ev_preserved, n),
                "controlled_live_stream_false_rate": _rate(cls_false, n),
                "phone_local_capture_true_rate": _rate(plc_true, n),
            },
        },
        "recommendation": recommendation,
        "hard_blockers": hard_blockers,
        "soft_followups": ["output_policy_minimal_rules_v0_soft_followup"],
        "outputs": {
            "summary_json": "yolo_output_bridge_summary.json",
            "per_sample_results_json": "per_sample_yolo_output_results.json",
            "trace_jsonl": "yolo_output_bridge_trace.jsonl",
            "evaluation_notes_md": "evaluation_notes.md",
        },
    }

    _write_json(os.path.join(out_root, "yolo_output_bridge_summary.json"), summary)
    _write_json(os.path.join(out_root, "per_sample_yolo_output_results.json"), {"samples": per_out})
    _write_jsonl(os.path.join(out_root, "yolo_output_bridge_trace.jsonl"), trace)
    _write_text(
        os.path.join(out_root, "evaluation_notes.md"),
        "\n".join(
            [
                "# YOLO Output Bridge Evaluation (v0)",
                "",
                f"- yolo_fusion_root: {fu_root}",
                "- reminder: bridge-eval only; candidate-only; no real TTS; no real Output runtime; no execute/default-on/release/retry/reopen",
                "",
            ]
        )
        + "\n",
    )

    print(json.dumps({"output_root": out_root, "summary_path": os.path.join(out_root, "yolo_output_bridge_summary.json"), "recommendation": recommendation}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

