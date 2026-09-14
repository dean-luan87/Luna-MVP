# -*- coding: utf-8 -*-
"""
长语音反馈与互动语义（v1 固定枚举）。

目标：稳定表达「听懂什么、缺什么、能否做、执行到哪」，不是拟人陪聊。
不接 TTS、不自动生成最终话术；模板供策略层引用。

情感引擎原则（架构边界）：
情感引擎可增强任务理解与建议，但不得擅自篡改用户明确任务；
体验增强须为用户确认、或弱插入且不影响主任务锚点。
"""

from __future__ import annotations

# —— 主反馈 6 类（与 LUNA_VOICE_LONG_INPUT_FEEDBACK_AND_INTERACTION_V1.md 一致）——

TASK_UNDERSTOOD_AND_READY = "task_understood_and_ready"
TASK_UNDERSTOOD_BUT_NEED_CLARIFICATION = "task_understood_but_need_clarification"
TASK_UNDERSTOOD_BUT_NEED_CONFIRMATION = "task_understood_but_need_confirmation"
PARTIALLY_SUPPORTED = "partially_supported"
UNSUPPORTED_OR_REJECTED = "unsupported_or_rejected"
MIXED_INPUT_ACKNOWLEDGED = "mixed_input_acknowledged"

PRIMARY_FEEDBACK_MODES_V1: tuple[str, ...] = (
    TASK_UNDERSTOOD_AND_READY,
    TASK_UNDERSTOOD_BUT_NEED_CLARIFICATION,
    TASK_UNDERSTOOD_BUT_NEED_CONFIRMATION,
    PARTIALLY_SUPPORTED,
    UNSUPPORTED_OR_REJECTED,
    MIXED_INPUT_ACKNOWLEDGED,
)

# —— 执行过程反馈 4 类 ——
EXECUTION_STARTED = "execution_started"
EXECUTION_PROGRESS = "execution_progress"
EXECUTION_WAITING_USER = "execution_waiting_user"
EXECUTION_COMPLETED = "execution_completed"

EXECUTION_FEEDBACK_MODES: tuple[str, ...] = (
    EXECUTION_STARTED,
    EXECUTION_PROGRESS,
    EXECUTION_WAITING_USER,
    EXECUTION_COMPLETED,
)

# —— 后续情感 / 体验增强（挂 task_plan_v2 候选，当前仅占位）——
EXPERIENCE_ENHANCEMENT_SUGGESTION = "experience_enhancement_suggestion"

# —— 无任务长对话保留式出口（非 6 类主任务枚举之一，结构化 Schema 默认使用）——
NON_TASK_PRESERVED_FOR_FUTURE = "non_task_preserved_for_future"

# —— 无任务互动（观察 / 临时问询等）——
NO_TASK_OBSERVATION_DIRECT = "no_task_observation_direct"
# 兼容旧常量名，与 NON_TASK_PRESERVED_FOR_FUTURE 同值
NO_TASK_LONG_DIALOGUE_ACK = NON_TASK_PRESERVED_FOR_FUTURE

# —— 临时插话 / 插入任务（概念位，供编排层消费）——
TEMP_QUERY_DIRECT = "temp_query_direct"
TEMP_INSERT_TASK_ACK = "temp_insert_task_ack"

# 推荐模板占位（策略层可覆盖）
TEMPLATE_TASK_READY = "我明白了。接下来我会先做 {a}，再做 {b}。"
TEMPLATE_NEED_CLARIFICATION = "我知道你想做 {intent}，但还需要你告诉我 {missing}。"
TEMPLATE_NEED_CONFIRMATION = "我建议这样安排：先做 {a}，再做 {b}。你要我这样做吗？"
TEMPLATE_PARTIALLY_SUPPORTED = "我可以先帮你做 {supported}，但 {unsupported} 这一步我现在还不能直接处理。"
TEMPLATE_UNSUPPORTED = "这个请求我现在还不能直接执行。"
TEMPLATE_MIXED_ACK = "我先帮你处理任务部分，其他内容我记住了。"
TEMPLATE_NO_TASK_HEARD = "我听到了。这个我先记下来。"
TEMPLATE_EXEC_STARTED = "我开始处理了。先做 {step}。"
TEMPLATE_EXEC_PROGRESS = "已经完成 {done}，接下来做 {next}。"
TEMPLATE_EXEC_WAIT_USER = "我现在需要你确认一下，是否继续做 {next}？"
TEMPLATE_EXEC_COMPLETED = "已经完成这次任务。"
TEMPLATE_TEMP_INSERT = "我会先处理这个临时任务，再回到原来的任务。"

# 兼容旧常量名（内部迁移用，新代码请用 PRIMARY 命名）
TASK_UNDERSTOOD_READY = TASK_UNDERSTOOD_AND_READY
TASK_NEED_DETAIL = TASK_UNDERSTOOD_BUT_NEED_CLARIFICATION
TASK_SUGGEST_REORDER_OR_PLAN = TASK_UNDERSTOOD_BUT_NEED_CONFIRMATION
TASK_PARTIAL_UNSUPPORTED = PARTIALLY_SUPPORTED
NON_TASK_PRESERVED_ACK = MIXED_INPUT_ACKNOWLEDGED

ALL_FEEDBACK_KINDS: tuple[str, ...] = PRIMARY_FEEDBACK_MODES_V1 + EXECUTION_FEEDBACK_MODES + (
    EXPERIENCE_ENHANCEMENT_SUGGESTION,
    NON_TASK_PRESERVED_FOR_FUTURE,
    NO_TASK_OBSERVATION_DIRECT,
    TEMP_QUERY_DIRECT,
    TEMP_INSERT_TASK_ACK,
)
