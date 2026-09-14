# -*- coding: utf-8 -*-
"""OCR provider adapter contract v0 — Phase-OCR-Real-Provider-Adapter-Selection-001 (interface only; no real OCR)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0


class OCRProviderAdapterV0(ABC):
    """Unified adapter surface for OCR runtime providers (stub or future real engines)."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Stable registry key / trace name (e.g. ocr_stub, paddleocr_candidate)."""

    @property
    @abstractmethod
    def provider_level(self) -> str:
        """Coarse cost / capability class: stub | lightweight | heavy."""

    def supports_input_pack(self) -> bool:
        return True

    def provider_input_pack_eligible(self, input_pack: Optional[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """Whether this adapter may consume the given pack (single-unit lightweight rules live in subclasses)."""
        if not self.supports_input_pack():
            return False, ["supports_input_pack_false"]
        return True, []

    @abstractmethod
    def run(
        self,
        input_pack: Optional[Dict[str, Any]],
        request: OCRRequestV0,
        deadline: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute OCR for this provider; must not side-effect MidPlatform / WorldModel."""

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Lightweight liveness / config sanity for observability."""

    @abstractmethod
    def estimate_cost(self, input_pack: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Opaque cost hint (latency / CPU / memory class); stub may return minimal structure."""
