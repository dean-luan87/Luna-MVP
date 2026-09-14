# -*- coding: utf-8 -*-
"""Stub OCR provider adapter — wraps ocr_provider_stub_v0 (no real OCR)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.ocr_runtime.ocr_provider_adapter_contract_v0 import OCRProviderAdapterV0
from capabilities.ocr_runtime.ocr_provider_stub_v0 import run_ocr_provider_stub_v0
from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0


class StubProviderAdapter(OCRProviderAdapterV0):
    """Adapter for the existing deterministic stub provider."""

    @property
    def provider_name(self) -> str:
        return "ocr_stub"

    @property
    def provider_level(self) -> str:
        return "stub"

    def supports_input_pack(self) -> bool:
        return True

    def run(
        self,
        input_pack: Optional[Dict[str, Any]],
        request: OCRRequestV0,
        deadline: Dict[str, Any],
    ) -> Dict[str, Any]:
        _ = deadline  # reserved for future budget enforcement
        return run_ocr_provider_stub_v0(trace_id=request.trace_id, request_id=request.request_id, input_pack=input_pack)

    def health_check(self) -> Dict[str, Any]:
        return {"ok": True, "provider": self.provider_name, "level": self.provider_level}

    def estimate_cost(self, input_pack: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        units = (input_pack or {}).get("input_units") if isinstance(input_pack, dict) else None
        n = len(units) if isinstance(units, list) else 0
        return {"cost_class": "negligible_stub", "input_unit_count_hint": n}


class DisabledCandidateAdapter(OCRProviderAdapterV0):
    """Placeholder for a registry entry that must never be selected or invoked in skeleton phases."""

    def __init__(self, *, provider_name: str, provider_level: str) -> None:
        self._provider_name = provider_name
        self._provider_level = provider_level

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @property
    def provider_level(self) -> str:
        return self._provider_level

    def run(
        self,
        input_pack: Optional[Dict[str, Any]],
        request: OCRRequestV0,
        deadline: Dict[str, Any],
    ) -> Dict[str, Any]:
        raise RuntimeError("disabled_candidate_adapter_must_not_be_invoked")

    def health_check(self) -> Dict[str, Any]:
        return {"ok": False, "provider": self.provider_name, "reason": "disabled_registry_candidate"}

    def estimate_cost(self, input_pack: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        _ = input_pack
        return {"cost_class": "unavailable_disabled_candidate"}

    def provider_input_pack_eligible(self, input_pack: Optional[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        _ = input_pack
        return False, ["disabled_registry_candidate"]
