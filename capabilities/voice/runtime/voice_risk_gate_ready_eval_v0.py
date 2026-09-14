# -*- coding: utf-8 -*-
"""
Risk gate-ready evaluator v0 (read-only).

Hard boundaries (v0):
- Only evaluates risk_summary_v1 fields against the frozen contract.
- Does NOT decide blocking / routing / submit.
- Does NOT invent missing fields (No Fabrication).
- Does NOT add system-level time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


_ALLOWED_RISK_LEVELS_V0 = ("none", "warning", "high")


def evaluate_risk_summary_v1_gate_ready_v0(
    risk_summary: Any,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Returns (present, eval_result).

    eval_result (minimal):
    - eval_scope: fixed string
    - gate_ready_passed: bool
    - risk_level_seen/source_seen when present
    - missing_fields/invalid_fields when failed
    - not_present when not present
    """
    scope = "risk_summary_v1_gate_ready_v0"
    if not isinstance(risk_summary, dict) or not risk_summary:
        return False, {
            "gate_ready_passed": False,
            "eval_scope": scope,
            "not_present": True,
        }

    missing: List[str] = []
    invalid: List[str] = []

    def _missing(name: str) -> None:
        if name not in missing:
            missing.append(name)

    def _invalid(name: str) -> None:
        if name not in invalid:
            invalid.append(name)

    # risk_level: required + enum
    rl = risk_summary.get("risk_level")
    if rl is None or str(rl).strip() == "":
        _missing("risk_level")
        rl_norm = ""
    else:
        rl_norm = str(rl).strip().lower()
        if rl_norm not in _ALLOWED_RISK_LEVELS_V0:
            _invalid("risk_level")

    # risk_type: required + non-empty
    rt = risk_summary.get("risk_type")
    if rt is None or str(rt).strip() == "":
        _missing("risk_type")

    # risk_reason: required + non-empty
    rr = risk_summary.get("risk_reason")
    if rr is None or str(rr).strip() == "":
        _missing("risk_reason")

    # confidence: required + numeric
    conf = risk_summary.get("confidence")
    if conf is None:
        _missing("confidence")
    else:
        if not isinstance(conf, (int, float)):
            _invalid("confidence")

    # source: required + non-empty
    src = risk_summary.get("source")
    if src is None or str(src).strip() == "":
        _missing("source")

    # is_gate_ready: required + bool
    igr = risk_summary.get("is_gate_ready")
    if igr is None:
        _missing("is_gate_ready")
    else:
        if not isinstance(igr, bool):
            _invalid("is_gate_ready")

    passed = (not missing) and (not invalid)
    out: Dict[str, Any] = {
        "gate_ready_passed": bool(passed),
        "eval_scope": scope,
    }
    # Only attach seen fields (non-derivative)
    if rl_norm:
        out["risk_level_seen"] = rl_norm
    if isinstance(src, str) and src.strip():
        out["source_seen"] = src.strip()

    if not passed:
        if missing:
            out["missing_fields"] = list(missing)
        if invalid:
            out["invalid_fields"] = list(invalid)
    return True, out

