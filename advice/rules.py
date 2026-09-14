"""
Advice v0 规则：只读 Task v2 状态，生成人类可理解的建议。
不执行、不触发 C、不改变 Task 状态。
"""
from tasks.types import TaskStatus


def advice_for_task(task, now: float):
    """
    根据 Task v2 状态生成建议。
    
    Args:
        task: Task v2 实例（BaseTask），必须有 state, last_reason, started_at, task_name
        now: 当前时间戳
    
    Returns:
        dict 或 None：建议数据（advice_id, category, text, confidence, evidence, is_safety）
    """
    duration = None
    if hasattr(task, 'started_at') and task.started_at is not None:
        duration = max(0.0, now - task.started_at)

    if task.state == TaskStatus.WAITING:
        return {
            "advice_id": "wait_condition",
            "category": "TASK_STATE",
            "text": "建议原地等待，当前条件尚未满足。",
            "confidence": 0.7,
            "evidence": {
                "task": getattr(task, 'task_name', 'Unknown'),
                "state": task.state.name if hasattr(task.state, 'name') else str(task.state),
                "reason": task.last_reason,
                "duration": duration,
            },
            "is_safety": False,
        }

    if task.state == TaskStatus.BLOCKED:
        return {
            "advice_id": "adjust_view",
            "category": "TASK_STATE",
            "text": "当前视野受限，建议稍微调整位置再观察。",
            "confidence": 0.6,
            "evidence": {
                "task": getattr(task, 'task_name', 'Unknown'),
                "state": task.state.name if hasattr(task.state, 'name') else str(task.state),
                "reason": task.last_reason,
                "duration": duration,
            },
            "is_safety": False,
        }

    if task.state == TaskStatus.TIMEOUT:
        return {
            "advice_id": "ask_next_step",
            "category": "TASK_STATE",
            "text": "等待时间较长，是否需要我帮你确认或更换方案？",
            "confidence": 0.8,
            "evidence": {
                "task": getattr(task, 'task_name', 'Unknown'),
                "state": task.state.name if hasattr(task.state, 'name') else str(task.state),
                "reason": task.last_reason,
                "duration": duration,
            },
            "is_safety": False,
        }

    return None
