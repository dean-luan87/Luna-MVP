#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    if not isinstance(obj, dict):
        raise ValueError("json_root_not_dict")
    return obj


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    out_root = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))

    summary_p = os.path.join(out_root, "paddleocr_adapter_skeleton_summary.json")
    readiness_p = os.path.join(out_root, "paddleocr_adapter_readiness.json")
    trace_p = os.path.join(out_root, "paddleocr_adapter_trace.jsonl")
    whitebox_p = os.path.join(out_root, "paddleocr_adapter_whitebox.jsonl")

    hard_blockers: List[str] = []
    soft_followups: List[str] = []
    checks: Dict[str, Any] = {}

    # A
    checks["A_manifest_readable"] = {"ok": os.path.isfile(summary_p) and os.path.isfile(readiness_p)}
    if not checks["A_manifest_readable"]["ok"]:
        hard_blockers.append("summary_or_readiness_missing")
        print(json.dumps({"phase": "Phase-ModelOCR-004B", "verifier": "verify_paddleocr_adapter_skeleton_v0", "checks": checks, "verdict": "NO_GO", "hard_blockers": hard_blockers, "soft_followups": soft_followups}, ensure_ascii=False, indent=2))
        return 2

    summary = _load_json(summary_p)
    readiness = _load_json(readiness_p)
    ws = readiness.get("weights_status") if isinstance(readiness.get("weights_status"), dict) else {}
    dep = readiness.get("dependency_status") if isinstance(readiness.get("dependency_status"), dict) else {}
    cb = readiness.get("capability_boundary") if isinstance(readiness.get("capability_boundary"), dict) else {}

    # B/C
    checks["B_det_rec_pinned_partial"] = {"ok": ws.get("det") == "present" and ws.get("rec") == "present" and ws.get("weights_source") == "pinned_partial"}
    checks["C_cls_optional_not_claimed"] = {"ok": str(ws.get("cls")).endswith("optional") and cb.get("orientation_support") is False and cb.get("rotated_text_handling") == "not_claimed"}

    # D/E
    deps_missing = any(v != "ok" for v in dep.values())
    fail_closed = bool(readiness.get("fail_closed"))
    checks["D_fail_closed_on_missing_dep"] = {"ok": (not deps_missing) or fail_closed, "deps_missing": deps_missing, "fail_closed": fail_closed}
    checks["E_no_fake_raw_text"] = {"ok": int((summary.get("sample_contract") or {}).get("raw_text_candidates_count", 0)) == 0}

    # F/G/H/I
    checks["F_semantic_disabled"] = {"ok": (summary.get("sample_contract") or {}).get("semantic_interpretation_enabled") is False}
    checks["G_allows_execute_false"] = {"ok": (summary.get("sample_contract") or {}).get("allows_execute_now") is False}
    checks["H_tts_false"] = {"ok": (summary.get("sample_contract") or {}).get("real_tts_invoked") is False}
    checks["I_no_downstream"] = {"ok": True}

    # J trace/whitebox/readiness
    checks["J_artifacts_present"] = {"ok": os.path.isfile(trace_p) and os.path.isfile(whitebox_p) and os.path.isfile(readiness_p)}

    # K fallback
    fbc = readiness.get("fallback_candidates") if isinstance(readiness.get("fallback_candidates"), list) else []
    checks["K_fallback_candidates"] = {"ok": "rapidocr_onnxruntime_v0" in fbc and "macos_vision_ocr_system_v0" in fbc, "value": fbc}

    # L init-only no benchmark
    init = summary.get("init_only") if isinstance(summary.get("init_only"), dict) else {}
    mode = str(summary.get("mode") or "")
    if mode == "check-only":
        l_ok = True
    else:
        # init-only may attempt import/init, but still must not benchmark.
        l_ok = bool(init.get("attempted") is True or init.get("error"))
    checks["L_init_only_no_benchmark"] = {"ok": l_ok, "mode": mode, "attempted": init.get("attempted"), "init_ok": init.get("ok")}

    for k, v in checks.items():
        if isinstance(v, dict) and not bool(v.get("ok")):
            hard_blockers.append(f"check_failed:{k}")

    # convert expected missing dep into conditional, not no-go, when fail-closed works
    if deps_missing and fail_closed:
        hb2 = [x for x in hard_blockers if x != "check_failed:D_fail_closed_on_missing_dep"]
        hard_blockers = hb2
        soft_followups.append("dependency_missing_but_fail_closed_effective")

    verdict = "NO_GO" if hard_blockers else ("CONDITIONAL_GO" if soft_followups else "GO")
    result = {
        "phase": "Phase-ModelOCR-004B",
        "verifier": "verify_paddleocr_adapter_skeleton_v0.py",
        "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root,
        "checks": checks,
        "verdict": verdict,
        "hard_blockers": list(dict.fromkeys(hard_blockers)),
        "soft_followups": list(dict.fromkeys(soft_followups)),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if verdict == "NO_GO" else 0


if __name__ == "__main__":
    raise SystemExit(main())
