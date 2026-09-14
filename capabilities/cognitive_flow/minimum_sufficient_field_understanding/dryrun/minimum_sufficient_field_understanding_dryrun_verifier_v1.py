"""Independent serialized-output verifier for Minimum Sufficient Field Understanding DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping, Tuple

from .minimum_sufficient_field_understanding_dryrun_serializer_v1 import write_canonical_json_v1


_EXPECTED_CASE_IDS_V1 = (
    "unknown_dark_environment", "industrial_factory_partial_understanding", "public_space_unknown_field",
    "identity_known_behavior_limited", "exploration_boundary_not_permission", "information_gap_preservation",
)
_FORBIDDEN_KEYS_V1 = frozenset(("fact_id", "decision_id", "action_id", "state_write_target", "memory_target", "permission_scope"))
_REQUIRED_FALSE_FLAGS_V1 = (
    "runtime_executed", "inference_executed", "model_invoked", "provider_invoked", "external_call",
    "action_created", "decision_created", "field_kernel_integrated", "reducer_integrated", "state_mutation",
    "memory_updated", "learning_integrated", "hive_integrated",
)


def _contains_forbidden_key_v1(value: object) -> bool:
    if isinstance(value, Mapping):
        return bool(set(value) & _FORBIDDEN_KEYS_V1) or any(_contains_forbidden_key_v1(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_key_v1(item) for item in value)
    return False


def verify_controlled_dryrun_output_v1(output_dir: Path) -> Mapping[str, object]:
    """Read only serialized evidence; never calls runner or skeleton."""

    payload = json.loads((output_dir / "dryrun_result_v1.json").read_text(encoding="utf-8"))
    issues = []
    cases = payload.get("cases", [])
    if tuple(payload.get("case_ids", ())) != _EXPECTED_CASE_IDS_V1 or len(cases) != 6:
        issues.append("case_inventory_invalid")
    statuses = {case.get("candidate", {}).get("identity_status") for case in cases}
    if statuses != {"known", "partially_known", "unknown"}:
        issues.append("identity_status_coverage_invalid")
    for case in cases:
        candidate = case.get("candidate", {})
        boundary = candidate.get("behavior_boundary", {})
        if not all(candidate.get(flag) is True for flag in ("candidate_only", "not_fact", "not_state", "not_decision", "not_action")):
            issues.append("candidate_boundary_invalid:" + str(case.get("case_id")))
        if not candidate.get("provenance", {}).get("source_refs") or candidate.get("provenance", {}).get("trace_ref") != candidate.get("trace_ref"):
            issues.append("provenance_invalid:" + str(case.get("case_id")))
        if boundary.get("exploration_boundary", {}).get("permission_granted") is not False:
            issues.append("exploration_permission_violation:" + str(case.get("case_id")))
        if _contains_forbidden_key_v1(candidate):
            issues.append("forbidden_authority_key:" + str(case.get("case_id")))
    flags = payload.get("runtime_flags", {})
    if any(flags.get(name) is not False for name in _REQUIRED_FALSE_FLAGS_V1):
        issues.append("runtime_boundary_invalid")
    if flags.get("fixture_only") is not True or flags.get("simulation_only") is not True:
        issues.append("fixture_boundary_invalid")
    if payload.get("deterministic_run2_equal") is not True:
        issues.append("deterministic_check_failed")
    return {"valid": not issues, "issues": sorted(issues), "case_count": len(cases), "verifier_independent": True, "runner_called": False, "skeleton_called": False}


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify serialized MSFU Controlled DryRun v1 output.")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    result = verify_controlled_dryrun_output_v1(args.output_dir)
    write_canonical_json_v1(args.output_dir / "verification_result_v1.json", result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
