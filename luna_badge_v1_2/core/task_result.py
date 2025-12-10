# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - 任务结果结构定义

定义 TaskResult 结构，用于表示任务执行的结果。
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class TaskResult:
    """
    任务结果结构
    
    Attributes:
        status: 任务状态，"ok" | "failed" | "cancelled"
        reason: 状态原因说明
        task_id: 任务 ID
        task_type: 任务类型
    """
    status: Literal["ok", "failed", "cancelled"]
    reason: str
    task_id: str
    task_type: str
    
    def __repr__(self) -> str:
        """字符串表示"""
        return (
            f"TaskResult(status='{self.status}', reason='{self.reason}', "
            f"task_id='{self.task_id}', task_type='{self.task_type}')"
        )
    
    def is_success(self) -> bool:
        """判断任务是否成功"""
        return self.status == "ok"
    
    def is_failed(self) -> bool:
        """判断任务是否失败"""
        return self.status == "failed"
    
    def is_cancelled(self) -> bool:
        """判断任务是否被取消"""
        return self.status == "cancelled"


