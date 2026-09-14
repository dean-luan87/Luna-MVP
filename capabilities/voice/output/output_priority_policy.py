# -*- coding: utf-8 -*-
"""
Output priority policy (Stage-1 placeholder).

只固化原则，不实现裁决逻辑。
"""

from __future__ import annotations

from dataclasses import dataclass

from capabilities.voice.output.output_categories import OutputCategory


@dataclass(frozen=True)
class OutputPriorityPolicy:
    category: OutputCategory
    priority: int

