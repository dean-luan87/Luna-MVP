#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-RuntimeReadiness-003 — Static wiring path mapping + gate snapshot.

Does not enable trials or call providers.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

_repo_insert = Path(__file__).resolve().parents[1]
if str(_repo_insert) not in sys.path:
    sys.path.insert(0, str(_repo_insert))

from capabilities.runtime_readiness.guarded_trial_abort_rollback_hooks_v0 import (
    build_guarded_trial_rollback_plan_v0,
    evaluate_guarded_trial_abort_conditions_v0,
)
from capabilities.runtime_readiness.guarded_trial_gate_v0 import (
    GuardedTrialGateInput,
    evaluate_guarded_trial_gate_v0,
    evaluate_global_guarded_trial_kill_switch_v0,
    evaluate_ocr_guarded_trial_gate_v0,
    evaluate_qwen_voice_guarded_trial_gate_v0,
    evaluate_yolo_guarded_trial_gate_v0,
    read_guarded_trial_env_snapshot_v0,
)
from capabilities.runtime_readiness.guarded_trial_trw_validator_v0 import (
    validate_guarded_trial_trw_fields_v0,
)

PHASE = "Phase-Mainline-RuntimeReadiness-003"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _default_env_for_doc() -> Dict[str, str]:
    """Explicit defaults matching Phase-002 (trial entry flags off)."""
    return {
        "LUNA_DISABLE_ALL_GUARDED_TRIALS": "",
        "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": "",
        "LUNA_YOLO_TRIAL_MODE": "",
        "LUNA_ENABLE_OCR_GUARDED_TRIAL_V1": "",
        "LUNA_OCR_TRIAL_MODE": "",
        "LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION": "",
        "LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1": "",
        "LUNA_QWEN_VOICE_TRIAL_MODE": "",
        "LUNA_QWEN_VOICE_TRIAL_ALLOW_PROVIDER_INVOCATION": "",
        "LUNA_QWEN_VOICE_TRIAL_ALLOW_PLAYBACK": "",
        "LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1": "",
        "LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1": "",
    }


def _wiring_path_matrix(repo: Path) -> List[Dict[str, Any]]:
    """Candidate wiring points — mapping_only for Phase-003."""
    rel = lambda *p: str(Path("capabilities").joinpath(*p)).replace("\\", "/")

    def row(
        capability: str,
        wiring_point: str,
        file_parts: tuple,
        func: str,
        mapped: bool,
        plane: str,
        phase003: str,
        notes: str,
    ) -> Dict[str, Any]:
        return {
            "capability": capability,
            "wiring_point": wiring_point,
            "candidate_file": rel(*file_parts),
            "candidate_function": func,
            "mapped": mapped,
            "enabled_by_default": False,
            "execution_plane": plane,
            "allowed_in_phase_003": phase003,
            "notes": notes,
        }

    return [
        row(
            "yolo",
            "frame_ingestion_point",
            ("model_perception", "yolo_shadow_adapter_v0.py"),
            "run_yolo_shadow_adapter_on_sample_v0",
            True,
            "shadow",
            "mapping_only",
            "Offline/shadow sample adapter; runtime frame hook maps here in later phase.",
        ),
        row(
            "yolo",
            "detector_invocation_point",
            ("model_perception", "yolo_shadow_adapter_v0.py"),
            "run_yolo_shadow_adapter_on_sample_v0",
            True,
            "shadow",
            "mapping_only",
            "Detector invocation contained within shadow adapter until guarded_local wiring.",
        ),
        row(
            "yolo",
            "request_trace_emission_point",
            ("core_trw", "yolo_request_trace_shadow_adapter_v0.py"),
            "build_yolo_request_trace_chain_v0",
            True,
            "shadow",
            "gate_stub_only",
            "Parallel RequestTrace chain builder — gate inserts before emission in future.",
        ),
        row(
            "yolo",
            "abort_hook_point",
            ("runtime_readiness", "guarded_trial_abort_rollback_hooks_v0.py"),
            "evaluate_guarded_trial_abort_conditions_v0",
            True,
            "sandbox",
            "gate_stub_only",
            "Abort predicate placeholder.",
        ),
        row(
            "yolo",
            "rollback_point",
            ("runtime_readiness", "guarded_trial_abort_rollback_hooks_v0.py"),
            "build_guarded_trial_rollback_plan_v0",
            True,
            "sandbox",
            "gate_stub_only",
            "Rollback plan placeholder.",
        ),
        row(
            "ocr",
            "source_policy_selector_point",
            ("model_ocr", "offline_source_policy_v0.py"),
            "select_ocr_offline_source_v0",
            True,
            "shadow",
            "mapping_only",
            "Policy selection — guarded_provider trial attaches gate upstream.",
        ),
        row(
            "ocr",
            "provider_invocation_point",
            ("model_ocr", "paddleocr_adapter_v0.py"),
            "(provider-specific run)",
            False,
            "shadow",
            "mapping_only",
            "Representative adapter path; exact invoke symbol varies by provider.",
        ),
        row(
            "ocr",
            "fallback_not_available_point",
            ("model_ocr", "yolo_ocr_bridge_v0.py"),
            "(bridge proposals → downstream acceptance)",
            True,
            "shadow",
            "mapping_only",
            "Bridge outputs proposals; trial forbids semantic downstream.",
        ),
        row(
            "ocr",
            "request_trace_emission_point",
            ("core_trw", "ocr_request_trace_shadow_adapter_v0.py"),
            "(ocr shadow adapter exports)",
            True,
            "shadow",
            "gate_stub_only",
            "OCR RequestTrace stages emitted via core_trw adapter.",
        ),
        row(
            "ocr",
            "abort_hook_point",
            ("runtime_readiness", "guarded_trial_abort_rollback_hooks_v0.py"),
            "evaluate_guarded_trial_abort_conditions_v0",
            True,
            "sandbox",
            "gate_stub_only",
            "",
        ),
        row(
            "ocr",
            "rollback_point",
            ("runtime_readiness", "guarded_trial_abort_rollback_hooks_v0.py"),
            "build_guarded_trial_rollback_plan_v0",
            True,
            "sandbox",
            "gate_stub_only",
            "",
        ),
        row(
            "qwen_voice",
            "voice_output_governance_decision_point",
            ("voice", "output", "voice_output_governance_v0.py"),
            "build_voice_output_governance_decision_v0",
            True,
            "runtime",
            "mapping_only",
            "Governance decision source — gate must precede governed entry.",
        ),
        row(
            "qwen_voice",
            "governed_voice_provider_entry_point",
            ("voice", "output", "governed_voice_provider_entry_v0.py"),
            "(governed entry exports)",
            True,
            "shadow",
            "mapping_only",
            "GovernedVoiceProviderEntry skeleton — dry-run path.",
        ),
        row(
            "qwen_voice",
            "before_run_tts_unified_entry_point",
            ("voice", "runtime", "tts_unified_entry.py"),
            "run_tts_unified_entry",
            True,
            "runtime",
            "mapping_only",
            "Unified TTS entry — trial never bypasses governance flags.",
        ),
        row(
            "qwen_voice",
            "before_provider_invocation_point",
            ("voice", "output", "voice_output_plane_v1.py"),
            "(VoiceOutputPlaneV1 submit path → run_tts_unified_entry)",
            True,
            "runtime",
            "mapping_only",
            "Plane.submit uses execute_tts flag then run_tts_unified_entry — gate before submit.",
        ),
        row(
            "qwen_voice",
            "request_trace_emission_point",
            ("voice", "output", "voice_output_trw_adapter_v0.py"),
            "(TRW adapter exports)",
            True,
            "shadow",
            "gate_stub_only",
            "Voice TRW / RequestTrace adaptation.",
        ),
        row(
            "qwen_voice",
            "abort_hook_point",
            ("runtime_readiness", "guarded_trial_abort_rollback_hooks_v0.py"),
            "evaluate_guarded_trial_abort_conditions_v0",
            True,
            "sandbox",
            "gate_stub_only",
            "",
        ),
        row(
            "qwen_voice",
            "rollback_point",
            ("runtime_readiness", "guarded_trial_abort_rollback_hooks_v0.py"),
            "build_guarded_trial_rollback_plan_v0",
            True,
            "sandbox",
            "gate_stub_only",
            "",
        ),
    ]


def _trw_validation_matrix() -> List[Dict[str, Any]]:
    good = {
        "request_id": "r1",
        "trace_id": "t1",
        "session_id": "s1",
        "runtime_run_id": "run1",
        "source_run_id": "",
        "hard_audit": {"real_qwen_invoked": False},
        "trace_ref": "tr",
        "replay_ref": "rp",
        "whitebox_ref": "wb",
    }
    bad = {"request_id": "", "hard_audit": {}, "pending_ref": False}
    pending = {
        "request_id": "r2",
        "hard_audit": {"pending_placeholder": True},
        "runtime_run_id": "x",
        "pending_ref": True,
    }
    return [
        {"case": "minimal_ok", "payload": good, **validate_guarded_trial_trw_fields_v0(good)},
        {"case": "blocked_missing_core", "payload": bad, **validate_guarded_trial_trw_fields_v0(bad)},
        {"case": "pending_refs_ok", "payload": pending, **validate_guarded_trial_trw_fields_v0(pending)},
    ]


def _abort_rollback_hook_matrix() -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for cap in ("yolo", "ocr", "qwen_voice"):
        abort = evaluate_guarded_trial_abort_conditions_v0(
            gate_decision="allowed_shadow_only",
            trial_capability=cap,
            signals={},
        )
        rollback = build_guarded_trial_rollback_plan_v0(
            trial_capability=cap,
            gate_decision="allowed_shadow_only",
            abort_payload=abort,
        )
        out.append({"capability": cap, "abort_eval": abort, "rollback_plan": rollback})
    abort_fire = evaluate_guarded_trial_abort_conditions_v0(
        gate_decision="allowed_guarded_local",
        trial_capability="yolo",
        signals={"detector_exception": True},
    )
    rollback_fire = build_guarded_trial_rollback_plan_v0(
        trial_capability="yolo",
        gate_decision="allowed_guarded_local",
        abort_payload=abort_fire,
    )
    out.append(
        {
            "capability": "yolo",
            "scenario": "detector_exception_signal",
            "abort_eval": abort_fire,
            "rollback_plan": rollback_fire,
        }
    )
    return out


def run_evaluation(repo: Path, out_root: Path) -> Dict[str, Any]:
    default_env = _default_env_for_doc()
    snap = read_guarded_trial_env_snapshot_v0(default_env)

    decisions_default = {
        "yolo_guarded_trial_v1": evaluate_yolo_guarded_trial_gate_v0(snap).to_dict(),
        "ocr_guarded_trial_v1": evaluate_ocr_guarded_trial_gate_v0(snap).to_dict(),
        "qwen_voice_governed_entry_trial_v1": evaluate_qwen_voice_guarded_trial_gate_v0(snap).to_dict(),
        "global_kill_switch_engaged": evaluate_global_guarded_trial_kill_switch_v0(snap),
    }

    invalid_env = dict(default_env)
    invalid_env.update(
        {
            "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": "1",
            "LUNA_YOLO_TRIAL_MODE": "not_a_real_mode",
        }
    )
    snap_bad = read_guarded_trial_env_snapshot_v0(invalid_env)
    invalid_mode_probe = {
        "env_override": {"LUNA_YOLO_TRIAL_MODE": "not_a_real_mode", "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": "1"},
        "decision": evaluate_yolo_guarded_trial_gate_v0(snap_bad).to_dict(),
    }

    kill_probe_env = dict(default_env)
    kill_probe_env["LUNA_DISABLE_ALL_GUARDED_TRIALS"] = "1"
    kill_probe_env["LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1"] = "1"
    snap_kill = read_guarded_trial_env_snapshot_v0(kill_probe_env)
    global_kill_probe = {
        "env_override": {"LUNA_DISABLE_ALL_GUARDED_TRIALS": "1", "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": "1"},
        "decision": evaluate_yolo_guarded_trial_gate_v0(snap_kill).to_dict(),
    }

    unified_input = GuardedTrialGateInput(
        trial_name="yolo_guarded_trial_v1",
        capability="yolo",
        env_snapshot=snap,
        trw_payload=None,
    )

    summary: Dict[str, Any] = {
        "phase": PHASE,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo),
        "output_root": str(out_root),
        "constraints": {
            "guarded_trial_wiring_mapping_only": True,
            "no_runtime_activation": True,
            "no_real_provider_calls": True,
            "no_real_qwen": True,
            "no_real_playback": True,
            "no_real_tts": True,
            "no_default_provider_policy_change": True,
            "no_env_semantics_change": True,
            "trials_default_off": True,
        },
        "verdict": {
            "phase_wiring_path_mapping": "GO",
            "implementation_wiring_next_phase": "CONDITIONAL_GO",
            "real_runtime_activation": "NO_GO",
        },
        "gate_evaluators_present": {
            "evaluate_yolo_guarded_trial_gate_v0": True,
            "evaluate_ocr_guarded_trial_gate_v0": True,
            "evaluate_qwen_voice_guarded_trial_gate_v0": True,
            "evaluate_guarded_trial_gate_v0": True,
            "evaluate_global_guarded_trial_kill_switch_v0": True,
        },
        "modules": {
            "gate": "capabilities/runtime_readiness/guarded_trial_gate_v0.py",
            "trw_validator": "capabilities/runtime_readiness/guarded_trial_trw_validator_v0.py",
            "abort_rollback_hooks": "capabilities/runtime_readiness/guarded_trial_abort_rollback_hooks_v0.py",
        },
        "invalid_mode_probe": invalid_mode_probe,
        "global_kill_probe": global_kill_probe,
        "unified_gate_sample": evaluate_guarded_trial_gate_v0(unified_input).to_dict(),
    }

    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "mainline_guarded_trial_wiring_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_gate_decisions.json").write_text(
        json.dumps(
            {
                "default_env_snapshot": asdict(snap),
                "decisions": decisions_default,
                "invalid_mode_probe": invalid_mode_probe,
                "global_kill_probe": global_kill_probe,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_root / "mainline_guarded_trial_wiring_path_matrix.json").write_text(
        json.dumps(_wiring_path_matrix(repo), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_env_snapshot.json").write_text(
        json.dumps({"explicit_defaults_for_evaluation": default_env, "snapshot_fields": snap.__dict__}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_root / "mainline_guarded_trial_trw_validation_matrix.json").write_text(
        json.dumps(_trw_validation_matrix(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_guarded_trial_abort_rollback_hook_matrix.json").write_text(
        json.dumps(_abort_rollback_hook_matrix(), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    notes = [
        f"# {PHASE} — wiring path evaluation",
        "",
        "Artifacts generated without enabling trials or invoking providers.",
        "",
        "## Priority",
        "",
        "`LUNA_DISABLE_ALL_GUARDED_TRIALS` overrides per-trial entry flags.",
        "",
    ]
    (out_root / "evaluation_notes.md").write_text("\n".join(notes), encoding="utf-8")

    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(_repo_root()))
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    out = Path(args.output_root) if args.output_root else repo / "logs" / f"mainline_guarded_trial_wiring_path_003_{_utc_tag()}"
    summary = run_evaluation(repo, out)
    print(json.dumps({"ok": True, "output_root": str(out), "verdict": summary.get("verdict")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
