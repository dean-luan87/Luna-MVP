#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-005
RequestTraceExtractor Governance Stage Integration (shadow/offline).

Reads Phase-004 adapter outputs (voice_output_trw_records.json etc),
and produces RequestTraceChain-like shadow chains with governance stages included.

Hard boundaries:
- Offline/shadow only.
- Does NOT invoke real TTS or playback.
- Does NOT change runtime wiring.
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


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _stage_name_map(ns: str, stage_name: str) -> str:
    # Mapping rules requested by user.
    base = f"{ns}.{stage_name}"
    if ns == "voice_output_governance_v0":
        return f"request_trace.stage.voice_output.{stage_name}"
    return f"request_trace.stage.unknown.{base}"


def _chain_type_from_final_status(final_status: str) -> Tuple[str, str]:
    """
    Returns (chain_type, status) compatible with RequestTraceChain semantics.
    """
    fs = str(final_status or "").strip().lower()
    if fs in ("dry_run_accepted", "passed"):
        return "success_chain", "ok"
    if fs in ("suppressed", "cancelled", "blocked"):
        return "suppressed_chain", "suppressed"
    if fs in ("fallback_candidate",):
        return "provider_fallback_chain", "partial"
    return "unknown", "partial"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True, help="Phase-004 adapter output root")
    ap.add_argument("--output-root", required=True, help="Output root")
    args = ap.parse_args()

    inp_root = Path(args.input_root)
    out_root = Path(args.output_root)
    out_root.mkdir(parents=True, exist_ok=True)

    from capabilities.voice.observations.request_trace_chain import (  # type: ignore
        RequestTraceChain,
        TraceStageRecord,
        TraceErrorRecord,
    )

    records_path = inp_root / "voice_output_trw_records.json"
    records = _read_json(records_path)
    if not isinstance(records, list):
        raise SystemExit("input records must be a list")
    records = [r for r in records if isinstance(r, dict)]

    # Group by request_id
    by_rid: Dict[str, List[Dict[str, Any]]] = {}
    for r in records:
        rid = str(r.get("request_id") or "")
        if not rid:
            continue
        by_rid.setdefault(rid, []).append(r)

    chains: List[Dict[str, Any]] = []
    stage_mapping: Dict[str, Any] = {
        "stage_namespace": "voice_output_governance_v0",
        "mapping_prefix": "request_trace.stage.voice_output.*",
        "rules": [
            {"from": f"voice_output_governance_v0.{name}", "to": f"request_trace.stage.voice_output.{name}"}
            for name in sorted({str(r.get('stage_name') or '') for r in records if str(r.get('stage_namespace') or '') == 'voice_output_governance_v0'})
            if name
        ],
    }
    per_request_whitebox: List[Dict[str, Any]] = []

    trace_jsonl = out_root / "voice_output_extractor_shadow_trace.jsonl"
    replay_jsonl = out_root / "voice_output_extractor_shadow_replay.jsonl"
    whitebox_jsonl = out_root / "voice_output_extractor_shadow_whitebox.jsonl"
    for p in (trace_jsonl, replay_jsonl, whitebox_jsonl):
        try:
            p.unlink()
        except Exception:
            pass

    for rid, recs in sorted(by_rid.items()):
        # Only accept recognized namespace for this phase.
        recs2 = [x for x in recs if str(x.get("stage_namespace") or "") == "voice_output_governance_v0"]
        recs2.sort(key=lambda x: int(x.get("stage_order") or 0))

        stages: List[TraceStageRecord] = []
        errors: List[TraceErrorRecord] = []
        notes: List[str] = ["shadow_mode_only:true", "source:voice_output_trw_adapter_v0"]
        refs: List[str] = [str(records_path)]

        final_status = "unknown"
        final_reason = None
        hard_audit = {}
        whitebox_ext = {}

        # Build stages
        for r in recs2:
            st_name = str(r.get("stage_name") or "")
            mapped = _stage_name_map(str(r.get("stage_namespace") or ""), st_name)
            status = "ok"
            s = str(r.get("status") or "")
            if s in ("suppressed", "cancelled", "blocked"):
                status = "fail"
            elif s in ("fallback_candidate",):
                status = "partial"
            elif s in ("dry_run_accepted", "passed"):
                status = "ok"
            else:
                status = "partial"

            key_fields = {
                "stage_namespace": r.get("stage_namespace"),
                "stage_name": st_name,
                "stage_order": r.get("stage_order"),
                "adapter_status": r.get("status"),
                "adapter_reason": r.get("reason"),
                "decision_ref": r.get("decision_ref"),
                "audit_envelope_ref": r.get("audit_envelope_ref"),
                "hard_audit": r.get("hard_audit"),
                "whitebox_extension": r.get("whitebox_extension"),
            }
            stages.append(
                TraceStageRecord(
                    stage_name=mapped,
                    status=status,
                    timestamp=None,
                    key_fields=key_fields,
                    source_observation_type="VoiceOutputTRWRecordV0",
                    source_ref=str(r.get("input_ref") or ""),
                )
            )

            if st_name == "final_governance_decision":
                final_status = str(r.get("status") or "unknown")
                final_reason = r.get("reason")
                hard_audit = r.get("hard_audit") if isinstance(r.get("hard_audit"), dict) else {}
                whitebox_ext = r.get("whitebox_extension") if isinstance(r.get("whitebox_extension"), dict) else {}

        chain_type, chain_status = _chain_type_from_final_status(final_status)

        # Add an error record when suppressed/cancelled/blocked for extractor visibility.
        if chain_status == "suppressed":
            errors.append(
                TraceErrorRecord(
                    stage_name="request_trace.stage.voice_output.final_governance_decision",
                    error_type="request_suppressed",
                    error_reason=str(final_reason or final_status),
                    severity="info",
                )
            )

        ch = RequestTraceChain(
            request_id=rid,
            trace_id=None,
            session_id=None,
            task_context_id=None,
            chain_type=chain_type,
            final_execution_mode="governance_shadow",
            provider_name=None,
            started_at=None,
            ended_at=None,
            status=chain_status,
            stages=stages,
            errors=errors,
            notes=notes,
            raw_observation_refs=refs,
        )
        chains.append(ch.to_dict())

        per_request_whitebox.append(
            {
                "request_id": rid,
                "chain_type": chain_type,
                "final_status": final_status,
                "hard_audit": hard_audit,
                "whitebox_explanation": whitebox_ext,
            }
        )

        _append_jsonl(
            trace_jsonl,
            {
                "type": "voice_output_request_trace_shadow_v0",
                "timestamp": _now(),
                "request_id": rid,
                "chain_type": chain_type,
                "final_status": final_status,
                "hard_audit": hard_audit,
            },
        )
        _append_jsonl(
            replay_jsonl,
            {
                "type": "voice_output_request_trace_shadow_replay_v0",
                "timestamp": _now(),
                "request_id": rid,
                "source_input_root": str(inp_root),
                "source_records_ref": str(records_path),
            },
        )
        _append_jsonl(
            whitebox_jsonl,
            {
                "type": "voice_output_request_trace_shadow_whitebox_v0",
                "timestamp": _now(),
                "request_id": rid,
                "whitebox_explanation": whitebox_ext,
            },
        )

    summary = {
        "phase": "Phase-Voice-OutputGovernance-005",
        "tool": "evaluate_voice_output_request_trace_extractor_shadow_v0.py",
        "generated_at_s": _now(),
        "input_root": str(inp_root),
        "output_root": str(out_root),
        "shadow_only": True,
        "request_count": len(by_rid),
        "chain_count": len(chains),
        "stage_namespace": "voice_output_governance_v0",
        "notes": [
            "This is a shadow/offline integration; it does not change runtime RequestTraceExtractor behavior.",
            "trace_id/session_id are null by design in this phase.",
        ],
    }

    _write_json(out_root / "voice_output_request_trace_extractor_summary.json", summary)
    _write_json(out_root / "voice_output_request_chains.json", chains)
    _write_json(out_root / "voice_output_request_stage_mapping.json", stage_mapping)
    _write_json(out_root / "voice_output_request_chain_whitebox.json", per_request_whitebox)

    (out_root / "evaluation_notes.md").write_text(
        "\n".join(
            [
                "# Phase-Voice-OutputGovernance-005 Evaluation Notes",
                "",
                f"- input_root: `{args.input_root}`",
                f"- output_root: `{str(out_root)}`",
                f"- request_count: {len(by_rid)}",
                f"- chain_count: {len(chains)}",
                "",
                "- boundary: shadow/offline only; no runtime wiring changes; no TTS/playback.",
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

