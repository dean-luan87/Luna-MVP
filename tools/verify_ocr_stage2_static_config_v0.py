#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-009 — Verify OCR Stage-2 static config validation artifacts v0.
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
    ap.add_argument("--ocr-precheck-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    pre_root = Path(args.ocr_precheck_root).expanduser()
    out_root = Path(args.output_root).expanduser()
    if not pre_root.is_absolute() or not out_root.is_absolute():
        raise SystemExit("ERROR: --ocr-precheck-root and --output-root must be absolute paths")
    pre_root = pre_root.resolve()
    out_root = out_root.resolve()

    required_files = [
        "ocr_stage2_static_config_summary.json",
        "ocr_stage2_static_config_result.json",
        "ocr_stage2_source_policy_entrypoint_matrix.json",
        "ocr_stage2_provider_candidate_matrix.json",
        "ocr_stage2_fallback_policy_matrix.json",
        "ocr_stage2_raw_text_candidate_schema_validation.json",
        "ocr_stage2_provider_output_schema_validation.json",
        "ocr_stage2_trw_output_contract_validation.json",
        "ocr_stage2_controlled_provider_runbook.json",
        "ocr_stage2_static_config_trace.jsonl",
        "ocr_stage2_static_config_replay.jsonl",
        "ocr_stage2_static_config_whitebox.jsonl",
        "validation_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    results.append(_case("A_output_root_exists", out_root.is_dir(), {"output_root": str(out_root)}))
    results.append(_case("B_ocr_precheck_root_readable", pre_root.is_dir(), {"ocr_precheck_root": str(pre_root)}))

    for fn in required_files:
        p = out_root / fn
        ok = p.is_file()
        details: Dict[str, Any] = {"path": str(p)}
        if fn.endswith(".jsonl") or fn.endswith(".md"):
            details["non_empty"] = _nonempty(p)
            ok = ok and details["non_empty"]
        results.append(_case(f"files_exist_{fn}", ok, details))

    res = _read_json(out_root / "ocr_stage2_static_config_result.json")
    runbook = _read_json(out_root / "ocr_stage2_controlled_provider_runbook.json")

    # readiness flags
    checks = {
        "J_source_policy_entrypoint_found": res.get("source_policy_entrypoint_found") is True,
        "K_provider_candidate_found": res.get("provider_candidate_found") is True,
        "L_fallback_policy_found": res.get("fallback_policy_found") is True,
        "M_raw_text_candidate_schema_found": res.get("raw_text_candidate_schema_found") is True,
        "N_trw_output_contract_ready": res.get("trw_output_contract_ready") is True,
        "I_controlled_provider_runbook_ready": res.get("controlled_provider_runbook_ready") is True,
    }
    for k, ok in checks.items():
        results.append(_case(k, ok, {"value": res.get(k.split("_", 1)[1])}))

    # hard boundary
    ha = res.get("hard_audit") or {}
    boundary = {
        "O_provider_invoked_false": res.get("provider_invoked") is False,
        "P_ocr_model_invoked_false": res.get("ocr_model_invoked") is False,
        "Q_semantic_false": ha.get("semantic_interpretation_enabled") is False,
        "R_midplatform_false": ha.get("midplatform_invoked") is False,
        "S_scene_delta_false": ha.get("scene_delta_invoked") is False,
        "T_world_context_false": ha.get("world_context_invoked") is False,
        "U_qwen_false": ha.get("qwen_invoked") is False,
        "V_real_tts_false": ha.get("real_tts_invoked") is False,
        "W_navigation_null": ha.get("navigation_action") in (None, "null"),
        "X_world_write_false": ha.get("world_write_invoked") is False,
        "Y_hive_upload_false": ha.get("hive_upload_invoked") is False,
    }
    for k, ok in boundary.items():
        results.append(_case(k, ok, {"value": ha}))

    # runbook must be non-executable in this phase
    results.append(
        _case(
            "runbook_execution_disallowed",
            runbook.get("execution_allowed_by_this_phase") is False
            and runbook.get("provider_invocation_allowed_by_this_phase") is False
            and runbook.get("semantic_interpretation_allowed_by_this_phase") is False
            and runbook.get("midplatform_forward_allowed_by_this_phase") is False,
            {"execution_allowed_by_this_phase": runbook.get("execution_allowed_by_this_phase")},
        )
    )

    all_ok = all(r["ok"] for r in results)
    report = {
        "verifier": "verify_ocr_stage2_static_config_v0",
        "verdict": "GO" if all_ok and res.get("static_validation_result") in {"GO", "CONDITIONAL_GO"} else "NO_GO",
        "static_validation_result": res.get("static_validation_result"),
        "hard_blockers": [r["case"] for r in results if not r["ok"]],
        "output_root": str(out_root),
        "ocr_precheck_root": str(pre_root),
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["verdict"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

