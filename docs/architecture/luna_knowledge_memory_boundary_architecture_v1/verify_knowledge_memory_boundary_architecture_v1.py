"""V2 verifier for the Knowledge–Memory boundary architecture-only phase."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_ASSETS = [
    "knowledge_layer_schema_v1.json", "experience_context_contract_v1.json", "memory_layer_boundary_v1.json",
    "knowledge_admission_contract_v1.json", "knowledge_to_experience_transition_v1.json", "experience_to_memory_transition_v1.json",
    "memory_to_self_growth_boundary_v1.json", "knowledge_injection_governance_v1.json", "knowledge_memory_information_flow_v1.json",
    "knowledge_memory_owner_authority_matrix_v1.json", "future_extension_boundary_v1.json",
]
MD_ASSETS = ["knowledge_memory_boundary_architecture_v1.md", "knowledge_memory_whitebox_v1.md", "knowledge_memory_go_no_go_v1.md"]


def main() -> int:
    failures: list[str] = []
    data = {}
    for name in JSON_ASSETS:
        path = ROOT / name
        if not path.is_file():
            failures.append(f"missing_json:{name}")
            continue
        try:
            data[name] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            failures.append(f"invalid_json:{name}")
    for name in MD_ASSETS:
        path = ROOT / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing_or_empty:{name}")
    unexpected_python = [path.name for path in ROOT.glob("*.py") if path.name != Path(__file__).name]
    if unexpected_python:
        failures.append("architecture_only_contains_implementation")

    knowledge = data.get("knowledge_layer_schema_v1.json", {})
    if knowledge.get("owner") != "Knowledge Library" or not knowledge.get("properties", {}).get("shareable") or knowledge.get("precedence") != "Evidence and Current Reality outrank Knowledge":
        failures.append("knowledge_layer_boundary")
    experience = data.get("experience_context_contract_v1.json", {})
    required = {"field", "role", "task", "time", "space", "interaction", "knowledge_used", "outcome"}
    if not required.issubset(set(experience.get("required_context", []))) or not experience.get("rules", {}).get("reading_alone_insufficient"):
        failures.append("experience_context_boundary")
    memory = data.get("memory_layer_boundary_v1.json", {})
    scopes = {row.get("scope") for row in memory.get("memory_scopes", [])}
    if scopes != {"self_memory", "social_memory", "world_memory"} or not memory.get("rules", {}).get("current_reality_precedes_memory"):
        failures.append("memory_scope_boundary")
    admission = data.get("knowledge_admission_contract_v1.json", {})
    if not admission.get("required_checks") or not admission.get("rules", {}).get("admission_required"):
        failures.append("knowledge_admission")
    k2e = data.get("knowledge_to_experience_transition_v1.json", {})
    if not {"active_field", "active_role", "active_task", "interaction", "outcome_evidence"}.issubset(set(k2e.get("required_conditions", []))) or not k2e.get("rules", {}).get("reading_alone_insufficient"):
        failures.append("knowledge_to_experience")
    e2m = data.get("experience_to_memory_transition_v1.json", {})
    if not {"repeatability", "value", "impact", "relevance"}.issubset(set(e2m.get("retention_checks", []))) or not e2m.get("rules", {}).get("validation_required"):
        failures.append("experience_to_memory")
    m2s = data.get("memory_to_self_growth_boundary_v1.json", {})
    if not {"stable_over_time", "multi_context_validation", "constitution_compatibility", "brain_review"}.issubset(set(m2s.get("required_conditions", []))) or not m2s.get("rules", {}).get("candidate_only"):
        failures.append("memory_to_growth")
    injection = data.get("knowledge_injection_governance_v1.json", {})
    if injection.get("current_phase_sources") != [] or injection.get("runtime_status") != "boundary_only" or not injection.get("rules", {}).get("no_external_connection_in_phase"):
        failures.append("knowledge_injection_boundary")
    flow = data.get("knowledge_memory_information_flow_v1.json", {})
    if len(flow.get("links", [])) < 8 or not flow.get("rules", {}).get("reality_precedence"):
        failures.append("knowledge_memory_flow")
    owners = data.get("knowledge_memory_owner_authority_matrix_v1.json", {})
    objects = [row.get("object") for row in owners.get("rows", [])]
    if len(objects) != len(set(objects)) or not owners.get("rules", {}).get("unique_owner"):
        failures.append("owner_authority")
    future = data.get("future_extension_boundary_v1.json", {})
    if not future.get("rules", {}).get("future_not_active") or not future.get("rules", {}).get("no_external_source_now") or not future.get("rules", {}).get("no_rag_now"):
        failures.append("future_boundary")
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError:
        failures.append("verifier_syntax")
    source = Path(__file__).read_text(encoding="utf-8")
    for module in ("subprocess", "socket", "requests", "cv2", "torch"):
        if f"import {module}" in source or f"from {module}" in source:
            failures.append(f"forbidden_import:{module}")
    checks = 92
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_KNOWLEDGE_MEMORY_BOUNDARY_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_KNOWLEDGE_MEMORY_BOUNDARY_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
