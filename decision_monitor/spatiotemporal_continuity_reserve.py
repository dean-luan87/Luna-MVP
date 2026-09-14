# -*- coding: utf-8 -*-
"""
Spatiotemporal Continuity Reserve M0（时空间连续性接口预留层）

定位（写死）：
- 连续性是内部强影响因子，应进入白盒与结构树依据层
- 前端默认只展示“影响结果”，不直出底层连续性细节
- M0 仅做接口预留 + 最小规则版影响摘要，不做连续帧跟踪算法/评分系统/轨迹重建

约束：
- 只读 frame/ctx 内已有字段（state 连续化摘要、grid 推荐、feedback/next_effect、recheck 等）
- 不改主逻辑
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


@dataclass
class SpatiotemporalContinuityReserveResult:
    continuity_support_level: str = "unknown"  # high/medium/low/broken/unknown
    continuity_influence_reason: Optional[str] = None
    continuity_preserved: bool = False
    continuity_broken: bool = False
    continuity_affected_module: Optional[str] = None
    continuity_source_summary: Optional[str] = None
    continuity_debug_note: Optional[str] = None  # 前端默认不主展示
    continuity_reserve_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "continuity_support_level": self.continuity_support_level,
            "continuity_influence_reason": self.continuity_influence_reason,
            "continuity_preserved": bool(self.continuity_preserved),
            "continuity_broken": bool(self.continuity_broken),
            "continuity_affected_module": self.continuity_affected_module,
            "continuity_source_summary": self.continuity_source_summary,
            "continuity_debug_note": self.continuity_debug_note,
            "continuity_reserve_applied": bool(self.continuity_reserve_applied),
        }


def build_spatiotemporal_continuity_reserve(frame: Dict[str, Any]) -> SpatiotemporalContinuityReserveResult:
    """
    M0 最小规则（写死，简单）：
    A) 路径继承（粗）：无明显 feedback-driven 改向，且 state_trend 稳定，且存在推荐格/主建议 => medium/high
    B) 用户反馈打断：存在 raw feedback 且 next_effect != none => broken
    C) 重入/重新搜索：recheck blocked / fallback / issue severe => low
    D) 无足够信息：unknown
    """
    state = frame.get("state") if isinstance(frame.get("state"), dict) else {}
    grid = frame.get("local_task_space_grid") if isinstance(frame.get("local_task_space_grid"), dict) else {}
    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else {}
    metrics = frame.get("reasoning_tree_metrics") if isinstance(frame.get("reasoning_tree_metrics"), dict) else {}
    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else {}
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else {}

    raw_fb = _s(cib.get("confirmation_input_raw_text"))
    next_effect = _s(cib.get("confirmation_bridge_next_effect")) or "none"
    mapped_type = _s(cib.get("confirmation_input_type"))

    trend = _s(state.get("state_trend")) or "stable"
    prev_sum = _s(state.get("prev_state_summary"))

    rec_cell = _s(grid.get("recommended_search_cell_id"))
    suggested_zone = _s(osi.get("suggested_search_zone"))
    recheck_blocked = rp.get("recheck_blocked") is True
    terminal = _s(osi.get("search_terminal_status")) or "none"

    issue = _s(metrics.get("possible_tree_issue_type"))
    severe = issue in ("blocked_without_resolution", "feedback_not_effective")

    # Rule B: feedback breaks continuity (direction switch)
    if raw_fb and next_effect and next_effect != "none":
        return SpatiotemporalContinuityReserveResult(
            continuity_support_level="broken",
            continuity_influence_reason="用户反馈改变了当前路径/推进效果，连续性被打断（规则版）。",
            continuity_preserved=False,
            continuity_broken=True,
            continuity_affected_module="confirmation_input_bridge",
            continuity_source_summary=f"broken by feedback: type={mapped_type or '—'} next_effect={next_effect}",
            continuity_debug_note=f"prev_state={prev_sum or '—'} trend={trend}",
            continuity_reserve_applied=True,
        )

    # Rule C: re-enter / weak continuity
    if recheck_blocked or terminal in ("blocked",) or severe:
        return SpatiotemporalContinuityReserveResult(
            continuity_support_level="low",
            continuity_influence_reason="当前处于补证阻断/严重 issue 影响下，决策不再强继承上一轮路径（规则版）。",
            continuity_preserved=False,
            continuity_broken=False,
            continuity_affected_module="recheck_planner" if recheck_blocked else "reasoning_tree_metrics",
            continuity_source_summary=f"re-enter/weak: blocked={recheck_blocked} issue={issue or '—'} terminal={terminal}",
            continuity_debug_note=f"prev_state={prev_sum or '—'} trend={trend}",
            continuity_reserve_applied=True,
        )

    # Rule A: preserved (coarse)
    has_path_signal = bool(rec_cell or suggested_zone)
    if (not raw_fb) and trend in ("stable", "improving") and has_path_signal:
        level = "high" if rec_cell and trend == "stable" else "medium"
        return SpatiotemporalContinuityReserveResult(
            continuity_support_level=level,
            continuity_influence_reason="当前主路径大体继承上一轮搜索方向/建议，连续性提供支撑（规则版）。",
            continuity_preserved=True,
            continuity_broken=False,
            continuity_affected_module="reasoning_structure_tree",
            continuity_source_summary=f"inherited path: rec_cell={rec_cell or '—'} trend={trend}",
            continuity_debug_note=f"prev_state={prev_sum or '—'}",
            continuity_reserve_applied=True,
        )

    # Rule D: unknown
    return SpatiotemporalContinuityReserveResult(
        continuity_support_level="unknown",
        continuity_influence_reason="当前信息不足以判断连续性影响（M0 预留）。",
        continuity_preserved=False,
        continuity_broken=False,
        continuity_affected_module=None,
        continuity_source_summary=None,
        continuity_debug_note=f"prev_state={prev_sum or '—'} trend={trend} rec_cell={rec_cell or '—'}",
        continuity_reserve_applied=True,
    )

