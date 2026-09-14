# -*- coding: utf-8 -*-
"""P1 Execution DryRun Foundation — review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.p1_execution_dryrun_foundation.p1_execution_dryrun_foundation_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    verify_stages,
)
from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
    write_test_board_records,
)
from capabilities.field_understanding.p1_execution_dryrun_foundation.p1_execution_dryrun_foundation_types_v1 import (  # noqa: E402
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_ONLY,
    DRYRUN_TRUE_INVARIANTS,
    EXECUTION_GRAPH_EDGES,
    EXECUTION_GRAPH_NODES,
    EXECUTION_MODE,
    EXECUTION_STATES,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FALLBACK_CHAINS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    LUNA_CORE_PRINCIPLE,
    MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
    MODEL_INVOCATION_STEPS,
    NEGATED_CREATION_FLAGS,
    NEGATIVE_GUARDS,
    NEW_ADMISSION_CONTRACT_CREATED,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_OPTIONS_REF,
    NON_EXECUTION_FLAGS,
    P1_DOWNLOAD_LICENSE_PLANNING_REF,
    PHASE_ID,
    PLANNING_PRINCIPLE_ZH,
    RESOURCE_CONSTRAINT_PROFILES,
    REUSE_FLAGS,
    RUNTIME_SIMULATION_NODES,
    SOURCE_CHAIN,
    SYSTEM_STAGE_SNAPSHOT,
    TARGET_CHAIN_REF,
    DependencyGraph,
    DryRunExecutionResult,
    ExecutionContext,
    ExecutionTrace,
    FallbackChain,
    ModelInvocationPlan,
    P1ExecutionDryRunHandoffReadiness,
    P1ExecutionDryRunNegativeGuard,
    ResourceConstraintProfile,
    RuntimeSimulationNode,
    candidate_to_dict,
    classify_execution_state,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_execution_dryrun_foundation_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_execution_dryrun_foundation_review_v1.json"

_PKG = "capabilities/field_understanding/p1_execution_dryrun_foundation"
STEP_FILES = (
    f"{_PKG}/p1_execution_dryrun_foundation_types_v1.py",
    f"{_PKG}/p1_execution_dryrun_foundation_registry_v1.py",
    f"{_PKG}/review_p1_execution_dryrun_foundation_v1.py",
)

CONTEXT_REF = "p1_execution_dryrun_foundation_context_v1"


def _build_context() -> Dict[str, Any]:
    return candidate_to_dict(
        ExecutionContext(
            context_ref=CONTEXT_REF,
            phase_id=PHASE_ID,
            execution_mode=EXECUTION_MODE,
            dryrun_only=DRYRUN_ONLY,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_admission_contract_created=NEW_ADMISSION_CONTRACT_CREATED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            p1_download_license_planning_ref=P1_DOWNLOAD_LICENSE_PLANNING_REF,
            model_governance_integrated_closure_ref=MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            invocation_steps=MODEL_INVOCATION_STEPS,
            governance_rules=DRYRUN_GOVERNANCE_RULES,
        )
    )


def _topological_order(nodes: List[Dict[str, Any]], edges: List[Dict[str, str]]) -> tuple:
    """Kahn topological sort; returns (order_tuple, has_cycle)."""
    ids = [n["node_id"] for n in nodes]
    indeg: Dict[str, int] = {i: 0 for i in ids}
    adj: Dict[str, List[str]] = {i: [] for i in ids}
    for e in edges:
        adj[e["src"]].append(e["dst"])
        indeg[e["dst"]] += 1
    # Stable queue by declared order field.
    order_field = {n["node_id"]: n["order"] for n in nodes}
    queue = sorted([i for i in ids if indeg[i] == 0], key=lambda x: order_field[x])
    out: List[str] = []
    while queue:
        cur = queue.pop(0)
        out.append(cur)
        nxts = sorted(adj[cur], key=lambda x: order_field[x])
        for nx in nxts:
            indeg[nx] -= 1
            if indeg[nx] == 0:
                queue.append(nx)
        queue.sort(key=lambda x: order_field[x])
    has_cycle = len(out) != len(ids)
    return tuple(out), has_cycle


def review_p1_execution_dryrun_foundation_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)

    # --- Execution context (1) -------------------------------------------- #
    execution_context_count = 1

    # --- Dependency graph build + cycle detection ------------------------- #
    nodes = list(EXECUTION_GRAPH_NODES)
    edges = list(EXECUTION_GRAPH_EDGES)
    topo_order, has_cycle = _topological_order(nodes, edges)
    declared_order = tuple(
        n["node_id"] for n in sorted(nodes, key=lambda x: x["order"])
    )
    graph_build = len(topo_order) == len(nodes)
    valid_hybrid = (topo_order == declared_order) and not has_cycle
    dependency_graph = DependencyGraph(
        node_count=len(nodes),
        edge_count=len(edges),
        graph_build=graph_build,
        cycle_detection="NONE" if not has_cycle else "CYCLE_DETECTED",
        topological_order=topo_order,
        valid_linear_branching_hybrid=valid_hybrid,
    )

    # --- Runtime simulation nodes + invocation plans + traces + results --- #
    runtime_nodes: List[RuntimeSimulationNode] = []
    invocation_plans: List[ModelInvocationPlan] = []
    execution_traces: List[ExecutionTrace] = []
    dryrun_results: List[DryRunExecutionResult] = []
    state_mismatch: List[str] = []

    for spec in RUNTIME_SIMULATION_NODES:
        mid = spec["model_id"]
        runtime_nodes.append(
            RuntimeSimulationNode(
                model_id=mid,
                graph_node=spec["graph_node"],
                import_ok=spec["import_ok"],
                dep_ok=spec["dep_ok"],
                mock_signature_ok=spec["mock_signature_ok"],
                license_constrained=spec["license_constrained"],
                local_available=spec["local_available"],
                deferred=spec["deferred"],
            )
        )
        invocation_plans.append(
            ModelInvocationPlan(
                model_id=mid,
                graph_node=spec["graph_node"],
                steps=MODEL_INVOCATION_STEPS,
                executes_now=False,
            )
        )
        execution_traces.append(
            ExecutionTrace(
                model_id=mid,
                graph_node=spec["graph_node"],
                import_feasibility_check=spec["import_ok"],
                dependency_resolution_check=spec["dep_ok"],
                execution_mock_signature_check=spec["mock_signature_ok"],
                executed_real_inference=False,
            )
        )
        state = classify_execution_state(
            import_ok=spec["import_ok"],
            dep_ok=spec["dep_ok"],
            mock_signature_ok=spec["mock_signature_ok"],
            license_constrained=spec["license_constrained"],
            deferred=spec["deferred"],
            local_available=spec["local_available"],
        )
        state_match = state == spec["expected_state"]
        if not state_match:
            state_mismatch.append(f"{mid}:{state}!={spec['expected_state']}")
        dryrun_results.append(
            DryRunExecutionResult(
                model_id=mid,
                graph_node=spec["graph_node"],
                execution_state=state,
                expected_state=spec["expected_state"],
                state_match=state_match,
                executed_real_inference=False,
                downloaded_model=False,
            )
        )

    failed_checks.extend(state_mismatch)

    runtime_simulation_node_count = len(runtime_nodes)
    model_invocation_plan_count = len(invocation_plans)
    execution_trace_count = len(execution_traces)
    dryrun_execution_result_count = len(dryrun_results)
    state_match_count = sum(1 for r in dryrun_results if r.state_match)

    state_distribution: Dict[str, int] = {}
    for r in dryrun_results:
        state_distribution[r.execution_state] = state_distribution.get(r.execution_state, 0) + 1

    # --- Fallback chains -------------------------------------------------- #
    fallback_chains = [
        FallbackChain(
            trigger=f["trigger"],
            fallback_route=f["fallback_route"],
            candidate_only=True,
            verified=f["verified"],
        )
        for f in FALLBACK_CHAINS
    ]
    fallback_chain_count = len(fallback_chains)

    # --- Resource constraint profiles ------------------------------------- #
    resource_profiles = [
        ResourceConstraintProfile(
            resource=r["resource"],
            available_mock=r["available_mock"],
            required_for_backbone=r["required_for_backbone"],
        )
        for r in RESOURCE_CONSTRAINT_PROFILES
    ]
    resource_constraint_profile_count = len(resource_profiles)

    # --- Invariant state for negative guards ------------------------------ #
    nef = NON_EXECUTION_FLAGS
    inv = DRYRUN_TRUE_INVARIANTS
    invariant_state: Dict[str, bool] = {
        "real_inference_not_allowed": nef["real_inference_allowed"] is False,
        "model_download_not_allowed": (
            nef["model_download_allowed"] is False and nef["auto_download_allowed"] is False
        ),
        "runtime_execution_not_allowed": nef["runtime_execution_allowed"] is False,
        "dataset_pull_not_allowed": (
            nef["dataset_pull_allowed"] is False and nef["dataset_download_allowed"] is False
        ),
        "dependency_install_not_allowed": nef["dependency_install_allowed"] is False,
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "runtime_escalation_not_allowed": (
            nef["runtime_escalation_allowed"] is False and nef["runtime_activation_allowed"] is False
        ),
        "governance_reuse_preserved": (
            inv["governance_reuse_preserved"]
            and inv["model_output_adapter_required"]
            and inv["midplatform_data_handling_required"]
            and inv["midplatform_model_control_required"]
            and NEW_ADMISSION_CONTRACT_CREATED is False
            and NEW_RUNTIME_GOVERNANCE_CREATED is False
        ),
    }

    negative_guards: List[P1ExecutionDryRunNegativeGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = invariant_state.get(spec["depends_on"], False)
        negative_guards.append(
            P1ExecutionDryRunNegativeGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_dryrun_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --- No real-execution / download proof over all results ------------- #
    no_real_inference_proven = all(not r.executed_real_inference for r in dryrun_results)
    no_download_proven = all(not r.downloaded_model for r in dryrun_results)

    # --- Handoff readiness (recorded only) -------------------------------- #
    handoff_readiness: List[P1ExecutionDryRunHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            P1ExecutionDryRunHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    go_conditions = {
        "execution_context_count_eq_1": execution_context_count == 1,
        "execution_graph_node_count_eq_5": len(nodes) == 5,
        "execution_graph_edge_count_eq_4": len(edges) == 4,
        "runtime_simulation_node_count_gte_8": runtime_simulation_node_count >= 8,
        "model_invocation_plan_count_eq_node_count": model_invocation_plan_count == runtime_simulation_node_count,
        "execution_trace_count_eq_node_count": execution_trace_count == runtime_simulation_node_count,
        "dryrun_result_count_eq_node_count": dryrun_execution_result_count == runtime_simulation_node_count,
        "all_states_match_expected": state_match_count == dryrun_execution_result_count,
        "execution_state_count_eq_4": len(EXECUTION_STATES) == 4,
        "fallback_chain_count_gte_4": fallback_chain_count >= 4,
        "resource_constraint_profile_count_gte_4": resource_constraint_profile_count >= 4,
        "graph_build_true": dependency_graph.graph_build is True,
        "cycle_detection_none": dependency_graph.cycle_detection == "NONE",
        "valid_linear_branching_hybrid": dependency_graph.valid_linear_branching_hybrid is True,
        "no_real_inference_proven": no_real_inference_proven,
        "no_download_proven": no_download_proven,
        "negative_guard_count_eq_8": negative_guard_count == 8,
        "negative_guard_passed_eq_8": negative_guard_passed == 8,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS.items()},
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": (
            verify_flags.get("controlled_trial_template_ref_ok") is True
        ),
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_admission_contract_created_false": NEW_ADMISSION_CONTRACT_CREATED is False,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        **{k: (v is True) for k, v in DRYRUN_TRUE_INVARIANTS.items()},
        **negative_guard_go,
        **handoff_go,
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Execution DryRun Foundation Review",
        "lifecycle_variant": "p1_execution_dryrun_foundation",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "execution_mode": EXECUTION_MODE,
        "dryrun_only": DRYRUN_ONLY,
        "p1_download_license_planning_ref": P1_DOWNLOAD_LICENSE_PLANNING_REF,
        "model_governance_integrated_closure_ref": MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "reuse_flags": dict(REUSE_FLAGS),
        "negated_creation_flags": dict(NEGATED_CREATION_FLAGS),
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES) + list(TEST_BOARD_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "execution_context": _build_context(),
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs) + 1,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "execution_states": [dict(s) for s in EXECUTION_STATES],
        "execution_graph_nodes": [dict(n) for n in EXECUTION_GRAPH_NODES],
        "execution_graph_edges": [dict(e) for e in EXECUTION_GRAPH_EDGES],
        "dependency_graph": asdict(dependency_graph),
        "runtime_simulation_nodes": [asdict(n) for n in runtime_nodes],
        "runtime_simulation_node_count": runtime_simulation_node_count,
        "model_invocation_plans": [asdict(p) for p in invocation_plans],
        "model_invocation_plan_count": model_invocation_plan_count,
        "execution_traces": [asdict(t) for t in execution_traces],
        "execution_trace_count": execution_trace_count,
        "dryrun_execution_results": [asdict(r) for r in dryrun_results],
        "dryrun_execution_result_count": dryrun_execution_result_count,
        "state_match_count": state_match_count,
        "state_distribution": state_distribution,
        "state_mismatch": state_mismatch,
        "fallback_chains": [asdict(f) for f in fallback_chains],
        "fallback_chain_count": fallback_chain_count,
        "resource_constraint_profiles": [asdict(r) for r in resource_profiles],
        "resource_constraint_profile_count": resource_constraint_profile_count,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "system_stage_snapshot": [dict(s) for s in SYSTEM_STAGE_SNAPSHOT],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "p1_execution_dryrun_foundation_status": (
                "execution_simulation_layer_established_structure_level_only"
                if review_ok
                else "blocked"
            ),
            "next_step_options_ref": NEXT_STEP_OPTIONS_REF,
            "transition_note": (
                "P1 runnable assets are placed into an abstract execution simulation layer for the first "
                "time. Each model maps to a RuntimeSimulationNode that runs only import-feasibility, "
                "dependency-resolution (mock) and execution-mock-signature checks, classified into "
                "STATE_A runnable / STATE_B partial / STATE_C blocked / STATE_D deferred. The dependency "
                "graph (segmentation -> tracking -> detection -> depth -> scene_relation) builds with no "
                "cycles and a valid linear+branching hybrid path. Fallback chains (YOLO->OpenCV, "
                "VLM->disabled) are candidate-only. This is structure-level run verification: no real "
                "inference, no model download, no runtime execution, no dataset pull, no dependency "
                "install; all outputs still pass adapter + midplatform and stay candidate-only; governance "
                "is reused with no bypass. Next: Phase-P1-Execution-Trace-Streaming-DryRun-v1-001 "
                "(continuous execution-trace / temporal candidate evolution / cross-frame consistency / "
                "midplatform stream governance) — still a dry-run."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        result["test_board_manifest"] = write_test_board_records(
            result,
            test_mode="dry_run",
            repo_root=board_root,
            source_review_file=result.get("output_review_file"),
        )

    return result


def main() -> int:
    result = review_p1_execution_dryrun_foundation_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_manifest", {}).get("written_record_count"),
                "runtime_simulation_node_count": result["runtime_simulation_node_count"],
                "state_match_count": result["state_match_count"],
                "state_distribution": result["state_distribution"],
                "graph_build": result["dependency_graph"]["graph_build"],
                "cycle_detection": result["dependency_graph"]["cycle_detection"],
                "fallback_chain_count": result["fallback_chain_count"],
                "negative_guard_passed": result["negative_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
