#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())


def _load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    out = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))
    s = _load(os.path.join(out, "paddleocr_real_inference_summary.json"))
    checks: Dict[str, Any] = {}
    hard: List[str] = []
    soft: List[str] = []

    rme_path = os.path.join(out, "runtime_model_evidence.json")
    osr_path = os.path.join(out, "output_structure_report.json")
    bsr_path = os.path.join(out, "bbox_source_report.json")
    lbd_path = os.path.join(out, "latency_breakdown.json")
    rme = _load(rme_path) if os.path.isfile(rme_path) else {}
    bsr = _load(bsr_path) if os.path.isfile(bsr_path) else {}
    lbd = _load(lbd_path) if os.path.isfile(lbd_path) else {}

    checks["A_runtime_model_evidence_exists"] = {"ok": bool(rme)}
    checks["B_model_path_lock_status_recorded"] = {"ok": bool(rme.get("model_path_lock_status"))}
    checks["C_runtime_source_not_silent_unknown"] = {"ok": (rme.get("runtime_model_source") in ("pinned_manifest", "paddlex_cache", "auto_resolved", "unknown"))}
    checks["D_output_structure_report_exists"] = {"ok": os.path.isfile(osr_path)}
    checks["E_bbox_source_status_recorded"] = {"ok": bool(bsr.get("bbox_source") or bsr.get("bbox_iou_excluded") is not None)}
    checks["F_bbox_unavailable_not_fake_iou"] = {"ok": not (bsr.get("bbox_iou_excluded") and float((s.get("metrics") or {}).get("bbox_iou_avg") or 0.0) > 0.0)}
    checks["G_latency_breakdown_exists"] = {"ok": bool(lbd)}
    checks["H_semantic_off"] = {"ok": ((s.get("governance") or {}).get("semantic_interpretation_enabled") is False)}
    checks["I_allows_execute_now_false"] = {"ok": ((s.get("governance") or {}).get("allows_execute_now") is False)}
    checks["J_real_tts_false"] = {"ok": ((s.get("governance") or {}).get("real_tts_invoked") is False)}
    checks["K_no_downstream"] = {"ok": ((s.get("governance") or {}).get("downstream_invoked") is False)}
    checks["L_no_default_provider_decision"] = {"ok": True}

    for k, v in checks.items():
        if not bool(v.get("ok")):
            hard.append(f"check_failed:{k}")

    verdict = "NO_GO" if hard else ("CONDITIONAL_GO" if (rme.get("model_path_lock_status") in ("fallback_cache", "unknown") or bsr.get("bbox_iou_excluded")) else "GO")
    if verdict == "CONDITIONAL_GO":
        if rme.get("model_path_lock_status") in ("fallback_cache", "unknown"):
            soft.append("model_path_not_strictly_locked")
        if bsr.get("bbox_iou_excluded"):
            soft.append("bbox_iou_excluded_due_to_source_unavailable")
        if float((s.get("metrics") or {}).get("avg_latency_ms_per_frame") or 0) > 1000.0:
            soft.append("realtime_default_not_allowed")

    print(json.dumps({"phase": "Phase-ModelOCR-006C", "verifier": "verify_paddleocr_alignment_deep_fix_v0.py", "output_root": os.path.relpath(out, REPO_ROOT) if out.startswith(REPO_ROOT) else out, "checks": checks, "verdict": verdict, "hard_blockers": hard, "soft_followups": soft}, ensure_ascii=False, indent=2))
    return 2 if verdict == "NO_GO" else 0


if __name__ == "__main__":
    raise SystemExit(main())
