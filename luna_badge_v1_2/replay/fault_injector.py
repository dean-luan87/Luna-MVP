#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""P0-3 Fault injection (test-only) for deterministic replay.

约束：
- 只允许在 adapter 边界注入（Vision/Map/TTS）
- 不修改业务语义，不引入 1.5+ 行为
- 注入配置必须可文件化，且只依赖 step_index（ReplayClock 友好）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
import json


FaultType = Literal[
    "vision_no_return",
    "vision_timeout",
    "map_timeout",
    "tts_block",
    "tts_exception",
]


@dataclass(frozen=True)
class FaultSpec:
    fault_type: FaultType
    start_step: int
    end_step: int
    message: str = ""

    def active_at(self, step: int) -> bool:
        return self.start_step <= step <= self.end_step


@dataclass
class FaultConfig:
    enabled: bool = False
    specs: List[FaultSpec] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FaultConfig":
        enabled = bool(data.get("enabled", False))
        specs_raw = data.get("specs") or []
        specs: List[FaultSpec] = []
        for s in specs_raw:
            specs.append(
                FaultSpec(
                    fault_type=s["fault_type"],
                    start_step=int(s["start_step"]),
                    end_step=int(s.get("end_step", s["start_step"])),
                    message=str(s.get("message") or ""),
                )
            )
        return FaultConfig(enabled=enabled, specs=specs)

    def validate(self) -> List[str]:
        errors: List[str] = []
        for i, s in enumerate(self.specs):
            if s.start_step < 0 or s.end_step < 0:
                errors.append(f"specs[{i}]: step must be >= 0")
            if s.end_step < s.start_step:
                errors.append(f"specs[{i}]: end_step must be >= start_step")
        return errors

    def match(self, step: int, fault_type: FaultType) -> Optional[FaultSpec]:
        if not self.enabled:
            return None
        for s in self.specs:
            if s.fault_type == fault_type and s.active_at(step):
                return s
        return None


def load_fault_config(path: str) -> FaultConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cfg = FaultConfig.from_dict(data)
    errs = cfg.validate()
    if errs:
        raise ValueError("Invalid fault config: " + "; ".join(errs))
    return cfg

