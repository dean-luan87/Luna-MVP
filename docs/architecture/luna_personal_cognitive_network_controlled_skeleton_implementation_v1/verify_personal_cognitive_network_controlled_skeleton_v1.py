#!/usr/bin/env python3
"""Final phase verifier for PCN controlled skeleton implementation v1."""

from __future__ import annotations

import ast
import json
import py_compile
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[2]
CODE_DIR = REPO / "capabilities/midplatform/core/personal_cognitive_network"

REQUIRED_CODE_FILES = {
    "personal_cognitive_network_types_v1.py",
    "personal_cognitive_link_types_v1.py",
    "personal_cognitive_activation_types_v1.py",
    "personal_cognitive_growth_types_v1.py",
    "personal_cognitive_interaction_types_v1.py",
    "personal_cognitive_projection_types_v1.py",
    "personal_cognitive_resource_types_v1.py",
    "personal_cognitive_trace_types_v1.py",
    "personal_cognitive_error_types_v1.py",
    "personal_cognitive_network_protocol_v1.py",
    "personal_cognitive_network_skeleton_v1.py",
    "personal_cognitive_activation_skeleton_v1.py",
    "personal_cognitive_growth_skeleton_v1.py",
    "personal_cognitive_interaction_handoff_skeleton_v1.py",
    "personal_cognitive_static_validators_v1.py",
    "personal_cognitive_network_fixture_v1.py",
    "run_personal_cognitive_network_controlled_skeleton_v1.py",
}

REQUIRED_DOC_FILES = {
    "personal_cognitive_network_controlled_skeleton_implementation_v1.md",
    "pcn_planning_to_code_mapping_v1.json",
    "pcn_controlled_skeleton_contract_v1.json",
    "pcn_skeleton_clarification_inheritance_v1.json",
    "pcn_controlled_skeleton_change_manifest_v1.json",
    "phase_contract.json",
    "verify_personal_cognitive_network_controlled_skeleton_v1.py",
}

REQUIRED_JSON_FILES = REQUIRED_DOC_FILES - {
    "personal_cognitive_network_controlled_skeleton_implementation_v1.md",
    "verify_personal_cognitive_network_controlled_skeleton_v1.py",
}

FORBIDDEN_IMPORT_ROOTS = {
    "networkx",
    "torch",
    "tensorflow",
    "keras",
    "sklearn",
    "numpy",
    "pandas",
    "requests",
    "httpx",
    "sqlite3",
    "psycopg2",
    "pymongo",
    "sqlalchemy",
    "socket",
}

FORBIDDEN_TEXT_TOKENS = {
    "cnn",
    "gnn",
    "neural network",
    "graph db",
    "networkx",
    "database",
    "runtime integration",
    "persist to",
    "write memory",
}


def check(
    condition: bool, check_id: str, checks: List[str], failures: List[str]
) -> None:
    checks.append(check_id)
    if not condition:
        failures.append(check_id)


def load_json(path: Path) -> Dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError(f"{path} must be a json object")
    return raw


def gather_imports(tree: ast.AST) -> Iterable[str]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


def parse_python(path: Path) -> Tuple[ast.AST, str]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    return tree, source


def main() -> int:
    checks: List[str] = []
    failures: List[str] = []

    check(CODE_DIR.is_dir(), "code_dir_exists", checks, failures)
    check(BASE.is_dir(), "doc_dir_exists", checks, failures)

    actual_code = {p.name for p in CODE_DIR.iterdir() if p.is_file()}
    actual_doc = {p.name for p in BASE.iterdir() if p.is_file()}
    check(REQUIRED_CODE_FILES <= actual_code, "required_code_files", checks, failures)
    check(REQUIRED_DOC_FILES <= actual_doc, "required_doc_files", checks, failures)

    docs: Dict[str, Dict[str, Any]] = {}
    for name in sorted(REQUIRED_JSON_FILES):
        path = BASE / name
        try:
            docs[name] = load_json(path)
            check(True, f"json_parse:{name}", checks, failures)
        except Exception:
            docs[name] = {}
            check(False, f"json_parse:{name}", checks, failures)

    impl_md = (
        BASE / "personal_cognitive_network_controlled_skeleton_implementation_v1.md"
    ).read_text(encoding="utf-8")
    check(
        "CONTROLLED_SKELETON_CANDIDATE" in impl_md, "markdown_status", checks, failures
    )
    check(
        "candidate-only" in impl_md.lower(), "markdown_candidate_only", checks, failures
    )

    contract = docs.get("pcn_controlled_skeleton_contract_v1.json", {})
    check(
        contract.get("skeleton_only") is True,
        "contract_skeleton_only",
        checks,
        failures,
    )
    check(
        contract.get("candidate_only") is True,
        "contract_candidate_only",
        checks,
        failures,
    )
    check(
        contract.get("synthetic_fixture_only") is True,
        "contract_synthetic_only",
        checks,
        failures,
    )
    for key in [
        "real_network_mutation_allowed",
        "source_mutation_allowed",
        "persistence_allowed",
        "runtime_integration_allowed",
        "model_call_allowed",
        "causal_reasoning_allowed",
        "intent_generation_allowed",
        "decision_allowed",
        "action_allowed",
    ]:
        check(contract.get(key) is False, f"contract_false:{key}", checks, failures)

    clarifications = docs.get("pcn_skeleton_clarification_inheritance_v1.json", {})
    clar_items = clarifications.get("clarifications", [])
    check(len(clar_items) == 5, "clarification_count_five", checks, failures)
    check(
        all(item.get("resolved") is False for item in clar_items),
        "clarification_none_resolved",
        checks,
        failures,
    )
    check(
        all(item.get("owner_changed") is False for item in clar_items),
        "clarification_owner_unchanged",
        checks,
        failures,
    )
    check(
        all(item.get("core_boundary_changed") is False for item in clar_items),
        "clarification_boundary_unchanged",
        checks,
        failures,
    )

    manifest = docs.get("pcn_controlled_skeleton_change_manifest_v1.json", {})
    check(
        manifest.get("modified_existing_files") == [],
        "side_effect_modified_existing_empty",
        checks,
        failures,
    )
    check(
        manifest.get("runtime_files_changed") == [],
        "side_effect_runtime_files_empty",
        checks,
        failures,
    )
    check(
        manifest.get("active_schema_changed") is False,
        "side_effect_schema_unchanged",
        checks,
        failures,
    )
    check(
        manifest.get("active_contract_changed") is False,
        "side_effect_contract_unchanged",
        checks,
        failures,
    )
    check(
        manifest.get("owner_metadata_changed") is False,
        "side_effect_owner_metadata_unchanged",
        checks,
        failures,
    )
    check(
        manifest.get("real_pcn_runtime_created") is False,
        "side_effect_no_real_runtime",
        checks,
        failures,
    )

    phase = docs.get("phase_contract.json", {})
    check(
        phase.get("execution_mode") == "Controlled Skeleton Implementation",
        "phase_execution_mode",
        checks,
        failures,
    )
    check(
        phase.get("runtime_execution") is False,
        "phase_runtime_execution_false",
        checks,
        failures,
    )
    check(
        phase.get("final_verifier_execution_by_agent") is False,
        "phase_final_verifier_agent_false",
        checks,
        failures,
    )
    check(
        phase.get("next_phase_not_authorized") is True,
        "phase_next_phase_not_authorized",
        checks,
        failures,
    )

    code_sources: Dict[str, str] = {}
    for name in sorted(REQUIRED_CODE_FILES):
        path = CODE_DIR / name
        try:
            tree, source = parse_python(path)
            py_compile.compile(str(path), doraise=True)
            code_sources[name] = source
            check(True, f"ast_parse:{name}", checks, failures)
            check(True, f"py_compile:{name}", checks, failures)
        except Exception:
            code_sources[name] = ""
            check(False, f"ast_parse:{name}", checks, failures)
            check(False, f"py_compile:{name}", checks, failures)
            continue

        imports = {mod.split(".")[0] for mod in gather_imports(tree)}
        check(
            not (imports & FORBIDDEN_IMPORT_ROOTS),
            f"import_boundary:{name}",
            checks,
            failures,
        )

    full_text = "\n".join(code_sources.values()).lower()
    for token in FORBIDDEN_TEXT_TOKENS:
        check(
            token not in full_text, f"forbidden_token_absent:{token}", checks, failures
        )

    fixture_source = code_sources.get("personal_cognitive_network_fixture_v1.py", "")
    check(
        "synthetic_only" in fixture_source,
        "fixture_synthetic_only_flag",
        checks,
        failures,
    )
    check("SCN_01_WEATHER_QUERY" in fixture_source, "fixture_case_1", checks, failures)
    check(
        "SCN_12_HIGH_LOW_RESOURCE_DEGRADATION" in fixture_source,
        "fixture_case_12",
        checks,
        failures,
    )
    check(
        "resource_label" in fixture_source,
        "fixture_resource_label_present",
        checks,
        failures,
    )

    interaction_source = code_sources.get(
        "personal_cognitive_interaction_types_v1.py", ""
    )
    for interaction_type in [
        "RESONANCE",
        "COMPETITION",
        "TEMPORARY_OCCUPATION",
        "OVERLAP",
        "COEXISTENCE",
        "FUSION_CANDIDATE",
        "HISTORICAL_REACTIVATION",
    ]:
        check(
            interaction_type in interaction_source,
            f"interaction_type:{interaction_type}",
            checks,
            failures,
        )

    link_source = code_sources.get("personal_cognitive_link_types_v1.py", "")
    check(
        "TRUTH_UNVERIFIED_OR_SUBJECTIVE" in link_source,
        "link_truth_status_subjective",
        checks,
        failures,
    )
    check(
        "strength_not_equal_truth" in link_source,
        "link_strength_not_truth_rule",
        checks,
        failures,
    )

    validators_source = code_sources.get(
        "personal_cognitive_static_validators_v1.py", ""
    )
    for fn in [
        "validate_source_owner_exists",
        "validate_no_source_payload_copied",
        "validate_no_source_mutation_authority",
        "validate_strength_not_truth",
        "validate_dormant_not_deleted",
        "validate_resonance_not_causal",
        "validate_competition_not_arbitration",
        "validate_kernel_not_owned_by_pcn",
        "validate_unknown_preserved",
        "validate_resource_reference_exists",
        "validate_no_fixed_propagation_depth",
        "validate_no_fixed_graph_size",
        "validate_no_fixed_retention_duration",
        "validate_projection_candidate_only",
        "validate_no_decision_output",
        "validate_no_causal_output",
        "validate_no_intent_output",
        "validate_no_runtime_execution",
    ]:
        check(fn in validators_source, f"validator_exists:{fn}", checks, failures)

    skeleton_source = code_sources.get("personal_cognitive_network_skeleton_v1.py", "")
    for token, check_id in [
        ("skeleton_only=True", "skeleton_flag_true"),
        ("candidate_only=True", "candidate_flag_true"),
        ("runtime_executed=False", "runtime_flag_false"),
        ("source_mutation_executed=False", "source_mutation_flag_false"),
        ("persistence_executed=False", "persistence_flag_false"),
        ("causal_reasoning_executed=False", "causal_flag_false"),
        ("intent_generation_executed=False", "intent_flag_false"),
        ("decision_executed=False", "decision_flag_false"),
    ]:
        check(token in skeleton_source, check_id, checks, failures)

    check(
        "TEMPORARY_OCCUPATION" in fixture_source,
        "field_temp_occupation_present",
        checks,
        failures,
    )
    check(
        "structural mutation" not in skeleton_source.lower(),
        "field_no_structural_mutation",
        checks,
        failures,
    )
    check("RESONANCE" in fixture_source, "resonance_present", checks, failures)
    check(
        "CAUSAL_FACT" not in fixture_source,
        "resonance_not_causal_fact",
        checks,
        failures,
    )
    check("COMPETITION" in fixture_source, "competition_present", checks, failures)
    check(
        "WINNER" not in fixture_source, "competition_not_arbitration", checks, failures
    )
    check(
        "rel-former-spouse-historical" in fixture_source,
        "multi_relation_coexistence",
        checks,
        failures,
    )
    check(
        "HISTORICAL" in fixture_source or "DORMANT" in fixture_source,
        "historical_reactivatable",
        checks,
        failures,
    )

    print("CHECKS")
    for item in checks:
        print(item)

    print("FAILED_CHECKS")
    for item in failures:
        print(item)

    print("PASSED_CHECK_COUNT")
    print(max(0, len(checks) - len(failures)))

    print("FAILED_CHECK_COUNT")
    print(len(failures))

    print("BLOCKER_COUNT")
    print(len(failures))

    print("FINAL_DECISION")
    print(
        "V2_FINAL_VERIFICATION_PASSED"
        if not failures
        else "BLOCKED_BY_VERIFIER_FAILURE"
    )

    print("NEXT")
    print(
        "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"
        if not failures
        else "REMEDIATE_REPORTED_FAILURES_ONLY"
    )

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
