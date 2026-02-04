from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from a3.types import EnvironmentMode


@dataclass
class RuntimeContext:
    env_mode: Optional[EnvironmentMode] = None
    engagement: Optional[Dict[str, Any]] = None
    # D) ENGAGED 失败诊断：在「最终决定不说」处归因用
    rhythm_state: Optional[str] = None
    eligibility: Optional[Dict[str, Any]] = None
    view_confidence: Optional[float] = None
    frame_quality: Optional[str] = None
