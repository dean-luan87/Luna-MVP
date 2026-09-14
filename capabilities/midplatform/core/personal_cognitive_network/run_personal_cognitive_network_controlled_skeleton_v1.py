"""Controlled runner for PCN skeleton using synthetic fixtures only.

This asset is created for user-side controlled execution. Agent must not execute it in this phase.
"""

from __future__ import annotations

from typing import Dict, List

from .personal_cognitive_network_fixture_v1 import get_pcn_synthetic_fixtures_v1
from .personal_cognitive_network_skeleton_v1 import PersonalCognitiveNetworkSkeletonV1


def run_controlled_skeleton() -> List[Dict[str, object]]:
    skeleton = PersonalCognitiveNetworkSkeletonV1()
    outputs: List[Dict[str, object]] = []
    for case in get_pcn_synthetic_fixtures_v1():
        result = skeleton.run_case(case)
        outputs.append(
            {
                "case_id": result.case_id,
                "skeleton_only": result.skeleton_only,
                "candidate_only": result.candidate_only,
                "runtime_executed": result.runtime_executed,
                "source_mutation_executed": result.source_mutation_executed,
                "persistence_executed": result.persistence_executed,
                "causal_reasoning_executed": result.causal_reasoning_executed,
                "intent_generation_executed": result.intent_generation_executed,
                "decision_executed": result.decision_executed,
                "projection_id": result.projection.projection_id,
                "trace_id": result.trace.trace_id,
                "active_reference_count": len(result.projection.active_reference_set),
                "active_link_count": len(result.projection.active_link_set),
            }
        )
    return outputs


def main() -> int:
    _ = run_controlled_skeleton()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
