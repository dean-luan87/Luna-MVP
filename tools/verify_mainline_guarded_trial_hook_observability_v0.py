#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Phase-Mainline-RuntimeReadiness-005 observability outputs against Phase-004 hook-in artifacts (read-only checks).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

STAGE_NAME = "request_trace.stage.runtime_readiness.guarded_trial_hook"
STAGE_NAMESPACE = "mainline_runtime_readiness_v0"

EXPECTED_FILES = [
    "mainline_guarded_trial_hook_observability_summary.json",
    "mainline_guarded_trial_hook_request_trace_stages.json",
    "mainline_guarded_trial_hook_observability_matrix.json",
    "mainline_guarded_trial_hook_side_effect_audit_export.json",
    "mainline_guarded_trial_hook_query_table.json",
    "mainline_guarded_trial_hook_trace.jsonl",
    "mainline_guarded_trial_hook_replay.jsonl",
    "mainline_guarded_trial_hook_whitebox.jsonl",
    "evaluation_notes.md",
]


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonl_nonempty(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8").strip()
    return len(text) > 0


def _bool_ok(v: Any, expected: bool) -> bool:
    return v is expected


def verify(*, hook_root: Path, output_root: Path) -> Tuple[bool, Dict[str, Any]]:
    checks: Dict[str, Any] = {}
    ok_all = True

    # A
    hr_path = hook_root / "mainline_guarded_trial_hook_results.json"
    checks["A_hook_root_readable"] = hr_path.is_file()
    if not checks["A_hook_root_readable"]:
        ok_all = False

    # B
    hook_blob: List[Dict[str, Any]] = []
    if checks["A_hook_root_readable"]:
        hook_blob = _load_json(hr_path)
        checks["B_hook_results_loaded"] = isinstance(hook_blob, list) and len(hook_blob) > 0
    else:
        checks["B_hook_results_loaded"] = False
    if not checks["B_hook_results_loaded"]:
        ok_all = False

    stages_path = output_root / "mainline_guarded_trial_hook_request_trace_stages.json"
    matrix_path = output_root / "mainline_guarded_trial_hook_observability_matrix.json"
    audit_path = output_root / "mainline_guarded_trial_hook_side_effect_audit_export.json"
    query_path = output_root / "mainline_guarded_trial_hook_query_table.json"
    summary_path = output_root / "mainline_guarded_trial_hook_observability_summary.json"
    trace_j = output_root / "mainline_guarded_trial_hook_trace.jsonl"
    replay_j = output_root / "mainline_guarded_trial_hook_replay.jsonl"
    white_j = output_root / "mainline_guarded_trial_hook_whitebox.jsonl"

    for name in EXPECTED_FILES:
        p = output_root / name
        if not p.is_file():
            checks[f"missing_file:{name}"] = False
            ok_all = False
        else:
            checks[f"missing_file:{name}"] = True

    stages: List[Dict[str, Any]] = []
    if stages_path.is_file():
        stages = _load_json(stages_path)

    checks["C_request_trace_stages_generated"] = isinstance(stages, list) and len(stages) >= 3
    if not checks["C_request_trace_stages_generated"]:
        ok_all = False

    caps_in_stages = {s.get("capability") for s in stages if isinstance(s, dict)}
    checks["D_yolo_hook_stage_present"] = "yolo" in caps_in_stages
    checks["E_ocr_hook_stage_present"] = "ocr" in caps_in_stages
    checks["F_qwen_voice_hook_stage_present"] = "qwen_voice" in caps_in_stages
    for k in ("D_yolo_hook_stage_present", "E_ocr_hook_stage_present", "F_qwen_voice_hook_stage_present"):
        if not checks[k]:
            ok_all = False

    ns_ok = all(
        s.get("stage_namespace") == STAGE_NAMESPACE and s.get("stage_name") == STAGE_NAME for s in stages if isinstance(s, dict)
    )
    checks["G_stage_namespace_correct"] = bool(stages) and ns_ok
    if not checks["G_stage_namespace_correct"]:
        ok_all = False

    checks["H_observability_matrix_generated"] = matrix_path.is_file()
    if checks["H_observability_matrix_generated"]:
        mx = _load_json(matrix_path)
        checks["H_observability_matrix_generated"] = isinstance(mx, list) and len(mx) >= 3
    if not checks["H_observability_matrix_generated"]:
        ok_all = False

    checks["I_side_effect_audit_export_generated"] = audit_path.is_file()
    if checks["I_side_effect_audit_export_generated"]:
        au = _load_json(audit_path)
        checks["I_side_effect_audit_export_generated"] = isinstance(au, list) and len(au) >= 3
    if not checks["I_side_effect_audit_export_generated"]:
        ok_all = False

    checks["J_query_table_generated"] = query_path.is_file()
    if checks["J_query_table_generated"]:
        qt = _load_json(query_path)
        checks["J_query_table_generated"] = isinstance(qt, list) and len(qt) >= 3
    if not checks["J_query_table_generated"]:
        ok_all = False

    # K–S from stages + audit rows (canonical default_env shadow)
    def _inv(rows: List[Dict[str, Any]], key: str, pred) -> bool:
        return all(pred(r.get(key)) for r in rows)

    checks["K_enabled_false_preserved"] = _inv(stages, "enabled", lambda v: v is False)
    checks["L_no_op_true_preserved"] = _inv(stages, "no_op", lambda v: v is True)

    ha_list = [s.get("hard_audit") or {} for s in stages if isinstance(s, dict)]
    checks["M_runtime_invoked_false"] = all(x.get("runtime_invoked") is False for x in ha_list)
    checks["N_provider_invoked_false"] = all(x.get("provider_invoked") is False for x in ha_list)
    checks["O_playback_invoked_false"] = all(x.get("playback_invoked") is False for x in ha_list)
    checks["P_downstream_invocation_count_zero"] = all(int(x.get("downstream_invocation_count") or 0) == 0 for x in ha_list)
    checks["Q_world_write_invoked_false"] = all(x.get("world_write_invoked") is False for x in ha_list)
    checks["R_navigation_action_null"] = all(x.get("navigation_action") is None for x in ha_list)
    checks["S_default_behavior_changed_false"] = all(x.get("default_behavior_changed") is False for x in ha_list)

    for k in (
        "K_enabled_false_preserved",
        "L_no_op_true_preserved",
        "M_runtime_invoked_false",
        "N_provider_invoked_false",
        "O_playback_invoked_false",
        "P_downstream_invocation_count_zero",
        "Q_world_write_invoked_false",
        "R_navigation_action_null",
        "S_default_behavior_changed_false",
    ):
        if not checks.get(k, False):
            ok_all = False

    checks["T_trace_replay_whitebox_nonempty"] = (
        _jsonl_nonempty(trace_j) and _jsonl_nonempty(replay_j) and _jsonl_nonempty(white_j)
    )
    if not checks["T_trace_replay_whitebox_nonempty"]:
        ok_all = False

    # U: input hook results sha256 matches summary (proves evaluate pass did not rewrite hook-root file content we hashed)
    checks["U_source_hook_output_integrity"] = False
    if summary_path.is_file() and hr_path.is_file():
        summ = _load_json(summary_path)
        expected = summ.get("input_hook_results_sha256")
        actual = _sha256_file(hr_path)
        checks["U_source_hook_output_integrity"] = expected == actual and isinstance(expected, str) and len(expected) == 64
    if not checks["U_source_hook_output_integrity"]:
        ok_all = False

    # Extra: audit export side_effect_ok
    if audit_path.is_file():
        au = _load_json(audit_path)
        checks["extra_side_effect_ok_all"] = all(r.get("side_effect_ok") is True for r in au if isinstance(r, dict))
        if not checks["extra_side_effect_ok_all"]:
            ok_all = False

    verdict = "GO" if ok_all else "NO_GO"
    return ok_all, {"verdict": verdict, "checks": checks, "hook_root": str(hook_root), "output_root": str(output_root)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook-root", default="logs/mainline_guarded_trial_hook_in_004_final")
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    repo = Path(REPO_ROOT)
    hook_root = Path(args.hook_root)
    if not hook_root.is_absolute():
        hook_root = (repo / hook_root).resolve()
    output_root = Path(args.output_root).resolve()

    ok, report = verify(hook_root=hook_root, output_root=output_root)
    print(json.dumps({"ok": ok, **report}, ensure_ascii=False, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
