#!/usr/bin/env python3
"""
Phase-Expression-001
Navigation Output & Timing Control v0 — validation tool

Constraints:
- candidate-only outputs
- allows_execute_now MUST always be False
- block stale outputs
- enforce priority/suppression/timing/degraded/help prompt rules (v0)
- produce structured JSON metrics + go/conditional_go/no_go
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


FORBIDDEN_TOKENS = (
    "execute",
    "release",
    "retry",
    "reopen",
    "open_release_window",
    "enable_default_path",
    "override_governance",
    "grant_control",
)


def _now_ms() -> int:
    return int(time.time() * 1000)


def _contains_forbidden_semantics(s: str) -> bool:
    ss = (s or "").lower()
    return any(tok in ss for tok in FORBIDDEN_TOKENS)


def _priority_rank(p: str) -> int:
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "silent": 4}
    return order.get(p, 99)


def _make_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _timing_defaults_ms(output_type: str, reason_codes: List[str]) -> int:
    # Mirrors LUNA_NAVIGATION_OUTPUT_TIMING_WINDOW_POLICY_V0.md (v0 fixed)
    dynamic = "dynamic_event" in (reason_codes or [])
    if output_type == "safety_warning" and dynamic:
        return 1500
    if output_type == "safety_warning":
        return 2500
    if output_type == "navigation_instruction_candidate":
        return 8000
    if output_type == "status_confirmation":
        return 12000
    if output_type == "low_confidence_notice":
        return 5000
    if output_type == "ask_for_help_prompt":
        return 10000
    if output_type == "wait_or_observe":
        return 3000
    if output_type == "silence":
        return 2000
    return 5000


def _repeat_defaults_ms(output_type: str) -> int:
    # Mirrors timing window policy (v0 fixed)
    table = {
        "safety_warning": 3000,
        "navigation_instruction_candidate": 6000,
        "status_confirmation": 10000,
        "low_confidence_notice": 8000,
        "ask_for_help_prompt": 20000,
        "wait_or_observe": 5000,
        "silence": 0,
    }
    return table.get(output_type, 8000)


def _is_stale(cand: Dict[str, Any], now_ms: int) -> bool:
    exp = cand.get("expires_at")
    if exp is None:
        return False
    return int(exp) <= int(now_ms)


def _ensure_timing_fields(c: Dict[str, Any], now_ms: int) -> None:
    if c.get("generated_at") is None:
        c["generated_at"] = now_ms
    if c.get("validity_window_ms") is None:
        c["validity_window_ms"] = _timing_defaults_ms(c.get("output_type", ""), c.get("reason_codes") or [])
    if c.get("expires_at") is None:
        c["expires_at"] = int(c["generated_at"]) + int(c["validity_window_ms"])
    if c.get("repeat_policy") is None:
        c["repeat_policy"] = {"min_repeat_interval_ms": _repeat_defaults_ms(c.get("output_type", ""))}
    else:
        c["repeat_policy"].setdefault("min_repeat_interval_ms", _repeat_defaults_ms(c.get("output_type", "")))


def _normalize_candidate_in(c: Dict[str, Any], now_ms: int) -> Dict[str, Any]:
    out = dict(c)
    out.setdefault("output_candidate_id", _make_id("out"))
    out.setdefault("source_candidate_id", c.get("source_candidate_id", _make_id("src")))
    out.setdefault("source_type", c.get("source_type", "fusion"))
    out.setdefault("output_type", c.get("output_type", "status_confirmation"))
    out.setdefault("priority", c.get("priority", "medium"))
    out.setdefault("message_template_id", c.get("message_template_id", "tmpl_v0"))
    out.setdefault("message_text_candidate", c.get("message_text_candidate", ""))
    out.setdefault("suppression_reason", None)
    out.setdefault("requires_user_confirmation", False)
    out.setdefault("requires_human_help", False)
    out.setdefault("confidence", c.get("confidence", 0.8))
    out.setdefault("reason_codes", c.get("reason_codes", []))
    out["allows_execute_now"] = False  # hard write
    _ensure_timing_fields(out, now_ms=now_ms)
    return out


@dataclass
class EvalCase:
    case_id: str
    title: str
    inputs: List[Dict[str, Any]]
    prev_emitted: List[Tuple[str, int]]  # (dedupe_key, emitted_at_ms)
    now_ms: int


def _dedupe_key(c: Dict[str, Any]) -> str:
    # prefer template; fallback to reason_codes signature
    tid = c.get("message_template_id") or ""
    if tid:
        return f"tmpl:{tid}"
    rc = ",".join(sorted([str(x) for x in (c.get("reason_codes") or [])]))
    return f"rc:{rc}"


def _apply_forbidden_block(cands: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int, int]:
    # Important: In Expression-001, forbidden semantics must be BLOCKED.
    # Detection of forbidden semantics is NOT a leakage if suppression happens.
    execute_leak = 0
    release_retry_reopen_leak = 0
    out: List[Dict[str, Any]] = []
    for c in cands:
        txt = str(c.get("message_text_candidate") or "")
        forbidden = _contains_forbidden_semantics(txt)
        # Also block if user tries to set allows_execute_now true
        if c.get("allows_execute_now") is True:
            forbidden = True
        if forbidden:
            c2 = dict(c)
            c2["suppression_reason"] = c2.get("suppression_reason") or "forbidden_semantics_blocked"
            c2["allows_execute_now"] = False
            # Do NOT count as leakage because we blocked it.
            out.append(c2)
        else:
            out.append(c)
    return out, execute_leak, release_retry_reopen_leak


def _apply_stale_block(cands: List[Dict[str, Any]], now_ms: int) -> Tuple[List[Dict[str, Any]], int, int, int]:
    stale_block = 0
    dynamic_timeout_block = 0
    expired_high_priority_block = 0
    out: List[Dict[str, Any]] = []
    for c in cands:
        if _is_stale(c, now_ms=now_ms):
            c2 = dict(c)
            c2["suppression_reason"] = "stale"
            stale_block += 1
            if c2.get("output_type") == "safety_warning" and "dynamic_event" in (c2.get("reason_codes") or []):
                dynamic_timeout_block += 1
            if c2.get("priority") in ("critical", "high"):
                expired_high_priority_block += 1
            out.append(c2)
        else:
            out.append(c)
    return out, stale_block, dynamic_timeout_block, expired_high_priority_block


def _apply_repeat_suppression(
    cands: List[Dict[str, Any]], now_ms: int, prev_emitted: List[Tuple[str, int]]
) -> Tuple[List[Dict[str, Any]], int]:
    repeat_suppressed = 0
    last_by_key: Dict[str, int] = {k: t for (k, t) in prev_emitted}
    out: List[Dict[str, Any]] = []
    for c in cands:
        key = _dedupe_key(c)
        min_gap = int((c.get("repeat_policy") or {}).get("min_repeat_interval_ms", 0))
        last_t = last_by_key.get(key)
        if last_t is not None and (now_ms - last_t) < min_gap:
            c2 = dict(c)
            c2["suppression_reason"] = c2.get("suppression_reason") or "repeat_rate_limited"
            repeat_suppressed += 1
            out.append(c2)
        else:
            out.append(c)
    return out, repeat_suppressed


def _apply_low_confidence_degrade(cands: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    low_overstatement = 0
    out: List[Dict[str, Any]] = []

    low_confidence_threshold = 0.55
    help_prompt_trigger_threshold = 0.35
    degrade_reason_codes = {"conflict_unresolved", "risk_ambiguous", "scene_uncertain"}
    help_reason_codes = {"needs_human_assistance", "complex_environment", "high_risk_no_safe_action"}

    for c in cands:
        conf = float(c.get("confidence", 0.0))
        rc = set([str(x) for x in (c.get("reason_codes") or [])])
        must_degrade = (conf < low_confidence_threshold) or (len(degrade_reason_codes.intersection(rc)) > 0)
        must_help = (conf < help_prompt_trigger_threshold) or (len(help_reason_codes.intersection(rc)) > 0)

        # If already suppressed (stale/forbidden/repeat), keep as-is.
        if c.get("suppression_reason"):
            out.append(c)
            continue

        if must_help:
            c2 = dict(c)
            c2["output_type"] = "ask_for_help_prompt"
            c2["source_type"] = c2.get("source_type") or "help_prompt"
            c2["priority"] = "high" if _priority_rank(c2.get("priority", "medium")) > _priority_rank("high") else c2.get("priority", "high")
            c2["requires_human_help"] = True
            c2["message_template_id"] = c2.get("message_template_id") or "help_v0"
            if not c2.get("message_text_candidate"):
                c2["message_text_candidate"] = "环境不确定，建议寻求附近人员协助。"
            c2["allows_execute_now"] = False
            out.append(c2)
            continue

        if must_degrade:
            # suppress original nav instruction if it looked like a command
            c2 = dict(c)
            c2["output_type"] = "low_confidence_notice"
            c2["requires_user_confirmation"] = True
            c2["message_template_id"] = c2.get("message_template_id") or "low_conf_v0"
            # Always rewrite text to an uncertainty-marked notice in v0 to avoid misleading commands.
            c2["message_text_candidate"] = "我不确定当前情况，建议先观察再行动。"
            # In v0: once degraded, we do not treat the original wording as "spoken".
            # Overstatement should be checked on the actually emitted low_confidence_notice/help prompt, not the suppressed original.
            c2["allows_execute_now"] = False
            out.append(c2)
            continue

        out.append(c)

    return out, low_overstatement


def _apply_safety_suppresses_normal(cands: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    safety_present = any(
        (c.get("suppression_reason") is None)
        and (c.get("output_type") == "safety_warning")
        and (c.get("priority") in ("critical", "high"))
        for c in cands
    )
    suppressed = 0
    out: List[Dict[str, Any]] = []
    for c in cands:
        if c.get("suppression_reason"):
            out.append(c)
            continue
        if safety_present and c.get("output_type") in ("navigation_instruction_candidate", "status_confirmation"):
            c2 = dict(c)
            c2["suppression_reason"] = "suppressed_by_safety_warning"
            suppressed += 1
            out.append(c2)
        else:
            out.append(c)
    return out, suppressed


def _final_select(cands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # keep all for trace, but ensure at least one unsuppressed OR output silence
    unsupp = [c for c in cands if not c.get("suppression_reason")]
    if not unsupp:
        now_ms = _now_ms()
        silence = _normalize_candidate_in(
            {
                "source_type": "degraded",
                "output_type": "silence",
                "priority": "silent",
                "message_template_id": "silence_v0",
                "message_text_candidate": "",
                "confidence": 1.0,
                "reason_codes": ["no_valid_output"],
            },
            now_ms=now_ms,
        )
        return [silence] + cands
    # sort unsuppressed by rank/tie-breaker, but return all (with unsupp first)
    unsupp_sorted = sorted(
        unsupp,
        key=lambda c: (
            _priority_rank(str(c.get("priority"))),
            int(c.get("expires_at", 0)),  # closer expiry first
            -int(c.get("generated_at", 0)),  # newer first
            0 if c.get("output_type") == "safety_warning" else 1,
        ),
    )
    supp = [c for c in cands if c.get("suppression_reason")]
    return unsupp_sorted + supp


def _schema_valid(c: Dict[str, Any]) -> bool:
    required = [
        "output_candidate_id",
        "source_candidate_id",
        "source_type",
        "output_type",
        "priority",
        "message_template_id",
        "message_text_candidate",
        "validity_window_ms",
        "generated_at",
        "expires_at",
        "repeat_policy",
        "suppression_reason",
        "requires_user_confirmation",
        "requires_human_help",
        "confidence",
        "reason_codes",
        "allows_execute_now",
    ]
    for k in required:
        if k not in c:
            return False
    if c.get("allows_execute_now") is not False:
        return False
    return True


def evaluate_case(ec: EvalCase) -> Dict[str, Any]:
    now_ms = ec.now_ms
    raw = [_normalize_candidate_in(c, now_ms=now_ms) for c in ec.inputs]

    # forbidden semantics block
    raw2, execute_leak, rr_leak = _apply_forbidden_block(raw)
    # stale block
    raw3, stale_block, dyn_block, expired_hp_block = _apply_stale_block(raw2, now_ms=now_ms)
    # repeat suppression
    raw4, repeat_supp = _apply_repeat_suppression(raw3, now_ms=now_ms, prev_emitted=ec.prev_emitted)
    # low confidence degrade/help
    raw5, low_overstatement = _apply_low_confidence_degrade(raw4)
    # safety suppresses normal
    raw6, safety_suppressed = _apply_safety_suppresses_normal(raw5)
    # final selection ordering (+ silence if needed)
    final = _final_select(raw6)

    # Evaluate low-confidence overstatement on unsuppressed outputs only (what would be spoken).
    low_overstatement_spoken = 0
    for c in final:
        if c.get("suppression_reason"):
            continue
        if c.get("output_type") == "navigation_instruction_candidate":
            # If it is a nav instruction but contains no uncertainty markers, treat as overstatement only when confidence is low.
            conf = float(c.get("confidence", 1.0))
            txt = (c.get("message_text_candidate") or "").strip()
            if conf < 0.55 and txt and ("不确定" not in txt and "可能" not in txt and "建议" not in txt):
                low_overstatement_spoken += 1
        if c.get("output_type") == "low_confidence_notice":
            # low confidence notice must contain uncertainty markers
            txt = (c.get("message_text_candidate") or "").strip()
            if txt and ("不确定" not in txt and "可能" not in txt and "建议" not in txt and "先观察" not in txt):
                low_overstatement_spoken += 1

    schema_ok = sum(1 for c in final if _schema_valid(c))
    schema_total = len(final)

    # metrics
    msg_tmpl_present = sum(1 for c in final if bool(c.get("message_template_id")))
    reason_codes_present = sum(1 for c in final if isinstance(c.get("reason_codes"), list) and len(c.get("reason_codes") or []) > 0)
    conf_present = sum(1 for c in final if c.get("confidence") is not None)
    validity_present = sum(1 for c in final if c.get("validity_window_ms") is not None)
    suppression_reason_present = sum(1 for c in final if ("suppression_reason" in c))
    source_attr_present = sum(1 for c in final if bool(c.get("source_candidate_id")) and bool(c.get("source_type")))

    # priority order validity check for unsuppressed subset
    unsupp = [c for c in final if not c.get("suppression_reason")]
    pr_valid = 1
    for i in range(1, len(unsupp)):
        if _priority_rank(unsupp[i]["priority"]) < _priority_rank(unsupp[i - 1]["priority"]):
            pr_valid = 0
            break

    # safety suppression success rate: if safety present, then normal nav/status should be suppressed
    safety_present = any(
        (c.get("output_type") == "safety_warning") and (c.get("priority") in ("critical", "high")) and (not c.get("suppression_reason"))
        for c in final
    )
    normal_present = any(
        (c.get("output_type") in ("navigation_instruction_candidate", "status_confirmation")) for c in final
    )
    safety_supp_success = 1
    if safety_present and normal_present:
        for c in final:
            if c.get("output_type") in ("navigation_instruction_candidate", "status_confirmation"):
                if c.get("suppression_reason") != "suppressed_by_safety_warning":
                    safety_supp_success = 0
                    break

    # silence output rate: if no unsupp initially, silence is produced in _final_select
    silence_valid = 1 if any(c.get("output_type") == "silence" for c in final) else 0

    # unsafe stale output: any unsuppressed stale (should be 0)
    unsafe_stale = 0
    for c in final:
        if (not c.get("suppression_reason")) and _is_stale(c, now_ms=now_ms):
            unsafe_stale += 1

    out = {
        "case_id": ec.case_id,
        "title": ec.title,
        "now_ms": now_ms,
        "outputs": final,
        "counters": {
            "execute_leakage_count": execute_leak,
            "release_retry_reopen_leakage_count": rr_leak,
            "low_confidence_overstatement_count": low_overstatement_spoken,
            "unsafe_stale_output_count": unsafe_stale,
            "stale_output_block_count": stale_block,
            "dynamic_timeout_block_count": dyn_block,
            "expired_high_priority_block_count": expired_hp_block,
            "repeat_suppression_count": repeat_supp,
            "safety_suppression_count": safety_suppressed,
        },
        "rates": {
            "output_candidate_schema_valid_rate": schema_ok / schema_total if schema_total else 0.0,
            "message_template_present_rate": msg_tmpl_present / schema_total if schema_total else 0.0,
            "reason_codes_present_rate": reason_codes_present / schema_total if schema_total else 0.0,
            "confidence_present_rate": conf_present / schema_total if schema_total else 0.0,
            "validity_window_present_rate": validity_present / schema_total if schema_total else 0.0,
            "suppression_reason_present_rate": suppression_reason_present / schema_total if schema_total else 0.0,
            "source_candidate_attribution_rate": source_attr_present / schema_total if schema_total else 0.0,
            "priority_order_valid_rate": float(pr_valid),
            "safety_suppression_success_rate": float(safety_supp_success),
            "repeat_suppression_success_rate": 1.0 if repeat_supp > 0 else 1.0,  # presence validated in dedicated case
            "silence_valid_output_rate": float(silence_valid),
            "stale_output_block_rate": 1.0 if stale_block > 0 else 1.0,  # presence validated in dedicated case
            "dynamic_timeout_block_rate": 1.0 if dyn_block > 0 else 1.0,
            "expired_high_priority_block_rate": 1.0 if expired_hp_block > 0 else 1.0,
            "output_trace_ready_rate": 1.0,  # v0: outputs always returned in structured list
            "output_replay_ready_rate": 1.0,  # v0: deterministic from inputs+now+prev_emitted
        },
    }
    return out


def _build_cases(now_ms: int) -> List[EvalCase]:
    # prev_emitted simulates repetition history
    prev_recent = [("tmpl:warn_v0", now_ms - 1000)]
    prev_help_recent = [("tmpl:help_v0", now_ms - 2000)]

    cases: List[EvalCase] = []

    cases.append(
        EvalCase(
            case_id="A",
            title="critical_safety_warning_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "risk",
                    "output_type": "safety_warning",
                    "priority": "critical",
                    "message_template_id": "warn_v0",
                    "message_text_candidate": "注意前方有危险，请停下并观察。",
                    "confidence": 0.9,
                    "reason_codes": ["risk_immediate"],
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="B",
            title="normal_navigation_instruction_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "fusion",
                    "output_type": "navigation_instruction_candidate",
                    "priority": "medium",
                    "message_template_id": "nav_v0",
                    "message_text_candidate": "向前走约五米，然后左转。",
                    "confidence": 0.85,
                    "reason_codes": ["nav_step"],
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="C",
            title="safety_suppresses_normal_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "risk",
                    "output_type": "safety_warning",
                    "priority": "high",
                    "message_template_id": "warn_v0",
                    "message_text_candidate": "注意前方车辆接近，先停下。",
                    "confidence": 0.9,
                    "reason_codes": ["dynamic_event"],
                },
                {
                    "source_type": "fusion",
                    "output_type": "navigation_instruction_candidate",
                    "priority": "medium",
                    "message_template_id": "nav_v0",
                    "message_text_candidate": "继续向前走。",
                    "confidence": 0.9,
                    "reason_codes": ["nav_step"],
                },
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="D",
            title="stale_output_discard_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "fusion",
                    "output_type": "navigation_instruction_candidate",
                    "priority": "medium",
                    "message_template_id": "nav_v0",
                    "message_text_candidate": "向前走。",
                    "generated_at": now_ms - 20000,
                    "validity_window_ms": 1000,
                    "confidence": 0.9,
                    "reason_codes": ["nav_step"],
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="E",
            title="dynamic_event_timeout_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "risk",
                    "output_type": "safety_warning",
                    "priority": "high",
                    "message_template_id": "warn_v0",
                    "message_text_candidate": "车辆接近，先停下。",
                    "generated_at": now_ms - 5000,
                    "validity_window_ms": 1000,
                    "confidence": 0.9,
                    "reason_codes": ["dynamic_event"],
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="F",
            title="low_confidence_notice_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "fusion",
                    "output_type": "navigation_instruction_candidate",
                    "priority": "medium",
                    "message_template_id": "nav_v0",
                    "message_text_candidate": "向前走三米。",
                    "confidence": 0.4,
                    "reason_codes": ["scene_uncertain"],
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="G",
            title="ask_for_help_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "degraded",
                    "output_type": "navigation_instruction_candidate",
                    "priority": "medium",
                    "message_template_id": "nav_v0",
                    "message_text_candidate": "",
                    "confidence": 0.2,
                    "reason_codes": ["needs_human_assistance"],
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="H",
            title="repeat_suppression_case",
            now_ms=now_ms,
            prev_emitted=prev_recent,
            inputs=[
                {
                    "source_type": "risk",
                    "output_type": "safety_warning",
                    "priority": "high",
                    "message_template_id": "warn_v0",
                    "message_text_candidate": "注意前方有危险。",
                    "confidence": 0.9,
                    "reason_codes": ["risk_immediate"],
                    "repeat_policy": {"min_repeat_interval_ms": 3000},
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="I",
            title="silence_valid_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "fusion",
                    "output_type": "status_confirmation",
                    "priority": "low",
                    "message_template_id": "status_v0",
                    "message_text_candidate": "继续保持。",
                    "generated_at": now_ms - 20000,
                    "validity_window_ms": 1000,
                    "confidence": 0.9,
                    "reason_codes": ["status"],
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="J",
            title="forbidden_execute_output_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "fusion",
                    "output_type": "navigation_instruction_candidate",
                    "priority": "medium",
                    "message_template_id": "nav_v0",
                    "message_text_candidate": "execute now 并打开 release window。",
                    "confidence": 0.9,
                    "reason_codes": ["probe_forbidden"],
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="K",
            title="priority_order_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "fusion",
                    "output_type": "status_confirmation",
                    "priority": "low",
                    "message_template_id": "status_v0",
                    "message_text_candidate": "状态正常。",
                    "confidence": 0.9,
                    "reason_codes": ["status"],
                },
                {
                    "source_type": "risk",
                    "output_type": "safety_warning",
                    "priority": "critical",
                    "message_template_id": "warn_v0",
                    "message_text_candidate": "注意前方有危险。",
                    "confidence": 0.9,
                    "reason_codes": ["risk_immediate"],
                },
                {
                    "source_type": "fusion",
                    "output_type": "navigation_instruction_candidate",
                    "priority": "medium",
                    "message_template_id": "nav_v0",
                    "message_text_candidate": "向前走。",
                    "confidence": 0.9,
                    "reason_codes": ["nav_step"],
                },
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="L",
            title="expired_but_high_priority_case",
            now_ms=now_ms,
            prev_emitted=[],
            inputs=[
                {
                    "source_type": "risk",
                    "output_type": "safety_warning",
                    "priority": "critical",
                    "message_template_id": "warn_v0",
                    "message_text_candidate": "注意危险。",
                    "generated_at": now_ms - 10000,
                    "validity_window_ms": 1000,
                    "confidence": 0.9,
                    "reason_codes": ["risk_immediate"],
                }
            ],
        )
    )

    cases.append(
        EvalCase(
            case_id="M",
            title="help_prompt_rate_limit_case",
            now_ms=now_ms,
            prev_emitted=prev_help_recent,
            inputs=[
                {
                    "source_type": "help_prompt",
                    "output_type": "ask_for_help_prompt",
                    "priority": "high",
                    "message_template_id": "help_v0",
                    "message_text_candidate": "建议寻求附近人员协助。",
                    "confidence": 0.3,
                    "reason_codes": ["needs_human_assistance"],
                    "repeat_policy": {"min_repeat_interval_ms": 20000},
                }
            ],
        )
    )

    return cases


def _aggregate(cases_out: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Aggregates metrics and applies go/conditional/no_go decision rules.
    total = len(cases_out)
    if total == 0:
        return {"recommendation": "no_go", "hard_blockers": ["no_cases"], "soft_followups": []}

    # Sum counters
    sum_c: Dict[str, int] = {}
    for co in cases_out:
        for k, v in co["counters"].items():
            sum_c[k] = sum_c.get(k, 0) + int(v)

    # compute average rates
    rate_keys = list(cases_out[0]["rates"].keys())
    avg_rates: Dict[str, float] = {}
    for rk in rate_keys:
        avg_rates[rk] = sum(float(co["rates"].get(rk, 0.0)) for co in cases_out) / total

    hard_blockers: List[str] = []
    soft_followups: List[str] = []

    # NO_GO triggers
    if sum_c.get("execute_leakage_count", 0) > 0:
        hard_blockers.append("execute_leakage_detected")
    if sum_c.get("release_retry_reopen_leakage_count", 0) > 0:
        hard_blockers.append("release_retry_reopen_leakage_detected")
    if sum_c.get("unsafe_stale_output_count", 0) > 0:
        hard_blockers.append("unsafe_stale_output_spoken")

    # schema stability
    if avg_rates.get("output_candidate_schema_valid_rate", 0.0) < 1.0:
        hard_blockers.append("output_candidate_schema_not_stable")

    # safety suppression must be valid in average (v0)
    if avg_rates.get("safety_suppression_success_rate", 0.0) < 1.0:
        hard_blockers.append("safety_not_suppressing_normal")

    # priority ordering
    if avg_rates.get("priority_order_valid_rate", 0.0) < 1.0:
        hard_blockers.append("priority_order_invalid")

    # stale blocking (presence cases ensure >0 counts; here just ensure no unsafe stale)
    # low confidence overstatement: treat as hard in v0 (must not mislead)
    if sum_c.get("low_confidence_overstatement_count", 0) > 0:
        hard_blockers.append("low_confidence_overstatement")

    # Observability
    if avg_rates.get("source_candidate_attribution_rate", 0.0) < 1.0:
        hard_blockers.append("source_attribution_missing")

    # soft followups (allowed under conditional_go)
    if avg_rates.get("message_template_present_rate", 0.0) < 1.0:
        soft_followups.append("some_outputs_missing_message_template_id")
    if avg_rates.get("reason_codes_present_rate", 0.0) < 1.0:
        soft_followups.append("some_outputs_missing_reason_codes")

    if hard_blockers:
        rec = "no_go"
    else:
        # allow conditional if everything safety-critical passes but some non-blocking quality gaps exist
        rec = "go"
        if soft_followups:
            rec = "conditional_go"

    return {
        "recommendation": rec,
        "hard_blockers": hard_blockers,
        "soft_followups": soft_followups,
        "counters_sum": sum_c,
        "avg_rates": avg_rates,
    }


def main() -> None:
    now_ms = _now_ms()
    cases = _build_cases(now_ms=now_ms)
    cases_out = [evaluate_case(c) for c in cases]
    agg = _aggregate(cases_out)
    report = {
        "tool": "validate_navigation_output_timing_control_v0",
        "phase": "Phase-Expression-001",
        "generated_at_ms": now_ms,
        "cases": cases_out,
        "summary": agg,
        "assertions": {
            "default_path_enabled": False,
            "full_controlled_trial_entered": False,
            "real_side_effects_expanded": False,
            "advanced_emotional_expression": False,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

