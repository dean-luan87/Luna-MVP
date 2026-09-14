#!/usr/bin/env python3
"""Final verifier for the M0 documentation-alignment phase.

This verifier is intentionally static. It validates documentation assets and
their declared boundaries; it does not import product modules, run Runtime,
or execute migration.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]

REQUIRED_MARKDOWN = [
    "dynamic_cognitive_architecture_v2_canonical_alignment.md",
    "module_responsibility_documentation_alignment.md",
    "documentation_alignment_summary.md",
]

REQUIRED_JSON = [
    "canonical_architecture_reference_registry_v2.json",
    "architecture_status_terminology_registry.json",
    "module_responsibility_alignment_registry.json",
    "documentation_reference_alignment_registry.json",
    "documentation_conflict_registry.json",
    "documentation_change_manifest.json",
    "phase_contract.json",
]

VERIFIER_NAME = "verify_controlled_architecture_alignment_m0_documentation_alignment_v1.py"
REQUIRED_FILES = REQUIRED_MARKDOWN + REQUIRED_JSON + [VERIFIER_NAME]

EXPECTED_STATUS_TERMS = {
    "ENGINEERING_BASELINE_ACTIVE",
    "ARCHITECTURE_AND_CONTROLLED_SKELETON",
    "ARCHITECTURE_VALIDATED",
    "ARCHITECTURE_ONLY",
    "PLANNING_ONLY",
    "FUTURE_BOUNDARY_ONLY",
    "FUTURE_CORE_CAPABILITY",
    "LEGACY_RUNTIME_UNALIGNED",
    "DOCUMENTATION_ALIGNMENT_CANDIDATE",
}

REQUIRED_MODULES = {
    "Field State System",
    "Observation Manager",
    "Task Manager",
    "Model Manager",
    "Memory System",
    "Personal Cognitive Network",
    "Field State Read Model",
    "Protocol Manager",
    "OCR and Vision Capabilities",
    "Self System",
    "Role System",
    "Relationship System",
    "Emotion Context",
    "Value Utility",
    "Intent Governance",
    "Causal Reasoning",
    "Experience Compression",
    "A/B Route Boundary",
    "Decision Arbitration",
    "Action Governance",
    "Root A3 Runtime",
}

REQUIRED_CONFLICTS = {
    "historical_implemented_status_ambiguity",
    "cognitive_flow_vs_migration_dependency_order",
    "brain_candidate_vs_decision_selection",
    "memory_vs_personal_cognitive_network",
    "architecture_runtime_vs_root_a3_runtime",
    "social_self_owner_label_granularity",
    "action_architecture_vs_runtime_activation",
}


class Checks:
    def __init__(self) -> None:
        self.total = 0
        self.failed: list[str] = []

    def check(self, condition: bool, name: str) -> None:
        self.total += 1
        if not condition:
            self.failed.append(name)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def joined_lower(values: list[str]) -> str:
    return " ".join(values).lower()


def main() -> int:
    checks = Checks()
    loaded: dict[str, Any] = {}

    for name in REQUIRED_FILES:
        checks.check((HERE / name).is_file(), f"required_file:{name}")

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    checks.check(actual_files == set(REQUIRED_FILES), "m0_directory_exact_file_set")
    checks.check(
        {path.name for path in HERE.glob("*.py")} == {VERIFIER_NAME},
        "verifier_only_python_file",
    )

    for name in REQUIRED_JSON:
        try:
            loaded[name] = load_json(HERE / name)
            checks.check(bool(loaded[name]), f"json_nonempty:{name}")
        except (OSError, json.JSONDecodeError):
            loaded[name] = {}
            checks.check(False, f"json_parse:{name}")

    for name in REQUIRED_MARKDOWN:
        try:
            content = (HERE / name).read_text(encoding="utf-8")
        except OSError:
            content = ""
        checks.check(len(content.strip()) > 300, f"markdown_substantial:{name}")

    try:
        ast.parse((HERE / VERIFIER_NAME).read_text(encoding="utf-8"))
        checks.check(True, "verifier_ast")
    except (OSError, SyntaxError):
        checks.check(False, "verifier_ast")

    canonical = loaded.get("canonical_architecture_reference_registry_v2.json", {})
    canonical_refs = canonical.get("references", [])
    canonical_ids = {item.get("reference_id") for item in canonical_refs}
    checks.check(
        {
            "system_architecture_baseline_v2",
            "dynamic_cognitive_architecture_v2_candidate",
            "controlled_migration_plan_v1",
            "m0_documentation_alignment_overlay",
        }.issubset(canonical_ids),
        "canonical_reference_completeness",
    )
    checks.check(len(canonical.get("interpretation_order", [])) >= 5, "canonical_interpretation_order")
    relation = canonical.get("dynamic_v2_relation", {})
    checks.check(relation.get("new_governance_layer") is False, "dynamic_v2_not_new_layer")
    checks.check(relation.get("replaces_architecture_baseline_v2") is False, "dynamic_v2_not_baseline_replacement")
    checks.check(relation.get("replaces_module_owners") is False, "dynamic_v2_not_owner_replacement")
    checks.check(relation.get("activates_runtime") is False, "dynamic_v2_no_runtime_activation")
    checks.check(canonical.get("no_dual_mainline") is True, "no_dual_mainline")
    for item in canonical_refs:
        checks.check((ROOT / item.get("path", "")).exists(), f"canonical_path:{item.get('reference_id')}")

    terminology = loaded.get("architecture_status_terminology_registry.json", {})
    terms = terminology.get("terms", [])
    term_names = {item.get("term") for item in terms}
    checks.check(term_names == EXPECTED_STATUS_TERMS, "status_term_exact_set")
    checks.check(all(item.get("definition") for item in terms), "status_definitions_complete")
    checks.check(
        all(item.get("evidence_required") for item in terms),
        "status_evidence_requirements_complete",
    )
    engineering = next((item for item in terms if item.get("term") == "ENGINEERING_BASELINE_ACTIVE"), {})
    checks.check(engineering.get("may_claim_runtime_implementation") is True, "engineering_status_claim_boundary")
    checks.check(
        all(
            item.get("may_claim_runtime_implementation") is False
            for item in terms
            if item.get("term") not in {"ENGINEERING_BASELINE_ACTIVE", "LEGACY_RUNTIME_UNALIGNED"}
        ),
        "architecture_status_no_runtime_claim",
    )
    historical = terminology.get("historical_implemented_interpretation", {})
    checks.check(historical.get("retroactive_rewrite") is False, "no_historical_rewrite")
    checks.check(terminology.get("status_inflation_forbidden") is True, "status_inflation_forbidden")
    checks.check(
        terminology.get("active_baseline_required_for_engineering_claim") is True,
        "baseline_required_for_engineering_claim",
    )

    module_registry = loaded.get("module_responsibility_alignment_registry.json", {})
    objects = module_registry.get("objects", [])
    by_module = {item.get("module"): item for item in objects}
    checks.check(REQUIRED_MODULES.issubset(by_module), "required_modules_covered")
    checks.check(len(by_module) == len(objects), "module_names_unique")
    checks.check(
        all(
            item.get("canonical_owner")
            and item.get("documentation_position")
            and item.get("responsibility")
            and item.get("not_responsible_for")
            and item.get("engineering_status") in EXPECTED_STATUS_TERMS
            and item.get("source_refs")
            and item.get("owner_preserved") is True
            for item in objects
        ),
        "module_responsibility_records_complete",
    )
    for item in objects:
        for ref in item.get("source_refs", []):
            checks.check((ROOT / ref).exists(), f"module_source_ref:{item.get('module')}:{ref}")

    checks.check(
        "user psychological understanding" in joined_lower(by_module.get("Field State System", {}).get("not_responsible_for", [])),
        "field_not_psychological_understanding",
    )
    checks.check(
        "final cognition" in joined_lower(by_module.get("Observation Manager", {}).get("not_responsible_for", [])),
        "observation_not_final_cognition",
    )
    checks.check(
        "intent generation" in joined_lower(by_module.get("Task Manager", {}).get("not_responsible_for", [])),
        "task_not_intent_generation",
    )
    checks.check(
        "cognitive subject" in joined_lower(by_module.get("Model Manager", {}).get("not_responsible_for", [])),
        "model_not_cognitive_subject",
    )
    checks.check(
        "full cognition" in joined_lower(by_module.get("Memory System", {}).get("not_responsible_for", [])),
        "memory_not_full_cognition",
    )
    pcn_forbidden = joined_lower(by_module.get("Personal Cognitive Network", {}).get("not_responsible_for", []))
    for object_name in ["self", "role", "relationship", "memory", "emotion", "value"]:
        checks.check(f"{object_name} ownership" in pcn_forbidden, f"pcn_not_owner:{object_name}")
    checks.check(module_registry.get("all_owners_preserved") is True, "all_owners_preserved")
    checks.check(module_registry.get("runtime_behavior_changed") is False, "module_registry_no_runtime_change")
    checks.check(module_registry.get("contract_or_schema_changed") is False, "module_registry_no_contract_schema_change")

    ref_registry = loaded.get("documentation_reference_alignment_registry.json", {})
    allowed_actions = set(ref_registry.get("allowed_actions", []))
    references = ref_registry.get("references", [])
    checks.check(
        allowed_actions == {"REFERENCE_AS_IS", "QUALIFY_IN_M0_OVERLAY", "PRESERVE_HISTORICAL"},
        "reference_allowed_actions",
    )
    checks.check(len(references) >= 20, "reference_inventory_coverage")
    checks.check(
        all(
            item.get("reference_id")
            and item.get("source_path")
            and item.get("canonical_term")
            and item.get("canonical_owner")
            and item.get("status_term") in EXPECTED_STATUS_TERMS
            and item.get("m0_action") in allowed_actions
            and item.get("alignment_note")
            and item.get("modified_in_m0") is False
            for item in references
        ),
        "reference_records_complete",
    )
    for item in references:
        checks.check((ROOT / item.get("source_path", "")).exists(), f"reference_path:{item.get('reference_id')}")
    checks.check(ref_registry.get("all_sources_are_read_only") is True, "reference_sources_read_only")
    checks.check(ref_registry.get("existing_source_modification_allowed") is False, "existing_source_modification_forbidden")
    checks.check(ref_registry.get("runtime_equivalence_inferred") is False, "no_runtime_equivalence_inference")
    checks.check(ref_registry.get("m1_started") is False, "reference_registry_m1_not_started")

    conflicts = loaded.get("documentation_conflict_registry.json", {})
    conflict_items = conflicts.get("conflicts", [])
    conflict_ids = {item.get("conflict_id") for item in conflict_items}
    checks.check(REQUIRED_CONFLICTS.issubset(conflict_ids), "required_documentation_conflicts")
    checks.check(
        all(item.get("status") == "resolved_by_documentation_qualification" for item in conflict_items),
        "conflicts_resolved_by_qualification",
    )
    checks.check(
        all(item.get("requires_existing_asset_edit") is False for item in conflict_items),
        "conflicts_require_no_existing_edits",
    )
    checks.check(all(item.get("blocks_m1") is False for item in conflict_items), "no_m1_blocking_documentation_conflicts")
    checks.check(conflicts.get("all_resolved") is True, "all_documentation_conflicts_resolved")
    checks.check(conflicts.get("unresolved_conflict_ids") == [], "no_unresolved_conflict_ids")
    checks.check(conflicts.get("runtime_changed") is False, "conflict_resolution_no_runtime_change")
    checks.check(conflicts.get("schema_or_contract_changed") is False, "conflict_resolution_no_schema_contract_change")

    manifest = loaded.get("documentation_change_manifest.json", {})
    checks.check(set(manifest.get("created_files", [])) == set(REQUIRED_FILES), "manifest_exact_created_files")
    for field in [
        "modified_existing_files",
        "deleted_files",
        "moved_files",
        "renamed_files",
        "code_files_changed",
        "runtime_files_changed",
        "schema_files_changed",
        "contract_files_changed",
        "active_baselines_changed",
        "historical_phase_assets_changed",
    ]:
        checks.check(manifest.get(field) == [], f"manifest_empty:{field}")
    checks.check(manifest.get("documentation_overlay_only") is True, "manifest_documentation_only")
    checks.check(manifest.get("migration_executed") is False, "manifest_no_migration")
    checks.check(manifest.get("owner_transferred") is False, "manifest_no_owner_transfer")
    checks.check(manifest.get("runtime_activated") is False, "manifest_no_runtime_activation")
    checks.check(manifest.get("m1_started") is False, "manifest_m1_not_started")

    canonical_text = (HERE / "dynamic_cognitive_architecture_v2_canonical_alignment.md").read_text(encoding="utf-8")
    responsibility_text = (HERE / "module_responsibility_documentation_alignment.md").read_text(encoding="utf-8")
    summary_text = (HERE / "documentation_alignment_summary.md").read_text(encoding="utf-8")
    combined_text = "\n".join([canonical_text, responsibility_text, summary_text]).lower()
    for phrase, name in [
        ("not a new governance layer", "markdown_dynamic_v2_not_new_layer"),
        ("migration precondition order", "markdown_migration_order_semantics"),
        ("not the runtime call graph", "markdown_not_runtime_call_graph"),
        ("user psychological understanding", "markdown_field_boundary"),
        ("final cognition", "markdown_observation_boundary"),
        ("intent generation", "markdown_task_boundary"),
        ("cognitive subject", "markdown_model_boundary"),
        ("not full cognition", "markdown_memory_boundary"),
        ("legacy_runtime_unaligned", "markdown_runtime_non_equivalence"),
        ("does not enter m1", "markdown_m1_stop_boundary"),
    ]:
        checks.check(phrase in combined_text, name)

    phase = loaded.get("phase_contract.json", {})
    checks.check(
        phase.get("Phase") == "Phase-Luna-Controlled-Architecture-Alignment-Migration-M0-Documentation-Alignment-v1-001",
        "phase_identity",
    )
    checks.check(phase.get("Execution Mode") == "Planning Only", "phase_execution_mode")
    checks.check(phase.get("Required Final Files") == REQUIRED_FILES, "phase_required_files_order")
    authority = phase.get("Verification Authority", {})
    checks.check(authority.get("V0") == "Agent", "v0_authority")
    checks.check(authority.get("V1") == "Not Authorized", "v1_authority")
    checks.check(authority.get("V2") == "User Terminal Only", "v2_authority")
    checks.check(authority.get("V3") == "ChatGPT Only", "v3_authority")
    checks.check(phase.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "agent_stop_point")
    checks.check(
        phase.get("User Terminal Commands")
        == [
            "python3 docs/architecture/luna_controlled_architecture_alignment_migration_m0_documentation_alignment_v1/verify_controlled_architecture_alignment_m0_documentation_alignment_v1.py"
        ],
        "exact_user_terminal_command",
    )
    prohibited = joined_lower(phase.get("Prohibited Agent Execution", []))
    for phrase, name in [
        ("run final phase verifier", "prohibit_agent_final_verifier"),
        ("modify code", "prohibit_code_change"),
        ("modify runtime", "prohibit_runtime_change"),
        ("modify schemas or contracts", "prohibit_schema_contract_change"),
        ("execute migration", "prohibit_migration"),
        ("enter m1", "prohibit_m1_entry"),
    ]:
        checks.check(phrase in prohibited, name)

    source = (HERE / VERIFIER_NAME).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])
    checks.check(
        imported_roots.issubset({"__future__", "ast", "json", "pathlib", "typing"}),
        "verifier_static_import_boundary",
    )

    failed = checks.failed
    passed_count = checks.total - len(failed)
    print(f"CHECKS: {checks.total}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {passed_count}")
    print(f"FAILED_CHECK_COUNT: {len(failed)}")
    print(f"BLOCKER_COUNT: {len(failed)}")
    if failed:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M0_DOCUMENTATION_ALIGNMENT_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1

    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M0_DOCUMENTATION_ALIGNMENT_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
