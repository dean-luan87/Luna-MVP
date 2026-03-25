# -*- coding: utf-8 -*-
"""
Advisory / Review Observation M0

定位：
- 只读观察层：把已验证的 SF-1′（人审高风险候选）以结构化对象挂到 frame 顶层
- 不参与 benchmark/hard-fail/triage
- 不触发 block/defer/fail，不改主链 closure，不改 recheck 行为

依据：
- docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md
- docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md（SF-1′）
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def _s(x: Any) -> str:
    if x is None:
        return ""
    return str(x).strip()


@dataclass
class AdvisoryReviewObservation:
    # SF-1′：人审高风险候选（提示权，无裁决权）
    soft_fail_candidate_observed: bool = False
    soft_fail_candidate_clause_id: Optional[str] = None  # e.g. "SF-1-prime"
    soft_fail_candidate_level: str = "none"  # "high_risk_candidate" | "none"
    soft_fail_candidate_reason_summary: Optional[str] = None
    review_gate_recommended: bool = False
    advisory_only: bool = True

    advisory_review_observation_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "soft_fail_candidate_observed": bool(self.soft_fail_candidate_observed),
            "soft_fail_candidate_clause_id": self.soft_fail_candidate_clause_id,
            "soft_fail_candidate_level": self.soft_fail_candidate_level,
            "soft_fail_candidate_reason_summary": self.soft_fail_candidate_reason_summary,
            "review_gate_recommended": bool(self.review_gate_recommended),
            "advisory_only": bool(self.advisory_only),
            "advisory_review_observation_applied": bool(self.advisory_review_observation_applied),
        }


def build_advisory_review_observation(frame: Dict[str, Any]) -> AdvisoryReviewObservation:
    """
    M0：仅实现 SF-1′（已验证边界）观察。

    条款（草案）：
    1) pc∧lg raw high
    2) resume_chain_fragility_summary == resume_declared_but_main_not_progressed
    3) task_chain_progress_summary 含 global_main_progress_not_terminal_complete
    且无健康对照排除（terminal=found 且 tcp 无 global token 等）
    """
    if not isinstance(frame, dict):
        return AdvisoryReviewObservation(advisory_review_observation_applied=False)

    netr = frame.get("narrative_evidence_tension_review")
    if netr is not None and hasattr(netr, "to_dict"):
        netr = netr.to_dict()
    net = netr if isinstance(netr, dict) else {}

    rsr = frame.get("run_summary_reference")
    if rsr is not None and hasattr(rsr, "to_dict"):
        rsr = rsr.to_dict()
    rsr_d = rsr if isinstance(rsr, dict) else {}

    osi = frame.get("object_search_interaction")
    if osi is not None and hasattr(osi, "to_dict"):
        osi = osi.to_dict()
    osi_d = osi if isinstance(osi, dict) else {}

    pc = _s(net.get("phase_closure_outcome_tension"))
    lg = _s(net.get("local_global_progress_tension"))
    sf1 = pc == "high" and lg == "high"

    rfrag = _s(rsr_d.get("resume_chain_fragility_summary")) or "none"
    tcp = _s(rsr_d.get("task_chain_progress_summary"))
    tcp_has_global = "global_main_progress_not_terminal_complete" in tcp

    sf1_prime = bool(sf1 and rfrag == "resume_declared_but_main_not_progressed" and tcp_has_global)

    terminal = _s(osi_d.get("search_terminal_status")) or "none"
    exclude_healthy_terminal = bool(terminal == "found" and (not tcp_has_global) and sf1)

    observed = bool(sf1_prime and not exclude_healthy_terminal)

    reason = None
    if observed:
        reason = "pc∧lg_high;rsr=resume_declared_but_main_not_progressed;tcp_has_global_main_not_terminal_complete"

    return AdvisoryReviewObservation(
        soft_fail_candidate_observed=observed,
        soft_fail_candidate_clause_id="SF-1-prime" if observed else None,
        soft_fail_candidate_level="high_risk_candidate" if observed else "none",
        soft_fail_candidate_reason_summary=reason,
        review_gate_recommended=observed,
        advisory_only=True,
        advisory_review_observation_applied=True,
    )

