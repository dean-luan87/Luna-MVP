#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EngineeringFlow-006
Offline Mainline Regression Acceptance v0

Hard boundaries:
- v0 defaults to reuse-existing-roots only (read-only inputs).
- Must not rerun models or offline mainline runner unless explicitly implemented in a future phase.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple


def _exists(p: str) -> bool:
    try:
        return os.path.exists(p)
    except Exception:
        return False


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _safe_float(x: Any) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0


def _require(cond: bool, code: str, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"check": code, "pass": bool(cond), **details}


def _load_ef004_summary(root: str) -> Dict[str, Any]:
    root = os.path.abspath(root)
    summ_p = os.path.join(root, "mainline_summary.json")
    per_p = os.path.join(root, "per_sample_mainline_results.json")
    out: Dict[str, Any] = {
        "root": root,
        "paths": {"summary": summ_p, "per_sample": per_p},
        "exists": {"summary": _exists(summ_p), "per_sample": _exists(per_p)},
        "summary": _read_json(summ_p) if _exists(summ_p) else {},
        "per_sample": _read_json(per_p) if _exists(per_p) else {},
    }
    return out


def _load_ef005_report(root: str) -> Dict[str, Any]:
    root = os.path.abspath(root)
    p_report = os.path.join(root, "observability_report.json")
    p_verify = os.path.join(root, "verification_result.json")
    p_cmp = os.path.join(root, "normal_vs_fallback_comparison.json")
    p_safety = os.path.join(root, "safety_boundary_summary.json")
    p_evidence = os.path.join(root, "evidence_boundary_summary.json")
    p_matrix = os.path.join(root, "sample_chain_matrix.json")
    p_index = os.path.join(root, "stage_artifact_index.json")
    return {
        "root": root,
        "paths": {
            "observability_report": p_report,
            "verification_result": p_verify,
            "comparison": p_cmp,
            "safety": p_safety,
            "evidence": p_evidence,
            "sample_chain_matrix": p_matrix,
            "stage_artifact_index": p_index,
        },
        "exists": {k: _exists(v) for k, v in {
            "observability_report": p_report,
            "verification_result": p_verify,
            "comparison": p_cmp,
            "safety": p_safety,
            "evidence": p_evidence,
            "sample_chain_matrix": p_matrix,
            "stage_artifact_index": p_index,
        }.items()},
        "report": _read_json(p_report) if _exists(p_report) else {},
        "verification": _read_json(p_verify) if _exists(p_verify) else {},
        "comparison": _read_json(p_cmp) if _exists(p_cmp) else {},
        "safety": _read_json(p_safety) if _exists(p_safety) else {},
        "evidence": _read_json(p_evidence) if _exists(p_evidence) else {},
        "sample_chain_matrix": _read_json(p_matrix) if _exists(p_matrix) else {},
        "stage_artifact_index": _read_json(p_index) if _exists(p_index) else {},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--normal-root", required=True)
    ap.add_argument("--fallback-root", required=True)
    ap.add_argument("--observability-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--mode", default="reuse-existing-roots", choices=["reuse-existing-roots"])
    args = ap.parse_args()

    if args.mode != "reuse-existing-roots":
        raise SystemExit("v0_only_supports_reuse_existing_roots")

    normal = _load_ef004_summary(args.normal_root)
    fallback = _load_ef004_summary(args.fallback_root)
    obs = _load_ef005_report(args.observability_root)

    out_root = os.path.abspath(args.output_root)
    if os.path.exists(out_root) and (not os.path.isdir(out_root) or os.listdir(out_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(out_root, exist_ok=True)

    run_id = f"reg-{uuid.uuid4()}"
    generated_at_s = time.time()

    # Extract expected values from EF-005 comparison (single source of truth for normal vs fallback)
    cmp_obj = obs.get("comparison") or {}
    safety_obj = obs.get("safety") or {}
    evidence_obj = obs.get("evidence") or {}
    obs_verify = obs.get("verification") or {}

    gates: List[Dict[str, Any]] = []

    # ---- Hard thresholds (as per user spec) ----
    # Chain
    gates.append(_require((_safe_float(cmp_obj.get("normal_chain_complete_rate")) == 1.0), "chain_normal_complete_rate_1.0", {"value": cmp_obj.get("normal_chain_complete_rate")}))
    gates.append(_require((_safe_float(cmp_obj.get("fallback_chain_complete_rate")) == 1.0), "chain_fallback_complete_rate_1.0", {"value": cmp_obj.get("fallback_chain_complete_rate")}))

    # Schema (from EF-004 summaries)
    ns = normal.get("summary") or {}
    fs = fallback.get("summary") or {}
    n_schema = ns.get("schema_valid_rates") or {}
    f_schema = fs.get("schema_valid_rates") or {}
    all_schema_ok = True
    for stage in ["perception", "scene_context", "scene_task", "fusion", "output"]:
        if _safe_float(n_schema.get(stage)) != 1.0 or _safe_float(f_schema.get(stage)) != 1.0:
            all_schema_ok = False
    gates.append(_require(all_schema_ok, "schema_all_stages_valid_1.0", {"normal": n_schema, "fallback": f_schema}))

    # Source policy
    n_dist = cmp_obj.get("normal_source_distribution") or {}
    f_dist = cmp_obj.get("fallback_source_distribution") or {}
    gates.append(_require(int(n_dist.get("yolo_shadow") or 0) == 3, "source_policy_normal_yolo_shadow_eq_3", {"dist": n_dist}))
    gates.append(_require(int(f_dist.get("baseline_mock") or 0) == 3, "source_policy_fallback_baseline_mock_eq_3", {"dist": f_dist}))

    # Fallback reason present rate: v0 minimal implementation uses fallback run; enforce fallback_count==3 as proxy
    fallback_count = (obs.get("report") or {}).get("source_policy_summary", {}).get("fallback_count")
    gates.append(_require(int(fallback_count or 0) == 3, "source_policy_fallback_count_eq_3", {"fallback_count": fallback_count}))

    # SceneContext presence (from EF-004 complete rates)
    n_complete = ns.get("stage_complete_rates") or {}
    f_complete = fs.get("stage_complete_rates") or {}
    gates.append(_require(_safe_float(n_complete.get("scene_context")) == 1.0 and _safe_float(f_complete.get("scene_context")) == 1.0, "scene_context_stage_complete_rate_1.0", {"normal": n_complete.get("scene_context"), "fallback": f_complete.get("scene_context")}))

    # Output: no real TTS + no execute
    gates.append(_require(_safe_float(safety_obj.get("real_tts_invoked_false_rate")) == 1.0, "output_real_tts_invoked_false_rate_1.0", {"value": safety_obj.get("real_tts_invoked_false_rate")}))
    gates.append(_require(_safe_float(safety_obj.get("allows_execute_now_false_rate")) == 1.0, "output_allows_execute_now_false_rate_1.0", {"value": safety_obj.get("allows_execute_now_false_rate")}))

    # Observability integrity
    required_obs_files = [
        "observability_report",
        "verification_result",
        "comparison",
        "safety",
        "evidence",
        "sample_chain_matrix",
        "stage_artifact_index",
    ]
    obs_exists = obs.get("exists") or {}
    gates.append(_require(all(bool(obs_exists.get(k)) for k in required_obs_files), "observability_required_files_exist", {"exists": obs_exists}))
    gates.append(_require(bool(obs_verify.get("all_pass") is True), "observability_verifier_all_pass", {"all_pass": obs_verify.get("all_pass"), "checks": obs_verify.get("checks_passed"), "total": obs_verify.get("checks_total")}))

    broken_refs = (obs_verify.get("broken_stage_refs") or [])
    gates.append(_require(len(broken_refs) == 0, "observability_broken_refs_eq_0", {"broken_refs_count": len(broken_refs)}))

    # Safety: leakage totals must be 0
    for k in [
        "execute_leakage_count_total",
        "default_on_leakage_count_total",
        "release_retry_reopen_leakage_count_total",
        "side_effects_expansion_count_total",
        "forced_navigation_action_count_total",
        "forbidden_output_semantic_count_total",
    ]:
        gates.append(_require(int(safety_obj.get(k) or 0) == 0, f"safety_{k}_eq_0", {"value": safety_obj.get(k)}))

    # Evidence boundary
    for k, expect in [
        ("evidence_type_preserved_rate", 1.0),
        ("controlled_live_stream_false_rate", 1.0),
        ("phone_local_capture_true_rate", 1.0),
        ("pending_real_sidewalk_run_true_rate", 1.0),
    ]:
        gates.append(_require(_safe_float(evidence_obj.get(k)) == expect, f"evidence_{k}_eq_1.0", {"value": evidence_obj.get(k)}))
    gates.append(_require(int(evidence_obj.get("evidence_type_mutation_count") or 0) == 0, "evidence_evidence_type_mutation_count_eq_0", {"value": evidence_obj.get("evidence_type_mutation_count")}))
    gates.append(_require(int(evidence_obj.get("pending_closed_count") or 0) == 0, "evidence_pending_closed_count_eq_0", {"value": evidence_obj.get("pending_closed_count")}))

    hard_failures = [g for g in gates if not g.get("pass")]
    recommendation = "go" if len(hard_failures) == 0 else "no_go"

    summary = {
        "phase": "Phase-EngineeringFlow-006",
        "tool": "run_offline_mainline_regression_acceptance_v0.py",
        "run_id": run_id,
        "generated_at_s": generated_at_s,
        "mode": args.mode,
        "inputs": {
            "normal_root": os.path.abspath(args.normal_root),
            "fallback_root": os.path.abspath(args.fallback_root),
            "observability_root": os.path.abspath(args.observability_root),
        },
        "outputs": {
            "output_root": out_root,
            "regression_acceptance_summary": "regression_acceptance_summary.json",
            "regression_acceptance_matrix": "regression_acceptance_matrix.json",
            "regression_gate_results": "regression_gate_results.json",
            "regression_notes": "regression_notes.md",
        },
        "hard_thresholds_total": len(gates),
        "hard_thresholds_passed": int(sum(1 for g in gates if g.get("pass"))),
        "hard_thresholds_failed": len(hard_failures),
        "hard_blockers": [f.get("check") for f in hard_failures],
        "soft_followups": ["v0_reuse_existing_roots_only", "allowed_variance_detection_count_total"],
        "recommendation": recommendation,
    }

    matrix = {
        "normal_vs_fallback": cmp_obj,
        "schema_validity": {"normal": n_schema, "fallback": f_schema},
        "stage_complete_rates": {"normal": n_complete, "fallback": f_complete},
        "safety_boundary_summary": safety_obj,
        "evidence_boundary_summary": evidence_obj,
        "observability_verification": {
            "all_pass": obs_verify.get("all_pass"),
            "checks_passed": obs_verify.get("checks_passed"),
            "checks_total": obs_verify.get("checks_total"),
            "broken_refs_count": len(broken_refs),
        },
        "allowed_variance": {
            "normal_detection_count_total": cmp_obj.get("normal_detection_count_total"),
            "fallback_detection_count_total": cmp_obj.get("fallback_detection_count_total"),
        },
    }

    gate_results = {
        "gates": gates,
        "all_pass": len(hard_failures) == 0,
        "hard_failures": hard_failures,
    }

    notes_lines = [
        "# Offline Mainline Regression Acceptance v0 (EF-006)",
        "",
        f"- run_id: `{run_id}`",
        f"- normal_root: `{summary['inputs']['normal_root']}`",
        f"- fallback_root: `{summary['inputs']['fallback_root']}`",
        f"- observability_root: `{summary['inputs']['observability_root']}`",
        f"- recommendation: **{recommendation}**",
        "",
        "## Hard blockers",
        "- " + ("\n- ".join(summary["hard_blockers"]) if summary["hard_blockers"] else "(none)"),
        "",
        "## Allowed variance (v0)",
        "- detection_count_total is allowed to vary (not a blocker).",
        "",
        "## Explicit boundary statement",
        "- 本工具仅复用既有产物做验收：不重跑模型、不重跑主链、不进入真实 runtime、不执行导航动作、不真实播报、不接 controlled_live_stream。",
        "",
    ]

    _write_json(os.path.join(out_root, "regression_acceptance_summary.json"), summary)
    _write_json(os.path.join(out_root, "regression_acceptance_matrix.json"), matrix)
    _write_json(os.path.join(out_root, "regression_gate_results.json"), gate_results)
    _write_text(os.path.join(out_root, "regression_notes.md"), "\n".join(notes_lines) + "\n")

    print(json.dumps({"output_root": out_root, "recommendation": recommendation}, ensure_ascii=False, indent=2))
    return 0 if recommendation != "no_go" else 2


if __name__ == "__main__":
    raise SystemExit(main())

