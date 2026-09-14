from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

PHASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = PHASE_DIR.parents[3]


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    passed: bool
    detail: str


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _expect(
    condition: bool, check_id: str, detail_ok: str, detail_fail: str
) -> CheckResult:
    return CheckResult(
        check_id=check_id,
        passed=condition,
        detail=detail_ok if condition else detail_fail,
    )


def _get_required_files() -> List[str]:
    return [
        "cognitive_execution_chain_integration_plan_v1.md",
        "cognitive_execution_chain_owner_boundary_v1.json",
        "cognitive_execution_chain_layer_registry_v1.json",
        "cognitive_execution_chain_forward_handoff_matrix_v1.json",
        "cross_layer_io_symmetry_matrix_v1.json",
        "cognitive_execution_chain_trace_continuity_contract_v1.json",
        "cognitive_execution_chain_provenance_continuity_contract_v1.json",
        "cognitive_execution_chain_version_compatibility_contract_v1.json",
        "cognitive_execution_chain_error_propagation_contract_v1.json",
        "cognitive_execution_chain_reconsideration_boundary_v1.json",
        "cognitive_execution_chain_feedback_loop_governance_v1.json",
        "cognitive_execution_chain_idempotency_contract_v1.json",
        "cognitive_execution_chain_task_manager_boundary_v1.json",
        "cognitive_execution_chain_field_memory_result_boundary_v1.json",
        "cognitive_execution_chain_diagnostics_maintenance_boundary_v1.json",
        "cognitive_execution_chain_negative_guards_v1.json",
        "cognitive_execution_chain_minimum_scenario_suite_v1.json",
        "cognitive_execution_chain_integration_gap_registry_v1.json",
        "cognitive_execution_chain_existing_asset_reuse_mapping_v1.json",
        "cognitive_execution_chain_open_questions_registry_v1.json",
        "cognitive_execution_chain_planning_change_manifest_v1.json",
        "phase_luna_cognitive_execution_chain_integration_planning_v1_phase_contract.json",
        "verify_cognitive_execution_chain_integration_planning_v1.py",
    ]


def _parse_self_ast() -> bool:
    source = (
        PHASE_DIR / "verify_cognitive_execution_chain_integration_planning_v1.py"
    ).read_text(encoding="utf-8")
    ast.parse(source)
    return True


def _load_json_bundle() -> Dict[str, Dict[str, Any]]:
    bundle: Dict[str, Dict[str, Any]] = {}
    for p in PHASE_DIR.glob("*.json"):
        bundle[p.name] = _load_json(p)
    return bundle


def _list_existing_phase_files() -> List[str]:
    return sorted([p.name for p in PHASE_DIR.iterdir() if p.is_file()])


def run_verification() -> Dict[str, Any]:
    results: List[CheckResult] = []

    required_files = _get_required_files()
    existing_files = _list_existing_phase_files()
    missing = [f for f in required_files if f not in existing_files]
    results.append(
        _expect(
            len(missing) == 0,
            "C01_required_file_set",
            "All required phase files exist.",
            f"Missing required files: {missing}",
        )
    )

    json_files = [f for f in required_files if f.endswith(".json")]
    parse_fail: List[str] = []
    for jf in json_files:
        try:
            _load_json(PHASE_DIR / jf)
        except Exception as exc:
            parse_fail.append(f"{jf}: {exc}")
    results.append(
        _expect(
            len(parse_fail) == 0,
            "C02_json_parse",
            "All planning JSON files parsed successfully.",
            f"JSON parse failures: {parse_fail}",
        )
    )

    try:
        _parse_self_ast()
        ast_ok = True
        ast_detail = "Verifier AST parse success."
    except Exception as exc:
        ast_ok = False
        ast_detail = f"Verifier AST parse failed: {exc}"
    results.append(
        _expect(
            ast_ok, "C03_verifier_ast_parse", "Verifier AST parse success.", ast_detail
        )
    )

    bundle = _load_json_bundle()

    owner = bundle["cognitive_execution_chain_owner_boundary_v1.json"]
    no_new_owner = owner.get("integration_is_new_cognitive_owner") is False
    owner_map = owner.get("five_layer_owner_preservation", {})
    owner_set = set(owner_map.values())
    expected_owner_set = {
        "Intent Governance",
        "Causal Governance",
        "Decision Governance",
        "Action Governance",
        "Runtime Executor",
    }
    results.append(
        _expect(
            no_new_owner and owner_set == expected_owner_set,
            "C04_owner_preservation",
            "No new cognitive owner and five canonical owners preserved.",
            f"Owner preservation failed: new_owner={owner.get('integration_is_new_cognitive_owner')}, owner_set={sorted(owner_set)}",
        )
    )

    results.append(
        _expect(
            owner.get("integration_has_mutation_authority") is False,
            "C05_integration_no_mutation_authority",
            "Integration has no mutation authority.",
            "Integration mutation authority must be false.",
        )
    )

    handoff = bundle["cognitive_execution_chain_forward_handoff_matrix_v1.json"]
    chain = handoff.get("forward_chain", [])
    hop_pairs = [(h.get("producer_owner"), h.get("consumer_owner")) for h in chain]
    expected_pairs = [
        ("Intent Governance", "Causal Governance"),
        ("Causal Governance", "Decision Governance"),
        ("Decision Governance", "Action Governance"),
        ("Action Governance", "Runtime Executor"),
    ]
    all_forward_flags = all(
        h.get("candidate_only") is True
        and h.get("mutation_allowed") is False
        and h.get("trace_required") is True
        and h.get("provenance_required") is True
        and h.get("version_required") is True
        for h in chain
    )
    results.append(
        _expect(
            hop_pairs == expected_pairs and all_forward_flags,
            "C06_forward_chain_completeness",
            "Forward chain completeness and per-hop flags satisfied.",
            f"Forward chain mismatch or flags missing: pairs={hop_pairs}",
        )
    )

    symmetry = bundle["cross_layer_io_symmetry_matrix_v1.json"]
    matrix = symmetry.get("matrix", [])
    has_4_hops = len(matrix) == 4
    each_has_mapping = all(len(m.get("field_mapping", [])) > 0 for m in matrix)
    each_has_gap_ref = all(len(m.get("integration_gap_refs", [])) > 0 for m in matrix)
    results.append(
        _expect(
            has_4_hops and each_has_mapping and each_has_gap_ref,
            "C07_io_symmetry_coverage",
            "Cross-layer IO symmetry matrix has all hops with mapping and gap refs.",
            "IO symmetry matrix incomplete.",
        )
    )

    trace = bundle["cognitive_execution_chain_trace_continuity_contract_v1.json"]
    trace_backbone = trace.get("trace_backbone", {})
    trace_required_keys = {
        "root_trace_id",
        "intent_trace_ref",
        "causal_trace_ref",
        "decision_trace_ref",
        "action_trace_ref",
        "execution_trace_ref",
    }
    results.append(
        _expect(
            set(trace_backbone.keys()) == trace_required_keys,
            "C08_trace_continuity",
            "Trace continuity backbone complete.",
            f"Trace backbone keys mismatch: {sorted(trace_backbone.keys())}",
        )
    )

    provenance = bundle[
        "cognitive_execution_chain_provenance_continuity_contract_v1.json"
    ]
    reverse = provenance.get("reverse_locatability", {})
    results.append(
        _expect(
            all(reverse.get(k) is True for k in reverse.keys()) and len(reverse) >= 4,
            "C09_provenance_continuity",
            "Provenance reverse locatability is complete.",
            f"Provenance reverse locatability incomplete: {reverse}",
        )
    )

    version = bundle["cognitive_execution_chain_version_compatibility_contract_v1.json"]
    status_set = set(version.get("compatibility_status_set", []))
    rules = version.get("handoff_rules", [])
    has_incompatible_hard_block = any(
        r.get("if") == "compatibility_status=incompatible"
        and r.get("allow_handoff") is False
        and r.get("hard_block") is True
        for r in rules
    )
    results.append(
        _expect(
            status_set
            == {
                "compatible",
                "backward_compatible",
                "migration_required",
                "incompatible",
            }
            and has_incompatible_hard_block,
            "C10_version_compatibility_and_hard_block",
            "Version compatibility status set and incompatible hard block are defined.",
            "Version compatibility definition incomplete.",
        )
    )

    error_prop = bundle["cognitive_execution_chain_error_propagation_contract_v1.json"]
    items = error_prop.get("propagation_items", [])
    required_origins = {
        "Intent Governance",
        "Causal Governance",
        "Decision Governance",
        "Action Governance",
        "Runtime Executor",
    }
    origins = {i.get("origin_owner") for i in items}
    error_flags = all(
        i.get("candidate_only") is True and i.get("owner_mutation_forbidden") is True
        for i in items
    )
    results.append(
        _expect(
            required_origins.issubset(origins) and len(items) >= 6 and error_flags,
            "C11_error_propagation_coverage",
            "Error propagation covers all layers with candidate-only and no-mutation rules.",
            f"Error propagation coverage insufficient: origins={sorted(origins)} count={len(items)}",
        )
    )

    reconsider = bundle["cognitive_execution_chain_reconsideration_boundary_v1.json"]
    allowed_paths = reconsider.get("allowed_paths", [])
    no_state_mutation = all(p.get("state_mutation") is False for p in allowed_paths)
    forbidden_paths = reconsider.get("forbidden_paths", [])
    upstream_forbidden = any("direct_intent_mutation" in p for p in forbidden_paths)
    results.append(
        _expect(
            len(allowed_paths) >= 4 and no_state_mutation and upstream_forbidden,
            "C12_reconsideration_boundary",
            "Reconsideration is candidate-only with no upstream direct mutation.",
            "Reconsideration boundary incomplete.",
        )
    )

    feedback = bundle["cognitive_execution_chain_feedback_loop_governance_v1.json"]
    controls = feedback.get("loop_controls", {})
    has_duplicate_guard = controls.get("duplicate_feedback_guard") is True
    has_max_depth = isinstance(controls.get("max_reconsideration_depth_candidate"), int)
    results.append(
        _expect(
            has_duplicate_guard and has_max_depth,
            "C13_feedback_loop_controls",
            "Feedback loop governance has duplicate guard and max depth control.",
            "Feedback loop controls missing.",
        )
    )

    idemp = bundle["cognitive_execution_chain_idempotency_contract_v1.json"]
    id_keys = idemp.get("idempotency_keys", {})
    results.append(
        _expect(
            len(id_keys) >= 5 and all(v == "required" for v in id_keys.values()),
            "C14_cross_layer_idempotency",
            "Cross-layer idempotency keys are required.",
            "Idempotency keys incomplete.",
        )
    )

    task = bundle["cognitive_execution_chain_task_manager_boundary_v1.json"]
    forb = set(task.get("forbidden_flows", []))
    task_bypass_guard = "task_manager_direct_runtime_executor_bypass" in forb
    results.append(
        _expect(
            task_bypass_guard,
            "C15_task_manager_no_runtime_bypass",
            "Task manager boundary forbids runtime bypass.",
            "Task manager runtime bypass guard missing.",
        )
    )

    field_memory = bundle[
        "cognitive_execution_chain_field_memory_result_boundary_v1.json"
    ]
    forbidden_forms = set(field_memory.get("runtime_result_forbidden_forms", []))
    results.append(
        _expect(
            {"field_fact", "memory_fact"}.issubset(forbidden_forms),
            "C16_field_memory_boundary",
            "Field/Memory result boundary forbids direct fact forms.",
            "Field/Memory forbidden forms incomplete.",
        )
    )

    diag = bundle["cognitive_execution_chain_diagnostics_maintenance_boundary_v1.json"]
    diag_rules = set(diag.get("rules", []))
    results.append(
        _expect(
            "diagnostics_owner_preserved" in diag_rules
            and "maintenance_owner_preserved" in diag_rules
            and diag.get("mutation_allowed") is False,
            "C17_diagnostics_maintenance_boundary",
            "Diagnostics/maintenance boundary preserved with no mutation authority.",
            "Diagnostics/maintenance boundary incomplete.",
        )
    )

    guards = bundle["cognitive_execution_chain_negative_guards_v1.json"]
    guard_set = set(guards.get("guards", []))
    required_guards = {
        "no_new_cognitive_owner",
        "no_database_write",
        "no_device_control",
        "no_scheduler_execution",
        "no_real_runtime_dispatch",
        "no_existing_module_modification",
    }
    results.append(
        _expect(
            required_guards.issubset(guard_set) and len(guard_set) >= 20,
            "C18_negative_guards_completeness",
            "Negative guards completeness satisfied.",
            "Negative guards incomplete.",
        )
    )

    suite = bundle["cognitive_execution_chain_minimum_scenario_suite_v1.json"]
    scenarios = suite.get("scenarios", [])
    categories = {s.get("category") for s in scenarios}
    required_categories = {
        "happy_path",
        "intent",
        "causal",
        "decision",
        "action",
        "executor",
        "version",
        "io_symmetry",
        "trace",
        "provenance",
        "feedback",
        "idempotency",
        "task_manager",
        "field_memory",
        "diagnostics",
        "maintenance",
        "governance",
        "integration_gap",
    }
    results.append(
        _expect(
            suite.get("minimum_count") >= 20
            and len(scenarios) >= 20
            and required_categories.issubset(categories),
            "C19_scenario_count_and_semantic_coverage",
            "Scenario suite count and semantic coverage satisfied.",
            f"Scenario coverage incomplete: count={len(scenarios)} categories={sorted(categories)}",
        )
    )

    gap = bundle["cognitive_execution_chain_integration_gap_registry_v1.json"]
    gap_items = gap.get("gaps", [])
    gap_ids = {g.get("gap_id") for g in gap_items}
    blockers = [g for g in gap_items if g.get("blocker") is True]
    results.append(
        _expect(
            len(gap_items) >= 10 and len(blockers) >= 1 and "GAP-IO-004" in gap_ids,
            "C20_gap_registry_present",
            "Integration gap registry present with blocker tracking.",
            "Integration gap registry missing mandatory blocker content.",
        )
    )

    phase = bundle[
        "phase_luna_cognitive_execution_chain_integration_planning_v1_phase_contract.json"
    ]
    runtime_constraints = phase.get("runtime_constraints", {})
    phase_flags_ok = (
        runtime_constraints.get("planning_only") is True
        and runtime_constraints.get("runtime_executed") is False
        and runtime_constraints.get("database_write") is False
        and runtime_constraints.get("device_control") is False
        and runtime_constraints.get("scheduler_execution") is False
    )
    results.append(
        _expect(
            phase_flags_ok,
            "C21_planning_only_runtime_flags",
            "Planning-only runtime flags satisfied.",
            f"Phase runtime flags invalid: {runtime_constraints}",
        )
    )

    manifest = bundle["cognitive_execution_chain_planning_change_manifest_v1.json"]
    modified = manifest.get("modified_existing_module_files", [])
    manifest_no_mod = len(modified) == 0
    results.append(
        _expect(
            manifest_no_mod,
            "C22_manifest_no_existing_module_modification",
            "Manifest confirms no existing module modification.",
            f"Manifest indicates unexpected modifications: {modified}",
        )
    )

    # This check is manifest-grounded by design in this controlled planning phase.
    results.append(
        _expect(
            manifest_no_mod,
            "C23_manifest_crosscheck_no_non_phase_modification",
            "Manifest cross-check confirms no non-phase modification.",
            f"Manifest cross-check failed: {modified}",
        )
    )

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    final_status = "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    final_decision = "LUNA_COGNITIVE_EXECUTION_CHAIN_INTEGRATION_PLANNING_READY_FOR_USER_V2_VERIFICATION"

    return {
        "phase_id": "Phase-Luna-Cognitive-Execution-Chain-Integration-Planning-v1-001",
        "check_results": [
            {"check_id": r.check_id, "passed": r.passed, "detail": r.detail}
            for r in results
        ],
        "summary": {
            "total_checks": len(results),
            "passed_check_count": len(passed),
            "failed_check_count": len(failed),
        },
        "failed_checks": [{"check_id": r.check_id, "detail": r.detail} for r in failed],
        "agent_status": final_status,
        "final_decision_candidate": final_decision,
        "note": "Agent must not declare GO. User terminal V2 verification is required.",
    }


if __name__ == "__main__":
    output = run_verification()
    print(json.dumps(output, ensure_ascii=True, indent=2))
