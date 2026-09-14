# -*- coding: utf-8 -*-
"""
M0：长语音任务拆解（long_voice_task_parse）相关模型注册卡（静态样例 + 真值记录）。

主选 ``qwen-plus`` / 备选 ``qwen-turbo`` / flash 淘汰 — 与 ``VOICE_LONG_VOICE_TASK_PARSE_POLICY_M0`` 一致。  
外部长输入 Provider 主链默认档位 **optimized** 见 ``EXTERNAL_PROVIDER_AB_PROFILE_DEFAULT``（policy 模块）及 Provider 决策短文。

说明：本文件不自动写入 registry service；由上层在初始化阶段选择性加载。
"""

from __future__ import annotations

from mid_platform.model_governance.schemas.model_registry_card import ModelRegistryCard


def qwen_plus_long_voice_task_parse_card() -> ModelRegistryCard:
    return ModelRegistryCard(
        model_id="qwen-plus",
        display_name="Qwen Plus (Model Studio compatible) — long_voice_task_parse",
        provider="qwen_model_studio_compatible",
        version="m0",
        deployment_type="external_api",
        runtime_location="cloud",
        role_type="production",
        capability_domains=["voice"],
        supported_tasks=["long_voice_task_parse"],
        input_contract_id="voice_long_input_text",
        input_contract_version="v1",
        output_contract_id="voice_task_parse_v1_1",
        output_contract_version="v1_1",
        allowed_in_mainline=True,
        allowed_in_shadow_mode=True,
        allowed_for_user_facing=True,
        fallback_target_model_id="qwen-turbo",
        fallback_to_rule_chain=True,
        latency_tier="medium",
        cost_tier="medium",
        schema_guard_required=True,
        self_judgement_forbidden=True,
        auto_promotion_forbidden=True,
        enabled=True,
        status="active",
        priority=1,
        owner_module="capabilities.voice",
    )


def qwen_turbo_long_voice_task_parse_card() -> ModelRegistryCard:
    return ModelRegistryCard(
        model_id="qwen-turbo",
        display_name="Qwen Turbo (Model Studio compatible) — long_voice_task_parse backup",
        provider="qwen_model_studio_compatible",
        version="m0",
        deployment_type="external_api",
        runtime_location="cloud",
        role_type="production",
        capability_domains=["voice"],
        supported_tasks=["long_voice_task_parse"],
        input_contract_id="voice_long_input_text",
        input_contract_version="v1",
        output_contract_id="voice_task_parse_v1_1",
        output_contract_version="v1_1",
        allowed_in_mainline=True,
        allowed_in_shadow_mode=True,
        allowed_for_user_facing=True,
        fallback_target_model_id=None,
        fallback_to_rule_chain=True,
        latency_tier="low",
        cost_tier="low",
        schema_guard_required=True,
        self_judgement_forbidden=True,
        auto_promotion_forbidden=True,
        enabled=True,
        status="active",
        priority=2,
        owner_module="capabilities.voice",
    )


def qwen_flash_long_voice_task_parse_deprecated_card() -> ModelRegistryCard:
    return ModelRegistryCard(
        model_id="qwen3.5-flash",
        display_name="Qwen 3.5 Flash — deprecated for user-facing long_voice_task_parse",
        provider="qwen_model_studio_compatible",
        version="m0",
        deployment_type="external_api",
        runtime_location="cloud",
        role_type="production",
        capability_domains=["voice"],
        supported_tasks=["long_voice_task_parse"],
        input_contract_id="voice_long_input_text",
        input_contract_version="v1",
        output_contract_id="voice_task_parse_v1_1",
        output_contract_version="v1_1",
        allowed_in_mainline=False,
        allowed_in_shadow_mode=True,
        allowed_for_user_facing=False,
        fallback_target_model_id=None,
        fallback_to_rule_chain=True,
        latency_tier="high",
        cost_tier="low",
        schema_guard_required=True,
        self_judgement_forbidden=True,
        auto_promotion_forbidden=True,
        enabled=False,
        status="deprecated",
        priority=99,
        owner_module="capabilities.voice",
    )


REGISTRY_CARDS_M0 = [
    qwen_plus_long_voice_task_parse_card(),
    qwen_turbo_long_voice_task_parse_card(),
    qwen_flash_long_voice_task_parse_deprecated_card(),
]

