"""
ScoreLogger: 模型评分日志记录器

统一记录模型评分与决策过程，用于后续分析和优化。

Patch-3-A: 增强支持聚合统计
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple

from .arbiter import ModelScore, ArbiterDecision


@dataclass
class ScoreLogEntry:
    """
    一次完整决策的日志记录。
    """
    task_id: str
    task_type: str
    winner: str
    scores: List[ModelScore]
    decision_error: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelStats:
    """
    针对单个 (task_type, model) 的长期统计信息。
    """
    task_type: str
    model: str
    total_calls: int = 0
    success_calls: int = 0
    failure_calls: int = 0
    sum_conf: float = 0.0  # 成功样本的 max_conf 总和
    sum_final_score: float = 0.0  # 成功样本的 final_score 总和
    last_error: str = ""  # 最近一次错误信息

    def record(self, s: ModelScore) -> None:
        """
        记录一次模型评分。

        Args:
            s: ModelScore 实例
        """
        self.total_calls += 1
        if s.ok:
            self.success_calls += 1
            self.sum_conf += s.max_conf
            self.sum_final_score += s.final_score
        else:
            self.failure_calls += 1
            if s.error:
                self.last_error = s.error

    @property
    def success_rate(self) -> float:
        """成功率"""
        if self.total_calls == 0:
            return 0.0
        return self.success_calls / float(self.total_calls)

    @property
    def avg_conf(self) -> float:
        """平均置信度"""
        if self.success_calls == 0:
            return 0.0
        return self.sum_conf / float(self.success_calls)

    @property
    def avg_final_score(self) -> float:
        """平均最终得分"""
        if self.success_calls == 0:
            return 0.0
        return self.sum_final_score / float(self.success_calls)


class ScoreLogger:
    """
    简易版本：将日志保存在内存，并提供聚合统计。

    未来可升级为写入文件、上传后台、做模型健康统计。
    """

    def __init__(self):
        """初始化日志记录器"""
        self._entries: List[ScoreLogEntry] = []
        # key: (task_type, model) -> ModelStats
        self._stats: Dict[Tuple[str, str], ModelStats] = {}

    # ---------- 日志记录 ----------

    def log(self, task_id: str, task_type: str, decision: ArbiterDecision) -> None:
        """
        记录一次决策日志。

        Args:
            task_id: 任务 ID
            task_type: 任务类型
            decision: 仲裁决策结果
        """
        entry = ScoreLogEntry(
            task_id=task_id,
            task_type=task_type,
            winner=decision.winner or "",
            scores=decision.scores,
            decision_error=decision.error or "",
        )
        self._entries.append(entry)

        # 更新聚合统计
        for s in decision.scores:
            key = (task_type, s.model)
            stats = self._stats.get(key)
            if stats is None:
                stats = ModelStats(task_type=task_type, model=s.model)
                self._stats[key] = stats
            stats.record(s)

    # ---------- 查询接口 ----------

    def get_all(self) -> List[ScoreLogEntry]:
        """
        获取所有日志记录。

        Returns:
            List[ScoreLogEntry]: 所有日志记录
        """
        return self._entries

    def clear(self) -> None:
        """清空所有日志记录和统计"""
        self._entries.clear()
        self._stats.clear()

    def get_recent(self, n: int = 10) -> List[ScoreLogEntry]:
        """
        获取最近的 N 条日志记录。

        Args:
            n: 记录数量

        Returns:
            List[ScoreLogEntry]: 最近的日志记录
        """
        return self._entries[-n:] if n > 0 else self._entries

    def get_stats(self, task_type: str, model: str) -> ModelStats:
        """
        获取指定 (task_type, model) 的统计信息。

        Args:
            task_type: 任务类型
            model: 模型名称

        Returns:
            ModelStats: 统计信息
        """
        key = (task_type, model)
        stats = self._stats.get(key)
        if stats is None:
            stats = ModelStats(task_type=task_type, model=model)
            self._stats[key] = stats
        return stats

    def get_stats_snapshot(self) -> Dict[str, Any]:
        """
        返回适合直接做可视化的快照（不含单条日志，只含聚合统计）。

        Returns:
            Dict[str, Any]: 统计快照，结构为 {task_type: {model: {...}}}
        """
        blocks: Dict[str, Dict[str, Any]] = {}

        for (task_type, model), s in self._stats.items():
            task_block = blocks.setdefault(task_type, {})
            task_block[model] = {
                "total_calls": s.total_calls,
                "success_calls": s.success_calls,
                "failure_calls": s.failure_calls,
                "success_rate": s.success_rate,
                "avg_conf": s.avg_conf,
                "avg_final_score": s.avg_final_score,
                "last_error": s.last_error,
            }

        return blocks

