#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import statistics
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _abs_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(os.path.join(REPO_ROOT, p))


def _variance(vals: List[float]) -> float:
    if len(vals) <= 1:
        return 0.0
    return float(statistics.pvariance(vals))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", required=True, help="comma separated output roots")
    ap.add_argument("--dataset-manifest", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    roots = [_abs_path(x.strip()) for x in str(args.roots).split(",") if x.strip()]
    out_root = _abs_path(args.output_root)
    dm = _abs_path(args.dataset_manifest)
    os.makedirs(out_root, exist_ok=True)

    providers = ["rapidocr", "macos_vision", "paddleocr"]
    metric_keys = [
        "text_exact_match_rate",
        "character_error_rate",
        "bbox_iou_avg",
        "avg_latency_ms_per_frame",
        "p95_latency_ms_per_frame",
    ]

    # Dataset distribution + imbalance risks
    man = _load_json(dm)
    samples = man.get("samples") if isinstance(man, dict) else []
    dist: Dict[str, Dict[str, int]] = {
        "expected_text_type": {},
        "language_type": {},
        "difficulty_level": {},
        "visual_condition": {},
    }
    for s in samples:
        for k in dist.keys():
            v = str(s.get(k) or "unknown")
            dist[k][v] = dist[k].get(v, 0) + 1
    _write_json(os.path.join(out_root, "dataset_distribution_summary.json"), {"sample_count": len(samples), "distribution": dist})

    risks: List[Dict[str, Any]] = []
    if len(dist["expected_text_type"]) < 6:
        risks.append({"risk_id": "type_coverage_low", "severity": "high", "detail": "expected_text_type < 6"})
    if "exit_sign" not in dist["expected_text_type"]:
        risks.append({"risk_id": "exit_sign_missing", "severity": "medium", "detail": "navigation high-value class missing"})
    if "warning_text" not in dist["expected_text_type"]:
        risks.append({"risk_id": "warning_text_missing", "severity": "medium", "detail": "safety class missing"})
    if dist["language_type"].get("zh", 0) < dist["language_type"].get("en", 0):
        risks.append({"risk_id": "zh_less_than_en", "severity": "low", "detail": "zh sample count lower than en"})
    _write_json(os.path.join(out_root, "imbalance_risk_register.json"), {"risks": risks})

    provider_metric_values: Dict[str, Dict[str, List[float]]] = {p: {k: [] for k in metric_keys} for p in providers}
    provider_failure_count: Dict[str, int] = {p: 0 for p in providers}
    governance_leakage_count = 0
    output_schema_drift_count = 0
    trace_replay_whitebox_drift_count = 0

    base_schema_keys: Dict[str, set] = {}
    base_summary_keys: set = set()

    for i, r in enumerate(roots):
        s_path = os.path.join(r, "ocr_benchmark_summary.json")
        s_obj = _load_json(s_path)
        cur_sum_keys = set(s_obj.keys()) if isinstance(s_obj, dict) else set()
        if i == 0:
            base_summary_keys = cur_sum_keys
        elif cur_sum_keys != base_summary_keys:
            output_schema_drift_count += 1

        gov = s_obj.get("governance") or {}
        if not (
            gov.get("semantic_interpretation_enabled") is False
            and gov.get("downstream_invoked") is False
            and gov.get("real_tts_invoked") is False
        ):
            governance_leakage_count += 1

        for d in ("trace", "replay", "whitebox"):
            if not os.path.isdir(os.path.join(r, d)):
                trace_replay_whitebox_drift_count += 1

        for p in providers:
            p_path = os.path.join(r, "provider_summaries", f"{p}_summary.json")
            pobj = _load_json(p_path)
            pkeys = set(pobj.keys()) if isinstance(pobj, dict) else set()
            if i == 0:
                base_schema_keys[p] = pkeys
            elif pkeys != base_schema_keys[p]:
                output_schema_drift_count += 1
            mets = pobj.get("metrics") or {}
            for mk in metric_keys:
                v = mets.get(mk)
                if isinstance(v, (int, float)):
                    provider_metric_values[p][mk].append(float(v))
            if (pobj.get("hard_blockers") or []):
                provider_failure_count[p] += 1

    metric_var: Dict[str, Any] = {}
    for p in providers:
        metric_var[p] = {}
        for mk in metric_keys:
            vals = provider_metric_values[p][mk]
            metric_var[p][mk] = {
                "runs": len(vals),
                "values": vals,
                "variance": round(_variance(vals), 10),
            }
        metric_var[p]["provider_failure_count"] = provider_failure_count[p]

    _write_json(os.path.join(out_root, "provider_metric_variance.json"), metric_var)

    governance_stability = {
        "runs": len(roots),
        "governance_leakage_count": governance_leakage_count,
        "stable_zero_leakage": governance_leakage_count == 0,
    }
    artifact_stability = {
        "runs": len(roots),
        "output_schema_drift_count": output_schema_drift_count,
        "trace_replay_whitebox_drift_count": trace_replay_whitebox_drift_count,
    }
    _write_json(os.path.join(out_root, "governance_stability.json"), governance_stability)
    _write_json(os.path.join(out_root, "artifact_stability.json"), artifact_stability)

    paddle_fairness_status = {
        "unfair_current_path": True,
        "needs_real_inference_path": True,
        "needs_same_input_same_gt": True,
        "no_default_decision_allowed": True,
        "reason": "current benchmark path for paddleocr remains skeleton/init-biased and not equivalent to full real-inference comparison",
    }

    stability_summary = {
        "phase": "Phase-ModelOCR-006",
        "roots": [os.path.relpath(x, REPO_ROOT) if x.startswith(REPO_ROOT) else x for x in roots],
        "repeat_run_count": max(0, len(roots) - 1),
        "exact_match_rate_variance": {p: metric_var[p]["text_exact_match_rate"]["variance"] for p in providers},
        "cer_variance": {p: metric_var[p]["character_error_rate"]["variance"] for p in providers},
        "bbox_iou_variance": {p: metric_var[p]["bbox_iou_avg"]["variance"] for p in providers},
        "avg_latency_variance": {p: metric_var[p]["avg_latency_ms_per_frame"]["variance"] for p in providers},
        "p95_latency_variance": {p: metric_var[p]["p95_latency_ms_per_frame"]["variance"] for p in providers},
        "provider_failure_count": provider_failure_count,
        "output_schema_drift_count": output_schema_drift_count,
        "governance_leakage_count": governance_leakage_count,
        "trace_replay_whitebox_drift_count": trace_replay_whitebox_drift_count,
        "paddleocr_fairness_status": paddle_fairness_status,
        "verdict": "GO"
        if (len(roots) >= 3 and governance_leakage_count == 0 and output_schema_drift_count == 0 and trace_replay_whitebox_drift_count == 0 and sum(provider_failure_count.values()) == 0)
        else ("CONDITIONAL_GO" if governance_leakage_count == 0 and output_schema_drift_count == 0 else "NO_GO"),
        "hard_blockers": [],
        "soft_followups": [],
    }
    if stability_summary["verdict"] == "CONDITIONAL_GO":
        stability_summary["soft_followups"].append("repeat_runs_less_than_3")
    _write_json(os.path.join(out_root, "stability_summary.json"), stability_summary)

    print(json.dumps({"ok": True, "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root, "verdict": stability_summary["verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
