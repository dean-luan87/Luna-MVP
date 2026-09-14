# -*- coding: utf-8 -*-
"""
任务域一级分类 v1（与 docs/architecture/task/LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md 一致）。
"""

from __future__ import annotations

# 八个一级域 id（primary_domain / secondary_domains 取值）
NAVIGATION = "navigation"
OBSERVATION = "observation"
TASK_CONTROL = "task_control"
TASK_QUERY = "task_query"
DEVICE_CONTROL = "device_control"
CONFIRMATION_FEEDBACK = "confirmation_feedback"
NO_TASK_OBSERVATION = "no_task_observation"
UNSUPPORTED_OR_REJECT = "unsupported_or_reject"
# 非任务长对话占位（情感引擎 / 陪聊未来接入；当前不生成 task_plan、不 reject 为无效）
NON_TASK_DIALOGUE_FUTURE = "non_task_dialogue_future"

PRIMARY_DOMAIN_V1: tuple[str, ...] = (
    NAVIGATION,
    OBSERVATION,
    TASK_CONTROL,
    TASK_QUERY,
    DEVICE_CONTROL,
    CONFIRMATION_FEEDBACK,
    NO_TASK_OBSERVATION,
    UNSUPPORTED_OR_REJECT,
    NON_TASK_DIALOGUE_FUTURE,
)
