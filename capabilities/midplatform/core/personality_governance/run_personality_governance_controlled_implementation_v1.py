"""User-terminal synthetic runner for Personality Governance controlled implementation v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List


def _find_repo_root(start: Path) -> Path:
    """Walk upward to a stable repository sentinel; never depend on cwd."""
    for candidate in (start, *start.parents):
        if (
            (candidate / "capabilities").is_dir()
            and (candidate / "docs").is_dir()
            and (candidate / "README.md").is_file()
        ):
            return candidate
    raise RuntimeError("stable repository sentinel not found")


MODULE_DIR = Path(__file__).resolve().parent
REPO_ROOT = _find_repo_root(MODULE_DIR)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.personality_governance.personality_governance_engine_v1 import (  # noqa: E402
    PersonalityGovernanceEngineV1,
)
from capabilities.midplatform.core.personality_governance.personality_governance_fixture_v1 import (  # noqa: E402
    get_personality_governance_fixture_v1,
)
from capabilities.midplatform.core.personality_governance.personality_governance_registry_v1 import (  # noqa: E402
    CANONICAL_OWNER,
    NEGATIVE_GUARDS,
    SEMANTIC_COMPRESSION_STATUS,
)
from capabilities.midplatform.core.personality_governance.personality_governance_static_validators_v1 import (  # noqa: E402
    validate_candidate_flags,
    validate_output,
)


OUTPUT_DIR = Path("_eval_out/personality_governance_controlled_implementation_v1")


def _case_result(case: Any, output: Any) -> Dict[str, Any]:
    checks = {
        "expected_stability_actual": output.trait_candidate.stability_candidate == case.expected_stability,
        "expected_admission_actual": output.admission_decision.admission_state == case.expected_admission_state,
        "expected_profile_actual": (output.profile_candidate is not None) == case.expected_profile,
        "expected_revision_actual": (output.revision_candidate is not None) == case.expected_revision,
        "expected_supersession_actual": (output.supersession_candidate is not None) == case.expected_supersession,
        "expected_revocation_actual": (output.revocation_candidate is not None) == case.expected_revocation,
        "expected_expiration_actual": (output.expiration_candidate is not None) == case.expected_expiration,
        "expected_sensitivity_actual": output.trait_candidate.sensitivity == case.expected_sensitivity,
        "expected_duplicate_guard_actual": output.admission_decision.duplicate_evidence_guard_triggered == case.expected_duplicate_guard,
        "expected_user_correction_actual": (output.user_correction_candidate is not None) == case.expected_user_correction,
        "expected_emotion_bridge_actual": (output.emotion_to_personality_candidate is not None) == case.expected_emotion_bridge,
        "candidate_only": output.candidate_only and output.synthetic_only and output.trait_candidate.candidate_only,
        "trait_not_activated": output.trait_candidate.activated is False and output.trait_activation is False,
        "trait_not_persisted": output.trait_candidate.persisted is False,
        "truth_not_declared": output.trait_candidate.truth_declared is False,
        "profile_not_single_score": output.profile_candidate is None or output.profile_candidate.single_personality_score is None,
        "profile_not_identity": output.profile_candidate is None or output.profile_candidate.immutable_identity is False,
        "profile_not_action": output.profile_candidate is None or output.profile_candidate.direct_action_control is False,
        "trace_reverse_locatable": output.trace.reverse_locatable and output.provenance.reverse_locatable,
        "trace_no_authority": output.trace.provenance_grants_authority is False,
        "semantic_compression_deferred": output.semantic_compression_status == SEMANTIC_COMPRESSION_STATUS,
        "negative_guards": all(value is False for key, value in output.negative_guard_status.guards if key not in {"synthetic_only", "candidate_only"}),
        "static_validation": not validate_output(output) and not validate_candidate_flags(output),
        "engine_issues_empty": not output.issues,
    }
    return {
        "scenario_id": case.scenario_id,
        "title": case.title,
        "expected": {
            "stability": case.expected_stability,
            "admission_state": case.expected_admission_state,
            "profile": case.expected_profile,
            "revision": case.expected_revision,
            "supersession": case.expected_supersession,
            "revocation": case.expected_revocation,
            "expiration": case.expected_expiration,
            "sensitivity": case.expected_sensitivity,
            "duplicate_guard": case.expected_duplicate_guard,
            "user_correction": case.expected_user_correction,
            "emotion_bridge": case.expected_emotion_bridge,
        },
        "actual": {
            "stability": output.trait_candidate.stability_candidate,
            "admission_state": output.admission_decision.admission_state,
            "trait_dimension": output.trait_candidate.trait_dimension,
            "candidate_only": output.trait_candidate.candidate_only,
            "activated": output.trait_candidate.activated,
            "persisted": output.trait_candidate.persisted,
            "truth_declared": output.trait_candidate.truth_declared,
            "profile_candidate_id": output.profile_candidate.profile_candidate_id if output.profile_candidate else None,
            "contradiction_refs": list(output.trait_candidate.contradiction_refs),
            "counterexample_refs": list(output.trait_candidate.counterexample_refs),
            "semantic_compression_status": output.semantic_compression_status,
        },
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }


def build_runner_result() -> Dict[str, Any]:
    engine = PersonalityGovernanceEngineV1()
    case_results: List[Dict[str, Any]] = []
    trace_results: List[Dict[str, Any]] = []
    raw_outputs: List[Any] = []
    for case in get_personality_governance_fixture_v1():
        output = engine.run_case(case.request)
        raw_outputs.append(output)
        case_results.append(_case_result(case, output))
        trace_results.append({
            "scenario_id": case.scenario_id,
            "trace": asdict(output.trace),
            "provenance": asdict(output.provenance),
            "reverse_locatable": output.trace.reverse_locatable and output.provenance.reverse_locatable,
            "provenance_grants_authority": output.trace.provenance_grants_authority,
            "contradiction_refs": list(output.trace.contradiction_refs),
            "counterexample_refs": list(output.trace.counterexample_refs),
            "lineage": {
                "revision_refs": list(output.trace.revision_refs),
                "supersession_refs": list(output.trace.supersession_refs),
                "revocation_refs": list(output.trace.revocation_refs),
                "expiration_refs": list(output.trace.expiration_refs),
            },
        })
    failed = [item["scenario_id"] for item in case_results if not item["all_checks_passed"]]
    summary = {
        "scenario_count": len(case_results),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "canonical_owner": CANONICAL_OWNER,
        "runtime_execution": False,
        "database_write": False,
        "vector_store_write": False,
        "embedding_execution": False,
        "model_call": False,
        "scheduler_execution": False,
        "task_mutation": False,
        "device_control": False,
        "source_owner_mutation": False,
        "personality_trait_activation": False,
        "semantic_compression_status": SEMANTIC_COMPRESSION_STATUS,
        "semantic_compression_execution": False,
        "affective_memory_compression": False,
        "emotion_memory_summary_generation": False,
        "personality_memory_semantic_fusion": False,
        "cross_user_transfer": False,
        "synthetic_only": True,
        "candidate_only": True,
        "negative_guards": dict(NEGATIVE_GUARDS),
    }
    return {"summary": summary, "case_results": case_results, "trace_results": trace_results, "raw_outputs": raw_outputs}


def main() -> int:
    result = build_runner_result()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "personality_governance_result_v1.json").write_text(json.dumps(result["summary"], indent=2), encoding="utf-8")
    (OUTPUT_DIR / "personality_governance_case_results_v1.json").write_text(json.dumps(result["case_results"], indent=2), encoding="utf-8")
    (OUTPUT_DIR / "personality_governance_trace_v1.json").write_text(json.dumps(result["trace_results"], indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
    return 0 if result["summary"]["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
