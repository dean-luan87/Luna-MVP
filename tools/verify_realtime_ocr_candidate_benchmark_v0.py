#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Phase-ModelOCR-006E realtime OCR candidate benchmark outputs."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())

FORBIDDEN_IN_RUN = {"paddleocr", "macos_vision", "surya", "doctr", "paddleocr_vl", "deepseek_ocr"}


def _load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _schema_ok_sample(raw: Dict[str, Any]) -> bool:
    if raw.get("semantic_interpretation_enabled") is not False:
        return False
    if raw.get("allows_execute_now") is not False:
        return False
    if raw.get("real_tts_invoked") is not False:
        return False
    cands = raw.get("raw_text_candidates")
    if not isinstance(cands, list):
        return False
    for c in cands:
        if not isinstance(c, dict):
            return False
        for k in ("text", "normalized_text", "bbox", "line_order"):
            if k not in c:
                return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    out = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))

    hard: List[str] = []
    soft: List[str] = []
    checks: Dict[str, Any] = {}

    sum_path = os.path.join(out, "realtime_ocr_candidate_benchmark_summary.json")
    if not os.path.isfile(sum_path):
        print(json.dumps({"verdict": "NO_GO", "hard_blockers": ["missing_summary_json"]}, indent=2))
        return 2

    summary = _load(sum_path)
    providers: List[str] = list(summary.get("providers") or [])
    checks["A_dataset_manifest_readable"] = bool(summary.get("dataset_manifest"))

    fg = summary.get("forbidden_gt_field_count")
    fcount = int(fg) if fg is not None else -1
    checks["B_gt_forbidden_fields_zero"] = fcount == 0
    if fcount != 0:
        hard.append("forbidden_gt_fields_nonzero")

    run_status = summary.get("per_provider_run_status") or {}
    checks["C_provider_statuses"] = run_status
    for pk in providers:
        st = run_status.get(pk)
        if st not in ("success", "partial", "not_available", "failed"):
            hard.append(f"invalid_status:{pk}:{st}")

    psc = os.path.join(out, "per_sample_comparison.json")
    checks["D_per_sample_comparison_exists"] = os.path.isfile(psc)

    schema_ok = False
    for pk in providers:
        rd = os.path.join(out, "raw_outputs", pk)
        if not os.path.isdir(rd):
            continue
        for fn in sorted(os.listdir(rd)):
            if not fn.endswith(".json"):
                continue
            rj = _load(os.path.join(rd, fn))
            raw = rj.get("raw_output") if isinstance(rj, dict) else None
            if isinstance(raw, dict) and isinstance(raw.get("raw_text_candidates"), list):
                schema_ok = _schema_ok_sample(raw)
                if schema_ok:
                    break
        if schema_ok:
            break
    checks["E_raw_schema_sample"] = schema_ok
    if not schema_ok and providers:
        hard.append("raw_text_schema_invalid")

    lat_ok = os.path.isfile(os.path.join(out, "metric_tables/latency_metrics.json"))
    bbox_ok = os.path.isfile(os.path.join(out, "metric_tables/bbox_metrics.json"))
    gov_m_ok = os.path.isfile(os.path.join(out, "metric_tables/governance_metrics.json"))
    checks["F_latency_metrics"] = lat_ok
    checks["G_bbox_metrics"] = bbox_ok
    checks["G_governance_metrics_file"] = gov_m_ok
    if not lat_ok:
        hard.append("latency_metrics_missing")
    if not bbox_ok:
        hard.append("bbox_metrics_missing")
    if not gov_m_ok:
        hard.append("governance_metrics_file_missing")

    gov = summary.get("governance") or {}
    leak = gov.get("semantic_interpretation_enabled") is True or gov.get("downstream_invoked") is True
    checks["H_governance_leakage_zero"] = not leak
    if leak:
        hard.append("governance_leakage")

    tr_ok = all(os.path.isfile(os.path.join(out, "trace", f"{p}_trace.jsonl")) for p in providers)
    rp_ok = all(os.path.isfile(os.path.join(out, "replay", f"{p}_replay.jsonl")) for p in providers)
    wb_ok = all(os.path.isfile(os.path.join(out, "whitebox", f"{p}_whitebox.jsonl")) for p in providers)
    checks["I_trace_replay_whitebox"] = tr_ok and rp_ok and wb_ok
    if not (tr_ok and rp_ok and wb_ok):
        hard.append("observability_incomplete")

    ar_path = os.path.join(out, "provider_asset_reports", "all_providers_assets.json")
    ar_ok = os.path.isfile(ar_path)
    checks["J_asset_report"] = ar_ok
    if not ar_ok:
        hard.append("asset_report_missing")
    else:
        assets_all = _load(ar_path)
        for pk in providers:
            if run_status.get(pk) == "not_available":
                a = assets_all.get(pk) if isinstance(assets_all, dict) else {}
                if not isinstance(a, dict):
                    a = {}
                if not (a.get("error") or a.get("missing_assets") or a.get("not_available_reason")):
                    hard.append(f"not_available_missing_reason:{pk}")
        checks["M_not_available_has_reason"] = len([x for x in hard if x.startswith("not_available_missing_reason")]) == 0

    bad = [p for p in providers if p.lower() in FORBIDDEN_IN_RUN]
    checks["K_no_complex_branch_providers"] = len(bad) == 0
    if bad:
        hard.append(f"forbidden_provider:{bad}")

    checks["L_no_default_provider"] = gov.get("default_ocr_provider_set") is False
    if gov.get("default_ocr_provider_set") is True:
        hard.append("default_provider_set")

    rc = run_status.get("rapidocr_current")
    if rc in ("not_available", "failed") or rc is None:
        hard.append("rapidocr_current_not_runnable")

    others_ok = sum(
        1
        for k in ("rapidocr_ppocrv5_mobile_onnx", "rapidocr_ppocrv4_mobile_onnx", "easyocr", "tesseract")
        if run_status.get(k) in ("success", "partial")
    )

    verdict = "NO_GO"
    if hard:
        verdict = "NO_GO"
    elif rc in ("success", "partial") and others_ok >= 2:
        verdict = "GO"
    elif rc in ("success", "partial") and others_ok >= 1:
        verdict = "CONDITIONAL_GO"
        soft.append("only_one_additional_candidate_success")
    elif rc in ("success", "partial"):
        verdict = "CONDITIONAL_GO"
        soft.append("no_additional_candidate_success")
    else:
        verdict = "NO_GO"

    print(
        json.dumps(
            {
                "phase": "Phase-ModelOCR-006E",
                "verifier": "verify_realtime_ocr_candidate_benchmark_v0.py",
                "output_root": os.path.relpath(out, REPO_ROOT) if out.startswith(REPO_ROOT) else out,
                "checks": checks,
                "verdict": verdict,
                "hard_blockers": hard,
                "soft_followups": soft,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 2 if verdict == "NO_GO" else 0


if __name__ == "__main__":
    raise SystemExit(main())
