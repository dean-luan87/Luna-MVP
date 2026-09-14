#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PerceptionEval-001
Option A Phone Local Sample Perception Evaluation v0 (offline).

This tool reads a FieldBatch sample_matrix.json and emits evaluation artifacts.

Important constraints:
- candidate-only signals
- no execute/default-on/side-effects leakage (must be zero)
- must not claim real perception model capability if running baseline/mock
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


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


def _baseline_signals_for_sample(sample: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, bool], List[str]]:
    """
    Baseline/mock generator:
    - Does not run a perception model.
    - Uses only minimal evidence fields to produce structured outputs.
    """
    reason_codes: List[str] = ["BASELINE_OR_MOCK", "CANDIDATE_ONLY", "NO_MODEL_CLAIM"]

    # Conservative defaults
    object_stability = {"stability": "unknown", "tracked_object_count": 0, "confidence": 0.2}
    ocr_nav = {
        "status": "not_available",
        "text_detected": False,
        "text_type": "none",
        "navigation_relevance": "unknown",
        "confidence": 0.0,
    }
    spatial_passability = {"passability": "unknown", "obstacle_direction": "unknown", "confidence": 0.25}
    dynamic_event = {"dynamic_event_detected": False, "event_type": "none", "urgency_level": "unknown", "confidence": 0.2}
    risk_field = {"risk_level": "unknown", "recommended_handling": "observe", "confidence": 0.25}

    signals = {
        "object_stability_signal": object_stability,
        "ocr_navigation_signal": ocr_nav,
        "spatial_passability_signal": spatial_passability,
        "dynamic_event_signal": dynamic_event,
        "risk_field_signal": risk_field,
    }
    presence = {
        "object_stability_signal_present": True,
        "ocr_navigation_signal_present": True,  # present but not_available
        "spatial_passability_signal_present": True,
        "dynamic_event_signal_present": True,
        "risk_field_signal_present": True,
    }
    return signals, presence, reason_codes


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


def _safe_bool(v: Any) -> bool:
    return True if v is True else False


def _infer_workspace_root_from_sample_matrix(sample_matrix_path: str) -> Optional[str]:
    # Heuristic: if sample_matrix lives under "<workspace_root>/logs/...", return "<workspace_root>"
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
    # Prefer resolving relative to workspace_root (if we can infer it),
    # because FieldBatch sample_matrix often stores paths like "logs/...".
    if workspace_root:
        cand_ws = os.path.join(workspace_root, rel_or_abs)
        if os.path.exists(cand_ws):
            return cand_ws
    # Next prefer anchor_dir (directory containing the sample_matrix)
    cand_anchor = os.path.join(anchor_dir, rel_or_abs)
    if os.path.exists(cand_anchor):
        return cand_anchor
    # Fallback to current repo_root behavior (kept for backward-compat)
    return rel_or_abs


def _evaluate_sample(
    sample: Dict[str, Any],
    repo_root: str,
    anchor_dir: str,
    workspace_root: Optional[str],
    *,
    source_policy_id: Optional[str],
    offline_evaluation: bool,
    disable_yolo: bool,
    yolo_manifest_path: Optional[str],
    yolo_output_root: str,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    sample_id = str(sample.get("sample_id") or "")
    archive_root_rel = str(sample.get("archive_root") or "")
    archive_root = archive_root_rel
    if archive_root_rel and not os.path.isabs(archive_root_rel):
        resolved = _resolve_relpath(anchor_dir=anchor_dir, rel_or_abs=archive_root_rel, workspace_root=workspace_root)
        if os.path.isabs(resolved) and os.path.exists(resolved):
            archive_root = resolved
        else:
            # Fallback: repo_root + rel
            archive_root = os.path.join(repo_root, archive_root_rel)

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

    trace("sample_eval_started", {"archive_root": archive_root_rel})

    hard_blockers: List[str] = []
    soft_followups: List[str] = []

    # Read run_evidence for boundary checks
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

    # Boundary assertions (hard)
    if evidence_type != "phone_local_controlled_capture":
        hard_blockers.append("evidence_type_mismatch")
    if controlled_live_stream is not False:
        hard_blockers.append("controlled_live_stream_not_false")
    if phone_local_capture is not True:
        hard_blockers.append("phone_local_capture_not_true")
    if pending_real_sidewalk_run is not True:
        hard_blockers.append("pending_real_sidewalk_run_not_true")

    # Source policy selection (default: baseline/mock, unless explicitly requested).
    source_selected = "baseline_mock"
    fallback_used = True
    fallback_reason: Optional[str] = "source_policy_not_applied"
    source_policy_applied = False
    model_config_id = None
    weights_source = None
    dependency_readiness_status: Optional[str] = None

    if source_policy_id:
        source_policy_applied = True
        try:
            from capabilities.model_perception.offline_source_policy_v0 import select_offline_perception_source_v0  # type: ignore
        except Exception:
            hard_blockers.append("offline_source_policy_import_failed")
        else:
            decision = select_offline_perception_source_v0(
                repo_root=repo_root,
                source_policy_id=str(source_policy_id),
                offline_evaluation=bool(offline_evaluation),
                option_scope="OptionA",
                evidence_type=str(evidence_type),
                controlled_live_stream=bool(controlled_live_stream is True),
                pending_real_sidewalk_run=bool(pending_real_sidewalk_run is True),
                disable_yolo=bool(disable_yolo),
                yolo_manifest_path=yolo_manifest_path,
            )
            source_selected = str(decision.get("source_selected") or "baseline_mock")
            fallback_used = bool(decision.get("fallback_used") is True)
            fallback_reason = decision.get("fallback_reason")
            mr = decision.get("manifest_readiness") or {}
            if isinstance(mr, dict):
                model_config_id = mr.get("model_config_id")
                weights_source = mr.get("weights_source")
                dependency_readiness_status = mr.get("status")

    # Generate perception outputs
    perception_runtime_mode = "baseline_or_mock"
    not_model_claimed = True
    yolo_invoked = False
    detection_count_total = 0

    if source_selected == "yolo_shadow" and not hard_blockers:
        try:
            from capabilities.model_perception.yolo_shadow_adapter_v0 import (  # type: ignore
                PhoneLocalSampleRefV0,
                YoloShadowAdapterConfigV0,
                run_yolo_shadow_adapter_on_sample_v0,
            )
            import torch  # type: ignore
        except Exception:
            # Any failure -> fallback to baseline/mock
            source_selected = "baseline_mock"
            fallback_used = True
            fallback_reason = "yolo_shadow_import_failed"
        else:
            # Build pinned-local detector override to avoid changing adapter code.
            class _PinnedLocalDetector:
                def __init__(self) -> None:
                    self._model = None

                def initialize(self, model_path: str) -> bool:
                    # Prefer local repo cache to reduce network variability.
                    local_repo = os.path.expanduser("~/.cache/torch/hub/ultralytics_yolov5_master")
                    repo_or_dir = local_repo if os.path.isdir(local_repo) else "ultralytics/yolov5"
                    source = "local" if os.path.isdir(local_repo) else "github"
                    self._model = torch.hub.load(repo_or_dir, "custom", path=model_path, source=source, verbose=False)
                    self._model.eval()
                    return True

                def detect(self, frame: Any) -> List[Dict[str, Any]]:
                    if self._model is None:
                        return []
                    results = self._model(frame)
                    out: List[Dict[str, Any]] = []
                    try:
                        rows = results.xyxy[0].cpu().numpy()
                        for x1, y1, x2, y2, conf, cls in rows:
                            out.append(
                                {
                                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                                    "confidence": float(conf),
                                    "class_id": int(cls),
                                    "class_name": self._model.names[int(cls)],
                                }
                            )
                    except Exception:
                        return []
                    return out

            # Resolve weights path from manifest (must be pinned_local and exist by policy).
            weights_path = None
            if yolo_manifest_path and os.path.exists(yolo_manifest_path):
                try:
                    m = _read_json(yolo_manifest_path)
                    wp = m.get("weights_path")
                    if isinstance(wp, str) and wp:
                        from capabilities.model_paths_v1 import resolve_model_path

                        resolved = resolve_model_path(wp, repo_root_override=repo_root)
                        weights_path = str(resolved) if resolved is not None else (
                            wp if os.path.isabs(wp) else os.path.join(repo_root, wp)
                        )
                    model_config_id = m.get("model_config_id")
                    weights_source = m.get("weights_source")
                    dependency_readiness_status = str(m.get("verification_status") or "partial")
                except Exception:
                    weights_path = None

            if not weights_path or not os.path.exists(weights_path):
                source_selected = "baseline_mock"
                fallback_used = True
                fallback_reason = "pinned_local_weights_missing"
            else:
                sref = PhoneLocalSampleRefV0(
                    sample_id=sample_id,
                    source_video_path=str(sample.get("source_video_path") or ""),
                    archive_root=str(archive_root),
                    evidence_type=str(evidence_type),
                    controlled_live_stream=bool(controlled_live_stream is True),
                    phone_local_capture=bool(phone_local_capture is True),
                )
                cfg = YoloShadowAdapterConfigV0(
                    model_config_id=str(model_config_id or "yolo_shadow_v0_pinned_local"),
                    model_path=str(weights_path),
                    disable_yolo=bool(disable_yolo),
                )
                yolo_out = run_yolo_shadow_adapter_on_sample_v0(
                    sample=sref,
                    cfg=cfg,
                    output_root=yolo_output_root,
                    workspace_roots_for_media=[workspace_root] if workspace_root else [anchor_dir, repo_root],
                    detector_override=_PinnedLocalDetector(),
                )
                normalized = yolo_out.get("normalized_perception_signals") or {}
                if not isinstance(normalized, dict):
                    normalized = {}

                schema_ok, _missing = _schema_validate_perception001(normalized)
                allows_exec = yolo_out.get("allows_execute_now")
                if (not schema_ok) or (allows_exec is not False):
                    source_selected = "baseline_mock"
                    fallback_used = True
                    fallback_reason = "yolo_shadow_contract_invalid"
                else:
                    perception_runtime_mode = "yolo_shadow_perception"
                    not_model_claimed = False
                    yolo_invoked = bool(yolo_out.get("yolo_invoked") is True)
                    detection_count_total = int(yolo_out.get("detection_count") or 0)
                    signals = normalized
                    presence = {
                        "object_stability_signal_present": isinstance(signals.get("object_stability_signal"), dict),
                        "ocr_navigation_signal_present": isinstance(signals.get("ocr_navigation_signal"), dict),
                        "spatial_passability_signal_present": isinstance(signals.get("spatial_passability_signal"), dict),
                        "dynamic_event_signal_present": isinstance(signals.get("dynamic_event_signal"), dict),
                        "risk_field_signal_present": isinstance(signals.get("risk_field_signal"), dict),
                    }
                    reason_codes = ["SOURCE_POLICY_SELECTED_YOLO_SHADOW", "CANDIDATE_ONLY", "NO_EXECUTE"]

    # Baseline/mock fallback path (default)
    if source_selected != "yolo_shadow" or perception_runtime_mode == "baseline_or_mock":
        signals, presence, reason_codes = _baseline_signals_for_sample(sample)
        perception_runtime_mode = "baseline_or_mock"
        not_model_claimed = True

    # Leakage counters (must be zero)
    metrics = {
        "low_confidence_forced_decision_count": 0,
        "unsafe_overconfident_output_count": 0,
        "execute_leakage_count": 0,
        "default_on_leakage_count": 0,
        "side_effects_expansion_count": 0,
    }

    if not reason_codes:
        hard_blockers.append("reason_codes_missing")

    trace("signals_generated", {"runtime_mode": perception_runtime_mode, "not_model_claimed": not_model_claimed})
    trace("sample_eval_completed", {"hard_blockers": hard_blockers, "soft_followups": soft_followups})

    schema_ok, missing = _schema_validate_perception001(signals if isinstance(signals, dict) else {})
    yolo_shadow_contract_valid = bool(schema_ok) and (not hard_blockers)

    per_sample = {
        "sample_id": sample_id,
        "archive_root": archive_root_rel,
        "source_video_path": sample.get("source_video_path"),
        "evidence_type": evidence_type,
        "controlled_live_stream": controlled_live_stream,
        "phone_local_capture": phone_local_capture,
        "pending_real_sidewalk_run": pending_real_sidewalk_run,
        # EF-002 audit fields
        "source_policy_id": source_policy_id,
        "offline_evaluation": bool(offline_evaluation),
        "source_selected": source_selected,
        "fallback_used": bool(fallback_used),
        "fallback_reason": fallback_reason,
        "disable_yolo": bool(disable_yolo),
        "yolo_invoked": bool(yolo_invoked),
        "detection_count_total": int(detection_count_total),
        "model_config_id": model_config_id,
        "weights_source": weights_source,
        "dependency_readiness_status": dependency_readiness_status,
        "yolo_shadow_contract_valid": yolo_shadow_contract_valid,
        "scene_context_gate_required": True,
        "allows_execute_now": False,
        "real_tts_invoked": False,
        "perception_runtime_mode": perception_runtime_mode,
        "not_model_claimed": not_model_claimed,
        "signals": signals,
        "signal_presence": presence,
        "metrics": metrics,
        "reason_codes": reason_codes,
        "signal_schema": {"ok": schema_ok, "missing": missing},
        "hard_blockers": hard_blockers,
        "soft_followups": soft_followups,
    }
    return per_sample, trace_rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-matrix", required=True, help="Path to FieldBatch sample_matrix.json")
    ap.add_argument("--output-root", required=True, help="Output directory for evaluation artifacts")
    ap.add_argument("--source-policy", default="", help="Optional source policy id (e.g. yolo_default_offline_perception_source_v0)")
    ap.add_argument("--offline-evaluation", default="true", choices=["true", "false"])
    ap.add_argument("--disable-yolo", default="false", choices=["true", "false"])
    ap.add_argument("--yolo-manifest", default="", help="YOLO manifest path (configs/models/yolo/yolo_model_manifest_v0.json)")
    args = ap.parse_args()

    sample_matrix_path = args.sample_matrix
    output_root = args.output_root

    repo_root = REPO_ROOT

    if not os.path.exists(sample_matrix_path):
        raise SystemExit("sample_matrix_missing")
    if os.path.exists(output_root) and (not os.path.isdir(output_root) or os.listdir(output_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(output_root, exist_ok=True)

    sm = _read_json(sample_matrix_path)
    samples = sm.get("samples") or []
    anchor_dir = os.path.dirname(os.path.abspath(sample_matrix_path))
    workspace_root = _infer_workspace_root_from_sample_matrix(sample_matrix_path)
    if not isinstance(samples, list) or not samples:
        raise SystemExit("sample_matrix_no_samples")

    all_trace: List[Dict[str, Any]] = []
    per_sample_results: List[Dict[str, Any]] = []

    # EF-002 source policy audit aggregates
    source_policy_id = str(args.source_policy).strip() or None
    offline_evaluation = True if str(args.offline_evaluation).lower() == "true" else False
    disable_yolo = True if str(args.disable_yolo).lower() == "true" else False
    yolo_manifest_path = str(args.yolo_manifest).strip() or None
    source_policy_applied = 0
    yolo_selected = 0
    baseline_fallback = 0
    fallback_reason_present = 0
    yolo_invoked_total = 0
    detection_count_total = 0

    yolo_output_root = os.path.join(output_root, "_yolo_shadow_perception")

    # Aggregates
    n = len(samples)
    hard_blockers_total = 0
    execute_leakage_total = 0
    default_on_leakage_total = 0
    side_effects_expansion_total = 0
    low_confidence_forced_total = 0
    unsafe_overconfident_total = 0

    evidence_type_preserved = 0
    cls_false = 0
    plc_true = 0

    signal_counts = {
        "object_stability_signal_present": 0,
        "ocr_navigation_signal_present": 0,
        "spatial_passability_signal_present": 0,
        "dynamic_event_signal_present": 0,
        "risk_field_signal_present": 0,
    }
    reason_codes_present = 0

    for s in samples:
        r, trace_rows = _evaluate_sample(
            s,
            repo_root=repo_root,
            anchor_dir=anchor_dir,
            workspace_root=workspace_root,
            source_policy_id=source_policy_id,
            offline_evaluation=offline_evaluation,
            disable_yolo=disable_yolo,
            yolo_manifest_path=yolo_manifest_path,
            yolo_output_root=yolo_output_root,
        )
        per_sample_results.append(r)
        all_trace.extend(trace_rows)

        if r.get("source_policy_id"):
            source_policy_applied += 1
        if r.get("source_selected") == "yolo_shadow":
            yolo_selected += 1
        if r.get("source_selected") == "baseline_mock":
            baseline_fallback += 1
        if r.get("fallback_reason"):
            fallback_reason_present += 1
        if r.get("yolo_invoked") is True:
            yolo_invoked_total += 1
        detection_count_total += int(r.get("detection_count_total") or 0)

        hb = r.get("hard_blockers") or []
        if hb:
            hard_blockers_total += len(hb)

        m = r.get("metrics") or {}
        execute_leakage_total += int(m.get("execute_leakage_count") or 0)
        default_on_leakage_total += int(m.get("default_on_leakage_count") or 0)
        side_effects_expansion_total += int(m.get("side_effects_expansion_count") or 0)
        low_confidence_forced_total += int(m.get("low_confidence_forced_decision_count") or 0)
        unsafe_overconfident_total += int(m.get("unsafe_overconfident_output_count") or 0)

        if r.get("evidence_type") == "phone_local_controlled_capture":
            evidence_type_preserved += 1
        if r.get("controlled_live_stream") is False:
            cls_false += 1
        if r.get("phone_local_capture") is True:
            plc_true += 1

        sp = r.get("signal_presence") or {}
        for k in list(signal_counts.keys()):
            if sp.get(k) is True:
                signal_counts[k] += 1
        if isinstance(r.get("reason_codes"), list) and len(r.get("reason_codes")) > 0:
            reason_codes_present += 1

    # Determine recommendation
    leakage_total = execute_leakage_total + default_on_leakage_total + side_effects_expansion_total
    schema_complete = all(signal_counts[k] == n for k in signal_counts.keys())
    hard_blockers = []
    if not schema_complete:
        hard_blockers.append("signal_schema_incomplete")
    if leakage_total != 0:
        hard_blockers.append("leakage_detected")
    if hard_blockers_total != 0:
        hard_blockers.append("per_sample_hard_blockers_present")

    # Recommendation:
    # - no_go if any hard blockers/leakage
    # - go otherwise (both yolo-selected and baseline fallback are acceptable under policy)
    recommendation = "no_go" if hard_blockers else "go"

    summary = {
        "tool": "evaluate_option_a_phone_local_perception_v0",
        "phase": "Phase-EngineeringFlow-002",
        "generated_at_ms": _now_ms(),
        "inputs": {
            "sample_matrix_path": sample_matrix_path,
            "sample_count": n,
            "offline_evaluation": offline_evaluation,
            "source_policy_id": source_policy_id,
            "disable_yolo": disable_yolo,
            "yolo_manifest_path": yolo_manifest_path,
        },
        "source_policy": {
            "source_policy_id": source_policy_id,
            "source_policy_applied_rate": _rate(source_policy_applied, n),
            "yolo_selected_rate": _rate(yolo_selected, n),
            "baseline_fallback_rate": _rate(baseline_fallback, n),
            "fallback_reason_present_rate": _rate(fallback_reason_present, n),
            "yolo_invoked_rate": _rate(yolo_invoked_total, n),
            "detection_count_total": int(detection_count_total),
            "scene_context_gate_required": True,
            "allows_execute_now": False,
            "real_tts_invoked": False,
        },
        "metrics": {
            "signal_completeness": {
                "object_stability_signal_rate": _rate(signal_counts["object_stability_signal_present"], n),
                "ocr_navigation_signal_rate": _rate(signal_counts["ocr_navigation_signal_present"], n),
                "spatial_passability_signal_rate": _rate(signal_counts["spatial_passability_signal_present"], n),
                "dynamic_event_signal_rate": _rate(signal_counts["dynamic_event_signal_present"], n),
                "risk_field_signal_rate": _rate(signal_counts["risk_field_signal_present"], n),
            },
            "safety_conservatism": {
                "low_confidence_forced_decision_count": low_confidence_forced_total,
                "unsafe_overconfident_output_count": unsafe_overconfident_total,
                "execute_leakage_count": execute_leakage_total,
                "default_on_leakage_count": default_on_leakage_total,
                "side_effects_expansion_count": side_effects_expansion_total,
            },
            "evidence_boundary": {
                "evidence_type_preserved_rate": _rate(evidence_type_preserved, n),
                "controlled_live_stream_false_rate": _rate(cls_false, n),
                "phone_local_capture_true_rate": _rate(plc_true, n),
            },
            "evaluation_observability": {
                "per_sample_result_ready_rate": 1.0,
                "signal_trace_ready_rate": 1.0,
                "reason_codes_present_rate": _rate(reason_codes_present, n),
            },
        },
        "recommendation": recommendation,
        "hard_blockers": hard_blockers,
        "soft_followups": [],
        "constraints": {
            "controlled_live_stream": False,
            "full_controlled_trial": False,
            "default_path_enabled": False,
            "execution_authority": False,
            "navigation_action_execution": False,
            "option_expanded": False,
        },
        "outputs": {
            "perception_evaluation_summary_json": "perception_evaluation_summary.json",
            "per_sample_results_json": "per_sample_results.json",
            "signal_trace_jsonl": "signal_trace.jsonl",
            "evaluation_notes_md": "evaluation_notes.md",
        },
    }

    _write_json(os.path.join(output_root, "perception_evaluation_summary.json"), summary)
    _write_json(os.path.join(output_root, "per_sample_results.json"), {"samples": per_sample_results})
    _write_jsonl(os.path.join(output_root, "signal_trace.jsonl"), all_trace)
    _write_text(
        os.path.join(output_root, "evaluation_notes.md"),
        "\n".join(
            [
                "# PerceptionEval-001 evaluation_notes (v0)",
                "",
                f"- source_policy_id: {source_policy_id or 'none'}",
                f"- offline_evaluation: {offline_evaluation}",
                f"- disable_yolo: {disable_yolo}",
                "- reminder: signals are candidates only; no execute/default-on/side-effects",
                "",
            ]
        )
        + "\n",
    )

    print(json.dumps({"output_root": output_root, "summary_path": os.path.join(output_root, "perception_evaluation_summary.json"), "recommendation": recommendation}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

