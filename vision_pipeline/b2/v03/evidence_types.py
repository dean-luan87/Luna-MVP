# vision_pipeline/b2/v03/evidence_types.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class FactorSnapshot:
    """
    单帧内，各因子的结构化快照
    """
    factors: Dict[str, Any]          # env/path/people/event 等
    confidence: Dict[str, float]     # 各因子置信度（0~1）


@dataclass
class ContinuitySnapshot:
    """
    连续性判定结果
    """
    visual_ok: bool
    spatial_ok: bool
    direction_consistent: bool
    gps_consistent: Optional[bool]
    gps_jump_m: Optional[float]


@dataclass
class EvidenceRecord:
    """
    记录级证据（窗口内的"一帧"）
    """
    t_video: float
    frame_idx: int

    factors: FactorSnapshot
    continuity: ContinuitySnapshot

