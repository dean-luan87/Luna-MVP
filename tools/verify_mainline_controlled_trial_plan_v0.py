#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Phase-Mainline-GuardedTrial-001 controlled trial plan outputs (read-only).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

EXPECTED = [
    "mainline_controlled_trial_plan_summary.json",
    "mainline_controlled_trial_order_matrix.json",
    "mainline_controlled_trial_scope_matrix.json",
    "mainline_controlled_trial_acceptance_matrix.json",
    "mainline_controlled_trial_abort_rollback_matrix.json",
    "mainline_controlled_trial_precheck_matrix.json",
    "mainline_controlled_trial_post_report_schema.json",
    "review_notes.md",
]


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def verify(*, output_root: Path) -> Tuple[bool, Dict[str, Any]]:
    checks: Dict[str, Any] = {}
    ok_all = True

    for name in EXPECTED:
        p = output_root / name
        key = f"A_file_{name}"
        checks[key] = p.is_file()
        if not checks[key]:
            ok_all = False

    if not (output_root / "mainline_controlled_trial_order_matrix.json").is_file():
        return False, {"verdict": "NO_GO", "checks": checks, "reason": "missing order matrix"}

    order = _load(output_root / "mainline_controlled_trial_order_matrix.json")
    caps = [row.get("capability") for row in order if isinstance(row, dict)]
    checks["B_order_yolo_ocr_qwen_voice"] = caps == ["yolo", "ocr", "qwen_voice"]

    summ = _load(output_root / "mainline_controlled_trial_plan_summary.json") if (output_root / "mainline_controlled_trial_plan_summary.json").is_file() else {}
    pol = summ.get("execution_policy") or {}
    checks["C_no_parallel_trial"] = pol.get("no_parallel_trials") is True and pol.get("single_active_capability_trial") is True

    dep_ok = True
    for row in order:
        if not isinstance(row, dict):
            continue
        idx = row.get("stage_index")
        after = row.get("starts_after") or []
        if idx == 2 and "Stage_1" not in str(after):
            dep_ok = False
        if idx == 3 and len(after) < 1:
            dep_ok = False
    checks["D_stage_dependency_defined"] = dep_ok and pol.get("prior_stage_go_required_for_next") is True

    scope = _load(output_root / "mainline_controlled_trial_scope_matrix.json") if (output_root / "mainline_controlled_trial_scope_matrix.json").is_file() else []
    by_cap = {r.get("capability"): r for r in scope if isinstance(r, dict)}
    checks["E_yolo_scope_defined"] = "yolo" in by_cap and bool(by_cap["yolo"].get("allowed"))
    checks["F_ocr_scope_defined"] = "ocr" in by_cap and bool(by_cap["ocr"].get("allowed"))
    checks["G_qwen_voice_scope_defined"] = "qwen_voice" in by_cap and bool(by_cap["qwen_voice"].get("allowed"))

    acc = _load(output_root / "mainline_controlled_trial_acceptance_matrix.json") if (output_root / "mainline_controlled_trial_acceptance_matrix.json").is_file() else []
    checks["H_acceptance_nonempty"] = isinstance(acc, list) and len(acc) > 0

    ar = _load(output_root / "mainline_controlled_trial_abort_rollback_matrix.json") if (output_root / "mainline_controlled_trial_abort_rollback_matrix.json").is_file() else []
    abort_nonempty = False
    rollback_nonempty = False
    for row in ar if isinstance(ar, list) else []:
        if isinstance(row, dict):
            for k in row:
                if "abort" in k.lower() and isinstance(row[k], list) and len(row[k]) > 0:
                    abort_nonempty = True
            ra = row.get("rollback_actions")
            if isinstance(ra, list) and len(ra) > 0:
                rollback_nonempty = True
    checks["I_abort_nonempty"] = abort_nonempty
    checks["J_rollback_nonempty"] = rollback_nonempty

    pre = _load(output_root / "mainline_controlled_trial_precheck_matrix.json") if (output_root / "mainline_controlled_trial_precheck_matrix.json").is_file() else []
    checks["K_precheck_nonempty"] = isinstance(pre, list) and len(pre) > 0

    schema = _load(output_root / "mainline_controlled_trial_post_report_schema.json") if (output_root / "mainline_controlled_trial_post_report_schema.json").is_file() else {}
    checks["L_post_report_schema_exists"] = isinstance(schema, dict) and bool(schema.get("required_fields"))

    defn = summ.get("definition_only") or {}
    checks["M_real_runtime_not_executed"] = defn.get("real_runtime_executed") is False and defn.get("real_trial_executed") is False
    checks["N_playback_not_approved_this_phase"] = defn.get("playback_approved_in_this_phase") is False
    checks["O_qwen_3C_future_only"] = (
        defn.get("qwen_voice_3C") == "future_only_not_approved_in_phase_001"
        or "NOT_APPROVED" in json.dumps(by_cap.get("qwen_voice", {}), ensure_ascii=False)
    )
    prior = summ.get("prior_closure_reference") or {}
    checks["P_global_kill_switch_required"] = prior.get("global_kill_switch_required") is True

    for k, v in checks.items():
        if k.startswith("A_file_"):
            continue
        if v is False:
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
