# -*- coding: utf-8 -*-
"""
Phase-Voice-OutputGovernance-009
Export package for governed submit shadow gate from Phase-008 enhanced request chains.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


STAGE_NAME = "request_trace.stage.output.voice.governed_submit_shadow_gate"
GATE_POSITIONS = ("_maybe_submit_real_output_v1_pre", "VoiceOutputPlane.submit_entry")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _mk_out_root(p: Optional[str]) -> Path:
    out = Path(p) if p else (Path("logs") / f"voice_governed_submit_unified_export_009_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    if not out.is_absolute():
        out = Path.cwd() / out
    out.mkdir(parents=True, exist_ok=True)
    return out


def _hard_audit_ok(ha: Dict[str, Any]) -> bool:
    return (
        ha.get("real_submit_invoked") in (False, None)
        and ha.get("real_tts_invoked") is False
        and ha.get("playback_invoked") is False
        and ha.get("provider_invoked") is False
        and ha.get("navigation_action") in (None, "")
        and ha.get("downstream_invocation_count") in (0, None)
    )


def _iter_gate_rows(enhanced: List[Dict[str, Any]], *, source_root: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for ch in enhanced:
        if not isinstance(ch, dict):
            continue
        rid = ch.get("request_id")
        if not isinstance(rid, str) or not rid:
            continue
        stages = ch.get("stages")
        if not isinstance(stages, list):
            continue
        for st in stages:
            if not isinstance(st, dict):
                continue
            if st.get("stage_name") != STAGE_NAME:
                continue
            kf = st.get("key_fields") if isinstance(st.get("key_fields"), dict) else {}
            ha = kf.get("hard_audit") if isinstance(kf.get("hard_audit"), dict) else {}
            rows.append(
                {
                    "source_root": source_root,
                    "request_id": rid,
                    "stage_name": STAGE_NAME,
                    "submit_gate_position": kf.get("submit_gate_position"),
                    "submit_shadow_result": kf.get("submit_shadow_result"),
                    "submit_allowed": kf.get("submit_allowed"),
                    "submit_block_reason": kf.get("submit_block_reason"),
                    "source_submit_shadow_decision_id": kf.get("source_submit_shadow_decision_id"),
                    "source_governance_decision_id": kf.get("source_governance_decision_id"),
                    "hard_audit": ha,
                    "hard_audit_ok": _hard_audit_ok(ha),
                    "whitebox_extension": kf.get("whitebox_extension"),
                }
            )
    return rows


def _gate_position_table(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for r in rows:
        out.append(
            {
                "request_id": r.get("request_id"),
                "submit_gate_position": r.get("submit_gate_position"),
                "submit_shadow_result": r.get("submit_shadow_result"),
                "submit_allowed": r.get("submit_allowed"),
                "submit_block_reason": r.get("submit_block_reason"),
                "source_submit_shadow_decision_id": r.get("source_submit_shadow_decision_id"),
                "source_governance_decision_id": r.get("source_governance_decision_id"),
                "hard_audit_ok": r.get("hard_audit_ok"),
            }
        )
    return out


def _result_table(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    agg: Dict[str, List[str]] = {}
    for r in rows:
        res = r.get("submit_shadow_result")
        rid = r.get("request_id")
        if isinstance(res, str) and isinstance(rid, str):
            agg.setdefault(res, [])
            if rid not in agg[res]:
                agg[res].append(rid)
    out = [{"submit_shadow_result": k, "count": len(v), "request_ids": sorted(v)} for k, v in agg.items()]
    return sorted(out, key=lambda x: x["submit_shadow_result"])


def _request_matrix(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_req: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for r in rows:
        rid = r.get("request_id")
        pos = r.get("submit_gate_position")
        if not isinstance(rid, str) or not isinstance(pos, str):
            continue
        by_req.setdefault(rid, {})
        by_req[rid][pos] = r

    out: List[Dict[str, Any]] = []
    for rid, m in by_req.items():
        pre = m.get("_maybe_submit_real_output_v1_pre")
        ent = m.get("VoiceOutputPlane.submit_entry")
        pre_res = pre.get("submit_shadow_result") if isinstance(pre, dict) else None
        ent_res = ent.get("submit_shadow_result") if isinstance(ent, dict) else None
        positions_consistent = (pre_res is not None and pre_res == ent_res)
        hard_ok = True
        for rr in (pre, ent):
            if isinstance(rr, dict) and rr.get("hard_audit_ok") is False:
                hard_ok = False
        out.append(
            {
                "request_id": rid,
                "maybe_submit_pre_result": pre_res,
                "output_plane_entry_result": ent_res,
                "positions_consistent": positions_consistent,
                "hard_audit_ok": hard_ok,
            }
        )
    return sorted(out, key=lambda x: x["request_id"])


def _hard_audit_table(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "request_id": r.get("request_id"),
            "submit_gate_position": r.get("submit_gate_position"),
            "hard_audit_ok": r.get("hard_audit_ok"),
            "hard_audit": r.get("hard_audit"),
        }
        for r in rows
    ]


def _field_mapping_report(source_file: str) -> List[Dict[str, Any]]:
    # Static mapping contract for governed submit shadow gate stage.
    fields = [
        ("request_id", "request_id"),
        ("stage_name", "stage_name"),
        ("key_fields.submit_gate_position", "submit_gate_position"),
        ("key_fields.submit_shadow_result", "submit_shadow_result"),
        ("key_fields.submit_allowed", "submit_allowed"),
        ("key_fields.submit_block_reason", "submit_block_reason"),
        ("key_fields.source_submit_shadow_decision_id", "source_submit_shadow_decision_id"),
        ("key_fields.source_governance_decision_id", "source_governance_decision_id"),
        ("key_fields.hard_audit.real_submit_invoked", "hard_audit.real_submit_invoked"),
        ("key_fields.hard_audit.real_tts_invoked", "hard_audit.real_tts_invoked"),
        ("key_fields.hard_audit.playback_invoked", "hard_audit.playback_invoked"),
        ("key_fields.hard_audit.provider_invoked", "hard_audit.provider_invoked"),
        ("key_fields.hard_audit.navigation_action", "hard_audit.navigation_action"),
        ("key_fields.hard_audit.downstream_invocation_count", "hard_audit.downstream_invocation_count"),
        ("key_fields.whitebox_extension.why_submit_allowed_shadow", "whitebox_extension.why_submit_allowed_shadow"),
        ("key_fields.whitebox_extension.why_submit_blocked_shadow", "whitebox_extension.why_submit_blocked_shadow"),
        ("key_fields.whitebox_extension.why_no_real_submit_invoked", "whitebox_extension.why_no_real_submit_invoked"),
    ]
    out: List[Dict[str, Any]] = []
    for src, uni in fields:
        out.append(
            {
                "source_file": source_file,
                "source_field": src,
                "unified_field": uni,
                "mapping_status": "mapped",
                "notes": "from Phase-008 governed_submit_shadow_gate stage key_fields",
            }
        )
    return out


def _md_report(summary: Dict[str, Any]) -> str:
    return (
        "# Voice Governed Submit Unified Export Report (v0)\n\n"
        "## Summary\n\n"
        "```json\n"
        + json.dumps(summary, ensure_ascii=False, indent=2)
        + "\n```\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--output-root", default=None)
    args = ap.parse_args()

    input_root = Path(args.input_root)
    chains_path = input_root / "voice_governed_submit_enhanced_request_chains.json"
    if not chains_path.exists():
        raise SystemExit(f"missing enhanced chains: {chains_path}")

    enhanced = _read_json(chains_path)
    if not isinstance(enhanced, list):
        raise SystemExit("enhanced chains must be a list")

    rows = _iter_gate_rows(enhanced, source_root=str(input_root))

    out_root = _mk_out_root(args.output_root)

    pos_table = _gate_position_table(rows)
    res_table = _result_table(rows)
    ha_table = _hard_audit_table(rows)
    req_matrix = _request_matrix(rows)
    mapping = _field_mapping_report(str(chains_path))

    summary = {
        "phase": "Phase-Voice-OutputGovernance-009",
        "tool": "export_voice_governed_submit_unified_view_v0.py",
        "input_root": str(input_root),
        "output_root": str(out_root),
        "counts": {
            "enhanced_chain_count": len(enhanced),
            "gate_stage_record_count": len(rows),
            "gate_position_table_rows": len(pos_table),
            "result_table_rows": len(res_table),
            "hard_audit_table_rows": len(ha_table),
            "request_matrix_rows": len(req_matrix),
            "field_mapping_rows": len(mapping),
        },
        "hard_audit_invariants": {
            "real_submit_invoked": False,
            "real_tts_invoked": False,
            "playback_invoked": False,
            "provider_invoked": False,
            "navigation_action": None,
            "downstream_invocation_count": 0,
        },
        "notes": ["offline/shadow only", "does not modify Phase-008 artifacts"],
    }

    _write_json(out_root / "voice_governed_submit_unified_export_summary.json", summary)
    _write_json(out_root / "voice_governed_submit_gate_position_table.json", pos_table)
    _write_json(out_root / "voice_governed_submit_result_table.json", res_table)
    _write_json(out_root / "voice_governed_submit_hard_audit_table.json", ha_table)
    _write_json(out_root / "voice_governed_submit_request_matrix.json", req_matrix)
    _write_json(out_root / "voice_governed_submit_field_mapping_report.json", mapping)
    (out_root / "voice_governed_submit_unified_export_report.md").write_text(_md_report(summary), encoding="utf-8")

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

