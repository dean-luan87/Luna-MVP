#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-010 — Verify OCR Stage-2 provider approval gate artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".webp"}


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
    ap.add_argument("--static-config-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    for label, pth in (("--static-config-root", args.static_config_root), ("--output-root", args.output_root)):
        if not Path(pth).expanduser().is_absolute():
            raise SystemExit(f"ERROR: {label} must be an absolute path")

    scr = Path(args.static_config_root).expanduser().resolve()
    out_root = Path(args.output_root).expanduser().resolve()

    required = [
        "ocr_stage2_provider_approval_summary.json",
        "ocr_stage2_provider_dependency_snapshot.json",
        "ocr_stage2_provider_credentials_snapshot.json",
        "ocr_stage2_input_sample_snapshot.json",
        "ocr_stage2_fallback_snapshot.json",
        "ocr_stage2_controlled_provider_runbook_snapshot.json",
        "ocr_stage2_provider_approval_gate_report.json",
        "ocr_stage2_provider_approval_trace.jsonl",
        "ocr_stage2_provider_approval_replay.jsonl",
        "ocr_stage2_provider_approval_whitebox.jsonl",
        "approval_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    results.append(_case("A_output_root_exists", out_root.is_dir(), {"output_root": str(out_root)}))
    results.append(_case("B_static_config_root_readable", scr.is_dir(), {"static_config_root": str(scr)}))

    for fn in required:
        p = out_root / fn
        ok = p.is_file()
        d: Dict[str, Any] = {"path": str(p)}
        if fn.endswith((".jsonl", ".md")):
            d["non_empty"] = _nonempty(p)
            ok = ok and d["non_empty"]
        results.append(_case(f"files_exist_{fn}", ok, d))

    rep = _read_json(out_root / "ocr_stage2_provider_approval_gate_report.json")
    inp = _read_json(out_root / "ocr_stage2_input_sample_snapshot.json")
    cred = _read_json(out_root / "ocr_stage2_provider_credentials_snapshot.json")
    rb_snap = _read_json(out_root / "ocr_stage2_controlled_provider_runbook_snapshot.json")
    ha = rep.get("hard_audit") or {}

    results.append(_case("C_provider_dependency_snapshot_in_report", "provider_dependencies" in rep, {"has": "provider_dependencies" in rep}))
    results.append(_case("D_credentials_in_report", "credentials" in rep, {"has": "credentials" in rep}))
    results.append(_case("E_input_sample_in_report", "input_sample" in rep, {"has": "input_sample" in rep}))
    results.append(_case("F_fallback_in_report", "fallback" in rep, {"has": "fallback" in rep}))
    results.append(_case("G_runbook_snapshot_found", rb_snap.get("found") is True, {"runbook_path": rb_snap.get("runbook_path")}))
    results.append(_case("H_approval_gate_report_valid", rep.get("approval_gate_result") in {"GO", "CONDITIONAL_GO", "NO_GO"}, {"result": rep.get("approval_gate_result")}))

    ext = Path(str(inp.get("path") or "")).suffix.lower()
    results.append(_case("I_input_extension_allowed", ext in ALLOWED_EXT, {"extension": ext}))
    results.append(_case("J_input_is_file", inp.get("is_file") is True, {"is_file": inp.get("is_file")}))
    results.append(_case("input_sha256_present", bool(inp.get("sha256")), {"present": bool(inp.get("sha256"))}))

    checks = {
        "K_ocr_provider_invoked": rep.get("ocr_provider_invoked") is False and ha.get("ocr_provider_invoked") is False,
        "L_ocr_model_invoked": rep.get("ocr_model_invoked") is False and ha.get("ocr_model_invoked") is False,
        "M_network_request": ha.get("network_request_invoked") is False,
        "N_semantic": ha.get("semantic_interpretation_enabled") is False,
        "O_midplatform": ha.get("midplatform_invoked") is False,
        "P_scene_delta": ha.get("scene_delta_invoked") is False,
        "Q_world_context": ha.get("world_context_invoked") is False,
        "R_qwen": ha.get("qwen_invoked") is False,
        "S_real_tts": ha.get("real_tts_invoked") is False,
        "T_playback": ha.get("playback_invoked") is False,
        "U_downstream": ha.get("downstream_invocation_count") == 0,
        "V_navigation": ha.get("navigation_action") in (None, "null"),
        "W_world_write": ha.get("world_write_invoked") is False,
        "X_hive": ha.get("hive_upload_invoked") is False,
    }
    for k, ok in checks.items():
        results.append(_case(k, ok, {"hard_audit": ha}))

    results.append(_case("Z_secret_values_not_logged", cred.get("secret_values_logged") is False, {"secret_values_logged": cred.get("secret_values_logged")}))

    all_ok = all(r["ok"] for r in results)
    verdict = "GO" if all_ok and rep.get("approval_gate_result") in {"GO", "CONDITIONAL_GO"} else "NO_GO"
    print(
        json.dumps(
            {
                "verifier": "verify_ocr_stage2_provider_approval_gate_v0",
                "verdict": verdict,
                "approval_gate_result": rep.get("approval_gate_result"),
                "hard_blockers": [r["case"] for r in results if not r["ok"]],
                "static_config_root": str(scr),
                "output_root": str(out_root),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
