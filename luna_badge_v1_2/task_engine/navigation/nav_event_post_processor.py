"""
NavigationEventPostProcessor: 结构化事件后处理器

核心能力：
- 去重复（duplicate suppression）
- 合并（merge）
- 冷却时间（cooldown）
- 抖动消除（jitter smoothing）
- 严重事件优先级（critical event override）
"""

import time
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger("NavigationEventPostProcessor")


class NavigationEventPostProcessor:
    """
    结构化事件后处理器：

    - 去重复
    - 冷却控制
    - 事件优先合并
    - 抖动过滤
    """

    def __init__(self):
        # 记录上次播报时间：{ code: timestamp }
        self.last_spoken: Dict[str, float] = {}

        # 冷却时间（秒）
        self.cooldown = {
            "obstacle_front": 4.0,
            "obstacle_left": 4.0,
            "obstacle_right": 4.0,
            "stairs_up": 5.0,
            "stairs_down": 5.0,
            "road_narrow": 5.0,
            "water_puddle": 6.0,
            "crowded_ahead": 4.0,
            "complex_environment": 5.0,
        }

        # 抖动过滤阈值（同类事件距离变化 < jit 阈值 → 抑制）
        self.jitter_threshold = {
            "obstacle_front": 0.3,     # 距离抖动小于 30cm 不重新播报
            "obstacle_left": 0.3,
            "obstacle_right": 0.3,
            "stairs_down": 0.4,
            "stairs_up": 0.4,
        }

        # 最近事件记录（用于抖动判定）
        self.last_event_state: Dict[str, Dict[str, Any]] = {}

        # 严重事件列表（发生则忽略一切小事件）
        self.critical_codes = {"obstacle_front", "stairs_down"}

    def _cooldown_pass(self, code: str) -> bool:
        """检查是否通过冷却时间"""
        now = time.time()
        last = self.last_spoken.get(code, 0)
        cd = self.cooldown.get(code, 3.0)
        return (now - last) >= cd

    def _jitter_pass(self, ev: Dict[str, Any]) -> bool:
        """检查是否通过抖动过滤"""
        code = ev.get("code")
        if not code or code not in self.jitter_threshold:
            return True

        prev = self.last_event_state.get(code)
        if not prev:
            return True

        # 抖动差值
        d_prev = prev.get("distance", None)
        d_now = ev.get("distance", None)
        if d_prev is None or d_now is None:
            return True

        diff = abs(float(d_now) - float(d_prev))
        threshold = self.jitter_threshold[code]
        passed = diff > threshold

        if not passed:
            logger.debug(f"[jitter] {code} 距离变化 {diff:.2f}m < {threshold}m，抑制播报")

        return passed

    def _update_state(self, ev: Dict[str, Any]) -> None:
        """更新状态记录"""
        code = ev.get("code")
        if not code:
            return

        self.last_event_state[code] = {
            "distance": ev.get("distance", None),
            "ts": time.time(),
        }
        self.last_spoken[code] = time.time()

    def process(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        输入：结构化事件列表（NavigationEngineV13.evaluate）
        输出：经过冷却 & 合并后的事件（用于 PhraseMapper）

        Args:
            events: 结构化事件列表

        Returns:
            经过筛选/合并/节流/降噪的事件列表
        """
        if not events:
            return []

        # Step 1 — 如果有严重事件，只允许输出严重事件
        critical = [ev for ev in events if ev.get("code") in self.critical_codes]
        if critical:
            # 选择最近（距离最小）一个
            selected = min(critical, key=lambda e: e.get("distance", 99.0))
            code = selected.get("code")
            if code and self._cooldown_pass(code) and self._jitter_pass(selected):
                self._update_state(selected)
                logger.debug(f"[critical] 严重事件 {code} 通过，忽略其他事件")
                return [selected]
            else:
                logger.debug(f"[critical] 严重事件 {code} 被冷却/抖动过滤")
                return []

        # Step 2 — 一般事件处理（过滤冷却 & 抖动）
        processed = []
        for ev in events:
            code = ev.get("code")
            if not code:
                continue

            if not self._cooldown_pass(code):
                logger.debug(f"[cooldown] {code} 仍在冷却期，跳过")
                continue

            if not self._jitter_pass(ev):
                continue

            processed.append(ev)
            self._update_state(ev)

        # Step 3 — 合并逻辑：若有多个事件，只返回原始 events 用 PhraseMapper 负责文本合并
        return processed

    def reset(self) -> None:
        """重置所有状态（用于测试或重新开始）"""
        self.last_spoken.clear()
        self.last_event_state.clear()


# 便于全局复用的单例
nav_event_post_processor = NavigationEventPostProcessor()












