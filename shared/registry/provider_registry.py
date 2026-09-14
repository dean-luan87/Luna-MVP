# -*- coding: utf-8 -*-
"""
Provider registry (Stage-0 placeholder).

原则：
- Core 不直接绑定单一 provider
- capability 层通过 registry 管理 provider 实例/配置
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass
class ProviderRecord(Generic[T]):
    name: str
    provider: T
    model_name: str = ""


class ProviderRegistry(Generic[T]):
    def __init__(self) -> None:
        self._providers: Dict[str, ProviderRecord[T]] = {}

    def register(self, name: str, provider: T, model_name: str = "") -> None:
        self._providers[name] = ProviderRecord(name=name, provider=provider, model_name=model_name)

    def get(self, name: str) -> Optional[ProviderRecord[T]]:
        return self._providers.get(name)

    def list_names(self) -> list[str]:
        return list(self._providers.keys())

