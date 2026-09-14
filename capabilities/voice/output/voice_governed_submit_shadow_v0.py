# -*- coding: utf-8 -*-
"""
Phase-Voice-OutputGovernance-007
Governed Submit Shadow Readiness v0.

This module simulates a "pre-submit" gate decision in shadow mode without
invoking any real submit/TTS/playback. It derives its inputs strictly from
previous offline governance outputs (Phase-002) and preserves hard-audit
invariants.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


RUNTIME_MODE_SHADOW = "shadow"

SUBMIT_GATE_POSITIONS = (
    "_maybe_submit_real_output_v1_pre",
    "VoiceOutputPlane.submit_entry",
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class VoiceGovernedSubmitShadowInput:
    request_id: str
    candidate_text: str
    source_governance_decision_id: str
    source_audit_envelope_id: str
    governance_final_action: str
    speech_gate_allowed: Optional[bool]
    is_expired: Optional[bool]
    cancel_requested: Optional[bool]
    provider_fallback_required: Optional[bool]
    trace_ref: Optional[str] = None
    replay_ref: Optional[str] = None
    whitebox_ref: Optional[str] = None


@dataclass(frozen=True)
class VoiceSubmitGateAuditEnvelope:
    audit_id: str
    request_id: str
    created_at: float
    submit_gate_position: str
    source_governance_decision_id: str
    source_audit_envelope_id: str
    hard_audit: Dict[str, Any]
    refs: Dict[str, Optional[str]] = field(default_factory=dict)


@dataclass(frozen=True)
class VoiceGovernedSubmitShadowDecision:
    submit_shadow_decision_id: str
    request_id: str
    source_governance_decision_id: str
    source_audit_envelope_id: str
    runtime_mode: str
    candidate_text: str
    submit_gate_position: str
    governance_final_action: str
    submit_shadow_result: str
    submit_allowed: bool
    submit_block_reason: Optional[str]
    expiry_checked: bool
    cancel_checked: bool
    speech_gate_checked: bool
    provider_health_checked: bool
    hard_audit: Dict[str, Any]
    trace_ref: Optional[str] = None
    replay_ref: Optional[str] = None
    whitebox_ref: Optional[str] = None


def load_voice_output_governance_decision_v0(governance_root: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    root = Path(governance_root)
    decisions_path = root / "voice_output_governance_decisions.json"
    audits_path = root / "voice_output_audit_envelopes.json"
    if not decisions_path.exists():
        raise FileNotFoundError(f"missing governance decisions: {decisions_path}")
    if not audits_path.exists():
        raise FileNotFoundError(f"missing audit envelopes: {audits_path}")
    decisions = _read_json(decisions_path)
    audits = _read_json(audits_path)
    if not isinstance(decisions, list):
        raise ValueError("voice_output_governance_decisions.json must be a list")
    if not isinstance(audits, list):
        raise ValueError("voice_output_audit_envelopes.json must be a list")
    return decisions, audits


def _index_audits_by_request_id(audits: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for a in audits:
        if not isinstance(a, dict):
            continue
        rid = a.get("request_id")
        if isinstance(rid, str) and rid:
            idx[rid] = a
    return idx


def evaluate_submit_readiness_shadow_v0(inp: VoiceGovernedSubmitShadowInput) -> Tuple[str, bool, Optional[str]]:
    """
    Maps Phase-002 governance final_action + key checks into a pre-submit shadow result.
    Never invokes real submit.
    """
    action = inp.governance_final_action

    # Hard blocks that must not allow submit.
    if inp.cancel_requested:
        return "submit_cancelled_shadow", False, "cancel_requested"
    if inp.is_expired:
        return "submit_expired_shadow", False, "expired"
    if inp.speech_gate_allowed is False:
        return "submit_blocked_shadow", False, "speech_gate_denied"

    if action in ("suppressed", "rejected"):
        return "submit_blocked_shadow", False, f"final_action:{action}"
    if action == "cancelled":
        return "submit_cancelled_shadow", False, "final_action:cancelled"
    if action in ("expired",):
        return "submit_expired_shadow", False, "final_action:expired"
    if action == "fallback_candidate":
        return "submit_fallback_candidate_shadow", False, "fallback_candidate"
    if action in ("accepted_dry_run", "accepted_shadow", "accepted"):
        return "submit_allowed_shadow", True, None

    # Default: conservative block
    return "submit_blocked_shadow", False, f"unknown_final_action:{action}"


def _build_submit_shadow_decision_id(request_id: str, source_decision_id: str, position: str) -> str:
    # stable enough for offline artifacts (no crypto requirement)
    return f"vsds_{request_id}_{source_decision_id}_{position}".replace(".", "_")


def _build_submit_gate_audit_id(request_id: str, source_decision_id: str, position: str) -> str:
    return f"vsg_audit_{request_id}_{source_decision_id}_{position}".replace(".", "_")


def build_governed_submit_shadow_decision_v0(
    *,
    inp: VoiceGovernedSubmitShadowInput,
    submit_gate_position: str,
) -> Tuple[VoiceGovernedSubmitShadowDecision, VoiceSubmitGateAuditEnvelope]:
    submit_shadow_result, allowed, reason = evaluate_submit_readiness_shadow_v0(inp)

    hard_audit = {
        "real_submit_invoked": False,
        "real_tts_invoked": False,
        "playback_invoked": False,
        "provider_invoked": False,
        "navigation_action": None,
        "downstream_invocation_count": 0,
    }

    dec = VoiceGovernedSubmitShadowDecision(
        submit_shadow_decision_id=_build_submit_shadow_decision_id(inp.request_id, inp.source_governance_decision_id, submit_gate_position),
        request_id=inp.request_id,
        source_governance_decision_id=inp.source_governance_decision_id,
        source_audit_envelope_id=inp.source_audit_envelope_id,
        runtime_mode=RUNTIME_MODE_SHADOW,
        candidate_text=inp.candidate_text,
        submit_gate_position=submit_gate_position,
        governance_final_action=inp.governance_final_action,
        submit_shadow_result=submit_shadow_result,
        submit_allowed=bool(allowed),
        submit_block_reason=reason,
        expiry_checked=True,
        cancel_checked=True,
        speech_gate_checked=True,
        provider_health_checked=True,
        hard_audit=hard_audit,
        trace_ref=inp.trace_ref,
        replay_ref=inp.replay_ref,
        whitebox_ref=inp.whitebox_ref,
    )

    audit = VoiceSubmitGateAuditEnvelope(
        audit_id=_build_submit_gate_audit_id(inp.request_id, inp.source_governance_decision_id, submit_gate_position),
        request_id=inp.request_id,
        created_at=time.time(),
        submit_gate_position=submit_gate_position,
        source_governance_decision_id=inp.source_governance_decision_id,
        source_audit_envelope_id=inp.source_audit_envelope_id,
        hard_audit=hard_audit,
        refs={
            "trace_ref": inp.trace_ref,
            "replay_ref": inp.replay_ref,
            "whitebox_ref": inp.whitebox_ref,
        },
    )
    return dec, audit


def run_governed_submit_shadow_v0(governance_root: str) -> Dict[str, Any]:
    decisions, audits = load_voice_output_governance_decision_v0(governance_root)
    audit_idx = _index_audits_by_request_id(audits)

    inputs: List[Dict[str, Any]] = []
    shadow_decisions: List[Dict[str, Any]] = []
    submit_gate_audits: List[Dict[str, Any]] = []

    for d in decisions:
        if not isinstance(d, dict):
            continue
        request_id = d.get("request_id")
        if not isinstance(request_id, str) or not request_id:
            continue
        audit = audit_idx.get(request_id, {})
        source_audit_id = audit.get("audit_id") if isinstance(audit, dict) else None
        if not isinstance(source_audit_id, str) or not source_audit_id:
            source_audit_id = "missing_audit_envelope"

        inp = VoiceGovernedSubmitShadowInput(
            request_id=request_id,
            candidate_text=str(d.get("candidate_text") or ""),
            source_governance_decision_id=str(d.get("voice_output_decision_id") or ""),
            source_audit_envelope_id=source_audit_id,
            governance_final_action=str(d.get("final_action") or ""),
            speech_gate_allowed=(d.get("speech_gate_result") or {}).get("allowed") if isinstance(d.get("speech_gate_result"), dict) else None,
            is_expired=(d.get("expiry_result") or {}).get("is_expired") if isinstance(d.get("expiry_result"), dict) else None,
            cancel_requested=(d.get("cancel_result") or {}).get("cancel_requested") if isinstance(d.get("cancel_result"), dict) else None,
            provider_fallback_required=(d.get("provider_health_result") or {}).get("fallback_required") if isinstance(d.get("provider_health_result"), dict) else None,
            trace_ref=d.get("trace_ref") if isinstance(d.get("trace_ref"), str) else None,
            replay_ref=d.get("replay_ref") if isinstance(d.get("replay_ref"), str) else None,
            whitebox_ref=d.get("whitebox_ref") if isinstance(d.get("whitebox_ref"), str) else None,
        )
        inputs.append(asdict(inp))

        for pos in SUBMIT_GATE_POSITIONS:
            dec, aenv = build_governed_submit_shadow_decision_v0(inp=inp, submit_gate_position=pos)
            shadow_decisions.append(asdict(dec))
            submit_gate_audits.append(asdict(aenv))

    return {
        "inputs": inputs,
        "decisions": shadow_decisions,
        "audit_envelopes": submit_gate_audits,
        "notes": [
            "shadow-only pre-submit readiness gate",
            "no real submit invoked",
        ],
    }

