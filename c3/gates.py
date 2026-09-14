# -*- coding: utf-8 -*-
from .config import C3Config


def env_allows_learning(env_mode, cfg: C3Config) -> bool:
    if env_mode is None:
        return False
    if env_mode.safety_level not in cfg.allowed_safety:
        return False
    if env_mode.control_mode not in cfg.allowed_control:
        return False
    if env_mode.complexity_score >= cfg.max_complexity:
        return False
    return True


def bucket_complexity(score: float) -> str:
    if score < 0.33:
        return "LOW"
    if score < 0.66:
        return "MID"
    return "HIGH"
