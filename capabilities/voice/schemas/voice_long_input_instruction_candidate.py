# -*- coding: utf-8 -*-
"""长输入拆解：单条系统指令候选（白名单映射产物）。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class VoiceLongInputInstructionCandidate:
    system_mapping_candidate: str
    param_candidates: Dict[str, Any] = field(default_factory=dict)
    requires_confirmation_candidate: bool = False
    confidence: float = 0.85
    segment_text: str = ""
    ordering_index: int = 0
    relation_hint: str = ""  # sequential | conditional | accompanying | ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "system_mapping_candidate": self.system_mapping_candidate,
            "param_candidates": dict(self.param_candidates),
            "requires_confirmation_candidate": self.requires_confirmation_candidate,
            "confidence": self.confidence,
            "segment_text": self.segment_text,
            "ordering_index": self.ordering_index,
            "relation_hint": self.relation_hint,
        }
