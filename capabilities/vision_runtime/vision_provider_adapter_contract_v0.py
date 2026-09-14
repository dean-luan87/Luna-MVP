# -*- coding: utf-8 -*-
"""Vision recognition provider adapter contract v0 (evaluation skeleton)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Literal, Optional

ProviderLevelV0 = Literal["stub", "lightweight", "heavy", "vlm"]


class VisionProviderAdapterV0(ABC):
    """Vision recognition providers consume only ``vision_provider_input_pack_v0`` units."""

    provider_name: str
    provider_level: ProviderLevelV0

    @abstractmethod
    def supports_input_pack(self, input_pack: Dict[str, Any]) -> bool:
        """Return True if this adapter can run on the given single-frame pack dict."""

    @abstractmethod
    def run(
        self,
        input_pack: Dict[str, Any],
        request: Dict[str, Any],
        deadline: Optional[float],
    ) -> Dict[str, Any]:
        """Execute recognition; must not write MidPlatform / Scene Delta / WorldModel."""

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Lightweight self-check (no heavy model load in stub)."""

    @abstractmethod
    def estimate_cost(self, input_pack: Dict[str, Any]) -> Dict[str, Any]:
        """Opaque cost hint (units, ms estimate, etc.)."""
