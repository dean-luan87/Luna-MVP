# -*- coding: utf-8 -*-
"""
观测帧构造器：必须用这两个构造，禁止模块自己补 0。
"""
from .observation_frame import ObservationFrame


def build_empty_observation_frame(ts: float, dt: float, seq: int) -> ObservationFrame:
    """空观测：没取数时派发 sampled=False，字段全 0 / NONE。Phase 2.0 外部感知字段默认 "" / 0.0。"""
    return ObservationFrame(
        ts=ts,
        dt=dt,
        seq=seq,
        sampled=False,
        motion=0.0,
        path=0.0,
        branch=0.0,
        roi=0,
        pal=0.0,
        complexity=0.0,
        vc=0.0,
        frame_quality="NONE",
        control_mode="NONE",
        ocr_text="",
        ocr_produced_ts=0.0,
        map_hint="",
        map_produced_ts=0.0,
        speech_event="",
        speech_produced_ts=0.0,
    )


def build_observation_frame(
    ts: float,
    dt: float,
    seq: int,
    sampled: bool,
    motion: float = 0.0,
    path: float = 0.0,
    branch: float = 0.0,
    roi: int = 0,
    pal: float = 0.0,
    complexity: float = 0.0,
    vc: float = 0.0,
    frame_quality: str = "GOOD",
    control_mode: str = "NONE",
    ocr_text: str = "",
    ocr_produced_ts: float = 0.0,
    map_hint: str = "",
    map_produced_ts: float = 0.0,
    speech_event: str = "",
    speech_produced_ts: float = 0.0,
) -> ObservationFrame:
    """从 pipeline/已有数据构造真实观测帧；缺的必须显式 0，不得 None / 沿用上次。Phase 2.0 字段默认占位。"""
    return ObservationFrame(
        ts=ts,
        dt=dt,
        seq=seq,
        sampled=sampled,
        motion=motion,
        path=path,
        branch=branch,
        roi=roi,
        pal=pal,
        complexity=complexity,
        vc=vc,
        frame_quality=frame_quality,
        control_mode=control_mode,
        ocr_text=ocr_text,
        ocr_produced_ts=ocr_produced_ts,
        map_hint=map_hint,
        map_produced_ts=map_produced_ts,
        speech_event=speech_event,
        speech_produced_ts=speech_produced_ts,
    )
