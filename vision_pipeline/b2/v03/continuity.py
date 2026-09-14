# vision_pipeline/b2/v03/continuity.py

from typing import Dict, Any, List
from .types import FactorDelta


class ContinuityChecker:
    """
    连续性判定器（B2 v0.3 核心）

    目标：
    - 判断【当前空间】是否与【上一时刻空间】连续
    - 明确区分：
        1) 视角连续性（可被遮挡/晃动打断）
        2) 空间连续性（进入新空间时必须重置）

    核心原则：
    - 空间连续性一旦断裂 → 原有 B2 判断全部作废
    - 突发事件可在"空间连续"的前提下，局部破坏空间属性
    """

    def __init__(self):
        self._last_signature: Dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # 对外主入口
    # ------------------------------------------------------------------

    def check(
        self,
        now_ts: float,
        context: Dict[str, Any],
        factors: List[FactorDelta],
    ) -> Dict[str, Any]:
        """
        返回：
        {
            "continuous": bool,        # 是否空间连续
            "reason": str | None,      # 不连续原因
            "reset_required": bool,    # 是否要求 B2/C 重置状态
        }
        """
        signature = self._build_signature(now_ts, context)

        # 首次进入
        if self._last_signature is None:
            self._last_signature = signature
            return {
                "continuous": True,
                "reason": None,
                "reset_required": False,
            }

        result = self._compare_signature(
            self._last_signature,
            signature,
            factors,
        )

        # 如果空间已断裂，更新签名
        if not result["continuous"]:
            self._last_signature = signature

        return result

    # ------------------------------------------------------------------
    # 空间签名构建
    # ------------------------------------------------------------------

    def _build_signature(self, now_ts: float, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        空间签名 = 用于判断"是否仍在同一空间"的关键因子
        """
        return {
            "ts": now_ts,
            "gps": context.get("gps"),                 # (lat, lon)
            "scene": context.get("scene"),             # street / indoor / mall
            "structure": context.get("structure"),     # open / closed
            "direction": context.get("direction"),     # heading / yaw
        }

    # ------------------------------------------------------------------
    # 连续性判断逻辑
    # ------------------------------------------------------------------

    def _compare_signature(
        self,
        last: Dict[str, Any],
        now: Dict[str, Any],
        factors: List[FactorDelta],
    ) -> Dict[str, Any]:
        """
        多因素联合判断空间连续性
        """

        # 1️⃣ 时间连续性（最基础，不允许瞬移）
        dt = now["ts"] - last["ts"]
        if dt < 0 or dt > 30:
            return self._break("time_jump")

        # 2️⃣ GPS 连续性（空间核实）
        if last["gps"] and now["gps"]:
            if self._gps_distance(last["gps"], now["gps"]) > 50:
                return self._break("gps_jump")

        # 3️⃣ 场景语义变化（室外 ↔ 室内）
        if last["scene"] != now["scene"]:
            return self._break("scene_change")

        # 4️⃣ 结构变化（开放 ↔ 封闭）
        if last["structure"] != now["structure"]:
            return self._break("structure_change")

        # 5️⃣ 方向突变补偿判断（防止"视觉跳转假象"）
        if not self._direction_reasonable(last, now, factors):
            return self._break("direction_discontinuity")

        return {
            "continuous": True,
            "reason": None,
            "reset_required": False,
        }

    # ------------------------------------------------------------------
    # 辅助判定函数
    # ------------------------------------------------------------------

    def _direction_reasonable(
        self,
        last: Dict[str, Any],
        now: Dict[str, Any],
        factors: List[FactorDelta],
    ) -> bool:
        """
        方向变化容忍规则：
        - 若存在 path / env 强变化，可接受方向突变
        """
        last_dir = last.get("direction")
        now_dir = now.get("direction")

        if last_dir is None or now_dir is None:
            return True

        delta = abs(now_dir - last_dir)
        if delta < 120:
            return True

        # 若有路径或环境强变化，允许方向突变
        for f in factors:
            if f.name in ("path", "env") and f.score >= 0.7:
                return True

        return False

    def _gps_distance(self, a, b) -> float:
        """
        简化距离计算（工程版，非高精度）
        """
        lat1, lon1 = a
        lat2, lon2 = b
        return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5 * 111000

    def _break(self, reason: str) -> Dict[str, Any]:
        return {
            "continuous": False,
            "reason": reason,
            "reset_required": True,
        }

