"""User-terminal fail-closed Verifier for controlled replay execution evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME


CANONICAL_COGNITION_OWNER = "Cognitive State Formation Governance"


def verify_summary_v1(summary: Dict[str, Any]) -> Dict[str, Any]:
    proof = summary.get("canonical_execution_proof") or {}
    transitions = proof.get("cognitive_transition_refs") or []
    checks: Dict[str, bool] = {
        "controlled_replay_mode": summary.get("execution_mode") == CONTROLLED_REPLAY_RUNTIME,
        "replay_input_identity_present": bool(summary.get("replay_input_ref")),
        "replay_origin_is_controlled_fixture": summary.get("replay_origin_class") == "CONTROLLED_RECORDED_FIXTURE",
        "gateway_admitted": summary.get("observation_gateway_admitted") is True,
        "gateway_admission_ref_present": bool(summary.get("observation_gateway_admission_ref")),
        "canonical_a_route_ingress_present": bool(summary.get("a_route_ingress_ref")),
        "canonical_a_route_execution_present": bool(summary.get("a_route_execution_ref")),
        "cognition_execution_claim_supported": summary.get("cognition_execution") is True
        and summary.get("runtime_executed") is True
        and proof.get("runtime_executed") is True,
        "execution_proof_is_canonical": proof.get("execution_proof_source") == "CognitiveStateFormationEngineV1.run_case",
        "execution_proof_mode_matches": proof.get("execution_mode") == CONTROLLED_REPLAY_RUNTIME,
        "canonical_cognition_owner": proof.get("owner_ref") == CANONICAL_COGNITION_OWNER,
        "execution_proof_candidate_boundary": proof.get("candidate_only") is True
        and proof.get("world_truth_declared") is False
        and proof.get("field_mutation") is False,
        "transition_proof_present": bool(transitions)
        and summary.get("cognitive_transition_count") == len(transitions)
        and summary.get("cognitive_transition_count", 0) >= 1,
        "transition_refs_are_not_evaluation_fixture": all(
            not str(ref).startswith(("fixture:", "synthetic-trace:", "evaluation:"))
            for ref in transitions
        ),
        "execution_proof_links_ingress": bool(proof.get("ingress_refs"))
        and bool(summary.get("replay_input_ref"))
        and summary.get("replay_input_ref") in proof.get("ingress_refs", []),
        "no_model_provider_live_observation_action": all(
            summary.get(key) is False
            for key in (
                "model_invocation",
                "provider_invocation",
                "live_observation_execution",
                "action_execution",
            )
        ),
        "canonical_proof_no_forbidden_capabilities": all(
            proof.get(key) is False
            for key in (
                "model_invocation",
                "provider_invocation",
                "live_observation_execution",
                "action_execution",
            )
        ),
        "no_field_mutation_or_world_truth": summary.get("field_mutation") is False
        and summary.get("world_truth_declared") is False,
        "no_validation_errors": not summary.get("validation_errors"),
        "synthetic_compatibility_declared": summary.get("synthetic_compatibility_preserved") is True,
    }
    issues: List[str] = [name for name, passed in checks.items() if not passed]
    return {
        "phase": "Phase-P1-Luna-A-Route-Controlled-Replay-Runtime-Enablement-v1-001",
        "checks": checks,
        "issues": issues,
        "all_checks_passed": not issues,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python -m capabilities.midplatform.core.a_route_orchestration.verify_a_route_controlled_replay_runtime_enablement_v1 <runner_summary.json>"
        )
    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = verify_summary_v1(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
