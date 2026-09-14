"""User-terminal synthetic runner for Self Governance controlled implementation v1."""

from __future__ import annotations

import json
import sys
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


PHASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = _find_repo_root(PHASE_DIR)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.self_governance.self_governance_engine_v1 import SelfGovernanceEngineV1
from capabilities.midplatform.core.self_governance.self_governance_fixture_v1 import get_self_governance_fixture_v1
from capabilities.midplatform.core.self_governance.self_governance_registry_v1 import CANONICAL_OWNER, NEGATIVE_GUARDS
from capabilities.midplatform.core.self_governance.self_governance_static_validators_v1 import validate_output


OUTPUT_DIR = Path("_eval_out/self_governance_controlled_implementation_v1")


def _case_result(case: Any, output: Any) -> Dict[str, Any]:
    checks = {
        "expected_boundary_actual": output.boundary_class == case.expected_boundary_class,
        "expected_state_actual": output.self_attribution is not None and output.self_attribution.state == case.expected_state,
        "expected_domain_actual": output.self_attribution is not None and output.self_attribution.attribution_domain == case.expected_domain,
        "expected_continuity_actual": (output.self_continuity is not None) == case.expected_continuity,
        "expected_revision_actual": (output.revision is not None) == case.expected_revision,
        "expected_revocation_actual": (output.revocation is not None) == case.expected_revocation,
        "expected_supersession_actual": (output.supersession is not None) == case.expected_supersession,
        "expected_expiration_actual": (output.expiration is not None) == case.expected_expiration,
        "expected_influence_actual": tuple(item.evidence_kind for item in output.influences) == case.expected_influence_kinds,
        "expected_sensitivity_actual": output.self_reference.sensitivity == case.expected_sensitivity,
        "expected_duplicate_guard_actual": output.duplicate_guard_triggered == case.expected_duplicate_guard,
        "expected_user_correction_actual": output.user_correction_precedence == case.expected_user_correction_precedence,
        "idempotency_guard_set": len(output.idempotency_guards) == 8,
        "candidate_only": output.candidate_only is True and output.self_reference.candidate_only is True,
        "fact_not_admitted": output.self_reference.fact_admitted is False and (output.self_attribution is None or output.self_attribution.fact_admitted is False),
        "no_persistence": output.self_reference.persisted is False and (output.self_attribution is None or output.self_attribution.persisted is False),
        "static_validation": not validate_output(output),
    }
    return {
        "scenario_id": case.scenario_id,
        "title": case.title,
        "expected": {
            "boundary_class": case.expected_boundary_class,
            "state": case.expected_state,
            "domain": case.expected_domain,
            "continuity": case.expected_continuity,
            "revision": case.expected_revision,
            "revocation": case.expected_revocation,
            "supersession": case.expected_supersession,
            "expiration": case.expected_expiration,
            "influence_kinds": list(case.expected_influence_kinds),
            "sensitivity": case.expected_sensitivity,
        },
        "actual": {
            "boundary_class": output.boundary_class,
            "state": output.self_attribution.state if output.self_attribution else None,
            "domain": output.self_attribution.attribution_domain if output.self_attribution else None,
            "candidate_only": output.candidate_only,
            "fact_admitted": output.self_reference.fact_admitted,
            "persisted": output.self_reference.persisted,
        },
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }


def build_runner_result() -> Dict[str, Any]:
    engine = SelfGovernanceEngineV1()
    case_results: List[Dict[str, Any]] = []
    trace_results: List[Dict[str, Any]] = []
    for case in get_self_governance_fixture_v1():
        output = engine.run_case(case.request)
        case_results.append(_case_result(case, output))
        trace_results.append({
            "scenario_id": case.scenario_id,
            "root_cycle_trace_id": output.trace.root_cycle_trace_id,
            "self_trace_id": output.trace.self_trace_id,
            "self_ref_id": output.trace.self_ref_id,
            "self_attribution_id": output.trace.self_attribution_id,
            "continuity_id": output.trace.continuity_id,
            "source_refs": list(output.provenance.original_source_refs),
            "evidence_refs": list(output.provenance.evidence_refs),
            "provenance_refs": list(output.trace.provenance_refs),
            "revision_refs": list(output.trace.revision_refs),
            "revocation_refs": list(output.trace.revocation_refs),
            "reverse_locatable": output.trace.reverse_locatable and output.provenance.reverse_locatable,
            "provenance_grants_authority": output.trace.provenance_grants_authority,
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
        "source_owner_mutation": False,
        "personality_mutation": False,
        "emotion_mutation": False,
        "semantic_compression_execution": False,
        "cross_user_transfer": False,
        "synthetic_only": True,
        "candidate_only": True,
        "negative_guards": dict(NEGATIVE_GUARDS),
    }
    return {"summary": summary, "case_results": case_results, "trace_results": trace_results}


def main() -> int:
    result = build_runner_result()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "self_governance_result_v1.json").write_text(json.dumps(result["summary"], indent=2), encoding="utf-8")
    (OUTPUT_DIR / "self_governance_case_results_v1.json").write_text(json.dumps(result["case_results"], indent=2), encoding="utf-8")
    (OUTPUT_DIR / "self_governance_trace_v1.json").write_text(json.dumps(result["trace_results"], indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
    return 0 if result["summary"]["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
