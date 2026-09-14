# -*- coding: utf-8 -*-
"""
运行态任务态覆盖（仅用于测试/验证，不写配置）

用于 ACTIVE × 视频 等最小验证脚本：强制本次运行使用 ACTIVE，
从而触发 arbitration → K → L，跑完即清理，不污染默认配置。
"""

from __future__ import annotations

from typing import Optional

from intervention.eligibility import TaskState


class TaskStateOverride:
    """运行态覆盖：仅本次进程生效，clear() 后恢复推断值。"""

    _override: Optional[TaskState] = None
    _source: str = ""

    @classmethod
    def set_active(cls, task_type: str = "NAVIGATION", source: str = "OVERRIDE") -> None:
        """强制本次运行使用 ACTIVE（任意 task_type 均可）。"""
        cls._override = TaskState.ACTIVE
        cls._source = source

    @classmethod
    def clear(cls) -> None:
        """清除覆盖，后续恢复 infer_task_state 推断。"""
        cls._override = None
        cls._source = ""

    @classmethod
    def get(cls) -> Optional[TaskState]:
        """若已 set_active 则返回 ACTIVE，否则 None。"""
        return cls._override
