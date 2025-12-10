# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - 事件类型枚举定义

定义系统事件类型枚举，用于事件总线和模块间通信。
"""

from enum import Enum


class EventType(Enum):
    """
    系统事件类型枚举
    
    用于标识系统中发生的各种事件类型，便于事件总线和模块间通信。
    """
    TASK_NODE_COMPLETE = "task_node_complete"     # 任务节点完成
    TASK_NODE_START = "task_node_start"            # 任务节点开始
    USER_INTENT = "user_intent"                    # 用户意图
    INQUIRY_RESPONSE = "inquiry_response"          # 问询响应
    SYSTEM_ALERT = "system_alert"                  # 系统告警
    USER_INACTIVE = "user_inactive"                # 用户无响应
    MODEL_STATUS = "model_status"                  # 模型状态变化
    
    def __str__(self) -> str:
        """返回事件类型的字符串值"""
        return self.value


