"""
Advice Engine v0：只读建议生成引擎。
不执行、不触发 C、不改变 Task 状态。
"""
from typing import List, Any, Optional

from advice.schema import Advice, AdviceTask
from advice.rules import advice_for_task


class AdviceEngine:
    """Advice Engine：根据 Task v2 状态生成建议。"""

    def generate(self, tasks: List[Any], now: float, context: Optional[dict] = None) -> List[Advice]:
        """
        为给定的任务列表生成建议。
        
        Args:
            tasks: Task v2 实例列表（BaseTask）
            now: 当前时间戳
        
        Returns:
            Advice 列表：每个任务最多一个建议
        """
        if tasks and isinstance(tasks[0], AdviceTask):
            return self._generate_from_advice_tasks(tasks, now, context)

        advices = []
        for t in tasks:
            data = advice_for_task(t, now)
            if data:
                advices.append(Advice(**data))
        return advices

    def generate_decisions(self, tasks: List[Any], now: float, context: Optional[dict] = None) -> List[dict]:
        """
        将 Advice 转为 Decision 边界可消费结构。
        """
        decisions = []
        for advice in self.generate(tasks, now, context):
            decisions.append({
                "type": "SPEAK",
                "text": advice.text,
                "advice_id": advice.advice_id,
                "advice_category": advice.category,
                "is_safety": advice.is_safety,
            })
        return decisions

    def _generate_from_advice_tasks(
        self,
        tasks: List[AdviceTask],
        now: float,
        context: Optional[dict] = None,
    ) -> List[Advice]:
        advices: List[Advice] = []
        for task in tasks:
            data = self._advice_from_task(task, now, context)
            if data:
                advices.append(Advice(**data))
        return advices

    def _advice_from_task(self, task: AdviceTask, now: float, context: Optional[dict]) -> Optional[dict]:
        if task.task_type == "REMINDER_FREQUENCY":
            return {
                "advice_id": "REMIND_PATH_CLEAR",
                "category": "REMINDER_FREQUENCY",
                "text": "前方道路通畅，可以继续前行",
                "confidence": 0.6,
                "evidence": {
                    "reason": task.context.get("reason"),
                    "env_mode": task.context.get("env_mode"),
                },
                "is_safety": False,
            }
        return None
