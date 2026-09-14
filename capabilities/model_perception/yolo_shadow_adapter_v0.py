"""
Phase-ModelPerception-002B

YOLO Shadow Adapter Implementation v0

Hard boundaries (must hold):
- Shadow-only, candidate-only: never triggers execute/release/retry/reopen; no default-on.
- Disable switch: if disable_yolo=True, must NOT invoke YOLO.
- Fallback: any failure/forbidden output/schema issue -> fallback to baseline/mock-shaped outputs (still candidate-only).
- No SceneTask/Fusion/Output integration; outputs are perception signals only.
- Auditable + replayable: write trace/replay/whitebox artifacts.
- Evidence boundary preserved: evidence_type must remain phone_local_controlled_capture; controlled_live_stream must remain false.
"""

from __future__ import annotations

import json
import os
import re
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Protocol, Tuple


FORBIDDEN_TOKENS_V0: Tuple[str, ...] = (
    "execute_now",
    "walk_now",
    "turn_now",
    "cross_now",
    "force_action",
    "release_side_effects",
    "retry_now",
    "reopen_now",
    "enable_default_path",
    "override_governance",
    "final_navigation_instruction",
    "actual_tts",
)


def _ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def _write_json(path: str, obj: Any) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)


def _write_jsonl(path: str, record: Mapping[str, Any]) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(dict(record), ensure_ascii=False, sort_keys=False) + "\n")


def _now_ts() -> float:
    return float(time.time())


def _hash_fingerprint(obj: Any) -> str:
    # Stable-enough v0 fingerprint (not cryptographic).
    try:
        s = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except Exception:
        s = repr(obj)
    return str(abs(hash(s)))


def _resolve_path(p: str, candidate_roots: List[str]) -> str:
    if os.path.isabs(p):
        return p
    for root in candidate_roots:
        cand = os.path.join(root, p)
        if os.path.exists(cand):
            return cand
    # Return best-effort first root join for diagnostics.
    return os.path.join(candidate_roots[0], p) if candidate_roots else p


class DetectorProvider(Protocol):
    def initialize(self, model_path: str) -> bool:  # pragma: no cover
        ...

    def detect(self, frame: Any) -> List[Dict[str, Any]]:  # pragma: no cover
        ...


@dataclass(frozen=True)
class YoloShadowAdapterConfigV0:
    model_config_id: str = "yolo_shadow_v0"
    model_provider: str = "yolov5_torchhub_ultralytics"
    model_path: str = "yolov5n.pt"
    device: str = "auto"
    max_frames: int = 60
    frame_step: int = 10
    confidence_threshold: float = 0.5
    disable_yolo: bool = True
    # Output contracts
    evidence_type_required: str = "phone_local_controlled_capture"


@dataclass(frozen=True)
class PhoneLocalSampleRefV0:
    sample_id: str
    source_video_path: str
    archive_root: str
    evidence_type: str
    controlled_live_stream: bool
    phone_local_capture: bool


def _forbidden_scan(obj: Any) -> Dict[str, Any]:
    hay = ""
    try:
        hay = json.dumps(obj, ensure_ascii=False, sort_keys=True)
    except Exception:
        hay = repr(obj)

    hits: List[str] = []
    low = hay.lower()
    for tok in FORBIDDEN_TOKENS_V0:
        # Token-aware scan: avoid substring false positives.
        # Boundary: non [a-z0-9_] on both sides (or string edges).
        pat = re.compile(rf"(^|[^a-z0-9_]){re.escape(tok)}([^a-z0-9_]|$)")
        if pat.search(low) is not None:
            hits.append(tok)
    return {"pass": len(hits) == 0, "hits": hits}


def _baseline_mock_fallback_signals(sample_id: str, reason: str) -> Dict[str, Any]:
    ts = _now_ts()
    # Do not include forbidden tokens as substrings in reason codes.
    base_reason = [reason, "yolo_shadow_fallback", "candidate_only", "allows_execute_guard_false"]
    return {
        "object_stability_signal": {
            "signal_type": "object_stability_signal",
            "sample_id": sample_id,
            "detected_objects": [],
            "object_count": 0,
            "class_distribution": {},
            "confidence_summary": {"min": 0.0, "mean": 0.0, "max": 0.0},
            "tracking_status": "not_available",
            "reason_codes": base_reason + ["object_detection_candidates_only"],
            "ts": ts,
            "allows_execute_now": False,
        },
        "spatial_passability_signal": {
            "signal_type": "spatial_passability_signal",
            "sample_id": sample_id,
            "passability": "unknown",
            "obstacle_candidates": [],
            "rough_obstacle_direction": "unknown",
            "passability_source": "object_detection_only",
            "depth_unavailable": True,
            "passability_confidence_limited": True,
            "reason_codes": base_reason + ["depth_not_available", "object_detection_only_passability_limited"],
            "ts": ts,
            "allows_execute_now": False,
        },
        "risk_field_signal": {
            "signal_type": "risk_field_signal",
            "sample_id": sample_id,
            "risk_candidates": [],
            "risk_source": "class_candidate_only",
            "collision_risk_not_confirmed": True,
            "motion_unavailable": True,
            "reason_codes": base_reason + ["class_based_risk_candidate_only"],
            "ts": ts,
            "allows_execute_now": False,
        },
        "ocr_navigation_signal": {
            "signal_type": "ocr_navigation_signal",
            "sample_id": sample_id,
            "status": "not_available",
            "reason_codes": base_reason + ["ocr_not_supported_by_yolo_detection_first"],
            "ts": ts,
            "allows_execute_now": False,
        },
        "dynamic_event_signal": {
            "signal_type": "dynamic_event_signal",
            "sample_id": sample_id,
            "status": "not_available",
            "reason_codes": base_reason + ["dynamic_event_not_confirmed_without_tracking"],
            "ts": ts,
            "allows_execute_now": False,
        },
    }


def _schema_validate_normalized_signals(signals: Mapping[str, Any]) -> Dict[str, Any]:
    required = [
        "object_stability_signal",
        "spatial_passability_signal",
        "risk_field_signal",
        "ocr_navigation_signal",
        "dynamic_event_signal",
    ]
    missing = [k for k in required if k not in signals]

    allows_execute_true: List[str] = []
    for k in required:
        v = signals.get(k, {})
        if isinstance(v, dict) and v.get("allows_execute_now") is True:
            allows_execute_true.append(k)

    ok = (len(missing) == 0) and (len(allows_execute_true) == 0)
    return {"pass": ok, "missing": missing, "allows_execute_true": allows_execute_true}


def _map_detections_to_signals(
    *,
    sample_id: str,
    frame_records: List[Dict[str, Any]],
    reason_codes: List[str],
) -> Dict[str, Any]:
    ts = _now_ts()

    all_dets: List[Dict[str, Any]] = []
    cls_counts: Dict[str, int] = {}
    confs: List[float] = []

    for fr in frame_records:
        for det in fr.get("detections", []):
            all_dets.append(det)
            cn = str(det.get("class_name", "unknown"))
            cls_counts[cn] = cls_counts.get(cn, 0) + 1
            try:
                confs.append(float(det.get("confidence", 0.0)))
            except Exception:
                confs.append(0.0)

    conf_summary = {
        "min": float(min(confs)) if confs else 0.0,
        "mean": float(sum(confs) / max(1, len(confs))) if confs else 0.0,
        "max": float(max(confs)) if confs else 0.0,
    }

    # Passability + risk are intentionally conservative and limited.
    obstacle_candidates = [
        {
            "class_name": d.get("class_name"),
            "class_id": d.get("class_id"),
            "confidence": d.get("confidence"),
            "bbox": d.get("bbox"),
            "frame_id": d.get("frame_id"),
            "ts": d.get("ts"),
        }
        for d in all_dets
    ]

    risk_candidates = []
    for d in all_dets:
        risk_candidates.append(
            {
                "class_name": d.get("class_name"),
                "class_id": d.get("class_id"),
                "confidence": d.get("confidence"),
                "frame_id": d.get("frame_id"),
                "ts": d.get("ts"),
                "risk_hint": "class_presence_candidate_only",
            }
        )

    return {
        "object_stability_signal": {
            "signal_type": "object_stability_signal",
            "sample_id": sample_id,
            "detected_objects": all_dets,
            "object_count": len(all_dets),
            "class_distribution": cls_counts,
            "confidence_summary": conf_summary,
            "tracking_status": "detection_only",
            "reason_codes": reason_codes + ["yolo_detection_shadow", "object_detection_candidates_only"],
            "ts": ts,
            "allows_execute_now": False,
        },
        "spatial_passability_signal": {
            "signal_type": "spatial_passability_signal",
            "sample_id": sample_id,
            "passability": "unknown",
            "obstacle_candidates": obstacle_candidates,
            "rough_obstacle_direction": "unknown",
            "passability_source": "object_detection_only",
            "depth_unavailable": True,
            "passability_confidence_limited": True,
            "reason_codes": reason_codes + ["depth_not_available", "object_detection_only_passability_limited"],
            "ts": ts,
            "allows_execute_now": False,
        },
        "risk_field_signal": {
            "signal_type": "risk_field_signal",
            "sample_id": sample_id,
            "risk_candidates": risk_candidates,
            "risk_source": "class_candidate_only",
            "collision_risk_not_confirmed": True,
            "motion_unavailable": True,
            "reason_codes": reason_codes + ["class_based_risk_candidate_only"],
            "ts": ts,
            "allows_execute_now": False,
        },
        "ocr_navigation_signal": {
            "signal_type": "ocr_navigation_signal",
            "sample_id": sample_id,
            "status": "not_available",
            "reason_codes": reason_codes + ["ocr_not_supported_by_yolo_detection_first"],
            "ts": ts,
            "allows_execute_now": False,
        },
        "dynamic_event_signal": {
            "signal_type": "dynamic_event_signal",
            "sample_id": sample_id,
            "status": "not_available",
            "reason_codes": reason_codes + ["dynamic_event_not_confirmed_without_tracking"],
            "ts": ts,
            "allows_execute_now": False,
        },
    }


def _load_detector_from_repo() -> DetectorProvider:
    # Note: importing the existing detector does not run inference.
    from Luna_Badge_MVP.vision.yolov5_detector import YOLOv5Detector  # type: ignore

    return YOLOv5Detector()


def run_yolo_shadow_adapter_on_sample_v0(
    *,
    sample: PhoneLocalSampleRefV0,
    cfg: YoloShadowAdapterConfigV0,
    output_root: str,
    workspace_roots_for_media: Optional[List[str]] = None,
    detector_override: Optional[DetectorProvider] = None,
) -> Dict[str, Any]:
    """
    Run YOLO shadow adapter on one sample.
    Writes per-sample artifacts under output_root/sample_id/.
    """

    ts0 = _now_ts()
    run_id = f"yolo-shadow-{uuid.uuid4()}"
    sample_dir = os.path.join(output_root, sample.sample_id)
    _ensure_dir(sample_dir)

    trace_path = os.path.join(sample_dir, "yolo_shadow_trace.jsonl")
    replay_path = os.path.join(sample_dir, "yolo_shadow_replay.jsonl")
    whitebox_path = os.path.join(sample_dir, "yolo_shadow_whitebox.jsonl")
    per_sample_path = os.path.join(sample_dir, "per_sample_yolo_shadow_results.json")

    # Phase-Mainline-RuntimeReadiness-004: guarded trial gate hook-in (default-off no-op).
    # Must not change behavior; we evaluate and ignore the result.
    try:
        from capabilities.runtime_readiness.yolo_guarded_trial_hook_v0 import (
            evaluate_yolo_guarded_trial_hook_v0,
        )

        _ = evaluate_yolo_guarded_trial_hook_v0(
            request_id=str(sample.sample_id or ""),
            trw_payload={
                "request_id": str(sample.sample_id or ""),
                "hard_audit": {"shadow_only": True, "real_runtime_activation": False},
                "source_run_id": str(sample.archive_root or ""),
                "pending_ref": True,
            },
        )
    except Exception:
        # Fail closed: hook-in must never break shadow adapter.
        pass

    # Boundary checks (fail-closed -> fallback).
    evidence_ok = (sample.evidence_type == cfg.evidence_type_required) and (sample.controlled_live_stream is False)
    if not evidence_ok:
        signals = _baseline_mock_fallback_signals(sample.sample_id, reason="evidence_boundary_violation")
        schema = _schema_validate_normalized_signals(signals)
        forb = _forbidden_scan(signals)
        out = {
            "sample_id": sample.sample_id,
            "run_id": run_id,
            "model_config_id": cfg.model_config_id,
            "model_provider": cfg.model_provider,
            "yolo_invoked": False,
            "yolo_disabled": True,
            "fallback_used": True,
            "fallback_reason": "evidence_boundary_violation",
            "frame_count_sampled": 0,
            "detection_count": 0,
            "normalized_perception_signals": signals,
            "schema_validation_result": schema,
            "forbidden_output_scan_result": forb,
            "evidence_type_preserved": True,
            "controlled_live_stream_false": True,
            "scene_context_gate_required": True,
            "visual_medium_gate_status": "not_executed_in_002b",
            "physics_consistency_gate_status": "not_executed_in_002b",
            "scene_continuity_gate_status": "not_executed_in_002b",
            "allows_execute_now": False,
            "hard_blockers": [],
            "soft_followups": ["sample_boundary_violation_fallback"],
            "timestamp": ts0,
        }
        _write_json(per_sample_path, out)
        _write_jsonl(trace_path, {"ts": ts0, "kind": "fallback", "reason": out["fallback_reason"], "sample_id": sample.sample_id})
        _write_jsonl(replay_path, {"ts": ts0, "kind": "replay", "sample_id": sample.sample_id, "input_media": sample.source_video_path, "frame_sampling": "none"})
        _write_jsonl(whitebox_path, {"ts": ts0, "kind": "whitebox", "sample_id": sample.sample_id, "reason_codes": ["evidence_boundary_violation"]})
        return out

    # Disable switch: do not invoke YOLO.
    if cfg.disable_yolo:
        signals = _baseline_mock_fallback_signals(sample.sample_id, reason="yolo_disabled")
        schema = _schema_validate_normalized_signals(signals)
        forb = _forbidden_scan(signals)
        out = {
            "sample_id": sample.sample_id,
            "run_id": run_id,
            "model_config_id": cfg.model_config_id,
            "model_provider": cfg.model_provider,
            "yolo_invoked": False,
            "yolo_disabled": True,
            "fallback_used": True,
            "fallback_reason": "yolo_disabled",
            "frame_count_sampled": 0,
            "detection_count": 0,
            "normalized_perception_signals": signals,
            "schema_validation_result": schema,
            "forbidden_output_scan_result": forb,
            "evidence_type_preserved": True,
            "controlled_live_stream_false": True,
            "scene_context_gate_required": True,
            "visual_medium_gate_status": "not_executed_in_002b",
            "physics_consistency_gate_status": "not_executed_in_002b",
            "scene_continuity_gate_status": "not_executed_in_002b",
            "allows_execute_now": False,
            "hard_blockers": [],
            "soft_followups": [],
            "timestamp": ts0,
        }
        _write_json(per_sample_path, out)
        _write_jsonl(trace_path, {"ts": ts0, "kind": "disable_switch", "sample_id": sample.sample_id})
        _write_jsonl(replay_path, {"ts": ts0, "kind": "replay", "sample_id": sample.sample_id, "input_media": sample.source_video_path, "frame_sampling": "none"})
        _write_jsonl(whitebox_path, {"ts": ts0, "kind": "whitebox", "sample_id": sample.sample_id, "reason_codes": ["yolo_disabled"]})
        return out

    # Attempt real YOLO invocation (still shadow-only). Must fallback on any failure.
    roots = workspace_roots_for_media or []
    video_path = _resolve_path(sample.source_video_path, roots) if roots else sample.source_video_path
    detector: Optional[DetectorProvider] = detector_override

    # Load dependencies lazily; any failure -> fallback.
    err: Optional[str] = None
    if detector is None:
        try:
            detector = _load_detector_from_repo()
        except Exception as e:  # noqa: BLE001
            err = f"detector_import_failed:{type(e).__name__}:{e}"

    model_loaded = False
    if err is None and detector is not None:
        try:
            model_loaded = bool(detector.initialize(cfg.model_path))
            if hasattr(detector, "set_threshold"):
                try:
                    detector.set_threshold(cfg.confidence_threshold, 0.4)  # type: ignore[attr-defined]
                except Exception:
                    pass
        except Exception as e:  # noqa: BLE001
            err = f"detector_initialize_failed:{type(e).__name__}:{e}"

    # Frame sampling and detection
    frame_records: List[Dict[str, Any]] = []
    sampled = 0
    det_count = 0

    if err is None and (not model_loaded):
        err = "model_load_failed"

    if err is None:
        try:
            import cv2  # local import to keep adapter import light
        except Exception as e:  # noqa: BLE001
            err = f"cv2_import_failed:{type(e).__name__}:{e}"

    if err is None:
        try:
            import cv2  # type: ignore

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                err = "video_open_failed"
            else:
                idx = 0
                while cap.isOpened():
                    ok, frame = cap.read()
                    if not ok:
                        break
                    if idx % max(1, int(cfg.frame_step)) == 0:
                        frame_id = f"{sample.sample_id}_f{idx}"
                        ts = _now_ts()
                        dets = detector.detect(frame) if detector is not None else []

                        # Normalize per detection with required metadata.
                        norm_dets: List[Dict[str, Any]] = []
                        for d in dets or []:
                            if not isinstance(d, dict):
                                continue
                            norm_dets.append(
                                {
                                    "bbox": d.get("bbox"),
                                    "confidence": d.get("confidence"),
                                    "class_id": d.get("class_id"),
                                    "class_name": d.get("class_name"),
                                    "frame_id": frame_id,
                                    "ts": ts,
                                }
                            )

                        det_count += len(norm_dets)
                        frame_records.append({"frame_id": frame_id, "ts": ts, "detections": norm_dets})
                        sampled += 1
                        if sampled >= max(1, int(cfg.max_frames)):
                            break
                    idx += 1
                cap.release()
        except Exception as e:  # noqa: BLE001
            err = f"detect_exception:{type(e).__name__}:{e}"

    if err is not None:
        signals = _baseline_mock_fallback_signals(sample.sample_id, reason=err)
        schema = _schema_validate_normalized_signals(signals)
        forb = _forbidden_scan(signals)
        out = {
            "sample_id": sample.sample_id,
            "run_id": run_id,
            "model_config_id": cfg.model_config_id,
            "model_provider": cfg.model_provider,
            "yolo_invoked": False,
            "yolo_disabled": False,
            "fallback_used": True,
            "fallback_reason": err,
            "frame_count_sampled": 0,
            "detection_count": 0,
            "normalized_perception_signals": signals,
            "schema_validation_result": schema,
            "forbidden_output_scan_result": forb,
            "evidence_type_preserved": True,
            "controlled_live_stream_false": True,
            "scene_context_gate_required": True,
            "visual_medium_gate_status": "not_executed_in_002b",
            "physics_consistency_gate_status": "not_executed_in_002b",
            "scene_continuity_gate_status": "not_executed_in_002b",
            "allows_execute_now": False,
            "hard_blockers": [],
            "soft_followups": ["yolo_dependency_or_runtime_error_fallback"],
            "timestamp": ts0,
        }
        _write_json(per_sample_path, out)
        _write_jsonl(trace_path, {"ts": ts0, "kind": "fallback", "reason": err, "sample_id": sample.sample_id})
        _write_jsonl(replay_path, {"ts": ts0, "kind": "replay", "sample_id": sample.sample_id, "input_media": sample.source_video_path, "resolved_video": video_path, "frame_sampling": {"max_frames": cfg.max_frames, "frame_step": cfg.frame_step}})
        _write_jsonl(whitebox_path, {"ts": ts0, "kind": "whitebox", "sample_id": sample.sample_id, "reason_codes": [err, "fallback_used"]})
        return out

    # Build normalized signals from detections.
    reason_codes = [
        "yolo_shadow_adapter_v0",
        "candidate_only",
        "no_execute",
        "no_default_on",
        "depth_not_available",
    ]
    signals = _map_detections_to_signals(sample_id=sample.sample_id, frame_records=frame_records, reason_codes=reason_codes)
    schema = _schema_validate_normalized_signals(signals)
    forb = _forbidden_scan({"frame_records": frame_records, "signals": signals})

    # Forbidden output blocks -> fallback (hard rule).
    forbidden_blocked = (not bool(forb.get("pass", False)))
    if forbidden_blocked or (not bool(schema.get("pass", False))):
        fb_reason = "forbidden_output_blocked" if forbidden_blocked else "schema_validation_failed"
        signals_fb = _baseline_mock_fallback_signals(sample.sample_id, reason=fb_reason)
        out = {
            "sample_id": sample.sample_id,
            "run_id": run_id,
            "model_config_id": cfg.model_config_id,
            "model_provider": cfg.model_provider,
            "yolo_invoked": True,
            "yolo_disabled": False,
            "fallback_used": True,
            "fallback_reason": fb_reason,
            "frame_count_sampled": sampled,
            "detection_count": det_count,
            "normalized_perception_signals": signals_fb,
            "schema_validation_result": _schema_validate_normalized_signals(signals_fb),
            "forbidden_output_scan_result": _forbidden_scan(signals_fb),
            "forbidden_output_blocked": forbidden_blocked,
            "evidence_type_preserved": True,
            "controlled_live_stream_false": True,
            "scene_context_gate_required": True,
            "visual_medium_gate_status": "not_executed_in_002b",
            "physics_consistency_gate_status": "not_executed_in_002b",
            "scene_continuity_gate_status": "not_executed_in_002b",
            "allows_execute_now": False,
            "hard_blockers": [],
            "soft_followups": ["adapter_blocked_and_fell_back"],
            "timestamp": ts0,
        }
        _write_json(per_sample_path, out)
        _write_jsonl(trace_path, {"ts": ts0, "kind": "blocked_then_fallback", "reason": fb_reason, "hits": forb.get("hits", []), "schema": schema, "sample_id": sample.sample_id})
        _write_jsonl(replay_path, {"ts": ts0, "kind": "replay", "sample_id": sample.sample_id, "input_media": sample.source_video_path, "resolved_video": video_path, "frame_sampling": {"max_frames": cfg.max_frames, "frame_step": cfg.frame_step}, "frame_records_fingerprint": _hash_fingerprint(frame_records)})
        _write_jsonl(whitebox_path, {"ts": ts0, "kind": "whitebox", "sample_id": sample.sample_id, "reason_codes": [fb_reason] + (forb.get("hits", []) if forbidden_blocked else [])})
        return out

    # Success path (shadow-only).
    out = {
        "sample_id": sample.sample_id,
        "run_id": run_id,
        "model_config_id": cfg.model_config_id,
        "model_provider": cfg.model_provider,
        "yolo_invoked": True,
        "yolo_disabled": False,
        "fallback_used": False,
        "fallback_reason": None,
        "frame_count_sampled": sampled,
        "detection_count": det_count,
        "raw_detection_records_fingerprint": _hash_fingerprint(frame_records),
        "normalized_perception_signals": signals,
        "schema_validation_result": schema,
        "forbidden_output_scan_result": forb,
        "forbidden_output_blocked": False,
        "evidence_type_preserved": True,
        "controlled_live_stream_false": True,
        "scene_context_gate_required": True,
        "visual_medium_gate_status": "not_executed_in_002b",
        "physics_consistency_gate_status": "not_executed_in_002b",
        "scene_continuity_gate_status": "not_executed_in_002b",
        "allows_execute_now": False,
        "hard_blockers": [],
        "soft_followups": [],
        "timestamp": ts0,
    }

    _write_json(per_sample_path, out)
    _write_jsonl(trace_path, {"ts": ts0, "kind": "ok", "sample_id": sample.sample_id, "frame_count_sampled": sampled, "detection_count": det_count})
    _write_jsonl(
        replay_path,
        {
            "ts": ts0,
            "kind": "replay",
            "sample_id": sample.sample_id,
            "input_media": sample.source_video_path,
            "resolved_video": video_path,
            "frame_sampling": {"max_frames": cfg.max_frames, "frame_step": cfg.frame_step},
            "frame_records_fingerprint": _hash_fingerprint(frame_records),
        },
    )
    _write_jsonl(whitebox_path, {"ts": ts0, "kind": "whitebox", "sample_id": sample.sample_id, "reason_codes": reason_codes})
    return out

