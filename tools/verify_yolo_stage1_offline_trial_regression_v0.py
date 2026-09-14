#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Phase-Mainline-GuardedTrial-007 regression & closure outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Tuple


EXPECTED = [
    "yolo_stage1_offline_trial_regression_summary.json",
    "yolo_stage1_offline_trial_phase_matrix.json",
    "yolo_stage1_offline_trial_window_matrix.json",
    "yolo_stage1_offline_trial_boundary_summary.json",
    "yolo_stage1_offline_trial_hard_audit_summary.json",
    "yolo_stage1_offline_trial_closure_recommendation.json",
    "regression_notes.md",
]


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _nj(p: Path) -> bool:
    return p.is_file() and bool(p.read_text(encoding="utf-8").strip())


def verify(*, output_root: Path) -> Tuple[bool, Dict[str, Any]]:
    checks: Dict[str, Any] = {}

    for name in EXPECTED:
        checks[f"A_{name}"] = (output_root / name).is_file()

    summ_p = output_root / "yolo_stage1_offline_trial_regression_summary.json"
    clo_p = output_root / "yolo_stage1_offline_trial_closure_recommendation.json"
    win_p = output_root / "yolo_stage1_offline_trial_window_matrix.json"
    bnd_p = output_root / "yolo_stage1_offline_trial_boundary_summary.json"

    if not summ_p.is_file() or not clo_p.is_file() or not win_p.is_file() or not bnd_p.is_file():
        return False, {"checks": checks, "verdict": "NO_GO"}

    summ = _load(summ_p)
    clo = _load(clo_p)
    wins = _load(win_p).get("rows") or []
    bnd = _load(bnd_p)

    checks["B_fix10_root_represented"] = bool((clo.get("closure_inputs") or {}).get("fix_10_root"))
    checks["C_multi_window_root_represented"] = bool((clo.get("closure_inputs") or {}).get("multi_window_root"))

    # D/E/F/G: window GO represented
    def _row(w: int):
        for r in wins:
            if int(r.get("window") or -1) == w:
                return r
        return {}

    r10 = _row(10)
    r50 = _row(50)
    r100 = _row(100)
    r200 = _row(200)

    checks["D_10_frame_go_represented"] = (r10.get("post_trial_recommendation") == "GO_next_window") and (int(r10.get("frames_processed") or 0) == 10)
    checks["E_50_frame_go_represented"] = (r50.get("post_trial_recommendation") == "GO_next_window") and (int(r50.get("frames_processed") or 0) == 50)
    checks["F_100_frame_go_represented"] = (r100.get("post_trial_recommendation") == "GO_next_window") and (int(r100.get("frames_processed") or 0) == 100)
    checks["G_200_frame_go_represented"] = (r200.get("post_trial_recommendation") == "GO_next_window") and (int(r200.get("frames_processed") or 0) == 200)

    checks["H_final_recommendation_go_next_phase"] = (clo.get("final_recommendation") == "GO_next_phase")

    # I–Q boundary
    checks["I_no_ocr"] = bnd.get("ocr_invoked") is False
    checks["J_no_qwen"] = bnd.get("qwen_invoked") is False
    checks["K_no_real_tts"] = bnd.get("real_tts_invoked") is False
    checks["L_no_playback"] = bnd.get("playback_invoked") is False
    checks["M_downstream_zero"] = int(bnd.get("downstream_invocation_count") or 0) == 0
    checks["N_nav_null"] = bnd.get("navigation_action") is None
    checks["O_world_write_false"] = bnd.get("world_write_invoked") is False
    checks["P_hive_upload_false"] = bnd.get("hive_upload_invoked") is False
    checks["Q_camera_false"] = bnd.get("camera_invoked") is False

    # R trace/replay/whitebox represented (as recorded in summary)
    trw = summ.get("trw_represented") or {}
    checks["R_trw_represented"] = (trw.get("ok") is True)

    checks["S_closure_recommendation_present"] = bool(clo.get("recommended_next_phase"))
    checks["T_closed_v0_fields_present"] = (clo.get("yolo_stage1_offline_trial_status") == "closed_v0") and isinstance(clo.get("closure_assertions"), dict)

    ok = all(bool(v) for v in checks.values())
    verdict = "GO" if ok else "NO_GO"
    return ok, {"checks": checks, "verdict": verdict, "closure_status": clo.get("yolo_stage1_offline_trial_status"), "final_recommendation": clo.get("final_recommendation")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()
    out = Path(args.output_root).resolve()
    ok, rep = verify(output_root=out)
    print(json.dumps({"ok": ok, **rep}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
