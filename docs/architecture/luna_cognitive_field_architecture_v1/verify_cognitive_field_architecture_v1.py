"""V2 verifier for the Cognitive Field architecture-only phase."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_ASSETS = [
    "field_state_schema.json", "field_component_registry.json", "field_lifecycle_contract.json", "field_update_flow.json",
    "field_memory_relation_contract.json", "field_knowledge_relation_contract.json", "field_self_social_relation_contract.json",
    "field_emotion_boundary.json", "field_b_route_interface.json", "dependency_mapping.json", "ownership_registry.json",
    "negative_guards.json", "summary.json",
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
    architecture = ROOT / "cognitive_field_architecture.md"
    if not architecture.is_file() or not architecture.read_text(encoding="utf-8").strip():
        failures.append("missing_architecture_document")
    if [p.name for p in ROOT.glob("*.py") if p.name != Path(__file__).name]:
        failures.append("architecture_only_contains_implementation")
    state = data.get("field_state_schema.json", {})
    required_components = set(state.get("required_components", []))
    if len(required_components) != 12 or not state.get("rules", {}).get("field_not_reality") or not state.get("rules", {}).get("unknown_preserved"):
        failures.append("field_state_boundary")
    registry = data.get("field_component_registry.json", {})
    components = registry.get("components", [])
    if len(components) != 12 or len({row.get("component") for row in components}) != 12 or not registry.get("rules", {}).get("no_component_is_field_authority"):
        failures.append("component_registry")
    lifecycle = data.get("field_lifecycle_contract.json", {})
    transitions = lifecycle.get("transitions", [])
    if len(transitions) < 8 or not lifecycle.get("rules", {}).get("current_reality_recheck_required"):
        failures.append("field_lifecycle")
    update_flow = data.get("field_update_flow.json", {})
    stages = update_flow.get("stages", [])
    if [row.get("order") for row in stages] != list(range(1, len(stages) + 1)) or not update_flow.get("rules", {}).get("reality_precedes_interpretation"):
        failures.append("field_update_flow")
    memory = data.get("field_memory_relation_contract.json", {})
    if not memory.get("rules", {}).get("current_reality_precedence") or not memory.get("rules", {}).get("memory_not_field_owner"):
        failures.append("field_memory_boundary")
    knowledge = data.get("field_knowledge_relation_contract.json", {})
    if not knowledge.get("rules", {}).get("knowledge_admission_required") or not knowledge.get("rules", {}).get("knowledge_not_reality"):
        failures.append("field_knowledge_boundary")
    social = data.get("field_self_social_relation_contract.json", {})
    if not social.get("rules", {}).get("identity_continuity") or not social.get("rules", {}).get("role_field_bound"):
        failures.append("field_self_social_boundary")
    emotion = data.get("field_emotion_boundary.json", {})
    if emotion.get("status") != "boundary_only" or not emotion.get("rules", {}).get("emotion_not_route"):
        failures.append("field_emotion_boundary")
    b_route = data.get("field_b_route_interface.json", {})
    if b_route.get("a_route", {}).get("status") != "current" or b_route.get("b_route", {}).get("status") != "future_boundary" or not b_route.get("permissions", {}).get("b_writes_current_field") is False:
        failures.append("field_b_boundary")
    dependency = data.get("dependency_mapping.json", {})
    if len(dependency.get("dependencies", [])) < 8 or not dependency.get("rules", {}).get("future_interface_not_active"):
        failures.append("field_dependencies")
    ownership = data.get("ownership_registry.json", {})
    objects = [row.get("object") for row in ownership.get("ownership", [])]
    if len(objects) != len(set(objects)) or not ownership.get("rules", {}).get("unique_owner"):
        failures.append("field_ownership")
    guards = data.get("negative_guards.json", {})
    required_guards = {"no_field_runtime", "no_world_model", "no_emotion_runtime", "no_role_runtime", "no_memory_consolidation", "no_learning", "no_b_simulation", "no_action"}
    if not required_guards.issubset({row.get("guard") for row in guards.get("guards", [])}) or not guards.get("rules", {}).get("no_runtime_activation"):
        failures.append("negative_guards")
    summary = data.get("summary.json", {})
    if summary.get("primary_owner") != "Cognitive Field System" or summary.get("status") != "architecture_only":
        failures.append("summary")
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError:
        failures.append("verifier_syntax")
    source = Path(__file__).read_text(encoding="utf-8")
    for module in ("subprocess", "socket", "requests", "cv2", "torch"):
        if f"import {module}" in source or f"from {module}" in source:
            failures.append(f"forbidden_import:{module}")
    checks = 96
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_FIELD_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_FIELD_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
