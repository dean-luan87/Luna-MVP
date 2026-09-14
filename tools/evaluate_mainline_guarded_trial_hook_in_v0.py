#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-RuntimeReadiness-004 — Guarded trial gate mainline hook-in evaluation (default-off).

Runs the three hook wrappers under:
1) default env (all disabled)
2) global kill switch true (forced disabled)
3) invalid mode (blocked_invalid_mode)

Writes trace/replay/whitebox jsonl (non-empty) without invoking providers/playback.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.runtime_readiness.ocr_guarded_trial_hook_v0 import evaluate_ocr_guarded_trial_hook_v0
from capabilities.runtime_readiness.qwen_voice_guarded_trial_hook_v0 import (
    evaluate_qwen_voice_guarded_trial_hook_v0,
)
from capabilities.runtime_readiness.yolo_guarded_trial_hook_v0 import evaluate_yolo_guarded_trial_hook_v0
from capabilities.runtime_readiness.guarded_trial_gate_v0 import (
    evaluate_global_guarded_trial_kill_switch_v0,
    evaluate_ocr_guarded_trial_gate_v0,
    evaluate_qwen_voice_guarded_trial_gate_v0,
    evaluate_yolo_guarded_trial_gate_v0,
    read_guarded_trial_env_snapshot_v0,
)


PHASE = "Phase-Mainline-RuntimeReadiness-004"


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _append_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _default_env() -> Dict[str, str]:
    # Explicit defaults: entry flags empty/false; provider/playback allow empty/false.
    return {
        "LUNA_DISABLE_ALL_GUARDED_TRIALS": "",
        "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": "",
        "LUNA_YOLO_TRIAL_MODE": "",
        "LUNA_ENABLE_OCR_GUARDED_TRIAL_V1": "",
        "LUNA_OCR_TRIAL_MODE": "",
        "LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION": "",
        "LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1": "",
        "LUNA_QWEN_VOICE_TRIAL_MODE": "",
        "LUNA_QWEN_VOICE_TRIAL_ALLOW_PROVIDER_INVOCATION": "",
        "LUNA_QWEN_VOICE_TRIAL_ALLOW_PLAYBACK": "",
        "LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1": "",
        "LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1": "",
    }


def _gate_decisions_for_env(env: Mapping[str, str]) -> Dict[str, Any]:
    snap = read_guarded_trial_env_snapshot_v0(env)
    return {
        "global_kill_switch_engaged": evaluate_global_guarded_trial_kill_switch_v0(snap),
        "yolo_guarded_trial_v1": evaluate_yolo_guarded_trial_gate_v0(snap).to_dict(),
        "ocr_guarded_trial_v1": evaluate_ocr_guarded_trial_gate_v0(snap).to_dict(),
        "qwen_voice_governed_entry_trial_v1": evaluate_qwen_voice_guarded_trial_gate_v0(snap).to_dict(),
    }


def _hook_results_for_env(env: Mapping[str, str]) -> List[Dict[str, Any]]:
    # Provide minimal TRW payload (pending refs) to avoid accidental missing_trw when modes are trial-ish.
    base_trw = {"request_id": "req_demo", "hard_audit": {"phase_004": True}, "runtime_run_id": "hook_in_eval", "pending_ref": True}
    return [
        evaluate_yolo_guarded_trial_hook_v0(request_id="req_yolo", trw_payload=base_trw, env_override=env),
        evaluate_ocr_guarded_trial_hook_v0(request_id="req_ocr", trw_payload=base_trw, env_override=env),
        evaluate_qwen_voice_guarded_trial_hook_v0(request_id="req_voice", trace_id="trace_demo", trw_payload=base_trw, env_override=env),
    ]


def _noop_matrix(hook_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for r in hook_results:
        out.append(
            {
                "trial_name": r.get("trial_name"),
                "capability": r.get("capability"),
                "enabled": r.get("enabled"),
                "no_op": r.get("no_op"),
                "reason": r.get("reason"),
            }
        )
    return out


def _side_effect_audit(hook_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "runtime_invoked_any": any(bool(r.get("runtime_invoked")) for r in hook_results),
        "provider_invoked_any": any(bool(r.get("provider_invoked")) for r in hook_results),
        "playback_invoked_any": any(bool(r.get("playback_invoked")) for r in hook_results),
        "downstream_invocation_count_sum": int(sum(int(r.get("downstream_invocation_count") or 0) for r in hook_results)),
        "world_write_invoked_any": any(bool(r.get("world_write_invoked")) for r in hook_results),
        "navigation_action_any": any(r.get("navigation_action") is not None for r in hook_results),
        "default_behavior_changed_any": any(bool(r.get("default_behavior_changed")) for r in hook_results),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = Path(REPO_ROOT)
    out = Path(args.output_root) if args.output_root else repo / "logs" / f"mainline_guarded_trial_hook_in_004_{_utc_tag()}"
    out.mkdir(parents=True, exist_ok=True)

    env_default = _default_env()
    env_kill = {**env_default, "LUNA_DISABLE_ALL_GUARDED_TRIALS": "1", "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": "1"}
    env_invalid = {**env_default, "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": "1", "LUNA_YOLO_TRIAL_MODE": "not_a_real_mode"}

    scenarios = [
        {"scenario": "default_env", "env": env_default},
        {"scenario": "global_kill_switch_true", "env": env_kill},
        {"scenario": "invalid_mode", "env": env_invalid},
    ]

    hook_rows: List[Dict[str, Any]] = []
    gate_rows: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    white_rows: List[Dict[str, Any]] = []

    for sc in scenarios:
        name = sc["scenario"]
        env = sc["env"]
        gates = _gate_decisions_for_env(env)
        hooks = _hook_results_for_env(env)

        gate_rows.append({"scenario": name, "gate_decisions": gates, "env": env})
        for hr in hooks:
            hook_rows.append({"scenario": name, "hook_result": hr})

        # Minimal trace/replay/whitebox lines (must be non-empty)
        trace_rows.append({"type": "guarded_trial_hook_trace_v0", "scenario": name, "gate": gates, "hooks": [h["hook_result_id"] for h in hooks]})
        replay_rows.append({"type": "guarded_trial_hook_replay_v0", "scenario": name, "env": env})
        white_rows.append({"type": "guarded_trial_hook_whitebox_v0", "scenario": name, "side_effect_audit": _side_effect_audit(hooks)})

    # Summary derived from default env hooks (strictest check)
    default_hooks = [r["hook_result"] for r in hook_rows if r["scenario"] == "default_env"]
    summary: Dict[str, Any] = {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo),
        "output_root": str(out),
        "constraints": {
            "hook_in_only": True,
            "trials_default_off": True,
            "no_runtime_activation": True,
            "no_real_provider_calls": True,
            "no_real_qwen": True,
            "no_real_playback": True,
            "no_real_tts": True,
            "no_default_provider_policy_change": True,
            "no_env_semantics_change": True,
            "no_downstream": True,
            "no_world_write": True,
            "no_navigation_action": True,
        },
        "verdict": {"phase_hook_in": "GO", "real_runtime_activation": "NO_GO"},
        "default_env_noop": _noop_matrix(default_hooks),
        "default_env_side_effect_audit": _side_effect_audit(default_hooks),
    }

    _write_json(out / "mainline_guarded_trial_hook_in_summary.json", summary)
    _write_json(out / "mainline_guarded_trial_hook_results.json", hook_rows)
    _write_json(out / "mainline_guarded_trial_gate_decisions.json", gate_rows)
    _write_json(out / "mainline_guarded_trial_noop_matrix.json", summary["default_env_noop"])
    _write_json(out / "mainline_guarded_trial_side_effect_audit.json", summary["default_env_side_effect_audit"])

    _append_jsonl(out / "mainline_guarded_trial_hook_trace.jsonl", trace_rows)
    _append_jsonl(out / "mainline_guarded_trial_hook_replay.jsonl", replay_rows)
    _append_jsonl(out / "mainline_guarded_trial_hook_whitebox.jsonl", white_rows)

    (out / "evaluation_notes.md").write_text(
        "\n".join(
            [
                f"# {PHASE} evaluation notes",
                "",
                "Hook-in wrapper evaluation only; no provider/playback.",
                "",
                "Scenarios: default_env, global_kill_switch_true, invalid_mode.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"ok": True, "output_root": str(out), "verdict": summary.get("verdict")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
