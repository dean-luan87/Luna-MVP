# -*- coding: utf-8 -*-
"""
Phase-Voice-Qianwen-002 — Governed Voice Provider Entry skeleton v0 (offline / dry-run only).

Hard boundaries:
- MUST NOT invoke real Qwen / DashScope / Piper executable / remote TTS.
- MUST NOT invoke playback.
- MUST NOT modify voice_tts_config.yaml or change default runtime policy.
- MUST preserve hard_audit invariants (real_* false, invocation counts 0).
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ProviderMode = str  # "online_prefer_qwen" | "offline_only"


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def load_voice_governance_decisions_v0(governance_root: str) -> List[Dict[str, Any]]:
    """
    Load Phase-002 style voice_output_governance_decisions.json (list).
    """
    path = Path(governance_root) / "voice_output_governance_decisions.json"
    if not path.is_file():
        raise FileNotFoundError(str(path))
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("voice_output_governance_decisions.json must be a list")
    return [x for x in data if isinstance(x, dict)]


def load_voice_governance_inputs_v0(governance_root: str) -> List[Dict[str, Any]]:
    path = Path(governance_root) / "voice_output_governance_inputs.json"
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def _guard_normalized_text(decision: Dict[str, Any]) -> str:
    gr = decision.get("guard_result") if isinstance(decision.get("guard_result"), dict) else {}
    return str(gr.get("normalized_text") or "")


def _candidate_text(decision: Dict[str, Any]) -> str:
    return str(decision.get("candidate_text") or "")


def build_voice_speakability_audit_v0(
    *,
    decision: Dict[str, Any],
    entry_allowed: bool,
) -> Dict[str, Any]:
    """
    VoiceSpeakabilityAuditV0 — qwen-tts layer never rewrites; guard may normalize upstream.
    """
    rid = str(decision.get("request_id") or "")
    sample_id = str(decision.get("sample_id") or "")
    source_text = _candidate_text(decision)
    gr = decision.get("guard_result") if isinstance(decision.get("guard_result"), dict) else {}
    speakable = bool(gr.get("speakable"))
    normalized = _guard_normalized_text(decision)

    diff_type = "none"
    rewrite_allowed = False
    rewrite_source = None
    diff_summary = None

    if not speakable:
        provider_input_text = ""
        spoken_text = ""
        diff_type = "unknown"
        diff_summary = "guard_blocked_or_empty"
        text_changed_flag = True
    elif not entry_allowed:
        # Synthesis not permitted: do not fabricate a user-uttered string.
        provider_input_text = ""
        spoken_text = ""
        text_changed_flag = False
    else:
        # Synthesis would use guard-normalized text; qwen-tts does not add another rewrite layer.
        provider_input_text = normalized
        spoken_text = normalized
        if source_text != normalized:
            diff_type = "formatting_only"
            rewrite_allowed = True
            rewrite_source = "guard_v1_speakable_text"
            diff_summary = "guard_normalized_candidate"
            text_changed_flag = True
        else:
            text_changed_flag = False

    audit_id = _new_id("vsa")

    return {
        "audit_id": audit_id,
        "request_id": rid,
        "sample_id": sample_id,
        "source_text": source_text,
        "provider_input_text": provider_input_text,
        "spoken_text": spoken_text,
        "text_diff_audit": {
            "text_changed": text_changed_flag,
            "diff_type": diff_type,
            "rewrite_allowed": rewrite_allowed,
            "rewrite_source": rewrite_source,
            "diff_summary": diff_summary,
        },
        "provider_boundary": {
            "provider_kind": "text_to_audio",
            "expression_provider": False,
            "model_may_rewrite_text": False,
        },
    }


def evaluate_qwen_first_tts_fallback_selection_dry_run_v0(
    *,
    decision: Dict[str, Any],
    provider_mode: ProviderMode,
    entry_allowed: bool,
) -> Dict[str, Any]:
    """
    Dry-run provider chain semantics only (no SDK / subprocess).
    """
    fa = str(decision.get("final_action") or "")
    ph = decision.get("provider_health_result") if isinstance(decision.get("provider_health_result"), dict) else {}
    fb_req = bool(ph.get("fallback_required"))

    if not entry_allowed:
        return {
            "provider_order": [],
            "selected_provider": "none",
            "fallback_provider": "none",
            "selection_reason": "governance_blocked_no_provider_dry_run",
            "provider_invoked": False,
            "dry_run": True,
            "provider_mode": provider_mode,
            "governance_final_action": fa,
        }

    if provider_mode == "offline_only":
        return {
            "provider_order": ["piper"],
            "selected_provider": "piper",
            "fallback_provider": "none",
            "selection_reason": "offline_only_piper_only_qwen_disabled_dry_run",
            "provider_invoked": False,
            "dry_run": True,
            "provider_mode": provider_mode,
            "governance_final_action": fa,
        }

    # online_prefer_qwen template semantics
    order = ["qwen", "piper"]
    if fa == "fallback_candidate" or fb_req:
        return {
            "provider_order": order,
            "selected_provider": "piper",
            "fallback_provider": "piper",
            "selection_reason": "provider_health_fallback_candidate_dry_run_prefer_piper",
            "provider_invoked": False,
            "dry_run": True,
            "provider_mode": provider_mode,
            "governance_final_action": fa,
        }

    return {
        "provider_order": order,
        "selected_provider": "qwen",
        "fallback_provider": "piper",
        "selection_reason": "online_prefer_qwen_primary_dry_run",
        "provider_invoked": False,
        "dry_run": True,
        "provider_mode": provider_mode,
        "governance_final_action": fa,
    }


def _entry_allowed_from_governance(decision: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    fa = str(decision.get("final_action") or "")
    if fa in ("accepted_dry_run", "fallback_candidate"):
        return True, None
    if fa == "suppressed":
        sr = decision.get("suppression_result") if isinstance(decision.get("suppression_result"), dict) else {}
        return False, str(sr.get("suppression_reason") or "suppressed")
    if fa == "cancelled":
        return False, "cancelled"
    return False, f"blocked_final_action:{fa}"


def build_governed_voice_provider_entry_decision_v0(
    *,
    decision: Dict[str, Any],
    provider_mode: ProviderMode,
    speakability_audit: Dict[str, Any],
) -> Dict[str, Any]:
    entry_allowed, block_reason = _entry_allowed_from_governance(decision)
    sel = evaluate_qwen_first_tts_fallback_selection_dry_run_v0(
        decision=decision,
        provider_mode=provider_mode,
        entry_allowed=entry_allowed,
    )

    gov = decision.get("governance") if isinstance(decision.get("governance"), dict) else {}
    hard_audit = {
        "real_qwen_invoked": False,
        "real_tts_invoked": False,
        "provider_invoked": False,
        "playback_invoked": False,
        "navigation_action": gov.get("navigation_action"),
        "downstream_invocation_count": 0,
    }

    entry_decision_id = _new_id("gvp")

    return {
        "entry_decision_id": entry_decision_id,
        "request_id": str(decision.get("request_id") or ""),
        "sample_id": str(decision.get("sample_id") or ""),
        "source_governance_decision_id": str(decision.get("voice_output_decision_id") or ""),
        "runtime_mode": "dry_run",
        "requested_provider_mode": provider_mode,
        "governance_final_action": str(decision.get("final_action") or ""),
        "entry_allowed": entry_allowed,
        "entry_block_reason": block_reason,
        "provider_selection": sel,
        "speakability_audit_ref": speakability_audit["audit_id"],
        "hard_audit": hard_audit,
    }


def run_governed_voice_provider_entry_skeleton_v0(
    *,
    governance_root: str,
    provider_mode: ProviderMode,
) -> Tuple[
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[Dict[str, Any]],
]:
    """
    Returns entry_decisions, audits, provider_selection_rows, trace_rows, replay_rows, whitebox_rows.
    """
    decisions = load_voice_governance_decisions_v0(governance_root)
    entry_decisions: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    sel_rows: List[Dict[str, Any]] = []

    trace_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    white_rows: List[Dict[str, Any]] = []

    for d in decisions:
        entry_allowed, _ = _entry_allowed_from_governance(d)
        au = build_voice_speakability_audit_v0(decision=d, entry_allowed=entry_allowed)
        ed = build_governed_voice_provider_entry_decision_v0(
            decision=d,
            provider_mode=provider_mode,
            speakability_audit=au,
        )
        entry_decisions.append(ed)
        audits.append(au)
        sel_rows.append({"sample_id": ed["sample_id"], **ed["provider_selection"]})

        trace_rows.append(
            {
                "type": "voice_governed_provider_entry_trace_v0",
                "phase": "Phase-Voice-Qianwen-002",
                "sample_id": ed["sample_id"],
                "request_id": ed["request_id"],
                "entry_decision_id": ed["entry_decision_id"],
                "provider_mode": provider_mode,
                "entry_allowed": ed["entry_allowed"],
                "governance_final_action": ed["governance_final_action"],
                "selected_provider": ed["provider_selection"]["selected_provider"],
            }
        )
        replay_rows.append(
            {
                "type": "voice_governed_provider_entry_replay_v0",
                "sample_id": ed["sample_id"],
                "request_id": ed["request_id"],
                "source_governance_decision_id": ed["source_governance_decision_id"],
                "speakability_audit_id": au["audit_id"],
                "provider_selection": ed["provider_selection"],
            }
        )
        white_rows.append(
            {
                "type": "voice_governed_provider_entry_whitebox_v0",
                "sample_id": ed["sample_id"],
                "why_no_provider": (not ed["entry_allowed"]),
                "why_qwen_not_selected": ed["provider_selection"]["selected_provider"] != "qwen",
                "why_piper_selected": ed["provider_selection"]["selected_provider"] == "piper",
                "hard_audit": ed["hard_audit"],
            }
        )

    return entry_decisions, audits, sel_rows, trace_rows, replay_rows, white_rows


def append_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
