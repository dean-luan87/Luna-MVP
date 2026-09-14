# -*- coding: utf-8 -*-
"""
Phase-CoreCapability-TRW-Unified-002
YOLO RequestTrace Shadow Adapter v0 (offline/shadow only).

Reads YOLO local TRW outputs (e.g. offline_mainline yolo_shadow_* artifacts)
and converts them into RequestTrace shadow stage records grouped into chains.

Hard boundaries:
- Read-only adapter (does not modify source root).
- Does not invoke runtime, navigation, TTS, playback.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


STAGE_NAMESPACE = "core_capability_request_trace_v0"

YOLO_STAGES: List[Tuple[str, int]] = [
    ("request_trace.stage.perception.yolo.input_frame", 0),
    ("request_trace.stage.perception.yolo.detector_invocation", 1),
    ("request_trace.stage.perception.yolo.detection_result", 2),
    ("request_trace.stage.perception.yolo.risk_or_object_classification", 3),
    ("request_trace.stage.perception.yolo.observability_envelope", 4),
]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _maybe_read_json(path: Optional[Path]) -> Any:
    if not path or not path.exists():
        return None
    try:
        return _read_json(path)
    except Exception:
        return None


def _source_run_id_from_root(root: Path) -> str:
    return root.name


def _deterministic_request_id(source_run_id: str, sample_id: str) -> str:
    return f"shadow_req_{source_run_id}_{sample_id}"


@dataclass(frozen=True)
class YoloShadowStageV0:
    stage_namespace: str
    stage_name: str
    stage_order: int
    request_id: str
    trace_id: Optional[str]
    session_id: Optional[str]
    source_run_id: str
    missing_fields: List[str] = field(default_factory=list)
    source_refs: Dict[str, Optional[str]] = field(default_factory=dict)
    hard_audit: Dict[str, Any] = field(default_factory=dict)
    fields: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class YoloShadowChainV0:
    request_id: str
    trace_id: Optional[str]
    session_id: Optional[str]
    source_run_id: str
    request_id_origin: str  # inherited|deterministic_shadow
    stages: List[Dict[str, Any]]
    notes: List[str] = field(default_factory=list)


def load_yolo_local_outputs_v0(yolo_root: str) -> Dict[str, Any]:
    """
    Loads minimal YOLO local outputs from an offline mainline root.
    Expected structure (one of):
    - stage_outputs/perception/_yolo_shadow_perception/<bucket>/{per_sample_yolo_shadow_results.json,yolo_shadow_trace.jsonl,...}
    """
    root = Path(yolo_root)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"yolo_root not found: {yolo_root}")

    source_run_id = _source_run_id_from_root(root)

    # Discover per-sample result files under the known yolo shadow folder.
    per_sample_files = list(
        root.glob("stage_outputs/perception/_yolo_shadow_perception/*/per_sample_yolo_shadow_results.json")
    )
    bundles: List[Dict[str, Any]] = []
    for p in sorted(per_sample_files):
        bucket_dir = p.parent
        bundles.append(
            {
                "bucket": bucket_dir.name,
                "per_sample_results_path": str(p),
                "trace_path": str(bucket_dir / "yolo_shadow_trace.jsonl"),
                "replay_path": str(bucket_dir / "yolo_shadow_replay.jsonl"),
                "whitebox_path": str(bucket_dir / "yolo_shadow_whitebox.jsonl"),
                "per_sample_results": _maybe_read_json(p),
            }
        )

    return {
        "yolo_root": str(root),
        "source_run_id": source_run_id,
        "bundle_count": len(bundles),
        "bundles": bundles,
    }


def _extract_sample_id(row: Dict[str, Any], *, fallback: str) -> str:
    for k in ("sample_id", "sample", "frame_id", "image_id", "id"):
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
        if isinstance(v, int):
            return str(v)
    return fallback


def _extract_detection_count(row: Dict[str, Any]) -> Optional[int]:
    for k in ("detection_count", "detections_count", "num_detections"):
        v = row.get(k)
        if isinstance(v, int):
            return v
        try:
            if v is not None:
                return int(v)
        except Exception:
            pass
    dets = row.get("detections")
    if isinstance(dets, list):
        return len(dets)
    return None


def build_yolo_request_trace_stage_v0(
    *,
    stage_name: str,
    stage_order: int,
    request_id: str,
    source_run_id: str,
    source_refs: Dict[str, Optional[str]],
    sample_fields: Dict[str, Any],
) -> YoloShadowStageV0:
    missing = ["trace_id", "session_id"]
    hard = {
        "runtime_invoked": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "real_tts_invoked": False,
    }
    return YoloShadowStageV0(
        stage_namespace=STAGE_NAMESPACE,
        stage_name=stage_name,
        stage_order=stage_order,
        request_id=request_id,
        trace_id=None,
        session_id=None,
        source_run_id=source_run_id,
        missing_fields=missing,
        source_refs=dict(source_refs),
        hard_audit=hard,
        fields=dict(sample_fields),
    )


def build_yolo_request_trace_chain_v0(
    *,
    source_run_id: str,
    request_id: str,
    request_id_origin: str,
    source_refs: Dict[str, Optional[str]],
    sample_fields: Dict[str, Any],
) -> YoloShadowChainV0:
    stages: List[Dict[str, Any]] = []
    for stage_name, stage_order in YOLO_STAGES:
        st = build_yolo_request_trace_stage_v0(
            stage_name=stage_name,
            stage_order=stage_order,
            request_id=request_id,
            source_run_id=source_run_id,
            source_refs=source_refs,
            sample_fields=sample_fields,
        )
        stages.append(asdict(st))
    return YoloShadowChainV0(
        request_id=request_id,
        trace_id=None,
        session_id=None,
        source_run_id=source_run_id,
        request_id_origin=request_id_origin,
        stages=stages,
        notes=["shadow_only:true", "runtime_invoked:false"],
    )


def run_yolo_request_trace_shadow_adapter_v0(yolo_root: str) -> Dict[str, Any]:
    loaded = load_yolo_local_outputs_v0(yolo_root)
    source_run_id = str(loaded.get("source_run_id") or "")
    bundles = loaded.get("bundles") if isinstance(loaded.get("bundles"), list) else []

    chains: List[Dict[str, Any]] = []
    missing_source_refs: List[Dict[str, Any]] = []

    for b in bundles:
        per_obj = b.get("per_sample_results")
        trace_ref = b.get("trace_path")
        replay_ref = b.get("replay_path")
        whitebox_ref = b.get("whitebox_path")
        src_refs = {
            "trace_ref": trace_ref if isinstance(trace_ref, str) else None,
            "replay_ref": replay_ref if isinstance(replay_ref, str) else None,
            "whitebox_ref": whitebox_ref if isinstance(whitebox_ref, str) else None,
            "original_summary_ref": b.get("per_sample_results_path"),
            "source_root": str(loaded.get("yolo_root") or ""),
        }
        # record missing refs (do not fabricate)
        miss = [k for k, v in src_refs.items() if not v]
        if miss:
            missing_source_refs.append({"bucket": b.get("bucket"), "missing_source_refs": miss})

        # per_sample_yolo_shadow_results.json is typically a single aggregated dict for the bucket.
        # We generate at least one chain per bucket without expanding large per-frame lists.
        if isinstance(per_obj, dict):
            sample_id = _extract_sample_id(per_obj, fallback=str(b.get("bucket") or "unknown_bucket"))
            request_id = _deterministic_request_id(source_run_id, sample_id)
            sample_fields = {
                "frame_id": sample_id,
                "bucket": b.get("bucket"),
                "run_id": per_obj.get("run_id"),
                "model_config_id": per_obj.get("model_config_id") or per_obj.get("model_id") or None,
                "model_provider": per_obj.get("model_provider") or None,
                "frame_count_sampled": per_obj.get("frame_count_sampled"),
                "detection_count": _extract_detection_count(per_obj),
                "fallback_used": per_obj.get("fallback_used"),
                "fallback_reason": per_obj.get("fallback_reason"),
            }
            ch = build_yolo_request_trace_chain_v0(
                source_run_id=source_run_id,
                request_id=request_id,
                request_id_origin="deterministic_shadow",
                source_refs=src_refs,
                sample_fields=sample_fields,
            )
            chains.append(asdict(ch))
        elif isinstance(per_obj, list):
            for idx, row in enumerate(per_obj):
                if not isinstance(row, dict):
                    continue
                sample_id = _extract_sample_id(row, fallback=f"{b.get('bucket')}_{idx:04d}")
                request_id = _deterministic_request_id(source_run_id, sample_id)
                sample_fields = {
                    "frame_id": sample_id,
                    "model_config_id": row.get("model_config_id") or row.get("model_id") or None,
                    "detection_count": _extract_detection_count(row),
                    "object_classes": row.get("object_classes") or row.get("classes") or None,
                }
                ch = build_yolo_request_trace_chain_v0(
                    source_run_id=source_run_id,
                    request_id=request_id,
                    request_id_origin="deterministic_shadow",
                    source_refs=src_refs,
                    sample_fields=sample_fields,
                )
                chains.append(asdict(ch))

    return {
        "capability": "yolo",
        "yolo_root": str(loaded.get("yolo_root") or ""),
        "source_run_id": source_run_id,
        "bundle_count": int(loaded.get("bundle_count") or 0),
        "chain_count": len(chains),
        "missing_source_refs": missing_source_refs,
        "chains": chains,
    }

