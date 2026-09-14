#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-009 — Verify OCR Stage-2 static configuration validation artifacts v0.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="ABSOLUTE output directory used by run tool")
    args = ap.parse_args()

    out_root = Path(args.output_root).expanduser()
    if not out_root.is_absolute():
        raise SystemExit("ERROR: --output-root must be an absolute path")
    out_root = out_root.resolve()

    required_files = [
        "ocr_stage2_static_config_validation_summary.json",
        "ocr_stage2_static_config_validation_result.json",
        "ocr_stage2_controlled_provider_runbook_009.json",
        "ocr_stage2_source_policy_entry_009.json",
        "ocr_stage2_provider_manifest_scan_009.json",
        "ocr_stage2_raw_text_candidate_schema_contract_009.json",
        "ocr_stage2_fallback_policy_readiness_009.json",
        "ocr_stage2_request_trace_trw_contract_009.json",
        "static_validation_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    results.append(_case("A_output_root_exists", out_root.is_dir(), {"output_root": str(out_root)}))
    for fn in required_files:
        p = out_root / fn
        ok = p.is_file()
        details: Dict[str, Any] = {"path": str(p)}
        if fn.endswith(".md"):
            details["non_empty"] = _nonempty(p)
            ok = ok and details["non_empty"]
        results.append(_case(f"files_exist_{fn}", ok, details))

    res = _read_json(out_root / "ocr_stage2_static_config_validation_result.json")
    runbook = _read_json(out_root / "ocr_stage2_controlled_provider_runbook_009.json")

    results.append(
        _case(
            "B_static_validation_result_value",
            res.get("static_validation_result") in {"GO", "CONDITIONAL_GO", "NO_GO"},
            {"value": res.get("static_validation_result")},
        )
    )

    # Hard boundary must remain false
    ha = res.get("hard_audit") or {}
    boundary = {
        "provider_invoked": res.get("provider_invoked") is False,
        "ocr_provider_invoked": ha.get("ocr_provider_invoked") is False,
        "semantic_interpretation_enabled": ha.get("semantic_interpretation_enabled") is False,
        "midplatform_invoked": ha.get("midplatform_invoked") is False,
        "scene_delta_invoked": ha.get("scene_delta_invoked") is False,
        "world_context_invoked": ha.get("world_context_invoked") is False,
        "qwen_invoked": ha.get("qwen_invoked") is False,
        "real_tts_invoked": ha.get("real_tts_invoked") is False,
        "playback_invoked": ha.get("playback_invoked") is False,
        "downstream_invocation_count": ha.get("downstream_invocation_count") == 0,
        "navigation_action": ha.get("navigation_action") in (None, "null"),
        "world_write_invoked": ha.get("world_write_invoked") is False,
        "hive_upload_invoked": ha.get("hive_upload_invoked") is False,
    }
    for k, ok in boundary.items():
        results.append(_case(f"hard_boundary_{k}", ok, {"value": ha.get(k) if k in ha else res.get(k)}))

    # Materials readiness flags
    readiness = {
        "source_policy_ready": res.get("source_policy_ready") is True,
        "provider_static_config_ready": res.get("provider_static_config_ready") is True,
        "raw_text_candidate_schema_ready": res.get("raw_text_candidate_schema_ready") is True,
        "fallback_policy_ready": res.get("fallback_policy_ready") is True,
        "request_trace_trw_contract_ready": res.get("request_trace_trw_contract_ready") is True,
        "controlled_provider_runbook_ready": res.get("controlled_provider_runbook_ready") is True,
    }
    for k, ok in readiness.items():
        results.append(_case(f"readiness_{k}", ok, {"value": res.get(k)}))

    # Runbook must be non-executable in 009
    results.append(
        _case(
            "runbook_execution_disallowed",
            runbook.get("execution_allowed_by_this_phase") is False,
            {"execution_allowed_by_this_phase": runbook.get("execution_allowed_by_this_phase")},
        )
    )

    all_ok = all(r["ok"] for r in results)
    verdict = "GO" if all_ok else "NO_GO"
    report = {
        "verifier": "verify_ocr_stage2_static_config_validation_v0",
        "verdict": verdict,
        "output_root": str(out_root),
        "static_validation_result": res.get("static_validation_result"),
        "hard_blockers": [r["case"] for r in results if not r["ok"]],
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all_ok and res.get("static_validation_result") in {"GO", "CONDITIONAL_GO"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

