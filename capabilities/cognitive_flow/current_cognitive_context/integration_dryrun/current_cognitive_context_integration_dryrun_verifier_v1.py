"""Independent serialized-output verifier; it never calls runner or skeleton."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Mapping
from .current_cognitive_context_integration_dryrun_serializer_v1 import write_canonical_json_v1

_EXPECTED = ("home_member_context", "workplace_assistant_context", "navigation_assistant_context", "unknown_environment_context", "role_conflict_context", "goal_change_context")
_FALSE_FLAGS = ("runtime_executed", "context_inferred", "model_invoked", "external_call", "field_kernel_integrated", "reducer_integrated", "state_mutation", "decision_created", "action_created", "memory_updated", "learning_integrated", "hive_integrated", "role_inferred", "role_evolved")

def verify_integration_dryrun_v1(output_dir: Path) -> Mapping[str, object]:
    value = json.loads((output_dir / "integration_dryrun_result_v1.json").read_text(encoding="utf-8"))
    issues = []
    cases = value.get("cases", [])
    if tuple(case.get("case_id") for case in cases) != _EXPECTED: issues.append("case_inventory_invalid")
    for case in cases:
        candidate = case.get("candidate", {})
        if not case.get("role_reference") or not case.get("goal_reference"): issues.append("role_goal_reference_missing")
        if not all(candidate.get(key) is True for key in ("candidate_only", "not_fact", "not_state", "not_decision", "not_action", "not_memory")): issues.append("candidate_boundary_invalid")
        if not candidate.get("field_reference") or not candidate.get("attention_context_reference") or not candidate.get("survival_context_reference") or not candidate.get("information_gap_reference") or not candidate.get("spatial_scope_reference") or not candidate.get("temporal_scope_reference") or not candidate.get("provenance_reference") or not candidate.get("trace_reference"): issues.append("reference_closure_invalid")
    flags = value.get("runtime_flags", {})
    if any(flags.get(name) is not False for name in _FALSE_FLAGS): issues.append("runtime_boundary_invalid")
    if flags.get("fixture_only") is not True or flags.get("simulation_only") is not True: issues.append("fixture_boundary_invalid")
    if value.get("deterministic_run2_equal") is not True: issues.append("deterministic_check_failed")
    return {"valid": not issues, "issues": sorted(set(issues)), "case_count": len(cases), "verifier_independent": True, "runner_called": False, "skeleton_called": False}

def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", required=True, type=Path); args = parser.parse_args()
    result = verify_integration_dryrun_v1(args.output_dir)
    write_canonical_json_v1(args.output_dir / "verification_result_v1.json", result)
    print(json.dumps(result, sort_keys=True))
    if not result["valid"]: raise SystemExit(1)
if __name__ == "__main__": main()
