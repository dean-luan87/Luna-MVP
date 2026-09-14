# -*- coding: utf-8
"""Network learning policy reviewer — deterministic stub v1."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

POLICY_REF = "network_assisted_situation_learning_policy_v1"
UNSAFE_SLAM_FOR_TEXT = {"read_text", "locate_place", "identify_place"}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def check_unsafe_rule(candidate: Dict[str, Any]) -> Tuple[bool, List[str]]:
    flags: List[str] = []
    task_clues = set(candidate.get("proposed_task_clues") or [])
    needed = set(candidate.get("proposed_needed_tools") or [])
    noop = set(candidate.get("proposed_noop_tools") or [])

    if task_clues & UNSAFE_SLAM_FOR_TEXT and "SLAM" in needed and "SLAM" not in noop:
        flags.append("unsafe_rule_risk:text_task_activates_slam_by_default")

    if "fact" in (candidate.get("evidence_summary") or "").lower():
        flags.append("unsupported_fact_risk")

    return bool(flags), flags


def check_provenance(candidate: Dict[str, Any], provenance: Optional[Dict[str, Any]] = None) -> bool:
    if not candidate.get("provenance_ref"):
        return False
    if provenance and provenance.get("provenance_id") != candidate.get("provenance_ref"):
        return False
    return True


def check_source_trust(source: Optional[Dict[str, Any]]) -> bool:
    if not source:
        return True
    return source.get("trust_tier") in ("high", "medium", "low", "unknown")


def check_training_eligibility(
    candidate: Dict[str, Any],
    review: Dict[str, Any],
) -> bool:
    if review.get("policy_decision") not in ("accept_as_case_candidate",):
        return False
    if review.get("unsafe_rule_risk"):
        return False
    if review.get("privacy_risk"):
        return False
    return True


def review_learning_candidate(
    candidate: Dict[str, Any],
    *,
    provenance: Optional[Dict[str, Any]] = None,
    source: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    rid = _uid("lpr")
    unsafe, risk_flags = check_unsafe_rule(candidate)
    prov_ok = check_provenance(candidate, provenance)
    trust_ok = check_source_trust(source)

    privacy_risk = "privacy" in " ".join(candidate.get("risk_flags", [])).lower()
    web_low_trust = source and source.get("trust_tier") in ("unknown", "low")

    if unsafe:
        decision = "reject"
        if "require_human_review" in risk_flags:
            decision = "require_human_review"
    elif not prov_ok:
        decision = "reject"
    elif web_low_trust and candidate.get("source_type") == "web_reference":
        decision = "hold"
    elif candidate.get("source_type") == "human_correction":
        decision = "require_human_review"
    elif candidate.get("source_type") == "test_trace":
        decision = "accept_as_case_candidate"
    else:
        decision = "accept_as_case_candidate"

    review = {
        "review_id": rid,
        "learning_candidate_id": candidate.get("learning_candidate_id"),
        "provenance_check_passed": prov_ok and trust_ok,
        "copyright_or_usage_risk": web_low_trust,
        "privacy_risk": privacy_risk,
        "hallucination_risk": False,
        "unsafe_rule_risk": unsafe,
        "unsupported_fact_risk": "unsupported_fact_risk" in risk_flags,
        "policy_decision": decision,
        "rejection_reason_optional": risk_flags[0] if risk_flags else None,
        "policy_refs": [POLICY_REF],
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "candidate_only": True,
        "not_fact": True,
        "risk_flags": risk_flags,
    }

    updated = dict(candidate)
    if decision == "accept_as_case_candidate":
        updated["review_status"] = "accepted_as_case"
    elif decision == "reject":
        updated["review_status"] = "policy_rejected"
    elif decision == "require_human_review":
        updated["review_status"] = "pending_human_review"
    else:
        updated["review_status"] = "pending_policy_review"

    return {"review": review, "learning_candidate": updated}
