#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge - 嵌入式硬件驱动层
"""

from .hardware_embedded import (
    EmbeddedHAL, EmbeddedCamera, EmbeddedMicrophone, EmbeddedSpeaker, 
    EmbeddedNetwork, EmbeddedYOLO, EmbeddedWhisper, EmbeddedTTS
)

__all__ = [
    'EmbeddedHAL',
    'EmbeddedCamera',
    'EmbeddedMicrophone', 
    'EmbeddedSpeaker',
    'EmbeddedNetwork',
    'EmbeddedYOLO',
    'EmbeddedWhisper',
    'EmbeddedTTS'
]
