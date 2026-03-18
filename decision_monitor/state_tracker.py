# -*- coding: utf-8 -*-
"""
状态层连续化（主线 1.3）：上一帧镜像 + 短时差分 + 状态趋势。

不做世界模型/长时记忆/预测，只做显示器侧最小连续状态解释。
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .schema import StateLayer, DecisionLayer, GoalLayer


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


# 风险变化阈值：超过视为明显上升/下降
_RISK_DELTA_UP = 0.08
_RISK_DELTA_DOWN = 0.06


def _mirror_from(
    state: StateLayer,
    decision: DecisionLayer,
    goal: GoalLayer,
    ctx: Dict[str, Any],
) -> Dict[str, Any]:
    """从当前 state/decision/goal/ctx 抽出用于差分的最小镜像。"""
    sampled = ctx.get("sampled")
    if sampled is None and ctx.get("inputs"):
        sampled = _get(ctx["inputs"], "sampled")
    return {
        "risk_score": _get(state, "risk_score"),
        "safety_level": _get(state, "safety_level"),
        "motion": _get(state, "motion"),
        "diff": _get(state, "diff"),
        "sampled": sampled,
        "decision_owner": _get(decision, "decision_owner"),
        "b2_impact_applied": _get(decision, "b2_impact_applied"),
        "floor_forced": _get(decision, "floor_forced"),
        "goal_type": _get(goal, "goal_type"),
        "subgoal_description": _get(goal, "subgoal_description"),
    }


def _one_line_summary(mirror: Dict[str, Any]) -> str:
    """根据镜像生成一句状态摘要（供下一帧作为 prev_state_summary 显示，viewer 可加「上一时刻：」前缀）。"""
    owner = mirror.get("decision_owner")
    floor = mirror.get("floor_forced")
    b2 = mirror.get("b2_impact_applied")
    sampled = mirror.get("sampled")
    risk = mirror.get("risk_score")

    if floor:
        return "触发守底采样"
    if b2:
        return "已进入谨慎观察"
    if owner == "sampling_gate" or sampled is False:
        return "节流跳过，正常推进"
    if risk is not None and risk >= 0.5:
        return "风险升高，谨慎观察"
    return "环境稳定，风险低，正常推进"


def _state_delta_summary(prev: Dict[str, Any], cur: Dict[str, Any]) -> str:
    """规则型短差分摘要。"""
    parts = []

    # 风险
    pr, cr = prev.get("risk_score"), cur.get("risk_score")
    if pr is not None and cr is not None:
        d = cr - pr
        if abs(d) < 0.03:
            pass  # 变化不大，不写
        elif d >= _RISK_DELTA_UP:
            parts.append("风险上升")
        elif d <= -_RISK_DELTA_DOWN:
            parts.append("风险下降")

    # 观察模式
    ps, cs = prev.get("sampled"), cur.get("sampled")
    if ps is False and cs is True:
        parts.append("从节流跳过转为主动观察")
    elif ps is True and cs is False:
        parts.append("从主动观察转为节流跳过")

    if prev.get("b2_impact_applied") is not True and cur.get("b2_impact_applied") is True:
        parts.append("进入谨慎观察")
    if prev.get("floor_forced") is not True and cur.get("floor_forced") is True:
        parts.append("触发守底采样")
    if prev.get("floor_forced") is True and cur.get("floor_forced") is not True:
        parts.append("守底解除，恢复正常")
    if prev.get("b2_impact_applied") is True and cur.get("b2_impact_applied") is not True:
        parts.append("B2 解除，恢复正常")

    # 决策责任
    po, co = prev.get("decision_owner"), cur.get("decision_owner")
    if po != co and po is not None and co is not None:
        parts.append(f"拍板者从 {po} 切换到 {co}")

    # 目标
    pg, cg = prev.get("goal_type"), cur.get("goal_type")
    if pg != cg and cg is not None:
        parts.append(f"目标从 {pg or '—'} 切换到 {cg}")

    if not parts:
        return "与上一时刻相比，变化不大"
    return "；".join(parts)


def _state_trend(prev: Dict[str, Any], cur: Dict[str, Any]) -> str:
    """规则型趋势标签：stable / improving / worsening / shifting / recovering。"""
    pr, cr = prev.get("risk_score"), cur.get("risk_score")
    po, co = prev.get("decision_owner"), cur.get("decision_owner")
    pb2, cb2 = prev.get("b2_impact_applied"), cur.get("b2_impact_applied")
    pfloor, cfloor = prev.get("floor_forced"), cur.get("floor_forced")
    ps, cs = prev.get("sampled"), cur.get("sampled")
    pg, cg = prev.get("goal_type"), cur.get("goal_type")
    psub, csub = prev.get("subgoal_description"), cur.get("subgoal_description")

    # worsening：风险上升 / 新进 B2 / 新进 floor / 从正常到谨慎或守底
    if pr is not None and cr is not None and cr - pr >= _RISK_DELTA_UP:
        return "worsening"
    if not pb2 and cb2:
        return "worsening"
    if not pfloor and cfloor:
        return "worsening"
    if (po == "controller" and co in ("b2_impact", "floor_guard")) or (po == "sampling_gate" and co == "floor_guard"):
        return "worsening"

    # recovering：从 floor_guard 或 B2 回到 controller；风险下降；sampled 恢复正常
    if (pfloor or pb2 or po in ("floor_guard", "b2_impact")) and co == "controller" and not cfloor and not cb2:
        return "recovering"
    if pr is not None and cr is not None and pr - cr >= _RISK_DELTA_DOWN:
        if not cb2 and not cfloor:
            return "recovering"
    if ps is False and cs is True and co == "controller":
        return "recovering"

    # shifting：目标切换 / 拍板者切换 / 节流→采样 / 子目标变化
    if pg != cg and cg is not None:
        return "shifting"
    if po != co:
        return "shifting"
    if ps is False and cs is True:
        return "shifting"
    if (psub or "") != (csub or ""):
        return "shifting"

    # improving：保守使用，仅风险明显下降且无新触发时
    if pr is not None and cr is not None and pr - cr >= _RISK_DELTA_DOWN and not cb2 and not cfloor:
        return "improving"

    return "stable"


def _goal_progress_delta(prev: Dict[str, Any], cur: Dict[str, Any]) -> str:
    """目标推进状态的变化。"""
    pfloor, cfloor = prev.get("floor_forced"), cur.get("floor_forced")
    pb2, cb2 = prev.get("b2_impact_applied"), cur.get("b2_impact_applied")
    pg, cg = prev.get("goal_type"), cur.get("goal_type")

    if cfloor:
        return "为守底暂停推进目标"
    if pg != cg and cur.get("goal_type") in ("hold_for_floor", "recheck_environment"):
        return "切换为重新确认环境"
    if cb2 and not pb2:
        return "转入谨慎观察，目标确认度待提升"
    if not cb2 and pb2:
        return "对目标确认度提升"
    if pg == cg and not cfloor and not cb2:
        return "目标推进无明显变化"
    return "目标推进无明显变化"


class StateTracker:
    """缓存上一帧最小状态镜像，生成连续状态摘要与趋势。"""

    def __init__(self) -> None:
        self._prev_mirror: Optional[Dict[str, Any]] = None
        self._prev_state_summary: Optional[str] = None

    def update(
        self,
        current_state: StateLayer,
        current_decision: DecisionLayer,
        current_goal: GoalLayer,
        ctx: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        基于上一帧镜像与当前 state/decision/goal 生成连续化四字段。
        返回: prev_state_summary, state_delta_summary, state_trend, goal_progress_delta
        调用后内部更新 _prev，供下一帧使用。
        """
        cur = _mirror_from(current_state, current_decision, current_goal, ctx)
        cur_summary = _one_line_summary(cur)

        if self._prev_mirror is None:
            out = {
                "prev_state_summary": "首帧，无上一时刻",
                "state_delta_summary": "—",
                "state_trend": "stable",
                "goal_progress_delta": "—",
            }
            self._prev_mirror = cur
            self._prev_state_summary = cur_summary
            return out

        prev = self._prev_mirror
        out = {
            "prev_state_summary": self._prev_state_summary or "—",
            "state_delta_summary": _state_delta_summary(prev, cur),
            "state_trend": _state_trend(prev, cur),
            "goal_progress_delta": _goal_progress_delta(prev, cur),
        }
        self._prev_mirror = cur
        self._prev_state_summary = cur_summary
        return out
