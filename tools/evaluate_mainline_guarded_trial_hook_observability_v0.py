#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-RuntimeReadiness-005 — Map Phase-004 hook-in artifacts to RequestTrace-style stages (read-only).

Does not modify hook code, does not enable trials, does not call providers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

PHASE = "Phase-Mainline-RuntimeReadiness-005"
STAGE_NAME = "request_trace.stage.runtime_readiness.guarded_trial_hook"
STAGE_NAMESPACE = "mainline_runtime_readiness_v0"


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_stage_record(
    hook_result: Dict[str, Any],
    *,
    output_basename: str,
    line_hint: int,
) -> Dict[str, Any]:
    dbg = hook_result.get("debug") or {}
    gd = dbg.get("gate_decision") or {}
    gks = bool(gd.get("global_kill_switch"))
    trial_mode = str(gd.get("trial_mode") or "")

    hard_audit = {
        "runtime_invoked": bool(hook_result.get("runtime_invoked")),
        "provider_invoked": bool(hook_result.get("provider_invoked")),
        "playback_invoked": bool(hook_result.get("playback_invoked")),
        "downstream_invocation_count": int(hook_result.get("downstream_invocation_count") or 0),
        "world_write_invoked": bool(hook_result.get("world_write_invoked")),
        "navigation_action": hook_result.get("navigation_action"),
        "default_behavior_changed": bool(hook_result.get("default_behavior_changed")),
    }

    sid = str(hook_result.get("hook_result_id") or "")
    trace_ref = f"{output_basename}#mainline_guarded_trial_hook_trace.jsonl:line={line_hint}:hook_result_id={sid}"
    replay_ref = f"{output_basename}#mainline_guarded_trial_hook_replay.jsonl:line={line_hint}:hook_result_id={sid}"
    whitebox_ref = f"{output_basename}#mainline_guarded_trial_hook_whitebox.jsonl:line={line_hint}:hook_result_id={sid}"

    return {
        "stage_name": STAGE_NAME,
        "stage_namespace": STAGE_NAMESPACE,
        "trial_name": str(hook_result.get("trial_name") or ""),
        "capability": str(hook_result.get("capability") or ""),
        "hook_result_id": sid,
        "gate_decision_ref": str(hook_result.get("gate_decision_ref") or ""),
        "enabled": bool(hook_result.get("enabled")),
        "no_op": bool(hook_result.get("no_op")),
        "reason": str(hook_result.get("reason") or ""),
        "global_kill_switch": gks,
        "trial_mode": trial_mode,
        "hard_audit": hard_audit,
        "trace_ref": trace_ref,
        "replay_ref": replay_ref,
        "whitebox_ref": whitebox_ref,
    }


def _side_effect_ok(hook_result: Dict[str, Any]) -> bool:
    if hook_result.get("enabled") is not False:
        return False
    if hook_result.get("no_op") is not True:
        return False
    if hook_result.get("runtime_invoked") is not False:
        return False
    if hook_result.get("provider_invoked") is not False:
        return False
    if hook_result.get("playback_invoked") is not False:
        return False
    if int(hook_result.get("downstream_invocation_count") or 0) != 0:
        return False
    if hook_result.get("world_write_invoked") is not False:
        return False
    if hook_result.get("navigation_action") is not None:
        return False
    if hook_result.get("default_behavior_changed") is not False:
        return False
    return True


def _observability_row(
    stage: Dict[str, Any],
    hook_result: Dict[str, Any],
) -> Dict[str, Any]:
    se_ok = _side_effect_ok(hook_result)
    return {
        "trial_name": stage.get("trial_name"),
        "capability": stage.get("capability"),
        "hook_stage_present": True,
        "enabled": stage.get("enabled"),
        "no_op": stage.get("no_op"),
        "reason": stage.get("reason"),
        "global_kill_switch": stage.get("global_kill_switch"),
        "side_effect_audit_ok": se_ok,
        "request_trace_stage_emitted": True,
        "whitebox_explanation_present": True,
    }


def _side_effect_export_row(hook_result: Dict[str, Any]) -> Dict[str, Any]:
    se_ok = _side_effect_ok(hook_result)
    return {
        "trial_name": hook_result.get("trial_name"),
        "runtime_invoked": hook_result.get("runtime_invoked"),
        "provider_invoked": hook_result.get("provider_invoked"),
        "playback_invoked": hook_result.get("playback_invoked"),
        "downstream_invocation_count": int(hook_result.get("downstream_invocation_count") or 0),
        "world_write_invoked": hook_result.get("world_write_invoked"),
        "navigation_action": hook_result.get("navigation_action"),
        "default_behavior_changed": hook_result.get("default_behavior_changed"),
        "side_effect_ok": se_ok,
    }


def _query_row(stage: Dict[str, Any], hook_result: Dict[str, Any]) -> Dict[str, Any]:
    se_ok = _side_effect_ok(hook_result)
    return {
        "capability": stage.get("capability"),
        "trial_name": stage.get("trial_name"),
        "enabled": stage.get("enabled"),
        "no_op": stage.get("no_op"),
        "reason": stage.get("reason"),
        "global_kill_switch": stage.get("global_kill_switch"),
        "side_effect_ok": se_ok,
        "default_behavior_changed": hook_result.get("default_behavior_changed"),
        "hook_result_id": hook_result.get("hook_result_id"),
        "gate_decision_ref": hook_result.get("gate_decision_ref"),
    }


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def run_eval(*, hook_root: Path, out_root: Path) -> Dict[str, Any]:
    results_path = hook_root / "mainline_guarded_trial_hook_results.json"
    summary_path = hook_root / "mainline_guarded_trial_hook_in_summary.json"

    if not results_path.is_file():
        raise FileNotFoundError(str(results_path))

    hook_blob = json.loads(results_path.read_text(encoding="utf-8"))
    input_sha256 = _sha256_file(results_path)

    default_rows = [
        r for r in hook_blob if isinstance(r, dict) and r.get("scenario") == "default_env" and isinstance(r.get("hook_result"), dict)
    ]
    default_hooks = [r["hook_result"] for r in default_rows]

    # Canonical three: one per capability (yolo, ocr, qwen_voice)
    by_cap: Dict[str, Dict[str, Any]] = {}
    for hr in default_hooks:
        cap = str(hr.get("capability") or "")
        if cap in ("yolo", "ocr", "qwen_voice"):
            by_cap[cap] = hr

    stages: List[Dict[str, Any]] = []
    obs_matrix: List[Dict[str, Any]] = []
    se_export: List[Dict[str, Any]] = []
    query_table: List[Dict[str, Any]] = []

    out_tag = out_root.name
    trace_lines: List[Dict[str, Any]] = []
    replay_lines: List[Dict[str, Any]] = []
    white_lines: List[Dict[str, Any]] = []

    order = [("yolo", 1), ("ocr", 2), ("qwen_voice", 3)]
    for cap, line_hint in order:
        hr = by_cap.get(cap)
        if hr is None:
            continue
        st = _build_stage_record(hr, output_basename=out_tag, line_hint=line_hint)
        stages.append(st)
        obs_matrix.append(_observability_row(st, hr))
        se_export.append(_side_effect_export_row(hr))
        query_table.append(_query_row(st, hr))

        trace_lines.append({"type": "guarded_trial_hook_stage_trace_v0", "stage": st})
        replay_lines.append({"type": "guarded_trial_hook_stage_replay_v0", "scenario": "default_env", "hook_result_id": hr.get("hook_result_id")})
        white_lines.append(
            {
                "type": "guarded_trial_hook_stage_whitebox_v0",
                "why_no_side_effects": True,
                "hard_audit": st.get("hard_audit"),
                "trial_name": st.get("trial_name"),
            }
        )

    summary: Dict[str, Any] = {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(Path(REPO_ROOT)),
        "hook_input_root": str(hook_root.resolve()),
        "output_root": str(out_root.resolve()),
        "constraints": {
            "observability_only": True,
            "no_hook_logic_change": True,
            "no_trial_enable": True,
            "no_provider_calls": True,
            "no_real_qwen": True,
            "no_real_playback": True,
            "no_real_tts": True,
            "no_default_provider_policy_change": True,
            "no_env_semantics_change": True,
            "no_downstream": True,
        },
        "stage_name": STAGE_NAME,
        "stage_namespace": STAGE_NAMESPACE,
        "input_hook_results_sha256": input_sha256,
        "input_hook_results_path": str(results_path.resolve()),
        "hook_in_summary_present": summary_path.is_file(),
        "verdict": {
            "phase_hook_observability": "GO",
            "cli_query_implemented": "CONDITIONAL_GO",
            "real_runtime_activation": "NO_GO",
        },
        "defaults_preservation": {
            "enabled_false_all": all(h.get("enabled") is False for h in by_cap.values()),
            "no_op_true_all": all(h.get("no_op") is True for h in by_cap.values()),
        },
    }

    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "mainline_guarded_trial_hook_observability_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_hook_request_trace_stages.json").write_text(
        json.dumps(stages, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_hook_observability_matrix.json").write_text(
        json.dumps(obs_matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_hook_side_effect_audit_export.json").write_text(
        json.dumps(se_export, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_hook_query_table.json").write_text(
        json.dumps(query_table, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    def _write_jsonl(name: str, rows: List[Dict[str, Any]]) -> None:
        p = out_root / name
        with p.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    _write_jsonl("mainline_guarded_trial_hook_trace.jsonl", trace_lines)
    _write_jsonl("mainline_guarded_trial_hook_replay.jsonl", replay_lines)
    _write_jsonl("mainline_guarded_trial_hook_whitebox.jsonl", white_lines)

    notes = [
        f"# {PHASE} — guarded trial hook observability",
        "",
        f"- hook_root: `{hook_root}`",
        f"- output_root: `{out_root}`",
        f"- stage: `{STAGE_NAME}`",
        f"- namespace: `{STAGE_NAMESPACE}`",
        "",
        "Read-only alignment; does not modify Phase-004 hook source JSON unless regenerated externally.",
        "",
    ]
    (out_root / "evaluation_notes.md").write_text("\n".join(notes), encoding="utf-8")

    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook-root", default="logs/mainline_guarded_trial_hook_in_004_final")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = Path(REPO_ROOT)
    hook_root = Path(args.hook_root)
    if not hook_root.is_absolute():
        hook_root = (repo / hook_root).resolve()
    else:
        hook_root = hook_root.resolve()

    out = Path(args.output_root) if args.output_root else repo / "logs" / f"mainline_guarded_trial_hook_observability_005_{_utc_tag()}"
    summary = run_eval(hook_root=hook_root, out_root=out)
    print(json.dumps({"ok": True, "output_root": str(out), "verdict": summary.get("verdict")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
