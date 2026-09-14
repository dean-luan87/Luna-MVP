"""V0 static verifier for the Self Regulation Boundary Amendment.

Planning Only: validates capability isolation, impact analysis, preservation,
upgrade rejection, homeostasis v2, permissions, and dependency contracts. It
does not execute Runtime, Provider, Model, Hardware, Learning, Emotion, or
Action code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "capability_isolation_contract_v1.json",
    "capability_failure_domain_schema_v1.json",
    "capability_impact_analysis_contract_v1.json",
    "self_preservation_governance_contract_v1.json",
    "upgrade_rejection_policy_v1.json",
    "capability_homeostasis_policy_v2.json",
    "self_regulation_permission_amendment_v1.json",
    "self_regulation_dependency_mapping_v1.json",
)
MD_ASSETS = (
    "self_regulation_boundary_amendment_v1.md",
    "self_regulation_boundary_whitebox_v1.md",
    "self_regulation_boundary_go_no_go_v1.md",
)


def _acyclic(nodes: set[str], edges: list[dict]) -> bool:
    graph = {node: [] for node in nodes}
    for edge in edges:
        source, target = edge.get("from"), edge.get("to")
        if source not in graph or target not in graph:
            return False
        graph[source].append(target)
    active: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in active:
            return False
        if node in visited:
            return True
        active.add(node)
        if not all(visit(child) for child in graph[node]):
            return False
        active.remove(node)
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

    isolation = data.get("capability_isolation_contract_v1.json", {})
    domain = data.get("capability_failure_domain_schema_v1.json", {})
    impact = data.get("capability_impact_analysis_contract_v1.json", {})
    preservation = data.get("self_preservation_governance_contract_v1.json", {})
    rejection = data.get("upgrade_rejection_policy_v1.json", {})
    homeostasis = data.get("capability_homeostasis_policy_v2.json", {})
    permissions = data.get("self_regulation_permission_amendment_v1.json", {})
    dependency = data.get("self_regulation_dependency_mapping_v1.json", {})

    check({"Failure Event", "Capability Registry", "Dependency Graph", "Capability Health", "Self State"}.issubset(set(isolation.get("inputs", []))), "isolation_inputs")
    check({"Capability Impact Analysis", "Affected Capability Update Candidate", "Unaffected Capability Preservation Record"}.issubset(set(isolation.get("outputs", []))), "isolation_outputs")
    check({"capability_id", "failure_domain", "affected_capabilities", "unaffected_capabilities", "degradation_policy"}.issubset(set(isolation.get("schema", []))), "isolation_schema")
    check(isolation.get("rules", {}).get("failure_domain_required") is True, "isolation_domain_required")
    check(isolation.get("rules", {}).get("unaffected_preserved") is True, "isolation_unaffected_preserved")
    check(isolation.get("rules", {}).get("system_not_collapsed_by_local_failure") is True, "isolation_system_operational")
    check(isolation.get("rules", {}).get("candidate_only") is True, "isolation_candidate_only")

    check({"capability_id", "failure_domain", "affected_capabilities", "unaffected_capabilities", "degradation_policy"}.issubset(set(domain.get("schema", []))), "domain_schema")
    examples = domain.get("examples", [])
    check(len(examples) >= 1, "domain_example")
    check(all(example.get("failure_domain") and example.get("affected_capabilities") is not None and example.get("unaffected_capabilities") is not None for example in examples), "domain_example_complete")
    check(domain.get("rules", {}).get("domain_declared_before_admission") is True, "domain_before_admission")
    check(domain.get("rules", {}).get("no_identity_impact_by_default") is True, "domain_identity_boundary")

    check(impact.get("pipeline") == ["Failure Event", "Capability Impact Analysis", "Dependency Graph Evaluation", "Affected Capability Update", "Self State Update"], "impact_pipeline")
    check({"Failure Event", "Failure Domain", "Dependency Graph", "Current Capability State", "Current Self State"}.issubset(set(impact.get("inputs", []))), "impact_inputs")
    check({"Affected Capability Update Candidate", "Unaffected Capability Confirmation", "System Operational Status Candidate"}.issubset(set(impact.get("outputs", []))), "impact_outputs")
    check(impact.get("rules", {}).get("dependency_evaluation_required") is True, "impact_dependency_required")
    check(impact.get("rules", {}).get("local_failure_isolated") is True, "impact_local_isolation")
    check(impact.get("rules", {}).get("unaffected_confirmation_required") is True, "impact_unaffected_confirmation")
    check(impact.get("rules", {}).get("no_direct_shutdown") is True, "impact_no_direct_shutdown")

    check(preservation.get("priority_order") == ["System Survival / Stability", "Core Cognitive Function", "User Task Completion", "Capability Improvement", "Performance Optimization"], "preservation_priority")
    check({"Upgrade Candidate", "Resource State", "Health State", "Risk", "Task Requirement", "Calibration Evidence"}.issubset(set(preservation.get("inputs", []))), "preservation_inputs")
    check({"Preservation Decision Candidate", "Upgrade Rejection Candidate", "Stable Operation Candidate"}.issubset(set(preservation.get("outputs", []))), "preservation_outputs")
    check(preservation.get("rules", {}).get("stability_first") is True, "preservation_stability_first")
    check(preservation.get("rules", {}).get("core_function_protected") is True, "preservation_core_function")
    check(preservation.get("rules", {}).get("optimization_not_authority") is True, "preservation_optimization_boundary")
    check(preservation.get("rules", {}).get("candidate_only") is True, "preservation_candidate_only")

    check({"Capability Value", "Resource Cost", "Risk", "Stability", "Task Requirement"}.issubset(set(rejection.get("evaluation_factors", []))), "rejection_factors")
    check({"reject", "stability_risk", "keep_current_version"}.issubset(set(rejection.get("decision_examples", [{}])[0].values())), "rejection_example")
    check({"accept_candidate", "reject_candidate", "defer_for_evidence", "keep_current_version"}.issubset(set(rejection.get("allowed_decisions", []))), "rejection_decisions")
    check(rejection.get("rules", {}).get("rejection_is_candidate") is True, "rejection_candidate")
    check(rejection.get("rules", {}).get("no_automatic_switch") is True, "rejection_no_switch")
    check(rejection.get("rules", {}).get("stability_risk_can_veto_optimization") is True, "rejection_stability_veto")
    check(rejection.get("rules", {}).get("calibration_required") is True, "rejection_calibration")

    check(homeostasis.get("evaluation_factors") == ["Capability Value", "Resource Cost", "Risk", "Stability", "Task Requirement"], "homeostasis_v2_factors")
    check({"Capability Fitness Score Candidate", "Homeostasis Candidate", "Upgrade Rejection Candidate", "Degradation Candidate"}.issubset(set(homeostasis.get("outputs", []))), "homeostasis_v2_outputs")
    check(homeostasis.get("rules", {}).get("stability_weighted") is True, "homeostasis_stability_weighted")
    check(homeostasis.get("rules", {}).get("no_max_capability_assumption") is True, "homeostasis_no_maximization")
    check(homeostasis.get("rules", {}).get("no_auto_switch") is True, "homeostasis_no_auto_switch")

    p = permissions.get("permissions", {})
    check({"Self State", "Capability Health", "Resource State", "Model Health", "Failure Evidence"}.issubset(set(p.get("observe", []))), "permissions_observe")
    check({"Failure Impact", "Dependency Blast Radius", "Capability Fitness", "Stability Risk"}.issubset(set(p.get("analyze", []))), "permissions_analyze")
    check({"Regulation Candidate", "Degradation Candidate", "Recovery Candidate", "Upgrade Rejection Candidate", "Capability Governance Request"}.issubset(set(p.get("propose", []))), "permissions_propose")
    check(p.get("execute") == [], "permissions_no_execute")
    check({"Constitution Modification", "Value Modification", "Identity Modification", "Goal Modification", "Brain Rule Modification", "Hardware Action", "Provider Invocation", "Model Switching", "Automatic Rollback", "Learning Execution"}.issubset(set(permissions.get("forbidden", []))), "permissions_forbidden")
    check(permissions.get("rules", {}).get("execute_empty") is True, "permissions_execute_empty")
    check(permissions.get("rules", {}).get("admission_externalized") is True, "permissions_admission_externalized")
    check(permissions.get("rules", {}).get("self_preservation_veto_allowed") is True, "permissions_preservation_veto")

    nodes = set(dependency.get("nodes", []))
    check({"Self Model", "Self Regulation", "Capability Isolation", "Capability Homeostasis", "Self Preservation", "Capability Governance", "Model Manager", "Calibration", "Provider", "Runtime"}.issubset(nodes), "dependency_nodes")
    check(len(dependency.get("edges", [])) >= 8, "dependency_edges")
    check(_acyclic(nodes, dependency.get("edges", [])), "dependency_acyclic")
    check({"Self Regulation → Capability Governance Ownership", "Self Regulation → Model Manager Ownership", "Self Regulation → Provider Direct Call", "Self Regulation → Hardware Action", "Self Regulation → Brain Rule Rewrite", "Self Regulation → Value Rewrite", "Self Regulation → Identity Rewrite", "Self Regulation → Goal Rewrite"}.issubset(set(dependency.get("forbidden_edges", []))), "dependency_forbidden")
    check(dependency.get("rules", {}).get("acyclic_control_graph") is True, "dependency_acyclic_rule")
    check(dependency.get("rules", {}).get("capability_governance_retains_admission") is True, "dependency_admission_owner")
    check(dependency.get("rules", {}).get("model_manager_is_option_source") is True, "dependency_model_option_source")
    check(dependency.get("rules", {}).get("runtime_read_only") is True, "dependency_runtime_read_only")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    check(not imports.intersection({"runtime_learning", "model_training", "emotion_runtime", "social_runtime", "provider_runtime"}), "planning_no_forbidden_import")
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
        print("READINESS: LUNA_COGNITIVE_SELF_REGULATION_BOUNDARY_AMENDMENT_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_SELF_REGULATION_BOUNDARY_AMENDMENT_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
