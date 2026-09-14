"""V0 static verifier for Luna Cognitive Core Integration Review.

Planning Only: validates contracts and boundaries without executing Runtime,
Model, Provider, Hardware, Action, Emotion, Social, or automatic Learning.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "cognitive_core_master_flow_v1.json", "cognitive_module_integration_matrix_v1.json",
    "brain_authority_review_v1.json", "self_system_integration_mapping_v1.json",
    "learning_boundary_review_v1.json", "memory_ownership_review_v1.json",
    "capability_integration_review_v1.json", "runtime_integration_boundary_review_v1.json",
    "emotion_boundary_review_v1.json", "architecture_conflict_registry_v1.json",
)
MD_ASSETS = ("luna_cognitive_core_integration_baseline_v1.md", "core_integration_whitebox_v1.md", "core_integration_go_no_go_v1.md")


def _acyclic(nodes: set[str], edges: list[dict]) -> bool:
    graph = {node: [] for node in nodes}
    for edge in edges:
        source, target = edge.get("from"), edge.get("to")
        if source not in graph or target not in graph:
            return False
        graph[source].append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return False
        if node in visited:
            return True
        visiting.add(node)
        if not all(visit(child) for child in graph[node]):
            return False
        visiting.remove(node)
        visited.add(node)
        return True

    return all(visit(node) for node in nodes)


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, name: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(name)

    data: dict[str, dict] = {}
    for name in JSON_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_json:{name}")
        if path.is_file():
            try:
                data[name] = json.loads(path.read_text(encoding="utf-8"))
                check(True, f"json_parse:{name}")
            except (OSError, json.JSONDecodeError):
                check(False, f"json_parse:{name}")
    for name in MD_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_md:{name}")
        if path.is_file():
            check(bool(path.read_text(encoding="utf-8", errors="replace").strip()), f"nonempty_md:{name}")

    flow = data.get("cognitive_core_master_flow_v1.json", {})
    matrix = data.get("cognitive_module_integration_matrix_v1.json", {})
    brain = data.get("brain_authority_review_v1.json", {})
    self_map = data.get("self_system_integration_mapping_v1.json", {})
    learning = data.get("learning_boundary_review_v1.json", {})
    memory = data.get("memory_ownership_review_v1.json", {})
    capability = data.get("capability_integration_review_v1.json", {})
    runtime = data.get("runtime_integration_boundary_review_v1.json", {})
    emotion = data.get("emotion_boundary_review_v1.json", {})
    conflicts = data.get("architecture_conflict_registry_v1.json", {})

    expected_stages = ["Observation", "Evidence", "Field", "Context", "Workspace", "Attention", "Hypothesis", "Belief", "Expectation", "Global State", "Brain", "Decision Candidate", "Commitment", "Action Request", "Action", "Outcome", "Feedback", "Learning", "Self Evolution", "Self Regulation", "State Update"]
    check(flow.get("stages") == expected_stages, "master_flow_stages")
    links = flow.get("links", [])
    check(len(links) >= 19, "master_flow_links")
    check(all(link.get("from") and link.get("to") and link.get("object") and link.get("owner") for link in links), "master_flow_link_completeness")
    check(len(flow.get("reentry_links", [])) >= 2, "master_flow_reentry")
    check(flow.get("rules", {}).get("single_canonical_flow") is True, "master_flow_canonical")
    check(flow.get("rules", {}).get("feedback_is_event_reentry_not_owner_cycle") is True, "master_flow_feedback_boundary")
    check(flow.get("rules", {}).get("candidate_outputs_require_review") is True, "master_flow_candidate_review")
    check(flow.get("rules", {}).get("provider_to_brain_forbidden") is True, "master_flow_provider_guard")

    modules = matrix.get("modules", [])
    module_names = [row.get("module") for row in modules]
    check(len(modules) >= 12, "integration_module_count")
    check(len(module_names) == len(set(module_names)) and all(module_names), "integration_module_names_unique")
    check(all(row.get("layer") and row.get("owner") and row.get("inputs") is not None and row.get("outputs") is not None and row.get("lifecycle") for row in modules), "integration_module_completeness")
    graph = matrix.get("dependency_graph", {})
    nodes = set(graph.get("nodes", []))
    check(nodes == set(module_names), "integration_graph_nodes_match")
    check(len(graph.get("edges", [])) >= 12, "integration_graph_edges")
    check(_acyclic(nodes, graph.get("edges", [])), "integration_dependency_acyclic")
    check(len(graph.get("feedback_edges", [])) >= 1, "integration_feedback_separate")
    check(graph.get("rules", {}).get("feedback_event_not_control_cycle") is True, "integration_feedback_event")

    check(brain.get("authority_owner") == "Brain", "brain_owner")
    check(set(["Context Integration", "Situation Understanding", "Candidate Evaluation", "Decision Candidate Generation", "Decision Trace"]).issubset(set(brain.get("can", []))), "brain_can_complete")
    check(set(["Action Execution", "Capability Ownership", "Memory Direct Mutation", "Constitution Modification", "Identity Rewrite"]).issubset(set(brain.get("cannot", []))), "brain_cannot_complete")
    check(brain.get("decision_candidate_sources") == ["Brain"], "brain_single_decision_source")
    check(brain.get("rules", {}).get("execution_separate") is True, "brain_execution_separate")

    self_layers = {row.get("module"): row for row in self_map.get("layers", [])}
    check({"Self Model", "Self Regulation", "Self Evolution"}.issubset(self_layers), "self_layers_complete")
    check(self_map.get("integration_flow") == ["Self Model", "Self Regulation", "Self Evolution"], "self_integration_order")
    check(self_map.get("rules", {}).get("identity_continuity_preserved") is True, "self_identity_continuity")
    check(self_map.get("rules", {}).get("regulation_and_evolution_separate") is True, "self_regulation_evolution_separate")
    check(self_map.get("rules", {}).get("candidate_review_required") is True, "self_candidate_review")

    check(learning.get("pipeline") == ["Experience", "Pattern", "Strategy Candidate", "Learning Signal", "Candidate Update"], "learning_pipeline")
    check(learning.get("approval", {}).get("active_change_requires_review") is True, "learning_review")
    check(set(["Experience → Automatic Rule Change", "Learning → Value Rewrite"]).issubset(set(learning.get("forbidden", []))), "learning_forbidden")
    check(learning.get("rules", {}).get("candidate_only") is True, "learning_candidate_only")
    check(learning.get("rules", {}).get("no_auto_adoption") is True, "learning_no_auto_adoption")

    memory_layers = {row.get("memory"): row for row in memory.get("layers", [])}
    check(memory.get("record_owner") == "Memory System", "memory_record_owner")
    check({"Working Memory", "Long-term Memory", "Experience Memory"}.issubset(memory_layers), "memory_layers_complete")
    check(memory.get("admission_flow") == ["Observation", "Evidence", "Validation", "Memory Candidate", "Consolidation"], "memory_admission_flow")
    check(set(["Action → Direct Memory Write", "Model Output → Direct Memory Fact"]).issubset(set(memory.get("forbidden", []))), "memory_forbidden")
    check(memory.get("rules", {}).get("single_long_term_owner") is True, "memory_single_owner")
    check(memory.get("rules", {}).get("admission_required") is True, "memory_admission_required")

    check(capability.get("flow") == ["Brain", "Capability Request", "Capability Governance", "Capability Runtime", "Evidence"], "capability_flow")
    check(capability.get("owners", {}).get("admission") == "Capability Governance", "capability_admission_owner")
    check(capability.get("owners", {}).get("evidence") == "Evidence Gateway", "capability_evidence_owner")
    check(set(["Capability → Direct Brain Decision", "Provider → Direct Cognitive Core"]).issubset(set(capability.get("forbidden", []))), "capability_forbidden")
    check(capability.get("rules", {}).get("evidence_gateway_required") is True, "capability_evidence_gateway")
    check(capability.get("rules", {}).get("failure_isolation_required") is True, "capability_failure_isolation")

    check(runtime.get("status") == "interface_closed_runtime_unimplemented", "runtime_status")
    check(set(["Global State", "Self State", "Capability State"]).issubset(set(runtime.get("state", []))), "runtime_states")
    check(set(["Observation Event", "Failure Event", "Learning Event"]).issubset(set(runtime.get("events", []))), "runtime_events")
    check(set(["Decision Trace", "Action Trace", "Recovery Trace"]).issubset(set(runtime.get("traces", []))), "runtime_traces")
    check(runtime.get("rules", {}).get("runtime_not_active") is True, "runtime_not_active")
    check(runtime.get("rules", {}).get("recovery_candidate_only") is True, "runtime_recovery_candidate")

    check(emotion.get("status") == "boundary_only", "emotion_boundary_only")
    check(set(["Decision", "Action", "Value", "Identity"]).issubset(set(emotion.get("cannot", []))), "emotion_forbidden")
    check(emotion.get("rules", {}).get("no_emotion_runtime") is True, "emotion_no_runtime")
    check(emotion.get("rules", {}).get("interface_only") is True, "emotion_interface_only")

    conflict_rows = conflicts.get("conflicts", [])
    check(len(conflict_rows) >= 5, "conflict_registry_count")
    check(all(row.get("conflict_id") and row.get("category") and row.get("canonical_owner") and row.get("resolution") and row.get("status") for row in conflict_rows), "conflict_registry_complete")
    check(conflicts.get("rules", {}).get("all_conflicts_have_owner") is True, "conflict_owner_rule")
    check(conflicts.get("rules", {}).get("no_unresolved_core_conflict") is True, "conflict_resolution_rule")
    check(conflicts.get("rules", {}).get("future_extensions_not_core_blockers") is True, "conflict_future_boundary")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    check(not imports.intersection({"runtime_learning", "model_training", "emotion_runtime", "social_runtime"}), "planning_no_extension_import")
    compile(verifier_text, str(Path(__file__)), "exec")
    check(True, "planning_verifier_compile")

    passed = checks - len(failures)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {passed}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_CORE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_CORE_BASELINE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
