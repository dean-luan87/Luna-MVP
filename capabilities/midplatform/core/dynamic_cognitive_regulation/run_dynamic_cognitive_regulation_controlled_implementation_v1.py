"""User-terminal controlled runner for Dynamic Cognitive Regulation v1.

The runner executes deterministic synthetic fixtures only and writes evaluation
artifacts.  It does not invoke Luna Runtime, models, providers, devices,
schedulers, tasks, databases, or upstream mutations.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        sentinel = candidate / "capabilities/midplatform/core/dynamic_cognitive_regulation"
        if sentinel.is_dir():
            return candidate
    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/dynamic_cognitive_regulation").is_dir():
        return cwd
    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()
if __package__ in {None, ""} and str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_engine_v1 import (
    DynamicCognitiveRegulationEngineV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_fixture_v1 import (
    get_dynamic_regulation_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_static_validators_v1 import (
    validate_bounds_contract,
    validate_output_contract,
    validate_parameter_class_coverage,
    validate_parameter_kind_coverage,
    validate_state_vector_boundary,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_registry_v1 import (
    CANONICAL_OWNER,
)


OUTPUT_DIR = (
    REPO_ROOT / "_eval_out/dynamic_cognitive_regulation_controlled_implementation_v1"
)


def _all_source_refs(request: Any) -> tuple[Any, ...]:
    return (
        request.context_refs
        + request.pcn_refs
        + request.intent_refs
        + request.hypothesis_refs
        + request.emotion_refs
        + request.resource_refs
        + request.learning_update_refs
    )


def run_controlled() -> Dict[str, Any]:
    engine = DynamicCognitiveRegulationEngineV1()
    fixtures = get_dynamic_regulation_synthetic_fixtures_v1()
    case_results: List[Dict[str, Any]] = []
    case_traces: List[Dict[str, Any]] = []

    all_parameter_kinds = tuple(
        item.parameter_kind
        for case in fixtures
        for item in case.request.parameter_candidates
    )
    class_coverage = validate_parameter_class_coverage()
    kind_coverage = validate_parameter_kind_coverage(all_parameter_kinds)

    for case in fixtures:
        output = engine.evaluate(case.request)
        duplicate_output = engine.evaluate(case.request)
        bounds_by_parameter = {
            item.parameter_id: item for item in case.request.parameter_bounds
        }
        influence_kinds = {
            item.influence_kind
            for item in output.regulation_candidate.influence_candidates
        }
        reason_codes = set(output.regulation_candidate.reason_codes)
        revision_expected = case.scenario_id == "R17"
        revocation_expected = case.scenario_id == "R18"
        conflict_expected = case.scenario_id == "R13"
        idempotency_expected = case.scenario_id == "R19"
        genome_expected = case.scenario_id == "R16"

        checks = {
            "scenario_id_preserved": output.scenario_id == case.scenario_id,
            "expected_behavior_status": (
                output.regulation_candidate.evaluation_status == case.expected_status
            ),
            "expected_reason_tokens": set(case.expected_reason_tokens).issubset(
                reason_codes
            ),
            "expected_influence_kinds": set(
                case.expected_influence_kinds
            ).issubset(influence_kinds),
            "state_vector_boundary_behavior": (
                (
                    not validate_state_vector_boundary(
                        case.request.cognitive_state_vector_candidate
                    )
                )
                if case.scenario_id == "R15"
                else validate_state_vector_boundary(
                    case.request.cognitive_state_vector_candidate
                )
            ),
            "parameter_class_coverage": class_coverage,
            "parameter_kind_coverage": kind_coverage,
            "bounds_contract": validate_bounds_contract(
                case.request.parameter_bounds
            ),
            "output_contract": validate_output_contract(
                output, _all_source_refs(case.request), bounds_by_parameter
            ),
            "canonical_owner": output.regulation_candidate.owner == CANONICAL_OWNER,
            "candidate_only": output.candidate_only is True
            and output.regulation_candidate.candidate_only is True,
            "synthetic_only": case.synthetic_only is True
            and case.request.synthetic_only is True
            and output.synthetic_only is True,
            "no_runtime_execution": output.runtime_executed is False,
            "no_source_mutation": output.source_mutation_executed is False,
            "revision_lineage": (
                (output.revision_candidate is not None)
                == revision_expected
                and (
                    not revision_expected
                    or bool(output.trace.revision_lineage_refs)
                )
            ),
            "revocation_lineage": (
                (output.revocation_candidate is not None)
                == revocation_expected
                and (
                    not revocation_expected
                    or bool(output.trace.revocation_lineage_refs)
                )
            ),
            "conflict_preservation": (
                bool(output.regulation_candidate.conflict_candidates)
                == conflict_expected
            ),
            "idempotent_result": (
                not idempotency_expected
                or asdict(output.regulation_candidate)
                == asdict(duplicate_output.regulation_candidate)
            ),
            "parameter_genome_candidate_only": (
                (output.genome_candidate is not None) == genome_expected
                and (
                    not genome_expected
                    or (
                        output.genome_candidate.candidate_only is True
                        and output.genome_candidate.active is False
                        and output.genome_candidate.persisted is False
                        and output.genome_candidate.model_weights_rewritten is False
                        and output.genome_candidate.user_identity_modified is False
                        and output.genome_candidate.cross_user_propagated is False
                        and output.genome_candidate.learned_truth is False
                    )
                )
            ),
        }

        actual_behavior = {
            "evaluation_status": output.regulation_candidate.evaluation_status,
            "state_candidate": output.regulation_candidate.state_candidate,
            "reason_codes": list(output.regulation_candidate.reason_codes),
            "influence_kinds": sorted(influence_kinds),
            "modulations": [
                {
                    "parameter_id": item.parameter_id,
                    "parameter_kind": item.parameter_kind,
                    "parameter_class": item.parameter_class,
                    "requested_value": item.requested_value,
                    "effective_value": item.effective_value,
                    "evaluation_status": item.evaluation_status,
                    "boundary_action": item.boundary_action,
                    "reason_codes": list(item.reason_codes),
                    "silent_coercion": item.silent_coercion,
                }
                for item in output.regulation_candidate.modulation_candidates
            ],
            "conflict_count": len(
                output.regulation_candidate.conflict_candidates
            ),
            "revision_lineage_present": bool(output.trace.revision_lineage_refs),
            "revocation_lineage_present": bool(
                output.trace.revocation_lineage_refs
            ),
            "handoff_candidate_only": output.handoff_candidate.candidate_only,
            "runtime_executed": output.runtime_executed,
            "source_mutation_executed": output.source_mutation_executed,
        }
        case_results.append(
            {
                "scenario_id": case.scenario_id,
                "scenario_name": case.name,
                "expected_behavior": case.expected_behavior,
                "actual_behavior": actual_behavior,
                "checks": checks,
                "all_checks_passed": all(checks.values()),
            }
        )
        case_traces.append(
            {
                "scenario_id": case.scenario_id,
                "root_trace_id": output.trace.root_trace_id,
                "cognitive_state_vector_ref": output.trace.cognitive_state_vector_ref,
                "source_influence_refs": list(output.trace.source_influence_refs),
                "parameter_refs": list(output.trace.parameter_refs),
                "parameter_bounds_refs": list(output.trace.parameter_bounds_refs),
                "policy_refs": list(output.trace.policy_refs),
                "regulation_function_id": output.trace.regulation_function_id,
                "regulation_function_version": output.trace.regulation_function_version,
                "prior_regulation_candidate_ref": output.trace.prior_regulation_candidate_ref,
                "resulting_regulation_candidate_ref": output.trace.resulting_regulation_candidate_ref,
                "influence_handoff_trace_ref": output.trace.influence_handoff_trace_ref,
                "revision_lineage_refs": list(output.trace.revision_lineage_refs),
                "revocation_lineage_refs": list(output.trace.revocation_lineage_refs),
                "reverse_lookup": {
                    key: list(value) for key, value in output.trace.reverse_lookup.items()
                },
                "reverse_locatable": output.provenance.reverse_locatable,
                "provenance_grants_authority": output.trace.provenance_grants_authority,
            }
        )

    passed = sum(1 for item in case_results if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-Dynamic-Cognitive-Regulation-Controlled-Implementation-v1-001",
        "canonical_owner": CANONICAL_OWNER,
        "scenario_count": len(case_results),
        "passed_case_count": passed,
        "failed_case_count": len(case_results) - passed,
        "scenario_ids": [item["scenario_id"] for item in case_results],
        "synthetic_only": True,
        "candidate_only": True,
        "runtime_executed": False,
        "database_write": False,
        "device_control": False,
        "scheduler_execution": False,
        "task_mutation": False,
        "model_call": False,
        "source_module_mutation": False,
        "status": "DYNAMIC_COGNITIVE_REGULATION_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE",
    }
    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "dynamic-cognitive-regulation-controlled-implementation-trace-v1",
            "case_traces": case_traces,
            "candidate_only": True,
            "reverse_locatable": True,
            "provenance_grants_authority": False,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUT_DIR / "dynamic_cognitive_regulation_result_v1.json"
    cases_path = OUTPUT_DIR / "dynamic_cognitive_regulation_case_results_v1.json"
    trace_path = OUTPUT_DIR / "dynamic_cognitive_regulation_trace_v1.json"
    result_path.write_text(
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
        "result": str(result_path),
        "cases": str(cases_path),
        "trace": str(trace_path),
    }


def main() -> int:
    payload = run_controlled()
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
