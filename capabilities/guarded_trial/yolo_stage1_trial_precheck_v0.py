# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-002 — YOLO Stage-1 dry-run precheck (no detector, no camera).

Uses guarded_trial_gate_v0, guarded_trial_trw_validator_v0, guarded_trial_abort_rollback_hooks_v0.
"""

from __future__ import annotations

import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from capabilities.runtime_readiness.guarded_trial_abort_rollback_hooks_v0 import (
    build_guarded_trial_rollback_plan_v0,
    evaluate_guarded_trial_abort_conditions_v0,
)
from capabilities.runtime_readiness.guarded_trial_gate_v0 import (
    evaluate_yolo_guarded_trial_gate_v0,
    read_guarded_trial_env_snapshot_v0,
)
from capabilities.runtime_readiness.guarded_trial_trw_validator_v0 import validate_guarded_trial_trw_fields_v0


@dataclass
class YoloStage1TrialPrecheckInput:
    """Inputs for YOLO Stage-1 precheck (paths checked for writability)."""

    output_root: str
    request_trace_dir: str
    trace_replay_whitebox_dir: str
    trw_payload: Mapping[str, Any]
    env_override: Optional[Mapping[str, str]] = None


@dataclass
class YoloStage1TrialEnvSnapshot:
    """YOLO-focused view; sourced from GuardedTrialEnvSnapshot fields."""

    raw: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.raw)


@dataclass
class YoloStage1RollbackPlan:
    rollback_action: str
    commands: List[str]
    safe_state: str
    retain_logs: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rollback_action": self.rollback_action,
            "commands": list(self.commands),
            "safe_state": self.safe_state,
            "retain_logs": self.retain_logs,
        }


@dataclass
class YoloStage1TrialPrecheckResult:
    trial_id: str
    capability: str
    stage: str
    precheck_mode: str
    would_execute_detector: bool
    detector_invoked: bool
    camera_invoked: bool
    entry_flag_enabled: bool
    global_kill_switch: bool
    single_trial_rule_ok: bool
    output_paths_writable: bool
    request_trace_path_writable: bool
    trace_replay_whitebox_path_writable: bool
    rollback_plan_ready: bool
    abort_conditions_registered: bool
    precheck_result: str
    blockers: List[str]
    warnings: List[str]
    hard_audit: Dict[str, Any]
    debug: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        del d["debug"]
        out = {**d, "debug": dict(self.debug)}
        return out


def build_yolo_stage1_trial_id_v0(*, prefix: str = "yolo_s1") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def read_yolo_stage1_trial_env_snapshot_v0(env_override: Optional[Mapping[str, str]] = None) -> YoloStage1TrialEnvSnapshot:
    snap = read_guarded_trial_env_snapshot_v0(env_override)
    raw = {
        "LUNA_DISABLE_ALL_GUARDED_TRIALS": snap.LUNA_DISABLE_ALL_GUARDED_TRIALS,
        "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": snap.LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1,
        "LUNA_YOLO_TRIAL_MODE": snap.LUNA_YOLO_TRIAL_MODE,
        "LUNA_ENABLE_OCR_GUARDED_TRIAL_V1": snap.LUNA_ENABLE_OCR_GUARDED_TRIAL_V1,
        "LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1": snap.LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1,
    }
    return YoloStage1TrialEnvSnapshot(raw=raw)


def _truthy(raw: Optional[str]) -> bool:
    if raw is None:
        return False
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _dir_writable(p: Path) -> bool:
    try:
        p = p.resolve()
        p.mkdir(parents=True, exist_ok=True)
        test = p / ".yolo_stage1_precheck_write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def validate_yolo_stage1_trial_preconditions_v0(
    inp: YoloStage1TrialPrecheckInput,
    *,
    trial_id: str,
) -> Dict[str, Any]:
    """
    Path checks, single-trial rule (no concurrent OCR/Qwen entry flags), TRW dry validation.
    Does not invoke detector or camera.
    """
    snap = read_guarded_trial_env_snapshot_v0(inp.env_override)
    raw = read_yolo_stage1_trial_env_snapshot_v0(inp.env_override).raw

    global_kill = _truthy(snap.LUNA_DISABLE_ALL_GUARDED_TRIALS)
    yolo_on = _truthy(snap.LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1)
    ocr_on = _truthy(snap.LUNA_ENABLE_OCR_GUARDED_TRIAL_V1)
    qwen_on = _truthy(snap.LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1)

    single_ok = (not ocr_on) and (not qwen_on)

    out_root = Path(inp.output_root)
    rt_dir = Path(inp.request_trace_dir)
    trw_dir = Path(inp.trace_replay_whitebox_dir)

    w_out = _dir_writable(out_root)
    w_rt = _dir_writable(rt_dir)
    w_trw = _dir_writable(trw_dir)

    trw_ok = validate_guarded_trial_trw_fields_v0(inp.trw_payload)

    blockers: List[str] = []
    if not w_out:
        blockers.append("output_root_not_writable")
    if not w_rt:
        blockers.append("request_trace_dir_not_writable")
    if not w_trw:
        blockers.append("trace_replay_whitebox_dir_not_writable")
    if not single_ok:
        blockers.append("ocr_or_qwen_trial_entry_flag_active")
    if not trw_ok.get("valid"):
        blockers.append("trw_validation_failed")

    warnings: List[str] = []
    if global_kill:
        warnings.append("global_kill_switch_engaged_trial_disabled")

    gd = evaluate_yolo_guarded_trial_gate_v0(snap, trw_validation_ok=bool(trw_ok.get("valid")))

    return {
        "trial_id": trial_id,
        "env_raw": raw,
        "global_kill_switch": global_kill,
        "entry_flag_enabled": yolo_on,
        "ocr_entry_active": ocr_on,
        "qwen_entry_active": qwen_on,
        "single_trial_rule_ok": single_ok,
        "output_paths_writable": w_out,
        "request_trace_path_writable": w_rt,
        "trace_replay_whitebox_path_writable": w_trw,
        "trw_validation": trw_ok,
        "gate_decision": gd.to_dict(),
        "blockers": blockers,
        "warnings": warnings,
    }


def build_yolo_stage1_rollback_plan_v0(
    *,
    gate_decision: str,
    abort_payload: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Rollback plan per Phase-GuardedTrial-002 contract (shell commands for documentation only).
    """
    base = build_guarded_trial_rollback_plan_v0(
        trial_capability="yolo",
        gate_decision=gate_decision,
        abort_payload=abort_payload,
    )
    return {
        "rollback_action": "disable_yolo_trial",
        "commands": [
            "unset LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1",
            "export LUNA_DISABLE_ALL_GUARDED_TRIALS=true",
        ],
        "safe_state": "shadow_only",
        "retain_logs": True,
        "gate_rollback_metadata": base,
    }


def run_yolo_stage1_trial_precheck_v0(
    inp: YoloStage1TrialPrecheckInput,
    *,
    trial_id: Optional[str] = None,
) -> YoloStage1TrialPrecheckResult:
    tid = trial_id or build_yolo_stage1_trial_id_v0()
    pre = validate_yolo_stage1_trial_preconditions_v0(inp, trial_id=tid)

    gate_decision = (pre.get("gate_decision") or {}).get("decision") or "unknown"
    abort_eval = evaluate_guarded_trial_abort_conditions_v0(
        gate_decision=str(gate_decision),
        trial_capability="yolo",
        signals={},
    )
    rollback = build_yolo_stage1_rollback_plan_v0(gate_decision=str(gate_decision))

    blockers = list(pre.get("blockers") or [])
    warnings = list(pre.get("warnings") or [])

    rollback_ready = bool(rollback.get("rollback_action")) and bool(rollback.get("commands"))
    abort_registered = True

    paths_ok = (
        pre.get("output_paths_writable")
        and pre.get("request_trace_path_writable")
        and pre.get("trace_replay_whitebox_path_writable")
    )
    rules_ok = pre.get("single_trial_rule_ok") is True and pre.get("trw_validation", {}).get("valid") is True

    would_execute = False

    if blockers:
        verdict = "NO_GO"
    elif paths_ok and rules_ok and rollback_ready and abort_registered:
        if pre.get("entry_flag_enabled") is True:
            verdict = "GO"
        else:
            verdict = "CONDITIONAL_GO"
            if not warnings:
                warnings.append("entry_flag_disabled_default_no_trial_execution")
    else:
        verdict = "NO_GO"

    hard_audit = {
        "runtime_invoked": False,
        "detector_invoked": False,
        "provider_invoked": False,
        "playback_invoked": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "world_write_invoked": False,
    }

    return YoloStage1TrialPrecheckResult(
        trial_id=tid,
        capability="yolo",
        stage="stage1_yolo_guarded_trial",
        precheck_mode="dry_run_precheck",
        would_execute_detector=would_execute,
        detector_invoked=False,
        camera_invoked=False,
        entry_flag_enabled=bool(pre.get("entry_flag_enabled")),
        global_kill_switch=bool(pre.get("global_kill_switch")),
        single_trial_rule_ok=bool(pre.get("single_trial_rule_ok")),
        output_paths_writable=bool(pre.get("output_paths_writable")),
        request_trace_path_writable=bool(pre.get("request_trace_path_writable")),
        trace_replay_whitebox_path_writable=bool(pre.get("trace_replay_whitebox_path_writable")),
        rollback_plan_ready=rollback_ready,
        abort_conditions_registered=abort_registered,
        precheck_result=verdict,
        blockers=blockers,
        warnings=warnings,
        hard_audit=hard_audit,
        debug={
            "ts": time.time(),
            "abort_evaluation": abort_eval,
            "rollback_plan": rollback,
            "trw_validation": pre.get("trw_validation"),
            "gate_decision": pre.get("gate_decision"),
        },
    )
