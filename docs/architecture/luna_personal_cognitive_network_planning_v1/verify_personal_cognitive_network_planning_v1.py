"""PLANNING_CANDIDATE verifier for Phase-Luna-Personal-Cognitive-Network-Planning-v1-001."""

from __future__ import annotations

import ast
import json
import py_compile
import sys
from pathlib import Path


def resolve_root() -> Path:
    script_path = Path(__file__) if "__file__" in globals() else None
    if script_path and script_path.exists():
        return script_path.resolve().parent

    cwd = Path.cwd().resolve()
    fallback = cwd / "docs/architecture/luna_personal_cognitive_network_planning_v1"
    if fallback.is_dir():
        return fallback

    return cwd


ROOT = resolve_root()

REQUIRED_FILES = [
    "personal_cognitive_network_object_model_candidate.json",
    "personal_cognitive_link_schema_candidate.json",
    "personal_cognitive_network_growth_model_candidate.json",
    "personal_cognitive_network_activation_model_candidate.json",
    "personal_cognitive_network_dormancy_reactivation_candidate.json",
    "personal_subjective_cognitive_boundary_candidate.json",
    "pcn_causal_boundary_contract_candidate.json",
    "pcn_memory_boundary_contract_candidate.json",
    "context_pcn_activation_contract_candidate.json",
    "pcn_context_projection_contract_candidate.json",
    "pcn_resource_constraint_model_candidate.json",
    "pcn_nested_constraint_model_candidate.json",
    "pcn_minimum_scenario_simulation_candidate.json",
    "pcn_architecture_risk_review.md",
    "personal_cognitive_network_planning_summary.md",
    "pcn_planning_change_manifest.json",
    "phase_contract.json",
    "verify_personal_cognitive_network_planning_v1.py",
]

REQUIRED_REFERENCE_PATHS = [
    "docs/architecture/luna_dynamic_cognitive_architecture_realignment_planning_v1/personal_cognitive_network_boundary.json",
    "docs/architecture/luna_controlled_architecture_alignment_migration_m1_schema_contract_alignment_v1/personal_cognitive_network_reference_contract_candidate.json",
    "docs/architecture/luna_context_foundation_module_closure_v1/context_to_pcn_handoff_contract_candidate.json",
]

PROJECT_ROOT = ROOT.parents[2]


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def load_json(filename: str) -> dict:
    return json.loads((ROOT / filename).read_text(encoding="utf-8"))


def check_required_files(failures: list[str]) -> None:
    for filename in REQUIRED_FILES:
        require(
            (ROOT / filename).is_file(), f"missing_required_file:{filename}", failures
        )


def check_json_parse(failures: list[str]) -> dict[str, dict]:
    parsed: dict[str, dict] = {}
    for path in ROOT.glob("*.json"):
        try:
            parsed[path.name] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"json_parse_error:{path.name}:{exc.msg}")
    return parsed


def check_markdown_nonempty(failures: list[str]) -> None:
    for filename in [
        "pcn_architecture_risk_review.md",
        "personal_cognitive_network_planning_summary.md",
    ]:
        content = (ROOT / filename).read_text(encoding="utf-8").strip()
        require(bool(content), f"markdown_empty:{filename}", failures)
        require(
            "PLANNING_CANDIDATE" in content,
            f"missing_planning_marker:{filename}",
            failures,
        )


def check_reference_validation(failures: list[str]) -> None:
    for rel in REQUIRED_REFERENCE_PATHS:
        require(
            (PROJECT_ROOT / rel).is_file(),
            f"missing_required_reference:{rel}",
            failures,
        )


def check_owner_uniqueness(parsed: dict[str, dict], failures: list[str]) -> None:
    object_model = parsed["personal_cognitive_network_object_model_candidate.json"]
    reference_types = object_model["source_object_reference_model"][
        "supported_reference_types"
    ]
    require(
        len(reference_types) == len(set(reference_types)),
        "duplicate_source_reference_type",
        failures,
    )

    nested = parsed["pcn_nested_constraint_model_candidate.json"]
    relations = [item.get("relation") for item in nested.get("relationships", [])]
    require(
        len(relations) == len(set(relations)), "duplicate_nested_relation", failures
    )


def check_no_source_object_ownership(
    parsed: dict[str, dict], failures: list[str]
) -> None:
    object_model = parsed["personal_cognitive_network_object_model_candidate.json"]
    forbidden = set(
        object_model["source_object_reference_model"]["forbidden_behaviors"]
    )
    require(
        "source_object_ownership_transfer" in forbidden,
        "source_ownership_transfer_not_forbidden",
        failures,
    )
    require(
        "source_object_persistence" in forbidden,
        "source_persistence_not_forbidden",
        failures,
    )
    require(
        "source_object_mutation" in forbidden, "source_mutation_not_forbidden", failures
    )

    pcn_memory = parsed["pcn_memory_boundary_contract_candidate.json"]
    pcn_memory_forbidden = set(pcn_memory.get("forbidden", []))
    require(
        "pcn_copies_memory_body" in pcn_memory_forbidden,
        "memory_copy_not_forbidden",
        failures,
    )
    require(
        "pcn_modifies_memory" in pcn_memory_forbidden,
        "memory_modify_not_forbidden",
        failures,
    )


def check_not_memory_causal_kg(parsed: dict[str, dict], failures: list[str]) -> None:
    object_model = parsed["personal_cognitive_network_object_model_candidate.json"]
    not_set = set(object_model.get("pcn_is_not", []))
    require("Memory" in not_set, "pcn_memory_separation_missing", failures)
    require("Causal Engine" in not_set, "pcn_causal_separation_missing", failures)
    require("Knowledge Graph" in not_set, "pcn_kg_separation_missing", failures)

    pcn_causal = parsed["pcn_causal_boundary_contract_candidate.json"]
    require(
        "pcn_generates_causal_fact" in set(pcn_causal.get("forbidden", [])),
        "pcn_causal_fact_forbidden_missing",
        failures,
    )


def check_candidate_fact_boundary(parsed: dict[str, dict], failures: list[str]) -> None:
    for filename, payload in parsed.items():
        if not filename.endswith(".json"):
            continue
        if filename == "phase_contract.json":
            continue
        if filename == "pcn_planning_change_manifest.json":
            continue
        require(
            payload.get("planning_status") == "PLANNING_CANDIDATE",
            f"planning_status_missing:{filename}",
            failures,
        )
        if "candidate_only" in payload:
            require(
                payload.get("candidate_only") is True,
                f"candidate_only_false:{filename}",
                failures,
            )

    object_model = parsed["personal_cognitive_network_object_model_candidate.json"]
    boundary = object_model.get("candidate_fact_boundary", {})
    require(
        boundary.get("candidate_only") is True,
        "object_model_candidate_only_missing",
        failures,
    )
    require(boundary.get("not_fact") is True, "object_model_not_fact_missing", failures)


def check_subjective_boundary(parsed: dict[str, dict], failures: list[str]) -> None:
    subj = parsed["personal_subjective_cognitive_boundary_candidate.json"]
    required = {
        "subjective",
        "bias",
        "self_interest",
        "non_rational",
        "logically_incomplete",
        "internally_contradictory",
        "emotion_driven",
    }
    require(
        required.issubset(set(subj.get("subjective_cognition_allowed", []))),
        "subjective_modes_incomplete",
        failures,
    )
    require(
        subj.get("truth_correction_by_system_rule_forbidden") is True,
        "subjective_correction_forbidden_missing",
        failures,
    )


def check_dormant_not_deleted(parsed: dict[str, dict], failures: list[str]) -> None:
    dormancy = parsed["personal_cognitive_network_dormancy_reactivation_candidate.json"]
    states = set(dormancy.get("states", []))
    require(
        states == {"ACTIVE", "WEAK", "DORMANT", "REACTIVATED"},
        "dormancy_states_mismatch",
        failures,
    )
    tp = dormancy.get("transition_principles", {})
    require(
        tp.get("dormant_is_not_deleted") is True,
        "dormant_not_deleted_missing",
        failures,
    )
    require(
        "inactivity_auto_delete" in set(dormancy.get("forbidden", [])),
        "inactivity_auto_delete_not_forbidden",
        failures,
    )


def check_resource_bounded_activation(
    parsed: dict[str, dict], failures: list[str]
) -> None:
    activation = parsed["personal_cognitive_network_activation_model_candidate.json"]
    propagation = activation.get("propagation_control", {})
    require(
        propagation.get("fixed_propagation_depth_forbidden") is True,
        "fixed_propagation_depth_not_forbidden",
        failures,
    )

    resource = parsed["pcn_resource_constraint_model_candidate.json"]
    fixed = resource.get("fixed_constant_controls_forbidden", {})
    require(
        fixed.get("fixed_max_nodes") is True, "fixed_max_nodes_not_forbidden", failures
    )
    require(
        fixed.get("fixed_max_links") is True, "fixed_max_links_not_forbidden", failures
    )
    require(
        fixed.get("fixed_retention_duration") is True,
        "fixed_retention_duration_not_forbidden",
        failures,
    )


def check_nested_constraints(parsed: dict[str, dict], failures: list[str]) -> None:
    nested = parsed["pcn_nested_constraint_model_candidate.json"]
    expected_relations = {
        "Context <-> PCN",
        "Resource <-> PCN",
        "Memory <-> PCN",
        "Field <-> PCN",
        "Role <-> PCN",
        "Relationship <-> PCN",
        "Emotion <-> PCN",
        "Intent <-> PCN (Future)",
        "Causal <-> PCN (Future)",
        "Experience <-> PCN (Future)",
    }
    seen = {item.get("relation") for item in nested.get("relationships", [])}
    require(seen == expected_relations, "nested_relations_incomplete", failures)
    for item in nested.get("relationships", []):
        for key in [
            "incoming_constraint",
            "outgoing_constraint",
            "source_owner",
            "mutation_authority",
            "feedback_type",
        ]:
            require(
                bool(item.get(key)),
                f"nested_field_missing:{item.get('relation')}:{key}",
                failures,
            )


def check_context_memory_causal_boundaries(
    parsed: dict[str, dict], failures: list[str]
) -> None:
    context_contract = parsed["context_pcn_activation_contract_candidate.json"]
    require(
        context_contract.get("output") == "PCN Activation Candidate",
        "context_output_mismatch",
        failures,
    )
    forbidden_context = set(context_contract.get("forbidden_output", []))
    require(
        {"Intent", "Causal Result", "Decision", "Action"}.issubset(forbidden_context),
        "context_forbidden_output_incomplete",
        failures,
    )

    memory_contract = parsed["pcn_memory_boundary_contract_candidate.json"]
    require(
        "Memory System" == memory_contract.get("memory_owner"),
        "memory_owner_mismatch",
        failures,
    )
    require(
        "Personal Cognitive Network Governance" == memory_contract.get("pcn_owner"),
        "pcn_owner_mismatch_in_memory_contract",
        failures,
    )

    causal_contract = parsed["pcn_causal_boundary_contract_candidate.json"]
    require(
        "Causal Reasoning Governance" == causal_contract.get("causal_owner"),
        "causal_owner_mismatch",
        failures,
    )


def check_no_second_writer(parsed: dict[str, dict], failures: list[str]) -> None:
    for name in [
        "pcn_causal_boundary_contract_candidate.json",
        "pcn_memory_boundary_contract_candidate.json",
        "context_pcn_activation_contract_candidate.json",
        "pcn_nested_constraint_model_candidate.json",
    ]:
        payload = parsed[name]
        if "second_writer_prohibited" in payload:
            require(
                payload.get("second_writer_prohibited") is True,
                f"second_writer_flag_missing:{name}",
                failures,
            )


def check_no_runtime_implementation(
    parsed: dict[str, dict], failures: list[str]
) -> None:
    manifest = parsed["pcn_planning_change_manifest.json"]
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
        manifest.get("active_schema_changed") is False,
        "active_schema_changed_true",
        failures,
    )
    require(
        manifest.get("active_contract_changed") is False,
        "active_contract_changed_true",
        failures,
    )
    require(
        manifest.get("owner_metadata_changed") is False,
        "owner_metadata_changed_true",
        failures,
    )
    require(
        manifest.get("pcn_runtime_created") is False,
        "pcn_runtime_created_true",
        failures,
    )
    require(
        manifest.get("causal_runtime_created") is False,
        "causal_runtime_created_true",
        failures,
    )
    require(
        manifest.get("migration_executed") is False, "migration_executed_true", failures
    )

    phase = parsed["phase_contract.json"]
    require(
        phase.get("Execution Mode") == "Planning Only",
        "execution_mode_not_planning_only",
        failures,
    )
    require(
        phase.get("implementation_started") is False,
        "implementation_started_true",
        failures,
    )
    require(phase.get("runtime_started") is False, "runtime_started_true", failures)
    require(phase.get("skeleton_started") is False, "skeleton_started_true", failures)
    require(
        phase.get("next_phase_not_authorized") is True,
        "next_phase_not_authorized_false",
        failures,
    )


def check_scenario_count(parsed: dict[str, dict], failures: list[str]) -> None:
    simulation = parsed["pcn_minimum_scenario_simulation_candidate.json"]
    cases = simulation.get("cases", [])
    require(len(cases) >= 6, "scenario_case_count_below_six", failures)


def check_python_ast_and_import_boundary(failures: list[str]) -> None:
    verifier_path = ROOT / "verify_personal_cognitive_network_planning_v1.py"
    source = verifier_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        failures.append(f"ast_parse_failed:{exc.msg}")
        return

    stdlib_allowed = {"__future__", "ast", "json", "py_compile", "sys", "pathlib"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_name = alias.name.split(".")[0]
                if root_name not in stdlib_allowed:
                    failures.append(f"non_stdlib_import:{alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            root_name = node.module.split(".")[0]
            if root_name not in stdlib_allowed:
                failures.append(f"non_stdlib_import_from:{node.module}")


def check_py_compile(failures: list[str]) -> None:
    verifier_path = ROOT / "verify_personal_cognitive_network_planning_v1.py"
    try:
        py_compile.compile(str(verifier_path), doraise=True)
    except py_compile.PyCompileError as exc:
        failures.append(f"py_compile_failed:{exc.msg}")


def emit_result(checks: list[str], failures: list[str]) -> int:
    print("CHECKS")
    for check in checks:
        print(check)

    print("FAILED_CHECKS")
    for failure in failures:
        print(failure)

    print("PASSED_CHECK_COUNT")
    passed_count = len(checks) - len(failures) if len(failures) <= len(checks) else 0
    print(passed_count)

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


def main() -> int:
    failures: list[str] = []
    checks = [
        "required_files",
        "json_parse",
        "markdown_nonempty",
        "python_ast",
        "py_compile",
        "stdlib_import_boundary",
        "reference_validation",
        "owner_uniqueness",
        "no_source_object_ownership_persistence_mutation",
        "pcn_not_memory_causal_knowledge_graph",
        "candidate_fact_boundary",
        "subjective_cognition_preserved",
        "dormant_not_deleted",
        "resource_bounded_activation",
        "no_fixed_graph_size",
        "no_fixed_propagation_depth",
        "no_fixed_retention_duration",
        "nested_constraint_relationships",
        "context_handoff",
        "memory_boundary",
        "causal_boundary",
        "no_second_writer",
        "no_runtime",
        "no_implementation",
        "no_existing_file_modification",
        "scenario_count",
        "cross_asset_consistency",
        "change_manifest_boundary",
    ]

    check_required_files(failures)
    if failures:
        return emit_result(checks, failures)

    parsed = check_json_parse(failures)
    check_markdown_nonempty(failures)
    check_python_ast_and_import_boundary(failures)
    check_py_compile(failures)
    check_reference_validation(failures)

    if not failures:
        check_owner_uniqueness(parsed, failures)
        check_no_source_object_ownership(parsed, failures)
        check_not_memory_causal_kg(parsed, failures)
        check_candidate_fact_boundary(parsed, failures)
        check_subjective_boundary(parsed, failures)
        check_dormant_not_deleted(parsed, failures)
        check_resource_bounded_activation(parsed, failures)
        check_nested_constraints(parsed, failures)
        check_context_memory_causal_boundaries(parsed, failures)
        check_no_second_writer(parsed, failures)
        check_no_runtime_implementation(parsed, failures)
        check_scenario_count(parsed, failures)

    return emit_result(checks, failures)


if __name__ == "__main__":
    sys.exit(main())
