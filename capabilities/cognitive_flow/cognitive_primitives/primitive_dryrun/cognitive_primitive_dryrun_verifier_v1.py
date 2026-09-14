"""Independent serialized-output verifier; never imports Runner or Skeleton."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .cognitive_primitive_dryrun_serializer_v1 import canonical_json_v1
from .cognitive_primitive_dryrun_types_v1 import PRIMITIVE_DRYRUN_PHASE_V1, PRIMITIVE_DRYRUN_RESULT_V1, PRIMITIVE_DRYRUN_SCHEMA_V1


_EXPECTED = {
    "case_1_vision_entity": "entity_primitive_candidate", "case_2_ocr_entity": "entity_primitive_candidate", "case_3_spatial_relation": "relation_primitive_candidate", "case_4_temporal_event": "event_primitive_candidate", "case_5_context_situation": "situation_primitive_candidate",
}


def verify_cognitive_primitive_dryrun_v1(output_dir: Path, comparison_dir: Path | None = None):
    path = output_dir / PRIMITIVE_DRYRUN_RESULT_V1
    raw = path.read_text(encoding="utf-8") if path.is_file() else ""
    try: source = json.loads(raw)
    except json.JSONDecodeError: source = {}
    flags = source.get("runtime_flags", {})
    checks = [raw == canonical_json_v1(source), source.get("phase") == PRIMITIVE_DRYRUN_PHASE_V1, source.get("schema_version") == PRIMITIVE_DRYRUN_SCHEMA_V1, source.get("all_cases_passed") is True, source.get("blocker_count") == 0, source.get("runtime_executed") is False, source.get("simulation_only") is True, all(flags.get(key) is False for key in ("runtime_executed", "model_invoked", "external_call", "database_written", "field_kernel_mutated", "reducer_invoked", "fact_created", "decision_created", "action_created", "state_writeback", "memory_updated"))]
    seen = set()
    for item in source.get("case_results", []):
        candidate, case_id = item.get("candidate", {}), item.get("case_id")
        seen.add(case_id)
        checks += [case_id in _EXPECTED, candidate.get("primitive_type") == _EXPECTED.get(case_id), item.get("schema_valid") is True, item.get("semantic_boundary_valid") is True, item.get("provenance_valid") is True, item.get("negative_guards_valid") is True, item.get("case_passed") is True, candidate.get("candidate_only") is True, candidate.get("fact_status") == "not_fact", not any(key in candidate for key in ("fact_id", "decision_id", "action_id", "state_write_target", "memory_target"))]
    checks.append(seen == set(_EXPECTED))
    comparison_ok = True
    if comparison_dir is not None:
        other = comparison_dir / PRIMITIVE_DRYRUN_RESULT_V1
        comparison_ok = other.is_file() and other.read_text(encoding="utf-8") == raw
        checks.append(comparison_ok)
    failed = sum(not check for check in checks)
    return {"verifier_id": "cognitive_primitive_dryrun_verifier_v1", "passed_checks": len(checks) - failed, "failed_checks": failed, "case_count": len(source.get("case_results", [])), "verifier_invoked_runner": False, "verifier_invoked_skeleton": False, "comparison_run_checked": comparison_dir is not None, "comparison_run_equal": comparison_ok if comparison_dir is not None else None, "blocker_count": failed, "warning_count": int(source.get("warning_count", 0)), "final_candidate_decision": "COGNITIVE_PRIMITIVE_DRYRUN_VERIFICATION_CANDIDATE_PASS" if failed == 0 else "COGNITIVE_PRIMITIVE_DRYRUN_VERIFICATION_CANDIDATE_BLOCKED"}


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", required=True); parser.add_argument("--comparison-dir")
    args = parser.parse_args(); print(canonical_json_v1(verify_cognitive_primitive_dryrun_v1(Path(args.output_dir), Path(args.comparison_dir) if args.comparison_dir else None)))


if __name__ == "__main__": main()
