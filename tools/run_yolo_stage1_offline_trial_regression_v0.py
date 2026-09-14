#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Mainline-GuardedTrial-007 — YOLO Stage-1 Offline Trial Regression & Closure v0.

Read-only aggregator:
- Aggregates Phase-005-Fix (10-frame) + Phase-006-Rerun (50/100/200) outputs.
- Preserves historical initial NO_GO / CONDITIONAL_GO as optional references.
- Produces closure artifacts and a closed_v0 recommendation.

Scope guard:
- Offline file video only.
- YOLO Stage-1 only.
- Must NOT enter OCR / MidPlatform / downstream / navigation / TTS / Qwen / world write / hive upload.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


PHASE = "Phase-Mainline-GuardedTrial-007"


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_md(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _nj(p: Path) -> bool:
    return p.is_file() and bool(p.read_text(encoding="utf-8").strip())


@dataclass
class RootRef:
    label: str
    root: Optional[Path]


def _try_root(s: str) -> Optional[Path]:
    if not s.strip():
        return None
    p = Path(s).expanduser()
    return p.resolve() if p.is_absolute() else (Path.cwd() / p).resolve()


def _summarize_fix10(root: Path) -> Tuple[Dict[str, Any], List[str]]:
    hard: List[str] = []
    summ_p = root / "yolo_stage1_10_frame_dry_run_summary.json"
    if not summ_p.is_file():
        return {"root": str(root), "present": False}, ["missing_fix10_summary"]
    summ = _load_json(summ_p)
    rec = summ.get("post_trial_recommendation")
    # Prefer verifier semantics: GO iff recommendation GO_next_window and frames_processed==10 and abort_triggered==False.
    fp = int(summ.get("frames_processed") or 0)
    abort = bool(summ.get("abort_triggered"))
    fix10_go = (rec == "GO_next_window") and (fp == 10) and (abort is False)
    if not fix10_go:
        hard.append("fix10_not_go")
    ha = summ.get("hard_audit") or {}
    return {
        "root": str(root),
        "present": True,
        "phase": summ.get("phase"),
        "trial_id": summ.get("trial_id"),
        "frames_processed": fp,
        "schema_invalid_count": int(summ.get("schema_invalid_count") or 0),
        "detector_invoked": bool(summ.get("detector_invoked")),
        "abort_triggered": abort,
        "post_trial_recommendation": rec,
        "video_stream_type": summ.get("video_stream_type"),
        "input_video": summ.get("input_video") or summ.get("input_video_path") or summ.get("input_video_resolved"),
        "hard_audit": ha,
        "go": fix10_go,
    }, hard


def _summarize_mw006(root: Path) -> Tuple[Dict[str, Any], Dict[int, Any], List[str]]:
    hard: List[str] = []
    summ_p = root / "yolo_stage1_multi_window_summary.json"
    if not summ_p.is_file():
        return {"root": str(root), "present": False}, {}, ["missing_multi_window_summary"]
    summ = _load_json(summ_p)
    wre = list(summ.get("windows_executed") or [])
    fr = summ.get("final_recommendation")
    phase_go = (summ.get("trial_phase_verdict") == "GO") or (fr == "GO_next_phase")
    if not phase_go:
        hard.append("multi_window_not_go")

    reports: Dict[int, Any] = {}
    for w in (50, 100, 200):
        rp = root / f"yolo_stage1_window_{w}_report.json"
        if rp.is_file():
            try:
                reports[w] = _load_json(rp)
            except Exception:
                reports[w] = {"error": "unparseable"}
        else:
            reports[w] = {"executed": False}

    # window-level hard checks: must be executed and GO_next_window
    for w in (50, 100, 200):
        r = reports.get(w) or {}
        fp = int(r.get("frames_processed") or 0)
        wf = int(r.get("window_frames") or w)
        rec = r.get("post_trial_recommendation")
        if fp != wf:
            hard.append(f"window_frames_not_full:{w}")
        if rec != "GO_next_window":
            hard.append(f"window_not_go_next_window:{w}")

    return {
        "root": str(root),
        "present": True,
        "phase": summ.get("phase"),
        "multi_window_trial_id": summ.get("multi_window_trial_id"),
        "windows_requested": list(summ.get("windows_requested") or []),
        "windows_executed": wre,
        "windows_skipped": list(summ.get("windows_skipped") or []),
        "final_recommendation": fr,
        "stop_reason": summ.get("stop_reason"),
        "side_effect_detected": summ.get("side_effect_detected"),
        "all_hard_audit_ok": summ.get("all_hard_audit_ok"),
        "go": phase_go and not hard,
    }, reports, hard


def _merge_boundary(*, fix10: Dict[str, Any], mw_reports: Dict[int, Any]) -> Dict[str, Any]:
    # Take hard_audit from fix10 summary + each window hard_audit, AND them.
    def _and_bool(vals: List[Optional[bool]]) -> bool:
        # treat None as False for safety
        return all(v is True or v is False and False for v in vals)  # never used

    # explicit fields required by phase doc
    out = {
        "camera_invoked": False,
        "ocr_invoked": False,
        "qwen_invoked": False,
        "real_tts_invoked": False,
        "playback_invoked": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "world_write_invoked": False,
        "hive_upload_invoked": False,
        "online_runtime_connected": False,
    }

    def _acc(ha: Dict[str, Any]) -> None:
        if not isinstance(ha, dict):
            return
        out["camera_invoked"] = out["camera_invoked"] or (ha.get("camera_invoked") is True)
        out["ocr_invoked"] = out["ocr_invoked"] or (ha.get("ocr_invoked") is True)
        out["qwen_invoked"] = out["qwen_invoked"] or (ha.get("qwen_invoked") is True)
        out["real_tts_invoked"] = out["real_tts_invoked"] or (ha.get("real_tts_invoked") is True)
        out["playback_invoked"] = out["playback_invoked"] or (ha.get("playback_invoked") is True)
        out["downstream_invocation_count"] = max(int(out["downstream_invocation_count"] or 0), int(ha.get("downstream_invocation_count") or 0))
        if ha.get("navigation_action") is not None:
            out["navigation_action"] = ha.get("navigation_action")
        out["world_write_invoked"] = out["world_write_invoked"] or (ha.get("world_write_invoked") is True)
        out["hive_upload_invoked"] = out["hive_upload_invoked"] or (ha.get("hive_upload_invoked") is True)

    _acc(fix10.get("hard_audit") or {})
    for w in (50, 100, 200):
        _acc((mw_reports.get(w) or {}).get("hard_audit") or {})

    return out


def _trw_represented(*, fix10_root: Path, mw_root: Path) -> Dict[str, Any]:
    # represent: trace/replay/whitebox nonempty
    fix_ok = (
        _nj(fix10_root / "yolo_stage1_10_frame_trace.jsonl")
        and _nj(fix10_root / "yolo_stage1_10_frame_replay.jsonl")
        and _nj(fix10_root / "yolo_stage1_10_frame_whitebox.jsonl")
    )
    mw_ok = (
        _nj(mw_root / "yolo_stage1_multi_window_trace.jsonl")
        and _nj(mw_root / "yolo_stage1_multi_window_replay.jsonl")
        and _nj(mw_root / "yolo_stage1_multi_window_whitebox.jsonl")
    )
    return {"fix10_trw_nonempty": fix_ok, "mw_trw_nonempty": mw_ok, "ok": fix_ok and mw_ok}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix-10-root", required=True)
    ap.add_argument("--multi-window-root", required=True)
    ap.add_argument("--output-root", default="")
    ap.add_argument("--initial-005-root", default="")
    ap.add_argument("--initial-006-root", default="")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[1]

    fix10 = _try_root(args.fix_10_root)
    mw = _try_root(args.multi_window_root)
    if fix10 is None or mw is None:
        print(json.dumps({"ok": False, "error": "missing_required_roots"}, ensure_ascii=False))
        return 2

    out = Path(args.output_root).expanduser() if args.output_root.strip() else (repo / "logs" / f"yolo_stage1_offline_trial_regression_007_{_utc_tag()}")
    out = out.resolve() if out.is_absolute() else (repo / out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    # Optional historical roots (best-effort)
    init005 = _try_root(args.initial_005_root)
    init006 = _try_root(args.initial_006_root)

    soft: List[str] = []
    if init005 and not init005.is_dir():
        soft.append("missing_initial_005_root")
        init005 = None
    if init006 and not init006.is_dir():
        soft.append("missing_initial_006_root")
        init006 = None

    hard: List[str] = []

    fix10_sum, fix10_hard = _summarize_fix10(fix10)
    mw_sum, mw_reports, mw_hard = _summarize_mw006(mw)
    hard.extend(fix10_hard)
    hard.extend(mw_hard)

    # Boundary summary
    boundary = _merge_boundary(fix10=fix10_sum, mw_reports=mw_reports)

    # Hard audit expectations
    hard_audit_ok = (
        boundary.get("camera_invoked") is False
        and boundary.get("ocr_invoked") is False
        and boundary.get("qwen_invoked") is False
        and boundary.get("real_tts_invoked") is False
        and boundary.get("playback_invoked") is False
        and int(boundary.get("downstream_invocation_count") or 0) == 0
        and boundary.get("navigation_action") is None
        and boundary.get("world_write_invoked") is False
        and boundary.get("hive_upload_invoked") is False
        and boundary.get("online_runtime_connected") is False
    )
    if not hard_audit_ok:
        hard.append("boundary_violation_detected")

    trw = _trw_represented(fix10_root=fix10, mw_root=mw)
    if not trw.get("ok"):
        hard.append("trw_not_represented")

    # Phase matrix
    phase_matrix = {
        "phase_005_initial": {"root": str(init005) if init005 else None, "note": "historical_reference_only"},
        "phase_005_fix": fix10_sum,
        "phase_006_initial": {"root": str(init006) if init006 else None, "note": "historical_reference_only"},
        "phase_006_rerun": mw_sum,
    }

    # Window matrix (10 from fix, 50/100/200 from rerun)
    window_rows: List[Dict[str, Any]] = []
    window_rows.append(
        {
            "window": 10,
            "source_phase": "005_fix",
            "frames_processed": fix10_sum.get("frames_processed"),
            "detector_invoked": fix10_sum.get("detector_invoked"),
            "schema_invalid_count": fix10_sum.get("schema_invalid_count"),
            "abort_triggered": fix10_sum.get("abort_triggered"),
            "post_trial_recommendation": fix10_sum.get("post_trial_recommendation"),
            "side_effect_ok": hard_audit_ok,
        }
    )
    for w in (50, 100, 200):
        r = mw_reports.get(w) or {}
        window_rows.append(
            {
                "window": w,
                "source_phase": "006_rerun",
                "frames_processed": r.get("frames_processed"),
                "detector_invoked": r.get("detector_invoked"),
                "schema_invalid_count": r.get("schema_invalid_count"),
                "abort_triggered": r.get("abort_triggered"),
                "post_trial_recommendation": r.get("post_trial_recommendation"),
                "side_effect_ok": hard_audit_ok,
            }
        )

    # Closure
    can_close = (not hard) and (fix10_sum.get("go") is True) and (mw_sum.get("final_recommendation") == "GO_next_phase")
    closure_status = "closed_v0" if can_close else "open"
    final = "GO" if can_close else ("CONDITIONAL_GO" if (not hard and soft) else "NO_GO")

    closure = {
        "phase": PHASE,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "yolo_stage1_offline_trial_status": closure_status,
        "scope": "offline_video_yolo_only_guarded_trial",
        "closure_inputs": {
            "fix_10_root": str(fix10),
            "multi_window_root": str(mw),
            "initial_005_root": str(init005) if init005 else None,
            "initial_006_root": str(init006) if init006 else None,
        },
        "closure_assertions": {
            "real_camera_runtime_allowed": False,
            "ocr_activation_allowed": False,
            "midplatform_activation_allowed": False,
            "navigation_allowed": False,
            "real_tts_allowed": False,
            "qwen_allowed": False,
            "world_write_allowed": False,
            "hive_upload_allowed": False,
        },
        "final_recommendation": "GO_next_phase" if can_close else "DO_NOT_ADVANCE",
        "recommended_next_phase": "OCR Stage-2 definition/precheck" if can_close else "Continue YOLO Stage-1 fixes",
        "decision": {
            "verdict": final,
            "hard_blockers": hard,
            "soft_followups": soft,
        },
    }

    summary = {
        "tool": "run_yolo_stage1_offline_trial_regression_v0",
        "phase": PHASE,
        "ok": True,
        "verdict": final,
        "hard_blockers": hard,
        "soft_followups": soft,
        "fix_10_go": bool(fix10_sum.get("go")),
        "multi_window_final_recommendation": mw_sum.get("final_recommendation"),
        "multi_window_windows_executed": mw_sum.get("windows_executed"),
        "boundary_clean": hard_audit_ok,
        "trw_represented": trw,
        "closure_status": closure_status,
        "output_root": str(out),
    }

    _write_json(out / "yolo_stage1_offline_trial_regression_summary.json", summary)
    _write_json(out / "yolo_stage1_offline_trial_phase_matrix.json", phase_matrix)
    _write_json(out / "yolo_stage1_offline_trial_window_matrix.json", {"rows": window_rows})
    _write_json(out / "yolo_stage1_offline_trial_boundary_summary.json", boundary)
    _write_json(out / "yolo_stage1_offline_trial_hard_audit_summary.json", {"boundary_clean": hard_audit_ok, "boundary": boundary})
    _write_json(out / "yolo_stage1_offline_trial_closure_recommendation.json", closure)

    _write_md(
        out / "regression_notes.md",
        "\n".join(
            [
                f"# {PHASE} — YOLO Stage-1 Offline Trial Regression & Closure v0",
                "",
                "## Scope",
                "- YOLO Stage-1 only (offline video file).",
                "- No OCR / MidPlatform / downstream / navigation / TTS / Qwen / world write / hive upload.",
                "",
                "## Inputs",
                f"- fix-10-root: `{fix10}`",
                f"- multi-window-root: `{mw}`",
                f"- initial-005-root: `{init005}`" if init005 else "- initial-005-root: (missing / not provided)",
                f"- initial-006-root: `{init006}`" if init006 else "- initial-006-root: (missing / not provided)",
                "",
                "## Verdict",
                f"- verdict: **{final}**",
                f"- closure_status: **{closure_status}**",
                f"- recommended_next_phase: **{closure['recommended_next_phase']}**",
                "",
                "## Blockers",
                f"- hard_blockers: `{hard}`",
                f"- soft_followups: `{soft}`",
                "",
            ]
        ),
    )

    print(json.dumps({"ok": True, "output_root": str(out), "verdict": final, "closure_status": closure_status}, ensure_ascii=False))
    return 0 if final == "GO" else (3 if final == "CONDITIONAL_GO" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
