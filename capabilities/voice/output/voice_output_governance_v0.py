# -*- coding: utf-8 -*-
"""
Phase-Voice-OutputGovernance-002
Voice Output Governance Minimal Skeleton v0 (offline-safe / dry-run only).

Hard boundaries:
- MUST NOT invoke real TTS providers.
- MUST NOT invoke playback.
- MUST NOT perform navigation actions.
- MUST NOT write world model.
- MUST emit auditable decision objects with real_tts_invoked/playback_invoked/provider_invoked all false.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

from capabilities.voice.schemas.speech_request import SpeechRequest


PriorityLabel = str  # safety|navigation|task|chat|debug (string enum by contract)


def _now() -> float:
    return time.time()


def _coerce_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return None


def _priority_rank(label: PriorityLabel) -> int:
    # Higher rank => higher priority.
    m = {
        "debug": 0,
        "chat": 1,
        "task": 2,
        "navigation": 3,
        "safety": 4,
    }
    return int(m.get(str(label or "").strip().lower(), 1))


@dataclass(frozen=True)
class SpeakableGuardResult:
    guard_name: str
    speakable: bool
    reason: Optional[str] = None
    guard_profile: str = "v1_minimal"
    normalized_text: str = ""
    degraded: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


def guard_v1_speakable_text(
    text: str,
    *,
    profile: str = "v1_minimal",
    max_len: int = 160,
) -> SpeakableGuardResult:
    """
    Minimal, importable speakable guard (Phase-002 hard gate).

    Notes:
    - This is NOT a full safety system. It is a conservative, offline-safe guard.
    - It must be callable and auditable; it must not depend on runtime providers.
    """
    raw = str(text or "")
    t = raw.strip()
    if not t:
        return SpeakableGuardResult(
            guard_name="guard_v1_speakable_text",
            speakable=False,
            reason="empty_text",
            guard_profile=profile,
            normalized_text="",
        )

    low = t.lower()
    # Block obvious placeholders/internal markers.
    placeholder_tokens = ("todo", "placeholder", "unknown", "n/a", "none")
    if any(tok in low for tok in placeholder_tokens) or "占位" in t or "内部" in t:
        return SpeakableGuardResult(
            guard_name="guard_v1_speakable_text",
            speakable=False,
            reason="placeholder_or_internal",
            guard_profile=profile,
            normalized_text="",
        )

    # Normalize length (avoid accidental long speech).
    degraded = False
    if len(t) > int(max_len):
        t = t[: int(max_len)]
        degraded = True

    # "Uncertain must not be certain": if mixing uncertainty with absolute certainty, degrade certainty tokens.
    # Example: "可能...但肯定..." -> replace certainty with "大概率".
    if ("可能" in t or "不确定" in t or "大概" in t) and any(x in t for x in ("一定", "肯定", "百分之百", "绝对")):
        for x in ("百分之百", "绝对", "肯定", "一定"):
            if x in t:
                t = t.replace(x, "大概率")
                degraded = True

    return SpeakableGuardResult(
        guard_name="guard_v1_speakable_text",
        speakable=True,
        reason=None,
        guard_profile=profile,
        normalized_text=t,
        degraded=degraded,
        metadata={"raw_len": len(raw), "final_len": len(t)},
    )


@dataclass(frozen=True)
class SpeechGateResultV0:
    gate_invoked: bool
    allowed: bool
    reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def evaluate_speech_gate_v0(
    *,
    scene_hash: Optional[str],
    user_speaking: bool,
    gate_owner: str,
) -> SpeechGateResultV0:
    """
    Invoke SpeechGate (by contract) but keep it dry-run safe.
    """
    try:
        from core.speech_gate import SpeechGate  # type: ignore

        g = SpeechGate()
        allowed, reason = g.can_speak(scene_hash=scene_hash, user_speaking=bool(user_speaking))
        # We do NOT acquire/release here because Phase-002 does not actually play audio.
        return SpeechGateResultV0(
            gate_invoked=True,
            allowed=bool(allowed),
            reason=str(reason),
            metadata={"gate_owner": str(gate_owner or "unknown")},
        )
    except Exception as e:
        return SpeechGateResultV0(
            gate_invoked=True,
            allowed=False,
            reason="speech_gate_exception",
            metadata={"error": f"{type(e).__name__}", "gate_owner": str(gate_owner or "unknown")},
        )


@dataclass(frozen=True)
class ExpiryResultV0:
    is_expired: bool
    expires_at: Optional[float] = None
    stale_suppressed: bool = False
    reason: Optional[str] = None


def evaluate_voice_output_expiry_v0(
    *,
    now: float,
    expires_at: Optional[float],
    stale: bool,
) -> ExpiryResultV0:
    exp = _coerce_float(expires_at)
    if stale:
        return ExpiryResultV0(is_expired=False, expires_at=exp, stale_suppressed=True, reason="stale")
    if exp is not None and float(now) > float(exp):
        return ExpiryResultV0(is_expired=True, expires_at=exp, stale_suppressed=False, reason="expired")
    return ExpiryResultV0(is_expired=False, expires_at=exp, stale_suppressed=False, reason=None)


@dataclass(frozen=True)
class PriorityResultV0:
    priority: PriorityLabel
    interrupt_allowed: bool
    interrupt_decision: str  # not_applicable|allowed|denied
    reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def evaluate_voice_output_priority_v0(
    *,
    request_priority: PriorityLabel,
    current_playing_priority: Optional[PriorityLabel],
    interrupt_requested: bool,
    interrupt_allowed_by_policy: bool,
    request_interruptible: bool,
) -> PriorityResultV0:
    rp = str(request_priority or "chat").strip().lower()
    cp = str(current_playing_priority or "").strip().lower() if current_playing_priority else None

    if not interrupt_requested or not cp:
        return PriorityResultV0(priority=rp, interrupt_allowed=False, interrupt_decision="not_applicable")

    if not request_interruptible:
        return PriorityResultV0(
            priority=rp,
            interrupt_allowed=False,
            interrupt_decision="denied",
            reason="request_not_interruptible",
        )

    if not interrupt_allowed_by_policy:
        return PriorityResultV0(priority=rp, interrupt_allowed=False, interrupt_decision="denied", reason="policy_denied")

    if _priority_rank(rp) <= _priority_rank(cp):
        return PriorityResultV0(
            priority=rp,
            interrupt_allowed=False,
            interrupt_decision="denied",
            reason="lower_or_equal_priority_cannot_interrupt",
            metadata={"current_playing_priority": cp},
        )

    return PriorityResultV0(
        priority=rp,
        interrupt_allowed=True,
        interrupt_decision="allowed",
        reason="higher_priority_interrupt",
        metadata={"current_playing_priority": cp},
    )


@dataclass(frozen=True)
class CancelResultV0:
    cancel_requested: bool
    cancelled: bool
    reason: Optional[str] = None


def evaluate_voice_output_cancellation_v0(*, cancel_requested: bool) -> CancelResultV0:
    if cancel_requested:
        return CancelResultV0(cancel_requested=True, cancelled=True, reason="cancel_requested")
    return CancelResultV0(cancel_requested=False, cancelled=False, reason=None)


@dataclass(frozen=True)
class SuppressionResultV0:
    suppressed: bool
    suppression_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def evaluate_voice_output_suppression_v0(
    *,
    guard: SpeakableGuardResult,
    gate: SpeechGateResultV0,
    expiry: ExpiryResultV0,
    cancel: CancelResultV0,
    duplicate_suppressed: bool,
) -> SuppressionResultV0:
    if cancel.cancelled:
        return SuppressionResultV0(suppressed=True, suppression_reason="cancelled")
    if not guard.speakable:
        return SuppressionResultV0(suppressed=True, suppression_reason=f"guard_blocked:{guard.reason}")
    if not gate.allowed:
        return SuppressionResultV0(suppressed=True, suppression_reason=f"speech_gate_blocked:{gate.reason}")
    if expiry.stale_suppressed:
        return SuppressionResultV0(suppressed=True, suppression_reason="stale")
    if expiry.is_expired:
        return SuppressionResultV0(suppressed=True, suppression_reason="expired")
    if duplicate_suppressed:
        return SuppressionResultV0(suppressed=True, suppression_reason="duplicate_or_cooldown")
    return SuppressionResultV0(suppressed=False, suppression_reason=None)


@dataclass(frozen=True)
class VoiceProviderHealthStateV0:
    provider_id: str
    provider_status: str  # healthy|degraded|unhealthy|unavailable
    dependency_ready: bool = False
    avg_latency_ms: Optional[float] = None
    p95_latency_ms: Optional[float] = None
    failure_count: int = 0
    timeout_count: int = 0
    circuit_breaker_state: str = "closed"  # closed|open|half_open
    fallback_candidates: List[str] = field(default_factory=list)
    runtime_invoked: bool = False


@dataclass(frozen=True)
class ProviderHealthResultV0:
    provider_id: str
    provider_status: str
    fallback_required: bool
    reason: Optional[str] = None


def evaluate_tts_provider_health_v0(
    *,
    provider_id: str,
    provider_status: str,
    dependency_ready: bool,
) -> Tuple[VoiceProviderHealthStateV0, ProviderHealthResultV0]:
    pid = str(provider_id or "dry_run_provider")
    st = str(provider_status or "healthy").strip().lower()
    dep = bool(dependency_ready)

    # Dry-run provider is always "safe" in Phase-002: it never invokes runtime and never forces fallback.
    if pid == "dry_run_provider":
        state = VoiceProviderHealthStateV0(
            provider_id=pid,
            provider_status="healthy",
            dependency_ready=True,
            circuit_breaker_state="closed",
            fallback_candidates=[],
            runtime_invoked=False,
        )
        return state, ProviderHealthResultV0(provider_id=pid, provider_status="healthy", fallback_required=False, reason="dry_run_provider")

    # Minimal skeleton:
    # - unhealthy/unavailable => require fallback_candidate
    # - dependency not ready but otherwise healthy => degraded, but do not force fallback in Phase-002
    if st in ("unhealthy", "unavailable"):
        state = VoiceProviderHealthStateV0(
            provider_id=pid,
            provider_status=st,
            dependency_ready=dep,
            circuit_breaker_state="open" if st in ("unhealthy", "unavailable") else "half_open",
            fallback_candidates=["dry_run_provider"],
            runtime_invoked=False,
        )
        return state, ProviderHealthResultV0(
            provider_id=pid,
            provider_status=st,
            fallback_required=True,
            reason="provider_unhealthy_or_dependency_not_ready",
        )

    if not dep:
        state = VoiceProviderHealthStateV0(
            provider_id=pid,
            provider_status="degraded",
            dependency_ready=False,
            circuit_breaker_state="half_open",
            fallback_candidates=["dry_run_provider"],
            runtime_invoked=False,
        )
        return state, ProviderHealthResultV0(
            provider_id=pid,
            provider_status="degraded",
            fallback_required=False,
            reason="dependency_not_ready_degraded_only",
        )

    state = VoiceProviderHealthStateV0(
        provider_id=pid,
        provider_status=st,
        dependency_ready=dep,
        circuit_breaker_state="closed",
        fallback_candidates=[],
        runtime_invoked=False,
    )
    return state, ProviderHealthResultV0(provider_id=pid, provider_status=st, fallback_required=False, reason=None)


@dataclass(frozen=True)
class VoiceOutputGovernanceInputV0:
    request: SpeechRequest
    now: float
    priority_label: PriorityLabel = "chat"
    expires_at: Optional[float] = None
    stale: bool = False
    cancel_requested: bool = False
    interrupt_requested: bool = False
    interrupt_allowed_by_policy: bool = False
    current_playing_priority: Optional[PriorityLabel] = None
    user_speaking: bool = False
    scene_hash: Optional[str] = None
    cooldown_keys_seen: List[str] = field(default_factory=list)
    provider_id: str = "dry_run_provider"
    provider_status: str = "healthy"
    dependency_ready: bool = False


@dataclass(frozen=True)
class VoiceOutputAuditEnvelopeV0:
    audit_id: str
    request_id: str
    created_at: float
    governance_version: str
    invariants: Dict[str, Any]
    decision_ref: str
    trace_ref: str
    replay_ref: str
    whitebox_ref: str


@dataclass(frozen=True)
class VoiceOutputGovernanceDecisionV0:
    voice_output_decision_id: str
    request_id: str
    candidate_text: str
    guard_result: Dict[str, Any]
    speech_gate_result: Dict[str, Any]
    expiry_result: Dict[str, Any]
    priority_result: Dict[str, Any]
    cancel_result: Dict[str, Any]
    suppression_result: Dict[str, Any]
    provider_health_result: Dict[str, Any]
    final_action: str  # accepted_dry_run|suppressed|cancelled|fallback_candidate|rejected
    governance: Dict[str, Any]
    trace_ref: str
    replay_ref: str
    whitebox_ref: str


def build_voice_output_governance_decision_v0(
    inp: VoiceOutputGovernanceInputV0,
) -> Tuple[VoiceOutputGovernanceDecisionV0, VoiceProviderHealthStateV0, VoiceOutputAuditEnvelopeV0, Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    rid = str(inp.request.request_id or "")
    did = f"vod_{uuid.uuid4().hex[:12]}"
    candidate = str(inp.request.text_candidate or "")

    guard = guard_v1_speakable_text(candidate, profile="v1_minimal")
    gate = evaluate_speech_gate_v0(
        scene_hash=inp.scene_hash,
        user_speaking=bool(inp.user_speaking),
        gate_owner="voice_output_governance_v0",
    )
    expiry = evaluate_voice_output_expiry_v0(now=float(inp.now), expires_at=inp.expires_at, stale=bool(inp.stale))
    cancel = evaluate_voice_output_cancellation_v0(cancel_requested=bool(inp.cancel_requested))

    # duplicate/cooldown suppression
    dup = False
    ck = str(inp.request.cooldown_key or "").strip()
    if ck and bool(inp.request.dedup_allowed):
        if ck in set(str(x) for x in (inp.cooldown_keys_seen or [])):
            dup = True

    pr = evaluate_voice_output_priority_v0(
        request_priority=str(inp.priority_label or "chat"),
        current_playing_priority=inp.current_playing_priority,
        interrupt_requested=bool(inp.interrupt_requested),
        interrupt_allowed_by_policy=bool(inp.interrupt_allowed_by_policy),
        request_interruptible=bool(inp.request.interruptible),
    )

    state, ph = evaluate_tts_provider_health_v0(
        provider_id=str(inp.provider_id or "dry_run_provider"),
        provider_status=str(inp.provider_status or "healthy"),
        dependency_ready=bool(inp.dependency_ready),
    )

    suppression = evaluate_voice_output_suppression_v0(
        guard=guard,
        gate=gate,
        expiry=expiry,
        cancel=cancel,
        duplicate_suppressed=dup,
    )

    final_action = "accepted_dry_run"
    if cancel.cancelled:
        final_action = "cancelled"
    elif suppression.suppressed:
        final_action = "suppressed"
    elif pr.interrupt_decision == "denied":
        final_action = "suppressed"
        suppression = SuppressionResultV0(suppressed=True, suppression_reason="interrupt_denied", metadata=pr.metadata)
    elif ph.fallback_required:
        final_action = "fallback_candidate"

    governance = {
        "real_tts_invoked": False,
        "playback_invoked": False,
        "provider_invoked": False,
        "navigation_action": None,
        "downstream_invocation_count": 0,
    }

    trace_ref = f"trace:{rid}:{did}"
    replay_ref = f"replay:{rid}:{did}"
    whitebox_ref = f"whitebox:{rid}:{did}"

    decision = VoiceOutputGovernanceDecisionV0(
        voice_output_decision_id=did,
        request_id=rid,
        candidate_text=candidate,
        guard_result=asdict(guard),
        speech_gate_result=asdict(gate),
        expiry_result=asdict(expiry),
        priority_result=asdict(pr),
        cancel_result=asdict(cancel),
        suppression_result=asdict(suppression),
        provider_health_result=asdict(ph),
        final_action=str(final_action),
        governance=governance,
        trace_ref=trace_ref,
        replay_ref=replay_ref,
        whitebox_ref=whitebox_ref,
    )

    # Minimal trace/replay/whitebox payloads (caller decides how to persist).
    trace = {
        "type": "voice_output_trace_v0",
        "timestamp": float(inp.now),
        "request_id": rid,
        "priority": str(inp.priority_label),
        "expires_at": _coerce_float(inp.expires_at),
        "guard_result": decision.guard_result,
        "speech_gate_result": decision.speech_gate_result,
        "expiry_result": decision.expiry_result,
        "cancel_result": decision.cancel_result,
        "interrupt_result": {"interrupt_decision": decision.priority_result.get("interrupt_decision"), "reason": decision.priority_result.get("reason")},
        "provider_health_result": decision.provider_health_result,
        "final_action": decision.final_action,
        "real_tts_invoked": False,
    }
    replay = {
        "type": "voice_output_replay_v0",
        "timestamp": float(inp.now),
        "request_id": rid,
        "input_request_ref": {"request_id": rid, "source_module": inp.request.source_module, "output_category": inp.request.output_category},
        "guard_policy_ref": {"guard_name": "guard_v1_speakable_text", "profile": "v1_minimal"},
        "speech_gate_policy_ref": {"gate": "SpeechGate", "version": "v1"},
        "provider_health_ref": {"provider_id": state.provider_id, "provider_status": state.provider_status},
        "decision_ref": {"voice_output_decision_id": did},
    }
    whitebox = {
        "type": "voice_output_whitebox_v0",
        "timestamp": float(inp.now),
        "request_id": rid,
        "why_spoken_dry_run": (decision.final_action == "accepted_dry_run"),
        "why_suppressed": decision.final_action == "suppressed",
        "why_expired": suppression.suppression_reason == "expired",
        "why_cancelled": suppression.suppression_reason == "cancelled",
        "why_interrupt_allowed": decision.priority_result.get("interrupt_decision") == "allowed",
        "why_interrupt_denied": suppression.suppression_reason == "interrupt_denied",
        "why_provider_blocked": decision.final_action == "fallback_candidate",
        "why_guard_blocked": str(suppression.suppression_reason or "").startswith("guard_blocked"),
        "reason": suppression.suppression_reason,
    }

    audit = VoiceOutputAuditEnvelopeV0(
        audit_id=f"voa_{uuid.uuid4().hex[:12]}",
        request_id=rid,
        created_at=_now(),
        governance_version="voice_output_governance_v0",
        invariants=governance,
        decision_ref=decision.voice_output_decision_id,
        trace_ref=trace_ref,
        replay_ref=replay_ref,
        whitebox_ref=whitebox_ref,
    )
    return decision, state, audit, trace, replay, whitebox


def run_voice_output_governance_v0(
    inp: VoiceOutputGovernanceInputV0,
) -> Tuple[VoiceOutputGovernanceDecisionV0, VoiceProviderHealthStateV0, VoiceOutputAuditEnvelopeV0, Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    return build_voice_output_governance_decision_v0(inp)

