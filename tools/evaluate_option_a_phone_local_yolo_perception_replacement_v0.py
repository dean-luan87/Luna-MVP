#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelPerception-006
YOLO Shadow PerceptionEval Replacement Trial v0 (offline).

This tool performs an *offline replacement trial*:
- Baseline/mock perception generation is NOT run.
- Instead, YOLO shadow adapter outputs (already produced offline) are used as the PerceptionEval "signals".

Hard boundaries (must hold):
- comparison/replacement-only; no runtime integration
- no SceneTask/Fusion/Output
- candidate-only, allows_execute_now must be false
- controlled_live_stream must be false, phone_local_capture must be true
- no execute/default-on/side-effects leakage (must be zero)
"""

from __future__ import annotations

import argparse
import json
import os
import time
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


def _safe_get_bool(v: Any) -> Optional[bool]:
    if v is True:
        return True
    if v is False:
        return False
    return None


def _infer_workspace_root_from_sample_matrix(sample_matrix_path: str) -> Optional[str]:
    marker = os.sep + "logs" + os.sep
    ap = os.path.abspath(sample_matrix_path)
    if marker in ap:
        return ap.split(marker)[0]
    return None


def _resolve_relpath(anchor_dir: str, rel_or_abs: str, workspace_root: Optional[str]) -> str:
    if not rel_or_abs:
        return rel_or_abs
    if os.path.isabs(rel_or_abs):
        return rel_or_abs
    if workspace_root:
        cand_ws = os.path.join(workspace_root, rel_or_abs)
        if os.path.exists(cand_ws):
            return cand_ws
    cand_anchor = os.path.join(anchor_dir, rel_or_abs)
    if os.path.exists(cand_anchor):
        return cand_anchor
    return rel_or_abs


def _load_yolo_shadow_index(yolo_root: str) -> Dict[str, Dict[str, Any]]:
    """
    Prefer the aggregated index file if present, else fall back to per-sample directories.
    Returns {sample_id: yolo_sample_obj}
    """
    index: Dict[str, Dict[str, Any]] = {}
    agg = os.path.join(yolo_root, "per_sample_yolo_shadow_results.json")
    if os.path.exists(agg):
        try:
            obj = _read_json(agg)
            samples = obj.get("samples") or []
            if isinstance(samples, list):
                for s in samples:
                    sid = str(s.get("sample_id") or "")
                    if sid:
                        index[sid] = s
            if index:
                return index
        except Exception:
            # fall through
            pass
    # per-sample folder fallback
    try:
        for name in os.listdir(yolo_root):
            p = os.path.join(yolo_root, name, "per_sample_yolo_shadow_results.json")
            if os.path.exists(p):
                try:
                    s = _read_json(p)
                    sid = str(s.get("sample_id") or name)
                    if sid:
                        index[sid] = s
                except Exception:
                    continue
    except Exception:
        return index
    return index


def _schema_validate_perception001(signals: Dict[str, Any]) -> Tuple[bool, List[str]]:
    missing: List[str] = []
    required = [
        "object_stability_signal",
        "ocr_navigation_signal",
        "spatial_passability_signal",
        "dynamic_event_signal",
        "risk_field_signal",
    ]
    for k in required:
        if k not in signals:
            missing.append(k)
    return (len(missing) == 0), missing


def _extract_detected_classes_from_object_signal(obj_sig: Any) -> List[str]:
    if not isinstance(obj_sig, dict):
        return []
    dist = obj_sig.get("class_distribution")
    if isinstance(dist, dict) and dist:
        return sorted([str(k) for k in dist.keys()])
    det = obj_sig.get("detected_objects")
    if isinstance(det, list) and det:
        out: List[str] = []
        for d in det:
            if isinstance(d, dict) and d.get("class_name"):
                out.append(str(d.get("class_name")))
        return sorted(list(set(out)))
    return []


def _evaluate_sample(
    sample: Dict[str, Any],
    yolo_index: Dict[str, Dict[str, Any]],
    anchor_dir: str,
    workspace_root: Optional[str],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    sample_id = str(sample.get("sample_id") or "")
    archive_root_rel = str(sample.get("archive_root") or "")
    archive_root = archive_root_rel
    if archive_root_rel and not os.path.isabs(archive_root_rel):
        resolved = _resolve_relpath(anchor_dir=anchor_dir, rel_or_abs=archive_root_rel, workspace_root=workspace_root)
        if os.path.isabs(resolved) and os.path.exists(resolved):
            archive_root = resolved

    trace_rows: List[Dict[str, Any]] = []

    def trace(event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        trace_rows.append(
            {
                "timestamp_ms": _now_ms(),
                "sample_id": sample_id,
                "event_type": event_type,
                "payload": payload or {},
            }
        )

    trace("replacement_sample_eval_started", {"archive_root": archive_root_rel})

    hard_blockers: List[str] = []
    soft_followups: List[str] = []

    # Evidence boundary checks (hard)
    ev_path = os.path.join(archive_root, "run_evidence.json")
    ev: Optional[Dict[str, Any]] = None
    if os.path.exists(ev_path):
        try:
            ev = _read_json(ev_path)
        except Exception:
            hard_blockers.append("run_evidence_unparseable")
    else:
        hard_blockers.append("run_evidence_missing")

    evidence_type = ev.get("evidence_type") if ev else sample.get("evidence_type")
    controlled_live_stream = _safe_get_bool(ev.get("controlled_live_stream") if ev else sample.get("controlled_live_stream"))
    phone_local_capture = _safe_get_bool(ev.get("phone_local_capture") if ev else sample.get("phone_local_capture"))
    pending_real_sidewalk_run = _safe_get_bool(ev.get("pending_real_sidewalk_run") if ev else sample.get("pending_real_sidewalk_run"))

    if evidence_type != "phone_local_controlled_capture":
        hard_blockers.append("evidence_type_mismatch")
    if controlled_live_stream is not False:
        hard_blockers.append("controlled_live_stream_not_false")
    if phone_local_capture is not True:
        hard_blockers.append("phone_local_capture_not_true")
    if pending_real_sidewalk_run is not True:
        hard_blockers.append("pending_real_sidewalk_run_not_true")

    # Load YOLO shadow sample
    yolo_obj = yolo_index.get(sample_id)
    if not yolo_obj:
        hard_blockers.append("yolo_shadow_sample_missing")
        yolo_obj = {}

    yolo_invoked = bool(yolo_obj.get("yolo_invoked") is True)
    fallback_used = bool(yolo_obj.get("fallback_used") is True)
    detection_count = int(yolo_obj.get("detection_count") or 0)

    normalized = yolo_obj.get("normalized_perception_signals") or {}
    if not isinstance(normalized, dict):
        normalized = {}

    schema_ok, missing = _schema_validate_perception001(normalized)
    if not schema_ok:
        hard_blockers.append("signal_schema_incomplete")

    # Candidate-only / safety: must be false
    allows_execute_now = yolo_obj.get("allows_execute_now")
    if allows_execute_now is not False:
        hard_blockers.append("allows_execute_now_not_false")

    # Unsupported capability honesty (hard checks)
    ocr_status = (normalized.get("ocr_navigation_signal") or {}).get("status")
    dyn_status = (normalized.get("dynamic_event_signal") or {}).get("status")
    depth_unavailable = (normalized.get("spatial_passability_signal") or {}).get("depth_unavailable")
    collision_risk_not_confirmed = (normalized.get("risk_field_signal") or {}).get("collision_risk_not_confirmed")

    if ocr_status != "not_available":
        hard_blockers.append("ocr_status_not_not_available")
    if dyn_status != "not_available":
        hard_blockers.append("dynamic_status_not_not_available")
    if depth_unavailable is not True:
        hard_blockers.append("depth_unavailable_not_true")
    if collision_risk_not_confirmed is not True:
        hard_blockers.append("collision_risk_not_confirmed_not_true")

    # Leakage counters (must be zero; replacement tool never executes)
    metrics = {
        "execute_leakage_count": 0,
        "default_on_leakage_count": 0,
        "release_retry_reopen_leakage_count": 0,
        "side_effects_expansion_count": 0,
    }

    # Evidence boundary fields from YOLO run
    evidence_type_preserved = bool(yolo_obj.get("evidence_type_preserved") is True)
    controlled_live_stream_false = bool(yolo_obj.get("controlled_live_stream_false") is True)

    # Presence flags (PerceptionEval style)
    presence = {
        "object_stability_signal_present": isinstance(normalized.get("object_stability_signal"), dict),
        "ocr_navigation_signal_present": isinstance(normalized.get("ocr_navigation_signal"), dict),
        "spatial_passability_signal_present": isinstance(normalized.get("spatial_passability_signal"), dict),
        "dynamic_event_signal_present": isinstance(normalized.get("dynamic_event_signal"), dict),
        "risk_field_signal_present": isinstance(normalized.get("risk_field_signal"), dict),
    }

    detected_classes = _extract_detected_classes_from_object_signal(normalized.get("object_stability_signal"))

    reason_codes: List[str] = []
    # Carry through YOLO reason codes if present, but enforce replacement tag
    try:
        rs = (normalized.get("object_stability_signal") or {}).get("reason_codes") or []
        if isinstance(rs, list):
            reason_codes.extend([str(x) for x in rs if x is not None])
    except Exception:
        pass
    if "PERCEPTION_REPLACEMENT_TRIAL" not in reason_codes:
        reason_codes.append("PERCEPTION_REPLACEMENT_TRIAL")
    if "CANDIDATE_ONLY" not in reason_codes:
        reason_codes.append("CANDIDATE_ONLY")
    if "NO_EXECUTE" not in reason_codes:
        reason_codes.append("NO_EXECUTE")

    trace(
        "replacement_signals_loaded",
        {
            "yolo_invoked": yolo_invoked,
            "fallback_used": fallback_used,
            "detection_count": detection_count,
            "schema_ok": schema_ok,
            "missing": missing,
        },
    )
    trace("replacement_sample_eval_completed", {"hard_blockers": hard_blockers, "soft_followups": soft_followups})

    per_sample = {
        "sample_id": sample_id,
        "archive_root": archive_root_rel,
        "source_video_path": sample.get("source_video_path"),
        "yolo_shadow_sample_root": os.path.join(yolo_obj.get("yolo_root", ""), sample_id) if isinstance(yolo_obj.get("yolo_root"), str) else None,
        "evidence_type": evidence_type,
        "controlled_live_stream": controlled_live_stream,
        "phone_local_capture": phone_local_capture,
        "pending_real_sidewalk_run": pending_real_sidewalk_run,
        "perception_runtime_mode": "yolo_shadow_replacement",
        "not_model_claimed": False,
        "yolo_invoked": yolo_invoked,
        "fallback_used": fallback_used,
        "detection_count": detection_count,
        "detected_classes": detected_classes,
        "signals": normalized,
        "signal_presence": presence,
        "unsupported_capability_honesty": {
            "ocr_status": ocr_status,
            "dynamic_status": dyn_status,
            "depth_unavailable": depth_unavailable,
            "collision_risk_not_confirmed": collision_risk_not_confirmed,
        },
        "candidate_only": {
            "allows_execute_now": allows_execute_now,
        },
        "metrics": metrics,
        "evidence_boundary": {
            "evidence_type_preserved": evidence_type_preserved,
            "controlled_live_stream_false": controlled_live_stream_false,
        },
        "reason_codes": reason_codes,
        "hard_blockers": hard_blockers,
        "soft_followups": soft_followups,
    }
    return per_sample, trace_rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-matrix", required=True, help="Path to FieldBatch sample_matrix.json")
    ap.add_argument("--yolo-shadow-root", required=True, help="YOLO shadow output root (enabled run)")
    ap.add_argument("--output-root", required=True, help="Output directory for replacement trial artifacts")
    args = ap.parse_args()

    sample_matrix_path = args.sample_matrix
    yolo_root = args.yolo_shadow_root
    output_root = args.output_root

    if not os.path.exists(sample_matrix_path):
        raise SystemExit("sample_matrix_missing")
    if not os.path.isdir(yolo_root):
        raise SystemExit("yolo_shadow_root_missing_or_not_dir")
    if os.path.exists(output_root) and (not os.path.isdir(output_root) or os.listdir(output_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(output_root, exist_ok=True)

    sm = _read_json(sample_matrix_path)
    samples = sm.get("samples") or []
    anchor_dir = os.path.dirname(os.path.abspath(sample_matrix_path))
    workspace_root = _infer_workspace_root_from_sample_matrix(sample_matrix_path)
    if not isinstance(samples, list) or not samples:
        raise SystemExit("sample_matrix_no_samples")

    yolo_index = _load_yolo_shadow_index(yolo_root)

    all_trace: List[Dict[str, Any]] = []
    per_sample_results: List[Dict[str, Any]] = []

    n = len(samples)
    generated = 0
    invoked = 0
    fallback = 0
    detection_available = 0
    schema_valid = 0

    # signal presence rates
    signal_counts = {
        "object_stability_signal_present": 0,
        "ocr_navigation_signal_present": 0,
        "spatial_passability_signal_present": 0,
        "dynamic_event_signal_present": 0,
        "risk_field_signal_present": 0,
    }

    # honesty rates
    ocr_na = 0
    dyn_na = 0
    depth_unavail = 0
    collision_nc = 0

    # safety
    allows_exec_false = 0
    execute_leakage_total = 0
    default_on_leakage_total = 0
    release_retry_reopen_total = 0
    side_effects_expansion_total = 0

    # evidence boundary
    ev_preserved = 0
    cls_false = 0
    plc_true = 0

    hard_blockers_total = 0

    for s in samples:
        r, trace_rows = _evaluate_sample(s, yolo_index=yolo_index, anchor_dir=anchor_dir, workspace_root=workspace_root)
        per_sample_results.append(r)
        all_trace.extend(trace_rows)
        generated += 1

        if r.get("yolo_invoked") is True:
            invoked += 1
        if r.get("fallback_used") is True:
            fallback += 1
        if int(r.get("detection_count") or 0) > 0:
            detection_available += 1

        # schema validity is "no schema hard blocker"
        hb = r.get("hard_blockers") or []
        if hb:
            hard_blockers_total += len(hb)
        else:
            schema_valid += 1

        sp = r.get("signal_presence") or {}
        for k in list(signal_counts.keys()):
            if sp.get(k) is True:
                signal_counts[k] += 1

        honesty = r.get("unsupported_capability_honesty") or {}
        if honesty.get("ocr_status") == "not_available":
            ocr_na += 1
        if honesty.get("dynamic_status") == "not_available":
            dyn_na += 1
        if honesty.get("depth_unavailable") is True:
            depth_unavail += 1
        if honesty.get("collision_risk_not_confirmed") is True:
            collision_nc += 1

        if (r.get("candidate_only") or {}).get("allows_execute_now") is False:
            allows_exec_false += 1

        m = r.get("metrics") or {}
        execute_leakage_total += int(m.get("execute_leakage_count") or 0)
        default_on_leakage_total += int(m.get("default_on_leakage_count") or 0)
        release_retry_reopen_total += int(m.get("release_retry_reopen_leakage_count") or 0)
        side_effects_expansion_total += int(m.get("side_effects_expansion_count") or 0)

        if r.get("evidence_type") == "phone_local_controlled_capture":
            ev_preserved += 1
        if r.get("controlled_live_stream") is False:
            cls_false += 1
        if r.get("phone_local_capture") is True:
            plc_true += 1

    # Final decision
    leakage_total = execute_leakage_total + default_on_leakage_total + release_retry_reopen_total + side_effects_expansion_total
    schema_complete = all(signal_counts[k] == n for k in signal_counts.keys())
    hard_blockers: List[str] = []
    if generated != n:
        hard_blockers.append("replacement_result_missing")
    if not schema_complete:
        hard_blockers.append("signal_schema_incomplete")
    if leakage_total != 0:
        hard_blockers.append("leakage_detected")
    if hard_blockers_total != 0:
        hard_blockers.append("per_sample_hard_blockers_present")

    recommendation = "go"
    if hard_blockers:
        recommendation = "no_go"

    summary = {
        "tool": "evaluate_option_a_phone_local_yolo_perception_replacement_v0",
        "phase": "Phase-ModelPerception-006",
        "generated_at_ms": _now_ms(),
        "inputs": {
            "sample_matrix_path": sample_matrix_path,
            "yolo_shadow_root": yolo_root,
            "sample_count": n,
        },
        "perception_runtime_mode": "yolo_shadow_replacement",
        "not_model_claimed": False,
        "constraints": {
            "replacement_trial_only": True,
            "controlled_live_stream": False,
            "full_controlled_trial": False,
            "default_path_enabled": False,
            "execution_authority": False,
            "navigation_action_execution": False,
            "option_expanded": False,
            "scene_task_fusion_output": False,
        },
        "metrics": {
            "replacement_completeness": {
                "sample_count_total": n,
                "replacement_result_generated_rate": _rate(generated, n),
                "yolo_invoked_rate": _rate(invoked, n),
                "fallback_rate": _rate(fallback, n),
                "detection_available_rate": _rate(detection_available, n),
            },
            "signal_schema": {
                "object_stability_signal_rate": _rate(signal_counts["object_stability_signal_present"], n),
                "ocr_navigation_signal_rate": _rate(signal_counts["ocr_navigation_signal_present"], n),
                "spatial_passability_signal_rate": _rate(signal_counts["spatial_passability_signal_present"], n),
                "dynamic_event_signal_rate": _rate(signal_counts["dynamic_event_signal_present"], n),
                "risk_field_signal_rate": _rate(signal_counts["risk_field_signal_present"], n),
                "signal_schema_valid_rate": _rate(schema_valid, n),
            },
            "unsupported_capability_honesty": {
                "ocr_not_available_rate": _rate(ocr_na, n),
                "dynamic_not_available_rate": _rate(dyn_na, n),
                "depth_unavailable_rate": _rate(depth_unavail, n),
                "collision_risk_not_confirmed_rate": _rate(collision_nc, n),
            },
            "candidate_only_safety": {
                "allows_execute_now_false_rate": _rate(allows_exec_false, n),
                "execute_leakage_count": execute_leakage_total,
                "default_on_leakage_count": default_on_leakage_total,
                "release_retry_reopen_leakage_count": release_retry_reopen_total,
                "side_effects_expansion_count": side_effects_expansion_total,
            },
            "evidence_boundary": {
                "evidence_type_preserved_rate": _rate(ev_preserved, n),
                "controlled_live_stream_false_rate": _rate(cls_false, n),
                "phone_local_capture_true_rate": _rate(plc_true, n),
            },
        },
        "recommendation": recommendation,
        "hard_blockers": hard_blockers,
        "soft_followups": ["torch_hub_reproducibility_risk_soft_followup"],
        "outputs": {
            "yolo_perception_replacement_summary_json": "yolo_perception_replacement_summary.json",
            "per_sample_results_json": "per_sample_yolo_perception_replacement_results.json",
            "trace_jsonl": "yolo_perception_replacement_trace.jsonl",
            "evaluation_notes_md": "evaluation_notes.md",
        },
    }

    _write_json(os.path.join(output_root, "yolo_perception_replacement_summary.json"), summary)
    _write_json(os.path.join(output_root, "per_sample_yolo_perception_replacement_results.json"), {"samples": per_sample_results})
    _write_jsonl(os.path.join(output_root, "yolo_perception_replacement_trace.jsonl"), all_trace)
    _write_text(
        os.path.join(output_root, "evaluation_notes.md"),
        "\n".join(
            [
                "# YOLO Perception Replacement Trial (v0)",
                "",
                "- perception_runtime_mode: yolo_shadow_replacement",
                "- reminder: candidate-only; no execute/default-on/side-effects; no SceneTask/Fusion/Output",
                "",
            ]
        )
        + "\n",
    )

    print(
        json.dumps(
            {
                "output_root": output_root,
                "summary_path": os.path.join(output_root, "yolo_perception_replacement_summary.json"),
                "recommendation": recommendation,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

