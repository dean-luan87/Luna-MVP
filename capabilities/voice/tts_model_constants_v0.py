# -*- coding: utf-8 -*-
"""TTS DashScope model constants — Phase-Voice-TTS-Model-Deprecation-Minimal-Patch-v1-001."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

DEFAULT_TTS_MODEL = "cosyvoice-v3-flash"
LEGACY_QWEN_TTS_MODEL = "qwen-tts"
TRANSITIONAL_QWEN_TTS_FLASH_MODEL = "qwen-tts-flash"
TTS_MODEL_ENV = "LUNA_TTS_MODEL"
LEGACY_QWEN_TTS_RETIREMENT_DATE = "2026-09-07"

ALLOWED_EXPLICIT_MODELS: Tuple[str, ...] = (
    DEFAULT_TTS_MODEL,
    LEGACY_QWEN_TTS_MODEL,
    TRANSITIONAL_QWEN_TTS_FLASH_MODEL,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ResolvedTTSModel:
    model: str
    source: str
    warnings: Tuple[str, ...] = field(default_factory=tuple)
    deprecated: bool = False
    transitional: bool = False


def resolve_tts_model(*, explicit: Optional[str] = None) -> ResolvedTTSModel:
    """Resolve runtime TTS model without performing synthesis."""
    requested = str(explicit or os.getenv(TTS_MODEL_ENV) or "").strip()
    if not requested:
        return ResolvedTTSModel(model=DEFAULT_TTS_MODEL, source="default")

    if requested == LEGACY_QWEN_TTS_MODEL:
        return ResolvedTTSModel(
            model=requested,
            source="explicit_or_env",
            warnings=(
                f"deprecated_notice: {LEGACY_QWEN_TTS_MODEL} retires on {LEGACY_QWEN_TTS_RETIREMENT_DATE}; "
                f"use {DEFAULT_TTS_MODEL}",
            ),
            deprecated=True,
        )
    if requested == TRANSITIONAL_QWEN_TTS_FLASH_MODEL:
        return ResolvedTTSModel(
            model=requested,
            source="explicit_or_env",
            warnings=(
                f"transitional_notice: {TRANSITIONAL_QWEN_TTS_FLASH_MODEL} is transitional only; "
                f"preferred default is {DEFAULT_TTS_MODEL}",
            ),
            transitional=True,
        )
    if requested == DEFAULT_TTS_MODEL:
        return ResolvedTTSModel(model=requested, source="explicit_or_env")

    return ResolvedTTSModel(
        model=requested,
        source="explicit_or_env",
        warnings=(f"unrecognized_tts_model: {requested}; verify against DashScope catalog",),
    )


def emit_tts_model_warnings(resolved: ResolvedTTSModel) -> None:
    for msg in resolved.warnings:
        if resolved.deprecated:
            logger.warning("⚠️ %s", msg)
            print(f"⚠️ {msg}")
        elif resolved.transitional:
            logger.info("ℹ️ %s", msg)
        else:
            logger.warning("⚠️ %s", msg)


def runtime_fallback_model(current: str) -> Optional[str]:
    """Runtime synthesis fallback when primary model is unavailable."""
    if current == DEFAULT_TTS_MODEL:
        return TRANSITIONAL_QWEN_TTS_FLASH_MODEL
    if current == LEGACY_QWEN_TTS_MODEL:
        return TRANSITIONAL_QWEN_TTS_FLASH_MODEL
    return None
