#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-002
Evaluate Voice Output Governance Minimal Skeleton v0.

Offline-safe: reads sample inputs, produces decisions + trace/replay/whitebox JSONL.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now() -> float:
    return time.time()


def _read_json(path: str) -> Dict[str, Any]:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: str, obj: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: str, obj: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _build_request(req: Dict[str, Any]):
    from capabilities.voice.schemas.speech_request import SpeechRequest  # type: ignore

    return SpeechRequest(
        request_id=str(req.get("request_id") or ""),
        source_module=str(req.get("source_module") or "sample"),
        output_category=str(req.get("output_category") or "prompt"),
        text_candidate=str(req.get("text_candidate") or ""),
        priority=int(req.get("priority") or 0),
        interruptible=bool(req.get("interruptible", True)),
        dedup_allowed=bool(req.get("dedup_allowed", True)),
        cooldown_key=(str(req.get("cooldown_key")) if req.get("cooldown_key") is not None else None),
        task_context_id=(str(req.get("task_context_id")) if req.get("task_context_id") is not None else None),
        trace_id=(str(req.get("trace_id")) if req.get("trace_id") is not None else None),
        metadata=(req.get("metadata") if isinstance(req.get("metadata"), dict) else {}),
    )


def _coerce_expires_at(now: float, ctx: Dict[str, Any]) -> Optional[float]:
    if "expires_at" in ctx and ctx.get("expires_at") is not None:
        try:
            return float(ctx.get("expires_at"))
        except Exception:
            return None
    off = ctx.get("expires_at_offset_s")
    if off is None:
        return None
    try:
        return float(now) + float(off)
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-input", required=True, help="Path to sample_matrix.json")
    ap.add_argument("--output-root", required=True, help="Output directory")
    args = ap.parse_args()

    samples = _read_json(args.sample_input)
    arr = samples.get("samples") if isinstance(samples, dict) else None
    if not isinstance(arr, list):
        raise SystemExit("Invalid sample matrix: samples must be a list")

    out_root = Path(args.output_root)
    out_root.mkdir(parents=True, exist_ok=True)

    from capabilities.voice.output.voice_output_governance_v0 import (  # type: ignore
        VoiceOutputGovernanceInputV0,
        run_voice_output_governance_v0,
    )

    inputs_out: List[Dict[str, Any]] = []
    decisions_out: List[Dict[str, Any]] = []
    provider_states_out: List[Dict[str, Any]] = []
    audit_out: List[Dict[str, Any]] = []

    trace_path = str(out_root / "voice_output_trace.jsonl")
    replay_path = str(out_root / "voice_output_replay.jsonl")
    whitebox_path = str(out_root / "voice_output_whitebox.jsonl")

    # Ensure fresh JSONL for this run.
    for p in (trace_path, replay_path, whitebox_path):
        try:
            Path(p).unlink()
        except Exception:
            pass

    now0 = _now()
    for s in arr:
        if not isinstance(s, dict):
            continue
        sid = str(s.get("sample_id") or "")
        req = s.get("request") if isinstance(s.get("request"), dict) else {}
        ctx = s.get("context") if isinstance(s.get("context"), dict) else {}

        request_obj = _build_request(req)
        now = _now()
        expires_at = _coerce_expires_at(now, ctx)

        inp = VoiceOutputGovernanceInputV0(
            request=request_obj,
            now=now,
            priority_label=str(ctx.get("priority_label") or "chat"),
            expires_at=expires_at,
            stale=bool(ctx.get("stale", False)),
            cancel_requested=bool(ctx.get("cancel_requested", False)),
            interrupt_requested=bool(ctx.get("interrupt_requested", False)),
            interrupt_allowed_by_policy=bool(ctx.get("interrupt_allowed_by_policy", False)),
            current_playing_priority=(str(ctx.get("current_playing_priority")) if ctx.get("current_playing_priority") is not None else None),
            user_speaking=bool(ctx.get("user_speaking", False)),
            scene_hash=(str(ctx.get("scene_hash")) if ctx.get("scene_hash") is not None else None),
            cooldown_keys_seen=(ctx.get("cooldown_keys_seen") if isinstance(ctx.get("cooldown_keys_seen"), list) else []),
            provider_id=str(ctx.get("provider_id") or "dry_run_provider"),
            provider_status=str(ctx.get("provider_status") or "healthy"),
            dependency_ready=bool(ctx.get("dependency_ready", False)),
        )

        decision, provider_state, audit_env, trace, replay, whitebox = run_voice_output_governance_v0(inp)

        # Attach sample_id and expectation for downstream verify.
        inputs_out.append({"sample_id": sid, "request": req, "context": ctx, "expect": s.get("expect")})
        decisions_out.append({"sample_id": sid, **decision.__dict__})
        provider_states_out.append({"sample_id": sid, **provider_state.__dict__})
        audit_out.append({"sample_id": sid, **audit_env.__dict__})

        _append_jsonl(trace_path, {"sample_id": sid, **trace})
        _append_jsonl(replay_path, {"sample_id": sid, **replay})
        _append_jsonl(whitebox_path, {"sample_id": sid, **whitebox})

    # Summary
    summary = {
        "phase": "Phase-Voice-OutputGovernance-002",
        "tool": "evaluate_voice_output_governance_v0.py",
        "generated_at_s": _now(),
        "duration_ms": int((_now() - now0) * 1000),
        "sample_count": len(decisions_out),
        "outputs": {
            "voice_output_governance_summary": "voice_output_governance_summary.json",
            "voice_output_governance_inputs": "voice_output_governance_inputs.json",
            "voice_output_governance_decisions": "voice_output_governance_decisions.json",
            "voice_provider_health_states": "voice_provider_health_states.json",
            "voice_output_audit_envelopes": "voice_output_audit_envelopes.json",
            "voice_output_trace_jsonl": "voice_output_trace.jsonl",
            "voice_output_replay_jsonl": "voice_output_replay.jsonl",
            "voice_output_whitebox_jsonl": "voice_output_whitebox.jsonl"
        },
        "governance_invariants": {
            "real_tts_invoked": False,
            "playback_invoked": False,
            "provider_invoked": False,
            "navigation_action": None,
            "downstream_invocation_count": 0
        },
        "notes": [
            "Dry-run only: no provider execution, no playback.",
            "SpeechGate is invoked via can_speak() inside skeleton.",
            "guard_v1_speakable_text is provided as importable function in Phase-002."
        ],
    }

    _write_json(str(out_root / "voice_output_governance_summary.json"), summary)
    _write_json(str(out_root / "voice_output_governance_inputs.json"), inputs_out)
    _write_json(str(out_root / "voice_output_governance_decisions.json"), decisions_out)
    _write_json(str(out_root / "voice_provider_health_states.json"), provider_states_out)
    _write_json(str(out_root / "voice_output_audit_envelopes.json"), audit_out)
    (out_root / "evaluation_notes.md").write_text(
        "\n".join(
            [
                "# Phase-Voice-OutputGovernance-002 Evaluation Notes",
                "",
                f"- sample_input: `{args.sample_input}`",
                f"- output_root: `{str(out_root)}`",
                "- boundary: dry-run only (no TTS, no playback, no downstream actions)",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

