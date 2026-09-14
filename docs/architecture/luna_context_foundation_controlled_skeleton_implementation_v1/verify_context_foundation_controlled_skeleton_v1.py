#!/usr/bin/env python3
"""Final phase verifier for Context Foundation controlled skeleton v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


BASE = Path(__file__).resolve().parent
STATUS = "CONTROLLED_SKELETON_CANDIDATE"
READY = "LUNA_CONTEXT_FOUNDATION_CONTROLLED_SKELETON_IMPLEMENTATION_READY"
REMEDIATION = (
    "LUNA_CONTEXT_FOUNDATION_CONTROLLED_SKELETON_IMPLEMENTATION_REMEDIATION_REQUIRED"
)

CODE_FILES = {
    "context_foundation_types_v1.py",
    "context_projection_types_v1.py",
    "context_carryover_types_v1.py",
    "context_foundation_protocol_v1.py",
    "context_foundation_skeleton_v1.py",
    "context_foundation_trace_types_v1.py",
    "context_foundation_static_validators_v1.py",
    "context_foundation_fixture_v1.py",
    "run_context_foundation_controlled_skeleton_v1.py",
}

DOC_FILES = {
    "context_foundation_controlled_skeleton_implementation_v1.md",
    "context_foundation_planning_to_code_mapping_v1.json",
    "context_foundation_skeleton_contract_v1.json",
    "context_foundation_controlled_skeleton_change_manifest_v1.json",
    "phase_contract.json",
    "verify_context_foundation_controlled_skeleton_v1.py",
}

JSON_FILES = DOC_FILES - {
    "context_foundation_controlled_skeleton_implementation_v1.md",
    "verify_context_foundation_controlled_skeleton_v1.py",
}


def find_repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current,) + tuple(current.parents):
        code_dir = candidate / "capabilities/midplatform/core/context_foundation"
        if code_dir.is_dir():
            return candidate
    raise RuntimeError("repository_root_with_context_foundation_not_found")


def load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return value


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

    def check(condition: bool, check_id: str) -> None:
        checks.append(check_id)
        if not condition:
            failures.append(check_id)

    try:
        repo_root = find_repo_root()
        check(True, "repo_root_resolved")
    except RuntimeError:
        repo_root = Path.cwd().resolve()
        check(False, "repo_root_resolved")

    code_dir = repo_root / "capabilities/midplatform/core/context_foundation"
    actual_code_files = {path.name for path in code_dir.iterdir() if path.is_file()}
    actual_doc_files = {path.name for path in BASE.iterdir() if path.is_file()}
    check(actual_code_files == CODE_FILES, "exact_code_file_set")
    check(actual_doc_files == DOC_FILES, "exact_doc_file_set")

    documents: Dict[str, Dict[str, Any]] = {}
    for name in sorted(JSON_FILES):
        try:
            documents[name] = load_json(BASE / name)
            check(True, f"json_parse:{name}")
        except (OSError, TypeError, json.JSONDecodeError):
            documents[name] = {}
            check(False, f"json_parse:{name}")

    for name, document in documents.items():
        check(document.get("status") == STATUS, f"candidate_status:{name}")

    implementation_doc = (
        BASE / "context_foundation_controlled_skeleton_implementation_v1.md"
    ).read_text(encoding="utf-8")
    for token, check_id in [
        (STATUS, "doc_status"),
        ("Context Envelope Candidate", "doc_envelope"),
        ("reference-only", "doc_reference_only"),
        ("Context -> Intent", "doc_no_intent"),
        ("Context -> Causal Explanation", "doc_no_causal"),
        ("runtime_executed = false", "doc_no_runtime"),
        ("state_mutation = false", "doc_no_mutation"),
        ("not Memory, not Emotion State, and not Causal Explanation", "doc_carryover_boundary"),
        ("does not authorize Agent execution", "doc_no_agent_runner"),
    ]:
        check(token in implementation_doc, check_id)

    mapping = documents.get("context_foundation_planning_to_code_mapping_v1.json", {})
    mapped_code = {
        Path(path).name for path in mapping.get("all_code_assets", [])
    }
    check(mapped_code == CODE_FILES, "mapping_all_code_files")
    check(len(mapping.get("mappings", [])) >= 8, "mapping_coverage")
    check(
        all(item.get("planning_asset_modified") is False for item in mapping.get("mappings", [])),
        "mapping_planning_unchanged",
    )
    check(mapping.get("existing_planning_assets_modified") is False, "mapping_no_existing_change")
    check(mapping.get("parallel_implementation_created") is False, "mapping_no_parallel")

    contract = documents.get("context_foundation_skeleton_contract_v1.json", {})
    for key in [
        "skeleton_only",
        "candidate_only",
        "reference_only",
        "synthetic_fixture_only",
        "deterministic_trace_required",
        "unknown_preservation_required",
        "provenance_required",
        "source_owner_precedence",
    ]:
        check(contract.get(key) is True, f"contract_true:{key}")
    for key in [
        "real_context_generation",
        "runtime_execution",
        "state_mutation",
        "source_object_storage",
        "source_owner_transfer",
        "database_access",
        "network_access",
        "model_call",
        "provider_call",
        "device_access",
        "production_data_access",
    ]:
        check(contract.get(key) is False, f"contract_false:{key}")
    required_forbidden_outputs = {
        "Fact",
        "Intent",
        "Goal",
        "Causal Explanation",
        "Decision",
        "Action",
        "Runtime Command",
        "Memory Mutation",
        "Field Mutation",
        "Emotion Calculation",
        "Emotion Mutation",
    }
    check(
        required_forbidden_outputs <= set(contract.get("forbidden_outputs", [])),
        "contract_forbidden_outputs",
    )

    manifest = documents.get(
        "context_foundation_controlled_skeleton_change_manifest_v1.json", {}
    )
    check(
        {Path(path).name for path in manifest.get("created_code_files", [])}
        == CODE_FILES,
        "manifest_code_files",
    )
    check(
        {Path(path).name for path in manifest.get("created_documentation_files", [])}
        == DOC_FILES,
        "manifest_doc_files",
    )
    for key in [
        "modified_existing_files",
        "deleted_files",
        "moved_files",
        "renamed_files",
        "runtime_files_changed",
        "planning_files_changed",
        "alignment_files_changed",
        "active_schema_files_changed",
        "active_contract_files_changed",
        "owner_metadata_files_changed",
    ]:
        check(manifest.get(key) == [], f"manifest_empty:{key}")
    for key in [
        "runtime_executed",
        "controlled_runner_executed_by_agent",
        "state_mutation_executed",
        "database_accessed",
        "model_called",
    ]:
        check(manifest.get(key) is False, f"manifest_false:{key}")

    phase = documents.get("phase_contract.json", {})
    required_phase_fields = {
        "phase",
        "stage",
        "execution_mode",
        "current_work_description",
        "previous_phase",
        "previous_phase_decision",
        "input_assets",
        "required_pre_read",
        "target_directory",
        "scope",
        "out_of_scope",
        "required_final_files",
        "implementation_principles",
        "required_checks",
        "negative_guards",
        "verification_authority",
        "allowed_agent_checks",
        "allowed_agent_execution",
        "prohibited_agent_execution",
        "agent_stop_point",
        "user_terminal_commands",
        "expected_success_decision",
        "expected_next",
        "expected_failure_decision",
        "expected_failure_next",
        "stop_condition",
        "blocker_conditions",
        "completion_report_format",
        "current_status_contract",
    }
    check(required_phase_fields <= set(phase), "phase_required_fields")
    check(phase.get("execution_mode") == "Controlled Skeleton Implementation", "phase_mode")
    check(
        phase.get("previous_phase_decision")
        == "LUNA_CONTEXT_FOUNDATION_PLANNING_ALIGNMENT_UPDATE_READY",
        "phase_previous_decision",
    )
    check(phase.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_stop")
    check(phase.get("expected_success_decision") == READY, "phase_ready_token")
    check(phase.get("runtime_executed") is False, "phase_no_runtime")
    check(phase.get("controlled_runner_executed_by_agent") is False, "phase_no_agent_runner")
    check(phase.get("state_mutation_executed") is False, "phase_no_state_mutation")
    check(phase.get("next_phase_auto_entry") is False, "phase_no_auto_next")
    authority = phase.get("verification_authority", {})
    check(authority.get("V0") == "Agent", "authority_v0")
    check(
        authority.get("V1") == "NOT_AUTHORIZED_FOR_AGENT_BY_PHASE_INSTRUCTION",
        "authority_v1",
    )
    check(authority.get("V2") == "USER_TERMINAL_ONLY", "authority_v2")
    check(authority.get("V3") == "CHATGPT_ONLY", "authority_v3")
    check(
        len(phase.get("required_final_files", []))
        == len(CODE_FILES) + len(DOC_FILES),
        "phase_file_count",
    )
    check(
        all((repo_root / path).exists() for path in phase.get("required_final_files", [])),
        "phase_references_exist",
    )

    code_trees: Dict[str, ast.AST] = {}
    for name in sorted(CODE_FILES):
        path = code_dir / name
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            compile(source, str(path), "exec")
            code_trees[name] = tree
            check(True, f"python_compile:{name}")
        except (OSError, SyntaxError, ValueError):
            code_trees[name] = ast.Module(body=[], type_ignores=[])
            check(False, f"python_compile:{name}")

    allowed_stdlib = {
        "__future__",
        "dataclasses",
        "enum",
        "hashlib",
        "json",
        "pathlib",
        "sys",
        "typing",
    }
    forbidden_import_markers = {
        "runtime",
        "memory",
        "emotion",
        "intent",
        "causal",
        "model_manager",
        "requests",
        "sqlite3",
        "socket",
        "subprocess",
    }
    forbidden_calls = {
        "open",
        "write_text",
        "write_bytes",
        "unlink",
        "rename",
        "replace",
        "mkdir",
        "rmdir",
        "connect",
        "system",
        "Popen",
    }
    for name, tree in code_trees.items():
        imported_modules = []
        call_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.append(node.module)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    call_names.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    call_names.add(node.func.attr)
        imports_valid = all(
            module.split(".")[0] in allowed_stdlib
            or module.startswith("capabilities.midplatform.core.context_foundation")
            for module in imported_modules
        )
        marker_free = all(
            not any(marker in module.lower().split(".") for marker in forbidden_import_markers)
            for module in imported_modules
        )
        check(imports_valid, f"import_boundary:{name}")
        check(marker_free, f"no_forbidden_import:{name}")
        check(not (call_names & forbidden_calls), f"no_side_effect_call:{name}")

    sys.dont_write_bytecode = True
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    try:
        from capabilities.midplatform.core.context_foundation.context_foundation_fixture_v1 import (
            get_context_foundation_fixture_cases_v1,
        )
        from capabilities.midplatform.core.context_foundation.context_foundation_protocol_v1 import (
            ContextFoundationProtocolV1,
        )
        from capabilities.midplatform.core.context_foundation.context_foundation_trace_types_v1 import (
            ContextFoundationTraceV1,
        )
        from capabilities.midplatform.core.context_foundation.context_foundation_types_v1 import (
            ContextEnvelopeCandidateV1,
        )
        from capabilities.midplatform.core.context_foundation.context_projection_types_v1 import (
            ProjectionReferenceV1,
        )
        from capabilities.midplatform.core.context_foundation.run_context_foundation_controlled_skeleton_v1 import (
            run_controlled_skeleton,
        )

        check(True, "controlled_imports")
    except (ImportError, ModuleNotFoundError, SyntaxError):
        get_context_foundation_fixture_cases_v1 = lambda: tuple()
        run_controlled_skeleton = lambda: tuple()
        ContextFoundationProtocolV1 = object
        ContextFoundationTraceV1 = object
        ContextEnvelopeCandidateV1 = object
        ProjectionReferenceV1 = object
        check(False, "controlled_imports")

    projection_fields = set(getattr(ProjectionReferenceV1, "__dataclass_fields__", {}))
    check(
        {
            "source_owner",
            "projection_id",
            "projection_version",
            "timestamp",
            "validity",
            "confidence",
            "unknown_state",
            "provenance",
        }
        <= projection_fields,
        "projection_fields",
    )
    envelope_fields = set(
        getattr(ContextEnvelopeCandidateV1, "__dataclass_fields__", {})
    )
    required_envelope_fields = {
        "context_id",
        "version",
        "temporal_scope",
        "field_projection_reference",
        "observation_projection_reference",
        "memory_projection_reference",
        "self_projection_reference",
        "role_projection_reference",
        "relationship_projection_reference",
        "emotion_projection_reference",
        "mental_field_continuity_reference",
        "provenance",
        "trace_reference",
    }
    check(required_envelope_fields <= envelope_fields, "envelope_fields")
    check(
        not envelope_fields
        & {"intent", "goal", "causal_explanation", "decision", "action"},
        "envelope_no_forbidden_fields",
    )
    protocol_methods = set(getattr(ContextFoundationProtocolV1, "__dict__", {}))
    check(
        {"validate_projection", "assemble_context", "create_trace", "get_context_snapshot"}
        <= protocol_methods,
        "protocol_methods",
    )
    trace_fields = set(getattr(ContextFoundationTraceV1, "__dataclass_fields__", {}))
    check(
        {
            "trace_id",
            "input_projection_refs",
            "assembly_steps",
            "output_context_reference",
            "timestamp",
            "status",
        }
        <= trace_fields,
        "trace_fields",
    )

    fixtures = get_context_foundation_fixture_cases_v1()
    required_case_ids = {
        "CF-01-WORK-TO-HOME",
        "CF-02-WEATHER-MINIMAL",
        "CF-03-TIRED-EXPRESSION",
        "CF-04-CHANGE-JOB",
    }
    check(len(fixtures) == 4, "fixture_count")
    check({item.case_id for item in fixtures} == required_case_ids, "fixture_ids")
    check(all(item.synthetic_only is True for item in fixtures), "fixtures_synthetic")

    try:
        results = run_controlled_skeleton()
        check(True, "controlled_runner_completed")
    except (TypeError, ValueError, AttributeError):
        results = tuple()
        check(False, "controlled_runner_completed")
    check(len(results) == 4, "controlled_result_count")
    check({item.get("case_id") for item in results} == required_case_ids, "controlled_result_ids")
    check(all(item.get("boundary_valid") is True for item in results), "controlled_boundaries")
    check(all(item.get("synthetic_only") is True for item in results), "controlled_synthetic_only")
    check(all(item.get("skeleton_only") is True for item in results), "controlled_skeleton_only")
    check(all(item.get("runtime_executed") is False for item in results), "controlled_no_runtime")
    check(all(item.get("state_mutation") is False for item in results), "controlled_no_mutation")
    check(all(item.get("database_accessed") is False for item in results), "controlled_no_database")
    check(all(item.get("model_called") is False for item in results), "controlled_no_model")

    forbidden_envelope_keys = {
        "intent",
        "goal",
        "causal_explanation",
        "decision",
        "action",
        "memory_mutation",
        "field_mutation",
    }
    check(
        all(
            not (set(item.get("context_envelope", {})) & forbidden_envelope_keys)
            for item in results
        ),
        "controlled_no_forbidden_output",
    )
    check(
        all(item.get("context_envelope", {}).get("candidate_only") is True for item in results),
        "controlled_candidate_only",
    )
    check(
        all(item.get("context_envelope", {}).get("reference_only") is True for item in results),
        "controlled_reference_only",
    )
    check(
        all(item.get("context_envelope", {}).get("runtime_executed") is False for item in results),
        "envelope_no_runtime",
    )
    check(
        all(item.get("context_envelope", {}).get("state_mutation") is False for item in results),
        "envelope_no_mutation",
    )
    check(
        all(item.get("trace", {}).get("runtime_executed") is False for item in results),
        "trace_no_runtime",
    )
    check(
        all(item.get("trace", {}).get("state_mutation_executed") is False for item in results),
        "trace_no_mutation",
    )

    result_by_id = {item.get("case_id"): item for item in results}
    carryover = result_by_id.get("CF-01-WORK-TO-HOME", {}).get(
        "context_envelope", {}
    ).get("mental_field_continuity_reference")
    check(isinstance(carryover, dict), "carryover_present")
    if isinstance(carryover, dict):
        check(carryover.get("reference_only") is True, "carryover_reference_only")
        check(carryover.get("memory_record_created") is False, "carryover_not_memory")
        check(carryover.get("emotion_calculation_executed") is False, "carryover_no_emotion_calculation")
        check(carryover.get("causal_explanation_created") is False, "carryover_no_causal")
        check(carryover.get("source_mutation_executed") is False, "carryover_no_mutation")
    weather_context = result_by_id.get("CF-02-WEATHER-MINIMAL", {}).get(
        "context_envelope", {}
    )
    check(weather_context.get("memory_projection_reference") is None, "weather_no_memory_expansion")
    check(weather_context.get("relationship_projection_reference") is None, "weather_no_relationship_expansion")
    change_job_context = result_by_id.get("CF-04-CHANGE-JOB", {}).get(
        "context_envelope", {}
    )
    check(change_job_context.get("role_projection_reference") is not None, "job_role_reference")
    check(change_job_context.get("relationship_projection_reference") is not None, "job_relationship_reference")
    check(change_job_context.get("memory_projection_reference") is not None, "job_memory_reference")
    check(change_job_context.get("emotion_projection_reference") is not None, "job_emotion_reference")
    check(change_job_context.get("intent_output_created") is False, "job_no_intent")

    print(f"CHECKS: {len(checks)}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {len(checks) - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print(f"READINESS: {REMEDIATION}")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print(f"READINESS: {READY}")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
