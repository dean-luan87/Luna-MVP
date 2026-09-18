"""Controlled runner for Cognitive State Formation implementation v1.

This runner is intended for user-terminal execution only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        sentinel = candidate / "capabilities/midplatform/core/cognitive_state_formation"
        if sentinel.is_dir():
            return candidate

    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/cognitive_state_formation").is_dir():
        return cwd

    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (  # noqa: E402
    CognitiveStateFormationEngineV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_fixture_v1 import (  # noqa: E402
    get_cognitive_state_formation_fixtures_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_static_validators_v1 import (  # noqa: E402
    validate_field_ref_read_only_boundary,
    validate_output_contract,
)


OUTPUT_DIR = (
    REPO_ROOT / "_eval_out/cognitive_state_formation_controlled_implementation_v1"
)


def run_controlled() -> Dict[str, Any]:
    engine = CognitiveStateFormationEngineV1()
    fixtures = get_cognitive_state_formation_fixtures_v1()

    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in fixtures:
        output = engine.run_case(case.request)
        all_refs = (
            case.request.context_refs
            + case.request.pcn_refs
            + case.request.intent_refs
            + case.request.field_refs
            + case.request.observation_refs
            + case.request.risk_refs
            + case.request.uncertainty_refs
            + case.request.task_refs
            + case.request.role_refs
            + case.request.memory_refs
        )

        primary_state = output.cognitive_hypotheses[0].state
        checks = {
            "output_contract": validate_output_contract(output, all_refs),
            "field_ref_read_only": validate_field_ref_read_only_boundary(
                case.request.field_refs
            ),
            "world_kind_expected": output.current_world_candidate.world_state_kind_candidate
            == case.expected_world_kind,
            "hypothesis_state_expected": primary_state
            == case.expected_hypothesis_state,
            "attention_count_expected": len(output.attention_candidates)
            >= case.expected_min_attention_count,
            "risk_override_expected": output.attention_selection_candidate.risk_override_applied
            == case.expect_risk_override,
            "uncertainty_retention_expected": output.attention_selection_candidate.uncertainty_retained
            == case.expect_uncertainty_retention,
            "conflict_preservation_expected": bool(
                output.current_world_candidate.conflict_refs
            )
            == case.expect_conflict_preservation,
            "revision_lineage_expected": (len(output.trace.revision_lineage_refs) > 0)
            == case.expect_revision,
            "revocation_lineage_expected": (
                len(output.trace.revocation_lineage_refs) > 0
            )
            == case.expect_revocation,
            "synthetic_only": case.synthetic_only is True
            and case.request.synthetic_only is True,
            "candidate_only": output.candidate_only is True,
        }

        case_results.append(
            {
                "case_id": case.case_id,
                "description": case.description,
                "world_kind": output.current_world_candidate.world_state_kind_candidate,
                "hypothesis_state": primary_state,
                "selected_attention_refs": list(
                    output.attention_selection_candidate.selected_attention_refs
                ),
                "active_hypothesis_refs": list(
                    output.hypothesis_competition_result.active_hypothesis_refs
                ),
                "conflict_refs": list(output.current_world_candidate.conflict_refs),
                "checks": checks,
                "all_checks_passed": all(checks.values()),
            }
        )

        traces.append(
            {
                "case_id": case.case_id,
                "root_trace_id": output.trace.root_trace_id,
                "world_trace": output.trace.current_world_trace_ref,
                "handoff_trace": output.trace.downstream_handoff_trace_ref,
                "reverse_lookup_keys": sorted(
                    key for key, _ in output.provenance.reverse_lookup
                ),
            }
        )

    passed = sum(1 for item in case_results if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-Cognitive-State-Formation-Controlled-Implementation-v1-001",
        "case_count": len(case_results),
        "passed_case_count": passed,
        "failed_case_count": len(case_results) - passed,
        "candidate_only": True,
        "runtime_executed": False,
        "source_mutation_executed": False,
        "status": "COGNITIVE_STATE_FORMATION_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }

    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "cognitive-state-formation-controlled-implementation-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result_path = OUTPUT_DIR / "cognitive_state_formation_result_v1.json"
    case_path = OUTPUT_DIR / "cognitive_state_formation_case_results_v1.json"
    trace_path = OUTPUT_DIR / "cognitive_state_formation_trace_v1.json"

    result_path.write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    case_path.write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    trace_path.write_text(
        json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "result": str(result_path),
        "cases": str(case_path),
        "trace": str(trace_path),
    }


def main() -> int:
    payload = run_controlled()
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
