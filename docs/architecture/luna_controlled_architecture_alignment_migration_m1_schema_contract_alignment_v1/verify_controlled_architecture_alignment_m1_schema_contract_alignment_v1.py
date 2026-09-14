"""PLANNING_CANDIDATE static verifier for M1 schema/contract alignment."""

from __future__ import annotations

import json
import py_compile
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "schema_ownership_mapping.json",
    "existing_contract_compatibility_review.md",
    "existing_contract_compatibility_matrix.json",
    "field_context_projection_contract_candidate.json",
    "observation_cognitive_handoff_contract_candidate.json",
    "memory_context_projection_contract_candidate.json",
    "personal_cognitive_network_reference_contract_candidate.json",
    "intent_binding_contract_candidate.json",
    "causal_candidate_contract_candidate.json",
    "experience_memory_projection_contract_candidate.json",
    "a_b_route_handoff_contract_candidate.json",
    "decision_input_contract_candidate.json",
    "cognitive_boundary_flow_contract_candidate.json",
    "legacy_compatibility_rollback_contract_candidate.json",
    "blocked_contract_registry.json",
    "schema_contract_alignment_plan.md",
    "m1_schema_contract_alignment_summary.md",
    "m1_change_manifest.json",
    "phase_contract.json",
    "verify_controlled_architecture_alignment_m1_schema_contract_alignment_v1.py",
]

CHAIN_CONTRACT_FILES = [
    "field_context_projection_contract_candidate.json",
    "observation_cognitive_handoff_contract_candidate.json",
    "memory_context_projection_contract_candidate.json",
    "personal_cognitive_network_reference_contract_candidate.json",
    "intent_binding_contract_candidate.json",
    "causal_candidate_contract_candidate.json",
    "experience_memory_projection_contract_candidate.json",
    "a_b_route_handoff_contract_candidate.json",
    "decision_input_contract_candidate.json",
    "cognitive_boundary_flow_contract_candidate.json",
]

CHAIN_REQUIRED_FIELDS = [
    "owner",
    "producer",
    "consumer",
    "candidate_fact",
    "unknown",
    "trace",
    "replay",
    "admission",
    "revision",
    "revocation",
    "failure_behavior",
    "write_authority",
]

PCN_FORBIDDEN_OWNERSHIP = {
    "Self",
    "Role",
    "Relationship",
    "Memory",
    "Emotion",
    "Value",
    "Belief",
}

BOUNDARY_ALLOWED_FLOWS = {
    "Field -> PCN",
    "Observation -> Evidence",
    "Memory -> Context",
    "PCN -> Intent/Causal Context",
    "Decision -> Action Candidate",
    "Outcome -> Experience",
}

BOUNDARY_FORBIDDEN_FLOWS = {
    "Model -> Cognitive Fact",
    "Observation -> Decision",
    "Memory -> Reality Override",
    "PCN -> Source Mutation",
    "Task Manager -> Intent",
}


def load_json(filename: str) -> dict:
    return json.loads((ROOT / filename).read_text(encoding="utf-8"))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def check_required_files(failures: list[str]) -> None:
    for name in REQUIRED_FILES:
        require((ROOT / name).is_file(), f"missing_required_file:{name}", failures)


def check_markdown_files(failures: list[str]) -> None:
    for name in [
        "existing_contract_compatibility_review.md",
        "schema_contract_alignment_plan.md",
        "m1_schema_contract_alignment_summary.md",
    ]:
        content = (ROOT / name).read_text(encoding="utf-8").strip()
        require(bool(content), f"markdown_empty:{name}", failures)
        require(
            "PLANNING_CANDIDATE" in content, f"missing_planning_marker:{name}", failures
        )


def check_json_parse(failures: list[str]) -> dict[str, dict]:
    parsed: dict[str, dict] = {}
    for path in ROOT.glob("*.json"):
        try:
            parsed[path.name] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"json_parse_error:{path.name}:{exc.msg}")
    return parsed


def check_contract_fields(parsed: dict[str, dict], failures: list[str]) -> None:
    for name in CHAIN_CONTRACT_FILES:
        payload = parsed.get(name, {})
        for field in CHAIN_REQUIRED_FIELDS:
            require(
                field in payload, f"missing_contract_field:{name}:{field}", failures
            )
        require(
            payload.get("planning_status") == "PLANNING_CANDIDATE",
            f"missing_planning_status:{name}",
            failures,
        )
        require(payload.get("consumer"), f"missing_consumer:{name}", failures)
        require(
            bool(payload.get("write_authority")),
            f"missing_write_authority:{name}",
            failures,
        )


def check_field_restrictions(parsed: dict[str, dict], failures: list[str]) -> None:
    field_payload = parsed["field_context_projection_contract_candidate.json"]
    require(
        field_payload.get("allowed_payload_fields")
        == [
            "field_id",
            "field_state",
            "world_state",
            "evidence_reference",
            "temporal_validity",
            "uncertainty",
            "trace",
        ],
        "field_allowed_payload_mismatch",
        failures,
    )
    require(
        set(field_payload.get("forbidden_payload_fields", []))
        == {"intent", "decision", "action", "memory_mutation"},
        "field_forbidden_payload_mismatch",
        failures,
    )


def check_observation_restrictions(
    parsed: dict[str, dict], failures: list[str]
) -> None:
    payload = parsed["observation_cognitive_handoff_contract_candidate.json"]
    require(
        set(payload.get("allowed_payload_fields", []))
        == {
            "observation_candidate",
            "priority",
            "evidence",
            "collection_recommendation",
        },
        "observation_allowed_payload_mismatch",
        failures,
    )
    require(
        set(payload.get("forbidden_payload_fields", []))
        == {"decision", "fact", "action"},
        "observation_forbidden_payload_mismatch",
        failures,
    )


def check_memory_restrictions(parsed: dict[str, dict], failures: list[str]) -> None:
    payload = parsed["memory_context_projection_contract_candidate.json"]
    require(
        set(payload.get("allowed_payload_fields", []))
        == {
            "historical_reference",
            "experience_reference",
            "association",
            "provenance",
        },
        "memory_allowed_payload_mismatch",
        failures,
    )
    require(
        set(payload.get("forbidden_payload_fields", []))
        == {"reality_override", "decision", "source_mutation"},
        "memory_forbidden_payload_mismatch",
        failures,
    )


def check_pcn_boundary(parsed: dict[str, dict], failures: list[str]) -> None:
    payload = parsed["personal_cognitive_network_reference_contract_candidate.json"]
    boundary = payload.get("pcn_boundary", {})
    require(
        set(boundary.get("allowed_responsibilities", []))
        == {"Connection", "Activation", "Context Projection"},
        "pcn_allowed_responsibilities_mismatch",
        failures,
    )
    require(
        set(boundary.get("forbidden_ownership", [])) == PCN_FORBIDDEN_OWNERSHIP,
        "pcn_forbidden_ownership_mismatch",
        failures,
    )
    require(
        boundary.get("source_owner_precedence") is True,
        "pcn_source_owner_precedence_missing",
        failures,
    )


def check_compatibility(parsed: dict[str, dict], failures: list[str]) -> None:
    matrix = parsed["existing_contract_compatibility_matrix.json"]
    modules = {entry.get("module") for entry in matrix.get("modules", [])}
    expected = {
        "Field State Reducer",
        "Field Read Model",
        "Observation Manager",
        "Task Manager",
        "Model Manager",
        "Protocol Manager",
        "OCR Manager",
        "Vision Manager",
        "Memory",
    }
    require(modules == expected, "compatibility_modules_incomplete", failures)
    for entry in matrix.get("modules", []):
        require(
            bool(entry.get("compatibility_alias")),
            f"missing_compatibility_alias:{entry.get('module')}",
            failures,
        )
        require(
            bool(entry.get("compatibility_status")),
            f"missing_compatibility_status:{entry.get('module')}",
            failures,
        )


def check_rollback(parsed: dict[str, dict], failures: list[str]) -> None:
    payload = parsed["legacy_compatibility_rollback_contract_candidate.json"]
    records = payload.get("records", [])
    require(bool(records), "rollback_records_missing", failures)
    for record in records:
        for key in [
            "existing_contract",
            "candidate_contract",
            "compatibility_alias",
            "rollback_trigger",
            "rollback_scope",
        ]:
            require(bool(record.get(key)), f"missing_rollback_field:{key}", failures)


def check_single_writer_and_cycles(
    parsed: dict[str, dict], failures: list[str]
) -> None:
    payload = parsed["schema_ownership_mapping.json"]
    schemas = payload.get("schemas", [])
    seen_names: set[str] = set()
    for schema in schemas:
        name = schema.get("schema_name")
        require(bool(name), "missing_schema_name", failures)
        require(name not in seen_names, f"duplicate_schema_name:{name}", failures)
        seen_names.add(name)
        require(
            bool(schema.get("write_authority")),
            f"missing_schema_write_authority:{name}",
            failures,
        )
    edges = payload.get("dependency_graph", {}).get("edges", [])
    graph: dict[str, set[str]] = {}
    indegree: dict[str, int] = {}
    for schema in seen_names:
        graph[schema] = set()
        indegree[schema] = 0
    for edge in edges:
        source = edge.get("from")
        target = edge.get("to")
        if source not in graph or target not in graph:
            continue
        if target not in graph[source]:
            graph[source].add(target)
            indegree[target] += 1
    ready = [name for name, degree in indegree.items() if degree == 0]
    visited = 0
    while ready:
        current = ready.pop()
        visited += 1
        for nxt in graph[current]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
    require(visited == len(graph), "cyclic_dependency_detected", failures)


def check_boundary_contract(parsed: dict[str, dict], failures: list[str]) -> None:
    payload = parsed["cognitive_boundary_flow_contract_candidate.json"]
    require(
        set(payload.get("allowed_flows", [])) == BOUNDARY_ALLOWED_FLOWS,
        "allowed_boundary_flow_mismatch",
        failures,
    )
    require(
        set(payload.get("forbidden_flows", [])) == BOUNDARY_FORBIDDEN_FLOWS,
        "forbidden_boundary_flow_mismatch",
        failures,
    )


def check_manifest_and_phase(parsed: dict[str, dict], failures: list[str]) -> None:
    manifest = parsed["m1_change_manifest.json"]
    require(
        manifest.get("modified_existing_files") == [],
        "modified_existing_files_not_empty",
        failures,
    )
    require(
        manifest.get("code_files_changed") == [],
        "code_files_changed_not_empty",
        failures,
    )
    require(
        manifest.get("runtime_files_changed") == [],
        "runtime_files_changed_not_empty",
        failures,
    )
    require(
        manifest.get("active_schema_files_changed") == [],
        "active_schema_files_changed_not_empty",
        failures,
    )
    require(
        manifest.get("active_contract_files_changed") == [],
        "active_contract_files_changed_not_empty",
        failures,
    )
    require(
        manifest.get("migration_executed") is False, "migration_executed_true", failures
    )
    phase = parsed["phase_contract.json"]
    require(
        phase.get("Execution Mode") == "Planning Only",
        "phase_execution_mode_mismatch",
        failures,
    )
    require(
        phase.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "phase_stop_point_mismatch",
        failures,
    )


def check_blocked_registry(parsed: dict[str, dict], failures: list[str]) -> None:
    blocked = parsed["blocked_contract_registry.json"]
    require(
        blocked.get("blocked_contracts") == [], "blocked_contracts_not_empty", failures
    )
    require(blocked.get("blocker_count") == 0, "blocker_count_not_zero", failures)


def check_py_compile(failures: list[str]) -> None:
    try:
        py_compile.compile(
            str(
                ROOT
                / "verify_controlled_architecture_alignment_m1_schema_contract_alignment_v1.py"
            ),
            doraise=True,
        )
    except py_compile.PyCompileError as exc:
        failures.append(f"py_compile_failed:{exc.msg}")


def main() -> int:
    failures: list[str] = []
    check_required_files(failures)
    if failures:
        print("CHECKS")
        print("required_files")
        print("FAILED_CHECKS")
        for failure in failures:
            print(failure)
        print("PASSED_CHECK_COUNT")
        print(0)
        print("FAILED_CHECK_COUNT")
        print(len(failures))
        print("BLOCKER_COUNT")
        print(len(failures))
        print("FINAL_DECISION")
        print("BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT")
        print("REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1

    check_markdown_files(failures)
    parsed = check_json_parse(failures)
    if not failures:
        check_contract_fields(parsed, failures)
        check_field_restrictions(parsed, failures)
        check_observation_restrictions(parsed, failures)
        check_memory_restrictions(parsed, failures)
        check_pcn_boundary(parsed, failures)
        check_compatibility(parsed, failures)
        check_rollback(parsed, failures)
        check_single_writer_and_cycles(parsed, failures)
        check_boundary_contract(parsed, failures)
        check_manifest_and_phase(parsed, failures)
        check_blocked_registry(parsed, failures)
        check_py_compile(failures)

    checks = [
        "required_files",
        "markdown_nonempty",
        "json_parse",
        "owner_producer_consumer",
        "candidate_fact_unknown_trace_replay_admission_revision_revocation_failure_behavior",
        "pcn_boundary",
        "compatibility",
        "rollback",
        "single_writer",
        "acyclic_dependency",
        "no_code_change",
        "no_runtime_modification",
        "py_compile",
    ]
    print("CHECKS")
    for item in checks:
        print(item)
    print("FAILED_CHECKS")
    for failure in failures:
        print(failure)
    print("PASSED_CHECK_COUNT")
    print(len(checks) - len(failures) if len(failures) <= len(checks) else 0)
    print("FAILED_CHECK_COUNT")
    print(len(failures))
    print("BLOCKER_COUNT")
    print(len(failures))
    print("FINAL_DECISION")
    print("V0_STATIC_CHECK_READY" if not failures else "BLOCKED_BY_VERIFIER_FAILURE")
    print("NEXT")
    print(
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
        if not failures
        else "REMEDIATE_REPORTED_FAILURES_ONLY"
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
