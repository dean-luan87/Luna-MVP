"""User-terminal V2 verifier for Self Governance controlled implementation v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


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

from capabilities.midplatform.core.self_governance.self_governance_engine_v1 import (  # noqa: E402
    SelfGovernanceEngineV1,
)
from capabilities.midplatform.core.self_governance.self_governance_fixture_v1 import (  # noqa: E402
    get_self_governance_fixture_v1,
)
from capabilities.midplatform.core.self_governance.self_governance_registry_v1 import (  # noqa: E402
    ATTRIBUTION_STATES,
    BOUNDARY_CLASSES,
    CANONICAL_OWNER,
    IDEMPOTENCY_GUARDS,
    NEGATIVE_GUARDS,
    SENSITIVITY_LEVELS,
)
from capabilities.midplatform.core.self_governance.self_governance_static_validators_v1 import (  # noqa: E402
    validate_output,
)


CODE_FILES = {
    "__init__.py",
    "self_governance_registry_v1.py",
    "self_governance_error_types_v1.py",
    "self_governance_core_types_v1.py",
    "self_reference_types_v1.py",
    "self_attribution_types_v1.py",
    "self_continuity_types_v1.py",
    "self_boundary_types_v1.py",
    "self_stability_types_v1.py",
    "self_revision_types_v1.py",
    "self_influence_types_v1.py",
    "self_trace_types_v1.py",
    "self_io_types_v1.py",
    "self_governance_protocol_v1.py",
    "self_governance_ownership_guard_v1.py",
    "self_governance_static_validators_v1.py",
    "self_governance_fixture_v1.py",
    "self_governance_engine_v1.py",
    "run_self_governance_controlled_implementation_v1.py",
}
DOC_FILES = {
    "self_governance_controlled_implementation_overview_v1.md",
    "self_governance_controlled_execution_contract_v1.json",
    "self_governance_negative_guards_v1.json",
    "self_governance_planning_to_code_mapping_v1.json",
    "self_governance_controlled_change_manifest_v1.json",
    "self_governance_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_self_governance_controlled_implementation_v1.py",
}
PLANNING_DIR = REPO_ROOT / "docs/architecture/luna_self_governance_architecture_planning_v1"
CODE_DIR = REPO_ROOT / "capabilities/midplatform/core/self_governance"
EVAL_DIR = REPO_ROOT / "_eval_out/self_governance_controlled_implementation_v1"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(checks: List[Dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def _all_fixture_expectations() -> Tuple[bool, List[str], List[Any]]:
    failures: List[str] = []
    outputs = []
    engine = SelfGovernanceEngineV1()
    for case in get_self_governance_fixture_v1():
        output = engine.run_case(case.request)
        outputs.append(output)
        checks = {
            "boundary": output.boundary_class == case.expected_boundary_class,
            "state": output.self_attribution is not None and output.self_attribution.state == case.expected_state,
            "domain": output.self_attribution is not None and output.self_attribution.attribution_domain == case.expected_domain,
            "continuity": (output.self_continuity is not None) == case.expected_continuity,
            "revision": (output.revision is not None) == case.expected_revision,
            "revocation": (output.revocation is not None) == case.expected_revocation,
            "supersession": (output.supersession is not None) == case.expected_supersession,
            "expiration": (output.expiration is not None) == case.expected_expiration,
            "influence": tuple(item.evidence_kind for item in output.influences) == case.expected_influence_kinds,
            "sensitivity": output.self_reference.sensitivity == case.expected_sensitivity,
            "duplicate_guard": output.duplicate_guard_triggered == case.expected_duplicate_guard,
            "correction_precedence": output.user_correction_precedence == case.expected_user_correction_precedence,
            "behavior_validation": not validate_output(output),
        }
        failures.extend(f"{case.scenario_id}:{name}" for name, passed in checks.items() if not passed)
    return not failures, failures, outputs


def run_verification() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    code_actual = {path.name for path in CODE_DIR.iterdir() if path.is_file()}
    doc_actual = {path.name for path in PHASE_DIR.iterdir() if path.is_file()}
    _check(checks, "exact_code_file_set", code_actual == CODE_FILES, f"missing={sorted(CODE_FILES-code_actual)} extra={sorted(code_actual-CODE_FILES)}")
    _check(checks, "exact_doc_file_set", doc_actual == DOC_FILES, f"missing={sorted(DOC_FILES-doc_actual)} extra={sorted(doc_actual-DOC_FILES)}")

    json_paths = [path for path in PHASE_DIR.iterdir() if path.suffix == ".json"]
    json_failures = []
    docs: Dict[str, Any] = {}
    for path in json_paths:
        try:
            docs[path.name] = _load_json(path)
        except Exception as exc:
            json_failures.append(f"{path.name}:{exc}")
    _check(checks, "json_parse", not json_failures, str(json_failures) if json_failures else "all implementation JSON parsed")

    ast_failures = []
    for path in [*(CODE_DIR / name for name in CODE_FILES if name.endswith(".py")), PHASE_DIR / "verify_self_governance_controlled_implementation_v1.py"]:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            ast_failures.append(f"{path.name}:{exc}")
    _check(checks, "ast_parse", not ast_failures, str(ast_failures) if ast_failures else "all Python source AST parsed")

    contract = docs.get("self_governance_controlled_execution_contract_v1.json", {})
    _check(checks, "canonical_owner", CANONICAL_OWNER == "Self Governance" and contract.get("canonical_owner") == CANONICAL_OWNER, "single canonical owner")
    sibling_names = {path.name for path in CODE_DIR.parent.iterdir() if path.is_dir()}
    forbidden_parallel_names = {"identity_governance", "self_attribution_governance", "self_continuity_governance", "personality_governance", "emotion_governance"}
    _check(checks, "no_parallel_owner", not sibling_names.intersection(forbidden_parallel_names), "no parallel owner directory")
    mapping = docs.get("self_governance_planning_to_code_mapping_v1.json", {}).get("planning_assets", {})
    planning_files = {path.name for path in PLANNING_DIR.iterdir() if path.is_file()}
    _check(checks, "planning_to_code_completeness", planning_files <= set(mapping), f"unmapped={sorted(planning_files-set(mapping))}")
    manifest = docs.get("self_governance_controlled_change_manifest_v1.json", {})
    _check(checks, "no_existing_owner_module_modification", manifest.get("existing_files_modified") == [] and manifest.get("planning_assets_modified") == [], "manifest records no existing or planning mutations")

    planning_scenarios = _load_json(PLANNING_DIR / "self_minimum_scenario_suite_v1.json")
    fixture_cases = get_self_governance_fixture_v1()
    planned_ids = {item["scenario_id"] for item in planning_scenarios["scenarios"]}
    fixture_ids = {item.scenario_id for item in fixture_cases}
    _check(checks, "fixture_scenario_count", len(fixture_cases) == planning_scenarios["scenario_count"] == 34, f"fixture={len(fixture_cases)} planned={planning_scenarios['scenario_count']}")
    _check(checks, "fixture_id_coverage", fixture_ids == planned_ids, f"missing={sorted(planned_ids-fixture_ids)} extra={sorted(fixture_ids-planned_ids)}")
    all_behaviors, behavior_failures, outputs = _all_fixture_expectations()
    _check(checks, "all_fixture_expectations_pass", all_behaviors, str(behavior_failures[:10]) if behavior_failures else "all fixture expected/actual checks passed")
    _check(checks, "all_fixture_behaviors_pass", all_behaviors, "deterministic candidate behaviors validated")

    _check(checks, "self_not_identity_truth", all(item.self_reference.fact_admitted is False and item.self_reference.identity_ref is not None or item.self_reference.subject_boundary_class in {"UNKNOWN", "CONTESTED", "OTHER"} for item in outputs), "identity ref remains a candidate boundary")
    _check(checks, "self_not_personality", NEGATIVE_GUARDS["self_can_mutate_personality"] is False and all(item.self_attribution.stability_partition != "FUTURE_PERSONALITY_DERIVED_SELF" or item.self_attribution.state != "ADMITTED_CANDIDATE" for item in outputs), "future personality partition remains deferred")
    _check(checks, "self_not_emotion", NEGATIVE_GUARDS["self_can_mutate_emotion"] is False, "emotion is evidence interface only")
    _check(checks, "self_not_memory", NEGATIVE_GUARDS["self_can_mutate_memory"] is False and NEGATIVE_GUARDS["semantic_compression_execution"] is False, "memory is consumed as evidence only")
    _check(checks, "self_not_pcn", NEGATIVE_GUARDS["self_can_mutate_pcn"] is False, "PCN ownership preserved")
    _check(checks, "self_not_intent", NEGATIVE_GUARDS["self_can_mutate_intent"] is False, "Intent ownership preserved")
    _check(checks, "self_not_regulation_parameters", NEGATIVE_GUARDS["self_can_mutate_regulation_parameter"] is False and NEGATIVE_GUARDS["self_can_activate_parameter_genome"] is False, "regulation parameter ownership preserved")
    _check(checks, "attribution_lifecycle_paths", set(ATTRIBUTION_STATES) >= {item.self_attribution.state for item in outputs}, "all emitted lifecycle states are registered")
    _check(checks, "revision_revocation_supersession", any(item.revision for item in outputs) and any(item.revocation for item in outputs) and any(item.supersession for item in outputs), "lineage candidates are emitted")
    _check(checks, "continuity_change_tolerance", outputs[29].self_continuity is not None and outputs[29].self_continuity.changed_refs and outputs[29].self_continuity.immutable_identity_claim is False, "continuity preserves change")
    _check(checks, "boundary_classification", set(BOUNDARY_CLASSES) >= {item.boundary_class for item in outputs} and len(BOUNDARY_CLASSES) == 7, "seven boundary classes are preserved")
    planned_privacy = _load_json(PLANNING_DIR / "self_privacy_sensitivity_boundary_v1.json")
    _check(checks, "privacy_sensitivity_guards", set(SENSITIVITY_LEVELS) == set(planned_privacy.get("sensitivity_levels", ())) and outputs[31].self_reference.sensitivity == "HIGH_SENSITIVITY" and outputs[32].self_reference.sensitivity == "DO_NOT_TRANSFER", "sensitivity registry and restricted cases present")
    _check(checks, "trace_continuity", all(item.trace.root_cycle_trace_id and item.trace.self_trace_id for item in outputs), "trace chain has root and self trace")
    _check(checks, "provenance_reverse_locatability", all(item.trace.reverse_locatable and item.provenance.reverse_locatable and not item.trace.provenance_grants_authority for item in outputs), "trace/provenance reverse route is preserved")
    _check(checks, "idempotency_guards", set(outputs[28].idempotency_guards) == set(IDEMPOTENCY_GUARDS) and outputs[28].duplicate_guard_triggered and outputs[28].replay_guard_triggered, "duplicate, replay, revision, revocation, supersession, continuity, and correction guards are explicit")
    _check(checks, "user_correction_precedence", outputs[5].user_correction_precedence and outputs[5].revision is not None and outputs[5].revision.explicit_user_correction, "user correction produces explicit revision precedence")
    _check(checks, "no_semantic_compression", NEGATIVE_GUARDS["semantic_compression_execution"] is False, "semantic compression remains deferred")
    _check(checks, "no_personality_mutation", all(item.personality_mutation is False for item in outputs), "personality mutation frozen")
    _check(checks, "no_emotion_mutation", all(item.emotion_mutation is False for item in outputs), "emotion mutation frozen")
    _check(checks, "no_runtime_side_effects", all(not any(getattr(item, key) for key in ("runtime_execution", "database_write", "vector_store_write", "embedding_execution", "model_call", "scheduler_execution", "task_mutation", "source_owner_mutation", "cross_user_transfer")) for item in outputs), "runtime and side effects are false")

    artifact_paths = [EVAL_DIR / name for name in ("self_governance_result_v1.json", "self_governance_case_results_v1.json", "self_governance_trace_v1.json")]
    artifacts_exist = all(path.is_file() for path in artifact_paths)
    _check(checks, "runner_artifact_existence", artifacts_exist, "runner artifacts must be created by the user-terminal runner")
    artifact_coverage = False
    if artifacts_exist:
        try:
            summary = _load_json(artifact_paths[0])
            cases = _load_json(artifact_paths[1])
            traces = _load_json(artifact_paths[2])
            artifact_coverage = summary.get("scenario_count") == 34 and {item.get("scenario_id") for item in cases} == planned_ids and {item.get("scenario_id") for item in traces} == planned_ids and summary.get("canonical_owner") == CANONICAL_OWNER
        except Exception:
            artifact_coverage = False
    _check(checks, "runner_artifact_scenario_coverage", artifact_coverage, "runner outputs cover all frozen scenario IDs")

    failed = [item for item in checks if not item["passed"]]
    result = {
        "CHECKS": {item["name"]: ("PASS" if item["passed"] else "FAIL") for item in checks},
        "FAILED_CHECKS": [item["name"] for item in failed],
        "PASSED_CHECK_COUNT": len(checks) - len(failed),
        "FAILED_CHECK_COUNT": len(failed),
        "BLOCKER_COUNT": len(failed),
        "FINAL_DECISION": "SELF_GOVERNANCE_CONTROLLED_IMPLEMENTATION_READY_FOR_AUDIT" if not failed else "SELF_GOVERNANCE_CONTROLLED_IMPLEMENTATION_REMEDIATION_REQUIRED",
        "NEXT": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not failed else "LUNA_SELF_GOVERNANCE_CONTROLLED_IMPLEMENTATION_REMEDIATION",
        "DETAILS": checks,
    }
    return result


def main() -> int:
    result = run_verification()
    print("CHECKS")
    for name, state in result["CHECKS"].items():
        print(f"- [{state}] {name}")
    print("FAILED_CHECKS")
    for name in result["FAILED_CHECKS"] or ["NONE"]:
        print(f"- {name}")
    print("PASSED_CHECK_COUNT")
    print(result["PASSED_CHECK_COUNT"])
    print("FAILED_CHECK_COUNT")
    print(result["FAILED_CHECK_COUNT"])
    print("BLOCKER_COUNT")
    print(result["BLOCKER_COUNT"])
    print("FINAL_DECISION")
    print(result["FINAL_DECISION"])
    print("NEXT")
    print(result["NEXT"])
    return 0 if result["BLOCKER_COUNT"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
