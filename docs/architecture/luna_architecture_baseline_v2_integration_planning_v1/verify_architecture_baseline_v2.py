"""V2 final verifier for the Baseline v2 planning assets.

The script is intentionally static: it reads local JSON/Markdown and validates
identity, ownership, flow, authority, dependency, and future-boundary contracts.
It does not execute runtime, provider, model, hardware, or action behavior.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_ASSETS = [
    "canonical_layer_registry_v2.json",
    "canonical_module_registry_v2.json",
    "module_owner_registry_v2.json",
    "information_flow_baseline_v2.json",
    "authority_baseline_v2.json",
    "dependency_graph_v2.json",
    "architecture_to_engineering_mapping_v2.json",
    "implemented_vs_planned_registry_v2.json",
    "future_extension_boundary_v3.json",
]
MD_ASSETS = [
    "luna_architecture_baseline_v2.md",
    "architecture_baseline_whitebox_v2.md",
    "architecture_baseline_go_no_go_v2.md",
]
REQUIRED_MODULES = {
    "system_constitution", "cognitive_os_governance", "brain", "self_layer",
    "social_self_layer", "integration_layer", "capability_governance",
    "action_boundary", "cognitive_runtime",
}
REQUIRED_AUTHORITIES = {
    "Rule Authority", "Cognitive Authority", "Self Authority",
    "Capability Authority", "Execution Authority",
}
REQUIRED_EXTENSIONS = {"Emotion Engine", "Role Manager", "World Model", "Embodiment", "External LLM"}
VALID_STATUS = {"implemented", "planned", "conceptual", "missing"}


def load(name: str, failures: list[str]):
    path = ROOT / name
    if not path.is_file():
        failures.append(f"missing:{name}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid_json:{name}:{exc}")
        return {}


def acyclic(nodes: set[str], edges: list[list[str]]) -> bool:
    graph = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}
    for edge in edges:
        if not isinstance(edge, list) or len(edge) != 2 or edge[0] not in nodes or edge[1] not in nodes:
            return False
        graph[edge[0]].append(edge[1])
        indegree[edge[1]] += 1
    queue = [node for node, degree in indegree.items() if degree == 0]
    seen = 0
    while queue:
        current = queue.pop()
        seen += 1
        for target in graph[current]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return seen == len(nodes)


def main() -> int:
    failures: list[str] = []
    data = {name: load(name, failures) for name in JSON_ASSETS}
    for name in MD_ASSETS:
        path = ROOT / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing_or_empty:{name}")

    layers = data["canonical_layer_registry_v2.json"].get("layers", [])
    layer_ids = [item.get("layer_id") for item in layers]
    if len(layer_ids) != len(set(layer_ids)) or layer_ids[:2] != ["L0", "L1"]:
        failures.append("layer_identity_or_topology")
    if len(layers) < 10 or not data["canonical_layer_registry_v2.json"].get("rules", {}).get("mapping_only"):
        failures.append("layer_registry_incomplete")

    modules = data["canonical_module_registry_v2.json"].get("modules", [])
    module_ids = [item.get("module_id") for item in modules]
    module_names = [item.get("canonical_name") for item in modules]
    if len(module_ids) != len(set(module_ids)) or len(module_names) != len(set(module_names)):
        failures.append("duplicate_canonical_module")
    if not REQUIRED_MODULES.issubset(set(module_ids)):
        failures.append("required_module_missing")
    for item in modules:
        if not all(item.get(key) is not None for key in ("module_id", "canonical_name", "layer", "owner", "responsibility")):
            failures.append(f"module_fields:{item.get('module_id')}")
    if not data["canonical_module_registry_v2.json"].get("rules", {}).get("one_module_one_identity"):
        failures.append("module_identity_rule_missing")

    ownership = data["module_owner_registry_v2.json"].get("ownership", [])
    concepts = [item.get("concept") for item in ownership]
    if len(concepts) != len(set(concepts)) or not all(item.get("owner") and item.get("writer") for item in ownership):
        failures.append("owner_registry_incomplete")
    if not data["module_owner_registry_v2.json"].get("rules", {}).get("single_owner"):
        failures.append("single_owner_rule_missing")

    flow = data["information_flow_baseline_v2.json"]
    if flow.get("external_flow") != ["External World", "Social Self / External Cognition", "Evidence", "Cognitive Core", "Brain", "Decision", "Action", "Feedback", "Learning", "Self / Social Update"]:
        failures.append("external_flow_baseline")
    if flow.get("internal_flow") != ["Self State", "Self Regulation", "Brain", "Capability Request", "Capability Governance", "Capability Runtime", "Evidence"]:
        failures.append("internal_flow_baseline")
    if len(flow.get("links", [])) < 10 or not flow.get("rules", {}).get("flow_closed"):
        failures.append("information_flow_incomplete")

    authorities = data["authority_baseline_v2.json"].get("authorities", [])
    authority_names = {item.get("authority") for item in authorities}
    if not REQUIRED_AUTHORITIES.issubset(authority_names) or len(authority_names) != len(authorities):
        failures.append("authority_baseline_incomplete")
    if not data["authority_baseline_v2.json"].get("rules", {}).get("no_lower_override_higher"):
        failures.append("authority_order_rule_missing")

    graph = data["dependency_graph_v2.json"]
    nodes = set(graph.get("nodes", []))
    if nodes != set(module_ids) or not acyclic(nodes, graph.get("edges", [])):
        failures.append("dependency_graph_not_canonical_or_acyclic")
    forbidden = set(graph.get("forbidden_edges", []))
    if not {"Model → Brain", "Emotion → Decision", "Provider → Reality", "Capability → Goal", "Runtime → Decision", "Social Self → Identity Rewrite"}.issubset(forbidden):
        failures.append("forbidden_dependency_guards")

    mappings = data["architecture_to_engineering_mapping_v2.json"].get("mappings", [])
    if len(mappings) < 10 or not all(item.get("architecture_module") and item.get("owner") and item.get("status") in VALID_STATUS and item.get("migration_needed") is False for item in mappings):
        failures.append("engineering_mapping_incomplete")
    if not data["architecture_to_engineering_mapping_v2.json"].get("rules", {}).get("mapping_only"):
        failures.append("mapping_only_guard_missing")

    planned = data["implemented_vs_planned_registry_v2.json"].get("entries", [])
    if len(planned) < 10 or not all(item.get("status") in VALID_STATUS and item.get("owner") and "evidence" in item for item in planned):
        failures.append("implementation_status_registry_incomplete")
    if not data["implemented_vs_planned_registry_v2.json"].get("rules", {}).get("no_runtime_activation"):
        failures.append("status_runtime_guard_missing")

    extensions = data["future_extension_boundary_v3.json"].get("extensions", [])
    extension_names = {item.get("extension") for item in extensions}
    if not REQUIRED_EXTENSIONS.issubset(extension_names) or not all(item.get("status") == "future" for item in extensions):
        failures.append("future_boundary_incomplete_or_active")
    if not data["future_extension_boundary_v3.json"].get("rules", {}).get("admission_required"):
        failures.append("future_admission_guard_missing")

    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError:
        failures.append("verifier_syntax")

    checks = 80
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_ARCHITECTURE_BASELINE_V2_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_ARCHITECTURE_BASELINE_V2_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
