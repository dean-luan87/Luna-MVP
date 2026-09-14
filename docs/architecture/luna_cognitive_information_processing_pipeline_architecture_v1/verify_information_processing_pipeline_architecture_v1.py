"""V2 final verifier for the A-route information-processing architecture.

The user terminal owns execution of this file. It is deliberately static: it
parses contracts and checks boundaries without importing or running runtime code.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "evidence_layer_contract.json",
    "information_structuring_schema.json",
    "cognitive_field_assembly_contract.json",
    "attention_processing_contract.json",
    "context_memory_activation_contract.json",
    "hypothesis_processing_contract.json",
    "understanding_contract.json",
    "decision_candidate_pipeline_contract.json",
    "experience_extraction_contract.json",
    "memory_consolidation_pipeline_contract.json",
    "growth_candidate_contract.json",
    "model_evidence_boundary.json",
    "pipeline_flow.json",
    "negative_guards.json",
    "ownership_registry.json",
    "summary.json",
]
MD_FILES = [
    "information_processing_pipeline_architecture.md",
    "pipeline_whitebox_v1.md",
    "pipeline_go_no_go_v1.md",
]
EXPECTED_PY = "verify_information_processing_pipeline_architecture_v1.py"


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> int:
    checks = 0
    failed: list[str] = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failed.append(label)

    files = {p.name for p in ROOT.iterdir() if p.is_file()}
    check(set(JSON_FILES) | set(MD_FILES) | {EXPECTED_PY} <= files, "required_assets")
    check(not ({p for p in files if p.endswith(".py")} - {EXPECTED_PY}), "no_unexpected_python")
    data = {name: load(name) for name in JSON_FILES}
    for name in JSON_FILES:
        check(isinstance(data[name], dict), f"json_object:{name}")
    for name in MD_FILES:
        check((ROOT / name).read_text(encoding="utf-8").strip() != "", f"markdown_nonempty:{name}")
    try:
        ast.parse((ROOT / EXPECTED_PY).read_text(encoding="utf-8"))
        check(True, "verifier_ast")
    except SyntaxError:
        check(False, "verifier_ast")

    evidence = data["evidence_layer_contract.json"]
    check(evidence["provider_stops_at_evidence"] is True, "provider_stops_at_evidence")
    check(evidence["meaning_authority"] is False, "evidence_no_meaning")
    check("evidence_candidate" in evidence["outputs"], "evidence_output")
    check("meaning" in evidence["forbidden_writes"], "evidence_forbidden_meaning")

    structuring = data["information_structuring_schema.json"]
    check(structuring["output_entities"] == ["Entity", "Event", "Relation", "State", "Change"], "structuring_entities")
    check(structuring["interpretation_authority"] is False, "structuring_no_interpretation")
    check(structuring["traceability_required"] is True, "structuring_traceability")

    field = data["cognitive_field_assembly_contract.json"]
    check("structured_information" in field["inputs"], "field_structured_input")
    check("role_context" in field["inputs"] and "self_state" in field["inputs"], "field_subject_inputs")
    check(field["field_is_current_reality_slice"] is True and field["field_is_reality"] is False, "field_boundary")
    check(field["unknown_preserved"] is True, "field_unknown")

    attention = data["attention_processing_contract.json"]
    required_dimensions = {"risk", "task_relevance", "change", "user_importance", "memory_match"}
    check(set(attention["priority_dimensions"]) == required_dimensions, "attention_dimensions")
    check(attention["decision_authority"] is False, "attention_no_decision")

    context = data["context_memory_activation_contract.json"]
    check(context["activation_trigger"] == "current_field_candidate", "field_memory_trigger")
    check(context["field_activates_memory"] is True and context["memory_not_autonomous"] is True, "memory_activation_boundary")
    check(context["current_reality_precedence"] is True, "memory_reality_precedence")

    hypothesis = data["hypothesis_processing_contract.json"]
    check(hypothesis["multiple_candidates_allowed"] is True and hypothesis["unknown_preserved"] is True, "hypothesis_multiplicity_unknown")
    check(hypothesis["evidence_required"] is True and hypothesis["automatic_resolution"] is False, "hypothesis_validation")

    understanding = data["understanding_contract.json"]
    check(understanding["is_reality"] is False and understanding["is_world_model"] is False, "understanding_not_reality")
    check(understanding["candidate_only"] is True and understanding["current_reality_precedence"] is True, "understanding_candidate")

    decision = data["decision_candidate_pipeline_contract.json"]
    check(decision["owner"] == "Brain" and decision["candidate_only"] is True, "brain_candidate_owner")
    check(decision["action_separate"] is True and decision["action_execution"] is False, "decision_action_boundary")
    check(decision["reality_write"] is False and decision["memory_write"] is False, "decision_no_mutation")

    experience = data["experience_extraction_contract.json"]
    check(experience["outcome_required"] is True and experience["not_action_log"] is True, "experience_boundary")
    check(experience["automatic_memory_write"] is False and experience["automatic_learning"] is False, "experience_no_auto")

    memory = data["memory_consolidation_pipeline_contract.json"]
    check(set(memory["stages"]) == {"value_filter", "temporal_decay", "reinforcement", "folding", "compression"}, "memory_lifecycle_stages")
    check(memory["governance_required"] is True and memory["automatic_consolidation"] is False, "memory_governance")

    growth = data["growth_candidate_contract.json"]
    check(growth["candidate_only"] is True and growth["direct_mutation"] is False, "growth_candidate_only")
    check(growth["review_required"] == ["Brain", "Constitution Governance"], "growth_review")
    check(growth["identity_write"] is False and growth["constitution_write"] is False, "growth_no_identity_constitution")

    model_boundary = data["model_evidence_boundary.json"]
    check(model_boundary["model_stops_at"] == "Evidence" and model_boundary["gateway_required"] is True, "model_evidence_stop")
    check("meaning" in model_boundary["forbidden_outputs"] and "decision" in model_boundary["forbidden_outputs"], "model_forbidden_meaning_decision")
    check(model_boundary["direct_core_access"] is False, "model_no_core_access")

    flow = data["pipeline_flow.json"]
    names = [stage["name"] for stage in flow["stages"]]
    check([stage["order"] for stage in flow["stages"]] == list(range(1, 14)), "pipeline_order_numbers")
    check(names[0] == "Reality" and names[1] == "Observation Evidence" and names[-1] == "Pattern / Growth Candidate", "pipeline_endpoints")
    check(names.index("Cognitive Field") < names.index("Attention Allocation") < names.index("Hypothesis Generation"), "pipeline_field_attention_hypothesis")
    check(names.index("Decision Candidate") < names.index("Experience Extraction") < names.index("Memory Consolidation"), "pipeline_decision_experience_memory")
    check(set(flow["rules"]) >= {"model_provider_stops_at_evidence", "field_activates_memory", "knowledge_requires_field_role_context", "decision_is_candidate", "experience_is_not_action_log", "unknown_preserved"}, "pipeline_rules")
    check(flow["execution_mode"] == "architecture_only" and flow["action_execution"] is False, "pipeline_architecture_only")

    guards = data["negative_guards.json"]
    required_guards = {"runtime_implementation", "model_or_provider_calls", "action_execution", "automatic_learning", "automatic_memory_consolidation", "b_route_simulation_runtime", "emotion_runtime", "role_runtime", "reality_mutation"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["unknown_must_be_preserved"] is True and guards["decision_must_remain_candidate"] is True, "negative_core_invariants")
    check(guards["no_check_weaken"] is True and guards["no_hardcoded_pass"] is True, "negative_verifier_guards")

    ownership = data["ownership_registry.json"]
    owners = [item["owner"] for item in ownership["objects"]]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_ownership")
    check({item["object"] for item in ownership["objects"]} >= {"Evidence", "Cognitive Field", "Attention Candidate", "Decision Candidate", "Experience Candidate", "Memory Candidate", "Growth Candidate"}, "ownership_coverage")

    summary = data["summary.json"]
    check(summary["status"] == "architecture_only", "summary_status")
    check(summary["readiness_token"] == "LUNA_COGNITIVE_INFORMATION_PROCESSING_PIPELINE_ARCHITECTURE_READY", "summary_readiness")
    check(summary["runtime_active"] is False and summary["model_integration"] is False and summary["action_execution"] is False, "summary_boundary")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers"}
    try:
        tree = ast.parse((ROOT / EXPECTED_PY).read_text(encoding="utf-8"))
        imports = {node.names[0].name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) and node.names}
        imports |= {node.module.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
        check(not (imports & forbidden_imports), "verifier_no_runtime_imports")
    except SyntaxError:
        check(False, "verifier_no_runtime_imports")

    blockers = len(failed)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {checks - blockers}")
    print(f"FAILED_CHECK_COUNT: {blockers}")
    print(f"BLOCKER_COUNT: {blockers}")
    if blockers:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_INFORMATION_PROCESSING_PIPELINE_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_INFORMATION_PROCESSING_PIPELINE_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
