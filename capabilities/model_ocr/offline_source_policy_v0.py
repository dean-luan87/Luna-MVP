# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-009 — OCR default offline raw text source policy (selector only).

Implements docs/architecture/LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md
Does not set runtime product defaults.
"""

from __future__ import annotations

import platform
from typing import Any, Dict, List, Optional

SOURCE_POLICY_ID_OCR_V0 = "ocr_default_offline_raw_text_source_policy_v0"

# Policy chain order (Tesseract / EasyOCR / Paddle / complex branch never appear here).
DEFAULT_OFFLINE_OCR_CHAIN: List[str] = [
    "rapidocr_ppocrv4_mobile_onnx",
    "rapidocr_current",
    "macos_vision_ocr_system_v0",
    "not_available",
]

FORBIDDEN_DEFAULT_CHAIN_PROVIDERS = frozenset(
    {
        "easyocr",
        "paddleocr_current",
        "rapidocr_ppocrv5_mobile_onnx",
        "tesseract",
    }
)


def _risk_str(val: Any) -> str:
    if val is True:
        return "reproducibility_risk_noted"
    if val is False:
        return "low"
    if isinstance(val, str):
        return val
    return str(val)


def probe_ocr_offline_provider_registry_v0(repo_root: str) -> Dict[str, Any]:
    """
    Build provider_status_registry for select_ocr_offline_source_v0 by probing local adapters.
    """
    repo_root = repo_root.rstrip("/")
    reg: Dict[str, Any] = {}

    # rapidocr_ppocrv4_mobile_onnx
    try:
        from capabilities.model_ocr.rapidocr_variant_adapter_v0 import RapidOCRVariantAdapterV0

        v4 = RapidOCRVariantAdapterV0(variant="ppocrv4_mobile", repo_root=repo_root)
        ar = v4.asset_report(repo_root=repo_root)
        ok, err = v4.is_available()
        mas = str(ar.get("model_assets_status") or "missing")
        reg["rapidocr_ppocrv4_mobile_onnx"] = {
            "provider_enabled": True,
            "provider_available": bool(ok),
            "dependency_ready": bool(ar.get("dependency_ready")),
            "model_assets_status": mas,
            "raw_text_schema_valid": True,
            "governance_boundary_valid": True,
            "avg_latency_profile_acceptable": True,
            "asset_report_present": True,
            "reproducibility_risk": _risk_str(ar.get("reproducibility_risk")),
            "model_config_id": ar.get("model_config_id"),
            "provider_id": ar.get("provider_id"),
            "provider_kind": ar.get("provider_kind"),
            "runtime_network_required": bool(ar.get("requires_network_at_runtime")),
            "probe_error": err,
        }
    except Exception as e:
        reg["rapidocr_ppocrv4_mobile_onnx"] = {
            "provider_enabled": True,
            "provider_available": False,
            "dependency_ready": False,
            "model_assets_status": "missing",
            "raw_text_schema_valid": False,
            "governance_boundary_valid": True,
            "avg_latency_profile_acceptable": True,
            "asset_report_present": False,
            "reproducibility_risk": "probe_exception",
            "probe_error": repr(e),
        }

    # rapidocr_current (bundled RapidOCR default ONNX)
    try:
        from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

        rc = RapidOCRAdapterV0()
        ar = rc.asset_report(repo_root=repo_root)
        ok, err = rc.is_available()
        mas = str(ar.get("model_assets_status") or "missing")
        reg["rapidocr_current"] = {
            "provider_available": bool(ok),
            "dependency_ready": bool(ar.get("dependency_ready")),
            "model_assets_status": mas,
            "raw_text_schema_valid": True,
            "governance_boundary_valid": True,
            "asset_report_present": True,
            "reproducibility_risk": _risk_str(ar.get("reproducibility_risk")),
            "model_config_id": ar.get("model_config_id"),
            "provider_id": ar.get("provider_id"),
            "provider_kind": ar.get("provider_kind"),
            "runtime_network_required": bool(ar.get("requires_network_at_runtime")),
            "probe_error": err,
        }
    except Exception as e:
        reg["rapidocr_current"] = {
            "provider_available": False,
            "dependency_ready": False,
            "model_assets_status": "missing",
            "raw_text_schema_valid": False,
            "governance_boundary_valid": True,
            "asset_report_present": False,
            "reproducibility_risk": "probe_exception",
            "probe_error": repr(e),
        }

    # macos_vision_ocr_system_v0
    try:
        from capabilities.model_ocr.macos_vision_ocr_adapter_v0 import MacOSVisionOCRAdapterV0

        mv = MacOSVisionOCRAdapterV0()
        ok, err = mv.is_available()
        reg["macos_vision_ocr_system_v0"] = {
            "platform_ok": platform.system() == "Darwin",
            "provider_available": bool(ok),
            "system_provider_ready": bool(ok),
            "raw_text_schema_valid": True,
            "model_config_id": mv.model_config_id,
            "provider_id": mv.provider_id,
            "provider_kind": "apple_vision_framework",
            "runtime_network_required": False,
            "probe_error": err,
        }
    except Exception as e:
        reg["macos_vision_ocr_system_v0"] = {
            "platform_ok": platform.system() == "Darwin",
            "provider_available": False,
            "system_provider_ready": False,
            "raw_text_schema_valid": False,
            "probe_error": repr(e),
        }

    return reg


def _v4_eligible(st: Dict[str, Any], *, disable_v4: bool) -> bool:
    if disable_v4:
        return False
    if not st.get("dependency_ready"):
        return False
    mas = st.get("model_assets_status")
    if mas not in ("pinned_local", "cache_detected"):
        return False
    if not st.get("raw_text_schema_valid", True):
        return False
    if not st.get("governance_boundary_valid", True):
        return False
    if not st.get("avg_latency_profile_acceptable", True):
        return False
    if not st.get("provider_enabled", True):
        return False
    if not st.get("asset_report_present", True):
        return False
    return bool(st.get("provider_available"))


def _current_eligible(st: Dict[str, Any]) -> bool:
    if not st.get("provider_available"):
        return False
    if not st.get("dependency_ready"):
        return False
    if not st.get("asset_report_present"):
        return False
    if not st.get("raw_text_schema_valid", True):
        return False
    if not st.get("governance_boundary_valid", True):
        return False
    return True


def _vision_eligible(st: Dict[str, Any]) -> bool:
    if not st.get("platform_ok"):
        return False
    if not st.get("provider_available"):
        return False
    if not st.get("system_provider_ready"):
        return False
    if not st.get("raw_text_schema_valid", True):
        return False
    return True


def select_ocr_offline_source_v0(
    *,
    source_policy_id: str,
    offline_evaluation: bool,
    raw_text_only: bool,
    controlled_live_stream: bool,
    disable_ocr_policy: bool = False,
    disable_rapidocr_ppocrv4: bool = False,
    disable_rapidocr_current: bool = False,
    disable_macos_vision: bool = False,
    provider_status_registry: Dict[str, Any],
    semantic_interpretation_enabled: bool = False,
    downstream_invocation_allowed: bool = False,
    real_tts_allowed: bool = False,
) -> Dict[str, Any]:
    """
    Pure selector — returns which offline OCR provider id should run (no adapter calls).
    """
    # Phase-Mainline-RuntimeReadiness-004: guarded trial gate hook-in (default-off no-op).
    # Must not change selection behavior; evaluate and ignore result.
    try:
        from capabilities.runtime_readiness.ocr_guarded_trial_hook_v0 import (
            evaluate_ocr_guarded_trial_hook_v0,
        )

        _ = evaluate_ocr_guarded_trial_hook_v0(
            request_id=str(source_policy_id or ""),
            trw_payload={
                "request_id": str(source_policy_id or ""),
                "hard_audit": {"shadow_only": True, "real_runtime_activation": False},
                "source_run_id": "ocr_offline_source_policy_selector_v0",
                "pending_ref": True,
            },
        )
    except Exception:
        pass

    hard_blockers: List[str] = []
    soft_followups: List[str] = []

    base_audit = {
        "source_policy_id": source_policy_id,
        "offline_evaluation": offline_evaluation,
        "raw_text_only": raw_text_only,
        "semantic_interpretation_enabled": semantic_interpretation_enabled,
        "allows_execute_now": False,
        "real_tts_invoked": False,
        "downstream_invocation_count": 0,
        "forbidden_semantic_output_count": 0,
        "trace_ref": None,
        "replay_ref": None,
        "whitebox_ref": None,
    }

    if source_policy_id != SOURCE_POLICY_ID_OCR_V0:
        hard_blockers.append(f"unknown_source_policy_id:{source_policy_id}")
        return {
            "source_policy_id": source_policy_id,
            "policy_applied": False,
            "provider_attempt_order": list(DEFAULT_OFFLINE_OCR_CHAIN),
            "provider_selected": "not_available",
            "fallback_used": True,
            "fallback_reason": "unknown_policy",
            "selection_audit": {**base_audit, "provider_status": "blocked"},
            "hard_blockers": hard_blockers,
            "soft_followups": soft_followups,
        }

    if disable_ocr_policy:
        return {
            "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
            "policy_applied": False,
            "provider_attempt_order": [],
            "provider_selected": "not_available",
            "fallback_used": False,
            "fallback_reason": "disable_ocr_policy",
            "selection_audit": {**base_audit, "provider_status": "policy_disabled"},
            "hard_blockers": [],
            "soft_followups": ["explicit_bypass_disable_ocr_policy"],
        }

    if not offline_evaluation or not raw_text_only:
        hard_blockers.append("scope_violation_offline_raw_text_only")
    if controlled_live_stream:
        hard_blockers.append("controlled_live_stream_forbidden_under_policy")
    if semantic_interpretation_enabled:
        hard_blockers.append("semantic_interpretation_forbidden")
    if downstream_invocation_allowed:
        hard_blockers.append("downstream_invocation_forbidden")
    if real_tts_allowed:
        hard_blockers.append("real_tts_forbidden")

    if hard_blockers:
        return {
            "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
            "policy_applied": False,
            "provider_attempt_order": list(DEFAULT_OFFLINE_OCR_CHAIN),
            "provider_selected": "not_available",
            "fallback_used": True,
            "fallback_reason": "precondition_failed",
            "selection_audit": {**base_audit, "provider_status": "blocked", "hard_blockers": hard_blockers},
            "hard_blockers": hard_blockers,
            "soft_followups": soft_followups,
        }

    reg = provider_status_registry
    st_v4 = reg.get("rapidocr_ppocrv4_mobile_onnx") or {}
    st_cur = reg.get("rapidocr_current") or {}
    st_vis = reg.get("macos_vision_ocr_system_v0") or {}

    full_order = [
        "rapidocr_ppocrv4_mobile_onnx",
        "rapidocr_current",
        "macos_vision_ocr_system_v0",
        "not_available",
    ]

    # 1) PP-OCRv4 mobile explicit path
    if _v4_eligible(st_v4, disable_v4=disable_rapidocr_ppocrv4):
        return {
            "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
            "policy_applied": True,
            "provider_attempt_order": full_order,
            "provider_selected": "rapidocr_ppocrv4_mobile_onnx",
            "fallback_used": False,
            "fallback_reason": None,
            "selection_audit": {
                **base_audit,
                "provider_status": "selected",
                "dependency_ready": st_v4.get("dependency_ready"),
                "model_assets_status": st_v4.get("model_assets_status"),
                "model_config_id": st_v4.get("model_config_id"),
                "provider_id": st_v4.get("provider_id"),
                "provider_kind": st_v4.get("provider_kind"),
                "reproducibility_risk": st_v4.get("reproducibility_risk"),
                "runtime_network_required": st_v4.get("runtime_network_required"),
                "raw_text_candidate_schema_valid": True,
            },
            "hard_blockers": [],
            "soft_followups": soft_followups,
        }

    fb_reason: Optional[str] = None
    if disable_rapidocr_ppocrv4:
        fb_reason = "rapidocr_ppocrv4_disabled"
    else:
        fb_reason = "rapidocr_ppocrv4_unavailable"

    # 2) rapidocr_current
    if not disable_rapidocr_current and _current_eligible(st_cur):
        return {
            "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
            "policy_applied": True,
            "provider_attempt_order": full_order,
            "provider_selected": "rapidocr_current",
            "fallback_used": True,
            "fallback_reason": fb_reason,
            "selection_audit": {
                **base_audit,
                "provider_status": "selected",
                "dependency_ready": st_cur.get("dependency_ready"),
                "model_assets_status": st_cur.get("model_assets_status"),
                "model_config_id": st_cur.get("model_config_id"),
                "provider_id": st_cur.get("provider_id"),
                "provider_kind": st_cur.get("provider_kind"),
                "reproducibility_risk": st_cur.get("reproducibility_risk"),
                "runtime_network_required": st_cur.get("runtime_network_required"),
                "raw_text_candidate_schema_valid": True,
            },
            "hard_blockers": [],
            "soft_followups": soft_followups,
        }

    fb2 = fb_reason
    if not disable_rapidocr_current:
        fb2 = "rapidocr_current_unavailable" if fb_reason is None else f"{fb_reason};rapidocr_current_unavailable"

    # 3) macOS Vision
    if not disable_macos_vision and _vision_eligible(st_vis):
        return {
            "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
            "policy_applied": True,
            "provider_attempt_order": full_order,
            "provider_selected": "macos_vision_ocr_system_v0",
            "fallback_used": True,
            "fallback_reason": fb2 or "rapid_stack_unavailable",
            "selection_audit": {
                **base_audit,
                "provider_status": "selected",
                "dependency_ready": st_vis.get("system_provider_ready"),
                "model_assets_status": "system_builtin",
                "model_config_id": st_vis.get("model_config_id"),
                "provider_id": st_vis.get("provider_id"),
                "provider_kind": st_vis.get("provider_kind"),
                "reproducibility_risk": "low",
                "runtime_network_required": False,
                "raw_text_candidate_schema_valid": True,
            },
            "hard_blockers": [],
            "soft_followups": soft_followups,
        }

    # 4) not_available
    fb3 = fb2 or "all_candidates_exhausted"
    return {
        "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
        "policy_applied": True,
        "provider_attempt_order": full_order,
        "provider_selected": "not_available",
        "fallback_used": True,
        "fallback_reason": fb3,
        "selection_audit": {
            **base_audit,
            "provider_status": "not_available",
            "dependency_ready": False,
            "model_assets_status": "n/a",
            "model_config_id": None,
            "provider_id": None,
            "provider_kind": None,
            "reproducibility_risk": "n/a",
            "runtime_network_required": False,
            "raw_text_candidate_schema_valid": False,
        },
        "hard_blockers": ["no_offline_ocr_source_available"],
        "soft_followups": soft_followups,
    }
