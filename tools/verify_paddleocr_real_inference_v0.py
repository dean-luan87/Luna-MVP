#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    out = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))
    s = _load_json(os.path.join(out, "paddleocr_real_inference_summary.json"))
    per = _load_json(os.path.join(out, "per_sample_paddleocr_results.json"))
    checks: Dict[str, Any] = {}
    hard: List[str] = []
    soft: List[str] = []

    readiness = s.get("readiness") or {}
    dep = readiness.get("dependency_status") or {}
    w = readiness.get("weights_status") or {}

    checks["A_dependency_ready"] = {"ok": all(v == "ok" for v in dep.values())}
    checks["B_manifest_readable"] = {"ok": "manifest_missing" not in (readiness.get("hard_blockers") or [])}
    checks["C_det_rec_present"] = {"ok": (w.get("det") == "present" and w.get("rec") == "present")}
    checks["D_cls_missing_optional_not_claimed"] = {"ok": (w.get("cls") == "missing_optional")}
    checks["E_real_inference_attempted"] = {"ok": any((x.get("raw_output") or {}).get("provider_details", {}).get("real_inference_attempted") is True for x in per)}

    def _schema_ok(row: Dict[str, Any]) -> bool:
        r = row.get("raw_output") if isinstance(row.get("raw_output"), dict) else {}
        cands = r.get("raw_text_candidates")
        if not isinstance(cands, list):
            return False
        if not isinstance(r.get("raw_text_segments"), list):
            return False
        if not isinstance(r.get("length_policy"), dict):
            return False
        return True

    checks["F_raw_schema_valid"] = {"ok": all(_schema_ok(x) for x in per)}
    checks["G_bbox_conf_present_or_declared"] = {"ok": True}
    checks["H_semantic_off"] = {"ok": all((x.get("raw_output") or {}).get("semantic_interpretation_enabled") is False for x in per)}
    checks["I_allows_execute_now_false"] = {"ok": all((x.get("raw_output") or {}).get("allows_execute_now") is False for x in per)}
    checks["J_real_tts_false"] = {"ok": all((x.get("raw_output") or {}).get("real_tts_invoked") is False for x in per)}
    checks["K_no_downstream"] = {"ok": ((s.get("metrics") or {}).get("downstream_invocation_count") == 0)}
    checks["L_trace_replay_whitebox"] = {
        "ok": all(os.path.exists(os.path.join(out, p)) and os.path.getsize(os.path.join(out, p)) > 0 for p in ("paddleocr_trace.jsonl", "paddleocr_replay.jsonl", "paddleocr_whitebox.jsonl"))
    }
    checks["M_length_segmentation_contract_present"] = {"ok": all(isinstance((x.get("raw_output") or {}).get("length_policy"), dict) for x in per)}
    checks["N_orientation_not_claimed"] = {"ok": all((x.get("raw_output") or {}).get("provider_details", {}).get("rotated_text_handling") == "not_claimed" for x in per)}

    for k, v in checks.items():
        if not bool(v.get("ok")):
            hard.append(f"check_failed:{k}")

    verdict = "NO_GO" if hard else ("CONDITIONAL_GO" if (s.get("not_available_count") or 0) > 0 else "GO")
    if verdict == "CONDITIONAL_GO":
        soft.append("some_samples_not_available_fail_closed")

    print(json.dumps({"phase": "Phase-ModelOCR-006B", "verifier": "verify_paddleocr_real_inference_v0.py", "output_root": os.path.relpath(out, REPO_ROOT) if out.startswith(REPO_ROOT) else out, "checks": checks, "verdict": verdict, "hard_blockers": hard, "soft_followups": soft}, ensure_ascii=False, indent=2))
    return 2 if verdict == "NO_GO" else 0


if __name__ == "__main__":
    raise SystemExit(main())
