"""Deterministic growth candidate skeleton from synthetic fixtures."""

from __future__ import annotations

from typing import Dict, Tuple

from .personal_cognitive_growth_types_v1 import (
    DormancyCandidate,
    LinkGrowthCandidate,
    LinkStrengtheningCandidate,
    LinkWeakeningCandidate,
    ReactivationCandidate,
)


def prepare_growth_candidates(case: Dict[str, object]) -> Dict[str, Tuple[object, ...]]:
    case_id = str(case.get("case_id", "unknown_case"))
    growth = []
    strengthen = []
    weaken = []
    dormant = []
    reactivate = []

    if case.get("new_link_candidate"):
        growth.append(
            LinkGrowthCandidate(
                candidate_id=f"growth-{case_id}",
                growth_reason="fixture_declared",
                source_ref_a=str(case.get("source_ref_a", "ref-a")),
                source_ref_b=str(case.get("source_ref_b", "ref-b")),
                relation_type=str(case.get("relation_type", "RELATED")),
                candidate_only=True,
            )
        )
    if case.get("strengthening_candidate"):
        strengthen.append(
            LinkStrengtheningCandidate(
                candidate_id=f"strengthen-{case_id}",
                link_id=str(case.get("link_id", "link-unknown")),
                strengthening_reason="fixture_declared",
                candidate_only=True,
            )
        )
    if case.get("weakening_candidate"):
        weaken.append(
            LinkWeakeningCandidate(
                candidate_id=f"weaken-{case_id}",
                link_id=str(case.get("link_id", "link-unknown")),
                weakening_reason="fixture_declared",
                candidate_only=True,
            )
        )
    if case.get("dormancy_candidate"):
        dormant.append(
            DormancyCandidate(
                candidate_id=f"dormant-{case_id}",
                link_id=str(case.get("link_id", "link-unknown")),
                dormant_reason="fixture_declared",
                dormant_not_deleted=True,
                candidate_only=True,
            )
        )
    if case.get("reactivation_candidate"):
        reactivate.append(
            ReactivationCandidate(
                candidate_id=f"reactivate-{case_id}",
                link_id=str(case.get("link_id", "link-unknown")),
                trigger_ref=str(case.get("trigger_ref", "context-trigger")),
                historical_state_ref=str(
                    case.get("historical_state_ref", "HISTORICAL")
                ),
                candidate_only=True,
            )
        )

    return {
        "new_link_candidate": tuple(growth),
        "strengthening_candidate": tuple(strengthen),
        "weakening_candidate": tuple(weaken),
        "dormancy_candidate": tuple(dormant),
        "reactivation_candidate": tuple(reactivate),
    }
