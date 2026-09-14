"""Static V0 verifier for Luna architecture hierarchy consolidation.

The phase is Planning Only. This verifier parses registries and contracts and
does not import or activate Runtime, Model, Hardware, Provider, or Action code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
REQUIRED_JSON = (
    "luna_layer_definition_v1.json",
    "luna_module_inventory_v2.json",
    "luna_module_ownership_matrix_v1.json",
    "luna_dependency_boundary_v1.json",
    "luna_module_migration_map_v1.json",
    "luna_governance_tree_v1.json",
    "luna_architecture_canonical_registry_v1.json",
    "luna_core_vs_capability_boundary_v1.json",
)
REQUIRED_MD = (
    "luna_architecture_hierarchy_v1.md",
    "luna_architecture_consolidation_strategy_v1.md",
    "luna_architecture_consolidation_go_no_go_v1.md",
)


def _check(condition: bool, name: str, failures: list[str]) -> None:
    if not condition:
        failures.append(name)


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, name: str) -> None:
        nonlocal checks
        checks += 1
        _check(condition, name, failures)

    payloads: dict[str, object] = {}
    for name in REQUIRED_JSON:
        path = BASE / name
        check(path.is_file(), f"missing_json:{name}")
        if path.is_file():
            try:
                payloads[name] = json.loads(path.read_text(encoding="utf-8"))
                check(True, f"json_parse:{name}")
            except (OSError, json.JSONDecodeError):
                check(False, f"json_parse:{name}")

    for name in REQUIRED_MD:
        path = BASE / name
        check(path.is_file(), f"missing_md:{name}")
        if path.is_file():
            check(bool(path.read_text(encoding="utf-8", errors="replace").strip()), f"nonempty_md:{name}")

    layers = payloads.get("luna_layer_definition_v1.json", {})
    inventory = payloads.get("luna_module_inventory_v2.json", {})
    ownership = payloads.get("luna_module_ownership_matrix_v1.json", {})
    boundary = payloads.get("luna_dependency_boundary_v1.json", {})
    migration = payloads.get("luna_module_migration_map_v1.json", {})
    tree = payloads.get("luna_governance_tree_v1.json", {})
    canonical = payloads.get("luna_architecture_canonical_registry_v1.json", {})
    core_boundary = payloads.get("luna_core_vs_capability_boundary_v1.json", {})

    layer_rows = layers.get("layers", [])
    layer_ids = [row.get("id") for row in layer_rows]
    check(layer_ids == ["L0", "L1", "L2", "L3", "L4"], "five_layer_order")
    check(len({row.get("owner") for row in layer_rows}) == 5, "unique_layer_owners")
    check(layers.get("rules", {}).get("exactly_five_layers") is True, "layer_count_rule")

    modules = inventory.get("modules", [])
    module_names = [row.get("module") for row in modules]
    check(bool(modules), "module_inventory_nonempty")
    check(len(module_names) == len(set(module_names)), "module_ids_unique")
    check(all(row.get("layer") in {"L0", "L1", "L2", "L3", "L4"} for row in modules), "module_layers_valid")
    check(all(row.get("owner") and row.get("responsibility") for row in modules), "module_owner_responsibility_complete")
    check(inventory.get("rules", {}).get("module_has_one_layer") is True, "module_single_layer_rule")
    check(inventory.get("rules", {}).get("module_has_one_owner") is True, "module_single_owner_rule")

    records = ownership.get("records", [])
    record_names = [row.get("module") for row in records]
    check(len(record_names) == len(set(record_names)), "ownership_record_ids_unique")
    check(set(record_names).issubset(set(module_names)), "ownership_records_registered")
    defaults = ownership.get("layer_defaults", {})
    check(set(defaults) == {"L0", "L1", "L2", "L3", "L4"}, "ownership_layer_defaults")
    check(all(row.get("layer") in defaults for row in modules), "ownership_all_modules_have_default")
    check(all(row.get("allowed_dependency") is not None and row.get("forbidden_dependency") is not None for row in records), "ownership_boundary_fields")
    check(ownership.get("rules", {}).get("one_owner_per_module") is True, "ownership_single_owner_rule")

    allowed = boundary.get("allowed", [])
    forbidden = boundary.get("forbidden", [])
    forbidden_text = json.dumps(forbidden, ensure_ascii=False)
    check(len(allowed) >= 6, "dependency_allowed_edges")
    check(len(forbidden) >= 6, "dependency_forbidden_edges")
    for source, target in (("Capability Provider", "Brain"), ("Model", "Decision"), ("Hardware", "Goal"), ("Provider", "Reality"), ("Emotion", "Reality"), ("Learning", "Constitution")):
        check(source in forbidden_text and target in forbidden_text, f"dependency_guard:{source}->{target}")
    check(boundary.get("rules", {}).get("evidence_gateway_required") is True, "evidence_gateway_rule")
    check(boundary.get("rules", {}).get("candidate_not_authority") is True, "candidate_authority_rule")

    entries = canonical.get("entries", [])
    canonical_ids = [row.get("canonical") for row in entries]
    aliases = [alias for row in entries for alias in row.get("aliases", [])]
    check(len(canonical_ids) == len(set(canonical_ids)), "canonical_ids_unique")
    check(not set(canonical_ids).intersection(aliases), "canonical_alias_disjoint")
    check(all(row.get("status") in {"active", "alias", "deprecated", "historical"} for row in entries), "canonical_status_values")
    check(canonical.get("rules", {}).get("no_delete") is True, "canonical_no_delete_rule")

    migration_entries = migration.get("entries", [])
    check(bool(migration_entries), "migration_map_nonempty")
    check(all(row.get("execution") == "not executed" for row in migration_entries), "migration_not_executed")
    check(all(row.get("action") in set(migration.get("actions", [])) for row in migration_entries), "migration_actions_registered")
    check(migration.get("rules", {}).get("no_delete") is True, "migration_no_delete_rule")

    check(tree.get("root", {}).get("children") == ["L0", "L1", "L2", "L3", "L4"], "governance_tree_layers")
    check(tree.get("tree_rules", {}).get("single_owner") is True, "governance_tree_owner_rule")
    check(tree.get("tree_rules", {}).get("boundary_only_l3") is True, "governance_tree_l3_boundary")

    core = core_boundary.get("core", {})
    capability = core_boundary.get("capability", {})
    check(core.get("layer") == "L2", "core_boundary_layer")
    check(capability.get("layer") == "L4", "capability_boundary_layer")
    check("Brain control" in capability.get("cannot", []), "capability_cannot_brain")
    check("Provider execution" in core.get("cannot", []), "core_cannot_provider")
    check(len(core_boundary.get("bridges", [])) == 3, "core_capability_bridge_count")

    # Static boundary check: no prohibited runtime imports in this planning verifier.
    verifier_text = Path(__file__).read_text(encoding="utf-8")
    tree_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports = set()
    for node in ast.walk(tree_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_verifier_no_runtime_import")
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
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_ARCHITECTURE_HIERARCHY_CONSOLIDATION_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
