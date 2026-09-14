# -*- coding: utf-8 -*-
"""
G) ACTIVE × 多任务并行「介入仲裁 v0」
I) 多任务「跨 tick 公平性」v0

当 多个任务同时具备介入资格 时，用可解释、可体检、非学习的仲裁器决定：
- 谁先介入
- 谁延后
- 谁本段不说

公平性：短期靠仲裁分数，长期靠"未满足补偿"。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# I) 公平性补偿 v0（冻结）
FAIRNESS_BOOST_PER_MISS = 0.1
FAIRNESS_BOOST_CAP = 0.3

# v0 任务类型优先级（固定）
SAFETY = "SAFETY"
NAVIGATION = "NAVIGATION"
ENV_AWARENESS = "ENV_AWARENESS"
TASK_STATE = "TASK_STATE"

# 将 advice_category 映射到 arbitrator task_type
CATEGORY_TO_TASK_TYPE: Dict[str, str] = {
    "TASK_STATE": TASK_STATE,
    "NAVIGATION_HINT": NAVIGATION,
    "ENV_AWARENESS": ENV_AWARENESS,
    "SAFETY_REMINDER": SAFETY,
    "REMINDER_FREQUENCY": ENV_AWARENESS,
}


@dataclass
class CandidateTask:
    """v0 只读：每个 tick 收集的候选任务（已通过主线 A eligibility）"""
    task_id: str
    task_type: str  # NAVIGATION / ENV_AWARENESS / TASK_STATE / SAFETY
    engagement_level: str  # L1 | L2 | L3
    pal: float
    complexity: float
    urgency: float  # v0 固定映射
    last_spoken_ts: float
    # 原始 decision 引用（用于后续 speak）
    decision: Dict[str, Any] = field(default_factory=dict)


# v0 权重（冻结）
W_LEVEL = 0.5
W_PAL = 0.3
W_URG = 0.2
T_MIN = 8.0  # 冷却最小间隔（秒）
SCORE_THRESHOLD = 0.25  # 最高分 < 此值 → 本 tick 不介入

LEVEL_SCORE: Dict[str, float] = {"L1": 0.3, "L2": 0.6, "L3": 1.0}
URGENCY_BY_TYPE: Dict[str, float] = {
    NAVIGATION: 0.8,
    ENV_AWARENESS: 0.6,
    TASK_STATE: 0.4,
    SAFETY: 1.0,
}


def _map_category_to_task_type(advice_category: Optional[str], is_safety: bool) -> str:
    if is_safety:
        return SAFETY
    if advice_category and advice_category in CATEGORY_TO_TASK_TYPE:
        return CATEGORY_TO_TASK_TYPE[advice_category]
    return TASK_STATE


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


@dataclass
class TaskFairness:
    """I) 公平性状态（只读记忆），只在 ENGAGED 内维护"""
    task_id: str
    missed_count: int
    last_win_ts: float


def _fairness_boost(missed_count: int) -> float:
    """I) 公平补偿因子：clamp(missed * 0.1, 0, 0.3)"""
    return _clamp(missed_count * FAIRNESS_BOOST_PER_MISS, 0, FAIRNESS_BOOST_CAP)


class ArbitratorV0:
    """
    多任务介入仲裁 v0。
    I) 跨 tick 公平性：missed_count 补偿，ENGAGED 结束清零。
    """

    def __init__(self):
        self._last_spoken: Dict[str, float] = {}  # task_id -> ts
        self._fairness: Dict[str, TaskFairness] = {}  # task_id -> TaskFairness

    def _get_missed(self, task_id: str) -> int:
        return self._fairness.get(task_id, TaskFairness(task_id, 0, 0.0)).missed_count

    def _update_fairness_after_pick(
        self,
        winner: Optional[CandidateTask],
        deferred: List[CandidateTask],
        all_candidates: List[CandidateTask],
        now: float,
    ) -> None:
        """I) 更新公平性状态：winner 清零，deferred +1，无 winner 时全部 +1"""
        if winner:
            self._fairness[winner.task_id] = TaskFairness(winner.task_id, 0, now)
            for t in deferred:
                prev = self._fairness.get(t.task_id, TaskFairness(t.task_id, 0, 0.0))
                self._fairness[t.task_id] = TaskFairness(
                    t.task_id, prev.missed_count + 1, prev.last_win_ts
                )
        else:
            for t in all_candidates:
                prev = self._fairness.get(t.task_id, TaskFairness(t.task_id, 0, 0.0))
                self._fairness[t.task_id] = TaskFairness(
                    t.task_id, prev.missed_count + 1, prev.last_win_ts
                )

    def pick(
        self,
        tasks: List[CandidateTask],
        now: float,
        control_mode: str,
    ) -> Tuple[Optional[CandidateTask], List[CandidateTask], Dict[str, float], Dict[str, Any]]:
        """
        仲裁：选出一个 winner，其余 deferred。
        I) final_score = base * cooldown + fairness_boost

        Returns:
            (winner, deferred_list, scores_dict, fairness_dict)
        """
        if not tasks:
            return None, [], {}, {}

        # SAFETY 永远最高，绕过仲裁；I) SAFETY 不参与公平，但 deferred 需 +1
        safety_tasks = [t for t in tasks if t.task_type == SAFETY]
        if safety_tasks:
            winner = safety_tasks[0]
            deferred = [t for t in tasks if t.task_id != winner.task_id]
            scores = {t.task_id: (1.0 if t.task_type == SAFETY else 0.0) for t in tasks}
            self._update_fairness_after_pick(winner, deferred, tasks, now)
            fairness = self._build_fairness_dict(tasks)
            return winner, deferred, scores, fairness

        # GUARDED：只允许 NAVIGATION 和 SAFETY（SAFETY 已处理，此处只剩 NAVIGATION）
        if control_mode == "GUARDED":
            tasks = [t for t in tasks if t.task_type == NAVIGATION]

        if not tasks:
            return None, [], {}, {}

        scored: List[Tuple[CandidateTask, float, float]] = []  # (task, final_score, fairness_boost)
        for t in tasks:
            base = (
                W_LEVEL * LEVEL_SCORE.get(t.engagement_level, 0.3)
                + W_PAL * _clamp(t.pal, 0, 1)
                + W_URG * URGENCY_BY_TYPE.get(t.task_type, 0.4)
            )
            elapsed = now - t.last_spoken_ts
            cooldown_penalty = _clamp(elapsed / T_MIN, 0, 1)
            boost = _fairness_boost(self._get_missed(t.task_id))
            final_score = base * cooldown_penalty + boost
            scored.append((t, final_score, boost))

        scored.sort(key=lambda x: x[1], reverse=True)
        winner, score, _ = scored[0]

        if score < SCORE_THRESHOLD:
            self._update_fairness_after_pick(None, [], [t for t, _, _ in scored], now)
            fairness = self._build_fairness_dict([t for t, _, _ in scored])
            return None, [t for t, _, _ in scored], {t.task_id: round(s, 3) for t, s, _ in scored}, fairness

        deferred = [t for t, _, _ in scored[1:]]
        scores = {t.task_id: round(s, 3) for t, s, _ in scored}
        self._update_fairness_after_pick(winner, deferred, [t for t, _, _ in scored], now)
        fairness = self._build_fairness_dict([t for t, _, _ in scored])
        return winner, deferred, scores, fairness

    def _build_fairness_dict(self, tasks: List[CandidateTask]) -> Dict[str, Any]:
        """I) Trace 用 fairness 结构"""
        out: Dict[str, Any] = {}
        for t in tasks:
            if t.task_type == SAFETY:
                continue
            f = self._fairness.get(t.task_id, TaskFairness(t.task_id, 0, 0.0))
            out[t.task_id] = {"missed": f.missed_count, "boost": round(_fairness_boost(f.missed_count), 2)}
        return out

    def record_spoken(self, task_id: str, now: float) -> None:
        """记录某任务已播报（用于冷却）"""
        self._last_spoken[task_id] = now

    def clear_state(self) -> None:
        """ENGAGED 结束时清空（不跨段记忆）"""
        self._last_spoken.clear()
        self._fairness.clear()

    def get_last_spoken_ts(self, task_id: str) -> float:
        """获取某任务上次播报时间"""
        return self._last_spoken.get(task_id, 0.0)


def build_candidate_tasks(
    advice_decisions: List[Dict[str, Any]],
    now: float,
    engagement_level: str,
    pal: float,
    complexity: float,
    arbitrator: ArbitratorV0,
) -> List[CandidateTask]:
    """
    将 advice_decisions 转为 CandidateTask 列表。
    """
    candidates: List[CandidateTask] = []
    for d in advice_decisions:
        if d.get("type") != "SPEAK" or not d.get("text"):
            continue
        task_id = d.get("advice_id") or f"fallback_{len(candidates)}"
        is_safety = bool(d.get("is_safety"))
        cat = d.get("advice_category")
        task_type = _map_category_to_task_type(cat, is_safety)
        urgency = URGENCY_BY_TYPE.get(task_type, 0.4)
        last_ts = arbitrator.get_last_spoken_ts(task_id)
        candidates.append(
            CandidateTask(
                task_id=task_id,
                task_type=task_type,
                engagement_level=engagement_level,
                pal=pal,
                complexity=complexity,
                urgency=urgency,
                last_spoken_ts=last_ts,
                decision=d,
            )
        )
    return candidates


_instance: Optional[ArbitratorV0] = None


def get_arbitrator_v0() -> ArbitratorV0:
    global _instance
    if _instance is None:
        _instance = ArbitratorV0()
    return _instance


def reset_arbitrator_state() -> None:
    global _instance
    if _instance:
        _instance.clear_state()
