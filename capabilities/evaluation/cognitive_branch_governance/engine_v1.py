"""Controlled evaluation engine for candidate-only Branch Governance."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from capabilities.midplatform.core.cognitive_flow.cognitive_branch_governance_v1 import (
    govern_cognitive_branches,
)

from .fixtures_v1 import SOURCE_MODE, build_branch_governance_cases_v1


class CognitiveBranchGovernanceEvaluationEngineV1:
    """Build deterministic governance decisions from synthetic candidates."""

    def run(self) -> Dict[str, Any]:
        cases = []
        for case in build_branch_governance_cases_v1():
            before = tuple(asdict(branch) for branch in case.request.branch_candidates)
            result = govern_cognitive_branches(case.request)
            after = tuple(asdict(branch) for branch in case.request.branch_candidates)
            cases.append(
                {
                    "case_id": case.case_id,
                    "evaluation_marker": case.evaluation_marker,
                    "expected_statuses": list(case.expected_statuses),
                    "request": asdict(case.request),
                    "candidate_snapshot_before": before,
                    "candidate_snapshot_after": after,
                    "result": asdict(result),
                }
            )

        return {
            "phase": "Phase-P1-Luna-Cognitive-Branch-Governance-v1-001",
            "source_mode": SOURCE_MODE,
            "governance_algorithm": (
                "explicit current-state refs; absent canonical equivalence "
                "retains distinct candidates; no semantic similarity, resource "
                "or execution policy"
            ),
            "cases": cases,
            "candidate_only": True,
            "read_only": True,
            "formation_executed": False,
            "new_branch_generated": False,
            "winner_take_all": False,
            "execution_priority_assigned": False,
            "resource_governance_executed": False,
            "resource_acquisition": False,
            "observation_demand_formed": False,
            "capability_requirement_formed": False,
            "current_world_mutation": False,
            "field_mutation": False,
            "truth_declared": False,
            "world_truth_declared": False,
            "decision_formed": False,
            "task_formed": False,
            "action_formed": False,
            "provider_invocation": False,
            "model_invocation": False,
            "memory_pcn_mutation": False,
            "merge_executed": False,
            "convergence_executed": False,
            "close_executed": False,
            "reopen_executed": False,
            "goal_string_governance": False,
            "question_string_governance": False,
            "scenario_id_semantic_driver": False,
            "case_id_semantic_driver": False,
            "fixture_specific_mapping": False,
            "semantic_string_similarity": False,
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


__all__ = ["CognitiveBranchGovernanceEvaluationEngineV1"]
