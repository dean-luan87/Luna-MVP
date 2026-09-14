# intervention/slot_l_v0.py
# L 层 v0：Slot / 对象抽象（只读、不接地图、可封板）

from enum import Enum
from typing import Dict, Optional


class SlotType(Enum):
    NAV_TARGET = "NAV_TARGET"
    ENV_TARGET = "ENV_TARGET"
    TASK_TARGET = "TASK_TARGET"
    NONE = "NONE"


class SlotL_v0:
    """
    L 层 v0：Slot / 对象抽象（只读）

    输入：
    - intent（来自 K）
    - a3_signals（已有世界信号快照）

    输出：
    - slot_type + slot（或 NONE）

    原则：宁可给 NONE，也不要编对象。
    """

    def decide(
        self,
        intent: str,
        a3_signals: Dict,
    ) -> Dict:
        """
        返回：
        {
          "slot_type": str,
          "slot": dict | None
        }
        """
        if intent == "NAV_GUIDE":
            return self._nav_slot(a3_signals)

        if intent == "ENV_NOTICE":
            return self._env_slot(a3_signals)

        if intent == "TASK_ASSIST":
            return self._task_slot(a3_signals)

        # SAFETY_WARN / STATUS_UPDATE / NONE
        return {
            "slot_type": SlotType.NONE.value,
            "slot": None,
        }

    # ---------- 内部规则 ----------

    def _nav_slot(self, sig: Dict) -> Dict:
        """
        v0 导航 slot：
        - 只区分「是否有可用路径提示」
        - 不生成具体目标、不接地图
        """
        path = sig.get("path_instability")
        if path is None:
            path = 1.0 - sig.get("path_stability", 1.0)
        path = float(path) if path is not None else 1.0
        branch = float(sig.get("branch_load") or 0.0)
        roi_count = int(sig.get("roi_count", 0))

        # 有稳定路径 & 分叉不高 → 可给 PATH_HINT
        if path < 0.6 and branch < 0.5:
            return {
                "slot_type": SlotType.NAV_TARGET.value,
                "slot": {
                    "mode": "PATH_HINT",
                    "confidence": round(1.0 - path, 2),
                },
            }

        return {
            "slot_type": SlotType.NONE.value,
            "slot": None,
        }

    def _env_slot(self, sig: Dict) -> Dict:
        """
        v0 环境 slot：
        - 只看是否有 ROI 聚集
        """
        roi_count = int(sig.get("roi_count", 0))
        motion = float(sig.get("motion_instability", 0.0))

        if roi_count >= 2 and motion > 0.3:
            return {
                "slot_type": SlotType.ENV_TARGET.value,
                "slot": {
                    "kind": "DYNAMIC_REGION",
                    "roi_count": roi_count,
                },
            }

        return {
            "slot_type": SlotType.NONE.value,
            "slot": None,
        }

    def _task_slot(self, sig: Dict) -> Dict:
        """
        v0 任务 slot：
        - 仅透传已有 task_state
        """
        task_state = sig.get("task_state")
        if task_state:
            return {
                "slot_type": SlotType.TASK_TARGET.value,
                "slot": {
                    "task_state": task_state,
                },
            }

        return {
            "slot_type": SlotType.NONE.value,
            "slot": None,
        }


_slot_l: Optional[SlotL_v0] = None


def get_slot_l_v0() -> SlotL_v0:
    global _slot_l
    if _slot_l is None:
        _slot_l = SlotL_v0()
    return _slot_l
