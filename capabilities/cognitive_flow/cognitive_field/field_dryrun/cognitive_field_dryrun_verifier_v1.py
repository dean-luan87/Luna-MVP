"""Independent verifier; reads serialized Field DryRun output only."""

from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .cognitive_field_dryrun_types_v1 import FIELD_DRYRUN_CASES_V1, FIELD_DRYRUN_PHASE_V1, FIELD_DRYRUN_SCHEMA_VERSION_V1

_FALSE_FLAGS = ("runtime_executed", "model_invoked", "provider_invoked", "external_call", "slam_invoked", "database_written", "field_kernel_mutated", "reducer_invoked", "state_mutation", "snapshot_updated", "temporal_history_modified", "fact_created", "decision_created", "action_created", "memory_updated", "learning_integrated")
_FORBIDDEN = {"state_id", "snapshot_write_target", "fact_id", "decision_id", "action_id", "memory_target"}


def verify_cognitive_field_dryrun_payload_v1(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    issues, checks = [], 0
    checks += 1
    if payload.get("schema_version") != FIELD_DRYRUN_SCHEMA_VERSION_V1 or payload.get("phase") != FIELD_DRYRUN_PHASE_V1: issues.append({"check_id":"root.identity","message":"schema or phase mismatch"})
    checks += 1
    if payload.get("execution_mode") != "controlled_dryrun" or payload.get("simulation_only") is not True or payload.get("fixture_only") is not True: issues.append({"check_id":"root.mode","message":"fixture-only DryRun mode required"})
    for name in _FALSE_FLAGS:
        checks += 1
        if payload.get(name) is not False: issues.append({"check_id":"guard."+name,"message":name+" must be false"})
    rows = payload.get("cases") if isinstance(payload.get("cases"), list) else []
    if len(rows) != len(FIELD_DRYRUN_CASES_V1): issues.append({"check_id":"case.count","message":"six fixed Field cases required"})
    seen = set()
    for row in rows:
        checks += 1
        candidate = row.get("candidate") if isinstance(row, Mapping) and isinstance(row.get("candidate"), Mapping) else {}
        case_id = row.get("case_id") if isinstance(row, Mapping) else None
        seen.add(case_id)
        if row.get("field_fixture_type") != FIELD_DRYRUN_CASES_V1.get(case_id): issues.append({"check_id":"case.mapping","message":"fixture mapping mismatch"})
        for key in ("field_candidate_id","context_refs","primitive_refs","concept_refs","temporal_scope","spatial_scope","task_scope","attention_scope","relevance_partition","uncertainty","provenance","trace_ref"):
            checks += 1
            if candidate.get(key) in (None,"",[],{},()): issues.append({"check_id":"candidate."+key,"message":"required field missing for "+str(case_id)})
        checks += 1
        if candidate.get("candidate_only") is not True or candidate.get("field_state") is not False or candidate.get("not_state") is not True or candidate.get("not_fact") is not True or _FORBIDDEN.intersection(candidate): issues.append({"check_id":"boundary.candidate","message":"candidate/state/fact boundary failed"})
        provenance = candidate.get("provenance")
        checks += 1
        if not isinstance(provenance, Mapping) or not all(provenance.get(k) for k in ("source_refs","concept_binding_refs","source_capability_refs")) or provenance.get("trace_ref") != candidate.get("trace_ref"): issues.append({"check_id":"trace.closure","message":"provenance chain incomplete"})
        checks += 1
        if not str(candidate.get("attention_scope", {}).get("priority_status", "")).endswith("selection_only"): issues.append({"check_id":"attention.boundary","message":"attention must be selection-only"})
    checks += 1
    if seen != set(FIELD_DRYRUN_CASES_V1): issues.append({"check_id":"case.coverage","message":"required case set missing"})
    return {"valid": not issues, "issues": issues, "checks_performed": checks, "verifier_independence":"serialized_output_only_no_runner_or_skeleton_import"}


def verify_cognitive_field_dryrun_file_v1(input_path: Path, compare_path: Path | None = None) -> Mapping[str, Any]:
    raw = input_path.read_text(encoding="utf-8"); payload = json.loads(raw); result = dict(verify_cognitive_field_dryrun_payload_v1(payload))
    result["canonical_serialization"] = raw == json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if compare_path is not None:
        result["comparison_equal"] = raw == compare_path.read_text(encoding="utf-8")
        if not result["comparison_equal"]: result["valid"] = False; result["issues"] = list(result["issues"])+[{"check_id":"determinism.comparison","message":"runs differ"}]
    return result


def main(argv: Iterable[str] | None = None) -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--input",required=True,type=Path); parser.add_argument("--compare",type=Path); args=parser.parse_args(argv)
    result=verify_cognitive_field_dryrun_file_v1(args.input,args.compare); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)); return 0 if result["valid"] else 1


if __name__ == "__main__": raise SystemExit(main())
