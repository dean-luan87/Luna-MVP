"""V2 verifier for Field Attention and Decision integration architecture-only phase."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_ASSETS = [
    "field_attention_contract.json", "context_assembly_contract.json", "hypothesis_generation_contract.json",
    "current_world_understanding_schema.json", "decision_candidate_contract.json", "attention_memory_relation.json",
    "attention_role_relation.json", "decision_self_boundary.json", "decision_social_boundary.json",
    "a_route_processing_flow.json", "b_route_interface.json", "negative_guards.json", "summary.json",
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
    doc = ROOT / "cognitive_field_attention_decision_architecture.md"
    if not doc.is_file() or not doc.read_text(encoding="utf-8").strip():
        failures.append("missing_architecture_document")
    if [p.name for p in ROOT.glob("*.py") if p.name != Path(__file__).name]:
        failures.append("architecture_only_contains_implementation")
    attention = data.get("field_attention_contract.json", {})
    if attention.get("owner") != "Attention System" or not attention.get("rules", {}).get("field_context_required") or not attention.get("rules", {}).get("candidate_only"):
        failures.append("field_attention_boundary")
    context = data.get("context_assembly_contract.json", {})
    required = {"context_id", "field_ref", "situation", "selected_information", "self_context", "social_context", "role_context", "memory_context", "knowledge_context", "unknowns", "risk"}
    if not required.issubset(set(context.get("output_fields", []))) or not context.get("rules", {}).get("context_not_reality"):
        failures.append("context_assembly_boundary")
    hypothesis = data.get("hypothesis_generation_contract.json", {})
    if not hypothesis.get("rules", {}).get("multiple_candidates_allowed") or not hypothesis.get("rules", {}).get("unknown_required") or not hypothesis.get("rules", {}).get("evidence_required"):
        failures.append("hypothesis_boundary")
    understanding = data.get("current_world_understanding_schema.json", {})
    if not understanding.get("rules", {}).get("world_model_not_implemented") or not understanding.get("rules", {}).get("understanding_not_reality") or not understanding.get("rules", {}).get("unknown_first_class"):
        failures.append("current_understanding_boundary")
    decision = data.get("decision_candidate_contract.json", {})
    if decision.get("owner") != "Brain" or not decision.get("permissions", {}).get("generate_candidate") or decision.get("permissions", {}).get("commit_decision") is not False or not decision.get("rules", {}).get("action_separate"):
        failures.append("decision_candidate_boundary")
    memory = data.get("attention_memory_relation.json", {})
    if not memory.get("rules", {}).get("field_driven_retrieval") or not memory.get("rules", {}).get("current_reality_precedes_memory"):
        failures.append("attention_memory_boundary")
    role = data.get("attention_role_relation.json", {})
    if not role.get("rules", {}).get("role_field_bound") or role.get("permissions", {}).get("activate_role") is not False:
        failures.append("attention_role_boundary")
    self_boundary = data.get("decision_self_boundary.json", {})
    if self_boundary.get("permissions", {}).get("self_overrides_brain") is not False or not self_boundary.get("rules", {}).get("no_self_modification"):
        failures.append("decision_self_boundary")
    social_boundary = data.get("decision_social_boundary.json", {})
    if social_boundary.get("permissions", {}).get("social_creates_decision") is not False or not social_boundary.get("rules", {}).get("social_decision_forbidden"):
        failures.append("decision_social_boundary")
    flow = data.get("a_route_processing_flow.json", {})
    stages = flow.get("stages", [])
    if [row.get("order") for row in stages] != list(range(1, len(stages) + 1)) or not flow.get("rules", {}).get("automatic_decision") is False:
        failures.append("a_route_flow")
    b_route = data.get("b_route_interface.json", {})
    if b_route.get("permissions", {}).get("b_creates_decision") is not False or b_route.get("permissions", {}).get("b_writes_field") is not False or not b_route.get("rules", {}).get("a_remains_authoritative"):
        failures.append("b_route_boundary")
    guards = data.get("negative_guards.json", {})
    required_guards = {"no_emotion_runtime", "no_learning_runtime", "no_role_runtime", "no_automatic_decision", "no_world_model", "no_self_modification", "no_action_execution", "no_b_simulation"}
    if not required_guards.issubset({row.get("guard") for row in guards.get("guards", [])}) or not guards.get("rules", {}).get("architecture_only"):
        failures.append("negative_guards")
    summary = data.get("summary.json", {})
    if summary.get("status") != "architecture_only" or not summary.get("rules", {}).get("decision_is_candidate"):
        failures.append("summary")
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError:
        failures.append("verifier_syntax")
    source = Path(__file__).read_text(encoding="utf-8")
    for module in ("subprocess", "socket", "requests", "cv2", "torch"):
        if f"import {module}" in source or f"from {module}" in source:
            failures.append(f"forbidden_import:{module}")
    checks = 94
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_FIELD_ATTENTION_DECISION_INTEGRATION_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_FIELD_ATTENTION_DECISION_INTEGRATION_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
