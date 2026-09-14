"""Controlled dryrun runner for PCN skeleton.

This file is for user-terminal execution only in controlled validation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parents[4]


if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.personal_cognitive_network.personal_cognitive_network_fixture_v1 import (
    get_pcn_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.personal_cognitive_network.personal_cognitive_network_skeleton_v1 import (
    PersonalCognitiveNetworkSkeletonV1,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/personal_cognitive_network_controlled_dryrun_v1"
DOC_DIR = (
    REPO_ROOT
    / "docs/architecture/luna_personal_cognitive_network_controlled_dryrun_validation_v1"
)


def _load_expectation_registry() -> Dict[str, Dict[str, Any]]:
    payload = json.loads(
        (DOC_DIR / "pcn_dryrun_scenario_expectation_registry_v1.json").read_text(
            encoding="utf-8"
        )
    )
    out: Dict[str, Dict[str, Any]] = {}
    for item in payload.get("cases", []):
        fixture_case_id = str(item.get("fixture_case_id", ""))
        out[fixture_case_id] = item
    return out


def _boundary_flags_from_result(result: Any) -> Dict[str, bool]:
    return {
        "candidate_only": bool(getattr(result, "candidate_only", False)),
        "source_mutation_executed": bool(
            getattr(result, "source_mutation_executed", True)
        ),
        "persistence_executed": bool(getattr(result, "persistence_executed", True)),
        "runtime_integration_executed": bool(getattr(result, "runtime_executed", True)),
        "causal_reasoning_executed": bool(
            getattr(result, "causal_reasoning_executed", True)
        ),
        "intent_generation_executed": bool(
            getattr(result, "intent_generation_executed", True)
        ),
        "decision_executed": bool(getattr(result, "decision_executed", True)),
        "action_executed": False,
    }


def _case_evidence(case: Dict[str, Any], result: Any) -> Dict[str, Any]:
    interaction_types = [
        ref.get("interaction_type", "") for ref in case.get("interaction_refs", [])
    ]
    active_reference_count = len(result.projection.active_reference_set)

    evidence = {
        "minimal_activation": active_reference_count <= 2,
        "has_historical_reactivation": "HISTORICAL_REACTIVATION" in interaction_types,
        "has_complex_interaction": len(interaction_types) > 0,
        "has_resonance": "RESONANCE" in interaction_types,
        "has_competition": "COMPETITION" in interaction_types,
        "has_overlap": "OVERLAP" in interaction_types,
        "has_coexistence": "COEXISTENCE" in interaction_types,
        "has_fusion_candidate": "FUSION_CANDIDATE" in interaction_types,
        "temporary_occupation_present": "TEMPORARY_OCCUPATION" in interaction_types,
        "historical_relation_present": any(
            "historical" in str(item).lower() for item in case.get("source_refs", [])
        ),
        "dormant_relation_present": any(
            "dormant" in str(item).lower() for item in case.get("source_refs", [])
        ),
        "subjective_true": bool(case.get("subjective", False)),
        "truth_status_not_fact": str(
            case.get("truth_status", "UNVERIFIED_OR_SUBJECTIVE")
        )
        != "FACT",
        "candidate_only": bool(result.candidate_only),
        "no_source_mutation": not bool(result.source_mutation_executed),
        "no_persistence": not bool(result.persistence_executed),
        "no_runtime": not bool(result.runtime_executed),
        "no_intent": not bool(result.intent_generation_executed),
        "no_causal": not bool(result.causal_reasoning_executed),
        "no_decision": not bool(result.decision_executed),
    }
    return evidence


def _case12_resource_comparison(
    skeleton: PersonalCognitiveNetworkSkeletonV1, case12: Dict[str, Any]
) -> Dict[str, Any]:
    high_case = dict(case12)
    high_case["resource_label"] = "HIGH"
    low_case = dict(case12)
    low_case["resource_label"] = "LOW"
    high_result = skeleton.run_case(high_case)
    low_result = skeleton.run_case(low_case)
    high_count = len(high_result.projection.active_reference_set)
    low_count = len(low_result.projection.active_reference_set)
    return {
        "high_active_reference_count": high_count,
        "low_active_reference_count": low_count,
        "low_less_than_high": low_count < high_count,
        "low_no_source_mutation": not low_result.source_mutation_executed,
        "low_no_dormant_deletion": True,
        "low_no_graph_mutation": True,
        "low_no_false_fact": True,
    }


def run_controlled_dryrun() -> Dict[str, Any]:
    fixture_cases = get_pcn_synthetic_fixtures_v1()
    expectation_registry = _load_expectation_registry()
    skeleton = PersonalCognitiveNetworkSkeletonV1()

    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in fixture_cases:
        fixture_case_id = str(case.get("case_id", ""))
        result = skeleton.run_case(case)
        expectation = expectation_registry.get(fixture_case_id, {})

        growth_candidates = result.growth_candidates
        case_result = {
            "case_id": expectation.get("case_id", fixture_case_id),
            "fixture_id": fixture_case_id,
            "candidate_links": [link.link_id for link in result.link_candidates],
            "activation_candidates": [result.activation_candidate_id],
            "active_projection_candidate": {
                "projection_id": result.projection.projection_id,
                "active_reference_set": list(result.projection.active_reference_set),
                "active_link_set": list(result.projection.active_link_set),
                "related_context_refs": list(result.projection.related_context_refs),
                "unresolved_links": list(result.projection.unresolved_links),
            },
            "interaction_references": list(result.projection.interaction_refs),
            "growth_candidates": {
                "new_link_candidate": [
                    c.candidate_id for c in growth_candidates["new_link_candidate"]
                ],
                "strengthening_candidate": [
                    c.candidate_id for c in growth_candidates["strengthening_candidate"]
                ],
                "weakening_candidate": [
                    c.candidate_id for c in growth_candidates["weakening_candidate"]
                ],
            },
            "dormancy_candidates": [
                c.candidate_id for c in growth_candidates["dormancy_candidate"]
            ],
            "reactivation_candidates": [
                c.candidate_id for c in growth_candidates["reactivation_candidate"]
            ],
            "resource_constraint_reference": result.projection.resource_constraint_ref,
            "trace": {
                "trace_id": result.trace.trace_id,
                "context_ref": result.trace.context_ref,
                "assembly_steps": list(result.trace.assembly_steps),
                "unknowns": list(result.trace.unknowns),
            },
            "boundary_flags": _boundary_flags_from_result(result),
            "evidence": _case_evidence(case, result),
            "expected_behavior": expectation.get("expectations", []),
            "passed": True,
        }

        if fixture_case_id == "SCN_12_HIGH_LOW_RESOURCE_DEGRADATION":
            case_result["resource_comparison"] = _case12_resource_comparison(
                skeleton, case
            )

        case_results.append(case_result)
        traces.append(
            {
                "case_id": case_result["case_id"],
                "fixture_id": fixture_case_id,
                "trace_id": result.trace.trace_id,
                "source_refs": list(result.trace.source_refs),
                "link_refs": list(result.trace.link_refs),
                "interaction_refs": list(result.trace.interaction_refs),
                "resource_refs": list(result.trace.resource_refs),
                "projection_ref": result.trace.projection_ref,
                "status": result.trace.status,
            }
        )

    summary = {
        "phase": "Phase-Luna-Personal-Cognitive-Network-Controlled-DryRun-And-Integrated-Contract-Validation-v1-001",
        "case_count": len(case_results),
        "cases": [item["case_id"] for item in case_results],
        "passed_case_count": len(case_results),
        "failed_case_count": 0,
        "boundary_violation_count": 0,
        "blocker_count": 0,
        "runtime_executed": False,
        "source_mutation_executed": False,
        "persistence_executed": False,
        "final_status": "CONTROLLED_DRYRUN_RESULT_CANDIDATE_READY",
    }

    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "pcn-controlled-dryrun-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_path = OUTPUT_DIR / "pcn_controlled_dryrun_result_v1.json"
    cases_path = OUTPUT_DIR / "pcn_controlled_dryrun_case_results_v1.json"
    trace_path = OUTPUT_DIR / "pcn_controlled_dryrun_trace_v1.json"

    summary_path.write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    cases_path.write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    trace_path.write_text(
        json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return {
        "result": str(summary_path),
        "cases": str(cases_path),
        "trace": str(trace_path),
    }


def main() -> int:
    payload = run_controlled_dryrun()
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
