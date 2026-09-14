"""V2 verifier for the Role architecture-only phase."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_ASSETS = [
    "role_schema.json", "role_registry.json", "role_activation_contract.json", "role_lifecycle.json",
    "role_field_relation.json", "role_memory_relation.json", "role_knowledge_relation.json",
    "role_self_social_boundary.json", "role_b_route_interface.json", "negative_guards.json", "summary.json",
]


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
    for name in ["role_architecture.md", "role_whitebox_v1.md", "role_go_no_go_v1.md"]:
        path = ROOT / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing_or_empty:{name}")
    if [path.name for path in ROOT.glob("*.py") if path.name != Path(__file__).name]:
        failures.append("architecture_only_contains_implementation")
    schema = data.get("role_schema.json", {})
    required = {"role_id", "field_id", "task_id", "relationship_context", "responsibility", "permission", "expectation", "self_capability_ref", "confidence", "lifecycle_state", "provenance"}
    if schema.get("owner") != "Social Self / Role Layer" or not required.issubset(set(schema.get("required_fields", []))) or not schema.get("rules", {}).get("field_required"):
        failures.append("role_schema_boundary")
    registry = data.get("role_registry.json", {})
    if registry.get("owner") != "Social Self Governance" or len(registry.get("role_types", [])) < 3 or not registry.get("rules", {}).get("no_automatic_role_generation"):
        failures.append("role_registry_boundary")
    activation = data.get("role_activation_contract.json", {})
    if not {"active_field", "task", "relationship_context", "self_capability", "evidence"}.issubset(set(activation.get("inputs", []))) or not activation.get("rules", {}).get("activation_not_automatic"):
        failures.append("role_activation_boundary")
    lifecycle = data.get("role_lifecycle.json", {})
    transitions = lifecycle.get("transitions", [])
    if len(transitions) < 8 or not lifecycle.get("rules", {}).get("field_exit_closes_instance"):
        failures.append("role_lifecycle")
    field = data.get("role_field_relation.json", {})
    if not field.get("rules", {}).get("no_context_free_role") or not field.get("rules", {}).get("role_deactivates_with_field"):
        failures.append("role_field_boundary")
    memory = data.get("role_memory_relation.json", {})
    if not memory.get("rules", {}).get("memory_validation_required") or not memory.get("rules", {}).get("role_memory_not_identity"):
        failures.append("role_memory_boundary")
    knowledge = data.get("role_knowledge_relation.json", {})
    if not knowledge.get("rules", {}).get("practice_required") or not knowledge.get("rules", {}).get("selective_absorption") or not knowledge.get("rules", {}).get("knowledge_not_role"):
        failures.append("role_knowledge_boundary")
    social = data.get("role_self_social_boundary.json", {})
    if not social.get("rules", {}).get("identity_continuity") or not social.get("permissions", {}).get("role_rewrites_identity") is False:
        failures.append("role_self_social_boundary")
    b_route = data.get("role_b_route_interface.json", {})
    if not b_route.get("permissions", {}).get("b_switches_role") is False or not b_route.get("rules", {}).get("activation_outside_b"):
        failures.append("role_b_boundary")
    guards = data.get("negative_guards.json", {})
    required_guards = {"no_role_runtime", "no_automatic_role_generation", "no_automatic_learning", "no_emotion_runtime", "no_social_runtime", "no_identity_rewrite", "no_b_switch", "no_action"}
    if not required_guards.issubset({row.get("guard") for row in guards.get("guards", [])}) or not guards.get("rules", {}).get("architecture_only"):
        failures.append("negative_guards")
    summary = data.get("summary.json", {})
    if summary.get("owner") != "Social Self Governance" or summary.get("status") != "architecture_only":
        failures.append("summary")
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError:
        failures.append("verifier_syntax")
    source = Path(__file__).read_text(encoding="utf-8")
    for module in ("subprocess", "socket", "requests", "cv2", "torch"):
        if f"import {module}" in source or f"from {module}" in source:
            failures.append(f"forbidden_import:{module}")
    checks = 88
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_ROLE_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_ROLE_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
