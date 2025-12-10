# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - Decision Logger 实现

决策层日志记录器，负责记录所有决策相关的日志。
"""

import time
import json
from typing import Dict, Optional, Any
from core.decision_output import DecisionOutput
from core.intent_schema import ParsedIntent


def log_decision(
    event_type: str,
    parsed_intent: Optional[ParsedIntent],
    decision_output: DecisionOutput,
    task_context: Dict[str, Any]
) -> None:
    """
    记录决策日志
    
    Args:
        event_type: 事件类型
        parsed_intent: 解析后的用户意图（如果有）
        decision_output: 决策输出
        task_context: 任务上下文
    """
    log_entry = {
        "event_type": event_type,
        "intent_name": parsed_intent.intent_name if parsed_intent else None,
        "action": decision_output.action.value,
        "reason": getattr(decision_output, "reason", ""),
        "task_id": task_context.get("task_id", ""),
        "task_type": task_context.get("task_type", ""),
        "need_confirm": parsed_intent.need_confirm if parsed_intent else False,
        "timestamp": time.time()
    }
    
    # 输出到 stdout（结构化 JSON 格式）
    print(f"[Decision] {json.dumps(log_entry, ensure_ascii=False)}")

