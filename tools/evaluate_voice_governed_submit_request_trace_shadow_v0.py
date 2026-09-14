# -*- coding: utf-8 -*-
"""
Phase-Voice-OutputGovernance-008
Integrate governed submit shadow gate into Voice RequestTrace shadow chains (parallel observation).

Reads Phase-007 submit shadow decisions and Phase-005 voice request chains; produces enhanced
chains without modifying source files on disk.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

GOVERNED_SUBMIT_STAGE_FULL = "request_trace.stage.output.voice.governed_submit_shadow_gate"
GOVERNED_SUBMIT_STAGE_SHORT = "governed_submit_shadow_gate"

GATE_ORDER = (
    "_maybe_submit_real_output_v1_pre",
    "VoiceOutputPlane.submit_entry",
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _max_stage_order(stages: List[Dict[str, Any]]) -> int:
    m = -1
    for st in stages:
        if not isinstance(st, dict):
            continue
        kf = st.get("key_fields")
        if isinstance(kf, dict) and isinstance(kf.get("stage_order"), int):
            m = max(m, kf["stage_order"])
    return m


def _group_decisions_by_request(decisions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    out: Dict[str, List[Dict[str, Any]]] = {}
    for d in decisions:
        if not isinstance(d, dict):
            continue
        rid = d.get("request_id")
        if isinstance(rid, str) and rid:
            out.setdefault(rid, []).append(d)
    return out


def _sort_decisions_for_chain(ds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pos_rank = {p: i for i, p in enumerate(GATE_ORDER)}

    def key(d: Dict[str, Any]) -> Tuple[int, str]:
        gp = d.get("submit_gate_position")
        s = str(gp) if gp is not None else ""
        return (pos_rank.get(s, 99), s)

    return sorted(ds, key=key)


def _whitebox_for_submit_shadow(d: Dict[str, Any]) -> Dict[str, Any]:
    result = str(d.get("submit_shadow_result") or "")
    allowed = bool(d.get("submit_allowed"))
    reason = d.get("submit_block_reason")
    gp = d.get("submit_gate_position")

    wb: Dict[str, Any] = {
        "why_submit_allowed_shadow": result == "submit_allowed_shadow" and allowed,
        "why_submit_blocked_shadow": result == "submit_blocked_shadow",
        "why_submit_expired_shadow": result == "submit_expired_shadow",
        "why_submit_cancelled_shadow": result == "submit_cancelled_shadow",
        "why_submit_fallback_candidate_shadow": result == "submit_fallback_candidate_shadow",
        "why_no_real_submit_invoked": True,
        "why_gate_position_safe": (
            "Shadow-only gate evaluation at "
            f"{gp}; no real submit wiring invoked; hard_audit.real_submit_invoked=false."
        ),
        "submit_gate_position": gp,
        "submit_shadow_result": result,
        "submit_block_reason": reason,
        "phase": "Phase-Voice-OutputGovernance-008",
    }
    return wb


def _build_submit_gate_stage_record(
    d: Dict[str, Any],
    *,
    stage_order: int,
) -> Dict[str, Any]:
    ha = d.get("hard_audit")
    if not isinstance(ha, dict):
        ha = {
            "real_submit_invoked": False,
            "real_tts_invoked": False,
            "playback_invoked": False,
            "provider_invoked": False,
            "navigation_action": None,
            "downstream_invocation_count": 0,
        }

    status = "ok" if d.get("submit_allowed") else "fail"
    key_fields: Dict[str, Any] = {
        "stage_namespace": "voice_output_governance_v0",
        "stage_name": GOVERNED_SUBMIT_STAGE_SHORT,
        "stage_order": stage_order,
        "stage_name_full": GOVERNED_SUBMIT_STAGE_FULL,
        "source_submit_shadow_decision_id": d.get("submit_shadow_decision_id"),
        "source_governance_decision_id": d.get("source_governance_decision_id"),
        "submit_gate_position": d.get("submit_gate_position"),
        "submit_shadow_result": d.get("submit_shadow_result"),
        "submit_allowed": d.get("submit_allowed"),
        "submit_block_reason": d.get("submit_block_reason"),
        "hard_audit": ha,
        "whitebox_extension": _whitebox_for_submit_shadow(d),
    }

    return {
        "stage_name": GOVERNED_SUBMIT_STAGE_FULL,
        "status": status,
        "timestamp": None,
        "key_fields": key_fields,
        "source_observation_type": "VoiceGovernedSubmitShadowGateV0",
        "source_ref": d.get("trace_ref") or d.get("replay_ref"),
    }


def run_integration(
    submit_shadow_root: Path,
    voice_request_trace_root: Path,
) -> Dict[str, Any]:
    dec_path = submit_shadow_root / "voice_governed_submit_shadow_decisions.json"
    chains_path = voice_request_trace_root / "voice_output_request_chains.json"

    if not dec_path.exists():
        raise FileNotFoundError(f"missing: {dec_path}")
    if not chains_path.exists():
        raise FileNotFoundError(f"missing: {chains_path}")

    decisions = _read_json(dec_path)
    if not isinstance(decisions, list):
        raise ValueError("voice_governed_submit_shadow_decisions.json must be a list")

    raw_chains = _read_json(chains_path)
    if not isinstance(raw_chains, list):
        raise ValueError("voice_output_request_chains.json must be a list")

    # Deep copy — do not mutate Phase-005 source when writing enhanced only to output_root
    chains = copy.deepcopy(raw_chains)

    by_rid = _group_decisions_by_request(decisions)
    chain_request_ids = {
        c.get("request_id") for c in chains if isinstance(c, dict) and isinstance(c.get("request_id"), str)
    }

    matched_count = 0
    unmatched_submit: List[Dict[str, Any]] = []

    for rid, ds in by_rid.items():
        if rid not in chain_request_ids:
            for d in ds:
                unmatched_submit.append(
                    {
                        "request_id": rid,
                        "submit_shadow_decision_id": d.get("submit_shadow_decision_id"),
                        "reason": "no_matching_voice_request_chain",
                    }
                )
            continue

        matched_count += 1

    enhanced: List[Dict[str, Any]] = []
    for ch in chains:
        if not isinstance(ch, dict):
            enhanced.append(ch)
            continue
        rid = ch.get("request_id")
        if not isinstance(rid, str) or rid not in by_rid:
            enhanced.append(ch)
            continue

        stages = ch.get("stages")
        if not isinstance(stages, list):
            enhanced.append(ch)
            continue

        base_order = _max_stage_order(stages)
        sorted_ds = _sort_decisions_for_chain(by_rid[rid])

        for i, d in enumerate(sorted_ds):
            if not isinstance(d, dict):
                continue
            stages.append(_build_submit_gate_stage_record(d, stage_order=base_order + 1 + i))

        ch.setdefault("enhancement_metadata", {})
        em = ch["enhancement_metadata"]
        if isinstance(em, dict):
            em["governed_submit_shadow_gate_appended"] = True
            em["appended_stage_count"] = len(sorted_ds)

        enhanced.append(ch)

    # Gate position matrix
    matrix: List[Dict[str, Any]] = []
    for d in decisions:
        if not isinstance(d, dict):
            continue
        ha = d.get("hard_audit") if isinstance(d.get("hard_audit"), dict) else {}
        ok = (
            ha.get("real_submit_invoked") in (False, None)
            and ha.get("real_tts_invoked") is False
            and ha.get("playback_invoked") is False
            and ha.get("provider_invoked") is False
            and ha.get("navigation_action") in (None, "")
            and ha.get("downstream_invocation_count") in (0, None)
        )
        matrix.append(
            {
                "request_id": d.get("request_id"),
                "gate_position": d.get("submit_gate_position"),
                "submit_shadow_result": d.get("submit_shadow_result"),
                "submit_allowed": d.get("submit_allowed"),
                "hard_audit_ok": ok,
            }
        )

    # Hard audit summary
    ha_summary = {
        "total_submit_decisions": len(decisions),
        "hard_audit_all_ok_sample": all(m.get("hard_audit_ok") for m in matrix) if matrix else True,
        "invariants": {
            "real_submit_invoked": False,
            "real_tts_invoked": False,
            "playback_invoked": False,
            "provider_invoked": False,
            "navigation_action": None,
            "downstream_invocation_count": 0,
        },
    }

    stage_mapping = {
        "phase": "Phase-Voice-OutputGovernance-008",
        "new_stage_full_name": GOVERNED_SUBMIT_STAGE_FULL,
        "stage_namespace": "voice_output_governance_v0",
        "join_key_primary": "request_id",
        "join_key_secondary": ["source_governance_decision_id", "source_audit_envelope_id"],
        "parallel_observation": True,
        "notes": [
            "Original Phase-005 stages preserved; new stages appended.",
            "Two gate positions per request_id when Phase-007 emitted both.",
        ],
    }

    # Flatten JSONL rows for trace/replay/whitebox (same payload, stream_kind differs)
    flat_rows: List[Dict[str, Any]] = []
    for ch in enhanced:
        if not isinstance(ch, dict):
            continue
        rid = ch.get("request_id")
        stlist = ch.get("stages") if isinstance(ch.get("stages"), list) else []
        for st in stlist:
            if not isinstance(st, dict):
                continue
            if st.get("stage_name") != GOVERNED_SUBMIT_STAGE_FULL:
                continue
            kf = st.get("key_fields") if isinstance(st.get("key_fields"), dict) else {}
            flat_rows.append(
                {
                    "request_id": rid,
                    "stage_name": GOVERNED_SUBMIT_STAGE_FULL,
                    "key_fields": kf,
                    "shadow_only": True,
                }
            )

    return {
        "enhanced_chains": enhanced,
        "voice_governed_submit_stage_mapping": stage_mapping,
        "voice_governed_submit_gate_position_matrix": matrix,
        "voice_governed_submit_hard_audit_summary": ha_summary,
        "flat_submit_gate_rows": flat_rows,
        "stats": {
            "submit_decision_count": len(decisions),
            "voice_chain_count": len(chains),
            "join_matched_request_count": matched_count,
            "unmatched_submit_decisions": unmatched_submit,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--submit-shadow-root", required=True)
    ap.add_argument("--voice-request-trace-root", required=True)
    ap.add_argument("--output-root", default=None)
    args = ap.parse_args()

    submit_root = Path(args.submit_shadow_root)
    voice_root = Path(args.voice_request_trace_root)

    out_root = Path(args.output_root) if args.output_root else (
        Path.cwd() / "logs" / f"voice_governed_submit_request_trace_008_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    if not out_root.is_absolute():
        out_root = Path.cwd() / out_root
    out_root.mkdir(parents=True, exist_ok=True)

    result = run_integration(submit_root, voice_root)
    enhanced = result["enhanced_chains"]
    stats = result["stats"]
    flat = result["flat_submit_gate_rows"]

    summary = {
        "phase": "Phase-Voice-OutputGovernance-008",
        "tool": "evaluate_voice_governed_submit_request_trace_shadow_v0.py",
        "mode": "governed_submit_request_trace_shadow_integration",
        "inputs": {
            "submit_shadow_root": str(submit_root),
            "voice_request_trace_root": str(voice_root),
        },
        "outputs": {
            "enhanced_chain_count": len(enhanced),
            "submit_decision_count": stats.get("submit_decision_count"),
            "join_matched_request_count": stats.get("join_matched_request_count"),
            "unmatched_submit_decision_count": len(stats.get("unmatched_submit_decisions") or []),
            "appended_submit_gate_stage_rows": len(flat),
        },
        "stats": stats,
        "hard_audit_invariants": {
            "real_submit_invoked": False,
            "real_tts_invoked": False,
            "playback_invoked": False,
            "provider_invoked": False,
            "navigation_action": None,
            "downstream_invocation_count": 0,
        },
        "env_snapshot": {"pwd": os.getcwd()},
        "notes": [
            "Does not modify Phase-005 files on disk; enhanced chains written only to output_root.",
            "Shadow-only; no real submit.",
        ],
    }

    _write_json(out_root / "voice_governed_submit_request_trace_summary.json", summary)
    _write_json(out_root / "voice_governed_submit_enhanced_request_chains.json", enhanced)
    _write_json(out_root / "voice_governed_submit_stage_mapping.json", result["voice_governed_submit_stage_mapping"])
    _write_json(out_root / "voice_governed_submit_gate_position_matrix.json", result["voice_governed_submit_gate_position_matrix"])
    _write_json(out_root / "voice_governed_submit_hard_audit_summary.json", result["voice_governed_submit_hard_audit_summary"])

    trace_rows = [{**r, "stream_kind": "trace"} for r in flat]
    replay_rows = [{**r, "stream_kind": "replay"} for r in flat]
    whitebox_rows = [{**r, "stream_kind": "whitebox"} for r in flat]
    _write_jsonl(out_root / "voice_governed_submit_request_trace_trace.jsonl", trace_rows)
    _write_jsonl(out_root / "voice_governed_submit_request_trace_replay.jsonl", replay_rows)
    _write_jsonl(out_root / "voice_governed_submit_request_trace_whitebox.jsonl", whitebox_rows)

    (out_root / "evaluation_notes.md").write_text(
        "# Voice Governed Submit RequestTrace Integration (v0)\n\n"
        "- Shadow-only parallel stage `request_trace.stage.output.voice.governed_submit_shadow_gate`.\n"
        "- Original Phase-005 chains are copied and appended to in-memory; source files unchanged.\n",
        encoding="utf-8",
    )

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
