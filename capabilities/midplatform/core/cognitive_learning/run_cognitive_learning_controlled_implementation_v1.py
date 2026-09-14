"""Controlled runner for Cognitive Learning implementation v1.

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
        sentinel = candidate / "capabilities/midplatform/core/cognitive_learning"
        if sentinel.is_dir():
            return candidate
    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/cognitive_learning").is_dir():
        return cwd
    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_learning.cognitive_learning_engine_v1 import (  # noqa: E402
    CognitiveLearningEngineV1,
)
from capabilities.midplatform.core.cognitive_learning.cognitive_learning_fixture_v1 import (  # noqa: E402
    get_cognitive_learning_fixtures_v1,
)
from capabilities.midplatform.core.cognitive_learning.cognitive_learning_static_validators_v1 import (  # noqa: E402
    validate_output_contract,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/cognitive_learning_controlled_implementation_v1"


def run_controlled() -> Dict[str, Any]:
    engine = CognitiveLearningEngineV1()
    fixtures = get_cognitive_learning_fixtures_v1()
    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in fixtures:
        output = engine.run_case(case.request)
        checks = {
            "output_contract": validate_output_contract(output),
            "learning_kind_expected": output.learning_candidate.learning_kind
            == case.expected_learning_kind,
            "generalization_expected": output.generalization_assessment.generalization_level_candidate
            == case.expected_generalization_level,
            "admission_state_expected": output.admission_decision_candidate.admission_state
            == case.expected_admission_state,
            "parameter_update_expected": (output.parameter_update_candidate is not None)
            == case.expected_parameter_update,
            "contradiction_expected": (output.contradiction_candidate is not None)
            == case.expected_contradiction,
            "counterexample_expected": (output.counterexample_candidate is not None)
            == case.expected_counterexample,
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
                "learning_kind": output.learning_candidate.learning_kind,
                "generalization_level": output.generalization_assessment.generalization_level_candidate,
                "admission_state": output.admission_decision_candidate.admission_state,
                "parameter_update": output.parameter_update_candidate is not None,
                "contradiction": output.contradiction_candidate is not None,
                "counterexample": output.counterexample_candidate is not None,
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
                "learning_trace_id": output.trace.learning_trace_id,
                "learning_evidence_id": output.trace.learning_evidence_id,
                "learning_candidate_id": output.trace.learning_candidate_id,
                "parameter_update_candidate_id": output.trace.parameter_update_candidate_id,
            }
        )

    all_cases_passed = all(item["all_checks_passed"] for item in case_results)
    summary = {
        "phase": "Phase-Luna-Cognitive-Learning-Governance-Controlled-Implementation-v1-001",
        "scenario_count": 32,
        "all_cases_passed": all_cases_passed,
        "runtime_execution": False,
        "runtime_training": False,
        "model_weight_update": False,
        "database_write": False,
        "vector_store_write": False,
        "embedding_execution": False,
        "parameter_mutation": False,
        "parameter_activation": False,
        "genome_activation": False,
        "memory_mutation": False,
        "intent_mutation": False,
        "state_mutation": False,
        "personality_mutation": False,
        "emotion_mutation": False,
        "semantic_compression_execution": False,
        "cross_user_transfer": False,
        "source_owner_mutation": False,
        "synthetic_only": True,
        "candidate_only": True,
        "passed_case_count": sum(
            1 for item in case_results if item["all_checks_passed"]
        ),
        "failed_case_count": sum(
            1 for item in case_results if not item["all_checks_passed"]
        ),
        "status": "COGNITIVE_LEARNING_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }
    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "cognitive-learning-controlled-implementation-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUT_DIR / "cognitive_learning_result_v1.json"
    cases_path = OUTPUT_DIR / "cognitive_learning_case_results_v1.json"
    trace_path = OUTPUT_DIR / "cognitive_learning_trace_v1.json"
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
