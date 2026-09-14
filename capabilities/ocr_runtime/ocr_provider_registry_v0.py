# -*- coding: utf-8 -*-
"""OCR provider registry v0 — stub enabled; real-engine candidates registered but disabled by default."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional

from capabilities.ocr_runtime.ocr_provider_adapter_contract_v0 import OCRProviderAdapterV0
from capabilities.ocr_runtime.ocr_rapidocr_provider_adapter_v0 import RapidOCRProviderAdapterV0
from capabilities.ocr_runtime.ocr_stub_provider_adapter_v0 import DisabledCandidateAdapter, StubProviderAdapter


def _env_true(name: str, default: str = "false") -> bool:
    import os

    return os.environ.get(name, default).strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class OCRProviderRegistryEntryV0:
    """Single registry row: adapter instance plus enablement (selection may still ignore disabled rows)."""

    key: str
    adapter: OCRProviderAdapterV0
    enabled: bool
    disabled_reason: str = ""


class OCRProviderRegistryV0:
    """In-memory provider registry; default construction matches skeleton governance."""

    def __init__(self) -> None:
        self._entries: Dict[str, OCRProviderRegistryEntryV0] = {}

    def register(
        self,
        key: str,
        adapter: OCRProviderAdapterV0,
        *,
        enabled: bool,
        disabled_reason: str = "",
    ) -> None:
        self._entries[key] = OCRProviderRegistryEntryV0(
            key=key,
            adapter=adapter,
            enabled=enabled,
            disabled_reason=disabled_reason or ("" if enabled else "default_disabled_skeleton_phase"),
        )

    def get(self, key: str) -> Optional[OCRProviderRegistryEntryV0]:
        return self._entries.get(key)

    def iter_entries(self) -> Iterator[OCRProviderRegistryEntryV0]:
        return iter(self._entries.values())

    def snapshot(self) -> Dict[str, Any]:
        rows: List[Dict[str, Any]] = []
        for e in sorted(self._entries.values(), key=lambda x: x.key):
            rows.append(
                {
                    "registry_key": e.key,
                    "provider_name": e.adapter.provider_name,
                    "provider_level": e.adapter.provider_level,
                    "supports_input_pack": e.adapter.supports_input_pack(),
                    "enabled": e.enabled,
                    "disabled_reason": e.disabled_reason,
                }
            )
        return {"schema_version": "ocr_provider_registry_snapshot_v0", "providers": rows}

    def snapshot_map(self) -> Dict[str, Any]:
        """Flattened map for audit embedding (sorted keys)."""
        snap = self.snapshot()
        m: Dict[str, Any] = {}
        for row in snap.get("providers") or []:
            if isinstance(row, dict) and row.get("registry_key"):
                m[str(row["registry_key"])] = row
        return m


def build_default_ocr_provider_registry_v0() -> OCRProviderRegistryV0:
    """Default registry: stub on; RapidOCR lightweight candidate enabled only via explicit env flags; Paddle disabled."""
    reg = OCRProviderRegistryV0()
    reg.register("ocr_stub", StubProviderAdapter(), enabled=True)

    rapid_enabled = _env_true("LUNA_ENABLE_OCR_REAL_PROVIDER_V0", "false") and _env_true("LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0", "false")
    reg.register(
        "rapidocr_candidate",
        RapidOCRProviderAdapterV0(),
        enabled=rapid_enabled,
        disabled_reason="" if rapid_enabled else "lightweight_real_provider_flags_off",
    )
    reg.register(
        "paddleocr_candidate",
        DisabledCandidateAdapter(provider_name="paddleocr_candidate", provider_level="heavy"),
        enabled=False,
        disabled_reason="skeleton_phase_paddle_runtime_forbidden_by_default",
    )
    return reg
