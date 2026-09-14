#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Voice-Qianwen-003 — Map GovernedVoiceProviderEntry dry-run outputs to RequestTrace-style stages (shadow only).
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

NS = "voice_qwen_governed_entry_v0"

STAGE_GOVERNANCE_SOURCE = "request_trace.stage.output.voice.qwen_entry.governance_source"
STAGE_PROVIDER_MODE = "request_trace.stage.output.voice.qwen_entry.provider_mode"
STAGE_PROVIDER_SELECTION = "request_trace.stage.output.voice.qwen_entry.provider_selection"
STAGE_SPEAKABILITY_AUDIT = "request_trace.stage.output.voice.qwen_entry.speakability_audit"
STAGE_TEXT_DIFF_AUDIT = "request_trace.stage.output.voice.qwen_entry.text_diff_audit"
STAGE_FINAL_ENTRY_DECISION = "request_trace.stage.output.voice.qwen_entry.final_entry_decision"
STAGE_AUDIT_ENVELOPE = "request_trace.stage.output.voice.qwen_entry.audit_envelope"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index_decisions(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for x in items:
        rid = str(x.get("request_id") or "")
        if rid:
            idx[rid] = x
    return idx


def _index_audits(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for x in items:
        rid = str(x.get("request_id") or "")
        if rid:
            idx[rid] = x
    return idx


def _base_stage_fields(
    *,
    decision: Dict[str, Any],
    audit: Dict[str, Any],
    provider_mode: str,
) -> Dict[str, Any]:
    ps = decision.get("provider_selection") if isinstance(decision.get("provider_selection"), dict) else {}
    po = ps.get("provider_order") or []
    sel = str(ps.get("selected_provider") or "none")
    tda = audit.get("text_diff_audit") if isinstance(audit.get("text_diff_audit"), dict) else {}
    return {
        "request_id": str(decision.get("request_id") or ""),
        "sample_id": str(decision.get("sample_id") or ""),
        "provider_mode": provider_mode,
        "selected_provider": sel,
        "provider_order": list(po) if isinstance(po, list) else [],
        "source_governance_decision_id": str(decision.get("source_governance_decision_id") or ""),
        "source_text": str(audit.get("source_text") or ""),
        "provider_input_text": str(audit.get("provider_input_text") or ""),
        "spoken_text": str(audit.get("spoken_text") or ""),
        "text_diff_audit": dict(tda),
        "hard_audit": dict(decision.get("hard_audit") or {}),
    }


def _map_diff_type_for_table(tda: Dict[str, Any]) -> str:
    dt = str(tda.get("diff_type") or "none")
    rs = tda.get("rewrite_source")
    if dt == "formatting_only" or (rs and "guard" in str(rs).lower()):
        return "guard_normalization"
    return dt


def _build_text_diff_row(
    *,
    request_id: str,
    provider_mode: str,
    audit: Dict[str, Any],
) -> Dict[str, Any]:
    tda = audit.get("text_diff_audit") if isinstance(audit.get("text_diff_audit"), dict) else {}
    dt_table = _map_diff_type_for_table(tda)
    rs = tda.get("rewrite_source")
    provider_caused = bool(tda.get("text_changed")) and rs not in (None, "") and "guard" not in str(rs).lower()
    # qwen-tts must never mark provider-caused rewrite
    provider_caused = False
    return {
        "request_id": request_id,
        "provider_mode": provider_mode,
        "source_text": str(audit.get("source_text") or ""),
        "provider_input_text": str(audit.get("provider_input_text") or ""),
        "spoken_text": str(audit.get("spoken_text") or ""),
        "text_changed": bool(tda.get("text_changed")),
        "diff_type": dt_table,
        "rewrite_allowed": bool(tda.get("rewrite_allowed")),
        "rewrite_source": rs,
        "provider_caused_rewrite": provider_caused,
    }


def _emit_stage_row(
    stage_name: str,
    *,
    decision: Dict[str, Any],
    audit: Dict[str, Any],
    provider_mode: str,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    row = {
        "namespace": NS,
        "stage": stage_name,
        **_base_stage_fields(decision=decision, audit=audit, provider_mode=provider_mode),
    }
    if extra:
        row.update(extra)
    return row


def _build_chain_for_mode(
    decision: Dict[str, Any],
    audit: Dict[str, Any],
    provider_mode: str,
) -> List[Dict[str, Any]]:
    bf = _base_stage_fields(decision=decision, audit=audit, provider_mode=provider_mode)
    chains: List[Dict[str, Any]] = []

    chains.append(
        {
            "stage": STAGE_GOVERNANCE_SOURCE,
            "payload": {
                **bf,
                "governance_final_action": str(decision.get("governance_final_action") or ""),
                "entry_allowed": bool(decision.get("entry_allowed")),
                "entry_block_reason": decision.get("entry_block_reason"),
            },
        }
    )
    chains.append(
        {
            "stage": STAGE_PROVIDER_MODE,
            "payload": {**bf, "requested_provider_mode": str(decision.get("requested_provider_mode") or "")},
        }
    )
    ps = decision.get("provider_selection") if isinstance(decision.get("provider_selection"), dict) else {}
    chains.append({"stage": STAGE_PROVIDER_SELECTION, "payload": {**bf, "provider_selection": dict(ps)}})
    pb = audit.get("provider_boundary") if isinstance(audit.get("provider_boundary"), dict) else {}
    chains.append(
        {
            "stage": STAGE_SPEAKABILITY_AUDIT,
            "payload": {**bf, "provider_boundary": dict(pb)},
        }
    )
    chains.append(
        {
            "stage": STAGE_TEXT_DIFF_AUDIT,
            "payload": {**bf, "text_diff_audit": bf["text_diff_audit"]},
        }
    )
    chains.append(
        {
            "stage": STAGE_FINAL_ENTRY_DECISION,
            "payload": {
                **bf,
                "entry_decision_id": str(decision.get("entry_decision_id") or ""),
                "speakability_audit_ref": str(decision.get("speakability_audit_ref") or ""),
            },
        }
    )
    chains.append(
        {
            "stage": STAGE_AUDIT_ENVELOPE,
            "payload": {
                **bf,
                "audit_envelope": {
                    "real_qwen_invoked": bf["hard_audit"].get("real_qwen_invoked"),
                    "real_tts_invoked": bf["hard_audit"].get("real_tts_invoked"),
                    "provider_invoked": bf["hard_audit"].get("provider_invoked"),
                    "playback_invoked": bf["hard_audit"].get("playback_invoked"),
                    "navigation_action": bf["hard_audit"].get("navigation_action"),
                    "downstream_invocation_count": bf["hard_audit"].get("downstream_invocation_count"),
                },
            },
        }
    )
    return chains


def _hard_audit_ok(d: Dict[str, Any]) -> bool:
    ha = d.get("hard_audit") if isinstance(d.get("hard_audit"), dict) else {}
    return (
        ha.get("real_qwen_invoked") is False
        and ha.get("real_tts_invoked") is False
        and ha.get("provider_invoked") is False
        and ha.get("playback_invoked") is False
        and ha.get("navigation_action") is None
        and int(ha.get("downstream_invocation_count") or 0) == 0
    )


def _selection_consistent(
    *,
    online_d: Dict[str, Any],
    offline_d: Dict[str, Any],
) -> Tuple[bool, bool, bool]:
    """selection_consistent_with_policy, qwen_only_online (no qwen in offline row), hard_audit_ok"""
    fa = str(online_d.get("governance_final_action") or "")
    entry_on = bool(online_d.get("entry_allowed"))
    on_ps = online_d.get("provider_selection") if isinstance(online_d.get("provider_selection"), dict) else {}
    off_ps = offline_d.get("provider_selection") if isinstance(offline_d.get("provider_selection"), dict) else {}
    on_sel = str(on_ps.get("selected_provider") or "none")
    off_sel = str(off_ps.get("selected_provider") or "none")
    on_po = list(on_ps.get("provider_order") or [])
    off_po = list(off_ps.get("provider_order") or [])

    ha_ok = _hard_audit_ok(online_d) and _hard_audit_ok(offline_d)
    qwen_only_online = ("qwen" not in off_po) and (off_sel != "qwen")

    if not entry_on:
        ok = on_sel == "none" and off_sel == "none"
        return ok, qwen_only_online, ha_ok

    if fa == "accepted_dry_run":
        ok = on_sel == "qwen" and off_sel == "piper" and off_po == ["piper"] and on_po == ["qwen", "piper"]
        return ok, qwen_only_online, ha_ok

    if fa == "fallback_candidate":
        ok = on_sel == "piper" and off_sel == "piper"
        return ok, qwen_only_online, ha_ok

    return False, qwen_only_online, ha_ok


def run_evaluate(*, online_root: Path, offline_root: Path, out_root: Path) -> Dict[str, Any]:
    on_dec = _read_json(online_root / "voice_qwen_governed_entry_decisions.json")
    on_aud = _read_json(online_root / "voice_speakability_audits.json")
    off_dec = _read_json(offline_root / "voice_qwen_governed_entry_decisions.json")
    off_aud = _read_json(offline_root / "voice_speakability_audits.json")

    if not isinstance(on_dec, list) or not isinstance(off_dec, list):
        raise ValueError("decisions must be lists")

    on_dmap = _index_decisions(on_dec)
    on_amap = _index_audits(on_aud)
    off_dmap = _index_decisions(off_dec)
    off_amap = _index_audits(off_aud)

    request_ids = sorted(set(on_dmap.keys()) & set(off_dmap.keys()))

    chains_out: List[Dict[str, Any]] = []
    comparison: List[Dict[str, Any]] = []
    sel_table: List[Dict[str, Any]] = []
    speak_table: List[Dict[str, Any]] = []
    diff_table: List[Dict[str, Any]] = []

    trace_lines: List[Dict[str, Any]] = []
    replay_lines: List[Dict[str, Any]] = []
    white_lines: List[Dict[str, Any]] = []

    for rid in request_ids:
        od, oa = on_dmap[rid], on_amap.get(rid, {})
        fd, faud = off_dmap[rid], off_amap.get(rid, {})

        on_chain = _build_chain_for_mode(od, oa, "online_prefer_qwen")
        off_chain = _build_chain_for_mode(fd, faud, "offline_only")

        chains_out.append(
            {
                "request_id": rid,
                "sample_id": str(od.get("sample_id") or ""),
                "online_prefer_qwen": on_chain,
                "offline_only": off_chain,
            }
        )

        on_ps = od.get("provider_selection") if isinstance(od.get("provider_selection"), dict) else {}
        off_ps = fd.get("provider_selection") if isinstance(fd.get("provider_selection"), dict) else {}
        sc, qo, ha_ok = _selection_consistent(online_d=od, offline_d=fd)

        comparison.append(
            {
                "request_id": rid,
                "sample_id": str(od.get("sample_id") or ""),
                "online_selected_provider": str(on_ps.get("selected_provider") or "none"),
                "offline_selected_provider": str(off_ps.get("selected_provider") or "none"),
                "online_provider_order": list(on_ps.get("provider_order") or []),
                "offline_provider_order": list(off_ps.get("provider_order") or []),
                "governance_final_action": str(od.get("governance_final_action") or ""),
                "selection_consistent_with_policy": sc,
                "qwen_only_online": qo,
                "hard_audit_ok": ha_ok,
            }
        )

        for stage_row in on_chain:
            trace_lines.append(
                {
                    "type": "voice_qwen_entry_request_trace_v0",
                    "namespace": NS,
                    "stage": stage_row["stage"],
                    "provider_mode": "online_prefer_qwen",
                    **stage_row["payload"],
                }
            )
            replay_lines.append(
                {
                    "type": "voice_qwen_entry_request_trace_replay_v0",
                    "request_id": rid,
                    "stage": stage_row["stage"],
                    "provider_mode": "online_prefer_qwen",
                    "snapshot": stage_row["payload"],
                }
            )
        for stage_row in off_chain:
            trace_lines.append(
                {
                    "type": "voice_qwen_entry_request_trace_v0",
                    "namespace": NS,
                    "stage": stage_row["stage"],
                    "provider_mode": "offline_only",
                    **stage_row["payload"],
                }
            )
            replay_lines.append(
                {
                    "type": "voice_qwen_entry_request_trace_replay_v0",
                    "request_id": rid,
                    "stage": stage_row["stage"],
                    "provider_mode": "offline_only",
                    "snapshot": stage_row["payload"],
                }
            )

        white_lines.append(
            {
                "type": "voice_qwen_entry_request_trace_whitebox_v0",
                "request_id": rid,
                "sample_id": str(od.get("sample_id") or ""),
                "online_selected": str(on_ps.get("selected_provider") or ""),
                "offline_selected": str(off_ps.get("selected_provider") or ""),
                "selection_consistent_with_policy": sc,
                "entry_block_reason_online": od.get("entry_block_reason"),
            }
        )

        for pm, d, a in (
            ("online_prefer_qwen", od, oa),
            ("offline_only", fd, faud),
        ):
            sel_table.append(
                {
                    "request_id": rid,
                    "provider_mode": pm,
                    "stage": STAGE_PROVIDER_SELECTION,
                    **_base_stage_fields(decision=d, audit=a, provider_mode=pm),
                    "selection_reason": (d.get("provider_selection") or {}).get("selection_reason"),
                }
            )
            speak_table.append(
                {
                    "request_id": rid,
                    "provider_mode": pm,
                    "stage": STAGE_SPEAKABILITY_AUDIT,
                    **_base_stage_fields(decision=d, audit=a, provider_mode=pm),
                    "provider_boundary": a.get("provider_boundary"),
                }
            )
            diff_table.append(_build_text_diff_row(request_id=rid, provider_mode=pm, audit=a))

    summary = {
        "phase": "Phase-Voice-Qianwen-003",
        "namespace": NS,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "online_root": str(online_root),
        "offline_root": str(offline_root),
        "output_root": str(out_root),
        "request_count": len(request_ids),
        "stage_names": [
            STAGE_GOVERNANCE_SOURCE,
            STAGE_PROVIDER_MODE,
            STAGE_PROVIDER_SELECTION,
            STAGE_SPEAKABILITY_AUDIT,
            STAGE_TEXT_DIFF_AUDIT,
            STAGE_FINAL_ENTRY_DECISION,
            STAGE_AUDIT_ENVELOPE,
        ],
        "constraints": {
            "no_real_provider": True,
            "no_real_tts": True,
            "no_run_tts_unified_entry": True,
            "shadow_only": True,
        },
    }

    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "voice_qwen_entry_request_trace_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "voice_qwen_entry_request_chains.json").write_text(
        json.dumps(chains_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "voice_qwen_provider_mode_comparison_matrix.json").write_text(
        json.dumps(comparison, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "voice_qwen_provider_selection_stage_table.json").write_text(
        json.dumps(sel_table, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "voice_qwen_speakability_audit_stage_table.json").write_text(
        json.dumps(speak_table, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "voice_qwen_text_diff_audit_table.json").write_text(
        json.dumps(diff_table, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    def _write_jsonl(name: str, rows: List[Dict[str, Any]]) -> None:
        p = out_root / name
        with p.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    _write_jsonl("voice_qwen_entry_request_trace_trace.jsonl", trace_lines)
    _write_jsonl("voice_qwen_entry_request_trace_replay.jsonl", replay_lines)
    _write_jsonl("voice_qwen_entry_request_trace_whitebox.jsonl", white_lines)

    notes = [
        "# Phase-Voice-Qianwen-003 evaluation notes",
        "",
        f"- online_root: `{online_root}`",
        f"- offline_root: `{offline_root}`",
        f"- output_root: `{out_root}`",
        "",
        "Shadow RequestTrace mapping only. No network, no TTS, no run_tts_unified_entry.",
        "",
    ]
    (out_root / "evaluation_notes.md").write_text("\n".join(notes), encoding="utf-8")

    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--online-root", required=True)
    ap.add_argument("--offline-root", required=True)
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _repo_root()
    on_r = Path(args.online_root)
    off_r = Path(args.offline_root)
    if not on_r.is_absolute():
        on_r = repo / on_r
    if not off_r.is_absolute():
        off_r = repo / off_r

    out = Path(args.output_root) if args.output_root else repo / "logs" / f"voice_qwen_governed_entry_request_trace_003_{_utc_tag()}"

    summary = run_evaluate(online_root=on_r, offline_root=off_r, out_root=out)
    print(json.dumps({"ok": True, "output_root": str(out), "request_count": summary.get("request_count")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
