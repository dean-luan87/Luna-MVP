from typing import List, Dict, Any

from .ability_matrix import AuthorityLevel
from .distortion_report import DistortionReport


_LEVEL_ORDER = ["A1", "A2", "A3", "A4", "A5"]
_DELAY_WINDOWS_SEC = {
    ("A5", "A4"): 10,
    ("A4", "A3"): 20,
    ("A3", "A2"): 30,
    ("A2", "A1"): 60,
}


def _level_rank(level: AuthorityLevel) -> int:
    return _LEVEL_ORDER.index(level.value)


def _next_higher(level: AuthorityLevel) -> AuthorityLevel:
    idx = _level_rank(level)
    if idx == 0:
        return level
    return AuthorityLevel(_LEVEL_ORDER[idx - 1])


def _stable_since(raw_history: List[Dict[str, Any]], target: AuthorityLevel) -> float:
    # Find the most recent time raw authority dropped below target
    for item in reversed(raw_history):
        raw = item.get("raw")
        if raw is None:
            continue
        if _LEVEL_ORDER.index(raw) > _LEVEL_ORDER.index(target.value):
            return item.get("ts", 0.0)
    if raw_history:
        return raw_history[0].get("ts", 0.0)
    return 0.0


def apply_authority_hysteresis(
    raw_authority: AuthorityLevel,
    authority_history: List[Dict[str, Any]],
    distortion_report: DistortionReport,
    now_ts: float,
    risk_context: Dict[str, Any] = None,
) -> AuthorityLevel:
    """
    返回最终可用 Authority
    """
    if not authority_history:
        return raw_authority

    current_effective = AuthorityLevel(authority_history[-1]["effective"])
    raw_rank = _level_rank(raw_authority)
    current_rank = _level_rank(current_effective)

    # 下降立即生效
    if raw_rank > current_rank:
        return raw_authority

    # 相同则保持
    if raw_rank == current_rank:
        return raw_authority

    risk_present = False
    risk_level = None
    if risk_context:
        risk_present = bool(risk_context.get("risk_present", False))
        risk_level = risk_context.get("risk_level")

    # 回升受阻：失真存在
    if distortion_report.distorted:
        return current_effective

    # 回升只允许一级
    target = _next_higher(current_effective)
    if _level_rank(target) < raw_rank:
        target = raw_authority

    # 回升受阻：短时风险存在（只影响回升，不影响降级）
    if risk_present:
        return current_effective

    delay = _DELAY_WINDOWS_SEC.get((current_effective.value, target.value), 30)
    stable_since = _stable_since(authority_history, target)
    if (now_ts - stable_since) < delay:
        return current_effective

    return target
