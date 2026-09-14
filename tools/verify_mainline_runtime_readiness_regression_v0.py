#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Phase-Mainline-RuntimeReadiness-006 regression outputs (read-only).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DOC_ANCHORS = {
    "001": Path(REPO_ROOT, "docs/architecture/LUNA_MAINLINE_RUNTIME_READINESS_REVIEW_V0.md"),
    "002": Path(REPO_ROOT, "docs/architecture/LUNA_MAINLINE_GUARDED_TRIAL_SCOPE_DEFINITION_V0.md"),
    "003": Path(REPO_ROOT, "docs/architecture/LUNA_MAINLINE_GUARDED_TRIAL_WIRING_PATH_MAPPING_V0.md"),
    "004": Path(REPO_ROOT, "capabilities/runtime_readiness/yolo_guarded_trial_hook_v0.py"),
    "005": Path(REPO_ROOT, "docs/architecture/LUNA_MAINLINE_GUARDED_TRIAL_HOOK_OBSERVABILITY_V0.md"),
}


def _load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _phase_row(matrix: List[Dict[str, Any]], num: str) -> Dict[str, Any]:
    want = f"Phase-Mainline-RuntimeReadiness-{num}"
    for r in matrix:
        if r.get("phase_id") == want:
            return r
    return {}


def verify(*, output_root: Path) -> Tuple[bool, Dict[str, Any]]:
    checks: Dict[str, Any] = {}
    ok_all = True

    summ_path = output_root / "mainline_runtime_readiness_regression_summary.json"
    pm_path = output_root / "mainline_runtime_readiness_phase_matrix.json"
    cap_path = output_root / "mainline_runtime_readiness_capability_matrix.json"
    gh_path = output_root / "mainline_runtime_readiness_gate_hook_matrix.json"
    obs_path = output_root / "mainline_runtime_readiness_observability_matrix.json"
    bnd_path = output_root / "mainline_runtime_readiness_boundary_summary.json"
    clo_path = output_root / "mainline_runtime_readiness_closure_recommendation.json"

    checks["A_regression_summary_exists"] = summ_path.is_file()
    checks["B_phase_matrix_exists"] = pm_path.is_file()
    if not checks["A_regression_summary_exists"] or not checks["B_phase_matrix_exists"]:
        return False, {"verdict": "NO_GO", "checks": checks, "reason": "missing core outputs"}

    summary = _load_json(summ_path)
    pm = _load_json(pm_path)
    cap = _load_json(cap_path) if cap_path.is_file() else []
    gh = _load_json(gh_path) if gh_path.is_file() else {}
    obs = _load_json(obs_path) if obs_path.is_file() else {}
    bnd = _load_json(bnd_path) if bnd_path.is_file() else {}
    clo = _load_json(clo_path) if clo_path.is_file() else {}

    def _rep_or_doc(num: str) -> bool:
        row = _phase_row(pm, num)
        if row.get("represented"):
            return True
        p = DOC_ANCHORS.get(num)
        return bool(p and p.is_file())

    checks["C_001_review_represented"] = _rep_or_doc("001")
    checks["D_002_trial_definition_represented"] = _rep_or_doc("002")
    checks["E_003_gate_module_represented"] = _rep_or_doc("003")
    checks["F_004_hook_in_represented"] = _rep_or_doc("004")
    checks["G_005_observability_represented"] = _rep_or_doc("005")

    trials = {"yolo_guarded_trial_v1", "ocr_guarded_trial_v1", "qwen_voice_governed_entry_trial_v1"}
    cap_names = {r.get("trial_name") for r in cap if isinstance(r, dict)}
    checks["H_yolo_trial_present"] = "yolo_guarded_trial_v1" in cap_names
    checks["I_ocr_trial_present"] = "ocr_guarded_trial_v1" in cap_names
    checks["J_qwen_voice_trial_present"] = "qwen_voice_governed_entry_trial_v1" in cap_names

    gks = gh.get("global_kill_switch") or {}
    checks["K_global_kill_switch_represented"] = bool(gks.get("represented")) or (
        "LUNA_DISABLE_ALL_GUARDED_TRIALS"
        in Path(REPO_ROOT, "capabilities/runtime_readiness/guarded_trial_gate_v0.py").read_text(encoding="utf-8")
        if Path(REPO_ROOT, "capabilities/runtime_readiness/guarded_trial_gate_v0.py").is_file()
        else False
    )

    inv = (gh.get("default_env_invariants") or {}) if isinstance(gh, dict) else {}
    has_004_data = inv.get("has_default_env_data") is True
    se_clear = inv.get("all_side_effect_clear")
    checks["L_all_default_enabled_false"] = (inv.get("all_enabled_false") is not False) or (not has_004_data)
    checks["M_all_hooks_no_op_true"] = (inv.get("all_no_op_true") is not False) or (not has_004_data)
    checks["N_all_side_effect_ok"] = (se_clear is not False) or (not has_004_data)

    rt = gh.get("request_trace_from_005") or {}
    checks["O_request_trace_hook_stage_represented"] = bool(rt.get("stage_schema_ok")) or bool(
        rt.get("trials_in_stages")
    )

    checks["P_whitebox_minimal_observability_represented"] = obs.get("whitebox_scope") == "minimal_observability_only"

    v = summary.get("verdict") or {}
    clo_v = (clo.get("verdict") if isinstance(clo, dict) else {}) or {}
    checks["Q_real_runtime_activation_no_go"] = (v.get("real_runtime_activation") == "NO_GO") or (
        clo_v.get("real_runtime_activation") == "NO_GO"
    )

    checks["R_provider_invoked_false"] = (inv.get("all_provider_invoked_false") is not False) or (not has_004_data)
    checks["S_playback_invoked_false"] = (inv.get("all_playback_invoked_false") is not False) or (not has_004_data)
    checks["T_world_write_invoked_false"] = (inv.get("all_world_write_invoked_false") is not False) or (not has_004_data)
    checks["U_navigation_action_null"] = (inv.get("all_navigation_action_null") is not False) or (not has_004_data)

    checks["V_closure_recommendation_present"] = clo_path.is_file() and isinstance(clo, dict) and bool(
        clo.get("runtime_readiness_status")
    )

    for k, val in list(checks.items()):
        if k.endswith("_note"):
            continue
        if val is False:
            ok_all = False

    return ok_all, {"verdict": "GO" if ok_all else "NO_GO", "checks": checks, "output_root": str(output_root)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    out = Path(args.output_root).resolve()
    ok, report = verify(output_root=out)
    print(json.dumps({"ok": ok, **report}, ensure_ascii=False, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
