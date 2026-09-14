# -*- coding: utf-8 -*-
"""
Guarded trial gate v0 — Phase-Mainline-RuntimeReadiness-003.

Definition-only gate evaluation: does not invoke providers, detectors, or TTS.
All trial entry paths default to disabled unless env explicitly enables them.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Mapping, Optional, Tuple

Capability = Literal["yolo", "ocr", "qwen_voice"]
TrialName = Literal[
    "yolo_guarded_trial_v1",
    "ocr_guarded_trial_v1",
    "qwen_voice_governed_entry_trial_v1",
]


def _truthy(raw: Optional[str]) -> bool:
    if raw is None:
        return False
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _norm_mode(raw: Optional[str]) -> str:
    return (raw or "").strip().lower() or "shadow_only"


YOLO_ALLOWED_MODES = frozenset({"shadow_only", "guarded_local"})
OCR_ALLOWED_MODES = frozenset({"shadow_only", "guarded_provider"})
QWEN_VOICE_ALLOWED_MODES = frozenset(
    {"shadow_only", "governed_entry", "provider_dry_run", "controlled_provider"}
)


@dataclass
class GuardedTrialEnvSnapshot:
    """Subset of env relevant to guarded trials (string values as in os.environ)."""

    LUNA_DISABLE_ALL_GUARDED_TRIALS: str = ""
    LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1: str = ""
    LUNA_YOLO_TRIAL_MODE: str = ""
    LUNA_ENABLE_OCR_GUARDED_TRIAL_V1: str = ""
    LUNA_OCR_TRIAL_MODE: str = ""
    LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION: str = ""
    LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1: str = ""
    LUNA_QWEN_VOICE_TRIAL_MODE: str = ""
    LUNA_QWEN_VOICE_TRIAL_ALLOW_PROVIDER_INVOCATION: str = ""
    LUNA_QWEN_VOICE_TRIAL_ALLOW_PLAYBACK: str = ""
    LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1: str = ""
    LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1: str = ""


@dataclass
class GuardedTrialGateInput:
    trial_name: TrialName
    capability: Capability
    env_snapshot: GuardedTrialEnvSnapshot
    trw_payload: Optional[Dict[str, Any]] = None


@dataclass
class GuardedTrialGateDecision:
    trial_name: str
    capability: str
    global_kill_switch: bool
    entry_flag_enabled: bool
    trial_mode: str
    decision: str
    default_enabled: bool = False
    runtime_invocation_allowed: bool = False
    provider_invocation_allowed: bool = False
    playback_allowed: bool = False
    downstream_allowed: bool = False
    world_write_allowed: bool = False
    requires_trw_validation: bool = True
    requires_abort_switch: bool = True
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trial_name": self.trial_name,
            "capability": self.capability,
            "global_kill_switch": self.global_kill_switch,
            "entry_flag_enabled": self.entry_flag_enabled,
            "trial_mode": self.trial_mode,
            "decision": self.decision,
            "default_enabled": self.default_enabled,
            "runtime_invocation_allowed": self.runtime_invocation_allowed,
            "provider_invocation_allowed": self.provider_invocation_allowed,
            "playback_allowed": self.playback_allowed,
            "downstream_allowed": self.downstream_allowed,
            "world_write_allowed": self.world_write_allowed,
            "requires_trw_validation": self.requires_trw_validation,
            "requires_abort_switch": self.requires_abort_switch,
            "notes": list(self.notes),
        }


def read_guarded_trial_env_snapshot_v0(env: Optional[Mapping[str, str]] = None) -> GuardedTrialEnvSnapshot:
    src = env if env is not None else os.environ
    def g(key: str) -> str:
        return str(src.get(key, "") or "")

    return GuardedTrialEnvSnapshot(
        LUNA_DISABLE_ALL_GUARDED_TRIALS=g("LUNA_DISABLE_ALL_GUARDED_TRIALS"),
        LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1=g("LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1"),
        LUNA_YOLO_TRIAL_MODE=g("LUNA_YOLO_TRIAL_MODE"),
        LUNA_ENABLE_OCR_GUARDED_TRIAL_V1=g("LUNA_ENABLE_OCR_GUARDED_TRIAL_V1"),
        LUNA_OCR_TRIAL_MODE=g("LUNA_OCR_TRIAL_MODE"),
        LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION=g("LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION"),
        LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1=g("LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1"),
        LUNA_QWEN_VOICE_TRIAL_MODE=g("LUNA_QWEN_VOICE_TRIAL_MODE"),
        LUNA_QWEN_VOICE_TRIAL_ALLOW_PROVIDER_INVOCATION=g("LUNA_QWEN_VOICE_TRIAL_ALLOW_PROVIDER_INVOCATION"),
        LUNA_QWEN_VOICE_TRIAL_ALLOW_PLAYBACK=g("LUNA_QWEN_VOICE_TRIAL_ALLOW_PLAYBACK"),
        LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1=g("LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1"),
        LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1=g("LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1"),
    )


def evaluate_global_guarded_trial_kill_switch_v0(snapshot: GuardedTrialEnvSnapshot) -> bool:
    return _truthy(snapshot.LUNA_DISABLE_ALL_GUARDED_TRIALS)


def _base_denials() -> Tuple[bool, bool, bool, bool, bool]:
    """runtime_invocation, provider, playback, downstream, world_write — default all False."""
    return False, False, False, False, False


def _merge_trw_block(
    decision: GuardedTrialGateDecision,
    trw_ok: Optional[bool],
    needs_trw: bool,
) -> None:
    if not needs_trw:
        return
    if trw_ok is None:
        decision.decision = "blocked_missing_trw"
        decision.notes.append("trw_required_but_not_provided_or_not_validated")
        return
    if trw_ok is False:
        decision.decision = "blocked_missing_trw"
        decision.notes.append("trw_validation_failed")


def evaluate_yolo_guarded_trial_gate_v0(
    snapshot: GuardedTrialEnvSnapshot,
    trw_validation_ok: Optional[bool] = None,
) -> GuardedTrialGateDecision:
    gk = evaluate_global_guarded_trial_kill_switch_v0(snapshot)
    entry = _truthy(snapshot.LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1)
    mode_raw = _norm_mode(snapshot.LUNA_YOLO_TRIAL_MODE or "shadow_only")
    mode_ok = mode_raw in YOLO_ALLOWED_MODES
    trial_mode_out = mode_raw if mode_ok else "invalid"

    ri, prov, pb, ds, ww = _base_denials()

    if gk:
        d = GuardedTrialGateDecision(
            trial_name="yolo_guarded_trial_v1",
            capability="yolo",
            global_kill_switch=True,
            entry_flag_enabled=entry,
            trial_mode=trial_mode_out,
            decision="forced_disabled_by_global_kill",
            runtime_invocation_allowed=False,
            provider_invocation_allowed=False,
            playback_allowed=False,
            downstream_allowed=False,
            world_write_allowed=False,
            notes=["global_kill_switch_engaged"],
        )
        return d

    if not entry:
        return GuardedTrialGateDecision(
            trial_name="yolo_guarded_trial_v1",
            capability="yolo",
            global_kill_switch=False,
            entry_flag_enabled=False,
            trial_mode="shadow_only",
            decision="disabled",
        )

    if not mode_ok:
        return GuardedTrialGateDecision(
            trial_name="yolo_guarded_trial_v1",
            capability="yolo",
            global_kill_switch=False,
            entry_flag_enabled=True,
            trial_mode="invalid",
            decision="blocked_invalid_mode",
            notes=[f"unsupported_mode:{mode_raw}"],
        )

    decision_str = "allowed_shadow_only" if mode_raw == "shadow_only" else "allowed_guarded_local"
    needs_trw = mode_raw == "guarded_local"
    d = GuardedTrialGateDecision(
        trial_name="yolo_guarded_trial_v1",
        capability="yolo",
        global_kill_switch=False,
        entry_flag_enabled=True,
        trial_mode=mode_raw,
        decision=decision_str,
        runtime_invocation_allowed=(mode_raw == "guarded_local"),
        provider_invocation_allowed=False,
        playback_allowed=False,
        downstream_allowed=False,
        world_write_allowed=False,
        notes=[],
    )
    _merge_trw_block(d, trw_validation_ok, needs_trw)
    return d


def evaluate_ocr_guarded_trial_gate_v0(
    snapshot: GuardedTrialEnvSnapshot,
    trw_validation_ok: Optional[bool] = None,
) -> GuardedTrialGateDecision:
    gk = evaluate_global_guarded_trial_kill_switch_v0(snapshot)
    entry = _truthy(snapshot.LUNA_ENABLE_OCR_GUARDED_TRIAL_V1)
    mode_raw = _norm_mode(snapshot.LUNA_OCR_TRIAL_MODE or "shadow_only")
    mode_ok = mode_raw in OCR_ALLOWED_MODES
    trial_mode_out = mode_raw if mode_ok else "invalid"
    allow_prov = _truthy(snapshot.LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION)

    if gk:
        return GuardedTrialGateDecision(
            trial_name="ocr_guarded_trial_v1",
            capability="ocr",
            global_kill_switch=True,
            entry_flag_enabled=entry,
            trial_mode=trial_mode_out,
            decision="forced_disabled_by_global_kill",
            notes=["global_kill_switch_engaged"],
        )

    if not entry:
        return GuardedTrialGateDecision(
            trial_name="ocr_guarded_trial_v1",
            capability="ocr",
            global_kill_switch=False,
            entry_flag_enabled=False,
            trial_mode="shadow_only",
            decision="disabled",
        )

    if not mode_ok:
        return GuardedTrialGateDecision(
            trial_name="ocr_guarded_trial_v1",
            capability="ocr",
            global_kill_switch=False,
            entry_flag_enabled=True,
            trial_mode="invalid",
            decision="blocked_invalid_mode",
            notes=[f"unsupported_mode:{mode_raw}"],
        )

    decision_str = "allowed_shadow_only" if mode_raw == "shadow_only" else "allowed_guarded_local"
    needs_trw = mode_raw == "guarded_provider"
    d = GuardedTrialGateDecision(
        trial_name="ocr_guarded_trial_v1",
        capability="ocr",
        global_kill_switch=False,
        entry_flag_enabled=True,
        trial_mode=mode_raw,
        decision=decision_str,
        runtime_invocation_allowed=False,
        provider_invocation_allowed=allow_prov and mode_raw == "guarded_provider",
        playback_allowed=False,
        downstream_allowed=False,
        world_write_allowed=False,
    )
    _merge_trw_block(d, trw_validation_ok, needs_trw)
    return d


def evaluate_qwen_voice_guarded_trial_gate_v0(
    snapshot: GuardedTrialEnvSnapshot,
    trw_validation_ok: Optional[bool] = None,
) -> GuardedTrialGateDecision:
    gk = evaluate_global_guarded_trial_kill_switch_v0(snapshot)
    entry = _truthy(snapshot.LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1)
    mode_raw = _norm_mode(snapshot.LUNA_QWEN_VOICE_TRIAL_MODE or "shadow_only")
    mode_ok = mode_raw in QWEN_VOICE_ALLOWED_MODES
    trial_mode_out = mode_raw if mode_ok else "invalid"
    allow_prov = _truthy(snapshot.LUNA_QWEN_VOICE_TRIAL_ALLOW_PROVIDER_INVOCATION)
    allow_pb = _truthy(snapshot.LUNA_QWEN_VOICE_TRIAL_ALLOW_PLAYBACK)

    if gk:
        return GuardedTrialGateDecision(
            trial_name="qwen_voice_governed_entry_trial_v1",
            capability="qwen_voice",
            global_kill_switch=True,
            entry_flag_enabled=entry,
            trial_mode=trial_mode_out,
            decision="forced_disabled_by_global_kill",
            notes=["global_kill_switch_engaged"],
        )

    if not entry:
        return GuardedTrialGateDecision(
            trial_name="qwen_voice_governed_entry_trial_v1",
            capability="qwen_voice",
            global_kill_switch=False,
            entry_flag_enabled=False,
            trial_mode="shadow_only",
            decision="disabled",
        )

    if not mode_ok:
        return GuardedTrialGateDecision(
            trial_name="qwen_voice_governed_entry_trial_v1",
            capability="qwen_voice",
            global_kill_switch=False,
            entry_flag_enabled=True,
            trial_mode="invalid",
            decision="blocked_invalid_mode",
            notes=[f"unsupported_mode:{mode_raw}"],
        )

    # Map mode -> decision label (schema-compatible)
    mode_to_decision = {
        "shadow_only": "allowed_shadow_only",
        "governed_entry": "allowed_guarded_local",
        "provider_dry_run": "allowed_guarded_local",
        "controlled_provider": "allowed_guarded_local",
    }
    decision_str = mode_to_decision.get(mode_raw, "allowed_shadow_only")
    needs_trw = mode_raw in {"controlled_provider", "provider_dry_run", "governed_entry"}

    d = GuardedTrialGateDecision(
        trial_name="qwen_voice_governed_entry_trial_v1",
        capability="qwen_voice",
        global_kill_switch=False,
        entry_flag_enabled=True,
        trial_mode=mode_raw,
        decision=decision_str,
        runtime_invocation_allowed=mode_raw in {"governed_entry", "provider_dry_run", "controlled_provider"},
        provider_invocation_allowed=allow_prov and mode_raw == "controlled_provider",
        playback_allowed=allow_pb and mode_raw == "controlled_provider",
        downstream_allowed=False,
        world_write_allowed=False,
    )
    _merge_trw_block(d, trw_validation_ok, needs_trw)
    return d


def evaluate_guarded_trial_gate_v0(inp: GuardedTrialGateInput) -> GuardedTrialGateDecision:
    trw_ok: Optional[bool] = None
    if inp.trw_payload is not None:
        from capabilities.runtime_readiness.guarded_trial_trw_validator_v0 import (
            validate_guarded_trial_trw_fields_v0,
        )

        trw_ok = bool(validate_guarded_trial_trw_fields_v0(inp.trw_payload).get("valid"))

    if inp.capability == "yolo":
        return evaluate_yolo_guarded_trial_gate_v0(inp.env_snapshot, trw_validation_ok=trw_ok)
    if inp.capability == "ocr":
        return evaluate_ocr_guarded_trial_gate_v0(inp.env_snapshot, trw_validation_ok=trw_ok)
    if inp.capability == "qwen_voice":
        return evaluate_qwen_voice_guarded_trial_gate_v0(inp.env_snapshot, trw_validation_ok=trw_ok)
    raise ValueError(f"unknown capability: {inp.capability}")
