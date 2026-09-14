"""Controlled runner for Cognitive Memory & Experience implementation v1.

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
        sentinel = (
            candidate / "capabilities/midplatform/core/cognitive_memory_experience"
        )
        if sentinel.is_dir():
            return candidate
    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/cognitive_memory_experience").is_dir():
        return cwd
    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_memory_experience.cognitive_memory_experience_engine_v1 import (  # noqa: E402
    CognitiveMemoryExperienceEngineV1,
)
from capabilities.midplatform.core.cognitive_memory_experience.cognitive_memory_experience_fixture_v1 import (  # noqa: E402
    get_cognitive_memory_experience_fixtures_v1,
)
from capabilities.midplatform.core.cognitive_memory_experience.cognitive_memory_experience_static_validators_v1 import (  # noqa: E402
    validate_output_contract,
)


OUTPUT_DIR = (
    REPO_ROOT / "_eval_out/cognitive_memory_experience_controlled_implementation_v1"
)


def run_controlled() -> Dict[str, Any]:
    engine = CognitiveMemoryExperienceEngineV1()
    fixtures = get_cognitive_memory_experience_fixtures_v1()
    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in fixtures:
        output = engine.run_case(case.request)
        checks = {
            "output_contract": validate_output_contract(output),
            "memory_type_expected": output.memory_candidate.memory_type
            == case.expected_memory_type,
            "admission_state_expected": output.admission_decision_candidate.admission_state
            == case.expected_admission_state,
            "retrieval_expected": (output.retrieval_candidate is not None)
            == case.expected_retrieval,
            "learning_evidence_expected": (
                output.learning_evidence_candidate is not None
            )
            == case.expected_learning_evidence,
            "personality_evidence_expected": (
                output.self_personality_evidence_candidate is not None
            )
            == case.expected_personality_evidence,
            "revision_expected": (output.revision_candidate is not None)
            == case.expected_revision,
            "supersession_expected": (output.supersession_candidate is not None)
            == case.expected_supersession,
            "revocation_expected": (output.revocation_candidate is not None)
            == case.expected_revocation,
            "expiration_expected": (output.expiration_candidate is not None)
            == case.expected_expiration,
            "negative_guards_expected": output.negative_guard_status is not None
            and all(
                getattr(output.negative_guard_status, key) == value
                for key, value in case.expected_negative_guards.items()
            ),
        }
        case_results.append(
            {
                "case_id": case.case_id,
                "description": case.description,
                "memory_type": output.memory_candidate.memory_type,
                "admission_state": output.admission_decision_candidate.admission_state,
                "retrieval": output.retrieval_candidate is not None,
                "learning_evidence": output.learning_evidence_candidate is not None,
                "personality_evidence": output.self_personality_evidence_candidate
                is not None,
                "revision": output.revision_candidate is not None,
                "supersession": output.supersession_candidate is not None,
                "revocation": output.revocation_candidate is not None,
                "expiration": output.expiration_candidate is not None,
                "checks": checks,
                "all_checks_passed": all(checks.values()),
            }
        )
        traces.append(
            {
                "case_id": case.case_id,
                "root_cycle_trace_id": output.trace.root_cycle_trace_id,
                "experience_candidate_id": output.trace.experience_candidate_id,
                "memory_candidate_id": output.trace.memory_candidate_id,
                "admission_trace": list(output.trace.admission_trace),
            }
        )

    all_cases_passed = all(item["all_checks_passed"] for item in case_results)
    summary = {
        "phase": "Phase-Luna-Cognitive-Memory-And-Experience-Governance-Controlled-Implementation-v1-001",
        "scenario_count": 28,
        "all_cases_passed": all_cases_passed,
        "runtime_execution": False,
        "database_write": False,
        "vector_store_write": False,
        "embedding_execution": False,
        "model_call": False,
        "source_owner_mutation": False,
        "learning_execution": False,
        "personality_mutation": False,
        "synthetic_only": True,
        "candidate_only": True,
        "passed_case_count": sum(
            1 for item in case_results if item["all_checks_passed"]
        ),
        "failed_case_count": sum(
            1 for item in case_results if not item["all_checks_passed"]
        ),
        "status": "COGNITIVE_MEMORY_EXPERIENCE_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }
    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "cognitive-memory-experience-controlled-implementation-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUT_DIR / "cognitive_memory_experience_result_v1.json"
    cases_path = OUTPUT_DIR / "cognitive_memory_experience_case_results_v1.json"
    trace_path = OUTPUT_DIR / "cognitive_memory_experience_trace_v1.json"
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
