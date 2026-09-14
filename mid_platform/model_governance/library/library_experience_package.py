# -*- coding: utf-8 -*-
"""占位：图书馆经验包（无自动打包流水线）。"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class LibraryExperiencePackage:
    package_id: str
    package_type: str
    applicable_domains: List[str]
    applicable_models: List[str]
    summary: str
    key_patterns: List[str] = field(default_factory=list)
    supporting_experiences: List[str] = field(default_factory=list)
    validation_level: str = "none"
    recommended_usage: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> LibraryExperiencePackage:
        return cls(
            package_id=str(d["package_id"]),
            package_type=str(d["package_type"]),
            applicable_domains=list(d.get("applicable_domains", [])),
            applicable_models=list(d.get("applicable_models", [])),
            summary=str(d.get("summary", "")),
            key_patterns=list(d.get("key_patterns", [])),
            supporting_experiences=list(d.get("supporting_experiences", [])),
            validation_level=str(d.get("validation_level", "none")),
            recommended_usage=str(d.get("recommended_usage", "")),
        )
