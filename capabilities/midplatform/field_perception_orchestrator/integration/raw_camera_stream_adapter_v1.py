from __future__ import annotations

import hashlib
import time
from pathlib import Path
from typing import Iterable, Optional, Tuple

from .raw_camera_stream_types_v1 import (
    CONTROL_ACTIONS,
    OWNER,
    SOURCE_TYPES,
    PerceptionIngressCandidateV1,
    RawCameraAdapterResultV1,
    RawFrameRecordV1,
    StreamControlCandidateV1,
    StreamSessionCandidateV1,
)


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def _file_hash(source_ref: str) -> str:
    path = Path(source_ref)
    if not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_exists(source_ref: str, *, source_mode: str) -> bool:
    if source_mode == "SYNTHETIC_REGRESSION" and source_ref.startswith("synthetic://"):
        return True
    if source_ref.startswith(("file://", "external://")):
        return True
    return Path(source_ref).is_file()


def _rejected(
    *, source_type: str, code: str, component_real: bool, synthetic_source: bool
) -> RawCameraAdapterResultV1:
    return RawCameraAdapterResultV1(
        accepted=False,
        duplicate=False,
        rejection_code=code,
        source_type=source_type,
        session=None,
        frames=(),
        ingress=None,
        control=None,
        component_real=component_real,
        synthetic_source=synthetic_source,
    )


def adapt_raw_camera_source(
    source_ref: str,
    *,
    source_type: str,
    observation_demand_ref: str,
    capability_requirement_ref: str = "capability:RAW_CAMERA_INPUT_STREAM",
    device_ref: Optional[str] = None,
    frame_index: int = 0,
    captured_at: Optional[int] = None,
    width: int = 0,
    height: int = 0,
    pixel_format: str = "UNKNOWN_RAW",
    max_frames: int = 1,
    max_duration_ms: int = 5000,
    sensitivity: str = "HIGH_SENSITIVITY",
    session_id: str = "",
    frame_id: str = "",
    source_mode: str = "REAL",
    seen_frame_ids: Iterable[str] = (),
    seen_session_ids: Iterable[str] = (),
) -> RawCameraAdapterResultV1:
    """Accept only raw source metadata; never decode or interpret pixels."""

    synthetic_source = source_mode == "SYNTHETIC_REGRESSION"
    component_real = not synthetic_source
    if source_type not in SOURCE_TYPES:
        return _rejected(source_type=source_type, code="UNSUPPORTED_SOURCE_TYPE", component_real=component_real, synthetic_source=synthetic_source)
    if not str(source_ref or "").strip():
        return _rejected(source_type=source_type, code="SOURCE_MISSING", component_real=component_real, synthetic_source=synthetic_source)
    if not _source_exists(source_ref, source_mode=source_mode):
        return _rejected(source_type=source_type, code="SOURCE_NOT_FOUND", component_real=component_real, synthetic_source=synthetic_source)
    if not str(observation_demand_ref or "").strip():
        return _rejected(source_type=source_type, code="MISSING_OBSERVATION_DEMAND", component_real=component_real, synthetic_source=synthetic_source)
    if not isinstance(max_frames, int) or max_frames <= 0 or max_frames > 300:
        return _rejected(source_type=source_type, code="FRAME_BUDGET_INVALID", component_real=component_real, synthetic_source=synthetic_source)
    if not isinstance(max_duration_ms, int) or max_duration_ms <= 0 or max_duration_ms > 60000:
        return _rejected(source_type=source_type, code="DURATION_BUDGET_INVALID", component_real=component_real, synthetic_source=synthetic_source)
    if frame_index < 0 or width < 0 or height < 0:
        return _rejected(source_type=source_type, code="FRAME_METADATA_INVALID", component_real=component_real, synthetic_source=synthetic_source)

    stamp = int(captured_at if captured_at is not None else time.time() * 1000)
    source_token = _digest(f"{source_type}|{source_ref}|{observation_demand_ref}|{session_id}|{frame_index}")
    resolved_session_id = session_id or f"s2-session:{source_token}"
    resolved_frame_id = frame_id or f"s2-frame:{source_token}"
    if resolved_session_id in frozenset(seen_session_ids):
        return RawCameraAdapterResultV1(False, True, "DUPLICATE_SESSION", source_type, None, (), None, None, component_real, synthetic_source)
    if resolved_frame_id in frozenset(seen_frame_ids):
        return RawCameraAdapterResultV1(False, True, "DUPLICATE_FRAME", source_type, None, (), None, None, component_real, synthetic_source)

    trace_ref = f"trace:s2-raw-camera:{source_token}"
    provenance_refs: Tuple[str, ...] = (f"prov:s2-raw-camera:{source_token}",)
    session = StreamSessionCandidateV1(
        session_id=resolved_session_id,
        source_type=source_type,
        source_ref=source_ref,
        started_at=stamp,
        ended_at=None,
        max_frames=max_frames,
        max_duration_ms=max_duration_ms,
        observation_demand_ref=observation_demand_ref,
        capability_requirement_ref=capability_requirement_ref,
        revocation_condition="active observation demand revoked or budget exhausted",
        stop_reason="",
        trace_ref=trace_ref,
        provenance_refs=provenance_refs,
    )
    frames: Tuple[RawFrameRecordV1, ...] = ()
    if source_type in {"IMAGE_FILE", "FRAME_REFERENCE", "IMAGE_SEQUENCE"}:
        payload_ref = source_ref
        frame = RawFrameRecordV1(
            frame_id=resolved_frame_id,
            stream_session_id=resolved_session_id,
            source_type=source_type,
            source_ref=source_ref,
            device_ref=device_ref,
            frame_index=frame_index,
            captured_at=stamp,
            width=width,
            height=height,
            pixel_format=pixel_format,
            frame_payload_ref=payload_ref,
            content_hash="synthetic-reference" if synthetic_source else _file_hash(source_ref),
            temporal_validity={"observed_at": stamp, "valid_from": stamp, "valid_until": None, "stale": False, "expired": False},
            sensitivity=sensitivity,
            trace_ref=trace_ref,
            provenance_refs=provenance_refs,
        )
        frames = (frame,)
    frame_refs = tuple(frame.frame_id for frame in frames)
    ingress = PerceptionIngressCandidateV1(
        ingress_id=f"s2-ingress:{source_token}",
        stream_session_ref=resolved_session_id,
        frame_refs=frame_refs,
        source_type=source_type,
        ingress_kind="RAW_FRAME_REFERENCE",
        observation_demand_ref=observation_demand_ref,
        trace_ref=trace_ref,
        provenance_refs=provenance_refs,
    )
    return RawCameraAdapterResultV1(True, False, "", source_type, session, frames, ingress, None, component_real, synthetic_source)


def control_stream_session(session: StreamSessionCandidateV1, action: str, reason: str) -> StreamControlCandidateV1:
    if action not in CONTROL_ACTIONS:
        raise ValueError("UNSUPPORTED_SESSION_CONTROL")
    token = _digest(f"{session.session_id}|{action}|{reason}")
    return StreamControlCandidateV1(
        control_id=f"s2-control:{token}",
        session_ref=session.session_id,
        action=action,
        reason=reason,
        trace_ref=f"{session.trace_ref}:{action.lower()}",
        provenance_refs=(f"{session.provenance_refs[0]}:{action.lower()}",),
    )


__all__ = ["adapt_raw_camera_source", "control_stream_session"]
