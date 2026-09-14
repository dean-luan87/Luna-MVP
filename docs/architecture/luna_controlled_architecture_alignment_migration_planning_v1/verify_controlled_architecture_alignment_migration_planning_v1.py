"""Final phase verifier for controlled architecture alignment migration planning.

V2 authority: User Terminal only. This verifier performs static planning checks;
it does not import Runtime modules or execute migration behavior.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
READY = "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_MIGRATION_PLAN_READY"

JSON_FILES = [
    "existing_asset_migration_inventory.json",
    "cognitive_asset_ownership_matrix.json",
    "migration_dependency_graph.json",
    "migration_risk_register.json",
    "phase_contract.json",
]
MD_FILES = [
    "controlled_migration_sequence.md",
    "migration_planning_summary.md",
]
VERIFIER = "verify_controlled_architecture_alignment_migration_planning_v1.py"


def load_json(name: str) -> dict:
    try:
        value = json.loads((ROOT / name).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def main() -> int:
    checks = 0
    failed: list[str] = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failed.append(label)

    expected_files = set(JSON_FILES) | set(MD_FILES) | {VERIFIER}
    actual_files = {path.name for path in ROOT.iterdir() if path.is_file()}
    check(expected_files <= actual_files, "required_files")
    check({path.name for path in ROOT.glob("*.py")} == {VERIFIER}, "planning_python_only")

    assets: dict[str, dict] = {}
    for name in JSON_FILES:
        value = load_json(name)
        assets[name] = value
        check(bool(value), f"json_parse:{name}")

    markdown: dict[str, str] = {}
    for name in MD_FILES:
        try:
            text = (ROOT / name).read_text(encoding="utf-8")
        except OSError:
            text = ""
        markdown[name] = text
        check(bool(text.strip()), f"markdown_nonempty:{name}")

    try:
        ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        check(True, "verifier_ast")
    except (OSError, SyntaxError):
        check(False, "verifier_ast")

    inventory = assets.get("existing_asset_migration_inventory.json", {})
    allowed_types = {
        "KEEP",
        "OWNER_ALIGNMENT_ONLY",
        "DOCUMENT_ALIGNMENT",
        "CONTRACT_ALIGNMENT",
        "FUTURE_MIGRATION",
        "BLOCKED",
    }
    check(set(inventory.get("migration_types", [])) == allowed_types, "migration_type_registry")
    check(inventory.get("scan_mode") == "baseline_first_targeted_read_only", "scan_mode")
    check(set(inventory.get("excluded_paths", [])) == {"_tmp_eval_out", "_eval_out"}, "scan_exclusions")
    check(
        set(inventory.get("scanned_roots", []))
        >= {"capabilities/", "capabilities/midplatform/core/", "docs/architecture/", "runtime/", "tools/"},
        "scan_scope",
    )

    records = inventory.get("assets", [])
    required_asset_fields = {
        "asset_name",
        "current_location",
        "current_owner",
        "new_architecture_owner",
        "migration_type",
        "migration_required",
        "reason",
        "risk_level",
        "dependency_notes",
    }
    check(len(records) >= 20, "inventory_asset_count")
    check(
        all(isinstance(item, dict) and required_asset_fields <= set(item) for item in records),
        "inventory_required_fields",
    )
    check(
        all(
            item.get("asset_name")
            and item.get("current_location")
            and item.get("current_owner")
            and item.get("new_architecture_owner")
            and item.get("reason")
            and item.get("dependency_notes")
            for item in records
        ),
        "inventory_nonempty_fields",
    )
    check(all(item.get("migration_type") in allowed_types for item in records), "inventory_migration_types")
    check(all(isinstance(item.get("migration_required"), bool) for item in records), "inventory_migration_flags")
    check(all(item.get("risk_level") in {"LOW", "MEDIUM", "HIGH", "CRITICAL"} for item in records), "inventory_risk_levels")
    check(len({item.get("asset_name") for item in records}) == len(records), "inventory_unique_assets")
    check(all((REPO_ROOT / item.get("current_location", "missing")).exists() for item in records), "inventory_locations_exist")

    required_inventory_assets = {
        "Field State Reducer",
        "Observation Manager",
        "Cognitive Attention",
        "Self System",
        "Role System",
        "Relationship System",
        "Memory System",
        "Emotion Context",
        "Value Utility",
        "Cognitive Intent Architecture",
        "Causal Reasoning",
        "Experience Compression",
        "A/B Route Boundary",
        "Decision Arbitration",
        "Task Manager",
        "Model Manager",
        "Personal Cognitive Network",
        "Protocol Manager",
        "OCR Manager",
        "Vision Manager",
    }
    check(required_inventory_assets <= {item.get("asset_name") for item in records}, "inventory_required_assets")
    check(
        inventory.get("all_assets_have_owner") is True
        and inventory.get("all_assets_have_target_owner") is True
        and inventory.get("no_unassigned_assets") is True,
        "inventory_owner_completeness",
    )
    check(
        inventory.get("personal_cognitive_network_implementation_found") is False
        and inventory.get("canonical_causal_runtime_found") is False
        and inventory.get("canonical_experience_compression_runtime_found") is False,
        "inventory_implementation_status",
    )
    check(
        inventory.get("runtime_modified") is False
        and inventory.get("migration_executed") is False
        and inventory.get("read_only") is True,
        "inventory_planning_boundary",
    )

    matrix = assets.get("cognitive_asset_ownership_matrix.json", {})
    required_objects = {
        "Field State System",
        "Personal Cognitive Network",
        "Self",
        "Role",
        "Relationship",
        "Memory",
        "Emotion",
        "Value",
        "Intent",
        "Causal Reasoning",
        "Experience Compression",
        "A/B Route",
        "Decision",
        "Task Manager",
        "Model Manager",
    }
    check(set(matrix.get("required_objects", [])) == required_objects, "ownership_required_objects")
    ownership = matrix.get("records", [])
    ownership_fields = {"object", "owner", "responsibility", "input", "output", "forbidden_responsibility"}
    check(all(ownership_fields <= set(item) for item in ownership), "ownership_required_fields")
    check(all(item.get("owner") and item.get("responsibility") for item in ownership), "ownership_nonempty")
    check(all(isinstance(item.get("input"), list) and item.get("input") for item in ownership), "ownership_inputs")
    check(all(isinstance(item.get("output"), list) and item.get("output") for item in ownership), "ownership_outputs")
    check(
        all(isinstance(item.get("forbidden_responsibility"), list) and item.get("forbidden_responsibility") for item in ownership),
        "forbidden_responsibility_present",
    )
    object_names = [item.get("object") for item in ownership]
    check(required_objects <= set(object_names), "ownership_coverage")
    check(len(object_names) == len(set(object_names)), "ownership_unique_objects")

    by_object = {item.get("object"): item for item in ownership}
    pcn = by_object.get("Personal Cognitive Network", {})
    check(
        set(pcn.get("allowed_responsibility", []))
        == {"Cross-object Connection", "Activation", "Context Projection"},
        "personal_network_allowed_scope",
    )
    check(
        {"Self", "Role", "Relationship", "Memory", "Emotion", "Value"}
        <= set(pcn.get("forbidden_responsibility", [])),
        "personal_network_forbidden_owners",
    )
    check(
        matrix.get("personal_cognitive_network", {}).get("source_owner_precedence") is True,
        "source_owner_precedence",
    )
    check(
        {"Causal Judgment", "Action Execution"}
        <= set(by_object.get("Task Manager", {}).get("forbidden_responsibility", [])),
        "task_manager_boundary",
    )
    check(
        {"Cognitive Conclusion", "Decision Authority", "Action Execution"}
        <= set(by_object.get("Model Manager", {}).get("forbidden_responsibility", [])),
        "model_manager_boundary",
    )
    check(
        {"Reality Override", "Direct Cognitive Core Mutation"}
        <= set(by_object.get("Memory", {}).get("forbidden_responsibility", [])),
        "memory_boundary",
    )
    check(
        matrix.get("runtime") is False
        and matrix.get("migration_execution") is False
        and matrix.get("candidate_only") is True,
        "ownership_planning_boundary",
    )

    graph = assets.get("migration_dependency_graph.json", {})
    primary_sequence = [
        "Field System",
        "Personal Cognitive Network",
        "Intent",
        "Causal Reasoning",
        "A/B Route",
        "Decision",
        "Task Execution",
    ]
    check(graph.get("primary_sequence") == primary_sequence, "dependency_primary_sequence")
    nodes = graph.get("nodes", [])
    check([item.get("node") for item in nodes] == primary_sequence, "dependency_nodes")
    check(all(item.get("owner") and item.get("current_status") and item.get("required_before_exit") for item in nodes), "dependency_node_fields")
    check([item.get("migration_position") for item in nodes] == list(range(7)), "dependency_positions")
    edges = graph.get("edges", [])
    expected_edges = list(zip(primary_sequence, primary_sequence[1:]))
    check([(item.get("from"), item.get("to")) for item in edges] == expected_edges, "dependency_edges")
    check(all(item.get("dependency_type") == "migration_precondition" for item in edges), "dependency_edge_type")
    check(all(item.get("reason") and item.get("failure_behavior") for item in edges), "dependency_edge_fields")
    check(
        graph.get("graph_semantics") == "migration_precondition_order_not_runtime_dataflow"
        and graph.get("field_foundation_cannot_be_bypassed") is True,
        "dependency_semantics",
    )
    check(
        graph.get("order_fixed") is True
        and graph.get("acyclic") is True
        and graph.get("runtime_dataflow_not_defined") is True
        and graph.get("migration_execution") is False,
        "dependency_boundary",
    )

    risks = assets.get("migration_risk_register.json", {})
    required_risks = {
        "双轨架构风险",
        "Owner 冲突风险",
        "Memory/Cognitive Network 混淆风险",
        "Task Manager 边界漂移风险",
        "Model Manager 权责扩大风险",
        "Field State 与 Personal Cognitive Network 混合风险",
        "文档与代码不一致风险",
    }
    risk_records = risks.get("risks", [])
    check(required_risks <= {item.get("risk") for item in risk_records}, "required_risks")
    check(
        all(
            item.get("risk_id")
            and item.get("cause")
            and item.get("impact")
            and item.get("detection")
            and item.get("mitigation")
            and item.get("stop_condition")
            and item.get("owner")
            for item in risk_records
        ),
        "risk_record_completeness",
    )
    check(all(item.get("risk_level") in {"LOW", "MEDIUM", "HIGH", "CRITICAL"} for item in risk_records), "risk_levels")
    check(
        risks.get("all_risks_have_owner") is True
        and risks.get("all_risks_have_stop_condition") is True
        and risks.get("risk_acceptance_is_not_migration_authority") is True,
        "risk_governance",
    )
    check(risks.get("runtime_modified") is False and risks.get("migration_executed") is False, "risk_planning_boundary")

    sequence_text = markdown.get("controlled_migration_sequence.md", "")
    stages = [
        "Phase M0 — Documentation Alignment",
        "Phase M1 — Schema / Contract Alignment",
        "Phase M2 — Owner Metadata Alignment",
        "Phase M3 — Runtime Boundary Alignment",
        "Phase M4 — Migration Integrity Validation",
        "Phase M5 — Architecture Freeze",
    ]
    check(all(stage in sequence_text for stage in stages), "migration_sequence_stages")
    check(sequence_text.find(stages[0]) < sequence_text.find(stages[1]) < sequence_text.find(stages[2]) < sequence_text.find(stages[3]) < sequence_text.find(stages[4]) < sequence_text.find(stages[5]), "migration_sequence_order")
    check(sequence_text.count("### Do") >= 12, "migration_sequence_do_and_do_not")
    check(sequence_text.count("### Input") == 6, "migration_sequence_inputs")
    check(sequence_text.count("### Output") == 6, "migration_sequence_outputs")
    check(sequence_text.count("### Verification") == 6, "migration_sequence_verification")
    check(sequence_text.count("### Stop condition") == 6, "migration_sequence_stop_conditions")
    check("migration_execution = false" in sequence_text and "runtime_change = false" in sequence_text, "migration_sequence_planning_boundary")

    summary_text = markdown.get("migration_planning_summary.md", "")
    summary_sections = [
        "## 1. 当前架构状态",
        "## 2. 新架构目标状态",
        "## 3. 已确认保持模块",
        "## 4. 需要调整模块",
        "## 5. 不允许发生的迁移行为",
        "## 6. 下一阶段建议",
    ]
    check(all(section in summary_text for section in summary_sections), "summary_sections")
    check("Personal Cognitive Network" in summary_text and "Runtime modified: false" in summary_text, "summary_boundaries")
    check("M0 Documentation Alignment" in summary_text and "不得直接进入" in summary_text, "summary_next_stage")

    phase = assets.get("phase_contract.json", {})
    required_phase_fields = {
        "Phase",
        "Stage",
        "Execution Mode",
        "Current Work Description",
        "Previous Phase",
        "Previous Phase Decision",
        "Input Assets",
        "Required Pre-Read",
        "Target Directory",
        "Scope",
        "Out Of Scope",
        "Required Final Files",
        "Implementation Principles",
        "Required Checks",
        "Negative Guards",
        "Verification Authority",
        "Allowed Agent Checks",
        "Allowed Agent Execution",
        "Prohibited Agent Execution",
        "Agent Stop Point",
        "User Terminal Commands",
        "Expected Success Decision",
        "Expected Next",
        "Expected Failure Decision",
        "Expected Failure Next",
        "Stop Condition",
        "Blocker Conditions",
        "Completion Report Format",
        "Current Status Contract",
    }
    check(required_phase_fields <= set(phase), "phase_required_fields")
    check(
        phase.get("Phase") == "Phase-Luna-Controlled-Architecture-Alignment-Migration-Planning-v1-001"
        and phase.get("Execution Mode") == "Planning Only",
        "phase_identity",
    )
    check(
        phase.get("Verification Authority")
        == {"V0": "Agent", "V1": "Not Authorized", "V2": "User Terminal Only", "V3": "ChatGPT Only"},
        "phase_verification_authority",
    )
    check(
        phase.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION"
        and phase.get("Current Status Contract") == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "phase_stop_point",
    )
    check(
        phase.get("User Terminal Commands")
        == ["python3 docs/architecture/luna_controlled_architecture_alignment_migration_planning_v1/verify_controlled_architecture_alignment_migration_planning_v1.py"],
        "phase_user_command",
    )
    prohibited = set(phase.get("Prohibited Agent Execution", []))
    check(
        {"run final phase verifier", "execute migration", "modify existing code", "modify Runtime", "create implementation module", "enter next phase"}
        <= prohibited,
        "phase_prohibited_execution",
    )
    guards = set(phase.get("Negative Guards", []))
    check("no-check-weaken" in guards and "no-hardcoded-pass" in guards, "phase_negative_guards")

    forbidden_imports = {
        "subprocess",
        "socket",
        "requests",
        "urllib",
        "sqlite3",
        "psycopg2",
        "cv2",
        "torch",
        "transformers",
        "runtime",
        "capabilities",
        "tools",
    }
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        check(not imports & forbidden_imports, "verifier_no_runtime_or_external_imports")
    except (OSError, SyntaxError):
        check(False, "verifier_no_runtime_or_external_imports")

    blockers = len(failed)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {checks - blockers}")
    print(f"FAILED_CHECK_COUNT: {blockers}")
    print(f"BLOCKER_COUNT: {blockers}")
    if blockers:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_MIGRATION_PLANNING_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print(f"READINESS: {READY}")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
