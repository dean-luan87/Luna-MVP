# -*- coding: utf-8 -*-
"""Provider selection v0/v1 — env + request + input_pack gates; lightweight RapidOCR path (Phase-OCR-Lightweight-Real-Provider-Adapter-001)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from capabilities.ocr_runtime.ocr_provider_adapter_contract_v0 import OCRProviderAdapterV0
from capabilities.ocr_runtime.ocr_provider_registry_v0 import OCRProviderRegistryV0
from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0


@dataclass(frozen=True)
class OCRProviderSelectionOutcomeV0:
    ok: bool
    error_code: str
    adapter: Optional[OCRProviderAdapterV0]
    selected_registry_key: Optional[str]
    selection_report: Dict[str, Any]


def _env_flags(
    *,
    env_enable_stub: bool,
    env_enable_real: bool,
    env_paddle_runtime: bool,
    env_rapid_runtime: bool,
) -> Dict[str, bool]:
    return {
        "env_enable_stub": env_enable_stub,
        "env_enable_real": env_enable_real,
        "env_paddle_runtime": env_paddle_runtime,
        "env_rapid_runtime": env_rapid_runtime,
    }


def _finalize_stub_selection(
    *,
    stub_entry: Any,
    base_report: Dict[str, Any],
    reason_codes: List[str],
) -> OCRProviderSelectionOutcomeV0:
    base_report["selected_provider"] = stub_entry.adapter.provider_name
    base_report["selected_provider_level"] = stub_entry.adapter.provider_level
    base_report["provider_selection_reason_codes"] = list(reason_codes)
    base_report["fallback_to_stub"] = bool(base_report.get("fallback_to_stub"))
    base_report["real_provider_invoked"] = False
    return OCRProviderSelectionOutcomeV0(True, "", stub_entry.adapter, "ocr_stub", base_report)


def select_ocr_provider_v0(
    *,
    request: OCRRequestV0,
    registry: OCRProviderRegistryV0,
    input_pack: Optional[Dict[str, Any]] = None,
    env_enable_stub: bool,
    env_enable_real: bool,
    env_paddle_runtime: bool,
    env_rapid_runtime: bool,
) -> OCRProviderSelectionOutcomeV0:
    """Choose provider adapter. Misconfig paddle-without-real is fatal; lightweight Rapid path requires flags + eligible pack + health."""
    reason_codes: List[str] = []
    snap_map = registry.snapshot_map()
    base_report: Dict[str, Any] = {
        "schema_version": "ocr_provider_selection_report_v0",
        "phase": "Phase-OCR-Lightweight-Real-Provider-Adapter-001",
        "selected_provider": None,
        "selected_provider_level": None,
        "provider_selection_reason_codes": reason_codes,
        "real_provider_requested": bool(env_enable_real or request.allow_heavy_ocr),
        "real_provider_allowed": bool(env_enable_real),
        "real_provider_invoked": False,
        "paddleocr_runtime_provider_enabled": bool(env_paddle_runtime),
        "rapidocr_runtime_provider_enabled": bool(env_rapid_runtime),
        "fallback_to_stub": False,
        "provider_registry_snapshot": snap_map,
        "env_flags": _env_flags(
            env_enable_stub=env_enable_stub,
            env_enable_real=env_enable_real,
            env_paddle_runtime=env_paddle_runtime,
            env_rapid_runtime=env_rapid_runtime,
        ),
    }

    if env_paddle_runtime and not env_enable_real:
        reason_codes.append("misconfiguration_paddle_runtime_without_real_provider")
        base_report["provider_selection_reason_codes"] = list(reason_codes)
        return OCRProviderSelectionOutcomeV0(
            False,
            "misconfiguration_paddle_runtime_without_real_provider",
            None,
            None,
            base_report,
        )

    if not env_enable_stub:
        reason_codes.append("stub_disabled:LUNA_ENABLE_OCR_STUB_PROVIDER_V0")
        base_report["provider_selection_reason_codes"] = list(reason_codes)
        return OCRProviderSelectionOutcomeV0(False, "stub_disabled", None, None, base_report)

    stub_entry = registry.get("ocr_stub")
    if stub_entry is None or not stub_entry.enabled:
        reason_codes.append("registry_missing_or_disabled:ocr_stub")
        base_report["provider_selection_reason_codes"] = list(reason_codes)
        return OCRProviderSelectionOutcomeV0(False, "stub_registry_unavailable", None, None, base_report)

    if not request.allow_heavy_ocr and env_paddle_runtime:
        reason_codes.append("paddleocr_selection_blocked_allow_heavy_ocr_false")

    if request.allow_heavy_ocr and not env_enable_real:
        base_report["fallback_to_stub"] = True
        reason_codes.append("heavy_ocr_signal_but_real_provider_disabled_fallback_stub")

    if env_enable_real and not env_rapid_runtime:
        reason_codes.append("real_provider_enabled_without_rapid_lightweight_flag_stub_only")

    rapid_entry = registry.get("rapidocr_candidate")
    if (
        env_enable_real
        and env_rapid_runtime
        and rapid_entry
        and rapid_entry.enabled
        and not env_paddle_runtime
    ):
        ok_pack, prc = rapid_entry.adapter.provider_input_pack_eligible(input_pack)
        if not ok_pack:
            base_report["fallback_to_stub"] = True
            reason_codes.extend(prc)
            reason_codes.append("lightweight_input_pack_rejected_fallback_stub")
            reason_codes.append("selected_stub_after_lightweight_reject")
            return _finalize_stub_selection(stub_entry=stub_entry, base_report=base_report, reason_codes=reason_codes)
        hc = rapid_entry.adapter.health_check()
        if hc.get("availability") != "available":
            base_report["fallback_to_stub"] = True
            base_report["provider_unavailable_reason"] = str(hc.get("reason") or "runtime_unavailable")
            reason_codes.append("provider_runtime_unavailable_fallback_stub")
            reason_codes.append("selected_stub_after_unavailable")
            return _finalize_stub_selection(stub_entry=stub_entry, base_report=base_report, reason_codes=reason_codes)
        reason_codes.append("selected_rapidocr_candidate_lightweight_path")
        base_report["selected_provider"] = rapid_entry.adapter.provider_name
        base_report["selected_provider_level"] = rapid_entry.adapter.provider_level
        base_report["provider_selection_reason_codes"] = list(reason_codes)
        base_report["fallback_to_stub"] = bool(base_report.get("fallback_to_stub"))
        base_report["real_provider_invoked"] = False
        return OCRProviderSelectionOutcomeV0(True, "", rapid_entry.adapter, "rapidocr_candidate", base_report)

    if env_enable_real and env_rapid_runtime and rapid_entry and not rapid_entry.enabled:
        reason_codes.append("rapidocr_registry_disabled_stub_fallback")

    if env_enable_real and env_rapid_runtime and env_paddle_runtime:
        reason_codes.append("paddle_runtime_flag_prevents_lightweight_rapid_selection")

    reason_codes.append("selected_stub_default_policy")
    return _finalize_stub_selection(stub_entry=stub_entry, base_report=base_report, reason_codes=reason_codes)


def merge_audit_provider_selection_v0(audit: Dict[str, Any], selection_report: Dict[str, Any]) -> None:
    """Copy selection fields into the flat OCR runtime audit dict (observability)."""
    audit["selected_provider"] = selection_report.get("selected_provider")
    audit["selected_provider_level"] = selection_report.get("selected_provider_level")
    audit["provider_selection_reason_codes"] = list(selection_report.get("provider_selection_reason_codes") or [])
    audit["real_provider_requested"] = bool(selection_report.get("real_provider_requested"))
    audit["real_provider_allowed"] = bool(selection_report.get("real_provider_allowed"))
    audit["real_provider_invoked"] = bool(selection_report.get("real_provider_invoked"))
    audit["paddleocr_runtime_provider_enabled"] = bool(selection_report.get("paddleocr_runtime_provider_enabled"))
    audit["rapidocr_runtime_provider_enabled"] = bool(selection_report.get("rapidocr_runtime_provider_enabled"))
    audit["fallback_to_stub"] = bool(selection_report.get("fallback_to_stub"))
    audit["provider_registry_snapshot"] = selection_report.get("provider_registry_snapshot") or {}
    if selection_report.get("provider_unavailable_reason"):
        audit["provider_unavailable_reason"] = selection_report.get("provider_unavailable_reason")
    else:
        audit.pop("provider_unavailable_reason", None)
