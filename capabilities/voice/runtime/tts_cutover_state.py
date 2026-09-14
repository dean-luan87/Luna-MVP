# -*- coding: utf-8 -*-
"""
TTS cutover runtime state (Stage-2.1 placeholder).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TTSCutoverState:
    enabled: bool = True
    mode: str = "provider_chain_first"
    legacy_fallback_enabled: bool = True

