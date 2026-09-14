"""V0 static verifier for Luna Core Architecture Baseline v1.0.

Planning Only: checks ownership, flow, permission, dependency, duplicate, and
future-extension contracts. It does not execute Runtime, Provider, Model,
Hardware, Emotion, Social, or Action code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "canonical_module_registry_v1.json",
    "module_responsibility_matrix_v1.json",
    "module_ownership_registry_v1.json",
    "dependency_graph_v1.json",
    "information_flow_contract_v1.json",
    "permission_matrix_v1.json",
    "state_ownership_matrix_v1.json",
    "decision_authority_matrix_v1.json",
    "memory_authority_matrix_v1.json",
    "duplicate_module_resolution_v1.json",
    "future_extension_boundary_v1.json",
    "emotion_extension_boundary_v1.json",
    "provider_extension_boundary_v1.json",
)
MD_ASSETS = (
    "luna_core_architecture_baseline_v1.md",
    "architecture_freeze_whitebox_v1.md",
    "architecture_freeze_go_no_go_v1.md",
)


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

    registry = data.get("canonical_module_registry_v1.json", {})
    responsibility = data.get("module_responsibility_matrix_v1.json", {})
    ownership = data.get("module_ownership_registry_v1.json", {})
    graph = data.get("dependency_graph_v1.json", {})
    flow = data.get("information_flow_contract_v1.json", {})
    permission = data.get("permission_matrix_v1.json", {})
    state = data.get("state_ownership_matrix_v1.json", {})
    decision = data.get("decision_authority_matrix_v1.json", {})
    memory = data.get("memory_authority_matrix_v1.json", {})
    duplicate = data.get("duplicate_module_resolution_v1.json", {})
    future = data.get("future_extension_boundary_v1.json", {})
    emotion = data.get("emotion_extension_boundary_v1.json", {})
    provider = data.get("provider_extension_boundary_v1.json", {})

    modules = registry.get("modules", [])
    module_ids = [entry.get("module_id") for entry in modules]
    owners = [entry.get("owner") for entry in modules]
    check(len(modules) >= 15, "canonical_module_count")
    check(len(module_ids) == len(set(module_ids)) and all(module_ids), "canonical_module_ids_unique")
    check(all(entry.get("layer") and entry.get("owner") and entry.get("responsibility") for entry in modules), "canonical_module_fields")
    check(len(owners) == len(set(owners)) and all(owners), "canonical_module_owners_unique")
    check(registry.get("rules", {}).get("one_concept_one_owner") is True, "canonical_one_owner")
    check(registry.get("rules", {}).get("historical_assets_preserved") is True, "canonical_history_preserved")
    required_ids = {"constitution", "governance_plane", "reality_workspace", "cognitive_field", "attention_system", "cognitive_workspace", "brain", "memory_system", "learning_system", "self_evolution", "cognitive_self_model", "capability_runtime", "action_boundary", "action_runtime"}
    check(required_ids.issubset(set(module_ids)), "canonical_required_modules")

    responsibility_rows = responsibility.get("rows", [])
    check(len(responsibility_rows) >= 6, "responsibility_rows")
    check(all(row.get("responsibility") and row.get("non_responsibility") and row.get("primary_output") for row in responsibility_rows), "responsibility_completeness")
    check(responsibility.get("rules", {}).get("one_primary_responsibility") is True, "responsibility_single_primary")

    ownership_rows = ownership.get("entries", [])
    ownership_concepts = [row.get("concept") for row in ownership_rows]
    check(len(ownership_rows) >= 8, "ownership_rows")
    check(len(ownership_concepts) == len(set(ownership_concepts)) and all(ownership_concepts), "ownership_concepts_unique")
    check(all(row.get("owner") and row.get("writer") and row.get("readers") is not None for row in ownership_rows), "ownership_complete")
    check(ownership.get("rules", {}).get("single_owner_per_concept") is True, "ownership_single_owner")

    nodes = set(graph.get("nodes", []))
    edges = graph.get("edges", [])
    check(nodes == set(module_ids), "graph_nodes_match_registry")
    check(len(edges) >= 12, "graph_edges")
    check(_acyclic(nodes, edges), "dependency_acyclic")
    check(len(graph.get("feedback_edges", [])) >= 1, "feedback_edges_separate")
    forbidden_graph = set(graph.get("forbidden_edges", []))
    for item in ("Capability → Brain Override", "Model → Brain Replacement", "Provider → Reality Authority", "Emotion → Direct Action", "Learning → Value Rewrite", "Self Evolution → Identity Rewrite", "Capability → Goal Ownership"):
        check(item in forbidden_graph, f"graph_forbidden:{item}")
    check(graph.get("rules", {}).get("feedback_is_event_not_owner_cycle") is True, "graph_feedback_event")

    check(flow.get("stages") == ["Observation", "Evidence", "Context", "State", "Hypothesis / Belief", "Expectation", "Decision", "Action", "Outcome", "Learning", "Evolution"], "flow_stages")
    check(len(flow.get("links", [])) >= 9, "flow_links")
    check(all(link.get("from") and link.get("to") and link.get("object") and link.get("owner") for link in flow.get("links", [])), "flow_link_completeness")
    check(len(flow.get("reentry_links", [])) >= 2, "flow_reentry")
    check(flow.get("rules", {}).get("single_canonical_flow") is True, "flow_single_canonical")
    check(flow.get("rules", {}).get("direct_provider_to_brain_forbidden") is True, "flow_provider_brain_guard")
    check(flow.get("rules", {}).get("direct_model_to_memory_forbidden") is True, "flow_model_memory_guard")

    permission_rows = permission.get("rows", [])
    check(len(permission_rows) >= 7, "permission_rows")
    check(all(set(["read", "propose", "update", "execute", "forbidden"]).issubset(row) for row in permission_rows), "permission_complete")
    check(permission.get("rules", {}).get("execute_requires_admission") is True, "permission_admission")
    check(permission.get("rules", {}).get("read_not_write") is True, "permission_read_write")

    state_rows = state.get("rows", [])
    state_names = [row.get("state") for row in state_rows]
    state_owners = [row.get("owner") for row in state_rows]
    check(len(state_rows) >= 8, "state_rows")
    check(len(state_names) == len(set(state_names)) and all(state_names), "state_names_unique")
    check(all(row.get("owner") and row.get("writer") and row.get("readers") is not None for row in state_rows), "state_complete")
    check(state.get("rules", {}).get("single_owner") is True, "state_single_owner")
    check(len(state_owners) == len(set(state_owners)), "state_owners_unique")

    check(decision.get("decision_owner") == "Brain", "decision_owner_brain")
    decision_rows = decision.get("rows", [])
    decision_generators = [row.get("module") for row in decision_rows if row.get("can_generate_decision_candidate")]
    check(decision_generators == ["Brain"], "decision_single_generator")
    check({"Capability → Decision", "Memory → Decision", "Emotion → Decision Override", "Provider → Brain Replacement"}.issubset(set(decision.get("forbidden", []))), "decision_forbidden")
    check(decision.get("rules", {}).get("execution_separate") is True, "decision_execution_separate")

    check(memory.get("record_owner") == "Memory System", "memory_owner")
    check(len(memory.get("rows", [])) >= 5, "memory_rows")
    check({"Action → Direct Memory Write", "Model Output → Direct Memory Fact", "Provider → Memory Authority"}.issubset(set(memory.get("forbidden", []))), "memory_forbidden")
    check(memory.get("rules", {}).get("admission_required") is True, "memory_admission")

    groups = duplicate.get("groups", [])
    check(len(groups) >= 4, "duplicate_groups")
    check(all(group.get("canonical") and group.get("decision") and group.get("preserve_history") is True for group in groups), "duplicate_resolution_complete")
    check(duplicate.get("rules", {}).get("no_delete") is True, "duplicate_no_delete")
    check(duplicate.get("rules", {}).get("canonical_reference_required_for_new_assets") is True, "duplicate_canonical_reference")

    extensions = {entry.get("extension"): entry for entry in future.get("extensions", [])}
    check({"Emotion", "Social", "Provider / Model", "Hardware"}.issubset(extensions), "future_extensions")
    check(all(entry.get("entry") and entry.get("allowed") and entry.get("forbidden") for entry in extensions.values()), "future_extension_complete")
    check(future.get("rules", {}).get("admission_required") is True, "future_admission")
    check(future.get("rules", {}).get("core_owner_unchanged") is True, "future_core_owner")

    check(emotion.get("status") == "interface_only", "emotion_interface_only")
    check(emotion.get("rules", {}).get("no_emotion_runtime") is True, "emotion_no_runtime")
    check({"Emotion → Direct Action", "Emotion → Decision Override", "Emotion → Constitution", "Emotion → Value Rewrite"}.issubset(set(emotion.get("forbidden", []))), "emotion_forbidden")

    check(provider.get("entry") == "Capability Boundary", "provider_entry_boundary")
    check(provider.get("rules", {}).get("capability_first") is True, "provider_capability_first")
    check(provider.get("rules", {}).get("model_not_cognitive_owner") is True, "provider_not_cognitive_owner")
    check(provider.get("rules", {}).get("admission_required") is True, "provider_admission")
    check({"LLM → Brain Replacement", "Provider → Reality Authority", "Provider → Memory Authority", "Provider → Goal Ownership"}.issubset(set(provider.get("forbidden", []))), "provider_forbidden")

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
        print("READINESS: LUNA_CORE_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_CORE_ARCHITECTURE_BASELINE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
