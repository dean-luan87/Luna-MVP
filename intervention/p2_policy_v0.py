# intervention/p2_policy_v0.py
"""
P2 v0：内容质量门禁（仅在 P1.apply_now 时生效）
不改 P1、不改仲裁、不引入生成，只做「内容是否值得说」的第二道闸门。
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class P2Decision:
    allow: bool
    reason: str
    checks: Dict[str, bool]
    text_hash: Optional[str] = None  # 供 executor 写入 recent_cache，避免重复计算

    def to_dict(self) -> Dict[str, Any]:
        out = {
            "allow": self.allow,
            "reason": self.reason,
            "checks": self.checks,
        }
        if self.text_hash is not None:
            out["text_hash"] = self.text_hash
        return out


@dataclass
class P2Config:
    # 最小信息量（中文字符数的近似）
    min_len: int = 6

    # 近时重复窗口（秒）
    duplicate_window_s: float = 60.0

    # v0 占位词黑名单（硬编码、可枚举）
    placeholder_phrases: List[str] = field(default_factory=lambda: [
        "不知道", "看不清", "可能是", "好像", "我不确定",
        "不太清楚", "也许", "应该是",
    ])


class RecentTextCache:
    """只存 hash + ts，不存原文（轻量/安全）"""
    def __init__(self):
        self._items = []  # list of (ts, hash)

    def prune(self, now: float, window_s: float):
        self._items = [(ts, h) for (ts, h) in self._items if now - ts <= window_s]

    def contains(self, h: str) -> bool:
        return any(h == _h for (_, _h) in self._items)

    def add(self, now: float, h: str):
        self._items.append((now, h))


def _hash_text(text: str) -> str:
    import hashlib
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def decide_p2_allow(
    *,
    cfg: P2Config,
    now_ts: float,
    text: str,
    recent_cache: RecentTextCache,
) -> P2Decision:
    text = (text or "").strip()

    checks = {
        "min_len": True,
        "duplicate": True,
        "placeholder": True,
    }

    # 规则 1：最小信息量
    if len(text) < cfg.min_len:
        checks["min_len"] = False

    # 规则 2：近时重复
    h = _hash_text(text)
    recent_cache.prune(now_ts, cfg.duplicate_window_s)
    if recent_cache.contains(h):
        checks["duplicate"] = False

    # 规则 3：占位词
    for p in cfg.placeholder_phrases:
        if p in text:
            checks["placeholder"] = False
            break

    allow = all(checks.values())
    if not allow:
        return P2Decision(
            allow=False,
            reason="BLOCKED_LOW_VALUE",
            checks=checks,
            text_hash=h,
        )

    return P2Decision(
        allow=True,
        reason="OK_CONTENT",
        checks=checks,
        text_hash=h,
    )
