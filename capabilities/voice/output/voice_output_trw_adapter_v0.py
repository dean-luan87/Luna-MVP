# -*- coding: utf-8 -*-
"""
Phase-Voice-OutputGovernance-004
Voice Output TRW Adapter v0 (offline/shadow adapter only).

Purpose:
- Read Phase-002 governance outputs (decisions/audit/trace/replay/whitebox).
- Convert them into extractor-friendly stage records and request-level timeline.

Hard boundaries:
- MUST NOT invoke real TTS providers.
- MUST NOT invoke playback.
- MUST NOT wire into runtime submit chain.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


STAGE_NAMESPACE_V0 = "voice_output_governance_v0"

STAGE_NAMES_V0: List[str] = [
    "candidate_input",
    "speakable_guard",
    "speech_gate",
    "expiry_check",
    "stale_check",
    "cancellation_check",
    "priority_check",
    "interruption_check",
    "suppression_check",
    "provider_health_check",
    "final_governance_decision",
    "audit_envelope",
]


def _now() -> float:
    return time.time()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    out: List[Dict[str, Any]] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            row = json.loads(ln)
        except Exception:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


@dataclass(frozen=True)
class VoiceOutputTRWRecordV0:
    record_id: str
    request_id: str
    trace_id: Optional[str]
    session_id: Optional[str]
    stage_namespace: str
    stage_name: str
    stage_order: int
    input_ref: str
    output_ref: str
    decision_ref: str
    audit_envelope_ref: str
    status: str  # passed|blocked|suppressed|cancelled|fallback_candidate|dry_run_accepted
    reason: Optional[str]
    hard_audit: Dict[str, Any]
    whitebox_extension: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VoiceOutputTRWAdapterLoadedV0:
    input_root: str
    decisions: List[Dict[str, Any]]
    audits: List[Dict[str, Any]]
    trace_rows: List[Dict[str, Any]]
    replay_rows: List[Dict[str, Any]]
    whitebox_rows: List[Dict[str, Any]]


def load_voice_output_governance_outputs_v0(input_root: str) -> VoiceOutputTRWAdapterLoadedV0:
    root = Path(input_root)
    decisions = _read_json(root / "voice_output_governance_decisions.json")
    audits = _read_json(root / "voice_output_audit_envelopes.json")
    trace_rows = _read_jsonl(root / "voice_output_trace.jsonl")
    replay_rows = _read_jsonl(root / "voice_output_replay.jsonl")
    whitebox_rows = _read_jsonl(root / "voice_output_whitebox.jsonl")
    if not isinstance(decisions, list):
        decisions = []
    if not isinstance(audits, list):
        audits = []
    return VoiceOutputTRWAdapterLoadedV0(
        input_root=str(root),
        decisions=[x for x in decisions if isinstance(x, dict)],
        audits=[x for x in audits if isinstance(x, dict)],
        trace_rows=[x for x in trace_rows if isinstance(x, dict)],
        replay_rows=[x for x in replay_rows if isinstance(x, dict)],
        whitebox_rows=[x for x in whitebox_rows if isinstance(x, dict)],
    )


def build_voice_output_whitebox_extension_v0(decision: Dict[str, Any], whitebox_row: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    sup = (decision.get("suppression_result") if isinstance(decision.get("suppression_result"), dict) else {}) or {}
    pr = (decision.get("priority_result") if isinstance(decision.get("priority_result"), dict) else {}) or {}
    gate = (decision.get("speech_gate_result") if isinstance(decision.get("speech_gate_result"), dict) else {}) or {}
    exp = (decision.get("expiry_result") if isinstance(decision.get("expiry_result"), dict) else {}) or {}
    ph = (decision.get("provider_health_result") if isinstance(decision.get("provider_health_result"), dict) else {}) or {}
    final_action = str(decision.get("final_action") or "")
    reason = str(sup.get("suppression_reason") or "")

    return {
        "why_guard_blocked": reason.startswith("guard_blocked"),
        "why_speech_gate_denied": reason.startswith("speech_gate_blocked") or (gate.get("allowed") is False),
        "why_expired": (reason == "expired") or (exp.get("is_expired") is True),
        "why_stale": (reason == "stale") or (exp.get("stale_suppressed") is True),
        "why_cancelled": (reason == "cancelled") or (final_action == "cancelled"),
        "why_suppressed": (final_action == "suppressed"),
        "why_interrupt_allowed": (pr.get("interrupt_decision") == "allowed"),
        "why_interrupt_denied": (reason == "interrupt_denied") or (pr.get("interrupt_decision") == "denied"),
        "why_provider_fallback_required": (final_action == "fallback_candidate") or (ph.get("fallback_required") is True),
        "why_dry_run_accepted": (final_action == "accepted_dry_run"),
        "why_real_tts_not_invoked": True,
        "whitebox_ref": (str(decision.get("whitebox_ref") or "") or None),
        "whitebox_row_hint": (whitebox_row.get("reason") if isinstance(whitebox_row, dict) else None),
    }


def _hard_audit_from_decision(decision: Dict[str, Any]) -> Dict[str, Any]:
    gov = decision.get("governance") if isinstance(decision.get("governance"), dict) else {}
    return {
        "real_tts_invoked": bool(gov.get("real_tts_invoked")) if "real_tts_invoked" in gov else False,
        "playback_invoked": bool(gov.get("playback_invoked")) if "playback_invoked" in gov else False,
        "provider_invoked": bool(gov.get("provider_invoked")) if "provider_invoked" in gov else False,
        "downstream_invocation_count": int(gov.get("downstream_invocation_count") or 0),
        "navigation_action": gov.get("navigation_action", None),
    }


def _status_from_decision(decision: Dict[str, Any]) -> Tuple[str, Optional[str]]:
    final_action = str(decision.get("final_action") or "")
    sup = decision.get("suppression_result") if isinstance(decision.get("suppression_result"), dict) else {}
    sup_reason = str((sup or {}).get("suppression_reason") or "") or None

    if final_action == "accepted_dry_run":
        return "dry_run_accepted", None
    if final_action == "cancelled":
        return "cancelled", "cancel_requested"
    if final_action == "fallback_candidate":
        return "fallback_candidate", str((decision.get("provider_health_result") or {}).get("reason") or "") or None
    if final_action == "suppressed":
        return "suppressed", sup_reason
    return "blocked", f"unknown_final_action:{final_action}"


def build_voice_output_stage_timeline_v0(request_id: str) -> List[Dict[str, Any]]:
    """
    Pure timeline skeleton (stage order only).
    Phase-004 doesn't infer missing stages; it lists expected stages for extractor mapping.
    """
    out: List[Dict[str, Any]] = []
    for i, name in enumerate(STAGE_NAMES_V0):
        out.append(
            {
                "request_id": str(request_id),
                "stage_namespace": STAGE_NAMESPACE_V0,
                "stage_name": name,
                "stage_order": int(i),
            }
        )
    return out


def build_voice_output_trw_record_v0(
    *,
    decision: Dict[str, Any],
    audit: Optional[Dict[str, Any]],
    stage_name: str,
    stage_order: int,
    whitebox_row: Optional[Dict[str, Any]],
) -> VoiceOutputTRWRecordV0:
    rid = str(decision.get("request_id") or "")
    # Phase-002 uses "voice_output_decision_id" field name.
    decision_ref = str(decision.get("voice_output_decision_id") or "")
    if not decision_ref:
        decision_ref = str(decision.get("trace_ref") or "")

    audit_ref = str(audit.get("audit_id") if isinstance(audit, dict) else "") or ""
    status, reason = _status_from_decision(decision)
    hard = _hard_audit_from_decision(decision)
    wb_ext = build_voice_output_whitebox_extension_v0(decision, whitebox_row)

    return VoiceOutputTRWRecordV0(
        record_id=f"trw_{uuid.uuid4().hex[:12]}",
        request_id=rid,
        trace_id=None,
        session_id=None,
        stage_namespace=STAGE_NAMESPACE_V0,
        stage_name=str(stage_name),
        stage_order=int(stage_order),
        input_ref=str(decision.get("replay_ref") or decision.get("trace_ref") or ""),
        output_ref=str(decision.get("trace_ref") or ""),
        decision_ref=str(decision_ref),
        audit_envelope_ref=str(audit_ref),
        status=str(status),
        reason=reason,
        hard_audit=hard,
        whitebox_extension=wb_ext,
        metadata={
            "sample_id": decision.get("sample_id"),
            "final_action": decision.get("final_action"),
        },
    )


def build_voice_output_extractor_mapping_report_v0() -> Dict[str, Any]:
    """
    Static report describing where fields come from and where they map to (per Phase-003).
    """
    return {
        "phase": "Phase-Voice-OutputGovernance-004",
        "adapter": "voice_output_trw_adapter_v0",
        "stage_namespace": STAGE_NAMESPACE_V0,
        "stage_names": list(STAGE_NAMES_V0),
        "sources": {
            "decisions": "voice_output_governance_decisions.json",
            "audit_envelopes": "voice_output_audit_envelopes.json",
            "trace": "voice_output_trace.jsonl",
            "replay": "voice_output_replay.jsonl",
            "whitebox": "voice_output_whitebox.jsonl",
        },
        "field_mapping": [
            {"from": "decision.guard_result", "to": "TRW.stage.speakable_guard.key_fields", "stage_name": "speakable_guard"},
            {"from": "decision.speech_gate_result", "to": "TRW.stage.speech_gate.key_fields", "stage_name": "speech_gate"},
            {"from": "decision.expiry_result", "to": "TRW.stage.expiry_check.key_fields", "stage_name": "expiry_check"},
            {"from": "decision.cancel_result", "to": "TRW.stage.cancellation_check.key_fields", "stage_name": "cancellation_check"},
            {"from": "decision.priority_result", "to": "TRW.stage.priority_check.key_fields", "stage_name": "priority_check"},
            {"from": "decision.provider_health_result", "to": "TRW.stage.provider_health_check.key_fields", "stage_name": "provider_health_check"},
            {"from": "decision.final_action", "to": "TRW.stage.final_governance_decision.key_fields", "stage_name": "final_governance_decision"},
            {"from": "audit_envelope.audit_id", "to": "TRW.audit_ref", "stage_name": "audit_envelope"},
            {"from": "decision.governance.*", "to": "TRW.whitebox.hard_audit", "stage_name": "final_governance_decision"},
        ],
        "missing_fields_expected_future": [
            {"field": "trace_id", "note": "Phase-002 samples do not inject trace_id; future mainline wiring should pass through SpeechRequest.trace_id"},
            {"field": "session_id", "note": "Phase-002 adapter uses request_id only; future mainline wiring should inject session_id from voice session anchor"},
            {"field": "candidate_text_hash", "note": "Hashing contract defined in Phase-003; implement in later adapter revision"},
        ],
        "hard_audit_fields": [
            "real_tts_invoked",
            "playback_invoked",
            "provider_invoked",
            "downstream_invocation_count",
            "navigation_action",
        ],
    }


def run_voice_output_trw_adapter_v0(
    *,
    input_root: str,
) -> Tuple[List[VoiceOutputTRWRecordV0], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
    loaded = load_voice_output_governance_outputs_v0(input_root)

    # Index audits/whitebox by request_id
    audits_by_rid: Dict[str, Dict[str, Any]] = {}
    for a in loaded.audits:
        rid = str(a.get("request_id") or "")
        if rid and rid not in audits_by_rid:
            audits_by_rid[rid] = a

    whitebox_by_rid: Dict[str, Dict[str, Any]] = {}
    for w in loaded.whitebox_rows:
        rid = str(w.get("request_id") or "")
        if rid and rid not in whitebox_by_rid:
            whitebox_by_rid[rid] = w

    records: List[VoiceOutputTRWRecordV0] = []
    timeline: List[Dict[str, Any]] = []

    for d in loaded.decisions:
        rid = str(d.get("request_id") or "")
        if not rid:
            continue
        audit = audits_by_rid.get(rid)
        wb = whitebox_by_rid.get(rid)

        # One TRW record per stage for this request (extractor-friendly).
        for i, stage in enumerate(STAGE_NAMES_V0):
            records.append(
                build_voice_output_trw_record_v0(
                    decision=d,
                    audit=audit,
                    stage_name=stage,
                    stage_order=i,
                    whitebox_row=wb,
                )
            )
        timeline.extend(build_voice_output_stage_timeline_v0(rid))

    mapping_report = build_voice_output_extractor_mapping_report_v0()

    # Summary
    summary = {
        "phase": "Phase-Voice-OutputGovernance-004",
        "tool": "voice_output_trw_adapter_v0",
        "generated_at_s": _now(),
        "input_root": str(loaded.input_root),
        "request_count": len({r.request_id for r in records}),
        "record_count": len(records),
        "stage_namespace": STAGE_NAMESPACE_V0,
        "stage_names": list(STAGE_NAMES_V0),
        "notes": [
            "Offline adapter only; does not invoke provider/playback.",
            "trace_id/session_id are null in adapter records by design (future mainline injection).",
        ],
    }

    return records, summary, timeline, mapping_report

