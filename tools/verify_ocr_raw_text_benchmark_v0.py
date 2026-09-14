#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
FORBIDDEN_GT_FIELDS = {"scene_type", "task_label", "navigation_action", "route_advice", "semantic_summary", "should_speak", "should_turn", "go_direction"}
FORBIDDEN_MANIFEST_FIELDS = {"scene_type", "route_advice", "task_label", "should_speak", "should_turn", "navigation_action"}
REQUIRED_STRATIFIED_FIELDS = {"difficulty_level", "visual_condition", "language_type"}


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-manifest", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    dm = args.dataset_manifest if os.path.isabs(args.dataset_manifest) else os.path.abspath(os.path.join(REPO_ROOT, args.dataset_manifest))
    out = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))

    checks: Dict[str, Any] = {}
    hard: List[str] = []
    soft: List[str] = []

    # A/B/C + stratified fields
    checks["A_dataset_manifest_readable"] = {"ok": os.path.isfile(dm)}
    if not checks["A_dataset_manifest_readable"]["ok"]:
        hard.append("dataset_manifest_missing")
        print(json.dumps({"phase": "Phase-ModelOCR-005B", "verifier": "verify_ocr_raw_text_benchmark_v0.py", "checks": checks, "verdict": "NO_GO", "hard_blockers": hard, "soft_followups": soft}, ensure_ascii=False, indent=2))
        return 2
    man = _load_json(dm)
    samples = man.get("samples") if isinstance(man, dict) else None
    if not isinstance(samples, list) or not samples:
        hard.append("dataset_samples_missing")
        checks["B_gt_readable"] = {"ok": False}
        checks["C_gt_forbidden_fields"] = {"ok": False}
    else:
        gt_ok = True
        forbid_cnt = 0
        manifest_forbidden_cnt = 0
        stratified_field_missing = 0
        for s in samples:
            manifest_forbidden_cnt += len(set(s.keys()).intersection(FORBIDDEN_MANIFEST_FIELDS))
            for rk in REQUIRED_STRATIFIED_FIELDS:
                if not s.get(rk):
                    stratified_field_missing += 1
            gp = str(s.get("gt_path") or "")
            gp_abs = gp if os.path.isabs(gp) else os.path.abspath(os.path.join(REPO_ROOT, gp))
            if not os.path.isfile(gp_abs):
                gt_ok = False
                continue
            g = _load_json(gp_abs)
            if isinstance(g, dict):
                forbid_cnt += len(set(g.keys()).intersection(FORBIDDEN_GT_FIELDS))
        checks["B_gt_readable"] = {"ok": gt_ok}
        checks["C_gt_forbidden_fields"] = {"ok": forbid_cnt == 0, "count": forbid_cnt}
        checks["M_sample_count_expanded"] = {"ok": len(samples) > 5, "sample_count": len(samples)}
        checks["N_manifest_stratified_fields_and_forbidden"] = {
            "ok": (stratified_field_missing == 0 and manifest_forbidden_cnt == 0),
            "missing_stratified_field_count": stratified_field_missing,
            "forbidden_manifest_field_count": manifest_forbidden_cnt,
        }
        if not gt_ok:
            hard.append("gt_missing")
        if forbid_cnt != 0:
            hard.append("gt_contains_forbidden_fields")
        if len(samples) <= 5:
            hard.append("sample_count_not_expanded")
        if stratified_field_missing != 0:
            hard.append("manifest_missing_stratified_fields")
        if manifest_forbidden_cnt != 0:
            hard.append("manifest_contains_forbidden_fields")

    sum_p = os.path.join(out, "ocr_benchmark_summary.json")
    checks["D_provider_outputs_or_not_available"] = {"ok": os.path.isfile(sum_p)}
    if not os.path.isfile(sum_p):
        hard.append("benchmark_summary_missing")
        print(json.dumps({"phase": "Phase-ModelOCR-005B", "verifier": "verify_ocr_raw_text_benchmark_v0.py", "checks": checks, "verdict": "NO_GO", "hard_blockers": hard, "soft_followups": soft}, ensure_ascii=False, indent=2))
        return 2

    sm = _load_json(sum_p)
    acc = os.path.join(out, "metric_tables", "accuracy_metrics.json")
    lat = os.path.join(out, "metric_tables", "latency_metrics.json")
    bb = os.path.join(out, "metric_tables", "bbox_metrics.json")
    st = os.path.join(out, "metric_tables", "stratified_metrics.json")
    cmpf = os.path.join(out, "per_sample_comparison.json")
    checks["E_metrics_files_exist"] = {"ok": all(os.path.isfile(p) for p in (acc, lat, bb))}
    checks["F_accuracy_metrics"] = {"ok": os.path.isfile(acc)}
    checks["G_latency_metrics"] = {"ok": os.path.isfile(lat)}
    checks["H_governance_leakage_zero"] = {
        "ok": (
            (sm.get("governance") or {}).get("semantic_interpretation_enabled") is False
            and (sm.get("governance") or {}).get("downstream_invoked") is False
            and (sm.get("governance") or {}).get("real_tts_invoked") is False
        )
    }
    checks["I_trace_replay_whitebox"] = {
        "ok": all(os.path.isdir(os.path.join(out, x)) for x in ("trace", "replay", "whitebox"))
    }
    checks["J_provider_comparison"] = {"ok": os.path.isfile(cmpf)}
    checks["O_stratified_metrics_present"] = {"ok": os.path.isfile(st)}

    # K paddle cls not_claimed record
    paddle_s = os.path.join(out, "provider_summaries", "paddleocr_summary.json")
    k_ok = False
    if os.path.isfile(paddle_s):
        ps = _load_json(paddle_s)
        k_ok = bool(ps.get("rotated_text_samples_not_claimed") is True and ps.get("orientation_sensitive_cases"))
    checks["K_paddle_cls_not_claimed_recorded"] = {"ok": k_ok}

    checks["L_no_downstream"] = {"ok": (sm.get("governance") or {}).get("downstream_invoked") is False}

    for k, v in checks.items():
        if not bool(v.get("ok")):
            hard.append(f"check_failed:{k}")

    sample_count = int(sm.get("sample_count") or 0)
    coverage = sm.get("dataset_coverage") or {}
    type_cov = len(set(coverage.get("expected_text_type") or []))
    lang_cov = len(set(coverage.get("language_type") or []))
    diff_cov = len(set(coverage.get("difficulty_level") or []))
    vis_cov = len(set(coverage.get("visual_condition") or []))
    if hard:
        verdict = "NO_GO"
    elif sample_count >= 30 and type_cov >= 6 and lang_cov >= 4 and diff_cov >= 3 and vis_cov >= 5:
        verdict = "GO"
    elif sample_count <= 12 or type_cov < 6:
        verdict = "NO_GO"
    else:
        verdict = "CONDITIONAL_GO"
    if verdict == "CONDITIONAL_GO":
        if sample_count < 20:
            soft.append("sample_count_below_20")
        elif sample_count < 30:
            soft.append("sample_count_between_20_29")
        if type_cov < 6:
            soft.append("expected_text_type_coverage_below_6")
        if lang_cov < 4:
            soft.append("language_coverage_below_4")
        if diff_cov < 3:
            soft.append("difficulty_coverage_below_3")
        if vis_cov < 5:
            soft.append("visual_condition_coverage_below_5")

    print(
        json.dumps(
            {
                "phase": "Phase-ModelOCR-005B",
                "verifier": "verify_ocr_raw_text_benchmark_v0.py",
                "output_root": os.path.relpath(out, REPO_ROOT) if out.startswith(REPO_ROOT) else out,
                "checks": checks,
                "verdict": verdict,
                "hard_blockers": list(dict.fromkeys(hard)),
                "soft_followups": list(dict.fromkeys(soft)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 2 if verdict == "NO_GO" else 0


if __name__ == "__main__":
    raise SystemExit(main())
