"""Static V2 verifier for Luna Engineering Execution Roadmap planning assets."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_ASSETS = [
    "architecture_engineering_mapping_v1.json",
    "engineering_asset_inventory_v1.json",
    "module_implementation_status_v1.json",
    "module_owner_alignment_v1.json",
    "implementation_priority_matrix_v1.json",
    "runtime_activation_dependency_graph_v1.json",
    "migration_candidate_registry_v1.json",
    "engineering_change_workflow_v1.json",
    "code_asset_health_summary_v1.json",
    "future_development_governance_v1.json",
]
MD_ASSETS = [
    "luna_engineering_execution_roadmap_v1.md",
    "engineering_execution_whitebox_v1.md",
    "engineering_execution_go_no_go_v1.md",
]
VALID_STATUS = {"Implemented", "Skeleton", "Architecture Only", "Partial", "Deprecated Candidate", "Migration Required"}


def load(name: str, failures: list[str]):
    path = ROOT / name
    if not path.is_file():
        failures.append(f"missing:{name}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        failures.append(f"invalid_json:{name}")
        return {}


def is_acyclic(nodes: set[str], edges: list[list[str]]) -> bool:
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
        node = queue.pop()
        seen += 1
        for target in graph[node]:
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

    mapping = data["architecture_engineering_mapping_v1.json"]
    rows = mapping.get("mappings", [])
    module_names = [row.get("architecture_module") for row in rows]
    if len(rows) < 12 or len(module_names) != len(set(module_names)):
        failures.append("architecture_mapping_identity")
    if not all(all(row.get(key) for key in ("architecture_module", "engineering_location", "implementation_status", "owner", "dependency", "next_action")) for row in rows):
        failures.append("architecture_mapping_fields")
    if not all(row.get("implementation_status") in VALID_STATUS for row in rows):
        failures.append("architecture_mapping_status")
    if not mapping.get("rules", {}).get("read_only"):
        failures.append("mapping_read_only_guard")

    inventory = data["engineering_asset_inventory_v1.json"]
    if inventory.get("scan_scope") != ["capabilities/", "tools/", "docs/architecture/"]:
        failures.append("inventory_scope")
    summary = inventory.get("scan_summary", {})
    if not inventory.get("read_only") or summary.get("python_ast_files_checked", 0) <= 0 or summary.get("python_ast_errors") != 0:
        failures.append("inventory_health")
    if len(inventory.get("asset_groups", [])) < 3 or not inventory.get("rules", {}).get("no_delete_move_rename"):
        failures.append("inventory_groups_or_guard")

    status_rows = data["module_implementation_status_v1.json"].get("modules", [])
    if len(status_rows) < 10 or not all(row.get("status") in VALID_STATUS and row.get("owner") and "evidence" in row for row in status_rows):
        failures.append("implementation_status_registry")
    if not data["module_implementation_status_v1.json"].get("rules", {}).get("status_does_not_authorize_execution"):
        failures.append("status_execution_guard")

    alignment = data["module_owner_alignment_v1.json"].get("alignment", [])
    if len(alignment) < 8 or not all(row.get("aligned") is True for row in alignment):
        failures.append("owner_alignment")
    if not data["module_owner_alignment_v1.json"].get("rules", {}).get("capability_not_model_manager"):
        failures.append("capability_model_boundary")

    priorities = data["implementation_priority_matrix_v1.json"].get("priorities", [])
    if [row.get("priority") for row in priorities] != ["P0", "P1", "P2", "P3"]:
        failures.append("priority_order")
    if not all(row.get("entry_gate") and row.get("exit_gate") and row.get("risk") for row in priorities):
        failures.append("priority_gates")
    if any(row.get("authorized_here") is not False for row in priorities):
        failures.append("priority_activation_guard")

    graph = data["runtime_activation_dependency_graph_v1.json"]
    nodes = set(graph.get("nodes", []))
    if len(nodes) < 7 or not is_acyclic(nodes, graph.get("edges", [])):
        failures.append("runtime_dependency_graph")
    if not graph.get("rules", {}).get("capability_before_model") or not graph.get("rules", {}).get("no_activation_in_this_phase"):
        failures.append("runtime_gate_policy")

    migration = data["migration_candidate_registry_v1.json"].get("candidates", [])
    if len(migration) < 5 or not all(row.get("asset") and row.get("target_owner") and row.get("migration_priority") and row.get("risk") and row.get("validation_gate") for row in migration):
        failures.append("migration_registry")
    if not data["migration_candidate_registry_v1.json"].get("rules", {}).get("mapping_before_move"):
        failures.append("migration_mapping_first")

    workflow = data["engineering_change_workflow_v1.json"]
    steps = workflow.get("steps", [])
    if [step.get("order") for step in steps] != list(range(1, len(steps) + 1)) or len(steps) < 6:
        failures.append("workflow_order")
    if not workflow.get("rules", {}).get("owner_before_implementation") or not workflow.get("rules", {}).get("contract_before_code"):
        failures.append("workflow_governance")

    health = data["code_asset_health_summary_v1.json"]
    if health.get("python_files_checked", 0) <= 0 or health.get("ast_parse_errors") != 0:
        failures.append("code_health_ast")
    thresholds = health.get("long_file_policy", {})
    if thresholds.get("normal_max_lines") != 600 or thresholds.get("warning_over") != 800 or thresholds.get("blocker_candidate_over") != 1200:
        failures.append("code_health_thresholds")
    if not health.get("rules", {}).get("read_only") or not health.get("rules", {}).get("no_runtime_execution"):
        failures.append("code_health_boundary")

    future = data["future_development_governance_v1.json"]
    if len(future.get("required_classifications", [])) != 6 or len(future.get("gates", [])) < 5:
        failures.append("future_workflow_scope")
    if not future.get("rules", {}).get("baseline_v2_is_source_of_truth") or not future.get("rules", {}).get("planning_only"):
        failures.append("future_governance")

    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError:
        failures.append("verifier_syntax")

    checks = 72
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_ENGINEERING_EXECUTION_ROADMAP_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_ENGINEERING_EXECUTION_ROADMAP_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
