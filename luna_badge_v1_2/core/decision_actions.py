# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - 决策动作枚举定义

定义 DecisionAction 枚举，表示系统可以执行的各种决策动作。
"""

from enum import Enum


class DecisionAction(Enum):
    """
    决策动作枚举
    
    表示系统根据上下文和用户意图做出的决策动作类型。
    """
    CONTINUE_TASK = "continue_task"           # 继续当前任务
    INSERT_TASK = "insert_task"                # 插入子任务
    REPLACE_TASK = "replace_task"              # 替换当前任务
    RESUME_MAIN_TASK = "resume_main_task"      # 恢复主任务
    NO_OP = "no_op"                            # 无操作
    ASK_USER = "ask_user"                      # 询问用户
    TRIGGER_PLANB = "trigger_planB"             # 触发 PlanB 降级策略
    
    def __str__(self) -> str:
        """返回动作的字符串值"""
        return self.value


