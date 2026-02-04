"""
C1 Controller Module

Phase C1 - Continuous Vision Controller
"""

from .c1_config import (
    MIN_FPS,
    MAX_FPS,
    MOTION_SCORE_THRESHOLD,
    RECOVERY_MOTION_THRESHOLD,
    CLASS_A_PUBLIC,
    CLASS_B_SEMI_PRIVATE,
    CLASS_C_PRIVATE,
    C1_MODE_SHADOW_ONLY,
    LOG_INTERVAL_SEC,
)

__all__ = [
    "MIN_FPS",
    "MAX_FPS",
    "MOTION_SCORE_THRESHOLD",
    "RECOVERY_MOTION_THRESHOLD",
    "CLASS_A_PUBLIC",
    "CLASS_B_SEMI_PRIVATE",
    "CLASS_C_PRIVATE",
    "C1_MODE_SHADOW_ONLY",
    "LOG_INTERVAL_SEC",
]


