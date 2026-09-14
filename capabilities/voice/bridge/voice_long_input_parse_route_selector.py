# -*- coding: utf-8 -*-
"""
长语音解析路由选择（v1）。

parse_mode：
- rule_only：仅规则链
- model_preferred_with_rule_fallback：优先模型 Provider，失败/超时/校验失败则规则链

model_only：本轮不开放（避免无兜底）。
"""

from __future__ import annotations

from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig


def should_use_rule_chain_only(cfg: VoiceLongInputParseConfig) -> bool:
    return cfg.parse_mode == "rule_only" or not cfg.enable_model_adapter


def should_attempt_model_chain(
    cfg: VoiceLongInputParseConfig,
    has_provider: bool,
) -> bool:
    return (
        cfg.parse_mode == "model_preferred_with_rule_fallback"
        and cfg.enable_model_adapter
        and has_provider
    )
