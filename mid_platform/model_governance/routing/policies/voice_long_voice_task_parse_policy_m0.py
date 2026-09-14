# -*- coding: utf-8 -*-
"""
静态路由策略（M0 决策落档）— **长语音任务拆解主链真值**。

目标：把「主选 / 速度型备选 / 淘汰」与 **Provider 默认档位** 写入中台可审计状态。

**主链默认（写死）**
- 任务域 ``long_voice_task_parse`` → 主选 ``qwen-plus``，备选 ``qwen-turbo``。
- 百炼 ``QwenExternalLongInputModelProvider`` 默认档位 **optimized**（与
  ``capabilities.voice.providers.qwen_external_long_input_model_provider.DEFAULT_QWEN_AB_PROFILE``
  对齐；环境变量未设置 ``LUNA_QWEN_AB_PROFILE`` 时即此档）。
- ``legacy`` 档位 **不作为**默认，仅用于 A/B、回归、排障（见
  ``docs/architecture/voice/LUNA_VOICE_QWEN_EXTERNAL_PROVIDER_AB_DECISION_M0.md``）。

**Fallback 语义（与业务 orchestrator 分层）**
- **模型 HTTP 失败 / 超时 / 无结构化 JSON**：见 ``voice_long_input_parse_orchestrator`` → 可切 **规则链**（由 ``VoiceLongInputParseConfig`` 控制）。
- **校验失败**（validator 不通过）：整表不穿透 → **规则链**。
- **模型输出语义**（unsupported / clarification）：由模型 JSON + builder 表达，**不等于**「自动切 turbo」；**plus → turbo** 的多模型重试由**接入层**按本策略与 registry 卡实现。

路线图与阶段顺序：``docs/architecture/voice/LUNA_VOICE_LONG_VOICE_TASK_PARSE_MAINLINE_ROADMAP_M1.md``。

注意：本文件不自动注入业务主链；仅作为静态 policy 的可加载样例与真值记录。
"""

from __future__ import annotations

from mid_platform.model_governance.routing.model_route_policy import ModelRoutePolicy

# 与 Provider 模块常量对齐，供中台/registry 文档交叉引用（不在此导入 capabilities，避免环依赖）
TASK_DOMAIN_LONG_VOICE_TASK_PARSE = "long_voice_task_parse"
EXTERNAL_PROVIDER_AB_PROFILE_DEFAULT = "optimized"

# 定案：
# - primary: qwen-plus
# - fallback: qwen-turbo
# - deprecated: qwen3.5-flash（不进入主链候选池）
VOICE_LONG_VOICE_TASK_PARSE_POLICY_M0 = ModelRoutePolicy(
    policy_id="voice_long_voice_task_parse_policy_m0",
    task_domain_to_primary={TASK_DOMAIN_LONG_VOICE_TASK_PARSE: "qwen-plus"},
    task_domain_to_fallback={TASK_DOMAIN_LONG_VOICE_TASK_PARSE: "qwen-turbo"},
    default_fallback_model_id="qwen-turbo",
    fallback_to_rule_chain=True,
    shadow_candidates=[],
    background_only_models=["qwen3.5-flash"],
)

