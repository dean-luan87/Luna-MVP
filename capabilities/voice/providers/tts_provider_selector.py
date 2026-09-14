# -*- coding: utf-8 -*-
"""
TTS provider selector (Stage-2).

职责：
- 系统控制 provider 顺序（主权在系统，不在前端）
- 返回选择结果与原因（可观察）
- 作为 provider chain 的唯一公开入口
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from capabilities.voice.output.tts_provider_runtime import TTSProviderResult
from capabilities.voice.providers.provider_types import LocalTTSProvider
from capabilities.voice.providers.tts_fallback_manager import TTSChainResult, _run_tts_chain_internal


@dataclass(frozen=True)
class ProviderSelection:
    provider_order: List[str]
    preset_name: str
    chosen_provider: str
    reason: str


def select_provider(
    *,
    provider_order: List[str],
    preset_provider: str,
    active_provider: str,
    fallback_provider: str,
) -> ProviderSelection:
    """
    选择逻辑（硬约束）：
    - 默认按 provider_order
    - preset 只能影响“建议 provider”，不能绕过系统顺序
    - active_provider 必须在 provider_order 内，否则视为配置错误
    """
    if not provider_order:
        return ProviderSelection(provider_order=[], preset_name="", chosen_provider="", reason="EMPTY_PROVIDER_ORDER")
    if active_provider not in provider_order:
        return ProviderSelection(
            provider_order=provider_order,
            preset_name="",
            chosen_provider=provider_order[0],
            reason="CONFIG_ERROR_ACTIVE_NOT_IN_ORDER",
        )

    # chosen provider = active_provider（系统主权）
    return ProviderSelection(
        provider_order=provider_order,
        preset_name="",
        chosen_provider=active_provider,
        reason="ACTIVE_PROVIDER",
    )


def execute_provider_chain(
    *,
    request_id: str,
    text: str,
    preset_name: str,
    preset: Dict,
    provider_order: List[str],
    active_provider: str,
    fallback_provider: str,
    providers: Dict[str, LocalTTSProvider],
    timeouts_ms: Dict[str, int],
    fallback_enabled: bool = True,
) -> TTSChainResult:
    """
    Provider chain 唯一公开入口：
    - 外部只调用 selector，不直调 fallback manager
    - fallback manager 作为内部机制使用
    """
    return _run_tts_chain_internal(
        request_id=request_id,
        text=text,
        preset_name=preset_name,
        preset=preset,
        provider_order=provider_order,
        active_provider=active_provider,
        fallback_provider=fallback_provider,
        providers=providers,
        timeouts_ms=timeouts_ms,
        fallback_enabled=fallback_enabled,
    )

