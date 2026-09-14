#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-009 — Verify OCR offline source policy selector + benchmark artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def _synthetic_registry_v4_ok() -> Dict[str, Any]:
    return {
        "rapidocr_ppocrv4_mobile_onnx": {
            "provider_enabled": True,
            "provider_available": True,
            "dependency_ready": True,
            "model_assets_status": "cache_detected",
            "raw_text_schema_valid": True,
            "governance_boundary_valid": True,
            "avg_latency_profile_acceptable": True,
            "asset_report_present": True,
            "reproducibility_risk": "noted",
        },
        "rapidocr_current": {
            "provider_available": True,
            "dependency_ready": True,
            "asset_report_present": True,
            "raw_text_schema_valid": True,
            "governance_boundary_valid": True,
        },
        "macos_vision_ocr_system_v0": {
            "platform_ok": True,
            "provider_available": True,
            "system_provider_ready": True,
            "raw_text_schema_valid": True,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--normal-root", default=None, help="Benchmark output root (policy normal run)")
    ap.add_argument("--fallback-root", default=None, help="Benchmark output root (--disable-rapidocr-ppocrv4)")
    ap.add_argument("--output-json", default=None, help="Write verifier report JSON")
    args = ap.parse_args()

    from capabilities.model_ocr.offline_source_policy_v0 import (
        FORBIDDEN_DEFAULT_CHAIN_PROVIDERS,
        SOURCE_POLICY_ID_OCR_V0,
        select_ocr_offline_source_v0,
    )

    results: List[Dict[str, Any]] = []
    PID = SOURCE_POLICY_ID_OCR_V0
    base = dict(
        source_policy_id=PID,
        offline_evaluation=True,
        raw_text_only=True,
        controlled_live_stream=False,
        semantic_interpretation_enabled=False,
        downstream_invocation_allowed=False,
        real_tts_allowed=False,
        disable_ocr_policy=False,
        disable_rapidocr_ppocrv4=False,
        disable_rapidocr_current=False,
        disable_macos_vision=False,
    )

    reg_ok = _synthetic_registry_v4_ok()
    d = select_ocr_offline_source_v0(provider_status_registry=reg_ok, **base)
    results.append(
        _case(
            "A_normal_select_ppocrv4",
            d.get("provider_selected") == "rapidocr_ppocrv4_mobile_onnx" and d.get("fallback_used") is False,
            d,
        )
    )

    d = select_ocr_offline_source_v0(
        provider_status_registry=reg_ok, **{**base, "disable_rapidocr_ppocrv4": True}
    )
    results.append(
        _case(
            "B_ppocrv4_disabled_to_current",
            d.get("provider_selected") == "rapidocr_current"
            and d.get("fallback_used") is True
            and "disabled" in str(d.get("fallback_reason") or ""),
            d,
        )
    )

    reg_v4_bad = {**reg_ok, "rapidocr_ppocrv4_mobile_onnx": {**reg_ok["rapidocr_ppocrv4_mobile_onnx"], "dependency_ready": False}}
    d = select_ocr_offline_source_v0(provider_status_registry=reg_v4_bad, **base)
    results.append(
        _case(
            "C_ppocrv4_unavailable_to_current",
            d.get("provider_selected") == "rapidocr_current" and d.get("fallback_used") is True,
            d,
        )
    )

    reg_no_rapid = {
        **reg_ok,
        "rapidocr_ppocrv4_mobile_onnx": {**reg_ok["rapidocr_ppocrv4_mobile_onnx"], "dependency_ready": False},
        "rapidocr_current": {**reg_ok["rapidocr_current"], "provider_available": False},
    }
    d = select_ocr_offline_source_v0(provider_status_registry=reg_no_rapid, **base)
    results.append(
        _case(
            "D_current_to_vision",
            d.get("provider_selected") == "macos_vision_ocr_system_v0",
            d,
        )
    )

    reg_none = {
        **reg_ok,
        "rapidocr_ppocrv4_mobile_onnx": {**reg_ok["rapidocr_ppocrv4_mobile_onnx"], "dependency_ready": False},
        "rapidocr_current": {**reg_ok["rapidocr_current"], "provider_available": False},
        "macos_vision_ocr_system_v0": {**reg_ok["macos_vision_ocr_system_v0"], "provider_available": False},
    }
    d = select_ocr_offline_source_v0(provider_status_registry=reg_none, **base)
    results.append(
        _case(
            "E_vision_unavailable_to_not_available",
            d.get("provider_selected") == "not_available",
            d,
        )
    )

    d = select_ocr_offline_source_v0(
        provider_status_registry=reg_ok,
        **{**base, "disable_ocr_policy": True},
    )
    results.append(
        _case(
            "F_disable_ocr_policy",
            d.get("provider_selected") == "not_available" and d.get("policy_applied") is False,
            d,
        )
    )

    d = select_ocr_offline_source_v0(
        provider_status_registry=reg_ok,
        **{**base, "controlled_live_stream": True},
    )
    results.append(
        _case(
            "G_controlled_live_blocks",
            d.get("policy_applied") is False and d.get("provider_selected") == "not_available",
            d,
        )
    )

    d = select_ocr_offline_source_v0(
        provider_status_registry=reg_ok,
        **{**base, "semantic_interpretation_enabled": True},
    )
    results.append(
        _case(
            "H_semantic_block",
            d.get("provider_selected") == "not_available",
            d,
        )
    )

    chain_providers = set()
    for _ in range(3):
        r = select_ocr_offline_source_v0(provider_status_registry=reg_ok, **base)
        chain_providers.add(r.get("provider_selected"))
    forbidden_hit = bool(chain_providers & FORBIDDEN_DEFAULT_CHAIN_PROVIDERS)
    results.append(_case("I_forbidden_not_in_chain", forbidden_hit is False, {"seen": list(chain_providers)}))

    d_j = select_ocr_offline_source_v0(provider_status_registry=reg_ok, **base)
    audit_keys = set((d_j.get("selection_audit") or {}).keys())
    required_subset = {
        "dependency_ready",
        "model_assets_status",
        "raw_text_candidate_schema_valid",
        "semantic_interpretation_enabled",
        "allows_execute_now",
        "real_tts_invoked",
        "downstream_invocation_count",
        "forbidden_semantic_output_count",
    }
    results.append(
        _case(
            "J_audit_fields_present",
            required_subset.issubset(audit_keys),
            {"audit_keys": sorted(audit_keys)},
        )
    )

    # Benchmark artifact checks
    if args.normal_root:
        p = os.path.join(os.path.abspath(args.normal_root), "ocr_benchmark_summary.json")
        summ = _read_json(p)
        ok_n = (
            summ.get("provider_selected") == "rapidocr_ppocrv4_mobile_onnx"
            and summ.get("fallback_used") is False
            and summ.get("source_policy_id") == PID
        )
        results.append(_case("bench_normal_summary", ok_n, {"path": p, "provider_selected": summ.get("provider_selected")}))

    if args.fallback_root:
        p = os.path.join(os.path.abspath(args.fallback_root), "ocr_benchmark_summary.json")
        summ = _read_json(p)
        ok_f = (
            summ.get("provider_selected") == "rapidocr_current"
            and summ.get("fallback_used") is True
            and "disabled" in str(summ.get("fallback_reason") or "").lower()
        )
        results.append(
            _case(
                "bench_fallback_summary",
                ok_f,
                {"path": p, "provider_selected": summ.get("provider_selected"), "fallback_reason": summ.get("fallback_reason")},
            )
        )

    all_ok = all(r["ok"] for r in results)
    report = {
        "verifier": "verify_ocr_offline_source_policy_v0",
        "verdict": "GO" if all_ok else "NO_GO",
        "governance_leakage": 0,
        "hard_blockers": [] if all_ok else [r["case"] for r in results if not r["ok"]],
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.output_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
